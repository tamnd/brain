---
title: "gopy vm remaining bytecodes"
description: "Bytecodes ported in v0.9 that finish the Tier-1 panel: import, generator, pattern-match, with/finally, set builders, and the async-protocol stubs."
tags: ["gopy", "spec"]
weight: 1693
---

# 1693. Remaining Tier-1 bytecodes

## What we are porting

Five panels of opcodes from `cpython/Python/bytecodes.c` that the v0.6
VM left as `ErrNotImplemented` placeholders. With v0.8 the import
machinery (1691) became real, which unblocked `IMPORT_*`. The rest
land here.

| Panel        | Opcodes                                                                | CPython lines |
|--------------|------------------------------------------------------------------------|---------------|
| Import       | IMPORT_NAME, IMPORT_FROM, IMPORT_STAR (intrinsic)                      | 2863, 2873    |
| Generator    | RETURN_GENERATOR, YIELD_VALUE, SEND, GET_YIELD_FROM_ITER, CLEANUP_THROW | 4982, 1370, 1297, 3091, 1471 |
| Pattern      | MATCH_MAPPING, MATCH_SEQUENCE, MATCH_KEYS, MATCH_CLASS                 | 3062, 3067, 3072, 3043 |
| With/finally | WITH_EXCEPT_START                                                      | 3524          |
| Set          | BUILD_SET, SET_ADD, SET_UPDATE                                         | 2034, 1058, 2027 |
| Async stubs  | GET_AWAITABLE, GET_AITER, GET_ANEXT, END_ASYNC_FOR                     | 1274, 1230, 1266, 1442 |

The async opcodes are deferred (full coroutine protocol lands in v0.10
with cycle GC and weakref). v0.9 ships error-returning stubs that
match the rest of the dispatch contract.

## Wiring

The dispatch panels live in three new files:

| File                   | What                                                              |
|------------------------|-------------------------------------------------------------------|
| `vm/eval_import.go`    | `tryImport`: IMPORT_NAME, IMPORT_FROM. IMPORT_STAR is special-cased in CALL_INTRINSIC_1. |
| `vm/eval_gen.go`       | `tryGen`: generator + with-except + async stubs                   |
| `vm/eval_match.go`     | `tryMatch`: MATCH_MAPPING / SEQUENCE / KEYS / CLASS               |

`vm/dispatch.go` consults them in order before falling back to the
generated arms in `vm/opcodes_gen.go`. Set opcodes were already wired
into the `eval_simple.go` panel; v0.9 only swaps the stubs for real
implementations now that `objects.Set` exists.

## Generator architecture

CPython suspends a generator by leaving its frame on the heap and
storing the instruction pointer in `gen->gi_frame_state`. Resuming a
generator restores that frame on the C stack and jumps to the saved
ip. Coroutines and async generators share the same machinery.

gopy can not switch C stacks. Instead each generator runs on its own
goroutine and synchronises with the caller through two buffered
channels:

```go
type GenMsg struct {
    Val Object
    Err error  // ErrStopIteration on normal completion
}

type Generator struct {
    Header
    Name    string
    YieldCh chan GenMsg  // generator -> caller
    SendCh  chan GenMsg  // caller -> generator
    ...
}
```

`RETURN_GENERATOR` detaches the current frame from the chunk arena
(via `frame.FrameStack.Detach`, prepared in 1637 v0.6), creates a
`Generator`, and spawns a goroutine that:

1. Blocks on `<-SendCh` for the priming `Send(None)` call.
2. Builds a fresh `evalState` whose `genYield` and `genSend` fields
   point at the generator's channels, then runs the saved frame.
3. On normal return or `ErrStopIteration`, writes
   `GenMsg{Err: ErrStopIteration}` on `YieldCh`.
4. On any other error, writes that error on `YieldCh`.

`YIELD_VALUE` pops the value, sends it on `genYield`, blocks on
`genSend`, and pushes the received value as the result of the yield
expression. `SEND` runs through `Generator.Send` for `*Generator`
receivers and through `tp_iternext` / `__send__` for everything else;
`StopIteration` jumps past the matching `END_SEND` by `oparg + 1`.
`CLEANUP_THROW` extracts a `StopIteration` value or re-raises.
`GET_YIELD_FROM_ITER` is `iter()` for non-generators and a no-op for
generators.

The goroutine model means each generator costs one OS-thread-shaped
goroutine while it is alive. Goroutines are cheap (a few KB of stack)
but not free; future work (post-v0.9) can flip to a stackless
green-thread scheduler if profiling demands it.

## Pattern matching

`MATCH_MAPPING` and `MATCH_SEQUENCE` consult two new flags on
`objects.Type.TpFlags` (`TpFlagMapping = 1 << 6`,
`TpFlagSequence = 1 << 5`) that mirror `Py_TPFLAGS_MAPPING` and
`Py_TPFLAGS_SEQUENCE` from `Include/object.h`. v0.9 sets them on
`DictType` (mapping) and `ListType` plus `TupleType` (sequence). The
match opcodes leave the subject on the stack and push a Bool.

`MATCH_KEYS` walks a keys tuple and looks each up via the mapping
protocol; missing key short-circuits to `None`. `MATCH_CLASS`
isinstance-checks against the type operand, then extracts positional
attributes via `__match_args__` and keyword attributes via the names
tuple. Any failed lookup short-circuits to `None`. The v0.9
isinstance check handles type identity plus a one-level `Bases`
walk; full MRO arrives with the type-system port (1672).

## WITH_EXCEPT_START

Five-element stack layout: `exit_fn, exit_self, lasti, unused, exc_val`.
Calls `exit_fn(type(exc), exc, None)` and pushes the result. The
traceback argument is `None` because traceback objects do not exist
yet (they arrive with the exceptions polish in v0.10). The exit
function is `peek(4)` below TOS.

## IMPORT_STAR

The intrinsic table entry shape is `func(ts *state.Thread, v Object)`,
which has no frame access. v0.9 special-cases `UnaryImportStarID`
inside the `CALL_INTRINSIC_1` arm so `e.importStar(v)` can read and
write the current frame's locals. The body lives in
`vm/eval_import.go` and follows `Python/intrinsics.c:124 import_star`:
prefer `__all__`, fall back to `__dict__` while skipping names that
start with `_`, and `SetItem` each name into the destination dict.

## Set opcodes

`BUILD_SET oparg` pops `oparg` items, adds each to a fresh
`objects.NewSet`, and pushes it. `SET_ADD oparg` pops the value
and adds it to the set at `peek(oparg-1)`. `SET_UPDATE oparg` pops
an iterable, expands it via `iterToSlice`, and adds every item.
The set lives at the same depth pattern as `LIST_APPEND` /
`LIST_EXTEND`; `oparg` is the depth from TOS to the target.

## Gate

Tests in `vm/eval_test.go`:

* `TestEvalGenerator`: build a code object that yields once, evaluate
  it to get a `*objects.Generator`, drive it with `Send(None)` until
  `ErrStopIteration`. Assert the yielded value and the terminating
  error.
* `TestEvalMatchMapping`, `TestEvalMatchSequence`: push a dict / list
  and assert the boolean push.
* `TestEvalMatchKeys`: extract two keys from a dict; assert the
  resulting tuple. Add a missing-key case asserting `None`.
* `TestEvalBuildSet`, `TestEvalSetAdd`, `TestEvalSetUpdate`: assert
  the set contents and length after each opcode.
* `TestEvalImportStar`: import a fixture module exposing `__all__`
  and assert the current frame's locals receive the listed names.
* `TestEvalGetYieldFromIter`: pass through a generator unchanged;
  call `iter()` on a list.

End-to-end gate (`vmtest/cpython_smoke`) covers a generator function
and a `match` statement.

## Out of scope

* Async iterator protocol (`GET_AITER`, `GET_ANEXT`, `END_ASYNC_FOR`)
  and full coroutine awaitable conformance (`GET_AWAITABLE`). v0.10
  with weakref / finalize support.
* `__match_args__` lookup that descends the MRO. v0.10 with the
  full type-system port.
* `WITH_EXCEPT_START` traceback argument. Becomes real when the
  traceback object lands.
* SEND specialisation (`SEND_GEN`). The v0.6 spec already excluded
  Tier-1 specialisation; v0.11.

## v0.9 checklist

### Files

* [x] `objects/generator.go`: `Generator` type, `GenMsg`, `Send`,
  `Close`, `genIterNext`, `genRepr`. `GeneratorType` registered.
* [x] `objects/type.go`: `TpFlags uint64` plus `TpFlagMapping` /
  `TpFlagSequence` constants.
* [x] `objects/dict.go`, `list.go`, `tuple.go`: set
  `TpFlagMapping` / `TpFlagSequence` in `init`.
* [x] `vm/eval.go`: `genYield` / `genSend` channel fields on
  `evalState`.
* [x] `vm/eval_gen.go`: `tryGen` panel.
* [x] `vm/eval_match.go`: `tryMatch` panel.
* [x] `vm/eval_import.go`: `tryImport` plus `importStar` helper.
* [x] `vm/dispatch.go`: wire `tryGen`, `tryMatch` after `tryImport`.
* [x] `vm/eval_simple.go`: real `BUILD_SET` / `SET_ADD` /
  `SET_UPDATE` arms; `IMPORT_STAR` special-case in
  `CALL_INTRINSIC_1`.

### Tests

* [x] Generator yield+resume+exhaust roundtrip
  (`TestEvalGenerator`, `TestEvalGetYieldFromIterPassesGenerator`,
  `TestEvalGetYieldFromIterCallsIter`).
* [x] Pattern-match: mapping flag (`TestEvalMatchMapping`),
  sequence flag (`TestEvalMatchSequence`,
  `TestEvalMatchSequenceFalse`), key extraction
  (`TestEvalMatchKeys`, `TestEvalMatchKeysMissing`), class match
  positional + keyword (`TestEvalMatchClassPositionalPlusKeyword`,
  `TestEvalMatchClassNotInstancePushesNone`).
* [x] Set builders (`TestEvalBuildSet`, `TestEvalSetAdd`,
  `TestEvalSetUpdate`).
* [x] `from x import *` exercising `__all__` and `__dict__`
  paths (`TestEvalImportStarUsesAll`,
  `TestEvalImportStarFallsBackToDict`).
* [x] `WITH_EXCEPT_START` calling a fake `__exit__`
  (`TestEvalWithExceptStartDispatchesExitFn`).
* [x] Async-stub opcodes return errors that mention "v0.9"
  (`TestEvalAsyncStubsMentionV09`).
