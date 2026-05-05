---
title: "gopy stackref"
description: "Port of cpython/Python/stackrefs.c. Tagged stack reference values, borrow tracking, and the conversion shims between PyObject* and stackref."
tags: ["gopy", "spec"]
weight: 1638
---

# 1638. Stack reference values

## What we are porting

`Python/stackrefs.c` (~250 lines) plus the inline declarations in
`Include/internal/pycore_stackref.h`. The stackref system is
CPython's compact representation for stack values that distinguishes
"strong reference" from "borrowed reference" without spending a
refcount op per push. It is the foundation the eval loop's stack
operations are written against.

A stackref is a tagged pointer: the low bit (or a deferred-refcount
bit on free-threading) marks whether the eval loop owns a reference
or borrowed it. Tier-1 and Tier-2 dispatch arms are written entirely
in stackref terms; the conversion to `PyObject*` happens at API
boundaries (CALL into builtin, raise an exception, etc.).

## Why this matters for v0.6

Even though gopy uses Go's GC and refcount ops are largely no-ops,
the stackref shape stays. Two reasons:

1. The bytecodes DSL refers to `PyStackRef_*` macros directly
   (`PyStackRef_AsPyObjectBorrow`, `PyStackRef_DUP`, ...). The
   generator (1621) translates those calls to Go, and they need to
   land somewhere typed.
2. The free-threaded build (v0.14) reuses the same stackref bits
   for biased refcounting. Keeping the wrapper now means v0.14
   adds bits, not concept.

In v0.6, stackref is structurally a wrapper around `object.Object`
with two helpers (`AsObject`, `New`) and four no-op refcount ops.
The bit manipulation lands in v0.14.

## Go shape

```go
// Ref is a tagged stack value. Mirrors _PyStackRef from
// Include/internal/pycore_stackref.h.
//
// In the GIL build, Ref is structurally a pointer with no tag
// bits. The wrapper exists so the eval loop matches CPython's
// stackref vocabulary, and so v0.14 can swap in the biased-refcount
// representation without touching the dispatch arms.
type Ref struct {
    bits uintptr
}

// FromObject wraps a strong reference. Mirrors
// PyStackRef_FromPyObjectSteal.
func FromObject(o object.Object) Ref

// FromObjectNew wraps a new strong reference (incrementing refcount).
// Mirrors PyStackRef_FromPyObjectNew.
func FromObjectNew(o object.Object) Ref

// AsObject extracts the object pointer. Mirrors
// PyStackRef_AsPyObjectBorrow. The caller must not retain past
// the lifetime of the stackref.
func (r Ref) AsObject() object.Object

// AsObjectSteal extracts the object pointer and consumes the
// stackref. Mirrors PyStackRef_AsPyObjectSteal.
func (r Ref) AsObjectSteal() object.Object

// Dup returns a duplicate strong reference. Mirrors
// PyStackRef_DUP.
func (r Ref) Dup() Ref

// IsNull reports whether the ref is the sentinel null. Mirrors
// PyStackRef_IsNull.
func (r Ref) IsNull() bool

// Null is the sentinel for absent values (uninitialized fast
// locals, popped stack slots after clear). Mirrors
// PyStackRef_NULL.
var Null = Ref{}
```

## Sentinels

CPython defines a small set of sentinel stackrefs:

* `PyStackRef_NULL`: absent value. Used for unbound fast locals
  and cleared stack slots.
* `PyStackRef_None`, `PyStackRef_True`, `PyStackRef_False`:
  pre-allocated singletons. The eval loop uses these for
  `LOAD_CONST None / True / False` to skip a refcount bump.

```go
var (
    None  Ref // wraps object.None
    True  Ref // wraps object.True
    False Ref // wraps object.False
)
```

These are populated at runtime init from the global object
singletons (Objects spec 1675).

## Conversion at API boundaries

CALL, IMPORT_NAME, RAISE_VARARGS, and a handful of other opcodes
hand a stackref off to a function written against `object.Object`.
The conversion shim is one of:

* `r.AsObject()` for borrowed: caller does not consume.
* `r.AsObjectSteal()` for steal: caller consumes the ref.
* `FromObject(o)` for return values that come back as
  `object.Object`.

The eval loop balances these: every steal at the top is matched by
either a `FromObject` of the return value or a frame teardown that
clears the popped slots.

## File mapping

| C source                                    | Go target                       |
|---------------------------------------------|---------------------------------|
| `Python/stackrefs.c`                        | `vm/stackref/stackref.go`       |
| `Include/internal/pycore_stackref.h` (struct, macros) | `vm/stackref/stackref.go` |
| `Python/stackrefs.c` (deferred refcount)    | `vm/stackref/deferred.go` (v0.14) |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `stackref/stackref.go`: `Ref` value, `FromObject`,
  `FromObjectNew`, `FromObjectImmortal`, `AsObject`, `AsObjectSteal`,
  `Dup`, `Close`, `IsNull`, `Null`. (Path: flat layout per project
  convention; spec originally said `vm/stackref/`.)
* [x] `stackref/sentinel.go`: `None`, `True`, `False`
  pre-allocated stackrefs, populated at init from
  `objects.None() / True() / False()`.
* [x] `stackref/stackref_test.go`: round-trip panel
  (`FromObject` then `AsObject`), null sentinel, dup semantics.

### Surface guarantees

* [x] `Ref` does not grow beyond one Go interface header
  (typeptr + dataptr; 16 bytes on 64-bit). CPython's
  `_PyStackRef` is one tagged uintptr; gopy stores
  `objects.Object` directly so the equivalent floor is one
  interface header. Pinned by `TestRefSize`. v0.14 can swap in
  a packed representation without touching dispatch arms.
* [x] `FromObject(o).AsObject() == o` for every non-nil object.
  Pinned by `TestFromObjectRoundTrip` plus `TestFromObjectNewAndImmortal`.
* [x] `Null.IsNull() == true`; every other sentinel returns
  false. Pinned by `TestNullSentinel` and `TestSentinels`.
* [x] `None.AsObject() == object.None` and the same for `True`,
  `False`. Pinned by `TestSentinels`.
* [x] `Dup` produces a stackref the eval loop can drop without
  affecting the original. Pinned by `TestDupIndependent`.

### Out of scope for v0.6

* Tagged-bit deferred refcount (free-threaded build). Lives in
  v0.14.
* `_PyStackRef_FromPyObjectImmortal`: the immortal-object path is
  no-op in gopy (Go's GC handles immortality differently). The
  helper exists as an alias for `FromObject` in v0.6.

### Cross-references

* Eval loop that reads and writes stackrefs: 1636.
* Frame storage backed by `[]Ref`: 1637.
* Object singletons (None / True / False): 1675.
* Free-threaded refcounting: 1614 (brc) and v0.14 free-threading.
