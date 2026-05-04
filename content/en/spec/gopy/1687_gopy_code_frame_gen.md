---
title: "gopy code, frame, generator"
description: "Port of cpython/Objects/codeobject.c, frameobject.c, genobject.c, and cellobject.c. The four objects the VM thinks in: bytecode, execution frame, generator state machine, and closure cells."
tags: ["gopy", "spec"]
weight: 1687
---

# 1687. Code, frame, generator, cell

## What we are porting

Four files, ~6000 lines. The objects that exist because there is a
bytecode interpreter:

* `Objects/codeobject.c`: `code` object. Bytecode, consts,
  names, varnames, freevars, cellvars, line/exception tables,
  co_flags, co_qualname, co_name, co_filename, co_firstlineno.
  PEP 626 / 657 tables.
* `Objects/frameobject.c`: `frame` object. The runtime activation
  record. f_back, f_code, f_locals, f_globals, f_builtins,
  f_lasti, f_lineno, f_trace, f_trace_lines, f_trace_opcodes.
  The PEP 558 fast-locals proxy.
* `Objects/genobject.c`: `generator`, `coroutine`, `async_generator`
  state machines. `send`, `throw`, `close`, `__await__`,
  `__aiter__`, `__anext__`.
* `Objects/cellobject.c`: `cell`. One slot, one ref. Used by the
  closure of a function for free variables.

## Phasing

* v0.5: code object scaffold (already used by `compile.Compile`).
* v0.5.5: code object port to `objects/code.go` proper.
* v0.6: frame, generator, coroutine, async generator, cell.
  Lands together because the VM (1620 hot path) needs all four
  to run a real program.

## Go shape

```go
// Code mirrors PyCodeObject.
type Code struct {
    VarHeader
    Argcount         int
    PosOnlyArgcount  int
    KwOnlyArgcount   int
    Stacksize        int
    Flags            uint32
    Code             []byte    // bytecode
    Consts           *Tuple
    Names            *Tuple    // *Str
    Localsplus       []localKind  // flat 3.11+ layout
    Localsplusnames  *Tuple
    Filename         *Str
    Name             *Str
    Qualname         *Str
    Firstlineno      int
    Linetable        []byte    // PEP 626
    Exceptiontable   []byte    // PEP 657
    Version          uint32    // bumped on specialization
}

// Frame mirrors PyFrameObject. Allocated per call.
type Frame struct {
    Header
    Back     *Frame
    Code     *Code
    Builtins *Dict
    Globals  *Dict
    Locals   *Dict      // lazy; promotion via PEP 558
    Lasti    int        // -1 before first dispatch
    Lineno   int
    Trace    Object     // tracing callback or None
    Stack    []Object   // value stack
    StackTop int
    Localsplus []Object // flat fast / cell / free layout
    Stop     bool       // set on return / raise
}

// Generator mirrors PyGenObject (and Coroutine, AsyncGenerator).
type Generator struct {
    Header
    Frame    *Frame    // suspended frame
    Code     *Code
    Name     *Str
    Qualname *Str
    State    GenState  // CREATED, RUNNING, SUSPENDED, CLOSED
    Closing  bool
    Origin   int       // for coroutines: tracked via sys.set_coroutine_origin_tracking_depth
}

// Cell mirrors PyCellObject.
type Cell struct {
    Header
    Ref Object   // may be nil (unbound)
}
```

## PEP 558 fast-locals proxy

`frame.f_locals` does NOT directly mutate fast locals. Instead it
returns a snapshot dict; writes through the proxy update the dict,
which is then folded back into fast locals at controlled points
(trace function call, exception handling). 3.13+ semantics. Port
the proxy from `frameobject.c:PyFrame_GetLocals`.

## Generator close semantics

`gen.close()` throws GeneratorExit into the suspended frame. If the
generator catches it and yields again, RuntimeError. If
GeneratorExit is suppressed in `finally`, run finalisation.
Mirrors `gen_close_iter` exactly.

## Async generator athrow / aclose

`async_generator.aclose()` returns a coroutine that, when awaited,
performs the close. `athrow` is similar. The state machine in
`genobject.c:async_gen_athrow_send` lands here.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/codeobject.c`                  | `objects/code.go`                        |
| linetable / exceptiontable readers      | `objects/code_tables.go`                 |
| `Objects/frameobject.c`                 | `objects/frame.go`                       |
| f_locals proxy (PEP 558)                | `objects/frame_locals.go`                |
| `Objects/genobject.c` generator         | `objects/gen.go`                         |
| coroutine                               | `objects/coroutine.go`                   |
| async_generator                         | `objects/async_gen.go`                   |
| `Objects/cellobject.c`                  | `objects/cell.go`                        |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files (code, v0.5.5)

* [x] `compile/code.go`: scaffold used by `compile.Compile` (v0.5).
* [ ] `objects/code.go`: full Code struct, replace_fields builders
  (`replace`), repr, hash (over the bytecode + consts + names +
  filename + name + firstlineno tuple).
* [ ] `objects/code_tables.go`: `co_lines()`, `co_positions()`,
  exception-table walker.
* [ ] `objects/code_test.go`: linetable round-trip, exception
  table round-trip, hash stability, replace().

### Files (frame, v0.6)

* [ ] `objects/frame.go`: Frame struct, allocation, reset,
  `f_back` walk.
* [ ] `objects/frame_locals.go`: PEP 558 proxy, fold-back at
  trace entry / exception, fast/cell/free dispatch.
* [ ] `objects/frame_test.go`: f_locals visibility panel,
  f_lineno follows linetable.

### Files (generator / coroutine / async-gen, v0.6)

* [ ] `objects/gen.go`: Generator, send, throw, close, iter,
  iter_next, GeneratorExit handling.
* [ ] `objects/coroutine.go`: Coroutine, send, throw, close,
  __await__.
* [ ] `objects/async_gen.go`: AsyncGenerator, asend, athrow,
  aclose, the `_PyAsyncGenAThrow` / `_PyAsyncGenASend`
  helper coroutines.
* [ ] `objects/gen_test.go`: state-machine panel, close
  semantics, async iteration.

### Files (cell, v0.6)

* [ ] `objects/cell.go`: Cell struct, MakeCell, get/set
  cell_contents, equality across cells.

### Surface guarantees

* [ ] `code.replace(co_consts=())` returns a new Code with the
  rest unchanged.
* [ ] `code.co_lines()` yields `(start, end, line)` triples
  matching CPython byte-for-byte for every linetable form.
* [ ] `code.co_positions()` yields the four-int tuples.
* [ ] `frame.f_locals` returns a dict that mutates back into
  fast locals per PEP 558.
* [ ] `gen.close()` swallows GeneratorExit if the body completes;
  raises RuntimeError if the body re-yields.
* [ ] `coroutine.__await__()` returns the coroutine itself
  (matching CPython).
* [ ] `async_gen.aclose()` returns a coroutine; awaiting it
  performs the close.
* [ ] `cell_contents` AttributeError when unbound.
* [ ] `hash(code)` is stable across equivalent code objects (same
  bytecode + consts + names + filename + name + firstlineno).

### Cross-references

* Compile pipeline that builds Code: 1620 series.
* Function object that wraps Code: 1685.
* VM execution loop (creates Frames, drives Generators): 1620
  hot path / future ceval spec.

### Out of scope

* PEP 657 enriched-locations accuracy improvements beyond what
  3.14 already offers.
* Free-threaded `dk_version` for code object specialization. Lands
  in v0.14.
