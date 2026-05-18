---
title: "Arm Morello"
description: "Arm Morello"
tags: ["memory-safety", "hardware"]
weight: 20
date: 2026-05-18T17:00:00+07:00
---

> The first industrial-scale CHERI silicon: a Neoverse N1 retrofitted with 128-bit capabilities, the closeout of UK DSbD.

## §1 Provenance

- Arm Morello programme overview. https://www.arm.com/architecture/cpu/morello
- UKRI, "DSbD Final Impact Evaluation Report", published October 2025. https://www.ukri.org/wp-content/uploads/2025/10/IUK-131025-2025-07-04_DSbD-Final-Impact-Evaluation-Report.pdf
- Watson et al., "CHERI: Hardware-Enabled C/C++ Memory Protection at Scale," IEEE S&P Magazine, July/Aug 2024. https://www.cl.cam.ac.uk/research/security/ctsrd/pdfs/20240419-ieeesp-cheri-memory-safety.pdf
- Grisenthwaite et al., "The Arm Morello Evaluation Platform: Validating CHERI-based Security in a High-performance System." *IEEE Micro*, 2023. https://www.cl.cam.ac.uk/research/security/ctsrd/pdfs/202305ieeemicro-morello-platform.pdf
- Morello Platform Open Source Software portal. https://www.morello-project.org/
- arXiv:2504.17904 (April 2025): "Adoption of the Arm Morello CHERI Platform in Defence: Lessons from a NATO Industrial Demonstrator." https://arxiv.org/pdf/2504.17904
- Sewell et al., "Verified Security for the Morello Capability-enhanced Prototype Arm Architecture." ESOP 2022. https://www.cl.cam.ac.uk/~pes20/morello-proofs-esop2022.pdf

## §2 Mechanism

Morello adapts an **Armv8.2-A Neoverse N1** SoC by adding the CHERI capability model as a new architectural state. The N1 cores are extended with:

- Capability registers `C0-C30`, `CSP`, `PCC`, `DDC` (the "default data capability" used to relocate legacy non-cap loads/stores) — 129 bits wide including tag.
- New instructions: `LDR`/`STR` variants that take a capability base, `SCBNDS` to shrink bounds, `SEAL`/`UNSEAL`, `BLR` via sealed sentry, etc.
- A tag-storage controller in the memory subsystem keeping one tag bit per 128-bit DRAM granule, stored in a reserved physical region.

The capability layout is the canonical CHERI Concentrate 128-bit format: ~18 bits permissions, ~16 bits otype, ~20 bits compressed bounds (mantissa+exponent), 64 bits cursor, plus the side-band tag. Morello drove two ISAv9 design choices: (i) non-monotonic modification clears the tag instead of trapping, (ii) DDC/PCC do not relocate legacy memory accesses by default.

The SoC is dual-cluster, 4-core Cortex-A-class with the Morello extensions, packaged on a development board with 16 GB DDR4 and full peripherals.

## §3 Threat model + guarantees

Same as CHERI ISA in §1 file:

- Spatial safety on every pointer, including pointers crossing DMA via the SMMU when properly configured.
- Pointer integrity via the side-band tag; no software-readable encoding.
- Compartmentalisation via sealed sentries.
- Temporal safety only with a revocation runtime (Cornucopia / Cornucopia Reloaded), not with bare Morello.
- Spectre v1/v2/v4 mitigations are inherited from Neoverse N1; no new side-channel protection from CHERI.
- The April 2025 NATO ICMCIS paper identifies **five new failure modes** specific to Morello deployment if mis-configured: state leaks, memory leaks, UAF, unsafe defaults, and toolchain instability.

Morello does **not** protect against: confidentiality leaks (tag is integrity-only), uninitialised reads, type confusion at the language level, or in-compartment logic bugs.

## §4 Production status (May 2026)

Morello was always a **research prototype**, not a product. As of May 2026:

- The Morello board (silicon date 2021, distribution since early 2022) shipped in the low hundreds of units to academic and industrial partners — Google, Microsoft, Cambridge, Edinburgh, multiple UK SMEs.
- The UK DSbD programme (Innovate UK, EPSRC, Arm, total ~£200M public+private 2019-2024) **closed out in October 2025** with the Final Impact Evaluation Report. Headline numbers: 405 new jobs created (vs. 100 target), £29.6M projected GVA, 80% of TAP survey respondents would consider the Morello board for future products, and a programme-level claim that "DSbD technology can mitigate 70% of known memory-safety vulnerabilities."
- **No follow-on commercial Morello silicon** from Arm. The capability-ISA torch for Arm itself has effectively passed to (a) CHERIoT for embedded and (b) the upstream RISC-V CHERI standardisation work. Arm publicly remains a CHERI Alliance member but has not, as of May 2026, announced a roadmap silicon product carrying Morello-style capabilities.
- The "Morello Industrial Demonstrator" projects (a TAP cohort funded by DSbD) ran 2023-2024 and produced about a dozen ports of real codebases (PostgreSQL, Nginx, parts of FreeBSD userspace, an automotive AUTOSAR stack). Reported porting effort is single-digit percent of LoC changed for clean modern C, growing for code with heavy pointer-int aliasing or DMA.
- IEEE CS awarded the 2024 Best Paper to the CHERI / Morello team's S&P Magazine paper (announced Aug 2025).

## §5 Software emulation cost

Approximating Morello's guarantees in software (e.g., a port of CheriABI to QEMU TCG, or SoftBound+CETS-style instrumentation) costs roughly:

- **2-3x slowdown** on pointer-heavy SPEC workloads with full bounds+temporal checks (CETS+SoftBound).
- **~25% memory overhead** for shadow-pointer metadata (vs. <1% on Morello which uses sideband tag bits).
- **~50-100% slowdown** for QEMU-instrumented capability semantics (this is largely interpreter overhead, not the safety per se).

The Morello papers report **typical 0-5% perf overhead** on hardware for spatial safety alone, climbing to **10-30%** with temporal-safety via Cornucopia. That gap is the canonical "what the hardware buys you" number for any software runtime trying to approximate the same guarantee.

## §6 Mochi adaptation note

Morello's main relevance to vm3 is as the **upper bound on what is possible** rather than as a target. Three takeaways:

1. Morello's 128-bit fat pointer with sideband tag is more expressive than the 8-byte vm3 Cell, but vm3 trades expressiveness for **fixed-shape arena/slab indexing**: bounds are *implicit* (slot size), provenance is the generation. We are essentially Morello-with-omitted-fields, optimised for a single-process managed runtime.
2. Morello's "clears tag on non-monotonic modify" behaviour maps directly to vm3's "stale generation on slot reuse" — we just bump rather than clear. The user-visible effect (next dereference traps) is the same.
3. Where vm3 falls short of Morello: **per-pointer permissions** (no PE/PW/PR/Pseal in our Cell) and **compartmentalisation** (sealed sentries). If MEP-41 wants either, it should look at carving permission bits out of the arena-tag nibble or out of the unused high bits of the slab index, not at widening the Cell.

We should not aim to match Morello's compartment story in software; that's MEP-15 effects' job. We should match its spatial-and-provenance story exactly, which we already do, and document the missing "permissions on the handle" as a deliberate omission justified by the type system.

Reference MEP-40 (handle layout: 4-bit arena tag, 12-bit gen, 32-bit slab index) and MEP-15 (effects as the compartment substitute).

## §7 Open questions for MEP-41 design

1. Should `mochi build` ever target a Morello/X730 backend that maps Cells onto real 128-bit capabilities and elides the software generation check? What's the conformance story?
2. The Morello programme's "70% of CVEs" headline number was a programme-level claim across multiple TAP cohorts, not a per-vuln measurement; can we set a more concrete vm3 acceptance target (e.g., "trap 100% of OSV-DB use-after-free PoCs in a Mochi standard-library port of CPython's `_ctypes`")?
3. Morello's lessons on DMA and SMMU integration: do we need an "untrusted memory" arena class in vm3 for, e.g., `mmap`'d files or shared memory with native peers?
4. Should the Morello porting blockers (state leaks, unsafe defaults, toolchain instability) inform MEP-41's defaults? In particular, should vm3 default to *deny* on any operation that would clear or skip a generation check?
5. Given that Arm has not committed to a Morello follow-on, do we treat Morello as historical and orient MEP-41 toward CHERI-RISC-V (X730/Sonata) instead?