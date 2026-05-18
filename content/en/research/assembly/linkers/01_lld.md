---
title: "LLD: The LLVM Linker"
description: "One binary, four object formats, cross-link from any host."
tags: ["native-codegen", "linkers"]
weight: 10
date: 2026-05-18T18:02:28+07:00
---

## §1 Provenance

- Project home: https://lld.llvm.org/
- Source tree: https://github.com/llvm/llvm-project/tree/main/lld
- Release notes (20.1.0): https://releases.llvm.org/20.1.0/tools/lld/docs/ReleaseNotes.html
- License: Apache 2.0 with LLVM exception (SPDX `Apache-2.0 WITH LLVM-exception`).
- Lead maintainers (ELF port): Fangrui Song (MaskRay), Igor Kudrin, Peter Smith. The COFF port is led by Martin Storsjo and Reid Kleckner. Apple, Sony, ARM, Google, and the broader LLVM community all contribute.

LLD ships as part of the LLVM monorepo and inherits LLVM's release cadence (approximately every six months).

## §2 Mechanism / function

LLD is a family of linkers behind a common name. Each format gets its own driver binary:

- `ld.lld` for ELF (Linux, BSD, illumos, bare metal).
- `ld64.lld` for Mach-O (macOS, iOS, watchOS, visionOS).
- `lld-link` for PE/COFF (Windows, MinGW).
- `wasm-ld` for WebAssembly.

All four share the LLVM object library (`llvm/Object`, `llvm/Support`, `llvm/BinaryFormat`) for reading inputs. Each driver is a thin front end over the relevant `lld/<format>/Driver.cpp` that parses command-line arguments, then a writer (`lld/<format>/Writer.cpp`) that emits the final image.

LLD performs the conventional linking phases (symbol resolution, section merging, garbage collection of unreferenced sections via `--gc-sections`, relocation, layout, output write) but with a heavily parallelized core. In LLVM 20 and beyond, mark-live (GC) became level-synchronized parallel BFS, and several other phases were rewritten with `parallelFor` (see https://maskray.me/blog/2026-04-12-recent-lld-elf-performance-improvements).

LLD also supports LTO natively via the LLVM `ThinLTO` and `FullLTO` plugins, so a single invocation can finish bitcode-to-image without an external plugin.

## §3 Platform coverage (May 2026)

ELF: AArch64, AMDGPU, ARM (v6-M through v9), Hexagon, LoongArch, MIPS 32/64 (big/little), PowerPC, PowerPC64, RISC-V (32/64), SPARC V9, x86, x86-64. The ELF port is the most feature-complete and is what Chromium, Rust, FreeBSD, and Android use.

Mach-O: arm64, arm64e, x86-64, x86-64h. The new ld64.lld is the default linker for Clang/macOS in many distro packages. Apple's official toolchain still ships their own ld (see `03_apple_ld_prime.md`), but LLD is the only viable cross-host option (linking a macOS binary from a Linux build agent).

COFF: x86, x86-64, ARM, ARM64, ARM64EC. LLVM 20 completed `/machine:arm64ec` support, the format used by Windows-on-ARM emulation glue. `lld-link` is the default linker for `clang-cl` and is widely used by Rust on Windows.

Wasm: wasm32, wasm64 (experimental). Used by Emscripten and clang `--target=wasm32-wasi`.

## §4 Current status (May 2026)

LLVM 20.1.0 shipped March 2025 (see https://releases.llvm.org/20.1.0/tools/lld/docs/ReleaseNotes.html). The 22.x branch has been cut, and post-22.1 patches have parallelized more phases. Per recent benchmarks from MaskRay (https://maskray.me/blog/2026-04-12-recent-lld-elf-performance-improvements), a Release+Asserts clang link with `--gc-sections` is now 1.37x as fast as lld 22.1, and a Chromium debug build with `--gdb-index` is 1.07x as fast. mold and wild remain ahead on pure throughput.

Production users include: Chrome/Chromium, Rust (default on most platforms except macOS), Zig (via its `zig cc` driver), FreeBSD (default since 13.x), OpenBSD, NetBSD, Sony PS4/PS5 SDK, Sony Open Source Console Toolchain, the official Android NDK, and most LLVM-based vendor toolchains (AMD ROCm, NVIDIA HPC SDK, Intel oneAPI).

Active maintainership is strong: hundreds of commits per release, multiple full-time contributors across vendor companies.

## §5 Engineering cost for Mochi

LLD is the only linker that meets every Phase 1 portability target with one codebase. The tradeoffs:

- Binary size: a statically linked LLD is around 30 to 50 MB depending on which format drivers are enabled. Mochi can ship a slimmed build by configuring only the formats we emit.
- Build cost: needs CMake plus a C++ toolchain to build from source. If Mochi distributes the linker, we either bundle prebuilt binaries (per-platform tarballs) or pull from system packages.
- License: Apache 2 plus LLVM exception is permissive and compatible with Mochi's BSD-style license. No copyleft.
- Cross-compile: LLD is fully cross-platform. From a Linux build host we can emit a macOS arm64 Mach-O, a Windows x86-64 PE, and a Linux ELF without leaving the process. No other tool gives us that.
- No cgo required. LLD has a stable command-line interface, so Mochi can invoke it as a subprocess via `os/exec`. There is also `lld::elf::link()` as a C++ entry point if we ever want to embed it.
- Concurrency: LLD is internally parallel, so we should not parallelize at the Mochi compiler level beyond `GOMAXPROCS` worth of links in parallel (it would just thrash threads).

## §6 Mochi adaptation note

Mochi `compiler3` emits typed IR via `compiler3/ir` and lowers through `compiler3/emit`. For native binaries, we extend the `emit` package with an object-file writer (per `linkers/05_skipping_linkers.md` we may write our own) or, more pragmatically, hand off to LLD.

Concrete integration sketch:

1. Add `compiler3/emit/obj` that produces relocatable `.o` files (ELF / Mach-O / COFF).
2. Add `tools/lld` (analogous to existing `tools/cosmo`) that wraps `os/exec.Command("ld.lld", ...)` with platform-aware default flags.
3. The Mochi driver in `cmd/mochi build` shells out to LLD with `--gc-sections`, `--icf=safe`, and `-O2`.
4. For Mach-O: prefer the system `ld` on macOS (per Mochi memory note `feedback_spec_in_sync.md`, we keep platform conventions) but fall back to `ld64.lld` for cross builds.
5. We do not embed LLD as a library (C++/cgo cost is too high for a Go-hosted compiler). We invoke the binary.

The `runtime/cosmo/Makefile` shows the precedent for shelling out to an external toolchain.

## §7 Open questions for MEP-42

- Do we ship LLD inside the Mochi distribution, or assume the user has a toolchain installed? Bundling adds 30 to 50 MB; assuming a toolchain breaks the "single download" promise.
- For macOS, do we prefer the system `ld` (better integration with Xcode signing, dSYM) or `ld64.lld` (better cross-host story)?
- Do we want LTO? If yes, we pin LLD plus a matching `llc` for ThinLTO. That doubles the bundle size.
- Phase 1 default: probably `ld.lld` on Linux, system `ld` on macOS, `lld-link` on Windows. Revisit in Phase 2.

Sources:
- [LLD: The LLVM Linker](https://lld.llvm.org/)
- [lld 20.1.0 Release Notes](https://releases.llvm.org/20.1.0/tools/lld/docs/ReleaseNotes.html)
- [Recent lld/ELF performance improvements (MaskRay)](https://maskray.me/blog/2026-04-12-recent-lld-elf-performance-improvements)
- [LLVM 20.X Release Milestone](https://github.com/llvm/llvm-project/milestone/26)
- [Fedora LLVM 20 changes](https://fedoraproject.org/wiki/Changes/LLVM-20)