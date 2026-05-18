---
title: "CakeML and the Verified-JIT Line"
description: "The bootstrapping verified ML compiler, its 2024 PLDI agenda, and the FM-JIT verified-JIT effort that builds on it."
tags: ["memory-safety", "verification"]
weight: 70
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Kumar, Myreen, Norrish, Owens. **"CakeML: a verified implementation of ML"**, POPL 2014. https://dl.acm.org/doi/10.1145/2535838.2535841
- Tan, Myreen, Kumar, et al. **"A New Verified Compiler Backend for CakeML"**, ICFP 2016. https://dl.acm.org/doi/10.1145/2951913.2951924
- CakeML home: https://cakeml.org/
- Myreen, PLDI 2024 keynote, **"Much Still to Do in Compiler Verification (A Perspective from the CakeML Project)"**. https://pldi24.sigplan.org/details/pldi-2024-papers/100/
- **Brack: A Verified Compiler for Scheme via CakeML** by Lasnier, Yallop, Myreen, CPP 2026. https://popl26.sigplan.org/details/CPP-2026-papers/15/
- **FM-JIT** (Barrière et al.), **"Formally Verified Native Code Generation in an Effectful JIT"**, POPL 2023. https://aurele-barriere.github.io/papers/fmjit.pdf (uses CompCert backend rather than CakeML, but is the canonical reference for verified JIT methodology).
- 2024 CakeML-adjacent papers: "End-to-end verification for subgraph solving" (AAAI 2024), "Verified Inlining and Specialisation for PureCake" (ESOP 2024), "Formally Certified Approximate Model Counting" (CAV 2024).

## §2 Claim or Mechanism
CakeML is an **end-to-end verified compiler for an ML-like functional language**, mechanised in HOL4. The compiler is "bootstrapped inside the logic": CakeML compiles a verified version of itself. The compiler backend takes the untyped AST through 8 intermediate languages to machine code on 6 target architectures (x86-64, ARMv6, ARMv7, ARMv8, MIPS-64, RISC-V). Every translation is proved to preserve observational behaviour, *including* memory-management correctness — CakeML ships with a *verified garbage collector*.

The verification covers:
- A verified parser.
- A verified type-checker.
- A verified front-end optimiser.
- A verified bytecode compiler.
- A verified register allocator and code generator.
- A verified copying / generational GC.
- Verified handling of out-of-memory: programs that run out of memory must report so, not silently misbehave.

For JIT: **FM-JIT** (Barrière et al., POPL 2023) is the leading verified-JIT artifact in 2024-2026, though it uses CompCert rather than CakeML as the verified backend. The methodology is to factor the JIT into (a) pure, Coq-verified components (the IR transformations, the call-into-CompCert) and (b) impure primitives (memory permission changes, native-code installation, instruction-cache flushing), where the impure primitives are *specified* in Coq and *implemented* outside the proof.

## §3 Scope and Limits
**Covered.** CakeML verifies the *whole* path from ML source to machine code for an ML-like functional language. FM-JIT verifies a *model* JIT that does on-demand native code generation with backtracking deoptimisation. Both produce executable artifacts.

**Not covered.** CakeML's source language is functional, not imperative; it has no equivalent of mutable arena handles. CakeML's GC is verified but is a copying GC, not a mark-sweep, so the verification techniques do not transfer mechanically to vm3's planned mark-sweep. FM-JIT is a model JIT, much simpler than V8 / SpiderMonkey / vm3jit; production JIT features (inline caching, polymorphic dispatch, OSR, deoptimisation under speculative inlining) are largely not yet verified.

Production performance: CakeML's generated code is competitive with hand-written ML, but is not a JIT. FM-JIT prototypes do not yet match production JIT performance.

## §4 May 2026 Status
CakeML remains the *only* mainstream bootstrapped verified compiler. Active development continues at Chalmers / Tallinn / CMU. The PLDI 2024 keynote spelled out the open problems: (1) verified memory management (mostly done for copying GC, less so for mark-sweep / concurrent GC), (2) compiler verification *in verified settings* (i.e., using verified compilers from inside other verified tools), (3) ruling out unwanted OOM errors. The CPP 2026 Brack paper extends CakeML to Scheme with first-class continuations and recursive bindings — a sign that the CakeML backend is mature enough to be a target for new verified frontends.

FM-JIT is the active reference for *verified JIT compilation* through 2025-2026; subsequent work has built on its impure-primitives factoring approach but not yet produced a production-grade verified JIT.

## §5 Cost
CakeML is a roughly **two-decade, multi-PhD-thesis effort** with a code base of hundreds of thousands of lines of HOL4 proofs. This is the multi-person-decade scale typical of foundational compiler verification. FM-JIT is more recent and smaller in scope (a focused POPL 2023 effort) but still significantly more than a typical PhD chapter.

Per-frontend cost (e.g., adding a new source language that targets the CakeML backend) is on the order of person-years — much cheaper than reimplementing the backend, which is exactly the value proposition.

## §6 Mochi Adaptation Note
CakeML is the right *aspiration* for "what end-to-end verification of Mochi vm3 would look like, if anyone ever did it". For MEP-41 today, it is *not* on the roadmap, but the methodological lessons matter:

- The CakeML stance on out-of-memory is exactly the right model for Mochi: a memory-safety guarantee should cover OOM (i.e., OOM is reported, not silently corrupted). MEP-41 should commit to this explicitly: the runtime must either succeed an allocation, return a defined error, or terminate; it must not return a partially-initialised Cell.
- The FM-JIT factoring (verified pure components + specified-but-unverified impure primitives) is *precisely* the right way to document vm3jit's safety story. Even without verification, MEP-41 can list the unverified primitives (mmap with PROT_EXEC, code installation, i-cache flush) and call them out as the TCB of the JIT. This brings the documentation to FM-JIT-paper-level rigour without doing the proofs.
- CakeML's verified GC is a copying GC. Mochi's mark-sweep is a different design and the proof would need to be redone; the most recent relevant work is IrisFit (TOPLAS 2025; see file 09) which handles tracing GC in Iris. MEP-41 should *not* claim mark-sweep correctness as a MEP-41 deliverable, but should note that the literature has now caught up to mark-sweep-style verification.
- A future Mochi MEP could explore using FM-JIT methodology for vm3jit. That would be a research-grade effort, not a productisation effort. MEP-41 should keep the option open in prose but not commit to it.

## §7 Open Questions for MEP-41
1. Should MEP-41 explicitly enumerate the JIT's unverified-primitives TCB in FM-JIT style? Three or four bullets would suffice.
2. Should the OOM-safety guarantee be elevated to a top-level MEP-41 commitment (in CakeML's spirit)?
3. Does Mochi want to track the IrisFit / CakeML mark-sweep verification literature as future-work pointers, signalling intent to revisit the GC story in a later MEP?
4. The Brack Scheme-via-CakeML 2026 paper demonstrates a viable "small frontend over a big verified backend" pattern. If Mochi ever pursued a verified subset, the same architectural move (define Mochi-Verified as a subset, target a verified backend) would be the cleanest path. Worth flagging.