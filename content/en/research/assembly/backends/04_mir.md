---
title: "MIR as a Code-Generation Backend for Mochi"
description: "Vladimir Makarov's lightweight JIT+AOT, fast compile times, lazy basic-block versioning."
tags: ["native-codegen", "backends"]
weight: 40
date: 2026-05-18T18:04:37+07:00
---

## §1 Provenance
- Source: https://github.com/vnmakarov/mir
- Author blog: https://vnmakarov.github.io/
- Releases: https://github.com/vnmakarov/mir/releases
- IR specification: https://github.com/vnmakarov/mir/blob/master/MIR.md
- C frontend (c2m): https://github.com/vnmakarov/mir/tree/master/c2mir
- Generator API: https://github.com/vnmakarov/mir/blob/master/mir-gen.h
- Author: Vladimir Makarov (formerly Red Hat, longtime GCC register allocator maintainer and RA designer of "IRA" in GCC).
- Project was originally a Ruby JIT experiment (the "Ruby MJIT replacement" discussion thread on the ruby-dev list), now a general-purpose backend.

## §2 Mechanism
MIR is a "Medium Internal Representation": typed, three-address, but not yet SSA at the surface. The MIR generator (mir-gen) internally converts to SSA using Braun's algorithm, runs a short optimization pipeline (global value numbering, copy propagation, redundant extension elimination, dead code elimination, simple inlining of leaf functions, simple loop invariant code motion), allocates registers, and emits machine code into an executable buffer.

The MIR text format is human-readable; a compact binary format exists and reads 10x faster while being 10x smaller (per the README).

Two execution modes:
1. **Interpreter** (~6-10x slower than JITted code), useful for unit-testing IR.
2. **JIT** via `MIR_gen` calls, plus an experimental **lazy basic-block versioning** mode (recent feature) where machine code for a BB is generated on first execution, enabling polymorphic inline caches and other dynamic-language tricks.

The included **c2m** is a real C11 compiler frontend (~30k lines) targeting MIR. It bootstraps and runs the full C compiler test suite.

## §3 Target coverage (May 2026)
- x86_64 (SysV and Win64): stable.
- aarch64 (Linux and macOS): stable.
- riscv64: stable.
- ppc64le: stable. (PPC64 big-endian was removed; "the last big-endian CPU power7 became too old.")
- s390x: stable.
- No Wasm backend in the mainline tree; a Wasm prototype existed as a research branch.
- No 32-bit targets.

Object files: MIR does not emit ELF/Mach-O/COFF directly. Output is in-memory machine code suitable for JIT. For AOT, the typical recipe is to dump MIR binary, ship it, and JIT at startup, similar to a `.pyc`. There is an experimental `c2m -S` flag to emit assembly via the c2m frontend for inspection.

DWARF: not emitted. Source maps are handled by the embedding application.

## §4 Production / language adoption status (May 2026)
- Originally explored as a Ruby JIT (the "RTL MJIT" line, https://developers.redhat.com/blog/2020/01/20/mir-a-lightweight-jit-compiler-project), though Ruby ended up shipping YJIT (Cranelift-adjacent) and now RJIT.
- **c2m**: production-quality C11 compiler used as a research vehicle.
- Smaller embedded uses include scientific computing kernels and academic JIT projects.
- The repo shows continuing activity into 2025 and 2026 (Vladimir's blog has posts dated November 2025 and April 2026), but the user base remains small compared to LLVM/Cranelift/QBE.

License: MIT.

Performance: Per Makarov's own benchmarks, MIR generates code roughly 2x slower than GCC `-O2`, with compile speed competitive with Cranelift and significantly faster than LLVM at any optimization level.

## §5 Engineering cost for Mochi
- **Binary footprint**: ~500 KB to 1 MB depending on enabled targets.
- **Build complexity**: Single C library, builds with `make`. For Go-hosted Mochi this means cgo. There is no maintained Go binding; we would write a thin wrapper (~few hundred lines).
- **License**: MIT, fully compatible.
- **Cross-compilation**: Single library targets all enabled architectures.
- **Debugging**: Weak. No DWARF emission; perf/stack traces would need help.
- **Runtime startup**: Sub-millisecond engine creation; JIT compiles in microseconds per function.

## §6 Mochi adaptation note
MIR is three-address typed IR, almost a 1:1 fit for compiler3's IR (`/Users/apple/github/mochilang/mochi/compiler3/ir`). The mapping is even more direct than QBE because MIR has explicit typed registers (matching Mochi's three-bank register file in `runtime/vm3/vm.go`). The lazy basic-block versioning feature would let Mochi reuse the vm3 interpreter for cold code and JIT only hot blocks, similar to what tieredjit (`/Users/apple/github/mochilang/mochi/runtime/jit/tieredjit/`) is trying to achieve manually.

Practical Phase 1 ramp:
1. Write a `compiler3/emit/mir` package that produces MIR text.
2. Shell out to a tiny C harness binary that calls `MIR_gen` and writes a relocatable blob.
3. Or, accept cgo and call mir-gen directly from `runtime/jit/mirjit`.

The existing `runtime/jit/vm2jit/` infrastructure (cache, page allocator, lowering) is reusable; the lowering step shrinks from hand-written assembly to MIR emission.

## §7 Open questions for MEP-42
- **JIT-only or AOT?** MIR is JIT-first. If MEP-42 wants standalone native binaries, we need to add an object-file emitter (see `13_emitting_object_files.md`), which MIR does not provide.
- **cgo cost**: Pure-Go MIR re-implementation is theoretically possible (MIR is ~15k lines of C) but would be a significant maintenance burden.
- **Wasm gap**: No Wasm target. Same conclusion as QBE: pair with `wasmtime compile` for Wasm.
- **Bus factor**: Essentially one author (Vladimir Makarov). Stable enough for a Phase 1 bet but a long-term risk.
- **Code quality**: Roughly competitive with QBE, slightly behind Cranelift, well behind LLVM `-O2`. Acceptable for Phase 1.
- **Should we wait for Wasm backend?** A wasm32 MIR target would make MIR a single solution for native+web. As of May 2026 it is not on the roadmap.