---
title: "Cranelift as a Code-Generation Backend for Mochi"
description: "Bytecode Alliance's Rust-native SSA backend, ISLE-driven, ~10x faster compile than LLVM."
tags: ["native-codegen", "backends"]
weight: 20
date: 2026-05-18T18:04:37+07:00
---

## §1 Provenance
- Project home: https://cranelift.dev/
- Source: in the Wasmtime monorepo, https://github.com/bytecodealliance/wasmtime/tree/main/cranelift
- ISLE language reference: https://github.com/bytecodealliance/wasmtime/blob/main/cranelift/isle/docs/language-reference.md
- 2022 roadmap RFC (most recent formal): https://github.com/bytecodealliance/rfcs/blob/main/accepted/cranelift-roadmap-2022.md
- ISLE RFC: https://github.com/bytecodealliance/rfcs/blob/main/accepted/cranelift-isel-isle-peepmatic.md
- E-graph midend RFC: https://github.com/bytecodealliance/rfcs/blob/main/accepted/cranelift-egraph.md
- Wikipedia summary: https://en.wikipedia.org/wiki/Cranelift
- "Cranelift Progress in 2022": https://bytecodealliance.org/articles/cranelift-progress-2022
- Bjorn3 progress reports (cg_clif): https://bjorn3.github.io/

## §2 Mechanism
Cranelift consumes CLIF, a target-independent SSA IR with block parameters (no phi nodes) and explicit memory operations. The pipeline is: legalization, an optional e-graph-based midend (constant folding, redundant load elimination, GVN, simple peepholes, enabled by default since 2023), instruction selection through ISLE (a Lisp-shaped term-rewriting DSL that compiles to Rust match trees), the regalloc2 register allocator (adapted from IonMonkey, https://github.com/bytecodealliance/regalloc2), prologue/epilogue insertion, and direct emission to a `MachBuffer` of raw bytes plus relocations. Output is in-memory machine code suitable for JIT or for being wrapped in an object file via the `cranelift-object` crate.

Cranelift was designed for fast compile times, not for the best possible code. There is no inlining, no loop vectorization, no scheduling beyond simple peepholes. Generated code is typically 1.5-2x slower than LLVM `-O2` but compiles 5-10x faster.

## §3 Target coverage (May 2026)
- x86_64 (SysV and Win64): production-quality, the primary Wasmtime target.
- AArch64 (Linux, macOS, Windows): production-quality.
- RISC-V RV64GC: production-quality since 2023.
- IBM s390x (z/Architecture): production-quality (IBM-funded).
- 32-bit Arm: not supported; not on the roadmap.
- WebAssembly: not a Cranelift target. Cranelift consumes Wasm via Wasmtime and emits native code.

Object formats: ELF and Mach-O via `cranelift-object`; PE/COFF support exists but is less battle-tested.

DWARF: line-table support yes; type info partial. cg_clif emits enough for `gdb` to do source-level stepping.

## §4 Production / language adoption status (May 2026)
- **Wasmtime** (https://wasmtime.dev): primary user, ships major releases roughly monthly. Wasmtime v35 (per https://bytecodealliance.org/articles) added AArch64 support to Winch, the single-pass tier-0 baseline compiler complementary to Cranelift.
- **Firefox SpiderMonkey**: uses Cranelift for the Wasm baseline tier on some platforms.
- **rustc_codegen_cranelift (cg_clif)**: alternative rustc backend (https://github.com/rust-lang/rustc_codegen_cranelift). 2025 was a milestone year: exception/unwind support landed, inline asm became stable, AArch64 macOS shipped as a rustup component, the formal "production-ready cranelift backend" Rust Project Goal targets full readiness on Linux/macOS x86_64+aarch64 (https://rust-lang.github.io/rust-project-goals/2025h2/production-ready-cranelift.html). Performance: roughly 20% reduction in codegen time vs LLVM, 5% speedup on clean builds, plus 10-50% extra from enabling lld.
- **Lucet**, **Fastly Compute@Edge**: heavy production users for Wasm AOT.

Active maintainership is healthy, Bytecode Alliance funding, ~weekly meetings. License is Apache 2.0 with LLVM Exceptions.

## §5 Engineering cost for Mochi
- **Binary footprint**: A `cranelift-codegen + cranelift-frontend + cranelift-jit` static blob is roughly 15-25 MB, an order of magnitude smaller than LLVM.
- **Build complexity**: Cranelift is pure Rust with no C dependencies. The hard problem for a Go-hosted Mochi is the cgo bridge: there is no maintained Go binding. Options are (a) write a thin C++ wrapper over the `cranelift-jit` C API and FFI to it via cgo, (b) run Cranelift in a child process and exchange CLIF text, or (c) link a Rust shared library (`staticlib`) and call it via cgo. None of these are turnkey.
- **License**: Apache 2.0 with LLVM Exceptions.
- **Cross-compilation**: Excellent: a single Cranelift build can target every supported triple.
- **Debugging**: Adequate. Line tables work; complex variable inspection is limited.
- **Runtime startup**: Sub-millisecond engine setup; JIT compiles a function in microseconds to low-millisecond range.

## §6 Mochi adaptation note
Cranelift's CLIF is almost a direct match for the compiler3 IR shape (`/Users/apple/github/mochilang/mochi/compiler3/ir`): SSA values, basic blocks with block parameters, explicit memory ops. The compiler3 register allocator under `/Users/apple/github/mochilang/mochi/compiler3/regalloc` becomes obsolete (regalloc2 is better than anything Mochi will write); the vm3 op table in `/Users/apple/github/mochilang/mochi/runtime/vm3/op.go` becomes a set of CLIF idioms. The integration question is purely the Go-to-Rust bridge, not the IR mapping.

Mochi's existing `runtime/jit/vm2jit` (`/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/lower.go`) uses twitchyliquid64/golang-asm to handcraft amd64+arm64; Cranelift would replace that lower step with a higher-level lower-then-let-Cranelift-finish flow, at the cost of cgo.

## §7 Open questions for MEP-42
- **Is cgo acceptable for Mochi?** If no, Cranelift is essentially out unless we run it as a subprocess.
- **Subprocess vs in-process?** A subprocess design (Mochi emits `.clif`, invokes `wasmtime compile --target=...` or a custom `mochi-cranelift` worker) avoids cgo at the cost of process-spawn latency.
- **Rust toolchain on every Mochi build host?** Even a `staticlib` requires `cargo` at build time. This is a step change in Mochi's build prerequisites.
- **Should Phase 1 instead go via Wasm + Wasmtime AOT?** Cranelift's biggest user is Wasmtime; a Mochi-to-Wasm path (see `12_wasmtime_aot.md`) gives us Cranelift's codegen quality for free, without ever touching the Cranelift API directly.
- **Code quality gap vs LLVM**: Cranelift will be 1.5-2x slower than LLVM `-O2` on tight loops. Is that acceptable for Phase 1? Almost certainly yes, given Mochi's current baseline is the vm3 interpreter.