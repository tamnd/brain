---
title: "gopy module and misc"
description: "Port of cpython/Objects/moduleobject.c, namespaceobject.c, structseq.c, capsule.c, iterobject.c, and enumobject.c. Module, SimpleNamespace, structseq, Capsule, the generic iterator wrappers, and enumerate / reversed."
tags: ["gopy", "spec"]
weight: 1688
---

# 1688. Module, namespace, structseq, capsule, iter, enum

## What we are porting

Six small files, ~3500 lines combined:

* `Objects/moduleobject.c`: `module` type. Holds `__dict__`,
  `__name__`, `__doc__`, `__loader__`, `__spec__`, `__file__`,
  `__path__`. The dual-storage pattern: most attributes live in
  `__dict__`, but the type also tracks `md_dict`, `md_def`,
  `md_state` for C-defined modules.
* `Objects/namespaceobject.c`: `types.SimpleNamespace`. Tiny:
  attribute access through `__dict__`, repr lists fields sorted.
* `Objects/structseq.c`: tuple-with-named-fields used by `os.stat_result`,
  `sys.version_info`, `time.struct_time`. Fixed-size, named
  fields, optional unnamed extras.
* `Objects/capsule.c`: `PyCapsule`. Opaque pointer container used
  by C extensions to expose internal pointers across module
  boundaries. gopy's port stores an `interface{}`; the C-pointer
  ABI is irrelevant since gopy does not link C extensions.
* `Objects/iterobject.c`: `iter` (sequence iterator) and
  `callable_iterator` (the two-argument iter() form). Generic
  wrappers used when a type has `__getitem__` but no `__iter__`.
* `Objects/enumobject.c`: `enumerate` and `reversed` builtins.

## Go shape

```go
// Module mirrors PyModuleObject.
type Module struct {
    Header
    Dict  *Dict
    Name  *Str
    State interface{}  // for "C-defined" modules; gopy uses Go struct
}

// Namespace mirrors _PyNamespaceObject.
type Namespace struct {
    Header
    Dict *Dict
}

// StructSeq is the per-type base. Each named struct-sequence
// (e.g. os.stat_result) is a Type whose instances are *StructSeq.
type StructSeq struct {
    VarHeader
    items []Object
}

// Capsule mirrors PyCapsule.
type Capsule struct {
    Header
    Pointer  interface{}
    Name     string
    Context  interface{}
    Destruct func()
}

// SeqIter is the sequence iterator wrapper.
type SeqIter struct {
    Header
    Index int
    Seq   Object
}

// CallableIter is the two-arg iter() form.
type CallableIter struct {
    Header
    Callable Object
    Sentinel Object
    Done     bool
}

// Enumerate mirrors enumobject.c:enumobject.
type Enumerate struct {
    Header
    Index   *Long
    Seq     Object  // an iterator
    Result  *Tuple  // recycled 2-tuple when refcount allows
}

// Reversed mirrors enumobject.c:reversedobject.
type Reversed struct {
    Header
    Index int
    Seq   Object  // sequence with __len__ and __getitem__
}
```

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/moduleobject.c`                | `objects/module.go`                      |
| `Objects/namespaceobject.c`             | `objects/namespace.go`                   |
| `Objects/structseq.c`                   | `objects/structseq.go`                   |
| `Objects/capsule.c`                     | `objects/capsule.go`                     |
| `Objects/iterobject.c`                  | `objects/seqiter.go`                     |
| `Objects/enumobject.c`                  | `objects/enum.go`                        |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [ ] `objects/module.go`: Module struct, getattr through dict
  with `__getattr__` fallback (PEP 562), repr (`<module 'name'
  from 'path'>`), `__dir__`.
* [ ] `objects/namespace.go`: SimpleNamespace, equality (compares
  `__dict__`), repr (sorted fields).
* [ ] `objects/structseq.go`: StructSeq base type, factory
  (`NewType(name, fields, n_unnamed_fields)`), getattr by name,
  positional access, repr (`name(field1=v1, field2=v2)`),
  pickling support.
* [ ] `objects/capsule.go`: opaque-pointer container; in gopy
  used only for stdlib bridge.
* [ ] `objects/seqiter.go`: SeqIter + CallableIter.
* [ ] `objects/enum.go`: Enumerate (with start arg), Reversed
  (handles `__reversed__` callback if defined).
* [ ] `objects/module_test.go`, `enum_test.go`, `seqiter_test.go`:
  per-file panels.

### Surface guarantees

* [ ] `module.__getattr__` (PEP 562) is honoured before raising
  AttributeError.
* [ ] `repr(module)` matches CPython for the four cases
  (filesystem path, builtin, frozen, namespace package).
* [ ] `SimpleNamespace(a=1, b=2) == SimpleNamespace(b=2, a=1)`.
* [ ] structseq `n_sequence_fields` vs `n_fields` distinction:
  named-but-not-sequence fields don't count in tuple length.
* [ ] `os.stat_result(...)` round-trips through pickle.
* [ ] `iter(obj)` with only `__getitem__` falls through to
  SeqIter; raises TypeError if neither.
* [ ] `iter(callable, sentinel)` stops on sentinel equality.
* [ ] `enumerate(['a', 'b'], start=10)` yields `(10, 'a'),
  (11, 'b')`.
* [ ] `reversed(range(3))` returns a range_iterator (specialised),
  not a Reversed wrapper.
* [ ] `reversed(d)` where `d` is a dict iterates keys in reverse
  insertion order.

### Cross-references

* Module / `__getattr__` (PEP 562): import system (v0.8).
* Capsule / stdlib bridge: any future stdlib module that needs
  cross-module C handles.

### Out of scope

* The frozen-module loader. Lands in v0.8 import system.
* Multi-phase module init (PEP 489). v0.8.
