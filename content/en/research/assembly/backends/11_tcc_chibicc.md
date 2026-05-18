---
title: "TCC, chibicc, Cuik as Reference Points for Mochi"
description: "\"How small can a useful native backend be?\""
tags: ["native-codegen", "backends"]
weight: 110
date: 2026-05-18T18:11:03+07:00
---

## §1 Provenance
- **TCC** (Tiny C Compiler): https://bellard.org/tcc/, mob branch at https://repo.or.cz/tinycc.git, mirror https://github.com/TinyCC/tinycc. Originally by Fabrice Bellard (~2001); since ~2012 maintained by grischka with community contributions through November 2025. Last official release: 0.9.27 (December 2017); the mob branch is the active line.
- **chibicc**: https://github.com/rui314/chibicc by Rui Ueyama (also author of LLVM lld and 8cc). Educational reference compiler for a book in progress.
- **8cc**: https://github.com/rui314/8cc, Ueyama's older C compiler, archived.
- **Cuik**: https://github.com/RealNeGate/Cuik, by Yasser Arguelles Snape ("NeGate"). Mastodon: https://mastodon.social/@negate. Active development through 2025; no formal releases yet.
- **TB** (Cuik's backend): https://yasserarg.com/tb (referenced in Compiler Explorer request https://github.com/compiler-explorer/compiler-explorer/issues/7995).

## §2 Mechanism
**TCC**: single-pass C99 compiler. Lexes, parses, and emits machine code in one walk of the source. No IR worth speaking of. The emitted code is approximately what you get from `gcc -O0`: correct, naive, no register allocation beyond a tiny window. The compile speed is the famous number: ~10x faster than GCC `-O0` on equivalent input. TCC also implements `-run`, which JITs source and runs it in-process.

**chibicc**: pedagogical single-pass C11 compiler. ~10k lines of C. No optimization. Emits assembly (x86_64 SysV only). The author's stated goal is readability for the accompanying book; chibicc happily compiles itself, Git, SQLite, libpng, and a few hundred thousand lines of real C code, with the catch that "chibicc emits terrible code which is probably twice or more slower than GCC's output."

**Cuik**: a modern C11 compiler aiming to replace GCC/MSVC/LLVM. Modular: `libCuik` is the frontend, `TB` (Tilde Backend) is the backend. TB has its own IR, instruction selection, register allocator; designed for fast compile times à la Cranelift. Cuik is "still early" per its README but development is steady through 2025.

## §3 Target coverage (May 2026)
- **TCC** (mob branch): x86_64, i386, ARM (32-bit), ARM64 (AArch64), RISC-V (RV64), Win64. ELF, PE, Mach-O are partially supported.
- **chibicc**: x86_64 Linux only. No other targets, no plans.
- **Cuik / TB**: x86_64 primarily; AArch64 in progress; Windows COFF support good (the author's focus).

Object formats: TCC emits ELF and PE/COFF; chibicc emits assembly only; Cuik emits ELF and COFF.

## §4 Production / language adoption status (May 2026)
- **TCC**: production-adjacent use in reproducible-builds projects (notably the bootstrappable builds initiative, where TCC is one of the smallest reachable C compilers from a hex-coded seed). Distros ship it (Debian, Fedora, Arch). Commits through October 2025; mailing list active through November 2025.
- **chibicc**: not production. Used as the canonical "build a C compiler" reference. There is amusing 2026 chatter that Anthropic's "Claude's C compiler" project shows chibicc-flavored bugs (https://github.com/anthropics/claudes-c-compiler/issues/232), suggesting chibicc's code may have been influential in training data.
- **Cuik**: hobbyist active project. Growing community interest; not production.

License: TCC is LGPL; chibicc is MIT (per the repo); Cuik is MIT.

## §5 Engineering cost for Mochi
These are **reference points**, not realistic Mochi backends. The takeaways:

- **TCC** demonstrates that a single binary covering x86_64+arm+arm64+riscv64 in ~80k lines of C is achievable. If Mochi wrote its own native backend from scratch (rejecting LLVM/QBE/Cranelift), TCC's source is the ceiling for "naive but useful."
- **chibicc** demonstrates that you can have a real C compiler in ~10k lines, single-file, single-pass, x86_64-only. For a Mochi "weekend prototype" emitter targeting only macOS arm64 or Linux x86_64, this is the closest existing template.
- **Cuik/TB** demonstrates a modern alternative to LLVM's pipeline in C, written by one person, with comparable architecture choices to Cranelift. TB might be a future target backend in its own right once it stabilizes.

For actual integration:
- **TCC as JIT**: TCC's `libtcc` lets us compile C strings at runtime and call them. This pairs with the `c_as_backend` strategy: Mochi emits C, libtcc JITs it for fast iteration, GCC/Clang compiles it for release. Mochi already has `runtime/tcc/Makefile`.
- **chibicc and Cuik**: too immature for Mochi to depend on; useful as design references only.

## §6 Mochi adaptation note
The existing `runtime/tcc/Makefile` (`/Users/apple/github/mochilang/mochi/runtime/tcc/Makefile`) suggests Mochi already considered TCC as a fast development-tier compiler. Concretely:
1. Mochi emits C (per `10_c_as_backend.md`).
2. For `mochi run` and tests: invoke `libtcc` via cgo to JIT the emitted C in ~10ms.
3. For `mochi build`: invoke `cc` (GCC/Clang/zig cc) for high-quality optimization.

This two-tier pattern (TCC for fast feedback, GCC/Clang for release) is the same pattern Cython, Nim, and Julia (in spirit) use.

If we want a non-C, non-LLVM lower-level backend written by ourselves, chibicc and Cuik are useful reference reads but not adoption candidates.

## §7 Open questions for MEP-42
- **Should Mochi ship a vendored TCC?** TCC's small size (~500 KB binary, LGPL) makes vendoring feasible, but LGPL bytecode-redistribution constraints would need legal review.
- **Bus factor on TCC**: grischka is the primary maintainer post-Bellard. Healthy mailing list but small community.
- **Is rolling our own naive emitter sensible?** Only if every external backend (LLVM, Cranelift, QBE, MIR) is rejected. The cost is multi-month for x86_64 alone, multi-year for full multi-arch parity. The chibicc and TCC source counts suggest realistic floors.
- **Cuik watch**: if Cuik/TB stabilizes by 2027 and gains AArch64 + RISC-V backends, it becomes a real "Cranelift in C" option for non-Rust hosts.
- **No Wasm**: none of these emit Wasm. Different problem.