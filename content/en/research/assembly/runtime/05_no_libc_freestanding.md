---
title: "Freestanding / no-libc"
description: "Direct syscalls on Linux, why this is impossible on macOS, and the APE alternative."
tags: ["native-codegen", "runtime"]
weight: 50
date: 2026-05-18T18:09:59+07:00
---

## §1 Provenance

- Linux syscall ABI man page: https://man7.org/linux/man-pages/man2/syscall.2.html
- Linux vDSO man page: https://man7.org/linux/man-pages/man7/vdso.7.html
- Darling docs on macOS syscalls: https://docs.darlinghq.org/internals/basics/system-call-emulation.html
- Cosmopolitan source (a real freestanding-style implementation): https://github.com/jart/cosmopolitan
- Zig freestanding target docs: https://ziglang.org/learn/overview/#small-self-contained-builds
- "UNIX Syscalls" (John Millikin): https://john-millikin.com/unix-syscalls

## §2 Mechanism / function

A "freestanding" or "no-libc" binary makes its own system calls directly to the kernel without going through any C library. The mechanism varies sharply per OS:

Linux: stable syscall ABI. You put a syscall number in `rax`, arguments in `rdi`, `rsi`, `rdx`, `r10`, `r8`, `r9`, and execute `syscall`. The kernel returns in `rax`. This has been stable since the dawn of x86-64 Linux. AArch64 uses `x8` for the number and `svc #0` to invoke. Linux also exposes a vDSO (https://man7.org/linux/man-pages/man7/vdso.7.html), a kernel-mapped ELF shared library that provides fast-path implementations of `clock_gettime`, `gettimeofday`, `getcpu`, etc. without the privilege-transition cost (typically 100 to 200 ns per `syscall`).

macOS: NOT a stable syscall ABI. Apple explicitly documents that you must go through `libsystem_kernel.dylib` (which is loaded as part of `libSystem.B.dylib`). The wrappers in libsystem_kernel may do bookkeeping (TLS updates, signal-mask state, errno propagation) that the kernel assumes is in place. Calling raw syscalls can corrupt userspace state and break unrelated library code. This is why Go switched away from direct syscalls on macOS and BSD (see https://news.ycombinator.com/item?id=32921086).

Windows: NOT a stable syscall ABI either, by Microsoft's design. The supported boundary is the Win32 API in `kernel32.dll`, `user32.dll`, etc., which call into NTAPI (`ntdll.dll`), which calls the kernel. NTAPI itself is technically documented for some functions but officially not supported as an application boundary.

Freestanding therefore means different things per OS:

- On Linux, "freestanding" can mean "issue raw syscalls" and the result is robust and portable across kernel versions.
- On macOS, "freestanding" still requires linking against `libSystem.dylib` for the syscall wrappers. You can avoid `malloc`, `printf`, threading, etc., but you cannot avoid `libsystem_kernel`.
- On Windows, "freestanding" means "link against `ntdll.dll` minimally" but you still need a DLL.

## §3 Platform coverage (May 2026)

True direct-syscall freestanding works on:

- Linux: all architectures (x86_64, AArch64, ARM, RISC-V, etc.). The pattern is universal.
- The BSDs: each has its own syscall ABI; some treat it as more stable than others. FreeBSD has a stable enough ABI that Go used to issue direct syscalls there (though it migrated to libc for consistency).

Direct-syscall freestanding does NOT work on:

- macOS (per Apple's explicit policy).
- iOS, tvOS, watchOS, visionOS (closed platforms; only Apple's tools).
- Windows (Microsoft policy).
- Most other proprietary OSes.

The Zig freestanding target (`-target x86_64-freestanding` or `aarch64-freestanding`) builds with no OS abstraction at all. Useful for bare metal, kernel modules, UEFI. Not "no libc on Linux"; that is `-target x86_64-linux-none` or just static linking with `--no-stdlib`.

## §4 Current status (May 2026)

The Linux direct-syscall pattern has been the basis of Go's runtime for over a decade. Rust's `nix` and `libc` crates both expose `syscall(SYS_xxx, ...)` for callers who need it. Static-PIE Linux binaries that use raw syscalls and no libc are around 200 bytes to 4 KB for a "hello world" (compare 7 KB for musl, 800 KB for static glibc).

The macOS situation has tightened. Apple Silicon enforces W^X strictly, requires code-signed dyld closures, and treats `libSystem.dylib` as the only legitimate path into the kernel. Even Cosmopolitan, which on Linux uses direct syscalls, on macOS does its system calls indirectly through documented entry points in dyld.

The Windows situation is similar. NTAPI is technically reachable but officially unsupported; Win32 (or modern UWP / WinUI APIs) is the supported boundary.

Cosmopolitan's APE format (see `03_cosmopolitan_libc.md`) is the strongest no-libc-runtime story available today, but even it must bring its own implementations of the OS-specific entry conventions.

## §5 Engineering cost for Mochi

Going freestanding on Linux for Mochi-emitted native code:

- Pros: tiny binaries, no libc version compatibility issue, no NSS/dlopen surprises, full control over the program's startup and the heap.
- Cons: we must implement everything ourselves. `malloc` (use `mmap` directly), `printf` (write our own), threading (raw `clone` + `futex`), file I/O (`openat`/`read`/`write`).
- Static-PIE works with raw syscalls; we get ASLR for free.
- Cross-arch syscall tables: we maintain one per supported arch (x86_64, aarch64, riscv64). The numbers differ.

Going freestanding on macOS is essentially impossible. We MUST link `libSystem.dylib`. The smallest macOS binary is around 50 KB with libSystem.

Going freestanding on Windows is similar. We MUST link `ntdll.dll` (or kernel32/user32). The smallest Windows binary is around 5 KB if we minimize everything.

Hybrid pattern: Mochi can offer "freestanding mode" only on Linux, and link the platform libc on macOS and Windows. This is what Go effectively does today.

## §6 Mochi adaptation note

The relevant integration:

1. Mochi's `runtime/vm3/memory.go` (the typed arena allocator from MEP-40 Phase 1) does not depend on libc malloc on the Go side. The same idea translates to native code: arenas backed by `mmap` on Linux, `vm_allocate` (through libsystem) on macOS, `VirtualAlloc` on Windows.
2. For Linux, a `runtime/freestanding/linux` package emits the syscall stubs. Each arch (x86_64, aarch64) has its own assembly file.
3. For macOS and Windows, we always link the platform's minimum dynamic library set. Document this as the platform reality.
4. The `runtime/vm3/op.go` and `runtime/vm3/vm.go` semantics do not change. Only the lowest layer (allocator, syscall, signal handler) is per-OS.
5. We can reuse Cosmopolitan's research (which is BSD-style licensed) for the syscall stubs and detection code.

The implication for Mochi's distribution: a freestanding Linux Mochi binary is the smallest possible build, a few hundred KB for a meaningful program. A macOS or Windows Mochi binary is larger because of platform requirements.

## §7 Open questions for MEP-42

- Do we offer a `mochi build --freestanding` target that only works on Linux? Recommended: yes, opt-in.
- For macOS, what is our minimum `libSystem.dylib` symbol set? We should keep it as small as possible.
- Do we ever attempt direct syscalls on macOS for non-Apple-distributed binaries? No. It violates Apple's policy and breaks on every macOS update.
- Do we want to reuse Cosmopolitan's research as upstream code or just reference it as a design? Reference is safer; importing the code creates a dependency on cosmo's update cadence.

Sources:
- [Linux syscall(2) man page](https://man7.org/linux/man-pages/man2/syscall.2.html)
- [Linux vDSO(7) man page](https://man7.org/linux/man-pages/man7/vdso.7.html)
- [Darling: System call emulation](https://docs.darlinghq.org/internals/basics/system-call-emulation.html)
- [vsyscall and vDSO (linux-insides)](https://0xax.gitbook.io/linux-insides/summary/syscall/linux-syscall-3)
- [UNIX Syscalls (John Millikin)](https://john-millikin.com/unix-syscalls)
- [HN discussion: Go switched from direct syscalls to libc on BSD](https://news.ycombinator.com/item?id=32921086)