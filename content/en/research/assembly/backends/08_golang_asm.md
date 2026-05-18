---
title: "golang-asm as a Code-Generation Backend for Mochi"
description: "Go's internal assembler exported as a library, already used by Mochi's vm2jit."
tags: ["native-codegen", "backends"]
weight: 80
date: 2026-05-18T18:07:50+07:00
---

## §1 Provenance
- Repository: https://github.com/twitchyliquid64/golang-asm
- Package docs: https://pkg.go.dev/github.com/twitchyliquid64/golang-asm
- Latest tag: v0.15.1 (mirrors Go's cmd/internal/obj/* state at the corresponding upstream Go version).
- Upstream code lives in the official Go tree: https://go.googlesource.com/go/+/master/src/cmd/internal/obj/
- Originally extracted by twitchyliquid64 (Tom Hennen) so that Wazero and similar Go-hosted projects could JIT Wasm without cgo.
- License: BSD-3-Clause (Go's license).

## §2 Mechanism
The Go toolchain has its own assembler (Plan 9 lineage), used by `cmd/asm` and indirectly by `cmd/compile` to produce object code. golang-asm vendors a sanitized slice of `cmd/internal/obj` and `cmd/internal/objabi` and exposes a programmatic API: you build a linked list of `obj.Prog` (program steps), feed them to a `obj.Link` context configured for a specific arch (`arm64.Linkarm64`, `x86.Linkamd64`), and get back a byte buffer of encoded instructions plus relocations.

You operate at the **instruction** level: each `obj.Prog` is roughly one assembly instruction with operands (`obj.Addr`). No SSA, no register allocator, no instruction selection. The caller picks every register and every encoding.

For executable code you allocate `RWX` pages (via `mmap`/`mprotect` on POSIX, `VirtualAlloc` on Windows) and copy the bytes in. For object files you would need to convert relocations into ELF/Mach-O/COFF format yourself (see `13_emitting_object_files.md`).

## §3 Target coverage (May 2026)
Inherits Go's assembler backends:
- amd64 (Linux, macOS, Windows, BSDs): production, the most exercised target.
- arm64 (Linux, macOS, Windows): production.
- 386: production.
- arm: production.
- ppc64le, ppc64, mips64*, s390x, riscv64, loong64, wasm: all present in Go's tree, exposed by the fork.

For **RISC-V**: yes, the `objabi` package in golang-asm carries `R_CALLRISCV`, `R_RISCV_PCREL_ITYPE`, `R_RISCV_PCREL_STYPE` relocations (per https://pkg.go.dev/github.com/twitchyliquid64/golang-asm/objabi). The riscv64 backend exists; how exercised it is by golang-asm consumers is unclear.

For **Wasm**: Go's wasm backend exists but the assembler is unusual; not a practical golang-asm target for JIT.

Object formats: golang-asm itself produces raw bytes plus a relocation list. Writing ELF/Mach-O is the caller's job.

## §4 Production / language adoption status (May 2026)
- **Wazero** (https://github.com/tetratelabs/wazero): used golang-asm for early JIT experiments; now has its own engine (Compiler engine), with golang-asm-derived ideas.
- **Mochi vm2jit**: per the repo (`/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/`), Mochi's existing JIT path uses this fork via `lower_amd64.go` and `lower_arm64.go`.
- A handful of other Go-hosted JITs and emulators use it for ergonomic in-process assembly.

Active maintainership is sporadic. The fork tracks upstream Go ABI changes only when contributors push updates (commits happen but slowly). The risk is that upstream Go restructures `cmd/internal/obj` and breaks the fork.

License: BSD-3-Clause (Go's license).

## §5 Engineering cost for Mochi
- **Binary footprint**: ~5-10 MB statically linked into the Mochi binary; Go vendoring handles it cleanly.
- **Build complexity**: **Pure Go, no cgo, no external tools**. This is the unique selling point for a Go-hosted compiler.
- **License**: BSD-3-Clause, compatible with anything.
- **Cross-compilation**: Go's `GOOS`/`GOARCH` matrix gives us free cross-compilation of the Mochi binary, but each target's assembler module must be imported and exercised independently.
- **Debugging**: minimal. No DWARF emission. We can emit our own debug info if we want.
- **Runtime startup**: zero. Per-function compile is microseconds.

## §6 Mochi adaptation note
This is the backend Mochi **already uses**. The relevant files are:
- `/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/arch.go` (target abstraction)
- `/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/arch_amd64.go`, `arch_arm64.go`, `arch_other.go`
- `/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/lower_amd64.go`, `lower_arm64.go` (per-arch lowering, currently stub on non-amd64/arm64)
- `/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/page_*.go` (RWX page allocator per OS+arch)
- `/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/compile.go`, `cache.go`

For MEP-42 the question is **whether to keep this in Phase 1 or replace it**. The "keep" case: it is the only backend on the shortlist that is pure Go, ships in `go build`, and is already working. The "replace" case: every other backend listed (QBE, MIR, Cranelift, copy-and-patch) gives us better generated code with less per-architecture hand-coding.

The realistic Phase 1 plan: **keep golang-asm for JIT, layer a higher-quality AOT backend on top** for `mochi build` to produce standalone binaries.

## §7 Open questions for MEP-42
- **Per-arch hand-coding scales poorly**: Mochi currently has stubs for non-amd64/arm64 hosts in `lower_amd64_stub.go` and `arch_other.go`. Adding RISC-V means writing the RISC-V lowering by hand. That cost grows linearly with the op set.
- **Object-file emission**: golang-asm gives us bytes + relocations; turning those into a linkable `.o` requires writing an ELF/Mach-O/COFF writer (see `13_emitting_object_files.md`). Most projects shortcut by using runtime JIT only.
- **Upstream Go fragility**: `cmd/internal/obj` is officially internal. Every Go release risks breaking the fork. Mitigation: pin to a tested Go version per Mochi release.
- **Should Phase 1 be "golang-asm JIT only, no native binaries"?** That keeps Mochi pure-Go and defers the AOT story to Phase 2. Simplest path forward.
- **Code quality**: roughly equivalent to a one-pass naive emitter (no peepholes, no register allocator). For interpreter-tier JIT this is fine; for `mochi build` it is well below Cranelift, QBE, or LLVM.