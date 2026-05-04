---
title: "gopy long"
description: "Port of cpython/Objects/longobject.c. Arbitrary-precision int with the small-int cache, base-2/8/10/16 parsing, hash, and the full numeric protocol."
tags: ["gopy", "spec"]
weight: 1673
---

# 1673. Long (int)

## What we are porting

`Objects/longobject.c` (~6500 lines). The most-used numeric type in
CPython. Arbitrary precision via 30-bit digit arrays (15-bit on
32-bit builds, but gopy is 64-bit-only). Per-process cache of the
small-int range (`-5..256`). Numeric-protocol slot table covering
add, subtract, multiply, true/floor div, mod, pow, bitwise ops,
shifts, negation, abs, conversion to/from float, hashing, repr,
parsing from string with arbitrary base.

CPython 3.12+ stores small ints inline in a tagged-pointer style
on free-threaded builds. gopy's GIL build matches the unboxed
layout but does not use tagged pointers; the small-int cache is a
plain `[262]*Long` array.

## Go shape

```go
// Long mirrors PyLongObject. Sign is encoded in size: positive
// magnitude in digits[], negative if size<0, zero if size==0.
type Long struct {
    Header
    digits []uint32  // 30 bits per digit, little-endian
    size   int       // signed; sign(size) == sign(value)
}
```

Use `int64` fast path for values that fit; spill to digit array
otherwise. CPython does the same with `_PyLong_IsCompact`.

## Small-int cache

```go
// smallInts[i] caches the int with value i-5 for i in [0..262).
// Mirrors _Py_SmallInts in longobject.c.
var smallInts [262]*Long
```

`-5..256` are singletons. `is` comparison preserves identity:
`x = 1; y = 1; assert x is y`.

## Parsing

`PyLong_FromString` accepts any base in `[2..36]` plus base 0
(autodetect from `0x`/`0o`/`0b` prefix or default to 10). Underscores
allowed between digits per PEP 515.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/longobject.c` (struct + ctors) | `objects/long.go`                        |
| arithmetic                              | `objects/long_arith.go`                  |
| bitwise + shifts                        | `objects/long_bitwise.go`                |
| parsing                                 | `objects/long_parse.go`                  |
| hash, repr, format                      | `objects/long_misc.go`                   |
| small-int cache                         | `objects/long_cache.go`                  |
| `clinic/longobject.c.h`                 | folded into the above                    |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/long.go`: `Long` struct, `FromInt64`, `FromUint64`,
  `AsInt64`, `IsZero`, `Sign`. v0.2 placeholder shipped; full
  digit-array spill pending.
* [ ] `objects/long_arith.go`: Add, Sub, Mul, FloorDiv, TrueDiv,
  Mod, DivMod, Pow, Negative, Abs.
* [ ] `objects/long_bitwise.go`: And, Or, Xor, Invert, Lshift,
  Rshift.
* [ ] `objects/long_parse.go`: `FromString(s, base)`, base-0
  autodetect, underscore handling, leading/trailing whitespace
  rules.
* [ ] `objects/long_misc.go`: Hash (compress to `Py_hash_t`),
  Repr (decimal), Str, Format (`__format__` with mini-language),
  RichCompare, Bool, Int, Float coercions.
* [ ] `objects/long_cache.go`: small-int cache initialiser, the
  `Get(i)` fast path.
* [ ] `objects/long_test.go`: per-op panel + small-int identity +
  hash parity.

### Surface guarantees

* [ ] `is` identity holds for `-5..256` across every constructor
  path.
* [ ] `hash(int)` matches CPython under PYTHONHASHSEED=0 for the
  full `-2**128 .. 2**128` corpus from `compat/hash_panel.txt`.
* [ ] `repr(int)` matches CPython for arbitrary-precision values.
* [ ] `int("0x1_0", 0) == 16` round-trips per PEP 515.
* [ ] `int(2**1000)` round-trips through digit-array path.
* [ ] `int.__pow__(b, e, m)` modular reduction matches CPython
  bit-for-bit.
* [ ] Division by zero raises ZeroDivisionError with the same
  text CPython uses.

### Cross-references

* Header / refcount: 1671.
* Type slots: 1672.
* Hash key: 1607 / 1661.
* Format mini-language: 1660.

### Out of scope

* `bool` subtype of `int`. Lives in 1675.
* SIMD-accelerated multiplication. Tracked under perf, not parity.
* Free-threaded tagged-pointer compaction. Lands with 1671 §free
  threading in v0.14.
