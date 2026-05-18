---
title: "PLDI 2024 and 2025: Relevant Code-Generation Papers"
description: "Recent work from the flagship PL conference on lightweight backends, baseline JIT design, superoptimization for stack bytecode, and library composition that sidesteps heavyweight compilation."
tags: ["native-codegen", "papers"]
weight: 10
date: 2026-05-18T18:09:59+07:00
---

## §1 Provenance

- PLDI 2024: 45th ACM SIGPLAN Conference on Programming Language Design and Implementation, Copenhagen, Denmark, June 24-28 2024. Proceedings in PACMPL vol 8, no PLDI: https://dl.acm.org/toc/pacmpl/2024/8/PLDI.
- PLDI 2025: 46th edition, Seoul, South Korea, June 16-20 2025. Proceedings in PACMPL vol 9, no PLDI: https://dl.acm.org/toc/pacmpl/2025/9/PLDI.
- Conference pages: https://pldi24.sigplan.org/ and https://pldi25.sigplan.org/.

## §2 Technique / contribution

Summarized below are six papers from PLDI 2024-2025 most relevant to MEP-42's "naive native codegen" charter.

### 1. Lesbre & Lemerre, "Compiling with Abstract Interpretation" (PLDI 2024)
- Authors: Dorian Lesbre, Matthieu Lemerre (CEA LIST, France).
- DOI: 10.1145/3656447 (PACMPL vol 8, PLDI).
- Idea: Run an abstract interpreter at compile time over the bytecode being compiled, capturing constant facts, value ranges, and register-availability invariants. Use these facts to specialize the emitted machine code without building a full optimizing IR.
- Result: Reduces emitted-code size by 12% (geomean), increases execution speed up to 30%, without harming compile-time overhead vs a direct template translator.
- Follow-up "Are Abstract-interpreter Baseline JITs Worth it?" (HAL preprint at https://inria.hal.science/hal-05407834v1/document) implemented several baseline-JIT variants for the Pharo Smalltalk VM and confirmed the technique pays off in a production-style setting.
- Mochi relevance: a "naive baseline + tiny abstract interpreter" combo could give us Mochi-quality codegen at very low compile-time cost.

### 2. SuperStack: Albert et al., "Superoptimization of Stack-Bytecode via Greedy, Constraint-Based, and SAT Techniques" (PLDI 2024)
- Authors: Elvira Albert, Pablo Gordillo, et al. (Complutense University of Madrid).
- ACM DOI: 10.1145/3656435 (PACMPL vol 8, PLDI).
- Idea: Superoptimize stack-bytecode (WebAssembly, EVM) by combining a greedy presolver, constraint-based reasoning, and SAT search. The greedy phase tightens the bound on the length of any equivalent optimal sequence; constraint and SAT phases search within that bound.
- Result: ~4x reduction in optimization time on 500,000 sample sequences, with greatly increased optimization gains vs prior superoptimizers.
- Mochi relevance: Mochi vm3 bytecode is stack-tagged in places. SuperStack's algorithm could mine canonical replacements for common Mochi op sequences as a build-time peephole pass. Cheap to integrate.

### 3. Stratton et al., "Optimistic Stack Allocation and Dynamic Heapification for Managed Runtimes" (PLDI 2024)
- Authors: Aditya Anand, et al. (IIT Madras).
- Idea: Combine static escape analysis with runtime "heapification" hooks. Objects start on the stack; if they would escape via a feature like a captured closure, the runtime moves them to the heap dynamically.
- Result: Demonstrated on a managed runtime; non-trivial speedup with bounded runtime overhead.
- Mochi relevance: Mochi's arena allocator could benefit from this: stack-promote where possible, fall back to arena allocation when escape is dynamic. Phase 2 or 3 of MEP-42.

### 4. Bansal, Sharlet, Ragan-Kelley, Amarasinghe, "Lightweight and Locality-Aware Composition of Black-Box Subroutines" (PLDI 2025)
- DOI: 10.1145/3729292.
- Preprint: https://dspace.mit.edu/bitstream/handle/1721.1/164683/3729292.pdf.
- System name: Fern.
- Idea: Compose library subroutines (think: dense linear algebra kernels) without a full heavyweight optimizer. Annotate subroutines with data-production/data-consumption patterns; Fern fuses across boundaries using only those annotations.
- Result: Matches manually-fused hand-tuned libraries (Intel OneDNN, others) across multiple domains.
- Mochi relevance: a path to "fast Mochi numerics" without committing to LLVM or MLIR. Annotate `runtime/vm3` numeric kernels with Fern-style metadata; let a small Mochi-side composer fuse across boundaries.

### 5. Type-Constrained Code Generation with Language Models (PLDI 2025)
- Site: https://pldi25.sigplan.org/details/pldi-2025-papers/25/.
- Idea: Use LLMs to generate code constrained by static type information. Less relevant to MEP-42's "naive emitter" charter, but worth noting because it changes what "naive" means: in a future world, code generation may be partly LLM-driven and partly template-driven.
- Mochi relevance: nothing immediate. Possible MEP-50+ direction.

### 6. From Batch to Stream: Automatic Generation of Online Algorithms (PLDI 2024)
- Site: https://pldi24.sigplan.org/details/pldi-2024-papers/42/.
- Idea: Compile batch-style algorithms into incremental/online versions automatically.
- Mochi relevance: nothing directly for codegen; relevant if Mochi adds reactive or streaming primitives.

## §3 Where it shines, where it fails

The Lesbre/Lemerre abstract-interpretation paper is the most directly applicable. It validates that adding ~500 LOC of analysis to a template emitter can claw back 30% perf. SuperStack is the cheapest add-on for peephole gains. Bansal et al. is the most ambitious; useful for Mochi's numerical and array-heavy workloads.

The Optimistic Stack Allocation paper is a phase-2 add-on rather than a phase-1 must-have.

Compile-time profile: the abstract-interpreter approach adds linear overhead, SuperStack is offline (build-time), Fern is build-time annotation plus link-time composition.

## §4 Status (May 2026)

- All papers are published; PACMPL DOIs are live.
- No production deployments of these specific systems yet, but the techniques are being picked up:
  - Pharo and Squeak Smalltalk VMs are experimenting with the Lesbre/Lemerre abstract interpretation approach.
  - WebAssembly toolchains (binaryen, wasm-opt) have prior peephole superoptimization that SuperStack improves on.
  - Fern is being upstreamed into TACO (Kjolstad's compiler) and TVM.

## §5 Engineering cost for Mochi

- Lesbre/Lemerre abstract interpreter for Mochi: ~3 weeks (a "small but smart" pass over `compiler3/ir/`).
- SuperStack peephole rewriter: ~2 weeks if we treat it as offline tooling.
- Fern-style fusion: ~6-8 weeks. Substantial but bounded.

For MEP-42 phase 1, none of these are required. They are all profitable phase-2 additions.

## §6 Mochi adaptation note

- `compiler3/opt/` would house the abstract-interpretation pass.
- `compiler3/ir/` is the natural target for SuperStack-style peephole replacements (build-time tooling generates `opt/peep_table.go`).
- `runtime/vm3/` numeric kernels (arrays.go, bignum.go, lists.go) are the natural Fern annotation targets.

## §7 Open questions for MEP-42

- Should phase 1 include any of these PLDI 2024-2025 ideas, or strictly ship raw templates first?
- For SuperStack, what is our equivalence-checking oracle? The vm3 interpreter is the natural ground truth.
- For abstract interpretation, what is the lattice? Constants? Ranges? Type-set-with-arena?
- For Fern, do we want to expose annotations to user code or keep them internal?

## §8 References

- PLDI 2024 papers track: https://pldi24.sigplan.org/track/pldi-2024-papers.
- PLDI 2025 papers track: https://pldi25.sigplan.org/track/pldi-2025-papers.
- PACMPL Vol 8 PLDI issue: https://dl.acm.org/toc/pacmpl/2024/8/PLDI.
- PACMPL Vol 9 PLDI issue: https://dl.acm.org/toc/pacmpl/2025/9/PLDI.
- Lesbre/Lemerre follow-up "Are Abstract-interpreter Baseline JITs Worth it?": https://inria.hal.science/hal-05407834v1/document.
- Fern (Bansal et al.) preprint: https://dspace.mit.edu/bitstream/handle/1721.1/164683/3729292.pdf.
- Pavel Panchekha's "Distinguished (for me) Papers of PLDI'25" blog: https://pavpanchekha.com/blog/pldi25.html.