---
title: "Google: Android Rust, Chrome Rust, V8 Sandbox"
description: "Google's published 2022-2026 data on memory-safety progress — Android's 76% → <20% trajectory, the CVE-2025-48530 near-miss, the V8 sandbox."
tags: ["memory-safety", "industry"]
weight: 20
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Google Online Security Blog. **"Rust in Android: move fast and fix things"** (Nov 2025). https://security.googleblog.com/2025/11/rust-in-android-move-fast-fix-things.html
- Coverage: The Hacker News, **"Rust Adoption Drives Android Memory Safety Bugs Below 20% for First Time"** (Nov 2025). https://thehackernews.com/2025/11/rust-adoption-drives-android-memory.html
- 2024 baseline: The Hacker News, **"Google's Shift to Rust Programming Cuts Android Memory Vulnerabilities by 68%"** (Sep 2024). https://thehackernews.com/2024/09/googles-shift-to-rust-programming-cuts.html
- The Register, **"Google's Rust belts bugs out of Android in Safe Coding push"** (Sep 2024). https://www.theregister.com/2024/09/25/google_rust_safe_code_android/
- Android Open Source Project memory-safety page. https://source.android.com/docs/security/test/memory-safety
- Chrome Security quarterly summaries: https://www.chromium.org/Home/chromium-security/quarterly-updates/ (Q1-Q4 2024, Q1-Q3 2025 all available).
- V8 sandbox README: https://chromium.googlesource.com/v8/v8.git/+/refs/heads/main/src/sandbox/README.md
- CVE-2025-48530 (CrabbyAVIF, CVSS 8.1): first near-miss Rust memory-safety CVE in Android, patched Aug 2025 security update.

## §2 Claim
Google has published the most-detailed industry data set on a multi-year memory-safe-language adoption program:

- **Android 2019**: 76% of all Android vulnerabilities involved memory safety issues, with 223 memory-safety CVEs in absolute terms.
- **Android 2024**: down to 24%. Absolute memory-safety bugs under 50.
- **Android 2025**: **below 20% for the first time**. 2025 was also the first year **more lines of Rust were added to Android than lines of C++**.
- **Rust vulnerability density vs C/C++**: Google reports a *1000× reduction* in memory-safety vulnerability density in Rust code vs C/C++ code in Android.
- **Process efficiency**: Rust changes have a 4× lower rollback rate and spend 25% less time in code review than C/C++ changes — *the safer path is also the faster path*, in Google's framing.
- **First Rust near-miss**: CVE-2025-48530 (Aug 2025), CVSS 8.1, a linear buffer overflow in CrabbyAVIF (an AVIF parser written in `unsafe` Rust). Caught before public release. Scudo allocator made it non-exploitable on Pixel.

For Chrome:
- **Rust JSON parser**: rolled to 100% on all platforms except Android WebView. Decoding 25-40% faster at p50, 42-99.5% at p99.
- **Rust PNG decoder**: landed in Chromium tree, on track for Finch experiments in early 2025.
- **Memory-safe browser kernel prototype**: in Rust, iterating through 2024-2025.
- **V8 sandbox**: still officially "in development, not a security boundary" as of late 2025, but Leaptiering shipped to deliver fine-grained CFI for JavaScript calls; trusted-space migration of BytecodeArrays / WasmInstanceObject completed; bytecode verifier under development.

## §3 Scope and Limits
**Scope.** Android user-space components (most new code written in Rust or Kotlin/Java), Chrome browser parsers (PNG, JSON, web fonts), V8 sandbox and CFI hardening, the Android Linux kernel (6.12 ships Google's first production Rust driver, with a Rust kernel-mode GPU driver in collaboration with Arm and Collabora).

**Limits.** Memory-safety CVE *share* is dropping, but absolute counts are non-zero and zero-days continue (8 in-the-wild Chrome zero-days in 2025: CVE-2025-2783, -4664, -5419, -6554, -6558, -10585, -13223, -14174). V8 zero-days are dominated by type-confusion bugs in the JIT compilers — exactly the category Mochi's vm3jit will face. The V8 sandbox is not yet a security boundary. C/C++ remains the bulk of Chrome and a large fraction of Android.

## §4 May 2026 Status
**Mature, ongoing, and publicly tracked.** Google publishes quarterly Chrome Security summaries with explicit memory-safety progress data. Android Rust is now a primary path for new code; the Rust-in-Linux kernel work has shipped its first production driver (Android 6.12 kernel). The strategy is *not* to rewrite legacy code but to ensure new code is memory-safe — backed by the empirical observation that vulnerabilities are concentrated in new/recently-modified code (the "exponential decay" hypothesis).

The CrabbyAVIF near-miss (CVE-2025-48530) is publicly framed by Google as confirmation that the strategy *works*: even when an `unsafe` Rust bug occurs, the Scudo allocator's guard pages render it non-exploitable; Google plans to continue issuing CVEs for sufficiently severe Scudo-mitigable bugs, working to make Scudo mandatory on all Android devices.

## §5 Cost
Multi-hundred engineer-years across 2020-2026. Google has not published a precise cost figure, but the visible deliverables include: Rust toolchain integration into AOSP, Rust support in the Linux kernel build, Rust ports of dozens of parsers/codecs in Chromium, the V8 sandbox + Leaptiering + bytecode-verifier effort, the Android Java/Kotlin runtime hardening, the Scudo allocator, the LibAFL integration. The Android Rust effort alone is documented in multiple Google Online Security Blog posts spanning 2021-2025. Estimated: ~$100-200M in direct labour costs over the period, paid back through Google's own security improvement (CVE counts) and reduced rollback rate (4× improvement per change).

## §6 Mochi Adaptation Note
Google's data is the **strongest single empirical justification** for any "we are a memory-safe language" claim, and MEP-41 should use it.

- **The Android 76% → 20% trajectory is the headline number to cite.** It is the most compelling single graph in the field. MEP-41 should reproduce or cite the November 2025 Google blog post as the primary evidence that memory-safe languages deliver measurable security wins at scale.
- **Adopt the "new code, not rewrite" framing.** Google's explicit strategy is to focus on new code, citing the empirical observation that vulnerabilities cluster in new/recently-modified code. Mochi is *all* new code, in the sense that it has no legacy C++ to retrofit. MEP-41 can claim this as a structural advantage.
- **The CrabbyAVIF near-miss is the right cautionary tale.** It shows that even Rust-with-`unsafe` can have buffer overflows. The lesson for Mochi: the Mochi-source language is safe; the Go-implemented runtime is not automatically safe just because it's in Go (Go has its own `unsafe` package). MEP-41 should call out the runtime as a TCB.
- **V8 zero-days are a warning.** Mochi's vm3jit is in the *same category* as V8 — a JIT for an interpreted language, where the JIT itself is implemented in `unsafe` host-language code. The 2025 V8 type-confusion zero-days (CVE-2025-6554, -10585, -13223) are exactly the bug class vm3jit could exhibit. MEP-41 should commit to (a) fuzzing the JIT, (b) optionally disabling the JIT for high-assurance deployments, (c) documenting the JIT's role in the TCB.
- **The V8 sandbox concept is the right model for vm3jit's blast radius.** Google's V8 sandbox aims to *contain* JIT compromise even if the JIT has bugs. Mochi could pursue an analogous "vm3jit sandbox" — restrict the JIT's output to a defined region — though this would be a future MEP, not MEP-41.

## §7 Open Questions for MEP-41
1. Should MEP-41 lead with the Android 76% → 20% number as the headline industry data point? It is the most compelling, recent, and Google-published number available.
2. Should Mochi commit to publishing annual memory-safety statistics in Android style once the user base supports it?
3. The Android Scudo allocator's guard pages turned CVE-2025-48530 into a non-exploitable bug. Does Mochi's arena allocator have analogous defence-in-depth? If not, should MEP-41 specify *adding* guard pages between arenas or between slabs?
4. The V8-style sandbox model (constrain JIT memory access to a defined region) is the right architectural direction for vm3jit. Should MEP-41 mention this as future work?
5. The "more lines of Rust than C++ added in 2025" milestone is a watchable indicator. Mochi's analogue: track the ratio of Mochi-source code to `unsafe` Go in the runtime. Worth committing to publish.