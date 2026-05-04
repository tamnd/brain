---
title: "gopy bool and singletons"
description: "Port of cpython/Objects/boolobject.c plus the None and NotImplemented singletons. bool is a subtype of int."
tags: ["gopy", "spec"]
weight: 1675
---

# 1675. Bool, None, NotImplemented

## What we are porting

* `Objects/boolobject.c` (~250 lines). `bool` is a subtype of
  `int` with exactly two singleton instances (`True`, `False`).
  Most slots inherit from `int`; only `repr`, `str`, `__and__`,
  `__or__`, `__xor__` override.
* The `None` singleton from `Objects/object.c`. Type
  `NoneType`, one instance, repr `'None'`, hash `0`.
* The `NotImplemented` singleton. Type `NotImplementedType`, one
  instance, repr `'NotImplemented'`, used as a richcompare /
  binop fallback signal.
* `Ellipsis` (the `...` literal) lives here for symmetry.

## Go shape

```go
// Bool mirrors PyBool_Type. Lives in objects.True / objects.False.
type Bool struct {
    Long  // embed long; bool is a subtype of int
}

// None is the NoneType singleton.
var None = &noneSingleton{}
type noneSingleton struct { Header }

// NotImplemented is the NotImplementedType singleton.
var NotImplemented = &notImplementedSingleton{}

// Ellipsis is the Ellipsis singleton.
var Ellipsis = &ellipsisSingleton{}
```

`True` and `False` carry the int values 1 and 0 respectively.
`type(True) == bool`, `bool.__mro__ == (bool, int, object)`.

## Singleton identity

The constructor `Bool(b)` returns either `True` or `False`. Never
constructs a new `*Bool`. Same rule for `NoneType()` (always
returns `None`) and `NotImplementedType()`.

## Bitwise ops on bool

`True & True`, `True | False`, `True ^ False` return `bool`, not
`int`, when both operands are `bool`. CPython 3.0+ rule. Falls
back to int arithmetic if either operand is not bool.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/boolobject.c`                  | `objects/bool.go`                        |
| `Objects/object.c:_Py_NoneStruct`       | `objects/none.go`                        |
| `Objects/object.c:_Py_NotImplementedStruct` | `objects/notimplemented.go`           |
| `Objects/sliceobject.c:Py_Ellipsis`     | `objects/ellipsis.go` (cross-listed in 1682) |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/bool.go`: `Bool` struct embedding `Long`, `True`,
  `False` package vars, `BoolFromBool(b bool)`. v0.2 placeholder
  shipped.
* [~] `objects/none.go`: `None` singleton, NoneType, repr/hash/bool.
* [ ] `objects/notimplemented.go`: NotImplemented singleton.
* [ ] `objects/ellipsis.go`: Ellipsis singleton.
* [ ] `objects/bool_test.go`: identity test for True/False,
  bitwise narrowing, MRO check.

### Surface guarantees

* [x] `True is True`, `False is False`, `None is None`,
  `NotImplemented is NotImplemented` across every constructor /
  protocol path.
* [ ] `bool.__mro__ == (bool, int, object)`.
* [ ] `True & False is False`, `True | False is True`,
  `True ^ True is False` (bool, not int).
* [ ] `True + 1 == 2` (falls through to int arithmetic).
* [ ] `repr(True) == 'True'`, `repr(None) == 'None'`,
  `repr(NotImplemented) == 'NotImplemented'`,
  `repr(Ellipsis) == 'Ellipsis'`.
* [ ] `hash(False) == 0`, `hash(True) == 1`, `hash(None) == 0`.
* [ ] `bool('') is False`, `bool('x') is True`,
  `bool(None) is False`.

### Out of scope

* User-subclassable `bool`. CPython forbids subclassing `bool`;
  we honour the same `Py_TPFLAGS_BASETYPE` clear bit.
