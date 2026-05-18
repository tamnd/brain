---
title: "APE (Actually Portable Executable) and Cosmopolitan Libc"
description: "A single binary that is simultaneously a valid ELF, Mach-O, PE, and BSD a.out."
tags: ["native-codegen", "formats"]
weight: 50
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- Cosmopolitan Libc source and docs: https://github.com/jart/cosmopolitan.
- APE specification: https://github.com/jart/cosmopolitan/blob/master/ape/specification.md.
- Cosmopolitan project page: https://justine.lol/cosmopolitan/.
- llamafile project: https://github.com/mozilla-ai/llamafile.
- redbean web server: https://redbean.dev/.
- Cosmopolitan release notes: https://github.com/jart/cosmopolitan/releases.
- ape-loader source (the 8 KB loader extracted at runtime on Linux): https://github.com/jart/cosmopolitan/tree/master/ape.
- The cosmocc toolchain releases: https://cosmo.zip/pub/cosmocc/.

## §2 Mechanism / specification

APE is a polyglot binary format invented by Justine Tunney. A single file simultaneously parses as:

- A Linux ELF executable.
- A macOS Mach-O executable.
- A Windows PE executable (MZ + PE signature).
- A FreeBSD/OpenBSD/NetBSD a.out (or, in modern builds, ELF).
- A ZIP archive (so resources can be appended and read by both the program itself and standard `unzip`).
- A POSIX shell script that bootstraps the binary on systems that try to interpret the shebang.

The trick: the first bytes of the file are carefully chosen so multiple OS loaders all accept them. The file starts with `MZqFpD='`, which is a valid MS-DOS / PE magic and also a valid POSIX shell assignment. The rest of the first 8192 bytes contains a series of `printf` shell commands that, when interpreted as a shell script, decode an embedded ELF or Mach-O header (in octal) into a temporary file (the "APE loader") and exec it.

On Windows, the kernel sees MZ at offset 0 and the standard PE signature later, so it loads natively.

On macOS, the kernel sees a valid Mach-O fat header (or single arch header) emitted as part of the printf output and loads natively if the kernel has been told to honor APE; otherwise the shell interprets the script.

On Linux, the kernel can be taught (via binfmt_misc registration) to recognize the APE magic and invoke `/usr/bin/ape` directly. Without that, the shell interprets the script, which extracts an 8 KB APE loader to `${TMPDIR:-${HOME:-.}}/.ape`, which then maps the embedded ELF segments into memory.

On the BSDs, similar shell-driven extraction.

### Multi-architecture APEs

A fat APE built with `apelink` (Cosmopolitan's linker) wraps multiple per-architecture binaries (AMD64 and ARM64 are the supported pair as of 4.x). The header contains two encoded ELF/Mach-O headers in octal; loaders that natively understand APE check the `e_machine` field of each to pick the right one. On systems that shell-interpret the script, multiple printf-decoded headers cover both architectures.

### Cosmopolitan Libc

Cosmopolitan is a static libc that abstracts over six OSes (Linux, macOS, Windows, FreeBSD, OpenBSD, NetBSD) and two CPU architectures (AMD64, ARM64). Every syscall is implemented as a multi-OS dispatch that picks the right system call number and ABI at runtime based on detected host. The result: a single static binary that calls `read()` and works on any of the supported OSes.

Cosmopolitan implements roughly the POSIX-ish surface of libc, plus Windows extensions, plus Cosmopolitan-specific helpers (dispatch tables, IsLinux(), IsXnu(), IsWindows(), etc.).

### dlopen support

Static linking is the natural fit for "build once, run anywhere", but it breaks GPU and GUI libraries that must be host-specific. Cosmopolitan addresses this via a limited `dlopen()` shim that manually loads a platform-specific helper executable and asks the OS-specific libc's dlopen to load OS-specific libraries. This is how llamafile uses CUDA / Metal / Vulkan GPU backends from inside an APE.

## §3 Platform coverage (May 2026)

A single APE binary runs on:

- Linux (every distro, x86_64 and aarch64).
- macOS (Intel and Apple Silicon, via Mach-O slice).
- Windows 10/11 (x86_64; ARM64 support via emulation).
- FreeBSD, OpenBSD, NetBSD (x86_64; ARM64 BSDs also supported).
- Linux with binfmt_misc APE registration: zero-overhead, no shell intermediary.

Notable adopters:

- llamafile (Mozilla): packages an LLM in a single APE, running on any of the six OSes without dependencies.
- whisperfile: same model for speech-to-text via whisper.cpp.
- redbean: a single-file web server with an embedded Lua interpreter and Forth runtime; ships as one APE binary.
- pkzip-derived tooling that wants a portable executable distribution.
- Various scientific computing one-shots (statistical solvers, format converters).

## §4 Current status (May 2026)

- cosmocc toolchain at version 4.x (4.0.2 is the version used by llamafile as of early 2026).
- Cosmopolitan 4.x added native ARM64 support, much-improved Windows-ARM64 story, and the `apelink` fat-binary linker.
- llamafile 0.10.0+ uses cosmocc 4.x and ships AMD64 + ARM64 in one file. GPU support via runtime-loaded helper modules.
- redbean continues to be the canonical Cosmopolitan showcase; small, fast, runs everywhere.
- Windows 4 GiB executable size limit remains a constraint; large datasets (LLM weights) are typically shipped as separate .gguf files.
- Linux distros increasingly preinstall the ape-loader or register binfmt_misc for APE.

## §5 Engineering cost for Mochi

High but not insurmountable, and pays off in extreme portability.

Two paths:

1. Emit pure APE from Mochi: significant work. Mochi would need to understand the polyglot header layout, the printf bootstrap, the binfmt_misc magic, the fat-binary encoding via apelink. The Cosmopolitan source is the only complete reference; replicating it in Go is multi-month effort.

2. Use cosmocc as the toolchain: much cheaper. Mochi emits C (or LLVM IR) and pipes through cosmocc. The resulting binary is automatically APE-formatted. This is how llamafile works.

For Mochi specifically, path 2 only makes sense if Mochi already has a C backend (or LLVM IR backend) in the pipeline. If Mochi emits native machine code directly, path 1 is the only option, and at that point it's hard to justify versus simply shipping per-OS binaries.

A middle path: Mochi emits per-architecture ELF/Mach-O/PE binaries (which we already pay for in Phase 1) and a separate `mochi-apelink` tool (a thin wrapper over Cosmopolitan's apelink) bundles them into a fat APE. This makes APE an opt-in distribution format rather than a primary backend.

## §6 Mochi adaptation note

compiler3 likely does not gain an "APE backend" per se. Instead, an `objfile/ape` post-link tool can consume the ELF / Mach-O / PE outputs of the per-target backends and weave them into a single polyglot binary. This is bookkeeping work (header layout, printf bootstrap, shell escape) rather than code generation.

The runtime/vm3 needs no awareness of APE: from its perspective, it's running as a normal native binary on whatever OS happens to be detected.

The Cosmopolitan libc would need to be linked in if Mochi wants to use it for IO portability. Alternatively, Mochi can ship its own thin syscall abstraction layer and avoid the cosmocc dependency.

## §7 Open questions for MEP-42

1. Is APE a Phase 1 feature, a Phase 2 feature, or never? Recommend Phase 2 or later: APE is high-value for distribution but low-value as a Phase 1 backend. Most users will be happy with per-OS binaries.
2. Path 1 (native APE emitter) vs path 2 (post-link bundler using Cosmopolitan)? Recommend path 2 (bundler). Lower engineering cost, leverages existing well-tested infrastructure.
3. Cosmopolitan dependency: bundle the cosmocc toolchain, or document an external install? Recommend external install with a Mochi flag `--package-as-ape` that fails informatively if cosmocc is missing.
4. GPU and dynamic-library support: opt-in only, requires Cosmopolitan's dlopen shim. Document the limitation.
5. License compatibility: Cosmopolitan is ISC-licensed (BSD-equivalent), no GPL contamination. Safe to depend on.
