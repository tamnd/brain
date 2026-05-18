---
title: "Source Maps and DWARF for WebAssembly"
description: "The two competing approaches to debugging Wasm, and why DWARF won inside Chrome."
tags: ["native-codegen", "debug"]
weight: 30
date: 2026-05-18T18:13:12+07:00
---

## §1 Provenance

- Chrome DevTools Wasm DWARF doc: https://developer.chrome.com/docs/devtools/wasm/
- Chrome blog (2020) "Improved WebAssembly debugging": https://developer.chrome.com/blog/wasm-debugging-2020
- Chrome blog (2019) precursor: https://developer.chrome.com/blog/wasm-debugging-2019/
- C/C++ DevTools Support extension: https://chrome.google.com/webstore/detail/cc++-devtools-support-dwa/pdcpmagijalfljmkmjngeonclgbbannb
- Source maps v3 spec: https://sourcemaps.info/spec.html
- DWARF in Wasm extension (originally a custom section `external_debug_info` and embedded `.debug_*` sections): tracked at https://github.com/WebAssembly/tool-conventions/blob/main/Debugging.md
- Node Wasm debugging tracker: https://github.com/nodejs/node/issues/37984

## §2 Mechanism / function

WebAssembly debugging has two formats in flight:

Source maps (the older approach) were originally designed for minified JavaScript. They are a JSON file listing a mapping from generated-code (file, line, column) tuples back to original (file, line, column) tuples. The mappings are VLQ-encoded to keep the JSON small. A Wasm module can reference a source map via the `sourceMappingURL` custom section (a name and a URL).

Source maps for Wasm have hard limits: they cannot describe types, variable layouts, scopes, or anything beyond "the byte at offset N in the .wasm came from line L of file F". For minified JS this is enough; for compiled C/C++/Rust/Zig it is not.

DWARF in Wasm (the modern approach) embeds the standard DWARF debug sections inside the Wasm module as custom sections named `.debug_info`, `.debug_line`, etc. The exact byte layout is the standard DWARF 4/5 layout described in `debug/01_dwarf_5.md`. The Wasm wrapper adds nothing beyond putting them in custom sections.

For separated debug info, the `external_debug_info` custom section (one URL) tells the debugger to fetch the DWARF from a separate `.wasm` file. Emscripten supports this via `-gseparate-dwarf=<filename>`.

The Chrome DevTools "C/C++ DevTools Support (DWARF)" extension is a privileged DevTools extension that reads the embedded DWARF, decodes it with LLVM's DWARF library compiled to Wasm, and feeds DevTools the source-mapping, scope, and type info needed for source-level debugging.

## §3 Platform coverage (May 2026)

DWARF in Wasm:

- Producers: Emscripten (`emcc -g`), Clang (`clang --target=wasm32 -g`), Rust (`-Cdebuginfo=2`), Zig.
- Consumers: Chrome (with the C/C++ DevTools Support extension), Firefox (read-only DWARF support landed in Firefox 116, 2023, with continued improvements through 2025), Safari (limited; lags behind Chrome).
- Node.js: long-standing gap (issue 37984 from 2021 still partially open). Source maps work; DWARF stack frames in panics do not show file/line.
- Server-side: wasmtime and wasmer can read DWARF for `wasmtime run --debug`.

Source maps:

- Producers: Emscripten (with `-gsource-map`), wasm-pack for Rust (limited; no DWARF transform).
- Consumers: every browser DevTools, plus Node.js inspector.
- Use case: minified-but-not-compiled Wasm, or as a fallback when DWARF tooling is not installed.

## §4 Current status (May 2026)

The Chrome 114 (May 2023) release made DWARF Wasm debugging non-experimental: the "Enable DWARF support" setting is on by default. Subsequent Chrome releases through 2025 and into 2026 have polished the UX, added path-mapping for container builds, and improved performance.

For Rust developers in 2025, the C/C++ DevTools Support extension is the recommended tool even though it is C/C++-branded (Rust DWARF is compatible). The wasm-bindgen toolchain does not yet rewrite DWARF when it transforms the Wasm, which is a known limitation but does not prevent basic debugging.

Performance caveat: opening DevTools causes Wasm to "tier down" to an unoptimized version. This is necessary for breakpoints and stepping but makes timing measurements unreliable while debugging.

Node.js (May 2026): still lacks Wasm DWARF stack-frame symbolication. Source maps work for JS but not for C++ source lines in Wasm panics. This is a frequently cited gap.

## §5 Engineering cost for Mochi

If Mochi ever has a Wasm target (Phase 2 or Phase 3 question), the debug story is:

- Use DWARF in Wasm custom sections. Same DWARF emitter we built for native targets (see `debug/01_dwarf_5.md`) outputs to the same byte format.
- Wrap the resulting bytes in a Wasm custom section. Wasm custom sections are length-prefixed name+bytes; trivial to emit.
- Document that Chrome with the C/C++ DevTools Support extension is the recommended debugger.
- Optionally emit a source map as well, for browsers without the extension.

The cost is essentially free if we already have a DWARF emitter. The Wasm-specific code is the custom section wrapper.

The `external_debug_info` separated-DWARF mode keeps the runtime `.wasm` small, which matters for browser download size.

## §6 Mochi adaptation note

For a Mochi-to-Wasm target:

1. Reuse `compiler3/emit/dwarf` from the native path.
2. Add `compiler3/emit/wasm` that produces the Wasm module (a `Module` section structure per https://webassembly.github.io/spec/core/binary/modules.html).
3. Concatenate the DWARF bytes as custom sections at the end of the Wasm module.
4. Optionally emit a `.wasm.map` source map file for the basic source-file-and-line case.
5. Document Chrome + C/C++ DevTools Support extension as the supported debug environment.

Mochi already has `compiler/wasm` (legacy) and could reuse some of that scaffolding. The MEP-42 native path and the Wasm path share most of the DWARF code.

## §7 Open questions for MEP-42

- Is Wasm a Phase 1 target or Phase 2? My read: Phase 2 or later, given the focus on native binaries first.
- Do we emit both DWARF and source maps, or pick one? Both, since the marginal cost of source maps is low.
- Do we ever produce a `.dwp` (DWARF Package) for split-DWARF in Wasm? Probably not; the Wasm custom-section approach is simpler.
- Node.js gap: do we wait for Node to fix Wasm DWARF, or just document the limitation?

Sources:
- [Chrome DevTools: Debug C/C++ WebAssembly](https://developer.chrome.com/docs/devtools/wasm/)
- [Chrome blog: Debugging WebAssembly with modern tools (2020)](https://developer.chrome.com/blog/wasm-debugging-2020)
- [Chrome blog: Improved WebAssembly debugging (2019)](https://developer.chrome.com/blog/wasm-debugging-2019/)
- [Wasm tool-conventions Debugging.md](https://github.com/WebAssembly/tool-conventions/blob/main/Debugging.md)
- [Source maps v3 spec](https://sourcemaps.info/spec.html)
- [Node.js Wasm DWARF tracking issue 37984](https://github.com/nodejs/node/issues/37984)
- [What's New in DevTools (Chrome 114)](https://developer.chrome.com/blog/new-in-devtools-114)