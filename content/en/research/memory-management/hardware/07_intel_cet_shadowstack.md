---
title: "Intel CET Shadow Stack + IBT"
description: "Intel CET Shadow Stack + IBT"
tags: ["memory-safety", "hardware"]
weight: 70
date: 2026-05-18T17:00:00+07:00
---

> A hardware second stack that records return addresses, plus indirect-branch landing pads. Shipping on every modern Intel/AMD CPU, default-on in Windows 11, opt-in on Linux.

## §1 Provenance

- Intel, "Control-flow Enforcement Technology Specification." Document 334525, Rev. 3. https://kib.kiev.ua/x86docs/Intel/CET/334525-003.pdf
- Linux kernel "Control-flow Enforcement Technology (CET) Shadow Stack" docs (v6.14+). https://docs.kernel.org/next/x86/shstk.html
- LWN, "Shadow stacks for userspace." Sept 2022. https://lwn.net/Articles/913934/
- Phoronix, "Glibc Updated For Recent Linux CET Shadow Stack Support." Jan 2024. https://www.phoronix.com/news/Glibc-Intel-CET-Shadow-Stack
- McGarr, "Exploit Development: Investigating Kernel Mode Shadow Stacks on Windows." https://connormcgarr.github.io/km-shadow-stacks/
- Synacktiv, "Analyzing the Windows kernel shadow stack mitigation." SSTIC 2025. https://www.synacktiv.com/sites/default/files/2025-06/sstic_windows_kernel_shadow_stack_mitigation.pdf
- h3xduck, "How to enable Intel CET." June 2025. https://h3xduck.github.io/cfi/2025/06/26/enabling-intel-cet.html
- x86.lol, "Hardening C Against ROP: Getting CET Shadow Stacks Working." Sept 2024. https://x86.lol/generic/2024/09/23/user-shadow-stacks.html

## §2 Mechanism

CET has two architectural components:

1. **Shadow Stack (SHSTK)**. The CPU maintains a second stack at a virtual address held in `SSP` (Shadow Stack Pointer), mapped with a special page-table attribute (`PTE.shadow=1`) such that only special instructions (`WRSS`, `RSTORSSP`, `INCSSP`) can write to it. On `CALL`, the CPU pushes the return address to both the regular stack and the shadow stack; on `RET`, it pops both and compares — mismatch raises `#CP` (Control Protection) exception.
2. **Indirect Branch Tracking (IBT)**. Every legal target of an indirect `JMP`/`CALL` must begin with `ENDBR64` (or `ENDBR32`). A `notrack` prefix can be used on jumps known to dispatch to non-instrumented code. Indirect branch into a non-`ENDBR` causes `#CP`.

Shadow stacks are per-thread; the OS lazily allocates one on the first `arch_prctl(ARCH_SHSTK_ENABLE)` call. The kernel can choose to enable shadow stack for itself separately (Windows does; Linux does as of 6.6).

Hardware: Intel **Tiger Lake** (11th gen, 2020) introduced SHSTK; **Sapphire Rapids** (4th gen Xeon, 2023) brought it to server. AMD **Zen 3** (2020) introduced shadow stack. IBT is supported on the same generations.

## §3 Threat model + guarantees

- **Backward-edge CFI**: SHSTK fully closes naive stack-buffer-overflow → ROP chains, *provided* the kernel has shadow stack on too. An attacker who corrupts the regular stack now has to corrupt the shadow stack as well, but the shadow stack is page-protected so this requires a privileged write primitive.
- **Forward-edge CFI**: IBT eliminates JOP gadgets that don't begin with `ENDBR`. Mostly equivalent to BTI on Arm.
- **Not protected by SHSTK**:
  - In-band control transfers (sigreturn-oriented programming, exception-handling chains) — recent CVEs in Windows kernel showed `KiSwapStack` and `_C_specific_handler` gadgets.
  - JIT-emitted code that doesn't emit `ENDBR` at each entry point.
  - Data-only attacks (write-what-where targeting application data not return addresses).
- **Not protected by IBT on Windows**: Windows specifically *did not* deploy IBT in production; it uses CFG (Control Flow Guard) bitmap instead. So Windows protection is SHSTK + CFG, not SHSTK + IBT.
- **Side channels**: no direct CET-specific leak as of May 2026, but standard Spectre v1/v2 still applies to indirect branches that pass IBT.

## §4 Production status (May 2026)

- **Windows 11**: SHSTK exposed via "Kernel-mode Hardware-enforced Stack Protection" toggle in Windows Security UI (since 22H2). Apps must opt-in via `/CETCOMPAT` link flag or via `SetProcessMitigationPolicy(ProcessUserShadowStackPolicy)` at runtime. Windows 11 23H2 and 24H2 enable kernel SHSTK by default on supported hardware. Win11 does **not** enforce IBT (uses CFG).
- **Linux**: SHSTK landed mainline in **6.6** (Oct 2023); fully usable interface stabilised by 6.8. **Glibc 2.39** (Feb 2024) added userspace SHSTK enablement; it's **opt-in** via `GLIBC_TUNABLES=glibc.cpu.hwcaps=SHSTK`. As of May 2026, no major distro enables it by default for all binaries; selected hardened distros (Gentoo hardened, Alpine) ship it on. Linux **does not** enforce userspace IBT either as of 6.x — too many older binaries fail without `ENDBR`.
- **GCC/Clang**: `-fcf-protection=full` emits both `ENDBR` and shadow-stack-compatible code (i.e., uses standard `CALL`/`RET`, since SHSTK is transparent).
- **Glibc 2.39** also added the dynamic loader's verification that all dependent shared libraries are CET-compatible before enabling for a process; this is the chief reason it's gated.
- **2025 status (SSTIC paper)**: Synacktiv showed real-world Windows kernel SHSTK bypasses via the exception-handling and stack-swap paths, motivating ongoing work to extend the protection to those code paths. The mitigation is real but the kernel TCB has plenty of gadgets that don't go through `RET`.

## §5 Software emulation cost

SHSTK in software (e.g., LLVM `-fsanitize=shadow-call-stack`):

- AArch64 shadow-call-stack reserves x18 and stores RA there; ~1-3% overhead, requires no hardware.
- x86-64 shadow-call-stack via `gs:`-offset shadow region: also ~1-3% overhead.
- LLVM SafeStack (split-stack model, sensitive locals on separate stack): ~0.1% overhead, very lightweight but only partial protection.
- Full software CFI (e.g., LLVM `-fsanitize=cfi`): ~1% overhead, works on x86/Arm without CET.

IBT in software: there is no fast software equivalent. CFG (Windows) costs ~1-2% on each indirect call due to bitmap lookup. Clang's `-fsanitize=cfi-icall` does class-hierarchy-aware CFI at ~1% but only for C++ virtual calls.

Net: hardware CET costs effectively zero on cycle-by-cycle benchmarks; the software equivalents cost 1-5%. The reason CET is exciting is that *that overhead is now negative* (it's actually free).

## §6 Mochi adaptation note

Like the PAC/BTI story, vm3-classic (the bytecode interpreter) doesn't need shadow stacks at user-program scope: the Mochi user cannot smash a return address into the Mochi runtime in any way. The interpreter dispatch loop is the only `RET` user bytecode interacts with, and Mochi return values do not touch the C-level stack.

vm3jit is different. Once Mochi functions are lowered to native x86-64 / AArch64:

- Each JIT'd function's prologue should be **CET-compatible**: `ENDBR64` as first instruction (for x86-64 builds), standard `CALL`/`RET` sequence (so SHSTK applies transparently), no manual stack-pointer tricks that confuse SHSTK.
- The vm3jit code-cache should be allocated via `mprotect` such that the shadow-stack does not consider it a non-CET-compatible region.
- The interpreter→JIT trampoline and JIT→interpreter return-slot must use the same calling convention so SHSTK's call/return bookkeeping doesn't desync.

Where vm3 currently falls short: as of May 2026, neither vm3 nor vm3jit emits `ENDBR64` at JIT-function entries on x86-64, and the runtime is not built with `-fcf-protection=full` by default (Go toolchain has partial support since 1.22). The smallest gap-closer for MEP-41:

1. Build the Go-side mochi binary with `-buildvcs=true -ldflags=-w -gcflags=-N -gcflags="-fcf-protection=full"` (or wait for Go to enable by default).
2. JIT-emit `ENDBR64` (x86-64) / `BTI c` (AArch64) as the first instruction of every JIT entry point.
3. Use standard `CALL`/`RET` in JIT (no manual `JMP`-based tail calls into the interpreter; those defeat SHSTK).

This doesn't touch the Cell layout (MEP-40) at all; it's purely a JIT code-generation discipline. Reference: MEP-39 (the JIT).

## §7 Open questions for MEP-41 design

1. Does Go's runtime cooperate well with userspace SHSTK as of 1.23+? Goroutine stack switches must update SSP; if Go's `runtime.cgocallback` path mis-handles SSP, we'll have spurious `#CP` faults.
2. Should vm3jit ever emit non-standard returns (tail-call-as-jump for inlined fast paths)? These break SHSTK; we may need a `notrack`-equivalent or to abandon them.
3. On x86-64 platforms without CET (older AMD, pre-Tiger-Lake Intel), should vm3jit fall back to a software shadow-call-stack, or accept the gap?
4. Apple Silicon doesn't have CET (it has PAC instead — see file 06). Should the same JIT codepath use PAC where available and fall through to nothing where not, treating these as two non-overlapping platform features?
5. The Synacktiv 2025 results show kernel SHSTK is still bypassable. Does the threat model we accept for Mochi include "the host kernel may have an SHSTK bypass", and if so, what does the runtime do about it (nothing? alert? abort?)?