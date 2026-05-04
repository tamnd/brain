---
title: "gopy abstract"
description: "Port of cpython/Objects/abstract.c. Cross-type protocol dispatch (PyObject_*, PyNumber_*, PySequence_*, PyMapping_*, PyIter_*) that the bytecode interpreter calls into."
tags: ["gopy", "spec"]
weight: 1683
---

# 1683. Abstract protocol

## What we are porting

`Objects/abstract.c` (~3000 lines). The dispatcher layer between
the VM and the type slots. Every BINARY_OP, COMPARE_OP, GET_ITER,
FOR_ITER opcode (and their kin) routes through here.

Five families:

* `PyObject_*`: Length, GetItem, SetItem, DelItem, GetAttr,
  SetAttr, RichCompare, Hash, Type, IsInstance, IsSubclass, Repr,
  Str, Bytes, Format, Call, Iter.
* `PyNumber_*`: Add, Subtract, Multiply, MatMul, TrueDivide,
  FloorDivide, Remainder, Divmod, Power, Negative, Positive,
  Absolute, Invert, Lshift, Rshift, And, Or, Xor, Index,
  AsSsizeT, ToBase, plus the in-place variants.
* `PySequence_*`: Length, Concat, Repeat, GetItem (int index),
  SetItem, GetSlice, SetSlice, Tuple, List, Fast, Count, Contains,
  Index, InPlaceConcat, InPlaceRepeat.
* `PyMapping_*`: Length, GetItem (key), SetItem, HasKey,
  Keys, Values, Items.
* `PyIter_*`: Check, Next, Send.

## Why this exists

Each family is a thin wrapper around the type slots, with
fallback rules. PyNumber_Add tries `nb_add` on the left operand,
then the reflected slot on the right operand if the left returns
NotImplemented or doesn't implement it, with the subclass-priority
rule. PySequence_GetItem normalises negative indices. PyObject_Hash
checks `tp_hash` and raises TypeError if NULL.

The fallback rules are observable through normal Python code, so
the dispatcher matters for behavioural compatibility.

## Go shape

```go
package objects

// Add is PyNumber_Add. Tries left.nb_add, falls through to
// right.nb_add (reflected) per the subclass-priority rule.
func Add(a, b Object) (Object, error)

// GetItem is PyObject_GetItem. Routes to mp_subscript first,
// falls through to sq_item with index conversion.
func GetItem(o, key Object) (Object, error)

// Iter is PyObject_GetIter. Returns o.tp_iter() if defined,
// or a sequence-fallback iter if sq_item is defined.
func Iter(o Object) (Object, error)

// IterNext is PyIter_Next. Returns (nil, ErrStopIteration) at end.
func IterNext(it Object) (Object, error)
```

Errors flow through Go return values; the C `NULL`-with-exception
convention becomes a typed error.

## Subclass priority

Critical rule: if the right operand's type is a strict subclass of
the left operand's type, the right's reflected slot runs first.
This is how `Fraction(1, 2) + 1` returns a `Fraction` rather than
falling through to `int.__add__`.

## File mapping

| C source                            | Go target                                |
|-------------------------------------|------------------------------------------|
| `Objects/abstract.c` PyObject_*     | `objects/abstract_object.go`             |
| `Objects/abstract.c` PyNumber_*     | `objects/abstract_number.go`             |
| `Objects/abstract.c` PySequence_*   | `objects/abstract_sequence.go`           |
| `Objects/abstract.c` PyMapping_*    | `objects/abstract_mapping.go`            |
| `Objects/abstract.c` PyIter_*       | `objects/abstract_iter.go`               |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/abstract_object.go`: Length, GetItem, SetItem,
  DelItem, RichCompare, Hash, Repr, Str. v0.2 subset shipped.
* [~] `objects/abstract_number.go`: Add, Subtract, Multiply,
  TrueDivide, FloorDivide, Remainder, Power, Negative,
  Positive, Absolute, Bool. Subclass-priority rule for binops.
  v0.2 subset shipped.
* [ ] `objects/abstract_number.go` (full): Lshift, Rshift, And,
  Or, Xor, Invert, MatMul, Index, AsSsizeT, ToBase, plus all
  in-place variants.
* [~] `objects/abstract_sequence.go`: Length, GetItem, SetItem,
  Tuple, List, Contains, Iter, Concat. v0.2 subset shipped.
* [ ] `objects/abstract_sequence.go` (full): GetSlice, SetSlice,
  Count, Index, Repeat, Fast, InPlaceConcat, InPlaceRepeat.
* [ ] `objects/abstract_mapping.go`: Length, GetItem, SetItem,
  HasKey, Keys, Values, Items.
* [~] `objects/abstract_iter.go`: Iter, IterNext. v0.2 shipped.
* [ ] `objects/abstract_iter.go` (full): Check, Send,
  GetAIter, ANext.
* [ ] `objects/abstract_test.go`: subclass-priority panel,
  reflected-slot fallback, NotImplemented handling.

### Surface guarantees

* [ ] Subclass priority: when `type(b)` is a strict subclass of
  `type(a)`, `a + b` calls `b.__radd__` first.
* [ ] NotImplemented from both sides raises TypeError with the
  CPython text ("unsupported operand type(s) for +: 'X' and
  'Y'").
* [ ] PyNumber_Index follows the `__index__` chain; reject
  bool-from-int special-cased path is preserved.
* [ ] PyIter_Next on a non-iterator raises TypeError with the
  CPython text.
* [ ] PySequence_Contains routes through `__contains__` if
  defined, falls back to iteration.
* [ ] PyObject_Hash raises TypeError on unhashable types with
  the CPython text including the type name.

### Cross-references

* Type slots: 1672.
* Per-type implementations: 1673-1689.

### Out of scope

* `tp_async_*` async-iter slots beyond the v0.2 subset. Lands
  alongside generators (1687) in v0.6.
