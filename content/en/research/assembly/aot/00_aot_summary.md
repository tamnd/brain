---
title: "AOT Compilation Case Studies: Summary for MEP-42"
description: "Cross-cutting patterns from twelve production AOT pipelines, with a recommendation for which one Mochi should learn from most."
tags: ["native-codegen", "aot"]
weight: 0
date: 2026-05-18T18:13:12+07:00
---

## §1 Scope

This summary distils the case studies in `01_*.md` through `12_*.md`: GraalVM Native Image, .NET NativeAOT, Zig self-hosted, Crystal, Nim, Hare, V, Julia/juliac, Mojo, GHC NCG, Swift / Embedded Swift, and Static Python / Cinder / CPython 3.13 JIT. Each file has its own provenance, architecture, target matrix, runtime, status, Mochi adaptation note, and open questions. This document looks only at the cross-cutting patterns.

## §2 Closed-world vs open-world

The most consequential architectural axis. Closed-world AOT requires the compiler to see every reachable function/type/resource at build time; open-world allows the program to extend itself at runtime.

- **Closed-world by construction:** Zig, Crystal, Hare, V (C backend), GHC, Embedded Swift, Mochi. These compilers can reason globally and trim aggressively.
- **Closed-world by retrofitting:** GraalVM Native Image, .NET NativeAOT, Julia juliac, Static Python. These started open-world and added a closed-world AOT path with escape hatches (reachability metadata, source generators, trim-safe/trim-unsafe, `[DynamicallyAccessedMembers]`).
- **Open-world even in AOT:** standard Swift (dynamic dispatch via vtables/witness tables that can be extended via dynamic loading), Mojo (Python interop).

Mochi is already closed-world, which is the more valuable starting point. The Native Image / NativeAOT / juliac stories are mostly cautionary: do not paint yourself into a corner where dynamic features force a "trim warning" UX nightmare.

## §3 Runtime-bundled vs runtime-shared

- **Runtime entirely bundled into the executable:** Native Image (SubstrateVM bundled), NativeAOT (CoreCLR trimmed and bundled), Crystal (Boehm GC linked statically when desired), Zig (no runtime to bundle), Nim (tiny runtime statically linked), Hare (almost no runtime), V (Boehm or none), GHC (RTS statically linked).
- **Runtime as a shared library next to the binary:** Julia/juliac (libjulia-internal.so + bundle layout), Swift (libswiftCore.dylib), Embedded Swift (no runtime to share, fully bundled).
- **Runtime is the host process:** Cinder, Static Python, CPython JIT (the binary is `python` plus extension modules).

Bundling is the dominant pattern for systems where users expect a single artefact to drop on a server or container. Sharing makes sense only when the runtime itself is heavy (Julia: libLLVM at runtime) or when an OS or app store wants to manage the runtime separately (Apple's libswiftCore).

## §4 Single-backend (LLVM) vs polyglot backend

- **LLVM-only:** Crystal, Swift, Mojo (LLVM under MLIR), Julia, Rust (not covered here but the canonical example), Mono AOT.
- **Multiple backends:** Zig (in-house + LLVM + C), GHC (NCG + LLVM + C + Wasm + JS), Nim (C + C++ + JS + LLVM via clang), V (C + native + JS + Go + LLVM via community).
- **Non-LLVM single backend:** Hare (QBE only), GraalVM Native Image (Graal compiler).
- **In-house only:** GraalVM (Graal compiler is in-house), GHC NCG (per-ISA hand-written).

LLVM gives you peak codegen and broad target reach at the cost of distribution size and compile time. In-house backends give you fast compile, control over your platform matrix, and independence from LLVM regressions, at the cost of significant engineering. The two-backend strategy (fast in-house for debug, LLVM for release) is the pragmatic compromise GHC and Zig both adopted.

## §5 GC choices

- **Conservative Boehm-Demers-Weiser:** Crystal, V (default). Easy to integrate, predictable, has a well-known throughput ceiling.
- **Reference counting (ARC) with optional cycle collection:** Swift (ARC), Nim (ARC/ORC).
- **Generational copying / parallel-mark / nonmoving hybrid:** GHC RTS, Java's G1/ZGC on Substrate VM, .NET CoreCLR GC.
- **No GC at all:** Zig, Hare, Embedded Swift (when explicit).
- **Multi-mode selectable per build:** Nim (`--mm:`), V (`-gc`).

Mochi currently has an arena allocator (MEP-40). The natural progression is to add an ARC option (Swift/Nim path) before considering tracing, because ARC plays well with closed-world ownership analysis and avoids a stop-the-world pause story.

## §6 Cross-compilation

- **Best in class:** Zig (`zig build -Dtarget=...` from any host to any target, bundled libcs), Nim (delegated to host C cross-compiler, often paired with `zig cc`).
- **Solid:** .NET NativeAOT (RID matrix via NuGet packages), Rust (rustup target add).
- **Workable but manual:** Crystal (`--cross-compile` emits object plus suggested cc command), Embedded Swift (LLVM cross + vendor SDK).
- **Limited:** GraalVM Native Image (essentially host-target), Julia juliac (host-target), Hare (BYO toolchain).

If Mochi cares about cross-compilation, Zig's model is the gold standard but expensive to copy fully. Crystal's "emit object plus cc command" is the minimal viable thing. Pairing with `zig cc` gives Nim-level cross capability with little Mochi engineering.

## §7 Hello-world binary sizes (May 2026 best efforts, stripped)

- Hare: ~25 KB
- Zig (no libc, ReleaseSmall): ~6 KB; with musl ~14 KB
- Embedded Swift on Cortex-M: hundreds of bytes
- Nim with `--mm:none`: ~50–80 KB
- V with `-gc none -skip-unused`: ~20–40 KB
- Crystal (musl static): ~2.4 MB
- Rust release (not covered, for reference): ~300 KB stripped
- .NET NativeAOT: ~1.3 MB stripped, ~9 MB default
- Mojo 1.0 beta: ~1–3 MB
- GHC static: ~12 MB
- GraalVM Native Image: ~8–12 MB stripped, ~4–6 MB with Epsilon GC
- Julia juliac trim-safe: ~5–20 MB

Mochi will likely land in the 1–10 MB band for a hello-world depending on whether MEP-42 chooses Boehm GC, ARC, or a Native-Image-style bundled runtime.

## §8 Recommendation for Mochi

Mochi is a statically-typed, closed-world, Go-hosted bytecode VM with an arena allocator and a typed compiler IR. Of the twelve case studies, the closest architectural analog is **Crystal**:

- Both are closed-world by construction with whole-program type information.
- Both ship a managed runtime (Mochi's vm3, Crystal's libgc plus fiber scheduler).
- Both have an existing IR that can be lowered to LLVM in a single step.
- Both target the same OS/ISA tier: linux/macos/windows on x86_64/arm64.
- Both face the same GC-vs-arena vs ARC trade-off.

The case study Mochi should *learn most from*, however, is **.NET NativeAOT**, because:

- It is the most mature production example of "managed language + bytecode VM + AOT pipeline that trims the runtime".
- The ILC trim model, the `[DynamicallyAccessedMembers]` annotation pattern, and the source-generator alternative to runtime reflection are all directly applicable to Mochi's stdlib (json, yaml, sql, http).
- The cross-platform RID matrix and single-file deployment story are exactly the UX Mochi users will expect.

Secondary patterns to import:

- From **Zig**: `zig cc` as a model for `mochi cc` (lower priority, defer to a later MEP) and the bundled-libc cross-compilation experience.
- From **GraalVM Native Image**: build-time heap snapshotting (Mochi can serialise its arena into a read-only data section).
- From **Nim/V**: a `--gc` mode flag exposing arena / ARC / tracing / none.
- From **Embedded Swift**: an explicit `mochi build --mode=embedded` subset that disables dynamic features for smallest binaries.
- From **GHC**: the discipline of a clean IR (Cmm-style) that admits multiple backends without entanglement.
- From **Crystal**: the pragmatic "emit object plus print cc command" cross-compile MVP.

The case studies that are interesting but **not** the right template for Mochi: Julia (Mochi does not start open-world, so the trim work is unnecessary), Mojo (MLIR is too heavy a dependency for v1), Hare (too constrained, no Windows), Static Python (Mochi is not retrofitting a dynamic language).

## §9 Reading order

For someone implementing MEP-42, the recommended reading order of the per-case-study files is:

1. `02_dotnet_nativeaot.md` (primary architectural template)
2. `04_crystal.md` (closest existing analog)
3. `01_graalvm_native_image.md` (heap-snapshot pattern, closed-world rigor)
4. `03_zig_self_hosted.md` (cross-compilation gold standard, two-backend strategy)
5. `10_ghc_ncg.md` (IR discipline, multi-backend sustainability)
6. `11_swift_embedded.md` (embedded-mode subset pattern)
7. `05_nim.md` (compile-to-C backend, ARC/ORC mode flags)
8. `07_v_language.md` (multi-mode memory flags, tcc-for-debug)
9. `08_julia.md` (cautionary tale, bundle layout)
10. `09_mojo.md` (long-horizon MLIR option)
11. `12_static_python_facebook.md` (typed-subset compilation lessons, copy-and-patch as JIT option)
12. `06_hare.md` (QBE as alternative small backend; size discipline)