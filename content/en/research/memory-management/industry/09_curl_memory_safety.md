---
title: "curl, Daniel Stenberg, and the \"Is C/C++ The Actual Problem?\" Debate"
description: "Stenberg's curl CVE data, the Hyper / Rust experiment, and the unresolved 2026 question of whether memory-safe languages are the whole answer."
tags: ["memory-safety", "industry"]
weight: 90
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Daniel Stenberg blog: https://daniel.haxx.se/blog/
- Stenberg, **"half of curl's vulnerabilities are C mistakes"**, March 2021. https://daniel.haxx.se/blog/2021/03/09/half-of-curls-vulnerabilities-are-c-mistakes/
- Stenberg, **December 2024 follow-up post** (URL pattern: https://daniel.haxx.se/blog/2024/12/12/), discussing CVE-2024-11053 and updating the C-attributable percentage to ~40%.
- The New Stack, **"Curl's Daniel Stenberg on Securing 180,000 Lines of C Code"**. https://thenewstack.io/curls-daniel-stenberg-on-securing-180000-lines-of-c-code/
- Software Engineering Radio episode 688 (Oct 2025), **"Daniel Stenberg on Removing Rust from Curl"**. https://se-radio.net/2025/10/se-radio-688-daniel-stenberg-on-removing-rust-from-curl/
- Slideshare deck, **"rust in curl"** from curl up 2024. https://www.slideshare.net/slideshow/rust-in-curl-by-daniel-stenberg-from-curl-up-2024/268617322
- Heise / Hacker News coverage of Stenberg's CVE-and-CVSS critique (2024-2025).
- CVE details for curl: https://www.cvedetails.com/product/1055/Daniel-Stenberg-Curl.html

## §2 Claim
Daniel Stenberg has published the most-rigorous-by-an-individual-maintainer set of memory-safety statistics for a single C codebase. His December 2024 post on `daniel.haxx.se` updates the long-running analysis:

- **161 CVEs total** in curl history (as of Dec 2024).
- **~40% of all curl security problems are attributable to C** (i.e., would have been prevented by a memory-safe language).
- **~50% of high/critical severity curl CVEs are C-attributable**.
- The median time a security problem exists in curl before being fixed: **2,583 days** (about 7 years).
- The earlier March 2021 figure was 18/26 (~69%) — meaning the C-attributable percentage has **dropped over time** as the project ages and as non-C bug classes accumulate.
- "A more narrow audit in 2024 resulted in 0 CVEs — an encouraging trend."

Stenberg knows the precise commit that introduced each CVE because every confirmed security issue prompts a personal git-archaeology exercise to find the introducing commit. He famously self-attributes nearly every curl CVE to his own mistakes.

The 2024 CVE that prompted the December 2024 post — CVE-2024-11053 — was at the time the **oldest bug ever fixed in curl** (introduced ~9,039 days, or ~25 years, before being fixed). Notably, this bug was a *plain logic error* and would *not* have been prevented by a memory-safe language. After January 2025 bisecting was redone and the bug was relocated more recently, but the point stands: not every long-lived bug is a memory-safety bug.

## §3 The Hyper/Rust Experiment
From 2020 through late 2024-2025, Stenberg partnered with the Internet Security Research Group (ISRG, of Let's Encrypt fame) to integrate **Hyper** — a Rust HTTP library — as an alternative HTTP backend for curl/libcurl. The goal: leverage Rust's memory safety in a critical security-sensitive component of one of the most-deployed pieces of software on Earth.

**The experiment ended.** In late December 2024 Stenberg announced the discontinuation of Hyper backend support and the removal of the related code. His phrasing: "The journey is ending. The experiment is over. We tried, but we failed." The SE Radio episode 688 (October 2025) is Stenberg's most-detailed public discussion of what went wrong:

- The last 5% of integration work was disproportionately difficult.
- Maintaining two HTTP backends (native C + Hyper Rust) added support and complexity costs that exceeded the security benefit.
- User support for the Rust backend was insufficient — Stenberg reports that the user community largely did not exercise the Hyper backend.
- The C codebase was *already* well-audited and well-fuzzed; the marginal security improvement from Hyper was less than the maintenance cost.

Notably, Stenberg has been clear curl will *not* be rewritten in Rust: at FOSDEM 2025, "We're not going to re-write Curl in Rust. In any language — we're not going to re-write it at all. It's there already." He acknowledged Rust as "possibly a great language" and said third-party curl dependencies can still be written in Rust.

## §4 May 2026 Status
**The "is C the actual problem" debate is live but converging.** As of May 2026:

- **The empirical answer is: yes, but not exclusively.** ~40-50% of curl's high-severity CVEs are C-attributable. The other 50-60% are *logic* bugs that no language change would prevent.
- **Stenberg's posture is the leading "moderate" position**: memory-safe languages reduce one category of bugs significantly, but rewriting a mature codebase is rarely a positive-ROI decision; the right move is *new code in memory-safe languages, old code stays where it is*.
- This converges with Google's Android strategy ("focus on new code") and is now the de-facto industry consensus.
- The Hyper-removal story is a useful **counterweight** to "Rust solves everything" rhetoric. Memory-safe-language adoption has real engineering costs and isn't always worth it.

For Mochi, the relevant takeaway is that **the Mochi-vs-C/C++ comparison is more nuanced than "memory-safe languages prevent 70% of CVEs"**. The number is real, the trend is real, but the question of *when* a rewrite is worth it is genuinely hard.

## §5 Cost
The Hyper-in-curl experiment is the most-detailed public example of the **failed-positive-Rust-integration** case. Cost: 5 years of intermittent engineering effort by Stenberg + ISRG + Hyper maintainers + curl contributors, ended without shipping a default Rust backend. Total cost likely in the low millions of dollars equivalent.

This is the right reference point for any conversation about cost of integrating memory-safe-language components into existing C codebases.

## §6 Mochi Adaptation Note
Stenberg's curl analysis is the **most-quotable individual-maintainer perspective** on memory safety in 2024-2026. MEP-41 should cite it for several reasons:

- **Honest framing of the upper bound.** Stenberg's ~40-50% C-attributable figure is *lower* than Microsoft's 70% and shows the variation across codebases. MEP-41 should acknowledge that memory-safe languages are not a complete answer — logic bugs persist.
- **The "0 CVEs from 2024 narrow audit" data point is a useful counter-narrative.** Mature, well-audited C codebases can achieve low CVE rates. MEP-41 should not over-claim that Mochi is intrinsically more secure than well-audited C — what Mochi offers is a *lower-effort path to memory safety*, not a *guaranteed-no-bugs path*.
- **The Hyper-removal story is a warning about FFI integration cost.** Mochi-as-an-FFI-component-in-other-languages would face similar challenges. MEP-41 should be honest that Mochi is most valuable when used end-to-end, not as an FFI library inside larger non-Mochi codebases.
- **Stenberg's median-7-year time-to-fix figure is sobering.** Even a well-maintained project has bugs in the field for years. MEP-41 should plan for Mochi to have CVEs and to have a published response timeline.

## §7 Open Questions for MEP-41
1. Should MEP-41 cite Stenberg's curl numbers as the *honest counter-balance* to the Microsoft 70% / Android 76% figures? Doing so signals intellectual honesty.
2. The Hyper-in-curl failure suggests that *retrofitting* memory-safe languages into existing C/C++ projects is hard. Should MEP-41 explicitly position Mochi as a *new-project* language rather than a retrofit candidate?
3. Stenberg's "we are not going to rewrite curl" position is the consensus position for mature C codebases. Should MEP-41 acknowledge this and frame Mochi as complementary to (not replacing) existing C/C++ for legacy systems?
4. Stenberg's data shows the C-attributable percentage *declining* over time in a single project as non-memory bugs accumulate. Does this mean Mochi should *also* publish "what would have been prevented" analysis for any Mochi-runtime CVE that occurs? Cheap and informative.
5. Should MEP-41 commit to a Stenberg-style git-archaeology discipline for every Mochi-runtime CVE — i.e., identify the introducing commit, classify the bug, and publish the analysis? Sets a high but reachable transparency bar.