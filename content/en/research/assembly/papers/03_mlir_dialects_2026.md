---
title: "MLIR Dialect Literature 2023-2026"
description: "The Triton dialect (OpenAI, GPU codegen), the IREE dialect (Google, ML compiler), Mojo's MLIR-based KGEN compiler, and the broader trend of language frontends as MLIR dialects. The \"if we wanted to be ambitious\" backend story for Mochi."
tags: ["native-codegen", "papers"]
weight: 30
date: 2026-05-18T18:11:03+07:00
---

## §1 Provenance

- MLIR project: https://mlir.llvm.org/. Originally Chris Lattner at Google (2018), released as part of LLVM in 2019.
- Wikipedia MLIR page: https://en.wikipedia.org/wiki/MLIR_(software).
- Triton (OpenAI): https://github.com/openai/triton. Recent paper "ML-Triton: A Multi-Level Compilation and Language Extension to GPU Programming" (2025), arXiv: https://arxiv.org/pdf/2503.14985.
- IREE (Google): https://iree.dev/, https://github.com/iree-org/iree.
- Mojo (Modular): https://docs.modular.com/mojo/. Vision page: https://docs.modular.com/mojo/vision/. KGEN compiler discussed at https://forum.modular.com/t/mlir-dialect-import-for-mojo/774.
- Awesome list: https://github.com/coderonion/awesome-mojo-max-mlir.
- Ramalho et al., "Mitigating the MLIR Learning Curve" (2024 conference paper, exact venue under our verification).

## §2 Technique / contribution

MLIR is a multi-level intermediate representation framework. Where LLVM IR is a single fixed IR, MLIR is a meta-IR with *dialects*: user-defined sets of operations, types, and attributes. A program traverses several dialects on its way to machine code, each lowering pass converting one dialect's ops into another's.

### Triton dialect (OpenAI, 2021+)
- Triton is a Python-embedded DSL for writing custom GPU kernels.
- Triton-MLIR is the MLIR-based reimplementation of Triton's compiler (Microsoft contributed substantially to this).
- Introduces dialects representing Triton's blocks, warps, and memory spaces. Lowers via the `gpu`, `nvvm`, and `llvm` standard MLIR dialects.
- Now used by vLLM, Mamba, DeepSpeed, and many other ML frameworks.

### IREE dialect (Google, 2020+)
- Maps ML graphs (TFLite, PyTorch ONNX) onto MLIR's `linalg`, `affine`, `scf`, `vector` dialects.
- Performs aggressive fusion, tiling, vectorization before lowering to LLVM IR or SPIR-V.
- IREE adds its own `flow`, `stream`, `hal` dialects for inter-device scheduling.

### Mojo / KGEN (Modular, 2023+)
- Mojo is a systems-programming language with Python syntax. The compiler (KGEN, "kernel generator") is built atop MLIR Core.
- Mojo deliberately does *not* use the `linalg`/`affine`/`scf` ML dialects. It uses MLIR Core only.
- Mojo code can directly express MLIR dialect operations as inline syntax: it is described as "syntactic sugar for MLIR."
- Supports out-of-tree custom dialects, making Mojo a candidate as a general-purpose MLIR frontend.

### Quake (NVIDIA CUDA Quantum), CIRCT (hardware design), Polygeist (C-to-MLIR)
- Quake: MLIR dialect for quantum-circuit compilation.
- CIRCT: MLIR for digital-hardware design (Chisel moved its backend here in 2023).
- Polygeist: lifts C/C++ into the `affine` dialect for polyhedral analysis.

## §3 Where it shines, where it fails

**Shines:**
- Modular: a small custom dialect plus standard lowerings yields LLVM-quality codegen.
- Multi-target: same dialect lowers to CPU, GPU, TPU, FPGA via different lowering paths.
- Active community, well-staffed (LLVM Foundation, Google, NVIDIA, Apple, Modular all contribute).
- The dialect pattern lets a language frontend stay small while inheriting world-class optimization.

**Fails:**
- Steep learning curve. Ramalho et al. (2024) note: building a new dialect or pass means delving into C++ templates and TableGen.
- Build complexity: full MLIR build is ~1 GB of LLVM dependencies.
- Pure-Go integration is essentially impossible. MLIR is C++ to its core.
- Stability: the `linalg`/`tensor` dialects in particular churn fast.
- Heavyweight: not "naive" at all. This is the polar opposite of MEP-42's stated phase-1 goal.

## §4 Status (May 2026)

- MLIR is the foundation for essentially every new ML compiler.
- Triton-MLIR is the production Triton compiler since 2023.
- IREE has shipping mobile and edge deployments.
- Mojo reached 1.0 stable in 2025; KGEN is in active development with new dialect work each quarter.
- MLIR governance was formalized in late 2024 with an area-team structure to manage the "dialect zoo."
- The ML-Triton 2025 paper (arXiv 2503.14985) proposes a multi-level extension to Triton, suggesting the dialect approach is still evolving.

## §5 Engineering cost for Mochi

This is the **expensive** end of the spectrum.

A Mochi-as-MLIR-dialect implementation would require:

- 3 months: define `mochi` dialect (operations, types, attributes). Use TableGen for declarative ops.
- 6 months: write lowering passes: `mochi -> arith + memref + scf -> llvm`.
- 3 months: build-system integration (Mochi compiler shells out to `mlir-opt` and `mlir-translate`).
- 6 months: stable for production.

Total: ~18 months. Plus the build dependency on LLVM/MLIR (~1 GB of C++ source).

Versus copy-and-patch at ~8 weeks for a working JIT, MLIR is 9-10x more expensive.

**When MLIR makes sense for Mochi**: only if Mochi grows GPU/TPU/accelerator support. For CPU-only naive native, MLIR is overkill.

## §6 Mochi adaptation note

- `compiler3/ir/` could be lifted into an MLIR `mochi` dialect.
- `runtime/vm3/arenas.go` would expose runtime hooks that the lowered LLVM IR calls.
- `runtime/vm3/cell.go` would map to an MLIR custom type `!mochi.cell`.
- The build would shift from pure-Go to Go+C++ (via cgo or shell-out to LLVM tools).

This conflicts with the project preference to stay pure-Go-no-cgo. **Recommendation: defer MLIR to MEP-50+ when accelerator support becomes a priority.**

## §7 Open questions for MEP-42

- Is GPU/TPU support a phase-1 goal? If no, skip MLIR.
- If yes, do we adopt Triton's dialect or define our own?
- Can we shell out to `mlir-opt` from a Go binary without cgo? (Yes, via subprocess, but the dependency is heavy.)
- What is our story for Mojo interop? If Mojo becomes the lingua franca of MLIR frontends, Mochi could expose a Mojo binding.

## §8 References

- MLIR project page: https://mlir.llvm.org/.
- MLIR users list: https://mlir.llvm.org/users/.
- ML-Triton paper (2025): https://arxiv.org/pdf/2503.14985.
- Mojo vision: https://docs.modular.com/mojo/vision/.
- IREE project: https://iree.dev/.
- Triton on GitHub: https://github.com/openai/triton.
- "Deep Engineering #9: Unpacking MLIR and Mojo with Ivo Balbaert": https://deepengineering.substack.com/p/deep-engineering-9-unpacking-mlir.
- Awesome Mojo / MAX / MLIR: https://github.com/coderonion/awesome-mojo-max-mlir.