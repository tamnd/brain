---
title: "Vale Generational References"
description: "The direct intellectual ancestor of vm3's handle design: a per-allocation generation counter, a per-reference remembered generation, and a check on every dereference. Same idea, different layer."
tags: ["memory-safety", "ownership"]
weight: 20
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Author**: Evan Ovadia.
- **Canonical write-up**: "Vale's Memory Safety Strategy: Generational References and Regions", https://verdagon.dev/blog/generational-references (originally Aug 2021, updated July 9 2023). Earlier v1 at https://verdagon.dev/blog/generational-references-v1 .
- **Project page**: https://vale.dev/vision/safety-generational-references and the Linear-Aliasing Model, https://vale.dev/linear-aliasing-model .
- **Memory Safety Grimoire** (Apr 24 2024): a survey of 14 memory-safety techniques, https://verdagon.dev/grimoire/grimoire .
- **2024 follow-up**: "Zero-Cost Memory Safety with Vale Regions, Part 1: Immutable Region Borrowing", https://verdagon.dev/blog/zero-cost-borrowing-regions-part-1-immutable-borrowing .
- **Cal Poly thesis (2024)**: Theodore C. Watkins, "Reducing Vale's Memory Management Overhead Through Static Analysis", https://digitalcommons.calpoly.edu/theses/2348/ .
- **Podcast (Apr 2024)**: Developer Voices, "Advanced Memory Management in Vale with Evan Ovadia".
- **2024–2025 author status**: From July 2024 through Dec 2025 Ovadia worked on Modular's Mojo, adding linear types, associated aliases, struct extensions, and CPU/GPU boundary type-checking. Vale itself is paused while he explores group borrowing and new blends.

## §2 Core type discipline

There is no annotation surface. Every allocation carries a `currentGeneration: u64` field above the user payload. Every non-owning reference is a fat pointer `(ptr, rememberedGen: u64)`. On free, the allocator increments `currentGeneration`. On every dereference, the compiler emits:

```
assert(*((u64*)alloc - offsetToGen) == ref.rememberedGen);
```

Owning references do not carry a remembered gen; they are unique by construction and their lifetime is the structural owner's lifetime, so the check is unnecessary. The discipline is therefore:

- **Owning ref**: unique, no gen, drop runs at scope exit.
- **Generational ref (non-owning)**: arbitrary aliasing, dynamic liveness check at use.

Judgement form: trivial. There is no borrow checker. The type system is a normal Hindley–Milner-ish system with sum types; the safety property is enforced *dynamically*.

Principal example: an observer can keep a generational ref to a target. Target frees; observer's next call panics at the check site with a useful stack trace instead of triggering UB. Same code in Rust requires `Rc<Weak<RefCell<…>>>` and gymnastics.

## §3 Memory-safety invariant

**No use-after-free, ever, on any reference, with negligible memory overhead.** The check is total: stale handles always fail. UAF and double-free both reduce to the same generation-mismatch trap.

What it does **not** preserve: aliasing-XOR-mutation, capability isolation, data-race freedom. Multiple actors can mutate through generational refs; Vale solves data races by combining generational refs with regions (immutable region borrowing skips checks and statically forbids writes for the duration of the borrow).

## §4 Compiler implementation cost

Microscopic. The compiler emits a check-call on every dereference unless it can prove the check redundant. The runtime cost was measured on the BenchmarkRL terrain generator against the same program compiled with three different memory strategies:

| Mode               | Time (s) | Overhead vs unsafe |
|--------------------|---------:|-------------------:|
| `unsafe-fast`      |  43.82   | —                  |
| `naive-rc`         |  54.90   | +25.29 %           |
| `resilient-v3` (GR)|  48.57   | +10.84 %           |

Newer write-ups summarise as **2–10.84 % overhead** depending on access patterns. The regions prototype eliminates every check in tight loops and approaches zero overhead.

Per-allocation memory cost: 8 bytes for the leading generation field. Per non-owning reference: 8 bytes for the remembered generation alongside the pointer. Vale notes most refs in a healthy program are owning, so the multiplicative pressure is small.

Error message quality: there is no compile-time error to message — the check failure is a runtime trap with the dereferencing site as PC. The story is "bugs surface immediately on first use rather than as UB".

## §5 Production / language adoption status (May 2026)

- Vale itself: development paused; Ovadia spent 18 months at Modular working on Mojo and is now back exploring "group borrowing".
- Generational references as an *idea* have travelled: they are explicitly cited as inspiration in vm3 (this codebase, `runtime/vm3/cell.go`), and discussed on the D-lang list in 2025 as a candidate safe-by-default reference type.
- No widely-deployed language uses the bare generational ref design in production yet; the closest analogues are tracing GC handles in JVM/.NET, which carry generation bits for collector bookkeeping rather than for safety.

## §6 Mochi adaptation note

This is **the** system that already lines up with vm3. The mapping is line-for-line:

| Vale                                  | vm3 (`runtime/vm3/cell.go`)        |
|---------------------------------------|------------------------------------|
| 64-bit `currentGeneration` per object | 16-bit `gen` field on every slab entry (`vmString.gen`, `vmList.gen`, … in `arenas.go`). |
| 64-bit `rememberedGen` per ref        | 12-bit `gen` packed into the handle Cell at `genShift=32`, `genMask=0xFFF<<32`. |
| Per-deref `assert(curr == remembered)`| `accessors.go` resolves a handle by looking up `arena[idx]` and (in debug mode) comparing the cell's 12-bit gen to the slab entry's 16-bit gen. |
| Free bumps generation                 | Phase 6 mark-sweep collector will bump `gen` on entry reuse (per `arenas.go` doc comment). |
| Owning ref skips check                | Single-owner static slots in the VM (function locals) can skip the gen check; only handles stored into long-lived containers need it. |

The smallest surface-language change MEP-41 needs to capture Vale's safety property is **none at all** — the runtime already pays for it. What MEP-41 should add on top is:

- An optional `weak` keyword on bindings that forces the runtime to keep the gen check even when escape analysis would let the compiler skip it. This is the user telling the compiler "I expect this to dangle some day, don't elide the check".
- A `gc.kill(x)` builtin (gated behind MEP-15 `meta` effect) that bumps the gen *now*, giving deterministic destruction semantics without changing the type system.

Incompatibility: vm3's 12-bit gen wraps every 4096 frees of the same slot. Vale's 64-bit gen never wraps in practice. MEP-41 must call out the wrap window and require Phase 6's collector to reject reuse of any slot whose previous holder is still reachable in the bytecode (which is exactly the GC's existing job).

Effect-system tie-in (MEP-15): a generation trap is a runtime panic, not an effect. MEP-41 should classify "may-trap-on-stale-handle" as an *implicit* effect that purity contexts (query predicates, compile-time constant folding) treat the way they currently treat `io`. This is a generalisation that MEP-15 left open.

Option discipline tie-in (MEP-16): a `try_deref(h: Handle<T>): Option<T>` operator could surface the gen-check failure as `none` instead of a trap. This is exactly the no-force-unwrap discipline of MEP-16 extended one layer down.

## §7 Open questions for MEP-41

1. Should the 12-bit gen be widened to 16 or 24 bits? The Cell layout has headroom in the arena-tag nibble if we restrict arenas to 8.
2. Do we expose generations to user code as a first-class type (`Weak<T>`-like), or keep them entirely internal?
3. The Vale region story buys ~10× compile-time check elision. vm3's BG (basic-block group) pass already does shape inference; can it do generation-check elision too?
4. Does MEP-41 want a `pin` annotation that bumps `gen` only on explicit `unpin`, mimicking the linear-aliasing model? This is the lightest possible borrowing story.
5. How do we surface gen-check failures in the JIT (vm3 MEP-39 deopt path) without breaking the 5–7 % overhead budget?

Sources: https://verdagon.dev/blog/generational-references ; https://verdagon.dev/grimoire/grimoire ; https://vale.dev/vision/safety-generational-references ; https://vale.dev/memory-safe ; Cal Poly thesis https://digitalcommons.calpoly.edu/theses/2348/ .