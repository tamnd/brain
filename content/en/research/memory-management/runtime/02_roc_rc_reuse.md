---
title: "Roc — Perceus in production-ish"
description: "The biggest real-world deployment of Perceus reference counting, layered with Morphic alias analysis and \"seamless slices\" so functional code rarely allocates."
tags: ["memory-safety", "runtime"]
weight: 20
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Roc language.** Designed by Richard Feldman et al., compiler in Rust, runtime in Zig.
- The reference-counting + reuse pass is a direct port of Perceus (Reinking, Xie, de Moura, Leijen, PLDI 2021).
- Alias analysis: **Morphic**, a Rust library developed at UC Berkeley (Sullivan et al.). The thesis "Reference Counting with Reuse in Roc" (Utrecht student thesis, https://studenttheses.uu.nl/bitstream/handle/20.500.12932/44634/Reference_Counting_with_Reuse_in_Roc.pdf) documents Roc-specific tweaks.
- Repo: https://github.com/roc-lang/roc — latest tag in early 2026 is alpha4 (Aug 2024).
- Marketing page: https://www.roc-lang.org/fast.

## §2 Mechanism

Roc layers four passes over Perceus:

1. **LLVM-Morphic alias analysis.** Before the RC pass runs, Morphic computes which references can alias which. Functions are duplicated (monomorphised) on their alias signatures so the RC pass sees as much uniqueness as possible.
2. **Perceus RC insertion.** Same as Koka — explicit `inc` / `dec` / `dec_reuse` instructions inserted into the IR.
3. **Reuse analysis with join points.** The Roc thesis describes treating tag-union pattern matches as join points so each branch can reuse the matched-on cell. This catches cases the original Perceus paper missed (different constructor shapes, same size class).
4. **Seamless slices.** A `List U8` slice is *not* a new allocation — it is a fat pointer into the parent. The RC discipline treats slices as borrowed views of the parent until they outlive it; only then is the slice promoted to its own allocation. Compile-time analysis decides which case applies.

Roc's runtime is a small Zig blob: it provides the allocator (`roc_alloc`, `roc_dealloc`, `roc_realloc`), panic, and dbg facilities. There is no GC, no thread runtime, no green threads. The host (a Rust program, a Node module, the Roc CLI itself) supplies the allocator. This is the "platform" model: language runtime stays tiny, host owns the OS.

## §3 Memory-safety property

Same as Perceus: precise, deterministic, garbage-free RC, no UAF, no double-free, no leaks except cycles. Roc's type system disallows cyclic types in the same way as Koka (immutable inductive ADTs), so cycles can only arise via opaque host pointers — which the platform vendor is responsible for.

Spatial safety on lists and strings comes from bounds-checked accessors plus the seamless-slice invariant (a slice never extends past the parent's length).

## §4 Production status (May 2026)

Roc is still pre-1.0. From a Jan 2025 Changelog interview and the official `/plans` page:

- 0.1.0 (first numbered release) is the next milestone — targeted for "sometime in 2026," after Advent of Code 2025 forced an interim usable build of the rewritten compiler.
- Alpha line rolls: alpha2 → alpha3 → alpha4 each represent a breaking change. Latest binary is alpha4 (Aug 2024) but the website warns it is being updated for the new compiler.
- Feldman: "There actually are people using Roc in production right now — a very, very small group — but we've actively tried to discourage that."
- Tooling shipped: LLVM backend complete, Morphic complete, Perceus complete, TCO+TCMC complete. WASM target is a stretch.
- The Roc team has expressed interest in improving Morphic itself.

So: Roc is the most ambitious production attempt at Perceus, but as of May 2026 it has not crossed the 1.0 line. The technique is validated; the language is not yet GA.

## §5 Cost

- **Throughput.** Roc's compiled output is roughly in the OCaml/Swift range, with the Perceus papers showing within 0-30% of OCaml on functional benchmarks.
- **Memory.** Low and predictable. No stop-the-world. Peak RSS often half of a tracing-GC equivalent.
- **Latency.** Same caveat as Perceus: recursive `dec` of a long unique linked list is O(n) and synchronous. Roc does not yet implement LXR-style deferred decrements.
- **Compile time.** Morphic and reuse analysis are expensive — Morphic itself is identified as a perf bottleneck for the Roc compiler. AOT cost is paid once.

## §6 Mochi adaptation note

Two ideas from Roc translate directly to vm3:

1. **Seamless slices for `list[T]` and `string` in vm3 (MEP-40 §6.1).** Today every `list.slice(i, j)` allocates a new handle into the list arena. With seamless slicing, the slice is just a `(parent_handle, start, len)` triple living in the typed register bank — *no arena allocation*. Promotion to a real slab entry happens lazily, on first mutation or when the parent is dropped. This is a pure compiler3 + accessor change; the arena code in `runtime/vm3/alloc.go` does not need to change. The Cell layout (§6.1) gains a new arena tag `kArenaSlice` whose 32-bit "slab index" actually encodes a packed (start, len) into a separate slice-descriptor table.
2. **Monomorphisation on uniqueness signatures.** Mochi already monomorphises generic functions by type. Add a second axis: "this `list[T]` parameter is uniquely owned vs borrowed." That mirrors Morphic without the heavy alias-graph solver. Roc shows this is enough for most reuse opportunities. It maps onto compiler3 §7.2's type-driven lowering pass: tag the IR types with `Unique | Borrowed`, monomorphise, then let the existing Perceus-style emit do its thing.

No design conflict — Roc is itself host-language-agnostic (its runtime is a few Zig functions). Mochi's Go-hosted model is friendlier than Roc's "you write a platform in Rust" model because Go's GC owns the backing slices for free.

## §7 Open questions for MEP-41

- Is the Roc seamless-slice trick worth the accessor-layer complexity, given that vm3's slab indices are already 32 bits? Concretely: does it cut allocator pressure enough on Mochi corpus benchmarks to pay back the new arena tag?
- Roc's RC + reuse only catches "same size class" reuse. Should vm3 partition arenas by size class (like jemalloc) to widen the reuse window, or stay with per-type arenas?
- Roc has chosen *not* to ship a cycle collector. Should Mochi follow, given that user-defined cycles in Mochi can only come through `&mut` self-loops in mutable structs (rare)?
- Does Morphic's Rust implementation port to Go cleanly, or do we want a simpler intra-procedural uniqueness pass for compiler3?

## Sources

- [Roc — Fast](https://www.roc-lang.org/fast)
- [Roc — Planned Changes](https://www.roc-lang.org/plans)
- [Roc on GitHub](https://github.com/roc-lang/roc)
- [Reference Counting with Reuse in Roc (Utrecht thesis)](https://studenttheses.uu.nl/bitstream/handle/20.500.12932/44634/Reference_Counting_with_Reuse_in_Roc.pdf)
- [Changelog #645 — The Roc programming language with Richard Feldman](https://changelog.com/podcast/645)
- [Perceus PLDI'21 paper (basis)](https://xnning.github.io/papers/perceus.pdf)