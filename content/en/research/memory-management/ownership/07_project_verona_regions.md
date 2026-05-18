---
title: "Project Verona Regions"
description: "Microsoft Research's experimental concurrent-ownership language. Ownership is over **regions** (groups of objects) instead of individual objects. Cowns (concurrent owners) serialise access; behaviours schedule work over multiple cowns atomically."
tags: ["memory-safety", "ownership"]
weight: 70
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Sponsor**: Microsoft Research Cambridge, Microsoft Special Projects, Imperial College London.
- **Core authors**: Sylvan Clebsch (also Pony founder), Matthew J. Parkinson, Sophia Drossopoulou, Tobias Wrigstad, Juliana Franco. PM support from Mads Torgersen (C#).
- **Project home**: https://www.microsoft.com/en-us/research/project/project-verona/ .
- **Publications**: https://microsoft.github.io/verona/publications.html .
- **Repo**: https://github.com/microsoft/verona (MIT license).
- **Key papers**:
  - Cheeseman, Parkinson, Clebsch, Kogias, Drossopoulou, Chisnall, Wrigstad, Liétar, "When Concurrency Matters: Behaviour-Oriented Concurrency", OOPSLA 2024.
  - Arvidsson, Castegren, Clebsch, Drossopoulou, Parkinson, Noble, Wrigstad, "Reference Capabilities for Flexible Memory Management", OOPSLA 2024.
  - Stoldt, Bucher, Clebsch, Johnson, Parkinson, Van Rossum, Snow, Wrigstad, "Dynamic Region Ownership for Concurrency Safety", PLDI 2025 — the Guido Van Rossum coauthorship signals this work is influencing Python's no-GIL future.
  - "DORADD: Deterministic Parallel Execution in the Era of Microsecond-Scale Computing", PPoPP 2025.
  - Parkinson, Clebsch, Wrigstad, "Reference Counting Deeply Immutable Data Structures with Cycles", ISMM 2024.
- **Underlying allocator**: snmalloc, https://github.com/microsoft/snmalloc , widely used (snmalloc-rs).

## §2 Core type discipline

Three primitives:

1. **Region**: a heap-allocated group of objects with a single entry point. Everything in the region is owned by the region; only the entry point is referenced from outside. A region is owned by exactly one thread of execution at a time.
2. **Cown (concurrent owner)**: a wrapper around a region (or set of regions) that mediates concurrent access. To touch a cown's contents you must acquire it.
3. **Behaviour**: a *when*-block that names a set of cowns and a body. The scheduler atomically acquires all named cowns, runs the body, releases them.

```verona
when (c1, c2) {
    // here c1 and c2's regions are mine, exclusively
}
```

Annotation surface (lightweight): region introduction via `new`/`Region.create`, reference capabilities (`iso`, `mut`, `imm`, …) per the OOPSLA'24 paper on flexible caps, and the `when` keyword for behaviours.

Judgement form: ownership is over the region. References within a region are unrestricted (you can do all the C-pointer tricks you want inside one region). References *across* regions must be `iso` or `imm`. The whole-program data-race-freedom property reduces to: at any moment, each region is owned by at most one thread.

Principal example — atomic transfer across two accounts modelled as cowns of regions:

```verona
when (var a = src, var b = dst) {
    a.balance = a.balance - amount;
    b.balance = b.balance + amount;
}
```

The scheduler ensures `src` and `dst` are acquired atomically; deadlock-free by construction (the scheduler orders acquisitions globally).

## §3 Memory-safety invariant

- **No data race**: region ownership is exclusive, behaviour acquisitions are atomic.
- **No deadlock**: scheduler-imposed lock ordering.
- **No UAF**: region lifetime is the dominator scope; objects within die together.
- **No aliasing-XOR-mutation violation across regions**: cross-region refs are `iso` or `imm`.

What it does **not** preserve in isolation: capability-based authority over effects. Verona's research is at the memory layer.

## §4 Compiler implementation cost

- The Verona prototype is in C++; the language is still under heavy iteration.
- The region check is dramatically simpler than per-object ownership: you reason about ~10 regions in a program instead of 10⁶ objects. Type rules are short.
- The behaviour scheduler is a substantial runtime, not a compile-time analysis. Cost moved from compiler to runtime.
- The PLDI'25 *Dynamic Region Ownership* paper showed regions can also be enforced dynamically (a runtime check), which is what makes Python integration possible. This is essentially Vale's idea applied at the region granularity instead of the object granularity.

Diagnostic story: region-level errors ("you tried to read across a region without holding the cown") are easier to phrase than per-object lifetime errors.

## §5 Production / language adoption status (May 2026)

- Verona remains a research project; no production binary depends on it.
- The **ideas** are spreading: the Van Rossum coauthorship on the PLDI'25 paper is a strong signal Python is studying region ownership for the no-GIL world.
- snmalloc, the supporting allocator, is in real production use (Rust ecosystem via snmalloc-rs).
- DORADD demonstrated microsecond-scale deterministic parallel execution in 2025, an industrial-relevance milestone.

## §6 Mochi adaptation note

Verona's *region as the unit of ownership* maps remarkably onto vm3's *arena as the unit of allocation*. The mapping is conceptual but suggestive.

vm3 already groups objects by **type** into arenas (`ArenaString`, `ArenaList`, `ArenaMap`, `ArenaStruct`, … in `runtime/vm3/cell.go:60`). A Verona region groups objects by **lifetime / ownership**. The two axes are orthogonal but composable: an `ArenaList` slab could be partitioned into sub-arenas keyed by region, and the 4-bit `ArenaTag` could grow to encode (arena-type, region-id).

A region-aware Mochi (call it a "region-extended vm3") gives:

- Bulk drop: a `region.dispose()` call frees every object in the region, bumping `gen` on each in O(N) where N is the slab count. This is the cheap analogue of Vale's per-object gen bump.
- Cross-goroutine safety: a `Spawn(region, f)` transfers the region to a new goroutine; the source slot is bumped, the destination owns the slab.
- Locality: the slab cache-friendliness story improves because a region's objects are contiguous.

Behaviours (`when`) are the part that does **not** translate. Mochi has no actors. If MEP-15 evolves to add async / structured concurrency, a `when (a, b)` block could become a first-class scheduling primitive on top of Goroutines.

Cowns (`acquire-this-region-exclusively`) could, however, ship today as a `borrow region { … }` block: inside the block, the runtime asserts exclusive access (one outstanding borrow per region) and the type checker tracks the borrowed regions in scope.

Surface-syntax change for MEP-41: introduce a *region* abstraction layered on arenas, with `region R { … }` blocks and `dispose R`. Per-handle ownership stays as it is (vm3 gen check); regions are a higher-level scoping mechanism for bulk freeing and cross-goroutine transfer.

Effect tie-in (MEP-15): a `when` block over cowns is a structured-effect handler. The effect surface could grow `region-write: R` and `region-read: R` labels.

Option tie-in (MEP-16): a region pointer becomes `Option<&Region>` once the region is disposed; gen-check failure surfaces as `None` rather than a trap.

Incompatible:

- Full per-object reference capabilities (the OOPSLA'24 paper). Too much complexity for v1 of MEP-41.
- The behaviour scheduler. That is a separate concurrency MEP entirely.

## §7 Open questions for MEP-41

1. Should MEP-41 introduce regions or stay at the per-handle granularity?
2. Can `ArenaTag` be repurposed as `RegionTag` without breaking the existing 16-arena ceiling?
3. Does a `region.dispose()` operator give MEP-41 the deterministic-destruction property without a full linear type system?
4. How does the JIT (vm3 MEP-39) optimise region-bounded loops the way the Vale "immutable region borrowing" paper does?

Sources: https://www.microsoft.com/en-us/research/project/project-verona/ ; https://microsoft.github.io/verona/publications.html ; https://github.com/microsoft/verona ; OOPSLA 2024, PLDI 2025, ISMM 2024 papers cited in §1.