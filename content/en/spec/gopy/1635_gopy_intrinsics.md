---
title: "gopy intrinsics"
description: "Port of cpython/Python/intrinsics.c. The CALL_INTRINSIC_1 / CALL_INTRINSIC_2 dispatch tables that back compile-time-emitted runtime helpers (print expr, list-to-tuple, import-star, type-alias)."
tags: ["gopy", "spec"]
weight: 1635
---

# 1635. Intrinsic dispatch

## What we are porting

`Python/intrinsics.c` (~400 lines). Two opcodes, `CALL_INTRINSIC_1`
and `CALL_INTRINSIC_2`, are emitted by the compiler in places where
a runtime helper is cleaner than a dedicated opcode. The oparg
selects which helper to call.

This is a small, well-bounded surface. The helper set is closed:
about 10 unary intrinsics and 4 binary intrinsics. CPython adds
to it sparingly (one or two per release), so a hand-port plus a
table is cheaper than codegen.

## The unary intrinsic table

`CALL_INTRINSIC_1 oparg`: pop one value, push one.

| ID                              | Helper                                       |
|---------------------------------|----------------------------------------------|
| `INTRINSIC_1_INVALID`           | guard; raises if reached                     |
| `INTRINSIC_PRINT`               | print expression result (REPL displayhook)   |
| `INTRINSIC_IMPORT_STAR`         | implements `from x import *`                 |
| `INTRINSIC_STOPITERATION_ERROR` | re-raise StopIteration as RuntimeError       |
| `INTRINSIC_ASYNC_GEN_WRAP`      | wrap value for async generator yield         |
| `INTRINSIC_UNARY_POSITIVE`      | `+x` (rare; usually inlined)                 |
| `INTRINSIC_LIST_TO_TUPLE`       | freeze a list comprehension into a tuple     |
| `INTRINSIC_TYPEVAR`             | PEP 695 `TypeVar(...)`                       |
| `INTRINSIC_PARAMSPEC`           | PEP 695 `ParamSpec(...)`                     |
| `INTRINSIC_TYPEVARTUPLE`        | PEP 695 `TypeVarTuple(...)`                  |
| `INTRINSIC_SUBSCRIPT_GENERIC`   | PEP 695 `Generic[T]` subscription            |
| `INTRINSIC_TYPEALIAS`           | PEP 695 `type X = ...`                       |

## The binary intrinsic table

`CALL_INTRINSIC_2 oparg`: pop two, push one.

| ID                               | Helper                                      |
|----------------------------------|---------------------------------------------|
| `INTRINSIC_2_INVALID`            | guard                                       |
| `INTRINSIC_PREP_RERAISE_STAR`    | ExceptionGroup re-raise prep                |
| `INTRINSIC_TYPEVAR_WITH_BOUND`   | `TypeVar('T', bound=int)`                   |
| `INTRINSIC_TYPEVAR_WITH_CONSTRAINTS` | `TypeVar('T', int, str)`                |
| `INTRINSIC_SET_FUNCTION_TYPE_PARAMS` | wire generic type params onto a function |

(IDs come from `Include/internal/pycore_intrinsics.h`. Numeric
values must match CPython byte-for-byte so emitted bytecode loads
the right entry.)

## Go shape

```go
// Unary is the CALL_INTRINSIC_1 entry. The eval loop reads
// UnaryTable[oparg] and calls it.
type Unary func(ts *state.Thread, v object.Object) (object.Object, error)

// Binary is the CALL_INTRINSIC_2 entry.
type Binary func(ts *state.Thread, lhs, rhs object.Object) (object.Object, error)

// UnaryTable is the dispatch table for CALL_INTRINSIC_1.
// Indexed by INTRINSIC_* enum value; entries match
// _PyIntrinsics_UnaryFunctions from Python/intrinsics.c.
var UnaryTable = [...]Unary{
    Unary1Invalid,
    UnaryPrint,
    UnaryImportStar,
    UnaryStopIterationError,
    UnaryAsyncGenWrap,
    UnaryUnaryPositive,
    UnaryListToTuple,
    UnaryTypevar,
    UnaryParamspec,
    UnaryTypevartuple,
    UnarySubscriptGeneric,
    UnaryTypealias,
}

// BinaryTable is the dispatch table for CALL_INTRINSIC_2.
var BinaryTable = [...]Binary{
    Binary2Invalid,
    BinaryPrepReraiseStar,
    BinaryTypevarWithBound,
    BinaryTypevarWithConstraints,
    BinarySetFunctionTypeParams,
}
```

The eval loop dispatch is one indexed call:

```go
case opcode.CALL_INTRINSIC_1:
    v := e.popObject()
    res, err := intrinsics.UnaryTable[oparg](e.ts, v)
    if err != nil {
        return 0, err
    }
    e.pushObject(res)
    return e.advance(1), nil
```

## File mapping

| C source                                          | Go target                          |
|---------------------------------------------------|------------------------------------|
| `Python/intrinsics.c` (unary table + helpers)     | `intrinsics/unary.go`              |
| `Python/intrinsics.c` (binary table + helpers)    | `intrinsics/binary.go`             |
| `Include/internal/pycore_intrinsics.h` (enum)     | `intrinsics/ids.go`                |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `intrinsics/ids.go`: `INTRINSIC_*` constants matching
  `pycore_intrinsics.h` numerically (12 unary, 6 binary, MAX_INTRINSIC_*).
* [x] `intrinsics/unary.go`: `Unary` type, `UnaryTable`, every
  unary helper (`UnaryPrint`, `UnaryImportStar`, ...). Bodies stubbed
  with notImplementedError pending cross-block prereqs.
* [x] `intrinsics/binary.go`: `Binary` type, `BinaryTable`, every
  binary helper. Includes BinarySetTypeparamDefault (3.13+).
* [x] `intrinsics/intrinsics.go`: `notImplementedError` shared
  between unary and binary stubs.
* [x] `intrinsics/intrinsics_test.go`: ID-value pinning, table
  population, invalid-ID error path, every stub returns
  notImplementedError.

### Unary panel

* [n] `UnaryPrint`: calls `sys.displayhook`. Defers to the `sys`
  module port (1651). Stub returns `notImplementedError`.
* [n] `UnaryImportStar`: walks `__all__` and copies into locals.
  Defers to the import system port (1683). Stub.
* [n] `UnaryStopIterationError`: wraps StopIteration in a
  RuntimeError (PEP 479). Defers to the exception module port
  (1686). Stub.
* [n] `UnaryAsyncGenWrap`: builds `_PyAsyncGenWrappedValue`.
  Defers to the async-generator object (1687). Stub.
* [n] `UnaryUnaryPositive`: `+x` via `__pos__`. Defers to the
  number-protocol slot dispatch (1684). Stub.
* [x] `UnaryListToTuple`: freezes a list comprehension into a
  tuple. Implemented in `intrinsics/unary.go`; consumed by the
  `LIST_TO_TUPLE` lowering in `vm/eval_simple.go`.
* [n] `UnaryTypevar` / `UnaryParamspec` / `UnaryTypevartuple` /
  `UnarySubscriptGeneric` / `UnaryTypealias`: PEP 695 type
  runtime objects. Defer to 1689. Stubs.

### Binary panel

* [n] `BinaryPrepReraiseStar`: reconstructs an ExceptionGroup
  for `raise except*` re-raise. Defers to the ExceptionGroup
  type (1686). Stub.
* [n] `BinaryTypevarWithBound`, `BinaryTypevarWithConstraints`,
  `BinarySetFunctionTypeParams`, `BinarySetTypeparamDefault`:
  PEP 695 helpers. Defer to 1689. Stubs.

### Surface guarantees

* [x] Numeric IDs match
  `Include/internal/pycore_intrinsics.h` byte-for-byte. Pinned
  by `intrinsics_test.go::TestUnaryIDValues` and
  `TestBinaryIDValues` (every entry plus `MaxUnary`/`MaxBinary`).
* [x] Each stubbed helper returns `notImplementedError`. Pinned
  by `TestStubHelpersReturnNotImplemented` (sweeps both tables,
  skips the implemented `UnaryListToTuple`).
* [n] PEP 695 helpers (Typevar / Paramspec / Typevartuple /
  Typealias) build runtime objects whose `repr` matches
  CPython's. Defers to 1689; stubs return `notImplementedError`
  in v0.6.

### Out of scope for v0.6

* Specialized variants: `INSTRUMENTED_CALL_INTRINSIC_*`. Falls
  back to base case until 1634 (monitoring) lands at v0.9.

### Cross-references

* Eval loop dispatch: 1636.
* PEP 695 type runtime objects: 1689 (typevar, generic alias).
* ExceptionGroup type: 1686.
* `sys.displayhook`: 1651 (sys module).
