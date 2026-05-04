---
title: "gopy arena spec"
description: "Faithful port of cpython/Python/pyarena.c to gopy/arena. Bump-allocator with linked-block layout used by the compiler pipeline for AST and scratch buffers."
tags: ["gopy", "spec"]
weight: 1604
---

# 1604. Arena allocator (`arena/`)

The arena is a bump allocator with a linked list of fixed-size blocks.
The compiler pipeline (parser, AST, symbol table, codegen) allocates
many small short-lived nodes that share a lifetime: they are all freed
together when compilation of a module finishes. CPython implements this
with `pyarena.c`. gopy ports the same shape into pure Go.

## C reference

Source: `cpython/Python/pyarena.c` (207 lines). Key constants:

```
DEFAULT_BLOCK_SIZE = 8192
ALIGNMENT          = 8
```

Layout (one C struct per type):

```
block:
    ab_size   total bytes the block can hand out
    ab_offset bytes already handed out
    ab_next   linked list pointer
    ab_mem    pointer to the first allocatable byte

PyArena:
    a_head    first block, used only on free
    a_cur     current block; new blocks get appended past it
    a_objects PyList of PyObject* to DECREF on free
```

Public C API (the only entry points the rest of CPython calls):

```
_PyArena_New        create
_PyArena_Free       free everything; DECREF tracked objects
_PyArena_Malloc     bump-allocate `size` bytes, aligned to 8
_PyArena_AddPyObject register an object that will be DECREFed on Free
```

## Go API

Package `arena`. The mapping follows the naming rules in 1601: drop the
`_Py` prefix, use exported Go identifiers, keep the call shape.

```go
package arena

type Arena struct { /* unexported */ }

func New() *Arena
func (a *Arena) Malloc(n int) []byte
func (a *Arena) AddObject(obj any) error
func (a *Arena) Free()
```

Notes on the translation:

1. `Malloc` returns `[]byte`, not a raw `unsafe.Pointer`. Callers that
   need a typed allocation will use a generic helper added in v0.5
   (`func NewObj[T any](a *Arena) *T`). v0.1 only exposes the byte-slice
   form; the AST does not exist yet.
2. `AddObject` takes `any` because gopy has no `PyObject` in v0.1. The
   roadmap in 1603 reaches the object model in v0.2 (handover from the
   Objects spec series). Until then, `AddObject` simply retains a
   reference so the value survives until `Free`.
3. `Free` drops all block buffers and the object list. Go's GC then
   reclaims them. There is no equivalent to `PyMem_Free`; clearing
   the pointers is enough.
4. Errors: the C version surfaces `PyErr_NoMemory()` on allocation
   failure. Go's `make` panics on out-of-memory, so `Malloc` and `New`
   never return nil. `AddObject` returns `error` only to mirror the C
   call shape (`int r = PyList_Append(...)`); in v0.1 it always returns
   nil.

## Block strategy

A block is a `struct { mem []byte; off int; next *block }`. `mem` has
length `cap = max(DEFAULT_BLOCK_SIZE, requestedSize)`. The first block
is created at `New()` time so `a.cur` is never nil.

Allocation (`Malloc(n)`):

1. Round `n` up to 8.
2. If `cur.off + n > len(cur.mem)`, allocate a new block of size
   `max(DEFAULT_BLOCK_SIZE, n)` and link it after `cur`.
3. Hand out `cur.mem[off : off+n : off+n]`. The capped slice prevents
   the caller from accidentally appending into the next allocation.
4. Advance `cur.off += n`.
5. If a new block was just linked, advance `cur` to it.

Step 5 mirrors the C code's "Reset cur if we allocated a new block"
trailer.

## Alignment

`ALIGNMENT = 8` matches CPython on every supported platform. The block
header in C uses `_Py_ALIGN_UP(b->ab_mem, ALIGNMENT)`. In Go, `make([]byte, n)`
returns memory aligned to at least `unsafe.Alignof(maxAlign_t)` which is
8 on amd64/arm64, so we do not need a runtime alignment trim. We round
allocation sizes to 8 anyway for parity with CPython.

## Tests

`arena/arena_test.go` covers:

- `Malloc(0)` returns an empty slice, does not advance `off`.
- `Malloc(n)` for several sizes, checks alignment and non-overlap.
- A request larger than `DEFAULT_BLOCK_SIZE` lands in its own block.
- Many small allocations grow the block list.
- `AddObject` retains the object until `Free` (verified with a
  finalizer that records when the value becomes unreachable).
- `Free` releases all blocks (verified by exhausting the per-block
  bump pointer then re-freeing).
- Concurrent `Malloc` is **not** safe: this matches CPython, which has
  no internal locking on `_PyArena_Malloc`. The doc string says so.

## Non-goals

- Per-allocation free. The arena frees in bulk; that is the point.
- Resizing an allocation. CPython has no `_PyArena_Realloc` and we do
  not introduce one.
- Concurrent access. Callers serialize externally.
