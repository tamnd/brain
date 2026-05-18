---
title: "LLVM as a Code-Generation Backend for Mochi"
description: "The workhorse SSA infrastructure, version 20 era, evaluated for MEP-42."
tags: ["native-codegen", "backends"]
weight: 10
date: 2026-05-18T18:04:37+07:00
---

## §1 Provenance
- Project home: https://llvm.org/
- Source: https://github.com/llvm/llvm-project
- Release notes (current trunk): https://llvm.org/docs/ReleaseNotes.html
- LLVM 20.1.0 tagged March 10, 2025 (Fedora tracking: https://fedoraproject.org/wiki/Changes/LLVM-20)
- LLVM 20.X milestone tracker: https://github.com/llvm/llvm-project/milestone/26
- Original paper: Chris Lattner and Vikram Adve, "LLVM: A Compilation Framework for Lifelong Program Analysis and Transformation," CGO 2004.
- Go bindings (community): https://github.com/tinygo-org/go-llvm
- Pure-Go IR builder (no cgo): https://github.com/llir/llvm

## §2 Mechanism
LLVM consumes a typed, SSA, three-address intermediate representation (LLVM IR) and lowers it to machine code through a long pipeline: IR-level transforms (mem2reg, inlining, GVN, LICM, loop vectorization), a target-independent SelectionDAG or GlobalISel instruction selector, the register allocator (greedy with PBQP fallback), prologue/epilogue insertion, and target-specific assembly emission. Output can be assembly text, an object file (via the integrated assembler), or in-memory machine code via OrcJIT/MCJIT.

IR is dual-encoded: human-readable `.ll` text and compact `.bc` bitcode. Both round-trip losslessly. A typical embedded use case writes `.bc`, hands it to `opt -O2` plus `llc`, and links with the system linker (`ld`, `lld`, `link.exe`). For JIT, OrcJIT v2 is the supported in-process compiler.

MLIR (covered separately in `09_mlir.md`) sits above LLVM IR and can lower to it; LLVM IR remains the lingua franca for object emission.

## §3 Target coverage (May 2026)
LLVM 20 has stable, production backends for:
- x86_64 SysV (Linux, macOS, FreeBSD, the BSDs) and x86_64 Win64.
- AArch64 on macOS (Apple Silicon), Linux, Windows on ARM.
- RISC-V RV32I/RV64GC including vector extensions, stable for years.
- WebAssembly (wasm32 and wasm64) with full SIMD and reference-types support.
- Arm32, PowerPC LE, MIPS (in maintenance), SystemZ, SPARC, Hexagon, AMDGPU, NVPTX, BPF.

Object formats: ELF, Mach-O, COFF/PE, XCOFF, Wasm. DWARF 5 is the default debug format on non-Windows targets; CodeView on Windows.

Experimental in 20.x: LoongArch is now stable, M68k remains experimental, the Xtensa backend is in mainline. AVX10 support was rewritten after Intel's mid-2025 spec change (https://www.phoronix.com/linux/LLVM).

## §4 Production / language adoption status (May 2026)
LLVM IR is the de facto target for new statically typed languages: Rust (primary backend), Swift, Julia, Crystal, Nim (optional alongside its C backend), Pony, Odin, Mojo (via MLIR, then LLVM), and Zig (for release builds, while Debug now defaults to Zig's self-hosted x86_64 backend, https://ziglang.org/devlog/2025/). It also remains the assembler driver for clang, flang, and most production C/C++ toolchains.

LLVM cuts a major release every six months. Active maintainership is healthy with hundreds of corporate and academic contributors (Apple, Google, Intel, AMD, ARM, Sony, AdaCore, Nvidia, Modular).

Performance: LLVM at `-O2`/`-O3` is the reference point that every other backend gets compared to. Tradeoff is well known: very long compile times and a multi-hundred-MB toolchain.

## §5 Engineering cost for Mochi
- **Binary footprint**: A static `libLLVM-20.a` is roughly 1.2 GB unstripped; the shared `.so/.dylib` ships at 100-200 MB depending on enabled targets. A minimal AArch64+x86_64+RISC-V build can be trimmed to 60-80 MB. Cranelift, MIR, and QBE are 10x to 100x smaller.
- **Build complexity**: For a Go-hosted compiler, the two realistic integration paths are:
  1. **cgo with go-llvm** (https://pkg.go.dev/tinygo.org/x/go-llvm): use TinyGo's actively maintained C-API binding. Build tags select LLVM 14 through 20. Requires libLLVM installed on the build machine and cross-compilation toolchains for each target. Single-maintainer concern per https://discourse.llvm.org/t/go-llvm-bindings-choice-for-language-development/84592.
  2. **Pure-Go llir/llvm** (https://github.com/llir/llvm) emits LLVM IR text only; you then shell out to `llc` or `opt`. No cgo, no native build. The cost is an external `llc` dependency at runtime, which is the same shape as the Zig 0.16 plan ("emit bitcode, let user run llc separately," https://github.com/ziglang/zig/issues/16270).
- **License**: Apache 2.0 with LLVM Exceptions, compatible with Mochi's permissive license.
- **Cross-compilation**: First-class. A single LLVM build can target every supported triple; no per-host toolchain.
- **Debugging**: Full DWARF 5 and CodeView, source-level debugging in gdb/lldb/WinDbg.
- **Runtime startup cost**: AOT path has zero runtime cost. JIT path pays multi-millisecond startup per OrcJIT engine plus ~50-500ms per function compiled at `-O0`, seconds at `-O2`.

## §6 Mochi adaptation note
The vm3 register file (three banks of typed registers) and the typed arena allocator in `/Users/apple/github/mochilang/mochi/runtime/vm3/arenas.go` map cleanly to LLVM IR: each typed register becomes an SSA value, each arena Cell becomes an `i64`/`{i8*, i64}` aggregate, and the existing op dispatch in `/Users/apple/github/mochilang/mochi/runtime/vm3/op.go` becomes a per-op IR template. The compiler3 IR under `/Users/apple/github/mochilang/mochi/compiler3/ir` is already SSA-flavored, so the lowering pass would live next to `/Users/apple/github/mochilang/mochi/compiler3/emit`. For Phase 1 the simplest route is to emit textual `.ll` from a new `compiler3/emit/llvmir` package and shell out to the system `llc`; this avoids cgo and matches the Zig direction of travel.

## §7 Open questions for MEP-42
- **Cgo or not?** Adopting `go-llvm` introduces a C toolchain dependency on every Mochi build host, which conflicts with Mochi's current "pure Go, no native deps" stance (`/Users/apple/github/mochilang/mochi` has no cgo today outside `runtime/tcc/Makefile`). Emitting `.ll` text and shelling out to `llc` keeps Mochi portable but ties release binaries to an installed LLVM.
- **Which LLVM version to pin?** Pin to LLVM 20 LTS for Phase 1; track LLVM 21/22 once the AVX10.2 churn settles.
- **JIT or AOT first?** AOT via `llc` is the obvious Phase 1; OrcJIT in-process needs cgo and balloons the runtime to hundreds of MB, conflicting with the vm3 minimalist design.
- **Where does this leave vm3?** Even with LLVM AOT, the vm3 interpreter stays as the development/REPL backend, mirroring Julia (interpreter for fast iteration, LLVM JIT for hot code).
- **MLIR or straight LLVM IR?** MLIR adds another major dependency and another learning curve; for a simple imperative language like Mochi the direct IR route is enough until GPU or accelerator targets become a goal.