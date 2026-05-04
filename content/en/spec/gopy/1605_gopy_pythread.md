---
title: "gopy pythread spec"
description: "Port of cpython/Python/thread.c to gopy/pythread. Thread create, join, ident, and stack-size hooks layered over Go's goroutine scheduler. The OS-specific thread_pthread.h / thread_nt.h files are dropped."
tags: ["gopy", "spec"]
weight: 1605
---

# 1605. Threads (`pythread/`)

## What we port and what we drop

`cpython/Python/thread.c` is the cross-platform shim. It includes one
of `thread_pthread.h`, `thread_pthread_stubs.h`, `thread_nt.h` to get
the platform primitives. Go's runtime already provides goroutines,
preemption, and a scheduler, so the platform `.h` files are dropped
outright (they are listed as `--` in 1602). We port only the
cross-platform layer.

In v0.1 the surface is intentionally narrow:

| C entry point                       | Go target                          | Notes                                          |
|-------------------------------------|------------------------------------|------------------------------------------------|
| `PyThread_init_thread`              | `pythread.Init`                    | No-op. The Go runtime is already initialized. |
| `PyThread_get_stacksize`            | `pythread.GetStacksize`            | Returns 0; per-interpreter stacksize lives in `state` once that exists (v0.7). |
| `PyThread_set_stacksize`            | `pythread.SetStacksize`            | Returns -2 (not supported). Goroutines grow stacks dynamically. |
| `PY_TIMEOUT_MAX`                    | `pythread.TimeoutMax`              | Constant, microseconds. Matches the POSIX branch. |
| (new) goroutine handle              | `pythread.Start`, `(*Handle).Join` | Replaces `PyThread_start_new_thread` plus the platform-specific join. |
| (new) thread ident                  | `pythread.Ident`, `(*Handle).Ident`| Unique per started handle. |

Deferred to later phases:

- `PyThread_acquire_lock_timed_with_retries`. Depends on `state` (for
  `_PyThreadState_GET`) and `pytime` (for deadlines). Lands when
  `state` lands in v0.3+.
- `PyThread_ParseTimeoutArg`. Depends on object protocol and `pytime`.
- `PyThread_tss_*`. Depends on the object model. v0.1 has no Python
  callers needing TSS; the parking-lot work uses goroutine-scoped
  state, not TSS.
- `PyThread_GetInfo`. Builds a `sys.thread_info` struct sequence; ports
  with `sysmod` in v0.7.

## API

```go
package pythread

const TimeoutMax int64 = ... // microseconds, mirrors PY_TIMEOUT_MAX

type Ident uint64

func Init()                 // no-op, kept for source-shape parity
func GetStacksize() int     // always 0 for now
func SetStacksize(int) int  // always -2 ("not supported")

type Handle struct { /* unexported */ }

// Start runs fn on a new goroutine and returns a Handle. fn must not
// be nil. The handle's Ident is unique for the lifetime of the
// process.
func Start(fn func()) *Handle

func (h *Handle) Ident() Ident
// Join blocks until fn returns. It returns the recovered panic value
// from fn, or nil if fn returned normally. Calling Join more than
// once is safe; subsequent calls return immediately with the same
// value.
func (h *Handle) Join() any
```

## Why a Handle, not a raw ident

CPython surfaces threads through opaque `unsigned long` idents and
relies on the platform to provide join (or to leak). The Go runtime
does not expose a goroutine ident; it instead encourages capturing a
handle. We follow Go conventions here. The naming spec (1601) allows
this: identifiers translate to Go idioms while semantics stay aligned.

The `Ident` type is still useful for parking-lot bookkeeping
(the parking lot keys waiters by address, but uses the ident in
diagnostics), so we keep it as a typed `uint64` minted from a global
atomic counter at `Start` time.

## Concurrency notes

- `Start` is safe to call concurrently.
- `Join` synchronizes-before any code that ran inside fn, in the Go
  memory model sense. We implement this with a `chan struct{}` closed
  on completion.
- Panics inside fn are recovered. The recovered value is delivered via
  `Join`. This matches CPython behavior where a thread's exception is
  surfaced through threading.Thread.run, except we do it at the
  primitive layer because the threading module is high-level Python.

## Tests

`pythread/thread_test.go`:

- `Init` and the stacksize stubs return the documented values.
- `Start` then `Join` runs fn exactly once, in a separate goroutine.
- `Ident` is unique across many Start calls.
- A panicking fn surfaces the value through `Join`.
- `TimeoutMax` is positive and divides cleanly to nanoseconds without
  overflow (the C invariant: `TimeoutMax * 1000` fits in int64).
