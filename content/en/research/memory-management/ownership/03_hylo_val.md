---
title: "Hylo (formerly Val)"
description: "Mutable value semantics with subscript-based projection borrowing, no lifetime variables, and the Law of Exclusivity enforced at call sites."
tags: ["memory-safety", "ownership"]
weight: 30
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Authors**: Dimitri Racordon, Dave Abrahams, Sean Parent, et al. Originally proposed in WG21 paper **P2676R0** (Oct 2022), https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2676r0.pdf .
- **Project home**: https://hylo-lang.org/ . Tour: https://docs.hylo-lang.org/language-tour/ . Specification: https://github.com/hylo-lang/specification/blob/main/spec.md .
- **Renamed Jan 2024**: Val → Hylo, to disambiguate from other "Val" projects.
- **Object-model doc for Swift designers**: https://github.com/hylo-lang/Documentation/blob/main/object-model-for-swift-designers.md .
- **Discussion on Rust comparison**: https://github.com/orgs/hylo-lang/discussions/788 .

## §2 Core type discipline

Hylo has **only** value types. There are no reference types in the source language; therefore the surface algebra is just regular product/sum types plus *projections*.

Annotation surface lives on **parameters** and **subscripts** only:

- `let x: T`  — borrow `x` immutably for the call.
- `inout x: T` — borrow `x` mutably; caller cannot touch the same storage until call returns.
- `sink x: T`  — consume `x`; equivalent to a Rust move.
- `set x: T`   — write-only out-parameter.

There are no lifetime variables. A function's signature alone determines all aliasing constraints.

Subscripts are the projection mechanism. Instead of returning a reference (which Hylo refuses to do), a subscript **yields**:

```
subscript longer_of(_ a: String, _ b: String): String {
    if a.count > b.count { yield a } else { yield b }
}
```

The caller receives temporary read or read/write access scoped to a single expression. Mechanically, `subscript` is sugar for a closure-passing inversion of control.

Judgement form (the **Law of Exclusivity**): for every projection `p` over object `o` at program point `P`, if `p` is `inout` then `o` is *unreachable through any other path* until `p` ends; if `p` is `let` then `o` is read-only via every path until `p` ends. The check is intra-procedural and structural.

Principal example: `swap(&xs[i], &xs[j])` — Rust requires `split_at_mut` or `unsafe`. Hylo just types `inout xs[i]`, `inout xs[j]`, sees the index expressions are different at the call site, and accepts.

## §3 Memory-safety invariant

Aliasing-XOR-mutation, but proven via a *whole-value disjointness* check rather than a borrow graph. No data races (single-thread safe subset), no UAF (no references to lose), no dangling pointer (the same reason).

The deep claim — the slogan "independence is the true source of fearless concurrency" — is that mutable value semantics gives you the Rust property for free because there are no aliases to police.

## §4 Compiler implementation cost

- The Hylo compiler is in Swift, ~50k LOC; the projection/exclusivity check is a single MIR-level pass over the SSA form.
- No region inference, no constraint solver, no datalog. The check is purely structural: at every call, do the projections name overlapping access paths?
- Diagnostics are local: the error always names the two conflicting access paths and the call site. No multi-page error explanations needed.
- Cost of moving a value: a memcpy. Hylo bets that the compiler's mem2reg + dead-store elimination removes most of them. There is no `Box<T>` discipline; the type-checker assumes by-value.

The cost the user pays is **expressiveness**: graphs, cycles, and shared mutable observers are awkward (you encode them through indices into a value-typed table).

## §5 Production / language adoption status (May 2026)

- Hylo is research-stage. No production deployments known. The compiler self-hosts limited examples; the standard library is a few thousand lines.
- The ideas have hard influence: Swift's `consuming`/`borrowing` (SE-0377) is directly cross-referenced in Hylo's spec, and Swift's law of exclusivity (SE-0176, stable since Swift 5) is the operational precedent.
- Active research community at SPLASH / PLDI workshops; no major language has adopted projections wholesale.

## §6 Mochi adaptation note

Hylo's MVS does **not** map onto Mochi because Mochi's lists, maps, structs, and closures are all reference types under the hood — they are handle Cells. Trying to bolt MVS on top of handle-arena semantics would require deep-copy-on-pass, killing performance and breaking the JIT.

Pieces that **do** map:

- **`inout` parameter convention**. Cheap to add to `types/check.go`. The check is: at a call site, no two `inout` arguments resolve to handle Cells that may alias. Aliasing of handle Cells is exactly handle-equality, which is computable. This catches `swap(xs[i], xs[i])` statically and gives Mochi a real "the callee may mutate this" annotation without any lifetime story.
- **Subscript / projection**. Mochi could ship a `subscript` keyword that desugars to a callback-style closure call. Use case: iterate-and-mutate over a slot of a struct without copying the whole struct. This pairs with vm3's accessors (`runtime/vm3/accessors.go`) which already do field-by-handle access.
- **`sink` parameter**. Same as Rust's "by move"; for handle types, the VM just bumps the gen of the source slot. This is the cheapest possible move semantics.

Incompatible pieces:

- The "no reference types" core premise. Mochi's list is a handle; passing it by value would mean deep-cloning the slab.
- Projection-based maps. Hylo's map indexing is a subscript that yields; Mochi's `m[k]` already returns `Option<V>` per MEP-16. Layering exclusivity on top would change the operator's signature.

Surface-syntax change MEP-41 should adopt verbatim from Hylo: the parameter qualifiers `inout`, `sink`, `let` (already implicit). They are tiny, orthogonal to types, and they encode caller intent the type checker can verify.

MEP-15 tie-in: an `inout` parameter is a write-effect on the parameter's storage. MEP-15's effect set could grow a single "mut: P" effect for each `inout` parameter and reject calls where two mut-effects target the same handle.

MEP-16 tie-in: a `sink` parameter on an `Option<T>` is the move-out story for `Option`. Combined with MEP-16's no-force-unwrap, this gives a `take(): T` that statically nulls the source without runtime cost.

## §7 Open questions for MEP-41

1. Is `inout` worth the syntactic noise on a GC'd language? Most Mochi mutations go through container methods that already encode mutation.
2. Should the exclusivity check be inter-procedural? Hylo says no (one call frame at a time). MEP-41 should follow.
3. Can MEP-41's `subscript` desugar to the same closure-passing pattern, and if so, can vm3 inline it the way the JIT already inlines small closures?
4. What is the diagnostic story when two `inout` parameters appear to alias because they are the same handle Cell?

Sources: https://hylo-lang.org/ ; https://github.com/hylo-lang/Documentation/blob/main/object-model-for-swift-designers.md ; P2676R0 PDF ; https://docs.hylo-lang.org/language-tour/subscripts .