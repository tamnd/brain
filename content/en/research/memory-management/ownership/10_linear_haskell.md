---
title: "Linear Haskell"
description: "Linearity attached to function arrows, not to types. Backwards-compatible: ordinary code continues to type-check unchanged. Experimental since GHC 9.0; still labelled experimental in 9.12 / 9.15 (2024–2026)."
tags: ["memory-safety", "ownership"]
weight: 100
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Paper**: Bernardy, Boespflug, Newton, Peyton Jones, Spiwack, "Linear Haskell: practical linearity in a higher-order polymorphic language", arXiv:1710.09756, POPL 2018.
- **GHC documentation** (user's guide):
  - 9.0 intro: https://downloads.haskell.org/ghc/9.0.1/docs/html/users_guide/exts/linear_types.html
  - 9.12 (Nov 2024): https://downloads.haskell.org/~ghc/9.12.0.20241128/docs/users_guide/exts/linear_types.html
  - 9.15 dev (2026): https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/linear_types.html
- **Status in user guide every release**: "currently considered experimental, with bugs, warts, and bad error messages expected".

## §2 Core type discipline

Linearity is a property of the **arrow**, not the value type. Two function arrows:

- `a -> b` — ordinary (i.e. `Many`-multiplicity), the existing Haskell arrow.
- `a %1 -> b` — linear (multiplicity `One`); also `a ⊸ b` under UnicodeSyntax.
- `a %m -> b` — multiplicity-polymorphic; `m :: Multiplicity = One | Many`.

A function of type `a %1 -> b` is linear, defined as: *if its result is consumed exactly once, then its argument is consumed exactly once*. The definition is intentionally consumption-conditional: a linear function used non-linearly does not constrain its arg; the constraint only fires under linear consumption.

Annotation surface:

- Multiplicity annotation on function arrows, written `%1 ->` or `%Many ->` or `%m ->`.
- Default for inferred arrows: `Many` (i.e. unconstrained). Linear arrows must be **declared**, never inferred. This decision keeps the system fully backwards-compatible.
- ADT fields: by default treated as linear in their constructors, so they enable linear consumption patterns without breaking code.

Judgement form: a multiplicity is attached to each variable in the typing context; a typing rule sums multiplicities along the AST. A linear context cannot duplicate variables; a many context can.

Principal example — in-place mutable array with a linear/pure interface:

```haskell
newArray :: Int %1 -> (MArray a %1 -> Ur b) %1 -> Ur b
read     :: MArray a %1 -> Int %1 -> (MArray a, Ur a)
write    :: MArray a %1 -> Int %1 -> a %1 -> MArray a
freeze   :: MArray a %1 -> Ur (Array a)
```

The mutable array `MArray` is linear: every operation threads it; the closing `freeze` produces the (unrestricted) pure `Array`. The compiler can compile this to in-place mutation because the linearity proves no aliasing.

## §3 Memory-safety invariant

- **No leaks** (linear values must be consumed).
- **No aliasing for linear data** (you cannot duplicate a `%1 ->` argument; the type rule forbids it).
- **Safe in-place mutation behind a pure interface**: the proof of single-use is what licenses the mutation.
- **Resource protocol enforcement**: file handles, sockets, etc., as linear values.
- **No double-free / use-after-free** on linear resources.

What it does **not** preserve: data-race freedom across threads (Haskell's STM/MVar story is separate), capability isolation, traditional effect tracking.

## §4 Compiler implementation cost

- GHC's multiplicity inference is folded into the existing type inferencer. The implementation is non-trivial (multiplicity unification through polymorphism is subtle), but it lives next to existing type-class machinery.
- Diagnostic quality: poor by GHC's standards. The documentation has carried the "bad error messages expected" warning since 2020.
- Pattern matching has been the moving piece across releases. GHC 9.12 (Nov 2024) refined the rule that non-variable lazy patterns consume the scrutinee with multiplicity `Many` (so you cannot accidentally take a linear value apart non-linearly).
- The big benefit is **backwards compatibility**: not a single existing Haskell program had to change.

## §5 Production / language adoption status (May 2026)

- LinearTypes extension shipped in GHC 9.0 (2021); still officially **experimental** through GHC 9.15 dev (2026).
- Adoption is real but niche: Tweag uses linear types in safety-critical contracts; the `linear-base` package provides a curated linear standard library on Hackage.
- No mainstream Haskell project requires the extension; most production code ignores it.
- Active research: ICFP / Haskell Symposium papers on linear constraints, dependent linear types, applications to FFI safety.

## §6 Mochi adaptation note

The single most important lesson from Linear Haskell, for Mochi, is **the arrow carries the discipline, not the type**. That keeps the surface small and the backwards-compat story trivial.

Pieces that map cleanly:

- **A linear function annotation**. Mochi already attaches an `EffectSet` to `FuncType` (MEP-15). Adding a `Multiplicity` field is one more orthogonal axis on the function type. Default is unrestricted; a function declared `linear fun f(x: T) -> U` (or `fun f(x %1 -> T) -> U` if Mochi wants the GHC sigil) enforces single use.
- **Polymorphism in multiplicity** for higher-order combinators. `map` should be multiplicity-polymorphic: `map :: (a %m -> b) -> List a %m -> List b`. Without this, `map` over a linear callback cannot be expressed.
- **Linear ADT fields by default**: existing record types do not change; constructors permit linear use when called linearly. This is exactly what Mochi needs to avoid breaking fixtures.

Incompatible:

- The `Ur a` (unrestricted) wrapper Haskell uses to lift unrestricted values into linear scopes. Mochi does not have a kind system rich enough to express it directly; we would simulate with a marker type.
- Multiplicity polymorphism's full generality. Mochi's generics are simpler; we should restrict to monomorphic linear functions in v1.

Surface-syntax change MEP-41 should adopt: a single `linear` keyword on `fun`, which is equivalent to declaring all parameters consume-once. No per-parameter multiplicity in v1; raise that flag only if the simple form proves insufficient.

vm3 tie-in: a linear parameter triggers `KILL_HANDLE` at the call boundary (same opcode as Swift's `consuming` parameter would emit). The runtime is unchanged.

Effect tie-in (MEP-15): a linear function is a "single-shot" effect; effect propagation through `map` and friends already uses a hidden row variable (per MEP-15 §Specification). The same row machinery can carry multiplicity if MEP-41 ever needs it.

Option tie-in (MEP-16): `linear fun consume_option(x: Option<T>): T` plus narrowing eliminates the need for any force-unwrap operator; the linear discipline guarantees a single take.

## §7 Open questions for MEP-41

1. Should the discipline live on the arrow (Haskell style) or on the type (Austral / OCaml-mode style)? They are largely interchangeable; arrow-style composes better with higher-order code.
2. Do we need multiplicity polymorphism, or is monomorphic linear-or-not enough?
3. How do we surface the "bad error messages" risk? Linear Haskell's diagnostics are still infamous; MEP-41 must invest more.
4. Does Linear Haskell's `Ur` wrapper teach us anything about Mochi's `Option` boxing strategy?

Sources: arXiv:1710.09756 ; GHC user's guide LinearTypes section (9.0, 9.6, 9.8, 9.12, 9.15) ; https://news.ycombinator.com/item?id=25582746 .