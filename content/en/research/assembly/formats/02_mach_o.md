---
title: "Mach-O"
description: "The Apple object/executable format: macOS, iOS, iPadOS, tvOS, watchOS, visionOS."
tags: ["native-codegen", "formats"]
weight: 20
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- Apple's loader.h header (canonical machine-readable spec): https://github.com/apple-oss-distributions/xnu/blob/main/EXTERNAL_HEADERS/mach-o/loader.h.
- Apple's Mach-O reference documentation (legacy archive): https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/MachORuntime/.
- Apple's TN3127 (Inside Code Signing: Requirements): https://developer.apple.com/documentation/technotes/tn3127-inside-code-signing-requirements.
- Apple's TN3151 (Choosing a tool chain): https://developer.apple.com/documentation/technotes/.
- Go's debug/macho package: https://pkg.go.dev/debug/macho.
- LLVM lld Mach-O backend source: https://github.com/llvm/llvm-project/tree/main/lld/MachO.
- Apple's open-source releases: https://opensource.apple.com/.

## §2 Mechanism / specification

A Mach-O file starts with a `mach_header_64` (32 bytes):

- magic: MH_MAGIC_64 (0xFEEDFACF).
- cputype, cpusubtype: x86_64 (0x01000007), arm64 (0x0100000C), arm64e (0x0100000C with ARM64E subtype).
- filetype: MH_OBJECT, MH_EXECUTE, MH_DYLIB, MH_BUNDLE, MH_DSYM, etc.
- ncmds, sizeofcmds: load command count and byte size.
- flags: MH_DYLDLINK, MH_PIE, MH_TWOLEVEL, MH_NOUNDEFS, etc.

After the header comes a sequence of `load_command` blobs, each typed. Key load commands:

- LC_SEGMENT_64: a region mapped into memory. Common segments: __TEXT (executable code, read-only), __DATA (read-write data), __DATA_CONST (read-only after relocations), __LINKEDIT (symbol tables, code signature, relocations).
- LC_SYMTAB: classic symbol table location.
- LC_DYSYMTAB: dynamic symbol table indexing into LC_SYMTAB.
- LC_LOAD_DYLINKER: path to dyld (`/usr/lib/dyld`).
- LC_LOAD_DYLIB: a required dynamic library, with timestamp and version.
- LC_RPATH: a runtime search path for @rpath-prefixed dependencies.
- LC_MAIN: the entry point offset within __TEXT (replaced LC_UNIXTHREAD for normal binaries).
- LC_BUILD_VERSION: platform (macOS, iOS, etc.), minOS version, SDK version, build tools used. Replaced the older LC_VERSION_MIN_MACOSX family.
- LC_CODE_SIGNATURE: pointer into __LINKEDIT where the signature blob lives.
- LC_UUID: a 128-bit unique identifier for the binary (used by debuggers and crash reporters).
- LC_FUNCTION_STARTS: a compact ULEB128 list of function start offsets.
- LC_DATA_IN_CODE: regions inside __TEXT that contain data (jump tables, etc.).
- LC_DYLD_INFO_ONLY (legacy) and LC_DYLD_CHAINED_FIXUPS + LC_DYLD_EXPORTS_TRIE (modern): the rebase/bind/lazy-bind/export info.
- LC_ENCRYPTION_INFO_64: required for App Store binaries on iOS.

Sections within __TEXT: __text (code), __cstring (C strings), __const (read-only constants), __stubs (PLT-equivalent), __stub_helper, __unwind_info (compact unwind), __eh_frame (DWARF unwind fallback).

### Universal (fat) binaries

A "fat" Mach-O is a thin wrapper containing multiple per-architecture Mach-O slices. The wrapper starts with `fat_header` (magic FAT_MAGIC 0xCAFEBABE or FAT_MAGIC_64 0xCAFEBABF), followed by `fat_arch` entries (cputype, cpusubtype, offset, size, align). The slices themselves are normal Mach-O files at the given offsets. Crucially, the fat header is big-endian regardless of the platform.

The `lipo` tool creates, inspects, and modifies fat binaries.

### @rpath and dyld search

When a Mach-O references a dependency with an install name beginning with `@rpath/`, dyld substitutes each LC_RPATH entry in turn until it finds the library. Other special prefixes: `@executable_path` (resolved relative to the main executable's directory) and `@loader_path` (resolved relative to the loading binary's directory; useful for plugins).

### Code signing

On Apple Silicon (since macOS 11), every executable and dylib must carry a code signature. An ad-hoc signature is sufficient (no Apple Developer cert needed) and the linker (`ld`) generates one automatically by default. The signature is a CodeDirectory blob (one or more hash subdirectories with SHA-256 hashes of every page of the binary) plus optional Requirements, Entitlements, and CMS envelope. Stored in __LINKEDIT, pointed to by LC_CODE_SIGNATURE.

Without a signature, Apple Silicon refuses to launch the binary (SIGKILL with EXC_BAD_ACCESS). x86_64 macOS does not enforce this requirement.

`codesign -s - binary` re-signs ad-hoc; `codesign --remove-signature` strips. Distribution outside the App Store requires Developer ID signing plus notarization.

### Compact unwind

Apple's `__unwind_info` section is a denormalized lookup table that maps PC ranges to "compact unwind encodings", small bit-packed descriptions of how to restore the stack and registers. Much faster than DWARF .eh_frame. Functions that do not fit the compact encoding fall back to DWARF in `__eh_frame`.

## §3 Platform coverage (May 2026)

Mach-O is used by every Apple OS: macOS (Intel and Apple Silicon), iOS, iPadOS, watchOS, tvOS, visionOS. Plus historical NeXTSTEP, OPENSTEP, and Darwin distributions like PureDarwin.

Tooling: Apple's `ld` (the system linker), lld (LLVM, MH_OBJECT and MH_EXECUTE production-quality), GNU binutils (poor Mach-O support, mostly ignored), Zig's built-in Mach-O linker, Go's cmd/link/internal/loadmacho.

## §4 Current status (May 2026)

- LC_BUILD_VERSION has replaced the older LC_VERSION_MIN_* family for new binaries.
- Chained fixups (LC_DYLD_CHAINED_FIXUPS) shipped with macOS 12 and are now the standard binding mechanism.
- PAC (pointer authentication) is mandatory for arm64e binaries (used by Apple's own frameworks); third-party apps can ship arm64 (plain) which interoperates fine.
- Universal 2 binaries (x86_64 + arm64) are the standard distribution format for apps that support both Intel and Apple Silicon.
- Apple has not deprecated x86_64 Macs as of macOS 15.x, but rumors suggest macOS 16 (or 17) will drop them; Phase 1 should still emit Universal 2.
- Notarization is required for Gatekeeper to accept binaries from outside the App Store; signing alone is insufficient for distribution.

## §5 Engineering cost for Mochi

Higher than ELF but lower than PE. Go has `debug/macho` for reading; writing requires hand-rolling or porting lld's emitter.

Must-have for a minimal viable backend:

1. mach_header_64 with correct cputype/cpusubtype.
2. LC_SEGMENT_64 for __TEXT and __LINKEDIT at minimum (Mochi can compile a static, no-data binary with just these).
3. LC_SYMTAB and LC_DYSYMTAB.
4. LC_LOAD_DYLINKER pointing at /usr/lib/dyld.
5. LC_LOAD_DYLIB for /usr/lib/libSystem.B.dylib (needed even for Hello World).
6. LC_MAIN with the entry offset.
7. LC_BUILD_VERSION with the target macOS/iOS/etc. version.
8. LC_UUID (16 random bytes).
9. LC_CODE_SIGNATURE pointing at an ad-hoc signature (or invoke `codesign -s - binary` post-link).
10. __unwind_info compact unwind section (or invoke `ld` to generate it from DWARF).

Should-have: LC_FUNCTION_STARTS, LC_DATA_IN_CODE, chained fixups.

Nice-to-have: dSYM emission for debugger support (separate Mach-O of type MH_DSYM), entitlements.

Cross-compile from Linux: lld targets Mach-O cleanly. Zig CC handles macOS targets out of the box. The only friction is code signing; Linux can produce an ad-hoc signature using the `sigtool` or `rcodesign` (rust) reimplementations.

## §6 Mochi adaptation note

compiler3 would gain an `objfile/macho` package. The MEP-40 runtime/vm3 needs to call mmap for the arena (works identically on macOS as Linux); the only Apple-specific concern is that `mmap` regions intended for code need MAP_JIT plus the `com.apple.security.cs.allow-jit` entitlement on hardened-runtime apps. For AOT-compiled Mochi this does not matter.

For Apple Silicon, the backend must emit position-independent code (Apple disables non-PIE binaries since macOS 12) and must include LC_BUILD_VERSION with a plausible minOS (recommend macOS 13.0 floor in 2026).

## §7 Open questions for MEP-42

1. Universal 2 (x86_64 + arm64) as default for macOS, or per-arch slices only? Recommend Universal 2 default; smaller per-arch flag.
2. Code signing in the build pipeline: bundle an `rcodesign`-equivalent, or shell out to `codesign`? Recommend shell out when on macOS host, bundle on cross-compile.
3. Notarization automation: Phase 2; requires Apple Developer credentials and is out of scope for an open-source language toolchain Phase 1.
4. iOS / visionOS support: defer beyond Phase 1; needs MH_BUNDLE handling, Info.plist generation, and provisioning profile machinery.
5. dSYM: Phase 1 emits inline DWARF in __DWARF section; Phase 2 produces separate dSYM bundles.
