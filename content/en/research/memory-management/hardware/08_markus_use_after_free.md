---
title: "MarkUs and quarantine-style UAF prevention"
description: "MarkUs and quarantine-style UAF prevention"
tags: ["memory-safety", "hardware"]
weight: 80
date: 2026-05-18T17:00:00+07:00
---

> Defer reuse of freed memory until it's provably unreferenced. The most direct software analogue to vm3's "bump generation on slot reuse".

## §1 Provenance

- Ainsworth & Jones, "MarkUs: Drop-in use-after-free prevention for low-level languages." *IEEE S&P 2020*. PDF: https://www.cl.cam.ac.uk/~tmj32/papers/docs/ainsworth20-sp.pdf
- MarkUs prototype code. https://github.com/SamAinsworth/MarkUs-sp2020
- Wickman et al., "Preventing Use-After-Free Attacks with Fast Forward Allocation (FFmalloc)." *USENIX Security 2021*. https://huhong789.github.io/papers/wickman:ffmalloc.pdf
- HUSHVAC: "Efficient Use-After-Free Prevention with Opportunistic Page-Level Sweeping." *NDSS 2024*. https://www.ndss-symposium.org/wp-content/uploads/2024-804-paper.pdf
- "S2Malloc: Statistically Secure Allocator for Use-After-Free Protection And More." arXiv 2402.01894 (2024). https://arxiv.org/html/2402.01894v1
- "Safeslab: Mitigating Use-After-Free Vulnerabilities via Memory Protection Keys." *ACM CCS 2024*. https://dl.acm.org/doi/10.1145/3658644.3670279
- Xia et al., "CHERIvoke: Characterising Pointer Revocation using CHERI Capabilities for Temporal Memory Safety." *MICRO 2019*.
- Filardo et al., "Cornucopia: Temporal Safety for CHERI Heaps." *IEEE S&P 2020*.
- Jones, "Addressing Temporal Memory Safety." Cambridge CST blog. https://www.cst.cam.ac.uk/blog/tmj32/addressing-temporal-memory-safety

## §2 Mechanism

The core MarkUs idea is simple:

1. When the program calls `free(p)`, do **not** return the chunk to the free-list. Move it to a **quarantine** list.
2. Periodically (when quarantine exceeds a threshold), pause the mutators briefly and **mark** all live data reachable from registers and the heap. Any quarantine entry that is unmarked = not reachable by any dangling pointer = safe to recycle.
3. Recycled chunks join the regular free list with new contents; chunks still marked stay in quarantine until the next sweep.

This is a Boehm-Demers-Weiser conservative-GC marker run for the *security* benefit, not for collection. The mutator owns `malloc`/`free` semantics; the GC is invisible.

Optimisations (in order of importance):

- **Skip marking for sub-threshold quarantine** — sweep is amortised.
- **Page-granularity unmapping** for large objects — early-free physical memory while quarantine keeps the VA.
- **Two-list small-object specialisation** — small allocations mark separately from large.

Performance results: SPEC CPU2006 mean **1.1x slowdown** (max 2x on `gcc`), **16% memory overhead** on average, never >2x.

FFmalloc's alternative approach: **never reuse a virtual address** at all. Every `free` returns memory to the kernel (or to a "bump-only" arena that grows monotonically). Result: ~2.3% CPU overhead, 61% memory overhead on SPEC CPU2006 — better time, worse memory, and impractical for long-running daemons because VA exhausts.

HUSHVAC (NDSS 2024) refines MarkUs with **opportunistic page-level sweeping**: pages with at least one safe-to-reuse chunk join a sub-page reuse batch list, avoiding global pause. Mean slowdown drops to 4.7% (vs 11.4% MarkUs / -2.1% FFmalloc on their benchmark set).

Safeslab (CCS 2024) replaces marking with **MPK** (Memory Protection Keys): each freed chunk gets a different key, dangling pointers trigger an MPK fault on access. Overhead ~4%.

## §3 Threat model + guarantees

- **Temporal safety against UAF**: complete in the limit (no chunk recycled while a dangling pointer exists). In practice, depends on conservative marking — *integer-typed pointers* in the heap may keep a chunk in quarantine forever (memory leak) without weakening safety.
- **Spatial safety**: not addressed by MarkUs itself; combine with bounds-checker (SoftBound) or hardware (MTE/CHERI).
- **Type confusion**: not addressed.
- **Control-flow**: not addressed.
- **Side channels**: quarantine introduces *delayed-free* timing fingerprints; not a practical exploit channel.
- **Not protected**: a UAF where the attacker can wait long enough for the quarantine to drain *while keeping a dangling pointer alive that the conservative scanner can't see* (e.g., XOR-encoded pointers, pointers in disk files). MarkUs makes "wait it out" exploitation very hard; not impossible.

## §4 Production status (May 2026)

MarkUs itself remains an academic prototype on Boehm-GC. However, the quarantine-with-revocation pattern has gone broad:

- **CHERIvoke / Cornucopia / Cornucopia Reloaded** apply the same idea on CHERI capability hardware: revoke caps pointing to quarantined memory instead of stalling reuse.
- **CHERIoT load-barrier + sweep** ships in commercial silicon (SCI ICENI 2025) — see file 03.
- **FFmalloc**: open-source drop-in `malloc` replacement; some hardening-focused server projects adopt it for short-lived workloads.
- **HUSHVAC** and **Safeslab** are research prototypes (2024); MPK-based variants are seeing real interest because MPK is on every Intel server CPU since Skylake-X.
- **Chromium MiraclePtr** is conceptually similar — a smart pointer that holds a back-reference; freed objects are kept alive until refcount drops. Deployed for most "PartitionAlloc-protected" types in Chrome since 2022.
- **Rust's `Rc<T>` / `Arc<T>`**: trivially gives the same guarantee at the language level for shared ownership.

Quantitative CVE impact: a Google study (cited in PartitionAlloc / MiraclePtr release notes) attributes ~50% of high-severity Chrome renderer CVEs to UAF; MiraclePtr blanket-protects all `raw_ptr<T>`-typed fields; reported field-deployment results show ~95% of attempted UAF exploits trapping on MiraclePtr's `dangling_untriaged` check rather than reaching memory corruption.

## §5 Software emulation cost

Pure-software quarantine costs, as published:

| System         | Time overhead | Memory overhead | Notes                              |
|----------------|---------------|-----------------|------------------------------------|
| MarkUs         | 1.1x          | 16%             | Boehm-GC conservative sweep        |
| FFmalloc       | 2.3% (1.023x) | 61%             | Never reuse VA                     |
| HUSHVAC        | 4.7%          | < MarkUs        | Page-batched sweep                 |
| Safeslab       | 4%            | small           | MPK-based, requires hw MPK         |
| MiraclePtr     | ~3-7%         | small           | Refcounted; deployed in Chrome     |
| Cornucopia/HW  | ~5%           | <1%             | CHERI-augmented                    |

For comparison, **vm3's per-deref generation check** costs effectively zero memory (the generation byte is already in the slot metadata, the bits are already in the Cell) and one predictable branch per dereference — roughly matching MarkUs's amortised cost without the periodic stall.

## §6 Mochi adaptation note

This is the **single most important section across all 10 files** for MEP-41. The MarkUs design articulates *exactly* what vm3 is already doing, plus a fall-back the paper doesn't have.

| MarkUs primitive                                | vm3 / MEP-40 equivalent                          |
|-------------------------------------------------|---------------------------------------------------|
| `free(p)` defers reuse                          | `free(cell)` increments slot generation; slot returns immediately to free list |
| Conservative GC mark to find dangling ptrs       | **No mark needed**: dangling Cells fail the gen check on next deref |
| Quarantine threshold + sweep                    | Not needed; reuse is immediate                   |
| 1.1x runtime, 16% memory                        | ~0% memory; one branch per deref                 |
| Probabilistic recycle (depends on mark accuracy)| **Deterministic** modulo gen-counter wrap (~4096 reuses) |

vm3 trades MarkUs's amortised-pause GC for a per-access check, gaining:

- No mutator pauses ever.
- No conservative-marking precision concerns (we don't need to know which words are pointers).
- Deterministic behaviour at the cost of one ALU compare per Cell deref.
- No 16% memory tax.

vm3 trades MarkUs's "infinite generation" for a 12-bit wraparound. **This is the chief gap.** After 4096 reuses of a slot, the generation field wraps, and a stale Cell with the original generation can spuriously match a recycled slot. MEP-40's mitigation is to **retire a slot from the allocator** after 4096 reuses (or some smaller threshold). For an arena that recycles a slot every microsecond, that's about 4 ms before a retire-and-grow.

The smallest concrete additions for MEP-41:

1. Make the **retire-on-wrap policy** part of the spec (it is implicit today): when a slot's generation field is about to wrap to 0, the allocator removes the slot from the live pool, calls `madvise(MADV_FREE)` on the underlying page if all slots are retired, and grows the slab.
2. Optionally **randomise the generation increment** (skip ahead by 1-7 each free) so an attacker who can leak one generation cannot predict the next reuse generation in O(1) tries.
3. Optionally **disable wrap entirely** by treating wrap as a programmer error / runtime abort; trade memory for safety.
4. Document the relationship to MarkUs explicitly so reviewers understand we are not naively repeating a known-bad pattern.

Reference: MEP-40 §4 (slot retirement), MEP-15 (effects), MEP-16 (null-safety).

## §7 Open questions for MEP-41 design

1. What is the **correct generation width**? 12 bits gives 1/4096 wrap collision; 16 bits gives 1/65536 at the cost of bits taken from arena tag or slab index.
2. Should the generation increment be **monotonic** (predictable, simple) or **random** (harder to derandomise via timing)?
3. Should we offer an **off-switch** for aggressive throughput uses ("trust me, no dangling pointer"), or is the security floor non-negotiable?
4. How do we handle **persistence** — if a Mochi process serialises a Cell to disk and reloads, the slot is gone, but a malicious serialised Cell can still hit the gen check by chance. Do we need an out-of-band "epoch" tied to process start?
5. MarkUs-style sweep would *also* trap dangling pointers stored in unforeseen places (FFI memory). Should MEP-41 add an optional sweep pass for FFI-shared arenas where the gen-check cannot fire?