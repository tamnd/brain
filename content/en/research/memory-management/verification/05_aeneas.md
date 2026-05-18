---
title: "Aeneas"
description: "Rust verification by functional translation: compile Rust to a pure lambda calculus, verify there."
tags: ["memory-safety", "verification"]
weight: 50
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Ho & Protzenko. **"Aeneas: Rust verification by functional translation"**, ICFP 2022 / PACMPL 6. https://dl.acm.org/doi/10.1145/3547647 ; arXiv https://arxiv.org/abs/2206.07185
- Ho, Fromherz, Protzenko. **"Sound Borrow-Checking for Rust via Symbolic Semantics"**, ICFP 2024. https://icfp24.sigplan.org/details/icfp-2024-papers/17/Sound-Borrow-Checking-for-Rust-via-Symbolic-Semantics
- Project: https://github.com/AeneasVerif/aeneas (Inria + Microsoft Research). Frontend: Charon → LLBC. Backends: F*, Coq, HOL4, Lean (Lean is the maintainers' primary 2024-2026 target).
- Lean integration documentation: https://lean-lang.org/use-cases/aeneas/
- Used in production: Microsoft's port of SymCrypt (the Windows / Azure / Xbox crypto library) from C to verified Rust.
- Cited in: Bhargavan et al., **"Formal Security and Functional Verification of Cryptographic Protocol Implementations in Rust"**, ACM CCS 2025.

## §2 Claim or Mechanism
Aeneas translates safe Rust to a **pure functional program in a higher-order lambda calculus**, suitable for direct reasoning in F* / Coq / HOL4 / Lean. The key theorem (ICFP 2024) is:

> The symbolic execution Aeneas performs on the Low-Level Borrow Calculus (LLBC) is a sound borrow-checker. Programs that symbolically execute without getting stuck do not get stuck under a low-level pointer-based CompCert-style operational semantics.

The translation idiom: every Rust function with mutable borrows compiles to a *forward function* (returning the result at call site) plus one *backward function* per outgoing lifetime (propagating the post-borrow state). Forward + backward together behave like a lens. Because LLBC is value-based — no addresses, no aliasing — the verifier deals only with pure functions over algebraic data types. Separation-logic framing, memory invariants, and modifies-clauses are *eliminated by construction*.

The ICFP 2024 paper additionally shows that adding a `join` operation to LLBC's symbolic semantics preserves soundness; this enables Aeneas to handle loops, which the original 2022 paper could not.

## §3 Scope and Limits
**Covered.** The subset of safe Rust that follows the static ownership discipline: no `unsafe`, no interior mutability (`Cell` / `RefCell`), no raw pointers. Mutable / shared borrows, lifetimes, generic functions, traits, recursion, and (since 2024) loops. Lean backend has the most active tactic support.

**Not covered.** Unsafe Rust is explicitly out of scope — Protzenko's argument is that unsafe code is better served by RustBelt-style frameworks. Interior mutability is out of scope by design. Concurrency is not handled.

This is a deliberately narrow but very productive niche: cryptographic libraries, parsers, data-structure cores, and protocol implementations sit cleanly in the Aeneas subset.

## §4 May 2026 Status
**Used in production crypto verification.** Microsoft's incremental port of SymCrypt from C to Rust is using Aeneas (alongside Verus). This is one of the largest verified-Rust crypto efforts in industry. The Lean backend is the maintainers' current primary target, fitting into Lean 4's broader uptake at companies running formal-methods programs.

The 2024 ICFP "Sound Borrow-Checking" paper is the most-cited Aeneas follow-up and made Aeneas the *only* borrow-checker shipping with a foundational soundness proof. Adoption is concentrated in the cryptography / protocol-verification community (the Bhargavan group at Inria/Microsoft is the heaviest user).

## §5 Cost
For pure-functional Rust modules in the Aeneas subset, proof effort is essentially the cost of the F*/Lean proof itself — no memory reasoning. For straightforward data-structure code, proofs are days; for crypto algorithms, weeks to months. SymCrypt-class libraries are a multi-engineer-year effort but were previously done at *similar* cost in C (HACL\*, EverCrypt). The novelty is that the Rust source can be *the executable*, not just a reference.

Trusted base: the Aeneas translator, the Charon frontend, the backend prover. Smaller than Verus's trust base because Aeneas produces explicit functional code that a human can read; if the prover succeeds the bug must be in Aeneas's translator (which is small) or in the backend.

## §6 Mochi Adaptation Note
Aeneas is the *most architecturally interesting* tool for MEP-41 — but only as an analogy, not as an integration.

- Mochi's vm3 IR plays roughly the role Aeneas's LLBC plays: a *value-based* description of what a program does without committing to a memory layout. The Aeneas insight — "if you can translate to a pure-functional model, memory reasoning is free" — informs how to *document* vm3 semantics in MEP-41. Cell handle operations can be described as pure functions over an abstract `(arena_tag, generation, slab_idx) → Value` map, with the runtime's job being to maintain that map.
- The Aeneas/SymCrypt story is the strongest single argument that "verified Rust is the production path for security-critical code". Mochi is positioned downstream of that argument (Mochi is for application code, not crypto kernels). MEP-41 should *cite* Aeneas as the existence proof that this works, but not claim to participate.
- Aeneas explicitly avoids interior mutability. Mochi's mutable Cells *are* interior mutability at the language level. MEP-41 should note this divergence and explain that Mochi pays the cost in *runtime* (generation counters, mark-sweep) rather than in *static analysis*.

## §7 Open Questions for MEP-41
1. Should MEP-41 sketch a pure-functional reference semantics for vm3 in the Aeneas style — `step : VMState → VMState` — as an appendix? Useful for documentation even without a Lean backend.
2. Aeneas excludes interior mutability; Mochi requires it. Is there a future MEP that splits Mochi into "Aeneas-style verifiable subset" and "general Mochi"? Probably premature, but MEP-41 should note the design fork.
3. The Lean backend is the active target. Should Mochi formal-methods discussion adopt Lean rather than Coq, to align with the 2025-2026 momentum? Cheap forward-looking statement to include.
4. If a future Mochi-to-Rust transpiler is ever contemplated (for performance-critical kernels), Aeneas would let one verify the result. Worth keeping the architectural option alive in MEP-41 prose.