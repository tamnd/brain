---
title: "Targets Summary"
description: "Single-page roll-up of every (target ISA x OS) combination Mochi MEP-42 could ship, with status and engineering complexity recommendations."
tags: ["native-codegen", "targets"]
weight: 0
date: 2026-05-18T18:12:07+07:00
---

## §1 Status legend

- **must-have**: Phase 1 ships this combination. Mochi without it is not a credible product.
- **should-have**: Phase 1 or early Phase 2. A serious gap if missing.
- **could-have**: Phase 2 or later. Valuable to advanced users, not blocking.
- **out-of-scope**: not planned for any phase of MEP-42 (might be MEP-43+ or never).

Engineering complexity is a rough 1 to 5 ordinal: 1 = a week or two, 5 = multi-month, multi-engineer effort.

## §2 Matrix

| Target ISA | OS | Format | ABI File | Format File | Status | Complexity | Notes |
|---|---|---|---|---|---|---|---|
| x86_64 | Linux | ELF | 01_x86_64_sysv | 01_elf | must-have | 2 | Cheapest first target. SysV + ELF + static link. |
| x86_64 | macOS | Mach-O | 01_x86_64_sysv | 02_mach_o | should-have | 3 | Universal 2 with arm64 makes this a freebie if arm64 macOS ships. |
| x86_64 | Windows | PE/COFF | 02_x86_64_windows | 03_pe_coff | should-have | 4 | Different ABI; .pdata/.xdata mandatory. |
| x86_64 | FreeBSD | ELF | 01_x86_64_sysv | 01_elf | could-have | 1 | Same as Linux modulo .note.ABI-tag. |
| x86_64 | OpenBSD | ELF | 01_x86_64_sysv | 01_elf | could-have | 1 | Same as FreeBSD; mandatory BTI on capable cores. |
| x86_64 | illumos/Solaris | ELF | 01_x86_64_sysv | 01_elf | out-of-scope | 1 | No reason to skip the work; just no current demand. |
| aarch64 | macOS (Apple Silicon) | Mach-O | 03_aarch64_aapcs | 02_mach_o | must-have | 3 | Apple variadic delta, ad-hoc signing mandatory. |
| aarch64 | Linux | ELF | 03_aarch64_aapcs | 01_elf | must-have | 2 | Pi, Ampere, Graviton, every cloud now has aarch64. |
| aarch64 | iOS / visionOS | Mach-O | 03_aarch64_aapcs | 02_mach_o | out-of-scope | 5 | Provisioning profiles, MH_BUNDLE, App Store machinery. |
| aarch64 | Android | ELF | 03_aarch64_aapcs | 01_elf | could-have | 3 | Bionic loader is stricter; NDK conventions. |
| aarch64 | FreeBSD/OpenBSD | ELF | 03_aarch64_aapcs | 01_elf | could-have | 1 | Pure AAPCS64; trivial increment over Linux. |
| aarch64 | Windows | PE/COFF | 04_aarch64_windows | 03_pe_coff | could-have | 4 | Snapdragon X / X2 Elite; ARM64 xdata is its own bytecode. |
| riscv64 | Linux | ELF | 05_riscv64 | 01_elf | could-have | 3 | RVA22/RVA23 hardware exists but user base is small. |
| riscv64 | FreeBSD | ELF | 05_riscv64 | 01_elf | out-of-scope | 2 | Niche. |
| wasm32 (Wasm 3.0 + GC) | browser | .wasm | 06_wasm | 04_wasm_module | must-have | 2 | Cheapest backend; massive distribution reach. |
| wasm32 (Wasm 3.0 + GC) | WASI Preview 2 runtime | .wasm | 06_wasm | 04_wasm_module | must-have | 2 | Same emitter, different host imports. |
| wasm64 | runtime | .wasm | 06_wasm | 04_wasm_module | could-have | 1 | Memory64; rarely needed but cheap to support. |
| ppc64le | Linux | ELF | 07_other_isas | 01_elf | out-of-scope | 4 | POWER10 winding down; very small user base. |
| s390x | Linux | ELF | 07_other_isas | 01_elf | out-of-scope | 5 | Big-endian, mainframe-only; no demand. |
| loongarch64 | Linux | ELF | 07_other_isas | 01_elf | out-of-scope | 4 | Chinese market only; ABI well-spec'd but no global demand. |
| mips* | * | ELF | 07_other_isas | 01_elf | out-of-scope | 3 | Sunset ISA; MIPS Inc pivoted to RISC-V in 2021. |
| Apple GPU | macOS | Metal AIR | 07_other_isas | n/a | out-of-scope | 5 | Separate compute pipeline; future MEP territory. |
| polyglot APE | all six | APE | n/a (post-link) | 05_ape_cosmopolitan | could-have | 3 | Distribution feature, Phase 2 bundler tool. |

## §3 Recommended Phase 1 targets

Five host targets, all "must-have" in the table above:

1. **x86_64 Linux (ELF, SysV)**: cheapest, largest test surface, every CI runner has it.
2. **aarch64 Linux (ELF, AAPCS64)**: covers Pi, Ampere, AWS Graviton, every modern cloud ARM instance.
3. **aarch64 macOS (Mach-O, Apple ABI)**: required for Apple Silicon developer adoption.
4. **x86_64 macOS (Mach-O, SysV)**: comes nearly for free if Mochi ships Universal 2 binaries.
5. **wasm32 with WasmGC**: single backend covering browsers and every standalone Wasm runtime (Wasmtime, WAMR, Wasmer, WasmEdge, Spin). Highest leverage per engineering hour.

Estimated Phase 1 effort: ~3-4 engineer-months for first working backends across all five targets, assuming Mochi reuses Go's `debug/elf`, `debug/macho`, and writes its own Wasm emitter from scratch.

## §4 Recommended Phase 2 targets

1. **x86_64 Windows (PE/COFF, MS ABI)**: required for desktop Windows adoption. Estimated 1-2 engineer-months due to .pdata/.xdata and IAT machinery.
2. **aarch64 Windows (PE/COFF, MS ARM64 ABI)**: Snapdragon X / X2 Elite laptops, ARM64 dev kits. ~1 engineer-month given the AAPCS64 + PE backends both exist by then.
3. **APE bundler**: post-link tool that combines per-OS binaries into a single polyglot APE for distribution. ~2 weeks if cosmocc is the dependency.
4. **riscv64 Linux (ELF, RV64GC LP64D)**: RVA22/RVA23 hardware is real. ~1 engineer-month.

## §5 Explicitly out-of-scope for MEP-42

- iOS / iPadOS / visionOS / tvOS / watchOS: requires Apple developer credentials, provisioning profiles, App Store review. Defer to a dedicated MEP for mobile.
- ppc64le, s390x, loongarch64: real but small user bases. Add on demand.
- MIPS: sunset.
- GPU compute (Metal AIR, CUDA PTX, ROCm, SPIR-V, WGSL): a separate MEP for SIMT codegen.
- macOS x86_64 once Apple removes Rosetta: handle when it happens (likely 2027+).
- ARM64EC: deferred until Mochi has a story for x64 plugin interop on Windows.

## §6 Critical decisions MEP-42 must make

1. Which native object writers does Mochi vendor (write itself) vs invoke (shell out to lld, ld, link)? Recommend vendor minimal ELF + Mach-O + PE writers, invoke system linker.
2. Static vs dynamic linking default? Recommend static for Phase 1 (simpler, fewer runtime dependencies); dynamic in Phase 2.
3. Linker choice: bundle lld, depend on system linker, or both? Recommend system linker with lld as fallback when missing.
4. Debug info: DWARF on Linux/Mach-O/Wasm; CodeView (Phase 1) then PDB (Phase 2) on Windows.
5. Cross-compilation: officially supported in Phase 1 for the five must-have targets from any host? Recommend yes; Go's standard cross-compile facilities make this cheap.
