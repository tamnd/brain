---
title: "gopy eval gil"
description: "Port of cpython/Python/ceval_gil.c. The GIL acquire/release protocol, the eval breaker bitfield, signal pending flags, and the gopy-vs-Go-runtime threading mapping."
tags: ["gopy", "spec"]
weight: 1639
---

# 1639. GIL and eval breaker

## What we are porting

`Python/ceval_gil.c` (~1500 lines) plus the eval-breaker bit
declarations in `Include/internal/pycore_ceval.h`. Two
intertwined concerns:

* **GIL**: the global interpreter lock. CPython serializes Python
  bytecode execution behind one mutex per interpreter. The eval
  loop drops it on long-running C calls and re-acquires it before
  returning to Python.
* **Eval breaker**: a bitfield the eval loop polls each `RESUME`
  and each backward jump. When any bit is set, the loop stops
  dispatching and runs the matching handler: GC, signals, async
  exceptions, GIL drop request, monitoring tool install, profiler
  attach.

## How gopy maps the GIL

Go has goroutines, not OS threads, and Go's scheduler is
cooperative-with-preemption. We do not need a mutex to serialize
bytecode execution because each interpreter runs in one goroutine
at a time. But we do need the GIL surface for two reasons:

1. **C extension shape parity**: Go-native modules that mirror
   CPython C modules (the `tamnd/gopy-stdlib` companion) call into
   the same `Py_BEGIN_ALLOW_THREADS` / `Py_END_ALLOW_THREADS`
   shape.
2. **Sub-interpreters**: v0.13 introduces sub-interpreters, each
   with its own GIL. The lock is a real lock at that point; in
   v0.6 it is a single-owner mutex with no contention.

So the v0.6 GIL is:

```go
// GIL is the per-interpreter execution lock. Mirrors _PyEval_GilState
// from Python/ceval_gil.c.
//
// In v0.6 each Interpreter runs in one goroutine and the lock has
// at most one waiter. The mutex still goes through Acquire / Release
// so the API matches CPython and so v0.13 sub-interpreters can keep
// the same call sites.
type GIL struct {
    mu          sync.Mutex      // protects the lock itself
    locked      bool            // is anyone holding it?
    holder      *state.Thread   // who holds it
    cond        sync.Cond       // signalled on release
    requestDrop atomic.Bool     // another thread asked us to drop
    interval    time.Duration   // sys.setswitchinterval
}

// Acquire blocks until ts holds the GIL. Mirrors take_gil from
// ceval_gil.c.
func (g *GIL) Acquire(ts *state.Thread)

// Release drops the GIL. Mirrors drop_gil.
func (g *GIL) Release(ts *state.Thread)

// RequestDrop asks the current holder to drop the GIL at the next
// poll point. Mirrors COMPUTE_EVAL_BREAKER (the GIL_DROP_REQUEST
// bit).
func (g *GIL) RequestDrop()
```

## Eval breaker

The breaker is a per-thread atomic uint32. Bits:

| Bit                              | Source signal                       |
|----------------------------------|-------------------------------------|
| `BreakerGILDropRequest`          | another thread wants the GIL        |
| `BreakerSignalsPending`          | a Unix signal arrived               |
| `BreakerCallsPending`            | `Py_AddPendingCall` queued work     |
| `BreakerGCScheduled`             | the cycle collector wants to run    |
| `BreakerAsyncException`          | `PyThreadState_SetAsyncExc`         |
| `BreakerProfileOrTrace`          | a profiler / tracer was installed   |
| `BreakerMonitoringVersion`       | PEP 669 monitoring tool changed     |

```go
// Breaker holds the eval-loop poll bits. Mirrors the eval_breaker
// field on PyThreadState plus the helpers in ceval_gil.c.
type Breaker struct {
    bits atomic.Uint32
}

// Set sets one bit. Mirrors _PyEval_AddPendingFlag.
func (b *Breaker) Set(bit uint32)

// Clear clears one bit. Mirrors _PyEval_ClearPendingFlag.
func (b *Breaker) Clear(bit uint32)

// Load reads the bitfield. Hot-path read; the eval loop checks
// this each RESUME / each backward JUMP.
func (b *Breaker) Load() uint32
```

The eval loop polls `Breaker.Load()` once per outer dispatch
iteration (1636) and dispatches to a handler when non-zero.

## Pending calls

`Py_AddPendingCall` queues a function to run on the main thread
under the GIL. Common use case: signal handlers cannot run Python
code directly, so they queue a pending call and set the
`BreakerCallsPending` bit.

```go
// Pending is the per-interpreter pending-call queue. Mirrors
// _Py_AddPendingCall. Bounded ring buffer; overflow returns an
// error.
type Pending struct {
    mu    sync.Mutex
    queue [32]func() error
    head  int
    tail  int
}

// Add enqueues a callback to run at the next eval-breaker poll.
func (p *Pending) Add(fn func() error) error

// Drain runs all queued callbacks. Called by the eval loop when
// BreakerCallsPending is set.
func (p *Pending) Drain() error
```

## File mapping

| C source                                | Go target                          |
|-----------------------------------------|------------------------------------|
| `Python/ceval_gil.c` (lock)             | `vm/gil/gil.go`                    |
| `Python/ceval_gil.c` (breaker)          | `vm/gil/breaker.go`                |
| `Python/ceval_gil.c` (pending)          | `vm/gil/pending.go`                |
| `Include/internal/pycore_ceval.h` (bits) | `vm/gil/bits.go`                   |
| `Python/ceval_gil.c` (signal handler bridge) | `vm/gil/signals.go`           |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `gil/gil.go`: `GIL` struct, `Acquire`, `Release`,
  `RequestDrop`, `DropRequested`, `SetSwitchInterval`. `sync.Mutex`
  plus `sync.Cond` for the wait. (Flat layout per project convention.)
* [x] `gil/breaker.go`: `Breaker` struct, `Set`, `Clear`,
  `Load`, `IsSet`. CAS loop over `atomic.Uint32`.
* [x] `gil/bits.go`: `Breaker*` bit constants matching
  `pycore_ceval.h` numerically.
* [x] `gil/pending.go`: `Pending` struct, `Add`, `Drain`,
  ring-buffer overflow error (`ErrPendingFull`).
* [x] `gil/signals.go`: bridge from `os/signal.Notify` to
  `Breaker.Set(BreakerSignalsPending)` + queued callback. SIGINT
  KeyboardInterrupt wiring lives in the signal module (1651).
* [x] `gil/gil_test.go` + `gil/signals_unix_test.go`: acquire/release
  round-trip, request-drop flag, breaker bits set/clear and CAS
  concurrent stress, pending-call FIFO + overflow + drain-stops-on-error,
  signal-bridge smoke test (SIGUSR1, gated to non-Windows).

### Surface guarantees

* [x] `GIL.Acquire` followed by `GIL.Release` from the same
  goroutine is contention-free in the steady state. Pinned by
  `gil/gil_test.go` (`TestGILAcquireRelease`,
  `TestGILWaitsForRelease`).
* [~] `GIL.RequestDrop` sets a flag that `Acquire` clears on next
  hand-off. Pinned by `TestGILRequestDrop`. Bit-on-`Breaker.Load`
  wiring at the holder still pending; lands when v0.13
  sub-interpreter contention shows up.
* [x] `Pending.Add` then `Pending.Drain` runs callbacks in FIFO
  order. Overflow returns `ErrPendingFull` and does not lose
  existing entries; drain stops on first error and leaves the
  remainder. Pinned by `TestPendingFIFO`, `TestPendingOverflow`,
  `TestPendingDrainStopsOnError`.
* [n] SIGINT delivered while the eval loop runs raises
  `KeyboardInterrupt` at the next poll point. Defers to the
  signal module port (1651); the bridge wiring is in place
  (`signals_unix_test.go` covers SIGUSR1) but the
  KeyboardInterrupt exception path needs the exception module
  (1686).
* [x] Eval-breaker bit values match
  `Include/internal/pycore_ceval.h` byte-for-byte. Pinned by
  `TestBreakerBitValues` (every bit + `BreakerEventsMask` mask).
* [x] Eval loop polls the breaker at three places: top of dispatch,
  `JUMP_BACKWARD`, and `RESUME` (oparg < 2). A queued
  `Pending.Add` callback paired with `Breaker.Set(BreakerCallsPending)`
  runs at the next poll, and the bit clears after a successful drain.
  `JUMP_BACKWARD_NO_INTERRUPT` skips the per-arm poll. Pinned by
  `vm/eval_breaker_test.go`
  (`TestEvalBreakerTopOfLoopPoll`, `TestEvalBreakerJumpBackwardPoll`,
  `TestEvalBreakerResumePoll`,
  `TestEvalBreakerJumpBackwardNoInterruptSkipsPoll`,
  `TestEvalBreakerNoBitNoDrain`).
* [~] `sys.setswitchinterval(s)` updates `GIL.interval`. Pinned
  by `TestGILSwitchInterval`. The cross-block `sys` binding test
  (`partest/setswitchinterval_test.go`) still needs the `sys`
  module port (1651).

### Out of scope for v0.6

* Real GIL contention between sub-interpreters. Lives in v0.13.
* PEP 703 free-threaded build (no GIL at all). Lives in v0.14.
* Multi-thread `Py_AddPendingCall` from worker goroutines. The
  v0.6 surface accepts the call but assumes one drainer.

### Cross-references

* Eval loop poll point: 1636.
* `state.Thread` struct that owns the breaker: 1615 (state spec,
  reserved).
* `sys.setswitchinterval` binding: 1651 (modules spec, reserved).
* Signal module bridge: 1651.
