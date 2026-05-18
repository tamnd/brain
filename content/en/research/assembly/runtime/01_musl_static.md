---
title: "musl libc"
description: "The static-friendly C library that makes \"build once, ship anywhere\" actually work on Linux."
tags: ["native-codegen", "runtime"]
weight: 10
date: 2026-05-18T18:06:46+07:00
---

## §1 Provenance

- Project home: https://musl.libc.org/
- Git: https://git.musl-libc.org/cgit/musl/
- Wiki: https://wiki.musl-libc.org/
- Release history: https://musl.libc.org/releases.html
- Author: Rich Felker (single principal maintainer since 2011).
- License: MIT (with a handful of files under various BSD-style and public-domain licenses; see the COPYRIGHT file).

musl was started in 2011 with the explicit goal of providing a small, correct, MIT-licensed libc that is fully usable as a static library. It is the libc used by Alpine Linux (https://alpinelinux.org/), by Zig's cross-compilation toolchain (https://ziglang.org/learn/overview/#zig-ships-with-libcs), and by most embedded Linux distributions that care about size.

## §2 Mechanism / function

musl implements ISO C, POSIX (largely 2008), and a curated subset of Linux-specific and BSD extensions. It is one library; there is no NSS plug-in framework, no separate `libpthread.so`/`librt.so`/`libdl.so` (those are all the same library, plus matching empty stubs for ABI compatibility), no locale `.so` modules, no DNS resolver `.so` modules. Everything is statically linkable.

Key design choices:

- The dynamic linker is the same code as `libc.so` (the dynamic loader is just `libc.so` invoked with a different entry point).
- DNS resolution is compiled in, not loaded via NSS. There is no `nsswitch.conf` mechanism.
- Threading is a thin wrapper over Linux `clone(2)` and `futex(2)`. No userspace thread scheduler.
- Locale support is minimal (C and C.UTF-8 only by default; full UTF-8 throughput).
- Static-PIE is fully supported. The `rcrt1.o` startup file relocates the binary at runtime using only relative relocations (see https://www.openwall.com/lists/musl/2020/04/27/2).

## §3 Platform coverage (May 2026)

OS: Linux only (this is fundamental; musl is a Linux libc).

Architectures (musl 1.2.5 / 1.2.6):

- x86, x86-64, x32
- ARM (v4 through v8, hardfloat and soft variants)
- AArch64
- MIPS (32 / 64, big and little endian)
- PowerPC (32 / 64, big and little endian)
- RISC-V (32 and 64)
- LoongArch (64)
- s390x
- m68k
- microblaze
- OpenRISC (or1k)
- SuperH (sh)

The 1.2.5 release (February 2024) added the riscv32 and loongarch64 ports. 1.2.6 (mid 2024) added the POSIX-2024 `posix_getdents` interface and `renameat2`, and patched CVE-2025-26519 (iconv out-of-bounds write).

## §4 Current status (May 2026)

musl 1.2.5 was the headline 2024 release; 1.2.6 followed with bug fixes and a CVE patch. The pace is deliberately slow: roughly one feature release per year, frequent micro patches.

Rust's `*-linux-musl` targets ship musl 1.2.5 starting with Rust 1.93 (January 22, 2026; see https://blog.rust-lang.org/2025/12/05/Updating-musl-1.2.5/). Alpine Linux 3.21 (December 2024) and Alpine 3.22 (May 2025) both ship musl 1.2.5; Alpine 3.23 (late 2025) ships musl 1.2.6.

Production users:

- Alpine Linux (the default libc for the most-used "minimal Linux container" base image).
- Void Linux (musl variant).
- Postmarket OS.
- Most Docker base images for size-conscious projects.
- Rust's static `linux-musl` targets.
- Zig's cross-compiled Linux toolchain.

Maintainership remains Rich Felker plus a small community. The bus factor is one; this has been openly discussed and not resolved.

## §5 Engineering cost for Mochi

- License: MIT, trivial.
- Static linking: full support, no NSS or dlopen gotchas. A `cc -static` produces a binary you can `scp` to any Linux of the same arch.
- Static-PIE: `cc -static-pie` works. Gives ASLR plus no-dynamic-loader.
- Size: a "hello world" linked against musl is roughly 7 to 15 KB. The same against glibc is 800 KB+ even with -Os.
- DNS: works correctly (per the 1.2.4 resolver rewrite cited in https://blog.rust-lang.org/2025/12/05/Updating-musl-1.2.5/), unlike static glibc which can silently fail with large records.
- Threading: pthreads work; futexes are direct Linux syscalls. Performance is competitive with glibc on most workloads but can be worse on contended mutex-heavy paths because musl deliberately avoids glibc's adaptive spin code.
- Cross-compile: musl.cc (https://musl.cc/) provides ready-to-use cross toolchains; Zig embeds musl source and rebuilds per target.

The main downside: musl is strict. Code that "happens to work" against glibc due to glibc extensions (or due to glibc being more lenient about `getline` buffer reuse, `printf("%n")`, etc.) sometimes fails against musl. This is a portability win in the long run.

## §6 Mochi adaptation note

For Mochi's Linux native target, musl is the recommended libc when the user wants a portable binary:

- Mochi's `tools/linkers` selection can include a `--libc=musl` option. When set, we invoke `musl-gcc`, `musl-clang`, or `zig cc -target x86_64-linux-musl`.
- The default Linux build can still use glibc (matches the host) for compatibility with `dlopen`-loaded native plugins.
- Mochi's `runtime/cosmo/Makefile` already implies a "we know how to drive an alternative toolchain" pattern. A `runtime/musl/Makefile` would follow the same idea.
- For "make a portable Linux binary" mode, Mochi can ship a small embedded `zig cc` (or expect Zig to be installed) and use Zig's bundled musl. Zig is roughly 50 MB; smaller than shipping a full GCC toolchain.

We do not need cgo from Mochi-Go to use musl. We just produce relocatable objects and let the musl-aware driver link.

## §7 Open questions for MEP-42

- Do we default to musl or glibc on Linux? My recommendation: glibc by default (matches host), musl on `mochi build --portable`.
- Do we ship a musl toolchain in the Mochi tarball, or require the user to install one? Bundling Zig solves both this and the cross-compile story in one move.
- Do we expose static-PIE as a build mode? Yes; it is free upside.
- Do we depend on the 1.2.6 features (POSIX getdents, etc.)? Probably not for Phase 1.

Sources:
- [musl libc home](https://musl.libc.org/)
- [musl release history](https://musl.libc.org/releases.html)
- [musl libc 1.2.5 Released (Phoronix)](https://www.phoronix.com/news/musl-libc-1.2.5)
- [Rust 1.93 musl 1.2.5 update](https://blog.rust-lang.org/2025/12/05/Updating-musl-1.2.5/)
- [musl static-PIE rcrt1 patch (openwall)](https://www.openwall.com/lists/musl/2020/04/27/2)
- [musl.cc cross toolchains](https://musl.cc/)