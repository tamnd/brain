---
title: "DoD Safe Coding Practices and Military / Aerospace Memory-Safety Procurement (2024-2026)"
description: "The DoD's evolving acquisition posture on memory-safe languages, the SWFT framework, and aerospace coding standards."
tags: ["memory-safety", "industry"]
weight: 60
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- US Air & Space Forces Magazine, **"DOD Plans Quicker Cybersecurity Contractor Standards"** (April 2025). https://www.airandspaceforces.com/dod-quicker-contractors-cybersecurity-standards/
- Rob Vietmeyer (DoD Chief Software Officer) public remarks, April 2025.
- Industrial Cyber: **"US DoD gets set to develop SWFT framework, issues RFIs to advance secure software development"**. https://industrialcyber.co/regulation-standards-and-compliance/us-dod-gets-set-to-develop-swft-framework-issues-rfis-to-advance-secure-software-development-and-authorization/
- CMU Software Engineering Institute. **"Supporting the Use of CERT Secure Coding Standards in DoD Acquisitions"**. https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=28033
- CISA / NSA. **"The Case for Memory Safe Roadmaps"** (2023).
- Military Embedded Systems. **"The convergence of safety and security — Five steps to building modern avionics software"**. https://militaryembedded.com/avionics/safety-certification/guest-blog-the-convergence-of-safety-and-security-five-steps-to-building-modern-avionics-software
- US Army article, **"The SAFE Advantage"**. https://www.army.mil/article/280344/the_safe_advantage
- MISRA C:2023; CERT C/C++ secure coding standards; DO-178C (avionics software certification); DO-326B (avionics cybersecurity); MIL-STD-882E (system safety); DoDI 5000.87 (Software Acquisition Pathway).

## §2 Mechanism
The DoD's posture on memory-safe coding combines three threads:

1. **Acquisition modernisation through the SWFT (Software Fast Track) Framework.** Launched 2025, formally announced by DoD CSO Rob Vietmeyer in April 2025. SWFT promises faster authorisation-to-operate for vendors who can demonstrate **assured supply chain** and **secure coding practices** — including memory-safe-language adoption. Current authorisation processes take months to years; SWFT targets dramatic reduction.

2. **Established safety-critical-software standards.** Military and aerospace systems continue to operate under DO-178C (software for airborne systems), DO-326B (airworthiness security), MIL-STD-882E (system safety), the CERT C/C++ secure coding standards, and MISRA C:2023. These standards predate the memory-safe-language conversation and operate by *constraining* C/C++ usage rather than replacing it. DO-178C compliance does not prohibit memory-unsafe languages but does require rigorous demonstration of correctness.

3. **Memory-safe-language adoption emerging.** Per CISA's "Case for Memory Safe Roadmaps" (joint with NSA), DoD-aligned vendors are expected to publish memory-safety roadmaps. Rust is the headline candidate language for new defence systems work; the US Army and the US Navy have visible Rust pilots.

The 2025 framing also introduces **DevSecSafOps** — an extension of DevSecOps that explicitly integrates software safety considerations, motivated by autonomous, AI, and robotics defence systems where unsafe outcomes can cause loss of life. DoDI 5000.87 (Software Acquisition Pathway) is being interpreted through this DevSecSafOps lens.

## §3 Scope and Limits
**Scope.** Defence and aerospace software procurement, including airborne weapons systems, unmanned systems, intelligence systems, command-and-control software, the broader DoD enterprise software stack.

**Limits.** The legacy install-base is enormous and largely in C / C++ / Ada. Hard-real-time avionics has very specific constraints (deterministic timing, no GC pauses, certifiable toolchain) that limit immediate language choices. Open-source software is treated as commercial software under DoD rules, requiring qualification of OSS components for DO-178C compliance — a non-trivial barrier to adopting any new language including Rust or Mochi.

## §4 May 2026 Status
**Memory-safety guidance is being woven into procurement, but not as a hard requirement.** SWFT is rolling out through 2025-2026. The CISA / NSA / ONCD signal is being absorbed into DoD acquisition language gradually; the most likely formal manifestation is **memory-safety roadmaps as a SWFT differentiator** rather than as a contract-bar. Rust adoption in DoD pilots is visible but small relative to the C/C++ install base.

DO-178C and MISRA C:2023 remain the *operational* standards for safety-critical avionics in 2026. There is no DO-178C analogue for memory-safe languages yet; the certification toolchain for Rust at DO-178C levels (especially DAL A) is still being developed by vendors like Ferrous Systems (ferrocene), AdaCore (Rust support), and others.

For Mochi specifically: Mochi is *not* a candidate language for DO-178C avionics today. Garbage-collected runtimes with non-deterministic pause times do not fit the safety-critical-avionics profile. Mochi *could* be a candidate for non-safety-critical DoD software (administrative systems, intelligence-analysis tooling, simulation, training) but is not on any visible DoD procurement list.

## §5 Cost
DoD-side: SWFT and DevSecSafOps are organisational changes, not capital programmes. The cost is institutional inertia, not budget. Vendor-side: complying with DO-178C costs roughly **$100-$200 per line of code** for DAL-A airborne software; certifying a new language toolchain to DO-178C standards is a multi-vendor-year, eight-figure undertaking.

For non-safety-critical DoD software, the cost of complying with SWFT / Secure-by-Design alignment is much lower — typically the same memory-safety-roadmap effort civilian organisations face.

## §6 Mochi Adaptation Note
DoD / mil-aero is the **hardest deployment target** for any new language. MEP-41 should be honest about Mochi's positioning relative to it.

- **Mochi is not a safety-critical-avionics language.** Mochi has a tracing GC (planned mark-sweep). Mochi has a JIT (vm3jit). Neither is permissible in a DO-178C DAL-A context. MEP-41 should explicitly disclaim safety-critical avionics applicability.
- **Mochi could plausibly be a non-safety-critical DoD language.** Administrative tools, intelligence-analysis backends, simulation pipelines, training systems — none of these require DO-178C compliance, all could benefit from a memory-safe language. MEP-41 can claim eligibility for this segment.
- **The SWFT memory-safety differentiator is reachable.** Mochi's CISA-Secure-by-Design-aligned positioning (see industry/03) maps cleanly onto SWFT's memory-safety expectations. Mochi-using organisations can use Mochi as part of their SWFT submission.
- **DevSecSafOps is the right vocabulary.** Even outside safety-critical contexts, the DoD framing of "safety and security together" is the right framing for Mochi — Cell-based memory safety is both a security and a safety property.
- **The DoD's Rust pilots are the relevant comparison set.** Mochi will compete (in some sense) with Rust adoption in the same procurement category. MEP-41 should acknowledge Rust as the leading candidate and articulate Mochi's value-add (faster development, simpler language, no borrow checker) rather than claiming superiority.

## §7 Open Questions for MEP-41
1. Should MEP-41 explicitly disclaim safety-critical-avionics applicability up front? This pre-empts a category of question and signals honesty.
2. Should Mochi commit to a "Mochi for non-safety-critical DoD use" positioning — i.e., an explicit statement that Mochi is suitable for administrative and analysis software but not airborne or weapon systems?
3. The DoD's DevSecSafOps framing combines safety and security; Mochi's Cell design also combines them. Worth a sentence in MEP-41 framing.
4. Should Mochi publish DoD-procurement-relevant material (a one-page "Mochi and Secure-by-Design alignment" doc) targeted at SWFT submitters? Cheap and useful.
5. The Rust-for-DoD ecosystem (ferrocene, AdaCore Rust support) is investing in DO-178C certification. Should Mochi note this trajectory as evidence that even formally-uncertifiable runtimes (GC, JIT) can be packaged for DoD with sufficient effort, while explicitly *not* committing Mochi to that path?