---
title: "Hare"
description: "Tiny systems language built on QBE, deliberately constrained, BSD/Linux-only, manual memory."
tags: ["native-codegen", "aot"]
weight: 60
date: 2026-05-18T18:08:55+07:00
---

## §1 Provenance

- Project home: https://harelang.org/
- Source: https://git.sr.ht/~sircmpwn/hare
- Specification: https://harelang.org/specification
- Announcement: https://harelang.org/blog/2022-04-25-announcing-hare/
- Backend (QBE): https://c9x.me/compile/ (Quentin Carbonneaux's QBE compiler backend).
- Blog (active 2024–2025): https://harelang.org/blog/
- Author: Drew DeVault and contributors (Sebastian, Pasta, spxtr, others). BDFL governance.

## §2 Architecture

The Hare pipeline is one of the simplest in modern language design:

1. Lexer/parser produce an AST.
2. The type checker resolves a static, inferred type system with tagged unions and no generics.
3. The compiler lowers the typed AST into QBE intermediate language (a small SSA IR designed by Quentin Carbonneaux as a deliberate "small LLVM").
4. QBE optimises and emits assembly for the target ISA (x86_64, aarch64, riscv64 as of 2024–2025).
5. The system assembler and linker produce the final ELF.

QBE is the entire backend story. There is no LLVM fallback, no native-codegen alternative. This is a deliberate constraint: the whole Hare toolchain (compiler plus QBE plus the runtime) sits in around 1.4 MB of binary, and the team values that footprint as evidence the language is "simple, stable, robust."

The language itself has no generics (closed by design), no macros, no operator overloading, no implicit conversions, and no async runtime. Error handling is via tagged unions. Manual memory management with no GC; the standard library exposes allocators as values, similar to Zig.

## §3 Targets and platforms (May 2026)

Supported ISA × OS matrix (tracked at https://harelang.org/installation/):

- x86_64-linux, aarch64-linux, riscv64-linux
- x86_64-freebsd, x86_64-openbsd, x86_64-netbsd, plus aarch64 on the BSDs.
- No Windows, no macOS. Drew DeVault has stated no plans to support non-free platforms; a fork could attempt it but the language deliberately leans on POSIX semantics.

Cross-compilation works by setting `HARE_ARCH` and `HARE_PLATFORM` and pointing at a target QBE plus assembler/linker. There is no bundled libc and no Zig-style sysroot mechanism; you bring your own toolchain.

Linking: typically static, against the Hare standard library (which is itself written in Hare and avoids libc where it can). Some platforms still link a small amount of libc for syscalls Hare has not yet reimplemented.

## §4 Runtime

Hare ships a minimal runtime, written in Hare itself:

- No garbage collector. Memory is managed manually; the stdlib provides allocator types (heap, alloca, fixed) that callers pass explicitly.
- A small "rt" module handles process start, syscalls, stack traces.
- No thread runtime in the standard library (proposed but not standardised in May 2026).
- FFI is direct: `@symbol` and `let foo: ... = bar;` declarations expose C symbols. There is no marshalling.

Hello-world on linux-x86_64: about 25 KB statically linked. The Hare toolchain itself is reported as 1.4 MB total. This places Hare in the same size class as Zig at the very low end.

## §5 Status (May 2026)

Hare remains pre-1.0. The blog (https://harelang.org/blog/) shows steady but small-scale activity through 2024 and 2025: roughly one to two posts per month from Drew DeVault and a handful of contributors. The roadmap focuses on stdlib gaps (TLS, raw IP sockets) and stability for a 1.0 release.

Production users are mostly the maintainers' own projects: Drew DeVault's Ares microkernel research, Himitsu (a secret store), and various SourceHut internal utilities. There is no commercial user base.

Performance: comparable to clang -O2 for most workloads, because QBE produces decent (not great) code. QBE deliberately optimises less aggressively than LLVM in exchange for compile speed and simplicity, so heavy numeric code can be 1.5–3x slower than equivalent C through clang/LLVM.

Known limitations: tied to QBE (limits target reach to whatever QBE supports), no Windows/macOS, no generics, no language async story, small ecosystem.

## §6 Mochi adaptation note

Hare is the most aggressive "constrain yourself to win simplicity" case study. Useful patterns:

- QBE as a real alternative backend to LLVM. QBE is a fraction of LLVM's size (a few thousand lines of C), the IR is readable, and it covers x86_64/aarch64/riscv64. If Mochi wants a small toolchain footprint and is willing to give up peak optimisation, a `compiler3/backend_qbe/` is a credible option, mirroring Hare's choice.
- No GC, allocators as values. Mochi already has an arena allocator in `runtime/vm3`; Hare shows that a useful systems language can ship with allocators as plain values and let users compose them. This is a viable subset for a "Mochi embedded" mode.
- Deliberate language constraint as a design rule. Hare refuses generics to stay small. Mochi will not go that far, but the principle (every feature has a cost in compile time, binary size, and bug surface) is the right lens for MEP-42.
- POSIX-first portability. Hare's narrow OS support is a feature for the maintainers. Mochi could publish an explicit "Tier 1: linux/macOS/Windows" matrix and stop pretending to support obscure platforms.

Affected Mochi files: `compiler3/backend_qbe/` (new), and possibly a `runtime/vm3/nogc/` subset for "Mochi embedded".

## §7 Open questions for MEP-42

1. Is QBE the right backend for a low-effort, small-footprint Mochi AOT path? Trade-off vs LLVM is meaningful.
2. Should Mochi expose a no-GC mode for embedded targets, the way Hare does by default?
3. How much should Mochi cut to keep the compiler binary small? Hare's 1.4 MB is a hard target Mochi probably cannot match without major sacrifices.
4. Mochi cares about Windows; Hare does not. This rules out Hare as a direct architectural template for the full Mochi story, but the QBE backend remains attractive for the Unix tier.