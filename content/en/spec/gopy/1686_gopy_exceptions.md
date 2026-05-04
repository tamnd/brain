---
title: "gopy exceptions"
description: "Port of cpython/Objects/exceptions.c. The full BaseException hierarchy with the args slot byte-equal to CPython for every constructor."
tags: ["gopy", "spec"]
weight: 1686
---

# 1686. Exceptions

## What we are porting

`Objects/exceptions.c` (~3000 lines). The full exception class
hierarchy plus the special slots (`__traceback__`, `__cause__`,
`__context__`, `__suppress_context__`, `__notes__`) and the
constructor-specific args-slot handling.

The hierarchy is wide: BaseException -> Exception -> ArithmeticError
-> {OverflowError, FloatingPointError, ZeroDivisionError},
LookupError -> {IndexError, KeyError}, OSError with the platform
errno subclasses (FileNotFoundError, PermissionError, etc.),
SyntaxError with the position fields, ImportError with name/path,
StopIteration with value, and so on. ~70 leaf classes total.

v0.3 already shipped BaseException and the gating subset (1611);
this spec is the full panel.

## Go shape

```go
// BaseException is the root. Mirrors PyBaseExceptionObject.
type BaseException struct {
    Header
    Args             *Tuple
    Traceback        Object  // *Traceback or None
    Cause            Object  // BaseException or None
    Context          Object  // BaseException or None
    SuppressContext  bool
    Notes            *List   // PEP 678
    Dict             *Dict   // instance __dict__
}
```

Each subclass either reuses BaseException's struct directly or
embeds it and adds typed fields. The typed fields appear on:

* `SyntaxError`: msg, filename, lineno, offset, text, end_lineno,
  end_offset, print_file_and_line.
* `ImportError`: msg, name, path.
* `OSError`: errno, strerror, filename, filename2,
  characters_written.
* `UnicodeError` / Unicode{Encode,Decode,Translate}Error:
  encoding, object, start, end, reason.
* `StopIteration`: value.
* `KeyError`: overrides `__str__` (the only subclass that does).

## KeyError __str__

KeyError's `__str__` returns `repr(args[0])` when `len(args) == 1`,
otherwise falls through to BaseException's `__str__`. The override
exists so `str({}[k])` shows the missing key with quotes if it is a
string. Pinned by 1611 and re-exercised here.

## OSError errno mapping

OSError dispatches on errno at construction time to the right
subclass:

```
EINTR  -> InterruptedError
EAGAIN -> BlockingIOError
EPIPE  -> BrokenPipeError
EISDIR -> IsADirectoryError
...
```

Same mapping table as CPython. We hand-port the table from
`exceptions.c:_PyErr_OSErrorTraversalSetClassesEntry`.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Objects/exceptions.c` BaseException    | `objects/exc_base.go` (already in 1611)  |
| Exception / StopIteration / GeneratorExit | `objects/exc_simple.go`                |
| ArithmeticError + subclasses            | `objects/exc_arithmetic.go`              |
| LookupError / IndexError / KeyError     | `objects/exc_lookup.go`                  |
| OSError + errno-mapped subclasses       | `objects/exc_os.go`                      |
| SyntaxError                             | `objects/exc_syntax.go`                  |
| ImportError + Module/Modulenot variants | `objects/exc_import.go`                  |
| UnicodeError + 4 variants               | `objects/exc_unicode.go`                 |
| Warning + subclasses                    | `objects/exc_warnings.go`                |
| ExceptionGroup / BaseExceptionGroup     | `objects/exc_group.go`                   |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [~] `objects/exc_base.go`: BaseException with args, traceback,
  cause, context, suppress_context, notes, dict. v0.3 shipped.
* [~] `objects/exc_lookup.go`: LookupError, IndexError, KeyError
  with the `__str__` override. v0.3 shipped.
* [ ] `objects/exc_simple.go`: Exception, StopIteration (with
  value), StopAsyncIteration, GeneratorExit, AssertionError,
  AttributeError (with name/obj), NameError (with name),
  UnboundLocalError, RuntimeError, NotImplementedError,
  RecursionError, ReferenceError, BufferError, MemoryError,
  EOFError, KeyboardInterrupt, SystemExit (with code),
  TypeError, ValueError, TimeoutError.
* [ ] `objects/exc_arithmetic.go`: ArithmeticError,
  OverflowError, FloatingPointError, ZeroDivisionError.
* [ ] `objects/exc_os.go`: OSError with the errno -> subclass
  mapping; BlockingIOError, ChildProcessError,
  ConnectionError + 4 subclasses, FileExistsError,
  FileNotFoundError, InterruptedError, IsADirectoryError,
  NotADirectoryError, PermissionError, ProcessLookupError,
  TimeoutError.
* [ ] `objects/exc_syntax.go`: SyntaxError with msg, filename,
  lineno, offset, text, end_lineno, end_offset, plus
  IndentationError and TabError.
* [ ] `objects/exc_import.go`: ImportError with name/path,
  ModuleNotFoundError.
* [ ] `objects/exc_unicode.go`: UnicodeError, UnicodeEncodeError,
  UnicodeDecodeError, UnicodeTranslateError with encoding,
  object, start, end, reason.
* [ ] `objects/exc_warnings.go`: Warning + DeprecationWarning,
  PendingDeprecationWarning, SyntaxWarning, RuntimeWarning,
  FutureWarning, ImportWarning, UnicodeWarning, BytesWarning,
  ResourceWarning, EncodingWarning.
* [ ] `objects/exc_group.go`: BaseExceptionGroup,
  ExceptionGroup, with `split`, `subgroup`, `derive`. PEP 654.
* [ ] `objects/exc_test.go`: args byte-equality panel, errno
  mapping, KeyError `__str__`.

### Surface guarantees

* [x] `KeyError({}).__str__()` matches CPython byte-for-byte.
  Pinned by 1611.
* [ ] Args slot is byte-equal to CPython for every constructor
  in the hierarchy. Pinned by `compat/exc_args_test.go`.
* [ ] OSError(errno=2) returns FileNotFoundError per the errno
  table.
* [ ] SyntaxError pretty-print includes the caret line for
  end_offset > offset.
* [ ] ExceptionGroup `split` partitions per the type or callable
  predicate; cause / context propagate.
* [ ] `__notes__` survives pickling (lands with v0.8 marshal).
* [ ] `repr(exc)` matches CPython (uses the class name plus
  `repr(args)`).
* [ ] `raise X from Y` sets `__cause__` and
  `__suppress_context__ = True`.

### Cross-references

* errors package raise/normalise: 1611.
* Traceback object: 1687 (alongside frame).
* Print exception (sys.excepthook default): 1611 / sysconfig.

### Out of scope

* User-defined exception subclassing through Python `class` syntax.
  Lands once user types are reachable (v0.7).
