---
title: "AArch64 Windows (Windows-on-ARM64)"
description: "Windows 11 on Snapdragon X / X2 Elite, Surface Pro X lineage, and ARM64EC interop."
tags: ["native-codegen", "targets"]
weight: 40
date: 2026-05-18T18:06:46+07:00
---

## §1 Provenance

- Microsoft ARM64 calling convention: https://learn.microsoft.com/en-us/cpp/build/arm64-windows-abi-conventions.
- ARM64EC ABI: https://learn.microsoft.com/en-us/windows/arm/arm64ec-abi.
- Windows on ARM developer docs: https://learn.microsoft.com/en-us/windows/arm/.
- PE/COFF spec: https://learn.microsoft.com/en-us/windows/win32/debug/pe-format (the IMAGE_FILE_MACHINE_ARM64 magic value is 0xAA64; ARM64EC is 0xA641).
- AAPCS64 base spec (Microsoft's ARM64 is a delta off this): https://github.com/ARM-software/abi-aa.
- Snapdragon X Elite developer kit reference: https://www.qualcomm.com/products/internet-of-things/development/snapdragon-developer-kits/snapdragon-dev-kit-for-windows.

## §2 Mechanism / specification

The Microsoft ARM64 ABI is based on AAPCS64 with these deltas:

1. Variadic functions: all floats in variadic position are passed as 64-bit integers in X registers; SIMD/FP registers are never used for variadic args. This applies even to named args of a variadic function.
2. Stack alignment: 16-byte at every call.
3. Frame pointer X29 is required (not just recommended); the OS unwinder depends on it.
4. Indirect result location: X8 (same as AAPCS64).
5. X18 is reserved by the OS for thread-local storage (TEB pointer). Compilers must not use X18 for general allocation.

Unwind on Windows ARM64 is table-driven, like x86_64 Windows: every nonleaf function has a `.pdata` entry pointing to an xdata blob. The xdata format is an ARM-specific compact unwind encoding documented in the ARM64 exception handling spec (https://learn.microsoft.com/en-us/cpp/build/arm64-exception-handling). Unlike x64 xdata which lists prolog operations, ARM64 xdata is a packed bytecode of unwind codes (save_reg, save_fpreg, alloc_s, alloc_m, alloc_l, set_fp, save_lrpair, etc.).

ARM64EC is a separate ABI flavor that lets ARM64EC code call x64 code (under emulation) and vice versa within the same process. ARM64EC binaries use a modified register usage map where some registers are reserved to shadow x64 registers; this enables "Arm64X" PE files that contain both pure-ARM64 and ARM64EC code paths. This is the mechanism behind Office, Edge, and other Microsoft apps running natively on Windows-on-ARM while still loading x64 plugins.

## §3 Platform coverage (May 2026)

- Windows 11 on ARM64: Snapdragon 8cx Gen 2/3 (Surface Pro X, Pro 9), Snapdragon X Elite/Plus (Surface Pro 11, Surface Laptop 7, Dell XPS 13, Lenovo Yoga Slim 7x, ASUS Vivobook S 15, HP OmniBook), Snapdragon X2 Elite/Extreme (2025-2026 generation, up to 18 cores at 5 GHz).
- Windows Server on ARM64: limited deployment, mostly for cloud (Azure ARM VMs use Ampere Altra).
- Snapdragon Dev Kit for Windows: Qualcomm's official ARM64 development desktop, shipped 2024 (with reported delays); 12-core Oryon at up to 3.8 GHz, 32GB RAM, 500GB SSD.
- Windows 10 on ARM64: end of mainstream support; Windows 11 ARM64 is the only relevant target for 2026 work.

Linux on Snapdragon X Elite is a separate effort (Linaro and Tuxedo are upstreaming kernel support); that path uses standard AAPCS64, not Microsoft's variant.

## §4 Current status (May 2026)

- Native ARM64 app catalog grew significantly through 2024-2025. Major apps with native ARM64 builds: Microsoft 365, Edge, Chrome, Firefox, VLC, Zoom, Adobe Photoshop, OBS, Visual Studio, Visual Studio Code, Git, Python, Node.js.
- Prism (Microsoft's x64-on-ARM emulator) added AVX/AVX2 emulation in 2024; performance loss vs native typically 10 to 25%.
- Snapdragon X2 Elite / X2 Elite Extreme announced at Snapdragon Summit 2025, up to 18 cores.
- ASIO low-latency audio driver in public preview for 2026.
- WSL on ARM64 runs natively and outperforms x86 WSL on I/O-heavy workloads.
- Microsoft moved most in-box tools and Store-curated apps to require ARM64 builds for Copilot+ certification.
- ARM64EC remains the recommended porting path for apps with extensive C++ dependencies that cannot all be recompiled at once.

## §5 Engineering cost for Mochi

Combines the AAPCS64 backend work with the PE/COFF object writer work from the x86_64 Windows backend:

1. Reuse the AAPCS64 instruction selector from the aarch64 Linux backend.
2. Plug in the Microsoft variadic delta (treat variadic floats as ints).
3. Generate ARM64 xdata: a different format from x64 xdata; the encoding is documented but writing a correct emitter from scratch is several weeks of work. lld and Go's linker have reference implementations.
4. Emit PE32+ with IMAGE_FILE_MACHINE_ARM64 (0xAA64) or IMAGE_FILE_MACHINE_ARM64EC (0xA641).
5. Honor X18 as reserved.
6. Generate `__C_specific_handler` / `__chkstk_arm64` references where required for large stack frames.

Cross-compiling: lld-link supports aarch64-pc-windows-msvc with full xdata generation. Zig's CC frontend covers it. Mingw-w64 has partial ARM64 support. Go's own linker can produce Windows ARM64 binaries (`GOOS=windows GOARCH=arm64`) since Go 1.17.

ARM64EC is much harder: requires understanding the dual-mode register model, the "checked function" stubs, and the Arm64X relocation format. Skip for Phase 1.

## §6 Mochi adaptation note

compiler3's `backend/native/aarch64` package would gain a `os=windows` flavor that swaps the unwind emitter and ABI lowering. Most of the instruction selector and register allocator are shared with Linux ARM64. The Cell handle from MEP-40 still fits in one X register.

The runtime/vm3 needs minor adjustments for X18 reservation (cannot use as a scratch register in inline asm), Windows TLS via TEB (different from gs:0 on x86_64 Windows or fs:0 on Linux), and the Windows heap allocator (HeapAlloc/VirtualAlloc instead of mmap).

## §7 Open questions for MEP-42

1. Is Windows-on-ARM64 in Phase 1? Recommend Phase 2 or later: small but growing user base, and the unwind data work is non-trivial.
2. ARM64EC: ignore for Phase 1, revisit if Mochi wants to interoperate with x64 plugins on Windows.
3. Snapdragon-specific tuning (Oryon microarch): Phase 1 should emit generic ARMv8.4 code; Snapdragon-tuned codegen waits for LLVM to ship a `-mcpu=oryon` entry (still pending as of May 2026).
4. Testing infrastructure: do we set up GitHub Actions ARM64 Windows runners (now generally available), or rely on emulation? Recommend native runners.
