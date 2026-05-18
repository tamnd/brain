---
title: "Swift and Embedded Swift"
description: "Apple's Swift in two modes: full LLVM-driven AOT for app platforms, and a stripped Embedded Swift mode for microcontrollers and freestanding binaries."
tags: ["native-codegen", "aot"]
weight: 110
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- Project home: https://swift.org/
- Source: https://github.com/swiftlang/swift
- Embedded Swift overview: https://www.swift.org/get-started/embedded/
- "Get Started with Embedded Swift on ARM and RISC-V Microcontrollers": https://www.swift.org/blog/embedded-swift-examples/
- WWDC24 session "Go small with Embedded Swift": https://developer.apple.com/videos/play/wwdc2024/10197/
- Swift 6 announcement: https://www.swift.org/blog/announcing-swift-6/
- Embedded Swift vision document (in-tree): https://github.com/swiftlang/swift-evolution/blob/main/visions/embedded-swift.md
- Authors: Apple's Swift team, with Embedded Swift led by Kuba Mracek, Alex Lorenz, and the Cupertino compiler group. Lattner was the original Swift creator (now at Modular working on Mojo).

## §2 Architecture

Swift's standard AOT pipeline:

1. Parse + import resolution.
2. Sema (semantic analysis, type inference, generics resolution).
3. SILGen lowers to SIL (Swift Intermediate Language), a typed SSA IR with high-level operations (`alloc_box`, `retain`, `release`, `dynamic_method`, generics still as parameters).
4. SIL passes: generic specialisation, devirtualisation, ARC optimisation (eliminating retain/release pairs), capture promotion, mandatory inlining, then optimisations.
5. IRGen lowers SIL to LLVM IR.
6. LLVM optimises and emits machine code.
7. The Swift driver invokes the system linker against the Swift runtime.

Embedded Swift is a specialised compilation mode of the same pipeline, controlled by `-enable-experimental-feature Embedded` plus `-wmo` (whole-module optimisation). It changes step 4 by:

- Forcing full generic specialisation (no runtime generic dispatch tables).
- Disabling existentials, runtime reflection (`Mirror`), and the Objective-C bridging runtime.
- Disabling ABI stability (no on-disk Swift ABI metadata; symbol mangling stays in-process only).
- Producing standalone binaries with no Swift runtime metadata, no type metadata, no demangler.

Whole-module optimisation is mandatory because Embedded Swift relies on complete visibility for specialisation; this is effectively a closed-world AOT pipeline within Swift's normally open-world dynamic dispatch model.

## §3 Targets and platforms (May 2026)

Standard Swift: iOS, macOS, watchOS, tvOS, visionOS, Linux (x86_64, aarch64), Windows (x86_64, arm64), and recently Android. Distributed via Swiftly (the new toolchain manager) and toolchain.swift.org.

Embedded Swift adds bare-metal targets: arm-none-eabi (Cortex-M0/M3/M4/M7/M33), aarch64-none-elf, riscv32-none-elf (ESP32-C3/C6, SiFive), riscv64-none-elf. Confirmed working chips include STM32F746, Raspberry Pi RP2040, Nordic nRF52840, Espressif ESP32-C6, plus Apple's own Secure Enclave Processor (where Embedded Swift has been shipping in production since well before WWDC24).

Cross-compilation is via the standard LLVM cross paths; the Embedded Swift example projects show ESP-IDF and Zephyr integration. No bundled libc story (you bring your own RTOS / freestanding libc).

Linking is fully static for Embedded Swift; standard Swift dynamically links against `libswiftCore.dylib`/.so.

## §4 Runtime

Standard Swift runtime is substantial:

- A reference-counted memory model (strong/weak/unowned), with ARC optimisation in SILGen.
- A demangler, type metadata layout, runtime generics support.
- Objective-C interop on Apple platforms (the Objective-C runtime is linked in).
- Concurrency runtime (async/await, actors, structured concurrency) added in Swift 5.5 and matured through 6.x.

Embedded Swift removes most of this. The remaining runtime fits in tens of KB:

- ARC primitives (`swift_retain`, `swift_release`) implemented as small C functions.
- A bump or fixed-region allocator (the embedded developer provides the strategy).
- No GC, no demangler, no reflection, no Objective-C runtime.
- Optional Swift MMIO library for safe memory-mapped register access.

FFI: `@_silgen_name` and `@_cdecl` provide C-callable entry points; `import C` modules expose C APIs. Standard Swift also has bidirectional Objective-C interop.

Hello-world: standard Swift on macOS-arm64 with `-O`: roughly 50 KB binary dynamically linked against the system libswiftCore. Embedded Swift on Cortex-M4 with full link-time DCE: a few hundred bytes for a minimal `_start` plus the LED blink.

## §5 Status (May 2026)

Standard Swift 6 (mid-2024) brought strict concurrency by default; Swift 6.2 (in development through 2025) brought Embedded Swift further out of "experimental". Embedded Swift is still officially marked experimental but is production-shipping inside the Secure Enclave Processor and is documented as ready for evaluation on third-party silicon.

Production users (standard Swift): Apple (iOS/macOS apps and system services), large swathes of fintech (the Square iOS app, the Robinhood iOS app), backend systems at Slack, Lyft, and others using Vapor or Hummingbird. Production users (Embedded Swift): Apple's Secure Enclave is the public reference; third-party adoption is early but visible in homebrew firmware projects and a growing number of vendor demos.

Performance: standard Swift is within 10–20 percent of Rust for typical workloads, sometimes faster on ARC-friendly code, slower on allocation-heavy paths. Embedded Swift trades language features for binary size; its generated code is the same LLVM output but with smaller surface area.

Known limitations: Embedded Swift is still experimental; some Swift features (existentials, runtime reflection, dynamic casts to non-final classes) are unavailable in embedded mode; toolchain installation on non-Apple platforms remains tricky.

## §6 Mochi adaptation note

The "Embedded mode is a subset, not a different language" pattern is the most adaptable piece for Mochi:

- Mochi can ship a `mochi build --mode=embedded` that disables: dynamic import, `runtime/vm3` reflection, the dataset/JSON/YAML built-ins, and the M:N scheduler if any. The result is a small standalone binary suitable for short CLIs or freestanding deployments, similar in spirit to Embedded Swift.
- Force whole-module optimisation in this mode (same as Embedded Swift's `-wmo`). For Mochi this is natural because the compiler is already closed-world.
- ARC as the memory strategy in embedded mode is a credible alternative to a tracing GC. Swift's ARC-optimisation passes are well-documented; Mochi could prototype ARC in `runtime/vm3/arc.go` and gate it behind the embedded mode.
- The two-mode model (full Swift vs Embedded Swift) maps onto a Mochi "full" vs "lean" build mode. The lean mode targets containers, AWS Lambda cold starts, and CLI tools; full mode targets long-running services where the runtime is amortised.
- Apple's experience shipping Embedded Swift inside the SEP for years before public announcement is a reminder that the embedded mode should be designed and tested for production hardware, not as a toy.

Affected Mochi files: `compiler3/embedded/` (new mode flags), `runtime/vm3/embedded/` (slim runtime variant), `runtime/vm3/arc.go` (new ARC allocator), `compiler3/wmo.go` (force whole-module specialisation).

## §7 Open questions for MEP-42

1. Does Mochi want an explicit "embedded" subset, or one runtime that scales down?
2. ARC vs tracing GC vs arena: should Mochi commit to ARC for embedded mode to avoid GC pauses?
3. Reflection and dynamic features: which are in core Mochi, which are mode-gated?
4. Do we target microcontrollers (Cortex-M, ESP32) seriously, or only "small Linux/macOS binaries"?
5. Should `mochi build --mode=embedded` produce static linking by default, the way Embedded Swift does?