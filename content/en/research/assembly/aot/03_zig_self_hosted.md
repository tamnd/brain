---
title: "Zig Self-Hosted Compiler"
description: "Systems language rebuilding its compiler around its own native backends, with LLVM demoted to an optional path."
tags: ["native-codegen", "aot"]
weight: 30
date: 2026-05-18T18:05:41+07:00
---

## §1 Provenance

- Project home: https://ziglang.org/
- Source: https://github.com/ziglang/zig
- Devlog (primary status source): https://ziglang.org/devlog/2025/
- Self-hosted milestone post by Loris Cro: https://kristoff.it/blog/zig-self-hosted-now-what/
- Self-hosted x86_64 default-in-debug announcement: https://ziggit.dev/t/self-hosted-x86-backend-is-now-default-in-debug-mode/10447
- Mitchell Hashimoto on real-world build-time wins in 0.15.1: https://mitchellh.com/writing/zig-builds-getting-faster
- Lead author: Andrew Kelley, with a substantial contributor community (Jakub Konka on linkers, Matthew Lugg on incremental, etc.). BDFL governance via the Zig Software Foundation.

## §2 Architecture

The Zig compiler pipeline is:

1. Tokenizer and parser produce a flat AST.
2. AstGen lowers the AST into ZIR (Zig Intermediate Representation), an untyped per-file representation that is the unit of caching.
3. Sema (semantic analysis) performs comptime evaluation, type inference, and monomorphisation of generic functions on demand. The output is AIR (Analyzed Intermediate Representation), a typed per-function SSA-ish form.
4. AIR is handed to a backend. Backends are pluggable: LLVM, C (emits portable C source), and Zig's own native backends for x86_64, aarch64, arm, riscv64, wasm, and SPIR-V.
5. The Zig compiler also embeds its own linkers (ELF, COFF, Mach-O, Wasm) so it does not need LLD for most targets.

The major 2024–2026 shift: Zig is moving its default debug pipeline off LLVM. As of 0.15.x (Aug 2025), the self-hosted x86_64 backend is the default in debug mode on Linux and macOS. The AArch64 backend is rapidly catching up; the Windows COFF linker is the remaining gap. ReleaseFast and ReleaseSmall still hand off to LLVM because LLVM's optimiser is currently better. The strategic motivation is sub-second incremental builds and architecture independence from LLVM regressions (e.g., the AVR breakage cited in mattnite's "Toward building self-hosted backends for Zig").

## §3 Targets and platforms (May 2026)

Supported triples (https://ziglang.org/download/0.15.1/release-notes.html): x86_64 / aarch64 / riscv64 / arm / wasm32 / powerpc64 / mips / s390x / loongarch64 on linux, macos, windows, freebsd, netbsd, openbsd, dragonfly, illumos, wasi, freestanding. Cross-compilation is the headline feature: `zig build -Dtarget=aarch64-linux-musl` works from any host with no toolchain install. Zig ships every supported libc (musl, glibc, MinGW, mingw-w64, wasi-libc) as source, builds them on demand, and caches per-target object files.

`zig cc` and `zig c++` expose this machinery as a Clang-compatible drop-in C/C++ cross-compiler (see https://andrewkelley.me/post/zig-cc-powerful-drop-in-replacement-gcc-clang.html), used widely in non-Zig projects (Hugo, Bun, Roc, Pixi) for "build once, ship everywhere" tooling.

Static vs dynamic linking: static by default for musl targets, dynamic for glibc targets (glibc cannot be statically linked safely). Windows builds default to dynamic CRT but `-Dlinkage=static` switches.

## §4 Runtime

Zig is explicitly runtime-free. There is no garbage collector, no managed allocator (allocators are explicit values passed in), no implicit thread runtime. The "runtime" is whatever the user links in (libc, wasi, freestanding, or nothing). FFI is C-direct via `@cImport` of C headers; no FFI shims, no marshalling.

Hello-world binary on linux-x86_64 with `-O ReleaseSmall -fstrip --gc-sections`: about 6 KB statically linked against nothing, 14 KB linked against musl. A debug build is roughly 1 MB because it includes panic strings and stack-trace metadata. This is in a fundamentally different size class from Mochi or any GC'd language.

## §5 Status (May 2026)

0.15.1 (mid-2025) is the latest tagged release; 0.16 is in development. Production users include Bun (JavaScript runtime), Ghostty (terminal emulator), TigerBeetle (financial database), Roc (functional language), and Uber's Buck2 ecosystem (zig cc as their cross C toolchain).

Performance: with LLVM enabled, generated code matches Clang for C-like workloads; without LLVM, the self-hosted x86_64 backend is currently roughly 1.5–3x slower than -O0 LLVM at runtime, but compiles 5–20x faster. Incremental compilation is partially functional (single-digit-millisecond rebuilds are claimed in the 0.15 devlog) but not yet enabled by default for all workflows.

Known limitations: still pre-1.0; no API stability commitment; async/await was removed in 0.11 and is being redesigned; the COFF linker on Windows lags Mach-O/ELF; AArch64 native backend is incomplete.

## §6 Mochi adaptation note

Zig's pipeline is the cleanest example of a "polyglot backend, multiple targets, one compiler binary" design that Mochi could borrow:

- The ZIR/AIR split mirrors Mochi's source → typed-IR boundary. `compiler3` already has a typed IR; promoting it to a stable on-disk format (analogous to ZIR) would unlock incremental compilation and tooling reuse.
- Bundling libc sources for cross-compilation is a powerful idea Mochi can adopt indirectly: ship a curated set of static C runtimes (musl, MinGW, wasi-libc) inside the Mochi distribution so that `mochi build --target aarch64-linux-musl` works from a macOS dev box with no extra install.
- Two-backend strategy: a fast in-house backend for debug/incremental, LLVM for release. Mochi could prototype an x86_64 backend in `compiler3/native/` for fast iteration and keep an LLVM (or QBE) backend for release optimisation.
- `zig cc` is a model for "Mochi as a C/Go cross-toolchain frontend" if Mochi wants to dogfood its own toolchain for Go FFI.

Affected Mochi files: `compiler3/` (would gain a `native/` subtree), `runtime/vm3` (would need a freestanding mode where allocators are explicit), and the build system (a new `mochi build --target` matrix).

## §7 Open questions for MEP-42

1. Should Mochi ship its own linker (Zig's choice) or rely on the system linker (Go's choice)? The former dramatically improves cross-compilation; the latter is far cheaper to maintain.
2. Two-backend strategy: do we have the engineering budget for both an in-house backend and an LLVM/Go-asm backend? Zig spent many person-years on this.
3. Does Mochi want a runtime-free mode (`-gc none` plus explicit allocators), the way Zig is runtime-free by default?
4. Do we bundle libc sources or require a sysroot? Zig's choice has been a marketing superpower but increases distribution size by hundreds of MB.
5. Is `mochi cc` a useful product surface? It would let Mochi piggyback on Zig's cross-compile mindshare while requiring substantial C-front-end work.