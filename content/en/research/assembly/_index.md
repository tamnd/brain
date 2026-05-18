---
title: "Native Code Emission"
description: "Research substrate for Mochi MEP-42 (May 2026). A 73-file deep dive into how managed-language runtimes lower typed IR to native machine code: code generation backends, AOT case studies, naive emission techniques, target ISAs and ABIs, object formats, linkers, runtime and libc, debug info, and recent PLDI/POPL papers."
tags: ["native-codegen", "research", "mep-42"]
weight: 2
cascade:
  type: docs
date: 2026-05-18T18:02:28+07:00
---

Background research for [Mochi MEP-42](https://mochi-lang.dev/docs/mep/mep-0042): the native-codegen positioning that pairs a copy-and-patch JIT (Xu+Kjolstad PLDI 2021, validated by CPython 3.13 in October 2024) for `mochi run` hot loops with a C-as-target AOT pipeline (Nim / V / Vala lineage) for `mochi build` distributables.

Each subsection drills into one thread of the 2024-2026 native-codegen landscape. Every file has a §1 Provenance with canonical URLs, a §2 Mechanism, a §3 status as of May 2026, a Mochi adaptation note, and open questions.

## Sections

1. [Backends](backends/) — LLVM 20, Cranelift, QBE, MIR, libgccjit, copy-and-patch, DynASM, golang-asm, MLIR, C-as-target, TCC/chibicc, Wasmtime AOT.
2. [AOT case studies](aot/) — GraalVM Native Image, .NET NativeAOT, Zig, Crystal, Nim, Hare, V, Julia, Mojo, GHC NCG, Embedded Swift, Static Python.
3. [Naive emission](naive/) — Sparkplug, JSC Baseline, copy-and-patch, single-pass classic, Wasm baseline, per-op template JIT, chibicc, QBE for naive.
4. [Targets](targets/) — x86_64, AArch64, RISC-V 64, Wasm 3.0, other ISAs.
5. [Formats](formats/) — ELF, Mach-O, PE/COFF, Wasm module, APE / Cosmopolitan.
6. [Linkers](linkers/) — LLD, mold, Apple ld_prime, GNU ld + gold, no-linker path.
7. [Runtime](runtime/) — musl, glibc, Cosmopolitan libc, Go runtime, freestanding, universal binaries, static-PIE, signing.
8. [Debug](debug/) — DWARF 5, CodeView / PDB, source maps for Wasm.
9. [Papers](papers/) — PLDI 2024-2025, POPL 2024-2025, MLIR dialects, Cranelift design, textbooks, compile-time vs runtime tradeoff.
