---
title: "Verus"
description: "Microsoft Research's SMT-backed Rust verifier, the leading tool for verified systems software at scale in 2025-2026."
tags: ["memory-safety", "verification"]
weight: 20
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Lattuada, Hance, Cho, Brun, Subasinghe, Zhou, Howell, Parno, Hawblitzel. **"Verus: Verifying Rust Programs using Linear Ghost Types"**, OOPSLA 2023 (PACMPL 7). https://www.microsoft.com/en-us/research/publication/verus-verifying-rust-programs-using-linear-ghost-types/
- Lattuada et al. **"Verus: A Practical Foundation for Systems Verification"**, SOSP 2024. https://dl.acm.org/doi/10.1145/3694715.3695952 ; PDF https://www.cs.utexas.edu/~hleblanc/pdfs/verus.pdf
- AutoVerus (Wang et al., OOPSLA October 2025), LLM-assisted proof generation. https://www.microsoft.com/en-us/research/publication/autoverus-automated-proof-generation-for-rust-code/
- VeriStruct (Sun, Sun, Amrollahi, Zhang, Lahiri, Lu, Dill, Barrett, TACAS April 2026), AI-assisted verification of data-structure modules in Verus.
- Atmosphere (SOSP 2025): a verified Rust kernel built with Verus.
- Project: https://github.com/verus-lang/verus ; tutorial https://verus-lang.github.io/verus/guide/
- MSR project page: https://www.microsoft.com/en-us/research/project/practical-system-verification/publications/

## §2 Claim or Mechanism
Verus is an **SMT-based deductive verifier** for a subset of Rust. The programmer writes specifications (preconditions, postconditions, invariants, decreases-clauses for termination) in a `spec`/`proof`/`exec` mode discipline embedded in Rust syntax. Verus encodes these into verification conditions, compiles them through its `air` IR to Z3, and reports either "verified" or a counter-example. Verification is fully static; no runtime checks are added; proof and spec code are erased before code generation. The slogan from SOSP 2024 is "full functional correctness for low-level systems code, in Rust, with proof overhead acceptable to systems researchers".

Verus' distinctive contribution is its use of **linear ghost types** (a.k.a. tracked permissions) inside Rust. A `tracked` permission token represents the right to access a piece of memory or a piece of state, and the Rust borrow checker propagates it for free. This lets Verus prove rich properties about pointers, raw memory, and concurrent data structures without a dedicated separation-logic layer.

## §3 Scope and Limits
**Covered.** Functional correctness of sequential and concurrent Rust code, including: distributed systems (the IronKV / IronSync line), an OS page-table implementation, NUMA-aware concurrent data-structure replication, crash-safe persistent storage, the NR (node-replicated) memory allocator, hashmap implementations, IronShield / verified hypervisor components.

**Not covered.** Verus does not yet handle the full safe Rust surface (traits with associated types in their full generality are restricted; closures have limited support; some lifetime patterns are not yet automated). Verus does not produce a foundational Coq proof; one must trust Verus's encoding into Z3 and trust Z3 itself. Verus does not (today) verify the Rust compiler, so the trust chain bottoms out at `rustc` + LLVM + Z3 + Verus's own verifier.

## §4 May 2026 Status
**Industrial use.** Two of three best papers at OSDI 2024 were built on Verus; Atmosphere at SOSP 2025 was a verified kernel using Verus. Verus is *already in industrial use at Microsoft and Amazon*. SymCrypt (Microsoft's production crypto library used in Windows, Azure, Xbox) is being incrementally ported from C to Verus-verified Rust through an effort that also involves Aeneas. AWS uses Verus for components of its Nitro and Firecracker security stack alongside Kani. Verus continues to release on a regular cadence; the GitHub repository is highly active. AutoVerus and VeriStruct represent the 2025-2026 line of using LLMs to push the spec/proof burden lower.

## §5 Cost
The SOSP 2024 paper reports a corpus totalling **6.1K lines of Rust implementation and 31K lines of proof** — a roughly 5× proof-to-code ratio for fully verified systems code. This is dramatically better than Coq-based verification (CompCert was ~30× at the time of publication) but still costly. AutoVerus (OOPSLA 2025) is the explicit response: LLM-driven proof generation reduces engineer effort for routine functional correctness obligations; reported success rates approach human performance on straightforward data-structure exercises but degrade on concurrent invariants.

For the typical Mochi-scale module (~1000 LOC), expert Verus users report **weeks** of effort to fully verify, dropping to days once the team is fluent. This is qualitatively cheaper than Iris/RustBelt but qualitatively more expensive than `cargo test`.

## §6 Mochi Adaptation Note
Verus is the most realistic vehicle if Mochi later wants to verify portions of the vm3 runtime, *but MEP-41 itself need not commit to using it*. The relevant adaptation:

- Verus is written for Rust, not Go. Mochi's vm3 runtime is Go-hosted. A direct port is not in scope; MEP-41 should not promise Verus integration.
- However, the Verus *vocabulary* (`spec`, `proof`, `exec`, tracked permissions, decreases-clauses) maps cleanly onto how MEP-41 should document Cell-invariant preservation: each runtime entry point can be informally annotated with a pre/post on (arena_tag, generation, slab_idx) integrity, even if those annotations are comments rather than verified statements.
- Should Mochi ever migrate a security-critical kernel (e.g., the mark-sweep root scanner, or the JIT permission-flipper) to Rust, Verus is the leading candidate to verify it. MEP-41 should keep that door open by *not* baking Go-specific assumptions into the Cell representation invariant.
- Verus's tracked-permission idiom is the natural way to model "the right to mutate this arena slot at this generation"; MEP-41 should document the Cell as morally a *capability* in this sense.

## §7 Open Questions for MEP-41
1. Is there value in a *non-mechanised* "Verus-style spec" for vm3 Cell operations attached as MEP-41 appendix? It would not be machine-checked but would force the authors to write down the invariants.
2. Does Mochi want to claim eligibility for the CISA / NSA "memory-safe" category on the strength of the bytecode-language guarantees alone, or also on the strength of the (unverified but inspectable) runtime invariants? The Verus comparison is useful here because Verus shows what "verified" actually buys you.
3. Should MEP-41 explicitly track the AutoVerus / VeriStruct 2025-2026 trajectory as future work, in case LLM-assisted verification becomes cheap enough to retrofit?
4. The Verus + SymCrypt port suggests verified-Rust is replacing C, not Go. Should MEP-41 note Mochi's Go runtime as a transitional position and not a permanent architectural commitment?