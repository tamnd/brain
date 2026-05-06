---
title: "gopy runtime helpers"
description: "Two small infra ports - getopt.c (CLI option parser used during interpreter init) and hashtable.c (generic _Py_hashtable_t internal hash table). Bundled because each is tiny and self-contained."
tags: ["gopy", "spec"]
weight: 1668
---

# 1668. getopt and hashtable

## What we are porting

Two unrelated but small files bundled into one spec:

| C source              | Lines | Go target                    |
|-----------------------|-------|------------------------------|
| `Python/getopt.c`     |   163 | `getopt/getopt.go`           |
| `Python/hashtable.c`  |   424 | `hashtable/hashtable.go`     |

Both are pre-existing infrastructure that other v0.9 callers depend
on but neither warranted their own multi-page spec. They share this
file because the alternative is two near-empty specs.

## getopt

`Python/getopt.c` is *not* GNU getopt; CPython ships its own to avoid
locale and `extern int optind` issues. The interpreter init code
(`Modules/main.c` → `pylifecycle.c`) calls `_PyOS_GetOpt` on the
command-line argv to parse the `-c`, `-m`, `-O`, `-W`, etc. flags.
Three module-globals back the iteration:

* `_PyOS_opterr` (error reporting on/off).
* `_PyOS_optind` (current index).
* `_PyOS_optarg` (arg for option taking a value).

### What gopy already does

`gopy` currently has its own ad-hoc CLI parsing in `cmd/gopy/main.go`.
v0.9 replaces that with the port so flags and error messages match
CPython byte-for-byte. The user-facing `gopy --help` text is whatever
`Python/initconfig.c` prints today.

### Go shape

```go
package getopt

// State is per-call (no globals). _PyOS_GetOpt's three module globals
// collapse into one struct that the caller threads through.
type State struct {
    OptInd int
    OptArg string
    OptErr bool   // print errors? defaults to true
}

func New() *State

// LongOption mirrors the static `longopts` table in initconfig.c.
type LongOption struct {
    Name    string
    HasArg  bool
    Flag    *int    // nil means return Val
    Val     int
}

// GetOpt parses one option from argv starting at s.OptInd. Returns
// the option char or 0 on long-option-with-flag, or -1 at end of
// args. The integer matches `option->val`.
func (s *State) GetOpt(argv []string, shortOpts string, longOpts []LongOption) (int, error)
```

The Go signature drops the wide-char (`wchar_t`) argv because gopy
already converts `os.Args` to UTF-8 strings during preconfig.

### Error parity

Two messages are pinned verbatim:

* `gopy: option requires an argument -- '%s'`
* `gopy: unrecognized option '%s'`

CPython prints `python` rather than `gopy`; the substitution happens
through `Py_GetProgramName()` which already returns `"gopy"` (1622).

## hashtable

`_Py_hashtable_t` is a generic open-addressing hash table used inside
the runtime: tracemalloc, type-cache invalidation, the freelist
diagnostic counters, and the .pyc rdep tracker. It is *not* the
Python `dict`; it has no PyObject parts.

Surface (verbatim translation):

```go
package hashtable

type HashFunc func(key any) uint64
type CompareFunc func(a, b any) bool
type DestroyFunc func(value any)

type Entry struct {
    Key   any
    Value any
    Hash  uint64
}

type Table struct {
    nentries int
    nbuckets int
    buckets  []*Entry
    hash     HashFunc
    cmp      CompareFunc
    keyDtor  DestroyFunc
    valDtor  DestroyFunc
    alloc    Allocator   // matches PyMem_RawMalloc family
}

func New(hash HashFunc, cmp CompareFunc) *Table
func NewFull(hash HashFunc, cmp CompareFunc, keyDtor, valDtor DestroyFunc, alloc Allocator) *Table

func (t *Table) Get(key any) (any, bool)
func (t *Table) Set(key, val any) error
func (t *Table) Steal(key any) (any, bool)   // matches _Py_hashtable_steal
func (t *Table) Foreach(fn func(*Entry) error) error
func (t *Table) Clear()
func (t *Table) Len() int
func (t *Table) Size() int                   // memory footprint, for tracemalloc
func (t *Table) Destroy()
```

The implementation follows `hashtable.c` byte-for-byte:

* Initial bucket count: 16 (matches `HASHTABLE_INITIAL_SIZE`).
* Resize on load factor > 75% (matches `HASHTABLE_HIGH`).
* Linear probing on collisions.
* `_Py_hashtable_hash_ptr` (pointer-as-key) maps to a Go helper that
  uses `unsafe.Pointer` arithmetic; we keep this because callers in
  the GC and tracemalloc code rely on the exact distribution.

### Why not a plain Go `map`?

Two reasons:

1. CPython callers want stable iteration order (`Foreach`) and a
   `Steal` operation that returns the value while removing the entry
   without invoking the destructor. Go's builtin map has neither.
2. Some callers pre-size the table from a known entry count to avoid
   rehash storms during startup. The runtime startup path expects
   this knob.

For most user-facing code a Go `map[K]V` is the right tool; this
package exists specifically for the runtime infra that mirrors
CPython.

## Gate

`getopt/getopt_test.go`:

* Parse `-c "print(1)" foo`. Assert `OptInd` and `OptArg` match
  CPython's documented behaviour for that argv.
* Parse `--help`. Assert long-option dispatch.
* Parse `-W ignore::DeprecationWarning`. Assert combined short+arg.

`hashtable/hashtable_test.go`:

* Round-trip insert / get / steal.
* Resize: insert 100 entries, assert no rehash error and final
  bucket count matches `_Py_hashtable_size` for that size.
* `Foreach` visits every entry exactly once.
* `Destroy` calls the value destructor for each entry.

## Out of scope

* `_PyOS_GetOpt` long-option flag pointer mode. CPython sets a
  separate variable when `flag` is non-NULL; we keep the field but
  every gopy caller passes `nil` (matches CPython's actual usage).
* `_Py_hashtable_get_entry_generic` vs `_Py_hashtable_get_entry_ptr`
  specialisation. Go's interface dispatch makes the distinction
  invisible at the call site; we keep one entry path.

## v0.9 checklist

### Files

* [x] `getopt/getopt.go`: `State`, `LongOption`, `GetOpt`. Shipped
  in commit `921e618`.
* [x] `getopt/getopt_test.go`: gate panel. 13 tests covering -c,
  --help, --help-all, -W, clustered, glued, --, lone dash,
  --version, --check-hash-based-pycs.
* [x] `cmd/gopy/main.go`: switched from `flag` to
  `getopt.GetOpt`, walking `PythonShortOpts` / `PythonLongOpts`.
  `--copyright` dropped (CPython has no such CLI flag; the
  `copyright()` builtin remains the user-facing surface). Test
  panel updated; build clean.
* [x] `hashtable/hashtable.go`: `Table` type and methods. Shipped
  in commit `8aba0f6`.
* [x] `hashtable/hashtable_test.go`: gate panel. 9 tests.

### Surface guarantees

* [x] CPython's two error strings reproduced verbatim. Pinned by
  `TestUnknownShortOption`, `TestMissingArgument`,
  `TestLongOptionUnknown`. (Note: actual CPython strings are
  `Unknown option: -%c` and `Argument expected for the -%c
  option`, not the `gopy: option requires...` shape this spec
  drafted; the port follows CPython verbatim per the
  port-not-patch rule.)
* [x] Hashtable load factor 50% (matches CPython
  `HASHTABLE_HIGH`, not the 75% this spec drafted) and initial
  size 16, pinned by `TestGrowthCurve` (100 entries → 256
  buckets, load ≤ 0.50).
