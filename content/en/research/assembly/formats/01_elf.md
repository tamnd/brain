---
title: "ELF (Executable and Linkable Format)"
description: "The universal Unix object/executable format: Linux, *BSD, Solaris, Haiku, embedded."
tags: ["native-codegen", "formats"]
weight: 10
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- System V Application Binary Interface Generic ABI (the gABI): https://www.sco.com/developers/gabi/latest/contents.html.
- Linux man page elf(5): https://www.man7.org/linux/man-pages/man5/elf.5.html.
- Original ELF specification (Tool Interface Standard, TIS Committee, 1995): https://refspecs.linuxfoundation.org/elf/elf.pdf.
- DWARF Debugging Information Format v5: https://dwarfstd.org/doc/DWARF5.pdf.
- GNU extensions reference: binutils source plus https://sourceware.org/binutils/docs/binutils/.
- GNU IFUNC documentation: https://sourceware.org/glibc/wiki/GNU_IFUNC.
- Go's debug/elf package: https://pkg.go.dev/debug/elf.

## §2 Mechanism / specification

ELF has three flavors of file: relocatable object (.o), executable, and shared object (.so / dynamic library). All three share an `ElfNN_Ehdr` at offset 0.

The 64-bit header (`Elf64_Ehdr`, 64 bytes):

- e_ident: 16-byte magic + class (32/64) + endianness + version + OS/ABI + ABI version + padding.
- e_type: relocatable, executable, shared object, core dump.
- e_machine: EM_X86_64 (62), EM_AARCH64 (183), EM_RISCV (243), EM_LOONGARCH (258), etc.
- e_entry: virtual address of the entry point.
- e_phoff, e_phnum, e_phentsize: program header table.
- e_shoff, e_shnum, e_shentsize: section header table.
- e_shstrndx: section name string table index.

Program headers (PT_*) describe segments for the loader. Key types: PT_LOAD (a segment to be mapped), PT_INTERP (dynamic linker path, typically `/lib64/ld-linux-x86-64.so.2`), PT_DYNAMIC (dynamic linking metadata), PT_NOTE (a region of notes; build-id, ABI tag, GNU stack property, gnu.property), PT_TLS (thread-local storage), PT_GNU_STACK (NX stack flag), PT_GNU_RELRO (read-only-after-relocation hint), PT_PHDR (the program header table itself).

Section headers (SHT_*) describe link-time structure. Key types: SHT_PROGBITS (code or data), SHT_SYMTAB, SHT_DYNSYM, SHT_STRTAB, SHT_RELA / SHT_REL (relocations), SHT_HASH / SHT_GNU_HASH (symbol lookup tables), SHT_NOTE, SHT_NOBITS (BSS).

Dynamic linking uses the PT_DYNAMIC segment, which contains DT_NEEDED entries (libraries to load), DT_RPATH/DT_RUNPATH (search paths), DT_SYMTAB, DT_STRTAB, DT_HASH/DT_GNU_HASH, DT_PLTGOT (Global Offset Table pointer), DT_JMPREL (PLT relocations), DT_INIT/DT_FINI (constructor/destructor), DT_INIT_ARRAY/DT_FINI_ARRAY.

GOT (Global Offset Table) and PLT (Procedure Linkage Table) implement lazy and immediate binding of external symbols.

### Key GNU/Linux extensions

- IFUNC (STT_GNU_IFUNC): a symbol whose actual implementation is selected at load time by a resolver function. Used for CPU dispatch in libc (memcpy variants for SSE2 vs AVX2 vs AVX-512). Triggered by `__attribute__((ifunc("resolver")))`.
- `.note.gnu.build-id`: a 160-bit (SHA1 default) or MD5 fingerprint of the binary, embedded by `ld --build-id`. Allows debug info matching across stripped binaries.
- `.note.gnu.property`: machine-specific properties bits. On x86_64 it carries CET feature bits (IBT, SHSTK). On AArch64 it carries BTI/PAC enablement flags. The dynamic loader uses these to decide page protections.
- `PT_GNU_STACK`: the p_flags bits describe whether the stack should be executable. Modern toolchains default to non-executable; the loader maps the stack with PROT_READ|PROT_WRITE (no EXEC).
- `PT_GNU_RELRO`: after relocations, the loader may remap the covered region read-only, hardening the GOT.

## §3 Platform coverage (May 2026)

ELF is used by:

- Linux (every distro, every architecture).
- FreeBSD, OpenBSD, NetBSD, DragonFly BSD.
- illumos / OpenIndiana / OmniOS, original Solaris.
- Haiku.
- Most embedded RTOSes that need ELF-loadable modules (Zephyr, NuttX, FreeRTOS with secondary loaders).
- Android (a constrained subset; bionic loader is stricter than glibc's).
- The Hurd, Plan 9 ports (some), Redox.

Per-OS quirks: Linux uses the LSB (Linux Standard Base) extensions plus the GNU extensions; FreeBSD uses .note.ABI-tag to identify itself; OpenBSD adds PT_OPENBSD_RANDOMIZE for stack canaries; Android imposes tighter restrictions on text relocations and DT_TEXTREL.

## §4 Current status (May 2026)

- ELF spec itself is stable (last major changes were in the 1990s).
- Active development happens in GNU extensions and per-arch psABIs.
- Compressed debug info (SHF_COMPRESSED) is widely deployed.
- Section grouping (SHT_GROUP) enables COMDAT-style template instantiation deduplication.
- DT_RELR (relative-relocation compression, ratified 2023) significantly shrinks PIE binaries; adopted by glibc 2.36+, musl 1.2.4+, Android API 35+.
- LLD, mold, and wild compete with GNU ld for performance; mold is the speed leader (~2x lld, ~10x ld.bfd on large links as of 2026).
- IFUNC support is universal.

## §5 Engineering cost for Mochi

ELF is the cheapest format to emit. Go has `debug/elf` for reading and the cmd/link source has battle-tested writers Mochi can crib from.

Must-have: write a relocatable .o (Elf64_Ehdr, .text, .rodata, .data, .bss, .symtab, .strtab, .rela.text). Pass to system linker.

Should-have: write a directly-loadable static executable (PT_LOAD segments, PT_GNU_STACK, .note.gnu.build-id). Skip dynamic linking in Phase 1; static linking against libc-free Mochi runtime is simpler.

Nice-to-have: dynamic loading (PT_INTERP, PT_DYNAMIC, GOT/PLT, DT_NEEDED), IFUNC, PT_GNU_RELRO, compressed debug info, DT_RELR.

Estimated effort: ~1 week for static executable emission, ~1 month for full dynamic linking support, plus per-arch relocation handling.

## §6 Mochi adaptation note

compiler3 would gain an `objfile/elf` package alongside the existing typed-IR pipeline. The arena allocator from runtime/vm3 needs no ELF awareness; it just calls mmap at startup. The runtime entry point is a small `_start` stub in the target backend that sets up the arena, runs Mochi's main, and exits via the syscall ABI for the target OS.

For dynamic libraries (.so), the runtime/vm3 arena would need to be allocated per-process, not per-module. This is the standard problem of multiple instances of an embedded VM.

## §7 Open questions for MEP-42

1. Static vs dynamic in Phase 1? Recommend static-only for Phase 1. Simpler, no GOT/PLT, no .interp dependency, fewer moving parts. Dynamic in Phase 2 for shared-library support.
2. Strip debug info by default? Recommend emit unstripped + .build-id, ship separate `mochi-stripped` artifact.
3. PT_GNU_STACK: always non-exec. PT_GNU_RELRO: always on. .note.gnu.property: emit CET bits on x86_64, BTI bits on aarch64. Recommend default-on for all hardening notes.
4. Linker: invoke system ld/lld/mold, or vendor mold source? Recommend system linker for Phase 1, in-process linker for Phase 2.
