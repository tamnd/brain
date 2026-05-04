---
title: "gopy errors"
description: "Port of cpython/Python/errors.c and the gating subset of cpython/Objects/exceptions.c. Exception types, set/get/clear, raise/chain, normalize."
tags: ["gopy", "spec"]
weight: 1611
---

# 1611. errors: exception protocol

## What we are porting

Two files from CPython:

- `cpython/Python/errors.c` (about 2200 lines). Holds the C-API for
  setting, fetching, clearing, formatting, normalizing, and printing
  exceptions, plus the chaining (`__cause__` / `__context__`)
  machinery. Reads and writes through the current thread state.
- `cpython/Objects/exceptions.c` (about 4500 lines). Defines every
  built-in exception class, the `BaseException` slots
  (`args`, `traceback`, `__cause__`, `__context__`, `__suppress_context__`,
  `__notes__`), and the type hierarchy.

`Python/errors.c` is a leaf of the runtime: it depends only on
exceptions, traceback, and thread state. We can port it before the VM
because every entry point is callable from Go directly.

`Objects/exceptions.c` is much larger. v0.3 ships only the gating
hierarchy: enough exception classes to cover what v0.1 and v0.2
internally raise (`ValueError`, `TypeError`, `KeyError`, `IndexError`,
`StopIteration`, `RuntimeError`, `OverflowError`,
`ZeroDivisionError`), plus their bases (`BaseException`, `Exception`,
`LookupError`, `ArithmeticError`). The remaining classes (`OSError`
subtree, `SyntaxError` and friends, `ImportError`, `Warning` subtree)
land incrementally as later phases need them.

## Go translation

```go
package errors

// Exception is the runtime representation of a raised Python exception.
// Mirrors PyBaseExceptionObject from Objects/exceptions.c.
type Exception struct {
    objects.Header
    Type     *objects.Type
    Args     *objects.Tuple
    Cause    *Exception
    Context  *Exception
    Suppress bool
    Notes    *objects.List
    TB       *traceback.Traceback
}

// Set raises an exception with the given args tuple. Mirrors PyErr_SetObject.
func Set(state *state.Thread, t *objects.Type, args *objects.Tuple)

// SetString raises an exception with a single-string args tuple.
// Mirrors PyErr_SetString.
func SetString(state *state.Thread, t *objects.Type, msg string)

// Format raises an exception built from a printf-style template.
// Mirrors PyErr_Format. Returns nil so callers can `return errors.Format(...)`.
func Format(state *state.Thread, t *objects.Type, format string, args ...any) *Exception

// Occurred returns the current exception or nil. Mirrors PyErr_Occurred.
func Occurred(state *state.Thread) *Exception

// Clear drops the current exception. Mirrors PyErr_Clear.
func Clear(state *state.Thread)

// Fetch atomically removes and returns the current exception triple.
// Mirrors PyErr_Fetch.
func Fetch(state *state.Thread) (typ *objects.Type, value *Exception, tb *traceback.Traceback)

// Restore atomically installs an exception triple. Mirrors PyErr_Restore.
func Restore(state *state.Thread, typ *objects.Type, value *Exception, tb *traceback.Traceback)

// NormalizeException ensures the value is an instance of the type.
// Mirrors PyErr_NormalizeException.
func NormalizeException(state *state.Thread)
```

## The state slot

CPython stores the current exception in `tstate->current_exception`.
In gopy this becomes a field on `state.Thread`:

```go
package state

type Thread struct {
    // ...
    exc atomic.Pointer[errors.Exception]
}
```

Atomic because under the free-threaded build readers (the VM
`POP_EXCEPT` handler) and writers (signal handlers) can race. GIL-build
reads remain single-threaded but the cost of an atomic load is
negligible.

## The exception class hierarchy

v0.3 ships the following classes, with their MRO matching CPython
exactly:

```
BaseException
  Exception
    LookupError
      KeyError
      IndexError
    ArithmeticError
      OverflowError
      ZeroDivisionError
    RuntimeError
      NotImplementedError
    AttributeError
    NameError
    TypeError
    ValueError
    StopIteration
```

Each class has a `Type` registered with the runtime. `KeyError` has
the special `__str__` that wraps args[0] in `repr(...)` if args has
one element; that override is preserved exactly.

The full hierarchy (`OSError` subtree, `SyntaxError`, `ImportError`,
`Warning`) is added in later phases as needed; the v0.3 spec only
guarantees the gating subset. See `1612_gopy_exceptions_full.md` for
the full list once it lands.

## Chaining: `__cause__` and `__context__`

`raise X` sets `X.__context__ = previous`. `raise X from Y` sets
`X.__cause__ = Y` and `__suppress_context__ = True`. CPython does this
in `do_raise()` in `Python/ceval.c`, but the same logic is reachable
from `_PyErr_SetObject`:

```go
// Raise sets exc as the current exception. If a previous exception
// was current, it becomes exc.Context.
func Raise(state *state.Thread, exc *Exception)

// RaiseFrom is `raise exc from cause`. It sets exc.Cause and
// suppresses context display.
func RaiseFrom(state *state.Thread, exc *Exception, cause *Exception)
```

## Normalize

`PyErr_NormalizeException` is the legacy 3-argument API. CPython 3.12+
folds normalization into `_PyErr_SetObject`; we follow the modern
single-step path. `NormalizeException` exists for source-shape parity
but its implementation is a single call to the modern set path.

## Print

`PyErr_Print` writes the exception to stderr. v0.3 ships a minimal
implementation that uses `traceback.Format` for the body and prepends
the type name; v0.6 hooks it into `sys.excepthook`.

## File mapping

| C source                                         | Go target                       |
|--------------------------------------------------|---------------------------------|
| `Python/errors.c:_PyErr_SetObject` and friends   | `errors/api.go`                 |
| `Python/errors.c:_PyErr_Occurred / _PyErr_Clear` | `errors/api.go`                 |
| `Python/errors.c:_PyErr_Fetch / _PyErr_Restore`  | `errors/api.go`                 |
| `Python/errors.c:_PyErr_FormatV`                 | `errors/api.go`                 |
| `Python/errors.c:_PyErr_NormalizeException`      | `errors/api.go`                 |
| `Python/errors.c:_PyErr_Display`                 | `errors/print.go`               |
| `Python/suggestions.c`                           | `errors/suggest.go`             |
| `Objects/exceptions.c:BaseException_*`           | `errors/exception.go`           |
| `Objects/exceptions.c:KeyError_str`              | `errors/keyerror.go`            |
| `Objects/exceptions.c:<each leaf>`               | `errors/builtins.go`            |

v0.3 bundles the small `errors.c` entry points into a single `api.go`.
The CPython source location is preserved in each function's doc
comment so the source-shape mapping stays auditable. Future phases
may split as the file grows.
