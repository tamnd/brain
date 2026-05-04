---
title: "gopy slice and range"
description: "Port of cpython/Objects/sliceobject.c and rangeobject.c. The slice and range builtins, plus the Ellipsis singleton."
tags: ["gopy", "spec"]
weight: 1682
---

# 1682. Slice and range

## What we are porting

* `Objects/sliceobject.c` (~700 lines). The `slice` type plus the
  `Ellipsis` singleton (cross-listed in 1675). Slice indices are
  arbitrary objects until normalization.
* `Objects/rangeobject.c` (~1100 lines). The `range` type and its
  iterator. Lazy: stores `(start, stop, step)`, never
  materialises the sequence.

## Go shape

```go
// Slice mirrors PySliceObject.
type Slice struct {
    Header
    Start Object  // may be None
    Stop  Object
    Step  Object  // may be None
}

// Range mirrors PyRangeObject. Always stores ints (CPython long).
type Range struct {
    Header
    Start  *Long
    Stop   *Long
    Step   *Long
    Length *Long
}

// RangeIter mirrors rangeiterobject.
type RangeIter struct {
    Header
    cur  *Long
    stop *Long
    step *Long
    len  *Long
}
```

## Slice normalisation

```go
// AdjustIndices clamps slice indices against length and returns
// (start, stop, step, slicelen). Mirrors PySlice_AdjustIndices.
func (s *Slice) AdjustIndices(length int) (int, int, int, int)
```

Negative indices, None, out-of-bounds are all clamped per
CPython's rules.

## Range arithmetic

`len(range(a, b, c))` is computed in arbitrary precision (it can
overflow int64). `range(...).count(x)`, `index(x)`, and
`__contains__` short-circuit by arithmetic instead of iteration.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/sliceobject.c`                 | `objects/slice.go`                       |
| Slice indices / AdjustIndices           | `objects/slice_indices.go`               |
| Ellipsis singleton                      | `objects/ellipsis.go` (also in 1675)     |
| `Objects/rangeobject.c`                 | `objects/range.go`                       |
| RangeIter                               | `objects/range_iter.go`                  |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/slice.go`: `Slice` struct, `NewSlice`, repr.
  v0.2 placeholder.
* [ ] `objects/slice_indices.go`: `AdjustIndices`,
  `Unpack` (extract Start/Stop/Step as ints with None handling),
  `slice.indices(length)` Python method.
* [~] `objects/range.go`: `Range` struct, `NewRange`, length,
  getitem, contains, iter. v0.2 placeholder.
* [ ] `objects/range_iter.go`: `RangeIter`, the iter protocol,
  `__length_hint__`.
* [ ] `objects/slice_test.go`, `range_test.go`: corner-case
  panel.

### Surface guarantees

* [ ] `slice(None, None, None).indices(10) == (0, 10, 1)`.
* [ ] `slice(-1, None, -1).indices(5) == (4, -1, -1)`.
* [ ] `range(0, 1<<100)` length is correct (arbitrary precision).
* [ ] `range(10).index(5) == 5` without iteration.
* [ ] `5 in range(0, 10, 2)` is `False`; `4 in range(0, 10, 2)`
  is `True`.
* [ ] `range(10) == range(0, 10, 1)` is `True`; `range(10) ==
  range(0, 10, 2)` is `False`.
* [ ] `hash(range(10))` matches CPython.
* [ ] `slice` is unhashable.

### Cross-references

* Long arithmetic: 1673.
* Iter protocol: 1683.

### Out of scope

* `__class_getitem__` for `slice` (PEP 585 isn't applied to it).
