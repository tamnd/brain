---
title: "gopy objects misc"
description: "Port of the remaining cpython/Objects/ files. weakref, memoryview, file, picklebuffer, typevar / TypeAliasType, union, GenericAlias, Interpolation / Template, plus the obmalloc stub."
tags: ["gopy", "spec"]
weight: 1689
---

# 1689. Object misc (weakref, memoryview, file, typing, templates, obmalloc)

## What we are porting

Ten files, ~7500 lines combined. The "everything else" of `Objects/`:

* `Objects/weakrefobject.c`: weak references, weakref proxies,
  callback chains. v0.10 along with cycle GC.
* `Objects/memoryobject.c`: `memoryview`. The buffer-protocol
  consumer. v0.10.
* `Objects/fileobject.c`: small set of file-object helpers
  (`PyFile_WriteObject`, `PyFile_GetLine`). The actual file types
  come from `io/` stdlib; this file is just glue.
* `Objects/picklebufobject.c`: `PickleBuffer` (PEP 574 out-of-band
  buffer). Used by `pickle.dumps` with `protocol=5`.
* `Objects/typevarobject.c`: PEP 695 `TypeVar`, `TypeVarTuple`,
  `ParamSpec`, plus `TypeAliasType`. Lands when type-params are
  reachable through real syntax (v0.7 alongside class creation).
* `Objects/unionobject.c`: `types.UnionType` (the result of `int |
  str`, PEP 604).
* `Objects/genericaliasobject.c`: `types.GenericAlias` (the result
  of `list[int]`, PEP 585).
* `Objects/interpolationobject.c`: `Interpolation` (PEP 750
  t-string field).
* `Objects/templateobject.c`: `Template` (PEP 750 t-string
  result type).
* `Objects/obmalloc.c`: small-block allocator. Stub only; Go GC
  does the work.

## Why this exists as one spec

These ten files are independent of each other and small. Bundling
them keeps the per-spec count manageable. Each gets its own
checklist sub-section below.

## Phasing

| File                    | Phase | Notes                              |
|-------------------------|-------|------------------------------------|
| typevarobject.c         | v0.7  | needs class creation               |
| unionobject.c           | v0.7  | created by `type.__or__`           |
| genericaliasobject.c    | v0.7  | created by `type.__class_getitem__`|
| interpolationobject.c   | v0.7  | needed by 1644                     |
| templateobject.c        | v0.7  | needed by 1644                     |
| fileobject.c            | v0.8  | needs io/                          |
| picklebufobject.c       | v0.8  | needs marshal/pickle               |
| weakrefobject.c         | v0.10 | needs cycle GC                     |
| memoryobject.c          | v0.10 | needs buffer protocol everywhere   |
| obmalloc.c              | v0.10+| stub; Go GC subsumes               |

## Go shape (key types)

```go
// WeakRef mirrors PyWeakReference.
type WeakRef struct {
    Header
    Object   Object        // strong while alive; cleared on death
    Callback Object        // optional callback
    Hash     int64
    Prev     *WeakRef      // intra-list link
    Next     *WeakRef
}

// MemoryView mirrors PyMemoryViewObject. Wraps a buffer export.
type MemoryView struct {
    VarHeader
    View    BufferView   // shape, strides, format, ndim, etc.
    Flags   uint32
}

// PickleBuffer mirrors PyPickleBufferObject.
type PickleBuffer struct {
    Header
    View BufferView
}

// TypeVar mirrors PyTypeVarObject.
type TypeVar struct {
    Header
    Name        *Str
    Bound       Object
    Constraints *Tuple
    Default     Object  // PEP 696
    InferVariance bool
    Covariant     bool
    Contravariant bool
}

// UnionType mirrors PyUnionObject.
type UnionType struct {
    Header
    Args     *Tuple
    Hashable bool
}

// GenericAlias mirrors Py_GenericAlias.
type GenericAlias struct {
    Header
    Origin    Object
    Args      *Tuple
    Parameters *Tuple
    Starred   bool
}

// Interpolation mirrors string.templatelib.Interpolation.
type Interpolation struct {
    Header
    Value      Object
    Expression *Str
    Conversion Object  // None or 'r'/'s'/'a'
    FormatSpec *Str
}

// Template mirrors string.templatelib.Template.
type Template struct {
    Header
    Strings        *Tuple  // *Str
    Interpolations *Tuple  // *Interpolation
}
```

## File mapping

| C source                            | Go target                                |
|-------------------------------------|------------------------------------------|
| `Objects/weakrefobject.c`           | `objects/weakref.go`                     |
| `Objects/memoryobject.c`            | `objects/memoryview.go`                  |
| `Objects/fileobject.c`              | `objects/file_glue.go`                   |
| `Objects/picklebufobject.c`         | `objects/picklebuf.go`                   |
| `Objects/typevarobject.c`           | `objects/typevar.go`                     |
| `Objects/unionobject.c`             | `objects/union.go`                       |
| `Objects/genericaliasobject.c`      | `objects/genericalias.go`                |
| `Objects/interpolationobject.c`     | `objects/interpolation.go`               |
| `Objects/templateobject.c`          | `objects/template.go`                    |
| `Objects/obmalloc.c`                | `objects/obmalloc_stub.go`               |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### typevarobject.c (v0.7)

* [ ] `objects/typevar.go`: TypeVar, TypeVarTuple, ParamSpec,
  TypeAliasType, plus the constructor that the
  `INTRINSIC_TYPEVAR` opcode calls.
* [ ] PEP 696 default values.
* [ ] Variance flags (`covariant`, `contravariant`,
  `infer_variance`).

### unionobject.c (v0.7)

* [ ] `objects/union.go`: UnionType, `__or__` chain that flattens
  nested unions, `__args__`, `__parameters__`, `__hash__` /
  `__eq__` over an order-insensitive set comparison.

### genericaliasobject.c (v0.7)

* [ ] `objects/genericalias.go`: `__class_getitem__` factory,
  `__args__`, `__origin__`, `__parameters__`,
  `__getitem__` for nested subscripts (e.g. `list[T][int]`).

### interpolationobject.c, templateobject.c (v0.7)

* [ ] `objects/interpolation.go`: PEP 750 Interpolation node.
* [ ] `objects/template.go`: Template, `+` concatenation rules,
  iteration that interleaves strings and interpolations.

### fileobject.c (v0.8)

* [ ] `objects/file_glue.go`: PyFile_WriteObject equivalent
  (`io.write_object_to_file`), PyFile_GetLine.

### picklebufobject.c (v0.8)

* [ ] `objects/picklebuf.go`: PickleBuffer with raw / readonly
  views, used by pickle protocol 5.

### weakrefobject.c (v0.10)

* [ ] `objects/weakref.go`: WeakRef, WeakProxy, weakref callback
  chain, weakref-list head on `Type` (`tp_weaklistoffset`
  equivalent).
* [ ] Callback fires after `__del__`, before deallocation.
* [ ] WeakValueDictionary / WeakKeyDictionary helpers.

### memoryobject.c (v0.10)

* [ ] `objects/memoryview.go`: BufferView shape struct, slice
  semantics, format-string parsing, casting (`memoryview.cast`),
  contiguous-vs-strided dispatch.

### obmalloc.c (v0.10+)

* [ ] `objects/obmalloc_stub.go`: `PyObject_Malloc`,
  `PyObject_Free`, `PyMem_Malloc`, `PyMem_Free` redirecting to
  Go's allocator. The free-threaded mimalloc path is N/A.

### Surface guarantees

* [ ] `weakref.ref(obj)()` returns `obj` while alive, `None`
  after death; callback fires once.
* [ ] `memoryview(b'abc')[1] == ord('b')`; slicing and casting
  match CPython's strides table.
* [ ] `int | str` produces a UnionType whose hash matches
  `hash(typing.Union[int, str])` per CPython.
* [ ] `list[int].__origin__ is list`,
  `list[int].__args__ == (int,)`.
* [ ] `t"hello {name}"` produces a Template with `.strings ==
  ('hello ', '')` and `.interpolations[0].expression == 'name'`.
* [ ] `hash(TypeVar('T')) != hash(TypeVar('T'))` (TypeVars are
  identity-keyed).

### Cross-references

* TypeAlias compile-time path: 1620 codegen (TypeAlias visitor).
* String parser t-string emission: 1644.
* Buffer protocol exposers: 1676 (bytes), 1677 (str), 1689 (the
  consumer side here).

### Out of scope

* `_typing` accelerator module (separate from `typing.py`).
  Stdlib bridge, not part of `Objects/`.
* `gc` module Python surface. The Go-side cycle collector lives
  in `gc/` (1611 series adjacent).
