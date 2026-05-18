---
title: "C as a Code-Generation Backend for Mochi"
description: "The lowest-cognitive-load path: emit C, let GCC/Clang do the rest."
tags: ["native-codegen", "backends"]
weight: 100
date: 2026-05-18T18:11:03+07:00
---

## §1 Provenance
- Nim's C backend: https://nim-lang.org/docs/backends.html
- Nim compiler user guide: https://nim-lang.org/docs/nimc.html
- Vlang (V): https://vlang.io/ ; the V compiler emits C by default.
- Hare uses QBE rather than C, so it is **not** an example here. Hare's c-cproc relative `cproc` is a C-to-QBE compiler.
- Cython: https://cython.org/
- MicroPython's mpy-cross with C emission: https://github.com/micropython/micropython
- Classic reference: Cooper and Torczon, "Engineering a Compiler" (EaC), Chapters 7 and 8 cover C as a target.
- Earlier well-known C backends: Eiffel (SmartEiffel), Sather, Mercury, Vala, Genie, Haskell's old `-fvia-C` mode (deprecated post-GHC 7.x in favor of LLVM/NCG).

## §2 Mechanism
The compiler emits a C source file (or many) representing the program's semantics. The host system C compiler (GCC, Clang, MSVC, TCC) handles preprocessing, optimization, instruction selection, register allocation, ABI, debug info, and linking.

Typical strategies:
- **One C function per source function**. Direct mapping; readable output if you want it.
- **Trampolined control flow**: turn each basic block into a labeled statement; use `goto` for arbitrary control flow. This is the Nim and Vala approach.
- **Computed goto for interpreters**: a fast switch-dispatch idiom (`&&label`, GCC-specific).
- **setjmp/longjmp for exceptions**: portable but slow.
- **Native exceptions via `__builtin_setjmp` or libunwind**: better but per-compiler.

For garbage-collected languages, a C backend usually carries a runtime library (its own GC, scheduler, etc.) and the emitted C calls into that runtime.

## §3 Target coverage (May 2026)
**Every target that GCC, Clang, MSVC, or TCC supports.** That is the appeal. Concretely for Mochi's MEP-42 priority list:
- x86_64 Linux/macOS/Windows: all four C compilers.
- AArch64 Linux/macOS/Windows: GCC, Clang, MSVC.
- RISC-V RV64GC Linux: GCC, Clang.
- Wasm: Emscripten (Clang-based), wasi-sdk (Clang-based). Both produce wasm32 modules.
- Plus: every embedded target with a C compiler (AVR, MSP430, PIC, ARM Cortex-M, RP2040, ESP32, etc.). This is unmatched by any other backend on this list.

Object formats: whatever the host toolchain produces.

DWARF: full, from GCC/Clang. PDB on MSVC.

## §4 Production / language adoption status (May 2026)
- **Nim**: ships C, C++, Objective-C, and JavaScript backends. C is the default. Used in production by Status (cryptocurrency), Galois, NimSkull, various game and systems shops.
- **V (Vlang)**: C-only backend. Active community, controversial design but real adoption.
- **Cython**: emits C for Python; ubiquitous in scientific Python.
- **Crystal**: was C-backed in early versions; switched to LLVM. Still illustrative.
- **GHC**: had a C backend (`-fvia-C`); removed because LLVM and the native code generator surpassed it in code quality.
- **Vala / Genie** (GObject ecosystem): emit C.
- **Haxe**: ships a C++ backend (`hxcpp`), morally similar.
- **MicroPython mpy-cross**: optional C emit path for AOT.
- **Eiffel / SmartEiffel**: classic; the "Liberty Eiffel" community continues this tradition.
- **TXR Lisp** and other small languages.

Maintainership of "C as a target" as a technique is not a single project; it is a folklore pattern. Every C compiler the user has counts as part of the ecosystem.

Performance: with GCC `-O3` or Clang `-O3`, generated code is essentially native-compiler quality. The penalty is purely compile-time: the C compiler must reparse, retypecheck, and re-optimize what the language frontend already understood.

License: unencumbered (the technique). Mochi's emitted C is whatever Mochi chooses to license it as; the host C compiler's license does not infect emitted code (Runtime Library Exception).

## §5 Engineering cost for Mochi
- **Binary footprint**: Mochi adds **zero** new dependencies; the C compiler is the user's responsibility.
- **Build complexity**: Mochi emits `.c` files and shells out to `cc`. No cgo. No external libraries to link against at Mochi build time.
- **License**: irrelevant; C-as-target is a technique.
- **Cross-compilation**: cross-compile by setting `CC=aarch64-linux-gnu-gcc` (or `zig cc -target ...` for the zero-install hack). Mochi can ship a recommended toolchain matrix.
- **Debugging**: full DWARF/PDB via the host compiler. Source mapping back to Mochi source requires `#line` directives in the emitted C (standard technique used by Cython, Nim, Bison, etc.).
- **Runtime startup**: pure AOT; nothing at runtime.

For a Go-hosted Mochi, this is the **lowest engineering cost** of every backend on the list. No FFI. No cgo. No new dependency. The downside is per-target compile speed and the awkwardness of shipping a C compiler with Mochi.

## §6 Mochi adaptation note
Mochi already has `runtime/tcc/Makefile` (`/Users/apple/github/mochilang/mochi/runtime/tcc/Makefile`), suggesting prior thought about TCC integration. A `compiler3/emit/c` package would:
1. Walk compiler3 IR (`/Users/apple/github/mochilang/mochi/compiler3/ir`).
2. Emit one C function per Mochi function. Each vm3 op in `/Users/apple/github/mochilang/mochi/runtime/vm3/op.go` becomes a small inline C function or macro.
3. Emit the vm3 typed Cell (`/Users/apple/github/mochilang/mochi/runtime/vm3/cell.go`) as a C `uint64_t` aggregate with helper macros.
4. Emit `#line` directives to preserve Mochi source locations.
5. Shell out to `cc` or `zig cc`.

The vm3 interpreter itself is essentially a C program written in Go; transliterating to C is straightforward. Memory management hooks would call into a small libmochi runtime (also written in C, or compiled from a Mochi runtime subset).

## §7 Open questions for MEP-42
- **Compile speed**: C compilers are slow. A 10k-line Mochi program emits ~50k-100k lines of C; GCC `-O2` may take seconds. Mitigation: ship `-O0` for debug builds and `-O2` for release.
- **Which C compiler?** TCC is fast but produces poor code; GCC/Clang is slow but excellent. Recommendation: detect at install time, default to whichever is present, document Clang and TCC tradeoffs.
- **Zig as portable cc**: `zig cc` (https://andrewkelley.me/post/zig-cc-powerful-drop-in-replacement-gcc-clang.html) bundles Clang with full cross-compilation toolchains for every target out of the box. A single Zig install gives Mochi cross-compilation to every triple. Strongly worth considering.
- **No JIT story**: C-as-target is AOT-only. JIT would use a separate backend (golang-asm for now, copy-and-patch later).
- **Runtime size**: Mochi's runtime (GC, scheduler, stdlib) must be available as either a static C library or as emitted C alongside user code.
- **Verdict**: C-as-target is the **default Phase 1 path for AOT** unless we have a strong reason to deviate. It maximizes target coverage and minimizes Mochi-side complexity.