---
title: "gopy call"
description: "Port of cpython/Objects/call.c. Vectorcall fast path, generic call dispatch, argument tuple construction, and the kwargs handling rules."
tags: ["gopy", "spec"]
weight: 1684
---

# 1684. Call protocol

## What we are porting

`Objects/call.c` (~1500 lines). Every Python call goes through
here. Three layers:

1. Generic `PyObject_Call(callable, args, kwargs)`.
2. The vectorcall fast path: `PyObject_Vectorcall(callable, args,
   nargsf, kwnames)`. Avoids constructing a tuple/dict for typical
   calls.
3. The bound-method / classmethod / staticmethod call routing.

Vectorcall is what the v0.6 VM hot path uses (CALL opcode). This
spec gates v0.6 because the bytecode interpreter cannot be fast
without it.

## Go shape

```go
// Vectorcall is the fast-call entry. nargsf is the positional arg
// count with optional flags in the high bits; kwnames is a tuple
// of keyword names (or nil). Mirrors PyObject_Vectorcall.
func Vectorcall(callable Object, args []Object, nargsf uintptr,
    kwnames *Tuple) (Object, error)

// Call is the generic entry. Routes to vectorcall when the
// callable supports it.
func Call(callable Object, args *Tuple, kwargs *Dict) (Object, error)

// CallNoArgs is the zero-arg fast path. Mirrors PyObject_CallNoArgs.
func CallNoArgs(callable Object) (Object, error)

// CallOneArg is the one-arg fast path. Mirrors PyObject_CallOneArg.
func CallOneArg(callable Object, arg Object) (Object, error)
```

The `nargsf` flag bit `PY_VECTORCALL_ARGUMENTS_OFFSET` lets the
caller stash a `self` slot one element before the args slice
start. The VM uses this for METHOD calls to avoid one slice copy.

## Bound methods

`bound_method.__call__(args, kwargs)` rebuilds the args with `self`
prepended, then calls the underlying function. The vectorcall
shortcut: when the underlying function supports vectorcall, the
bound method routes through `tp_vectorcall_offset` and does the
prepend in-place.

## Argument unpacking

The `*args` and `**kwargs` star-call forms unpack via separate
helpers (`_PyEval_GetCallableSignatureForBoundMethod` etc.). v0.6
ports these alongside the VM CALL_FUNCTION_EX opcode.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/call.c` PyObject_Call          | `objects/call_generic.go`                |
| Vectorcall                              | `objects/call_vector.go`                 |
| Bound method routing                    | `objects/call_method.go`                 |
| Argument tuple construction             | `objects/call_args.go`                   |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [ ] `objects/call_generic.go`: `Call`, `CallObject`,
  `CallFunction`, `CallMethod`. The kwargs-as-dict path.
* [ ] `objects/call_vector.go`: `Vectorcall`, `VectorcallMethod`,
  the `PY_VECTORCALL_ARGUMENTS_OFFSET` flag handling, the
  `tp_vectorcall_offset` lookup.
* [ ] `objects/call_method.go`: bound-method dispatch, classmethod
  / staticmethod descriptors at the call site.
* [ ] `objects/call_args.go`: tuple/dict construction helpers,
  `*args` / `**kwargs` unpack, signature mismatch error text.
* [ ] `objects/call_test.go`: vectorcall vs generic parity panel,
  bound-method shortcut, kwargs ordering.

### Surface guarantees

* [ ] `f(*args, **kwargs)` with overlapping positional/keyword
  raises TypeError with the CPython text ("got multiple values
  for argument 'x'").
* [ ] Missing required arg raises TypeError with the CPython
  text ("missing 1 required positional argument: 'x'").
* [ ] Vectorcall and generic call produce identical results for
  every callable in `compat/call_panel.txt`.
* [ ] Bound methods preserve `__self__` identity:
  `obj.method.__self__ is obj`.
* [ ] `classmethod.__func__` and `staticmethod.__func__` expose
  the wrapped callable.
* [ ] Recursion limit kicks in via `Py_EnterRecursiveCall` mirror
  and raises RecursionError with the CPython text.

### Cross-references

* `tp_call` slot: 1672.
* VM CALL opcode hot path: 1620 series.

### Out of scope

* PEP 590 vectorcall ABI for C extensions. gopy does not load
  C extensions.
