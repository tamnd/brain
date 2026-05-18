---
title: "Perceus (Koka)"
description: "\"Garbage-free\" precise reference counting with reuse — in-place updates without locks, statically inserted at compile time."
tags: ["memory-safety", "runtime"]
weight: 10
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- Alex Reinking, Ningning Xie, Leonardo de Moura, Daan Leijen. **"Perceus: Garbage Free Reference Counting with Reuse."** *PLDI 2021*, ACM SIGPLAN Conf. on Programming Language Design and Implementation, June 2021. Distinguished Paper.
- Extended TR: Microsoft Research MSR-TR-2020-42, Nov 2020 (v4 2021-06-07).
- Follow-up: Lorenzen, Leijen. **"Reference Counting with Frame Limited Reuse"** (ICFP 2022 / TR 2021).
- Most recent: Leijen, Lorenzen. **"Tail recursion modulo context: an equational approach (extended version),"** *J. Functional Programming*, 24 Oct 2025.
- URLs:
  - https://www.microsoft.com/en-us/research/publication/perceus-garbage-free-reference-counting-with-reuse-2/
  - https://xnning.github.io/papers/perceus.pdf
  - https://dl.acm.org/doi/10.1145/3453483.3454032
  - Koka repo: https://github.com/koka-lang/koka

## §2 Mechanism

Perceus runs as a compile pass on a linear-resource calculus derived from Koka's typed core. After erasure to explicit-control IR, every variable use is rewritten to one of:

- `dup(x)` — increment refcount of `x`.
- `drop(x)` — decrement refcount; if it reached zero, recursively drop fields, then free.
- `drop_reuse(x)` — like drop, but if `x` is uniquely owned, return its raw memory address into a reuse token slot.

The compiler then pairs each `drop_reuse` with a constructor allocation of the same size (the **reuse analysis**). If the token is non-null at runtime, the new node is built **in place** in `x`'s old memory, with zero allocator calls and no refcount traffic. If the token is null, the allocator handles a fresh block.

Because Koka constructors are immutable and typed, Perceus is **precise** — there is exactly one `dup` per shared use and exactly one `drop` per dead binding; no read-barrier scan is needed. Reuse analysis is the analogue of TCO for purely functional programs and underlies the "Functional But In-Place" (FBIP) idiom: a textbook functional `map`, `reverse`, or red-black-tree rebalancing compiles to the same machine code as a destructive C loop.

Multi-threaded sharing uses atomic refcount ops *only* on values whose static type allows them to escape a thread (Koka tracks this with its effect/region system). Single-threaded values use plain integer ops.

## §3 Memory-safety property

Perceus delivers **deterministic, garbage-free reclamation**: an unreachable object is freed at the program point it becomes unreachable, with no heap walk. Combined with Koka's lack of cyclic mutable types, the result is sound spatial and temporal safety **without** a tracing GC and **without** stop-the-world pauses. The "in-place update" win comes from compile-time uniqueness; reuse is never wrong, because the token is only non-null when refcount = 1.

## §4 Production status (May 2026)

- Koka itself is research-grade. Stable line is v3.1.3 (Jan 2025), with concurrent build system at v3.1.0 (Feb 2024). Production usage outside Microsoft Research is essentially nil.
- Perceus the *technique* is in production via **Roc** (which adopted the algorithm; see file 02) and inspired **Lean 4**'s RC scheme. Both are far larger user-bases than Koka itself.
- Microsoft Research continues active work (TRMC 2025 paper on tail-recursion-modulo-context, frame-limited reuse).
- Public benchmarks from the PLDI paper showed Koka/Perceus matching or beating OCaml, Haskell GHC, Swift ARC, Java G1, and Java Shenandoah on the BIM functional benchmark suite (red-black trees, deriv, nqueens, cfold). Often 2-3× lower peak RSS than tracing collectors.

## §5 Cost

- **Throughput.** Comparable to a generational tracing GC for allocation-heavy functional code; slightly slower than Java G1 on highly-allocating loops where the nursery wins; faster on phases dominated by unique-owner mutation thanks to FBIP. Roughly 0-15% off OCaml on most benchmarks.
- **Memory.** Wins by 30-60% vs tracing GCs on the BIM suite because frees are immediate.
- **Latency.** Worst case is the recursive drop of a long singly-linked list, which is O(n) and pause-the-mutator. LXR/MMTk noted this same problem and solved it by deferring decrements; Perceus does not, relying on the assumption that long unique lists are rare in idiomatic Koka.
- **Atomic-refcount overhead.** Only on cross-thread values. Empirically a few percent.

## §6 Mochi adaptation note

Perceus is a *strong* fit for vm3 because Mochi is statically typed and the §6.1 handle Cell already names a typed slab. The smallest patch shape:

1. **Static unique-owner inference in compiler3 (MEP-40 §7.2 type-driven lowering).** Add a "uniqueness" lattice on top of compiler3's IR types: a value is `unique` if no concurrent reader holds a handle and no live alias exists in the same frame. This is decidable from the type-driven lowering pass since Mochi already tracks borrows for the closure planner.
2. **vm3 `OP_DUP_HANDLE` / `OP_DROP_HANDLE` (MEP-40 §6.5).** Currently MEP-40 §9 plans free-list reuse only after a mark-sweep cycle. Emit explicit `OP_DROP_HANDLE` at the AST-derived "last-use" point — the arena `Free(handle)` already nils the backing slot and pushes the slot index, so this is a one-line emit change in compiler3/emit.
3. **`OP_REUSE_LIST` / `OP_REUSE_STRUCT` super-op.** Pair a known-size constructor with the immediately preceding drop. If the refcount-equivalent (slot generation matches and no aliases live) check passes at runtime, bypass `AllocList` entirely and overwrite the slot's backing slice in place. This is the FBIP win and maps cleanly onto MEP-40 §6.2 because the slab index does not change — only the generation bumps.
4. **No conflict with Go GC (MEP-40 §6.3).** Backing slices remain Go-rooted; we are only deciding *when* to nil the slab entry. Go's GC still owns the underlying bytes.

This is consistent with Mochi's design ethos (static-typed, Go-hosted, no cgo). The only design-philosophy decision is whether to commit to Perceus *instead of* a mark-sweep collector (MEP-40 Phase 6) or *alongside* it as an optimisation. The latter is safer and matches the "Lobster + cycle detection at exit" trade-off.

## §7 Open questions for MEP-41

- Can compiler3's uniqueness lattice prove enough cases to make reuse profitable, given Mochi's closure-heavy style and dynamic `list[T]` slicing?
- How does Perceus interact with vm3's planned mark-sweep over arenas (MEP-40 §9.2, Phase 6)? If RC is precise, mark-sweep is only needed for cycles — can it run rarely (every N seconds) like Python's cycle collector?
- Do we want atomic refcounts at all? Mochi today is single-threaded per vm. If Phase 7 ever opens up Go-style goroutines, we need to know now what the per-arena handoff looks like.
- Does the FBIP reuse win survive vm3jit (MEP-40 §6.5, Phase 5)? The interpreter pays a dispatch tax that hides RC ops; the JIT does not.

## Sources

- [Perceus PLDI'21 paper PDF](https://xnning.github.io/papers/perceus.pdf)
- [Microsoft Research project page](https://www.microsoft.com/en-us/research/publication/perceus-garbage-free-reference-counting-with-reuse-2/)
- [Reference Counting with Frame Limited Reuse (TR 2021)](https://www.microsoft.com/en-us/research/wp-content/uploads/2021/11/flreuse-tr.pdf)
- [Koka on GitHub](https://github.com/koka-lang/koka)
- [Koka project at Microsoft Research](https://www.microsoft.com/en-us/research/project/koka/)