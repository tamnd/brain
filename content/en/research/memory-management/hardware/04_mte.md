---
title: "Arm MTE"
description: "Arm MTE"
tags: ["memory-safety", "hardware"]
weight: 40
date: 2026-05-18T17:00:00+07:00
---

> Per-16-byte 4-bit lock-and-key tags on every allocation granule, in Armv8.5-A and shipping on Pixel 8/9.

## §1 Provenance

- Arm, "Armv8.5 Memory Tagging Extension," whitepaper (2019, rev. 2023). https://developer.arm.com/documentation/108035/latest/Introduction-to-the-Memory-Tagging-Extension
- Serebryany et al. (Google), "MTE: The promising path forward for memory safety." Google Security Blog, Nov 2023. https://security.googleblog.com/2023/11/mte-promising-path-forward-for-memory.html
- Google Project Zero, "First handset with MTE on the market." November 2023. https://projectzero.google/2023/11/first-handset-with-mte-on-market.html
- Android Open Source Project: Arm MTE. https://source.android.com/docs/security/test/memory-safety/arm-mte
- Android NDK guide: Arm Memory Tagging Extension. https://developer.android.com/ndk/guides/arm-mte
- Kim, Jang, et al. "TIKTAG: Breaking ARM's Memory Tagging Extension with Speculative Execution." USENIX Security 2024. https://www.theregister.com/2024/06/18/arm_memory_tag_extensions_leak/
- Blumbergs, "Memory Tagging Extension in 2025 — what actually works." Sept 2025. https://medium.com/@e.blumbergs/memory-tagging-extension-in-2025
- Göbel, "Introduction to Arm Memory Tagging Extensions." Sept 2025. https://thore.io/posts/2025/09/introduction-to-arm-memory-tagging-extensions/

## §2 Mechanism

MTE is an Armv8.5-A architectural extension (carried into v9 baseline) that introduces:

- A **16-byte tag granule** of physical memory. Every aligned 16 B chunk has an associated **4-bit allocation tag** (the "lock") stored in a separate physical tag region (hidden from data loads/stores).
- A **4-bit address tag** placed in pointer bits **[59:56]** (the high byte, leveraging the existing Top-Byte-Ignore convention).
- On every load/store, the CPU compares pointer-tag against the granule's allocation-tag. Mismatch raises a **synchronous** or **asynchronous** tag check fault depending on `TCR_EL1.TCMA*` configuration.
- Tag-generation instructions `IRG` (random tag) and `ADDG`/`SUBG` (arithmetic with tag) plus `STG`/`STZG` (set tag) / `STGM` (multi-granule set) let the allocator stamp tags efficiently. `LDG` reads the current tag.
- Tag carry-through: MTE is integrated with the data cache. Tags ride alongside cache lines; eviction writes them to a kernel-reserved DRAM region.

Three operating modes:

1. **SYNC** — tag mismatch SIGSEGV with `SEGV_MTESERR`, full fault address. Used in production where the cost is acceptable, used in dev/test always.
2. **ASYNC** — mismatch logged in registers but execution continues until the next kernel entry; SIGSEGV `SEGV_MTEAERR` without fault address. Low overhead (~5-10%).
3. **Asymmetric** (Armv8.7-A): sync on loads, async on stores. Currently recommended by Google over plain ASYNC.

Linux kernel KASAN-HW uses MTE for kernel-side detection (since 5.10) and HWASan uses MTE for userspace under Android.

## §3 Threat model + guarantees

- **Spatial safety (probabilistic)**: a linear OOB into a *differently-tagged* neighbour traps. Same-tag neighbours collide with probability 1/16.
- **Temporal safety (probabilistic)**: on `free`, the allocator re-tags the granule, so a dangling pointer with the old tag traps on next use. Collision again 1/16 in the worst case; in practice MTE allocators rotate tags to maximise distance.
- **Type confusion / control-flow / side-channel**: **not** protected by MTE. PAC+BTI cover CFI; MTE covers memory tagging only.
- **Side channels**: TIKTAG (USENIX Sec 2024) shows two speculative-execution gadgets (v1/v2) that derandomise the 4-bit allocation tag at any address in <4 s with >95% success against Chrome processes on Pixel 8, by observing prefetch-induced timing variations after a tag-check fault. Google bug-bountied and patched the userspace impact; the architectural class remains.
- **Not protected**: information disclosure (tag is integrity), uninitialised reads, logic bugs, JIT-spray once an attacker can leak tags.

## §4 Production status (May 2026)

- Hardware: every Arm v9 Cortex-A core supports MTE (A510, A710, A715, A720, X2-X4, A725, X925, plus Apple's M3/M4 for kernel use; Apple has historically not exposed MTE to userspace).
- **Pixel 8 (Oct 2023)** was the first commercial handset with MTE exposed. **Pixel 9** (2024) and **Pixel 10** (2025) continue support via Tensor G3/G4/G5. MTE remains **opt-in via Developer Options** in stock Android 14/15/16 — not on by default for arbitrary apps. The Android Runtime (ART), Bionic libc, and some system services run MTE-on by Google.
- **GrapheneOS** has MTE-by-default for the OS and any opting-in apps since 2023.
- Android version support: stack-tagging added in **Android 14 QPR3** (mid-2024); heap-tagging on by default for many Google-built apps in Android 15.
- Linux kernel: KASAN-HW since 5.10; user-mode HWASan on AOSP toolchains.
- **Glibc MTE** integration: ongoing — Glibc 2.39 (Feb 2024) shipped some support; production-default still off for most distros; Ubuntu 24.04 LTS treats MTE as opt-in via `glibc.malloc.mta_*` tunables on supported hardware. Android Bionic is the integrated baseline.
- **Google's "MTE in production" data**: not a single canonical paper as of May 2026, but the Project Zero Nov 2023 post and the 2024 security blog give the substantive deployment claims — MTE reduced a class of bugs by an unspecified large factor in Pixel internal fleet tests; specific CVE-elimination percentages are not published openly.
- TIKTAG and follow-up SCA work demonstrate that **MTE alone cannot defend against an attacker with a JIT/sandbox-side timing oracle**; this is the published consensus driving V8's "sandbox + MTE" hybrid (see §5 doc).

## §5 Software emulation cost

A pure-software MTE analogue (HWASan in software-only mode, AddressSanitizer, Valgrind, MarkUs-style quarantine):

- **HWASan software (no MTE hardware)**: ~2x slowdown, ~2x memory (one shadow byte per 16 B + compiler instrumentation on every load/store).
- **ASan**: ~2x slowdown, ~3x memory, 8x-shadow scheme. Used for testing, not production.
- **MarkUs quarantine** for temporal-only: 1.1x geomean, peak 2x; 16% memory overhead.
- **FFmalloc** (never-reuse-VA, related to MTE temporal goal): ~2.3% CPU but 61% memory on SPEC.

Compared with MTE hardware (typically **<5% time, ~3% memory** in async / asymmetric mode on Pixel 8), the software gap is roughly **2-3 orders of magnitude on time** and 1-2 on memory. This is why MTE is interesting to deploy even though its protection is probabilistic.

## §6 Mochi adaptation note

vm3's **12-bit generation in the Cell is essentially MTE-in-software, with 256x more collision resistance** (12 bits vs MTE's 4) at the cost of one extra check per dereference. Direct mapping:

| MTE                                  | vm3 Cell                                       |
|---------------------------------------|------------------------------------------------|
| 4-bit address tag in pointer bits     | 12-bit generation in Cell                      |
| 4-bit allocation tag per 16 B granule | 12-bit generation in slab slot metadata        |
| Tag-mismatch trap on dereference      | Generation-mismatch check in handle resolve    |
| Tag rotation on free                  | Generation bump on slot reuse                  |
| 1/16 collision rate                   | 1/4096 collision rate                          |
| Hardware-checked, ~<5% overhead       | Software-checked, ~one branch per deref        |

Quantitatively: where MTE allows a UAF on the same slot to succeed with probability ≈ 6.25% (1/16), vm3's 12-bit generation makes that ≈ 0.0244% (1/4096) — about 256x better. The cost is the explicit check; on a JITted hot path that branch is one predictable compare. Where the MEP-40 design already pays off most strongly, MTE provides essentially nothing extra; where MEP-40 might want to drop the check (e.g., behind a "known-fresh" optimisation), MTE-on-native could be a fallback safety net.

**MTE is most interesting to us not as something to copy but as something to inherit.** If a Mochi binary is JITted to AArch64 v8.5+ and runs under an MTE-enabled allocator, the *Go-allocated slab pages themselves* gain MTE protection against C-level corruption — useful for the FFI boundary even though vm3 itself is already covered by the generation check.

Where vm3 *falls short*: we have no protection against **bit-flip / Rowhammer attacks on the slab metadata itself**. MTE doesn't either, really, but its tag is sideband. Closing this gap would mean storing the slot generation in a separate page guarded by `mprotect` or in MTE-tagged memory when available.

References: MEP-40 (the 12-bit gen sizing decision), MEP-16 (null-safety which already routes through generation check).

## §7 Open questions for MEP-41 design

1. Do we ever want to *shrink* the 12-bit generation? MTE got away with 4 bits because the OS rotates tags well; if our scheduler does aggressive arena recycling, can we drop to 8 bits and reclaim 4 bits for permissions?
2. Should the vm3 generation increment be **random** (MTE-style IRG) rather than monotonic, to defeat predictability attacks on long-running processes?
3. If we run on MTE hardware, do we route Go slab allocations through `mte_tag_region` so the underlying memory also gets hw-tagged?
4. TIKTAG-style side channels exist when an attacker has a fast timing oracle. vm3 currently has no such oracle exposed — should MEP-41 explicitly forbid features that would create one (high-resolution timers, certain debug effects)?
5. Is there a meaningful integration story with **kernel MTE** for the Go runtime page heap that backs our slabs?