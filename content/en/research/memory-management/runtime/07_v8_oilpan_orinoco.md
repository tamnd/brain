---
title: "V8 — Orinoco + Oilpan"
description: "Chrome's two cooperating collectors. Orinoco runs V8's young-generation JS heap in parallel; Oilpan is Blink's traced C++ GC, recently hosted inside V8 as a library, learning to do generational collection with conservative stack scanning."
tags: ["memory-safety", "runtime"]
weight: 70
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Orinoco.** V8's collector family — concurrent and parallel marking, parallel Scavenger young-gen. Blog posts: https://v8.dev/blog/orinoco-parallel-scavenger, https://v8.dev/blog/trash-talk, https://v8.dev/blog/concurrent-marking.
- **Oilpan.** Blink's traced C++ GC, originally in `third_party/WebKit/Source/platform/heap/`, migrated to V8 as a library since V8 v9.4 (2021): https://v8.dev/blog/oilpan-library. Design doc: https://chromium.googlesource.com/chromium/src.git/+/65.0.3283.0/third_party/WebKit/Source/platform/heap/BlinkGCDesign.md.
- May 2026 status overview: Andy Wingo, "The last couple years in v8's garbage collector," https://wingolog.org/archives/2025/11/13/the-last-couple-years-in-v8s-garbage-collector/.

## §2 Mechanism

V8 manages two heaps that the user mostly can't tell apart:

1. **V8 JS heap, managed by Orinoco.** Generational, partly-concurrent, partly-parallel:
   - **Scavenger (young gen).** Copying semispace collector. Parallel — multiple GC threads cooperatively evacuate. JEPs in trees not relevant; the design is from the V8 team's `v8.dev` blog.
   - **Mark-Compact (old gen).** Concurrent marking (most work done off the main thread, with write barriers tracking mutator updates) plus parallel compaction during STW pauses.
   - Numbers from the original Orinoco rollout: parallel Scavenger cut young-gen processing time **20-50%**; idle-time GC reduced Gmail's used heap by **45%**; concurrent marking+sweeping cut WebGL pauses **up to 50%**.
2. **Oilpan, the Blink C++ heap.** Trace-based, used for every DOM node, every CSS rule object, every Blink runtime object. Marking is concurrent; sweeping interleaves with the renderer. Oilpan is **precise on the heap and conservative on the native stack** — it knows where Member<T> fields live in C++ objects but treats stack words as ambiguous roots.

The 2021-2025 work focused on:
- Carving Oilpan out of Blink and hosting it inside V8 (`v8/include/cppgc/`). This let Blink share infrastructure (work queues, GC threads, scheduler) with V8's main heap.
- Adding **generational Oilpan**, which required solving how to promote-pin objects whose only references are conservative stack pointers.
- Replacing V8's `Handle<T>` API with **DirectHandle** in 2024-2025: the original `Handle<T>` was a double-indirection (handle scope → pointer → object) precisely because conservative scanning couldn't keep up with raw pointers. The new direct-handle scheme leverages improved Oilpan tracking to give zero-overhead handles in C++.
- Preparing for **multi-threaded mutators** to support WebAssembly's shared memory + GC interaction.

## §3 Memory-safety property

Orinoco gives the standard tracing-GC guarantee on JS heap objects. Oilpan extends the same guarantee to Blink's C++ object graph: a `Member<Node>` is always live as long as the holder is reachable, so the historical class of Blink UAFs in DOM operations is structurally prevented. The cost is that all heap-resident C++ objects must inherit `GarbageCollected<T>` and use `Member<T>` instead of raw pointers.

What this *does not* defend against is V8 sandbox escapes via type confusion on the JS heap — that's what the V8 Sandbox (file 08) addresses.

## §4 Production status (May 2026)

- Orinoco ships in every Chrome, Edge, and Chromium-derived browser. Hundreds of millions of users daily.
- Oilpan is shipped in every Chromium since ~2014, hosted in V8 since 9.4 (2021). All Blink-managed C++ objects are Oilpan-managed.
- The generational Oilpan + DirectHandle work has been merged but, per Andy Wingo's Nov 2025 retrospective, the user-facing rollout (e.g. promotion-pinning under conservative scan) is gated behind a Finch experiment for a fraction of users as of late 2025. Full default-enable is plausibly 2026-H1.
- New 2024-2026 priorities split roughly: **~20% V8 Sandbox, ~40% Oilpan Odyssey, ~20% multi-mutator preparation**, rest scheduler/heuristics.

## §5 Cost

- **Throughput.** Optimised aggressively; concurrent marking moves >80% of marking off the main thread.
- **Memory.** Generational + compacting means V8's heap is dense; Oilpan adds modest per-object header overhead.
- **Latency.** Headline-grade. Scavenger pauses ≤ 1 ms on typical pages. Old-gen STW compaction can hit 10-50 ms on pathological pages, but background concurrent marking minimises this.
- **Engineering cost.** Massive. V8 is the largest production GC codebase in the JS ecosystem.

## §6 Mochi adaptation note

V8's two-heap design has a parallel in vm3's typed arenas: each arena (MEP-40 §6.2) is its own little heap. But the directly applicable lessons are narrower:

1. **Concurrent marking with write barriers.** Phase 6's mark-sweep (MEP-40 §9.2) is currently STW. The smallest patch to make it concurrent: a Go channel-based work queue for the GC goroutine, plus an `OP_WRITE_BARRIER` emitted by compiler3 wherever a slab field is overwritten. The barrier records the target index into a per-mutator log. The GC re-marks logged objects at the start of each handshake.
2. **Generational discipline at the slab level.** V8's Scavenger semispace doesn't map onto vm3 (we don't move objects), but the *idea* of "most objects die young" justifies biasing free-list reuse toward young slabs. Each arena's free-list becomes two lists: `freeYoung` and `freeOld`. Reuse pops from `freeYoung` first; survivors-from-mark-sweep migrate to `freeOld`. Simple bookkeeping, big win on allocation-heavy code.
3. **Oilpan-style "host-managed C++ heap."** This is what Go gives us for free. The Mochi user never sees a raw pointer; the host (Go runtime) owns the backing slices; the VM owns slot liveness. So we already have V8's *future* state (host-cooperating C++ GC) with zero engineering work. This is worth calling out in the MEP-41 motivation.
4. **DirectHandle.** Mochi's 8-byte Cell handle (MEP-40 §6.1) *is* V8's DirectHandle: a direct, fixed-size, unstable-in-memory-but-stable-in-name reference. We win this round.

No conflict with the design ethos.

## §7 Open questions for MEP-41

- Does concurrent marking buy anything for typical Mochi corpus sizes (KB-MB heaps)? STW mark of a few thousand slab entries is microseconds.
- Do we want a young/old slab split inside each arena, or should that wait until empirical evidence of survivor accumulation?
- Is there a Mochi analogue of "Oilpan multi-mutator readiness"? Today vm3 is single-threaded per VM, but if Mochi grows goroutine-style concurrency, the arena code needs `sync.Mutex` or per-goroutine sub-arenas.
- The Andy Wingo retrospective notes that V8's GC team is small and pulled in many directions. What's our staffing reality for the equivalent Mochi work?

## Sources

- [Orinoco: young generation garbage collection (V8 blog)](https://v8.dev/blog/orinoco-parallel-scavenger)
- [Trash talk: the Orinoco garbage collector (V8 blog)](https://v8.dev/blog/trash-talk)
- [Oilpan library (V8 blog)](https://v8.dev/blog/oilpan-library)
- [Blink GC Design doc](https://chromium.googlesource.com/chromium/src.git/+/65.0.3283.0/third_party/WebKit/Source/platform/heap/BlinkGCDesign.md)
- [The last couple years in V8's garbage collector — wingolog](https://wingolog.org/archives/2025/11/13/the-last-couple-years-in-v8s-garbage-collector)