---
title: "Creusot"
description: "A deductive verifier for safe Rust that compiles to Why3 and discharges to off-the-shelf SMT solvers."
tags: ["memory-safety", "verification"]
weight: 30
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Denis, Jourdan, Marché. **"Creusot: A Foundry for the Deductive Verification of Rust Programs"**, FM 2022. https://dl.acm.org/doi/10.1007/978-3-031-17244-1_6 ; preprint https://inria.hal.science/hal-03526634/document
- Project: https://creusot.rs ; repo https://github.com/creusot-rs/creusot ; user guide https://creusot-rs.github.io/creusot/guide/tutorial.html
- Underlying platform: Why3 / Coma (the new Creusot IR, replacing Why3's older WhyML emission path), targeting Z3, CVC5, Alt-Ergo 2.6.0 and others.
- Notable applications: CreuSAT (a verified SAT solver) and Sprout (a verified SMT solver), both Creusot case studies.
- Related: Ayoun et al. **"A Hybrid Approach to Semi-automated Rust Verification"** (PACMPL 2025) integrates Creusot with Gillian-Rust to extend coverage to unsafe code.

## §2 Claim or Mechanism
Creusot proves **functional correctness** of safe-Rust programs against user-supplied contracts. The pipeline:

1. The Rust source is compiled to Rust MIR via the regular `rustc` toolchain.
2. Creusot's plugin translates MIR functions into Coma (an intermediate verification language in the Why3 ecosystem).
3. Why3 generates verification conditions from the Coma program plus contracts.
4. The verification conditions are dispatched to SMT solvers; if all VCs are discharged, the program meets its contracts.

The two distinctive technical ideas are:
- **Prophetic specification of borrows**: a mutable borrow `&mut T` is translated as a logical pair `(current, final)` — the current value and the prophesied final value at the end of the borrow's lifetime. This is the RustHorn-style encoding (Matsushita et al. 2020, RustHornBelt PLDI 2022) and means that mutation is handled within first-order logic without separation-logic framing.
- **Trait-based abstraction**: traits become abstract specification types; this lets Creusot specify and verify generic algorithms in a way that matches Rust's actual abstraction style.

## §3 Scope and Limits
**Covered.** Safe-Rust data-structure and algorithm code: lists, vectors, hash maps, iterator combinators, parsers, SAT/SMT engines. Termination via `variant` clauses. Trait-based abstractions and generic code. Reborrowing in loops works thanks to the prophetic encoding.

**Not covered.** Unsafe Rust — by design — is outside Creusot's reach. Heavy concurrency is awkward; Creusot is currently best suited for sequential data-structure / algorithm verification, less so for systems-code that exploits concurrency or interacts heavily with the OS. As with all SMT-based tools, the trusted base is huge: one must trust Creusot, Why3, every SMT solver invoked, and any interactive proof assistant used. Z3 alone is roughly half a million lines of code.

Creusot is *experimental software*; users should expect missing features and occasional crashes.

## §4 May 2026 Status
Creusot remains *the* state-of-the-art tool for **safe-Rust functional verification** and is the typical baseline in the 2025-2026 academic literature. Recent improvements include separated `verif/` artifacts, one Coma file per module for faster iteration, stable Coma identifiers (so Rust refactors don't break Why3 proofs), and Alt-Ergo upgraded to 2.6.0.

In the broader 2025 landscape, Creusot is one of three SMT-based Rust verifiers (with Verus and Prusti); Verus and Creusot diverge primarily on whether they use linear-ghost types inside Rust (Verus) or external Why3 contracts (Creusot). Hybrid approaches (Gillian-Rust + Creusot from PACMPL 2025) layer separation-logic reasoning on unsafe blocks atop Creusot's safe-code verification.

## §5 Cost
Lower than Verus per safe-Rust function because Why3 + SMT do more inference. Typical published case studies: CreuSAT has thousands of lines of Rust with a low single-digit proof-to-code ratio for the verified core. The barrier is the learning curve of Why3 specification syntax, not the solver runtime. Recurring problem: SMT proof obsolescence — small Rust refactors used to invalidate Why3 proofs; the 2024-2025 stable-identifier work addresses that.

## §6 Mochi Adaptation Note
Creusot is the natural reference point if Mochi's documentation wants to discuss "what functional-correctness verification of a safe-only memory-safe language looks like".

- Creusot proves correctness *only* of programs written in the safe fragment. This mirrors exactly what MEP-41 should claim for Mochi: the Mochi-source language is the safe fragment, and any reasoning about correctness has to assume the Go-implemented runtime is trusted.
- The RustHorn prophecy encoding is the canonical technique to *specify* what a mutating operation does without dragging in separation logic. If MEP-41 ever wants to write down a contract for `vm3.Set(cell, value)` it would be cheaper to give it as a (current, final) pair than as an Iris triple.
- Creusot is *not* a tool Mochi can adopt directly: it targets Rust, and Mochi has no Rust frontend. The honest position for MEP-41 is to note Creusot as the leading semi-automated verifier for the verification-by-contract style and to acknowledge that Mochi makes no analogous claim.

## §7 Open Questions for MEP-41
1. Should the Mochi spec document use prophecy-style notation (current/final pairs) for mutable runtime entry points, even informally? It is a cheap notation upgrade.
2. Does MEP-41 want to commit to a "Creusot-equivalent contract style" for future Mochi-source verification, or leave the question open?
3. Hybrid Creusot + Gillian-Rust (PACMPL 2025) is the model for "verify the safe fragment cheaply, verify unsafe by separation logic". Should Mochi adopt the analogous discipline of "trust the runtime invariants by inspection, verify the bytecode-language soundness as a separate concern"?
4. Creusot's SMT trust base is large; should MEP-41 explicitly discuss the trusted computing base of Mochi vm3 (Go compiler, runtime, OS) and state that Mochi does not aim to shrink that base in this MEP?