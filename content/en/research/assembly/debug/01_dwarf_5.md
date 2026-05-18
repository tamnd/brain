---
title: "DWARF 5 (and the DWARF 6 draft)"
description: "The cross-platform binary debug format, its current standard, and where the next version is going."
tags: ["native-codegen", "debug"]
weight: 10
date: 2026-05-18T18:11:03+07:00
---

## §1 Provenance

- Standards body: DWARF Standards Committee (independent since 2007), https://dwarfstd.org/
- DWARF 5 spec (PDF): https://dwarfstd.org/doc/DWARF5.pdf
- DWARF 5 press release (Feb 2017): https://dwarfstd.org/dwarf5-press-release.html
- DWARF 6 working draft (May 2025 snapshot): https://snapshots.sourceware.org/dwarfstd/dwarf-spec/2025-05-05_22-29_1746484141/dwarf6-20250505-2228.pdf
- Errata: https://dwarfstd.org/dwarf5std.html
- Go reader: https://pkg.go.dev/debug/dwarf

The committee includes representatives from Google, Apple, Intel, NVIDIA, AMD, ARM, Sony, IBM, Red Hat, SUSE, and the LLVM and GCC projects.

## §2 Mechanism / function

DWARF is a binary format for describing a compiled program back to a debugger: the source files, the types, the variables, the line-number mapping, the call frame layout, the macro definitions, and (in DWARF 5) the unit hashes for split debug info.

A DWARF debug image is a collection of sections, each with a `.debug_*` name:

- `.debug_info` contains DIEs (Debugging Information Entries), the recursive tree of types, scopes, variables, functions. Each DIE has a tag (TAG_subprogram, TAG_variable, etc.) and attribute/value pairs.
- `.debug_abbrev` contains an abbreviation table that compresses the per-DIE attribute layout.
- `.debug_str` is a string pool referenced by DIEs.
- `.debug_str_offsets` is an indirection table (DWARF 5).
- `.debug_line` is a bytecode program that, when executed, emits the source-line-to-PC mapping.
- `.debug_line_str` is the line-program string pool (DWARF 5).
- `.debug_loclists` (replaces `.debug_loc`) and `.debug_rnglists` (replaces `.debug_ranges`) describe location lists and address-range lists in a more compact, relocation-free way.
- `.debug_addr` is an address pool (DWARF 5; supports split DWARF).
- `.debug_names` is the accelerated lookup table (DWARF 5; replaces `.debug_pubnames` and `.debug_pubtypes`).
- `.debug_macro` (DWARF 5; replaces `.debug_macinfo`) is the macro definition stream.
- `.debug_frame` describes call-frame unwind info.

A debugger reads `.debug_info`, finds the function containing the current PC, walks DIEs to find local variables, reads the line program to map PC to source location, and consults loclists to find where each variable lives (register, stack offset, computed expression).

DWARF 5's split-DWARF feature allows the heavy DIEs to live in a separate `.dwo` file or in a DWARF Package (`.dwp`), so the executable stays small. The `.gdb_index` (or DWARF 5 `.debug_names`) provides O(1) symbol lookup so debuggers do not parse the entire DIE tree.

## §3 Platform coverage (May 2026)

DWARF is the native debug format on:

- Linux (in ELF `.debug_*` sections of the executable, or as a separate `.debug` file via `eu-strip --strip-debug --reloc-debug-sections`).
- FreeBSD, NetBSD, OpenBSD, illumos, Solaris.
- macOS (Mach-O), but with a twist: DWARF lives in a sidecar `.dSYM` bundle (`MyApp.dSYM/Contents/Resources/DWARF/MyApp`) produced by `dsymutil` from the per-object DWARF in the relocatable `.o` files. The linker output binary typically contains only stubs.
- WebAssembly, via a vendor extension (Chrome's C/C++ DevTools Support extension reads DWARF embedded in `.wasm`; see `debug/03_source_maps_wasm.md`).
- iOS, Android, embedded Linux: all the same as their parent OS.

DWARF is NOT used on Windows for MSVC-built binaries (which use CodeView/PDB; see `debug/02_codeview_pdb.md`). Clang on Windows can emit DWARF in PE COFF sections, and GCC under MinGW does so by default, but debuggers other than gdb/lldb generally cannot read it.

## §4 Current status (May 2026)

DWARF 5 is the current published standard (since February 2017). It is fully supported by:

- GCC: default since GCC 11 (2021).
- Clang/LLVM: default since LLVM 16 (2023).
- gdb: full read support since gdb 10.
- lldb: read support throughout.
- Rust: emits DWARF 5 by default with `-Cdebuginfo=2`.
- Go: the Go runtime ships its own DWARF emitter inside `cmd/link` and produces DWARF 4 with selected DWARF 5 extensions.

DWARF 6 is a working draft (May 2025 snapshot is the most recent public PDF). It is incremental: most DWARF 2-and-up constructs are kept unchanged, with a few compactly superseded. Notable adds include separated language and language-version attributes (DW_AT_language_name + DW_AT_language_version, per issue 210419.1) and editorial cleanups. There is no firm publication date for DWARF 6 as of May 2026.

The committee remains active. LLVM's heterogeneous debugging extensions (https://llvm.org/docs/AMDGPUDwarfExtensionsForHeterogeneousDebugging.html) propose a separate path for GPU and accelerator debug info, designed to be backward compatible with DWARF 5.

## §5 Engineering cost for Mochi

DWARF is the right cross-platform debug format because we get gdb, lldb, perf, and most profilers for free. The cost:

- The encoding is intricate. We must implement an emitter for the abbreviation table, the DIE tree, the line program (a small bytecode), and the call-frame info.
- Go's standard library has `debug/dwarf` (read-only). The write side is in `cmd/link/internal/ld/dwarf.go`; it is BSD-licensed Go code we can study or partially adapt.
- macOS requires the dSYM workflow. We must teach `mochi build` to either run `dsymutil` (the system tool) or emit a dSYM ourselves.
- DWARF 5 is the right level to target. DWARF 4 is older but supported by more tools; DWARF 5's split-DWARF and `.debug_names` are nice-to-haves we can defer.
- The line program (PC-to-source mapping) is the only debug info Mochi STRICTLY needs for Phase 1. Type info, variable locations, and unwind tables are Phase 2.

Compile-time cost of emitting DWARF is real (10 to 30% of total compile time for unoptimized debug builds with full type info). Mochi's `--release` mode can omit DWARF entirely.

## §6 Mochi adaptation note

Mochi's path:

1. Phase 1: emit `.debug_line` only. This gives stack traces with source filenames and line numbers, which is all most users need.
2. Phase 2: add `.debug_info`, `.debug_abbrev`, `.debug_str` with type and variable info. Now gdb/lldb can show locals.
3. Phase 3: split DWARF (`.dwo` and `.dwp`) for large programs.
4. macOS: integrate with `dsymutil` (subprocess) to produce `.dSYM` bundles from our object-level DWARF.
5. Relevant Mochi files: a new `compiler3/emit/dwarf` package. The IR already in `compiler3/ir` carries source-location info we can map.
6. Mochi's `diagnostic` package already has source-location types; we reuse them as the DWARF line-program input.

We do NOT need cgo for DWARF emission. It is pure byte serialization. Go's `encoding/binary` and `bytes.Buffer` are sufficient.

## §7 Open questions for MEP-42

- Do we target DWARF 4 (maximum tool compat) or DWARF 5 (newer, smaller, slightly less compatible)? Recommendation: DWARF 5.
- Do we emit type information for Mochi types in Phase 1? Or only line numbers? Recommendation: lines only in Phase 1.
- How do we represent Mochi's generic and union types in DWARF? Probably as DW_TAG_typedef chains plus DW_TAG_variant_part (which DWARF supports for tagged unions).
- macOS dSYM: do we always emit it, or only on `--debug`? Probably always emit, since release builds can omit DWARF entirely if they prefer.

Sources:
- [DWARF Standards Committee home](https://dwarfstd.org/)
- [DWARF 5 spec PDF](https://dwarfstd.org/doc/DWARF5.pdf)
- [DWARF 5 press release](https://dwarfstd.org/dwarf5-press-release.html)
- [DWARF 6 working draft (May 2025)](https://snapshots.sourceware.org/dwarfstd/dwarf-spec/2025-05-05_22-29_1746484141/dwarf6-20250505-2228.pdf)
- [Go debug/dwarf package](https://pkg.go.dev/debug/dwarf)
- [LLVM DWARF heterogeneous debugging extensions](https://llvm.org/docs/AMDGPUDwarfExtensionsForHeterogeneousDebugging.html)