---
title: "RustBelt and Iris"
description: "Foundational separation-logic verification of Rust's safe / unsafe core, and its 2024-2026 RefinedRust successor."
tags: ["memory-safety", "verification"]
weight: 10
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Original paper: Jung, Jourdan, Krebbers, Dreyer. **"RustBelt: Securing the Foundations of the Rust Programming Language"**, POPL 2018 (PACMPL 2). https://dl.acm.org/doi/10.1145/3158154
- Underlying logic: Jung, Krebbers, Jourdan, Bizjak, Birkedal, Dreyer. **"Iris from the ground up"**, JFP 2018; received the 2025 Most Influential POPL Paper Award and the 2023 Alonzo Church Award.
- Project home: https://plv.mpi-sws.org/rustbelt/ (MPI-SWS). The ERC RustBelt project formally ended April 2021 but the line continues.
- Major follow-up: Gäher, Sammler, Jung, Krebbers, Dreyer. **"RefinedRust: A Type System for High-Assurance Verification of Rust Programs"**, PACMPL PLDI 2024, Article 192. https://dl.acm.org/doi/10.1145/3656422 ; PDF https://iris-project.org/pdfs/2024-pldi-refinedrust.pdf
- Adjacent 2024-2026 papers: Matsushita & Tsukada, **"Nola: Later-Free Ghost State for Verifying Termination"** (PLDI 2025); Timany, Krebbers, Dreyer, Birkedal, **"A Logical Approach to Type Soundness"** (JACM 71(6), Nov 2024); Golfouse et al., **"Ghost Ownership for Union-Find and Persistent Arrays in Rust"** (CPP 2026); Ayoun, Denis, Maksimović, Gardner, **"A Hybrid Approach to Semi-automated Rust Verification"** (PACMPL 2025).

## §2 Claim or Mechanism
RustBelt mechanises, in Coq + Iris, a semantic model of an idealised Rust core called λRust. The theorem proven is that **every well-typed λRust program (including programs that compose safe code with carefully checked `unsafe` library implementations) is memory-safe and data-race-free**, in a relaxed-memory operational semantics. The key technical device is a *lifetime logic* layered over Iris which gives a separation-logic account of borrows and lifetimes.

What makes RustBelt distinctive is that it does **not** simply re-derive what `rustc` already knows about safe code. It additionally lets one prove `unsafe` blocks correct against the public type signature. RustBelt mechanically discharged this proof for `Cell`, `RefCell`, `Rc`, `Arc`, `Mutex`, `RwLock`, thread spawning, and the unsafe core of `mem::swap` and `Vec`. RustBelt-Relaxed (Dang et al., POPL 2020) extended the result to the C/C++11 relaxed-memory model.

RefinedRust (PLDI 2024) is the 2024 successor. It supplies *refinement types* on top of the lifetime logic so the model can also express functional correctness, and it does so with a higher degree of automation through the Lithium proof engine inherited from RefinedC. The PLDI 2024 evaluation verifies a substantial subset of the real `Vec` implementation. The model uses *borrow names* (prophecy variables in RustHorn style) and adds *pinned borrows*, requiring Iris's Later Credits (Spies et al. 2022).

## §3 Scope and Limits
**What is covered.** λRust core constructs, lifetimes, mutable / shared borrows, threads, the most common smart-pointer abstractions, an Iris-internal account of C11 relaxed memory in the RBRlx extension. RefinedRust additionally covers refinement-typed reasoning about real Rust data structures.

**What is not covered.** Trait resolution and the bulk of the surface Rust language are not modelled. The compilation chain from Rust to machine code is not verified by RustBelt itself; RustBelt is a semantic model of the source-level type system, not a verified compiler. Asynchrony (`async`/`await`), Pin gymnastics in real ecosystems, and the full standard library remain out of scope. Like all Iris models, RustBelt's *trusted base* includes the Coq kernel and the modelled λRust operational semantics; bugs in the modelled semantics would not be caught.

## §4 May 2026 Status
Active research but not deployed at production scale. RefinedRust is the leading-edge artifact and its mechanisation has appeared at PLDI 2024 with continuing CPP 2026 papers building on it. The 2025-2026 momentum is concentrated in (a) hybrid verifiers like Gillian-Rust and the Ayoun et al. 2025 PACMPL approach that combine RustBelt-style unsafe-code reasoning with Creusot for the safe layer, and (b) Tree-Borrows-aware program logics under construction (see §08). RustBelt itself is not used inside the Rust compiler, but informs the official Rust semantics working group.

## §5 Cost
Original RustBelt 2018: roughly 14 000 lines of Coq for the model plus the unsafe-library proofs; multiple person-years of MPI-SWS PhD effort. RefinedRust 2024 supplementary material runs into hundreds of pages and required substantial extensions to the lifetime logic (pinned borrows, later-credit usage). Per-proof effort for verifying a non-trivial unsafe abstraction is still measured in *weeks* per data structure for an expert; this is the main reason hybrid approaches are gaining ground.

## §6 Mochi Adaptation Note
Mochi need not (and should not) prove a RustBelt-style soundness theorem for vm3 itself in MEP-41 scope. RustBelt's relevance for MEP-41 is methodological:

- The *threat model* RustBelt formalises (memory safety = no UB under any context, including adversarial unsafe library callers) is the right framing for Mochi's claim that vm3 Cell handles cannot be forged from arbitrary user input. MEP-41 should state explicitly that the Mochi-language layer offers a *capability-safe* surface where, by construction, no program written in safe Mochi can synthesize a Cell pointing into a different arena tag or stale generation.
- The borrow-name / prophecy idiom used in RefinedRust is exactly how one would specify Mochi's mutable arena handles if a later MEP wanted to verify the JIT pipeline.
- Mochi should adopt RustBelt-style vocabulary in MEP-41 prose ("the safe fragment", "the trusted runtime", "logical invariants preserved across `unsafe` Go boundaries") and document the boundary between the Go-implemented runtime (`vm3` allocator, mark-sweep, `vm3jit`) and the bytecode-language surface.

## §7 Open Questions for MEP-41
1. Does Mochi want to claim only *type-safety* of the bytecode language, or the stronger property that the Go-hosted runtime preserves the type-safety invariant? RustBelt makes that distinction crisp; MEP-41 should pick one.
2. If a future MEP-N (N ≥ 42) wants to mechanise the 4-bit-tag / 12-bit-generation invariant, would the right vehicle be Iris (well-suited to concurrent mark-sweep) or a lighter Verus-style spec on the Go runtime?
3. RefinedRust's pinned borrows are designed for `Pin<&mut T>`-style abstractions; do Mochi's planned mutable iterators need analogous machinery, and if so should MEP-41 reserve a generation bit for "pinned"?
4. Should MEP-41 require that any `unsafe` Go fragment in the vm3 runtime carry a free-form "semantic specification" comment in the RustBelt style, even if not mechanised? This is cheap documentation that buys auditability.