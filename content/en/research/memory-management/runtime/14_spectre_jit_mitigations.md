---
title: "Spectre Mitigations in Hosted JITs"
description: "Speculative-execution attacks haven't gone away. As of May 2026, every shipping JIT either implements index masking + bounds-check hardening, or relies on process-level Site Isolation, or both. The consensus: software mitigations alone are necessary but not sufficient; hardware (eIBRS, BHI controls, CET-IBT) carries the load on CPUs that have it."
tags: ["memory-safety", "runtime"]
weight: 140
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Spectre v1 (Bounds Check Bypass)** and **Spectre v2 (Branch Target Injection)** disclosed Jan 2018, Kocher et al.
- WebKit's response: https://webkit.org/blog/8048/what-spectre-and-meltdown-mean-for-webkit/ (2018), still architecturally accurate.
- Chrome's response: Site Isolation (out-of-process iframes); Spectre-aware codegen in V8.
- Intel guidance: https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/runtime-speculative-side-channel-mitigations.html, https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/branch-history-injection.html.
- Linux kernel mitigations: https://docs.kernel.org/admin-guide/hw-vuln/spectre.html.
- Recent attacks: PB-Inception (2025), BHI variants (2024-2025), CVE-2024-28956, CVE-2025-24495.

## §2 Mechanism

Spectre attacks induce the CPU to speculatively execute instructions that wouldn't run architecturally, then read the resulting cache state via a side channel.

### Per-variant defences

| Variant | Mitigation |
|---|---|
| v1 (Bounds Check Bypass) | **Index masking** in JITs, `LFENCE` insertion, `array_index_nospec`-style barriers |
| v2 (Branch Target Injection) | **Retpoline** (compiler-level), **IBRS**/**eIBRS** (microcode), **IBPB** on context switch, **STIBP** for SMT siblings |
| v4 (Speculative Store Bypass) | `SSBD` MSR |
| BHI (Branch History Injection, 2022) | BHB clearing on domain entry, `BHI_DIS_S` MSR; future CPUs handle in hardware |
| MDS/L1TF | Hardware fixed in newer CPUs; software fallbacks via flush-on-VMEntry |

### JIT-specific tactics

WebKit's index masking is the textbook: every JIT-compiled array access does
```asm
ldr x_len, [array, #length_off]
mask = round_up_to_pow2(x_len) - 1
masked = idx AND mask
ldr value, [array_base + masked * stride]
```
Modern CPUs do not speculate on AND-masking, so even if the bounds branch is mispredicted, the masked index can only point inside a power-of-two-rounded subset of the array — not arbitrary memory. WebKit reported ≤ 2.5% slowdown on JetStream.

V8 uses a similar mask-based hardening on certain hot paths and relies more heavily on Site Isolation (each web origin in its own OS process) so that a successful in-process leak can only read same-origin data.

### Hardware-assisted controls

- **eIBRS** (Enhanced IBRS): CPU enters a mode where indirect-branch prediction can't be influenced by less-privileged code. Enabled by default on modern Intel chips; obsoletes retpoline at the kernel level.
- **IBPB**: Indirect Branch Predictor Barrier; flushes prediction state at context switch.
- **STIBP**: Single-Thread Indirect Branch Predictor; prevents SMT-sibling cross-pollination.
- **AMD jmp2ret / safeRET / IBRS**: AMD's parallel set, used to mitigate BTC-IND and BTC-RET.

### Recent attacks (2024-2025)

- **PB-Inception** (Wikner et al., ETH Zurich, 2025): bypasses IBPB on AMD Zen 1+/2 by mis-training the return predictor *before* the barrier executes.
- **CVE-2024-28956, CVE-2025-24495**: Intel-specific. Re-enable user-user, guest-guest, even guest-host Spectre-v2 via self-training. Intel and ARM issued advisories.
- The Register (May 2025): "Intel data-leaking Spectre defenses scared off once again."

The arms race continues. Microcode updates and `IBPB-on-entry` patches are still landing in 2025.

## §3 Memory-safety property

Spectre mitigations are not memory safety per se. They defend against **information leak via speculative execution**. The leaked bytes are normally not corruptible (it's a read-only side channel), but in a JIT context, the consequence of leaking a JIT-cache layout or an internal pointer can chain into a full sandbox bypass.

The consensus property a hosted JIT must provide:
- **No speculative OOB reads** from JIT-emitted code (index masking or speculation barriers).
- **No speculative branch-target injection** across security domains (rely on hardware eIBRS or compiler retpolines).
- **No timing oracle for the engine's secrets** (e.g. random seeds, address-space layout).

Combined with process-level isolation (Site Isolation in Chromium, per-tab WebContent process in Safari), this is enough to put Spectre into the category of "very expensive, very specialised attacker territory" — but not zero risk.

## §4 Production status (May 2026)

- Every shipping JIT (V8, JSC, SpiderMonkey, Hermes, .NET, JVMs) implements at least Spectre v1 hardening on JIT'd code.
- Linux kernel reports mitigation status via `/sys/devices/system/cpu/vulnerabilities/`.
- eIBRS is standard on Intel since Tiger Lake; AMD has parallel mechanisms (jmp2ret, safeRET).
- Site Isolation has been on by default in Chrome for years; Safari uses per-tab WebContent processes.
- WebAssembly engines apply the same JIT hardening; Wasm doesn't escape Spectre's reach.
- The recent (2024-2025) attacks have re-opened the question of "is software hardening ever sufficient?" Answer: no, but it raises the bar substantially when combined with hardware controls.

## §5 Cost

- **Index masking:** ≤ 2.5% on JetStream (WebKit measurement).
- **Retpoline:** ~5-15% slowdown on indirect-call-heavy kernel and userspace code; obsolete on CPUs with eIBRS.
- **eIBRS:** ~1-3% throughput.
- **IBPB on context switch:** 5-15% on syscall-heavy workloads; can be disabled per process.
- **Site Isolation:** ~10-13% memory overhead per renderer process; throughput cost negligible.

## §6 Mochi adaptation note

vm3jit (MEP-40 Phase 5) emits machine code, so it inherits the JIT-Spectre obligation. *However*, Mochi's threat surface is much narrower than a browser's:

- Mochi code is *not* user-supplied JS-from-the-internet. It's developer-authored Mochi source compiled ahead of time. The "attacker submits adversarial JS" model doesn't apply directly.
- The risk is "attacker-controlled *data* triggers a Spectre gadget in the JIT'd code that leaks server-process secrets." Still real, especially for Mochi-as-web-handler.

Smallest plumbing:

1. **Index masking in vm3jit accessors (MEP-40 §6.5).** Every JIT-emitted `ListGet`, `StringByte`, `MapGet` must mask the index against the array length *before* the speculative load. The pattern is identical to WebKit's:
   ```
   mask = nextPow2(len) - 1
   safe_idx = idx & mask
   value = base[safe_idx]
   ```
   This is ~3 extra instructions per access and costs ≤ 2-3% per JSC measurements. Easy lift.
2. **No `eval`-style attacker-controlled bytecode.** This is a Mochi design property: bytecode is compiled from `.mochi` source AOT. We should not add a `compile-string-at-runtime` API without a separate threat-model review.
3. **eIBRS/CET reliance.** Rely on the host OS + CPU mitigations for v2-class attacks. Document the supported-platform baseline: "vm3jit assumes eIBRS-equipped CPUs on x86_64 and BTI-equipped CPUs on AArch64."
4. **Site-isolation analogue.** If Mochi grows multi-tenant deployment (a single process running code for multiple users), we need per-tenant arena isolation *and* OS-level process isolation. This is a vm3jit-level question only insofar as the JIT cache must not leak across tenants.

No design conflict. The cost is real (a few percent in JIT'd accessors) but unavoidable for production.

## §7 Open questions for MEP-41

- Should the index-masking be unconditional in vm3jit, or gated on a hardening flag? My recommendation: unconditional. The 2-3% cost is the cost of being a JIT in 2026.
- Does Mochi need a documented multi-tenancy story? If yes, Spectre is one of several issues; if no, Site-Isolation-style mitigations are out of scope.
- BHI / BHB clearing: does vm3jit need to emit a software BHB clear at "domain transitions"? In Mochi the only domain transition is "Mochi code calling out to a Go function." Probably we get this from the kernel on syscall, but worth checking.
- Should there be a runtime-disable for Spectre hardening for users who explicitly opt out (e.g. trusted-input batch jobs)? Probably no — the flag itself is an attack surface.

## Sources

- [What Spectre and Meltdown Mean For WebKit (WebKit blog)](https://webkit.org/blog/8048/what-spectre-and-meltdown-mean-for-webkit/)
- [Intel — Managed Runtime Speculative Execution Side Channel Mitigations](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/runtime-speculative-side-channel-mitigations.html)
- [Linux kernel — Spectre side channels](https://docs.kernel.org/admin-guide/hw-vuln/spectre.html)
- [Intel — Branch History Injection (BHI)](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/branch-history-injection.html)
- [Oracle — Understanding Spectre v2 Mitigations on x86](https://blogs.oracle.com/linux/understanding-spectre-v2-mitigations-on-x86)
- [PB-Inception (Wikner et al., 2025)](https://comsec.ethz.ch/wp-content/files/ibpb_sp25.pdf)
- [Project Zero — JSC Exploits](https://googleprojectzero.blogspot.com/2019/08/jsc-exploits.html)