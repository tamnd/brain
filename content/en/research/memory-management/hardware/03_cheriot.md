---
title: "CHERIoT"
description: "CHERIoT"
tags: ["memory-safety", "hardware"]
weight: 30
date: 2026-05-18T17:00:00+07:00
---

> Microsoft's tiny CHERI: a 32-bit capability profile + RTOS that delivers complete spatial, temporal and compartment safety to microcontrollers, now in commercial silicon.

## §1 Provenance

- Amar, Chen, Chisnall, Domke, Filardo, Liu, Norton-Wright, Tao, Watson, Xia. "CHERIoT: Complete Memory Safety for Embedded Devices." *MICRO 2023*. https://dl.acm.org/doi/pdf/10.1145/3613424.3614266 — and the matching uArch paper, IEEE Micro 2023. https://www.cl.cam.ac.uk/research/security/ctsrd/pdfs/202310ieeemicro-cheriot-uarch.pdf
- "CHERIoT Architecture Specification v1.0." https://cheriot.org/cheriot-sail/cheriot-architecture.pdf
- Chisnall et al. "CHERIoT RTOS: An OS for Fine-Grained Memory-Safe Compartments on Low-Cost Embedded Devices." *SOSP 2025*. https://dl.acm.org/doi/pdf/10.1145/3731569.3764844
- CHERIoT ISA roadmap, Oct 2024. https://cheriot.org/isa/roadmap/2024/10/31/isa-roadmap.html
- lowRISC + SCI Semiconductor "ICENI" / "Sunburst Chip" tapeout press release, Nov 2024. https://www.globenewswire.com/news-release/2024/11/11/2978489/0/en/lowRISC-and-SCI-Semiconductor-Partner-to-Create-First-CHERIoT-Commercial-Tapeout.html
- Sunburst Chip repository release, April 2025. https://www.globenewswire.com/news-release/2025/04/02/3054051/0/en/lowRISC-and-SCI-Semiconductor-Release-Sunburst-Chip-Repository-for-Secure-Microcontroller-Development.html
- Sonata FPGA platform overview. https://www.electronicdesign.com/technologies/embedded/article/55284831/lowrisc-sonata-an-open-source-cheriot-ibex-evaluation-platform
- Microsoft Research, CHERIoT publication portal. https://www.microsoft.com/en-us/research/publication/cheriot-rethinking-security-for-low-cost-embedded-systems/

## §2 Mechanism

CHERIoT is a **32-bit CHERI profile** (RV32E base) designed for microcontrollers measured in 100s of KB of SRAM. Compared with 64-bit CHERI:

- **Capability width 64 bits + 1 tag** (vs. 128+1 for CHERI-RISC-V/Morello). Bounds are even more aggressively compressed and capability size matches a single load.
- A novel **load-barrier** plus a background **revocation sweeper** give *deterministic* temporal safety: every load through a capability checks a per-page "epoch" colour; freed objects' colours are revoked, and the sweeper subsequently clears all capabilities to revoked memory.
- A richer set of **sentries**: sealed entry capabilities can also encode interrupt-disable-on-entry / capture-prior-state, which is essential for real-time compartment switches.
- An **architecturally enforced compartment switcher** (a tiny trusted shim) plus a partially-trusted memory allocator and scheduler.

Silicon area cost: ~3% extra on the open-source Ibex core (CHERIoT-Ibex) once the load barrier and optimised background revoker are added (4.5% for the load filter alone, up to ~10% with the revoker, all measured against a 16-element PMP baseline).

## §3 Threat model + guarantees

CHERIoT promises **deterministic** (not probabilistic):

- **Spatial safety**: per-object bounds on every pointer at the C language level.
- **Temporal safety**: no use-after-free reaches a load; load-barrier traps stale colours, revoker cleans up.
- **Compartmentalisation**: unlimited mutually-distrusting compartments at <100 bytes each, with shared-memory passing via simple pointer arguments.
- **Real-time**: deterministic worst-case interrupt latency; sentry interrupt-state control means a compartment cannot be interrupted at an arbitrary capability boundary.

Not protected:

- Logic bugs inside a compartment.
- Side channels — CHERIoT has no architectural countermeasure for Spectre-style transient leaks, though its small-cores microarchitecture has fewer speculation gadgets than a typical OoO superscalar.
- Inter-compartment information flow beyond what the type system enforces.
- Supply chain of the trusted switcher/allocator/scheduler (these are TCB, ~13K LoC C++/C in the open-source RTOS).

## §4 Production status (May 2026)

- **CHERIoT ISA v1.0** frozen 2024; being upstreamed into the RISC-V CHERI standardisation track as the **recommended microcontroller profile**.
- **CHERIoT-Ibex** open-source core (lowRISC) reaches production-grade in 2025.
- **lowRISC Sonata** FPGA evaluation board (CHERIoT-Ibex on Xilinx Artix-7) is for sale on Mouser since 2024 and is the DSbD TAP cohort-6 reference platform.
- **SCI Semiconductor ICENI** is the first commercial CHERIoT chip: 22 nm process, first silicon Q3 2025, sampling in H2 2025, targeted at industrial OT/IoT (PLC, sensor gateways, automotive ECU). SCI is co-owner of the open-source CHERIoT repo alongside Microsoft, with contributions from Google, Cambridge and lowRISC.
- **Sunburst project** (UKRI / DSbD funded, lowRISC + SCI + Oxford Innovation): phase 2 (April 2025) released the open-source Sunburst Chip top-level design on GitHub (`lowRISC/sunburst-chip`), built on OpenTitan Earl Grey IP plus the CHERIoT-Ibex core.
- Microsoft has demonstrated CHERIoT running the **Microvium JavaScript** interpreter in its own compartment plus a TLS network stack at 20 MHz with 17.5% CPU load on FPGA.
- No published CVE-elimination measurement yet, but the architectural arguments (object-granularity caps + deterministic UAF + compartments) close exactly the classes that dominate embedded-firmware CVE reports.

## §5 Software emulation cost

A software-only CHERIoT-equivalent on a Cortex-M-class MCU would be brutal: 32-bit MCUs have neither the RAM nor cycles to run a software bounds checker plus a Boehm-style sweeper plus compartment marshalling at line rate. Realistic numbers from the related literature:

- SoftBound+CETS on x86 server class: ~2x time, ~50% memory.
- MarkUs-style quarantine on a 64 KB-RAM MCU: typically untenable (the quarantine alone consumes the heap).
- Microvium-in-CHERIoT vs. Microvium-without: ~10-20% slowdown for full compartmentalisation, deterministic real-time preserved.

That gap (≈10-20% with hardware vs. unrunnable in software at MCU scale) is exactly why CHERIoT matters more than full CHERI for **runtimes** — a managed runtime running on a small device cannot afford the software-only path, so the hardware does the heavy lifting and the runtime's job is to express compartment boundaries and allocator semantics.

## §6 Mochi adaptation note

CHERIoT is the most directly relevant of the hardware schemes to vm3 because:

1. Like vm3, CHERIoT is designed around **a managed allocator that participates in the safety story** (the partially-trusted heap manager). Our slab-and-generation scheme is exactly the same shape of thing.
2. CHERIoT's **load-barrier + background sweep** is the deterministic-temporal-safety analogue of MEP-40's "bump generation on slot reuse" — but CHERIoT actually *revokes* stale capabilities in memory, while we leave them in place and rely on the generation check at deref. The trade-off: we save the sweeper but pay one branch per access. CHERIoT spends silicon on a load filter to make the check free; we have no silicon, so the branch is what we have.
3. CHERIoT's **compartment switcher** (a trusted ~hundreds-of-bytes routine) maps almost exactly to a hypothetical MEP-15 effect-domain switcher in vm3.
4. Crucially, CHERIoT runs a JavaScript VM **inside one compartment** with its own heap, and CHERIoT's protection wraps the entire VM. The lesson: **vm3 should never assume it is the outermost safety boundary** — if running under CHERIoT, our cells live in *the compartment's* heap and our generation bumps coexist with CHERIoT revocation.

Where vm3 falls short of CHERIoT today: we have no equivalent of the **sealed-sentry interrupt control**; we rely on goroutine cooperative scheduling. If we ever target hard-realtime embedded use as a mochi profile, this is a gap. The smallest addition would be a "sealed handle" bit reserved in the arena-tag nibble of the Cell that marks a handle as only-callable-via-effect-domain-entry.

References: MEP-40 (handle = 4+12+32), MEP-15 (effects), MEP-16 (null-safety).

## §7 Open questions for MEP-41 design

1. Do we want a full compartment story, or is "effects as types" enough? CHERIoT shows that *deployed* compartments need a runtime substrate, not just a type-system check.
2. Should we adopt CHERIoT's **explicit revocation sweep** as an option for arenas that recycle slots too fast for a 12-bit generation to give a comfortable margin?
3. The ICENI / Sunburst commercial roadmap is real. If a Mochi-on-ICENI target appears, what is the minimum we cut from vm3 to fit in 256 KB SRAM?
4. CHERIoT publishes its ISA against a Sail formal model. Should the vm3 handle semantics get a Sail or K-framework spec for the same reason?
5. CHERIoT's "shared memory by pointer-passing" is enabled by tagged capabilities. Can we do the equivalent in vm3 by handing out an arena-handle whose generation is "fresh" only for the receiver, or do we need explicit copy?