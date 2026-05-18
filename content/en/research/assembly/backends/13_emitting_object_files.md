---
title: "Emitting Object Files Directly for Mochi"
description: "What it takes to write a valid ELF/Mach-O/COFF from a backend's raw bytes."
tags: ["native-codegen", "backends"]
weight: 130
date: 2026-05-18T18:13:12+07:00
---

## §1 Provenance
- **gimli** (DWARF read/write, Rust): https://github.com/gimli-rs/gimli, https://crates.io/crates/gimli, current 0.31.1.
- **object** (ELF/Mach-O/COFF read/write, Rust): https://github.com/gimli-rs/object.
- **ddbug** (DWARF visualization): https://github.com/gimli-rs/ddbug.
- **Go's debug/elf, debug/macho, debug/pe**: https://pkg.go.dev/debug/elf, https://pkg.go.dev/debug/macho, https://pkg.go.dev/debug/pe (read-only in standard library).
- **Go's debug/dwarf**: https://pkg.go.dev/debug/dwarf (read-only).
- **golang-asm objabi relocations**: https://pkg.go.dev/github.com/twitchyliquid64/golang-asm@v0.15.1/objabi
- **llvm-objdump**, **llvm-readelf**, **llvm-objcopy**: standard LLVM utilities for round-trip inspection.
- **System V ABI ELF spec**: https://refspecs.linuxfoundation.org/elf/elf.pdf
- **Mach-O reference (Apple)**: https://github.com/aidansteele/osx-abi-macho-file-format-reference
- **PE/COFF spec (Microsoft)**: https://learn.microsoft.com/en-us/windows/win32/debug/pe-format

## §2 Mechanism
A native backend (golang-asm, MIR, copy-and-patch, etc.) produces:
1. A byte buffer containing machine code (`.text`).
2. Optional `.data`, `.rodata`, `.bss` byte buffers.
3. A list of **symbols** (function entry points, globals).
4. A list of **relocations** (places in the buffers that reference symbols by name and need a final address patched in).

Turning these into a linkable object file requires:
- Writing the container's headers (ELF Ehdr+Phdr+Shdr, Mach-O mach_header+load_commands, COFF header).
- Building a string table (`.strtab`, `.shstrtab`).
- Building a symbol table (`.symtab`, COFF symbol table, Mach-O nlist).
- Encoding each relocation in the container's specific format (ELF Rela entries, Mach-O scattered relocations, COFF relocation table).
- Encoding section table entries, with correct alignment, file offsets, virtual addresses.
- For debug info, emitting `.debug_info`, `.debug_abbrev`, `.debug_line`, `.debug_str`, `.debug_ranges` (DWARF 5: `.debug_line_str`, `.debug_loclists`, `.debug_rnglists`).

This is **mechanically straightforward but voluminous code**. A minimal ELF writer fits in ~500 lines; a production-quality writer with all sections, DWARF 5, and BTF for eBPF is ~10k lines.

## §3 Target coverage (May 2026)
We are choosing among formats, not architectures:
- **ELF**: Linux, FreeBSD, OpenBSD, NetBSD, illumos, Solaris.
- **Mach-O**: macOS, iOS, tvOS, watchOS, visionOS.
- **PE/COFF**: Windows.
- **Wasm**: Wasmtime `.cwasm` and standard `.wasm` module format.

For each, you must support every relocation type your backend emits. For x86_64 SysV ELF that is roughly 30 reloc types; for AArch64 Mach-O it is ~20; for RISC-V it is ~50 (RISC-V has many small reloc forms because of its instruction encoding).

## §4 Production / language adoption status (May 2026)
- **gimli + object**: the de facto Rust solution; used by Cranelift's `cranelift-object` crate, by Bjorn3's cg_clif, by Wasmtime for `.cwasm`, by `wasm-tools`, by `bpf-linker`, by Inko, by Roc.
- **Go's debug/* family**: read-only. There is no first-class object writer in the standard library. The Go toolchain has its own internal writers in `cmd/link/internal/{ld,elf,macho,pe,wasm}`, not exposed.
- **mholt/archiver** and various community ELF builders exist but none are production-grade.
- **C++ LLVM API**: `llvm::MCObjectWriter` is the canonical reference and the most complete writer in the wild.
- **Zig's std.elf, std.macho, std.coff**: read-write, used by Zig's self-hosted linker work (https://ziglang.org/devlog/2025/), increasingly mature.

License situation: gimli/object are MIT/Apache, debug/* is BSD-3-Clause, LLVM MCO is Apache 2.0 LLVM-Exception.

## §5 Engineering cost for Mochi
Two integration paths for a Go-hosted Mochi:

**Path A: write our own object writer in Go.**
- Pros: pure Go, no cgo, no Rust toolchain. Full control over what we emit.
- Cons: real work. A minimum-viable Mochi ELF+Mach-O+COFF writer with DWARF line tables is ~3000-5000 lines of Go. Add another ~2000 for full DWARF type info. Multiply per format. Initial implementation can crib heavily from Go's internal `cmd/link` (BSD-licensed, public source).
- Existing Mochi files this would join: a new `compiler3/object/` package; would consume the bytes produced by `runtime/jit/vm2jit/` or a new `runtime/jit/copyandpatch/`.

**Path B: shell out to system tools.**
- Emit assembly text (`.s`), invoke `as` and `ld`.
- Pros: zero new code. Cross-platform via the system toolchain.
- Cons: requires `binutils` or `cctools` or MSVC's `ml64.exe` installed. We give up control over debug info quality and exact section layout.

**Path C: use cranelift-object via Rust subprocess or staticlib.**
- Pros: production-grade output, well-tested across architectures.
- Cons: cgo or subprocess; same friction as adopting Cranelift directly.

For Phase 1, **Path B (shell out)** is almost certainly correct. We pair with QBE (which already emits assembly) or with C-as-target (which emits C). The system toolchain handles the object file.

## §6 Mochi adaptation note
The bytes-and-relocations interface mirrors what `runtime/jit/vm2jit/lower_*.go` already produces (golang-asm gives us a `[]byte` plus a `[]obj.Reloc`). Today those bytes go straight into RWX memory via the page allocator (`/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/page_*.go`). For AOT we would instead route them into a new `compiler3/object/` package that writes ELF or Mach-O.

The minimum useful step for Phase 1: add a `compiler3/object/elf.go` that writes `.text + .symtab + .strtab + .rela.text`, no debug info. That is ~300 lines and unlocks Linux x86_64+arm64+riscv64 binaries. Mach-O and PE follow the same template.

For DWARF, the cheapest route is to emit minimal `.debug_line` entries (one source map per Mochi instruction) and skip `.debug_info` entirely. `gdb` and `lldb` will give us file:line info on crashes without type-aware variable inspection. The Go `debug/dwarf` package can help us validate our output by reading it back.

## §7 Open questions for MEP-42
- **Pure Go object writer vs system linker?** The system linker route is dramatically less code and arguably more correct. The pure-Go route preserves Mochi's "one binary, no deps" identity.
- **DWARF effort budget**: full DWARF 5 with type info is months of work; minimal `.debug_line` is days. Where do we land?
- **Static vs dynamic linking**: Mochi binaries embedding the vm3 runtime as a static library is simplest. Dynamic linking against a `libmochi.so` is nicer for tooling but is a separate problem.
- **macOS code signing**: Mach-O on Apple Silicon requires every binary to be code-signed (or at least ad-hoc signed). Our object writer must either ad-hoc sign or hand off to `codesign`.
- **Windows PE peculiarities**: PE requires correct subsystem, characteristics, base-of-data/code fields, and a delay-load import table for any DLL imports. Less forgiving than ELF.
- **Recommended sequencing**: Phase 1 shells out to `cc` (Path B). Phase 2 considers Path A if the dependency reduction is worth the code investment.