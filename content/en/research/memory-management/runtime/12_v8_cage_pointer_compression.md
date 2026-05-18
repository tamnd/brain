---
title: "V8 Pointer Compression Cage"
description: "A direct ancestor of vm3's 32-bit slab index. V8 squeezes 64-bit pointers down to 32-bit offsets within a per-isolate 4 GB virtual region (the \"cage\"). Cut V8's heap by 43%, Chrome renderer memory by 20%."
tags: ["memory-safety", "runtime"]
weight: 120
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- V8 team at Google. Igor Sheludko, Toon Verwaest, Tobias Tebbi et al.
- Blog post (canonical): https://v8.dev/blog/pointer-compression.
- Oilpan companion: https://v8.dev/blog/oilpan-pointer-compression.
- Shipped initially in V8 v8.0; default-on V8 v9.2 (shared-cage mode).
- Multi-cage / IsolateGroups: Dmitry Bezhetskov, https://dbezhetskov.dev/multi-sandboxes/.
- Related: Node.js issue tracker #55735 on multi-cage isolate groups.

## §2 Mechanism

V8's heap pointers used to be raw 64-bit `Object*`. Pointer compression replaces them with 32-bit "compressed pointers" (`Tagged_t`) interpreted as offsets within a 4 GB **cage**:

```
full_ptr = base + zext32(compressed_ptr)
```

The cage is a 4 GB virtually-contiguous region reserved at isolate startup. Every V8 heap object is allocated within. With the base held constant per isolate (and per process, in shared-cage mode), `compressed_ptr` alone uniquely identifies the object.

Smi (small integer) tagging coexists: the low bit of a compressed value distinguishes pointer vs Smi. Heap objects align to 8 bytes; tagged values use bit 0 = 1 for heap, bit 0 = 0 for Smi.

**Shared-cage mode** (default since V8 9.2): all isolates in a process share one 4 GB cage. This was done to prototype shared-memory JS features. Caps total V8 heap *across all threads* at 4 GB — uncomfortable for server workloads.

**Multi-cage mode / IsolateGroups**: each `IsolateGroup` owns its own cage, lifting the 4 GB total cap. The V8 Sandbox (file 08) extends multi-cage to give each group its own sandbox. Multi-cage is opt-in.

The "40-bit pointer" reference in the prompt is a slight misremembering — V8 itself uses **32-bit compressed pointers in a 4 GB cage**. Oilpan can extend the cage to 16 GB without changing the encoding (because Member<T> stores 32-bit offsets to *8-byte-aligned* objects, effectively 35-bit reach, but the architectural number is "4 GB" with room to grow).

## §3 Memory-safety property

Pointer compression by itself is a **memory-density** feature, not a memory-safety feature. Adding a sandbox on top (the V8 Sandbox, file 08) turns the cage into a security boundary, but that's a separate layer.

However, the cage *does* incidentally limit some bug classes: an OOB write that scribbles a corrupted compressed pointer still points somewhere inside the 4 GB cage, not into arbitrary process memory. This is the seed that the V8 Sandbox grew from.

## §4 Production status (May 2026)

- Pointer compression default-on in V8 since v8.0 (~2020).
- Shared-cage default since v9.2 (2021).
- Multi-cage available since 2022, used by Node.js for worker-thread isolation.
- Combined with the V8 Sandbox (file 8), shipped to billions of users via Chrome 123+ (April 2024).
- Empirical impact (per the V8 blog): **43% reduction in heap size**, **20% reduction in Chrome renderer memory**.
- Real-world Node.js impact: ~50% memory reduction in some server workloads (Platformatic blog, "We cut Node.js' Memory in half").

## §5 Cost

- **Throughput.** Each pointer load gains a shift+add (cage_base + zext32(compressed)). On a modern OOO CPU this is essentially free (folded into address-generation). Speedometer & JetStream show ~0% perf hit, sometimes a small win from cache density.
- **Memory.** -43% V8 heap is the headline.
- **Cache footprint.** Big win. More objects per cache line, more useful work per L2 fetch.
- **Address-space cost.** 4 GB virtual per cage. Trivial on 64-bit, was a concern on 32-bit Android (V8 disabled compression there).
- **Multi-cage cost.** Each additional cage = 4 GB more VA reservation; mostly a paper-cost on 64-bit.

## §6 Mochi adaptation note

This is **the** most direct architectural cousin of vm3. The mapping:

| V8 pointer compression | vm3 Cell (MEP-40 §6.1) |
|---|---|
| 4 GB cage = base of pointer | Each typed arena's backing slice (a Go []byte/[]Cell) |
| 32-bit compressed pointer | 32-bit slab index in the Cell |
| Smi tagging (low bit) | Arena tag bits (currently 4 bits) in the Cell — same idea, more types |
| Shared cage (one per process) | We have one VM per process |
| Multi-cage isolate groups | One VM per goroutine, in a future concurrent-Mochi world |
| Cage base in a CPU register | Backing-slice header in a Go local; covered by Go's bounds-check elision |

So vm3 *already implements* pointer compression — in fact, it does better than V8, because:

1. **We don't even need a cage.** Each arena's backing slice has its own base (Go pointer), and the slab index is interpreted relative to *that* base. V8 has one cage because it has one heap; we have N arenas, each with its own implicit cage.
2. **Generation tag for ABA defence.** V8's compressed pointer has no temporal-safety bit; ours has 12. We get UAF detection for free.
3. **No 4 GB cap.** Each arena can grow to 2^32 slots × per-slot-size, and we have 16 arenas. The aggregate ceiling is 64+ GB without any multi-cage gymnastics.

The smallest patch shape for MEP-41 is essentially "do nothing, claim the win":

1. **Document the architectural lineage.** MEP-41 should explicitly cite V8 pointer compression as the design ancestor of MEP-40's Cell. Saves a generation of reviewers from re-deriving the rationale.
2. **Inline-storage optimisation à la i31ref.** V8 packs Smis directly in compressed-pointer slots. vm3's typed register banks already do this for primitive types, but a future "compact list of small ints" could use a special arena tag where the "slab index" *is* the value. Tiny patch in `runtime/vm3/accessors.go` and a new opcode.
3. **JIT-friendliness.** vm3jit (MEP-40 Phase 5) should compile slab-index dereferences to the V8 idiom: `mov rdi, [r_base + r_index * stride]`. AArch64 has the `add x, base, index, lsl #N` form that does it in one instruction. The arena base lives in a callee-saved register for the lifetime of a function.

No conflict with design ethos — this is one of the strongest validations of vm3's bet.

## §7 Open questions for MEP-41

- Should we adopt V8's "Smi" packing for `int` types, eliminating the typed register banks for ints? Saves register-bank complexity but loses some JIT codegen opportunities.
- Multi-cage mode's main use case in V8 is allowing isolates > 4 GB total. Mochi's per-arena design already gives us this. What threading model would benefit from explicit multi-vm?
- Should arena backing slices be `[]Cell` (typed) or `[]byte` (untyped)? Today they're typed; V8's cage is byte-indexed. Typed gives us better Go bounds-check codegen, untyped gives us packing flexibility.
- Cage-base-in-register: how do we make sure Go's escape analysis keeps the arena slice header live in a register through a hot loop? Inspect a few benchmarks' generated assembly.

## Sources

- [Pointer Compression in V8 (V8 blog)](https://v8.dev/blog/pointer-compression)
- [Pointer compression in Oilpan (V8 blog)](https://v8.dev/blog/oilpan-pointer-compression)
- [V8 release v9.2 (shared-cage default)](https://v8.dev/blog/v8-release-92)
- [Electron and the V8 Memory Cage](https://www.electronjs.org/blog/v8-memory-cage)
- [Multi-cage mode and multiple sandboxes — Dmitry Bezhetskov](https://dbezhetskov.dev/multi-sandboxes/)
- [Pointer Compression and Isolate Groups (Node.js issue 55735)](https://github.com/nodejs/node/issues/55735)
- [We cut Node.js' Memory in half (Platformatic blog)](https://blog.platformatic.dev/we-cut-nodejs-memory-in-half)