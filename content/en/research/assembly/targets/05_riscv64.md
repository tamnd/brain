---
title: "RISC-V RV64GC"
description: "The general-purpose 64-bit RISC-V baseline plus vector and recent extensions."
tags: ["native-codegen", "targets"]
weight: 50
date: 2026-05-18T18:06:46+07:00
---

## §1 Provenance

- RISC-V Unprivileged ISA Manual: https://github.com/riscv/riscv-isa-manual (the canonical Volume I).
- RISC-V Privileged ISA Manual: same repo, Volume II.
- RISC-V psABI (ELF): https://github.com/riscv-non-isa/riscv-elf-psabi-doc.
- RISC-V Vector ISA (V 1.0): https://github.com/riscv/riscv-v-spec.
- RISC-V Profiles (RVA20, RVA22, RVA23): https://github.com/riscv/riscv-profiles.
- RISC-V Ratified Extensions list: https://riscv.atlassian.net/wiki/spaces/HOME/pages/16154732/Ratified+Extensions.
- Linux kernel arch/riscv documentation: https://docs.kernel.org/arch/riscv/.

## §2 Mechanism / specification

RV64GC = RV64I (base 64-bit integer) + M (multiply/divide) + A (atomics) + F (single-precision FP) + D (double-precision FP) + Zicsr + Zifencei + C (compressed 16-bit instructions). This is the de facto Linux baseline.

Calling convention (LP64D ABI):

- Integer/pointer arguments: a0-a7 (x10-x17).
- Floating-point arguments: fa0-fa7 (f10-f17).
- Return values: a0 (and a1 for 128-bit), fa0 (and fa1 for complex).
- Indirect result pointer: arg-0 (a0), unlike AArch64.
- Stack: 16-byte aligned at function entry.
- Callee-saved (s-registers): s0-s11 (x8-x9, x18-x27), fs0-fs11. s0 doubles as the frame pointer when used.
- Caller-saved: t0-t6 (x5-x7, x28-x31), all argument regs, ft0-ft11.
- ra (x1) holds the return address (caller-saved).
- sp (x2), gp (x3), tp (x4) are special-purpose.

Aggregates up to 16 bytes pass in two registers; larger aggregates pass by reference. Floats inside small structs can use FP arg registers (the "hardfloat" ABI rule).

Variadic args follow the integer convention (no FP args in vararg position), similar to MS ARM64.

There is no shadow space and no red zone.

Vector (RVV 1.0) calling convention: vector args use v8-v23 when present; vtype/vl are caller-saved. The vector length is configurable per call site via vsetvl.

## §3 Platform coverage (May 2026)

Linux distributions with first-class RV64GC support:

- Debian: official port since Debian 13 (trixie).
- Ubuntu: 24.04 LTS on SpacemiT K1 family; 26.04 LTS (Resolute Raccoon) planned for SpacemiT K3 in April 2026.
- Fedora: Fedora 41 (January 2025) and Fedora 42 (April 2025) ship RISC-V images. Build infrastructure expanded with a dedicated Koji instance in early 2025. Hardware tested: StarFive VisionFive 2, SiFive HiFive Premier P550, Banana Pi BPI-F3, Milk-V Jupiter, LicheePi 4A, Milk-V Megrez (P550 cores).
- openSUSE Tumbleweed: rolling RISC-V port.
- Alpine, Arch (riscv64), Gentoo: community ports.

Hardware boards (May 2026):

- LicheePi 4A: TH1520 with 4 C910 cores at 2.0 GHz, RV64GCV, up to 16 GB LPDDR4X, 4 TOPS NPU. Vector extension is the pre-1.0 0.7.1 draft, requiring special toolchain handling.
- Banana Pi BPI-F3: SpacemiT K1 8-core (X60 cores at 1.6 GHz), up to 16 GB DDR. RVV 1.0 on K1.
- StarFive VisionFive 2 / JH7110: 4 U74 cores at 1.5 GHz, mature Linux support.
- SiFive HiFive Premier P550: 4 P550 cores at 1.8 GHz, server-class.
- Milk-V Jupiter / K1: SpacemiT K1, similar to BPI-F3.
- SpacemiT K3 (2026): 8 X100 cores at up to 2.4 GHz, RVA23 compliant, 60 TOPS AI accelerator.
- Tenstorrent Ascalon-X (late 2025 / 2026): 8-wide out-of-order, claims IPC parity with AMD Zen 5; targeted at data center.
- Sophgo SG2380: cancelled (TSMC declined to fab after US sanctions on Sophgo). The Milk-V Oasis never shipped.

Server class: SG2042 (64-core, 2023), SG2380 cancelled, Ventana Veyron (Qualcomm bought Ventana in 2025), Rivos (Meta acquired).

## §4 Current status (May 2026)

- RVV 1.0 ratified November 2021.
- RVA22 profile ratified 2023. RVA23 profile ratified in 2024 and mandates Vector 1.0, Hypervisor, Bitmanip; this is the platform contract that ended the "wild west" fragmentation.
- RVA23-class silicon: SpacemiT X100, Tenstorrent Ascalon-X, plus several Chinese designs.
- Zfh (half-precision FP, IEEE binary16): ratified.
- Zfbfmin / Zvfbfmin (BFloat16): ratified.
- B extension (bitmanip = Zba + Zbb + Zbs): ratified, part of RVA22+.
- Zicond (integer conditional ops): ratified.
- Matrix extension: in development, drafts have shipped in some Chinese silicon.
- RVA23 is the recommended platform target for general-purpose Linux distros that want broad portability.
- Industry consolidation: Qualcomm/Ventana, Meta/Rivos.

## §5 Engineering cost for Mochi

Comparable to AArch64 in complexity, simpler in some ways (no PAC/BTI/MTE matrix):

1. Instruction selector for RV64GC. The compressed extension complicates instruction encoding but reduces code size 25-30%.
2. ABI lowering for LP64D. Aggregate rules are like AAPCS but with a different register split.
3. ELF emission (psABI well documented).
4. DWARF unwind for stack unwinding (no compact unwind variant).
5. Linker stub conventions: AUIPC+JALR pairs for far calls; PLT and GOT for dynamic linking.

Optional but valuable: bitmanip-aware instruction selection, Zicond for branchless conditional moves, vector codegen (significant effort: per-call vsetvl, register grouping LMUL, mask handling).

Cross-compile from any host: clang/GCC riscv64-linux-gnu, Go's `GOARCH=riscv64`. Mochi can rely on the system linker.

Testing: QEMU-system-riscv64 is mature and well-supported on x86_64 hosts. Real silicon is helpful but not blocking for Phase 1.

## §6 Mochi adaptation note

compiler3 gains a `backend/native/riscv64` package. The 8-byte Cell handle fits in a single a-register. The simplest path is to target RVA22 (RVV optional) for Phase 1, then add RVA23 (vector mandated) once Mochi has SIMD intrinsics or auto-vectorization in compiler3.

runtime/vm3 has no architectural dependencies that change for RISC-V beyond atomic primitives (LR/SC vs CAS semantics differ slightly from x86 and ARM).

## §7 Open questions for MEP-42

1. Phase 1 or Phase 2? Recommend Phase 2; the ecosystem is real but not yet at the scale of x86_64 or AArch64, and Mochi's user base is unlikely to demand it on day one.
2. Profile target: RVA22 (broader hardware) or RVA23 (vector mandated, smaller hardware)? Recommend RVA22 with optional RVA23 codegen path.
3. Vector codegen in Phase 1? Recommend no; revisit when Mochi gains SIMD source support.
4. LicheePi 4A specifically: the vector extension is 0.7.1 draft, not 1.0. Recommend ignoring this hardware for Phase 1; target K1/K3 and P550-class boards instead.
