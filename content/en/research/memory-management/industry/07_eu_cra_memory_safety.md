---
title: "EU Cyber Resilience Act and Memory Safety"
description: "The CRA's 2026-2027 enforcement timeline and the implicit pressure toward memory-safe languages."
tags: ["memory-safety", "industry"]
weight: 70
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- European Commission, **Cyber Resilience Act** main page. https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act
- CRA Reporting Obligations page. https://digital-strategy.ec.europa.eu/en/policies/cra-reporting
- CRA legislative-text summary. https://digital-strategy.ec.europa.eu/en/policies/cra-summary
- Hogan Lovells client alert, **"EU Cyber Resilience Act: Key 2026 milestones toward CRA compliance"**. https://www.hoganlovells.com/en/publications/eu-cyber-resilience-act-getting-ready-for-cra-compliance-in-2026
- OpenSSF analysis of the CRA. https://openssf.org/public-policy/eu-cyber-resilience-act/
- Keysight, **"One Year Countdown to EU CRA Compliance — September 11, 2026, Changes Everything"**. https://www.keysight.com/blogs/en/tech/nwvs/2025/09/11/one-year-countdown-to-eu-cra-compliance-september-11-2026-changes-everything
- ScanReco, **"Current state of the EU Cyber Resilience Act — and why no-one can claim they comply"**.
- Armorcode CRA requirements guide. https://www.armorcode.com/learning-center/eu-cyber-resilience-act-cra-requirements-guide

## §2 Mechanism
The Cyber Resilience Act (CRA, Regulation (EU) 2024/2847) is a **horizontal EU regulation imposing cybersecurity requirements on products with digital elements (PDEs)** sold on the EU market. The CRA entered into force on **10 December 2024**. Key obligations roll out across a three-year window:

- **10 December 2024**: CRA enters into force.
- **11 June 2026**: Member States must designate notifying authorities for conformity-assessment bodies.
- **11 September 2026**: **Vulnerability and incident reporting obligations begin**. Manufacturers must report actively exploited vulnerabilities (24-hour early warning, 72-hour full notification, 14-day final report) and severe incidents through the CRA Single Reporting Platform (SRP). This is the first day the CRA actively *bites* on industry.
- **11 December 2027**: All other CRA obligations apply — Essential Cybersecurity Requirements (Annex I), conformity assessment, CE marking, SBOM obligations.

Crucially, the CRA's Annex I Essential Cybersecurity Requirements are written at a *principles* level. They require products to be "designed, developed and produced in such a way that they ensure an appropriate level of cybersecurity", to be **delivered without known exploitable vulnerabilities**, to be **secure by default**, to **protect the integrity of stored, transmitted, and processed data**, and to **ensure that vulnerabilities can be addressed through security updates**. The CRA does *not* mandate memory-safe languages by name. But several Annex I requirements are *de facto* easier to meet with memory-safe languages — particularly "designed to limit attack surface" and "designed to provide security-related information by recording and monitoring relevant internal activity".

## §3 Scope and Limits
**Scope.** "Products with digital elements" — a broad category including most software, hardware with embedded software, IoT devices, libraries, browser components, OS components. **Excluded**: medical devices (covered by MDR/IVDR), motor vehicles (covered by UN R155 / R156), aviation, marine equipment, defence-specific products.

**Limits.** The CRA does not mandate memory-safe languages. The CRA does not provide an explicit Mochi-like-language certification path. Industry guidance is still being developed: harmonised standards are in draft (CEN/CENELEC, ETSI) and **no organisation can yet claim full CRA compliance** because the conformity-assessment framework is incomplete. The European Commission published draft guidance on 3 March 2026, with comments open until 13 April 2026.

The most-painful practical near-term obligation is the **September 2026 vulnerability-reporting deadline**: vendors must know exactly which components are in their products (necessitating SBOM readiness) and must report exploited vulnerabilities within strict timelines. Memory-safe languages help here by *reducing the frequency* of vulnerabilities that need to be reported.

## §4 May 2026 Status
**Reporting obligations are imminent (Sept 11, 2026); Essential Cybersecurity Requirements come into force Dec 11, 2027.** The current state in May 2026:

- Harmonised standards in draft, not final.
- Conformity-assessment-body framework being designated by Member States (June 2026 deadline).
- No vendor can credibly claim "fully CRA-compliant" — the conformity-assessment mechanism does not yet exist.
- Industry is in inventory-and-readiness mode: SBOM, vulnerability-tracking, supplier-due-diligence programmes are being stood up.
- The EU Commission's March 2026 draft guidance is being commented on.

For memory safety specifically: the CRA does not name memory-safe languages, but the policy environment strongly favours them. The CRA's "secure by design", "delivered without known exploitable vulnerabilities", and "limit attack surface" requirements are all easier to evidence with memory-safe-language adoption. The 24/72-hour vulnerability-reporting timelines reward *fewer* vulnerabilities, which memory-safe languages structurally provide.

## §5 Cost
The CRA is the **most expensive single piece of cybersecurity legislation** in Europe to date. Industry estimates range from €50K-€500K per product for full CRA conformity-assessment (including SBOM tooling, vulnerability-reporting infrastructure, conformity-body engagement). Annual ongoing compliance cost: low five figures per product line. For large vendors with many products: many millions per year.

Memory-safe-language adoption reduces *one* category of cost (frequency of reportable vulnerabilities) but does not address the conformity-assessment / documentation burden, which is independent of language choice.

## §6 Mochi Adaptation Note
The CRA is **the most important non-US regulatory framework for Mochi to position against**, especially if Mochi targets European users.

- **Mochi-the-language helps CRA compliance, but is not itself CRA-regulated.** Mochi is a language; the CRA regulates products. Mochi is more like Rust or Go in this respect — it is a *toolchain* product distributors use, not a product placed on the EU market on its own. The CRA exemption for *free and open-source software not placed on the market in the course of a commercial activity* may apply, depending on how Mochi is distributed.
- **Mochi adoption is a CRA-compliance asset for downstream users.** A vendor selling a Mochi-based product can argue that memory-safe-by-construction language choice supports the Annex I "designed to limit attack surface" requirement. MEP-41 should document this argument for downstream use.
- **MEP-41 should not commit Mochi to CRA conformity-assessment.** CRA conformity-assessment is for products, not for languages. The right MEP-41 posture is to *enable* downstream conformity rather than *claim* it directly.
- **Cite the CRA as an example of why memory safety is an emerging regulatory expectation, not just a US-government preference.** This globalises the case for Mochi: the EU, the US, Five Eyes, and (increasingly) UK / Japan / Australia all converge on the same direction.
- **September 11, 2026 is a meaningful date.** Any Mochi-using EU vendor needs to be ready for the vulnerability-reporting obligations. MEP-41 can pre-emptively articulate Mochi's vulnerability-disclosure policy in a CRA-compatible shape — at minimum, naming a contact and timeline for reporting Mochi-runtime CVEs to downstream users.

## §7 Open Questions for MEP-41
1. Should MEP-41 explicitly address the FOSS exemption in the CRA — i.e., clarify Mochi's distribution model and the resulting CRA obligation status?
2. Should Mochi publish a CRA-aligned vulnerability disclosure policy (24h initial, 72h full, 14d final) for the Mochi runtime, anticipating that downstream users will need it?
3. Should MEP-41 articulate, for downstream Mochi users, how Mochi adoption maps to Annex I Essential Cybersecurity Requirements? A one-page mapping would be a meaningful contribution.
4. Should Mochi commit to SBOM-friendliness (a published BOM format for the Mochi runtime + standard library) to support downstream CRA compliance?
5. The CRA-style regulation is likely to spread (UK PSTI, Japan equivalents, etc.). Should MEP-41 commit to tracking the international regulatory landscape rather than only the US one?