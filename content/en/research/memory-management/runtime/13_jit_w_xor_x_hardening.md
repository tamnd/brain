---
title: "W^X Enforcement in Modern JITs"
description: "What every shipping JIT must do on day 1 to be production-grade: never have a code page that is both writable and executable to the same thread at the same time. MAP_JIT + pthread_jit_write_protect_np on Apple Silicon, mprotect dance elsewhere, hardware shadow stacks (Intel CET, ARM BTI) increasingly mandatory."
tags: ["memory-safety", "runtime"]
weight: 130
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Apple Silicon model.** Apple Platform Security guide and: https://developer.apple.com/documentation/apple-silicon/porting-just-in-time-compilers-to-apple-silicon. Apple Silicon enforces per-thread W^X via the M-series memory permissions extension.
- **Hardened Runtime entitlements.** `com.apple.security.cs.allow-jit`, `com.apple.security.cs.allow-unsigned-executable-memory`, the newer `jit-write-allowlist`. https://developer.apple.com/documentation/BundleResources/Entitlements/com.apple.security.cs.allow-jit.
- **JSC pioneered** the MAP_JIT + pthread_jit_write_protect_np pattern in 2015; Firefox, V8, .NET, asmjit followed.
- **Intel CET.** https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/speculative-execution-side-channel-mitigations.html, kernel docs https://www.kernel.org/doc/html/next/x86/shstk.html. Default-enabled on Windows since W10 19H1 and Linux since 6.4 (2023).
- **ARM BTI** (Branch Target Identification): part of Armv8.5-A. Used by JSC on Apple Silicon for IBT-equivalent guards.

## §2 Mechanism

The threat: JIT'd code pages are uniquely dangerous. If an attacker can write to a page and then execute it, they can inject shellcode trivially. **W^X (Write-XOR-Execute)** says: any given page is *either* writable *or* executable, never both. JITs need both — to emit code, then to run it.

### Per-thread permission (Apple Silicon)

Apple Silicon's CPU implements per-thread permission flips:

1. `mmap(..., MAP_JIT, ...)` allocates a page that starts R-X. All threads see R-X.
2. `pthread_jit_write_protect_np(false)` flips the calling thread's view to RW- (other threads still see R-X).
3. JIT writes/patches code.
4. `pthread_jit_write_protect_np(true)` flips back to R-X.
5. `sys_icache_invalidate()` over the patched range.
6. Execute.

Critical rule: **never share a MAP_JIT region across threads where one thread has write permission**. The privilege escalation primitive is "thread A writes, thread B executes" — exactly what this design prevents per-thread.

### Page-permission dance (Intel, ARM Linux, Windows)

No per-thread permission flip; use `mprotect`:

1. `mmap(..., PROT_READ | PROT_EXEC, ...)`.
2. To patch: `mprotect(page, len, PROT_READ | PROT_WRITE)` → write → `mprotect(page, len, PROT_READ | PROT_EXEC)` → flush icache.

More expensive than the per-thread flip but universally portable.

### Hardware shadow stack & IBT (Intel CET, ARM BTI)

Once W^X is in place, the next attack surface is ROP/JOP: chain together legitimate code gadgets to do attacker-chosen things. Defences:

- **Shadow Stack (CET).** Hardware-managed second stack records return addresses. Mismatch on `ret` → control-protection fault. Enabled by default on Windows since 19H1, Linux 6.4+.
- **Indirect Branch Tracking (CET-IBT).** Indirect call/jump must land on an `ENDBRANCH` instruction; otherwise fault. JIT'd code must emit `ENDBR64` at every indirect-call landing pad. .NET runtime issue #47309 tracks the .NET work.
- **ARM BTI.** Similar to CET-IBT but ARM-flavoured: `BTI c`/`BTI j` instructions, enforced by hardware.

### New macOS hardening: `jit-write-allowlist`

A 2024-2026 Apple entitlement that *removes* `pthread_jit_write_protect_np` as a permission-flip path. Apps with this entitlement can no longer toggle thread JIT permission at will; they must use the `MAP_JIT + mprotect` flow. Designed to harden against attacker-controlled flips.

## §3 Memory-safety property

W^X alone is not memory safety — the JIT can still emit wrong code. But W^X **prevents code injection** as an exploitation primitive. Combined with shadow stacks and IBT, the class of "use a memory-corruption bug to redirect control flow to attacker-chosen code" becomes substantially harder.

It is a **mitigation** in the V8-Sandbox sense (file 08): assume corruption, contain blast radius.

## §4 Production status (May 2026)

- Every shipping JS engine (V8, JSC, SpiderMonkey, Hermes) implements W^X correctly. Failure to do so would be a major-CVE finding.
- Apple Silicon's `pthread_jit_write_protect_np` is universal across macOS/iOS JITs as of 2020+.
- Intel CET default-on for compatible binaries (`/CETCOMPAT` on Windows, `-fcf-protection=full` on Linux glibc with userspace tunable).
- ARM BTI shipped on Apple M-series and post-2020 ARM server cores; Linux kernel supports BTI for both userspace and kernel.
- `jit-write-allowlist`: opt-in but increasingly recommended on iOS.
- .NET runtime ships JIT'd code with CET shadow-stack and IBT support since .NET 9 (2024).

## §5 Cost

- **`pthread_jit_write_protect_np` toggle:** sub-microsecond per JIT patch. Cheaper than `mprotect`.
- **`mprotect` dance:** ~1-10 μs each call; dominates micro-benchmark JIT compile-time.
- **CET shadow-stack:** ~1-3% throughput cost reported in JIT benchmarks. Significant only at very high call rates.
- **CET-IBT / ARM BTI:** ~0.5% code-size growth (ENDBR/BTI instructions); near-zero perf cost.

## §6 Mochi adaptation note

vm3jit (MEP-40 §6.5, Phase 5) targets AArch64 and AMD64. For the JIT to ship at all on macOS, iOS, or recent Linux/Windows, it **must** implement W^X correctly from day one. Concrete minimum-bar checklist:

1. **Code cache allocation in `vm3jit/codecache.go`.**
   - macOS/iOS (AArch64): `mmap(MAP_JIT)` via syscall package; require `com.apple.security.cs.allow-jit` entitlement in the Mochi binary's plist.
   - Linux/Windows (AMD64 and AArch64): `mmap(PROT_READ|PROT_EXEC)` + `mprotect` flip on patch.
2. **Per-patch flip on Apple Silicon.** Use `pthread_jit_write_protect_np` via cgo *or* via direct syscall (`SYS_PTHREAD_JIT_WRITE_PROTECT_NP` isn't quite a syscall — needs Darwin libsystem). This is the *one* place vm3jit will need cgo on Darwin, and the cost is unavoidable. MEP-41 should accept this scoped cgo exception explicitly.
3. **icache invalidation.** After every patch: `sys_icache_invalidate` on Darwin, `__builtin___clear_cache` (gcc/clang intrinsic) elsewhere. On AArch64 this is a `dc cvau` + `dsb ish` + `ic ivau` + `isb` sequence; Go runtime has a helper.
4. **ENDBR/BTI emission.** Every indirect-jump target the JIT emits (vtable entry, deopt resume, super-op tail) needs `ENDBR64` (x86) or `BTI c`/`BTI j` (AArch64). Tiny, mandatory. Linker option `-z noexecstack -z relro -z now` on the host Go binary, plus `/CETCOMPAT` on Windows builds.
5. **Shadow-stack compatibility.** On CET-enabled Windows/Linux, JIT'd calls must push to both stacks. Go's runtime already handles this for Go calls; vm3jit's emitted call sequences must use the standard ABI (`call`/`bl` with normal `ret`/`braa`) so the hardware tracks them.
6. **Audit boundary.** A "vm3jit security checklist" doc, like JSC's, that lists every code-emission site and the W^X / IBT obligation. Maintainable.

This *does* introduce scoped cgo (for Darwin's pthread_jit_write_protect_np). The alternative is "Mochi doesn't ship a JIT on macOS," which is unacceptable for Phase 7's production migration. MEP-41 should call this out as the one accepted cgo exception in an otherwise pure-Go runtime.

## §7 Open questions for MEP-41

- Does vm3jit need to support iOS at all in v1? If yes, `jit-write-allowlist` posture (toggle vs full MAP_JIT+mprotect) matters. If no, scope it explicitly.
- How do we test W^X correctness in CI? Hard to test "kernel kills us on bad permission" outside of macOS hardware. Suggestion: dedicated nightly job on an Apple Silicon GitHub runner.
- Does the per-thread-permission model interact badly with Go's preemptive scheduler? Specifically: if a Goroutine yields mid-patch, can another Goroutine on the same OS thread land in the wrong permission view? Investigate.
- CET shadow-stack assumes a single linear call stack. vm3 has a typed register-bank frame model (MEP-40 §6.4). The JIT's emitted *machine-level* call/ret must still use the standard x86/ARM stack, and the interpreter's frame must round-trip through it cleanly.
- Should we support `--no-jit` builds for hardened deployments where any JIT is disallowed?

## Sources

- [Porting JIT compilers to Apple silicon (Apple Developer)](https://developer.apple.com/documentation/apple-silicon/porting-just-in-time-compilers-to-apple-silicon)
- [Allow execution of JIT-compiled code entitlement](https://developer.apple.com/documentation/BundleResources/Entitlements/com.apple.security.cs.allow-jit)
- [Saagar Jha — Apple silicon JIT fix gist](https://gist.github.com/saagarjha/d1ddd98537150e4a09520ed3ede54f5e)
- [Outflank — macOS JIT memory (Feb 2026)](https://www.outflank.nl/blog/2026/02/19/macos-jit-memory/)
- [Linux Kernel — CET Shadow Stack documentation](https://www.kernel.org/doc/html/next/x86/shstk.html)
- [Synacktiv SSTIC 2025 — Windows kernel shadow stack mitigation](https://www.synacktiv.com/sites/default/files/2025-06/sstic_windows_kernel_shadow_stack_mitigation.pdf)
- [Intel CET in Action (Offensive Security)](https://www.offsec.com/blog/intel-cet-in-action/)
- [.NET runtime — Epic: Support Intel CET (#47309)](https://github.com/dotnet/runtime/issues/47309)