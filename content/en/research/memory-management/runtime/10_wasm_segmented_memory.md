---
title: "WebAssembly Segmented Memory (and friends)"
description: "The CG-track answer to \"what's beyond a single 4 GB linear memory?\" Multiple memories shipped in Wasm 3.0 (Sep 2025). Memory64 shipped at the same time. A formal \"segmented memory\" proposal in the MSWasm vein has not yet entered the CG track but is influencing design."
tags: ["memory-safety", "runtime"]
weight: 100
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **WebAssembly Community Group (CG) and Working Group (WG).** W3C process.
- **Wasm 3.0** specification — W3C Recommendation, September 24, 2025. Bundles 9 features: WasmGC, exception handling, tail calls, **memory64**, **multiple memories**, 128-bit SIMD, relaxed-SIMD, extended-const, JS Promise integration.
- Proposal repos:
  - https://github.com/WebAssembly/memory64 (phase 4 → merged)
  - https://github.com/WebAssembly/multi-memory (phase 4 → merged)
  - https://github.com/WebAssembly/proposals (master proposal list and status)
- Discussion on integration: https://github.com/WebAssembly/design/issues/1036.
- Status overview: https://webassembly.org/features/.

## §2 Mechanism

Two complementary CG outputs are now standardised; together they get partway to MSWasm's segmented model without the formal-safety claim.

### Multiple memories (Wasm 3.0)

A Wasm module can declare or import multiple `(memory ...)` objects (previously: at most one). Memory instructions like `i32.load`, `memory.grow`, `memory.copy` take an explicit memory index. Data can be `memory.copy`'d between memories. This lets a module:

- Isolate untrusted data (e.g. parsing-buffer memory) from its main memory.
- Run multiple "tenants" inside one module without one tenant's OOB write touching another's data.
- Implement segmented-allocator patterns: every allocation arena gets its own memory.

This is the "poor man's MSWasm" — coarse-grained but cheap. No new types, no fat pointers, no provenance tags.

### Memory64 (Wasm 3.0)

64-bit memory addresses. Loads/stores take `u65` addresses (a u32 base + offset, or u64 with offset). Bounds checks remain mandatory, with the same guard-page trick — but now over a u64 address space.

In practice browsers cap at 16 GB (Firefox/Chrome) per memory. Cloudflare and Fermyon use it for LLM model weights at the edge; video editing and scientific simulation are the other early adopters.

Note: memory64 doesn't get you safer pointers — it just makes them bigger. Bounds-check cost goes up (since browser-style guard pages now cost more virtual address space). The "wasm32 vs wasm64 binaries can't interop" issue (the design discussion) was partially resolved by deferring full unification.

### Segmented Memory (proposed, not yet standardised)

There is **no** CG proposal repo named "segmented-memory" as of May 2026. The phrase appears in:

- Older design discussions about combining multi-memory + atomics + SIMD orthogonally.
- The MSWasm-style "fat pointer" line of research, which depends on segments but hasn't reached the standards track.
- Various blog posts speculating about a future Wasm extension that would give per-segment provenance.

The current CG position: multi-memory + memory64 satisfies the *capacity* requirement, while WasmGC (file 11) satisfies the *typed-pointer* requirement. A separate MSWasm-style segmentation proposal is not actively in CG queues.

## §3 Memory-safety property

Multiple memories gives **modular isolation** — a bug in one memory's bounds check doesn't reach another memory. No provenance, no fat pointers, no temporal safety beyond what the module itself enforces.

Memory64 gives **no new safety**; it's a capacity feature.

The combination is meaningfully weaker than MSWasm: an OOB read *within* a memory still reads neighbouring data. Multi-memory lets you make the radius of damage smaller by partitioning aggressively.

## §4 Production status (May 2026)

- Wasm 3.0 finalised September 2025; full feature set is mostly cross-browser usable in 2026.
- Memory64: Chrome and Firefox stable; Safari still missing as of early 2026.
- Multiple memories: Chrome and Firefox stable; Safari rolling out.
- Standalone runtimes (Wasmtime, WAVM, Wasmer) shipped both proposals through 2024-2025.
- Languages targeting Wasm rarely use multi-memory yet; the toolchains (LLVM, Emscripten) haven't built around it because most C/C++ code expects a single flat memory.

## §5 Cost

- **Multiple memories.** Per-load cost: one extra register lookup for the memory base. Negligible after JIT compilation.
- **Memory64.** Bounds-check cost rises modestly; guard-page trick is more expensive in virtual address space (a 64-bit memory + 32 GB guard = 32 GB VA per memory).
- **No safety overhead** because no new safety is provided.

## §6 Mochi adaptation note

vm3 already implements something more like multi-memory than like a single linear memory: each typed arena (MEP-40 §6.2) is its own memory. The arena tag in the Cell is effectively a memory index. So the conceptual move from Wasm-1.0 single-memory to Wasm-3.0 multi-memory was made by vm3 from day one.

What can vm3 borrow:

1. **`memory.copy` between arenas as a primitive.** Today `runtime/vm3/alloc.go` has 12 typed allocators; we don't have a typed `Copy` that crosses arenas. For Mochi's `bytes ↔ string` conversions and `list[u8] ↔ bytes` (relatively common), an inter-arena bulk copy primitive could be a useful super-op. Tiny patch.
2. **Memory64 lesson on bounds-check guard pages.** Mochi doesn't use mmap'd guard pages — Go owns the backing slices, and bounds checks are explicit. Stay this way; the Wasm guard-page trick adds OS-level complexity for marginal speed.
3. **Multi-memory as security boundary.** Per-arena isolation already gives us the multi-memory security property: a bug in `ListGet` cannot touch the `kArenaString` storage. Worth documenting in MEP-41.

No design conflict; in fact, vm3 has *less* to gain from this proposal because we already have its win.

## §7 Open questions for MEP-41

- Should arena boundaries be advertised as a *security* property of vm3 (i.e., "list memory and string memory cannot collide")? Today it's an implementation detail; making it a guarantee constrains future refactors.
- Memory64-style bounds checking would let us use Go's slice bounds-check elision in tight loops. Is the compiler3 JIT (Phase 5) going to lean on `bounds.Range`-style hints?
- Is there value in modelling vm3 as a *Wasm guest* in some future version (Mochi-on-Wasm with `wasm_of_mochi`)? Multi-memory would give us the arena pattern natively.
- The lack of a formal "segmented memory" CG proposal means vm3 is unlikely to be able to compile to a standardised memory-safe Wasm target soon. MSWasm (file 9) remains the academic anchor.

## Sources

- [WebAssembly Feature Status](https://webassembly.org/features/)
- [WebAssembly/memory64 GitHub repo](https://github.com/WebAssembly/memory64)
- [WebAssembly/multi-memory GitHub repo](https://github.com/WebAssembly/multi-memory)
- [State of WebAssembly 2026](https://devnewsletter.com/p/state-of-webassembly-2026/)
- [WebAssembly 3.0 Officially Released (x-cmd blog)](https://www.x-cmd.com/blog/250924/)
- [Mozilla Intent to ship: memory64](https://groups.google.com/a/mozilla.org/g/dev-platform/c/I-MywEnFxKc)
- [Integrating multiple memories and 64-bit addresses with other extensions (design issue 1036)](https://github.com/WebAssembly/design/issues/1036)