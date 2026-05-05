---
title: "gopy frame"
description: "Port of cpython/Python/frame.c. Frame layout, locals-plus storage, frame chain push/pop, generator frame suspension."
tags: ["gopy", "spec"]
weight: 1637
---

# 1637. Frame layout and lifecycle

## What we are porting

`Python/frame.c` (~700 lines) plus the `_PyInterpreterFrame`
declarations in `Include/internal/pycore_frame.h`. The frame is the
runtime activation record the eval loop reads and writes on every
instruction: it owns the value stack, the fast locals array, the
current instruction pointer, the previous frame, and a back-pointer
to the code object.

The Python-visible `frame` object (the one `sys._getframe()`
returns) is a thin wrapper over `_PyInterpreterFrame` and lives in
`Objects/frameobject.c` (spec 1687). This spec covers the
interpreter frame; the user-visible wrapper depends on it.

## Go shape

```go
// Frame is the interpreter-side activation record. Mirrors
// _PyInterpreterFrame from Include/internal/pycore_frame.h.
//
// Frames live on a per-thread chunk-allocated stack (see
// frame.Chunk). They are not GC'd through Go's heap; the eval
// loop pushes and pops them explicitly so the layout matches
// CPython's _PyThreadState_PushFrame call shape.
type Frame struct {
    Code        *object.Code   // the code being executed
    Globals     object.Object  // module globals dict
    Builtins    object.Object  // module builtins dict
    Locals      object.Object  // locals dict (None for fast-locals frames)
    Func        *object.Function // the function object, if any
    Previous    *Frame         // caller frame (frame chain)
    InstrPtr    int            // current instruction index
    PrevInstr   int            // for RESUME after yield
    StackTop    int            // index into LocalsPlus where stack begins
    LocalsPlus  []stackref.Ref // locals + cells + free + value stack
    Owner       OwnerKind      // generator, frame object, eval loop
    ReturnOffset int           // for inline frames: caller's resume point
    YieldOffset  int           // for generators: last YIELD_VALUE offset
}

// OwnerKind tracks which subsystem holds the canonical pointer to
// this frame. Mirrors _PyFrameOwner.
type OwnerKind uint8
const (
    OwnedByEval OwnerKind = iota
    OwnedByGenerator
    OwnedByThread     // top-of-stack frame
    OwnedByFrameObj   // a Python frame object refs this
    OwnedByCstack     // C-stack-allocated, do not free
)
```

## Locals-plus layout

CPython packs locals, cells, free vars, and the value stack into
one contiguous array `localsplus`. The eval loop indexes into it
by offset:

```
[ 0 .. nlocals          )  fast locals
[ nlocals .. nlocals+ncells )  cell variables
[ ... .. nlocals+ncells+nfree )  free variables
[ ... .. ... + co_stacksize )    value stack
```

We mirror this with one Go slice:

```go
// SizeFor computes the LocalsPlus length needed for the given
// code object. Mirrors _PyFrame_NumSlotsForCodeObject.
func SizeFor(co *object.Code) int {
    return co.NLocalsPlus + co.StackSize
}
```

## Frame stack

CPython allocates frames out of a per-thread chunk allocator
(`_PyThreadState_AllocateFrame`). We mirror this with a Go-side
chunk allocator backed by a `[]Frame` arena per Thread:

```go
// Chunk is a per-thread frame arena. Mirrors _PyStackChunk from
// pycore_pystate.h. Frames are bumped into chunks; chunks chain
// when full.
type Chunk struct {
    Frames []Frame
    Top    int
    Prev   *Chunk
}

// Push allocates a frame in ts's chunk stack, links it to the
// current top of the frame chain, and returns it. Mirrors
// _PyThreadState_PushFrame.
func Push(ts *state.Thread, co *object.Code) *Frame

// Pop unlinks the top frame and returns its slot to the chunk.
// Mirrors _PyThreadState_PopFrame.
func Pop(ts *state.Thread)
```

The chunk allocator is a thin wrapper over a Go slice. Go's
escape analysis would normally heap-allocate `Frame` but the
chunk arena keeps allocations bounded and amortized.

## Generator frames

Generator frames are not freed when the eval loop returns to the
caller. They are owned by the generator object and revived on
`g.send(...)`. The generator object holds the `*Frame` directly.

```go
// CopyToGenerator copies the live frame state into a Generator
// object's frame slot, transferring ownership. Mirrors
// _PyGen_CopyToFrame from Objects/genobject.c, lifted here so the
// frame side owns the layout knowledge.
func CopyToGenerator(g *object.Generator, src *Frame)
```

When `RESUME` runs in a generator frame, the eval loop reads from
the generator's frame slot rather than from the per-thread chunk.

## Frame teardown on exception

When an exception escapes a frame, the eval loop walks the frame
chain calling `clear` on each frame. `clear` decrefs every locals
slot, every cell, every free var, and every live stack value.
This mirrors `_PyFrame_ClearExceptCode` from `frame.c`.

## File mapping

| C source                          | Go target                                  |
|-----------------------------------|--------------------------------------------|
| `Python/frame.c`                  | `vm/frame/frame.go`                        |
| `Include/internal/pycore_frame.h` (struct) | `vm/frame/frame.go`               |
| `Python/frame.c` (chunk alloc)    | `vm/frame/chunk.go`                        |
| `Python/frame.c` (clear / unlink) | `vm/frame/teardown.go`                     |

Note: the user-visible `frame` Python object (the `_PyFrame_Type`
in `Objects/frameobject.c`) lives in spec 1687. This spec covers
only the interpreter-side `_PyInterpreterFrame`.

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `frame/frame.go`: `Frame` struct, `OwnerKind` enum,
  `SizeFor`, count helpers (`NLocalsOf`/`NCellsOf`/`NFreeOf`/`NLocalsPlusOf`),
  layout-offset helpers (`CellsStart`/`FreesStart`/`StackStart`),
  `Init`, stack ops (`PushStack`/`PopStack`/`PeekStack`), local
  ops (`SetLocal`/`LocalAt`). (Flat layout per project convention.)
* [x] `frame/chunk.go`: `Chunk` per-thread arena, `FrameStack`,
  `Push`, `Pop`, chunk-chain growth. 32-frame slabs.
* [x] `Frame.Clear` (in `frame/frame.go`): closes every stackref
  in LocalsPlus and resets Code/Globals/Builtins/Locals/Func.
  Folded into the existing file rather than a separate teardown.go
  to keep the Frame struct and its lifecycle in one place.
* [x] `Frame.Suspend`/`Frame.Resume` + `FrameStack.Detach` for
  generator ownership transfer. The objects.Generator wrapper that
  consumes the detached frame still lands in 1687.
* [x] `frame/frame_test.go`: SizeFor + layout offsets, Init,
  stack ops round-trip, local access, push/pop, chain walk across
  chunk-boundary growth.

### Surface guarantees

* [~] `Push` followed by `Pop` is amortized O(1) on the chunk
  arena and grows across chunk boundaries. Pinned structurally
  by `TestFrameStackPushPop` and `TestFrameStackChunkGrowth`. The
  test_call.py corpus comparison waits on the cpython_smoke
  harness (1630).
* [x] Frame chain (`Previous`) walk produces the caller sequence
  for nested calls, including across chunk-boundary growth.
  Pinned by `TestFrameStackChunkGrowth` (walks `Previous` for
  ChunkSize+5 frames).
* [x] Generator suspend / resume preserves every stack slot,
  every fast local, and the instruction pointer. Pinned by
  `TestFrameSuspendResume` and `TestFrameStackDetach`.
* [x] `Clear` releases every owned slot. Pinned by
  `TestFrameClearReleasesRefs` (LocalsPlus all-null after Clear,
  Code/Globals/Builtins/Locals/Func/Previous all nil).
* [x] LocalsPlus layout: locals at `[0:NLocals)`, cells at
  `[NLocals:NLocals+NCells)`, frees at
  `[NLocals+NCells:NLocalsPlus)`, stack at
  `[NLocalsPlus:NLocalsPlus+StackTop)`. Pinned by `TestSizeFor`
  (`CellsStart`/`FreesStart`/`StackStart` plus `NLocalsPlusOf`).

### Cross-block dependencies

* [~] `object.Code` carries the count info via `Varnames`,
  `Cellvars`, `Freevars`, `Stacksize`. The named accessors
  (`NLocalsPlus`, `NLocals`, `NCells`, `NFree`) live on the
  frame side as helpers. The Objects-side fields land alongside
  the rest of 1687.
* [ ] `object.Generator` exposes a frame slot the eval loop can
  write to (Objects spec 1687). Frame side ships
  `Suspend`/`Resume`/`FrameStack.Detach` already; the wrapper
  type is pending.
* [ ] `object.Function` carries the closure cells the frame
  receives at push time (Objects spec 1685). Function exists,
  cell wiring still pending.

### Out of scope for v0.6

* Inlined CALL frames (CPython's "inline" call optimization that
  avoids a real frame push). v0.6 always pushes a real frame.
  Inline frames land alongside the specializer in v0.11.
* Async-generator-specific frame paths beyond what plain
  generators need. The async-generator object lives in 1687.
* Free-threaded frame ownership transitions. Lives in v0.14.

### Cross-references

* Eval loop that reads / writes the frame: 1636.
* Stack reference values stored in LocalsPlus: 1638.
* User-visible frame object wrapper: 1687.
* Generator / coroutine objects: 1687.
