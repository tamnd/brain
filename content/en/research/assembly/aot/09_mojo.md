---
title: "Mojo"
description: "Python-syntax systems language built on MLIR, with both AOT and JIT pipelines, on the path to 1.0 in H1 2026."
tags: ["native-codegen", "aot"]
weight: 90
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- Project home: https://www.modular.com/mojo and https://mojolang.org/
- Source (now public): https://github.com/modular/modular (the Mojo language tree)
- Documentation: https://docs.modular.com/mojo/
- FAQ: https://docs.modular.com/mojo/faq/
- 1.0 beta announcement: https://forum.modular.com/t/modular-26-3-mojo-1-0-beta-mojolang-org-max-video-gen-and-more/3038
- "Path to Mojo 1.0" blog post (5 Dec 2025): https://www.modular.com/blog/the-path-to-mojo-1-0
- MLIR foundation paper: Lattner et al., "MLIR: Scaling Compiler Infrastructure for Domain Specific Computation" (CGO 2021).
- Authors: Chris Lattner (LLVM/Swift/MLIR creator), Tim Davis, and the Modular Inc. team. Founded 2022.

## §2 Architecture

Mojo's compiler pipeline is an MLIR pipeline, not a traditional Python-to-native pipeline:

1. Parser produces an AST.
2. The compiler lowers to a stack of MLIR dialects: a high-level Mojo dialect (parameters, traits, lifetimes), a parameter-domain dialect (Mojo's compile-time parameters and template instantiation engine), and progressively lower dialects.
3. Pre-elaboration and post-elaboration optimisation passes run; templates are specialised between them.
4. The MLIR pipeline lowers to LLVM IR for CPU targets, or to the GPU dialects (NVPTX, AMDGPU, custom accelerators) for GPU/TPU targets. Mojo can produce both `.o` (CPU object) and `.ptx` (GPU kernel) from the same source.
5. LLVM optimises and emits machine code. The optimisation and code generation stages run in parallel (llvm-opt/llc) to reduce build time.

`mojo build` performs ahead-of-time compilation to save an executable. `mojo run` JIT-compiles. Mojo packages (`.mojopkg`) use format version 2 in 1.0.0b1, with zstd-compressed MLIR bytecode for smaller distribution.

The MLIR choice is the architectural keystone. Unlike Julia, Crystal, Swift, or Rust (all of which sit directly on top of LLVM IR), Mojo can express higher-level abstractions in dedicated dialects, then lower them to LLVM only for the final step. This is exactly the case MLIR was invented for. It also gives Mojo the route to non-LLVM hardware backends (TPUs, custom ASICs) without retrofitting LLVM.

## §3 Targets and platforms (May 2026)

Tier-1 CPU: linux-x86_64, linux-aarch64, macos-arm64. GPU: NVIDIA (CUDA via PTX), AMD (ROCm), with documented Compilation Targets page covering inspection of the host and cross-compilation for accelerators.

Windows is not yet a first-class CPU target as of 1.0 beta; the focus is on Modular's MAX platform (server-side AI inference) where Linux dominates. macOS-x86_64 has limited support.

Cross-compilation for accelerators is the headline feature: from one Mojo source, the compiler can produce a fat artefact targeting both CPU and one or more GPU architectures. CPU-to-CPU cross-compilation (e.g., from a Linux build host to a different Linux ISA) is supported but less polished than Zig's offering.

Linking is dynamic against libc by default. Static linking is gated on MAX-platform integration questions.

## §4 Runtime

Mojo bundles:

- Its own allocator and reference-capability system (lifetimes, ownership, borrowing similar to Rust). There is no garbage collector in Mojo; memory management is via ownership and explicit reference types.
- The MAX runtime when used in the AI-inference context (linked separately).
- A small Python-interop runtime: Mojo embeds CPython for `python.import` interop, calling into Python via the standard CPython C API.
- FFI: direct C call via `external_call` and the MLIR `llvm` dialect; structured C bindings via `@register_passable`.

Hello-world AOT binary on linux-aarch64 in 1.0 beta: roughly 1–3 MB stripped (no Python runtime); larger if Python interop is linked.

## §5 Status (May 2026)

Mojo 1.0.0b1 (the first 1.0 beta) shipped recently before May 2026; final 1.0 is targeted for H1 2026 per the 5 Dec 2025 announcement. The prior stable release was Mojo 25.4 (19 Jun 2025) under the old version scheme.

The Mojo compiler is closed-source as of May 2026 with an open-source standard library, but Modular committed to open-sourcing the compiler in "fall 2026" alongside or after 1.0 GA.

Production users: Modular's MAX inference platform is the flagship deployment. Several AI infra companies (Lambda, Together, others) have public Mojo benchmarks. HPC scientific computing has early adopters (see the Sep 2025 paper "Mojo: MLIR-Based Performance-Portable HPC Science Kernels on GPUs for the Python Ecosystem", arxiv 2509.21039).

Performance: comparable to optimised C/CUDA for the AI kernels Mojo was designed around; orders of magnitude faster than CPython for the same source. Vs Julia or Swift for general CPU code, Mojo is competitive but not consistently better.

Known limitations: async story still WIP (excluded from 1.0); private members not in 1.0; Mojo is not Python-source-compatible (Python interop is via embedding CPython, not by running Python source through the Mojo compiler); ecosystem outside AI/HPC is thin; compiler is still closed-source.

## §6 Mochi adaptation note

Mojo is the most relevant case study for Mochi because of shared Python heritage in surface syntax and shared aspiration to "look high-level, run as native code". Specific patterns worth examining:

- MLIR as a layered IR. Mochi's `compiler3` IR could be refactored as an MLIR-style dialect stack: a high-level Mochi dialect (for sets, datasets, queries), a mid dialect (closures lowered, generics specialised), and a low dialect handed to a CPU/wasm backend. This is more engineering than rolling a single typed SSA IR, but it pays off if Mochi ever targets GPUs or accelerators.
- Two compilation modes from the same compiler: `mojo run` (JIT) and `mojo build` (AOT). Mochi can offer the same UX without bundling a JIT, by making `mochi run` a fast AOT-then-execute path on top of `mochi build`.
- Compile-time parameters as a first-class IR layer. Mojo's "parameter domain IR" is a clean way to handle generic monomorphisation explicitly. Mochi's generics (if and when they exist) could be specialised at the IR layer rather than at parse time.
- Closed-source compiler is a cautionary tale. Even with a strong team and large funding, the closed-source compiler hurt Mojo's early ecosystem growth. Mochi being open from MEP-0 is a strategic advantage.
- Embedding CPython for interop is a precedent for how Mochi could embed the Go runtime if FFI requirements demand it. The performance trade-offs (an FFI boundary per call) are well-documented.

Affected Mochi files: long-term, `compiler3/ir/` could grow MLIR-style dialects; near-term, the AOT-then-execute UX for `mochi run` is achievable on top of any backend choice.

## §7 Open questions for MEP-42

1. Is MLIR a reasonable dependency for Mochi, or too heavy? MLIR drags LLVM in.
2. Do we want a single compiler binary for both AOT and JIT, or two modes from a unified frontend?
3. Generic monomorphisation: explicit IR pass (Mojo's parameter domain) or implicit at type-check?
4. Mojo's lifetime/reference-capability system is a third memory model option beyond GC and arenas; does MEP-42 stake out a position?
5. Cross-compilation to accelerators (GPU, NPU) is not a Mochi v1 goal, but the MLIR architecture makes it possible later; should MEP-42 keep that door open?