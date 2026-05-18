---
title: "AArch64 AAPCS64"
description: "The base 64-bit Arm calling standard, with Apple and Microsoft deltas called out."
tags: ["native-codegen", "targets"]
weight: 30
date: 2026-05-18T18:03:33+07:00
---

## §1 Provenance

- AAPCS64 canonical text: https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst (and the published PDF at https://developer.arm.com/documentation/ihi0055/latest/).
- ARM Architecture Reference Manual for A-profile (Arm ARM): https://developer.arm.com/documentation/ddi0487/latest/.
- ELF for the Arm 64-bit architecture (AAELF64): https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst.
- Apple ARM64 documented deviations: https://developer.apple.com/documentation/xcode/writing-arm64-code-for-apple-platforms.
- Microsoft ARM64 calling convention: https://learn.microsoft.com/en-us/cpp/build/arm64-windows-abi-conventions.
- Apple ARM64e (PAC) overview: https://developer.apple.com/documentation/security/preparing-your-app-to-work-with-pointer-authentication.

## §2 Mechanism / specification

Integer/pointer arguments: X0 to X7. Floating-point/SIMD arguments: V0 to V7 (V is the 128-bit vector view; D is the 64-bit FP view of the same registers). Eight slots in each class. Arguments beyond go on the stack.

Return values: X0 (and X1 for 128-bit integers), V0 to V3 for vector/FP, or via an indirect result location pointer in X8 for large returns.

Stack: 16-byte aligned at function entry (always). Frame pointer X29 should point at the previous frame's saved X29/X30 pair; the link register X30 holds the return address. The final frame in the chain has X29 = 0.

Callee-saved (nonvolatile): X19 to X28, plus the lower 64 bits of V8 to V15 (D8-D15). Everything else, including X9 to X15 and V16 to V31, is caller-saved. X16 (IP0) and X17 (IP1) are intra-procedure-call scratch registers usable by linker stubs. X18 is platform-reserved (Apple uses it for thread state; Linux leaves it free for kernel modules).

Aggregates: a homogeneous floating-point or short-vector aggregate (HFA/HVA) of up to four members of the same type goes in V registers, otherwise INTEGER classification fills X registers, with anything larger than 16 bytes going indirect.

PSTATE: SP must be 16-byte aligned at all times after the prolog; certain syscalls fault otherwise.

### Variadic divergence

Standard AAPCS64 (Linux, *BSD): variadic args use the same X0-X7/V0-V7 sequence as named args, with overflow on stack.

Apple ARM64 (Darwin): all variadic args are passed on the stack, period. Fixed named args still use X0-X7/V0-V7, but the moment a function is declared variadic, everything past the named parameters spills to the stack. This is hardcoded in clang's Darwin AArch64 ABI lowering.

Microsoft ARM64 (Windows): variadic floats are passed in X registers (treated as 64-bit integers), not V registers. SIMD/FP regs are not used for variadics at all. Otherwise close to AAPCS64.

### PAC and BTI

Apple Silicon (M1 onward, ARMv8.3+ with Apple extensions) ships with userspace PAC armed. Function returns use PACIASP at prolog and AUTIASP at epilog. Indirect calls go through authenticated variants (BLRAA/BLRAB). Apple's variant is called ARM64e and is required for system libraries; third-party apps can opt in.

Linux on AArch64: PAC and BTI are opt-in (compile with `-mbranch-protection=pac-ret+bti`). When enabled, the linker emits the GNU_PROPERTY_AARCH64_FEATURE_1_BTI/PAC bits in `.note.gnu.property`; the dynamic loader uses these to decide whether to map pages as guarded.

BTI inserts a landing-pad instruction at every valid indirect branch target. Hardware (ARMv8.5+) traps any indirect branch into a non-BTI instruction. The Apple Silicon variant is mandatory for system frameworks since macOS 14.

## §3 Platform coverage (May 2026)

- macOS on Apple Silicon (M1 to M5 generation as of 2026): Apple ABI with ARM64e.
- iOS, iPadOS, tvOS, watchOS, visionOS: same Apple ABI with mandatory ARM64e for system frameworks.
- Linux on AArch64: AAPCS64 base ABI. Every major distro (Debian arm64, Fedora aarch64, Ubuntu arm64, RHEL, openSUSE).
- Android on ARMv8: AAPCS64 with NDK-specific extensions; tagged pointers (MTE-aware) since Android 14.
- FreeBSD/aarch64: AAPCS64.
- OpenBSD/arm64: AAPCS64 with mandatory BTI on bti-capable cores.
- Windows on ARM64: see `04_aarch64_windows.md`.

## §4 Current status (May 2026)

- AAPCS64 has been stable in shape since 2014. Amendments in 2024-2026 added: SME (Scalable Matrix Extension) ABI rules for ZA storage and streaming-mode transitions; SVE2.1 vector register handling; clarified rules for `_Float16` arguments.
- ARMv9.4 and ARMv9.5 add new prediction control features; the ABI gained MOPS (memcpy/memset acceleration) intrinsics.
- SME on Apple M4/M5 is exposed but Apple has not standardized a system-wide ABI yet; libraries that use SME bracket their use with SMSTART/SMSTOP.
- Apple deprecated 32-bit ARM (armv7) years ago; only AArch64 matters on Apple platforms.
- MTE (Memory Tagging Extension) is shipping in Android 15+ on Pixel hardware and in some Linux distros as a hardening option.

## §5 Engineering cost for Mochi

Lower complexity than x86_64 because the calling convention is more uniform (no SysV/MS split for the base ABI; the splits are localized to variadic and pointer-auth). Key work:

1. Lower Mochi values into X0-X7 / V0-V7 (the 8-byte Cell handle fits in a single X register).
2. Emit ELF (Linux/BSD) or Mach-O (Apple) objects. AAELF64 is well documented; Go's `debug/elf` writer side, combined with `cmd/link/internal/loadelf`, is workable.
3. Emit unwind information: AArch64 uses DWARF CFI on Linux and a compact-unwind variant on Apple (`__unwind_info` section in the `__TEXT` segment).
4. Handle Apple's variadic-on-stack divergence.
5. For Apple targets, opt into PAC if Phase 2 wants Apple Silicon: emit PACIASP/AUTIASP, add the appropriate `__LINKEDIT` notes, sign with at minimum an ad-hoc signature (`codesign -s -`).
6. For Linux, opt into BTI by setting the GNU property note and emitting BTI landing pads (`bti c` at function entry, `bti j` at indirect branch targets).

Go's own AArch64 backend (`cmd/internal/obj/arm64`) is a reference implementation Mochi can crib from; it speaks both Linux and Darwin conventions.

## §6 Mochi adaptation note

compiler3's planned `backend/native/aarch64` would be the second backend after x86_64. The MEP-40 Cell handle (8 bytes) maps cleanly to X registers. The arena allocator needs no ABI awareness. For Apple targets, the runtime/vm3 should be built with `-mbranch-protection=pac-ret+bti` if Mochi distributes prebuilt binaries; ad-hoc signing of the final executable is mandatory on Apple Silicon.

For Linux, AAPCS64 plus DWARF unwind is enough. For Apple, the compact-unwind format plus Mach-O LC_BUILD_VERSION plus ad-hoc signing is the minimum to launch a binary on macOS 14+.

## §7 Open questions for MEP-42

1. Apple Silicon vs Linux/aarch64 priority: which ships first? Recommend Linux/aarch64 first (simpler tooling), Apple second.
2. ARM64e (PAC) in Phase 1 for Apple: required for system frameworks but third-party can ship plain ARM64. Recommend plain ARM64 in Phase 1, ARM64e in Phase 2.
3. BTI default-on for Linux? Recommend default-on; cost is one instruction per function entry.
4. Compact-unwind on Apple vs DWARF: must ship compact-unwind for Apple (DWARF is allowed but discouraged and triggers slow paths).
5. SVE/SME: defer entirely until Mochi has SIMD intrinsics in source.
