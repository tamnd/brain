---
title: "Chrome Memory-Safety Data and the Rust-in-Chrome Rollout"
description: "Chrome Security's published per-quarter memory-safety data for 2024-2026, the JSON / PNG / fonts Rust rollouts, and the V8 sandbox."
tags: ["memory-safety", "industry"]
weight: 80
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Chrome Security quarterly summaries: https://www.chromium.org/Home/chromium-security/quarterly-updates/
  - **Q1 2024**: https://groups.google.com/a/chromium.org/g/chromium-dev/c/K_HO5LsPDKc
  - **Q2 2024**: https://groups.google.com/a/chromium.org/g/chromium-dev/c/cMM7RIc1kZI
  - **Q3 2024**: https://groups.google.com/a/chromium.org/g/chromium-dev/c/KOmfh5BW6Mw
  - **Q3 2025**: https://groups.google.com/a/chromium.org/g/security-dev/c/s-UR_4pJvOY
- Chromium memory-safety policy page: https://www.chromium.org/Home/chromium-security/memory-safety/
- V8 Sandbox README: https://chromium.googlesource.com/v8/v8.git/+/refs/heads/main/src/sandbox/README.md
- 2025 vulnerability landscape: Quttera, **"Inside Chrome's 2025 Vulnerability Landscape: 80 CVEs Revealed in V8 and Core Components"**. https://blog.quttera.com/post/inside-chrome-80-vulnerabilities-since-jan-2025
- Penligent AI, **"Chrome Zero-Day Vulnerabilities Exploited in 2025"** (CVE-2025-14174 analysis). https://www.penligent.ai/hackinglabs/chrome-zero-day-vulnerabilities-exploited-in-2025-a-comprehensive-analysis-of-cve-2025-14174-v8-type-confusion-and-sandbox-escapes/

## §2 Data
Chrome's published memory-safety rollout (selected highlights, 2024-2025):

**Rust components shipped or in pipeline**
- **JSON parser** (Q3 2024): Rust replacement rolled to 100% on all platforms except Android WebView. Performance: 25-40% faster decoding at p50, 42-99.5% at p99. Runs in-process because memory-safe code does not require sandboxing.
- **PNG decoder** (Q3 2024 → 2025): Rust replacement landed in Chromium tree; Finch experiments planned for early 2025. Goal: remove the C `libpng` library entirely.
- **Web fonts parser**: Rust rewrite in progress (referenced in 2025 status).
- **Memory-safe browser kernel prototype** (Q1-Q4 2024 + Q3 2025): Rust model of browser-kernel concepts including documents, navigations, session history, process model.
- **LibAFL fuzzer** (Q3 2025): Rust-based reusable fuzzer-component library being integrated into Chrome.

**Defence-in-depth for the C++ remainder**
- **Spanification** (Q3 2024): `-Wunsafe-buffers-usage` warning expanded to **8.5 million lines of shipping C++**.
- **V8 sandbox** (multi-quarter): trusted-space migration of BytecodeArrays and WasmInstanceObject, bytecode verifier under development, `mseal`-based sealing of executable memory, memory-protection-keys-based forward-edge CFI under investigation.
- **Leaptiering** (Q3 2024): shipped, providing fine-grained forward-edge CFI for JavaScript calls.
- **App-bound cookie encryption** (Q3 2024): launched, leading to measurable decrease in detected Windows cookie theft.

**Sanitizer / fuzzing infrastructure**
- AddressSanitizer, MemorySanitizer, UndefinedBehaviorSanitizer, Control Flow Integrity, libFuzzer, AFL — all continue to catch most vulnerabilities pre-release.

**2024-2025 notable memory-safety CVEs**
- CVE-2024-3157 (out-of-bounds write in Compositing, $21K bounty).
- CVE-2024-3515 (UAF in Dawn, heap corruption).
- CVE-2024-3516 (heap buffer overflow in ANGLE).
- 8 actively-exploited Chrome zero-days in 2025: CVE-2025-2783 (sandbox escape via Mojo), CVE-2025-4664, CVE-2025-5419, CVE-2025-6554 (V8 type confusion), CVE-2025-6558, CVE-2025-10585 (V8 type confusion), CVE-2025-13223 (V8 type confusion), CVE-2025-14174 (ANGLE out-of-bounds, CISA KEV with Jan 2, 2026 federal patch deadline).
- CVE-2025-13224: V8 type confusion flagged by Google's Big Sleep AI agent.
- Over 80 Chrome vulnerabilities reported in 2025.

## §3 Scope and Limits
**Scope.** Chromium-the-browser, V8-the-JIT, Chrome-the-product across desktop and mobile platforms.

**Limits.** Chrome is overwhelmingly C++. The Rust effort, while public and visible, has so far replaced *small parsers* and the *browser-kernel prototype* — not core rendering, layout, or DOM. V8 is C++ and will remain so for the foreseeable future; the V8 sandbox is officially "not yet a security boundary". The 2025 zero-day stream shows that the V8 JIT compilers (Maglev, TurboFan, Sparkplug) remain a high-value attacker target, with type-confusion bugs in JIT-generated code being the dominant class.

## §4 May 2026 Status
**Active, ongoing, publicly tracked.** Chrome Security publishes quarterly updates that explicitly enumerate Rust adoption, sanitizer wins, V8 sandbox progress, and CFI work. The 2024-2025 pattern is *consistent incremental Rust adoption in small components* alongside *aggressive C++ hardening* (Spanification, V8 sandbox, Leaptiering, mseal) in the bulk codebase.

The V8 sandbox VRP (Vulnerability Reward Program) launched in 2024-2025 — a strong signal that V8 sandbox bugs will be paid out even though the sandbox is not yet officially a security boundary, indicating Google's confidence that the sandbox is *almost* shippable as a boundary.

The CVE-2025-13224 detection by Google's **Big Sleep AI agent** is the first publicly-acknowledged AI-found-zero-day in a major browser, indicating a new vector in the defensive ecosystem.

## §5 Cost
Chrome's memory-safety effort is one of the largest single-product memory-safety investments in industry. Estimated at multiple hundreds of engineer-years over 2020-2026: the Spanification effort alone touched 8.5M lines of C++. V8 sandbox + Leaptiering are multi-engineer-year undertakings. The Rust component rollouts are smaller but ongoing.

Performance: the Rust JSON parser is *faster* than the C++ original, because removing sandboxing wins more than Rust's safety overhead costs. This is a meaningful data point — memory-safe-language adoption is not always a performance regression.

## §6 Mochi Adaptation Note
Chrome is the **most-visible large-scale Rust-adoption-in-C++ case study** and the **most-relevant data on JIT memory-safety hazards**. Both matter for MEP-41.

- **The Rust-JSON-parser performance win is the most-quotable data point.** "Replaced C++ JSON parser with Rust, removed sandboxing because memory-safe, ended up 25-40% faster at p50 and 42-99.5% faster at p99." This is the strongest single counter to "memory safety is slow" objections. MEP-41 can cite this when discussing Mochi's runtime overhead.
- **The V8 zero-day stream is a direct warning for vm3jit.** Eight actively-exploited Chrome zero-days in 2025, dominated by **V8 type confusion in JIT compilers**. Mochi's vm3jit is in the same architectural category. MEP-41 must commit to:
  - Fuzzing the JIT continuously.
  - Documenting the JIT as part of the TCB.
  - Considering a "vm3jit sandbox" (V8-sandbox-equivalent) as a future MEP.
  - Allowing the JIT to be disabled for high-assurance deployments.
- **Spanification (8.5M lines of C++ with `-Wunsafe-buffers-usage`) is the right model for incremental in-language safety improvement.** Mochi's analogue: minimise `unsafe` Go in the vm3 runtime; commit to a periodic audit; document the surface area.
- **The Big Sleep AI-zero-day finding is a watchable trend.** AI agents are now finding zero-days. Mochi should expect AI-driven fuzzing of vm3 to be a normal part of the security landscape by 2026-2027.
- **The CISA KEV federal-patch deadlines (Jan 2, 2026 for CVE-2025-14174) reinforce CRA-style obligations.** US federal agencies are now treated like CRA-regulated EU vendors with respect to known-exploited vulnerabilities. Mochi-using federal customers will need Mochi to have a comparable patch-pipeline.

## §7 Open Questions for MEP-41
1. Should MEP-41 cite the Rust-JSON-parser performance result as evidence that memory-safe runtimes can match or beat C++ in real workloads?
2. The V8 type-confusion zero-day pattern is *exactly* the bug class vm3jit could exhibit. Should MEP-41 explicitly enumerate the JIT-specific memory-safety hazards (type confusion, out-of-bounds in compiled code, deoptimisation races) and commit to defences?
3. Should Mochi commit to publishing a quarterly memory-safety update in Chrome Security style once the user base supports it?
4. Should MEP-41 commit to a "JIT can be disabled" knob for users who want bytecode-only execution with the smaller TCB?
5. The V8 sandbox is the most-relevant defence-in-depth architecture for a JIT. Should MEP-41 reserve language for a future "vm3jit sandbox" MEP?