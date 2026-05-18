---
title: "GHC NCG and the LLVM Backend Choice"
description: "The Glasgow Haskell Compiler's native code generator: hand-written, x86_64 / aarch64 / risc-v, alongside an LLVM alternative."
tags: ["native-codegen", "aot"]
weight: 100
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- Project home: https://www.haskell.org/ghc/
- Source: https://gitlab.haskell.org/ghc/ghc
- Backends documentation: https://downloads.haskell.org/ghc/9.12.2/docs/users_guide/codegens.html
- 9.12.1 release blog: https://www.haskell.org/ghc/blog/20241216-ghc-9.12.1-released.html
- 9.12.2 release blog: https://www.haskell.org/ghc/blog/20250314-ghc-9.12.2-released.html
- 9.12.3-rc2 announcement (Nov 2025): https://www.haskell.org/ghc/blog/20251111-ghc-9.12.3-rc2-released.html
- Well-Typed activity reports (the most consistent NCG status source): https://www.well-typed.com/blog/
- Tweag's "Making GHC faster at emitting code": https://www.tweag.io/blog/2022-12-22-making-ghc-faster-at-emitting-code/
- Foundational paper: Marlow et al., "Faster Laziness Using Dynamic Pointer Tagging" (ICFP 2007); the Cmm/STG split traces to the Spineless Tagless G-machine (Peyton Jones 1992).

## §2 Architecture

GHC's pipeline is one of the most carefully engineered in any compiler:

1. Parsing and renaming produce HsSyn (Haskell syntax tree).
2. Type checking and desugaring produce Core (a small typed lambda calculus, essentially System FC).
3. Many Core-to-Core optimisation passes: inlining, specialisation, strictness analysis, demand analysis, simplification.
4. Core is lowered to STG (Spineless Tagless G-machine), the language-of-thunks IR.
5. STG is lowered to Cmm (C-minus-minus), a C-like portable assembly IR. Cmm explicitly represents the stack, heap, and registers and is the meeting point of all backends.
6. Cmm is then handed to a backend:
   - **NCG (Native Code Generator), default, `-fasm`.** Hand-written per-ISA backend: x86, x86_64, aarch64, ppc, riscv64 (experimental in 9.12.1). Each NCG is roughly 5,000–15,000 lines of Haskell that translates Cmm directly to assembly. Fastest compilation; best shared-library support.
   - **LLVM backend, `-fllvm`.** Emits LLVM IR, lets LLVM optimise and codegen. Slower compile (LLVM IR is verbose, LLVM optimisation expensive), but often better performance on numeric/array-heavy code.
   - **C backend, `-fviaC` (unregisterised).** For porting to platforms where neither NCG nor LLVM works.
   - **WebAssembly backend, since 9.6.** Cmm → wasm via a custom backend.
   - **JavaScript backend, since 9.6.** Experimental, ECMA-262.

GHC kept its own NCG despite having an LLVM backend because (a) compile times: NCG is dramatically faster than going through LLVM; (b) integration with the runtime: Cmm has explicit knowledge of the STG stack and heap layout that is awkward to express in LLVM IR; (c) platform independence: when LLVM regresses on a target, the NCG can pick up the slack (and vice versa).

## §3 Targets and platforms (May 2026)

Tier-1: x86_64 and aarch64 on linux/darwin/windows/freebsd. AArch64 NCG was added in 9.2 (Nov 2021) and has matured through 9.12. RISC-V NCG is experimental as of 9.12.1 (Dec 2024). PowerPC NCG is maintained but less actively. Other ISAs (LoongArch, System Z, ARM 32-bit) are LLVM-backend only.

Cross-compilation works via GHC's `--target=` flag plus a target-aware runtime. The WebAssembly backend has made cross-compilation a routine workflow (e.g., the Cabal/Hackage Wasm builds).

Linking: GHC produces position-dependent executables by default, dynamic linkage against the GHC RTS as a shared library when configured for it; static linkage produces fully self-contained binaries (commonly 5–20 MB for a real Haskell program). musl-static is supported via the alpine builds.

## §4 Runtime

The GHC RTS (runtime system) is substantial:

- A generational copying garbage collector (multi-generation, parallel-mark, optional parallel-copy, nonmoving collector since 8.10 for the oldest generation). Roughly 20,000 lines of C.
- An M:N thread scheduler (lightweight "green" threads multiplexed onto OS threads). Light-weight thread creation is sub-microsecond.
- STM (Software Transactional Memory) primitives.
- Profiling, RTS statistics, event log infrastructure.
- Foreign function interface (FFI) via `foreign import ccall`.

Hello-world on linux-x86_64 with `ghc -O2 -optl-s`: about 1.2 MB dynamically linked; about 12 MB statically linked because the RTS is large. The static binary is comparable in size to Native Image and significantly larger than Zig or Nim.

## §5 Status (May 2026)

GHC 9.12.3 RC2 dropped in Nov 2025 with the final targeted for week of 22 Dec 2025. GHC 9.14 is in development, bringing SSE/AVX SIMD support in the x86 NCG (the SIMD work started in 9.12 and continues), a major Windows toolchain refresh, and specialisation improvements. The RISC-V NCG is being polished.

Production users: GitHub (much of GitHub Enterprise tooling), Cardano (the IOG cryptocurrency stack), Facebook (Sigma anti-abuse system, now mostly retired but still informs GHC funding), Tweag's clients, plus Wire, Standard Chartered, Mercury, and a long tail of fintech and DSL users.

Performance: NCG and LLVM are within a few percent of each other for most Haskell programs; LLVM wins on tight numeric loops (typically 10–30 percent), NCG wins on compile time (5–10x faster). Both produce code that is competitive with OCaml and within 1.5–3x of equivalent Rust for typical Haskell idioms.

Known limitations: GHC's NCG does not auto-vectorise (SIMD work is just landing); aarch64 NCG had ABI bugs through early 9.10 that have been fixed; the LLVM backend's compile-time penalty makes it impractical for incremental development.

## §6 Mochi adaptation note

GHC's NCG is the strongest existence proof that a small in-house native backend is worth maintaining alongside LLVM. Patterns Mochi should consider:

- Cmm-style portable assembly IR. Mochi's IR could explicitly model its stack and heap (the way Cmm models the STG stack), making it a clean handoff point to either an in-house NCG or LLVM. This decouples backend choice from the rest of the compiler.
- The two-backend strategy. GHC has demonstrated for two decades that maintaining both an NCG (fast compile, decent codegen) and an LLVM backend (slow compile, best codegen) is sustainable. Mochi can adopt the same posture.
- Per-ISA NCG of modest size. The aarch64 NCG is roughly 8,000 lines of Haskell; a Mochi aarch64 NCG in Go would be a similar engineering scope, doable in one engineer-quarter.
- Cmm as a documented IR that other tools can consume. If MEP-42 publishes Mochi's IR as a stable text format (NIF-style or Cmm-style), the IR becomes a contract for third-party backends.
- The runtime is allowed to be large if it earns its place. GHC's RTS is 20 KLOC of C and nobody complains because it delivers M:N threading, STM, and a serious GC. Mochi can grow `runtime/vm3` similarly if the features justify it.

Affected Mochi files: `compiler3/ir/cmm.go` (a portable IR layer), `compiler3/backend_ncg_amd64/`, `compiler3/backend_ncg_aarch64/`, `compiler3/backend_llvm/`. The split makes each backend a small, focused module.

## §7 Open questions for MEP-42

1. Do we publish a stable Cmm-like IR as a contract for backends, or keep the IR private?
2. Single-backend (LLVM only) or two-backend (NCG + LLVM)?
3. Does Mochi want M:N green threading in `runtime/vm3` à la GHC RTS, or stick with OS threads?
4. How big is the runtime allowed to be? GHC's 12 MB static hello-world is acceptable to its users; is it acceptable to Mochi's?
5. SIMD: NCG can do it (GHC 9.14 will) but is significant work. Defer to LLVM backend only?