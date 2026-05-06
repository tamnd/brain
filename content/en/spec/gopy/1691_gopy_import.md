---
title: "gopy import"
description: "Port of cpython/Python/import.c (4956 lines) and Python/frozen.c (132 lines). Frozen module loader, sys.modules lookup, source and bytecode loaders, builtin module table, and the IMPORT_NAME / IMPORT_FROM / IMPORT_STAR bytecodes. Gates v0.8."
tags: ["gopy", "spec"]
weight: 1691
---

# 1691. Import system (Python/import.c, Python/frozen.c)

## What we are porting

`Python/import.c` (4956 lines) and `Python/frozen.c` (132 lines):
the full module import machinery.

The import system is the gating deliverable for v0.8. `import json;
json.dumps({"a": 1})` requires all of the following to work:

1. `sys.modules` dict lookup (fast path).
2. Frozen `importlib._bootstrap` bootstrap sequence.
3. A source-file loader (`.py` source to parse + compile + exec).
4. A .pyc bytecode-cache loader (read, validate via source hash or
   mtime, exec).
5. The `IMPORT_NAME`, `IMPORT_FROM`, and `IMPORT_STAR` bytecodes
   in the VM.
6. A builtin module table analogous to `PyImport_Inittab`.

CPython's import path flows through
`PyImport_ImportModuleLevelObject` (`Python/import.c:3460`), which
delegates to `importlib._bootstrap._find_and_load`, which walks
`sys.meta_path` finders. For v0.8, gopy bypasses `sys.meta_path`
and implements the two loaders directly in Go. Full `meta_path`
protocol comes later.

The frozen bootstrap blobs (`_frozen_importlib`,
`_frozen_importlib_external`, `_collections_abc`, `_sitebuiltins`)
are taken verbatim from CPython 3.14's
`Programs/_freeze_module`-generated C headers, converted to Go byte
literals. gopy re-uses the pre-compiled bytecode rather than
re-compiling with its own compiler, because the bytecode format is
identical.

### Key CPython functions

| Function | Location |
|---|---|
| `PyImport_ImportModuleLevelObject` | `Python/import.c:3460` |
| `PyImport_ImportFrozenModuleObject` | `Python/import.c:3095` |
| `init_importlib` | `Python/import.c:3185` |
| `PyImport_ExecCodeModuleObject` | `Python/import.c:2726` |
| `PyImport_GetModule` | `Python/import.c:149` |
| `PyImport_AddModuleObject` | `Python/import.c:160` |
| `PyImport_RemoveModule` | `Python/import.c:191` |
| `get_module_dict` (sys.modules accessor) | `Python/import.c:2549` |
| `PyImport_Inittab` builtin table | `Python/import.c` global |
| `FrozenModule` table | `Python/frozen.c` |
| `_find_frozen` | `Python/import.c:2836` |
| `IMPORT_NAME` bytecode | `Python/bytecodes.c` IMPORT_NAME |
| `IMPORT_FROM` bytecode | `Python/bytecodes.c` IMPORT_FROM |
| `IMPORT_STAR` bytecode | `Python/bytecodes.c` IMPORT_STAR |

### IMPORT_NAME

`Python/bytecodes.c IMPORT_NAME`: pops `fromlist` and `level` from
the stack, looks up `co_names[namei]`, calls
`PyImport_ImportModuleLevelObject(name, globals, locals, fromlist,
level)`, pushes the returned module.

### IMPORT_FROM

`Python/bytecodes.c IMPORT_FROM`: reads `co_names[namei]`, calls
`PyObject_GetAttr(module, name)`; on AttributeError with a package,
synthesises a more helpful error message before re-raising.

### IMPORT_STAR

`Python/bytecodes.c IMPORT_STAR`: if the module defines `__all__`,
iterates it and copies each attribute into the local namespace. If
`__all__` is absent, copies every attribute whose name does not start
with `_`.

## Go shape

```go
// FrozenModule mirrors struct _frozen from Include/cpython/import.h.
type FrozenModule struct {
    Name      string
    Code      []byte  // marshalled code object bytes
    IsPackage bool
}

// FindFrozen looks up name in the frozen module table.
// CPython: Python/import.c:2836 _find_frozen
func FindFrozen(name string) (*FrozenModule, bool)

// ExecFrozen imports a frozen module by name.
// Unmarshals Code, runs it in a new module, registers in sys.modules.
// CPython: Python/import.c:3095 PyImport_ImportFrozenModuleObject
func ExecFrozen(name string) (*objects.Module, error)

// ImportModuleLevel is the entry point for IMPORT_NAME.
// Handles relative-to-absolute resolution then delegates to the loader chain.
// CPython: Python/import.c:3460 PyImport_ImportModuleLevelObject
func ImportModuleLevel(name string, globals, locals *objects.Dict, fromlist *objects.Tuple, level int) (*objects.Module, error)

// AddModule returns or creates the sys.modules entry for name.
// CPython: Python/import.c:160 PyImport_AddModuleObject
func AddModule(name string) (*objects.Module, error)

// GetModule returns the module from sys.modules, or nil if absent.
// CPython: Python/import.c:149 PyImport_GetModule
func GetModule(name string) (*objects.Module, error)

// RemoveModule deletes name from sys.modules.
// CPython: Python/import.c:191 PyImport_RemoveModule
func RemoveModule(name string) error

// ExecCodeModule executes a code object in a new module and registers it.
// CPython: Python/import.c:2726 PyImport_ExecCodeModuleObject
func ExecCodeModule(name string, co *objects.Code, pathname, cpathname string) (*objects.Module, error)
```

## File mapping

| C source | Go target |
|---|---|
| `Python/frozen.c` frozen module table | `imp/frozen.go` |
| CPython 3.14 frozen bytecode blobs | `imp/frozen_bootstrap.go` (generated) |
| `Python/import.c:149` `PyImport_GetModule` | `imp/sysmodules.go` |
| `Python/import.c:160` `PyImport_AddModuleObject` | `imp/sysmodules.go` |
| `Python/import.c:191` `PyImport_RemoveModule` | `imp/sysmodules.go` |
| `Python/import.c:2549` `get_module_dict` | `imp/sysmodules.go` |
| `Python/import.c:3460` `PyImport_ImportModuleLevelObject` | `imp/import.go` |
| `Python/import.c:3095` `PyImport_ImportFrozenModuleObject` | `imp/frozen.go` |
| `Python/import.c:2726` `PyImport_ExecCodeModuleObject` | `imp/exec.go` |
| `Python/import.c:3185` `init_importlib` | `imp/bootstrap.go` |
| `PyImport_Inittab` builtin module table | `imp/inittab.go` |
| .pyc cache read/write helpers | `imp/loader.go` |
| `Python/bytecodes.c` IMPORT_NAME | `vm/opcodes_import.go` |
| `Python/bytecodes.c` IMPORT_FROM | `vm/opcodes_import.go` |
| `Python/bytecodes.c` IMPORT_STAR | `vm/opcodes_import.go` |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Prerequisites (must land before this spec)

* [ ] `objects/module.go`: Module struct, `NewModule(name string)`,
  `GetAttr` routing through `__dict__` with PEP 562 `__getattr__`
  fallback, `SetAttr`, `__dir__`, repr
  (`<module 'name' from 'path'>`). CPython: `Objects/moduleobject.c`.
* [ ] `objects/exc_import.go`: `ImportError(msg, name, path)`,
  `ModuleNotFoundError` as a subclass of `ImportError`.
  CPython: `Objects/exceptions.c` ImportError arm.

### imp/frozen.go

* [ ] `FrozenModule` struct matching `struct _frozen`
  (`Include/cpython/import.h`).
* [ ] `frozenModules` slice (the Go equivalent of the C `_PyImport_FrozenModules`
  array). Entries: `_frozen_importlib`, `_frozen_importlib_external`,
  `_collections_abc`, `_sitebuiltins`. CPython: `Python/frozen.c`.
* [ ] `FindFrozen(name string)`: linear scan of `frozenModules`,
  returns `(*FrozenModule, bool)`. CPython: `Python/import.c:2836 _find_frozen`.
* [ ] `ExecFrozen(name string)`: call `marshal.ReadCodeFromBytes`,
  then `ExecCodeModule`. CPython: `Python/import.c:3095
  PyImport_ImportFrozenModuleObject`.
* [ ] Frozen packages set `__path__` to `[name]` on the module after exec.
  CPython: `Python/import.c:3095` package path fixup.

### imp/frozen_bootstrap.go

* [ ] `frozenImportlibBootstrap []byte`: copy the `uint8` array from
  CPython 3.14 `Python/frozen_modules/importlib._bootstrap.h` verbatim
  as a Go byte literal. Do not attempt to compile from source.
* [ ] `frozenImportlibExternalBootstrap []byte`: same from
  `Python/frozen_modules/importlib._bootstrap_external.h`.
* [ ] `frozenCollectionsAbc []byte`: same from
  `Python/frozen_modules/abc.h` (which backs `_collections_abc`).
* [ ] `frozenSitebuiltins []byte`: same from
  `Python/frozen_modules/site.h` (which backs `_sitebuiltins`).
* [ ] Each array is referenced by the `FrozenModule` entries in
  `imp/frozen.go`.

### imp/sysmodules.go

* [ ] `GetModule(name string)`: look up `sys.modules[name]`, return
  nil if absent or if value is `None` (the "blocked" sentinel).
  CPython: `Python/import.c:149 PyImport_GetModule`.
* [ ] `AddModule(name string)`: if `sys.modules[name]` already exists
  and is a module, return it; otherwise create a new `objects.Module`
  with `__name__ = name`, insert it, return it.
  CPython: `Python/import.c:160 PyImport_AddModuleObject`.
* [ ] `RemoveModule(name string)`: delete from `sys.modules`.
  CPython: `Python/import.c:191 PyImport_RemoveModule`.
* [ ] `modulesDict()`: return the `*objects.Dict` for `sys.modules`.
  CPython: `Python/import.c:2549 get_module_dict`.

### imp/bootstrap.go

* [ ] `InitImportlib()`: the bootstrap sequence run once at interpreter
  startup. CPython: `Python/import.c:3185 init_importlib`.
  Steps:
  1. Create a minimal `_imp` builtin module (see `imp/inittab.go`).
  2. Call `ExecFrozen("_frozen_importlib")`.
  3. Retrieve `_frozen_importlib._install(sys, _imp)` and call it.
  4. Call `ExecFrozen("_frozen_importlib_external")`.
  5. Call `_frozen_importlib_external._install(_frozen_importlib)`.
* [ ] If bootstrap fails, return a wrapped `ImportError` with the
  module name and cause. CPython: `Python/import.c:3185` error path.

### imp/inittab.go

* [ ] `Inittab`: a `map[string]func() (*objects.Module, error)` that
  maps builtin module names to their initializer.
  CPython: `Python/import.c` `PyImport_Inittab` global array.
* [ ] Initial entries: `_imp` (the import helper functions that
  `_frozen_importlib` calls back into Go for), `_io` stub.
* [ ] `_imp` module must expose at minimum:
  `is_frozen(name)`, `is_builtin(name)`, `create_builtin(spec)`,
  `exec_builtin(mod)`, `is_frozen_package(name)`,
  `get_frozen_object(name)`, `create_dynamic`, `exec_dynamic`.
  CPython: `Python/import.c` `_imp` method table.
* [ ] `FindBuiltin(name string)`: check `Inittab` and return the
  initializer function if present.

### imp/exec.go

* [ ] `ExecCodeModule`: create a new `objects.Module` via `AddModule`,
  set `__file__` to `pathname`, set `__cached__` to `cpathname`,
  set `__loader__` to the loader used, eval the code object in the
  module's `__dict__`, return the module.
  CPython: `Python/import.c:2726 PyImport_ExecCodeModuleObject`.
* [ ] On eval error, remove the module from `sys.modules` before
  returning the error. CPython: `Python/import.c:2726` cleanup path.
* [ ] Set `__spec__` on the module after exec using a minimal
  `ModuleSpec` struct. CPython: `Python/import.c:2726` spec fixup.

### imp/loader.go

* [ ] `LoadSource(name, path string)`: read `.py` file, parse + compile
  to a code object, optionally validate or write a `.pyc` cache,
  then call `ExecCodeModule`.
* [ ] Source-file hash computation for the `.pyc` cache: SipHash-1-3
  of the source bytes, matching `Lib/importlib/_bootstrap_external.py
  _get_hash`.
* [ ] `.pyc` cache path: `__pycache__/<stem>.cpython-314.pyc` next to
  the source file. CPython: `Lib/importlib/_bootstrap_external.py
  cache_from_source`.
* [ ] Read `.pyc` via `marshal.ReadPyc`; on stale/missing cache, fall
  back to compiling from source and writing a fresh `.pyc`.
* [ ] Write `.pyc` via `marshal.WritePyc` after successful compile.
* [ ] `LoadBytecode(name, cpathname string)`: load directly from a
  `.pyc` file without a `.py` counterpart.

### imp/import.go

* [ ] `ImportModuleLevel`: CPython: `Python/import.c:3460
  PyImport_ImportModuleLevelObject`.
  1. Resolve relative `level` to an absolute name using the `__package__`
     or `__spec__.parent` of `globals`.
  2. Fast path: return immediately if `sys.modules[absname]` exists and
     is not `None`.
  3. Try `FindFrozen`; if found, call `ExecFrozen`.
  4. Try `FindBuiltin`; if found, call the initializer.
  5. Try `LoadSource` by searching `sys.path`.
  6. If nothing found, raise `ModuleNotFoundError`.
* [ ] `resolveRelative(level int, globals *objects.Dict) string`:
  strips `level` components from `__package__` (or infers package from
  `__name__`). CPython: `Python/import.c:3460` relative resolution
  block.
* [ ] On successful import return the top-level name if `fromlist` is
  empty, or the final sub-module if `fromlist` is non-empty.
  CPython: `Python/import.c:3460` fromlist handling.

### vm/opcodes_import.go

* [ ] `IMPORT_NAME` handler: pop `fromlist` (TOS) and `level` (TOS1)
  from the value stack, read `co_names[namei]`, call
  `imp.ImportModuleLevel`, push result.
  CPython: `Python/bytecodes.c IMPORT_NAME`.
* [ ] `IMPORT_FROM` handler: peek at TOS (the module), read
  `co_names[namei]`, call `objects.GetAttr`; on `AttributeError`
  synthesise the "cannot import name 'X' from 'Y'" message before
  re-raising. CPython: `Python/bytecodes.c IMPORT_FROM`.
* [ ] `IMPORT_STAR` handler: pop module from stack, check for `__all__`;
  if present, iterate it and `STORE_NAME` each attribute; if absent,
  iterate `module.__dict__` and store each key not starting with `_`.
  CPython: `Python/bytecodes.c IMPORT_STAR`.

### Tests

* [ ] `imp/import_test.go`: import a frozen module (`_collections_abc`);
  verify `sys.modules["_collections_abc"]` is set after the call.
* [ ] `imp/import_test.go`: import a temp `.py` file written to a
  `t.TempDir`; verify the module attribute set in that file is
  accessible.
* [ ] `imp/import_test.go`: second `GetModule` call for an already-imported
  module returns the same `*objects.Module` pointer without re-executing.
* [ ] `imp/import_test.go`: `level=1` relative import resolves against
  `globals["__package__"]`.
* [ ] `imp/import_test.go`: importing an absent module raises
  `ModuleNotFoundError`.
* [ ] `imp/loader_test.go`: `LoadSource` round-trip: write a `.py` file,
  call `LoadSource`, verify a `.pyc` was created; call again and verify
  the `.pyc` is used (stub the compile step to detect re-use).
* [ ] `imp/loader_test.go`: stale `.pyc` (wrong source hash) causes
  re-compile.
* [ ] Gate test: `gopy -c "import json; print(json.dumps({'a': 1}))"` exits
  0 and prints `{"a": 1}`.

## Cross-references

* `marshal.ReadPyc` / `marshal.WritePyc` used by `imp/loader.go`: 1690.
* `objects.Module`: 1688 (`Objects/moduleobject.c`).
* `objects.Code` needed by `ExecCodeModule`: 1687.
* `ImportError` / `ModuleNotFoundError`: 1686.
* VM eval loop that dispatches IMPORT_NAME etc.: 1620 hot path.
* `sys.path`, `sys.modules`, `sys.meta_path` wiring: `sys/` package
  (spec 1630 area).

## Out of scope

* `importdl.c`: C-extension (`.so` / `.pyd`) loading. Not applicable
  since gopy does not link C extensions.
* Multi-phase module init (PEP 489). Deferred past v0.8.
* Namespace packages (PEP 420 / implicit namespaces). Deferred to v0.9.
* `zipimport`: zip-file importer. Deferred.
* Import locking (`_PyImport_AcquireLock`). gopy is single-threaded
  through v0.10; the lock is a no-op stub.
* Full `sys.meta_path` / `sys.path_hooks` protocol. v0.8 uses the
  direct Go loader chain; full protocol in v0.9.
* `importlib.util`, `importlib.resources`, `importlib.metadata`. Stdlib
  bridge, not part of `Python/import.c`.
