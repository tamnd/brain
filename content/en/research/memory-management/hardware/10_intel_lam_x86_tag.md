---
title: "Intel LAM (Linear Address Masking) and the x86 top-byte-tag story"
description: "Intel LAM (Linear Address Masking) and the x86 top-byte-tag story"
tags: ["memory-safety", "hardware"]
weight: 100
date: 2026-05-18T17:00:00+07:00
---

> Let userspace stash metadata in the unused high bits of a 64-bit pointer. Intel calls it LAM; AMD calls it UAI; Arm has had TBI since v8.0. SLAM (2024) almost killed Linux's LAM support.

## §1 Provenance

- Intel SDM, Vol 3 Ch 7, "Linear Address Masking (LAM)." https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- LWN, "Support for Intel's Linear Address Masking." Aug 2022. https://lwn.net/Articles/902094/
- LWN, "Linear Address Masking enabling." Oct 2022. https://lwn.net/Articles/911572/
- LWN, "Linear Address Masking (LAM) KVM Enabling." May 2023. https://lwn.net/Articles/931504/
- Phoronix, "Linux 6.12-rc5 Disabling Intel's Linear Address Masking 'LAM' Due To Security Concerns." Oct 2024. https://www.phoronix.com/news/Linux-Disabling-Intel-LAM
- Bhattacharyya et al. (VUSec), "Leaky Address Masking: Exploiting Unmasked Spectre Gadgets" (SLAM). *IEEE S&P 2024*. https://download.vusec.net/papers/slam_sp24.pdf
- VUSec SLAM project page. https://www.vusec.net/projects/slam/
- LWN, "SLAM: a new Spectre technique." Dec 2023. https://lwn.net/Articles/953880/
- x86-64-psABI, "Add Intel LAM support" mailing list thread. https://groups.google.com/g/x86-64-abi/c/f8-nrJ8Clbc

## §2 Mechanism

x86-64 architecturally requires linear addresses to be **canonical** — bits above the implemented VA must be sign-extended (47 → bits 48-63 all equal bit 47 in 4-level paging; 56 → bits 57-63 in 5-level). A non-canonical pointer fault on use.

LAM relaxes this: it lets the OS configure, per process (via `arch_prctl(ARCH_ENABLE_TAGGED_ADDR)`), that some of the high bits be **masked off before translation**. The CPU effectively does `addr = addr & ~LAM_MASK` before the page walk.

Two modes:

- **LAM_U57**: leaves bits 0-56 for VA, masks bits 62-57 (6 bits of metadata available). Compatible with 5-level paging.
- **LAM_U48**: leaves bits 0-47 for VA, masks bits 62-48 (15 bits of metadata). Conflicts with 5-level paging.

Bit 63 is excluded because flipping it switches user/kernel halves and would create a privilege issue (AMD's UAI had a related vulnerability, CVE-2020-12965).

Equivalent features:
- **AMD UAI (Upper Address Ignore)**: same idea, slightly different bit layout. Shipped on Zen 4 / Zen 5.
- **Arm TBI (Top-Byte-Ignore)**: bits 63:56 ignored; the original of the family, supported on every AArch64 since v8.0. Linux supports it since 5.4. MTE *piggybacks on* TBI by repurposing 4 of the 8 ignored bits.

Use cases: pointer-tagging in JITs (V8, JSC), userspace sanitisers (HWASan), MTE-software emulation, FFI marshalling that stashes a tenant ID in a pointer.

## §3 Threat model + guarantees

LAM itself **is not a safety mechanism**. It provides a *substrate* for software safety mechanisms (HWASan, MTE-emulation, V8 sandbox, capability schemes) that need free bits.

Direct guarantees: none. LAM doesn't trap on tag mismatch — it discards the tag silently. Software must compare tags itself.

Threats and limitations:

- **SLAM (S&P 2024)** is the headline issue. By loosening canonicality checks, LAM **enables Spectre gadgets that were previously impossible**: pointer-chasing code paths that use a secret as an address (so-called "unmasked" gadgets) now speculatively execute past what was a canonicality fault. Combined with the right disclosure primitive, this lets an attacker leak arbitrary kernel ASCII data through unmasked Spectre v2 gadgets at high rate. Affects Intel LAM, AMD UAI, and Arm TBI on systems without Linear Address Space Separation (LASS).
- The fix is **LASS** (Intel Linear Address Space Separation): enforces that user execution only touches addresses with bit 63 = 0, and kernel execution bit 63 = 1, *even speculatively*. LASS is in hardware on Arrow Lake / Lunar Lake (2024+) but kernel support is incomplete as of May 2026.
- **Linux 6.12 (Oct 2024) disabled LAM by default** because of SLAM. Specifically: `ADDRESS_MASKING` is compile-disabled unless `SPECULATION_MITIGATIONS` is also disabled or `COMPILE_TEST` is set. The practical effect: **LAM is unusable on stock distro kernels through May 2026** despite hardware support on Tiger Lake / Sapphire Rapids / Arrow Lake / Lunar Lake.
- AMD said "use existing Spectre v2 mitigations" rather than disabling UAI; this is widely considered insufficient.
- Arm published guidance for TBI on future cores; existing TBI deployments (e.g., MTE pointer tags) are not directly affected because MTE checks happen *before* speculation reaches the dereference.

So as of May 2026, x86-side pointer tagging is largely **disabled in upstream Linux** until LASS kernel support arrives and stabilises.

## §4 Production status (May 2026)

- **Hardware**: Intel Sapphire Rapids, Emerald Rapids, Granite Rapids, Sierra Forest, Tiger Lake, Alder Lake, Raptor Lake, Meteor Lake, Arrow Lake, Lunar Lake, Panther Lake — all have LAM. AMD Zen 4 / Zen 5 have UAI. Arm v8+ has TBI universally; Arm v8.5+ has MTE on top of TBI.
- **Linux 6.4** (June 2023) merged LAM upstream after Linus's well-publicised rejection of the original 6.2 patches.
- **Linux 6.8** (March 2024) added KVM LAM virtualisation for guests.
- **Linux 6.12-rc5** (Oct 2024) **disabled LAM at compile time** pending LASS. Current Linux mainline (May 2026 ≈ 6.18) still gates LAM behind LASS support, which is itself work-in-progress for the kernel side.
- **glibc / libcs**: have not committed to LAM-aware ABI changes; the existing x86-64 psABI thread is open but not converged.
- **Userspace consumers**: HWASan x86 backend (compiler-rt) supports LAM where the kernel allows; AddressSanitizer's `--use-lam` mode exists but is experimental. V8, JSC, .NET — no production LAM use as of May 2026.
- **Arm TBI**: in continuous production use under MTE (Pixel 8/9) and under iOS/macOS where Apple uses high pointer bits for ObjC class encoding, AOT-compiled tag bits, etc.

The net story: x86 pointer-tagging is **architecturally available, operationally stalled**. The Arm equivalent (TBI under MTE) is **broadly deployed**.

## §5 Software emulation cost

LAM-equivalent in software (without hardware tag-ignore):

- HWASan currently masks pointer tags in software on x86-64 without LAM, costing **~2x runtime** and **~2x memory** (one shadow byte per 16 B). With LAM enabled, HWASan x86 approaches Arm HWASan's ~30% overhead.
- V8 32-bit-offset compressed pointers (V8 Sandbox) use a related but distinct technique: bake the upper 32 bits into a fixed sandbox base, leaving 32 bits for offsets. Cost: ~5-15% slowdown vs raw pointers; recovered on memory.
- ASan on x86 *without* LAM: ~2x slowdown, 8x memory shadow; "production-usable" only with sampling.
- Generic top-bit-tag software emulation: pay one masking instruction per dereference, ~1-3% slowdown if predictable.

So LAM is worth a meaningful 1-2x of perf for sanitiser-class consumers, and substantially less for any consumer that already pays a software mask.

## §6 Mochi adaptation note

LAM is a *substrate*, not a property. vm3's Cell already encodes its arena+gen+idx in an 8-byte word; we do not need pointer high bits because we don't store native pointers in the Cell. So LAM as such is **not a direct fit for vm3 on x86**.

Where LAM-class features become interesting:

1. **If vm3 ever interns a raw Go pointer in a Cell** (e.g., for FFI handles), the upper bits are available for a tag, and LAM/TBI would let us use them without explicit masking on dereference. We chose not to do this in MEP-40 to keep the Cell a fixed-shape index; LAM doesn't change that decision.
2. **If we adopt MTE (Arm)** in some future Mochi-on-Pixel target, TBI is what makes MTE pointer tags free; this is already covered in file 04.
3. **For vm3jit code on Arm**, we may want to use TBI for the JIT's own internal book-keeping (e.g., closure-environment back-pointer tagging) — same caveat as JSC's PAC: the JIT must hold the masking primitives behind an interface.
4. **SLAM lesson**: any future Mochi feature that gives user code high-precision *timing* access (e.g., a benchmark effect with rdtsc-granularity) could enable Spectre-style oracles against any Cell-tag scheme. The current spec exposes only millisecond timers (MEP-15 timer effect), which is too coarse for SLAM-style derandomisation. We should keep it that way unless we have a strong reason to relax.

Where vm3 *falls short*: nothing related to LAM. The 8-byte Cell carries its own metadata in dedicated bit-fields, not in pointer high bits, so the LAM debate is largely orthogonal.

References: MEP-40 (Cell as index, not pointer), MEP-15 (effects, including timer granularity), MEP-16 (null-safety).

## §7 Open questions for MEP-41 design

1. Do we ever want a "wide cell" that *is* a tagged native pointer, e.g., for zero-copy FFI to Go slices? If so, we'd lean on TBI on Arm and (eventually) LAM-via-LASS on Intel.
2. The SLAM CVE class makes us cautious about **giving Mochi programs fine-grained timing**. Should MEP-41 explicitly cap timer resolution as a security invariant?
3. Should vm3jit emit different code on `LAM=on` vs `LAM=off` machines (saving an explicit mask instruction)? Probably not worth the complexity given LAM's stalled deployment.
4. If we ever build a Mochi-on-bare-metal port, do we want to *use* LAM (or TBI) for our own slab metadata, freeing a few bits in the Cell?
5. Given that x86 LAM is effectively disabled in Linux until LASS arrives, should we treat LAM as a non-feature for the foreseeable future and document Arm TBI as the only pointer-tag substrate we'd consider supporting?