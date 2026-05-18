---
title: "CodeView and PDB"
description: "Microsoft's native debug format, the sidecar PDB file, and the pain of producing one on Linux."
tags: ["native-codegen", "debug"]
weight: 20
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- LLVM PDB format documentation: https://llvm.org/docs/PDB/index.html
- llvm-pdbutil reference: https://llvm.org/docs/CommandGuide/llvm-pdbutil.html
- Reid Kleckner (Google), "CodeView, the MS debug info format, in LLVM" (2016): https://llvm.org/devmtg/2016-11/Slides/Kleckner-CodeViewInLLVM.pdf
- Microsoft cvinfo.h (CodeView record definitions): https://github.com/microsoft/microsoft-pdb (the canonical reference dump from Microsoft, last published 2017, still authoritative)
- Format is owned by Microsoft and partially open. The "MS-PDB" specification was never formally published; the LLVM team reverse-engineered enough to produce a complete writer.

## §2 Mechanism / function

Three distinct concepts that get conflated:

MSF (Multi-Stream Format) is the container, an old Microsoft file format that stores N independent byte streams in fixed-size blocks. A PDB file is an MSF file with a specific set of streams.

PDB (Program Database) defines the named streams within the MSF: the PDB info stream (versioning, GUID, age), the TPI stream (type info), the IPI stream (id info, separated in newer toolchains), the DBI stream (per-module info), the public symbol stream, the global symbol stream, the section contribution stream, and one Module Information Stream per compilation unit.

CodeView is the encoding of the type records and symbol records that live inside the TPI, IPI, and per-module streams. CodeView dates back to Microsoft's pre-Win32 debugger format. CodeView records describe types (structs, unions, enums, classes, function signatures), symbols (locals, params, public symbols, inlined frames), and line tables.

When MSVC or clang-cl compiles a `.c` / `.cpp` file with `/Zi`, the compiler emits CodeView records into the resulting `.obj` file (in the `.debug$S` and `.debug$T` sections). When the linker (`link.exe` or `lld-link`) runs, it merges all the per-object CodeView records, deduplicates types via a hash, and writes the result as a separate `.pdb` file referenced from the `.exe` via a PE debug directory entry.

The debugger (WinDbg, Visual Studio, lldb on Windows) opens the `.exe` or `.dll`, follows the debug directory to the PDB, opens the PDB, and uses its symbol streams to map PC to source and to enumerate locals.

## §3 Platform coverage (May 2026)

Producing PDB:

- Windows native: MSVC `cl /Zi` + `link /DEBUG`, clang-cl + lld-link. Fully supported.
- Linux/macOS cross: clang plus lld-link can produce PE binaries with PDBs from a Linux host. Rust on Windows targets uses this path when cross-compiling.
- Go: produces PE binaries with embedded DWARF, not PDB. WinDbg and Visual Studio cannot debug Go binaries natively; you use Delve.

Consuming PDB:

- Windows: WinDbg, Visual Studio, Visual Studio Code C++ extension, all native and feature-complete.
- Linux/macOS: lldb has limited PDB read support via the LLVM `PDB` library. gdb does not read PDB.
- llvm-pdbutil works on Linux for low-level dump/inspect but cannot do "show me locals at this PC" because the `pretty` subcommand depends on the Windows DIA SDK and is unavailable cross-platform.

## §4 Current status (May 2026)

LLVM 22 (released early 2026) and the in-development LLVM 23 continue incremental PDB work. The LLVM PDB writer has been considered feature-complete since around LLVM 7 (2018) per Reid Kleckner's talk. It is what powers clang-cl, lld-link, and Rust on Windows.

Microsoft's own toolchain (MSVC 17.13 in Visual Studio 2022 17.13, May 2025) continues to be the gold standard for PDB production. MSVC PDB output is bit-for-bit different from LLVM's but semantically equivalent for debuggers.

Production users:

- Every C/C++ developer on Windows produces PDBs.
- Rust on Windows produces PDB (LLVM-based).
- Chromium for Windows produces PDBs that get uploaded to Microsoft's public symbol server.
- Go does not produce PDB (it uses DWARF embedded in PE, which is rare but valid).

The "PDB on Linux" problem: tooling to read a PDB on Linux is incomplete. llvm-pdbutil's `dump` works but you cannot run WinDbg's "step through this Linux-built Windows binary and see locals" with lldb. People who need that ship the build to a Windows machine.

## §5 Engineering cost for Mochi

If Mochi targets Windows and we want Windows users to be able to debug Mochi-emitted binaries in WinDbg or Visual Studio, we must emit PDB. The cost:

- The format is non-trivial. LLVM's PDB writer is roughly 30,000 lines of C++. We do not want to reimplement that in Go.
- Two practical options:
  - Shell out to `lld-link` with our `.o` files containing CodeView records; lld-link writes the PDB. We must emit CodeView records in our `.o`s.
  - Skip PDB entirely and emit DWARF in the PE binary, like Go does. This works with gdb and lldb but not with WinDbg/Visual Studio.
- License: LLVM's code is Apache-2 + LLVM exception, so we could fork/port the writer. Microsoft's cvinfo.h is published under a license that effectively permits reuse for compatibility.
- Cross-host: lld-link runs everywhere. So if Mochi emits CodeView in `.o`s and shells out to lld-link, we can produce PDBs from a Linux build host.

For Mochi Phase 1, the recommendation is "emit DWARF in PE, like Go does". Most Mochi users on Windows will use VS Code / Delve-style tooling that prefers DWARF. We add PDB later if there is demand.

## §6 Mochi adaptation note

Mochi-on-Windows debug path:

1. Phase 1: emit DWARF inside our PE COFF object files (in `.debug_info`, `.debug_line`, etc. sections). lld-link or gnu-ld can preserve them.
2. Phase 1: NO PDB. Document that Mochi binaries on Windows are debuggable with gdb and lldb but not WinDbg.
3. Phase 2: add a CodeView emitter (`compiler3/emit/codeview`) that writes the `.debug$S` and `.debug$T` sections in our `.o` files. Then `lld-link /DEBUG` produces the PDB.
4. Phase 2: ship `lld-link` as part of the Mochi-Windows toolchain (or detect the user's `lld-link` install).
5. Relevant Mochi files: a new `compiler3/emit/pe` for the PE writer, paired with `compiler3/emit/codeview` for the records.

The Microsoft PDB GitHub repo (https://github.com/microsoft/microsoft-pdb) and LLVM's documentation are our primary references. Microsoft's repo is sparse but contains the canonical struct definitions.

## §7 Open questions for MEP-42

- Phase 1 default on Windows: DWARF only, no PDB? My recommendation: yes.
- Phase 2: do we implement PDB ourselves (large engineering bet) or vendor LLVM's writer via lld-link subprocess?
- Do we ever support symbol-server upload (the Microsoft public symbol server pattern)? Probably not in scope.
- Do we test debugger compatibility in CI? At least basic line-table coverage with lldb on Windows.

Sources:
- [LLVM PDB File Format docs](https://llvm.org/docs/PDB/index.html)
- [llvm-pdbutil command guide](https://llvm.org/docs/CommandGuide/llvm-pdbutil.html)
- [Reid Kleckner, "CodeView in LLVM" (2016 LLVM Dev Meeting)](https://llvm.org/devmtg/2016-11/Slides/Kleckner-CodeViewInLLVM.pdf)
- [Microsoft PDB GitHub repo](https://github.com/microsoft/microsoft-pdb)
- [Ubuntu manpage for llvm-pdbutil](https://manpages.ubuntu.com/manpages/jammy/man1/llvm-pdbutil-13.1.html)