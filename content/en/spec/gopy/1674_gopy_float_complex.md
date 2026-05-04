---
title: "gopy float and complex"
description: "Port of cpython/Objects/floatobject.c and complexobject.c. IEEE-754 binary64 float with shortest-roundtrip repr, plus the complex builtin used by cmath."
tags: ["gopy", "spec"]
weight: 1674
---

# 1674. Float and complex

## What we are porting

* `Objects/floatobject.c` (~2400 lines): boxed IEEE-754 binary64.
  Numeric protocol, repr (shortest-roundtrip via dtoa), hash,
  `__format__`, parsing.
* `Objects/complexobject.c` (~1400 lines): `complex` built on two
  `float64` fields. Same numeric protocol shape with explicit
  real/imag.

`floatobject.c` lands in v0.2 (it gates the v0.2 `repr` corpus).
`complexobject.c` lands in v0.6 (no upstream user before then).

## Go shape

```go
// Float mirrors PyFloatObject.
type Float struct {
    Header
    Value float64
}

// Complex mirrors PyComplexObject.
type Complex struct {
    Header
    Real float64
    Imag float64
}
```

Both store values directly. No NaN-canonicalisation: `float('nan')`
is one specific bit pattern (`0x7ff8000000000000`), the same one
CPython uses.

## Hashing

`float.__hash__` runs the modular-reduction algorithm from
`Objects/object.c:_Py_HashDouble`. Reuses the `hash` package
(1661) which already exposes `Double`.

`complex.__hash__` combines the real and imag hashes:
`hash(z) == hash(z.real) + 1000003 * hash(z.imag)` (mod
`2**61 - 1`), matching CPython.

## Repr / str

Shortest-roundtrip via `pystrtod.FormatFloat` (1660). Special
cases:

* `inf` / `-inf` / `nan` repr verbatim.
* Integer-valued floats render as `1.0`, not `1`.
* Negative zero renders as `-0.0`.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/floatobject.c`                 | `objects/float.go`                       |
| arithmetic + richcompare                | `objects/float_arith.go`                 |
| repr / str / format                     | `objects/float_repr.go`                  |
| parsing                                 | `objects/float_parse.go`                 |
| `Objects/complexobject.c`               | `objects/complex.go` (v0.6)              |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files (float, v0.2)

* [~] `objects/float.go`: `Float` struct, `FromFloat64`,
  `AsFloat64`. v0.2 placeholder landed; richcompare panel pending.
* [ ] `objects/float_arith.go`: Add, Sub, Mul, TrueDiv, FloorDiv,
  Mod, DivMod, Pow, Negative, Abs, Bool.
* [ ] `objects/float_repr.go`: Repr (shortest roundtrip), Str,
  Format (mini-language with `f/e/g/F/E/G/%`), Hash via
  `hash.Double`.
* [ ] `objects/float_parse.go`: `FromString` with whitespace
  trimming, underscore PEP 515, signed `inf`/`nan` parsing.
* [ ] `objects/float_test.go`: repr corpus, hash corpus, parsing
  corner cases, NaN comparisons.

### Files (complex, v0.6)

* [ ] `objects/complex.go`: `Complex` struct, real/imag accessors,
  numeric protocol, `__format__`.
* [ ] `objects/complex_test.go`: hash combine, division, abs,
  `__format__`.

### Surface guarantees

* [ ] `repr(float)` matches CPython on the
  `compat/repr/floats.txt` corpus (subnormals, denormals, exact
  powers of two, near-roundoff cases).
* [ ] `hash(float)` matches CPython on every value in
  `compat/hash/floats.txt`.
* [ ] `float('inf')`, `float('nan')` produce the exact bit
  patterns CPython produces.
* [ ] `0.1 + 0.2 == 0.30000000000000004` (no silent rounding).
* [ ] `int(float('inf'))` raises OverflowError with the CPython
  text.
* [ ] Division by zero raises ZeroDivisionError; modulo with NaN
  returns NaN.
* [ ] `complex(1, 2) ** 2 == complex(-3, 4)` (panel pinned).

### Cross-references

* `pystrtod` parsing / formatting: 1660.
* Hash key: 1661.
* Format mini-language: 1660.

### Out of scope

* `decimal.Decimal`. Stdlib effort.
* `fractions.Fraction`. Stdlib.
* Long-double / `_Float128`. Not exposed in CPython 3.14 either.
