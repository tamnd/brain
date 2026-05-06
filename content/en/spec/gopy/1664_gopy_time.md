---
title: "gopy pytime"
description: "Internal time utilities. Ports cpython/Python/pytime.c. Provides PyTime_t (int64 nanoseconds), monotonic / perf / wall clocks, double / timespec / timeval conversions, deadline math."
tags: ["gopy", "spec"]
weight: 1664
---

# 1664. PyTime utilities

## What we are porting

| C source                                  | Lines | Go target              |
|-------------------------------------------|-------|------------------------|
| `Python/pytime.c`                         |  1356 | `pytime/pytime.go`     |
| `Include/cpython/pytime.h` (public types) |   ~80 | `pytime/types.go`      |

`pytime` is the runtime's clock layer. Every part of CPython that
deals with time (lock timeouts, signal alarms, `time.monotonic`,
asyncio deadlines, `selectors`, the GIL release interval) goes
through it. The header exposes one type, `PyTime_t = int64_t`
nanoseconds, plus a small constellation of conversion and clock
helpers.

The stdlib `time` module is a thin wrapper on top of these helpers.
v0.9 ships `pytime` as the foundation; the user-facing `time` module
follows in the stdlib spec series.

## Why we need it now

contextvars (1663) does not depend on pytime, but asyncio does, and
v0.9's stated gate is `python -m asyncio` smoke. The eval breaker
(1639) currently uses Go's `time.Now()` directly; once pytime lands,
the breaker switches to `pytime.Monotonic()` so the GIL release
interval is byte-for-byte CPython.

## API surface

```go
package pytime

// PyTime_t equivalent: nanoseconds since the relevant epoch.
// Public so callers can do arithmetic; clamping/overflow uses helpers.
type Time int64

// Conversions.
func FromSeconds(s float64, round Rounding) (Time, error)
func FromNanoseconds(ns int64) Time
func FromTimespec(ts syscall.Timespec) (Time, error)
func AsSecondsDouble(t Time) float64
func AsTimespec(t Time) (syscall.Timespec, error)
func AsTimeval(t Time, round Rounding) (syscall.Timeval, error)

// Clocks. *WithInfo variants populate ClockInfo for time.get_clock_info().
func Time_(out *Time) error           // wall clock; "Time_" because "Time" is the type
func Monotonic(out *Time) error
func PerfCounter(out *Time) error
func MonotonicWithInfo(out *Time, info *ClockInfo) error
func PerfCounterWithInfo(out *Time, info *ClockInfo) error
func TimeWithInfo(out *Time, info *ClockInfo) error

// Deadline math. Used by select(), Lock.acquire(timeout), asyncio.
func Deadline(timeout Time) Time
func DeadlineFromObject(timeoutObj objects.Object, round Rounding) (Time, error)

type Rounding int
const (
    RoundFloor Rounding = iota
    RoundCeiling
    RoundHalfEven
    RoundUp
)

type ClockInfo struct {
    Implementation string
    Monotonic      bool
    Adjustable     bool
    Resolution     float64
}
```

The Go signatures keep CPython's `out *Time` style for clocks because
they can fail (e.g., `clock_gettime` ENOTSUP) and we want a single
error path.

## Clock backing

| OS               | wall                | monotonic           | perf                |
|------------------|---------------------|---------------------|---------------------|
| linux / freebsd  | `clock_gettime CLOCK_REALTIME` | `clock_gettime CLOCK_MONOTONIC` | `clock_gettime CLOCK_MONOTONIC` |
| darwin           | `gettimeofday`      | `mach_absolute_time` + timebase | same                |
| windows          | `GetSystemTimePreciseAsFileTime` | `QueryPerformanceCounter` | same                |

We use `golang.org/x/sys/unix` on POSIX and `syscall` on Windows.
The Darwin path needs `mach_timebase_info` once at process start
(matches `pytime_init_monotonic` in CPython); we cache the numerator
and denominator in a `sync.Once`.

Where CPython falls back to `time(NULL)` for low-precision systems we
do the same (Go's `time.Now()` is fine but we want CPython's exact
fall-back semantics for the `ClockInfo.Resolution` field).

## Rounding

CPython's `_PyTime_FromSeconds` and friends accept a rounding mode so
sub-nanosecond float values map deterministically to int ns. The four
modes pin to:

| Mode          | C constant                  | Go            |
|---------------|-----------------------------|---------------|
| RoundFloor    | `_PyTime_ROUND_FLOOR`       | `math.Floor`  |
| RoundCeiling  | `_PyTime_ROUND_CEILING`     | `math.Ceil`   |
| RoundHalfEven | `_PyTime_ROUND_HALF_EVEN`   | banker's      |
| RoundUp       | `_PyTime_ROUND_UP`          | away-from-zero|

The "half even" mode requires a careful float-to-int that does not go
through `math.Round` (which is half-away-from-zero); we replicate
`_PyTime_RoundHalfEven` byte-for-byte.

## Overflow

`PyTime_t` is int64 ns, so the range is roughly ±292 years.
Conversions clamp on overflow with `OverflowError` matching CPython:

* From float seconds: anything outside ±9223372036.854775 raises.
* `AsTimeval` clamps microseconds to int64 then to `syscall.Timeval`
  (which is 32 bit on some platforms; we match CPython's per-platform
  size).

## Eval breaker integration

`vm/eval_gil.go` currently uses `time.Now().Sub(...)` for the
release-interval math. v0.9 swaps that for `pytime.Monotonic` so
`sys.setswitchinterval(0.005)` matches CPython's nanosecond
arithmetic. The breaker spec (1639) is updated; this spec is
load-bearing for that change.

## Gate

`pytime/pytime_test.go`:

* Round-trip: `FromSeconds(1.5, RoundFloor) == 1500000000`.
* Half-even: pin a panel of CPython values
  (`_PyTime_FromSecondsObject` testdata).
* `Monotonic` increases monotonically across two calls separated by
  a `time.Sleep(1ms)`; difference ≥ 1ms - resolution.
* `ClockInfo` for monotonic on linux reports
  `Implementation == "clock_gettime(CLOCK_MONOTONIC)"`.
* Overflow: `FromSeconds(1e20, RoundFloor)` returns `OverflowError`.

## Out of scope

* PEP 564 nanosecond stdlib wrappers (`time.time_ns`, etc.). They are
  one-line wrappers on top of `pytime.Time_`; ship with the `time`
  module.
* `time.localtime` / `gmtime`. They go through `localtime_r` /
  `gmtime_r` which are platform-shaped; ship with the `time` module.
* `_PyTime_localtime` (timezone-aware path). Same.

## v0.9 checklist

### Files

* [x] `pytime/pytime.go`: type plus conversion helpers plus
  rounding plus deadline. Shipped in commit `99f477f`.
* [x] `pytime/clocks.go` (cross-platform dispatcher) plus
  `info_linux.go` / `info_darwin.go` / `info_windows.go` for the
  per-OS `ClockInfo`. (Single file rather than three `clocks_*.go`
  files; the platform split is in the info accessors.)
* [x] `pytime/pytime_test.go`: gate panel.
* [x] `vm/eval_gil.go`: switch-interval timer reads `pytime.Monotonic`
  and arms `BreakerGILDropRequest` once a drop has been requested
  and the interval has elapsed. Wired through the eval loop's
  per-iteration poll via `SetGIL` + `gilSwitchTimer.poll`. The
  drop bit only fires when sub-interpreter contention attaches a
  GIL (v0.13); v0.9 leaves the field nil so production stays a
  no-op. Pinned by `vm/eval_gil_test.go`
  (`TestGILSwitchTimerArmsAfterIntervalWithDropRequest`,
  `TestGILSwitchTimerNoDropRequestNoArm`,
  `TestGILSwitchTimerIntervalNotElapsed`,
  `TestGILSwitchTimerResetClearsArm`).

### Surface guarantees

* [x] `Time` is a typed int64.
* [x] All four rounding modes match CPython (Floor, Ceiling,
  HalfEven, Up; the spec's "five" was a draft typo).
* [x] `Monotonic` strictly non-decreasing on every supported
  platform.
* [x] `ClockInfo.Resolution` matches CPython's reported value within
  the platform's resolution noise.
