---
title: "gopy lifecycle"
description: "Port of cpython/Python/pylifecycle.c, preconfig.c, initconfig.c, interpconfig.c, pathconfig.c. Py_Initialize / Py_Finalize and the config plumbing they consume."
tags: ["gopy", "spec"]
weight: 1622
---

# 1622. Lifecycle: initialize, finalize, configuration

## What we are porting

Five C files, ~11k lines total, that together drive the
runtime from cold start to `Py_Initialize()` returning, and
back down through `Py_Finalize()`:

* `Python/pylifecycle.c` (~3.6k lines). The `Py_Initialize` and
  `Py_Finalize` entry points plus the staged init phases:
  preinit, core, main. Sets up the runtime, builtins, sys, the
  initial thread state, and the import system.
* `Python/preconfig.c` (~1k lines). Pre-init: locale, encoding
  detection, `-X` flags read before site.py runs.
* `Python/initconfig.c` (~4.7k lines). The full `PyConfig`
  schema, env-var and CLI parsing, defaults, validation.
* `Python/pathconfig.c` (~600 lines). `sys.path` defaults,
  prefix/exec_prefix discovery, `PYTHONHOME` handling.
* `Python/interpconfig.c` (~300 lines). Per-sub-interpreter
  config knobs (mostly relevant in v0.13).

The companion `Python/pythonrun.c` lives in spec 1624 because
its surface (REPL, `PyRun_*`) is consumer-facing rather than
init-time.

## Why this lands in v0.7

In v0.6 the `cmd/gopy` entry point hand-rolled a tiny boot
sequence: `state.NewThread`, `builtins.Init`, then
`vm.EvalCode`. v0.7 replaces that with the real CPython
lifecycle so `gopy -c` and `gopy script.py` both flow through
`Py_Initialize` / `pythonrun` / `Py_Finalize`. Once 1622 is
in place, every later subsystem (import in v0.8, contextvars
in v0.9, monitor in v0.11) can attach via the standard init
hooks instead of bespoke wiring.

## Package layout

```
gopy/
  initconfig/             # 1622 — preconfig + initconfig
    preconfig.go
    config.go
    config_env.go         # PYTHON* env-var parsing
    config_cli.go         # CLI -X / -c / -m parsing
    config_validate.go
  pathconfig/             # 1622 — path discovery
    pathconfig.go
    pathconfig_unix.go
    pathconfig_win.go
  lifecycle/              # 1622 — Py_Initialize / Py_Finalize
    init.go
    init_phases.go
    finalize.go
    interp.go
    main.go               # the Py_Main equivalent that cmd/gopy calls
  pythonrun/              # 1624 — separate spec, listed for context
    runstring.go
    runfile.go
    repl.go
    pyc.go
```

Existing v0.6 packages it touches:

* `gopy/state` — Runtime / Interpreter / Thread already exist
  but were minimal. Lifecycle wires them through the real init.
* `gopy/builtins` — `builtins.Init` keeps its signature but
  becomes one of the init phases instead of the entry point.
* `gopy/cmd/gopy` — `main.go` shrinks to a thin
  `lifecycle.Main(os.Args)` call.

## Init staging (the porting unit)

CPython splits init into ordered phases. We mirror them
one-for-one because import, signals, codecs, and warnings each
attach at a specific phase and changing the order would change
when their callbacks fire.

| Phase                     | CPython call                              | gopy entry                          |
|---------------------------|-------------------------------------------|-------------------------------------|
| pre-init: locale + UTF-8  | `_PyPreConfig_Read`                       | `initconfig.PreConfig.Read`         |
| pre-init: allocators      | `_PyPreConfig_InitFromPreConfig`          | `initconfig.PreConfig.Apply`        |
| core init: runtime alloc  | `pyinit_core` step 1                      | `lifecycle.initRuntime`             |
| core init: types          | `_PyTypes_InitTypes`                      | (handled in objects, called here)   |
| core init: builtins       | `_PyBuiltin_Init`                         | `builtins.Init` (already exists)    |
| core init: sys            | `_PySys_Create`                           | `sysmod.Init` (1651)                |
| core init: import system  | `init_importlib_external`                 | (deferred to v0.8 spec 1623)        |
| main init: site/userpath  | `init_set_builtins_open`, `pymain_run_*`  | `pythonrun.*` (1624)                |
| finalize: shutdown phases | `Py_FinalizeEx`                           | `lifecycle.Finalize`                |

Each row maps to one Go function with a CPython citation. The
spec 1622 work order is top-to-bottom: a phase only lands when
the phase above it lands.

## v0.7 release blockers

Tracked as individual tasks; each one must close before
tagging v0.7.0.

* `1622-A` Port `PyPreConfig` struct + defaults +
  `PyPreConfig_InitPythonConfig`.
  CPython: `Python/preconfig.c:33 PyPreConfig_InitPythonConfig`.
* `1622-B` Port the `PYTHON*` env-var reader subset gopy
  honours (`PYTHONHOME`, `PYTHONPATH`, `PYTHONHASHSEED`,
  `PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED`, `PYTHONUTF8`,
  `PYTHONDEBUG`, `PYTHONVERBOSE`, `PYTHONOPTIMIZE`,
  `PYTHONNOUSERSITE`).
  CPython: `Python/initconfig.c:_Py_str_to_int` panel.
* `1622-C` Port the `PyConfig` struct (the v0.7 subset; full
  schema lands incrementally with later phases).
* `1622-D` Port `PyConfig_Read` (env then CLI then defaults).
  CPython: `Python/initconfig.c:_PyConfig_Read`.
* `1622-E` Port `pyinit_core` and `pyinit_main` skeletons.
  CPython: `Python/pylifecycle.c:pyinit_core`,
  `Python/pylifecycle.c:pyinit_main`.
* `1622-F` Port the path-config defaults for `darwin` and
  `linux` (Windows arrives later).
  CPython: `Modules/getpath.py` is the modern source — gopy
  reimplements the resolved logic in Go.
* `1622-G` Port `Py_Finalize` shutdown order (modules, sys,
  threads, types, runtime).
  CPython: `Python/pylifecycle.c:Py_FinalizeEx`.
* `1622-H` `lifecycle.Main` entry: parses args, runs init,
  hands off to `pythonrun`, runs finalize.
  CPython: `Modules/main.c:Py_Main`.

## Test gates

* `lifecycle/init_test.go` — Initialize, ask for
  `state.GetThreadState()`, Finalize, Initialize again. Must
  not panic and must not leak goroutines (counted via
  `runtime.NumGoroutine`).
* `lifecycle/main_test.go` — feed `[]string{"-c", "print(1+2)"}`
  through `lifecycle.Main` with a captured stdout. Output is
  `"3\n"` and exit code 0.
* `initconfig/config_test.go` — env-var precedence: a flag set
  in env is overridden by a CLI value; CLI is overridden by an
  explicit `PyConfig` field set after `Read`.
* `pathconfig/pathconfig_unix_test.go` — given a synthetic
  prefix layout (a temp dir with `lib/python3.14/`), the
  resolved `sys.path` matches the documented order from
  `Doc/using/cmdline.rst`.

## Out of scope for v0.7

* `Py_NewInterpreter` and the sub-interpreter init flow stays
  stubbed; spec 1622 lands a single-interpreter shape.
* The `pymain_run_module` import-driven case (`gopy -m foo`)
  is gated on import (v0.8); v0.7 returns
  `ErrNotImplemented`.
* `Py_BytesMain` (the wide-char Windows entry) is deferred.

## CPython divergences worth pinning here

* gopy never reads C-level allocator hooks (`PyMemAllocatorEx`)
  because Go owns allocation. The fields exist on
  `PyPreConfig` for shape parity but have no effect.
* `sys.implementation.cache_tag` is `"gopy-3140"` (see
  1690_quirks). The init code that builds `sys.implementation`
  must hard-code this string and pin it in tests.
