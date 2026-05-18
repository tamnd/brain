---
title: "WebAssembly"
description: "Wasm 3.0 (2025) as the stable target, plus WASI Preview 2/3 and the component model."
tags: ["native-codegen", "targets"]
weight: 60
date: 2026-05-18T18:06:46+07:00
---

## §1 Provenance

- WebAssembly Core Specification 3.0: https://webassembly.github.io/spec/core/ (W3C release September 2025).
- Wasm 3.0 release announcement: https://webassembly.org/news/2025-09-17-wasm-3.0/.
- Feature status tracker: https://webassembly.org/features/.
- Component Model spec: https://github.com/WebAssembly/component-model.
- WASI roadmap: https://wasi.dev/roadmap.
- WASI Preview 2 standard: https://github.com/WebAssembly/WASI/tree/main/wasip2.
- Wasmtime documentation: https://docs.wasmtime.dev/.
- WAMR (WebAssembly Micro Runtime): https://github.com/bytecodealliance/wasm-micro-runtime.

## §2 Mechanism / specification

Wasm is a stack-based virtual ISA with structured control flow (no arbitrary jumps; blocks, loops, ifs, branches). The binary format is a sequence of typed sections:

- Type section (function signatures).
- Import section (host imports).
- Function section (function index to type index).
- Table section (function reference tables for indirect calls).
- Memory section (linear memory definitions).
- Global section.
- Export section.
- Start section (initializer).
- Element section (populates tables).
- Code section (function bodies).
- Data section (populates memory).
- DataCount section.
- Custom sections (debug info, names, etc.).

Calling convention is implicit: arguments and results are described by the function type, and the runtime pushes/pops them off the operand stack. There are no register conventions visible to Wasm; the underlying engine (V8, SpiderMonkey, Wasmtime, etc.) handles ABI lowering to the host machine.

Memory model: by default a single linear memory addressed by i32 (4 GiB max). Memory64 proposal (in Wasm 3.0) allows i64 addressing (up to 16 EiB theoretical).

Wasm 3.0 additions:

- Garbage collection (WasmGC): struct and array heap types with i31ref tagged ints. The runtime owns the GC; Wasm declares layouts.
- Typed references: ref types describe exact heap shapes, enabling safe indirect calls via call_ref.
- Tail calls (return_call, return_call_indirect, return_call_ref).
- Multiple memories.
- Exception handling (try, throw, catch).
- 128-bit SIMD (already in 2.0, refined).
- Relaxed SIMD (architecture-dependent results in exchange for speed).

WASI Preview 2 (stable as of 2026): components plus the worlds/interfaces model. Major WASI worlds: wasi:cli (CLI runner), wasi:http (HTTP proxy), wasi:filesystem, wasi:sockets, wasi:clocks, wasi:random, wasi:io.

WASI Preview 3 (release candidates through 2026): native async function ABI, first-class futures and streams, simplified WIT (wasi:http drops from 11 resource types to 5). Threading is still unresolved.

## §3 Platform coverage (May 2026)

Browsers (all support WasmGC and tail calls): V8 (Chrome, Edge, Node.js), SpiderMonkey (Firefox), JavaScriptCore (Safari, since December 2024 for GC).

Server / standalone runtimes:

- Wasmtime: reference Bytecode Alliance runtime; WASIp3 snapshot support since Wasmtime 43 (March 2026).
- WAMR: lightweight, embedded-focused; AOT and interpreter modes.
- Wasmer: commercial, edge-focused.
- WasmEdge: CNCF project, cloud and edge.
- Wizard Engine: research-focused, fast in-place interpreter.
- Spin (Fermyon): WASIp2 framework that shipped a WASIp3 RC in v3.5 (November 2025).

Edge platforms: Cloudflare Workers, Fastly Compute@Edge, Fermyon Cloud, Vercel Edge Functions. All support WASI components.

Embedded: ESP32, RP2040 via WAMR. Browser-less Wasm on microcontrollers is mature.

WASIX: a Wasmer-led extended POSIX-like layer; not standardized, competes with WASI in some niches.

## §4 Current status (May 2026)

- Wasm 3.0 standardized September 2025 with nine features: GC, exception handling, tail calls, memory64, multiple memories, relaxed SIMD, typed function references, type imports, JS-Promise integration.
- WasmGC enables JVM-language toolchains (Kotlin/Wasm, Scala.js, Dart) to ship without bundling their own collector.
- WASI 0.3.0 (Preview 3) finalization expected through 2026; WASI 1.0 planned for 2026.
- Wasm 3.0 usage at ~5.5% of Chrome page loads (early 2026), up from 4.5% the prior year.
- Production deployments: Figma's rendering engine, Adobe Photoshop on the web, AutoCAD Web, Google Meet video processing.
- Threading: shared-memory threading is in the browser spec but not yet in WASI. No concrete ship date.

## §5 Engineering cost for Mochi

Lowest engineering cost of any target. The Wasm binary format is simple enough to emit directly without third-party libraries.

1. Emit Wasm modules: ~2-3 weeks for a basic backend writing all standard sections. Reference implementations: Go's `golang.org/x/wasm` (limited), the binaryen library (C++; can be invoked as a CLI), wabt (CLI tools), and the official spec repo's reference interpreter.
2. Lower Mochi values: easiest if Mochi targets WasmGC (Wasm 3.0). Then Mochi's typed Cell maps to anyref / struct types, and the host runtime collects.
3. WASI for IO: link against `wasi:cli`, `wasi:filesystem`, `wasi:sockets`, etc.
4. Component model for FFI: optional in Phase 1, valuable for interop later.

A non-GC linear-memory backend is also viable but requires Mochi to ship its own collector inside the module (significant runtime overhead).

Cross-compilation is trivial: Wasm is host-independent. The Go compiler already supports `GOOS=wasip1 GOARCH=wasm`.

## §6 Mochi adaptation note

compiler3's `backend/wasm` would emit Wasm 3.0 with WasmGC. The MEP-40 8-byte Cell handle does not map directly; instead, Mochi would declare struct types per Mochi type and let the engine handle layout. The runtime/vm3 arena allocator is bypassed entirely: the Wasm engine's GC takes over.

For a non-GC linear-memory backend, Mochi would compile the runtime/vm3 arena into Wasm linear memory and have Mochi code call into it via function imports. This is a heavier port (the arena handle, the Cell encoding, and all type dispatch must work inside a 4 GiB i32 linear memory) but matches the MEP-40 design more literally.

## §7 Open questions for MEP-42

1. Phase 1 or not? Recommend yes. Wasm is the cheapest backend to ship and the highest-leverage target (browsers, edge, embedded all in one).
2. WasmGC vs linear-memory backend? Recommend WasmGC for Phase 1: less work, smaller output, faster runtime, leverages decades of engine GC investment. Provide a `-wasm-no-gc` flag as escape hatch.
3. WASI Preview 2 (stable) or Preview 3 (async, RC)? Recommend Preview 2 in Phase 1, Preview 3 once WASI 1.0 ratifies.
4. Component model in Phase 1? Recommend deferring: components are valuable for FFI and composition, but the tooling is still maturing. A plain `wasi:cli` world is enough for v1.
5. Browser target: ship raw .wasm with a tiny JS loader, or use the JS-Promise integration spec? Recommend raw .wasm + small loader; JS-PI is for interop, not standalone apps.
