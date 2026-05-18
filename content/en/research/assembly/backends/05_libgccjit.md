---
title: "libgccjit as a Code-Generation Backend for Mochi"
description: "GCC as a shared library, used by Emacs native compilation, GCC Rust, GDC, Cython."
tags: ["native-codegen", "backends"]
weight: 50
date: 2026-05-18T18:07:50+07:00
---

## §1 Provenance
- Documentation: https://gcc.gnu.org/onlinedocs/jit/
- Source: in the GCC tree, https://gcc.gnu.org/git/?p=gcc.git;a=tree;f=gcc/jit
- Author: David Malcolm (Red Hat), with steady contributions from a Red Hat compiler team.
- Initial paper: David Malcolm, "libgccjit: An embeddable code-generation library backed by GCC," GCC Cauldron 2014 (slides at https://gcc.gnu.org/wiki/cauldron2014).
- Emacs native compilation tracking: https://www.gnu.org/software/emacs/manual/html_node/elisp/Native_002dCompilation-Functions.html
- Andrea Corallo's gccemacs writeup: https://akrl.sdf.org/gccemacs.html

## §2 Mechanism
libgccjit exposes a C API (with C++ and Python bindings) that lets callers build a GCC GIMPLE-shaped IR programmatically: types, functions, blocks, RVALUEs, LVALUEs, calls, returns. Once the API graph is built, a single `gcc_jit_context_compile` (or `gcc_jit_context_compile_to_file`) call drives the full GCC backend: GIMPLE → RTL → register allocator → instruction selection → ELF emission. The "JIT" name is misleading; it works equally well as an AOT compiler-as-a-library.

Output options:
- In-memory machine code, callable as `void*` function pointers (JIT mode).
- Object file (`.o`).
- Executable.
- Static or dynamic library.
- Assembly text.

Optimization levels match GCC: `-O0` through `-O3`, `-Ofast`, `-Os`. At `-O3` libgccjit-generated code is identical in quality to `gcc -O3` on the same input, because it is the same backend.

## §3 Target coverage (May 2026)
libgccjit inherits every GCC backend that ships with GCC 15:
- x86_64 SysV+Win64, i386, x32.
- AArch64 Linux, AArch64 Darwin (Apple Silicon, finally usable in GCC 14+), AArch64 Windows is partial.
- RISC-V RV64GC and RV32 with vector extensions.
- ARM32, PowerPC (LE and BE), s390x, SPARC, MIPS, m68k, SH, IA-64, RX, RL78, AVR, MSP430, Xtensa, LoongArch, Nios II.
- No Wasm backend in GCC. Use emscripten or wasi-sdk (clang-based) for that.

Object formats: ELF natively; COFF on MinGW; Mach-O on Apple targets (Apple Silicon support requires GCC 14+).

DWARF: full DWARF 5 support, identical to GCC.

## §4 Production / language adoption status (May 2026)
- **Emacs native compilation** (since Emacs 28, default since 29): every native-compiled `.eln` file in your Emacs install was produced by libgccjit. Most modern Emacs distros (Debian, Fedora, Arch, Homebrew) ship native-comp by default. Pain points in 2025-2026 remain mainly macOS Homebrew path config (https://blog.roberthallam.org/2026/01/fixed-error-invoking-gcc-driver-brew-macos/).
- **GCC Rust** (`gccrs`): early-stage Rust frontend in the GCC tree; uses libgccjit's IR builders.
- **GDC**: D frontend in GCC, shares the same backend infrastructure.
- **Cython**: optional libgccjit backend for compile-time code emission.
- **PostgreSQL JIT**: actually uses LLVM, not libgccjit, but is the closest analogue.

Maintainership is steady (David Malcolm plus the GCC release cadence: GCC 15 was released April 2025). License is GPL v3 with the GCC Runtime Library Exception.

## §5 Engineering cost for Mochi
- **Binary footprint**: libgccjit.so is large, ~80-150 MB depending on enabled targets and whether LTO/Polly equivalents are linked.
- **Build complexity**: GCC must be built with `--enable-languages=jit --enable-host-shared`. Most distros ship a `libgccjit-15-dev` package. For Mochi we would link via cgo. There is no Go binding; we would write our own thin wrapper.
- **License**: **GPL v3 with Runtime Library Exception**. This is the deal-breaker for many host languages. The Runtime Library Exception explicitly allows compiled programs to be redistributed under any license, but **the compiler binary itself (the Mochi tool) would be subject to GPL v3 because it links libgccjit**. For Mochi (currently a permissive license) this means either dual-licensing the tool, isolating libgccjit in a separate process, or rejecting this backend.
- **Cross-compilation**: One libgccjit per host triple per target triple. Not as friendly as LLVM/Cranelift. Distro packages typically ship native-only; cross-libgccjit requires a custom GCC build.
- **Debugging**: Full DWARF, excellent.
- **Runtime startup**: Several hundred milliseconds to construct a `gcc_jit_context`; compilation itself is GCC-grade slow at `-O2`+.

## §6 Mochi adaptation note
The mapping from compiler3 IR (`/Users/apple/github/mochilang/mochi/compiler3/ir`) to libgccjit's API is straightforward but verbose: each Mochi function becomes a `gcc_jit_function`, each basic block becomes a `gcc_jit_block`, each op becomes a sequence of `gcc_jit_block_add_assignment`/`add_eval`/`end_with_*` calls. The cost is the C API ergonomics: building IR through opaque pointers in cgo is significantly more cumbersome than emitting text (QBE) or building a Rust crate (Cranelift).

Existing Mochi files affected: a new `compiler3/emit/gccjit` package plus a cgo bridge under `runtime/jit/gccjit/`. The vm3 typed Cell shape would compile to `gcc_jit_type_get_int(ctx, 8, 0)` aggregates.

## §7 Open questions for MEP-42
- **GPL contagion**: The licensing answer dominates everything else. If Mochi must remain permissively licensed (Apache 2.0 / MIT), libgccjit is out as an in-process backend. Out-of-process invocation (subprocess `gcc -x ir`) is a workaround but loses the JIT story.
- **AOT-only is viable**: If we use libgccjit only at build time (Mochi compiler invokes it, emits an object file, never ships libgccjit in the runtime), the contagion problem is much smaller (some interpretations still flag the build tool itself).
- **No Wasm**: Same gap as MIR/QBE. Wasm needs a separate path.
- **Why pick this over LLVM?** Only one reason: GCC produces measurably better code than LLVM on a handful of workloads (mostly Fortran, certain integer loops on AArch64). For a young language like Mochi, that 5-10% upside is not worth the licensing and binary-size cost.
- **Emacs precedent**: Emacs's success with libgccjit shows the path works for a GPL host. Mochi is not GPL today.