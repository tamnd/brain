---
title: "Use-After-Free Landscape: Temporal vs Spatial, kCFI, and the Proven-by-Construction Story"
description: "The 2024-2026 industry picture on temporal memory safety, kernel mitigations, and the convergence of UAF defences."
tags: ["memory-safety", "industry"]
weight: 100
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- MITRE CWE Top 25. CWE-416 (Use After Free) ranked 7th in 2022, 4th in 2023, remains in the top 25 in 2024-2025.
- White House ONCD, **"Back to the Building Blocks"** (Feb 2024) — formalises spatial vs temporal vulnerability distinction.
- IEEE Security & Privacy 2024, **"Full Spatial and Temporal Memory Safety for C"**, Rutgers. https://people.cs.rutgers.edu/~sn349/papers/safety-sp-2024.pdf
- CMU SEI, **"AI-Powered Memory Safety with the Pointer Ownership Model"**. https://www.sei.cmu.edu/blog/ai-powered-memory-safety-with-the-pointer-ownership-model/
- RunSafe Security, **"Types of Memory Safety Vulnerabilities & How to Address Them"**. https://runsafesecurity.com/blog/memory-safety-vulnerabilities/
- RunSafe Security, **"Memory Safety KEVs Are Increasing"** — VulnCheck data showing ~200 memory-safety KEVs in 2024. https://runsafesecurity.com/blog/memory-safety-kevs-increasing/
- Chromium memory-safety policy: https://www.chromium.org/Home/chromium-security/memory-safety/ — "CWE-416 is the source of more than a third of the high-severity security bugs in the Chromium codebase".
- 2024-2025 notable UAFs: CVE-2024-1086 (Linux nf_tables double-free → privilege escalation), CVE-2025-49844 (Redis Lua RCE), CVE-2025-49761 (Windows kernel SYSTEM compromise), CVE-2025-8292 (Chrome Media Stream RCE).
- Linux kernel CFI / kCFI: Sami Tolvanen et al., kCFI in upstream Linux since 2022; kMSAN; Linux 6.x mitigations.
- Android Scudo allocator: guard pages preventing exploitation of CVE-2025-48530 (CrabbyAVIF, Aug 2025).

## §2 Claim
Memory-safety CVEs split into two disjoint categories:

- **Spatial memory safety bugs** — out-of-bounds reads, out-of-bounds writes, buffer overflows. CWE-787 (out-of-bounds write), CWE-125 (out-of-bounds read), CWE-119 (improper restriction).
- **Temporal memory safety bugs** — use-after-free, double-free, use-after-realloc. CWE-416 (use after free), CWE-415 (double free), CWE-672 (use of expired resource).

**Spatial bugs are easier to defend against in C/C++.** Stack canaries, ASLR, fortified `memcpy`, bounds checking, AddressSanitizer in CI — all reduce exploitability. The 2024-2025 record shows that *spatial* memory-safety zero-days are increasingly rare in modern hardened software.

**Temporal bugs are much harder.** The C/C++ heap allocator has limited information about pointer liveness. Dangling pointers after `free()` are valid C — the bug is in the *use*, not the *free*. Hardware mitigations help (Intel MPX failed; CHERI capabilities do work but require new silicon; MTE on ARM is partial). Software mitigations include:

- **Hardened allocators**: Scudo (Android), GWP-ASan (Chrome), PartitionAlloc, mimalloc-secure. Reduce reliability of exploitation but don't *prevent* the bug.
- **Quarantine pools**: delay reuse of freed memory until likely-stale pointers have been cleared.
- **GC-style memory**: never reuse memory while a pointer to it might be live. This is what JVM, V8, Go, Mochi do — and is the *only* fully-effective software-level UAF defence in C-like languages.
- **Memory tagging**: MTE on ARMv8.5+, HWASan in software. Probabilistic detection; not prevention.
- **Control-flow integrity**: kCFI in Linux, Intel CET, ARM BTI. Reduces what an attacker can *do* with a UAF, doesn't prevent the UAF itself.

The dominance of CWE-416 in CVE rankings reflects this asymmetry — **temporal bugs are now the dominant memory-safety bug class** in modern hardened C/C++ codebases.

## §3 Scope and Limits
**Industry data 2024-2025:**
- VulnCheck records ~200 memory-safety KEVs in 2024 — a high. The trend in absolute terms is *up*, not down, despite the *percentage* trend going down.
- CWE-416 is **at or near the top of the CWE Top 25** every year 2022-2025.
- Chromium attributes **more than a third of high-severity bugs** to CWE-416 alone.
- 2024-2025 production UAF CVEs include CVE-2024-1086 (Linux netfilter, leveraged for kernel privilege escalation in the wild), CVE-2025-49844 (Redis Lua RCE), CVE-2025-49761 (Windows kernel SYSTEM), CVE-2025-8292 (Chrome Media Stream).
- The Linux kernel deploys kCFI, kASLR, kPGT (pointer guard tables — being explored), kmsan (kernel-level MemorySanitizer for CI), CONFIG_INIT_ON_FREE (zero memory on free, blunting some UAF exploitation), CONFIG_INIT_ON_ALLOC, GFP_USERCOPY hardening, slab freelist hardening.

**Limits.** None of the software-only defences in C/C++ *prevent* UAF; they only make it harder to exploit. The only "proven-by-construction" UAF defences in production are:
- **Tracing GC** (JVM, V8, Go, Mochi, Erlang, etc.).
- **Reference counting** (Swift, Python, sometimes Rust `Rc`/`Arc`).
- **Region-based memory** (Cyclone, parts of Rust via lifetimes).
- **CHERI capability revocation** in hardware.

Of these, *only* tracing GC, refcounting, and Rust's borrow check are mainstream. CHERI is shipping but limited to specialist deployments.

## §4 May 2026 Status
**Temporal safety is the unresolved frontier in C/C++.** Spatial safety is largely a solved problem (ASan/MSan/UBSan + Spanification-style hardening); temporal safety remains hard. The 2024-2025 production-CVE record confirms this: most actively-exploited memory-safety zero-days in 2024-2025 are *temporal*, not spatial.

**The "proven-by-construction" story is winning.** Languages with GC or borrow-checking eliminate UAF *as a category*. Rust's "no UAF in safe Rust" guarantee, plus the V8 / JVM / Go / Python reality that GC'd languages have no UAF, is the headline argument. The 2025 NSA-CISA CSI cites this directly.

**Mitigations are deployed at scale but probabilistic.** kCFI is in upstream Linux; Scudo is Android's default allocator; ARM MTE is shipping on Pixel 8 and later. Production *hardened* C/C++ has dramatically lower exploit reliability than 2010-era C/C++ — but the bugs remain present.

**Hardware solutions are emerging.** CHERI is shipping (Morello, CHERIoT, Microsoft CHERIoT-Ibex). ARM MTE is shipping. These offer hardware-enforced temporal safety, but only on specific silicon.

## §5 Cost
The aggregate cost of temporal-memory-safety mitigation in C/C++ is **enormous and ongoing**: every Linux kernel hardening feature, every allocator hardening, every browser sandbox, every fuzzing campaign. Hundreds of engineer-years per year industry-wide. The CVE bounty payouts alone — Chrome's $41K-per-high-severity, Microsoft's $20K-$200K MSRC bounties, Apple Security Bounty up to $1M — quantify the market value of UAF defences.

**Memory-safe-language adoption is competitive on cost.** Google's Android trajectory (76% → 20% memory-safety bugs over 6 years) shows that *redirecting new code* to memory-safe languages costs less per CVE prevented than continuing to harden C/C++.

## §6 Mochi Adaptation Note
**This is the single most-relevant industry topic for Mochi's Cell design.**

- **Mochi's generation tags are a temporal-safety mechanism.** The 12-bit generation field on every Cell is exactly the kind of revocation token CHERI provides in hardware — a way to say "this handle is stale because the underlying object has been reclaimed". MEP-41 should *explicitly frame* the generation tag as Mochi's UAF defence and cite the industry data showing why UAF is the dominant bug class.
- **The "proven-by-construction" story is Mochi's strongest claim.** Mochi-source code cannot produce a use-after-free, because (a) Cell handles are checked on every dereference and (b) the planned mark-sweep ensures Cells become unreachable before their generation is reused. MEP-41 should make this claim explicitly.
- **The CHERI parallel is the right architectural framing.** Mochi's Cell is a software CHERI-like capability with a revocation tag (generation). CHERIoT is the hardware analogue; Mochi is the language-runtime analogue. MEP-41 should call out the parallel (see also verification/10).
- **The 12-bit generation choice has direct industry analogue.** ARM MTE uses 4-bit tags; CHERI uses larger object-identity fields. Mochi's 12 bits sits comfortably in the middle — long enough to make ABA-style stale-handle reuse extremely improbable (1 in 4096 reuse collision rate, with practical sequences much lower because of mark-sweep ordering). MEP-41 should justify the 12-bit choice against this comparison set.
- **The industry data refutes "just harden C/C++".** Stenberg, Chrome, Microsoft, Android all show that mitigation is partial. The only way to *prevent* UAF in a language is by design. MEP-41 can use this to justify Mochi's existence.
- **kCFI / kMSAN / Scudo / MTE are *defence-in-depth*, not prevention.** Mochi gets to claim *prevention*. MEP-41 should articulate the distinction clearly.

## §7 Open Questions for MEP-41
1. Should MEP-41 explicitly state "Mochi prevents use-after-free by construction" as a top-line claim? It is true and the most-defensible claim Mochi can make.
2. Should MEP-41 justify the 12-bit generation tag against the ARM MTE 4-bit choice and the CHERI larger-field choice? Doing so makes the design legible to security architects.
3. Should MEP-41 commit to ABA-style stale-handle re-use analysis — i.e., publish a worst-case scenario for generation-tag collisions and the mitigation (mark-sweep ordering)?
4. Should MEP-41 reference the 2024 IEEE S&P "Full Spatial and Temporal Memory Safety for C" paper as the *baseline of difficulty* that Mochi avoids by virtue of being a new language?
5. CHERI is shipping in hardware. Should MEP-41 commit to a "Mochi-on-CHERI" exploration in a future MEP, anticipating that hardware capability machines may become the natural deployment target for software capability designs like Mochi's Cell?