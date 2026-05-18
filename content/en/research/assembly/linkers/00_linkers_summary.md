---
title: "MEP-42 Linker and Runtime Recommendation"
description: "One paragraph each, Phase 1 vs Phase 2."
tags: ["native-codegen", "linkers"]
weight: 0
date: 2026-05-18T18:15:20+07:00
---

## §1 Phase 1 recommendation

Use LLD as the universal linker, with platform-aware overrides: `ld.lld` on Linux, the system `ld` (ld_prime) on macOS, `lld-link` on Windows. Bundle LLD inside the Mochi distribution (Apache 2 + LLVM exception license, one binary covers all four formats: ELF, Mach-O, PE, Wasm) so cross-host builds work from any developer machine. For the C runtime, use the host glibc on Linux (dynamic link, document the glibc-2.31 minimum) and the system libSystem on macOS / ntdll on Windows; for the explicit "portable Linux binary" mode (`mochi build --portable`), switch to musl 1.2.6 with static-PIE. Emit DWARF 5 (line tables only in Phase 1) for native targets on all OSes; skip PDB for now and tell Windows users that gdb and lldb work, WinDbg does not. Ship signed Mochi releases (Apple Developer ID + Microsoft Trusted Signing) but leave user-binary signing as an optional wrapper around the platform tools. Net stack: LLD + glibc (default) or musl-static-PIE (portable) + DWARF 5 line tables.

## §2 Phase 2 recommendation

Move toward a self-hosted writer for ELF, Mach-O, and PE, following Go's `cmd/link` pattern of "compiler emits the final image directly". This drops the LLD subprocess on the common path, halves cold-start build time, and lets us tune the output for Mochi-specific needs (typed-arena debug info, MEP-40 vm3 metadata sections). Keep LLD as the fallback for "I need to link against a C library" mode. On the libc side, push musl to be the default for new projects (it is already the default for the portable mode in Phase 1, and the Phase 2 freestanding path makes the libc choice almost irrelevant). Add a Cosmopolitan APE output target for "single binary, run anywhere" distribution, complementing per-OS native binaries rather than replacing them. Add full DWARF 5 type and variable info (Phase 1 had only line tables), with CodeView/PDB as an optional add-on for users who want WinDbg. Begin investing in a Wasm target with DWARF in custom sections for browser debugging via the Chrome C/C++ DevTools Support extension. Net stack at the Phase 2 end: Mochi-native image writer + musl (or freestanding direct syscalls on Linux) + libSystem on macOS + ntdll on Windows + DWARF 5 full + optional Cosmo APE + optional Wasm.

## §3 The single sentence

Phase 1: LLD plus host libc, DWARF 5 lines, musl for portable mode. Phase 2: self-hosted writers plus musl/freestanding, DWARF 5 full, Cosmo APE side-target.