---
title: "Cosmopolitan Libc"
description: "One binary, six operating systems, two ISAs. The APE format and cosmocc toolchain."
tags: ["native-codegen", "runtime"]
weight: 30
date: 2026-05-18T18:08:55+07:00
---

## §1 Provenance

- Project home: https://justine.lol/cosmopolitan/
- Source: https://github.com/jart/cosmopolitan
- Cosmopolitan "Third Edition" essay (Justine Tunney): https://justine.lol/cosmo3/
- cosmocc README: https://github.com/jart/cosmopolitan/blob/master/tool/cosmocc/README.md
- Prebuilt apps: https://cosmo.zip/
- Discussion: https://groups.google.com/g/cosmopolitan-libc
- License: ISC (a permissive 1-clause BSD variant).
- Author: Justine Tunney, with Mozilla MIECO sponsorship for 3.x.

## §2 Mechanism / function

Cosmopolitan Libc produces a single binary, called an "Actually Portable Executable" (APE), that is simultaneously:

- A Linux ELF (you can `./prog` on Linux and it runs).
- A FreeBSD / NetBSD / OpenBSD ELF.
- A macOS Mach-O.
- A Windows PE.
- A BIOS bootloader.

The trick is a polyglot file format. Bytes that the Linux kernel reads as ELF program headers are simultaneously valid PE headers (interpreted by Windows), valid Mach-O fat headers (interpreted by macOS), and valid x86 boot code (interpreted by BIOS). The same `.com` file behaves correctly under each OS loader.

The libc layer abstracts over six different system call conventions:

- Linux: `syscall` instruction with Linux numbers.
- FreeBSD/NetBSD/OpenBSD: each has its own `syscall` ABI.
- macOS: indirect via libsystem_kernel calls (not direct syscall; macOS forbids that).
- Windows: NTAPI through ntdll plus a custom loader.
- BIOS: int 0x10/0x13/0x15 etc.

At process startup, code runs a tiny detector that figures out the host OS and dispatches the right syscall stubs into a global table.

`cosmocc` is the compiler driver. It is a wrapper around GCC 14.1.0 and Clang 19 that pre-configures the compile and link flags to emit APE binaries. It supports both x86_64 and aarch64 via separate command-line tools (`cosmocc` for fat x86_64+aarch64 output, `cosmocc -m64` for x86_64-only, etc.).

## §3 Platform coverage (May 2026)

OS at runtime: Linux, macOS, Windows (10 and 11), FreeBSD, OpenBSD 7.3+, NetBSD, BIOS / bare metal.

ISA at runtime: x86_64 and aarch64 (since 3.x; older versions were x86_64 only).

Host for building: Linux is the usual host (cosmocc is a Linux toolchain). It can also run under WSL on Windows and under Rosetta on macOS, but Linux is canonical.

## §4 Current status (May 2026)

Cosmopolitan 4.0.2 was the early-2025 release line (4.0.1 was January 4, 2025; subsequent point releases through 2025 and into 2026). The 4.x line is the "things have started to work well" tier per Tunney's release notes.

The toolchain bundle currently ships GCC 14.1.0, Clang 19, Cosmopolitan Libc, LLVM libcxx, LLVM compiler-rt, LLVM OpenMP, plus pieces from musl and the BSDs.

Production users:

- Llamafile (https://github.com/Mozilla-Ocho/llamafile) ships LLM weights and inference engine as one APE binary. This is the highest-profile cosmo deployment.
- Redbean (https://redbean.dev/) is a single-file web server / Lua application stack.
- Cosmo Software ports of bash, vim, emacs, git, links, wget, qjs, python (https://cosmo.zip/) all work cross-platform.
- A growing tail of CLI tools that want zero install friction.

Mozilla's MIECO program funded the 3.x rewrite. The project has one principal maintainer (Tunney). The bus factor is therefore one, but the code is BSD-style permissive and could be forked.

## §5 Engineering cost for Mochi

The promise: one Mochi build produces one binary that runs on Linux, macOS, Windows, BSDs.

The cost:

- We must use Cosmo's libc, not the host libc. Anything that relies on `dlopen`-ing system libraries is out. Cosmo does not link against `libc.so.6` or `libSystem.dylib`.
- We compile with cosmocc, which means GCC 14 or Clang 19 with cosmo's flags. We do not get to use the system clang.
- The output binary is larger because it bundles per-OS syscall code. A "hello world" APE is around 130 KB.
- macOS notarization is awkward (the APE is not a standard Mach-O bundle). Cosmo binaries are usually distributed as "Linux first, runs on Mac as a convenience" rather than "shipped to the Mac App Store".
- Windows Defender SmartScreen will warn about unsigned APE binaries the same way it would warn about any unsigned `.exe`.
- License: ISC. Trivially compatible.
- Cross-compile: cosmocc is Linux-hosted but produces a binary that runs on everything. So one Linux build host suffices.
- The startup detector adds tens of microseconds; negligible.

For Mochi, cosmo is attractive precisely because it solves the cross-OS distribution problem in one move. The cost is that we are betting on a one-maintainer project and a specific toolchain version.

## §6 Mochi adaptation note

Mochi already has scaffolding for this idea. The existing `tools/cosmo/cosmo.go` and `tools/cosmo/cosmo_test.go` files plus `runtime/cosmo/Makefile` show prior interest in cosmo-style distribution. The MEP-42 path:

1. Add a `mochi build --cosmo` mode that drives `cosmocc` on the user's Linux host (or via a bundled toolchain).
2. The Mochi runtime emitted in this mode must avoid POSIX features that cosmo does not implement (most are fine; some edge cases exist).
3. Output is a single `.com` file that the user can ship anywhere.
4. Phase 2 question: do we use cosmo as the ONLY Mochi distribution target, or as one of several? Recommended: one of several. Cosmo for "release to end users", per-OS native for "production server".
5. We can reuse `runtime/cosmo/Makefile` patterns to drive cosmocc as a subprocess.

The `runtime/vm3/op.go` and `runtime/vm3/vm.go` are pure Go and do not need changes. The native code generated by `compiler3/emit` is where the cosmo-specific flags apply.

If Mochi wants to ship the Mochi compiler itself as an APE (so users download one file), we can do that too: build the Go compiler with `GOOS=linux GOARCH=amd64` and link with cosmocc instead of the Go linker. This is non-trivial and probably Phase 3.

## §7 Open questions for MEP-42

- Do we bundle the cosmocc toolchain in the Mochi distribution? It is around 200 MB; not trivial.
- Do we support cosmo as a first-class target, or as a `--experimental-cosmo` opt-in?
- How do we handle "this Mochi program uses fork+exec / dlopen / network features cosmo restricts"? Document the subset.
- What is our story when the single cosmo maintainer steps back? Fork or migrate.

Sources:
- [Cosmopolitan Libc](https://justine.lol/cosmopolitan/)
- [Cosmopolitan Third Edition](https://justine.lol/cosmo3/)
- [cosmocc README](https://github.com/jart/cosmopolitan/blob/master/tool/cosmocc/README.md)
- [jart/cosmopolitan releases](https://github.com/jart/cosmopolitan/releases)
- [Cosmo Software (prebuilt binaries)](https://cosmo.zip/)
- [Catching up with the Cosmopolitan ecosystem (Simon Willison)](https://til.simonwillison.net/cosmopolitan/ecosystem)