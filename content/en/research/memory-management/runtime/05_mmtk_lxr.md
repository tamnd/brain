---
title: "MMTk and LXR"
description: "A research framework that cleanly separates GC plans from policies, plus the LXR collector that proves a stop-the-world RC+mark-region design can beat industrial concurrent GCs on tail latency."
tags: ["memory-safety", "runtime"]
weight: 50
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **MMTk (Memory Management Toolkit).** Stephen M. Blackburn et al., ANU. Originally a Java framework (Blackburn, Cheng, McKinley, 2004), rewritten in Rust as `mmtk-core` (~2018-present). https://www.mmtk.io/, https://github.com/mmtk/mmtk-core.
- **LXR — "Low-Latency, High-Throughput Garbage Collection."** Wenyu Zhao, Stephen M. Blackburn, Kathryn S. McKinley. *PLDI 2022*, San Diego, June 2022, pp. 76-91. https://www.steveblackburn.org/pubs/papers/lxr-pldi-2022.pdf.
- Recent follow-up: Zhao, Blackburn, McKinley, "Work Packets: A New Abstraction for GC Software Engineering, Optimization, and Innovation," *OOPSLA 2025*.
- MMTk is in production for: V8 (experimental), Ruby (CRuby 3.4 modular GC, 2025), Julia (experimental), and several research interpreters.
- LXR builds: https://github.com/wenyuzhao/lxr-builds.

## §2 Mechanism

**MMTk** is a *plan-policy separation* model:
- A **policy** is a concrete heap-management strategy: `MarkSweepSpace`, `CopySpace`, `ImmixSpace`, `LargeObjectSpace`, `ReferenceCountSpace`, etc. Each policy owns a contiguous chunk of address space and answers questions like "is this address yours?" and "trace this object."
- A **plan** wires policies together into a full collector: e.g. `GenImmix` = young CopySpace + old ImmixSpace + large LOS. Adding a new collector means writing ~hundreds of lines of Rust gluing existing policies, not rewriting an allocator from scratch.
- The host VM ("binding") calls into MMTk through a fixed C/Rust ABI for allocation, write barriers, mutator/GC handshakes, and root scanning. This is how a Ruby VM and a JVM share the same `MarkSweepSpace` implementation.

**LXR** is one such plan: **L**atency-critical **I**mmi**X** with **R**eference counting. It combines:
- **Mark-region heap** (Immix, Blackburn & McKinley 2008): allocations into 32-KB regions with line-granularity reclamation; copying happens *opportunistically* via cursor-based bump allocation into recycled lines.
- **Reference counting as the fast path.** Each object carries a 2-bit RC field in line metadata (0 = free, 1, 2, 3+). Most reclamation comes from RC reaching zero, not from tracing.
- **Temporal coarsening.** Instead of one inc/dec per pointer write, LXR batches modifications per mutator log buffer, so 1000 writes pay ≤ ~10 atomic ops.
- **Concurrent decrements.** When a singly-linked list dies, recursive dec is offloaded to a GC thread, so the mutator never sees a long chain.
- **Backup tracing.** A periodic stop-the-world trace catches cycles and confirms RC-claimed dead objects.

The PLDI 2022 paper showed LXR delivering **lower tail latency than Shenandoah and ZGC** on every latency-critical benchmark tested, while matching G1 throughput. Shenandoah suffered 77% and 37% slowdowns on 1.3× and 2× heaps. The counter-intuitive headline: **a stop-the-world collector can beat concurrent collectors on tail latency**, because concurrent work pollutes mutator caches and bloats the working set.

## §3 Memory-safety property

Same as any modern tracing/RC hybrid: full reachability-precise temporal safety on managed objects. The RC fast path delivers immediate reclamation for the common case; the periodic trace plugs the RC cycle loophole.

LXR adds no new spatial-safety story beyond what the host VM already enforces (bounds checks).

## §4 Production status (May 2026)

- **MMTk itself.** In production-or-near-production for CRuby (the Ruby 3.4 release added modular GC infrastructure, with MMTk as one option). Active research backings: OpenJDK (third-party-heap), V8, Julia, Octave's interpreters, several university VMs.
- **LXR.** Not yet shipped as a default JVM collector, but available as nightly OpenJDK builds (wenyuzhao/lxr-builds) and as a benchmark target for academic comparison. The PLDI 2022 results have not been overturned in any subsequent paper I can find.
- The team has published incremental improvements through 2024-2025 (OOPSLA 2025 "Work Packets") that refine GC-thread scheduling and reduce engineering cost of new plans.

## §5 Cost

- **Throughput.** LXR matches or beats G1 on most workloads (it has G1-class throughput but better latency).
- **Memory.** Mark-region uses ~1 bit per word for metadata; RC adds 2 bits per object. Modest.
- **Latency.** Pauses are short (sub-ms in most measurements) and predictable, because they only do root scan + decrement-list processing.
- **Concurrency cost.** LXR exploits parallelism aggressively (parallel marking, parallel dec processing) but the mutator is single-threaded during a GC pause.
- **Engineering cost.** Implementing a *new* MMTk plan in Rust is genuinely small (compare: implementing a new collector in HotSpot is months).

## §6 Mochi adaptation note

MMTk's **plan-policy separation** is the lesson that ports best to vm3. Today MEP-40 plans:
- One allocator code path per arena type (`AllocString`, `AllocList`, ...).
- One mark-sweep policy in Phase 6, hard-coded.

A policy abstraction would let us, e.g., put `kArenaString` and `kArenaBytes` under a copying compactor (immutable byte arrays compress beautifully) while leaving `kArenaList` and `kArenaStruct` under free-list reuse. Concrete smallest patch:

1. **Introduce a `Policy` interface in `runtime/vm3`.** Methods: `Alloc(size) HandleIndex`, `Free(idx)`, `Mark(idx)`, `Sweep()`, `Compact() (optional)`. Each arena (MEP-40 §6.2) gets a `Policy` field instead of inheriting from a single `Arena` type. Default policy is the existing free-list one. This is a refactor of `arenas.go` and `alloc.go`.
2. **Add a `kPolicyCompact` for immutable byte arenas** in Phase 6. Strings, bytes, and bignum payloads can be compacted because their handles are not pointers and the relocation is internal to the backing slice (the slab index doesn't change, only the in-slab offset for variable-size payloads).
3. **LXR's deferred decrement.** When MEP-41 lands Perceus-style `OP_DROP_HANDLE` (see file 01), append the index to a small ring buffer instead of running `Free` synchronously. A goroutine drains the buffer between mutator slices. This handles the "long unique list collapse" pause hazard without changing the language model.

This does not conflict with Mochi's ethos. Go's runtime owns the backing slice anyway; MMTk-style policy plug-ins are just an internal refactor.

## §7 Open questions for MEP-41

- Should vm3's policy interface be Go-interface-typed (and thus virtually dispatched), or compile-time-monomorphised per arena? The PLDI work-packets paper suggests careful engineering matters more than the interface cost.
- Can we reproduce LXR's "RC + opportunistic trace" exactly, or is a simpler Perceus-style precise RC enough for Mochi's heap shapes?
- Does LXR-style temporal coarsening (batched inc/dec via a log buffer) buy us anything if our RC is precise and statically inserted? Probably no — the win is for imprecise/conservative RC.
- Should the policy abstraction land before or after MEP-40 Phase 6's mark-sweep? Cleanest is before, but it costs schedule.

## Sources

- [LXR PLDI 2022 paper PDF](https://www.steveblackburn.org/pubs/papers/lxr-pldi-2022.pdf)
- [Stop-the-World GC Beats Concurrent: LXR at PLDI'22 (Dangling Pointers)](https://danglingpointers.substack.com/p/low-latency-high-throughput-garbage)
- [mmtk-core on GitHub](https://github.com/mmtk/mmtk-core)
- [Ruby 3.4 Modular GC and MMTk (Rails at Scale)](https://railsatscale.com/2025-01-08-new-for-ruby-3-4-modular-garbage-collectors-and-mmtk/)
- [LXR builds for OpenJDK](https://github.com/wenyuzhao/lxr-builds)
- [Adding GC to Rust-based interpreters with MMTk (Octave Larose)](https://octavelarose.github.io/2025/01/30/mmtk.html)