---
title: "gopy overview"
description: "Top-level overview of the gopy project. Ports CPython's Python/ runtime to Go with 100% behavioural compatibility."
tags: ["gopy", "spec"]
weight: 1600
---

# 1600. gopy: Porting CPython's `Python/` to Go

## Goal

`gopy` is a fresh re-implementation of CPython's interpreter core in Go. The
target is **100% behavioural compatibility** with the upstream CPython 3.14-era
sources at `$HOME/github/python/cpython`. That means same data structures,
same models, same code logic, same wire formats, same error messages. The
only change is **naming and surface API style**, which adopts Go-idiomatic
conventions modelled on the Go standard library.

This is *not* a clean-room reimagining. It is a line-by-line port. When
behaviour deviates from CPython, the bug is in the port, not in CPython.

The CPython source-of-truth folder is `cpython/Python/` (about 138k lines of
C across 91 .c files plus ~30 .h files). The Go target is `tamnd/gopy`,
currently at v0.9.0; v0.10 is in flight on `feat/v0.10.0-gc`.

## Non-goals

- No new features. No improved API. No "better" GC.
- No Python 2 support.
- No alternative implementations (we are not PyPy / Cinder / GraalPython).
- No partial Python. The goal is to run unmodified CPython 3.14 stdlib.
- C extension compatibility (PyObject* ABI) is **out of scope**. We will not
  load `.so` modules. C extensions are reimplemented in Go on demand.

## Sources of truth

| Concern                           | Source                                                |
|-----------------------------------|-------------------------------------------------------|
| Runtime semantics                 | `cpython/Python/*.c`, `cpython/Include/internal/*.h`  |
| Object semantics                  | `cpython/Objects/*.c`                                 |
| Parser / lexer                    | `cpython/Parser/*`                                    |
| Stdlib                            | `cpython/Lib/*`                                       |
| Tests                             | `cpython/Lib/test/*`                                  |
| Spec authority for ambiguity      | the C source, *not* the docs                          |

This 1600-series covers `cpython/Python/`, `cpython/Objects/`, and
`cpython/Parser/`. The Objects port lives in the 1670-1689 sub-block
(formerly numbered 1700-series, renumbered to keep one folder).
The Parser port lives in the 1640-1645 sub-block. Stdlib ports
are tracked in their own spec series.

## High-level architecture

```
                ┌────────────────────────────────────────────────┐
                │                  gopy/cmd/gopy                 │
                │            (entry point, like python.c)        │
                └────────────────────┬───────────────────────────┘
                                     │
                ┌────────────────────▼───────────────────────────┐
                │                  gopy/lifecycle                │
                │        Initialize / Finalize / NewInterp       │
                └─┬──────────────┬──────────────┬────────────────┘
                  │              │              │
        ┌─────────▼──┐    ┌──────▼──────┐  ┌────▼────────┐
        │ initconfig │    │   imp       │  │ pythonrun   │
        │  preconfig │    │  importlib  │  │  REPL/eval  │
        │ pathconfig │    │  marshal    │  │   pyc rd/wr │
        └────────────┘    └──────┬──────┘  └────┬────────┘
                                 │              │
                ┌────────────────▼──────────────▼─────────────────┐
                │                  gopy/state                     │
                │  Runtime · Interpreter · Thread · CrossInterp   │
                └─┬──────────────┬─────────────────┬──────────────┘
                  │              │                 │
       ┌──────────▼─┐    ┌───────▼──────┐   ┌──────▼─────────┐
       │   gopy/    │    │    gopy/     │   │     gopy/      │
       │     vm     │    │   compile    │   │      gc        │
       │  (ceval,   │    │  ast/sym/    │   │  cycle coll,   │
       │  frame,    │    │  codegen/    │   │  refcount,     │
       │  uops)     │    │  flowgraph/  │   │  arena, brc,   │
       │            │    │  assemble    │   │  qsbr, weakref │
       └──┬─────────┘    └──┬───────────┘   └────────────────┘
          │                 │
   ┌──────▼────────┐  ┌─────▼──────────┐
   │  gopy/        │  │  gopy/         │
   │  specialize   │  │  tokenize      │
   │  optimizer    │  │  parser  (sep.)│
   │  jit (deferred│  └────────────────┘
   │  monitor      │
   └───────────────┘

Cross-cutting: gopy/pysync, gopy/hash, gopy/pytime,
               gopy/format, gopy/pystrconv, gopy/codecs,
               gopy/errors, gopy/traceback, gopy/warnings,
               gopy/contextvar, gopy/hamt, gopy/hashtable,
               gopy/intrinsics, gopy/structmember, gopy/getargs,
               gopy/modsupport, gopy/builtin, gopy/sysmod,
               gopy/tracemalloc, gopy/audit, gopy/monitor
```

## Spec files in this series

### Implemented (spec written and code shipped)

#### Meta / infrastructure

| #    | File                            | Focus                                         | Shipped |
|------|---------------------------------|-----------------------------------------------|---------|
| 1600 | `1600_gopy_overview.md`         | This file                                     | meta    |
| 1601 | `1601_gopy_naming.md`           | Naming conventions: C to Go translation rules | meta    |
| 1602 | `1602_gopy_filemap.md`          | C source to Go package mapping (every file)   | meta    |
| 1603 | `1603_gopy_roadmap.md`          | Phased milestone plan v0.1 to v1.0            | meta    |
| 1630 | `1630_gopy_vm_overview.md`      | VM block overview (Tier-1 interpreter)        | meta    |
| 1640 | `1640_gopy_parser_overview.md`  | Parser block overview                         | meta    |

#### v0.1 — arena and sync

| #    | File                        | Focus                                         | Shipped |
|------|-----------------------------|-----------------------------------------------|---------|
| 1604 | `1604_gopy_arena.md`        | pyarena.c port                                | v0.1    |
| 1605 | `1605_gopy_pythread.md`     | thread.c cross-platform port                  | v0.1    |
| 1606 | `1606_gopy_pysync.md`       | lock.c, parking_lot.c, critical_section.c     | v0.1    |
| 1607 | `1607_gopy_hashsecret.md`   | bootstrap_hash.c seed init                    | v0.1    |

#### v0.3 — errors and traceback

| #    | File                        | Focus                                         | Shipped |
|------|-----------------------------|-----------------------------------------------|---------|
| 1611 | `1611_gopy_errors.md`       | errors.c plus the BaseException gating subset | v0.3    |

#### v0.4 — strings, numbers, hash

| #    | File                            | Focus                                                        | Shipped |
|------|---------------------------------|--------------------------------------------------------------|---------|
| 1660 | `1660_gopy_strings_numbers.md`  | pyctype, pystrcmp, mystrtoul, pystrtod, dtoa, pystrhex, pymath, pyfpe, formatter_unicode | v0.4 |
| 1661 | `1661_gopy_hash.md`             | pyhash.c (SipHash-1-3, FNV-1a)                               | v0.4    |

#### v0.5 / v0.5.5 — compiler and parser

| #    | File                            | Focus                                                                   | Shipped |
|------|---------------------------------|-------------------------------------------------------------------------|---------|
| 1620 | `1620_gopy_compile_pipeline.md` | ast, asdl, future, symtable, codegen, flowgraph, assemble, compile, instruction_sequence, ast_preprocess, ast_unparse | v0.5 |
| 1625 | `1625_gopy_compile_testing.md`  | Per-checkbox test plan for 1620 and 1665                                | v0.5    |
| 1626 | `1626_gopy_codegen.md`          | codegen.c port detail                                                   | v0.5    |
| 1627 | `1627_gopy_flowgraph.md`        | flowgraph.c port detail (CFG, passes; stackdepth + super-instr deferred)| v0.5    |
| 1628 | `1628_gopy_assemble.md`         | assemble.c port detail                                                  | v0.5    |
| 1629 | `1629_gopy_compile_goldens.md`  | Disassembly golden corpus for v05test                                   | v0.5    |
| 1641 | `1641_gopy_lexer_tokenizer.md`  | Parser/lexer/, Parser/tokenizer/                                        | v0.5.5  |
| 1642 | `1642_gopy_pegen.md`            | pegen.c, parser.c, generated PEG runtime                               | v0.5.5  |
| 1643 | `1643_gopy_parser_errors.md`    | pegen_errors.c, action_helpers.c, peg_api.c, token.c                   | v0.5.5  |
| 1644 | `1644_gopy_string_parser.md`    | string_parser.c (f-string, t-string, bytes)                             | v0.5.5  |

#### v0.6 — VM Tier-1

| #    | File                        | Focus                                                  | Shipped |
|------|-----------------------------|--------------------------------------------------------|---------|
| 1621 | `1621_gopy_bytecodes_dsl.md`| bytecodes.c DSL parser + Go-emitting generator         | v0.6    |
| 1635 | `1635_gopy_intrinsics.md`   | intrinsics.c (CALL_INTRINSIC_1 / 2 dispatch)           | v0.6    |
| 1636 | `1636_gopy_eval_loop.md`    | ceval.c, ceval_macros.h, opcode dispatch loop          | v0.6    |
| 1637 | `1637_gopy_frame.md`        | frame.c, frame layout, locals, generator state         | v0.6    |
| 1638 | `1638_gopy_stackref.md`     | stackrefs.c, tagged stack values                       | v0.6    |
| 1639 | `1639_gopy_eval_gil.md`     | ceval_gil.c, GIL, eval breaker, signal bridge          | v0.6    |

#### v0.7 — lifecycle, sys, builtins, warnings

| #    | File                        | Focus                                                  | Shipped |
|------|-----------------------------|--------------------------------------------------------|---------|
| 1622 | `1622_gopy_lifecycle.md`    | pylifecycle, preconfig, initconfig, pathconfig         | v0.7    |
| 1624 | `1624_gopy_pythonrun.md`    | RunString / RunFile / REPL                             | v0.7    |
| 1651 | `1651_gopy_modules.md`      | builtins, sys, _warnings subsets                       | v0.7    |

#### v0.8 — marshal, import, codecs; Module and set objects

| #    | File                        | Focus                                                                                  | Shipped |
|------|-----------------------------|----------------------------------------------------------------------------------------|---------|
| 1681 | `1681_gopy_set.md`          | setobject.c (set, frozenset)                                                           | v0.8    |
| 1686 | `1686_gopy_exceptions.md`   | exceptions.c — ImportError / ModuleNotFoundError hierarchy                             | v0.8    |
| 1688 | `1688_gopy_module_misc.md`  | moduleobject.c (Module type, __name__ / __doc__ / __file__ / __loader__ / __spec__)    | v0.8    |
| 1690 | `1690_gopy_marshal.md`      | marshal.c — TYPE_LONG, FLAG_REF, TYPE_CODE, TYPE_SET, TYPE_DICT, TYPE_COMPLEX, .pyc header (PEP 552) | v0.8 |
| 1691 | `1691_gopy_import.md`       | import.c, frozen.c — sys.modules cache, inittab, frozen table, ExecCodeModule, source/.pyc loaders, ImportModuleLevel, IMPORT_NAME/FROM | v0.8 |
| 1692 | `1692_gopy_codecs.md`       | codecs.c — registry, error handlers, built-in utf-8 / ascii / latin-1 codecs          | v0.8    |

### Written, partial scaffold (spec written, some code shipped, full panel pending)

| #    | File                            | Focus                                         | Phase      |
|------|---------------------------------|-----------------------------------------------|------------|
| 1665 | `1665_gopy_tokenize.md`         | Python-tokenize.c public iterator surface     | v0.5 / v0.9 |
| 1670 | `1670_gopy_objects_overview.md` | Objects block overview (1670-1689)            | meta       |
| 1671 | `1671_gopy_object_protocol.md`  | Object interface, Header, VarHeader, refcount | v0.2       |
| 1672 | `1672_gopy_type.md`             | Type, slots, MRO, lookup                      | v0.2       |
| 1683 | `1683_gopy_abstract.md`         | abstract.c subset (PyObject_*, PyNumber_*)    | v0.2+      |

### Written, pending implementation

#### v0.9 — contextvars, time, remaining VM bytecodes, runtime helpers (shipped)

Tag `v0.9.0` published 2026-05-06. Tracker rows kept here for the
file-by-file map; full release notes live in `changelog/v0.9.0.md`.

| #    | File                          | Focus                                                       | Status | Phase |
|------|-------------------------------|-------------------------------------------------------------|--------|-------|
| 1634 | `1634_gopy_monitor.md`        | sys.monitoring + sys.settrace / setprofile                  | W      | v0.9+ |
| 1645 | `1645_gopy_myreadline.md`     | myreadline.c, interactive readline editing                  | W      | v0.9+ |
| 1662 | `1662_gopy_hamt.md`           | hamt.c, HAMT backing store for contextvars                  | S      | v0.9  |
| 1663 | `1663_gopy_context.md`        | context.c, _contextvars.c, PEP 567 contextvars              | S      | v0.9  |
| 1664 | `1664_gopy_time.md`           | pytime.c, monotonic clock, conversions, deadline math       | S      | v0.9  |
| 1668 | `1668_gopy_runtime_helpers.md`| getopt.c CLI option parser plus hashtable.c generic table   | S      | v0.9  |
| 1693 | `1693_gopy_vm_remaining.md`   | IMPORT_*, RETURN_GENERATOR / YIELD / SEND, MATCH_*, WITH_EXCEPT_START, BUILD_SET / SET_ADD | S | v0.9 |

#### v0.10 — cycle GC, weakrefs, finalizers (in flight)

Branch `feat/v0.10.0-gc`. Spec status legend: **W** = spec written,
no code. **C** = code shipped, tests pending. **S** = code + tests shipped.

| #    | File                          | Focus                                                       | Status | Phase |
|------|-------------------------------|-------------------------------------------------------------|--------|-------|
| 1613 | `1613_gopy_gc.md`             | gc.c full collector (generations, weakref clearing, finalizer queue) plus gc_gil.c, object_stack.c | W | v0.10 |
| 1666 | `1666_gopy_tracemalloc.md`    | allocation tracing                                          | W      | v0.10 |
| 1689 | `1689_gopy_obj_misc.md`       | weakrefobject.c rows pulled forward to feed cycle clearing  | W      | v0.10 |

#### v0.11+ — specialization, optimizer, debug

| #    | File                          | Focus                                                       | Phase     |
|------|-------------------------------|-------------------------------------------------------------|-----------|
| 1631 | `1631_gopy_specialize.md`     | PEP 659 adaptive specialization                             | v0.11     |
| 1632 | `1632_gopy_optimizer.md`      | Tier-2 trace projector + abstract interp                    | v0.12     |
| 1633 | `1633_gopy_jit.md`            | Copy-and-patch JIT (deferred)                               | post-v1.0 |
| 1667 | `1667_gopy_remote_debug.md`   | remote debugging hooks                                      | v0.13     |

#### Objects block — pending (code lands incrementally v0.2-v0.9)

| #    | File                          | Focus                                                                  | Phase       |
|------|-------------------------------|------------------------------------------------------------------------|-------------|
| 1673 | `1673_gopy_long.md`           | longobject.c (PyLong, small-int cache)                                 | v0.2        |
| 1674 | `1674_gopy_float_complex.md`  | floatobject.c (v0.2), complexobject.c (v0.6)                           | v0.2 / v0.6 |
| 1675 | `1675_gopy_bool_none.md`      | boolobject.c, None, NotImplemented, Ellipsis                           | v0.2        |
| 1676 | `1676_gopy_bytes.md`          | bytesobject.c, bytearrayobject.c, bytes_methods.c                      | v0.4        |
| 1677 | `1677_gopy_unicode.md`        | unicodeobject.c, unicodectype.c                                        | v0.4        |
| 1678 | `1678_gopy_tuple.md`          | tupleobject.c, empty-tuple singleton                                   | v0.2        |
| 1679 | `1679_gopy_list.md`           | listobject.c, list_resize curve, Timsort                               | v0.2        |
| 1680 | `1680_gopy_dict.md`           | dictobject.c, odictobject.c                                            | v0.2        |
| 1682 | `1682_gopy_slice_range.md`    | sliceobject.c, rangeobject.c                                           | v0.2        |
| 1684 | `1684_gopy_call.md`           | call.c, vectorcall                                                     | v0.6        |
| 1685 | `1685_gopy_descr_method.md`   | descrobject.c, methodobject.c, classobject.c, funcobject.c             | v0.4 / v0.6 |
| 1687 | `1687_gopy_code_frame_gen.md` | codeobject.c, frameobject.c, genobject.c, cellobject.c                 | v0.5.5 / v0.6 |
| 1689 | `1689_gopy_obj_misc.md`       | weakref, memoryview, typevar, union, GenericAlias, Interpolation, Template, obmalloc | v0.9+ |

### Reserved (spec not yet written)

| #    | File (planned)              | Focus                                                       | Phase        |
|------|-----------------------------|-------------------------------------------------------------|--------------|
| 1612 | `1612_gopy_traceback.md`    | traceback.c data and formatting                             | v0.3 (retro) |
| 1614 | `1614_gopy_brc.md`          | brc.c biased refcount field layout                          | v0.3+        |
| 1615 | `1615_gopy_state.md`        | pystate.c Runtime / Interpreter / Thread                    | v0.3+        |
| 1698 | `1698_gopy_quirks.md`       | Cross-cutting quirks the porter must preserve               | meta         |
| 1699 | `1699_gopy_glossary.md`     | Glossary: C term to Go term mapping                         | meta         |

## Compatibility floors (what "100% compatible" means in practice)

The port is graded on the following observable surfaces. Each must match
CPython byte-for-byte, except where noted:

1. **Bytecode**: same opcode numbers, same oparg encoding, same EXTENDED_ARG
   widening, same exception table format, same line-number table
   (`co_linetable`) format, same cache layout. `dis.dis(f)` output identical.
2. **Marshal**: `marshal.dumps(obj)` produces identical bytes for the same
   object graph. `.pyc` files produced by gopy are loadable by CPython and
   vice versa, including version-magic-number compatibility.
3. **Hash**: SipHash-1-3 with the same key-derivation from the seed,
   producing identical `hash(x)` for str/bytes/numeric. (PYTHONHASHSEED=0
   gives deterministic match.)
4. **Eval semantics**: every observable behaviour of `eval` + `exec` matches:
   exception types, exception messages (string-equal), traceback frame order,
   `__cause__`/`__context__` chains, generator state, async iteration order.
5. **Built-in module attributes**: `sys.flags`, `sys.implementation.cache_tag`
   (gopy uses its own cache tag, see Quirks), `sys.version_info`, and
   `sys.path` semantics.
6. **Import**: `importlib._bootstrap` runs to completion. `import foo` finds
   modules by the same rules. `__pycache__` layout is identical.
7. **Repr / format**: `repr(obj)` and `format(obj, spec)` produce identical
   strings for builtins. Float repr uses shortest-roundtrip dtoa.
8. **Error messages**: exception constructors produce identical `str(exc)`
   for identical inputs. (This is a high bar but a non-negotiable test
   target.)

Items where we *intentionally* diverge (recorded in `1698_gopy_quirks.md`):

- `sys.implementation.name` is `"gopy"`, not `"cpython"`.
- `sys.implementation.cache_tag` is `"gopy-3140"` so `.pyc` files do not collide.
- `gc.is_finalized` and friends behave per CPython, but the underlying
  mechanism uses Go's GC plus an emulated refcount/cycle layer (see 1613).
- C extension loading (`importlib.machinery.ExtensionFileLoader`) is disabled
  by default; only Go-native extension modules load.

## Test strategy

- The CPython test suite (`Lib/test/`) is the reference oracle.
- Phase 0 ships a "smoke" subset: `test_grammar`, `test_builtin`, `test_dis`,
  `test_marshal`, `test_compile`, `test_dict`, `test_list`, `test_int`,
  `test_str`, `test_exceptions`. Once these pass, broaden.
- Bytecode-level tests: dis(f) round-trip equivalence between `gopy` and
  reference CPython, executed in CI.
- Hash-stability tests with `PYTHONHASHSEED=0`.
- A `compat/` subdirectory at the gopy root holds CPython-cross tests that run
  the same Python source under both runtimes and diff outputs.
