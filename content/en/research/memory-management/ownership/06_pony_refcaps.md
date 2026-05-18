---
title: "Pony Reference Capabilities"
description: "Six capabilities (iso, trn, ref, val, box, tag) make actor-based concurrency data-race-free at compile time. Production at WallarooLabs and Microsoft; foundation for Verona's region work."
tags: ["memory-safety", "ownership"]
weight: 60
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Authors**: Sylvan Clebsch (founder), Sebastian Blessing, Sophia Drossopoulou; Imperial College London + Microsoft Research.
- **Tutorial home**: https://tutorial.ponylang.io/reference-capabilities/reference-capabilities.html .
- **Foundational paper**: Clebsch, Drossopoulou, Blessing, McNeil, "Deny Capabilities for Safe, Fast Actors", AGERE 2015.
- **Subtyping**: https://tutorial.ponylang.io/reference-capabilities/capability-subtyping.html .
- **Recovery**: https://tutorial.ponylang.io/reference-capabilities/recovering-capabilities.html .
- **Practitioner intro**: https://zartstrom.github.io/pony/2016/08/28/reference-capabilities-in-pony.html ; https://bluishcoder.co.nz/2017/07/31/reference_capabilities_consume_recover_in_pony.html .

## §2 Core type discipline

Every reference in Pony has both a type `T` and a capability `cap`. The 2-D matrix specifies, per reference, what is denied to **local aliases** and what is denied to **global** (other-actor) aliases.

| Cap   | Local-alias denial          | Global-alias denial            | Sendable? |
|-------|-----------------------------|--------------------------------|-----------|
| `iso` | none other (this is the only ref) | none other globally       | yes       |
| `trn` | other writers locally       | all readers/writers globally    | no        |
| `ref` | nothing                     | all readers/writers globally    | no        |
| `val` | other writers globally      | other writers globally          | yes       |
| `box` | other writers locally       | other writers globally          | no        |
| `tag` | reads & writes              | reads & writes                  | yes (identity only) |

Annotation surface: `String iso`, `String val`, etc., attached at every type position. Subtyping `iso <: trn <: ref <: box` and `trn <: val <: box`; values upcast as guarantees weaken.

Judgement form: standard subtype checking plus a *consume* / *recover* discipline. `consume e` evacuates the binding (so the unique-alias invariant of `iso`/`trn` holds across moves). A `recover` block enforces an *isolation boundary*: only sendable values may enter; whatever comes out can be re-typed at a stronger cap.

Principal example — sending a freshly built string between actors:

```pony
let s: String iso = recover String("hello") end
actor.greet(consume s)   // s is iso; consume hands it off; binding now dead
```

## §3 Memory-safety invariant

- **No data race**, by design. The aliasing matrix guarantees that no two actors hold concurrent write access to the same object.
- **No iterator invalidation across actors**: a `val` is globally immutable.
- **No deadlock**: actors are non-blocking; the type system does not need to reason about locks.
- **Memory safety**: relies on Pony's tracing GC per actor; no UAF.

What it does **not** preserve: capability isolation in the object-capability sense (Pony's "capability" is reference-cap, not authority-cap). Effect tracking is absent.

## §4 Compiler implementation cost

- Six caps × subtyping × generic instantiation = combinatorial growth in the type-rule table. The Pony compiler (ponyc, in C) is ~200k LOC; the cap subsystem is a non-trivial fraction.
- Error messages are notoriously terse and require user training. The diagnostic story has been the main barrier to adoption.
- The reward is a runtime that uses zero locks and no STW pauses (per-actor GC with orca cycle detector).

## §5 Production / language adoption status (May 2026)

- **WallarooLabs** built a stream processor in Pony; the company has since pivoted, but the runtime is still maintained.
- **Microsoft Research**: Pony's cap system is the direct ancestor of Project Verona's region capability system (see file 07).
- Pony's core team remains small; the ecosystem is niche. ponyc continues to release (latest series uses LLVM 18 / 19 on a quarterly cadence).
- No FAANG production deployment is public.

## §6 Mochi adaptation note

Six capabilities is too many. The lesson Mochi should take is the **two- or three-cap subset** that buys the property it needs.

If Mochi cared about actor / multi-Goroutine safety (it does not, yet), the minimal subset would be:

- `iso` — unique, owner can mutate, sendable across goroutines.
- `val` — deeply immutable, freely shareable.
- `ref` — local mutable (the existing default).

With just those three, MEP-41 would give Mochi data-race freedom across goroutine boundaries: a Go-hosted `mochi.Spawn(f)` would only accept callbacks whose captured environment is `iso` or `val`. The check is structural and small (~200 LOC).

vm3 tie-in: an `iso` annotation lets the runtime skip the gen check on this handle because it knows there is only one alias. A `val` annotation lets the runtime mark the slab entry's `flagShared` bit (already in `arenas.go`) and share it across actors without copying.

Effect tie-in (MEP-15): a `time`, `io`, or `fs` effect is incompatible with an `iso` parameter being passed to another actor (because the callee could observe interleaving). MEP-15's effect set already gives us the ingredients.

Option tie-in (MEP-16): an `Option<iso T>` allows safe transfer-or-keep: `take(): iso T?`. Same semantics as Pony's `consume`, expressed through the option discipline Mochi already has.

Incompatible:

- `trn`, `box`, `tag`. They make sense only in the full six-cap matrix; cherry-picking them creates confusion.
- The deny-local / deny-global axis. Mochi is single-process for now.
- Per-cap subtyping. The full lattice triples the typechecker complexity.

Surface-syntax change MEP-41 should consider: a single suffix on the *outer* type only, written `T@iso`, `T@val`, `T@ref` (default). No nesting. No per-field caps. The check is a single function in `types/check.go` that runs at goroutine-spawn sites.

## §7 Open questions for MEP-41

1. Does Mochi care about cross-goroutine safety in v1? If not, Pony's lessons can wait.
2. Is `iso` enough on its own, or do we need `val` to share immutable config?
3. Can the runtime *enforce* `iso` (e.g. trap on double-aliasing) without changing the bytecode shape?
4. Pony's diagnostics are infamously bad. How does MEP-41 avoid the same fate?

Sources: https://tutorial.ponylang.io/reference-capabilities/reference-capabilities.html ; https://tutorial.ponylang.io/reference-capabilities/capability-matrix.html ; https://tutorial.ponylang.io/reference-capabilities/capability-subtyping.html ; https://tutorial.ponylang.io/reference-capabilities/recovering-capabilities.html ; https://bluishcoder.co.nz/2017/07/31/reference_capabilities_consume_recover_in_pony.html .