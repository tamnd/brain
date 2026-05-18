---
title: "Rust Polonius (2026)"
description: "The state of Rust's borrow checker as the Polonius \"alpha\" lands behind a nightly feature gate, and what a non-ownership language can still steal from it."
tags: ["memory-safety", "ownership"]
weight: 10
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Working group**: Polonius WG, Rust compiler-team. Niko Matsakis (design), Jack Huey, Matthew Jasper, Amanda Stjerna (impl/PhD).
- **Foundational papers**:
  - Matsakis et al., *Non-Lexical Lifetimes RFC* (RFC 2094, 2017), stabilised by default in Rust 1.63 (Aug 2022).
  - Stjerna, *Polonius Revisited* (2023, Inside Rust blog).
- **2026 stabilisation goal**: "Stabilize and model Polonius Alpha", https://rust-lang.github.io/rust-project-goals/2026/polonius.html
- **WG page**: https://rust-lang.github.io/compiler-team/working-groups/polonius/
- **Crate**: https://github.com/rust-lang/polonius (Datafrog/Datalog reference impl, now superseded by in-tree alpha).
- **NLL retrospective**: https://blog.rust-lang.org/2022/08/05/nll-by-default/

## §2 Core type discipline

Rust's ownership algebra is `(owned T) ⊕ (&'a T) ⊕ (&'a mut T)`. A value has exactly one owner; references are second-class, carry a lifetime `'a`, and obey aliasing-XOR-mutation: any number of `&T`, **or** exactly one `&mut T`, never both. Drop runs at the end of the owner's scope.

Annotation surface: lifetime parameters `'a, 'b, …` on `fn`, `struct`, and `impl`. Most are inferred via lifetime elision; the rest are written explicitly. Borrow expressions `&e`, `&mut e`, dereference `*r`, reborrow `&*r`.

Judgement form (NLL/Polonius, simplified): at every MIR program point `P`, for every loan `L = (place, kind)` issued earlier and still **live**, no conflicting access to `place` is permitted. Polonius reformulates "still live" from the NLL "live at this lexical region" to "the loan flows on the CFG to a point that still reads it", which is the *origin* relation in Datalog form.

Principal example (NLL problem case #3 — accepted by alpha, rejected by current stable):

```rust
fn get_or_insert<'a>(map: &'a mut HashMap<K, V>, k: K) -> &'a V {
    if let Some(v) = map.get(&k) { return v; }   // borrow #1 should end here
    map.insert(k, V::default());                  // but stable NLL keeps it live
    map.get(&k).unwrap()
}
```

## §3 Memory-safety invariant

Aliasing-XOR-mutation, statically enforced. Implies:
- No use-after-free (the borrow checker forbids holding `&T` past the owner's drop).
- No double-free (move semantics consume the owner exactly once).
- No data race on memory (because `Send`/`Sync` are derived from the same discipline; `&mut` is by definition unshared).
- No iterator invalidation (mutating the container while a `&` is live is rejected).

The system intentionally does **not** preserve capability isolation or effect tracking; that lives in the `unsafe` boundary and the `Send`/`Sync` auto-traits.

## §4 Compiler implementation cost

- NLL is a `~`5–10k LOC analysis pass on MIR, lifetime inference via region equality, requires a region inference engine.
- Polonius alpha is a *location-sensitive* reachability over a subset+CFG graph; the 2025h2 implementation passes the full in-tree test suite and crater runs but is 10–20% slower than NLL (within the team's bounded-cost budget).
- The full datalog Polonius (datafrog) was abandoned because it did not scale beyond toy crates.
- Error messages are a multi-year saga: `error[E0502]` etc. have evolved through three generations of suggestion engines and quick-fix machinery. Even now they require explanation pages on rust-lang.org. The lesson: a sound borrow checker without world-class diagnostics is unusable.

## §5 Production / language adoption status (May 2026)

- NLL: stable since Rust 1.63 (2022), the default for four years.
- Polonius alpha: shipping behind `-Z polonius=next` on nightly; a stabilisation report is the 2026 project goal but stable shipment is still gated on (a) resolving the opaque-type liveness soundness issue and (b) upstreaming the a-mir-formality formal model into the Rust Reference.
- Async-fn-in-traits: stable since Rust 1.75 (Dec 2023), `dyn` safety for async traits closed out in 2025 via the "RTN" return-type-notation feature.
- Rust itself is the production proof: kernels (Linux, Windows components), browsers, AWS Firecracker, all major cloud runtimes.

## §6 Mochi adaptation note

Mochi is **type-checked but GC'd and arena-backed**. A full borrow checker is incompatible with handle Cells: a Cell can be copied freely (it is 8 bytes, by-value), and mutation is mediated by the VM (`STORE_FIELD`, `LIST_SET`), not by direct memory writes. There is no aliasing problem in the Rust sense because there are no raw pointers at the source level.

What still maps cleanly:

- **Lifetime elision as a documentation discipline**: every function in `types/check.go` already knows the lifetime of its arguments is "at least the call". An `&borrow` annotation on parameters would be pure metadata that produces a warning if the body stores the parameter into a longer-lived structure. No borrow checker; just a reachability check riding on the existing type pass.
- **Move semantics for resources**: pair with MEP-15's `io`/`fs`/`net` effects. A `FileHandle` value could be marked `consumed-by` on its `close` method. The check is single-use, not full linear — much closer to Mochi's "let vs var" discipline (MEP-10 A3).
- **`mut` parameter convention**: a fresh keyword on parameters that says "I will write through this handle". The VM does not need it (handles are already mutable) but the type checker can use it as a hint and reject silent mutation through a parameter that was not declared `mut`. This mirrors Swift's `inout` and is cheap.

Incompatible pieces:

- Lifetime parameters `<'a>` on user types. Mochi has parametric polymorphism (`poly.go`) but adding a second universe of lifetime variables doubles the inference surface for no safety win when GC is doing the work.
- Reborrow `&*r`. Handles dereference to handles; the operation is uniform.

The generation counter in vm3's `Cell` (12 bits, see `runtime/vm3/cell.go:42`) already gives Mochi a **dynamic** stale-handle check — the opposite side of what Polonius does statically. MEP-41 should embrace that and call out: "Mochi catches use-after-free at the generation check, not at the type level."

## §7 Open questions for MEP-41

1. Is the smallest borrow-style annotation `mut`/`borrow` on parameters worth the diagnostic noise it creates?
2. Should MEP-41 introduce a `consume` annotation that the VM honours by zeroing the source slot, in lieu of a real linear type?
3. Can the alpha-style location-sensitive analysis be reused as the engine for MEP-15's effect propagation (both are flow-sensitive subset propagation problems)?
4. Do we want a `Cell.kill()` operator that bumps the generation eagerly, giving callers an explicit "I'm done with this handle"? This is the runtime analogue of `drop(x)` and lets MEP-41 stay purely advisory while still letting users get deterministic destruction.

Sources used: Rust Project Goals 2026, https://rust-lang.github.io/rust-project-goals/2026/polonius.html ; NLL stabilisation post, https://blog.rust-lang.org/2022/08/05/nll-by-default/ ; Polonius status, https://rust-lang.github.io/polonius/current_status.html .