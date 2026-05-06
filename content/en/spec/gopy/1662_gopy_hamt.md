---
title: "gopy hamt"
description: "Hash Array Mapped Trie immutable mapping. Backs contextvars (1663). Ports cpython/Python/hamt.c byte-for-byte preserving the 5-bit-per-level tree shape."
tags: ["gopy", "spec"]
weight: 1662
---

# 1662. HAMT immutable mapping

## What we are porting

`cpython/Python/hamt.c` (~2885 lines) plus the public API in
`cpython/Include/internal/pycore_hamt.h`. Output:

| C source                                      | Lines | Go target              |
|-----------------------------------------------|-------|------------------------|
| `Python/hamt.c`                               |  2885 | `hamt/hamt.go`         |
| `Include/internal/pycore_hamt.h` (public API) |   ~120| `hamt/api.go`          |

The HAMT (Hash Array Mapped Trie) is an immutable persistent mapping
used as the backing store for `Context` in PEP 567. Its API is private
to the runtime: stdlib code reaches it only through contextvars. gopy
ships it as a small, self-contained package with no callers other
than `contextvar/`.

## Why immutable

Three properties matter:

1. **O(1) copy**. `ctx.run(...)` copies the entire mapping; HAMT
   shares structure so the copy is a single pointer assignment.
2. **O(log32 N) get / set / delete**. Branching factor 32 keeps the
   tree shallow; for any practical context size the depth is ≤ 7.
3. **Structural sharing**. `set` and `delete` rebuild the spine but
   keep all untouched subtrees, so memory footprint per snapshot is
   O(log N) rather than O(N).

## Tree shape

A 32-bit Python hash drives indexing. Each level consumes 5 bits, so
the maximum tree depth is `ceil(32/5) = 7`. A collision node at level
7 holds keys whose 32-bit hashes agree; that gives a total maximum
depth of 8 (the constant `_Py_HAMT_MAX_TREE_DEPTH`).

Three node types match CPython exactly:

| Node           | When used                                                  |
|----------------|------------------------------------------------------------|
| `BitmapNode`   | The default. Holds up to 16 entries with a popcount index. |
| `ArrayNode`    | Promoted from BitmapNode when entries exceed the bitmap.   |
| `CollisionNode`| Level-7 leaf for keys with identical 32-bit hashes.         |

The bitmap layout is two 32-bit fields: one for keys (`shift_array`)
and one for sub-nodes. Slot index is `popcount(bitmap & (bit-1))`.
The Go port pins this byte-for-byte; iteration order matches CPython.

## Go shape

```go
package hamt

type Hamt struct {
    objects.Header
    root  node
    count int
}

type node interface {
    assoc(level, hash int, key, val objects.Object) (node, bool, error)
    without(level, hash int, key objects.Object) (node, bool, error)
    find(level, hash int, key objects.Object) (objects.Object, bool, error)
}

type bitmapNode struct {
    bitmap uint32
    array  []objects.Object  // alternating keys, values, or sub-nodes
}

type arrayNode struct {
    count    int
    children [32]node
}

type collisionNode struct {
    hash  int32
    array []objects.Object  // alternating keys, values
}

// Public API.
func New() *Hamt
func (h *Hamt) Assoc(key, val objects.Object) (*Hamt, error)
func (h *Hamt) Without(key objects.Object) (*Hamt, bool, error)
func (h *Hamt) Find(key objects.Object) (objects.Object, bool, error)
func (h *Hamt) Len() int
func (h *Hamt) Eq(other *Hamt) (bool, error)

// Iterator state matches PyHamtIteratorState: zero-allocation depth-first.
type Iter struct {
    nodes [maxDepth]node
    pos   [maxDepth]int
    level int8
}

func (h *Hamt) Iter() *Iter
func (it *Iter) Next() (key, val objects.Object, ok bool, err error)
```

`Hamt` is registered as `HamtType` for repr and equality. Three
"view" types (`HamtKeysType`, `HamtValuesType`, `HamtItemsType`)
expose the corresponding iterators; CPython exposes them as
`_PyHamtKeys_Type` etc. but they are private to runtime callers.

## CPython parity points

* Bitmap-to-array promotion happens at exactly 16 entries (CPython
  `_PyHamt_Array_From_Bitmap` threshold).
* Collision node insertion preserves insertion order on hash
  collisions, matching `hamt_node_collision_assoc`.
* Iteration emits keys in tree order. The exact ordering is
  observable through `Context.copy()` and through stdlib tests, so
  the port pins the bitmap walk direction.
* `Eq` short-circuits on identity, then walks both trees in parallel
  and is O(N).

## Errors

HAMT operations raise `KeyError` only via `Without` on a missing key
(returns `ok=false` rather than the C `NULL`-with-PyErr pattern).
Hashing errors propagate through `Find` / `Assoc` / `Without` from
the underlying `objects.Hash`.

## Gate

`hamt/hamt_test.go`:

* Round-trip: `New().Assoc(k1,v1).Assoc(k2,v2).Find(k1)` returns
  `(v1, true, nil)`.
* Structural sharing: `h2 := h1.Assoc(k,v)`; check that nodes
  outside the path-from-root are pointer-equal between `h1` and
  `h2`.
* Promotion: insert 17 keys whose hashes share the top 5 bits and
  assert the level-1 node is `*arrayNode`.
* Collision: insert two keys whose 32-bit hashes are equal; assert
  level-7 holds a `*collisionNode` with both entries.
* Iter: ordering matches a CPython oracle for a fixed key set. (The
  oracle is a one-off Python-side script that prints
  `list(_HamtClass(...).items())`; the result is checked in.)
* Eq: equal trees built by different insertion orders compare equal.

A property-based check generates random sequences of `Assoc` /
`Without` and asserts equivalence with a Go `map[Object]Object`
oracle.

## Out of scope

* The `_testcapi` HAMT exports. CPython only uses these in
  `Lib/test/test_context.py`; we cover the same behaviour through
  the contextvars tests.
* Mutating helpers used inside `_PyHamt_Assoc` for transient nodes.
  Go has no refcount, so the "transient" optimisation collapses into
  the immutable path with no measurable cost.

## v0.9 checklist

### Files

* [x] `hamt/hamt.go`: `Hamt`, `node`, `bitmapNode`, `arrayNode`,
  `collisionNode`. Shipped in commit `9c1d96f`.
* [x] `hamt/api.go`: public Assoc/Without/Find/Len/Eq.
* [x] `hamt/iter.go`: depth-first `Iter`.
* [x] `hamt/types.go`: `HamtType` registered.
* [x] `hamt/hamt_test.go`: 12-test gate panel.

### Surface guarantees

* [x] Tree depth ≤ 8 for any 32-bit hash distribution.
* [x] BitmapNode promoted to ArrayNode at the CPython threshold.
* [x] Iteration order pinned.
* [x] `Hamt` is hashable through `tp_hash` returning `frozenset`-style
  XOR over `(hash(k), hash(v))` pairs (matches `_PyHamt_Hash`).
