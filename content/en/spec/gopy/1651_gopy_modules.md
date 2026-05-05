---
title: "gopy modules"
description: "Port of cpython/Python/bltinmodule.c (subset), sysmodule.c (subset), _warnings.c, and the _contextvars hook. The minimum builtins/sys surface v0.7 needs to ship."
tags: ["gopy", "spec"]
weight: 1651
---

# 1651. Modules: builtins, sys, _warnings

## What we are porting

Three companion modules that the runtime hands to user code as
soon as `Py_Initialize` returns:

* `Python/bltinmodule.c` (the v0.7 subset listed below). The
  `builtins` module: `print`, `len`, `range`, `iter`, `abs`,
  `type`, `isinstance`, `repr`, `str`, `int`, `float`, `list`,
  `tuple`, `dict`, `set`, `getattr`, `setattr`, `hasattr`,
  `callable`, `id`, `hash`, `sorted`, `reversed`, `enumerate`,
  `zip`, `map`, `filter`, `sum`, `min`, `max`, `any`, `all`,
  `divmod`, `pow`, `chr`, `ord`, `bin`, `oct`, `hex`, `ascii`,
  `format`, `vars`, `dir`.
* `Python/sysmodule.c` (the v0.7 subset). The `sys` module:
  `path`, `modules`, `argv`, `version`, `version_info`,
  `flags`, `implementation`, `stdin`, `stdout`, `stderr`,
  `exit`, `getrefcount`, `setrecursionlimit`,
  `getrecursionlimit`, `executable`, `platform`,
  `byteorder`, `maxsize`, `intern`.
* `Python/_warnings.c` (~1.5k lines). The `_warnings` module
  that backs `warnings.warn`. Includes the filter list, the
  default actions, and the once-per-location dedup.
* `Python/_contextvars.c` is a one-line module init hook;
  the actual ContextVar implementation lives in spec 1663
  (v0.9). v0.7 ships the import hook only so `import
  _contextvars` works.

## Why this lands in v0.7

`Py_Initialize` (spec 1622) must produce a usable interpreter,
which means `print`, `len`, `range` and `sys.path` have to be
populated by the time `pythonrun.RunString` (spec 1624) takes
over. The v0.6 builtins package shipped just `print`; v0.7
fills in the rest.

`_warnings` has to land in v0.7 because `DeprecationWarning`
and `PendingDeprecationWarning` are emitted from the eval
loop and codecs paths gopy already exercises.

## Package layout

```
gopy/builtins/
  init.go             # _PyBuiltin_Init: registers everything below
  abs.go              # abs / divmod / pow / round
  bool_int_float.go   # bool / int / float / complex
  bytes_str.go        # bytes / bytearray / str / chr / ord / ascii / bin / oct / hex
  collections.go      # list / tuple / dict / set / frozenset
  iters.go            # iter / next / reversed / enumerate / zip / map / filter
  reflect.go          # type / isinstance / issubclass / getattr / setattr / hasattr
                      # delattr / vars / dir / id / hash / callable / repr
  sequence_aggs.go    # sum / min / max / any / all / sorted / len
  format.go           # format / range / slice
  exec_eval.go        # exec / eval / compile (stubbed v0.7; full v0.8)

gopy/sysmod/
  init.go             # _PySys_Create
  attributes.go       # path, argv, version, flags, implementation
  recursion.go        # set/getrecursionlimit, getrefcount
  io.go               # stdin/stdout/stderr placeholders (real wiring in v0.8)
  intern.go

gopy/warnings/
  warnings.go         # _Py_Warn family
  filters.go          # filter list and default actions
  registry.go         # __warningregistry__ per-module dedup
```

## v0.7 release blockers

builtins (spec drives ~30 individual tasks; grouped in the
release rollup):

* `1651-builtins-A` `len`, `iter`, `next`, `reversed`,
  `enumerate`, `zip`, `range`. The iteration panel.
* `1651-builtins-B` `type`, `isinstance`, `issubclass`,
  `callable`, `id`, `hash`, `repr`, `str`. The reflection
  panel.
* `1651-builtins-C` `getattr`, `setattr`, `hasattr`,
  `delattr`, `vars`, `dir`. The attribute panel.
* `1651-builtins-D` `sum`, `min`, `max`, `any`, `all`,
  `sorted`. The aggregation panel (sorted needs Timsort from
  spec 1679 which is already in objects).
* `1651-builtins-E` `abs`, `divmod`, `pow`, `chr`, `ord`,
  `bin`, `oct`, `hex`, `ascii`, `format`. The numeric and
  formatting panel.
* `1651-builtins-F` Constructor wrappers `int(...)`,
  `float(...)`, `bool(...)`, `list(...)`, `tuple(...)`,
  `dict(...)`, `set(...)`. These call into the existing object
  ports.

sys:

* `1651-sys-A` `_PySys_Create` plus the static attribute
  panel (version, version_info, platform, byteorder, maxsize,
  implementation).
  CPython: `Python/sysmodule.c:_PySys_Create`.
* `1651-sys-B` `sys.path`, `sys.argv`, `sys.modules` populated
  from `PyConfig` (1622).
* `1651-sys-C` `sys.flags` named-tuple bound to the
  `PyConfig` int fields.
* `1651-sys-D` `sys.exit`, `sys.setrecursionlimit`,
  `sys.getrecursionlimit`, `sys.getrefcount`, `sys.intern`.
* `1651-sys-E` Pin `sys.implementation.name == "gopy"` and
  `sys.implementation.cache_tag == "gopy-3140"` per spec 1690.

_warnings:

* `1651-warn-A` Port `_Py_Warn`, `_Py_Warn_NoCharField`, the
  filter list, and the default rule set.
* `1651-warn-B` Per-module `__warningregistry__` dedup.
* `1651-warn-C` `simplefilter`, `filterwarnings`,
  `resetwarnings` so user code can install filters.

## Test gates

* `builtins/init_test.go` — after `Init`, the returned
  globals dict has every name from the v0.7 panel.
* `builtins/print_test.go` (already in v0.6) keeps passing.
* `builtins/<file>_test.go` — table-driven tests per file
  comparing gopy output to `python3 -c "print(<expr>)"`.
* `sysmod/sysmod_test.go` — `sys.version_info` is the right
  named tuple; `sys.path[0]` is the script directory after
  Main runs against a script.
* `warnings/warnings_test.go` — install a filter, emit a
  warning, assert `__warningregistry__` carries the entry and
  the second emission is suppressed.

## Out of scope

* `compile`, `exec`, `eval` builtins land as stubs that call
  through to the v0.6 parser+compile+vm pipeline only when the
  caller passes pre-validated source. The full PEP 263 source
  encoding handshake is deferred to v0.8 with import.
* `breakpoint()` is not wired (depends on monitor; v0.11).
* `help()`, `copyright()`, `credits()`, `license()` are not
  wired (they live in `site.py`).
