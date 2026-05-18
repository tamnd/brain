---
title: "JavaScriptCore Baseline JIT"
description: "Apple WebKit's original template-style baseline compiler, the longest-running production baseline JIT for a dynamic language, and the design template for every modern four-tier VM."
tags: ["native-codegen", "naive"]
weight: 20
date: 2026-05-18T18:03:33+07:00
---

## §1 Provenance

- Project: JavaScriptCore (JSC), the JavaScript engine in Apple WebKit/Safari.
- Architect-of-record: Filip Pizlo (Apple), with contributions from Gavin Barraclough, Geoffrey Garen, Saam Barati, and others.
- Origin: ~2008 (the "SquirrelFish Extreme" / "Nitro" announcement), continuously evolved since.
- Authoritative writeups:
  - Filip Pizlo, "Speculation in JavaScriptCore" (https://webkit.org/blog/10308/speculation-in-javascriptcore/), 2020.
  - Pizlo DLS/VMIL 2017 slides, "The JavaScriptCore Virtual Machine" (http://www.filpizlo.com/slides/pizlo-dls2017-vmil2017-jscvm-slides.pdf).
  - Saelo (Samuel Gross), "JavaScriptCore Internals Part II: The LLInt and Baseline JIT" (https://zon8.re/posts/jsc-internals-part2-the-llint-and-baseline-jit/).
  - WebKit docs, "JavaScriptCore Deep Dive" (https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html).
- Source code: WebKit tree under `Source/JavaScriptCore/jit/`.

## §2 Technique / contribution

JSC pioneered the four-tier strategy that essentially every dynamic-language VM has since copied:

1. **LLInt** (Low Level Interpreter, 2012, Pizlo): a bytecode interpreter written in "offlineasm", a portable assembly that compiles to x86-64, arm64, riscv, or plain C. Each handler is hand-tuned to share a JIT calling convention with the next tier.
2. **Baseline JIT**: triggered after ~100 statement executions or ~6 function calls. Template-emits one canned native sequence per bytecode op. No register allocator. Same calling convention as LLInt, so cross-tier OSR is free.
3. **DFG JIT** (Data Flow Graph): triggered around 60 invocations or 1000 loop iterations. Builds a CPS-style IR, runs speculation, does register allocation, dead code elimination, sparse conditional constant prop. Speculates on profiled types and bails out via OSR if wrong.
4. **FTL JIT** (Faster Than Light): only for the hottest code (thousands of invocations). Originally LLVM-backed (2014), replaced in 2016 by **B3** (Bare Bones Backend), an internal compiler that runs about 5x faster than LLVM while producing comparable code.

The **Baseline JIT** specifically is the focus here. Per-bytecode it emits a short native sequence with:
- Inline-cache (IC) slots: small patchable regions of code that start as a slow-path call and get rewritten to fast paths on first hit.
- A profiling header that captures observed types, written into a `ValueProfile` struct.
- A fixed register convention shared with LLInt so on-stack frames are inter-tier compatible.

Pizlo quantifies the cost ratios: DFG takes ~4x the time of Baseline, FTL takes ~6x the time of DFG.

## §3 Where it shines, where it fails

**Shines:**
- Eliminates the dispatch overhead of LLInt (~75% of LLInt's runtime for hot ops, per WebKit measurements).
- IC slots are the secret weapon: they make polymorphic property access nearly as fast as static dispatch.
- Profile collection costs almost nothing because it is written inline into the emitted code.
- Tier-up cost is bounded: a single Baseline compile is roughly as expensive as running the function once in LLInt.

**Fails:**
- Generates large code: each IC slot is allocated even when unused.
- No register lifetime tracking, so values are constantly bounced through the frame.
- Without DFG above it, Baseline is only ~2x faster than LLInt. The four-tier story is what unlocks the real wins.

## §4 Status (May 2026)

- Still the foundation of Safari and every iOS/macOS JS engine.
- Pizlo's blog and the WebKit docs are still the canonical writeups; no replacement architecture has emerged.
- The four-tier pattern was copied wholesale by V8 (LLInt-equivalent Ignition, Baseline = Sparkplug, mid-tier = Maglev, top tier = TurboFan) and partially by SpiderMonkey (interpreter + Baseline + WarpMonkey).
- B3 (FTL's backend) inspired Cranelift's split of vcode/MachInst from optimization passes.

## §5 Engineering cost for Mochi

JSC's Baseline JIT is significantly more work than Sparkplug, because:

- Inline caches require runtime patching infrastructure (mprotect, instruction cache flush, atomic patch site rewriting).
- The profiling instrumentation needs per-call-site `ValueProfile` records.
- The IR-free template emitter is the easy part; the IC machinery is the hard part.

Estimated cost for a JSC-style Mochi baseline:
- 4 weeks: assembler + per-op template skeletons (x86-64 only).
- 4 weeks: inline-cache framework (patchable stubs, miss handlers, repatch logic).
- 3 weeks: value-profile collection and tier-up trigger plumbing.
- 4 weeks per additional ISA.

This is too expensive for MEP-42 phase 1. Better strategy: ship Sparkplug-style first (no IC), add IC later in MEP-43 or MEP-44.

## §6 Mochi adaptation note

- `runtime/vm3/op.go`: the per-op handlers in Mochi already encode the slow-path logic. We can reuse them as IC miss handlers.
- `runtime/vm3/cell.go`: Mochi cells are statically typed already (compiler3 has type info), so we do not need the full type-feedback IC machinery JSC uses. Most Mochi sites are monomorphic at compile time.
- `compiler3/ir/`: provides the static type info that lets us skip JSC-style speculation entirely. This is a major simplification.
- `runtime/vm3/memory.go`: for patchable code regions we need an executable arena distinct from the typed-Cell arenas.

The big takeaway for Mochi: because Mochi is statically typed, we get the win of JSC speculation "for free" without the OSR/deopt machinery. That means Mochi can skip the DFG-tier entirely and go straight from Baseline to a properly optimizing tier when warranted.

## §7 Open questions for MEP-42

- Do we want inline caches at all? Static typing may make them unnecessary, except for first-class function dispatch.
- What is the IC granularity? Per call site? Per method lookup? Per dispatch table?
- Code cache management: how do we reclaim baseline code when a function is recompiled at a higher tier?
- Should Mochi adopt JSC's offlineasm-style portable interpreter, or stay in pure Go for the vm3 interpreter?
- Profiling overhead: how much can we afford to bake into emitted code?

## §8 References

- WebKit Blog, "Speculation in JavaScriptCore" (https://webkit.org/blog/10308/speculation-in-javascriptcore/).
- WebKit Blog, "Introducing the WebKit FTL JIT" (https://webkit.org/blog/3362/introducing-the-webkit-ftl-jit/).
- Pizlo, DLS/VMIL 2017 slides (http://www.filpizlo.com/slides/pizlo-dls2017-vmil2017-jscvm-slides.pdf).
- Saelo, "JSC Internals Part II" (https://zon8.re/posts/jsc-internals-part2-the-llint-and-baseline-jit/).
- WebKit Deep Dive, "JavaScriptCore" (https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html).