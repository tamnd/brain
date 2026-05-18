---
title: "Crystal"
description: "Ruby-syntax statically-typed language with global type inference, LLVM backend, and Boehm GC."
tags: ["native-codegen", "aot"]
weight: 40
date: 2026-05-18T18:05:41+07:00
---

## §1 Provenance

- Project home: https://crystal-lang.org/
- Source: https://github.com/crystal-lang/crystal
- Release blog: https://crystal-lang.org/blog/ (1.15.0 in Jan 2025, 1.16.0 in Apr 2025, 1.17.0 in Jul 2025, 1.18.0 in Oct 2025).
- Reference manual: https://crystal-lang.org/reference/
- Author: Ary Borenszweig, Juan Wajnerman, Brian Cardiff at Manas Technology Solutions. Community-led since 2021 with 84codes sponsoring multi-threading work.
- Wikipedia overview: https://en.wikipedia.org/wiki/Crystal_(programming_language)

## §2 Architecture

Crystal is a whole-program AOT compiler. The pipeline:

1. Parser builds an AST.
2. Semantic phases run macro expansion, then a global Hindley-Milner-style type inference that uses union types as the basic representation (any expression can have type `A | B | nil`).
3. After type inference the compiler lowers to its own MIR-style representation.
4. The backend is LLVM. Crystal emits LLVM IR per fiber-friendly module, links them, and hands off to LLVM (currently supporting LLVM 13 through 20 across distributions) for optimisation and codegen.
5. The system linker (ld, lld, link.exe) produces the final ELF/Mach-O/PE.

Type inference is global rather than per-function: the compiler must see the whole program to type-check a method, because dispatch on union types requires complete instantiation knowledge. This makes Crystal effectively closed-world: there is no separate compilation of libraries, just a fast recompile from sources every time. The standard library and your code go through one compilation. Macros run in a subprocess that compiles a tiny Crystal program at compile time.

## §3 Targets and platforms (May 2026)

Tier-1: linux-x86_64-gnu, linux-x86_64-musl, linux-aarch64-gnu, darwin-x86_64, darwin-arm64, freebsd-x86_64. Tier-2/3 (as of 1.15.0, Jan 2025) added x86_64-windows-gnu, aarch64-windows-msvc, and aarch64-windows-gnu via the new MinGW-w64 / MSYS2 toolchains, enabling cross-compilation to Windows from Unix hosts. Crystal 1.16.0 (Apr 2025) extended multi-threaded execution contexts to Windows and the BSDs across x86 and ARM.

Cross-compilation works in two steps: `crystal build --cross-compile --target=...` emits a target-specific object file plus a printed `cc ...` command line that you run on the target (or in a sysroot) to link. This is more manual than Zig's "press one button" model but more flexible than .NET NativeAOT's RID matrix.

Static vs dynamic linking: musl targets static-link cleanly. The default glibc Linux builds dynamically link libc, libpcre2, libgc (Boehm), libssl, libcrypto. Crystal 1.16.1 fixed Windows linking against bcrypt for libxml2.

## §4 Runtime

The bundled runtime includes:

- Boehm-Demers-Weiser conservative GC (libgc), version 8.2.0+ for first-class multi-threading. Crystal has discussed switching to an Immix-style precise GC (see https://github.com/crystal-lang/crystal/issues/5271) but Boehm remains shipped.
- Crystal's fiber scheduler. Pre-1.16 was single-threaded by default. 1.16+ ships pluggable "execution contexts" with single-thread, multi-thread, and isolated variants, completing the multi-year MT project.
- libpcre2 for regex, libevent for I/O, OpenSSL for TLS.
- FFI is direct C call via the `lib` keyword binding to C headers, similar to Zig's `@cImport` but written manually.

Hello-world on linux-x86_64 with `--release --no-debug`: about 1.1 MB dynamically linked, around 2.4 MB statically musl-linked. Substantially smaller than Native Image, larger than Zig/Rust because of Boehm GC and libevent.

## §5 Status (May 2026)

Crystal 1.18.0 (Oct 2025) is the latest in the 1.x line. The 2025 release cadence has been three to four feature releases per year. Production users: Manas (the maintainer company), 84codes (CloudAMQP and CloudKarafka, the dominant Crystal production deployment), AppSignal, Nikola Motor, and a long tail of web shops using Lucky and Kemal frameworks.

Performance is generally within 2x of optimised C for arithmetic, often equal for I/O-bound workloads because of the fiber runtime. Boehm GC throughput is the historic ceiling.

Known limitations: compile times scale poorly with program size because of whole-program inference (a multi-thousand-line app can take 30+ seconds); Boehm GC pauses are unpredictable; Windows support is younger than the Unix port; the type system has corner cases (instance variable inference) that surprise users.

## §6 Mochi adaptation note

Crystal is the closest "managed, statically typed, LLVM-back, GC-bundled" language to what Mochi could become. Specific patterns to steal:

- LLVM as a release-mode backend. Mochi already has a typed IR in `compiler3`; emitting LLVM IR via the existing Go bindings or via text emission is a low-risk first AOT path.
- Whole-program type inference plus union types maps very loosely onto Mochi's existing type checker. Mochi is already closed-world; Crystal demonstrates that closed-world plus union types can compile to fast native code without sacrificing inference power.
- The cross-compile via `--cross-compile + cc` script is a low-engineering-cost MVP for MEP-42 before Mochi commits to a Zig-style bundled toolchain.
- Boehm GC as a stepping stone: link `libgc` into `runtime/vm3` for the initial native build, defer building a precise collector to a later MEP. Crystal has lived with Boehm for a decade; the trade-offs are well documented.
- Multi-stage threading model rollout: ship single-thread first, add execution contexts later. Mochi can plan the same trajectory rather than blocking MEP-42 on a fully concurrent runtime.

Affected Mochi files: `runtime/vm3/gc.go` (would wrap Boehm initially), `compiler3/backend_llvm/` (new), and the `lib` binding syntax could be inspired by Crystal's `lib` block style.

## §7 Open questions for MEP-42

1. Is Boehm acceptable as a v1 GC for Mochi-native, with a plan to replace later, or does MEP-42 require a precise collector from day one?
2. Does Mochi adopt Crystal's "emit object, print link command" cross-compile model, or invest in Zig-style bundled linking?
3. Are sub-second compile times a hard requirement (which rules out whole-program inference) or acceptable to defer to a future MEP?
4. Do we expose multiple execution contexts (single-thread, multi-thread, isolated), or commit to one model?
5. Crystal does not ship a Native Image-style "build-time heap snapshot". Should Mochi do the snapshot or stay simple like Crystal?