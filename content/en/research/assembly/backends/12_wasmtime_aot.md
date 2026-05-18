---
title: "Wasmtime AOT as a Code-Generation Backend for Mochi"
description: "\"Mochi → Wasm → wasmtime compile → native\": skip the backend, use the wasm ecosystem."
tags: ["native-codegen", "backends"]
weight: 120
date: 2026-05-18T18:11:03+07:00
---

## §1 Provenance
- Project home: https://wasmtime.dev/
- Source: https://github.com/bytecodealliance/wasmtime
- AOT docs: https://docs.wasmtime.dev/examples-pre-compiling-wasm.html
- CLI options: https://docs.wasmtime.dev/cli-options.html
- WASI Preview 2 launched (vote January 25, 2024): https://eunomia.dev/blog/2025/02/16/wasi-and-the-webassembly-component-model-current-status/
- Bytecode Alliance blog: https://bytecodealliance.org/articles/
- Wasmtime v25 release: WASI 0.2.1, user stack maps, extended consts.
- Wasmtime v27 release: completed Wasm GC, PyTorch wasi-nn backend.
- Wasmtime v35 release: AArch64 support in Winch, plus Component Model and Custom Page Sizes (per https://bytecodealliance.org/articles).

## §2 Mechanism
You bring a Wasm module. `wasmtime compile` reads it, runs Cranelift (or Winch for fast tier-0) over each function, and writes a `.cwasm` file: an ELF-shaped container holding native machine code plus metadata needed by the Wasmtime runtime. At deployment, `wasmtime run --allow-precompiled foo.cwasm` mmap's the file and jumps into the precompiled code without re-running the compiler.

`.cwasm` is **tightly bound** to:
1. The Wasmtime version that produced it.
2. The exact engine `Config` (enabled proposals, memory model, signal handling).
3. The target triple (e.g., `aarch64-unknown-linux`).

`wasmtime explore` produces an HTML visualizer of the wasm-to-native mapping. `wasmtime serve` runs a precompiled HTTP component.

For Mochi's purposes the model is: **Mochi compiles to Wasm; Wasmtime compiles Wasm to native**. Mochi avoids ever writing a native backend.

## §3 Target coverage (May 2026)
Native targets supported by `wasmtime compile`:
- x86_64 Linux, macOS, Windows.
- AArch64 Linux, macOS, Windows.
- RISC-V RV64GC Linux.
- s390x Linux.

This matches Cranelift's coverage exactly because Wasmtime uses Cranelift for AOT.

Object container: a custom ELF-flavored `.cwasm` format. The bytes inside are native machine code with Wasmtime-specific trampolines for imports, traps, memory access.

WASI Preview 2 (component model, wasi-cli, wasi-http, wasi-io, wasi-filesystem, wasi-sockets, wasi-clocks, wasi-random) is shipping. WASI Preview 3 (async, streams as values) is on the horizon (https://techbytes.app/posts/wasm-components-wasi-preview-3-edge-optimization-2026/).

## §4 Production / language adoption status (May 2026)
Wasmtime AOT is a production codepath for:
- **Fastly Compute@Edge**: every customer module is precompiled.
- **Fermyon Spin**: precompile-on-deploy is the default.
- **Shopify**: function compilation pipeline.
- **Microsoft Hyperlight**: serverless wasm executor.
- **wasmCloud, wasmEdge interop**, various Kubernetes wasm runtimes.

Many languages target Wasm: Rust, C/C++ (via wasi-sdk), Go (via TinyGo or the upcoming GOOS=wasip2), Zig, AssemblyScript, Swift, Java (via TeaVM and CheerpJ), .NET (Wasm AOT in .NET 10, per the Medium "WebAssembly .NET 10 Runtime Revolution"), Python (CPython wasmtime port), Ruby (mruby-wasm), JavaScript (via Static Hermes, Jaws). Any of these can be precompiled with `wasmtime compile`.

License: Apache 2.0 with LLVM Exceptions.

Performance: Wasm-via-Cranelift is roughly 1.5-2.5x slower than native C `-O2`. Significantly faster than interpreted, somewhat slower than JS V8 TurboFan on JIT-friendly code, faster than V8 Liftoff baseline.

## §5 Engineering cost for Mochi
- **Binary footprint**: Mochi ships `.wasm` (small, often KB-scale). Users install `wasmtime` separately (~70-100 MB). Alternatively, Mochi ships precompiled `.cwasm` per target, skipping wasmtime at runtime by embedding the Wasmtime runtime.
- **Build complexity**: Mochi needs a Wasm backend in its compiler. Choices:
  1. Emit Wasm text (`.wat`) and shell out to `wasm-tools` to assemble.
  2. Emit Wasm binary directly using a Go library like https://github.com/tetratelabs/wabin or https://github.com/bytecodealliance/wasm-tools (Rust, would need cgo).
  3. Emit C and use Emscripten or wasi-sdk's Clang.
- **License**: Apache 2.0 LLVM-Exception throughout.
- **Cross-compilation**: trivial. Wasm is the IR; per-host native compilation is a deployment step.
- **Debugging**: Wasm DWARF support is improving but still rough; native debugging of `.cwasm` is poor.
- **Runtime startup**: precompiled `.cwasm` instantiation is sub-millisecond.

## §6 Mochi adaptation note
A `compiler3/emit/wasm` package would lower compiler3 IR (`/Users/apple/github/mochilang/mochi/compiler3/ir`) to the Wasm binary format. Mochi's vm3 typed Cell layout maps to Wasm i64 (with some bit-packing) plus Wasm GC structs (now stable in Wasmtime v27+). The three-bank register file becomes Wasm locals.

Files touched:
- New `compiler3/emit/wasm/` package (~2000-3000 lines of Go).
- New `runtime/wasm/` wrapper for embedding wasmtime (if we want in-process execution).
- The existing `compiler3/opt` IR optimizations apply unchanged; Wasm gets the same SSA-flavored IR.

This is **the most pragmatic path to "Mochi binaries on every platform"** because it offloads the native codegen problem to a well-funded, well-tested project.

## §7 Open questions for MEP-42
- **Wasm-only or Wasm-plus-native?** If Mochi targets Wasm first, the native binary story is "wasmtime compile your wasm." If users dislike the wasmtime dependency, we need a native AOT path anyway.
- **Wasm GC vs no GC**: Mochi's vm3 has typed arenas; mapping to Wasm GC (now stable) gets us a managed heap for free, but ties us to GC-aware runtimes. Without GC, we manage memory manually inside linear memory.
- **Component Model**: wasi-p2 components compose. Mochi modules as components would let Mochi code interop cleanly with Rust, Go, Python on the wasm side. Worth considering.
- **`.cwasm` portability**: a `.cwasm` is host-specific. Mochi shipping per-arch precompiled binaries is straightforward; shipping a portable Wasm and asking users to precompile is also fine.
- **Toolchain dependency**: users need either `wasmtime` installed or an embedded wasmtime in Mochi. Embedded wasmtime via FFI from Go is moderately involved (no first-class Go binding, but a C API exists).
- **Verdict**: for Phase 1 this is the **single highest-leverage backend choice** because it gets us x86_64+arm64+riscv64+browser in one move. Pair with C-as-target for users who do not want wasmtime.