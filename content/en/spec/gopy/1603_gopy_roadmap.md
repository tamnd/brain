---
title: "gopy roadmap"
description: "Phased milestone plan from v0.0.1 (parser smoke) to v1.0 (full CPython parity). Defines the ordering of subsystem ports and the gating criteria for each release."
tags: ["gopy", "spec"]
weight: 1603
---

# 1603. Phased roadmap

The port advances along a critical path: **runtime state, then object
model, then compiler, then VM, then import, then runtime polish**. Each
phase has a boot test and a release tag. Anything past v0.5 can interleave;
the order before v0.5 is load-bearing.

Each phase lists:
- **In scope**: which `cpython/Python/*` files are ported in this phase.
- **Out of scope**: explicitly deferred to a later phase.
- **Gate**: the executable test that must pass before the next phase starts.

## v0.0. Project scaffolding

**Goal**: An empty Go module that builds. No Python yet.

**In scope**:
- `cmd/gopy/main.go`. Prints version, exits 0.
- `build/{version,platform,compiler,copyright}.go`. Static strings (the
  four trivial getX.c files).
- `go.mod`, `go.sum`, basic CI (build + `go vet`).

**Gate**: `go build ./... && go test ./... && gopy --version` prints
`gopy 0.0.0 (3.14.0+) [go1.22 darwin/arm64]` or similar.

## v0.1. Memory, arena, primitive sync

**Goal**: The compiler-side allocator and basic synchronization primitives
that everything else needs.

**In scope** (`Python/` files):
- `pyarena.c` to `arena/arena.go`.
- `lock.c`, `parking_lot.c`, `critical_section.c` to `pysync/`.
- `thread.c` to `pythread/thread.go`. Just thread create/join wrappers on
  top of Go's runtime.
- `bootstrap_hash.c` to `hash/secret.go`. Just the seed init; hash funcs
  come in v0.4.

**Out of scope**: GC, brc, qsbr (these need PyObject).

**Gate**: arena alloc/free unit tests pass, mutex stress test passes.

## v0.2. Object model foundation (handover from `cpython/Objects/`)

**Note**: The 1600-series spec covers only `cpython/Python/`. This v0.2
phase is the integration boundary with the `Objects/` port (a separate
spec series). We list the dependency for completeness.

**Required from object spec**:
- `Object` interface, `Type`, `Header`, `VarHeader`.
- Concrete types: `int`, `float`, `bool`, `None`, `bytes`, `str`, `list`,
  `tuple`, `dict`, `set`, `frozenset`, `slice`, `range`.
- Tuple/list/dict basic ops, hashing of int/str/tuple/frozenset.
- `Type.Slot(...)` dispatch and the tp_* protocol.

**Gate**: Construct a dict, hash a tuple, iterate a list, all from a
test-only `gopy/objtest/` package, since we have no parser yet.

## v0.3. Errors, traceback, refcount-only GC

**Goal**: We can raise and catch exceptions in Go-only fixtures.

**In scope**:
- `errors.c` to `errors/`.
- `traceback.c` to `traceback/`.
- `suggestions.c` to `errors/suggest.go`.
- `gc.c` (refcount path only; no cycle collector yet) to `gc/`.
- `brc.c` partial: just the field layout, ops are no-ops in the GIL build.
- `pystate.c` skeleton (Runtime, Interpreter, Thread structs; no init
  flow).

**Out of scope**: Cycle collector, free-threading, qsbr, finalize-on-resurrect.

**Gate**: `errors.SetString(state.PyExc_ValueError, "boom")` then
`errors.Occurred(ts) != nil`, and `traceback.Format(ts.Exception())`
produces a non-empty string.

## v0.4. Strings, hashing, ctype, int/float parsing

**Goal**: Number/string conversion and hashing, the bedrock of dict and
the parser.

**In scope**:
- `pyhash.c` to `hash/{fnv,siphash,hash}.go`.
- `pyctype.c` to `pystrconv/ctype.go`.
- `pystrcmp.c` to `pystrconv/cmp.go`.
- `mystrtoul.c` to `pystrconv/strtoul.go`.
- `pystrtod.c` plus `dtoa.c` to `pystrconv/{strtod,dtoa}.go`.
  - **Decision point**: cgo-wrap David Gay's dtoa, or pure-Go reimplement?
    See 1660 §"dtoa decision". Recommend pure-Go using the reference
    algorithm to keep the project cgo-free.
- `pystrhex.c` to `pystrconv/hex.go`.
- `mysnprintf.c`: drop, use `fmt`.
- `pymath.c`, `pyfpe.c` to `pymath/{pymath,fpe}.go`.
- `formatter_unicode.c` to `format/format.go`.

**Gate**: `hash.Buffer([]byte("hello"))` matches CPython's
`hash(b"hello")` under `PYTHONHASHSEED=0`. `pystrconv.ParseFloat("3.14")`
returns the same `uint64` bit pattern as CPython.

## v0.5. Compiler pipeline (parser-side handover)

**Note**: The Python parser (PEG) port lives in the 1640-1645 sub-block
and lands in v0.5.5 (next phase). v0.5 itself exercises the
ast-to-Code path on hand-built modules; once v0.5.5 lands the
disassembly goldens get re-pinned against parsed source.

**In scope** (the rest of the compiler is in this spec):
- `asdl.c` plus `Python-ast.c` to `ast/{asdl,nodes_gen}.go`.
- `ast.c` to `ast/validate.go`.
- `ast_preprocess.c` to `ast/preprocess.go`.
- `ast_unparse.c` to `ast/unparse.go`.
- `future.c` to `future/future.go`.
- `symtable.c` to `symtable/`.
- `instruction_sequence.c` to `compile/instrseq.go`.
- `codegen.c` to `compile/codegen.go`.
- `flowgraph.c` to `compile/flowgraph.go`.
- `assemble.c` to `compile/assemble.go`.
- `compile.c` to `compile/compiler.go`.

**Gate (structural)**: `compile.Compile(module("a = 1 + 2"))` produces
a `*Code` whose disassembly contains LOAD_CONST and STORE_NAME and
whose const pool holds the folded `int(3)` after the int-int BINARY_OP
pass runs.

**Gate (disassembly parity)**: the `v05test` package pins compile
output via two layers. Structural assertions live in
`gate_test.go` (`TestGateEmptyModule`, `TestGateSimpleAssign`,
`TestGateBinaryAdd`, `TestGateLoadAfterStore`, `TestGateIfWhile`,
`TestGateDef`, `TestGateAsyncFunction`). Disassembly-text goldens
live in `golden_test.go` against `testdata/golden/*.golden` for the
ten-fixture panel in spec 1629 (`empty_module`, `simple_assign`,
`binary_add`, `load_after_store`, `if_pass`, `while_pass`,
`def_add_one`, `async_def_pass`, `class_pass`, `type_alias`).
Two structural cases (`TestGateTryExcept`, `TestGateComprehension`)
are wired but `t.Skip`'d pending the CFG-based stack-depth analyser
(handler entry seeding / comprehension back-edge); they flip green
once that lands.

**Gate (full byte-equal marshal parity)**: deferred to v0.8 alongside
the import system. v0.5 has the marshal package skeleton plus a
roundtrip test, but the code-object marshal arm (TYPE_LONG,
ref-dedup, line/exception-table byte parity) lands with import.

**Optimisation panel status**: int-int `BINARY_OP` constant folding,
jump threading, conditional-jump propagation, unreachable-block
elimination, post-terminator dead-code elimination, and
redundant-NOP compaction landed for v0.5 alongside the CFG-driven
pass driver. Swaptimize, super-instructions, LOAD_FAST ref-stack,
cold-block hoist, CFG-based stackdepth, and full pseudo-op lowering
are deferred and tracked separately.

**Other v0.5 landings**: full `ast.Validate` panel
(forbidden-name, comprehension shape, expr_context, Starred placement,
match-pattern shape, PEP 695 type-param constraints), TypeAlias
codegen via INTRINSIC_TYPEALIAS, PEP 626 line-table writer, PEP 657
exception-table writer, `co_qualname` walk, type-keyed const dedup.

## v0.5.5. Parser handover

**Goal**: Real source text reaches `compile.Compile`. The disassembly
goldens shipped in v0.5 against hand-built AST modules get re-pinned
against parsed source.

**In scope** (`Parser/` files; spec block 1640-1645):
- `Parser/lexer/{lexer,state,buffer}.c` to `parser/lexer/`. Spec 1641.
- `Parser/tokenizer/{utf8,string,file,readline}_tokenizer.c` plus
  `helpers.c` to `parser/lexer/driver_*.go`. Spec 1641.
- `Parser/pegen.c`, `Parser/pegen_errors.c`, `Parser/peg_api.c`,
  `Parser/action_helpers.c`, `Parser/token.c` to `parser/pegen/`
  and `parser/errors/`. Specs 1642 and 1643.
- `Parser/parser.c` regenerated from `Grammar/python.gram` via a
  Go-target fork of `Tools/peg_generator/`. Lives at
  `tools/parser_gen/`. Output checked in to
  `parser/pegen/parser_gen.go`. Spec 1642.
- `Parser/string_parser.c` to `parser/string/`. Spec 1644.

**Out of scope**: `Parser/myreadline.c` (interactive readline; lands
in v0.9 alongside the REPL). Soft keyword work beyond what 3.14
already needs.

**Gate**: `partest/gate_test.go` parses each v0.5 golden fixture
from source and round-trips through `compile.Compile`, producing
disassembly text that matches the v0.5 golden file byte-for-byte.
The `partest/errors_panel_test.go` corpus pins SyntaxError text
byte-for-byte to CPython.

## v0.6. Bytecode interpreter (Tier-1 only)

**Goal**: Execute the compiled bytecode. No specialization, no Tier-2.

**In scope**:
- `bytecodes.c` (DSL) plus Go-emitting code generator to `vm/opcodes_gen.go`.
- `ceval.c` to `vm/eval.go`.
- `ceval_macros.h` to `vm/dispatch.go`.
- `ceval_gil.c` to `vm/gil.go`.
- `frame.c` to `vm/frame.go`.
- `stackrefs.c` to `vm/stackref.go`.

**Out of scope**: `specialize.c`, `optimizer.c`, `jit.c`,
`instrumentation.c`. Stub out the entry hooks (e.g.
`_Py_call_instrumentation` becomes a no-op).

**Gate**: `gopy -c "print(1+2)"` prints `3`. The `dis` builtin shows
unspecialized bytecode. All exception types raise correctly through the
frame chain.

## v0.7. Init/Finalize and minimum sys/builtins

**Goal**: Real Py_Initialize / Py_Finalize lifecycle. `gopy -c` works
without manual setup boilerplate.

**In scope**:
- `pystate.c` complete to `state/`.
- `pylifecycle.c` to `lifecycle/`.
- `preconfig.c`, `initconfig.c`, `interpconfig.c` to `initconfig/`.
- `pathconfig.c` to `pathconfig/`.
- `pythonrun.c` to `pythonrun/`.
- `bltinmodule.c` minimal subset (print, len, range, iter, abs, type,
  isinstance, repr, str, int, float, list, tuple, dict, set, getattr,
  setattr, hasattr, callable, id, hash, sorted, reversed, enumerate, zip,
  map, filter, sum, min, max, any, all, divmod, pow, chr, ord, bin, oct,
  hex, ascii, format, vars, dir) to `builtin/`.
- `sysmodule.c` minimal subset (path, modules, argv, version,
  version_info, flags, implementation, stdin/stdout/stderr placeholders,
  exit, getrefcount, setrecursionlimit, getrecursionlimit) to `sysmod/`.
- `_warnings.c` to `warnings/`.
- `getargs.c` to `getargs/`.
- `modsupport.c` to `modsupport/`.
- `structmember.c` to `structmember/`.

**Gate**: `gopy -c "import sys; print(sys.version_info)"` works
end-to-end through full Initialize, Run, Finalize.

## v0.8. Import, marshal, codecs

**Goal**: `import foo` from a `.py` file, with `__pycache__` round-trip.

**In scope**:
- `marshal.c` to `marshal/`.
- `import.c` to `imp/import.go`.
- `frozen.c` (table only; frozen importlib bootstrap is a separate task)
  to `imp/frozen.go`.
- `codecs.c` to `codecs/`.
- The frozen importlib._bootstrap blob, regenerated with our
  `freeze_modules` Go tool that mirrors CPython's. Produces an equivalent
  .h-equivalent .go file.

**Out of scope**: `importdl.c` (native .so loading). gopy does not load C
extensions.

**Gate**: `import json; json.dumps({"a": 1})` works. The .pyc generated
by gopy can be loaded by CPython 3.14.

## v0.9. Contextvars, hamt, time, tokenize (shipped 2026-05-06)

**Goal**: Stdlib `time`, `contextvars`, `tokenize` modules work.

**Shipped**:
- `hamt.c` to `hamt/`.
- `context.c` plus `_contextvars.c` to `contextvar/`.
- `pytime.c` to `pytime/` (`Time_`, `Monotonic`, `PerfCounter`, rounding modes,
  per-platform info files).
- `Python-tokenize.c` to `tokenize/` (real lexer state machine).
- `getopt.c` to `getopt/` (`cmd/gopy` parses through this now).
- `hashtable.c` to `hashtable/`.
- vm tail: generators on goroutines, `MATCH_*`, `WITH_EXCEPT_START`, set
  builders, `IMPORT_STAR`, async-stub opcodes.

**Deferred to v0.10+**: frozen importlib code-object embedding,
sub-interpreter contention path, `__match_args__` MRO walk, full async
iterator surface.

**Gate**: `python -m asyncio` smoke test runs (asyncio uses contextvars).

## v0.10. Cycle GC, weakrefs, finalizers (in flight)

**Goal**: Reference cycles are reclaimed. `gc.collect()` works.

**In scope**:
- `gc.c` complete to `gc/collector.go` (generations, `gc_collect_main`,
  reachability walk, weakref clearing pass).
- `gc_gil.c` to `gc/gil.go` (collector-vs-mutator interlock).
- `object_stack.c` to `gc/objstack.go`.
- `weakrefobject.c` to `objects/weakref.go` (PyWeakref, callback queue,
  `_PyWeakref_ClearWeakRefsExceptCallbacks`).
- Finalizer (tp_finalize) queue and resurrection check.
- `gc` built-in module: `collect`, `enable`, `disable`, `get_threshold`,
  `set_threshold`, `get_count`, `get_objects`, `is_tracked`.
- Replace the current `gc.Collect()` no-op stub at `gc/gc.go:113`.

**Spec**: `1613_gopy_gc.md` (writing in this branch).

**Gate**: `test_gc` from CPython passes; cycle of two objects with
mutual references is reclaimed; finalizer fires once and only once.

## v0.11. Specialize, monitor

**Goal**: Adaptive specialization (PEP 659) and monitoring (PEP 669).

**In scope**:
- `specialize.c` to `specialize/`.
- `instrumentation.c` to `monitor/instrumentation.go`.
- `legacy_tracing.c` to `monitor/legacy.go`.

**Gate**: `dis.dis` shows specialized variants on hot loops.
`sys.settrace(f)` fires on every line.

## v0.12. Tier-2 optimizer (interpreter-only, no JIT)

**Goal**: Trace projection, abstract interp, and Tier-2 micro-op
interpreter.

**In scope**:
- `optimizer.c`, `optimizer_analysis.c`, `optimizer_symbols.c` to
  `optimizer/`.
- `optimizer_bytecodes.c` (DSL) plus Go-emitting generator to
  `optimizer/cases_gen.go` and `optimizer/executor_gen.go`.

**Out of scope**: `jit.c`. JIT remains a stub that returns "no executor".

**Gate**: A long-running tight loop measurably faster than v0.11. We
don't need to match CPython speed yet.

## v0.13. Sub-interpreters and cross-interpreter data

**In scope**:
- `crossinterp.c` to `crossinterp/`.
- `interpconfig.c` polishing (per-interp PyConfig).

**Gate**: `interpreters` PEP 734 module (in stdlib) basic usage works.

## v0.14. Free-threaded build

**Goal**: An optional `-tags pygil_disabled` build path. Not the default.

**In scope**:
- `gc_free_threading.c` to `gc/freethreading.go`.
- `brc.c` complete (real biased refcount) to `gc/brc.go`.
- `qsbr.c` to `gc/qsbr.go`.
- `uniqueid.c`, `index_pool.c` to `gc/{uniqueid,indexpool}.go`.
- Free-threaded variants of object slots (mostly in `Objects/` spec).

**Gate**: Same test suite as v0.13 passes under `-tags pygil_disabled`.

## v0.15. Tracemalloc, audit, faulthandler, perf

**In scope**:
- `tracemalloc.c` to `tracemalloc/`.
- audit hooks (`pycore_audit.h`) to `audit/`.
- faulthandler module.
- `remote_debugging.c` (best-effort) to `remotedebug/`.

**Gate**: `tracemalloc.start()` then `tracemalloc.get_traced_memory()`
returns sane values.

## v1.0. CPython test-suite parity

**Goal**: A defined subset (about 80%) of `cpython/Lib/test/` passes.

This phase is iterative bug-fixing. No new files; just polish plus test
investment.

**Gate**: `python -m test --pgo` analogue. A curated subset of CPython
tests all pass on gopy.

## Out-of-roadmap (post-v1.0, not in this spec series)

- **JIT (jit.c)**: Copy-and-patch JIT requires LLVM stencil generation.
  Defer indefinitely. gopy will use Go's compiler-level optimizations
  plus the Tier-2 trace interpreter for now.
- **C extension loading (importdl.c, dynload_*.c)**: Out of scope. The
  Go port reimplements common C extensions in Go on demand.
- **Emscripten / wasm support**: drop unless explicitly funded.
- **perf trampoline**: drop.

## Summary table

| Tag    | Theme                                | Critical files                                    |
|--------|--------------------------------------|---------------------------------------------------|
| v0.0   | Scaffold                             | get*.c                                            |
| v0.1   | Arena, sync                          | pyarena, lock, parking_lot, critical_section, thread |
| v0.2   | Object model (handover)              | (cpython/Objects/)                                |
| v0.3   | Errors, refcount GC                  | errors, traceback, suggestions, gc (rc-only)      |
| v0.4   | Strings, numbers, hash               | pyhash, pyctype, pystr*, mystr*, dtoa, formatter  |
| v0.5   | Compiler pipeline                    | ast, asdl, future, symtable, codegen, flowgraph, assemble, compile, instruction_sequence |
| v0.6   | VM Tier-1                            | ceval, ceval_gil, ceval_macros, bytecodes, frame, stackrefs |
| v0.7   | Init, lifecycle, sys, builtins       | pystate, pylifecycle, *config, pathconfig, pythonrun, bltinmodule, sysmodule, _warnings, getargs, modsupport, structmember |
| v0.8   | Import, marshal, codecs              | import, marshal, frozen, codecs                   |
| v0.9   | Contextvars, time, tokenize          | hamt, context, _contextvars, pytime, Python-tokenize, getopt, hashtable, intrinsics |
| v0.10  | Cycle GC                             | gc (cycle path), gc_gil, object_stack             |
| v0.11  | Specialize, monitor                  | specialize, instrumentation, legacy_tracing       |
| v0.12  | Tier-2 optimizer                     | optimizer*, executor_cases.c.h                    |
| v0.13  | Sub-interpreters                     | crossinterp, interpconfig                         |
| v0.14  | Free-threaded build                  | gc_free_threading, brc (full), qsbr, uniqueid, index_pool |
| v0.15  | Profiling, debugging                 | tracemalloc, audit, faulthandler, remote_debugging |
| v1.0   | CPython test parity                  | (no new files)                                    |
