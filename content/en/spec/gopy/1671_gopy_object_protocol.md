---
title: "gopy object protocol"
description: "Object interface, Header, VarHeader, refcount, and identity. Mirrors PyObject and PyVarObject in cpython/Include/object.h."
tags: ["gopy", "spec"]
weight: 1671
---

# 1671. Object protocol

## What we are porting

`cpython/Include/object.h` and `cpython/Include/cpython/object.h` define
`PyObject` and `PyVarObject`. Every Python value carries a header with a
refcount and a type pointer; variable-size types (tuple, str, bytes, int)
add an `ob_size` field.

In CPython:

```c
struct _object {
    Py_ssize_t ob_refcnt;
    PyTypeObject *ob_type;
};

typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size;
} PyVarObject;
```

The free-threaded build adds `ob_tid`, `ob_mutex`, `ob_gc_bits`, `ob_ref_local`,
`ob_ref_shared`. v0.1 to v0.13 ship the GIL build, so we only need the GIL-build
fields. The free-threaded fields land in v0.14.

## Go translation

```go
// Header is the per-object header. Mirrors struct _object in
// Include/object.h. The zero value is invalid; objects are built by
// each type's constructor which initializes refcount=1 and type.
type Header struct {
    refcnt int64
    typ    *Type
}

// VarHeader extends Header with ob_size. Used by tuple, str, bytes,
// int (long), and any other variable-length builtin.
type VarHeader struct {
    Header
    size int64
}

// Object is what every Python value satisfies. Concrete types embed
// *Header (or *VarHeader) and add their own data.
type Object interface {
    Type() *Type
    Hdr() *Header
}
```

`Hdr()` lets generic code reach the refcount and type without knowing
the concrete shape. The C macro `Py_TYPE(o)` becomes `o.Type()`. The
macro `Py_REFCNT(o)` becomes `o.Hdr().refcnt` (unexported; only the
runtime fiddles with it).

### Why a method, not field access

Go interfaces force a method, not a field. We pay one indirection per
`Type()` lookup. CPython pays the same indirection through `Py_TYPE` in
the free-threaded build. v0.6 adds a vectorized fast path for common
types if the indirection shows up in the VM hot path.

## Refcount

The Go GC reclaims memory; the refcount exists to drive `__del__`, weak
references, and the cycle collector exactly as CPython does. v0.2 ships
the refcount field and the `Incref`/`Decref` ops; the actual cycle
collector arrives in v0.10.

```go
// Incref bumps the refcount. Mirrors Py_INCREF.
func Incref(o Object) {
    atomic.AddInt64(&o.Hdr().refcnt, 1)
}

// Decref drops the refcount. If it reaches zero, the type's tp_dealloc
// is invoked. Mirrors Py_DECREF.
func Decref(o Object) {
    if atomic.AddInt64(&o.Hdr().refcnt, -1) == 0 {
        o.Type().Dealloc(o)
    }
}
```

In v0.2 there is no Dealloc to call (we are not yet running user code
that creates cycles). The slot stays nil and Decref is a no-op when the
slot is nil. v0.3 wires up `__del__` and v0.10 wires up the cycle
collector.

### Atomicity

GIL-build CPython uses non-atomic `++`/`--`. Go uses `atomic.AddInt64`
because Go has no GIL of its own; even GIL-build gopy needs atomic
refcount because goroutines can race. The cost is one LOCK XADD per
incref/decref. CPython pays the same cost in the free-threaded build.

## Identity (`is`)

Two Go values are `is`-equal if they are the same `Object` pointer.
Concrete types embed pointer headers, so identity is pointer identity.

```go
func Is(a, b Object) bool {
    return a == b
}
```

Singletons (None, True, False, the small-int cache) preserve identity
across constructions because the constructor returns the cached pointer.

## Equality (`==`)

`==` calls the type's `tp_richcompare`. v0.2 lands a richcompare slot
on `Type` and the four builtins that need it for the gate:

- `int`: numeric equality with `int`/`bool`/`float`.
- `float`: numeric equality.
- `bool`: numeric equality (True == 1, False == 0).
- `tuple`: elementwise equality, fall through to identity.
- Other types in v0.2 (list, dict, slice, range): identity only. Full
  richcompare lands in v0.4 alongside string equality.

## Hash (`__hash__`)

Hashable in v0.2: `int`, `float`, `bool`, `None`, `tuple`. Unhashable:
`list`, `dict`. Frozenset arrives in v0.4 with the real SipHash.

The hash protocol is `tp_hash`. Returning -1 signals an error in CPython;
in gopy we return `(int64, error)`.

```go
type HashFunc func(o Object) (int64, error)
```

v0.2 uses placeholder hash functions that match CPython's algorithm
exactly except the SipHash key is all-zero. The v0.1 hash package
already produces the per-process key; v0.4 wires it through.

## Header alignment

CPython uses pointer-sized alignment. Go does the same automatically.
`unsafe.Sizeof(Header{})` is 16 bytes on 64-bit (8 for refcount, 8 for
type pointer). VarHeader adds 8 for size. Same as CPython.

## Borrowed vs owned references

CPython distinguishes borrowed from owned references at the API level.
gopy does not. Go GC handles lifetime; the refcount is bookkeeping for
finalizers and the cycle collector. We do not write `Py_INCREF` /
`Py_DECREF` at every borrow. We bump refs only at observable transfer
points (assignment to a container, return from a constructor, finalize
hooks).

This is a meaningful divergence from CPython's API surface but **not**
from its observable behaviour. As long as `__del__` runs at the right
time and weakrefs trigger at the right time, the user cannot tell that
the underlying counting is sparser.

The exact set of "observable transfer points" lives in 1671 §"Refcount
emit points" once v0.10 lands. v0.2 ships a placeholder where Incref
and Decref are spam-callable.

## File mapping

| C source                          | Go target                               |
|-----------------------------------|-----------------------------------------|
| `Include/object.h` (struct)       | `objects/header.go`                     |
| `Include/object.h` (Py_INCREF)    | `objects/refcount.go`                   |
| `Objects/object.c` (Py_NewRef)    | `objects/object.go`                     |
| `Objects/object.c` (PyObject_Hash)| `objects/hash.go`                       |
| `Objects/object.c` (PyObject_Repr)| `objects/repr.go`                       |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/header.go`: `Header`, `VarHeader`, `Object` interface.
  Scaffold landed in v0.2; field naming and method set still match
  this spec, but the embedded-pointer convention for concrete types
  needs an audit pass once the long port lands.
* [~] `objects/refcount.go`: `Incref`, `Decref` over `atomic.AddInt64`.
  Decref currently no-ops when `tp_dealloc` is nil; that branch goes
  away once v0.10 wires the cycle collector.
* [ ] `objects/object.go`: `NewRef`, `XNewRef`, `Clear`, the protocol
  helpers from `Objects/object.c` that are not hash or repr.
* [ ] `objects/hash.go`: `Hash(o)` dispatcher that calls `tp_hash` and
  threads the per-process SipHash key from `hash/`. Placeholder
  zero-key path retired.
* [ ] `objects/repr.go`: `Repr(o)`, `Str(o)`, plus the recursion guard
  from `Objects/object.c:PyObject_Repr` (the
  `Py_ReprEnter`/`Py_ReprLeave` pair).
* [ ] `objects/identity.go`: `Is(a, b)`, singleton registry hooks.

### Surface guarantees

* [x] `Hdr()` returns the same `*Header` for the lifetime of the
  object. Pinned by the v0.2 gate (dict insert + lookup round-trip).
* [x] Refcount writes are atomic on every architecture Go supports.
* [ ] `Repr` and `Str` round-trip every concrete builtin's value to a
  string that `eval` would accept for the literal types. Pinned by
  `compat/repr_test.go` (lands with `compat/`).
* [ ] `Hash` matches CPython under `PYTHONHASHSEED=0` for `int`,
  `float`, `bool`, `None`, `tuple`, `bytes`, `str`, `frozenset`.
  Pinned by `compat/hash_test.go`.
* [ ] `Is` returns `true` for the documented singletons (None, True,
  False, NotImplemented, Ellipsis, `()`, small ints `-5..256`) across
  every constructor path.

### Refcount emit points (v0.10)

Tracked here so the v0.10 cycle GC has a written contract to honour.
Placeholders only until then.

* [ ] Container insert: list append, tuple build, dict insert, set
  add. Each bumps the refcount of the inserted value.
* [ ] Container remove: list pop / del, dict del, set discard. Each
  drops one ref.
* [ ] Frame locals: STORE_FAST and friends. The VM owns one ref per
  local slot.
* [ ] Return value: every C-implemented callable returns an owned
  ref; the caller must drop it.
* [ ] Weakref callbacks fire before the refcount hits the freelist.

### Out of scope for v0.2

* Free-threaded fields (`ob_tid`, `ob_mutex`, `ob_gc_bits`,
  `ob_ref_local`, `ob_ref_shared`). Land in v0.14 with
  `gc/freethreading.go`.
* Borrowed-vs-owned API surface. gopy does not expose this
  distinction; see "Borrowed vs owned references" above.
* `tp_dealloc` body. Slot exists, body lands per type from v0.3
  onward.
