---
title: "Austral"
description: "Strict linear types as the load-bearing primitive for memory and protocol safety, plus capability-based effect control. Spec-and-compiler-small enough to read in a weekend."
tags: ["memory-safety", "ownership"]
weight: 50
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Author**: Fernando Borretti.
- **Reference site**: https://austral-lang.org/ . Spec: https://austral-lang.org/spec . Features: https://austral-lang.org/features .
- **Introduction post**: https://borretti.me/article/introducing-austral .
- **Implementation post**: https://borretti.me/article/how-australs-linear-type-checker-works (the linear checker is **<600 LOC** of OCaml).
- **Long essay** on why this matters: https://borretti.me/article/type-systems-memory-safety .
- **External comparison**: https://verdagon.dev/blog/linear-types-borrowing by Evan Ovadia.
- **HN thread**: https://news.ycombinator.com/item?id=34168452 .
- **Repo**: https://github.com/austral/austral .

## §2 Core type discipline

Austral has a single concept doing all the work: **strict linear types**. The discipline is reduced to two rules:

1. **Linear Universe Rule** — every type lives in exactly one of two universes, *Free* (ordinary, droppable, copyable) or *Linear* (use-once, must be consumed). Mixing is via explicit borrows.
2. **Use-Once Rule** — a linear value must be used exactly once. Not zero times (no leaks), not twice (no use-after-free / double-free / iterator invalidation).

Annotation surface:

- Types declare their universe: `type FileHandle: Linear`.
- Variables of linear type cannot be assigned, returned, or stored without consuming the source.
- Borrow: `borrow!` and `borrow-write!` are scoped macros/forms that lend a linear value as a non-linear reference for a lexical block. The borrow region is purely lexical (no NLL, no Polonius).

Judgement form: a flow-sensitive count of uses across the AST. Each linear binding must reach exactly one consuming use on every control path. The check is a single recursive descent.

Principal example — file handle protocol enforced at compile time:

```
let f: FileHandle := open("a.txt");
let f': FileHandle := write(f, "hello");   -- f is consumed, f' takes its place
close(f');                                  -- f' consumed; binding becomes unusable
-- writing close(f) would be rejected: f is already consumed
```

The same machinery enforces double-free freedom, leak freedom, use-after-free freedom, and protocol invariants (`Closed -> Open -> Writing -> Closed` etc.) with no extra typing rule.

Capability-based security composes on top: a `RootCapability: Linear` value is needed to mint `FilesystemCapability`, which is needed to call `open`. Capabilities are linear, so they can be subdivided (`split`) and consumed. No ambient authority.

## §3 Memory-safety invariant

- **No use-after-free**: a consumed value's binding does not type-check at later uses.
- **No double-free**: the value is consumed once.
- **No leak**: the value must be consumed (closed/deallocated) on every path.
- **No data race**: a linear value can be in only one place; no aliasing means no race.
- **Capability isolation**: side effects need a linear capability; the capability is the proof.

The trade-off: every protocol becomes part of the type. Graphs and cycles are awkward — linear types can directly represent only **trees**. Cyclic data structures need indices into a separately-managed pool.

## §4 Compiler implementation cost

- Spec: short. Compiler (OCaml): small.
- Linear checker: **<600 LOC** including borrow handling. Compare to Rust's borrow checker (multi-tens-of-thousands).
- Error messages are easy because the discipline is local: "you used `f` twice; first at line N, second at line M".
- No region inference, no constraint solver. The checker is essentially a use-counter with a `match` on each AST shape.
- Diagnostic quality is excellent because there is no inferred state to explain.

The cost shows up at the *use site*: every protocol step must thread the linear handle through return values. Borretti himself calls linear types "onerous to write".

## §5 Production / language adoption status (May 2026)

- Austral is research-stage; one bootstrapping OCaml compiler. The author keeps a small std lib and capability-based filesystem demo.
- No known industrial deployment.
- Influence: Austral is cited in nearly every recent ownership-design discussion (Vale, Inko, Hylo, Mojo) as the reference point for "strict linear, simple checker".

## §6 Mochi adaptation note

Full strict linearity is **incompatible** with Mochi: Mochi has GC, lists are aliasable, and most user code passes structures around by handle copy. Forcing every value to be consumed exactly once breaks every existing fixture.

Pieces that map cleanly:

- **A linear sub-universe for capabilities / resources**. MEP-41 could introduce a `linear` keyword that marks a type as use-once. The checker tracks one bit per binding: `consumed` or `live`. The runtime does nothing different. Cost: ~200 LOC in `types/check.go`, modelled exactly on Austral's checker.
- **Capability-based effects**. MEP-15 already has effect labels. Austral's lesson: tying an effect to a linear capability value makes the effect *constructive*. A function with effect `io` would, in this model, take a `linear IoCap` parameter. The effect set is then the set of capability types the function consumes.
- **Protocol typing**. The classic `FileHandle` example would type-check in Mochi if `FileHandle` were `linear`. Today Mochi catches double-close at runtime; with this change it catches at compile time.

Incompatible:

- All current container types being linear. Wrong default.
- Strict-linearity at the user-data layer. The handle Cell is freely copyable in vm3; making it linear means breaking the JIT's spill/restore.

Surface-syntax change: one keyword, `linear`. Apply it to a type declaration; the checker treats every binding of that type as a use-once linear value, and the existing handle-Cell representation in vm3 is unchanged. The runtime safety net (gen check) catches any holes the static check missed.

MEP-15 tie-in: rewrite the effect surface as "function `f` has effect `e`" iff "function `f` consumes a `linear E` capability". This is a more principled story than the labelled-set version and admits user-defined effects naturally.

MEP-16 tie-in: a `linear Option<T>` is the natural type for a one-shot result (a continuation, a `Promise`). The take/match pattern collapses to a single linear consume.

## §7 Open questions for MEP-41

1. Should `linear` be a per-type modifier (Austral style) or a per-binding modifier (linear-Haskell style)?
2. How do we mix `linear` types with Mochi's existing generics? Austral has no generics in the original spec; Borretti's later work adds them through restricted instantiation.
3. Can MEP-15 effects be re-derived as linear capabilities, or is that too disruptive for stage 1?
4. Does MEP-41 need a *graph-friendly escape hatch* (e.g. `weak linear T`) for cyclic data? Vale's lesson: cycles need a different mechanism.

Sources: https://austral-lang.org/ ; https://austral-lang.org/spec ; https://borretti.me/article/introducing-austral ; https://borretti.me/article/how-australs-linear-type-checker-works ; https://github.com/austral/austral .