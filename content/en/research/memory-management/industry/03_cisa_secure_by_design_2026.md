---
title: "CISA Secure-by-Design Pledge and the January 2026 Memory-Safety Deadline"
description: "The voluntary US federal pledge that has set the de-facto industry baseline for memory-safety roadmaps."
tags: ["memory-safety", "industry"]
weight: 30
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- CISA Secure by Design page: https://www.cisa.gov/securebydesign
- CISA Secure by Design Pledge: https://www.cisa.gov/securebydesign/pledge
- Pledge signers list: https://www.cisa.gov/securebydesign/pledge/secure-design-pledge-signers
- **"Product Security Bad Practices"** publication (Oct 2024, updated): https://www.ic3.gov/CSA/2024/241016-2.pdf ; CISA page https://www.cisa.gov/resources-tools/resources/product-security-bad-practices
- CISA Secure by Design Pledge Progress Reports: https://www.cisa.gov/securebydesign/pledge/progress-reports
- Original announcement (May 2024): **"CISA Announces Secure by Design Commitments from Leading Technology Providers"**. https://www.cisa.gov/news-events/news/cisa-announces-secure-design-commitments-leading-technology-providers
- Industry analysis: DEVOPSdigest, **"Fix It or Face the Consequences: CISA's Memory-Safe Muster"**. https://www.devopsdigest.com/fix-it-or-face-the-consequences-cisas-memory-safe-muster
- RunSafe Security, **"CISA's 2026 Memory Safety Deadline"**. https://runsafesecurity.com/blog/cisa-memory-safety-ot-leaders/

## §2 Mechanism
The CISA Secure by Design Pledge is a **voluntary public commitment** by software manufacturers to seven security goals. It was launched in May 2024 with 68 initial signers; by 2026 the count has grown to **roughly 300 organisations** including Microsoft, Google, AWS, IBM, Cloudflare, GitHub, Fortinet, BeyondTrust, Hewlett Packard Enterprise, BitGo, and many smaller vendors.

The seven goals are:
1. **Multi-factor authentication** — measurable progress within one year.
2. **Default passwords** — reduce defaults across product lines.
3. **Reducing entire classes of vulnerability** — this is the **memory-safety goal**.
4. **Security patches** — measurable increase in customer patch adoption.
5. **Vulnerability disclosure policy** — publish a clear VDP and CVE coverage.
6. **CVEs** — issue accurate, complete CVEs for all critical / high-severity vulnerabilities.
7. **Intrusion evidence** — give customers ways to detect compromise.

Under goal 3, CISA's **"Product Security Bad Practices"** companion guidance specifies that software manufacturers should publish a **memory-safety roadmap by January 1, 2026**, outlining their prioritised approach to eliminating memory-safety vulnerabilities — particularly in network-facing code and cryptographic code. The roadmap should detail transition plans to memory-safe languages or to hardware capabilities (like CHERI) that prevent memory-safety vulnerabilities.

The 2024 CISA framing is that **failing to publish a memory-safety roadmap by January 1, 2026 is "dangerous and significantly elevates risk to national security, national economic security, and national public health and safety"**.

## §3 Scope and Limits
**Scope.** Enterprise software products and services, including on-premises software, cloud services, and SaaS. Physical products (IoT, consumer electronics) are *not* in the pledge's primary scope, though companies may demonstrate progress voluntarily.

**Limits.** The pledge is *voluntary*. CISA does not enforce it and does not verify adherence. There is no centralised scorecard of who has actually published roadmaps by the January 2026 deadline; companies post individual progress reports on the CISA progress-reports page at their own pace. The list of named memory-safe languages is implicit — CISA's text language repeats the standard set (Rust, Go, C#, Java, Swift, Python, JavaScript) but does not have a formal certification mechanism.

## §4 May 2026 Status
**Deadline has passed; compliance is voluntary and inconsistent.** As of May 2026:
- ~300 signers, growing.
- Several major signers (Cloudflare, Fortinet, BeyondTrust) have published progress reports referencing memory-safety roadmaps.
- No CISA-issued consolidated "compliance scorecard" for the January 2026 memory-safety-roadmap deadline; CISA's enforcement posture is *naming-and-shaming through procurement language*, not direct enforcement.
- Federal procurement guidance increasingly references Secure-by-Design alignment as a procurement input, especially in DoD / civilian-agency software acquisition.
- The DoD SWFT (Software Fast Track) framework launched in 2025 explicitly rewards Secure-by-Design alignment with faster security authorisation for products on DoD networks.

Importantly, **CISA does not require memory-safe languages**. The pledge requires a **roadmap**. A manufacturer can satisfy the letter of the pledge with a credible plan to migrate, hardware-capability alternatives (CHERI), or even just enhanced static-analysis discipline if backed by evidence. The political signal, however, is unambiguous: the federal government considers memory-safe languages the preferred direction.

## §5 Cost
For signers, the cost is principally an internal commitment to the seven goals plus the engineering work to produce the roadmaps. Microsoft and Google were ready signers because they already had massive memory-safety investment underway. For smaller vendors, the visible cost is the engineering effort to produce a credible roadmap — typically a multi-month, multi-team effort to inventory C/C++ codebases, prioritise network-facing components, and commit to migration timelines.

The implicit cost is reputational: not signing, or signing without a credible roadmap, increasingly carries reputational risk in federal procurement.

## §6 Mochi Adaptation Note
The CISA pledge is the **most important industry-policy document for MEP-41 to position against** — because Mochi may want to publicly claim memory-safety-category eligibility, and CISA's framework is the dominant US-government taxonomy.

- **Mochi-the-language sits squarely in the "memory-safe language" category that CISA implicitly endorses.** MEP-41 should state this claim explicitly with citation to CISA's Product Security Bad Practices and to the standard list (Rust / Go / C# / Java / Swift / Python / JavaScript). Mochi belongs in that family.
- **Mochi's vm3 runtime is implemented in Go.** Go is on CISA's implicit list. The provenance chain — Mochi safety relies on vm3 runtime correctness, vm3 is in Go, Go is memory-safe — is the *same chain* that justifies Java-on-JVM or Python-on-CPython. MEP-41 should claim parity with those well-accepted examples.
- **MEP-41 need not commit to a roadmap.** Mochi is not a CISA pledge signer (Mochi is not a vendor). But MEP-41 *should* document Mochi's position in the language taxonomy so that any downstream Mochi user (who *is* a signer) can cite Mochi adoption as roadmap-aligned.
- **The right rhetorical move**: state that "Mochi is designed to enable signatories of the CISA Secure-by-Design Pledge to use it as part of their memory-safety roadmap, equivalent to selecting any other named memory-safe language". This is honest, defensible, and useful for Mochi-adopting organisations.
- **CHERI / hardware-capability alternative is also in scope.** The CISA framework explicitly allows hardware-capability solutions as alternatives to memory-safe-language migration. Mochi's Cell design is a *software* capability machine (see verification/10). MEP-41 can note Mochi's structural compatibility with CHERI / CHERIoT, even though it does not require CHERI hardware.

## §7 Open Questions for MEP-41
1. Should MEP-41 explicitly claim "memory-safe language" status with reference to the CISA / NSA / ONCD framework? This is the highest-value cheap statement available.
2. Should Mochi maintain a one-page public-facing "memory-safety statement" suitable for downstream organisations to attach to their CISA roadmaps?
3. Mochi's "runtime is Go, language is Mochi" is exactly analogous to "runtime is C, language is Python" or "runtime is C++, language is V8/JavaScript". Should MEP-41 explicitly draw this analogy?
4. CISA's framework prefers memory-safe languages but permits CHERI-style hardware capabilities. Should MEP-41 make the case that Mochi's Cell-as-capability design is *both* — memory-safe at the language layer *and* capability-safe at the runtime layer? This is a stronger claim than the standard language-only positioning.
5. Should MEP-41 reserve a clause for the case where Mochi is used by US federal customers — i.e., commit that Mochi will track US federal memory-safety guidance evolutions, in particular any CISA / NSA / OMB updates after January 2026?