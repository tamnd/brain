---
title: "V Language"
description: "Statically-typed Go-influenced language that defaults to emitting C, with experimental native and LLVM backends and a multi-mode memory model."
tags: ["native-codegen", "aot"]
weight: 70
date: 2026-05-18T18:08:55+07:00
---

## §1 Provenance

- Project home: https://vlang.io/
- Source: https://github.com/vlang/v
- FAQ: https://github.com/vlang/v/wiki/FAQ
- Memory management docs: https://docs.vlang.io/memory-management.html
- Native backend discussion: https://github.com/vlang/v/discussions/13675
- Architecture wiki (DeepWiki overview): https://deepwiki.com/vlang/v
- Author: Alexander Medvednikov (Medvednikov), Estonia. First public release 2019, MIT license, beta in May 2026. Notable as a 2025 entrant on the TIOBE index.

## §2 Architecture

V's pipeline:

1. Parser → AST. The parser is hand-written and pegs single-pass single-file parsing as the performance budget.
2. Checker does name resolution and type checking. V's type system is deliberately small (no implicit conversions, no generics in early V, partial generics now).
3. The compiler then dispatches to one of several backends:
   - **C backend (default and production).** Emits human-readable C source, then invokes `tcc`, `gcc`, `clang`, or `msvc`.
   - **Native backend.** Emits machine code directly without going through C. Targets x86_64 ELF, Mach-O, and PE in May 2026, with partial aarch64. The DeepWiki architecture page describes "Native Backend: Architecture Support" and "Native Backend: Binary Formats" as the two layers.
   - **JavaScript backend.** Emits JS for browser/Node.
   - **Go backend.** Emits Go source (experimental).
   - **LLVM backend.** Community-developed.
4. The build system handles parallel compilation by splitting generated C into many files.

The strategic posture is: C backend for production (delegates optimisation to gcc/clang), `tcc` for sub-second debug builds, native backend as a future hedge to drop the C dependency entirely. V markets itself on compile time: "compiles itself in under a second" on a developer laptop.

## §3 Targets and platforms (May 2026)

Anything the chosen C compiler supports. Officially: linux-x86_64/arm64, macos-x86_64/arm64, windows-x86_64, freebsd, openbsd, netbsd, dragonfly, solaris, android (via NDK), iOS (via Xcode), wasm via emscripten or directly. The native backend currently covers a smaller matrix.

Cross-compilation uses the underlying C cross-compiler. `v -os linux ...` from macOS works if you have a Linux `cc` (commonly `zig cc`). V ships pre-built `tcc` binaries via the vlang/tccbin repo so the default debug build needs nothing on the host.

Linking: dynamic by default against system libc. `-prod` enables optimisations through the chosen cc; `-skip-unused` performs dead-code elimination at the IR level before C emission.

## §4 Runtime

Four memory management modes, selectable per build:

- **GC (default).** Boehm-Demers-Weiser conservative GC, the same library Crystal uses. Disable with `-gc none`.
- **Autofree (`-autofree`).** Compiler inserts `free()` calls based on lifetime analysis; remaining ~5 percent is caught by a fallback GC. Still WIP and not the default.
- **Manual (`-gc none`).** Caller manages memory; useful for embedded.
- **Arena (`-prealloc`).** Bump allocator, freed at process exit. Aimed at compilers and short-lived batch tools.

Threading is via V's `spawn` keyword and a small runtime built on pthreads/Win32 threads. FFI to C is the first-class story: `#include "header.h"` + `fn C.foo() int` and you are calling C. Optional binding generators exist for C, C++, JavaScript, and Python.

Hello-world on linux-x86_64: about 100 KB dynamically linked with Boehm GC (`-prod`); around 20–40 KB with `-gc none` and `-skip-unused`; under 10 KB with `-prod -gc none -skip-unused` and external stripping. The native backend can produce even smaller artefacts but with limited stdlib coverage.

## §5 Status (May 2026)

V remains officially in beta. Production users include VOSCA's cloud tooling, ttytter-style CLIs, and a handful of game-dev projects. The Vinix kernel is written in V. Notable adoption: Wails (the popular Go GUI toolkit) has experimented with V bindings.

Performance is "C-level" when running on the C backend with `-prod` (because it literally is C, optimised by gcc/clang). The native backend trails by 2–4x today. Autofree's lifetime analysis is still considered experimental and is not recommended for production use.

Known limitations: documentation and tooling lag behind the language's marketing; some advertised features (full autofree, full native backend) are works in progress; generics support is partial; the project has historically been controversial in online discourse for promising more than has shipped. The C backend, however, is widely acknowledged to work and to be fast.

## §6 Mochi adaptation note

V's most relevant lessons for Mochi are about pragmatism in backend choice and multi-mode memory:

- Emit C as the default backend, `tcc` for fast iteration, gcc/clang for release. Mochi could ship the same "two-cc strategy": a tiny embedded `tcc` for `mochi run`/iteration, hand off to the host gcc/clang for `mochi build --release`. This delivers sub-second compile times for development without giving up production performance.
- Multi-mode memory management exposed per-build, not per-source-file. V's `-gc`, `-autofree`, `-prealloc` flags are a clean UX. Mochi can adopt the same surface, mapping to its existing arena allocator and a future tracing/RC option.
- Keep human-readable C emission. V's generated C is intentionally readable so users can debug into it. Mochi should do the same; readable C is also a viable distribution format for places where Mochi cannot install a toolchain (e.g., shipping generated C as a tarball).
- Defer the native backend. V's experience shows that the native backend is a multi-year project; Mochi should not block MEP-42 on it. Ship C-backend first, add native later if at all.

Affected Mochi files: `compiler3/backend_c/` (new), `runtime/vm3/gc/` (multi-mode allocator), and a build flag matrix in the CLI.

## §7 Open questions for MEP-42

1. Bundle `tcc` (as V does) for instant compile-and-run, or rely entirely on the host cc?
2. Do we expose all four V-style memory modes, or pick a smaller set?
3. Should generated C be a first-class output (mochi-to-C as a product) or strictly intermediate?
4. V's track record (promising > delivering) is a cautionary tale for MEP-42's roadmap claims.