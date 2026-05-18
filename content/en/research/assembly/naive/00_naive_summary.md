---
title: "MEP-42 Phase 1: Naive Backend Recommendation"
description: "One-paragraph recommendation, plus reasoning, for which naive-emission technique Mochi MEP-42 should adopt as the first cut."
tags: ["native-codegen", "naive"]
weight: 0
date: 2026-05-18T18:14:16+07:00
---

## §1 Provenance

This is a synthesis document. Sources are the eight technique deep-dives in `naive/01_*.md` through `naive/08_*.md` and the six paper surveys in `papers/01_*.md` through `papers/06_*.md`. Project context: MEP-40 specification of vm3 + compiler3, the Cell/arena/three-bank-register-file design, and the project preference to stay pure-Go-no-cgo.

## §2 Recommendation

**Mochi MEP-42 phase 1 should ship a copy-and-patch JIT.** Hand-write one C function per `runtime/vm3/op.go` opcode, compile each with Clang at build time, extract the resulting machine code and relocations into a generated Go file, and at runtime memcpy + patch the stencils into an mmap'd executable region. Reserve callee-save registers (R12-R14 on x86-64) for arena base pointers and a frame pointer, in line with the vm3 register-bank design.

## §3 Reasoning

**Why copy-and-patch beats the alternatives:**

1. **Engineering cost (~8 weeks for x86-64 plus arm64)** is the lowest of the four serious candidates. Per-opcode template JIT is ~11 weeks, chibicc-style AOT is ~11 weeks for two ISAs, QBE integration is ~5 weeks but adds a runtime dependency or a Rust-style libqbe Go port.
2. **Pure-Go runtime.** Clang is a build-time dependency, not a runtime one. The shipping Mochi binary stays cgo-free. This matters because the project explicitly favors pure-Go-no-cgo.
3. **Code quality inherits from LLVM.** Each stencil was compiled by Clang -O2, so even though the runtime patcher does nothing clever, the per-op code body is as good as LLVM produces. Expected runtime perf: ~2x slower than full LLVM-O2, ~3-5x faster than vm3 interpreter for hot loops.
4. **Production validation.** CPython 3.13 shipped this exact technique in October 2024, with Brandt Bucher's port using ~1000 lines of Python build-time tooling plus ~100 lines of C runtime. The risk is well-understood.
5. **Compile time is essentially free.** Memcpy + a few stores per opcode. We get tens of MB/s of generated machine code, which means a 10,000-line Mochi program JITs in milliseconds. This satisfies MEP-23's compile-time budget by an order of magnitude.
6. **Static typing is a free win.** CPython had to fit untyped values into LLVM. Mochi has typed bytecode in compiler3 already, so we can ship typed stencils (e.g., `add_int_int` distinct from `add_float_float`) and eliminate runtime type tests that CPython must perform.
7. **Path to optimization.** Once copy-and-patch ships, the natural phase-2 upgrade is a Liftoff-style virtual-stack overlay that does cross-op register allocation. The stencils stay the same; we just stop spilling between them. This is a smooth growth path, not a rewrite.

**Why not the alternatives:**

- **Sparkplug-style per-op template JIT** (`06_template_jit_per_opcode.md`): requires us to hand-write all the assembly, including ABI prologues, slow paths, and per-ISA encodings. Copy-and-patch lets Clang generate this for us. Sparkplug is the right phase-2 choice if we want IC slots.
- **chibicc-style single-pass AOT** (`07_chibicc_walkthrough.md`): excellent for AOT-only deployment, but slow at compile time (shells out to `cc`) and produces a worse JIT story. Best reserved for `mochi build` AOT mode, layered on top of the JIT.
- **QBE backend** (`08_qbe_for_naive_emit.md`): smaller engineering cost than chibicc but adds a runtime dependency. The libqbe Go port mitigates this. Strong runner-up; the right phase-2 choice if we want better long-running-server perf.
- **JSC Baseline JIT** (`02_jsc_baseline_jit.md`): too much engineering for phase 1 (inline-cache machinery dominates). Defer to phase 3.
- **MLIR dialects** (`papers/03_mlir_dialects_2026.md`): ~18 months of work and a C++ build dependency. Phase 5+.

## §4 Phased plan

- **Phase 1 (MEP-42, 8-10 weeks):** Copy-and-patch JIT, x86-64 Linux + macOS, arm64 macOS. AOT mode reuses the same stencils written to ELF/Mach-O via a small linker driver.
- **Phase 2 (MEP-43, 6-8 weeks):** Add Liftoff-style virtual-stack cross-op register allocation. Same stencil set, smarter glue.
- **Phase 3 (MEP-44, 8-12 weeks):** Add tier-2 optimizing backend via QBE (or roll our own).
- **Phase 4 (MEP-45 or later):** Inline caches for first-class function dispatch and dynamic-dispatch sites.

## §5 Engineering cost summary

| Approach | Phase 1 cost | Phase 2 cost | Runtime perf vs vm3 |
|---|---|---|---|
| Copy-and-patch (recommended) | 8 wk | n/a | 3-5x |
| Per-op template JIT | 11 wk | +6 wk arm64 | 3-5x |
| chibicc-style AOT | 11 wk | +regalloc | 3x |
| QBE via libqbe | 5 wk | n/a | 5x |
| MLIR/LLVM | 78+ wk | n/a | 10x |

## §6 Mochi adaptation note

Map to existing Mochi code:

- `runtime/vm3/op.go`: source for the opcode list. Each Op gets a C stencil function.
- `runtime/vm3/cell.go`: the 8-byte Cell handle is what stencils manipulate.
- `runtime/vm3/arenas.go`: arena base pointers occupy reserved registers; stencils load via known offsets.
- `runtime/vm3/frame.go`: the three-bank register file dictates the stencil register convention.
- `compiler3/emit/`: existing package, add the patcher here.
- `compiler3/stencils/` (new): generated Go file with stencil byte arrays and hole tables.
- `compiler3/ir/`: source of typed IR ops that drive stencil selection.

## §7 Open risks

1. **ABI drift.** Clang's stencil output may not match what our runtime patcher expects across Clang versions. Mitigation: pin a Clang version in CI; differential-test against the vm3 interpreter on every change.
2. **macOS arm64 JIT entitlement.** Requires a signed binary with the proper entitlement plist. We need to document this and ship a signed Mochi binary.
3. **Code-cache memory pressure.** Stencils are larger than handwritten templates. Cap the executable region and fall back to vm3 interpretation when full.
4. **Cross-compilation testing.** Stencils are platform-specific. CI must build and test on every target.

## §8 References

- All `naive/0*.md` and `papers/0*.md` files in this directory.
- Xu/Kjolstad copy-and-patch PDF: https://fredrikbk.com/publications/copy-and-patch.pdf.
- PEP 744: https://peps.python.org/pep-0744/.
- LWN coverage of the CPython JIT: https://lwn.net/Articles/977855/.
- Mochi MEP-40 spec (vm3 + compiler3): /Users/apple/notes/Spec/MEP-40-vm3-compiler3.md (internal).