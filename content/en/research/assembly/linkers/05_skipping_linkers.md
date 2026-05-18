---
title: "Skipping the Linker Entirely"
description: "Emitting a self-contained executable from the compiler, no external linker required."
tags: ["native-codegen", "linkers"]
weight: 50
date: 2026-05-18T18:05:41+07:00
---

## §1 Provenance

- Go internal linker: https://github.com/golang/go/tree/master/src/cmd/link
- Zig self-hosted backends: https://ziglang.org/devlog/2025/
- Zig linker source layout: https://github.com/ziglang/zig/tree/master/src/link
- LLD as a library API: `lld::elf::link()`, `lld::macho::link()`, `lld::coff::link()`, `lld::wasm::link()` at https://github.com/llvm/llvm-project/tree/main/lld/include/lld/Common
- "Mostly statically linked" Go binary mechanism (debug/elf, debug/macho, debug/pe writers in the standard library): https://pkg.go.dev/debug/elf

Authors are language toolchain authors: the Go team (Russ Cox, Cherry Mui, Than McIntosh on linker), the Zig team (Andrew Kelley, Jakub Konka), and the Wild linker maintainer.

## §2 Mechanism / function

A linker is a function from "set of object files" to "executable image". If your compiler is the only thing producing those object files and you control the calling conventions and the runtime, you can collapse compiler-plus-linker into one program that emits the final image directly.

The basic moves:

1. Compile to an in-memory IR (Mochi already does this in `compiler3/ir`).
2. Lay out sections and assign virtual addresses up front, using a fixed memory map (text at 0x400000 on x86-64 Linux is the historical default for ET_EXEC).
3. Emit machine code with relocations resolved against the chosen layout. Because the compiler picked the layout, there are no unknown symbol addresses.
4. Write an ELF (or Mach-O, or PE) header, segment table, and section table directly to disk.
5. Done: the executable runs.

Go has done this since 1.0. Its internal linker is not really a linker in the bfd/lld sense, since it consumes Go-specific object files produced by `cmd/compile`, not general ELF relocatables. It writes ELF, Mach-O, PE, or Plan 9 a.out directly.

Zig's self-hosted backends do the same. When `zig build-exe -fno-llvm` is used on x86_64-linux, Zig's self-hosted x86 backend emits machine code straight into an in-memory ELF buffer and writes it out. No external linker is involved.

The library-form of LLD (`lld::elf::link()` and friends) is a middle road: still a real linker, but invoked in-process so there is no `fork`/`exec` overhead.

## §3 Platform coverage (May 2026)

Go's internal linker covers: linux/{amd64, arm64, arm, 386, mips, mips64, ppc64, riscv64, s390x, loong64}, darwin/{amd64, arm64}, windows/{amd64, arm64, 386}, freebsd, netbsd, openbsd, dragonfly, solaris/illumos, plan9, aix, wasip1, js/wasm. Comprehensive.

Zig's self-hosted linker as of May 2026:

- ELF: x86_64, aarch64, mostly riscv64. Default on Linux for the self-hosted x86 backend (https://ziglang.org/devlog/2025/).
- Mach-O: x86_64 and arm64. Maintained by Jakub Konka. Usable.
- COFF: in progress. Not yet the default on Windows; LLD is still used.
- WebAssembly: works.

LLD-as-library is available for all four formats. Mochi could link against it via cgo, but the maintenance cost and C++ ABI surface are high.

## §4 Current status (May 2026)

Go's internal linker is mature and the default for every `go build`. It is the second-most-used linker in the world after the system ld on Linux, simply because of Go's deployment volume.

Zig 0.14.0 (early 2025) made the self-hosted x86 backend the default in Debug mode on Linux x86_64, which implicitly relies on the self-hosted ELF writer. Zig 0.15.x continued the trend. As of mid 2026, COFF is still the gap; Windows builds still go through LLD.

Wild (https://github.com/davidlattimore/wild) is a 2024-2025 project to build an even-faster Rust-written ELF linker. It is mentioned in MaskRay's benchmarks as ahead of LLD on certain workloads. It is "linker as a binary" not "linker as a library", so it is closer to mold's slot than to Go's pattern.

LLD-as-library is used by clangd and some Rust IDE tooling but rarely by other compilers as a primary path.

## §5 Engineering cost for Mochi

Pros of skipping the linker:

- Zero external dependencies. The Mochi binary becomes a complete toolchain.
- No `fork`/`exec` cost. For small Mochi programs this is a real percentage of compile time.
- Tight error messages. The linker step never produces "undefined reference to `foo`" style errors that no longer relate to Mochi source.
- Easy cross-compile. We are not bound to the host linker's target list.

Cons:

- We must write and maintain an object/executable writer for each format (ELF, Mach-O, PE). That is roughly 5,000 to 10,000 lines of careful, well-tested code per format.
- We do not get to link against arbitrary C libraries (libc, OpenSSL). We can only link our own emitted code.
- We do not get to use system-installed shared libraries.
- DWARF emission must be ours.
- No LTO across our code and C code.

Go can do this because Go programs do not link to system libraries by default (they use the Go runtime's own syscall layer, see `runtime/05_no_libc_freestanding.md`). Mochi is in the same position: vm3 is Go-hosted, and the Mochi runtime is Mochi-defined. If we keep the same boundary, we can keep the same trick.

The pragmatic compromise: emit relocatable `.o` files for the "I need to link against C" case, but ALSO have a "freestanding" mode that writes a complete executable in one shot.

## §6 Mochi adaptation note

Mochi can do this in stages:

1. Phase 1: emit `.o` (ELF / Mach-O / COFF) via `compiler3/emit/obj`, then shell out to a real linker. This is the safe default.
2. Phase 2: add `compiler3/emit/image`, a self-contained executable writer for `freestanding` mode. The implementation mirrors Go's `cmd/link` minus the input-object-parsing part: we already have our own IR, we just need the file-format encoder.
3. ELF is the easiest to write first (well-documented, tolerant tooling). Mach-O is next (chained fixups, code-signature placeholder). PE is hardest (PDB cooperation).
4. The relevant Mochi files are `compiler3/emit/` (we add `image_elf.go`, `image_macho.go`, `image_pe.go`) and `runtime/vm3/program.go` (which defines our bytecode/IR boundary).

Go's `debug/elf`, `debug/macho`, and `debug/pe` packages are read-only but provide the structural blueprints we can mirror for our writers. They are part of the standard library and we already depend on them indirectly.

## §7 Open questions for MEP-42

- Do we commit to writing our own image writer in Phase 2, or do we just embed LLD's library form?
- If we go freestanding, do we abandon ever linking against `.a` archives? Or do we ship a minimal archive parser?
- How much of Go's `cmd/link` can we directly adapt under its BSD-style license? (License is compatible.)
- Does Mochi want a "build-once run-anywhere" Cosmopolitan-style binary as a separate target? See `runtime/03_cosmopolitan_libc.md`.

Sources:
- [Go cmd/link source](https://github.com/golang/go/tree/master/src/cmd/link)
- [Zig 2025 devlog: self-hosted x86 default in Debug](https://ziglang.org/devlog/2025/)
- [Zig 0.12.0 release notes](https://ziglang.org/download/0.12.0/release-notes.html)
- [Zig: COFF freestanding output issue 3182](https://github.com/ziglang/zig/issues/3182)
- [LLD common library interface](https://github.com/llvm/llvm-project/tree/main/lld/include/lld/Common)
- [Go debug/elf package](https://pkg.go.dev/debug/elf)