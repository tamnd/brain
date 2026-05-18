---
title: "Separation Logic for Managed (GC'd) Heaps"
description: "Iris-based separation logics with space credits, tracing GC, and the 2025 IrisFit + Nextgen-Modality lines."
tags: ["memory-safety", "verification"]
weight: 90
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- McCreight et al. **"GCSL: A logic for low-level programs with GC interfaces"** (foundational, pre-Iris). https://ieeexplore.ieee.org/document/5970244/
- Madiot & Pottier. **"A Separation Logic for Heap Space under Garbage Collection"**, POPL 2022 / PACMPL 6. https://dl.acm.org/doi/10.1145/3498672 ; PDF https://cambium.inria.fr/~fpottier/publis/madiot-pottier-diamonds-2022.pdf
- Charguéraud, Moine, Pottier. **"A High-Level Separation Logic for Heap Space under Garbage Collection"**, POPL 2023 / PACMPL 7. https://dl.acm.org/doi/10.1145/3571218 ; PDF https://www.chargueraud.org/research/2022/space_with_gc/space_with_gc.pdf
- Moine, Charguéraud, Pottier. **"Will It Fit? Verifying Heap Space Bounds of Concurrent Programs under Garbage Collection"** (IrisFit), ACM TOPLAS 2025. https://doi.org/10.1145/3716312 ; PDF https://iris-project.org/pdfs/2025-toplas-willitfit.pdf
- Vindum, Georges, Birkedal, Stark, Timany, Blazy, Tabareau. **"The Nextgen Modality: A Modality for Non-Frame-Preserving Updates in Separation Logic"**, CPP 2025. (Birkedal's group.)
- Iron (2019): "Iron: Managing Obligations in Higher-Order Concurrent Separation Logic" — affine separation logic for GC'd languages.
- Melocoton (Guéneau, Hostert, Spies, Sammler, Birkedal, Dreyer, OOPSLA 2023): cross-language verification at the OCaml/C boundary.
- Lars Birkedal personal note: his Reynolds-era PhD work used separation logic to verify a copying GC. ETAPS blog https://etaps.org/blog/019-lars-birkedal/

## §2 Claim or Mechanism
Reasoning about heap *space* (not just heap *correctness*) under garbage collection is harder than reasoning about heap space in a manual-allocation language, because a GC can deallocate any subset of currently unreachable objects at any time. The 2022-2025 sequence of "space credits" logics solves this with the following central idea:

- **Space credits** are a separation-logic resource representing *available logical space*. Allocation consumes credits; logical deallocation produces them.
- **Logical deallocation is decoupled from physical deallocation.** A program can logically deallocate a block — releasing space credits to the verifier — without immediately freeing physical memory. The GC eventually catches up.
- **Reachability is the gate.** A block can be logically deallocated only once it is no longer reachable from any logical root. The logic enforces this through *deallocation witnesses* — Vindum & Birkedal (2021) introduced `ℓ ↦ □` as a token saying "this location can be logically forgotten".

**IrisFit** (TOPLAS 2025) extends this to **concurrency**. The technical wrinkle: under arbitrary thread interleaving, a sleeping thread holding a stale root can pin arbitrarily much memory unrecoverable. IrisFit solves this by introducing language features the verifier requires from the runtime: **possibly-blocking memory allocation**, **polling points**, and **protected sections**. Under these, the logic guarantees that at any allocation point, either enough space is available or the program is in a state where the GC can free enough.

**The Nextgen Modality** (Birkedal et al., CPP 2025) handles non-frame-preserving updates — exactly the kind of operations a generational GC performs (object identity is preserved across collections, but the predecessor relation is not). This is a recent technical primitive needed to scale Iris-style reasoning to realistic GC implementations.

## §3 Scope and Limits
**Covered.** Sequential and concurrent tracing GC. Space-bounds verification (i.e., "this program will not run out of memory under this GC"). Treiber-stack-style concurrent data structures whose space behaviour depends on synchronisation. Mechanised in Iris/Coq.

**Not covered.** The reasoning is at the *semantic* level — the user proves their program against a GC abstraction, not against a real-world GC implementation. The connection between the semantic GC and an actual mark-sweep / generational / concurrent GC is still being assembled. There is no end-to-end "verify a real Go-style GC in Iris" result yet. Performance: these are static *correctness* proofs, not runtime checks; they don't tell you what the GC actually does at runtime, only what bound the program respects.

## §4 May 2026 Status
The IrisFit + Nextgen-Modality + Melocoton trio represents the **2023-2025 frontier of GC verification in separation logic**. IrisFit specifically (TOPLAS 2025) is the leading-edge published artifact for concurrent GC. The work continues at MPI-SWS, Aarhus, Inria.

This area is still firmly research-grade. The 2024-2026 trajectory is towards bridging the gap with real GC implementations: Melocoton handled OCaml ↔ C interop, the natural next steps are GHC-Haskell, MMTk-style modular GC frameworks, and JVM-class GCs. None of those have a finished verification yet; the IrisFit recipe scales to a "model GC", not (yet) to G1 / Shenandoah / ZGC.

## §5 Cost
IrisFit and the surrounding papers are **multi-person-year PhD-thesis efforts**. The Madiot-Pottier 2022 baseline is on the order of 10 000 lines of Coq; IrisFit adds significantly more for the concurrent case. Per-program verification cost on top of the IrisFit framework is days to weeks for a small concurrent data structure — competitive with hand-rolled Iris proofs but with explicit space accounting.

## §6 Mochi Adaptation Note
This area is **the closest existing formal-methods literature to Mochi's actual problem domain**. Mochi has per-type arenas, a planned mark-sweep, generation-tagged Cells, and a Go-implemented runtime. IrisFit / GCSL / Iron answer exactly the question MEP-41 *could* ask: "what does it mean to formally verify our mark-sweep?".

- MEP-41 should **explicitly cite** the IrisFit / space-credit line as the most-relevant body of theory, even though MEP-41 itself does no mechanised verification. This is good "documents-its-position" hygiene: a reader who knows the formal-methods literature will see Mochi is aware of where the bar is.
- The IrisFit insight about *polling points* and *protected sections* is directly applicable: Mochi's vm3 will need similar concepts when mark-sweep is added. A "Mochi safepoint" must be a point where (a) all live Cells are rooted and observable to the collector, and (b) the runtime is permitted to advance generation. MEP-41 should reserve language for this even if the implementation is later.
- The Nextgen Modality is conceptually the *right* model for arena-tag and generation transitions: these are exactly the non-frame-preserving updates the modality is designed for. Even without using the formal modality, MEP-41 can document the generation-bump operation as "non-frame-preserving with respect to old Cells".
- Melocoton-style cross-language reasoning is the right template for the Go ↔ Mochi FFI: Mochi's Go-managed and Mochi-managed heaps interact much like OCaml's GC heap and C's `malloc` heap.

## §7 Open Questions for MEP-41
1. Should MEP-41 explicitly identify the vm3 GC safepoint as a "polling point" in IrisFit terminology? It is good vocabulary and free.
2. The IrisFit approach requires the runtime to expose certain operations the language guarantees. Should MEP-41 enumerate the runtime operations Mochi guarantees to bytecode (allocate, read-with-generation-check, write-with-generation-check, safepoint)? This makes the runtime/bytecode contract explicit.
3. The Nextgen-Modality 2025 work suggests that "generation bump" is well-studied formally. Is it worth a brief MEP-41 appendix sketching the operational semantics of a Cell read in the presence of a generation bump? Cheap and informative.
4. Mochi has no concurrent mark-sweep planned (yet). Should MEP-41 explicitly defer concurrency to a future MEP, citing IrisFit as the model that *would* apply when concurrency is added?
5. Should Mochi adopt the "space credits" idea as a *runtime* discipline — i.e., upper-bound heap pressure with a budget rather than an arbitrary `OutOfMemory` panic? IrisFit shows the formal payoff; Mochi could borrow the API.