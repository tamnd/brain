---
title: "MLIR as a Code-Generation Backend for Mochi"
description: "Multi-Level IR, dialect framework, the foundation under Mojo, IREE, and OpenXLA."
tags: ["native-codegen", "backends"]
weight: 90
date: 2026-05-18T18:11:03+07:00
---

## §1 Provenance
- Project home: https://mlir.llvm.org/
- Source: https://github.com/llvm/llvm-project/tree/main/mlir
- Users page: https://mlir.llvm.org/users/
- Original paper: Chris Lattner et al., "MLIR: Scaling Compiler Infrastructure for Domain Specific Computation," CGO 2021.
- Mojo MLIR docs: https://docs.modular.com/mojo/notebooks/BoolMLIR/
- Mojo vision: https://docs.modular.com/mojo/vision/
- Awesome-MLIR/Mojo list: https://github.com/coderonion/awesome-mojo-max-mlir
- Mojo source-language Wikipedia: https://en.wikipedia.org/wiki/Mojo_(programming_language)
- Mojo HPC paper (SC25 workshops): https://arxiv.org/pdf/2509.21039

## §2 Mechanism
MLIR is an IR framework rather than a single IR. It provides:
- A common SSA infrastructure (Operations, Regions, Blocks, Values, Types, Attributes).
- A **dialect** mechanism: each dialect defines its own ops, types, and attributes; many dialects can coexist in a single module.
- Standard dialects: `func`, `arith`, `scf` (structured control flow), `cf`, `memref`, `tensor`, `vector`, `affine`, `linalg`, `gpu`, `llvm` (the LLVM IR dialect), and many more.
- Pattern-based rewriting and progressive lowering: a frontend emits ops in a high-level dialect, then conversion passes lower them step-by-step through standard dialects, ultimately to the `llvm` dialect, which translates to LLVM IR for backend code generation.

The "code generation" itself still goes through LLVM (or, for accelerators, SPIR-V or PTX). MLIR's value is in the high-level optimization passes (loop fusion, tiling, vectorization at the affine level) before LLVM ever sees the code.

For Mochi's purposes, MLIR is best understood as **LLVM plus extra layers**. Build complexity, binary size, and target coverage are all LLVM's, plus more.

## §3 Target coverage (May 2026)
MLIR itself targets:
- All LLVM targets via the `llvm` dialect (x86_64, AArch64, RISC-V, Wasm, PowerPC, etc.).
- GPU dialects lower to NVPTX, AMDGPU, and SPIR-V.
- Wasm dialect: proposed, in flight as of CGO 2025 (per https://mlir.llvm.org/users/).
- Custom hardware: TPU, Apple Neural Engine, AWS Trainium/Inferentia, custom NPUs via dialect-specific backends.

Object formats: inherit from LLVM (ELF, Mach-O, COFF, Wasm).

What is stable as of LLVM 20: the core infrastructure, the standard dialects, the LLVM lowering. What is in flux: GPU async dialects, transform dialect (introduced CGO 2025), Wasm dialect, the Clang CIR integration (a new C/C++ frontend that lowers via MLIR).

## §4 Production / language adoption status (May 2026)
- **Mojo** (Modular): the highest-profile MLIR consumer. Mojo is described as "syntactic sugar for MLIR." Mojo's compiler is closed-source through May 2026; Modular has committed to open-sourcing it in fall 2026. Mojo standard library is open.
- **Modular MAX**: production AI graph compiler that hosts Mojo kernels.
- **IREE** (https://iree.dev): runtime for ML models, lowers through MLIR.
- **OpenXLA**: TensorFlow/JAX/PyTorch shared compiler stack, MLIR-based, backed by NVIDIA, AMD, Intel, Apple, AWS.
- **CIRCT**: hardware description toolchain (Verilog generation).
- **Clang CIR**: an experimental Clang IR dialect, lowering C/C++ via MLIR.
- **Flang**: the Fortran frontend uses MLIR (FIR dialect → HLFIR → LLVM IR).
- **Polygeist**: C-to-MLIR (research).
- **Polymage / Tiramisu** descendants for polyhedral compilation.

Maintainership is healthy with significant Google and Modular backing. Release cadence matches LLVM's six-month train.

License: Apache 2.0 with LLVM Exceptions.

## §5 Engineering cost for Mochi
- **Binary footprint**: MLIR adds tens of MB on top of LLVM. A typical "MLIR + LLVM" binary is 150-300 MB.
- **Build complexity**: same as LLVM, plus another sub-project (`-DLLVM_ENABLE_PROJECTS=mlir`). No Go binding. Integration via cgo to a C++ wrapper, or via emitting MLIR text and shelling out to `mlir-opt | mlir-translate | llc`.
- **License**: Apache 2.0 with LLVM Exceptions.
- **Cross-compilation**: same as LLVM (single build targets all triples).
- **Debugging**: full DWARF via LLVM; MLIR also has location attributes that flow through lowering.
- **Runtime startup**: hundreds of ms to construct the MLIR context, similar to LLVM.

For a small imperative language like Mochi, MLIR is **massive overkill**. MLIR's value emerges when you have many lowering levels (e.g., tensor programs → linalg → affine → scf → llvm). Mochi's compiler3 IR is already low-level; lowering it through MLIR adds layers without unlocking new optimizations.

## §6 Mochi adaptation note
Mochi's compiler3 IR (`/Users/apple/github/mochilang/mochi/compiler3/ir`) would skip most of MLIR's standard dialects and lower almost directly into the `llvm` dialect. At that point we have all the cost of MLIR with none of the benefit; we might as well emit LLVM IR text directly (see `01_llvm.md`).

The only Mochi scenarios where MLIR earns its weight:
1. Mochi grows a tensor/array dialect for ML workloads. Mochi's current `runtime/vector` and `runtime/llm` modules hint at this direction.
2. Mochi wants to target GPUs or custom accelerators.
3. Mochi adopts polyhedral or vectorization passes that need `affine` and `linalg`.

None of these is a Phase 1 concern.

## §7 Open questions for MEP-42
- **Verdict for Phase 1**: skip. MLIR's cost is justified only if Mochi targets heterogeneous compute.
- **Long-term hedge**: if Mochi grows tensor support, MLIR becomes the obvious choice for that subsystem; the rest of the language can keep emitting plain LLVM IR.
- **Closed-source Mojo precedent**: Modular has shown that you can build a serious systems language as an MLIR frontend. The downside is two-axis evolution: Mochi would track both LLVM and MLIR release trains.
- **Dialect maintenance**: a Mochi dialect would need a TableGen description and ongoing conformance with MLIR core. Not free.
- **Wasm dialect timing**: if the Wasm dialect lands stable in LLVM 22 or 23, MLIR becomes a single answer for "all of Mochi's targets" (LLVM CPU triples + Wasm). Watch this.