---
title: "gopy contextvars"
description: "PEP 567 contextvars. Ports cpython/Python/context.c plus _contextvars.c. Uses the HAMT (1662) as backing store."
tags: ["gopy", "spec"]
weight: 1663
---

# 1663. Context, ContextVar, Token

## What we are porting

| C source                | Lines | Go target                  |
|-------------------------|-------|----------------------------|
| `Python/context.c`      |  1359 | `contextvar/context.go`    |
| `Python/_contextvars.c` |    68 | `contextvar/module.go`     |

`_contextvars.c` is the thin module-init wrapper that exposes the
three classes (`Context`, `ContextVar`, `Token`) under the
`_contextvars` import name. `context.c` is the full implementation,
including the HAMT-backed mapping, the per-thread context stack, and
`Context.run()` semantics.

## What contextvars is

PEP 567 gives you per-task implicit state with snapshot-and-restore
semantics. `cv.get()` reads, `cv.set(x)` returns a `Token` you pass to
`cv.reset(token)` to undo. `Context.run(callable, *args)` enters the
context for the duration of the call and pops it on return, even if
the call raises.

asyncio uses contextvars for the implicit "current task" and for any
state libraries want to scope to a task without thread-local hacks.

## Per-thread context stack

Each `state.Thread` holds a pointer to the current `*Context`. PyEval
saves and restores it across `Context.run` calls. The chain forms a
stack:

```
Thread.current_ctx  ->  Context_inner (entered by ctx.run)
                          .prev    ->  Context_outer
                                          .prev -> nil
```

Entering pushes; leaving pops. `Context.copy()` clones the HAMT but
not the prev pointer. `Context.run` raises RuntimeError if the same
context is entered twice (CPython's `entered` flag).

## Go shape

```go
package contextvar

type Context struct {
    objects.Header
    vars     *hamt.Hamt
    prev     *Context  // for ctx.run() unwind
    entered  bool
}

type ContextVar struct {
    objects.Header
    name        string
    defaultVal  objects.Object   // nil means "no default"
    cachedTSID  uint64           // matches CPython tsid cache
    cachedVer   uint64
    cachedVal   objects.Object
}

type Token struct {
    objects.Header
    ctx     *Context
    cv      *ContextVar
    oldVal  objects.Object  // sentinel MISSING for "was not set"
    used    bool
}

// Public API.
func NewContext() *Context
func (c *Context) Copy() *Context
func (c *Context) Run(ts *state.Thread, fn objects.Object, args ...objects.Object) (objects.Object, error)
func (c *Context) Get(cv *ContextVar) (val objects.Object, found bool, err error)

func NewContextVar(name string, defaultVal objects.Object) *ContextVar
func (cv *ContextVar) Get(ts *state.Thread) (objects.Object, error)
func (cv *ContextVar) Set(ts *state.Thread, val objects.Object) (*Token, error)
func (cv *ContextVar) Reset(ts *state.Thread, tok *Token) error

// Token sentinels.
var Missing objects.Object  // _PyContextTokenMissing_Type singleton
```

## state.Thread integration

`state.Thread` gains a `Context *contextvar.Context` field, plus
`SetContext` / `GetContext` getters. `_PyContext_Enter` and
`_PyContext_Exit` from `context.c` map to methods on the Thread.

The thread-state ID + version cache that `ContextVar_Get` keeps in
CPython is preserved for performance: each `ContextVar` caches the
last `(thread_id, ctx_version)` plus the value it found. v0.9 ships
this cache because `cv.get()` is hot in any asyncio program.

`ctx.version` increments on every `set` / `reset` and is checked
against the cache.

## Error parity

* `cv.get()` with no default and no value: `LookupError(cv)`.
* `cv.reset(token)` where the token is from a different context:
  `ValueError("Token was created in a different Context")`.
* Reusing a token: `RuntimeError("Token has already been used")`.
* `Context.run(...)` re-entry: `RuntimeError("cannot enter context: <ctx> is already entered")`.

Strings are pinned verbatim from `context.c`.

## Module surface

`_contextvars` exports:

* `Context()` -> empty Context.
* `ContextVar(name, *, default=...)` -> a ContextVar.
* `Token` is exposed as a class but instances come from
  `ContextVar.set` only.
* `copy_context()` -> snapshot of the running thread's context.

The stdlib `contextvars.py` re-exports these. v0.9 wires the module
through `imp/sysmodules.go`'s frozen-module / built-in module table.

## Gate

`contextvar/context_test.go`:

* `cv.set(1); cv.get() == 1`.
* `cv.set(1); tok = cv.set(2); cv.reset(tok); cv.get() == 1`.
* `Context.copy().run(lambda: cv.set(99))` does not affect the
  outer context.
* `cv.get()` with no default and not set raises `LookupError`.
* `Context.run` recursion raises RuntimeError on re-entry.
* `copy_context()` snapshots are independent.
* Multi-goroutine: each goroutine gets its own thread and its own
  context stack; setting in one does not bleed into another.

End-to-end: a small asyncio-shaped goroutine pump (no asyncio yet,
just goroutines + a pretend event loop) verifies that
`Context.run(coro)` keeps state per goroutine.

## Out of scope

* asyncio integration. asyncio is a stdlib module that ships in a
  later phase; v0.9 only needs contextvars to *exist* so when asyncio
  arrives nothing changes here.
* `_PyContext_NewHamtForTests` (CPython test-capi exports).
* Free-threaded specialisation. The CPython version uses a per-thread
  HAMT cache; we ship it for parity but free-thread correctness lands
  with v0.14.

## v0.9 checklist

### Files

* [x] `contextvar/context.go` and `contextvar.go` and `token.go` and
  `types.go`: types and methods. Shipped in commit `1a443d2`.
* [x] `contextvar/module.go`: built-in module registration plus the
  three constructors. Wires `tp_call` on `ContextType` /
  `ContextVarType` / `TokenType`, builds the module dict
  (`Context`, `ContextVar`, `Token`, `copy_context`), and registers
  via `imp.AppendInittab("_contextvars", buildModule)` in init().
  `copy_context()` short-circuits with RuntimeError pending the
  `_PyThreadState_GET` accessor; callers use `CopyCurrent(ts)`
  directly today.
* [x] `contextvar/missing.go`: the `_PyContextTokenMissing_Type`
  singleton.
* [x] cache: per-ContextVar tsid-and-version cache embedded in
  `ContextVar` struct (cachedTSID/cachedVer/cachedVal/cachedValid)
  rather than a separate cache.go file. Matches CPython
  `contextvar->var_cached_tsid` semantics.
* [x] `state/state.go`: `id`, `ctx any`, `ctxVersion` fields plus
  `Context()` / `SetContext()` / `ContextVersion()` accessors. (Stored
  as `any` to avoid an `imp/contextvar` import cycle.)
* [x] inittab registration: handled inline by `contextvar`'s
  package init() rather than a static row in
  `imp/sysmodules.go`, matching how Go-implemented built-in
  modules will register going forward (`AppendInittab` is
  reentrant and safe from init()).
* [x] `contextvar/context_test.go`: 12-test gate panel covering
  set/get/reset, isolation, LookupError, token reuse, re-entry,
  multi-goroutine.

### Surface guarantees

* [x] `cv.get()` is O(log32 N) via HAMT path-walk.
* [x] `Token.used` flag matches CPython.
* [x] All four CPython error strings reproduced verbatim.
* [x] `Context.run` exception propagation pops the context before
  re-raising (use `defer`).
