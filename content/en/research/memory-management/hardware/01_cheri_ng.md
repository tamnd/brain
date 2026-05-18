---
title: "CHERI (Next Generation)"
description: "CHERI (Next Generation)"
tags: ["memory-safety", "hardware"]
weight: 10
date: 2026-05-18T17:00:00+07:00
---

> Hardware capabilities: 128-bit fat pointers with bounds, permissions and an out-of-band tag, enforced by the ISA.

## §1 Provenance

- Watson, Chisnall, Clarke, Davis, Filardo, Laurie, Moore, Neumann, Richardson, Sewell, Witaszczyk, Woodruff. "CHERI: Hardware-Enabled C/C++ Memory Protection at Scale." *IEEE Security & Privacy*, vol. 22 no. 4, July/Aug 2024, pp. 50-61. DOI 10.1109/MSEC.2024.3396701 (IEEE CS 2024 Best Paper Award for S&P Magazine). https://www.cl.cam.ac.uk/research/security/ctsrd/pdfs/20240419-ieeesp-cheri-memory-safety.pdf
- Watson et al. "Capability Hardware Enhanced RISC Instructions: CHERI Instruction-Set Architecture, Version 9." Technical Report UCAM-CL-TR-987, University of Cambridge Computer Lab, Sept 2023. https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/
- RISC-V International draft "RISC-V Specification for CHERI Extensions" (RV64Y baseline encoding derived from CHERI v9). https://riscv.github.io/riscv-cheri/
- Woodruff et al. "CHERI Concentrate: Practical Compressed Capabilities." *IEEE Transactions on Computers*, 2019 (the compression scheme adopted in ISAv7+). https://www.cl.cam.ac.uk/research/security/ctsrd/pdfs/2019tc-cheri-concentrate.pdf
- Codasip X730 (first commercial CHERI-RISC-V core) product page. https://codasip.com/solutions/riscv-processor-safety-security/cheri/x730-risc-v-application-processor/
- CHERI Research Centre, Cambridge. https://cheri.cst.cam.ac.uk/

## §2 Mechanism

CHERI replaces 64-bit native pointers with **128-bit capabilities** held in extended general-purpose registers (a "merged" file in ISAv9; previous versions had split files). Each capability carries:

- a **64-bit address/cursor** (the value the program uses)
- **compressed bounds** (lower, upper) stored in ~28 bits using a floating-point-style mantissa+exponent scheme (CHERI Concentrate); on ISAv9 mantissa width MW=14 with two derived bits
- **permissions** (load, store, execute, load-cap, store-cap, store-local-cap, seal, unseal, system-regs, etc.), typically ~18 bits split into hw-defined and sw-defined fields
- **object type / otype** (~16 bits) for sealed-capability compartmentalisation
- a **flag** bit and CP control bits

A **separate 1-bit tag** travels with every 128-bit memory granule through caches and DRAM in a sideband. Any non-capability store to a granule clears its tag. The tag is invisible to load/store instructions and cannot be forged in software; it is what distinguishes a real capability from arbitrary data.

Loads/stores accept a capability operand, the hardware decompresses the bounds in parallel with TLB translation, and any access outside `[base, top)` or violating permissions raises a CHERI exception. Branches and indirect calls require a capability with `Execute` permission (PCC is itself a capability). Bounds are **monotonic**: a `CSetBounds` instruction may only shrink, not grow. Per ISAv9 (a Morello-influenced decision), attempted non-monotonic modification *clears the tag* rather than trapping, which simplifies generic code that doesn't know if a value is a capability.

Sealing (`CSeal`/`CUnseal`) freezes a capability so it can only be invoked through a controlled entry point (`CCall`/sentry); this is the substrate for compartments.

## §3 Threat model + guarantees

- **Spatial safety**: deterministic per-pointer bounds; linear and non-linear OOB writes are stopped at the ISA boundary, including DMA on CHERI-enabled fabrics.
- **Pointer integrity / provenance**: untagged data cannot be dereferenced. An attacker who corrupts a capability in memory clears the tag; the next load-via-cap traps.
- **Compartmentalisation**: sealed caps + per-thread DDC/PCC support millions of in-process compartments with cheaper boundary crossings than process isolation.
- **Temporal safety (partial)**: CHERI itself does not prevent UAF; you still need a *revocation* mechanism (CHERIvoke, Cornucopia Reloaded, CHERIoT's load-barrier+sweep). With revocation deployed, UAF is closed deterministically.
- **Type confusion**: not addressed by the ISA; addressed by language-level use of sealed caps and refined types in CHERI-C++.
- **Control-flow**: sealed entry points + bounded PCC kill arbitrary ROP/JOP within a compartment, but in-compartment ROP is still possible.
- **Side channels**: CHERI tags ride normal cache lines, so cache and timing side channels remain. TIKTAG-style attacks against MTE do **not** directly apply, but other Spectre variants do.
- **Not protected**: information leaks (the tag is integrity, not confidentiality), uninitialised reads (see Mon CHÉRI / conditional caps research), supply-chain bugs, logic flaws.

## §4 Production status (May 2026)

- **Codasip X730** (rebrand of A730-CHERI) is the first commercial CHERI-RISC-V application core, **licensable since April 2025**, shipped on the "Codasip Prime" FPGA exploration platform; the register file extends to 129 bits to carry capabilities.
- **CHERI Alliance** (founded mid-2024) includes Cambridge, Arm, Codasip, Google, Microsoft, lowRISC, SCI Semiconductor, NCSC, Dstl.
- **Arm Morello** prototype (Neoverse N1 + CHERI) shipped several hundred boards 2022-2024; DSbD program closed-out Oct 2025 with a £200M spend, 405 jobs, 80% positive evaluation from TAP participants, and a programme-level claim that DSbD-style hardware would mitigate ~**70% of known memory-safety CVEs**.
- **Microsoft CHERIoT** ISA v1.0 frozen 2024; **SCI Semiconductor ICENI** (CHERIoT-Ibex) tapeout in 22nm, first commercial silicon H2 2025, with lowRISC's Sonata FPGA board distributed via Mouser through 2025-2026.
- Vendor commitments: NCSC, Google and Microsoft publicly endorse CHERI for high-assurance embedded use; no full-CHERI server CPU is yet on a public roadmap as of May 2026.

## §5 Software emulation cost

A pure-software CHERI emulation (e.g. CheriABI on QEMU; or sketches that store fat-pointer metadata next to each pointer) typically pays:

- **2x pointer footprint** (cache pressure ~20-30% on pointer-heavy workloads)
- **per-deref bounds + permission check** in software: 5-15% on bounds checks alone, more if revocation is added
- **tag tracking** requires either a shadow map (1 bit per 16 B of address space, ~0.8% RAM but every store must update it, ~30-100% slowdown for naive impls) or per-allocation metadata.

Reported numbers from MorelloBSD on Morello hardware are **<5% on most SPEC** subprograms; the same protection in software (Softbound+CETS, Low-Fat Pointers, EffectiveSan) historically lands at 1.5x-3x runtime and 1.5x-2x memory. CHERIvoke revocation adds ~5% on hardware, ~25-50% in software.

## §6 Mochi adaptation note

vm3's Cell is already a "software CHERI lite":

| CHERI 128-bit cap                       | vm3 Cell (8 B)                                        |
|----------------------------------------|-------------------------------------------------------|
| 64-bit cursor                           | implicit: arena+idx encode an address                 |
| compressed bounds                       | implicit: per-slab fixed-size slots, bounds=slot size |
| 1-bit out-of-band tag                   | the 12-bit **generation** carried in-band             |
| permissions (~18 bits)                  | 4-bit **arena tag** (read-only on const arena, etc.)  |
| otype (~16 bits)                        | not present                                           |
| monotonic bounds                        | trivially true: vm3 cells never re-bound              |

What MEP-40 already gives us (per the handle layout doc): spatial safety inside a slab is automatic because the slab index times a fixed slot size cannot escape the slab; provenance/integrity is the generation check. We are stronger than CHERI on monotonicity (we cannot widen) and weaker on permissions (arena tag has 16 possible values, CHERI has ~18 bits).

The **smallest gap-closer** for MEP-41 is a **permissions field carved out of the 32-bit slab index** (e.g. take 4-6 bits of the high end of the slab index for `perm` once we cap slabs at 16-26 bits of slots; we lose some range but gain read-only / no-cap-store / no-execute distinctions). This is the software analogue of CHERI's permission word, and it composes with MEP-15 effects (an effect-typed handle can be downgraded to no-write at runtime).

No sealing analogue today. Compartments (MEP-15 effect domains) currently rely on the type system, not on handle metadata. If we wanted in-process least-privilege compartments without language-level cooperation, a 1-bit "sealed" flag + a 4-bit "otype" inside the arena-tag byte would suffice for a small number of compartments.

## §7 Open questions for MEP-41 design

1. Do we want a fixed-shape Cell forever, or a "wide handle" variant (16 B) for compartmentalised code, similar to how CHERI runs both 64- and 128-bit modes on Morello?
2. If we add a permissions field, do we let the compiler narrow it at known-safe call sites (like CHERI's `CAndPerm`), and how do we keep the generation-check fast?
3. Should the arena tag also carry a *colour* for revocation sweeps (à la CHERIoT's load-barrier), or do we rely entirely on bump-generation for temporal safety?
4. Sealing: do MEP-15 effect handles need ISA-level sealing, or is per-effect arena assignment sufficient?
5. How do we expose CHERI hardware when present (Morello / X730 / ICENI)? Can the vm3 backend lower a Cell directly to a 128-bit capability and inherit hardware spatial safety for free?