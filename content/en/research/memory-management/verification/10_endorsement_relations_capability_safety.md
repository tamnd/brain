---
title: "Capability-Machine Formalism and Endorsement Relations"
description: "Cerise, the CHERI-C Coq memory model, and capability-safety logical relations as the formal model behind handle-based runtimes."
tags: ["memory-safety", "verification"]
weight: 100
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Cerise (logsem/cerise): Iris-based Coq mechanisation of a capability machine. https://github.com/logsem/cerise
- **"Cerise: Program Verification on a Capability Machine in the Presence of Untrusted Code"**, Journal of the ACM (JACM), 2023. https://dl.acm.org/doi/10.1145/3623510
- Park, Pai et al. **"A Formal CHERI-C Semantics for Verification"**, TACAS 2023; **"A CHERI C Memory Model for Verified Temporal Safety"**, CPP 2025.
- CHERI hardware lineage: Watson et al., CHERI ISA reports, with hardware in ARM Morello and Microsoft CHERIoT.
- Sail-based mechanised CHERI-MIPS / CHERI-ARM ISA models, with HOL4 / Isabelle / Coq backends produced via translation.
- CHERI-Y86 (FMCAD 2025): an ACL2 formalisation of a CHERI-equipped Y86. https://repositum.tuwien.at/bitstream/20.500.12708/219552/1/Kwan-2025-A%20Formal%20Y86%20Simulator%20with%20CHERI%20Features-vor.pdf
- Lower-level theory: Devietti / Pierce capability logics (the Cap-OS line) and the Devietti hardware-bounded-pointers work.
- Compositional symbolic execution for CHERI (OOPSLA 2025): https://arxiv.org/pdf/2508.15576

## §2 Claim or Mechanism
A capability machine is a hardware/architecture model where every pointer is replaced by a **capability**: an unforgeable tuple containing (base, bound, permission, [identity/object-type]). The hardware enforces that loads/stores can only touch the region the capability authorises, and capabilities cannot be synthesised from raw bits — they are tagged and must derive from existing capabilities by *monotone* operations (shrink-and-pass-down, no extension).

CHERI is the dominant real-world capability architecture; Morello (ARM) and CHERIoT (Microsoft) are silicon implementations. Software stacks that target CHERI (the FreeBSD CheriBSD, the Linux CHERI port, Morello-tagged libraries) gain *strong spatial memory safety* and, with revocation, *strong temporal memory safety* for free at the hardware level.

The Iris-based **Cerise** logic is the leading formal model: it instantiates Iris on top of a simplified CHERI-style ISA and defines a *unary logical relation* that captures "this capability is safe to share with untrusted code". A capability is safe iff it cannot be used to invalidate any of the program's logical invariants. This logical relation is the formal *capability-safety* statement, often called an **endorsement relation** in the language of object-capability theory.

The CPP 2025 CHERI-C memory model paper additionally verifies *temporal* safety — the property that capabilities revoked at deallocation cannot be used afterward.

## §3 Scope and Limits
**Covered.** Cerise: a small ISA inspired by CHERI, with sufficient features (sealing, permission monotonicity, locality, untrusted-code interaction) to mechanically prove capability-safety theorems. CHERI-C: realistic C semantics on CHERI hardware, with verified temporal safety. The Sail-based ISA models: production-grade ISA specifications usable across HOL4 / Isabelle / Coq.

**Not covered.** Cerise simplifies the full CHERI feature set. Full CHERI-RISC-V or CHERI-ARM/Morello mechanisation in a single proof framework is still work-in-progress. Performance / microarchitectural state (caches, speculation) is generally out of scope — these are functional models. Side-channel resistance is *not* a CHERI guarantee.

## §4 May 2026 Status
**CHERI is shipping hardware.** Microsoft has launched CHERIoT as an open-source embedded-systems architecture. ARM's Morello hardware exists for research. Production OS support (CheriBSD) is mature; production Linux support is in progress. The mechanised CHERI-ISA models (Sail) are the reference specifications used by CHERI implementers and software porters.

Cerise has reached JACM publication; CHERI-C memory-model verification is at CPP 2025 (CPP 2026 has further mechanisation). The OOPSLA 2025 compositional-symbolic-execution work is the most recent formal CHERI tooling. The space is mature enough that *new* mechanisation projects can plug into Sail + Iris + the CHERI-C semantics rather than building from scratch.

## §5 Cost
Cerise and CHERI-C are each multi-person-year PhD efforts. The cost of *using* CHERI (porting an existing C codebase to CheriBSD/Morello) is reported in the CHERI papers as low single-digit percentage code changes for compliant C, much higher for code that abuses integer-pointer casts. The hardware cost of CHERI on a real CPU is in the single-digit percent area (extra tag bits in memory, slightly wider register file).

## §6 Mochi Adaptation Note
This is the **single most important formal-methods area for MEP-41 to position against**. Mochi's Cell representation is *literally a software capability*: an unforgeable 64-bit handle whose validity is checked on every dereference. The arena-tag field is morally CHERI's object-type / sealing field; the generation field is the CHERI revocation mechanism; the slab-index is the offset-within-base.

- MEP-41 should **explicitly position Mochi as a software capability machine** in the Cerise vocabulary. This is not a stretch claim — it is an accurate technical description of the design. The 4-bit arena tag is a *type seal*; the 12-bit generation is a *temporal-safety tag*; the 32-bit slab index is a *bounded offset*; the unforgeability of Cells (no Mochi-source operation can synthesise one from arbitrary bits) is the capability-safety property.
- The endorsement-relation / capability-safety vocabulary maps directly to "what does it mean for a Cell to be valid?". MEP-41 can state: "A Cell is safe to pass to arbitrary Mochi code iff every dereference will either succeed against its tagged (arena, generation) or produce a defined error." This is the unary-logical-relation statement of Cerise in plain English.
- The CHERIoT comparison is the more practical of the two: CHERIoT is targeting embedded systems where a 64-bit capability is too big. Mochi's 64-bit Cell is in the same design ballpark. MEP-41 can claim a *family resemblance* without claiming hardware-level enforcement.
- Mochi's enforcement is *software*, not hardware. This is a real difference: a sufficiently devious `unsafe` Go fragment in the runtime can forge a Cell. MEP-41 must be honest about this — the capability-safety claim is at the Mochi-language layer, not at the silicon layer. Cerise / CHERI-C / CHERIoT all enforce in hardware, which is strictly stronger.
- **The most powerful single move** MEP-41 can make: explicitly cite Cerise as the formal model of what Mochi is doing in software. Even one paragraph of "this design is a software analogue of the capability-machine line; see Cerise (JACM 2023) for the formal account" is enormous documentary value for any reader from the PL community.

## §7 Open Questions for MEP-41
1. Should MEP-41 use the term "software capability" for Cell, with an explicit citation to Cerise and CHERI? This is the highest-value cheap move available.
2. Should the (arena_tag, generation, slab_idx) layout be documented in *capability-machine vocabulary* — type seal, revocation tag, bounded offset — rather than ad-hoc names? Cheap rename, big legibility win.
3. Does Mochi want to claim eligibility for the "CHERI / capability-machine" software-defence category in the CISA / NSA / OMB classifications (see industry files), in addition to "memory-safe language"? Cerise gives precedent that the capability story is independently meaningful even when implemented in software.
4. Should MEP-41 commit to an "if-Mochi-runs-on-CHERIoT" future-work statement, anticipating that CHERI hardware would let Mochi enforce its Cell invariant in silicon rather than in Go?
5. The Cerise logical relation is "safe to share with untrusted code". The Mochi analogue is "safe to share across an FFI boundary". Should MEP-41 state the FFI Cell-handing contract in capability-safety terms?