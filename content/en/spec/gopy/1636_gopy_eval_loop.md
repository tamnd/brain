---
title: "gopy eval loop"
description: "Port of cpython/Python/ceval.c and cpython/Python/ceval_macros.h. The Tier-1 bytecode dispatch loop, exception unwind, generator resume, and call/return trampolines."
tags: ["gopy", "spec"]
weight: 1636
---

# 1636. Eval loop and dispatch macros

## What we are porting

Two files, ~10k lines total:

* `Python/ceval.c` (~9000 lines): the Tier-1 eval loop. Entry,
  dispatch, exception unwind, frame push/pop on call and return,
  generator resume, eval breaker poll points, and the small set of
  hand-written opcodes that do not live in `bytecodes.c`
  (RESUME, ENTER_EXECUTOR, INSTRUMENTED_*).
* `Python/ceval_macros.h` (~700 lines): macros the generated
  dispatch arms expand against. STACK_GROW, GETLOCAL, SETLOCAL,
  TARGET, DISPATCH, JUMPBY, INSTRUCTION_SIZE, the inline-cache
  walk macros, deopt machinery.

The generated dispatch arms themselves live in `vm/opcodes_gen.go`
(spec 1621). This spec covers everything around them: the loop
that calls them, the helpers they expand against, and the unwind
logic when one of them returns an error.

## Go shape

Top-level entry in `vm/eval.go`:

```go
// Eval runs frame f to completion under thread state ts and
// returns the value the frame produced (RETURN_VALUE) or the
// error that escaped (uncaught exception).
//
// Mirrors _PyEval_EvalFrameDefault from Python/ceval.c.
func Eval(ts *state.Thread, f *frame.Frame) (object.Object, error)

// EvalCode is the convenience wrapper that builds a frame from a
// code object plus globals/locals and calls Eval. Mirrors
// PyEval_EvalCode.
func EvalCode(ts *state.Thread, co *object.Code, globals, locals object.Object) (object.Object, error)
```

The eval state is a goroutine-local struct that survives the
whole call:

```go
// evalState is the per-call state the dispatch arms read and write.
// Mirrors the locals at the top of _PyEval_EvalFrameDefault.
type evalState struct {
    ts        *state.Thread
    f         *frame.Frame  // current frame
    pc        int           // instruction offset within f.code
    stack     []stackref.Ref
    sp        int           // stack pointer
    fastlocals []stackref.Ref // f.localsplus alias
    err       *errors.Exception
    breaker   uint32        // eval-breaker shadow read each DISPATCH
}
```

## Dispatch shape

CPython uses computed gotos when the compiler supports them and
falls back to a switch otherwise. Go has no computed goto; we use
a switch with a function-call indirection only for the rare
adaptive paths. The hot loop is:

```go
for {
    inst := e.f.code.Instructions[e.pc]
    op := opcode.Op(inst >> 8)
    oparg := uint32(inst & 0xff)
    if e.breaker != 0 {
        if err := e.handleEvalBreaker(); err != nil {
            return e.unwind(err)
        }
    }
    next, err := e.dispatch(op, oparg)
    if err != nil {
        if v, handled := e.handleException(err); handled {
            continue
        } else {
            return v, err
        }
    }
    e.pc = next
}
```

`dispatch` is the generated function from 1621.

## Exception unwind

`Python/ceval.c` walks the code object's exception table to find a
handler when an opcode raises. The walk format is PEP 657 and was
already ported in 1628 (assemble) for the writer side. The reader
side ports here:

```go
// handleException walks the exception table starting at e.pc to
// find a handler. Returns (recovered_pc, true) on hit and
// (zero, false) on miss. Mirrors _PyFrame_GetExceptionTableHandler.
func (e *evalState) handleException(err error) (object.Object, bool)
```

The exception table walk is a varint decode against
`co.ExceptionTable`. Same algorithm CPython uses; the byte format
is what 1628 emits.

## Eval breaker

CPython's eval breaker is a bitmask of pending things the eval
loop must react to: signals, GIL drop requests, async exceptions,
GC requests, profiler attach, monitoring tool installs.

Detail lives in 1639. The eval-loop side just polls the bit and
calls into `vm/gil.go` when it is set.

## Special opcodes (hand-written)

A small set of opcodes are not in `bytecodes.c`. They live in
`vm/eval.go` directly:

* `RESUME`: re-enter a frame after a yield. Reads
  `f.PrevInstr`, advances past `RESUME`, polls eval breaker.
* `INSTRUMENTED_RESUME`, `INSTRUMENTED_*`: monitoring hooks
  (PEP 669). For v0.6 these reduce to their non-instrumented
  base case.
* `ENTER_EXECUTOR`: Tier-2 entry. For v0.6 this is an unconditional
  fall-through (the executor table is empty).

## File mapping

| C source                  | Go target                                        |
|---------------------------|--------------------------------------------------|
| `Python/ceval.c`          | `vm/eval.go`                                     |
|                           | `vm/eval_unwind.go` (exception table walk)       |
|                           | `vm/eval_call.go` (CALL trampoline, frame push)  |
|                           | `vm/eval_resume.go` (RESUME, generator re-entry) |
| `Python/ceval_macros.h`   | `vm/dispatch.go` (DISPATCH, JUMPBY, GETLOCAL...) |
| `Python/ceval.c` (helpers) | `vm/eval_helpers.go` (deoptHere, stack push/pop) |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `vm/eval.go`: `Eval`, `EvalCode`, the dispatch loop driver,
  `evalState` struct, fetch with EXTENDED_ARG accumulation, push/pop/peek
  shortcuts, advance/jumpBy, local helpers.
* [x] `vm/eval_unwind.go`: PEP 657 exception-table walk in
  `handleException` (drives stack truncation + handler jump).
  `unwind` / `handleEvalBreaker` still placeholder for #161.
* [x] `vm/exctable.go`: `readExcVarint` + `findExcHandler`,
  round-tripped against `compile/assemble_exceptions.go` in
  `vm/exctable_test.go`. End-to-end parity panel in
  `vm/exception_table_parity_test.go` runs curated handler-range
  fixtures through `compile.AssembleExceptionTable`, then walks every
  byte offset to assert the reader reproduces the writer's
  (start, end, target, depth, lasti) tuples.
* [~] `vm/eval_call.go`: CALL trampoline, frame push on call,
  frame pop on return. Wires `objects.FunctionType.Call` to push a
  frame, bind positional+keyword args, fill defaults, and re-enter
  Eval. Vectorcall plumbing waits on the abstract layer (#161).
* [~] `vm/eval_resume.go`: RESUME with eval-breaker poll. Generator
  re-entry / RETURN_GENERATOR blocked on objects.Generator (1687).
* [x] `vm/dispatch.go`: dispatch driver returning typed
  notImplemented{op} until B2-B5 generates the real arms.
* [x] `vm/threadstate.go`: per-Thread VM state (breaker, frame
  stack, pending-call queue) keyed by *state.Thread.
* [x] `vm/eval_helpers.go`: `incref`, `decref`, `newref`,
  `decrefInputs` (Go-GC no-ops), plus `iterToSlice`, slice helpers,
  intrinsics dispatch tables. (B6)
* [~] `vm/eval_test.go`: surface tests for ErrNotImplemented wrap,
  opcode-name in error message, EXTENDED_ARG fetch, lazy
  threadstate init, plus per-arm smoke tests (CALL builtin,
  MAKE_FUNCTION + Call, UNPACK_SEQUENCE, LIST_APPEND,
  CALL_INTRINSIC_1 list-to-tuple, CALL_KW, BINARY_SLICE).
  Wider coverage comes after B2-B5 generates arms.

### Opcode panel (Tier-1, unspecialized)

Each row flips to `[x]` once its switch arm in `vm/opcodes_gen.go`
runs without panicking and `vm/eval_test.go` covers the happy
path. Adaptive variants (`*_INT`, `*_STR`, ...) inherit their
parent row.

* [x] Stack ops: `NOP`, `RESUME`, `POP_TOP`, `PUSH_NULL`, `COPY`,
  `SWAP`, `POP_BLOCK`, `POP_ITER`, `NOT_TAKEN`, `TO_BOOL`.
* [x] Constant / fast load: `LOAD_CONST`, `LOAD_SMALL_INT`,
  `LOAD_FAST`, `LOAD_FAST_BORROW`, `LOAD_FAST_CHECK`,
  `LOAD_FAST_AND_CLEAR`, `LOAD_FAST_LOAD_FAST`,
  `LOAD_FAST_BORROW_LOAD_FAST_BORROW`, `STORE_FAST`,
  `STORE_FAST_LOAD_FAST`, `STORE_FAST_STORE_FAST`,
  `DELETE_FAST`. (`RETURN_VALUE` lives here too for the v0.6 starter.)
* [x] Global / name: `LOAD_GLOBAL`, `LOAD_NAME`, `STORE_GLOBAL`,
  `STORE_NAME`, `DELETE_GLOBAL`, `DELETE_NAME`.
* [x] Closure / cell: `LOAD_DEREF`, `STORE_DEREF`, `DELETE_DEREF`,
  `LOAD_FROM_DICT_OR_DEREF`, `MAKE_CELL`, `COPY_FREE_VARS`.
* [~] Attribute / subscript: `STORE_SUBSCR`, `DELETE_SUBSCR`
  shipped; `BINARY_OP NB_SUBSCR` routes through `getItem` against
  `MappingMethods.GetItem` / `SequenceMethods.GetItem`. `LOAD_ATTR`,
  `STORE_ATTR`, `DELETE_ATTR` route through `objects.GetAttr` /
  `SetAttr` / `DelAttr` (which dispatch through `tp_getattro` /
  `tp_setattro`). `LOAD_SUPER_ATTR`, `LOAD_SPECIAL` still wait on
  the descriptor / method-resolution work in 1685.
* [~] Arithmetic: `BINARY_OP` covers Add, Sub, Mul, TrueDivide,
  FloorDivide, Remainder, Power, And, Or, Xor, Lshift, Rshift, and
  the Subscr sub-op; the matching inplace forms (NB_INPLACE_*) reuse
  the non-inplace slot since Int is immutable. MatMul still returns
  TypeError pending its own slot. `UNARY_NEGATIVE`, `UNARY_NOT`,
  `UNARY_INVERT`, `COMPARE_OP`, `IS_OP`, `CONTAINS_OP` (sequence-aware,
  falls back to iterator walk). Floor and modulo use Python
  sign-of-divisor semantics; true divide always returns float;
  `numericForward` honors the `NotImplemented` sentinel so an int +
  float pair falls through to the float slot.
* [~] Iteration: `GET_ITER`, `FOR_ITER`, `END_FOR` shipped.
  `GET_AITER`, `GET_ANEXT` defer to async (#165).
* [~] Containers: `BUILD_LIST`, `BUILD_TUPLE`, `BUILD_MAP`,
  `BUILD_STRING`, `LIST_APPEND`, `LIST_EXTEND`, `MAP_ADD`,
  `DICT_UPDATE`, `DICT_MERGE`. `BUILD_SET` returns a TypeError
  pending the set port (1681). `LIST_TO_TUPLE` lands via the
  intrinsic dispatch (`CALL_INTRINSIC_1`).
* [x] Unpacking: `UNPACK_SEQUENCE`, `UNPACK_EX`.
* [x] Slicing: `BINARY_SLICE`, `STORE_SLICE`, `BUILD_SLICE`.
* [x] Control flow: `JUMP_FORWARD`, `JUMP_BACKWARD`, `JUMP`,
  `JUMP_NO_INTERRUPT`, `POP_JUMP_IF_TRUE`, `POP_JUMP_IF_FALSE`,
  `POP_JUMP_IF_NONE`, `POP_JUMP_IF_NOT_NONE`,
  `JUMP_BACKWARD_NO_INTERRUPT`, `RETURN_VALUE`. (`RETURN_GENERATOR`
  is held back for #161 alongside the CALL trampoline; `RETURN_CONST`
  was removed in 3.14.)
* [x] Calls: `CALL`, `CALL_KW`, `CALL_FUNCTION_EX`,
  `MAKE_FUNCTION`, `SET_FUNCTION_ATTRIBUTE`. `KW_NAMES` is folded
  into `CALL_KW` in 3.14 (the kwnames tuple ships on the stack).
* [~] Generator / coroutine: `END_SEND` shipped (drops the receiver
  and forwards the value, matching the `yield from` cleanup contract).
  `YIELD_VALUE`, `SEND`, `GET_AWAITABLE`, `GET_YIELD_FROM_ITER`,
  `RETURN_GENERATOR` block on objects.Generator (#165).
* [ ] Async: `BEFORE_ASYNC_WITH`, `BEFORE_WITH`,
  `WITH_EXCEPT_START`, `CLEANUP_THROW`, `LOAD_SPECIAL`. (#165)
* [~] Exception handling: `RAISE_VARARGS`, `RERAISE`,
  `PUSH_EXC_INFO`, `POP_EXCEPT`, `CHECK_EXC_MATCH` shipped.
  `CHECK_EG_MATCH` and `LOAD_ASSERTION_ERROR` wait on the
  exception module port (1686). The unwind uses Go errors as
  exception values until the exception class hierarchy lands.
* [~] Class / type: `GET_LEN`, `EXIT_INIT_CHECK` shipped (the latter
  raises TypeError when `__init__` returns non-None, matching CPython).
  `LOAD_BUILD_CLASS`, `MATCH_CLASS`, `MATCH_MAPPING`, `MATCH_SEQUENCE`,
  `MATCH_KEYS` defer to the class / pattern-matching ports.
* [x] f-strings: `FORMAT_SIMPLE`, `FORMAT_WITH_SPEC`,
  `CONVERT_VALUE`, `BUILD_STRING`. Empty spec routes through `Str`;
  non-empty spec waits on `PyObject_Format`. `FORMAT_VALUE` was
  retired in 3.14.
* [ ] Imports: `IMPORT_NAME`, `IMPORT_FROM`, `IMPORT_STAR`. Defer
  to the import system port (1683).
* [~] Type alias / TypeVar / PEP 695: `INTERPRETER_EXIT`,
  `LOAD_CLOSURE`, `LOAD_LOCALS`, `LOAD_FROM_DICT_OR_GLOBALS`,
  `LOAD_FROM_DICT_OR_DEREF`, `LOAD_COMMON_CONSTANT` shipped.
  `TYPE_ALIAS`, `INSTRUMENTED_LOAD_SUPER_ATTR` reach through the
  intrinsics table; bodies ship in 1689.
* [x] Intrinsic dispatch: `CALL_INTRINSIC_1`, `CALL_INTRINSIC_2`
  routed through `intrinsics.UnaryTable` / `BinaryTable`. Most
  helpers stay stubs until their owning blocks land;
  `UnaryListToTuple` is wired.

### Surface guarantees

* [x] `EvalCode(ts, co, globals, nil)` runs hand-built bytecode
  end-to-end through the v0.6 release gate
  (`gopy -c "print(1+2)"` prints `3`). Pinned by
  `vmtest/smoke_test.go::TestSmokeReleaseV06` and the
  `vmtest/gate_test.go` panel (Constant, Arithmetic, IfElse,
  ListBuild, FString). The v0.5 disassembly golden corpus
  comparison waits on parser rule-body emission (1640).
* [~] Exception table walk: round-trip parity with the writer side
  pinned by `vm/exctable_test.go`. The CPython golden corpus
  comparison still needs `vm/exception_table_test.go`.
* [n] Generator state machine: `g = gen(); next(g); next(g); ...`
  visits the same bytecode offsets in the same order as CPython.
  Defers to objects.Generator (1687) plus the pending YIELD_VALUE
  / SEND / RETURN_GENERATOR handlers tracked in #193.
* [n] Async coroutine state machine: same shape as generator,
  same defer.
* [x] Eval breaker fires at every `RESUME` and at every backward
  `JUMP_BACKWARD`, plus the unconditional top-of-loop poll;
  `JUMP_BACKWARD_NO_INTERRUPT` skips the per-arm poll. Pinned by
  `vm/eval_breaker_test.go` (top-of-loop, JUMP_BACKWARD, RESUME,
  no-interrupt skip, no-bit no-drain).
* [x] Line table walk: round-trip parity with the writer pinned by
  `vm/positions_test.go`, which builds curated `*compile.Sequence`
  fixtures, runs them through `compile.AssembleLineTable`, and walks
  every byte offset to assert the reader reproduces the writer's
  (line, endLine, column, endColumn) tuples across all five PEP 626
  record formats (short, oneline, no-column, long, none) plus
  multi-record split spans.
* [x] `EvalCode` is goroutine-safe for distinct calls; one
  `evalState` is not safe for concurrent use. Pinned by
  `TestEvalCodeGoroutineSafety` (32 goroutines × shared `*Code`).

### Out of scope for v0.6

* `INSTRUMENTED_*` opcodes execute their non-instrumented base
  case. Real monitoring lands in 1634 at v0.9.
* `ENTER_EXECUTOR`: falls through. Tier-2 lands in 1632 at v0.12.
* Adaptive specialization: adaptive variants reduce to base case.
  Lands in 1631 at v0.11.

### Cross-references

* Generated dispatch table: 1621.
* Frame storage: 1637.
* Stack reference values: 1638.
* GIL and eval breaker: 1639.
* Intrinsic dispatch: 1635.
* Vectorcall protocol: 1684 (Objects block).
* Code / Frame / Generator / Cell objects: 1687 (Objects block).
