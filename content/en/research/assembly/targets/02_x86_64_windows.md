---
title: "x86_64 Windows (Microsoft x64) ABI"
description: "The 4-register fast-call convention used by every Windows-on-AMD64 binary."
tags: ["native-codegen", "targets"]
weight: 20
date: 2026-05-18T18:03:33+07:00
---

## §1 Provenance

- Microsoft x64 calling convention reference: https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention.
- x64 stack usage and prolog/epilog: https://learn.microsoft.com/en-us/cpp/build/stack-usage and https://learn.microsoft.com/en-us/cpp/build/prolog-and-epilog.
- x64 exception handling: https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64.
- PE/COFF spec (the file-format counterpart): https://learn.microsoft.com/en-us/windows/win32/debug/pe-format.
- Intel SDM and AMD64 Programmer's Manual (same as SysV).
- PDB / CodeView reference: Microsoft's docs are partial; the de-facto reference is the LLVM `llvm-pdbutil` and `microsoft-pdb` GitHub repo at https://github.com/microsoft/microsoft-pdb.

## §2 Mechanism / specification

Integer/pointer arguments: RCX, RDX, R8, R9 (in order). Floating-point: XMM0 through XMM3. The slots are positional, not by class; floats in slot 0 use XMM0 and RCX is skipped, ints in slot 1 use RDX even if slot 0 was a float. There are exactly four register slots; everything beyond goes on the stack.

Shadow space: the caller allocates 32 bytes (4 * 8) below the return address before invoking the callee. The callee owns this space and may spill RCX, RDX, R8, R9 there or use it as scratch. Even leaf functions taking zero arguments get the 32 bytes if they call other functions.

Stack alignment: 16-byte aligned just before CALL; RSP is therefore 8 modulo 16 at function entry, identical to SysV.

Return values: RAX (integer up to 64 bits), XMM0 (floating point), or hidden pointer in RCX (for large or non-trivially-copyable aggregates), in which case the user-visible RCX shifts to RDX and so on.

Callee-saved (nonvolatile): RBX, RBP, RDI, RSI, RSP, R12, R13, R14, R15, XMM6 to XMM15. Caller-saved (volatile): RAX, RCX, RDX, R8, R9, R10, R11, XMM0 to XMM5. Notice that XMM6 to XMM15 are nonvolatile, which differs from SysV where every XMM is volatile.

There is no red zone on Windows x64. Signal-equivalent handling is structured exception handling (SEH), which lives entirely outside the stack proper.

SEH on x64 is table-driven via the PE `.pdata` section. Every nonleaf function must have a `RUNTIME_FUNCTION` entry pointing at an `UNWIND_INFO` block. The unwind codes describe the prolog's register saves and stack allocations in reverse order, sized so the OS unwinder can virtually undo any prolog instruction at any prolog offset. Leaf functions skip pdata/xdata entirely.

For JIT-emitted code, `RtlAddFunctionTable` (eager) or `RtlInstallFunctionTableCallback` (lazy) register unwind tables with the OS.

## §3 Platform coverage (May 2026)

Windows on x64: every edition of Windows 7 through Windows 11 24H2/25H1 client and Windows Server 2008 R2 through Server 2025. Same ABI for kernel-mode drivers (with extra restrictions). Wine on Linux/macOS also implements this ABI for hosting Windows binaries.

ReactOS implements a Windows-compatible x64 ABI, though most desktop work is still 32-bit. Cygwin and MSYS2 use Microsoft x64 calling convention for native binaries but layer POSIX semantics on top.

## §4 Current status (May 2026)

The Microsoft x64 ABI itself has been stable since Windows Server 2003. Recent additions are around hardening:

- CET shadow stack: marked by a bit in the PE optional header (`/CETCOMPAT` from MSVC link.exe). Hardware-enforced via Intel CET or AMD shadow stacks. Windows 11 24H2 enables kernel-mode CET by default on supported CPUs. Strict mode is opt-in per process.
- Control Flow Guard: indirect branch protection (CFG) since Windows 10. The image has a guard-CF function table; the loader checks every indirect call against it.
- Authenticode signing requirements: more strict for kernel drivers (cross-signing was retired), still optional for user binaries but increasingly required for SmartScreen reputation.
- ARM64EC: a flavor that lets x64 modules call into ARM64 code in the same process (relevant to Windows-on-ARM, not Windows-on-x64 backends).

APX support on Windows is in progress; no client OS ships APX-aware unwind data yet as of May 2026.

## §5 Engineering cost for Mochi

Higher than SysV. Key new work items:

1. Emit PE/COFF objects (Go's `debug/pe` reads but does not write; `cmd/link/internal/loadpe` writes minimally; `golang.org/x/exp/cmd/...` has some tooling).
2. Generate `.pdata` and `.xdata` for every nonleaf function. This is mandatory; without it, any exception or thread suspension that walks the stack crashes.
3. Honor 32-byte shadow space at every call site.
4. Track XMM6 to XMM15 as callee-saved.
5. Emit `_DllMainCRTStartup` and a startup stub that calls into the Mochi runtime.
6. Handle TLS via the `_tls_used` IMAGE_TLS_DIRECTORY structure (different from POSIX `__thread`).

Cross-compiling from Linux/macOS to x86_64-pc-windows-msvc is supported by clang-cl + lld-link, by Zig CC, or by mingw-w64. Mochi can use lld-link without needing an MSVC license. There is no need to ship a PDB in Phase 1; CodeView in the COFF object is enough for basic debugging via WinDbg.

CET and CFG are nice-to-have. CFG without writing the guard-CF table is a no-op (the linker just does not set the IMAGE_DLLCHARACTERISTICS_GUARD_CF bit).

## §6 Mochi adaptation note

In compiler3, a `backend/native/x86_64_windows` package would share the instruction selector with the SysV backend but ship a different ABI-lowering pass and a different object writer. The Mochi runtime/vm3 needs no changes; the arena allocator just calls VirtualAlloc instead of mmap.

The 8-byte Cell handle still fits in a single GPR, so most calls use RCX/RDX/R8/R9 and ignore shadow space. The pdata/xdata generator is a new code generator pass that walks every function's prolog and emits the matching unwind codes.

## §7 Open questions for MEP-42

1. Is Windows in Phase 1? Recommend yes if Mochi wants any enterprise/desktop traction; recommend deferring to Phase 2 if Phase 1 focuses on backend/CLI use cases (where Linux+macOS suffice).
2. Linker: bundle lld-link, depend on the user installing the Windows SDK, or use mingw-w64 ld? Recommend lld-link bundled.
3. Calling Windows APIs: through stub import-libraries (the MSVC way) or through GetProcAddress at runtime (the GNU way)? Recommend stub imports for performance.
4. CET/CFG: ship a minimal-compliance PE flag in Phase 1, or skip until Mochi has thread-safety stories? Recommend skip with the option to enable per-binary later.
5. ARM64EC on Windows: out of scope for an x64 backend; tracked separately under `04_aarch64_windows.md`.
