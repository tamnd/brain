---
title: "WebAssembly Module Binary Format"
description: "The .wasm container, plus the component model binary and WAT text format."
tags: ["native-codegen", "formats"]
weight: 40
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- WebAssembly Core Specification 3.0, Binary Format chapter: https://webassembly.github.io/spec/core/binary/index.html.
- Component Model Binary Format: https://github.com/WebAssembly/component-model/blob/main/design/mvp/Binary.md.
- WAT (text format) reference: https://webassembly.github.io/spec/core/text/index.html.
- Custom section conventions (name section, source maps): https://github.com/WebAssembly/design/blob/main/BinaryEncoding.md#name-section.
- WASI Preview 2 worlds and interfaces: https://github.com/WebAssembly/WASI/tree/main/wasip2.
- Wabt (WebAssembly Binary Toolkit): https://github.com/WebAssembly/wabt.
- Binaryen (optimizer and toolkit): https://github.com/WebAssembly/binaryen.

## §2 Mechanism / specification

A Wasm module begins with an 8-byte preamble: magic 0x00 0x61 0x73 0x6D ("\0asm") followed by version 0x01 0x00 0x00 0x00 (current stable version, unchanged since MVP).

Then a sequence of sections, each: 1-byte section ID, ULEB128 section size, section payload.

Standard section IDs (in canonical order, though only required for the binary to be valid that they not interleave incorrectly):

- 0 = Custom (any number, anywhere). Used for the name section, source maps, producer info, debug info.
- 1 = Type. List of function types (param types, result types). With Wasm 3.0 GC, this section also declares struct, array, and recursive type groups.
- 2 = Import. External imports (functions, tables, memories, globals). Each entry: module name, field name, kind, type descriptor.
- 3 = Function. Maps function indices (within the module) to type indices.
- 4 = Table. Tables of references (func refs, externrefs, GC refs).
- 5 = Memory. Linear memories (initial pages, optional max pages, optional shared flag, optional i64 address type flag).
- 6 = Global. Mutable/immutable globals with initializer expressions.
- 7 = Export. Public symbols.
- 8 = Start. Index of a function called automatically on instantiation.
- 9 = Element. Table initializers.
- 10 = Code. Function bodies (one per function declared in section 3). Each body: local declarations (count + type pairs) + expression bytes terminating in 0x0B.
- 11 = Data. Memory initializers (active or passive).
- 12 = DataCount. Required if bulk-memory instructions reference data segments.
- 13 = Tag. Exception tags (Wasm 3.0 exception handling).

All integers are LEB128 (signed or unsigned as appropriate). Floats are little-endian IEEE-754. Strings are UTF-8 with a ULEB128 length prefix.

### Instruction encoding

Each instruction is a 1-byte opcode (with multi-byte extensions via prefix bytes 0xFB for GC, 0xFC for non-trapping conversions/bulk memory, 0xFD for SIMD, 0xFE for threads/atomics). Immediates (memory args, local indices, type indices, etc.) follow as LEB128 or floats.

Control flow opcodes carry a block type immediate (either a value type, an empty result, or a type index for multi-value). Block / loop / if open a structured region terminated by `end` (0x0B). Branches are relative (target is a label depth).

### Custom sections of interest

- `name`: function and local names (used by stack traces and debuggers).
- `producers`: language and toolchain identification (Mochi should write itself in here).
- `target_features`: feature flags consumed by the producer (mutable globals, SIMD, etc.).
- `external_debug_info` / `build_id`: emerging DWARF-via-custom-section convention.

### Component model binary

A component is a Wasm module wrapped in a different preamble:

- Magic 0x00 0x61 0x73 0x6D (same), version 0x0D 0x00 0x01 0x00 (the component model version differs from core Wasm).
- Then a sequence of sections: core module, core instance, core type, component, instance, alias, type, canon, start, import, export, value.

Components glue multiple core modules together with typed interfaces (defined in WIT, WebAssembly Interface Type). The `canon` section bridges core types and component types (lowering and lifting).

### WAT text format

S-expression syntax. Round-trippable with the binary form via wabt (`wat2wasm` and `wasm2wat`). Used for hand-written tests, debugging, and small examples in spec documents.

## §3 Platform coverage (May 2026)

Browsers consume Wasm modules via the JavaScript WebAssembly API (`WebAssembly.compile`, `WebAssembly.instantiate`). Standalone runtimes (Wasmtime, WAMR, Wasmer, WasmEdge) load .wasm files directly. Edge platforms (Cloudflare Workers, Fastly Compute@Edge, Fermyon Cloud) accept either raw modules or components.

WASI components are the package format for cross-runtime Wasm: a single .wasm file that declares its host interface requirements via WIT.

## §4 Current status (May 2026)

- Wasm 3.0 binary format finalized September 2025: GC type encoding, exception tags, memory64, tail call opcodes, relaxed SIMD opcodes, multi-memory all standardized.
- Component model spec is post-MVP and stabilizing for the WASI 1.0 milestone.
- The "name" custom section is universally used; "producers" is increasingly common.
- DWARF in custom sections is the de facto debugging format; Chrome DevTools, Wasmtime, and wizer all consume it.
- The text format (WAT) has not changed in shape since MVP; new instructions just gain new keywords.

## §5 Engineering cost for Mochi

Lowest of any format. The entire binary spec is ~50 pages of LEB128 + tagged sections. Mochi can write a complete emitter in a few thousand lines of Go without any third-party library.

Must-have: types, imports, functions, code, exports, memory or GC types depending on backend choice. ~2 weeks of work for a first complete emitter targeting WasmGC.

Should-have: name section for stack traces, producers section for tooling identification, start section if Mochi needs module-init code.

Nice-to-have: component model wrapping (only if Mochi wants first-class FFI). DWARF custom sections (for debugging). Source maps (for browser debugging).

Validation: every Mochi-emitted module should round-trip through `wasm-validate` (from wabt) in CI. The validator catches type errors, malformed LEB128, broken control flow, etc.

## §6 Mochi adaptation note

compiler3 gains a `backend/wasm` package. Two code paths:

1. WasmGC backend: declare Mochi types as Wasm struct/array types. Mochi values become typed references, the engine GC manages them. Bypasses runtime/vm3 arena entirely.
2. Linear memory backend: compile runtime/vm3 arena into Wasm linear memory. Mochi's Cell handles work the same as in native code. Heavier, but matches the MEP-40 design literally.

For Phase 1 with WasmGC, the runtime/vm3 arena is unused; the Wasm engine becomes the arena. The Cell handle (8 bytes) maps to an anyref or a typed (struct $cell) ref.

Custom sections to emit:

- `name`: Mochi function and local names for stack traces.
- `producers`: language=mochi, version=<VERSION>, processed-by=<toolchain>.

## §7 Open questions for MEP-42

1. WasmGC (Wasm 3.0) vs linear memory? Already discussed in target file 06. Recommend WasmGC for Phase 1.
2. Components in Phase 1 or just core modules? Recommend core modules in Phase 1; components in Phase 2 when WASI 1.0 ships.
3. Debug info: DWARF in custom sections (works in Chrome DevTools and Wasmtime) vs source maps (works in browser only)? Recommend DWARF in Phase 2; no debug info in Phase 1 to keep modules small.
4. WAT round-trip in Mochi's test suite? Recommend yes; cheap and catches encoding bugs early.
5. Validation tool: shell out to wasm-validate, or vendor a Go validator? Recommend shell out in Phase 1; consider vendoring later.
