---
title: "Formal Models of the Rust Borrow Checker"
description: "Stacked Borrows, the 2025 Tree Borrows replacement, and the trajectory of NLL / two-phase formalisation."
tags: ["memory-safety", "verification"]
weight: 80
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Jung, Dang, Kang, Dreyer. **"Stacked Borrows: An Aliasing Model for Rust"**, POPL 2020 / PACMPL 4. The original operational aliasing semantics for Rust.
- Villani, Hostert, Dreyer, Jung. **"Tree Borrows"**, PLDI 2025 / PACMPL 9 Article 188. https://dl.acm.org/doi/10.1145/3735592 ; PDF https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf
  - **Distinguished Paper Award**, PLDI 2025.
  - Became the most-downloaded PACMPL paper of all time shortly after publication.
- Background blog: Jung, "From Stacks to Trees: A new aliasing model for Rust" (2023). https://www.ralfj.de/blog/2023/06/02/tree-borrows.html
- Tree Borrows research home at ETH Zürich PLF lab: https://plf.inf.ethz.ch/research/pldi25-tree-borrows.html
- NLL / two-phase historical thread: https://github.com/rust-lang/rust/issues/56254
- McCormack, Sunshine, Aldrich (2024), **"A Study of Undefined Behavior Across Foreign Function Boundaries in Rust Libraries"**, arXiv:2404.11671.
- Rust formal-methods working-group meeting summary: https://rust-formal-methods.github.io/meetings/tree-borrows/
- Aeneas's complementary contribution: Ho, Fromherz, Protzenko, **"Sound Borrow-Checking for Rust via Symbolic Semantics"**, ICFP 2024 (see verification/05).

## §2 Claim or Mechanism
Both Stacked Borrows and Tree Borrows are **operational-semantics models of pointer aliasing in Rust**: every memory access checks a per-location data structure (a stack or a tree) of "permission tags"; if the access is inconsistent with the tags, the program has Undefined Behaviour. The point of these models is to enable optimisations that reorder memory accesses around opaque function calls — optimisations that would be unsound under unrestricted aliasing but are sound under the aliasing discipline.

**Stacked Borrows** uses a stack per memory location. Each new borrow pushes; ends-of-lifetime pop. The stack discipline is conservative: a number of common real-world patterns (e.g., two-phase borrows from NLL, certain raw-pointer patterns) are rejected as UB.

**Tree Borrows** replaces the stack with a tree. Children inherit permissions from their parent borrow; siblings can coexist; raw pointers form their own branch. The tree allows much more permissive behaviour while still enabling the desired optimisations. Empirically, on the 30 000 most-downloaded crates, Tree Borrows rejects **54% fewer** test cases as UB than Stacked Borrows does. Tree Borrows is the leading candidate to become Rust's official aliasing model.

Both models are mechanised in Rocq (Coq) and run as a *MIRI* mode (the official Rust UB-detector). NLL / two-phase borrows — historically painful for Stacked Borrows, which had to treat them as raw pointers — are first-class in Tree Borrows.

## §3 Scope and Limits
**Covered.** Pointer aliasing semantics for `&T`, `&mut T`, `Box<T>`, raw pointers `*const T` / `*mut T`, and their interactions through `transmute` and FFI. NLL and two-phase borrows.

**Not covered.** The full Rust language semantics (these are *aliasing* models, not whole-language semantics). Relaxed-memory effects (handled separately by RustBelt-Relaxed). The proof that Rust's safe fragment respects the aliasing model — this is the *RustBelt-Tree-Borrows integration*, which is **ongoing 2025-2026 work** and not yet complete. LLVM-level optimisations correspondence (LLVM's `noalias` is similar but not identical; an LLVM-formal-semantics convergence is also ongoing).

## §4 May 2026 Status
**Tree Borrows is the de-facto current aliasing model for Rust**, replacing Stacked Borrows in 2025-2026 discourse. MIRI has both modes; the community recommendation is Tree Borrows. The PLDI 2025 paper won the Distinguished Paper award and became PACMPL's most-downloaded paper. While the original author (Villani) has moved on, work continues at ETH (Hostert) and MPI-SWS (Jung's group) to build:
1. A program logic for Tree Borrows, ideally an extension of the RustBelt lifetime logic, so that safe Rust can be proved to satisfy Tree Borrows.
2. Tools for unsafe-code authors to check that their `unsafe` blocks are TB-compatible.
3. Convergence with LLVM's formal-semantics effort and the `noalias` attribute.

The 2024 McCormack et al. paper on FFI-boundary UB is the canonical reference for how Rust's aliasing model interacts with C / C++ across `extern "C"` boundaries.

## §5 Cost
Tree Borrows itself was a roughly **two-year PhD-scale research effort** at ETH/MPI-SWS, with the proofs mechanised in Rocq. The cost of *adopting* the model is essentially zero for the average Rust user (it's transparent), but the cost of *integrating* it with RustBelt and with LLVM is the active 2025-2026 research front, expected to be multi-person-year.

## §6 Mochi Adaptation Note
The relevance of borrow-check formalisation to MEP-41 is **conceptual, not direct**. Mochi has no borrow checker. The relevant takeaways:

- The *category of vulnerability* Tree Borrows addresses — temporal memory safety bugs arising from pointer aliasing across function calls — is exactly the category vm3 handles by *generation tags*. Both are doing the same job: detecting "I held a reference too long" violations. Tree Borrows does it statically (the compiler rejects programs with UB); Mochi does it dynamically (the runtime invalidates Cells when the generation advances).
- MEP-41 should *cite* Tree Borrows as the leading static technique for temporal safety and explicitly contrast Mochi's runtime-generation-tag approach. Both are valid solutions to the same problem; they make different cost / expressiveness tradeoffs. Static: zero runtime cost, language-design cost. Dynamic: runtime cost (the generation field, the check on access), but no language-design tax — the Mochi programmer never has to think about lifetimes.
- The McCormack 2024 FFI study is directly relevant: when Mochi crosses into Go-native code, the same boundary-UB issues arise. MEP-41 should note that Cell handles crossing FFI boundaries must be treated like raw pointers in Tree Borrows terms — once they cross out of the Mochi-managed region, the generation invariant is suspended and the FFI caller must restore it before passing the Cell back.
- Mochi need not prove any aliasing-model theorem. The bytecode-language-level guarantee is "no program written in safe Mochi can hold a stale Cell", and this is a *runtime* property, not a static one.

## §7 Open Questions for MEP-41
1. Should MEP-41 explicitly contrast Rust's static lifetime/borrow approach with Mochi's dynamic generation-tag approach as a *design-tradeoff explanation* for readers who arrive expecting borrow checking?
2. The FFI / `extern "C"` boundary in Rust is a known UB hazard; Mochi's Go FFI boundary is the same hazard wearing different clothes. Should MEP-41 spell out the contract for Cells crossing into Go-native code?
3. Tree Borrows allows two-phase borrows because real code wants them. Are there Mochi patterns analogous to two-phase borrows (e.g., "I want to read the length of this vector then write to it") that should be designed-for at the Mochi-language level?
4. Should MEP-41 commit to a Mochi-specific equivalent of MIRI — a runtime checking mode that detects "this Cell access would have been UB under stricter rules"? Useful for fuzzing and CI.