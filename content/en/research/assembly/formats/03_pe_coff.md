---
title: "PE/COFF"
description: "The Windows executable and object format."
tags: ["native-codegen", "formats"]
weight: 30
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- Microsoft PE Format reference: https://learn.microsoft.com/en-us/windows/win32/debug/pe-format.
- The .NET runtime maintains a more thorough PE/COFF spec: https://github.com/dotnet/runtime/blob/main/docs/design/specs/PE-COFF.md.
- Windows x64 exception handling: https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64.
- Windows ARM64 exception handling: https://learn.microsoft.com/en-us/cpp/build/arm64-exception-handling.
- PDB / CodeView (partial Microsoft docs + the open-source reverse engineering): https://github.com/microsoft/microsoft-pdb.
- DWARF (used by mingw): https://dwarfstd.org/doc/DWARF5.pdf.
- Authenticode specification: https://download.microsoft.com/download/9/c/5/9c5b2167-8017-4bae-9fde-d599bac8184a/Authenticode_PE.docx.
- Go's debug/pe package: https://pkg.go.dev/debug/pe.

## §2 Mechanism / specification

A PE file starts with an MS-DOS stub (the "This program cannot be run in DOS mode" message), at offset 0x3C of which is a pointer to the PE signature ("PE\0\0"). After the signature:

- COFF file header (20 bytes): machine (IMAGE_FILE_MACHINE_AMD64 = 0x8664, IMAGE_FILE_MACHINE_ARM64 = 0xAA64, IMAGE_FILE_MACHINE_ARM64EC = 0xA641, IMAGE_FILE_MACHINE_I386 = 0x14C, IMAGE_FILE_MACHINE_RISCV64 = 0x5064), number of sections, timestamp, symbol table offset (legacy), number of symbols, optional header size, characteristics flags.
- Optional header (PE32 = 224 bytes, PE32+ = 240 bytes): magic (PE32 = 0x10B, PE32+ = 0x20B), linker version, code size, initialized data size, BSS size, entry point RVA, base of code, image base, section alignment, file alignment, OS version, image version, subsystem version, image size, headers size, checksum, subsystem (CUI, GUI, etc.), DLL characteristics, stack reserve/commit, heap reserve/commit, number of data directories (16), data directory entries.

Data directories are RVA+size pairs pointing into sections: Export Table, Import Table, Resource Table, Exception Table (.pdata), Certificate Table (code signature), Base Relocation Table, Debug Directory, TLS Table, Load Config Table, Bound Import, IAT, Delay Import, COM Descriptor.

Section table follows immediately: each entry is 40 bytes (name, virtual size, virtual address, raw data size, raw data pointer, relocation pointer, line number pointer, relocation count, line number count, characteristics).

Typical sections: .text (code), .data (initialized data), .rdata (read-only data), .bss (zero-initialized), .pdata (exception data), .xdata (unwind data), .reloc (base relocations), .idata (import directory), .edata (export directory), .tls (thread-local), .CRT (CRT init array), .rsrc (resources).

### Import Address Table

External function calls go through the IAT, a table of function pointer slots in .rdata (or .idata). At load time, the loader walks the Import Directory, opens each named DLL, looks up each named symbol, and writes the resolved address into the corresponding IAT slot. Code uses `call qword ptr [IAT+offset]` for indirect calls. This is conceptually equivalent to the ELF PLT/GOT, but without lazy binding (Windows resolves all imports at load time unless delay-load is configured).

### Exception handling on x64 (Table-based SEH)

The .pdata section holds `RUNTIME_FUNCTION` structures (BeginAddress, EndAddress, UnwindInfoAddress, all image-relative). UnwindInfoAddress points into .xdata, where `UNWIND_INFO` (header + array of UNWIND_CODE) describes the prolog operations to undo. Leaf functions need no pdata.

For dynamically generated code (JITs), `RtlAddFunctionTable` registers a table at runtime; `RtlInstallFunctionTableCallback` registers a lazy lookup.

### Exception handling on ARM64

ARM64 .xdata uses a different, more compact bytecode (save_reg, save_fpreg, alloc_s/m/l, set_fp, save_lrpair, save_regp, etc.) interpreted by the OS unwinder. Documented in Microsoft's ARM64 exception handling page.

### Hardening features

- Safe SEH (x86 only): a table of valid exception handler RVAs that the OS checks before dispatching. Set via /SAFESEH.
- Control Flow Guard (CFG): the loader populates a bitmap of valid indirect-call targets; the compiler emits `_guard_check_icall` before every indirect call. Enabled via /guard:cf.
- CET shadow stack: a single bit in the load config table (and DLL characteristics) marks the module CET-compatible. Hardware-enforced via Intel CET or AMD shadow stacks. Enabled via /CETCOMPAT in MSVC, `-z cet-report=error` style in lld. Compatibility mode (default) is per-module; strict mode terminates on any return-address mismatch.
- ASLR: requires base relocations (.reloc section); /DYNAMICBASE bit in DLL characteristics.
- DEP/NX: /NXCOMPAT bit.

### Code signing (Authenticode)

A PKCS#7 signed blob in the Certificate Table data directory. The signature covers the entire PE file with the certificate table itself, the certificate-table data directory entry, and the optional header checksum field excluded from the hash. Required for kernel drivers; recommended (and increasingly enforced via SmartScreen reputation) for user apps.

### Debug info

PDB: external file referenced from the Debug Directory via a CodeView IMAGE_DEBUG_TYPE_CODEVIEW record (the modern format starts with "RSDS" magic + 16-byte GUID + 4-byte age + null-terminated PDB path). Debuggers match the PDB to the PE via the GUID and age.

CodeView: legacy embedded debug info (NB09, NB10, NB11 magics), still seen in some C/C++ workflows.

DWARF: emitted by mingw-w64 toolchains in .debug_* sections within the PE. WinDbg does not consume DWARF; GDB does.

### Rich Header

Microsoft toolchain artifact between the DOS stub and PE signature. Records the toolchain versions of every contributing .obj. Useful for malware attribution; ignored by the loader.

## §3 Platform coverage (May 2026)

PE/COFF is used by:

- Windows (every version since NT 3.1).
- ReactOS.
- UEFI firmware images (a PE32+ subset).
- Wine on Linux/macOS/BSD (consumes PE for Windows app emulation).
- Cosmopolitan APE (see formats/05_ape_cosmopolitan.md): produces PE-compatible polyglot binaries.

## §4 Current status (May 2026)

- PE spec itself stable since the late 1990s; new bits land via DLL characteristics flags and load config table extensions.
- CET shadow stack default-enabled in Windows 11 24H2 kernel mode on supported hardware.
- CFG widespread in MSVC-built binaries.
- ARM64EC PE format mature, used by Office, Edge, Visual Studio.
- Arm64X (a PE that contains both ARM64 and ARM64EC code paths) used for system DLLs.
- Authenticode requirements for kernel drivers tightened: cross-signing retired, EV cert required.
- Modern MSVC defaults: /guard:cf, /CETCOMPAT, /SAFESEH (x86 only), /DYNAMICBASE, /NXCOMPAT, /HIGHENTROPYVA.

## §5 Engineering cost for Mochi

Highest complexity of the major formats:

1. Write a minimal PE32+ executable: DOS stub + PE signature + COFF header + optional header + section table + .text + .rdata. ~2-3 weeks for first working binary.
2. .pdata + .xdata emission: critical for any function that allocates stack space or calls other functions. Without it, any debugger or exception walk crashes. ~2-3 weeks for x64; similar effort for ARM64 (different bytecode format).
3. Import Directory + IAT: required to call any Win32 function. ~1 week.
4. Base relocations (.reloc): required for ASLR-compatible binaries. ~1 week.
5. TLS Directory: needed for thread-local storage. Optional in Phase 1.
6. Resources (.rsrc): icons, manifests, version info. Optional but expected for polished binaries.

Go's `debug/pe` reads but does not write. `cmd/link/internal/loadpe` and `cmd/link/internal/pe` write minimally. lld-link is the cleanest cross-platform PE writer.

Cross-compile from Linux/macOS: clang-cl + lld-link works well; Zig CC also handles this. mingw-w64 ld can produce PE/COFF but emits DWARF debug info (incompatible with WinDbg). No Microsoft toolchain dependency required.

## §6 Mochi adaptation note

compiler3 would gain an `objfile/pe` package. The MEP-40 runtime/vm3 arena allocator switches from mmap to VirtualAlloc. The Cell handle is unaffected. The startup stub for a Windows executable calls `mainCRTStartup` (the standard MSVC entry point) or a Mochi-specific `_start` that does its own initialization and calls into the program.

For Windows-on-ARM64, share the PE writer with x64 but plug in the ARM64 xdata encoder.

## §7 Open questions for MEP-42

1. .pdata/.xdata emission: must-have or leave to user to compile with /CETCOMPAT-style escape hatches? Recommend must-have; without unwind data even basic stack traces are broken.
2. CFG: opt-in via flag or default-on? Recommend opt-in for Phase 1, default-on once Mochi's stable.
3. PDB emission: Phase 1 ships CodeView in the COFF object (basic debugging in WinDbg), Phase 2 ships full external PDB.
4. Authenticode: out of scope for Phase 1 toolchain. Users sign their own binaries with signtool.exe or osslsigncode.
5. ARM64X (dual ARM64+ARM64EC) binaries: out of scope until Mochi has its own FFI story for x64 plugins.
