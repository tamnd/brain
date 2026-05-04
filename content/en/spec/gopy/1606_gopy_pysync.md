---
title: "gopy pysync spec"
description: "Port of cpython/Python/lock.c, parking_lot.c, and critical_section.c into the gopy/pysync package. Address-keyed parking, byte-flag PyMutex, PyEvent, PyOnceFlag, RecursiveMutex, RWMutex, SeqLock, and the PEP 703 critical-section stack."
tags: ["gopy", "spec"]
weight: 1606
---

# 1606. Synchronization primitives (`pysync/`)

CPython's runtime uses a small set of custom synchronization primitives
that have semantics distinct from `sync.Mutex` / `sync.Cond`:

- `PyMutex` is a 1-byte field with a parked-waiter flag. It does not
  use a heavy OS mutex per instance.
- `_PyRawMutex` is the same idea but reuses the mutex word itself as
  the head of a linked list of waiters, so it can be used inside the
  parking lot's bucket protection.
- `PyEvent`, `_PyOnceFlag`, `_PyRWMutex`, `_PyRecursiveMutex`, `_PySeqLock`
  are layered on top of `PyMutex` plus the parking lot.
- The parking lot itself is an address-keyed wait/wake registry, very
  similar to WebKit's. It is the substrate every other primitive uses
  to block.

We use the package name `pysync` to make it clear the primitives are
distinct from Go's `sync`. Naming follows 1601: drop `_Py`, export
the Go names, keep the call shape.

## C-to-Go map

| C identifier                               | Go target                              |
|--------------------------------------------|----------------------------------------|
| `_PyParkingLot_Park`, `_PyParkingLot_Unpark`, `_PyParkingLot_UnparkAll`, `_PyParkingLot_AfterFork` | `pysync.Park`, `Unpark`, `UnparkAll`, `AfterFork` |
| `PyMutex`, `PyMutex_Lock`, `PyMutex_Unlock`, `PyMutex_IsLocked`, `_PyMutex_LockTimed`, `_PyMutex_TryUnlock` | `pysync.Mutex` with methods `Lock`, `Unlock`, `IsLocked`, `LockTimed`, `TryLock`, `TryUnlock` |
| `PyEvent`, `_PyEvent_IsSet`, `_PyEvent_Notify`, `PyEvent_Wait`, `PyEvent_WaitTimed` | `pysync.Event` with `IsSet`, `Notify`, `Wait`, `WaitTimed` |
| `_PyOnceFlag`, `_PyOnceFlag_CallOnce` | `pysync.OnceFlag` with `Do` |
| `_PyRecursiveMutex` | `pysync.RecursiveMutex` |
| `_PyRWMutex` | `pysync.RWMutex` |
| `_PySeqLock` | `pysync.SeqLock` |
| `_PyRawMutex` | `pysync.RawMutex` (sync.Mutex-backed in v0.1; the linked-list-in-the-word trick triggers go vet's unsafeptr) |
| `_PyCriticalSection*` (`critical_section.c`) | `pysync.CriticalSection`, `BeginX2`, `End`, `Suspend`, `Resume` |
| `_PySemaphore*`                            | not ported. Replaced by a `chan struct{}` waiter inside the parking lot. |

## Parking lot

CPython's parking lot uses 257 buckets, an address mod hash, a per-bucket
`_PyRawMutex`, and a doubly-linked list of waiters. Each waiter owns a
`_PySemaphore` (POSIX `sem_t`, Win32 semaphore, or pthread mutex+cond).

Go port:

- 257 buckets, same hash.
- Per-bucket `sync.Mutex` instead of `_PyRawMutex`. We still port
  `RawMutex` separately, but the parking-lot bucket does not need it
  because Go's `sync.Mutex` is fine as a leaf primitive.
- Each waiter holds a `chan struct{}` of capacity 1. `Wakeup` sends;
  the parked goroutine receives, with a `select` on `time.After` for
  timeouts. This replaces the semaphore.
- The address key is `uintptr(unsafe.Pointer(addr))` where `addr` is
  the pointer the caller passes. Same hash as in C.
- `atomic_memcmp` in C inspects 1, 2, 4, or 8 bytes atomically. In Go
  we cannot translate raw memcmp without `unsafe`, so the API takes
  a `func() bool` predicate the caller implements with the right-sized
  atomic load. This is the only API-shape change from C.

```go
type ParkStatus int

const (
    ParkOK ParkStatus = iota
    ParkTimeout
    ParkAgain
    ParkIntr
)

func Park(addr unsafe.Pointer, check func() bool,
          timeout time.Duration, parkArg any, detach bool) ParkStatus

type UnparkFn func(parkArg any, hasMore bool)

// Unpark wakes one waiter. fn is called with the waiter's parkArg
// while the bucket lock is held; the waiter is woken after the lock
// is released. If no waiter exists, fn is called with (nil, false).
func Unpark(addr unsafe.Pointer, fn UnparkFn)

func UnparkAll(addr unsafe.Pointer)
func AfterFork()
```

`detach` is the hook for the PEP 703 attach/detach protocol. In v0.1
we have no thread state to detach; the parameter is plumbed through
for source-shape parity but currently has no effect. The state package
will wire it up in v0.3 / v0.7.

## PyMutex

Faithful 1-byte port. The state machine:

```
bit 0 (0x01) _Py_LOCKED
bit 1 (0x02) _Py_HAS_PARKED
```

`Lock` fast-paths when bit 0 is clear. On contention it spins (only
under the `pygil_disabled` build tag, since the GIL serializes
contention to begin with), then sets `_Py_HAS_PARKED` and parks via
the parking lot. The `mutex_entry` carries a "time to be fair" deadline
(1 ms after the wait started); the unlocking thread directly hands off
ownership to the parked thread when that deadline has passed, to avoid
starvation.

We translate the C `mutex_entry` into a Go struct with the same two
fields: `timeToBeFair time.Time` and `handedOff bool`. The unparking
function receives the entry through `parkArg`.

`TryLock` and `TryUnlock` map to the timed variants with a zero
timeout, exactly as in C.

## PyEvent, OnceFlag, RecursiveMutex

`Event`: 1-byte field, three states (`_Py_UNLOCKED`, `_Py_LOCKED`
meaning set, `_Py_HAS_PARKED` meaning waiters parked). `Notify` flips
to set and wakes everyone.

`OnceFlag`: 1-byte field with the same three states plus a fourth
`_Py_ONCE_INITIALIZED` (== `_Py_LOCKED`). The first caller runs the
function; concurrent callers park on the flag and wake when the
function finishes. Failure resets to `_Py_UNLOCKED` so a future caller
can retry.

`RecursiveMutex`: a `Mutex` plus an owner ident (`pythread.Ident`) and
a recursion depth. Same recursion contract as `_PyRecursiveMutex`.

## RWMutex

Faithful port of the four-state bit packing:

```
bit 0      _Py_WRITE_LOCKED
bit 1      _Py_HAS_PARKED
bits 2..   reader count
```

We keep the same waiter-fairness property (a parked writer blocks new
readers).

## SeqLock

Pure-atomic primitive, no parking. Port verbatim, swap C atomics for
`sync/atomic.Uint32`.

## CriticalSection (PEP 703)

`critical_section.c` implements per-object critical sections that
serialize access to a Python object in the free-threaded build. In a
GIL build the GIL already provides serialization, so the operations
become bookkeeping only.

We port the full structure (single-object CS, two-object CS, suspend,
resume, push, pop), but the v0.1 implementation runs without thread
state. The fields a `CriticalSection` carries are:

- `prev *CriticalSection` (linked into a per-thread stack)
- `mutex *Mutex` (acquired on Begin, released on End)
- `mutex2 *Mutex` (only for the 2-object form)

The per-thread stack lives in goroutine-local state. Since Go has no
goroutine-local storage, v0.1 stores the stack head on the
`pysync.CSThread` value passed into `Begin`. v0.7 will fold this into
the real `state.ThreadState` once it exists.

The full PEP 703 attach/detach interaction (the suspend bit on the
critical section, plus the dance with the GIL) is deferred to v0.14
along with the rest of free-threading. The shape here is correct;
v0.14 just turns "no-op when no other thread can run" into "actually
acquire the mutex".

## What we drop

- `_PySemaphore`. Replaced by a channel inside the waiter struct. The
  C semaphore is a platform-specific abstraction whose only client
  was the parking lot.
- `_Py_yield` (a SwitchToThread / sched_yield wrapper). Not needed.
  Go's scheduler already preempts.
- The `AfterFork` reset for the buckets clears parked waiters from
  threads that no longer exist after `fork()`. Go programs do not
  fork in the POSIX sense; the function is a no-op. We keep it to
  preserve the call shape.

## Tests

Each primitive has a unit test plus a stress test:

- Mutex: hammer with `runtime.GOMAXPROCS(N)` goroutines incrementing
  a counter, then assert the final value.
- Event: 100 waiters, one notifier, all waiters return.
- OnceFlag: `Do` runs the function exactly once across N goroutines.
- RecursiveMutex: same goroutine can take and release N times; a
  different goroutine cannot release.
- RWMutex: writer-vs-readers fairness assertion.
- SeqLock: writer/reader race on a struct, validate consistency.
- ParkingLot: `Park` then `Unpark` from another goroutine. Timeout
  works. `UnparkAll` wakes everyone.
- CriticalSection: Begin/End balance; nested; two-object form acquires
  in deterministic order.

## Free-threaded considerations

The `Py_GIL_DISABLED` branch in `lock.c` enables a brief spin
(`MAX_SPIN_COUNT = 40`) before parking. We surface this as a build
tag `pygil_disabled` (matching the gopy convention introduced in 1603
v0.14). When the tag is off, spin count is zero and the lock parks
immediately, exactly like the GIL build in C.
