---
title: "NSA \"Software Memory Safety\" Guidance (2022) and the June 2025 Reissue"
description: "The NSA's formal language-level guidance, the named-language list, and the joint CISA reissue."
tags: ["memory-safety", "industry"]
weight: 40
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- NSA. **"Software Memory Safety"** Cybersecurity Information Sheet, November 2022. https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/3215760/nsa-releases-guidance-on-how-to-protect-against-software-memory-safety-issues/
- NSA + CISA joint CSI. **"Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development"**, June 2025. U/OO/172709-25 | PP-25-2574. https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF
- CISA alert (June 24, 2025): **"New Guidance Released for Reducing Memory-Related Vulnerabilities"**. https://www.cisa.gov/news-events/alerts/2025/06/24/new-guidance-released-reducing-memory-related-vulnerabilities
- NSA press release on the 2025 CSI: https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4223298/
- CISA / NSA joint **"The Case for Memory Safe Roadmaps"** (2023).
- Coverage: The Register, **"CISA, NSA repeat call for memory safe programming languages"** (June 2025). https://www.theregister.com/2025/06/27/cisa_nsa_call_formemory_safe_languages/
- CPO Magazine analysis of the 2025 reissue. https://www.cpomagazine.com/cyber-security/new-cisa-nsa-joint-report-reiterates-call-for-memory-safe-languages/

## §2 Mechanism
The NSA's November 2022 Cybersecurity Information Sheet was the **first US federal-government document to formally recommend memory-safe languages by name**. It identified memory-safety vulnerabilities as "the most readily exploitable category of software flaws" and recommended that software developers and organisations adopt memory-safe languages.

The 2022 sheet listed the following languages as memory-safe: **C#, Go, Java, Ruby, Rust, Swift**. Notably absent from the original list: Python (presumably for performance / GC-related reasons), JavaScript (the NSA does not explicitly address it).

The June 2025 NSA-CISA joint reissue, **"Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development"**, expands and updates this framing. Key 2025 additions:

- Identifies the **main obstacles** to adopting memory-safe languages: legacy code dependencies, tooling immaturity in specific domains, developer training, performance concerns for hard real-time / kernel code.
- Provides **practical solutions** to each: gradual interop strategies, language-level protections, library support, robust tooling, developer training programmes.
- Cites Microsoft's CVE data (the 70% figure, see industry/01) and Google's Android Rust trajectory (76% → 24% by 2024) as empirical justification.
- References Google Project Zero data: **75% of CVEs used in the wild involved memory exploits**.
- Articulates Android as the **success story** of language-strategy-driven security improvement.

## §3 Scope and Limits
**Scope.** Recommendations to "national security customers, critical infrastructure operators, software manufacturers, and the broader software ecosystem". Not regulation; guidance.

**Limits.** The NSA does not directly enforce the guidance. It functions as a *signal* to procurement officers, defence contractors, and critical-infrastructure operators that memory-safe-language adoption is expected. The 2022 sheet's named-language list is *informative, not exhaustive* — languages not on the list (e.g., Python, JavaScript, Kotlin) are not implicitly excluded; they are simply not enumerated.

The 2025 reissue acknowledges that **memory-safe-language adoption is not a complete solution**. Defence-in-depth (sanitizers, fuzzers, runtime checks, hardware mitigations) remains necessary.

## §4 May 2026 Status
**The June 2025 NSA + CISA joint CSI is the current canonical reference.** It is cited in:
- DoD acquisition guidance documents (e.g., the SWFT framework).
- Civilian-agency federal procurement language.
- The CISA Secure-by-Design pledge's memory-safety-roadmap guidance.
- International equivalents (the UK NCSC, the Five Eyes coordination outputs).

The 2025 reissue *implicitly endorses* Rust as the preferred direction for systems-level work — it is repeatedly cited as the primary example — but stops short of mandating a specific language. The Five Eyes' 2023-2024 joint coordination ("Secure-by-Design international principles") echoes the same line.

As of May 2026 there is no further NSA reissue planned that this research has surfaced; the June 2025 document is the live one.

## §5 Cost
The cost to the NSA of producing the guidance is negligible. The *cost to industry* of complying is enormous — multi-billion-dollar Rust / safe-language adoption programmes at Google, Microsoft, AWS, Meta, Apple are all in part driven by federal-government signals like this guidance.

For Mochi specifically, the cost is zero: Mochi-the-language is already memory-safe in the same sense the NSA's named languages are.

## §6 Mochi Adaptation Note
The NSA guidance is the **primary federal-government authority that Mochi can cite to claim category eligibility**.

- **Mochi belongs on the NSA list.** Mochi-the-language has the same memory-safety properties as Go (which is on the list). The vm3 runtime is implemented in Go. MEP-41 should explicitly draw the analogy: "Mochi is memory-safe in the same sense Java, Python, JavaScript, Go, Rust, C#, and Swift are memory-safe — by-construction language-level prevention of buffer overflows, use-after-free, and the other CWE-119 / CWE-416 / CWE-787 classes the NSA enumerates."
- **The NSA's list is informal, not certified.** There is no Mochi-on-NSA-list procedure to follow. The right move is for MEP-41 to claim the property and let downstream users carry the citation.
- **The 2025 CSI's "obstacles to adoption" section is instructive.** The named obstacles — legacy code, tooling immaturity, developer training, performance — are exactly the things a small new language like Mochi can pre-empt. MEP-41 can position Mochi as *avoiding* these obstacles by design.
- **Cite the 2025 joint CSI explicitly.** This is the current authoritative document. Citing it gives MEP-41 instant federal-government legibility.

## §7 Open Questions for MEP-41
1. Should MEP-41 directly request listing on any future NSA / CISA memory-safe-language enumeration? Plausible but premature.
2. Should MEP-41 state that Mochi's by-construction memory safety is *equivalent in kind* to Java's JVM-enforced safety or Go's runtime-enforced safety, rather than to Rust's compile-time safety? This is the more honest framing — Mochi enforces safety dynamically, not statically.
3. Should MEP-41 anticipate the next NSA / CISA update (likely 2026-2027) and commit to tracking its language list?
4. The 2025 CSI emphasises "language-level protections, library support, robust tooling, developer training" as a four-pillar requirement. Should MEP-41 inventory Mochi's position on each of the four (language: yes, library: in progress, tooling: in progress, training: minimal) and commit to a plan?
5. Does Mochi want to claim NSA-CSI category eligibility, or merely *cite* the NSA-CSI as the standard frame? The first is stronger; the second is safer.