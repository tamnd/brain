---
title: "gopy type"
description: "Type, slots, MRO, lookup. Mirrors PyTypeObject from cpython/Include/cpython/typeobject.h."
tags: ["gopy", "spec"]
weight: 1672
---

# 1672. Type and slots

## What we are porting

`PyTypeObject` is the meta-class. Every Python value has an `ob_type`
pointing to its `PyTypeObject`. The type carries slots: function pointers
for arithmetic, comparison, hashing, calling, attribute access, and so
on. Slots are the dispatch table that drives the entire object protocol.

CPython has roughly 80 slots split across `tp_*` (type-level), `nb_*`
(numeric protocol, `PyNumberMethods`), `sq_*` (sequence,
`PySequenceMethods`), `mp_*` (mapping, `PyMappingMethods`), `am_*`
(async, `PyAsyncMethods`), `bf_*` (buffer).

v0.2 ships only the slots needed by the gate plus the fields used by every
type. The rest land slot-by-slot as later phases need them.

## v0.2 slot table

```go
type Type struct {
    Header

    Name     string  // tp_name
    BaseSize int     // tp_basicsize, used by GC sizing later
    ItemSize int     // tp_itemsize, for VarObject types

    Bases    []*Type // tp_bases
    MRO      []*Type // tp_mro

    Repr      func(o Object) (string, error)            // tp_repr
    Str       func(o Object) (string, error)            // tp_str
    Hash      func(o Object) (int64, error)             // tp_hash
    RichCmp   func(a, b Object, op CompareOp) (Object, error) // tp_richcompare
    Iter      func(o Object) (Object, error)            // tp_iter
    IterNext  func(o Object) (Object, error)            // tp_iternext
    Call      func(o Object, args []Object, kwargs map[string]Object) (Object, error) // tp_call
    Dealloc   func(o Object)                            // tp_dealloc

    Number   *NumberMethods   // tp_as_number
    Sequence *SequenceMethods // tp_as_sequence
    Mapping  *MappingMethods  // tp_as_mapping
}
```

Slots are nil when the type does not implement them. CPython uses
`NULL` the same way.

The remaining slots (getattro, setattro, descr_get, descr_set, init,
new, alloc, free, traverse, clear, finalize, weaklist, dict, mro_entries,
init_subclass, set_name, vectorcall) arrive in later phases:

- `init`, `new`, `alloc`: v0.7 once we have a parser.
- `getattro`, `setattro`, `descr_*`: v0.2 covers attribute access only as
  needed by the gate. Full descriptor protocol is v0.4.
- `traverse`, `clear`, `finalize`, `weaklist`: v0.10 (cycle GC).
- `vectorcall`: v0.6 (VM Tier-1 fast call path).

## CompareOp

```go
type CompareOp int

const (
    CompareLT CompareOp = iota
    CompareLE
    CompareEQ
    CompareNE
    CompareGT
    CompareGE
)
```

Same numeric values as CPython's `Py_LT`/`Py_LE`/.../`Py_GE` (0..5).

## NumberMethods, SequenceMethods, MappingMethods

These are smaller slot bundles. v0.2 needs a subset:

```go
type NumberMethods struct {
    Add      func(a, b Object) (Object, error)
    Subtract func(a, b Object) (Object, error)
    Multiply func(a, b Object) (Object, error)
    Negative func(o Object) (Object, error)
    Bool     func(o Object) (bool, error)
    Int      func(o Object) (Object, error)
    Float    func(o Object) (Object, error)
}

type SequenceMethods struct {
    Length    func(o Object) (int, error)
    Concat    func(a, b Object) (Object, error)
    Repeat    func(o Object, n int) (Object, error)
    GetItem   func(o Object, i int) (Object, error)
    SetItem   func(o Object, i int, v Object) error
    Contains  func(o, v Object) (bool, error)
}

type MappingMethods struct {
    Length    func(o Object) (int, error)
    GetItem   func(o, key Object) (Object, error)
    SetItem   func(o, key, v Object) error
    DelItem   func(o, key Object) error
}
```

Add/Subtract/Multiply lack reflected variants here because the abstract
layer (`abstract/numeric.go`) handles fallback to the right operand's
type. CPython does the same in `BINARY_OP1`.

## MRO

`tp_mro` is the C3 linearization of `tp_bases`. v0.2 lands C3 in
`typeobj/mro.go` ported from `Objects/typeobject.c:mro_implementation`.

For built-in types in v0.2 the MRO is trivial: each type's bases is
`[object]`, except `bool` which is `[int]` and `object` which has no
base. C3 still runs to keep the path identical.

```
type.mro(int) == [int, object]
type.mro(bool) == [bool, int, object]
type.mro(tuple) == [tuple, object]
```

## Slot lookup

`lookup_maybe_method` walks the MRO. v0.2 has no Python-defined types
yet, so this is a degenerate walk: just check `tp_<slot>` on the type
itself, fall through to bases. We still ship the walk because v0.3
exceptions and v0.5 user types depend on it.

```go
func (t *Type) Lookup(slot string) Object { ... }
```

## What "subtype" means in v0.2

Pure read-only subtype checks (`isinstance(x, T)`) need a base-walk only.
v0.2 supports those. Subtype creation (`type(name, bases, dict)`)
requires `tp_new`/`tp_init`/`tp_alloc` which arrive in v0.7.

## File mapping

| C source                              | Go target                       |
|---------------------------------------|---------------------------------|
| `Include/cpython/typeobject.h`        | `objects/type.go` (struct)      |
| `Objects/typeobject.c:type_repr`      | `typeobj/repr.go`               |
| `Objects/typeobject.c:type_call`      | `typeobj/call.go`               |
| `Objects/typeobject.c:mro_*`          | `typeobj/mro.go`                |
| `Objects/typeobject.c:lookup_maybe_*` | `typeobj/lookup.go`             |
| `Objects/typeobject.c:type_getattro`  | `typeobj/getattr.go` (v0.4)     |
| `Objects/typeobject.c:type_new`       | `typeobj/new.go` (v0.7)         |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/type.go`: `Type` struct with the v0.2 slot subset.
  Landed for the v0.2 gate; Number / Sequence / Mapping bundles still
  partially typed.
* [~] `objects/compareop.go`: `CompareOp` constants (CompareLT..GE)
  pinned to CPython's 0..5.
* [ ] `objects/numbermethods.go`: full `NumberMethods` matching
  `PyNumberMethods` field-for-field, not just the v0.2 subset.
* [ ] `objects/sequencemethods.go`: full `SequenceMethods`.
* [ ] `objects/mappingmethods.go`: full `MappingMethods`.
* [~] `typeobj/mro.go`: C3 linearisation. Trivial-base path landed;
  multi-base panel pending the v0.7 user-type port.
* [~] `typeobj/lookup.go`: `Lookup(slot)` MRO walk. v0.2 degenerate
  path landed; the descriptor-aware walk lands in v0.4.
* [ ] `typeobj/repr.go`: `type_repr` (`<class 'foo'>` formatting).
* [ ] `typeobj/call.go`: `type_call` (instance creation via
  `tp_new` + `tp_init`).
* [ ] `typeobj/getattr.go`: `type_getattro` with the data-descriptor
  beats instance dict beats non-data-descriptor ordering.
* [ ] `typeobj/new.go`: `type_new`, `type.__init__`, the metaclass
  resolution rule.
* [ ] `typeobj/inherit.go`: slot inheritance + `inherit_slots`
  fixpoint that CPython runs at type-creation time.

### Surface guarantees

* [x] `CompareOp` numeric values match `Py_LT..Py_GE` (0..5).
* [ ] `type.__mro__` matches CPython's C3 output for every multi-base
  pattern in `Lib/test/test_descr.py`. Pinned by
  `compat/mro_test.go`.
* [ ] `Lookup` returns the same descriptor that `_PyType_Lookup`
  returns, including for slot wrappers that live on `object`.
* [ ] `type_repr` produces `<class 'name'>` exactly, including module
  prefix for non-builtin types.
* [ ] Slot inheritance fixpoint converges in the same iteration count
  as CPython for the builtin hierarchy. Diagnostic only; not
  user-observable.

### Out of scope for v0.2

* `tp_new`, `tp_init`, `tp_alloc`, `tp_free`. Land in v0.7 alongside
  user-defined types.
* `tp_traverse`, `tp_clear`, `tp_finalize`, `tp_weaklistoffset`,
  `tp_dictoffset`. Land in v0.10 with cycle GC and weakrefs.
* `tp_vectorcall_offset`, `tp_vectorcall`. Land in v0.6 with the VM
  Tier-1 fast call path.
* `tp_descr_get`, `tp_descr_set`. Land in v0.4 with the descriptor
  protocol port.
* Metaclass resolution beyond `type` itself. Lands in v0.7.
