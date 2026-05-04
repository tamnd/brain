---
title: "gopy bytes"
description: "Port of cpython/Objects/bytesobject.c, bytearrayobject.c, and bytes_methods.c. Immutable bytes plus mutable bytearray with the full string-like method panel."
tags: ["gopy", "spec"]
weight: 1676
---

# 1676. Bytes and bytearray

## What we are porting

Three files, ~6000 lines total:

* `Objects/bytesobject.c`: immutable `bytes`. Hash, repr, the
  string-like method surface (`split`, `join`, `find`, `replace`,
  `translate`, `decode`, etc.), parsing, `%`-formatting,
  buffer protocol exposure.
* `Objects/bytearrayobject.c`: mutable `bytearray`. Same method
  surface plus mutation (`append`, `extend`, `pop`,
  `__setitem__`, slice assignment).
* `Objects/bytes_methods.c`: shared method bodies that both
  `bytes` and `bytearray` dispatch into. The `is*`, `find`,
  `count`, `lower`, `upper`, `swapcase`, `title`, `capitalize`
  family.

## Go shape

```go
// Bytes mirrors PyBytesObject. Immutable.
type Bytes struct {
    VarHeader
    data []byte  // never aliased, never appended to
    hash int64   // -1 = uncomputed
}

// ByteArray mirrors PyByteArrayObject. Mutable.
type ByteArray struct {
    VarHeader
    data    []byte  // may grow; cap >= len
    exports int     // outstanding buffer exports; mutation forbidden when > 0
}
```

Empty-bytes singleton: `b''` returns the same `*Bytes` every time
(matches CPython's `_PyBytes_Empty`).

## Hash

SipHash-1-3 over `data`, keyed via `hash` (1661). Cached in the
`hash` field. Same algorithm as `bytes_hash` in CPython.

## Buffer protocol

Both types implement `tp_as_buffer`. v0.4 ships the read-side; the
mutable side of bytearray's buffer (write-back into the same
storage) lands with memoryview in 1689.

## Method surface

The `bytes_methods.c` shared bodies take a buffer pointer; we
translate to:

```go
func bmFind(haystack []byte, needle []byte, start, end int) int
func bmCount(haystack []byte, needle []byte, start, end int) int
func bmLower(src []byte) []byte
func bmIsAscii(src []byte) bool
// ... etc
```

`bytes` wraps each in a `Bytes`-returning method; `bytearray`
wraps the mutating variants in-place.

## File mapping

| C source                          | Go target                                |
|-----------------------------------|------------------------------------------|
| `Objects/bytesobject.c`           | `objects/bytes.go`                       |
| bytes parsing / repr              | `objects/bytes_repr.go`                  |
| bytes methods (immutable wrap)    | `objects/bytes_methods_wrap.go`          |
| `Objects/bytearrayobject.c`       | `objects/bytearray.go`                   |
| bytearray methods                 | `objects/bytearray_methods.go`           |
| `Objects/bytes_methods.c`         | `objects/bytes_shared.go`                |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [ ] `objects/bytes.go`: `Bytes` struct, `FromString`,
  `FromBytes`, `EmptyBytes` singleton, len/getitem/iter, hash,
  richcompare.
* [ ] `objects/bytes_repr.go`: repr (with `\x`/`\t`/`\n` escapes
  and quote-style choice), str, decode.
* [ ] `objects/bytes_methods_wrap.go`: split, rsplit, splitlines,
  partition, rpartition, join, find, rfind, index, rindex,
  count, replace, strip, lstrip, rstrip, translate, maketrans,
  startswith, endswith, expandtabs, center, ljust, rjust, zfill,
  hex, fromhex.
* [ ] `objects/bytearray.go`: `ByteArray` struct, mutable
  constructors, `__setitem__`, slice assignment, append, extend,
  pop, insert, remove, reverse, clear, copy.
* [ ] `objects/bytearray_methods.go`: same surface as bytes plus
  the in-place variants (`+=` calls `extend`).
* [ ] `objects/bytes_shared.go`: shared method bodies.
* [ ] `objects/bytes_test.go`: hash parity, repr parity,
  method-surface panel.

### Surface guarantees

* [ ] `b''` returns the singleton; `is` identity holds.
* [ ] `hash(bytes)` matches CPython under PYTHONHASHSEED=0.
* [ ] `repr(b'\x00\xff') == "b'\\x00\\xff'"` byte-for-byte.
* [ ] Quote-style choice: prefer `'`, switch to `"` if the
  payload contains `'` and not `"`.
* [ ] `bytes.fromhex('1f 2a')` strips inner whitespace per
  CPython.
* [ ] `bytearray()` is mutation-safe across slice assignment with
  growth and shrinkage.
* [ ] `bytearray` mutation while a memoryview is exported raises
  BufferError.
* [ ] `b'%d' % (1,)` formats per `printf` (CPython percent-bytes
  rules).

### Cross-references

* Hash key: 1661.
* Format mini-language: 1660.
* Buffer protocol exposure / memoryview: 1689.

### Out of scope

* The `array.array` type. Stdlib.
* `mmap`. Stdlib (and CPython's mmap is a separate module).
