---
title: "gopy dict"
description: "Port of cpython/Objects/dictobject.c and odictobject.c. Insertion-ordered open-addressing hash table with the CPython probing sequence."
tags: ["gopy", "spec"]
weight: 1680
---

# 1680. Dict and OrderedDict

## What we are porting

* `Objects/dictobject.c` (~5500 lines). Insertion-ordered
  open-addressing hash table. The dual-table layout (compact
  index array + dense entry array) introduced in 3.6 and kept
  through 3.14. Combined / split storage for instance dicts.
* `Objects/odictobject.c` (~1500 lines). `collections.OrderedDict`
  C accelerator. Distinct from `dict` despite both preserving
  order: OrderedDict has `move_to_end` and equality compares
  order.

## Go shape

```go
// Dict mirrors PyDictObject. Compact-and-ordered.
type Dict struct {
    Header
    indices []int32   // hash-modulo bucket -> entry index, or empty/dummy
    entries []dictEntry
    used    int       // number of live entries
    fill    int       // number of buckets with dummy or live
    version uint64    // bump on every mutation; iter checks
}

type dictEntry struct {
    hash int64
    key  Object
    value Object
}
```

Indices array uses int8/int16/int32/int64 depending on size, the
same density-based packing CPython does.

## Probing sequence

```
i = hash & (size - 1)
perturb = hash
while occupied:
    perturb >>= 5
    i = (5 * i + 1 + perturb) & (size - 1)
```

`5 * i + 1 + perturb` with `perturb >>= 5` per probe, mask down to
table size. Mirrors `dictobject.c:lookdict`.

## Lookdict variants

CPython has four:

1. `lookdict_unicode_nodummy`: all-string keys, no deletes.
2. `lookdict_unicode`: all-string keys, may have deletes.
3. `lookdict_split`: split-table (instance __dict__) keys.
4. `lookdict`: generic.

We ship the same four; the dispatch is via a function pointer in
the `Dict` struct, swapped on first non-string insert / first
delete.

## OrderedDict

OrderedDict adds a doubly-linked list across the entries (via
`prev` / `next` indices). Iteration order matches list order;
`move_to_end` re-links. Equality compares the link order, unlike
regular dict.

## File mapping

| C source                          | Go target                                |
|-----------------------------------|------------------------------------------|
| `Objects/dictobject.c`            | `objects/dict.go`                        |
| lookdict variants                 | `objects/dict_lookup.go`                 |
| resize / insert / delete          | `objects/dict_mutate.go`                 |
| iter / views / repr               | `objects/dict_iter.go`                   |
| split-table (instance dict)       | `objects/dict_split.go`                  |
| `Objects/odictobject.c`           | `objects/odict.go`                       |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/dict.go`: `Dict` struct, `New`, `Get`, `Set`,
  `Del`, `Contains`, length, iter. v0.2 placeholder shipped with
  the CPython probing sequence.
* [ ] `objects/dict_lookup.go`: the four lookdict variants and
  the dispatch swap.
* [ ] `objects/dict_mutate.go`: resize curve, insert with kept
  order, delete leaving dummy slots, recompact on shrink.
* [ ] `objects/dict_iter.go`: keys / values / items views,
  view operations (union, intersection, etc.), version-tag
  check on iter.
* [ ] `objects/dict_split.go`: split-table layout for instance
  __dict__ (used by 1672 type machinery).
* [ ] `objects/odict.go`: OrderedDict with the doubly-linked
  list, move_to_end, popitem(last=False), order-aware equality.
* [ ] `objects/dict_test.go`: probing-sequence pin, iteration
  order pin, view set ops, version-tag mutation guard.

### Surface guarantees

* [ ] Insertion order is preserved across all dict operations
  (matches CPython 3.7+ guarantee).
* [ ] Probing sequence is byte-identical to CPython for the
  same hash inputs. Pinned by `compat/dict_probing_test.go`.
* [ ] `dict.__sizeof__` matches CPython after the same sequence
  of inserts and deletes.
* [ ] Mutation during iteration raises RuntimeError ("dictionary
  changed size during iteration") via the version tag.
* [ ] View set operations: `d1.keys() & d2.keys()` returns a
  set, not a dict_keys.
* [ ] `OrderedDict([(1,2)]) == OrderedDict([(1,2)])` but
  `OrderedDict([(1,2),(3,4)]) != OrderedDict([(3,4),(1,2)])`
  (order-aware), while plain dict equality ignores order.

### Cross-references

* Hash key: 1661.
* Type instance __dict__: 1672 / 1685.

### Out of scope

* Free-threaded dict reader path (`ob_tid`, `ob_mutex`,
  `dk_version`). Lands in v0.14.
* PEP 768 (compact dict for typed slots). Not in 3.14.
