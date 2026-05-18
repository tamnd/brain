---
title: "QBE as a Code-Generation Backend for Mochi"
description: "Quentin Carbonneaux's deliberately tiny SSA backend, \"70% of LLVM in 10% of the code.\""
tags: ["native-codegen", "backends"]
weight: 30
date: 2026-05-18T18:04:37+07:00
---

## §1 Provenance
- Project home: https://c9x.me/compile/
- Source: https://c9x.me/git/qbe.git (mirror: https://github.com/8l/qbe)
- Releases page: https://c9x.me/compile/release/ (current stable: qbe-1.2.tar.xz)
- Lobsters thread for QBE 1.0: https://lobste.rs/s/yqakzf/qbe_1_0
- Mailing list: ~mpu/qbe@lists.sr.ht (subscribe via sourcehut)
- Personal branch with extra patches: https://git.sr.ht/~mcf/qbe
- NLnet ARM32 grant (2025-10 start): https://nlnet.nl/project/QBE-32-bit-ARM-support/
- Author: Quentin Carbonneaux (assistant professor at Yale, prior PhD work at Yale on cost-bounded program analysis).

## §1.5 Self-description (from project home)
> "QBE aims to provide 70% of the performance of industrial optimizing compilers in 10% of the code."

The C codebase is kept "hobby-scale and pleasant to hack on" (https://c9x.me/compile/).

## §2 Mechanism
QBE consumes a small text IR called the QBE IL. The IL is SSA, has block labels, basic types (`w`, `l`, `s`, `d`, plus aggregates), and a tiny set of instructions covering arithmetic, memory, compare-and-branch, and calls with full C ABI compliance. The compiler reads `.ssa` text, runs a handful of passes (SSA construction, sparse conditional constant propagation, copy elimination, simple GVN, dead-code elimination, register allocation by a graph-coloring allocator from Briggs/Cooper-style literature, peephole), then emits target-specific GAS-style assembly to stdout. The user invokes `as` and `ld` (or `cc`) to finish.

There is no JIT API. QBE is strictly a textual frontend-to-asm pipe. Total source is ~12k lines of C in the official tarball.

## §3 Target coverage (May 2026)
- amd64 on Linux, macOS, OpenBSD, FreeBSD: stable.
- arm64 on Linux, macOS: stable.
- riscv64 (RV64GC) on Linux: stable, added 2022-2023.
- ARM32: in active development under NLnet funding (2025-10 start, https://nlnet.nl/project/QBE-32-bit-ARM-support/), driven by the Hare ecosystem needing it for ARMv7 hardware.
- No Wasm, no Windows, no PowerPC, no MIPS. No s390x.

Object format: QBE emits text assembly. The system `as` produces ELF on Linux/BSD and Mach-O on macOS. PE/COFF is not natively supported.

DWARF: basic line tables emitted as `.loc` directives that GAS handles; no full DI tree.

## §4 Production / language adoption status (May 2026)
- **Hare** (https://harelang.org): primary production user. Drew DeVault's systems language uses QBE as its only backend and has driven much of QBE's recent feature work, including the upcoming ARM32 port.
- **cproc** (https://sr.ht/~mcf/cproc): a C11 compiler that targets QBE; useful as a small, hackable C frontend.
- **Lacc** (https://github.com/larmel/lacc): another C compiler with a QBE backend option.
- **bf-q**, **scc**: various small experiments.

Maintainership is essentially Quentin Carbonneaux plus a small group of patch contributors via sourcehut. Releases are infrequent but the mob branch is reasonably active.

Performance: per Carbonneaux's own claim (validated by Hare benchmarks), generated code runs at roughly 70% of LLVM `-O2` speed on integer-heavy code; QBE typically loses on tight FP loops and on code that benefits from vectorization (QBE has no auto-vectorizer).

## §5 Engineering cost for Mochi
- **Binary footprint**: The qbe binary is ~500 KB stripped. No runtime library is required.
- **Build complexity**: Trivial. `make && make install`. No dependencies beyond a C99 compiler. For Mochi, the easiest integration is: shell out to `qbe` with a textual `.ssa` input, capture assembly, pipe through `as` and `ld`. This is the same model that Hare itself uses.
- **License**: MIT.
- **Cross-compilation**: Built-in via `qbe -t amd64_sysv|amd64_apple|arm64|arm64_apple|rv64`. One QBE binary handles all targets.
- **Debugging**: Minimal. Adequate for stack traces; not enough for source-level debugging without extra DWARF emission.
- **Runtime startup**: None. QBE is invoked at build time only.

## §6 Mochi adaptation note
QBE IL is a near-perfect target for compiler3's existing IR (`/Users/apple/github/mochilang/mochi/compiler3/ir`). The mapping:
- Mochi typed Cells (8-byte handles, see `/Users/apple/github/mochilang/mochi/runtime/vm3/cell.go`) become QBE `l` (64-bit) values.
- The three-bank register file in `runtime/vm3/vm.go` becomes SSA temporaries.
- Each vm3 op in `runtime/vm3/op.go` becomes a small QBE snippet, often 2-5 QBE instructions.
- A new `compiler3/emit/qbe` package would be ~1000-2000 lines of Go, emitting text and invoking `qbe`+`as`+`ld` as a build step.

This is the cleanest "Phase 1 naive native emitter" candidate: it preserves Mochi's pure-Go ethos at build time (QBE is a subprocess), it covers x86_64, arm64, riscv64 (matching MEP-42's three priority targets), and total integration cost is one weekend of work.

## §7 Open questions for MEP-42
- **No Wasm target**: If MEP-42 wants Wasm as a first-class peer to x86_64/arm64/riscv64, QBE alone is insufficient. Pair with `wasmtime compile` (see `12_wasmtime_aot.md`).
- **No Windows native**: Mochi-on-Windows-x86_64 would need a different backend, or a WSL/MinGW workaround.
- **70% performance ceiling**: If MEP-42 Phase 2 targets parity with optimized C/Go output, QBE caps out; a Phase 2 LLVM/MLIR path becomes necessary.
- **Bus factor**: QBE is essentially one person. Mochi depending on it long-term means accepting that risk or being prepared to fork.
- **DWARF gap**: Native source-level debugging will need extra work (probably emitting our own `.debug_line`).
- **Will the ARM32 work land on schedule?** NLnet started funding October 2025; ARMv7 hosts would unlock Mochi-on-Raspberry-Pi-Zero if it does.