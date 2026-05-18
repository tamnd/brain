---
title: "MEP-42 Backend Survey: Summary and Recommendation"
description: "Comparison table and Phase 1 / Phase 2 recommendation for Mochi's native code-generation backend."
tags: ["native-codegen", "backends"]
weight: 0
date: 2026-05-18T18:13:12+07:00
---

## §1 What is in this directory
This directory contains a per-backend evaluation for MEP-42:

- `01_llvm.md` LLVM 20.x
- `02_cranelift.md` Cranelift (Wasmtime)
- `03_qbe.md` QBE
- `04_mir.md` MIR (Vladimir Makarov)
- `05_libgccjit.md` libgccjit
- `06_copy_and_patch.md` copy-and-patch (CPython JIT)
- `07_dynasm.md` DynASM (LuaJIT)
- `08_golang_asm.md` golang-asm (already used by Mochi vm2jit)
- `09_mlir.md` MLIR
- `10_c_as_backend.md` C as a backend (Nim, V style)
- `11_tcc_chibicc.md` TCC, chibicc, Cuik (reference points)
- `12_wasmtime_aot.md` Wasmtime AOT
- `13_emitting_object_files.md` Direct object file emission
- `14_jit_libraries_survey.md` AsmJit, Xbyak, Keystone, Iced, etc.

## §2 Comparison table

| Backend | Compile speed | Code quality (vs C -O2) | x86_64 | AArch64 | RISC-V64 | Wasm | Host lang | License | Binary footprint | Cost from Go (cgo?) |
|---|---|---|---|---|---|---|---|---|---|---|
| **LLVM 20** | slow | 100% | yes | yes | yes | yes | C++ | Apache 2.0 + LLVM Exc. | 60-300 MB | cgo via tinygo go-llvm, or shell out to llc |
| **Cranelift** | fast | 60-70% | yes | yes | yes | (via Wasmtime) | Rust | Apache 2.0 + LLVM Exc. | 15-25 MB | cgo to Rust staticlib, or subprocess |
| **QBE** | very fast | 70% | yes | yes | yes | no | C | MIT | 500 KB | subprocess (text IR) |
| **MIR** | very fast | 50-60% | yes | yes | yes | no | C | MIT | 500 KB-1 MB | cgo |
| **libgccjit** | slow | 100%+ | yes | yes | yes | no | C | **GPL v3 + RLE** | 80-150 MB | cgo, **GPL contagion risk** |
| **copy-and-patch** | instant | 70-80% (no cross-op opt) | yes | yes | yes (via clang) | no | technique | unencumbered | KB-MB of stencils | clang at build time, none at runtime |
| **DynASM** | instant | 90%+ (you control everything) | yes | yes | community | no | Lua+C | MIT | KB | Lua at build time, cgo |
| **golang-asm** | instant | 50% (no regalloc) | yes | yes | yes (untested) | no | Go | BSD-3-Clause | 5-10 MB | **none (pure Go)** |
| **MLIR** | slow | 100% | yes | yes | yes | yes | C++ | Apache 2.0 + LLVM Exc. | 150-300 MB | cgo or shell out, big ramp |
| **C as target** | medium-slow | 100% | yes | yes | yes | yes (Emscripten) | technique | unencumbered | 0 (user's cc) | none |
| **TCC** | instant | 30% (no opts) | yes | yes | partial | no | C | LGPL | 500 KB | cgo to libtcc |
| **Wasmtime AOT** | fast | 70% (via Cranelift) | yes | yes | yes | yes | Rust | Apache 2.0 + LLVM Exc. | 70-100 MB | subprocess `wasmtime compile` |
| **Object file emit (own)** | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | pure Go writers, ~3-5k LOC |
| **AsmJit / Xbyak / Iced** | instant | varies | yes | yes (AsmJit) | no | no | C++/Rust | various | small | cgo |

Notes:
- "Code quality vs C -O2" is informal; numbers are author claims plus community benchmarks.
- Wasm column "yes (via X)" means the backend covers Wasm only by chaining through another tool.
- "RISC-V64" means RV64GC unless noted.

## §3 What MEP-42 actually needs
The four MEP-42 priority targets are x86_64, AArch64, RISC-V RV64GC, and Wasm. No single backend covers all four with stable production support and a Go-friendly integration story:
- LLVM and MLIR cover all four but are huge and need cgo (or shell out).
- Cranelift covers x86_64 + AArch64 + RISC-V; Wasm is "use Wasmtime."
- QBE and MIR cover the three CPUs; Wasm is gone.
- C-as-target covers everything (any C compiler the user has, plus Emscripten/wasi-sdk for Wasm) with zero new Mochi dependencies.
- Wasmtime AOT covers everything **by making Wasm the universal IR**: Mochi emits Wasm once, `wasmtime compile` lowers to native.

## §4 Recommendation

**Phase 1 (MEP-42 1.0, target Q3 2026): adopt two complementary backends.**

- **Primary AOT backend: C-as-target (per `10_c_as_backend.md`).** Mochi's compiler3 lowers IR to C, shells out to the user's `cc` (preferring `zig cc` for hassle-free cross-compilation). This is the only backend that requires zero new dependencies of Mochi itself, covers all four MEP-42 priority targets plus every embedded toolchain on Earth, and produces code as good as the user's C compiler. It also reuses Mochi's existing `runtime/tcc/` scaffolding for a fast dev-tier compile (libtcc for `mochi run`, GCC/Clang for `mochi build`).
- **Primary JIT backend: keep golang-asm (per `08_golang_asm.md`).** Mochi's existing `runtime/jit/vm2jit` already uses twitchyliquid64/golang-asm to JIT on x86_64 and arm64. It is pure Go, ships in `go build`, and is good enough for an interpreter-tier JIT. Extend it to RISC-V (the relocations exist; the lowering does not). For Wasm JIT, defer (browsers and Wasmtime handle that).

This pair gives Mochi: zero new external runtime deps, native binaries on every MEP-42 target, a working JIT on the same targets, and a clean upgrade path.

**Phase 2 (MEP-42 2.0, target 2027): add Wasmtime AOT plus a higher-quality native AOT.**

- **Wasm path: `compiler3/emit/wasm` (per `12_wasmtime_aot.md`).** A native Wasm emitter unlocks browsers, edge runtimes, and Wasmtime AOT for native binaries. This is the highest-leverage single feature beyond Phase 1.
- **Higher-quality native AOT: QBE (per `03_qbe.md`).** When users need better-than-C-quality binaries (small startup, no libc dependency, tighter code), shelling out to QBE gives us a 500 KB toolchain that covers x86_64+arm64+riscv64. QBE pairs with Mochi's "small and pleasant to hack on" aesthetic better than LLVM/MLIR.

**Phase 3 (deferred): LLVM as a heavyweight option.** If Mochi ever needs vectorization, profile-guided optimization, or LTO-quality output, layer in LLVM via `compiler3/emit/llvmir` emitting `.ll` text and shelling to `llc`. This avoids cgo on every Mochi build host while keeping the LLVM option available for users who install it.

**Explicitly rejected for Phase 1**:
- libgccjit (GPL contagion).
- MLIR (massive overkill until Mochi grows tensor/GPU support).
- Cranelift in-process (cgo to Rust is too much friction; reach Cranelift transitively via Wasmtime AOT instead).
- DynASM (Lua build dependency, no RISC-V).
- TCC/chibicc/Cuik as the main native backend (too immature or too narrow).

## §5 One-line takeaway
**Phase 1 = C-as-target for AOT + golang-asm for JIT. Phase 2 = add Wasm emit and QBE.** This sequence preserves Mochi's "pure Go, no native deps at build time" identity, gives users native binaries on every MEP-42 priority platform via standard system toolchains, and leaves a clean upgrade path to higher-quality backends when needed.