---
title: "gopy descriptor and method"
description: "Port of cpython/Objects/descrobject.c, methodobject.c, classobject.c, and funcobject.c. The descriptor protocol (data and non-data), bound methods, builtin function objects, and Python function objects."
tags: ["gopy", "spec"]
weight: 1685
---

# 1685. Descriptor and method

## What we are porting

Four files, ~5000 lines:

* `Objects/descrobject.c`: descriptor objects (`property`,
  `member_descriptor`, `getset_descriptor`, `method_descriptor`,
  `wrapper_descriptor`, `slot_wrapper`). The descriptor protocol
  (`__get__`, `__set__`, `__delete__`).
* `Objects/methodobject.c`: `PyCFunction` (built-in functions and
  bound methods of C-implemented methods). v0.4 lands the surface;
  v0.6 wires it into the VM call path.
* `Objects/classobject.c`: bound-method (`method`) for Python
  functions called on instances. Same shape as the C-method
  bound, different underlying callable.
* `Objects/funcobject.c`: Python function object. Carries the
  code object, defaults, closure, globals, name, qualname,
  annotations, type-params (PEP 695). v0.6 once frame/gen exist.

## Go shape

```go
// Function mirrors PyFunctionObject.
type Function struct {
    Header
    Code         *Code
    Globals      *Dict
    Defaults     *Tuple   // positional defaults
    KwDefaults   *Dict    // keyword-only defaults
    Closure      *Tuple   // cell objects
    Name         *Str
    Qualname     *Str
    Doc          Object   // str or None
    Dict         *Dict    // function attributes
    Module       Object
    Annotations  Object   // dict or function (lazy)
    TypeParams   *Tuple   // PEP 695
    Vectorcall   func(args []Object, kwnames *Tuple) (Object, error)
    Version      uint32   // bumped on Defaults / Globals change
}

// Method (bound method) mirrors PyMethodObject.
type Method struct {
    Header
    Func Object  // the function (or any callable)
    Self Object  // the bound instance
}

// CFunction mirrors PyCFunctionObject (C-implemented builtin).
type CFunction struct {
    Header
    Def    *MethodDef
    Self   Object   // module or class
    Module *Module
}
```

## Descriptor protocol

```go
// LookupDescriptor walks the type MRO and applies the
// data-descriptor / non-data-descriptor rule. Mirrors
// _PyObject_GenericGetAttrWithDict from object.c.
func LookupDescriptor(obj Object, name *Str) (Object, error)
```

Order: data descriptors on the type (those with `__set__` or
`__delete__`) > instance `__dict__` > non-data descriptors >
TypeError.

This ordering is observable through user code; getting it wrong
breaks every metaclass, every property, every classmethod.

## Property

`property(fget, fset, fdel, doc)` is a data descriptor. The four
slots wrap callables. `prop.setter`, `prop.getter`, `prop.deleter`
return new property objects with one slot replaced.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/descrobject.c` (descriptors)   | `objects/descr.go`                       |
| `descrobject.c` (property)              | `objects/property.go`                    |
| `descrobject.c` (member / getset)       | `objects/descr_member.go`                |
| `Objects/methodobject.c`                | `objects/cfunction.go`                   |
| `Objects/classobject.c`                 | `objects/method.go`                      |
| `Objects/funcobject.c`                  | `objects/function.go`                    |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files (v0.4 descriptor protocol)

* [ ] `objects/descr.go`: descriptor base, the `__get__` /
  `__set__` / `__delete__` slot wrappers, the descriptor-walk
  helper used by `type_getattro`.
* [ ] `objects/property.go`: `property` type with fget/fset/fdel,
  `setter` / `getter` / `deleter` returning replacement
  properties, `__set_name__` hook.
* [ ] `objects/descr_member.go`: `member_descriptor` and
  `getset_descriptor` for slot-backed instance attributes.
* [ ] `objects/cfunction.go`: `CFunction` type, `MethodDef`
  table, the dispatch table for METH_O / METH_NOARGS /
  METH_VARARGS / METH_FASTCALL / METH_FASTCALL|METH_KEYWORDS /
  METH_METHOD.
* [ ] `objects/method.go`: bound method type, `__call__` that
  prepends `self`, `__func__` / `__self__` accessors.
* [ ] `objects/descr_test.go`: data-vs-non-data ordering panel,
  property setter chaining, MRO walk.

### Files (v0.6 function object)

* [ ] `objects/function.go`: `Function` struct, `MakeFunction`
  (used by VM MAKE_FUNCTION), defaults handling, closure cell
  binding, vectorcall implementation that builds a frame.
* [ ] `objects/function_versions.go`: version tag bumped on
  defaults/globals/__code__ change (used by the VM specializer).

### Files (v0.7 tp_new / tp_init)

* [ ] `objects/descr_classmethod.go`, `descr_staticmethod.go`:
  classmethod / staticmethod descriptors. Land alongside user
  type creation.

### Surface guarantees

* [ ] Data descriptor beats instance dict beats non-data
  descriptor. Pinned by `compat/descriptor_test.go`.
* [ ] `property` raises AttributeError with the CPython text
  when the missing slot is accessed.
* [ ] `method.__self__ is obj`, `method.__func__ is f`.
* [ ] `CFunction` calls preserve the right `self` for module
  functions vs unbound class methods.
* [ ] `__set_name__` fires at class-creation time.
* [ ] Function `__defaults__` is shared (mutable surface; same
  object across calls until reassigned).
* [ ] `__closure__` cells round-trip with `cell_contents`.

### Cross-references

* Type slots: 1672.
* Code object: 1687.
* Cell object: 1687 (cellobject.c).
* Call dispatch: 1684.

### Out of scope

* PEP 558 frame `f_locals` semantics; lives in 1687.
