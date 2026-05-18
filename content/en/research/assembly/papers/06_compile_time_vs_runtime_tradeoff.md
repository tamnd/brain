---
title: "The Compile-Time vs Runtime Trade-Off"
description: "A conceptual essay on where Mochi MEP-42 should sit on the curve from \"compile slowly, run fast\" (LLVM -O3) through \"compile and run at medium speed\" (Cranelift, B3) to \"compile instantly, run okay\" (copy-and-patch, Sparkplug). Includes a back-of-envelope budget derived from MEP-17 and MEP-23 bench numbers."
tags: ["native-codegen", "papers"]
weight: 60
date: 2026-05-18T18:14:16+07:00
---

## §1 Provenance

- The trade-off is folklore across the JIT community; quantified in many published papers and blog posts. Key data points:
  - Sparkplug: ~10x faster compile than TurboFan, code ~5-10x slower at runtime. V8 blog https://v8.dev/blog/sparkplug.
  - Liftoff: ~15-20x faster compile than TurboFan, code ~1.1-1.5x slower (Sightglass benchmarks). https://v8.dev/blog/liftoff.
  - Copy-and-Patch: ~100x faster compile than LLVM, code ~2x slower at runtime. Xu/Kjolstad PLDI 2021, https://fredrikbk.com/publications/copy-and-patch.pdf.
  - JSC tier ratios: DFG ~4x Baseline compile time; FTL ~6x DFG compile time. Pizlo, https://webkit.org/blog/10308/speculation-in-javascriptcore/.
  - Cranelift vs LLVM: ~2-3x faster compile, ~10-30% slower code. Bytecode Alliance retrospective.
  - QBE vs LLVM: ~5-10x faster compile, ~30% slower code (project's own claim: "70% of the performance of advanced compilers in 10% of the code"). https://c9x.me/compile/.
- Mochi-specific bench numbers: MEP-17 (vm2 micro-benchmarks) and MEP-23 (compiler1 codegen budgets), referenced from /Users/apple/notes/Spec/ (not enumerated here since they are internal).

## §2 Technique / contribution

The conceptual model:

```
quality of generated code (runtime perf)
  ^
  |                                          * LLVM-O3, B3, TurboFan
  |                                    * Cranelift, FTL
  |                              * QBE
  |                        * Cranelift-fast, DFG
  |                  * Liftoff, Maglev
  |             * Sparkplug, JSC Baseline
  |       * Copy-and-Patch
  |  * Interpreter (no compile)
  +-------------------------------------------------------> compile speed
```

The right-hand side is "compile instantly, run okay". The left-hand side is "compile slowly, run fast". MEP-42 is a phase-1 effort; the user explicitly said "naive". That puts us on the right-hand side.

**Three concrete choices to evaluate:**

1. **Copy-and-patch** (CPython 3.13 model): compile speed ~10 MB/s of source equivalent; code ~2x slower than LLVM -O2; ~2-3x faster than vm3 interpreter for hot loops.
2. **Per-opcode template JIT** (Sparkplug, Liftoff style): compile speed ~5 MB/s; code ~1.5-2x slower than optimized; ~3-5x faster than vm3 interpreter.
3. **chibicc-style single-pass AOT to GAS asm + shell out to cc**: compile speed limited by `cc` (~1-2 MB/s); code ~3-5x slower than optimized (but cc does some opt for us); ~3x faster than vm3 interpreter.
4. **QBE backend** (textual SSA + shell out): compile speed ~3-5 MB/s; code ~30% slower than LLVM -O2; ~5x faster than vm3 interpreter.

## §3 Where it shines, where it fails

The trade-off curve is not a single number; it depends on workload:

**Short-lived programs (CLI tools, scripts, build helpers):**
- Compile time dominates total time.
- Copy-and-patch and Sparkplug shine.
- chibicc-style AOT loses because `cc` invocation is slow.

**Long-running programs (servers, batch jobs, data pipelines):**
- Runtime dominates.
- QBE, Cranelift, or LLVM shine.
- Copy-and-patch and Sparkplug leave performance on the table.

**Mixed workloads (typical for Mochi: interactive REPL plus running production handlers):**
- A tiered strategy wins: ship a baseline JIT for cold code, an optimizing tier for hot code.
- But phase 1 of MEP-42 cannot be tiered; we pick one point.

## §4 Status (May 2026)

- Every major dynamic-language VM is tiered (V8, JSC, SpiderMonkey, BEAM, HotSpot, OpenJ9, .NET CoreCLR, Wasmtime).
- Recent research (Lesbre/Lemerre PLDI 2024) shows even baseline JITs can be 30% faster with cheap abstract interpretation.
- For static languages with AOT-only output (Go, Rust, OCaml), the trade-off is one-sided: only runtime perf matters because compile time is amortized over many runs.
- Mochi sits between these worlds. The vm3 interpreter exists, so we have a runtime tier; MEP-42 is asking us to add a compile-to-native tier.

## §5 Engineering cost for Mochi

Back-of-envelope budget from MEP-17 and MEP-23:

- vm3 interpreter executes Mochi bench programs at roughly the speed of CPython 3.13 (within 1.5x, based on MEP-17 numbers).
- Copy-and-patch JIT for CPython yielded 2-9% over interpreter. Mochi would likely see similar (let's call it 5-15%).
- A per-opcode template JIT (Sparkplug-style) would likely yield 30-50% improvement, based on V8's measured 5-15% on optimized JS interpreter that is much better than vm3.
- A QBE-via-textual-SSA emission would likely yield 2-5x improvement on numeric workloads.
- An LLVM/MLIR-based optimizing tier would yield 5-10x on hot loops.

**Compile-time budget**: MEP-23 set an informal target of "compile a 10,000-line Mochi program in under 1 second on a 2024 laptop." This rules out LLVM/MLIR for phase 1. It comfortably fits copy-and-patch and template JIT; it tightly fits QBE; it slightly exceeds chibicc-style shell-to-cc (cc on 10k LOC is closer to 2-5 seconds).

**Recommendation by workload:**
- For Mochi REPL + interactive use: copy-and-patch (fastest compile, decent run).
- For Mochi scripts: template JIT (compile once per run, decent code).
- For Mochi long-running services: QBE (slower compile, 5x better code).
- For Mochi AOT binaries we ship to users: chibicc-style + `cc -O2`. Slow compile, fastest code that doesn't require LLVM.

## §6 Mochi adaptation note

- `runtime/vm3/` is the existing baseline (no compile cost; interpreter speed).
- A phase-1 naive emitter should target the **fastest compile time** point on the curve. That argues for copy-and-patch.
- A phase-2 optimizing emitter should aim for QBE-equivalent quality.
- The vm3 interpreter remains the always-available fallback for unsupported ops or platforms.

## §7 Open questions for MEP-42

- What is the right phase-1 point on the curve? My recommendation (see `naive/00_naive_summary.md`): copy-and-patch.
- Do we want to support multiple emitters simultaneously, selected per file or per function? (Yes, eventually.)
- How do we measure "naive code is good enough"? What is the Mochi MEP-42 acceptance benchmark?
- Should we bench against CPython 3.13 (interpreter), CPython 3.13 with JIT, Go, and Rust on Mochi corpus equivalents?
- Tiering: phase 1 is single-tier. When do we add a second tier?

## §8 References

- Sparkplug numbers: https://v8.dev/blog/sparkplug.
- Liftoff numbers: https://v8.dev/blog/liftoff.
- Copy-and-Patch paper: https://fredrikbk.com/publications/copy-and-patch.pdf.
- CPython 3.13 JIT report (Brandt Bucher): https://peps.python.org/pep-0744/.
- Cranelift/Wasmtime 2023 retrospective: https://bytecodealliance.org/articles/wasmtime-and-cranelift-in-2023.
- QBE design notes: https://c9x.me/compile/.
- Pizlo on JSC speculation: https://webkit.org/blog/10308/speculation-in-javascriptcore/.
- Lesbre/Lemerre baseline-JIT-with-AI evaluation: https://inria.hal.science/hal-05407834v1/document.
- Titzer "Whose Baseline Compiler Is It Anyway?" CGO 2024: https://arxiv.org/pdf/2305.13241.