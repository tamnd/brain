---
title: "gopy list"
description: "Port of cpython/Objects/listobject.c. Mutable variable-length sequence with the CPython list_resize growth curve and Timsort."
tags: ["gopy", "spec"]
weight: 1679
---

# 1679. List

## What we are porting

`Objects/listobject.c` (~3500 lines). The most-used mutable
container. Append-amortised, sort via Timsort, slice assignment,
in-place reverse, the full mutable sequence protocol.

## Go shape

```go
// List mirrors PyListObject.
type List struct {
    VarHeader
    items []Object  // len = size, cap >= len
}
```

We back the list with a Go slice. `append` already amortises, but
CPython's `list_resize` curve is observable (it determines how
often `__sizeof__` changes), so we mirror it instead of letting Go
choose.

## list_resize curve

CPython's growth: `new_cap = (size + (size >> 3) + 6) & ~3`. Same
formula in `listResize`. The user can probe it via `sys.getsizeof`.

```go
func listResize(l *List, newLen int) {
    needed := newLen
    if needed <= cap(l.items) && needed*2 >= cap(l.items) {
        l.items = l.items[:needed]
        return
    }
    newCap := (needed + (needed >> 3) + 6) &^ 3
    next := make([]Object, needed, newCap)
    copy(next, l.items)
    l.items = next
}
```

## Sort

`list.sort()` runs Timsort over the items with the user-supplied
key function (or identity). Port from `Objects/listobject.c:listsort_impl`.
Stable; in-place; same merge run lengths CPython picks.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/listobject.c` (struct + ctors) | `objects/list.go`                        |
| resize + setitem + slice                | `objects/list_resize.go`                 |
| sort                                    | `objects/list_sort.go`                   |
| richcompare + repr                      | `objects/list_misc.go`                   |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/list.go`: `List` struct, `New`, `FromSlice`,
  `Append`, `Pop`, length, getitem, iter, contains. v0.2
  placeholder shipped.
* [ ] `objects/list_resize.go`: `listResize` mirroring the CPython
  growth curve; slice assignment with size delta.
* [ ] `objects/list_sort.go`: Timsort port with key callback,
  reverse flag, stability.
* [ ] `objects/list_misc.go`: richcompare (lexicographic), repr,
  index, count, copy, clear, extend, insert, remove, reverse.
* [ ] `objects/list_test.go`: resize-curve probe, sort-stability
  panel, slice-assign size-delta panel.

### Surface guarantees

* [ ] `sys.getsizeof([1])` matches CPython after the same append
  history. Pinned by `compat/sizeof_test.go`.
* [ ] `list.sort()` is stable.
* [ ] `list.sort(key=f)` calls `f` exactly once per item.
* [ ] `[1, 2] + [3, 4]` returns a new list.
* [ ] `list * n` for negative or zero `n` returns `[]`.
* [ ] Slice assignment with size delta moves trailing items
  exactly once.
* [ ] `list` is unhashable; `hash([1])` raises TypeError.
* [ ] Mutation during iteration raises RuntimeError on the next
  step (via the version-tag check CPython uses).

### Cross-references

* Sequence protocol: 1683.

### Out of scope

* Free-threaded list element-level locking. Lands in v0.14.
* `array.array`. Stdlib.
