---
title: "QBE as a Naive-But-Good-Enough Backend"
description: "A 14k-LOC SSA compiler backend by Quentin Carbonneaux that targets x86-64, arm64, and riscv64 from a textual SSA IR. The \"70% of LLVM in 10% of the code\" pitch. The natural fallback if writing our own emitter feels too risky."
tags: ["native-codegen", "naive"]
weight: 80
date: 2026-05-18T18:08:55+07:00
---

## §1 Provenance

- Author: Quentin Carbonneaux (Yale), with contributions for arm64 and riscv64 by additional collaborators.
- Canonical site: https://c9x.me/compile/.
- Source mirror: https://github.com/8l/qbe.
- License: MIT.
- FOSDEM 2022 introduction by Drew DeVault (SourceHut): https://archive.fosdem.org/2022/schedule/event/lg_qbe/attachments/slides/4878/.
- Notes by Bill Mill: https://notes.billmill.org/programming/compilers/QBE.html.
- Go wrapper (cgo-free): `modernc.org/libqbe` (https://pkg.go.dev/modernc.org/libqbe), a port of QBE to Go.

## §2 Technique / contribution

QBE's value proposition: take an SSA IR in a simple textual form, run a small set of standard optimizations (constant folding, dead code elimination, basic copy propagation, simple loop-invariant code motion), generate native code via a small backend.

**Input IR shape** (from c9x.me docs):

```
function w $sum(l %array, w %n) {
@start
    %s =w copy 0
    %i =w copy 0
@loop
    %cond =w csltw %i, %n
    jnz %cond, @body, @end
@body
    %offset =l extsw %i
    %ptr =l add %array, %offset
    %ld =w loadw %ptr
    %s =w add %s, %ld
    %i =w add %i, 1
    jmp @loop
@end
    ret %s
}
```

The frontend (your language) only needs to write this textual SSA. QBE handles SSA->machine. Sizes per port (per FOSDEM 2022):
- x86_64: 2,118 LOC
- aarch64: 1,665 LOC
- riscv64: 1,458 LOC

Total backend ~14k LOC. Compile time ~2 seconds for QBE itself with -O2.

**ABI:** QBE implements the C ABI fully, so QBE-compiled functions interoperate with C libraries. This is a significant feature compared to LLVM where each frontend re-implements the ABI.

## §3 Where it shines, where it fails

**Shines:**
- Three architectures out of the box: x86-64, arm64, riscv64.
- Textual IR is easy to emit from any frontend (no API binding required).
- Full C ABI compliance, so we can link against system libraries trivially.
- Small enough to read end-to-end in a long weekend.
- Optimizes enough that output is ~70% of LLVM-O2 quality, per the project's own benchmarks.

**Fails:**
- SSA construction is on the frontend's shoulders unless you use a helper library.
- No JIT mode; QBE is AOT only. You shell out to `qbe`, then `as`, then `ld`.
- No Windows COFF backend; Linux ELF and macOS Mach-O only.
- No SIMD/vector codegen, no LTO, no PGO.
- Compile speed is slower than copy-and-patch or pure templates, but still 10-20x faster than LLVM.

## §4 Status (May 2026)

- Used in production by **Hare** language (https://harelang.org/), Drew DeVault's systems language. Hare ships QBE as its only backend.
- Used by **cproc** (Michael Forney), a small ISO C11 compiler.
- Used by **Myrddin** (Ori Bernstein) experimentally.
- riscv64 port landed in 2023; arm64 port matured through 2022-2024.
- Debian packaging discussion in 2024 (Bug#1070495) confirmed amd64+arm64+riscv64 architecture support is intentional and stable.
- The Go port `modernc.org/libqbe` lets a Go program link QBE in-process without cgo.

## §5 Engineering cost for Mochi

Two implementation paths:

**Path A: Shell out to QBE binary.**
- 1 week: install QBE in CI, vendor a known-good release.
- 2 weeks: write `compiler3/emit/qbe.go` that walks `compiler3/ir/` and emits QBE textual SSA.
- 1 week: driver that runs `qbe input.ssa | as | ld -o output` per target triple.
- 1 week: smoke tests against `compiler3/corpus/`.
- Total: ~5 weeks for one ISA, plus ~1 week each for arm64 and riscv64 (just changing the QBE target flag).

**Path B: Link `modernc.org/libqbe` in-process.**
- 1 week: integrate libqbe as a Go dependency.
- 3 weeks: emitter from compiler3 IR to QBE in-memory IR (richer API than text).
- 1 week: driver.
- Total: ~5 weeks plus zero cost per architecture beyond what QBE already supports.

Path B is preferred because Mochi can stay pure-Go-no-cgo (libqbe is a Go port, no native QBE dependency).

This is dramatically cheaper than writing our own emitter, and the code-quality floor is significantly higher (QBE has standard optimizations baked in).

## §6 Mochi adaptation note

- `compiler3/ir/` provides typed ops; we lower them to QBE SSA. Many Mochi ops have direct equivalents (`add`, `mul`, `load`, `store`, branches).
- `runtime/vm3/cell.go` defines Cell as 8 bytes; we represent Cell as QBE `l` (64-bit integer) and use type tags via bitfield ops in QBE.
- `runtime/vm3/arenas.go` becomes a set of QBE-callable runtime functions: `mochi_alloc_int(l) -> l`, `mochi_alloc_string(l, l) -> l`, etc.
- `compiler3/emit/` gets a new file `qbe_emit.go`.
- `compiler3/regalloc/` and `compiler3/opt/` become unnecessary because QBE handles both.

The QBE path also gives us **C-ABI-compatible binaries for free.** Mochi programs become dynamic libraries other languages can call into. This is a major MEP-42 win we get incidentally.

## §7 Open questions for MEP-42

- libqbe vs shelling out: do we want the runtime simplicity of libqbe (in-process) or the deploy simplicity of shelling out?
- Windows: QBE has no COFF backend. Do we ship Mochi-on-Windows via WSL2 only, or maintain a parallel chibicc-style emitter for Windows?
- Cell representation: bitfield tags or shadow-tag arrays? QBE has no tagged-pointer support, so we encode in our IR.
- GC integration: QBE has no GC hooks. Mochi's arena model is mostly GC-free, but for cycle collection we need stack-walking primitives. Possible to emit QBE that calls vm3 GC helpers at safepoints.
- Build dependency: do we vendor QBE source under `vendor/qbe/` or pull `modernc.org/libqbe` as a Go module?

## §8 References

- QBE official site: https://c9x.me/compile/.
- QBE GitHub mirror: https://github.com/8l/qbe.
- Drew DeVault's FOSDEM 2022 introduction: https://archive.fosdem.org/2022/schedule/event/lg_qbe/.
- Brian Callahan, "Let's get hands-on with QBE" (2021): https://briancallahan.net/blog/20210829.html.
- modernc.org/libqbe Go port: https://pkg.go.dev/modernc.org/libqbe.
- Hare language (production QBE consumer): https://harelang.org/.
- cproc (C frontend on QBE): https://sr.ht/~mcf/cproc/.