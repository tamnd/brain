---
title: "Mochi-to-C Transpiler"
description: "Research substrate for Mochi MEP-45 (May 2026). A 12-file deep dive into ahead-of-time transpilation from Mochi to ISO C23: language surface, design philosophy, prior-art transpilers, runtime building blocks, codegen design, type-system lowering, C-target portability, dataset pipeline, streams and agents, build system, testing gates, and risks."
tags: ["c-target", "research", "mep-45"]
weight: 3
cascade:
  type: docs
date: 2026-05-22T18:00:00+07:00
---

Background research for [Mochi MEP-45](https://mochi-lang.dev/docs/mep/mep-0045): the deep-dive specification for the C-as-target AOT half of [MEP-42](https://mochi-lang.dev/docs/mep/mep-0042). The transpiler takes compiler3 IR, lowers it to ISO C23 plus a thin `libmochi.a` runtime, and ships a statically-linked single-file native binary for every tier-1 triple (x86_64-linux-{gnu,musl}, aarch64-linux-{gnu,musl}, aarch64-darwin, x86_64-darwin, x86_64-windows-msvc, x86_64-windows-gnu, wasm32-wasi). The master correctness gate is byte-equal stdout from the produced binary versus vm3 on the entire fixture corpus.

Each file in this section pins down one piece of the lowering contract. The notes are first-principles design work, not summaries of the current implementation. They were written ahead of code so the spec leads the build.

## Files

1. [Language surface](01-language-surface/) -- every Mochi construct the codegen must lower, walked through one section per topic (value core, function core, collection core, ADT core, query DSL, stream/agent core, logic, AI/FFI, tests, modules, error model, concurrency).
2. [Design philosophy](02-design-philosophy/) -- the five guiding principles (spec-first, boring C, no ABI surprises, portability over performance, verifiable output) plus the runtime shape and a sample C output.
3. [Prior-art transpilers](03-prior-art-transpilers/) -- Nim, Crystal, Vala, OCaml, Roc, Koka, MLton, Cosmopolitan, zig cc, Cython, ATS, MLton, Soufflé, plus 12 distilled lessons and a full sources list.
4. [Runtime building blocks](04-runtime/) -- GC (BDWGC, MMTk, Perceus), allocator (mimalloc, scudo), coroutines (minicoro), I/O (libuv, libxev), strings (utf8proc, simdutf), hash tables (cwisstable), JSON/YAML/CSV, HTTP (libcurl), LLM, FFI.
5. [Codegen design](05-codegen-design/) -- pipeline, name mangling, type lowering table, expression/statement lowering, setjmp/longjmp errors, Maranget pattern matching, modules, debug info.
6. [Type-system lowering](06-type-lowering/) -- monomorphisation, records, sum types with niche optimisation, closures with fat pointer, strings with short-string optimisation, lists, Swiss-table maps, sets, time, errors.
7. [C target portability](07-c-target-portability/) -- C23 features used, compiler matrix (clang, gcc, msvc, zig cc, cosmocc, tcc), tier-1/2/3 targets, ABI per arch, libc matrix, sanitisers, reproducibility, hardening, style guide for emitted C.
8. [Dataset pipeline lowering](08-dataset-pipeline/) -- query DSL lowering with operator fusion, joins (inner, left, cross), group-by, order-by, distinct/union/intersect/except, arena allocation, load/save adapters.
9. [Streams and agents](09-agent-streams/) -- stream/agent/mailbox lowering, M:N work-stealing scheduler over minicoro fibers, channels, shutdown protocol.
10. [Build system](10-build-system/) -- `mochi build` command surface, cache layout (BLAKE3 content-addressed), cross-compile via bundled zig cc, APE via cosmocc, WASM via wasi-sdk, distribution, versioning.
11. [Testing and CI gates](11-testing-gates/) -- differential testing vs vm3, BG corpus, sanitiser matrix (ASan/UBSan/TSan/MSan/LeakSan), property tests, fuzzing, reproducibility check, 16 phased gates.
12. [Risks and alternatives](12-risks-and-alternatives/) -- semantic, build, supply-chain, performance risks; explicit rejection of LLVM IR / WASM / Rust / JIT / C++ / Zig as primary; kill switches; comparable industrial precedent.

## See also

- [Native Code Emission](../assembly/) -- the parent research substrate for MEP-42, of which this is the C-AOT half. Pair with the copy-and-patch JIT notes there for the full picture.
- [Memory Management](../memory-management/) -- the MEP-41 substrate; the GC choice and capability story in note 04 and the hardening defaults in note 07 inherit from this.
