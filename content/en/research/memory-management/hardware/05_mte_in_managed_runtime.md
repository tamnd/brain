---
title: "MTE in a Managed Runtime"
description: "MTE in a Managed Runtime"
tags: ["memory-safety", "hardware"]
weight: 50
date: 2026-05-18T17:00:00+07:00
---

> Why hardware tags don't save V8/ART/JSC, and what vm3's 12-bit generation already buys us.

## §1 Provenance

- Google V8 Team, "The V8 Sandbox." V8 blog, April 2024. https://v8.dev/blog/sandbox
- Groß (Project Zero), "V8 Sandbox proposal." Issue thread + 2021 design doc, ongoing. https://docs.google.com/document/d/1FM4fQmIhEqPG8uGp5o9A-mnPB5BOeScZYpkHjo0KKA8/edit
- Kim et al., "TIKTAG: Breaking ARM's Memory Tagging Extension with Speculative Execution." USENIX Security 2024. https://arxiv.org/abs/2406.08719
- TIKTAG-v2 in V8 reproduction notes. https://www.emergentmind.com/open-problems/v8-constructible-tiktag-v1-gadget
- Android NDK Arm MTE guide (covers ART integration). https://developer.android.com/ndk/guides/arm-mte
- Apple ARM64e + JavaScriptCore PAC discussion (WebKit commit). https://github.com/WebKit/WebKit/commit/3e3d0883c84955472ece1b2f2e63f31522c5440d
- Vatalloc / VA-Tagging paper (managed-runtime allocator + MTE), 2024-2025 follow-up.

## §2 Mechanism

A managed runtime (V8, ART/Hotspot, JavaScriptCore, CPython, vm3) controls its own allocator and its own object layout. Hardware tagging like MTE can be plugged in at three different layers:

1. **Native heap below the runtime**: every `malloc`/`new` issued by the runtime VM (compiler buffers, parser state, GC bookkeeping) gets MTE-tagged. This is what Android Bionic + Scudo provides automatically on Pixel 8/9 today when the process opts in.
2. **Managed object heap**: the runtime explicitly stamps each managed-heap object with an MTE tag matching the pointer it hands back. Requires changes to the GC: copying GCs must re-tag on relocation; mark-sweep can keep tags stable if free-list reuse rotates them.
3. **Pointer types**: the runtime tags *pointer-bearing fields* in objects so that overwrites via a different tagged pointer trap.

The V8 Sandbox is a *different* mechanism: it confines V8's HeapObject world to a single, large reserved virtual-address region, replaces 64-bit raw pointers inside that region with 32- or 40-bit offsets, and forbids out-of-sandbox dereferences. MTE is **complementary** to the sandbox — V8 has not made MTE the primary mitigation precisely because of the issues in §3.

## §3 Threat model + guarantees

Within a managed runtime, MTE alone has fundamental problems:

- **Side-channel leaks of the tag.** JavaScript, Java and similar languages give an attacker a *precise enough* timing primitive that TIKTAG-class oracles can derandomise the 4-bit tag at any address with ≥95% success in seconds. The V8 team explicitly cited "memory tagging would not be an effective solution because CPU side channels, which can easily be exploited from JavaScript, could be abused to leak tag values" as the rationale for the sandbox.
- **Logic bugs in the JIT.** Half of V8 CVEs are in the optimising compilers (TurboFan, Maglev) and produce well-formed, correctly-tagged accesses that nonetheless do the wrong thing. MTE catches *malformed* accesses, not *misdirected* ones.
- **Tag collisions on hot small-object pools.** Managed heaps reuse objects rapidly; with 4-bit MTE the 1/16 collision rate is reached on every other free.
- **Tag spill across native/managed boundary.** A native C library inside the same process that does not adopt MTE creates a fault-free path to memory that the managed runtime *thinks* is tagged.

What MTE *does* still buy:

- A noise floor against trivially exploitable C-level UAF/OOB in the *unmanaged parts* of the runtime (the parser, the GC's internal data structures, the FFI surface).
- A debugging/testing signal: MTE-SYNC in CI catches a wide class of bugs faster than ASan with much lower overhead.
- Hardening of the V8 Sandbox surface itself — once the sandbox bounds the corruption to V8's heap, MTE on the *external* memory (everything else in the process) ensures sandbox-escape attempts trap.

## §4 Production status (May 2026)

- **V8**: full sandbox implementation went on-by-default for renderer processes in Chrome M118 (Nov 2023) and is now the canonical V8 protection model. MTE is **not** a V8 mitigation. The "MTE on the V8 heap" experiments published in 2023 were dropped after TIKTAG showed the side channel.
- **ART (Android Runtime)**: Google has progressively enabled MTE-async for system_server, zygote, and selected high-risk processes in Android 14 QPR3 → 16. Many user apps remain off-by-default. There is *no published paper* with detailed deployment telemetry as of May 2026 (despite informal reports of "promising" CVE class reduction in Google's internal fleet).
- **JavaScriptCore on Apple Silicon**: Apple does not expose MTE to userspace on M-series chips through May 2026. JSC instead relies on **PAC** (signing JIT-generated control pointers and certain data pointers like TypedArray backing store) plus its own gigacage / ScribbleCage allocator confinement. The combination is functionally analogous to V8's sandbox but uses different primitives.
- **HotSpot / OpenJ9**: experimental MTE patches exist (Red Hat 2024); no production deployment as of May 2026.
- **Microvium under CHERIoT**: the *only* production managed runtime that runs inside a hardware-enforced safety boundary today, courtesy of CHERIoT's compartment substrate (see file 03).

**Headline finding for May 2026**: outside of CHERIoT, no major managed runtime has adopted hardware memory tagging as its primary memory-safety mitigation. Sandboxing (V8) or capability hardware (CHERIoT) carry the load.

## §5 Software emulation cost

For a managed runtime that already pays the cost of an object header, a software tag check is *cheap*:

- vm3-style 12-bit generation in the handle adds one ALU compare and a predictable branch to each `resolve(Cell)`. JIT-inlined, this is typically one extra cycle in the issue stream.
- Java's existing per-object header (mark word + class pointer) already contains room for hashing a generation; some Hotspot JEPs (Lilliput, Project Valhalla) reclaim header bits but in principle the same generation trick is implementable.
- V8's sandbox-offset pointers (32-bit offset + side table) implicitly carry "the right object is at this offset"; adding a generation bump on free is essentially an MTE-software equivalent.

Concretely: Vatalloc (an MTE-aware allocator) reports 1.7-3.05% overhead on top of dlmalloc/jemalloc *with* MTE-tag rotation. Software-only equivalent is approximately the same since the hardware tag is checked free.

## §6 Mochi adaptation note

**vm3 already implements an MTE-superior scheme for managed objects.** The 12-bit generation in each Cell + matching generation in each slab slot is exactly the lock-and-key model, with the following deltas:

| Property                         | MTE on V8 / ART        | vm3 generation                        |
|----------------------------------|------------------------|---------------------------------------|
| Tag width                        | 4 bits                 | 12 bits                                |
| Collision probability            | 1/16 ≈ 6.25%           | 1/4096 ≈ 0.024%                        |
| Check cost                       | hw load+compare (~0)   | sw compare + branch (~1 cycle JIT'd)   |
| Leakable via timing side channel | Yes (TIKTAG)           | Yes in principle but vm3 exposes no JS-class oracle |
| Rotation policy                  | random per `IRG`       | monotonic ++; should it be random?     |
| Native-FFI memory covered        | optional / opt-in      | not covered; out of vm3's TCB          |

The single biggest message for MEP-41: **vm3 is not a JavaScript engine**. The TIKTAG side-channel only matters if the attacker can run a high-resolution-timing workload *inside the same process*. Mochi programs don't get raw access to performance counters; the timer effect is coarse-grained (MEP-15). So the principal failure mode that pushed V8 to a sandbox does not directly threaten vm3.

The remaining concern is the **FFI surface**. If a Mochi binary calls into a native library that corrupts the slab page directly, vm3's generation check fires only if the native code overwrites a Cell-shaped slot in a way that fluffs the generation. A bit-flip that *preserves* the generation field but corrupts a value below escapes. The smallest gap-closer is to keep the slab metadata (where the generation is stored) on a separate page from the slot payload, and `mprotect(PROT_READ)` the metadata page during execution. Native code that scribbles over metadata gets SIGSEGV; benign payload writes proceed.

Reference: MEP-40 §3 (generation sizing), MEP-15 (effect-typed FFI), MEP-16 (null-safety implementations route through the same check).

## §7 Open questions for MEP-41 design

1. Should we **randomise** the generation increment to make TIKTAG-style timing attacks harder, given that JIT'd Mochi code may eventually be embedded in adversarial contexts?
2. Is there a story for **MTE-augmented vm3** when running on Armv9 hardware — i.e., do we delegate slab-page tagging to MTE and shrink our 12-bit gen back down to 4 or 8 bits? The cost/benefit hinges on whether we want a separate FFI tag check.
3. Should we *separate the metadata page* (slot generation + arena tag) from the payload page so the FFI cannot corrupt it without trapping?
4. Should we publish a write-up "vm3 generation = MTE-software, 256x better, no side channel" as part of MEP-41 to forestall the question?
5. If JS engine experience teaches us that JIT/optimiser bugs dominate over raw memory bugs, do we need a "vm3 sandbox" analogue for the JIT'd code path (vm3jit), and how does that interact with the handle check?