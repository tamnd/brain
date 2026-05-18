---
title: "GNU ld (bfd) and gold"
description: "The historical Linux workhorse and its dying sibling."
tags: ["native-codegen", "linkers"]
weight: 40
date: 2026-05-18T18:04:37+07:00
---

## §1 Provenance

- GNU binutils home: https://www.gnu.org/software/binutils/
- Source and ChangeLog: https://sourceware.org/git/binutils-gdb.git
- Binutils 2.44 release announcement (February 2025): https://lists.gnu.org/archive/html/info-gnu/2025-02/msg00001.html
- gold Wikipedia entry: https://en.wikipedia.org/wiki/Gold_(linker)
- License: GPLv3 (with binary GPLv2-compatible link exemption for certain libraries).
- Maintainer: Nick Clifton (Red Hat) leads binutils. gold was originally Ian Lance Taylor's project at Google.

## §2 Mechanism / function

Two distinct linkers ship in the GNU binutils family:

`ld.bfd` is the classical GNU linker. It is built on libbfd, the GNU "binary file descriptor" library, which provides a unified abstraction over dozens of object formats (a.out, ECOFF, ELF flavors, PE/COFF, Mach-O reader, XCOFF, even some niche embedded formats). bfd's versatility is its strength and its weakness: the indirection costs cycles, and the single-threaded design has not aged well versus modern parallel linkers.

`ld.gold` is a from-scratch ELF-only linker that Google wrote in 2008 to speed up large C++ link times. It was multithreaded before lld and significantly faster than ld.bfd at the time. It has since fallen behind LLD on speed and far behind mold.

Both linkers do the same thing in concept: read object files and archives, resolve symbols, apply relocations, lay out segments, write the output. ld.bfd uniquely supports linker scripts in their full GNU flavor; many embedded and kernel projects depend on these scripts.

## §3 Platform coverage (May 2026)

`ld.bfd` covers a long tail of architectures: every ELF arch you can name (x86, x86-64, AArch64, ARM, MIPS variants, PowerPC, RISC-V, SPARC, m68k, s390, IA-64, Alpha, PA-RISC, SH, Xtensa, AVR, Blackfin, Microblaze, NDS32, ARC, OpenRISC, VAX), plus PE/COFF for MinGW, plus several niche formats. This is the linker for "I just want to bring up a new architecture".

`ld.gold` only does ELF and supports a narrower set of architectures (mainly x86, x86-64, AArch64, ARM, PowerPC).

Operating systems: Linux is primary. The binutils tree also targets BSDs, illumos, AIX, HP-UX, and Windows (MinGW for PE/COFF emission).

## §4 Current status (May 2026)

binutils 2.44 (February 2, 2025) was the watershed. It officially deprecated gold and moved the gold sources into a separate `binutils-with-gold-2.44.tar` tarball. Per Nick Clifton's announcement (https://lists.gnu.org/archive/html/info-gnu/2025-02/msg00001.html):

> "the binutils-2.44.tar tarball does not contain the sources for the gold linker, because the gold linker is now deprecated and will eventually be removed unless volunteers step forward and offer to continue development and maintenance."

The split-tarball policy (even-numbered releases include `binutils-with-gold`, odd-numbered ones do not) is a slow walk to retirement. As of May 2026, no new maintainer has emerged, and gold's removal is expected within the next two release cycles.

Downstream impact (cataloged in Fedora's deprecation page https://fedoraproject.org/wiki/Changes/DeprecateGoldLinker and Phoronix coverage https://www.phoronix.com/news/GNU-Gold-Linker-Deprecated):

- Fedora has begun the deprecation of `binutils-gold`.
- Debian still ships it (as of November 2025) but `buildd` no longer prefers it.
- Swift's bootstrap scripts were updated to default away from gold (https://github.com/swiftlang/swift/issues/79163).
- Clang LTO tests fail without gold's plugin interface, but those tests are being rewritten to use LLD.

`ld.bfd`, by contrast, is alive and well. It remains the default on Debian-based distros for `gcc` and is the only viable linker for many embedded and bare-metal projects because of its linker-script support.

## §5 Engineering cost for Mochi

- License: GPLv3. We do not ship binutils as part of Mochi (we shell out to the system). The GPL boundary is therefore at the process level and does not infect our compiler.
- Speed: ld.bfd is the slowest of the modern options. For Mochi-scale binaries (low single-digit MB) the absolute time is still well under a second, so this is not painful. For larger binaries the gap matters.
- Cross-compile: ld.bfd has the widest target coverage of any single linker, useful when Mochi wants to target an odd embedded ISA.
- Cgo: not relevant; we invoke `ld` or `cc -fuse-ld=bfd` as a subprocess.
- Distribution: ld.bfd is preinstalled on essentially every Linux distro. We never need to ship it.

For Mochi specifically, ld.bfd is the "fallback that always works" linker. We use it when nothing better is detected. We do not use gold under any circumstance, since it is deprecated.

## §6 Mochi adaptation note

In `tools/linkers` selection order on Linux:

1. `mold` if available.
2. `ld.lld` if available.
3. `ld.bfd` (always present, last resort).

Skip `ld.gold` entirely. Even if `gold` is on PATH, prefer `ld.bfd` because gold is deprecated and is being removed from major distros.

For Mochi's bare-metal or embedded targets (a Phase 3+ concern), `ld.bfd` is the only realistic linker because it understands GNU linker scripts that map memory regions, set entry points, and place sections in flash vs RAM. If Mochi ever grows a "make me an STM32 binary" target, this is where it lives.

The Mochi build system should never silently fall through to gold. If the user explicitly requests gold via a flag, emit a deprecation warning that references binutils 2.44.

## §7 Open questions for MEP-42

- Do we maintain a "compat" path for gold? Recommendation: no. Print a warning if detected, do not use.
- Do we test against ld.bfd in CI? Recommendation: yes, as the lowest-common-denominator fallback.
- For embedded targets, we need ld.bfd plus linker scripts; that is out of scope for Phase 1 but should not be designed away.

Sources:
- [GNU Binutils 2.44 Released (info-gnu list)](https://lists.gnu.org/archive/html/info-gnu/2025-02/msg00001.html)
- [Phoronix: GNU Gold Linker Is Deprecated](https://www.phoronix.com/news/GNU-Gold-Linker-Deprecated)
- [Fedora: DeprecateGoldLinker](https://fedoraproject.org/wiki/Changes/DeprecateGoldLinker)
- [LLVM discourse: binutils 2.44 deprecated ld.gold](https://discourse.llvm.org/t/binutils-2-44-deprecated-ld-gold/84444)
- [Swift: drop deprecated GNU Gold linker](https://github.com/swiftlang/swift/issues/79163)
- [Wikipedia: gold (linker)](https://en.wikipedia.org/wiki/Gold_(linker))