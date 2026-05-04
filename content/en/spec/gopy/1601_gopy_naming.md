---
title: "gopy naming conventions"
description: "Mechanical translation rules for converting CPython C identifiers to Go-idiomatic names while preserving 1:1 semantics."
tags: ["gopy", "spec"]
weight: 1601
---

# 1601. Naming conventions: CPython C to gopy Go

The port keeps **structure**, **logic**, and **field-by-field state**
identical to CPython. Only **identifier surface** changes. This file is the
canonical translation table. When in doubt, follow these rules.

## Guiding principles

1. **Preserve fidelity.** A Go reader should be able to grep CPython for the
   original symbol and find the Go counterpart in seconds.
2. **Look like Go stdlib.** Match conventions of `go/ast`, `go/parser`,
   `runtime`, `sync`, `encoding/binary`, `strconv`. Short package names,
   exported CamelCase, unexported camelCase, single-word interfaces with
   `-er` suffix where idiomatic.
3. **Drop redundancy.** `Py`/`_Py`/`_PyXXX_` prefixes go. Package
   qualification replaces them: `Py_DECREF` becomes `gc.Decref`,
   `_PyEval_EvalFrameDefault` becomes `vm.EvalDefault`, `PyDict_GetItem`
   becomes `dict.GetItem`.
4. **No abbreviations beyond CPython's own.** If CPython uses `tstate`, we
   use `ts` (or full `state.Thread`). If CPython uses `co`, we use `co` (or
   full `code.Code`). Don't invent new shorthands.

## Prefix translation table

| CPython prefix          | Go translation                                    |
|-------------------------|---------------------------------------------------|
| `Py_`                   | drop                                              |
| `_Py_`                  | drop (becomes unexported if leading underscore was internal-only) |
| `PyXxx_`                | package `xxx` + drop                              |
| `_PyXxx_`               | package `xxx` + drop, possibly unexported         |
| `pycore_xxx.h`          | package `xxx` (no `internal/`; the whole module is the implementation) |
| `Py_BUILD_*`            | `build.*` constants                               |
| `_Py_OPCODE_*`          | `opcode.*`                                        |

## Symbol class translation

| C class                    | Go class                                            |
|----------------------------|-----------------------------------------------------|
| `typedef struct { ... } Foo` | `type Foo struct { ... }`                         |
| `typedef enum { ... } Foo`   | `type Foo int` + `const ( ... Foo = iota )`       |
| `#define FOO_BAR 3`          | `const FooBar = 3` (or grouped iota where the C has a sequence) |
| function-like macro          | inlinable Go function (or, for very hot ones, an inlined helper kept short for the Go inliner) |
| top-level `static` func      | unexported package func                           |
| top-level non-static func    | exported package func                             |
| `struct _frame *f`           | `f *Frame`                                        |
| `Py_ssize_t`                 | `int` (Go's `int` is signed and at least 32-bit; Go has no `ssize_t`) |
| `int32_t`/`uint32_t`/etc.    | `int32`/`uint32` exactly                          |
| `Py_uhash_t`                 | `Hash` (alias for `uintptr` on 64-bit, `uint32` on 32-bit) |
| `Py_hash_t`                  | `Hash` (signed variant; CPython uses signed, we keep `Hash int64` for portability) |
| `PyObject *`                 | `Object` (interface), see "Object representation" below |

## Snake_case to CamelCase

The mapping is mechanical:

```
PyEval_EvalFrameDefault    => vm.EvalDefault
_PyEval_EvalFrameDefault   => vm.EvalDefault          (the public/private duo collapses)
_PyFrame_GetCode           => frame.Code
_PyFrame_StackPush         => (*Frame).StackPush      (method)
_PyOpcode_Caches[]         => opcode.Caches           (var, []uint8)
PySys_SetArgvEx            => sysmod.SetArgvEx        (package `sysmod`; `sys` is too generic in Go)
PyImport_ImportModule      => imp.Import              ("Module" is redundant)
_PyImport_BootstrapImp     => imp.Bootstrap
_PyTime_FromSeconds        => pytime.FromSeconds
_Py_HashSecret             => hash.Secret             (var)
_Py_NewReference           => gc.NewReference
Py_INCREF / Py_DECREF      => gc.Incref / gc.Decref
Py_XDECREF                 => gc.XDecref
Py_NewRef                  => gc.NewRef
Py_CLEAR                   => gc.Clear
Py_IS_TYPE(o, t)           => o.IsType(t)             (method on Object)
Py_TYPE(o)                 => o.Type()
PyType_Ready               => typeobj.Ready
PyArg_ParseTuple           => getargs.ParseTuple
PyArg_ParseTupleAndKeywords=> getargs.ParseTupleAndKw
Py_BuildValue              => modsupport.BuildValue
PyMem_Malloc / PyMem_Free  => mem.Alloc / mem.Free    (typically not needed in Go; see 1640)
```

When a C function is method-like (its first arg is a pointer to the "self"
struct), port it to a Go method on that type:

```
_PyFrame_GetCode(PyInterpreterFrame *f)      => (f *Frame) Code() *Code
_PyFrame_LocalsToFastUnsafe(f, ...)           => (f *Frame) LocalsToFast(...)
PyDict_GetItem(d, k)                          => (d *Dict).GetItem(k)
```

For functions that take *two* "selves" (e.g. `PyDict_Merge(a, b, override)`),
prefer the method form on the *destination* (mutated arg).

## Object representation

CPython's `PyObject *` becomes `Object` in Go. Two design choices, both
preserved from CPython:

```go
// Object is every Python value. Implementations live in the various
// type packages (int, str, list, dict, ...). The interface is intentionally
// thin; most operations dispatch via Type().Slot(...).
type Object interface {
    Type() *Type
    // ... no other methods. We dispatch through Type for slot calls,
    //     mirroring CPython's tp_* slot system.
}
```

Behind the scenes every value embeds a header equivalent to `PyObject`:

```go
// Header is the equivalent of CPython's PyObject struct. Every Python
// value's underlying type embeds Header at offset 0.
type Header struct {
    refcnt   int64        // Py_ssize_t ob_refcnt; immortal sentinel = _Py_IMMORTAL_REFCNT
    typ      *Type        // ob_type
    // GC linkage lives in a separately-allocated PyGC_Head for tracked types
    // (mirrors CPython's _PyObject_HEAD_INIT / _PyGC_Head adjacency).
}
```

For variable-size types (`PyVarObject`):

```go
type VarHeader struct {
    Header
    size int64          // ob_size
}
```

These types live in package `gopy/object` and are embedded by every
concrete type in its `gopy/<typename>` package.

## Field naming inside ported structs

When porting a CPython struct, **keep field order identical** (this matters
for some debugger offsets, see `pycore_debug_offsets.h`) and translate:

```c
struct _frame {
    PyObject ob_base;
    struct _frame *f_back;
    PyInterpreterFrame *f_frame;
    PyObject *f_trace;
    int f_lineno;
    char f_trace_lines;
    char f_trace_opcodes;
    char f_extra_locals_allocated;
    PyObject *f_locals_cache;
    PyObject *f_overwritten_fast_locals;
};
```

becomes

```go
type FrameObject struct {
    object.Header
    Back                   *FrameObject
    Frame                  *InterpreterFrame
    Trace                  Object
    Lineno                 int32
    TraceLines             bool
    TraceOpcodes           bool
    ExtraLocalsAllocated   bool
    LocalsCache            Object
    OverwrittenFastLocals  Object
}
```

Notes:
- `ob_base` is replaced by struct embedding (`object.Header`).
- The `f_` prefix is dropped; package + type qualifies it.
- `char` flags become `bool` *only* when used as 0/1; if used as a tri-state
  or counter, keep as `int8`.
- Pointer types preserve nilability semantics (a `NULL` PyObject* stays as a
  Go `nil` pointer or `nil` `Object` interface).

## Constants and enums

```c
typedef enum { COMPILER_SCOPE_MODULE, COMPILER_SCOPE_CLASS, ... } _PyCompile_scope_type;
```

becomes:

```go
type ScopeType int

const (
    ScopeModule ScopeType = iota
    ScopeClass
    ScopeFunction
    ScopeAsyncFunction
    ScopeLambda
    ScopeComprehension
    ScopeTypeParams
    ScopeTypeVariable
    ScopeTypeAlias
)
```

Numeric `#define` constants become typed Go constants where they have a
natural type, otherwise untyped:

```c
#define MARSHAL_VERSION 5
```

becomes:

```go
const Version = 5  // package marshal
```

Bitflags get their own typed `uint*` and a const block:

```c
#define CO_OPTIMIZED  0x0001
#define CO_NEWLOCALS  0x0002
```

becomes:

```go
type CodeFlags uint32

const (
    Optimized CodeFlags = 1 << iota
    NewLocals
    VarArgs
    VarKeywords
    Nested
    Generator
    NoFree
    Coroutine
    AsyncGenerator
    // ... preserve exact bit positions; do not reshuffle.
)
```

## Function signatures

```c
PyObject *PyEval_EvalCode(PyObject *co, PyObject *globals, PyObject *locals);
```

becomes:

```go
func EvalCode(co Object, globals, locals Object) Object
```

Error returns: CPython signals failure by returning `NULL` and setting the
thread-state's current exception. We **preserve** that protocol (with
`(*state.Thread).SetException` and `(*state.Thread).Exception`), because
1) it is the contract every port consumer expects, and 2) it lets us share
the eval loop unchanged. Some ports (`os` syscalls etc.) may *also* return
a Go `error` for convenience, but the canonical exception signal stays the
same.

```go
// EvalCode returns nil and sets the current thread's exception on failure.
func EvalCode(co Object, globals, locals Object) Object
```

For functions that return `int` (0/-1) we return `bool` *only* when the
function is purely a predicate. If the return is "0 = ok, -1 = error", we
keep `int` and document the convention, because mixing `bool` and exception
state is more confusing than helpful.

## File layout per package

Each Go package mirrors a single C file (or a tightly grouped set). Inside
each package:

```
gopy/<pkg>/
    doc.go           // package-level doc, references CPython source paths
    <name>.go        // main port of <name>.c
    <name>_test.go   // golden + property tests
    types.go         // struct/enum/const definitions if too large for <name>.go
    constants.go     // exported constants
    helpers.go       // unexported helpers (do not name this `internal.go`)
```

Note: we deliberately avoid Go's `internal/` directory convention. The
`tamnd/gopy` module's runtime packages live at the module root (`gopy/vm`,
`gopy/compile`, `gopy/gc`, etc.) so they can be imported by companion
modules (Go-native stdlib re-implementations, embedders) without the
`internal/` import barrier getting in the way.

We do **not** put one C file per Go file blindly. Group when reasonable.
For example `optimizer.c`, `optimizer_analysis.c`, `optimizer_bytecodes.c`,
and `optimizer_symbols.c` collapse into `gopy/optimizer/` with multiple .go
files inside.

## Tests

Each ported file gets a sibling `_test.go`. CPython's `Lib/test/test_xxx.py`
is the integration oracle but we also write targeted unit tests at the Go
level. Test data (e.g. golden bytecode disassembly) goes in `testdata/`.

## Cheat sheet

| You see                              | Type / port as                              |
|--------------------------------------|---------------------------------------------|
| `PyObject *`                         | `Object`                                    |
| `PyTypeObject *`                     | `*Type`                                     |
| `PyCodeObject *`                     | `*code.Code`                                |
| `PyFrameObject *`                    | `*frame.Object`                             |
| `_PyInterpreterFrame *`              | `*vm.InterpreterFrame`                      |
| `PyThreadState *tstate`              | `ts *state.Thread`                          |
| `PyInterpreterState *interp`         | `interp *state.Interpreter`                 |
| `_PyRuntimeState *runtime`           | `rt *state.Runtime`                         |
| `_PyOpcache_*`                       | `code.Cache*`                               |
| `_Py_CODEUNIT`                       | `code.Unit` (16-bit)                        |
| `_PyStackRef`                        | `vm.StackRef` (tagged uintptr)              |
| `Py_buffer`                          | `Buffer` (in package `buffer`)              |
| `PyObject *exc`                      | `exc Object` (same protocol)                |
| `PyObject *args, PyObject *kwargs`   | `args, kwargs Object`                       |

## What we DO NOT translate

- C preprocessor directives that gate platform features (`#ifdef HAVE_*`).
  Go doesn't need them. Use build tags only when *truly* platform-specific.
- `PyAPI_FUNC`/`PyAPI_DATA` decoration macros. Drop entirely.
- `Py_LOCAL_INLINE`, `Py_ALWAYS_INLINE`. Go decides inlining.
- `Py_UNUSED(x)`. Go has `_ = x`.
- `_Py_static_string` and the global string interning glue. Port to a
  package-level `var globalStr` initialized in `init()`.

## When you must deviate

If preserving the exact CPython API would produce un-Goish code (e.g. a
function that takes 12 positional bool flags), wrap it in a config struct.
But the *underlying* implementation must still walk the same code paths,
visit the same data, and set the same fields, so that the C-side test
suite passes.

Document any deviation in `1690_gopy_quirks.md` with a 2-line justification
and a link to the original C site.
