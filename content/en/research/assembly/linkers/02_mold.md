---
title: "mold: The Modern Linker"
description: "The fastest production ELF linker, single-author, MIT licensed."
tags: ["native-codegen", "linkers"]
weight: 20
date: 2026-05-18T18:03:33+07:00
---

## §1 Provenance

- Project home and source: https://github.com/rui314/mold
- Author: Rui Ueyama (also the original author of LLD).
- Commercial vehicle: Blue Whale Systems PTE LTD (Tokyo / Singapore).
- License: MIT (since mold 2.0, October 2023). The earlier AGPL plus commercial dual-license was retired (see https://www.phoronix.com/news/Mold-2.0-Linker).
- Slides and design background: https://easybuild.io/tech-talks/006_mold_slides.pdf

## §2 Mechanism / function

mold is an ELF-only linker that targets the same role as `ld.bfd`, `ld.gold`, and `ld.lld`: take a set of `.o` files and shared libraries, resolve symbols, apply relocations, lay out segments, and write an executable or shared object.

The design choices that make it fast:

- Thread-parallel everything. Symbol resolution, section merging, relocation application, and output writing all use a work-stealing thread pool. mold scales nearly linearly to the number of cores on a typical build host.
- `mmap` based output. The output file is `ftruncate`d to its final size up front, then written via `mmap`. This avoids `write(2)` system call overhead and lets the kernel's page cache batch the I/O.
- Optimistic symbol resolution. mold computes symbol tables in parallel using lock-free hash tables (Ankerl's `unordered_dense`) rather than the historical single-threaded BFS that older linkers use.
- Aggressive use of SIMD for string interning, CRC, and hash construction.

mold is a `ld.bfd`-compatible drop-in. Most projects switch by setting `LDFLAGS="-fuse-ld=mold"` or, since CMake 3.29, `-DCMAKE_LINKER_TYPE=MOLD`.

## §3 Platform coverage (May 2026)

ELF only. Supported architectures: x86-64, i386, AArch64, ARM (32-bit), RISC-V (32 and 64), PowerPC, PowerPC64 (BE and LE), s390x, SPARC64, LoongArch64, M68K, SH-4.

Operating systems: Linux is the primary target. FreeBSD, OpenBSD, NetBSD, illumos, and Solaris all work, though less heavily tested.

No Mach-O. The "sold" Mach-O port that Ueyama started in 2022 was abandoned as an open-source effort but is sold (no pun intended) as a paid commercial product through Blue Whale Systems (https://bluewhale.systems/). The free, public mold has no Mach-O code today and no public roadmap for adding it.

No COFF. No Wasm.

## §4 Current status (May 2026)

mold 2.41.0 shipped April 13, 2026 (per Ueyama's announcement at https://x.com/rui314/status/2043672282695090291). Releases occur roughly every two months and consist of incremental performance work plus architecture-specific bug fixes.

The 2.x line has been stable since late 2023. mold 2.31 brought another roughly 10 percent speedup on large debug-info-enabled binaries.

Production users:

- Chromium's official Linux build documentation recommends mold for developer builds.
- Many large monorepos (Meta's internal builds, Google's Bazel-on-Linux, multiple game engines) use mold.
- Alpine, Arch, Debian, Ubuntu, Fedora, and openSUSE all package mold.
- The Linux kernel build system can use mold (and frequently does for developer builds).

mold has effectively replaced ld.gold (deprecated in binutils 2.44, February 2025) as the recommended fast Linux linker. See `04_gnu_ld_and_gold.md`.

The benchmark Ueyama frequently quotes (https://github.com/rui314/mold) shows mold is approximately 4x faster than LLD, 18x faster than ld.gold, and 31x faster than ld.bfd on a Chromium-class link.

## §5 Engineering cost for Mochi

- License: MIT, no problems.
- Binary size: roughly 6 to 12 MB static; smaller than LLD because it only handles one format.
- Cross-compile: mold can be invoked from a non-Linux host (the binary builds on macOS and Windows under MSYS), but it only emits ELF. So mold solves "fast ELF linking" but does nothing for our Windows or macOS targets.
- Cgo: not required. Standard `os/exec` invocation.
- Active maintainership: one principal author (Ueyama) plus a community of contributors. This is a key risk: if Ueyama stops working on it, the project's velocity slows dramatically. The bus factor is similar to musl libc (also Rich-Felker-driven).
- Build cost: requires C++20 plus CMake. Distros ship binaries.

Where mold shines for Mochi specifically: developer link times. If Mochi-compiled native binaries are large (whole VM3 statically linked plus Mochi standard library), incremental link is exactly where mold pays off.

## §6 Mochi adaptation note

mold is the right choice as the default ELF linker for Mochi's Linux target when one is detected on the build host. Concrete pattern:

1. `tools/lld` (or a new `tools/linkers` package) probes for available linkers in order: `mold` -> `ld.lld` -> system `ld`. Cache the choice per build session.
2. The probe lives next to the existing `tools/cosmo/cosmo.go` precedent.
3. Mochi's `compiler3/emit/obj` writes ELF relocatables; mold resolves them.
4. We do not ship mold inside the Mochi tarball. We require a system installation on Linux, document this in `INSTALL.md`, and fall back gracefully to `ld.lld` (we do bundle LLD on Linux as a smaller, all-format default).
5. On non-Linux hosts targeting Linux, we use `ld.lld` because mold's cross-OS story (running the mold binary on macOS) is not well supported.

## §7 Open questions for MEP-42

- Do we depend on mold's presence (faster developer experience, more tooling assumption) or auto-detect (more portable, slower default)?
- Bus-factor mitigation: is the project's risk of single-maintainer drop-off acceptable? LLD has a wider pool.
- Phase 2 question: do we revisit Mach-O when "sold" or a successor matures? Probably not, since Apple's own ld is already fast on modern hardware.
- Do we run mold's `--icf=safe` and `--gc-sections` by default for size?

Sources:
- [mold on GitHub](https://github.com/rui314/mold)
- [Mold 2.0 Released, Moves From AGPL To MIT (Phoronix)](https://www.phoronix.com/news/Mold-2.0-Linker)
- [Mold 2.31 release coverage](https://www.phoronix.com/forums/forum/software/programming-compilers/1461609-mold-2-31-now-~10-faster-when-linking-very-large-debug-info-enabled-binaries)
- [Rui Ueyama mold 2.41.0 announcement](https://x.com/rui314/status/2043672282695090291)
- [mold design slides](https://easybuild.io/tech-talks/006_mold_slides.pdf)