---
title: "gopy hash"
description: "Port of cpython/Python/pyhash.c. SipHash-1-3 plus FNV-1a, secret seed bootstrap from 1607."
tags: ["gopy", "spec"]
weight: 1661
---

# 1661. Hash

## What we are porting

`cpython/Python/pyhash.c` (498 lines). Plus the public API in
`cpython/Include/pyhash.h`. The companion seed-init file
`cpython/Python/bootstrap_hash.c` was already ported to `hash/secret.go`
in v0.1 (spec 1607).

`pyhash.c` carries:

* **SipHash-1-3** the default hash for str, bytes, memoryview, and
  any object whose hash falls back to a buffer hash. Two 64-bit
  rounds in compress, three in finalize.
* **FNV-1a** the fallback path used when CPython is built with
  `Py_HASH_ALGORITHM == Py_HASH_FNV`. Kept for parity but not the
  default in 3.14.
* **The hash secret installation** `_Py_HashSecret_t` is a 24-byte
  union that holds two 64-bit SipHash keys plus a 16-byte FNV seed.
  Installed once at runtime startup from `bootstrap_hash.c`, read by
  every hash call.
* **`Py_HashPointer`** the address-derived hash for objects that
  fall back to identity, with the rotation that prevents alignment
  patterns from clustering low bits.

## The SipHash-1-3 spec

Two 64-bit halves of state per round, four-state SipHash core
(`v0..v3`). Compress = 1 round per 8-byte block. Finalize = 3 rounds
after XORing the length byte. CPython 3.14 uses the same constants
SipHash defines:

```
v0 = key0 ^ 0x736f6d6570736575
v1 = key1 ^ 0x646f72616e646f6d
v2 = key0 ^ 0x6c7967656e657261
v3 = key1 ^ 0x7465646279746573
```

The output is `v0 ^ v1 ^ v2 ^ v3`, masked into a `Py_hash_t` (signed
64-bit) with the value `-2` reserved for "uninitialized hash" and
remapped to `-3`.

```go
// Buffer mirrors _Py_HashBytes. Returns Py_hash_t.
func Buffer(b []byte) int64
```

## The hash secret

`hash/secret.go` (already shipped, v0.1) reads from `/dev/urandom` (or
the OS RNG equivalent) at first use and caches a `[24]byte` blob.
Setting `PYTHONHASHSEED=0` in the environment forces the secret to
all zeros so reference outputs are deterministic. v0.4's `pyhash.go`
consumes the secret without reaching for the OS:

```go
type Key struct {
    K0, K1 uint64 // SipHash keys
    Prefix uint64 // FNV prefix
    Suffix uint64 // FNV suffix
    DJBX33A uint8 // expansion fallback for very short inputs
}

// Secret returns the runtime-wide key. First call materialises it.
func Secret() Key
```

## Pointer hash

Object identity hashes (the default `tp_hash`) round-trip through
`Py_HashPointer`. The pointer bits are rotated by 4 to defeat the
common alignment pattern, then XORed with the secret key 0:

```go
// Pointer mirrors Py_HashPointer.
func Pointer(p unsafe.Pointer) int64
```

## File mapping

| C source                         | Go target                  |
|----------------------------------|----------------------------|
| `Python/pyhash.c:_Py_HashBytes`  | `hash/hash.go:Buffer`      |
| `Python/pyhash.c:siphash13`      | `hash/siphash.go`          |
| `Python/pyhash.c:fnv`            | `hash/fnv.go`              |
| `Python/pyhash.c:Py_HashPointer` | `hash/hash.go:Pointer`     |
| `Python/bootstrap_hash.c`        | `hash/secret.go` (v0.1)    |

## Gate

`hash.Buffer([]byte("hello"))` under `PYTHONHASHSEED=0` matches CPython
3.14 byte-for-byte. The reference vector is computed once with `python3
-c 'import sys; print(hash(b"hello"))'` under the same env and pinned
in the test.
