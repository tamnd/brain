---
title: "Arm PAC + BTI"
description: "Arm PAC + BTI"
tags: ["memory-safety", "hardware"]
weight: 60
date: 2026-05-18T17:00:00+07:00
---

> Pointer Authentication Codes sign code/data pointers in the unused high bits; Branch Target Identification confines indirect jumps to legal landing pads. Both ship on every modern Arm.

## §1 Provenance

- Arm, "Providing Protection for Complex Software: Pointer Authentication, BTI, and MTE." Learn-the-Architecture PDF. https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Providing%20protection%20for%20complex%20software.pdf
- Arm Newsroom, "Better Security at the Flick of a Compiler Switch: PAC + BTI." https://newsroom.arm.com/blog/pac-bti
- Liljestrand et al., "PACStack: an Authenticated Call Stack." USENIX Security 2021. https://www.usenix.org/conference/usenixsecurity21/presentation/liljestrand
- Google Project Zero, "JITSploitation III: Subverting Control Flow." 2020 (PAC bypass against JSC on iOS). https://googleprojectzero.blogspot.com/2020/09/jitsploitation-three.html
- Exodus Intelligence, "Oops Safari, I think You Spilled Something!" August 2025 (PAC + APRR bypass for CVE-2024-44308 in WebKit DFG). https://blog.exodusintel.com/2025/08/04/oops-safari-i-think-you-spilled-something/
- WebKit commit "Make it harder to get a PAC signing gadget in JIT code." May 2024. https://github.com/WebKit/WebKit/commit/3e3d0883c84955472ece1b2f2e63f31522c5440d
- Arm community blog, "Enabling PAC and BTI on AArch64 for Linux." https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/enabling-pac-and-bti-on-aarch64
- Apple Developer, "Preparing your app to work with pointer authentication." https://developer.apple.com/documentation/security/preparing-your-app-to-work-with-pointer-authentication

## §2 Mechanism

**PAC** (Armv8.3-A, mandatory in v8.5+ and v9). The CPU has up to 5 secret 128-bit keys (`IA`, `IB`, `DA`, `DB`, `GA`). Each PAC instruction (`PACIASP`, `PACIA`, `PACDA`, etc.) computes a cryptographic MAC over (pointer, 64-bit context, key) — typically QARMA-64 or QARMA3 on v9 cores — and places the result in unused high bits of the pointer (bits 63:VA, depending on TCR config). The matching `AUT*` instruction recomputes the MAC and either zeroes-out the PAC field on success or flips the pointer to a non-canonical value on failure; a subsequent dereference faults.

Typical usage:
- Function prologue: `PACIASP` signs the link register against SP-as-context, stores it on stack.
- Function epilogue: `AUTIASP; RET` verifies and returns. A stack smash that overwrites the return slot now triggers a translation fault on `RET`.
- Vtables, function pointers, language-level pointer-to-member: sign with `PACDA`/`PACIA` against the containing object's address.

**BTI** (Armv8.5-A). The first instruction at every legal indirect-branch target must be a `BTI` *landing-pad* instruction. Four flavours: `BTI c` (call), `BTI j` (jump), `BTI jc` (either), and the implicit landing pads supplied by `PACIASP`/`PACIBSP`. An indirect branch to a non-BTI target raises a Branch Target exception (`#BTI`). BTI eliminates the vast majority of useful JOP/COP gadgets without touching pointer encodings.

PACBTI on **Armv8.1-M** (Cortex-M85, M52) brings the same protection to microcontrollers, with a simpler key model.

## §3 Threat model + guarantees

- **Backward-edge CFI**: PAC on return addresses prevents ROP chaining unless the attacker can either (a) leak a signed pointer and reuse it in matching context, or (b) leak a PAC key (kept in EL1/EL2/EL3 system registers, normally unreachable from EL0).
- **Forward-edge CFI**: PAC on vtable/fnptr entries + BTI landing pads cut indirect-jump gadgets dramatically. NSA reports a 50x reduction in usable gadgets across a Linux distro; Arm reports >97% gadget reduction in glibc.
- **Not protected**: PAC has 64-VA-width effective bits; on a 48-bit VA it's ~15 bits of MAC — brute-forceable in ~32 K attempts if the process survives that many faults. Many designs add `SIGSEGV → kill` to make this impractical.
- **Side channels**: PAC verification has been the subject of timing-leak research; current consensus is the leakage rate is far too low to derandomise the MAC in a typical process lifetime.
- **JIT-specific**: a JIT must sign its newly-emitted code pointers (handing the freshly-generated function back to the interpreter as a signed callable). If the signing gadget is reachable to the attacker, PAC can be forged for *some* contexts; this is what JSC has been hardening against in 2018 → 2024 → 2025.

## §4 Production status (May 2026)

- **Apple Silicon**: A12 (Sept 2018) introduced ARM64e in production. Every iPhone, iPad and Mac since uses PAC for kernel return addresses, vtable pointers, Objective-C `isa` pointers, signed function pointers (`__ptrauth(...)` qualifier), JavaScriptCore JIT-emitted code pointers, and more. The kernel and Safari are compiled with `-arch arm64e` and explicit `__ptrauth` annotations. As of M4 (2024) and M5 (2025) Apple uses QARMA3 for performance.
- **Android**: AArch64 Linux kernel has had PAC for kernel since 5.7, BTI for kernel since 5.10, and userland enablement via `-mbranch-protection=standard` since Android 12. Pixel 8/9 with Tensor G3/G4 use PAC+BTI broadly.
- **Linux glibc**: PACBTI baseline support in glibc 2.36 (2022); fully enabled in default Ubuntu 24.04 and RHEL 10 (2025) builds for AArch64 packages.
- **Microsoft Windows-on-Arm**: ships PAC for return addresses by default since Win 11 23H2.
- **NSA / DoD attestation**: USAF and selected DoD systems require PAC+BTI on Arm builds as of 2024.
- **JavaScriptCore JIT signing**: deployed since 2018 on Apple Silicon. The actual JIT-side PAC code lives in Apple-internal `WebKitSupport`, not the open-source WebKit repo. May 2024 commit "Make it harder to get a PAC signing gadget in JIT code" reflects ongoing 2024-2025 hardening. CVE-2024-44308 (Nov 2024) showed a DFG-uninitialised-variable bug could still be chained with PAC+APRR bypass primitives to escape the renderer — Apple patched the underlying bug rather than the PAC bypass class.

## §5 Software emulation cost

PAC-equivalent software signing:

- **Software shadow stack** for return-address protection (no MAC): ~5-10% slowdown depending on call density; LLVM has `-fsanitize=safe-stack` and `-fsanitize=shadow-call-stack`.
- **Cryptographic-MAC pointer signing in software**: extremely expensive (~50% slowdown if HMAC; ~10-20% with truncated SipHash). Not deployed widely.
- **CFG (Microsoft Control Flow Guard)**: bitmap of valid indirect-call targets, ~1-2% overhead. Used in lieu of BTI on Windows x86 and ARM64 (Windows uses CFG even where BTI is available).

In aggregate: PAC+BTI **hardware** is approximately free (single-digit % overhead on most workloads). Software-only forward+backward CFI on the same workloads is 5-15% with shadow-stack + CFG, more if cryptographically signed.

## §6 Mochi adaptation note

vm3's bytecode interpreter does not have a forward-edge CFI problem: the dispatch is a table-indexed jump to interpreter handlers compiled into the Mochi runtime binary. These handler addresses are not user-controllable. **vm3-classic is essentially immune to ROP/JOP in the userland sense** because user bytecode cannot synthesise native code.

The story changes for **vm3jit** (the JIT'd execution path, MEP-39). Once Mochi code is lowered to native AArch64:

- Returns from JIT'd functions must be signable; otherwise, a memory-corruption bug in the Cell layer (already largely closed by MEP-40) that did escape would land on a corrupted return slot.
- JIT-emitted indirect calls (typeclass dispatch, closure calls) must target BTI landing pads if BTI is enforced.
- The JIT itself must hold the signing primitives behind an interface that does not become a universal forgery gadget — exactly JSC's lesson.

Where vm3 currently falls short: vm3jit (MEP-39) emits AArch64 code via Go's `asm` package without consistent `-mbranch-protection` enablement; on Apple Silicon Macs in particular, generated code does not sign returns. The **smallest addition** for MEP-41 is to:

1. Emit a `PACIASP`/`AUTIASP` pair on every JIT'd function with `_jit_call` ABI when the runtime detects PAC support.
2. Emit `BTI c` at every indirect-call landing in JIT code.
3. Plumb a hash of the Cell's generation into the PAC context, so a stale Cell cannot be reused to forge a signed return address.

Reference: MEP-40 (the Cell whose generation feeds the PAC context), MEP-39 (the JIT that needs the signing).

The combination "generation in Cell" + "PAC over (return, gen)" is a software-software-hardware composition: the software gen-check defeats the data-corruption path that a software shadow-stack would catch, and the hardware PAC defeats the residual return-address corruption.

## §7 Open questions for MEP-41 design

1. Should vm3jit *require* PAC at runtime on Apple Silicon / Tensor / Cortex, or stay best-effort?
2. What's the context we sign with — function frame, current effect domain, generation of the receiver? Each choice has different security and debuggability implications.
3. BTI is mandatory in Cortex-A715+; do we have a backup CFG-style table for AArch64 builds on older cores or for non-Arm targets?
4. JIT-signing keys: who owns them, and how are they rotated across vm3jit recompiles?
5. Is there a meaningful PAC-on-data-pointers story for vm3 — e.g., signing the *cell pointer to the slab* with `PACDA` to make memory disclosure not yield a forgeable handle?