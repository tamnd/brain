---
title: "Static-PIE"
description: "Statically linked, position-independent, ASLR-friendly, and no dynamic loader required."
tags: ["native-codegen", "runtime"]
weight: 70
date: 2026-05-18T18:14:16+07:00
---

## §1 Provenance

- glibc design discussion (initial GCC patch by H.J. Lu): https://patchwork.ozlabs.org/project/gcc/patch/20170824200227.GA14790@gmail.com/
- musl rcrt1 patch (Szabolcs Nagy, 2020): https://www.openwall.com/lists/musl/2020/04/27/2
- Eklitzke, "The Curious Case of Position Independent Executables": https://eklitzke.org/position-independent-executables
- Gaultier, "Build PIE executables in Go: I got nerd-sniped": https://gaultier.github.io/blog/build-pie-executables-with-pie.html
- ASLR for statically linked binaries (Leviathan Security): https://www.leviathansecurity.com/blog/aslr-protection-for-statically-linked-executables

## §2 Mechanism / function

A traditional static executable has ELF type `ET_EXEC` and is hard-loaded at a fixed virtual address (historically `0x400000` on Linux x86_64). It does not depend on the dynamic loader (`/lib/ld-linux.so.2`).

A shared library or PIE executable has ELF type `ET_DYN` and contains only position-independent code. The dynamic loader picks a base address at runtime (randomized via ASLR), applies the relative relocations, and jumps to the entry point.

Static-PIE combines the two: ELF type `ET_DYN`, no dynamic loader dependency, but contains its own startup glue that:

1. Discovers its own load address by reading the `_DYNAMIC` symbol.
2. Walks the relative relocations (no symbol lookups, only `R_*_RELATIVE`).
3. Patches itself.
4. Jumps to `main`.

This startup glue is provided by `rcrt1.o` (in musl) or by `Scrt1.o` for the static-PIE case (in glibc). The compiler driver injects it when you pass `-static-pie`.

The build is:

```
cc -fPIE -c foo.c -o foo.o
cc -static-pie foo.o -o foo
```

The resulting binary is loadable at any address (ASLR works), has no dynamic loader dependency, and runs without any `.so` files on the target system.

## §3 Platform coverage (May 2026)

Static-PIE works on Linux with most libc choices:

- musl: full support across all architectures. The musl rcrt1 implementation has been stable since 2020.
- glibc: supported on x86_64, i386, x32 (binutils 2.29+), AArch64 (binutils 2.30+), and most other 64-bit Linux architectures. ARMv7l historically not.
- diet libc: partial.
- klibc: no.

OpenBSD has shipped all base binaries as static-PIE since 2015 (per `clang -static -pie` default).

FreeBSD supports static-PIE.

macOS: Mach-O does not have an exact equivalent. Mach-O binaries are always position-independent on modern hardware (PIE is the default since macOS 10.7), but the static-vs-dynamic libc question is moot since macOS forbids static linking against libSystem (see `runtime/05_no_libc_freestanding.md`).

Windows: PE has its own "DLL characteristics" `DYNAMIC_BASE` flag for ASLR. Static linking against the CRT is supported but does not have a directly analogous concept.

## §4 Current status (May 2026)

Static-PIE is the default for Rust's `*-linux-musl` targets (`rustc` generates static-PIE on musl since around Rust 1.45 in 2020). Go can emit static-PIE through `-buildmode=pie` plus `CGO_ENABLED=0` and an external linker hint. OpenBSD makes static-PIE the default for everything.

Adoption is growing because static-PIE gives both:

- The deployment simplicity of a static binary (one file, no runtime dependency).
- The security of ASLR (each run loads at a randomized address, making ROP / return-to-libc attacks harder).

glibc static-PIE has historically been more brittle than musl static-PIE (more edge cases, more architecture limitations). musl is the recommended path.

The 2024-2025 NixOS thread (https://github.com/NixOS/nixpkgs/pull/123989) shows ongoing work to make `--enable-static-pie` the default for the Nixpkgs glibc, indicating active community interest.

## §5 Engineering cost for Mochi

For Mochi-emitted Linux native binaries:

- If we use musl: pass `-static-pie` to the compiler driver. The resulting binary is portable and ASLR-protected.
- If we use glibc: pass `-static-pie` on supported architectures. Be prepared for it to fail on some.
- The compile-time cost is essentially zero (the rcrt1 startup glue is tiny).
- The runtime cost is one extra page of code for the self-relocation step, run once at startup. Microseconds at most.
- Size: a static-PIE musl binary is roughly the same size as a non-PIE static musl binary, perhaps 1 to 2 KB larger.
- Tooling: gdb, perf, strace all handle static-PIE correctly.

The complication: static-PIE requires that ALL input objects be compiled with `-fPIE`. If Mochi statically links third-party `.a` files that were built without PIE, the link fails with a "relocation R_X86_64_32 against .text" error. We must either rebuild dependencies with PIE or refuse to link them.

For Mochi's own code (which we always compile ourselves), this is no problem.

## §6 Mochi adaptation note

Mochi's `mochi build --portable` should default to static-PIE on Linux:

1. The Mochi compiler emits `-fPIE` object files (no absolute address relocations in `.text`).
2. The linker step (mold, lld, or system ld) passes `-static-pie`.
3. The libc is musl (per `runtime/01_musl_static.md`).
4. The result is a 200 KB to 2 MB binary that runs on any Linux of the right arch with ASLR.

For the default Linux build (host-libc, dynamic), PIE is still on but not static. This matches Ubuntu / Fedora defaults for system binaries.

Relevant Mochi files: `compiler3/emit/obj` emits PIC code (the `regalloc` package needs to know we are PIC and avoid absolute-address optimizations). The link driver in `tools/linkers` adds the `-static-pie` flag when in portable mode.

## §7 Open questions for MEP-42

- Do we make static-PIE the default for all Linux builds, or only the portable mode? Recommendation: portable mode only, since static-PIE precludes dynamic libraries.
- Do we attempt static-PIE on glibc, or insist on musl for static? Recommendation: insist on musl for the static path.
- For non-Linux targets, do we need a static-PIE equivalent? macOS PIE is default; Windows ASLR is a separate switch (`/DYNAMICBASE`). Document both.
- ARMv7l: do we support static-PIE there? Probably skip; ARMv7l Linux is shrinking anyway.

Sources:
- [GCC patch: Add --enable-static-pie to build static PIE](https://patchwork.ozlabs.org/project/gcc/patch/20170824200227.GA14790@gmail.com/)
- [musl rcrt1 patch (Szabolcs Nagy)](https://www.openwall.com/lists/musl/2020/04/27/2)
- [Eklitzke: The Curious Case of Position Independent Executables](https://eklitzke.org/position-independent-executables)
- [Gaultier: Build PIE executables in Go](https://gaultier.github.io/blog/build-pie-executables-with-pie.html)
- [Leviathan Security: ASLR for statically linked binaries](https://www.leviathansecurity.com/blog/aslr-protection-for-statically-linked-executables)
- [NixOS PR: glibc static-PIE default](https://github.com/NixOS/nixpkgs/pull/123989)