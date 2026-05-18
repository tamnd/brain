---
title: "Microsoft \"70% of CVEs Are Memory Safety\" Statistic"
description: "The canonical industry data point on memory-safety vulnerability prevalence, and every follow-up through 2026."
tags: ["memory-safety", "industry"]
weight: 10
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Miller (MSRC). **"Trends, challenges, and strategic shifts in the software vulnerability mitigation landscape"**, BlueHat IL 2019. Primary source for the 70% number.
- MSRC blog: **"A proactive approach to more secure code"** (Jul 2019). https://www.microsoft.com/en-us/msrc/blog/2019/07/a-proactive-approach-to-more-secure-code
- MSRC blog: **"We need a safer systems programming language"** (Jul 2019). https://www.microsoft.com/en-us/msrc/blog/2019/07/we-need-a-safer-systems-programming-language
- CISA. **"The Urgent Need for Memory Safety in Software Products"** (Dec 2023). https://www.cisa.gov/news-events/news/urgent-need-memory-safety-software-products
- NSA/CISA Joint Cybersecurity Information Sheet (June 2025). U/OO/172709-25 | PP-25-2574 | **"Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development"**. https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF
- White House ONCD, **"Back to the Building Blocks"** (Feb 2024). https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf

## §2 Claim
Matt Miller's 2019 BlueHat IL presentation reported that each year from **2006 through 2018**, approximately **70%** of vulnerabilities to which Microsoft assigned a CVE were memory-safety issues — buffer overflows, use-after-free, double-free, uninitialised memory, out-of-bounds reads/writes, type confusion, and similar. The 70% figure has remained the canonical industry shorthand ever since, despite Microsoft never having published an official follow-up restating the percentage for years after 2018.

The figure is a *percentage*, not an absolute count. It reports the fraction of Microsoft-assigned CVEs (so it captures the Microsoft ecosystem — Windows, Office, Edge, Azure, Visual Studio runtimes, etc.) classified as memory-safety. It does not directly bear on other ecosystems, though similar figures have been reported by Google Chrome (~70% of serious bugs), Mozilla Firefox (32 of 34 critical/high in one analysis), and Apple (multiple high-severity iOS vulnerabilities each year).

## §3 Scope and Limits
**Scope.** Microsoft-assigned CVEs over 2006-2018, across the Microsoft product portfolio dominated by C/C++ codebases.

**Limits.** (1) Percentage, not absolute. The total number of CVEs has *grown* over the years, so a flat 70% still means more memory-safety bugs in absolute terms each year. (2) The figure was not formally restated by Microsoft after 2018. The 2025 NSA/CISA CSI cites continuing data points but uses Google's "75% of CVEs used in the wild involved memory exploits" (Project Zero) as the most recent corroboration. (3) Some commentators argue that the percentage figure says less than it appears: a decline from 70% to 50% can come from *more non-memory bugs*, not fewer memory bugs.

## §4 May 2026 Status
**Still the canonical citation.** The 2025 NSA/CISA joint CSI continues to feature "Figure 1: Microsoft CVEs | Memory Safety vs Non-Memory Safety Patches" derived from the original 2019 data. CISA's 2023 "Urgent Need for Memory Safety" advisory leans on the 70% number. The 2024 White House ONCD report cites it. The 2025 CSI updates the picture by noting Microsoft's number has come down "from about 70% in 2016 to 50% in more recent studies", attributing the drop to Microsoft's investment in mitigations (ASLR, CFG, CET, hardware-enforced stack protection) — but 50% is still half of all CVEs, a substantial share.

The 70% figure has effectively become a regulatory shibboleth. Every US federal cybersecurity document from 2022 onward cites it. The figure is also the de facto justification for the CISA Secure-by-Design pledge memory-safety-roadmap requirement (Jan 1, 2026 deadline).

## §5 Cost
The number itself was inexpensive to produce (an internal MSRC analysis presented at one conference). The *consequences* of citing it have been enormous: it underpins every multi-year corporate Rust adoption program (Microsoft's own Rust effort in Azure / Windows components, Google's Android Rust, AWS's Rust-in-Firecracker). Microsoft's Rust adoption costs alone run into many hundreds of engineer-years over 2020-2026.

For corroboration: Google's published Android numbers (see industry/02) — memory-safety bugs dropped from 223 in 2019 to under 50 in 2024 with the Rust adoption push — show the *delta* a memory-safe-language strategy can produce. Microsoft has not published a comparable Rust-adoption-impact number publicly.

## §6 Mochi Adaptation Note
The 70% figure is the **single most-cited number** in any memory-safety justification document, and MEP-41 should cite it once, accurately, with appropriate caveats.

- **Mochi can claim category eligibility.** The CISA / NSA / ONCD frame is "memory-safe language" as a *category*. Mochi-the-language is memory-safe in the same sense Go, Java, C#, Python, Swift, Rust, JavaScript are: by-construction guarantees prevent the bug classes Miller's 70% covers. MEP-41 should explicitly claim membership in this category.
- **Mochi should not over-claim.** Mochi's safety is enforced by the vm3 runtime (which is itself Go-hosted, hence inherits Go's safety, which inherits from `runtime` and the OS). MEP-41 should be honest that Mochi's safety stack is no more sound than Go's runtime. This matches how the CISA framework treats Java (memory-safe by virtue of JVM) and Python (memory-safe by virtue of CPython).
- **Cite the 70% figure once and move on.** Every memory-safety document does this, and the figure has become regulatory boilerplate. MEP-41 should follow suit rather than re-derive its own statistics.
- **Note the 2024-2025 trend.** Microsoft's number is reportedly down to 50%, Android's to under 20% (Google's late-2025 announcement). MEP-41 can use this as evidence the *strategy works* — memory-safe-language adoption demonstrably reduces the CVE share.

## §7 Open Questions for MEP-41
1. Should MEP-41 cite the 70% figure as the *motivating* number, or as a *category-membership-justification* number? They are different rhetorical moves.
2. Mochi-the-language is small. Should MEP-41 commit to publishing per-year vulnerability counts (analogous to Microsoft / Android) once the user base is large enough? Cheap forward-commitment, useful credibility.
3. Should MEP-41 distinguish between "Mochi-source CVEs" (programmer's bug, type-safe ones still possible) and "Mochi-runtime CVEs" (vm3 / vm3jit bug, memory-safety hazards possible)? This is the right distinction for any future security-disclosure policy.
4. The 50% Microsoft / 20% Android trajectory suggests that even with memory-safe languages, *some* memory-safety issues persist (typically at FFI boundaries, in `unsafe` blocks, in JITs). Should MEP-41 anticipate this — i.e., state in advance that Mochi-runtime memory-safety bugs are *possible* and there will be a process for handling them?