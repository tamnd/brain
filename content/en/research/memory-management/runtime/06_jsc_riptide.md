---
title: "JavaScriptCore — Riptide"
description: "WebKit's retreating-wavefront concurrent garbage collector. Marks objects while JS runs, throttles allocation when it falls behind, and uses logical versioning to skip clearing bitmaps."
tags: ["memory-safety", "runtime"]
weight: 60
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Riptide.** Filip Pizlo and the JavaScriptCore team at Apple. Introduced in WebKit r209827, blog post Jan 30 2017: https://webkit.org/blog/7122/introducing-riptide-webkits-retreating-wavefront-concurrent-garbage-collector/.
- Companion blog from 2022: "Understanding Garbage Collection in JavaScriptCore From Scratch," https://webkit.org/blog/12967/understanding-gc-in-jsc-from-scratch/.
- Related deep dive: "Concurrent JavaScript: It can work!" https://webkit.org/blog/7846/concurrent-javascript-it-can-work/.
- Source: `Source/JavaScriptCore/heap/` in https://github.com/WebKit/WebKit.

## §2 Mechanism

Riptide is a **concurrent, parallel, non-compacting, generational** mark-sweep collector for JS objects in JSC.

Key pieces:

1. **Marking concurrently with the mutator.** The GC threads walk the object graph while JS code runs. To prevent the mutator from "outrunning" the collector, Riptide uses a **retreating-wavefront write barrier**: when JS code writes a reference into a black (marked) object that points to a white (unmarked) object, the barrier *un-marks* (retreats) the parent back to grey, forcing the GC to revisit it. This is the dual of the more common Yuasa snapshot barrier and is what lets Riptide unify concurrent and generational tracking with one barrier.
2. **Conservative root scanning.** The C++ stack, registers, and JIT-spilled locals are scanned conservatively — every word is checked against the heap's object-start bitmap. This means JSC, C++ helpers, and JIT'd code can hold raw object pointers in any local without cooperating with the GC.
3. **Sticky-mark generational mode.** No moving young-gen. Instead, after a full GC the mark bits are *not* cleared; objects with sticky marks are old. An "Eden" collection only walks the unmarked (= newly allocated) set. This emulates generational behaviour without a copying nursery.
4. **Space-time scheduler.** If the mutator is allocating faster than the collector marks, the scheduler shrinks the mutator's time quota until it stalls, falling back to STW as a degenerate case. Without this, JSC measured up to 5× memory blowup.
5. **Logical versioning.** Mark bitmaps are not cleared between GC cycles. Instead, a global "logical version" counter increments. Bitmap reads compare against the version; a stale bitmap is treated as zero until physically cleared lazily on first write. This skips one of the biggest per-cycle costs in a traditional mark-sweep.
6. **Parallel marking across up to 8 threads.**

## §3 Memory-safety property

Reachability-precise temporal safety for JS objects. UAF impossible from the JS surface. Conservative stack scanning means the collector cannot move objects (no compaction), trading some heap fragmentation for the ability to integrate freely with native code.

The **Gigacage** mitigation (a separate JSC feature) sits underneath: typed-array backing stores and JSValue caches live in dedicated 32+GB virtual regions, so a UAF on a JSObject doesn't grant full process-memory R/W.

## §4 Production status (May 2026)

Riptide has been the default JSC collector since 2017 and has shipped in Safari on every Apple device since then. JSC also runs in many embedded contexts (PlayStation, Nintendo Switch firmware historically, various IoT). The 2022 WebKit deep-dive remains the canonical doc; no major architectural overhaul has been published since, although bug fixes and barrier optimisations land regularly.

Note: concurrent GCs are inherently subject to subtle races. Riptide has had several historical CVEs from collector-mutator interleavings (e.g. RET2 / Pwn2Own 2018 in `Array.prototype.reverse`). These are bug-class issues, not design flaws.

## §5 Cost

- **Throughput.** JetStream improved 5% on Riptide's introduction (the splay-latency subtest improved 5×). Riptide costs throughput relative to a perfectly tuned STW collector, but the latency win is enormous for interactive JS.
- **Memory.** Modest barrier metadata; conservative scanning forces non-compacting design so fragmentation can grow on long-running JS contexts.
- **Latency.** Pauses are typically ≤ 1 ms. The space-time scheduler bounds worst-case behaviour even under allocation storms.
- **Cache footprint.** Logical versioning was specifically introduced to fight cache pollution from clearing bitmaps every cycle.

## §6 Mochi adaptation note

Riptide is built for a *dynamically typed*, *conservative-stack-scanning*, *no-cooperation-required-from-JIT* setting — the exact opposite of vm3, which is statically typed and where the host language (Go) owns the GC of backing memory. Several specific lessons still port:

1. **Logical versioning for the mark bitmap (MEP-40 §9.2, Phase 6).** vm3's planned mark-sweep needs to clear mark bits between cycles. Replace per-cycle bitmap clears with a 32-bit "mark epoch" stored in each arena. Each Cell's 12-bit generation already exists; designate, say, 4 of those bits to encode `(epoch & 0xF)` during a cycle. On the next cycle, increment epoch and consider mismatched bits as "unmarked." This is a small change in `arenas.go`.
2. **Space-time scheduler analogue.** If vm3 grows a concurrent sweep goroutine (likely needed once Mochi supports long-running web servers), copy the JSC pattern: when the sweep thread's queue length exceeds a watermark, throttle the mutator's allocation rate by inserting a small `runtime.Gosched()` after every N allocations. This is a one-knob policy.
3. **Retreating-wavefront barrier.** *Not directly applicable* because vm3 doesn't move objects. But the *idea* — that a write into a marked-old object can demote it to grey — is exactly what's needed if Mochi ever adds a generational distinction without a moving nursery.
4. **Conservative scanning.** **Avoid this.** Mochi handles are not pointers, so we have perfectly precise root info from the typed register banks (MEP-40 §6.4). Riptide's conservatism is a tax we don't pay.

No design-ethos conflict; we're cherry-picking the techniques, not the policy.

## §7 Open questions for MEP-41

- Does the logical-versioning trick measurably help if vm3's mark-sweep pauses are already 100 μs on typical heaps? Maybe not at small N, but it scales.
- Should we copy JSC's space-time scheduler verbatim, or is Mochi's predicted heap so much smaller that backpressure is unnecessary?
- Riptide gets a lot of mileage from JSC's bytecode JIT inserting barriers correctly. vm3jit (MEP-40 Phase 5) will face the same problem. How do we *verify* barrier insertion?
- The 2022 deep-dive notes JSC uses lock-free programming heavily. Go's standard `sync/atomic` is enough for our needs, but it's worth checking that no place in `runtime/vm3` makes assumptions Go's race detector will flag.

## Sources

- [Introducing Riptide (WebKit blog, 2017)](https://webkit.org/blog/7122/introducing-riptide-webkits-retreating-wavefront-concurrent-garbage-collector/)
- [Understanding Garbage Collection in JavaScriptCore From Scratch (WebKit blog, 2022)](https://webkit.org/blog/12967/understanding-gc-in-jsc-from-scratch/)
- [Concurrent JavaScript: It can work! (WebKit blog)](https://webkit.org/blog/7846/concurrent-javascript-it-can-work/)
- [WebKit GitHub mirror](https://github.com/WebKit/WebKit)
- [JavaScriptKicks summary of Riptide](https://javascriptkicks.com/stories/100160/introducing-riptide-webkits-retreating-wavefront-concurrent-garbage-collector)