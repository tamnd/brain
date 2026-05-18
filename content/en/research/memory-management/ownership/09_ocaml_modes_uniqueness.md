---
title: "Jane Street OxCaml — Modes (Uniqueness, Locality, Linearity)"
description: "Orthogonal modes layered onto OCaml's type system. Mode is a property of a value, separate from its type, tracked through inference. Production in Jane Street; open-sourced as OxCaml in 2025."
tags: ["memory-safety", "ownership"]
weight: 90
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Vendor**: Jane Street Capital, in collaboration with Tarides on the upstream merge.
- **Project**: OxCaml — open-source branch of OCaml. Announced/rebranded July 2025. Repo: `ocaml-flambda/ocaml-jst`.
- **Docs**: https://oxcaml.org/documentation/modes/intro/ .
- **Blog series "Oxidizing OCaml"**:
  - Locality: https://blog.janestreet.com/oxidizing-ocaml-locality/
  - Rust-Style Ownership: https://blog.janestreet.com/oxidizing-ocaml-ownership/
  - Data Race Freedom: https://blog.janestreet.com/oxidizing-ocaml-parallelism/
- **Data-race-freedom proposal in tree**: https://github.com/ocaml-flambda/ocaml-jst/blob/main/jane/doc/proposals/data-race-freedom.md .
- **2025 community write-up**: Tarides, "Introducing Jane Street's OxCaml Branch!", https://tarides.com/blog/2025-07-09-introducing-jane-street-s-oxcaml-branch/ .
- **Production milestone**: ICFP / SPLASH 2025 REBASE workshop — Yaron Minsky announced Jane Street's production servers run on the OCaml 5 multicore runtime.
- **Theory note**: KC Sivaramakrishnan, "Uniqueness for Behavioural Types", https://kcsrk.info/ocaml/modes/oxcaml/2025/05/29/uniqueness_and_behavioural_types/ .

## §2 Core type discipline

A *mode* is a property of a value orthogonal to its type. Each axis is a lattice; the system tracks each variable's modes alongside its type during inference.

Three active mode axes (and a few more in development):

- **Locality**: `local | global`. A *local* value cannot escape its allocating function; the compiler stack-allocates it. A *global* value can be returned, stored, captured.
- **Uniqueness**: `unique | aliased`. A *unique* value has exactly one reference; a *aliased* value may be referenced elsewhere. A function accepting a `unique` parameter effectively consumes it.
- **Linearity** (in development): `once | many`. A *once* function may be invoked at most once; *many* is the default. Combines with uniqueness to safely capture unique values in closures.

Annotation surface: `(x : 'a @ unique)`, `(x : 'a @ local)`, etc. Default is the weakest mode (`global`, `aliased`, `many`); modes need to be opted into via signature.

Judgement form: standard HM type inference extended with mode inference. Subtyping is per-axis: `unique <: aliased`, `local <: global` (a stack value can become a heap value with a copy; the reverse is forbidden), `once <: many`. The check is local; no cross-module region inference.

Principal example — safe memory allocator API:

```
val alloc : unit -> bytes @ unique
val free  : bytes @ unique -> unit
val read  : bytes @ aliased -> int -> char
```

`alloc` returns a unique buffer; `free` consumes it; `read` borrows it via aliased mode. Double-free is rejected by uniqueness: after `free b`, `b` is consumed.

## §3 Memory-safety invariant

Per axis:

- **Locality** → no stack value escapes. Eliminates GC pressure for stack-allocatable data; safe by construction.
- **Uniqueness** → no use-after-free, no double-free for resources you mark `unique`. The check is a flow-sensitive use-counter on `unique` bindings, very similar to Austral's linear check.
- **Linearity** → captures of unique values are safe; no accidental retention.

Combined: a Rust-like discipline as an *opt-in layer*, while the default OCaml story (GC, aliasing everywhere) continues to work for existing code.

Crucially, **data-race-freedom for OCaml 5 multicore** is being built on the same mode machinery (the *portability* and *contention* axes). Yaron Minsky's strategy: rather than retrofit Rust ownership, add modes one axis at a time, each one with backwards-compatible defaults.

## §4 Compiler implementation cost

- The OCaml 5 type checker is HM-based; adding mode inference threads each axis through the same algorithm. Each axis is ~1–2k LOC of additions.
- Per-axis defaults keep existing code valid: a program with no mode annotations type-checks unchanged.
- Diagnostics: error messages mention the mode mismatch ("expected `unique`, got `aliased`"); Jane Street's tooling adds suggestions.
- The cost is **library API design**: which functions take `unique`? `local`? The std-lib migration is ongoing.

## §5 Production / language adoption status (May 2026)

- **OxCaml has been used in production at Jane Street for years** (locality since at least 2023). 2025 milestones:
  - Production servers on the OCaml 5 multicore runtime (announced at REBASE workshop, ICFP/SPLASH 2025).
  - OxCaml officially open-sourced (July 2025, Tarides post).
  - Unique + once modes merged into the OxCaml branch.
- Upstream OCaml plans to merge OxCaml's modes once they bake; no precise upstream date as of May 2026.
- Docker case study (also at ICFP 2025) shows non-Jane-Street OCaml 5 production adoption.

## §6 Mochi adaptation note

This is the **template** MEP-41 should follow. Backwards-compat is non-negotiable for Mochi; OxCaml proves that an ownership-style discipline can be added one axis at a time with defaulted modes that keep existing code valid.

Each axis to consider:

- **Locality / stack allocation** — Mochi's vm3 already has inline Cells for short strings (`tagSStr`) and inline ints (`tagInt48`). A `@local` mode could direct the compiler to keep a value inline rather than allocating a slab entry. The check: a `@local` value never reaches a `STORE` into a long-lived container. This is one of the highest-ROI MEP-41 additions.
- **Uniqueness** — Mochi grows a `unique` mode for handle types. The static check follows Austral's linear pattern: each `unique` binding must reach a consume point on every path. The runtime extends `flagShared` in vm3's slab entries to enforce: a `unique` slab entry has `flagShared = 0`; aliasing breaks the property at the bytecode level.
- **Linearity (once / many)** on closures — Mochi has closures (`ArenaClosure`). A `@once` closure may be invoked at most once; the VM enforces by bumping the closure's `gen` on entry. This buys safe captures of `unique` data.

Mode annotations live next to types, do not change the type. This is exactly Mochi's preferred extension shape because `types/check.go` already threads type information through inference; mode information is a parallel channel.

Effect tie-in (MEP-15): an effect is logically a mode on the function type. MEP-15's existing `Effects EffectSet` field on `FuncType` is the precedent. A mode is a special case of a generalised mode-set; MEP-41 could unify the two if/when worth it.

Option tie-in (MEP-16): `unique Option<T>` is a one-shot result; `take` consumes uniquely. `local Option<T>` is a stack-allocated maybe-result. Both compose cleanly with the existing option discipline.

Incompatible:

- HM-style mode inference. Mochi's inference is more constrained (Algorithm W variant with explicit annotations on top-level signatures). Modes default to weakest, just like OCaml; the check should be local at call sites, not full bidirectional.

Surface-syntax change for MEP-41: introduce a `@mode` postfix on parameter and return types, with `@local`, `@unique`, `@once` as the initial axes. The check is per-axis, fully local, defaulted-to-weakest.

## §7 Open questions for MEP-41

1. Which axis ships first — locality (immediate vm3 perf win) or uniqueness (safety win)?
2. Should modes appear on bindings (`let x @ unique = …`) or only on parameters? OxCaml allows both; Mochi should start with parameters.
3. Can MEP-15 effects be unified with modes (a single mode-set machinery) without disrupting existing code?
4. How does the JIT interact with `@local`? Inlining and stack allocation should compose; OxCaml's locality story is precisely what vm3 needs to get tight inner loops.

Sources: https://oxcaml.org/documentation/modes/intro/ ; https://blog.janestreet.com/oxidizing-ocaml-locality/ ; https://blog.janestreet.com/oxidizing-ocaml-ownership/ ; https://blog.janestreet.com/oxidizing-ocaml-parallelism/ ; https://tarides.com/blog/2025-07-09-introducing-jane-street-s-oxcaml-branch/ .