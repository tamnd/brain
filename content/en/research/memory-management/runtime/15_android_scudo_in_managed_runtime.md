---
title: "Android Scudo + MTE inside ART"
description: "The canonical \"secure allocator inside a managed runtime.\" Scudo is Android's hardened native heap, used for ART's non-managed allocations (JIT code, off-heap buffers, JNI). Pairs with ARM MTE on Armv9 hardware for hardware-checked tagging. Default for all native allocations on Android since 11."
tags: ["memory-safety", "runtime"]
weight: 150
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Scudo.** Originally LLVM's hardened allocator (sub-project of compiler-rt's sanitizer family). Maintainer: Kostya Kortchinsky and others. Brought to Android by Google.
- AOSP doc: https://source.android.com/docs/security/test/scudo.
- Android Developers blog: https://android-developers.googleblog.com/2020/06/system-hardening-in-android-11.html (Scudo default from Android 11).
- **Arm MTE.** Armv8.5-A feature, mainline in Armv9. AOSP: https://source.android.com/docs/security/test/memory-safety/arm-mte. Android Developers: https://developer.android.com/ndk/guides/arm-mte.
- LLVM review for MTE in Scudo: https://reviews.llvm.org/D70762.
- Security analyses: WOOT 2024 — "Exploiting Android's Hardened Memory Allocator" (Mao et al.); DARKNAVY 2024 — MTE comparison across PartitionAlloc, Ptmalloc, Scudo.
- Bionic MTE doc: https://android.googlesource.com/platform//bionic/+/07658227385ce0f294a22e76b904470dc46d289e/docs/mte.md.

## §2 Mechanism

**Scudo** is a size-class, segregated-fit allocator with hardening features:

- **Primary allocator**: blocks of slabs, each slab dedicated to a single size class. Allocations from a class are 16-byte aligned (for tag-granule compatibility).
- **Secondary allocator**: large allocations (≥ 1 page). Each large allocation is page-aligned and surrounded by guard pages.
- **Quarantine**: freed chunks are not immediately reused; they sit in a quarantine list for some interval to delay UAF reuse.
- **Header integrity**: each chunk has a header with a checksum derived from a process-secret; corruption is detected on free.
- **Randomised allocation order** within slabs.

ART (Android Runtime) uses Scudo for *all native allocations*: JNI buffers, native libraries, JIT-compiled method code, internal data structures. The Java heap is managed separately by ART's own moving GC (CC: Concurrent Copying). So "Scudo inside a managed runtime" means: the managed (Java) side has its own GC and its own safety story; the unmanaged (C/C++ native) side, which is just as exploitable, is hardened by Scudo.

**Arm MTE** (Memory Tagging Extension) is the hardware piece. Each 16-byte memory granule carries a 4-bit tag in side metadata. Each pointer to that memory carries the same tag in its high bits (uses ARM's Top-Byte-Ignore feature). On every load/store, the CPU compares the pointer tag against the memory tag; mismatch → `SIGSEGV` (mode-dependent: sync or async).

Scudo + MTE integration:
- On `malloc`: allocate a chunk, generate a random non-zero tag, tag both the memory granules and the returned pointer with that tag.
- On `free`: generate a *new* random tag, tag the freed granules with it. The old pointer (now stale) carries the old tag → tag mismatch → UAF detected.
- **Granules adjacent to the allocation** are tagged with `0` (which the random allocator avoids), so linear OOB triggers a deterministic mismatch.

Two operating modes for production:
- **SYNC mode**: fault on every mismatch. Higher overhead, deterministic bug reports. Used in development and on hardened apps.
- **ASYNC mode**: defer fault to next kernel entry. Lower overhead, less precise reports. Used in production for tolerable-overhead deployments.

## §3 Memory-safety property

Scudo alone:
- **Spatial safety**: probabilistic on linear OOB (guard pages catch large overflows; quarantine + randomisation catch small).
- **Temporal safety**: probabilistic on UAF (quarantine delays reuse).
- **Header integrity**: detects naive heap corruption.

Scudo + MTE:
- **Spatial safety**: *deterministic* for linear OOB into the adjacent granule (tag 0 trap).
- **Temporal safety**: ~93% probability of UAF detection (1 - 1/16 chance the new tag collides with the stale one).
- **Buffer overflow into next chunk**: detected because chunks have alternating tags.

This is the strongest *managed-runtime + native-allocator* safety story shipping in production.

## §4 Production status (May 2026)

- Scudo is default for native allocations on Android since 11 (2020). Hundreds of millions of devices.
- WOOT 2024 audit of 15 devices found 6 use Scudo, 9 still on jemalloc (low-memory tier).
- MTE shipped first in Pixel 8 (Tensor G3, late 2023) and is on every Armv9-capable Android device thereafter. MTE in *production user-facing apps* is opt-in via app manifest.
- DARKNAVY (Jan 2024) compared MTE deployments in PartitionAlloc (Chrome), Ptmalloc (glibc), and Scudo (Android). Scudo's choice of "tag 0 for chunk headers + alternating tags for adjacent chunks" was identified as the strongest spatial-safety story.
- 2024 WOOT paper showed bypass techniques exist for Scudo given adequate memory-corruption primitives, so the assumption is "raises the bar," not "eliminates the class."

## §5 Cost

- **Scudo without MTE**: ~5-10% perf cost vs jemalloc on typical workloads; ~10-20% memory cost from quarantine + guard pages.
- **MTE SYNC**: ~5-15% additional perf cost on memory-heavy code (every load/store does the tag check). High-bandwidth memory workloads see more.
- **MTE ASYNC**: ~1-3% additional perf cost. Recommended for production.
- **MTE storage**: 4 bits per 16-byte granule = 3.125% memory overhead, in dedicated kernel-managed tag memory.

## §6 Mochi adaptation note

The Scudo + MTE pattern is **the most directly relevant defence-in-depth example for vm3**, because the architecture splits exactly the way Mochi does:

- **Managed side (Java / Mochi)**: typed objects, traced GC or RC, structurally safe.
- **Unmanaged side (native C++ / Go)**: backing memory for the managed heap, plus FFI buffers and JIT code.

vm3's split:
- Managed side: Cell-handle indexed slabs (MEP-40 §6.1, §6.2). Spatial + temporal safety by construction (handle generation tag + accessor bounds checks).
- Unmanaged side: Go-allocated slab backing slices, JIT code cache, ffi buffers if any.

Adaptation:

1. **MTE-style "tag" reuse for free-list slots (MEP-40 §6.2, §9).** The vm3 Cell's 12-bit generation field already serves as a temporal tag — bump it on every `Free`, check it on every accessor. This is MTE's pattern, implemented in software, with 12 bits instead of 4 (much smaller collision probability: 1/4096 vs 1/16).
2. **Quarantine for `kArenaList` and `kArenaStruct`.** Scudo's idea: don't reuse a freed slot immediately. Instead push it onto a FIFO queue of size K (say, 64 entries). Only reuse after the queue is full. Catches UAF that races with the next allocation. Tiny patch to `runtime/vm3/alloc.go`: change the free-list from a LIFO stack to a quarantine ring.
3. **Guard the JIT code cache.** vm3jit (Phase 5) should allocate its code cache via `mmap` with guard pages on each side (analogous to Scudo's secondary allocator). This catches OOB writes from JIT bugs.
4. **No MTE hardware reliance.** Mochi can't assume Armv9 MTE because:
   - Most user devices don't have it yet (developers' laptops are Apple Silicon, no MTE).
   - Go doesn't natively support MTE-tagged pointers.
   - vm3's handle isn't a pointer in the first place.
   So we get MTE's *property* (tag-based UAF detection) from the generation field, in pure Go, on every platform.

There is **no design conflict** with Mochi's ethos (static-typed, Go-hosted, no cgo). The lesson is: the design pattern is right; the implementation can be pure Go because we already have a software analogue.

## §7 Open questions for MEP-41

- Is a quarantine layer between `Free` and reuse worth the modest memory cost? Suggest measuring on Mochi corpus first.
- The generation field is 12 bits, so the wrap-around period is 4096 reuses per slot. On a hot slot (e.g. a slot reused in a tight loop), this could wrap in milliseconds. Do we need to either (a) widen to 16 bits, (b) refuse reuse after wraparound, or (c) burn the slot on wrap?
- Should vm3 ever expose MTE on supported hardware as an *additional* layer (defence in depth)? Possible but requires cgo and a per-arch path. Not worth it for v1.
- For JIT code cache: guard-page-protected vs `MAP_JIT` exclusive — what's the right combination? See file 13 for the W^X discussion.
- Scudo's "header integrity checksum" pattern: any value for vm3? Probably no — handles aren't pointers, so they don't have headers to corrupt.

## Sources

- [Android — Scudo (AOSP)](https://source.android.com/docs/security/test/scudo)
- [Android — Arm Memory Tagging Extension](https://source.android.com/docs/security/test/memory-safety/arm-mte)
- [Android NDK — Arm MTE Guide](https://developer.android.com/ndk/guides/arm-mte)
- [Bionic — MTE Implementation Documentation](https://android.googlesource.com/platform//bionic/+/07658227385ce0f294a22e76b904470dc46d289e/docs/mte.md)
- [Exploiting Android's Hardened Memory Allocator (WOOT 2024)](https://nebelwelt.net/files/24WOOT.pdf)
- [DARKNAVY — MTE in Heap Allocators (Jan 2024)](https://www.darknavy.org/blog/strengthening_the_shield_mte_in_memory_allocators/)
- [LLVM Review D70762 — Scudo initial memory tagging support](https://reviews.llvm.org/D70762)
- [Android Developers Blog — System Hardening in Android 11](https://android-developers.googleblog.com/2020/06/system-hardening-in-android-11.html)
- [Arm — MTE User Guide for Android OS](https://documentation-service.arm.com/static/660d6857aec7154a17ee1c5f)