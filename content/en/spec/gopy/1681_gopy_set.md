---
title: "gopy set"
description: "Port of cpython/Objects/setobject.c. set and frozenset on the same open-addressing layout as dict, sharing the probing sequence."
tags: ["gopy", "spec"]
weight: 1681
---

# 1681. Set and frozenset

## What we are porting

`Objects/setobject.c` (~2500 lines). `set` (mutable) and
`frozenset` (immutable, hashable) share one struct. Layout is the
same open-addressing hash table as `dict` minus the values column.

## Go shape

```go
// Set mirrors PySetObject. Used for both set and frozenset; the
// type is decided by the type pointer in the Header.
type Set struct {
    Header
    table   []setEntry
    used    int
    fill    int
    mask    int
    hash    int64  // for frozenset; -1 = uncomputed; set leaves -1
    version uint64
}

type setEntry struct {
    hash int64
    key  Object  // nil = empty, sentinel = dummy
}
```

Two type pointers: `objects.SetType` for mutable, `objects.FrozenSetType`
for immutable. Methods dispatch on the type pointer; the struct is
identical.

## Probing

Same `5 * i + 1 + perturb`, `perturb >>= 5` formula as dict, with
the same per-table mask. `set & frozenset` produce identical
iteration order for inputs that differ only in mutability.

## frozenset hash

```go
func frozensetHash(s *Set) (int64, error)
```

XOR-based combine of element hashes with the avalanche constants
from `setobject.c:frozenset_hash`. Cached in `Set.hash`.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/setobject.c` (struct + ctors)  | `objects/set.go`                         |
| insert / delete / probe                 | `objects/set_lookup.go`                  |
| set ops (union, intersect, etc.)        | `objects/set_ops.go`                     |
| frozenset hash + iter                   | `objects/set_misc.go`                    |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [ ] `objects/set.go`: `Set` struct, `NewSet`, `NewFrozenSet`,
  add, discard, remove, pop, clear, length, contains, iter.
* [ ] `objects/set_lookup.go`: lookkey with the dict-shared
  probing sequence; dummy-slot handling on delete.
* [ ] `objects/set_ops.go`: union, intersection, difference,
  symmetric_difference, plus the in-place variants and the
  `<`, `<=`, `>`, `>=` subset / superset checks.
* [ ] `objects/set_misc.go`: frozenset hash, repr (sorted for
  deterministic output? no, CPython is iteration-order),
  isdisjoint, copy.
* [ ] `objects/set_test.go`: probing pin, frozenset hash pin,
  set-op correctness, mutation-during-iteration guard.

### Surface guarantees

* [ ] `hash(frozenset({1, 2, 3}))` matches CPython under
  PYTHONHASHSEED=0.
* [ ] `set` iteration order equals dict iteration order for the
  same insert sequence (shared probing).
* [ ] `set` mutation during iteration raises RuntimeError
  ("Set changed size during iteration").
* [ ] `frozenset` is hashable; `set` raises TypeError on hash.
* [ ] Set operations produce the type of the left operand
  (`s1 - s2` is set if s1 is set, frozenset if frozenset).
* [ ] `s.update(d)` over a dict iterates keys, not items.

### Cross-references

* Hash key: 1661.
* Probing sequence: 1680.

### Out of scope

* `weakset`. Stdlib.
* Free-threaded set reader path. v0.14.
