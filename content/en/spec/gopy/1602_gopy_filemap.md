---
title: "gopy file map"
description: "One-line per CPython source file, with the target Go package path and a short purpose note. Canonical lookup table for porters."
tags: ["gopy", "spec"]
weight: 1602
---

# 1602. File map: `cpython/Python/*` to `gopy/*`

The mapping is **one-to-many**: a CPython file may split across several Go
files (or vice-versa). Where multiple C files collapse into one Go package,
the package's `doc.go` lists the source files it derives from.

Conventions:
- All Go packages live at the **module root** (`gopy/<pkg>`). We do **not**
  use Go's `internal/` directory convention. See 1601 for rationale.
- Files named like `dynload_*.c` and `emscripten_*.c` are platform glue we
  do not port. Go's runtime handles the equivalents. They are listed here
  for completeness with a `--` Go target.
- Generated headers (`generated_cases.c.h`, `executor_cases.c.h`,
  `optimizer_cases.c.h`, `opcode_targets.h`) are regenerated from the
  CPython DSL via our own Go-emitting code generator. See 1621.

## Compiler pipeline

| C file                          | Go target                                     | Purpose                                          |
|---------------------------------|-----------------------------------------------|--------------------------------------------------|
| `Python/asdl.c`                 | `ast/asdl.go`                                 | ASDL sequence helpers (`asdl_seq_*`)             |
| `Python/Python-ast.c`           | `ast/nodes_gen.go` (generated)                | Generated AST node constructors                  |
| `Python/ast.c`                  | `ast/validate.go`                             | `_PyAST_Validate`                                |
| `Python/ast_preprocess.c`       | `ast/preprocess.go`                           | Constant fold, PEP 765 control-flow checks       |
| `Python/ast_unparse.c`          | `ast/unparse.go`                              | AST → source (annotations)                       |
| `Python/symtable.c`             | `symtable/`                                   | Two-pass symbol table builder                    |
| `Python/future.c`               | `future/future.go`                            | `__future__` extraction                          |
| `Python/compile.c`              | `compile/compiler.go`                         | Pipeline orchestration                           |
| `Python/codegen.c`              | `compile/codegen.go` plus `codegen_*.go` panel | AST → instruction sequence (split per stmt/expr family) |
| `Python/instruction_sequence.c` | `compile/instrseq.go`                         | Labeled instruction sequence                     |
| `Python/flowgraph.c`            | `compile/flowgraph.go`, `flowgraph_passes.go`, `flowgraph_stackdepth.go` | CFG build + optimization panel + stackdepth |
| `Python/assemble.c`             | `compile/assemble.go`, `assemble_locations.go`, `assemble_exceptions.go`, `assemble_varint.go` | Bytecode + PEP 626 line table + PEP 657 exception table |
| `Lib/dis.py`                    | `compile/dis.go`                              | Disassembler used by the v05test gate            |
| (none)                          | `compile/code.go`                             | `Code` value type, mirrors `PyCodeObject`        |
| (generator output)              | `compile/opcodes_gen.go`                      | Opcode constants and metadata (generated)        |

## Bytecode interpreter & frame

| C file                                | Go target                                | Purpose                                  |
|---------------------------------------|------------------------------------------|------------------------------------------|
| `Python/ceval.c`                      | `vm/eval.go`                             | Eval loop entry & unwind                 |
| `Python/ceval_gil.c`                  | `vm/gil.go`                              | GIL acquire/release, eval breaker        |
| `Python/ceval_macros.h`               | `vm/dispatch.go`                         | Dispatch helpers                         |
| `Python/bytecodes.c`                  | (input to generator)                     | Source-of-truth ISA                      |
| `Python/generated_cases.c.h`          | `vm/opcodes_gen.go` (generated)          | Tier-1 dispatch handlers                 |
| `Python/opcode_targets.h`             | `vm/opcode_targets_gen.go` (generated)   | Computed-goto table replaced by switch   |
| `Python/frame.c`                      | `vm/frame.go`                            | `PyFrameObject`                          |
| `Python/stackrefs.c`                  | `vm/stackref.go`                         | Tagged stack references                  |

## Specializer / optimizer / JIT / instrumentation

| C file                          | Go target                                | Purpose                                      |
|---------------------------------|------------------------------------------|----------------------------------------------|
| `Python/specialize.c`           | `specialize/`                            | PEP 659 adaptive specialization              |
| `Python/optimizer.c`            | `optimizer/optimizer.go`                 | Trace projection, executor build             |
| `Python/optimizer_analysis.c`   | `optimizer/analysis.go`                  | Type/global watcher, dataflow                |
| `Python/optimizer_bytecodes.c`  | (input to generator)                     | Tier-2 abstract-interp DSL                   |
| `Python/optimizer_symbols.c`    | `optimizer/symbols.go`                   | Symbol lattice                               |
| `Python/optimizer_cases.c.h`    | `optimizer/cases_gen.go` (generated)     | Abstract interp cases                        |
| `Python/executor_cases.c.h`     | `optimizer/executor_gen.go` (generated)  | Tier-2 interpreter cases                     |
| `Python/jit.c`                  | `jit/stub.go` (deferred)                 | Copy-and-patch JIT, deferred                 |
| `Python/instrumentation.c`      | `monitor/instrumentation.go`             | PEP 669 monitoring                           |
| `Python/legacy_tracing.c`       | `monitor/legacy.go`                      | sys.settrace / sys.setprofile                |
| `Python/intrinsics.c`           | `intrinsics/intrinsics.go`               | INTRINSIC_1 / INTRINSIC_2                    |

## State, lifecycle, init, run

| C file                          | Go target                                | Purpose                                      |
|---------------------------------|------------------------------------------|----------------------------------------------|
| `Python/pystate.c`              | `state/`                                 | Runtime / Interpreter / Thread               |
| `Python/pylifecycle.c`          | `lifecycle/lifecycle.go`                 | Initialize / Finalize phases                 |
| `Python/initconfig.c`           | `initconfig/config.go`                   | `PyConfig`                                   |
| `Python/preconfig.c`            | `initconfig/preconfig.go`                | `PyPreConfig`                                |
| `Python/interpconfig.c`         | `initconfig/interpconfig.go`             | Per-interpreter config                       |
| `Python/pathconfig.c`           | `pathconfig/pathconfig.go`               | sys.path, prefix, exec_prefix                |
| `Python/bootstrap_hash.c`       | `hash/secret.go`                         | PYTHONHASHSEED bootstrap                     |
| `Python/pythonrun.c`            | `pythonrun/`                             | REPL, file/string eval                       |
| `Python/frozen.c`               | `imp/frozen.go`                          | Frozen module table                          |
| `Python/frozenmain.c`           | `cmd/gopy-frozen/`                       | Embedded entry point                         |
| `Python/import.c`               | `imp/import.go`                          | importlib bootstrap, sys.modules             |
| `Python/importdl.c`             | `imp/importdl_stub.go` (deferred)        | Native .so/.pyd loading, deferred            |
| `Python/marshal.c`              | `marshal/marshal.go`                     | .pyc wire format                             |
| `Python/crossinterp.c`          | `crossinterp/`                           | XIData, sub-interpreter handoff              |

## Errors, modules, codecs

| C file                          | Go target                                | Purpose                                      |
|---------------------------------|------------------------------------------|----------------------------------------------|
| `Python/errors.c`               | `errors/errors.go`                       | `PyErr_*` exception protocol                 |
| `Python/traceback.c`            | `traceback/traceback.go`                 | Traceback objects, formatting                |
| `Python/suggestions.c`          | `errors/suggest.go`                      | "Did you mean…?" hints                       |
| `Python/bltinmodule.c`          | `builtin/`                               | `__builtins__`                               |
| `Python/sysmodule.c`            | `sysmod/`                                | `sys`                                        |
| `Python/_warnings.c`            | `warnings/warnings.go`                   | `warnings`                                   |
| `Python/_contextvars.c`         | `contextvar/contextvars_module.go`       | `_contextvars` C module                      |
| `Python/codecs.c`               | `codecs/codecs.go`                       | Codec registry, error handlers               |
| `Python/modsupport.c`           | `modsupport/modsupport.go`               | `Py_BuildValue`, module init helpers         |
| `Python/structmember.c`         | `structmember/structmember.go`           | `tp_members` descriptors                     |
| `Python/getargs.c`              | `getargs/getargs.go`                     | `PyArg_Parse*` parsers                       |

## Memory, GC, concurrency

| C file                          | Go target                                | Purpose                                      |
|---------------------------------|------------------------------------------|----------------------------------------------|
| `Python/gc.c`                   | `gc/collector.go`                        | Generational cycle collector (GIL)           |
| `Python/gc_gil.c`               | `gc/gil.go`                              | GIL-build helpers                            |
| `Python/gc_free_threading.c`    | `gc/freethreading.go`                    | nogil cycle collector                        |
| `Python/brc.c`                  | `gc/brc.go`                              | Biased reference counting                    |
| `Python/qsbr.c`                 | `gc/qsbr.go`                             | Quiescent-state-based reclamation            |
| `Python/uniqueid.c`             | `gc/uniqueid.go`                         | Per-thread refcount index pool               |
| `Python/index_pool.c`           | `gc/indexpool.go`                        | Free index allocator                         |
| `Python/object_stack.c`         | `gc/objstack.go`                         | GC mark stack                                |
| `Python/pyarena.c`              | `arena/arena.go`                         | Bump arena (compiler scratch)                |
| `Python/thread.c`               | `pythread/thread.go`                     | Thread create/join                           |
| `Python/lock.c`                 | `pysync/lock.go`                         | `PyMutex`, `_PyOnceFlag`                     |
| `Python/parking_lot.c`          | `pysync/parkinglot.go`                   | WebKit-style park/unpark                     |
| `Python/critical_section.c`     | `pysync/criticalsection.go`              | Per-object critical sections (nogil)         |

> **Note on `pysync`**: we use the package name `pysync` (not `sync`) to
> avoid shadowing Go's standard library `sync` package inside the gopy
> module, since these CPython primitives have semantics distinct from
> `sync.Mutex` / `sync.Cond`.

## Strings, numbers, hashing, time, hamt, context

| C file                          | Go target                                | Purpose                                      |
|---------------------------------|------------------------------------------|----------------------------------------------|
| `Python/formatter_unicode.c`    | `format/format.go`                       | `__format__` mini-language                   |
| `Python/pystrtod.c`             | `pystrconv/strtod.go`                    | strtod wrapper (calls dtoa)                  |
| `Python/dtoa.c`                 | `pystrconv/dtoa.go`                      | David Gay shortest-roundtrip dtoa            |
| `Python/pystrhex.c`             | `pystrconv/hex.go`                       | bytes-to-hex helpers                         |
| `Python/pystrcmp.c`             | `pystrconv/cmp.go`                       | locale-independent strcmp                    |
| `Python/mystrtoul.c`            | `pystrconv/strtoul.go`                   | int parsing                                  |
| `Python/mysnprintf.c`           | (drop, use `fmt.Sprintf`)                | n/a in Go                                    |
| `Python/pyhash.c`               | `hash/hash.go`                           | SipHash-1-3, FNV, x86_aes                    |
| `Python/pyctype.c`              | `pystrconv/ctype.go`                     | ASCII isalpha/isdigit (locale-independent)   |
| `Python/pymath.c`               | `pymath/pymath.go`                       | math primitives, NaN/Inf                     |
| `Python/pyfpe.c`                | `pymath/fpe.go`                          | float-point exception handling               |
| `Python/hamt.c`                 | `hamt/hamt.go`                           | Hash array mapped trie (contextvars)         |
| `Python/hashtable.c`            | `hashtable/hashtable.go`                 | Internal hash table for caches               |
| `Python/context.c`              | `contextvar/context.go`                  | PEP 567 contextvars                          |
| `Python/pytime.c`               | `pytime/pytime.go`                       | monotonic, perf_counter, FromSeconds         |
| `Python/Python-tokenize.c`      | `tokenize/tokenize.go`                   | tokenizer C-API hooks                        |
| `Grammar/Tokens` plus `Include/internal/pycore_token.h` plus `Lib/token.py` | `tokenize/types_gen.go` (generated by `tools/tokens_go`), `tokenize/types.go` | Token kind constants and `Type.String` |
| `Python/getopt.c`               | `getopt/getopt.go`                       | argv parsing for python.exe                  |
| `Python/tracemalloc.c`          | `tracemalloc/tracemalloc.go`             | allocation tracing                           |
| `Python/remote_debugging.c`     | `remotedebug/remotedebug.go` (deferred)  | remote debug hooks                           |

> **Note on `pystrconv`**: same reasoning as `pysync`. Avoids colliding
> with Go's standard library `strconv`. `pystrconv` holds the
> Python-specific string/number routines (dtoa, locale-independent
> strcmp, mystrtoul). Go's `strconv` is used for plain Go conversions.

## Misc / drop list

| C file                          | Go target / disposition       | Note                                         |
|---------------------------------|-------------------------------|----------------------------------------------|
| `Python/getversion.c`           | `build/version.go`            | Hard-coded version string                    |
| `Python/getplatform.c`          | `build/platform.go`           | `runtime.GOOS`/`runtime.GOARCH` based        |
| `Python/getcompiler.c`          | `build/compiler.go`           | "gopy 0.x using go1.X" string                |
| `Python/getcopyright.c`         | `build/copyright.go`          | static copyright string                      |
| `Python/getopt.c`               | `getopt/`                     | Already listed above                         |
| `Python/dynload_shlib.c`        | `--`                          | Drop. Go does not load `.so` extensions      |
| `Python/dynload_win.c`          | `--`                          | Drop                                         |
| `Python/dynload_hpux.c`         | `--`                          | Drop                                         |
| `Python/dynload_stub.c`         | `--`                          | Drop                                         |
| `Python/dup2.c`                 | `--`                          | Use Go's `os` package                        |
| `Python/dynamic_annotations.c`  | `--`                          | TSAN annotations; drop                       |
| `Python/perf_jit_trampoline.c`  | `--`                          | perf-jit trampoline; drop                    |
| `Python/perf_trampoline.c`      | `--`                          | perf trampoline; drop                        |
| `Python/asm_trampoline.S`       | `--`                          | asm; drop                                    |
| `Python/emscripten_*.c`         | `--`                          | Emscripten platform; drop                    |
| `Python/fileutils.c`            | `fileutils/`                  | Path helpers (only the bits not in `os`/`filepath`) |
| `Python/condvar.h`              | `--`                          | Use `sync.Cond`                              |
| `Python/config_common.h`        | `--`                          | autoconf glue                                |
| `Python/thread_pthread.h`       | `--`                          | Use Go runtime                               |
| `Python/thread_pthread_stubs.h` | `--`                          | Drop                                         |
| `Python/thread_nt.h`            | `--`                          | Use Go runtime                               |
| `Python/crossinterp_*.h`        | `crossinterp/types.go`        | XIData type registry                         |
| `Python/remote_debug.h`         | `remotedebug/`                | header                                       |
| `Python/stdlib_module_names.h`  | `imp/stdlib_names_gen.go`     | Generated list of stdlib module names        |

## Go top-level layout

```
gopy/
├── go.mod                        # module tamnd/gopy
├── cmd/
│   ├── gopy/                     # main interpreter entry (mirror of python.c)
│   └── gopy-frozen/              # embedded-only entry (mirror of frozenmain.c)
├── arena/
├── ast/
├── build/                        # version/platform/compiler/copyright strings
├── builtin/                      # __builtins__ module
├── codecs/
├── compile/                      # codegen, flowgraph, assemble, instrseq
├── contextvar/
├── crossinterp/
├── errors/
├── fileutils/
├── format/
├── future/
├── gc/
├── getargs/
├── getopt/
├── hamt/
├── hash/
├── hashtable/
├── imp/                          # import + frozen + stdlib_names; see 1612
├── initconfig/
├── intrinsics/
├── jit/                          # stub
├── lifecycle/
├── marshal/
├── modsupport/
├── monitor/
├── object/                       # NB: cpython/Objects/* lives in a separate spec series
├── opcode/                       # opcode constants + metadata
├── optimizer/
├── pathconfig/
├── pymath/
├── pystrconv/                    # Python-specific str/number conversion
├── pysync/                       # Python-specific sync primitives
├── pythonrun/
├── pythread/
├── pytime/
├── remotedebug/                  # stub
├── specialize/
├── state/
├── structmember/
├── symtable/
├── sysmod/
├── tokenize/
├── traceback/
├── tracemalloc/
├── vm/
├── warnings/
└── compat/                       # cross-runtime golden tests
    ├── bytecode/
    ├── marshal/
    └── hash/
```

## On flat layout vs `internal/`

Go's `internal/` directory convention restricts imports to packages within
the same module subtree. We deliberately **do not** use it for gopy, for
three reasons:

1. **Embedders**: third-party Go programs that embed gopy as a Python
   runtime (think `python -c` style execution from Go code) need to import
   `vm`, `state`, `lifecycle`, `compile` etc. directly. Burying them under
   `internal/` would block that.
2. **Stdlib re-implementations**: the Go-native ports of CPython's
   `Modules/*` and `Lib/*` live in companion modules (`tamnd/gopy-stdlib`,
   etc.). Those need to import from this module's runtime packages.
3. **Tooling and tests**: `compat/` and external golden-test harnesses
   import the same packages the runtime uses. `internal/` would force
   awkward indirections.

Discoverability is preserved by the package name itself. There is no
ambiguity that `compile`, `vm`, `gc`, `frame` etc. belong to the gopy
runtime.
