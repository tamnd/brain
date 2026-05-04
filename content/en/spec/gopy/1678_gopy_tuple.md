---
title: "gopy tuple"
description: "Port of cpython/Objects/tupleobject.c. Immutable sequence with the empty-tuple singleton and the CPython tuple hash."
tags: ["gopy", "spec"]
weight: 1678
---

# 1678. Tuple

## What we are porting

`Objects/tupleobject.c` (~1300 lines). Immutable, fixed-size
heterogeneous sequence. Used everywhere: argument tuples, multiple
return values, dict keys, namedtuple base, exception args.

## Go shape

```go
// Tuple mirrors PyTupleObject. Immutable after construction.
type Tuple struct {
    VarHeader
    items []Object
}
```

Empty-tuple singleton: `()` returns the same `*Tuple` every call.
CPython's `_Py_SINGLETON(tuple_empty)`.

Small-tuple freelist: CPython caches tuples of size 1..20 in a
type-specific freelist. Go GC does not need a freelist; we skip
this micro-optimization.

## Hash

```go
// hash(tuple) follows the xxHash-derived algorithm from
// _PyHASH_XXPRIME_*. Mirrors tuplehash from tupleobject.c
// exactly, including the 64-bit prime constants.
func tupleHash(t *Tuple) (int64, error)
```

The algorithm is xxHash-style with 64-bit primes; we use the same
constants CPython does so `hash((1, 2, 3))` matches byte-for-byte.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/tupleobject.c`                 | `objects/tuple.go`                       |
| richcompare                             | `objects/tuple_cmp.go`                   |
| hash + repr                             | `objects/tuple_misc.go`                  |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/tuple.go`: `Tuple` struct, `FromSlice`, `Pack(args
  ...Object)`, length, getitem, iter, contains. v0.2 placeholder
  shipped with the empty-tuple singleton.
* [ ] `objects/tuple_cmp.go`: lexicographic richcompare.
* [ ] `objects/tuple_misc.go`: hash (xxHash-style), repr, str,
  count, index.
* [ ] `objects/tuple_test.go`: empty-singleton identity, hash
  parity, slicing, concatenation.

### Surface guarantees

* [x] `() is ()` returns `True`. Singleton across every
  constructor path (`tuple()`, `tuple([])`, `(*x for x in [])`).
* [ ] `hash((1, 2, 3))` matches CPython byte-for-byte.
* [ ] `hash((1.0,)) == hash((1,))` (numeric coercion in hashing).
* [ ] `repr((1,))` includes the trailing comma.
* [ ] `(1, 2) + (3, 4)` returns a new tuple (not a list).
* [ ] `tuple * n` repeats; `tuple([])` returns the singleton.
* [ ] Slicing `t[a:b]` returns a new tuple (or the singleton if
  empty).
* [ ] Tuples containing unhashable values (e.g. lists) raise
  `TypeError: unhashable type` on hash.

### Cross-references

* Hash algorithm: 1661 (the xxHash primes).
* Sequence protocol: 1683.

### Out of scope

* `namedtuple`. Lives in `collections.namedtuple` (stdlib);
  `structseq` (1688) covers the C-side struct-sequence.
* Free-thread small-tuple freelist. The Go GC subsumes this.
