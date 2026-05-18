---
title: "Scudo & friends: hardened allocators in production"
description: "Scudo & friends: hardened allocators in production"
tags: ["memory-safety", "hardware"]
weight: 90
date: 2026-05-18T17:00:00+07:00
---

> The bag-of-tricks malloc (guard pages, sized buckets, randomisation, double-free detection) that ships on every Android device and most of Chrome.

## §1 Provenance

- LLVM, "Scudo Hardened Allocator." https://llvm.org/docs/ScudoHardenedAllocator.html
- Android Open Source Project, "Scudo." https://source.android.com/docs/security/test/scudo
- Serebryany et al., "GWP-ASan: Sampling-Based Detection of Memory-Safety Bugs in Production." *ASPLOS 2024*. arXiv 2311.09394. https://arxiv.org/html/2311.09394v2
- Chromium Project, "GWP-ASan: Sampling heap memory error detection in-the-wild." https://www.chromium.org/Home/chromium-security/articles/gwp-asan/
- Google tcmalloc GWP-ASan docs. https://google.github.io/tcmalloc/gwp-asan.html
- Chromium PartitionAlloc docs. https://chromium.googlesource.com/chromium/src.git/+/HEAD/base/allocator/partition_allocator/PartitionAlloc.md
- struct/HardenedPartitionAlloc fork. https://github.com/struct/HardenedPartitionAlloc
- GrapheneOS `hardened_malloc`. https://github.com/GrapheneOS/hardened_malloc
- mimalloc (Microsoft Research). https://github.com/microsoft/mimalloc
- Trail of Bits, "Use GWP-ASan to detect exploits in production environments." Dec 2025. https://blog.trailofbits.com/2025/12/16/use-gwp-asan-to-detect-exploits-in-production-environments/

## §2 Mechanism

A "hardened allocator" is a userspace `malloc`/`free` that trades some throughput and memory for runtime detection and mitigation of heap-corruption bugs. The toolbox:

- **Sized buckets / size classes**: chunks of the same size class are pooled together. Limits type confusion between objects of wildly different sizes; OOB into a neighbour hits a same-shape neighbour, so corruption is more contained.
- **Per-partition isolation**: high-value objects (e.g., DOM nodes vs. ArrayBuffer storage in Chrome) live in entirely separate VA partitions. Linear overflow can't cross partition boundaries.
- **Guard pages**: every large allocation is `mmap`'d with `PROT_NONE` pages around it; OOB read/write traps. GWP-ASan applies this to a *sampled* subset of all small allocations too.
- **Randomised free-list ordering**: instead of returning the most-recently-freed chunk (which is exactly what UAF wants), pick a random chunk from the free list.
- **Random allocation offset within a page**: GWP-ASan flips a coin to align allocations left or right inside a guarded page, so OOB reads on the wrong side also trap.
- **Header checksumming**: each chunk has a small inline header (size, state, double-free guard) protected by an XOR-style checksum keyed by a per-process secret + the chunk address. Tampering trips a check on `free`.
- **Delayed re-use / quarantine**: like MarkUs but bounded. Each freed chunk waits N other frees before becoming eligible again.
- **Type-aware free**: deallocator must match allocator (`free` vs `delete` vs `delete[]`). Mismatch = abort.
- **Pointer poisoning on free**: payload `memset` to 0xDE so old contents don't leak.
- **Tag integration (Scudo + MTE)**: on Pixel 8/9, Scudo uses MTE if available to stamp each chunk with a hardware tag. Free re-tags. Free MTE = free temporal+spatial detection.
- **Backtrace logging on abort**: shipped crash carries the call stack of the corrupting `free`.

## §3 Threat model + guarantees

- **Heap overflow (linear)**: stopped against guard pages and partition boundaries; merely *detected* probabilistically inside a partition (size-class bucket hides smallish OOB).
- **Use-after-free**: quarantine delays + randomised reuse make exploitation hard, not impossible. MTE integration (Pixel) raises detection to 1/16 per attempt.
- **Double-free**: deterministically detected via state bits in chunk header.
- **Free of invalid pointer**: header checksum traps with very high probability.
- **Heap spray**: less effective due to randomised free list and partition separation.
- **Type confusion**: PartitionAlloc partitions help; Scudo's size classes help less.
- **Side channels**: GWP-ASan introduces a tiny timing bias for guarded allocations; not exploitable. Header secrets are not cryptographic; an attacker with a leak primitive can defeat header checks.
- **Not protected**: deep logic bugs, JIT bugs, anything the allocator isn't on the path of.

## §4 Production status (May 2026)

- **Scudo**: default allocator in **Android 11+** for all non-low-memory devices. Default in **Fuchsia**. Available via Clang `-fsanitize=scudo` for any C/C++ project on Linux. Standalone version in `compiler-rt`. Detection events surface in `logcat` and crash reports.
- **GWP-ASan**: shipping in **Android** since Android 11 (via Scudo) and in **Chrome** on all platforms for malloc and PartitionAlloc. Apple's **Probabilistic Guard Malloc (PGM)** is a sibling: as of Sept 2023, 3748 PGM bug reports filed, **99% fix rate**, only 13 closed without resolution. Trail of Bits Dec 2025 post promotes GWP-ASan for production hardening of arbitrary C/C++ services.
- **PartitionAlloc**: Chrome's per-partition allocator, ~150 partitions covering DOM, ArrayBuffer, etc. MiraclePtr (built on PartitionAlloc) protects `raw_ptr<T>` fields from UAF; >90% of UAF exploit attempts now trap on MiraclePtr in production telemetry.
- **HardenedPartitionAlloc**: third-party fork adding canaries, additional freelist randomisation, delayed-free vectors. Not in mainline Chrome; used by some hardened distros.
- **GrapheneOS hardened_malloc**: ground-up rewrite emphasising security over throughput. Default on every GrapheneOS install (Pixel-only).
- **mimalloc-secure**: build flag in Microsoft's `mimalloc` enabling guards, encoded free list, randomised initial free list. Used in some .NET production deployments.
- **tcmalloc** (Google server-side): GWP-ASan integration documented; per Google docs, default sampling rate keeps CPU overhead negligible, max RAM ~512 KB on x86_64 / 4 MB on POWER.
- **glibc malloc**: has the `MALLOC_CHECK_` family of weaker hardenings; full Scudo replacement is per-project opt-in, no distro default change as of May 2026.

CVE-class evidence: Chrome's MiraclePtr is credited with eliminating a non-trivial fraction of renderer UAFs; PGM's 99% fix rate (Apple) speaks to detection quality. Per Google Security Blog, MTE+Scudo on Pixel catches an "order of magnitude" more bugs than HWASan-only builds.

## §5 Software emulation cost

These *are* the software-only hardening layer. There is nothing cheaper to emulate; they *are* the emulation.

Reported numbers:

- **Scudo standalone**: typically a few percent faster than glibc malloc on multithreaded benchmarks (size-class design wins on contention), with the security-mitigations enabled.
- **GWP-ASan in Chrome**: amortised near-zero overhead at the default sampling rate (~1/4096 allocations).
- **PartitionAlloc**: ~5-10% memory overhead vs jemalloc for the partition bookkeeping; CPU comparable.
- **Hardened mimalloc-secure**: ~5-15% slower than mimalloc-release on alloc-heavy benchmarks.
- **GrapheneOS hardened_malloc**: ~30-50% slower than glibc; trades throughput for security.
- **PGM (Apple)**: <1% CPU on most workloads.

A managed runtime that uses a hardened C allocator under the hood gets these benefits for the *runtime's own* memory (parser tables, GC bookkeeping, etc.) without further work.

## §6 Mochi adaptation note

vm3 sits *above* the underlying Go allocator. Go's runtime allocator (mheap + mcentral + mcache) already does:

- Size-class buckets (matches Scudo's pattern).
- Spans (Go's per-thread cache) reduce contention.
- A simple guard via `mprotect` is available but not used by default.
- No GWP-ASan equivalent in Go's runtime.

The slab arenas that back vm3's Cells are allocated *from Go*. So vm3 inherits some of Scudo's properties (size classes, span isolation) by virtue of being on Go.

What Scudo-style hardening would mean for vm3:

| Scudo trick                    | vm3 / MEP-40 mapping                                  |
|--------------------------------|------------------------------------------------------|
| Size-class buckets             | **Per-type slabs** = one bucket per concrete type     |
| Per-partition isolation        | **Arena tag (4-bit)** chooses which arena owns slot   |
| Guard pages                    | Could `mprotect` boundary pages between slabs         |
| Randomised free list           | We currently free LIFO; could randomise              |
| Header checksum                | The 12-bit generation IS our checksum-equivalent     |
| Quarantine                     | Implicit via generation bump (see file 08)            |
| Pointer poisoning              | Could `memclr` slot on free                          |
| GWP-ASan sampling              | Could allocate 1/N Cells to a guarded sub-arena      |
| Type-aware free                | Trivially: free of wrong-arena Cell is a tag mismatch |

vm3 already gets most of these structurally. The biggest *additions* a hardened-allocator stance would bring:

1. **`memclr`-on-free** of the slot payload. Costs O(slot size) per free; recovers a class of info-leak defences. MEP-40 doesn't mandate this today.
2. **GWP-ASan-style guarded sub-arena** for low-rate sampling. Useful in CI / canary deployments to detect a use-of-stale-cell that snuck past generation collision. Cheap if 1/4096 of allocations.
3. **`mprotect` on the metadata page** so out-of-process / FFI corruption of slot metadata is detected (already raised in file 05).
4. **Randomised generation increment** (also raised in file 08).
5. **Slab-boundary guard pages** between slabs to convert linear OOB writes into SIGSEGV instead of relying on the next-slot generation to also be stale.

Reference: MEP-40 (arena+slab+gen), MEP-15 (effects partition arenas naturally), MEP-16 (null-safety).

## §7 Open questions for MEP-41 design

1. Should vm3 maintain its own arena allocator (MEP-40 today) or delegate to Scudo via cgo when available? The latter gives us free GWP-ASan; the former keeps vm3 portable to non-LLVM toolchains and to Go-only builds.
2. **`memclr` on free**: is the perf cost acceptable? For small Cells (slot ≤ 64 B), it's a single cacheline write. For large object Cells, it's not.
3. Should a fraction of allocations route to a guarded sub-arena (vm3's GWP-ASan)? What's the sample rate, and how is the trap surfaced as a Mochi error?
4. How do we expose the equivalent of Apple's PGM 99% fix rate — a clear, blameable backtrace at the corrupting site, not at the deref site?
5. If we ever build a native Mochi production runtime (not Go-hosted), should it use Scudo, mimalloc-secure, hardened_malloc, or its own thing?