---
title: "DynASM as a Code-Generation Backend for Mochi"
description: "Mike Pall's preprocessor-driven assembler with runtime patching; LuaJIT's secret weapon."
tags: ["native-codegen", "backends"]
weight: 70
date: 2026-05-18T18:07:50+07:00
---

## §1 Provenance
- Project home: https://luajit.org/dynasm.html
- Features: https://luajit.org/dynasm_features.html
- Source in LuaJIT tree: https://github.com/LuaJIT/LuaJIT/tree/v2.1/dynasm
- ARM64 module: https://github.com/LuaJIT/LuaJIT/blob/v2.1/dynasm/dasm_arm64.lua
- Unofficial docs: https://corsix.github.io/dynasm-doc/
- MoarVM fork: https://github.com/MoarVM/dynasm
- Author: Mike Pall (LuaJIT). Copyright 2005-2025 Mike Pall, MIT-licensed.
- Originally developed for LuaJIT 1, retained as a build-time tool for LuaJIT 2's hand-written interpreter.

## §2 Mechanism
DynASM is a two-stage system:
1. **Preprocess time**: a Lua script (`dynasm.lua`) reads a C source file with embedded `|`-prefixed assembly lines. The script substitutes the assembly with C calls into a small runtime encoder, producing a normal `.c` file.
2. **Runtime**: the encoder (`dasm_x86.h`, `dasm_arm64.h`, etc.) emits machine bytes into a buffer. The assembly may contain "holes" (`->label`, `=>dynlabel`, literal placeholders) that get filled in via runtime API calls.

The model is fundamentally "assembler embedded in C": you write actual assembly, with full mnemonic richness, in your C function. Macros and DSL features handle register parameterization. This is closer to writing assembler than to writing an IR.

There is no instruction selection, no register allocator, no optimization pass. The programmer makes every codegen decision. The runtime cost is essentially `memcpy` plus a handful of patch operations.

## §3 Target coverage (May 2026)
Per https://luajit.org/dynasm_features.html and the LuaJIT v2.1 tree:
- x86 and x86_64: production-quality, the original target.
- ARM (32-bit): production-quality.
- ARM64 (AArch64): production-quality, the module stabilized in 2021 (`Mike Pall, 2005-2025`).
- PowerPC (32 and 64): production-quality.
- MIPS (32 and 64, big and little endian): production-quality.
- No RISC-V module in the upstream LuaJIT tree as of May 2026. Several third-party RV64 forks exist but none has been merged.
- No Wasm.

Object formats: DynASM does not produce object files. Output is in-memory bytes; the embedding application handles linking, executable-memory mapping, and ABI.

## §4 Production / language adoption status (May 2026)
- **LuaJIT 2.x** (https://luajit.org): the interpreter loop is one giant DynASM-authored assembly file. The trace JIT does **not** use DynASM at runtime; it has its own backend.
- **MoarVM** (the Raku/Perl 6 VM): used DynASM for its JIT. The fork at https://github.com/MoarVM/dynasm has not been resynced with upstream since around 2014 (per copyright headers), indicating limited recent activity.
- **OpenResty**: ships LuaJIT, so depends on DynASM transitively.
- **Various academic projects**: DynASM is a popular pedagogical choice for "writing a JIT in a weekend" tutorials.

Maintenance: DynASM upstream tracks LuaJIT, which Mike Pall maintains solo. LuaJIT's commit cadence slowed in the late 2010s but resumed. The ARM64 module has been stable since 2021 with only minor updates.

License: MIT.

## §5 Engineering cost for Mochi
- **Binary footprint**: the encoder headers compile to a few KB of C per architecture. Total runtime weight is negligible.
- **Build complexity**: Mochi would need a Lua interpreter at build time (Lua 5.1 / LuaJIT) to run `dynasm.lua` over assembly templates. The output is normal C, then compiled with the host C compiler. For a Go-hosted Mochi this means we are introducing both Lua and cgo as build prerequisites, plus per-architecture assembly source files that we author by hand.
- **License**: MIT.
- **Cross-compilation**: Each target needs its own assembly source file. There is no shared IR. Add a target = add a new `.c` file with new mnemonics.
- **Debugging**: We control the assembly, so we control the line tables. DWARF is on us to emit.
- **Runtime startup**: Zero. Function compile is microseconds.

## §6 Mochi adaptation note
DynASM is **not a backend in the LLVM/QBE/Cranelift sense**; it is an assembler. Adopting it for Mochi would mean hand-writing the lowering for each vm3 op for each target architecture, exactly the model Mochi's existing `runtime/jit/vm2jit/lower_amd64.go` already follows (with golang-asm). The win over golang-asm would be **assembly syntax that looks like real assembly** rather than Go method calls, plus richer macro/template support.

Practical fit: Mochi cannot natively use DynASM because it requires Lua at build time and a C compilation toolchain. The closest pure-Go analogue is `runtime/jit/tmpljit/` (template JIT) which already exists in the tree.

If we wanted DynASM specifically, the integration would replace `runtime/jit/vm2jit/lower_amd64.go` and `lower_arm64.go` with `.dasc` (DynASM) files compiled to C and linked into a `runtime/jit/vm2jit-native/` cgo package.

## §7 Open questions for MEP-42
- **Is the "embedded assembler" model preferable to golang-asm?** Probably yes for readability, but not enough to justify a Lua build dependency.
- **No RISC-V**: third-party patches exist but nothing official. Mochi would need to either contribute a port or use another backend on RISC-V.
- **Cgo and Lua at build time**: a serious dependency expansion. Mochi today builds with `go build`. After DynASM it would need `make + lua + clang + go`.
- **Solo maintainer (Mike Pall)**: same bus-factor concern as QBE.
- **Verdict**: DynASM is technically excellent but architecturally a step backward for Mochi compared to QBE or copy-and-patch. Useful as a reference for "how to write a clean embedded assembler" rather than as a real Phase 1 candidate.