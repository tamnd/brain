---
title: "White House ONCD \"Back to the Building Blocks\" (February 2024)"
description: "The White House Office of the National Cyber Director's memory-safety report and the C/C++-adverse federal stance."
tags: ["memory-safety", "industry"]
weight: 50
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- White House Office of the National Cyber Director. **"Back to the Building Blocks: A Path Toward Secure and Measurable Software"**, February 2024. 19 pages. https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf
- Press release: https://bidenwhitehouse.archives.gov/oncd/briefing-room/2024/02/26/press-release-technical-report/
- Anjana Rajan, Assistant National Cyber Director for Technology Security — primary spokesperson at release.
- Coverage: Tom's Hardware, **"White House urges developers to avoid C and C++, use 'memory-safe' programming languages"**. https://www.tomshardware.com/software/security-software/white-house-urges-developers-to-avoid-c-and-c-use-memory-safe-programming-languages
- The Record from Recorded Future News, **"After decades of memory-related software bugs, White House calls on industry to act"**. https://therecord.media/memory-related-software-bugs-white-house-code-report-oncd
- InfoWorld, **"White House urges developers to dump C and C++"**. https://www.infoworld.com/article/2336216/white-house-urges-developers-to-dump-c-and-c.html
- Stack Overflow Blog, **"In Rust we trust? White House Office urges memory safety"** (Dec 2024). https://stackoverflow.blog/2024/12/30/in-rust-we-trust-white-house-office-urges-memory-safety/
- ISO C++ Directions Group response (Feb 2024) pushing back on the framing.

## §2 Claim
The report's central claim is a **dual call to action**:

1. **Adopt memory-safe languages.** Memory-safe languages are the most effective single intervention for reducing memory-safety vulnerabilities at scale. The report explicitly names **C and C++** as examples of memory-unsafe languages and **Rust** as an example of a memory-safe language.
2. **Improve software measurability.** The research community should make progress on the hard problem of measuring software cybersecurity quality — so that procurement officers, regulators, and customers can compare products meaningfully.

The report frames memory-safety vulnerabilities as a **35-year problem**: from the Morris worm (1988) through Slammer (2003), Heartbleed (2014), Trident (2016), and BLASTPASS (2023) — all rooted in memory-safety bugs. It cites Microsoft and Google studies that "approximately 70 percent of all security vulnerabilities are caused by memory safety issues".

The report distinguishes **spatial** memory-safety bugs (out-of-bounds access) from **temporal** bugs (use-after-free, double-free, race-on-free) and notes that *both* must be addressed.

The report carves out a careful exception for **space systems**, noting three constraints (close-to-kernel, deterministic timing, no garbage collector) and acknowledging that "at this time, the most widely used languages that meet all three properties are C and C++". This is the report's only explicit concession to legacy C/C++ use.

## §3 Scope and Limits
**Scope.** Federal-government technology procurement, US software-industry direction-setting, research community framing. The report is technical and aspirational, not regulatory.

**Limits.** No enforcement, no procurement clauses, no funding attached. It is a *signal*, not a rule. The "C/C++-adverse" framing is real but rhetorical: the report does not ban C/C++ acquisition, and its space-systems carve-out shows the authors were aware of the impracticality of a hard ban. Critics — most notably the ISO C++ Directions Group — pointed out that memory safety is "a very small part of security" and argued for the in-progress C++ Profiles work as an alternative path.

## §4 May 2026 Status
**Has not been formally re-issued as of May 2026 by the current administration.** The original Biden-era report sits on the National Archives mirror; the document text has not been retracted, and the policy direction has been reinforced by subsequent NSA + CISA guidance (June 2025 CSI) and by the DoD SWFT framework (2025). The Biden-era ONCD also issued related letters / requests for information on open-source security and software measurability.

The 2025 NSA-CISA joint CSI explicitly cites the 2024 ONCD report as a baseline, treating it as the canonical White House position even after administration change. No new ONCD report has been issued that this research has surfaced.

C++ continues to evolve with **Profiles** (Stroustrup's proposed mechanism for selectively restricting unsafe C++ features at compile time), targeting C++26 and beyond. This is the C++ ecosystem's own response to the ONCD pressure. Whether it satisfies the ONCD criteria remains debated; the ONCD report's authors did not endorse Profiles as a substitute for memory-safe languages.

## §5 Cost
The cost of producing the report is negligible (a small ONCD technical-report effort). The *industry cost* is enormous and largely indirect: the report's signalling effect contributes to multi-billion-dollar memory-safe-language adoption efforts at major vendors. The exception carve-out for space systems means specialist domains face no direct conversion pressure, but the broader software market does.

For a small project like Mochi, the "cost" is zero — Mochi is memory-safe by construction. The cost to *anyone using Mochi* is the same as adopting any other memory-safe language.

## §6 Mochi Adaptation Note
The ONCD report is the **single most authoritative White House signal on memory safety**, and Mochi should explicitly align with it.

- **The C/C++-adverse stance is what MEP-41 should explicitly endorse.** Mochi is in part a response to the same observation: dynamic languages and Go-style languages are memory-safe by construction; C and C++ are not; the cost of bug-fixing in C/C++ is unbounded. MEP-41 can quote the report's framing.
- **The "spatial vs temporal" distinction is the right vocabulary.** MEP-41 should use this terminology when discussing Mochi's Cell design: the (base, slab_idx) component handles spatial safety; the generation tag handles temporal safety. Both are first-class concerns, both are explicitly addressed by the Cell design, and the ONCD report is the right citation.
- **The "memory safety is the dominant single CWE category" framing is the right rhetorical move.** MEP-41 can use the ONCD's 35-year vulnerability history as the motivating story for why a new language warrants a new runtime design.
- **The space-systems carve-out is irrelevant to Mochi.** Mochi is not aimed at hard-real-time embedded systems. MEP-41 need not engage with the carve-out except to note that Mochi targets the general-application space the report applies to.
- **The "software measurability" leg of the ONCD report is interesting for Mochi.** ONCD asked the research community to make progress on measurability. Mochi can contribute one tiny piece: publishing memory-safety-relevant data about Mochi-runtime issues over time. MEP-41 can commit to this as a contribution to the measurability agenda.

## §7 Open Questions for MEP-41
1. Should MEP-41 directly quote the ONCD report's "memory-safe languages are the most effective intervention" sentence as its motivating claim?
2. Should MEP-41 explicitly classify Mochi as *memory-safe-by-construction at the language layer, memory-safe-by-runtime-enforcement at the program-state layer*? This is more precise than the ONCD's binary safe/unsafe framing.
3. The ONCD's measurability ask is mostly unanswered by industry. Should Mochi commit to publishing per-release memory-safety metrics as a small contribution to this open problem?
4. C++ Profiles are positioned as the C++ alternative path. Should MEP-41 briefly contrast Mochi's runtime-enforced safety with the static-analysis-augmented-C++ direction Profiles represents?
5. The ONCD report does not name Go, Java, Python, or JavaScript — only Rust as the safe-language example. Should MEP-41 note that Mochi is more in the Go / Java / Python family (runtime-enforced) than in the Rust family (compile-time-enforced)? Honest framing matters here.