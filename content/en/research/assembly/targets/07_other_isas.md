---
title: "Other ISAs: PowerPC, MIPS, LoongArch, s390x, Apple GPU/Metal"
description: "Survey of niche or specialized architectures that MEP-42 should be aware of but probably defer."
tags: ["native-codegen", "targets"]
weight: 70
date: 2026-05-18T18:06:46+07:00
---

## §1 Provenance

- Power ISA v3.1 (and later) specification: https://openpowerfoundation.org/specifications/isa/.
- 64-bit ELFv2 ABI Specification (ppc64le): https://openpowerfoundation.org/specifications/64bitelfv2abi/.
- MIPS Architecture for Programmers documentation: https://www.mips.com/products/architectures/ (Imagination's MIPS pages; the canonical spec PDFs).
- LoongArch ELF psABI: https://github.com/loongson/la-abi-specs.
- LoongArch architecture reference: https://loongson.github.io/LoongArch-Documentation/.
- z/Architecture Principles of Operation (IBM): https://www.ibm.com/support/pages/zarchitecture-principles-operation-spreadsheet (search for SA22-7832).
- ELF ABI for s390x: https://github.com/IBM/s390x-abi.
- Metal Shading Language specification (Apple): https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf.

## §2 PowerPC / POWER

POWER10 launched in 2021 and IBM is winding down sales as of early 2026: most Power10 models exit marketing by July 31, 2026 globally (July 30, 2027 in China and South Korea). Power11 takes over.

Two ABIs matter: ELFv2 little-endian (ppc64le; what every modern Linux distro uses since RHEL 7.2 / Ubuntu 16.04) and the older ELFv1 big-endian (ppc64; still used by AIX and some legacy IBM i workloads).

ELFv2 ppc64le calling convention: integer/pointer args in r3-r10, FP args in f1-f13, vector args in v2-v13. The TOC (table of contents) pointer is in r2; this is the most distinctive feature, used for position-independent global access without a GOT-equivalent. Stack alignment 16 bytes.

OpenPOWER community: still active. Raptor Talos II/Blackbird workstations remain available. POWER10 firmware schedules published through 2026 by IBM.

For Mochi: low priority. The market is enterprise IBM Power Systems shops, which run AIX or RHEL/SLES on ppc64le. ELFv2 is well-specified and clang/GCC support is excellent, so a backend could exist but the user base for a new language is small.

## §3 MIPS

MIPS is effectively a sunset architecture in 2026. Imagination's MIPS division was sold to Wave Computing in 2017, which went bankrupt; MIPS Technologies has pivoted to RISC-V (announced 2021).

Remaining MIPS deployments: legacy embedded networking (some Cisco, Juniper, MikroTik), legacy SOC designs, and Loongson 3A/3B/3C-series chips (which used a MIPS-derived ISA before LoongArch took over).

ABIs: o32 (32-bit, oldest), n32 (32-bit ABI with 64-bit registers), n64 (64-bit). MIPS Linux uses n32 or n64; embedded uses o32.

For Mochi: ignore entirely. Any developer with serious MIPS needs is using LLVM directly. No Phase ever.

## §4 LoongArch (LA664 / Loongson 3A6000)

LoongArch is Loongson's clean-sheet ISA introduced 2020-2021, replacing their MIPS-derived line. The LA664 microarch powers the 3A6000 (announced 2023) and 3C6000 server chips. LA664 is a 6-issue out-of-order core with 4 ALU, 4 AGU, 4 SIMD/FPU units, SMT, 64 KB L1 i/d, 256 KB L2.

ABI: lp64d data model (LA64 instruction set, double-precision FPU). Integer args in $a0-$a7, FP args in $fa0-$fa7. Static (callee-saved) regs $s0-$s9 and $fs0-$fs7. No red zone. 16-byte stack alignment. Aggregates classification mostly mirrors RISC-V LP64D rules.

LSX (128-bit) and LASX (256-bit) SIMD are LoongArch's AVX equivalents. LA664 enables them by default in `-march=la664`.

Recent psABI updates (2024-2025) added: vector arg passing rules, code-model chapter (extreme/medium/normal), R_LARCH_CALL36 relocation, TLS descriptor relocations, DWARF for LoongArch.

Linux support: mainline kernel, Loongnix and AOSC OS as primary distros. Fedora and Debian have ports in progress.

For Mochi: low priority globally; potentially relevant for China-market deployments. The ABI is well-specified and stable. Defer to Phase 3 or later unless a concrete user requests it.

## §5 s390x (IBM Z / LinuxONE)

s390x is the 64-bit z/Architecture used by IBM Z mainframes and LinuxONE. Calling convention: integer args in r2-r6, FP args in f0/f2/f4/f6 (paired), return in r2/r3 and f0. Stack growth is downward but with a 160-byte (or 224-byte) save area at the top of each frame, unique to s390x. Big-endian.

The s390x platform remains actively supported by RHEL, SLES, Ubuntu, openSUSE, and IBM publishes monthly open-source software validation reports. Tens of thousands of open-source packages are tested.

For Mochi: very low priority. Mainframe shops are conservative about language choices. The big-endian byte order also complicates any cross-target development. Skip until a paying customer asks.

## §6 Apple Silicon GPU / Metal compute

Out of MEP-42's primary scope (which is CPU code generation) but worth noting:

Apple Silicon GPUs are first-class compute targets via Metal. Mochi could grow a SIMT/compute backend that emits Metal Shading Language (a C++14-derived shader language) or AIR (Apple Intermediate Representation, the LLVM-based bitcode Metal consumes).

This is the same category as CUDA, ROCm/HIP, SYCL: a separate kernel-language compilation pipeline that lives next to the CPU backend. Wasm GPU (WebGPU + WGSL) is the cross-vendor analog.

Other GPU compute paths: NVIDIA PTX/SASS (CUDA), AMD GCN/RDNA (ROCm), Intel SPIR-V (Level Zero / OneAPI), Vulkan/SPIR-V (cross-vendor).

For Mochi: out of MEP-42 scope. Worth flagging as MEP-43 or later for a dedicated GPU backend. The runtime/vm3 has no story for SIMT code today.

## §7 Open questions for MEP-42

1. Power, MIPS, s390x, LoongArch: should MEP-42 commit to "never" or "maybe later"? Recommend "later, not Phase 1" for Power and LoongArch; "no" for MIPS; "later, on request" for s390x.
2. Cross-compile testing infrastructure: even if we ship these ISAs, do we run CI for them? Recommend QEMU-only smoke tests for any non-Phase-1 target.
3. GPU/Metal/CUDA: explicitly defer to a future MEP. Document the boundary clearly so users know what to expect.
4. Big-endian support: needed for s390x and ppc64 (BE flavor). Recommend designing the IR with byte-order agnosticism but only testing little-endian targets in Phase 1.
