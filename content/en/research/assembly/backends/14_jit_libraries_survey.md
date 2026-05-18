---
title: "Hostable JIT/AOT Library Survey for Mochi"
description: "The \"honorable mentions\" beyond LLVM/Cranelift/MIR/QBE."
tags: ["native-codegen", "backends"]
weight: 140
date: 2026-05-18T18:13:12+07:00
---

## §1 Provenance
- **AsmJit**: https://asmjit.com/, https://github.com/asmjit
- **Xbyak**: https://github.com/herumi/xbyak
- **Keystone**: https://www.keystone-engine.org/, https://github.com/keystone-engine/keystone (sibling of Capstone, https://www.capstone-engine.org/)
- **Capstone**: https://www.capstone-engine.org/ (disassembler, not codegen; relevant for round-trip testing)
- **distorm3**: https://github.com/gdabah/distorm
- **Iced (Rust/.NET)**: https://github.com/icedland/iced
- **Zydis**: https://github.com/zyantific/zydis
- **zasm**: https://github.com/zyantific/zasm
- **libgccjit**: covered separately in `05_libgccjit.md`.

## §2 Mechanism + §3 Target coverage + §4 Adoption + §5 Engineering cost (combined per library)

### AsmJit (C++, x86_64 / AArch64)
A lightweight C++ JIT assembler with two layers: a low-level `Assembler` API (you write the opcodes) and a high-level `Compiler` API with optional register allocator. Type-safe at compile time. Targets x86, x86_64, AArch64. Used by Blender's geometry nodes, by various trading-firm internal JITs, by VirtualMachineGarbageCollector experiments. The project banner notes it "cannot be maintained nor developed without funding" (https://asmjit.com/), so its long-term momentum is uncertain. Apache 2.0. For Mochi: requires cgo to a C++ wrapper, similar bridging cost as Cranelift. Useful if we want a register-allocator-on-demand without the full Cranelift/LLVM weight.

### Xbyak (C++, x86 / x86_64)
Herumi Mitsunari's header-only C++ JIT assembler. Supports the full x86_64 instruction set including AVX-512, AVX10.2, APX (added late 2024-2025). Used by Intel oneDNN, by various deep-learning kernel libraries (because Xbyak's AVX coverage is best-in-class). The name comes from Japanese 開闢 ("kaibyaku", "creation"). Recent changes: stricter disp32 checking, far-jump support, exception-less mode, optional `mmap`-based allocator (https://github.com/herumi/xbyak). BSD-3-Clause. For Mochi: x86_64 only is a non-starter on its own; pairs with a separate AArch64 assembler. Cgo bridging required.

### Keystone (C/C++, all architectures from LLVM)
The Capstone authors' assembler counterpart. Takes assembly mnemonics in a string, returns machine bytes. Targets every architecture Capstone disassembles: x86, x86_64, ARM, AArch64, MIPS, PowerPC, SPARC, SystemZ, Hexagon. Stable since 2016; maintenance pace has slowed (last major release 0.9.2 in 2018, with intermittent patches through 2023-2024 per the GitHub repo). Useful as a "drop string assembly in, get bytes out" tool. For Mochi: would let us write each per-architecture lowering as assembly strings instead of golang-asm method calls, but we lose programmatic structure. License: GPL v2 (with the same caveats as libgccjit for Mochi).

### Capstone (C, disassembler)
Bookend to Keystone, by Nguyen Anh Quynh. The reference disassembler used by everything from `gdb` integrations to malware analysis tools. For Mochi: not a codegen library, but indispensable for **round-trip testing**. Any backend Mochi adopts should run Capstone over the emitted bytes in CI to validate that what we wrote disassembles to what we intended. BSD-3-Clause.

### distorm3 (C, disassembler)
Older x86/x86_64 disassembler by Gil Dabah. Largely superseded by Capstone and Zydis in new projects, but still used. For Mochi: alternative to Capstone for round-trip testing on x86 specifically.

### Iced (Rust/.NET, x86 / x86_64)
Wegner Norkow's high-fidelity x86/x86_64 assembler and disassembler, written in both Rust and C#. Cycle-accurate instruction encoding, full AVX-512 / APX coverage, perfect round-trip with binary identity. Used by ILSpy (decompiler), various .NET reverse-engineering tools, and the Rust port (`iced-x86`) is used by some Rust JIT projects. Active maintainership through 2025-2026. Apache 2.0 / MIT dual. For Mochi: the Rust crate is the most polished x86_64 assembler available; cgo bridging required if used from Go.

### Zydis + zasm (C/C++, x86 / x86_64)
Florian Bernd's modern x86 disassembler (Zydis) plus assembler frontend (zasm). Zydis v4 is the current stable line with semantic versioning for the API; v3 receives security updates through 2025 per https://github.com/zyantific/zydis. zasm provides an AsmJit-style interface and idiomatic C++ wrapper. For Mochi: same x86-only ceiling as Xbyak.

### libgccjit
Covered in `05_libgccjit.md`. Linked here for completeness.

## §6 Mochi adaptation note (combined)
None of these libraries is a Phase 1 Mochi backend candidate on its own, because:
- The x86-only ones (Xbyak, Iced, Zydis/zasm) cover only one of Mochi's three priority architectures.
- The cross-architecture ones (AsmJit) only cover x86_64 + AArch64, missing RISC-V.
- Keystone covers everything but is GPL and unmaintained.

**Where these earn their keep**:
- **Capstone** belongs in Mochi's CI as a round-trip validator. We feed the bytes we emit (from golang-asm or copy-and-patch) back through Capstone and assert the disassembly matches the source IR. This catches encoding bugs immediately.
- **AsmJit** is the best candidate if Mochi later wants a higher-tier x86_64+AArch64 JIT than golang-asm provides, without paying Cranelift's adoption cost. Cgo to a small C++ shim.
- **Iced** is the gold standard for x86_64 encoding fidelity; useful as a reference implementation when debugging golang-asm output discrepancies.

Concretely the files affected: a new `runtime/jit/validate/capstone.go` (cgo to libcapstone) that runs in tests; nothing else in Phase 1.

## §7 Open questions for MEP-42
- **Round-trip testing in CI**: should Capstone-based validation be required for every Mochi release on every supported architecture? This catches reloc and encoding bugs before they ship.
- **AsmJit as a Phase 2 step**: if golang-asm proves limiting (no register allocator, no peepholes), AsmJit is the lowest-cost upgrade for x86_64+AArch64 without going all-in on Cranelift or LLVM.
- **Keystone's licensing**: GPL v2 makes Keystone unusable as a linked dependency in Mochi. Could still run as a subprocess.
- **None of these targets Wasm or RISC-V cross-arch well**: confirms that Mochi's "all four MEP-42 architectures" coverage cannot come from this category. It comes from LLVM, Cranelift, QBE, MIR, or C-as-target.
- **Verdict**: useful tooling, not backend candidates. Catalogue them, validate against them in CI, do not build the Phase 1 stack on them.