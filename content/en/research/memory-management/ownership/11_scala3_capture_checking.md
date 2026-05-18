---
title: "Scala 3 Capture Checking"
description: "Capability tracking in the type system. Each value's type may carry a capture set listing which capabilities it could reference. Foundation for capability-based effects, separation checking (System Capybara), and ownership for resources."
tags: ["memory-safety", "ownership"]
weight: 110
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Lead**: Martin Odersky and the EPFL LAMP group. Capture-checking research and Capybara extension led by Oliver Bračevac.
- **Reference docs (experimental)**: https://docs.scala-lang.org/scala3/reference/experimental/cc.html . Advanced: https://docs.scala-lang.org/scala3/reference/experimental/cc-advanced.html . Nightly basics: https://nightly.scala-lang.org/docs/reference/experimental/capture-checking/basics.html .
- **Scala Days 2025 talk**: Oliver Bračevac (EPFL/LAMP), https://bracevac.org/assets/pdf/scaladays2025_annot.pdf and https://scaladays.org/editions/2025/talks/capture-checking-a-new-approach .
- **Conference papers**:
  - "What's in the Box: Ergonomic and Expressive Capture Tracking over Generic Data Structures", OOPSLA 2025 (System Capless). https://2025.splashcon.org/details/OOPSLA/133/...
  - "System Capybara: Capture Tracking for Ownership and Borrowing", Scala Workshop 2025. https://2025.workshop.scala-lang.org/details/scala-2025/6/...
- **Practitioner write-ups**: SoftwareMill, https://softwaremill.com/understanding-capture-checking-in-scala/ ; Tanishiking blog, https://tanishiking.github.io/posts/introduction-to-scala-3s-capture-checking-and-separation-checking/ .
- **Status flag**: `import scala.language.experimental.captureChecking` or `-Ycc`. Still highly experimental as of May 2026.

## §2 Core type discipline

A **capability** is a syntactic role: a method parameter, a class parameter, a local variable, or `this`. Every capability has a type with a non-empty *capture set*.

Types take the form `T^{c1, ..., cn}` where `{c1, …, cn}` is the capture set — a set of references to capabilities that the value of type `T` may capture. A universal capability `cap` (or `any` in some docs) sits at the top of the lattice; every capability is derived from `cap`.

Function arrows split:

- `A -> B` — *pure* function arrow, captures nothing.
- `A => B` — impure (legacy), captures arbitrary capabilities.
- `A ->{c,d} B` — captures exactly `c` and `d`. Shorthand for `(A -> B)^{c,d}`.

Annotation surface: capture sets in postfix `^{ … }` notation on any type. Functions, classes, methods, type aliases. Empty capture set means "pure"; absence means "any".

Judgement form: a constraint-based propagation. Constraint variables stand for unknown capture sets; constraint flow follows variable bindings; explicit annotations become constants. The check runs as a separate compiler phase after typing.

**Classifiers (2025 addition)** organise capabilities into a hierarchy with two roots: `SharedCapability` (the standard capture-checking root) and `ExclusiveCapability` (Capybara/separation-checking root, capabilities that must be unaliased). The `.only[C]` operator filters capture sets to keep just the capabilities of a chosen class.

Principal example — a logger capability that should not escape its scope:

```scala
def withLog[T](body: Log^ => T): T = ...
val r = withLog { log =>
  () => log.info("hi")              // function captures log
}
// r : (() -> Unit)^{log}            // capture set leaks log
// but log has gone out of scope; this is rejected
```

The capture-checker rejects the leak because `log` is not in scope at the call site of `r`.

## §3 Memory-safety invariant

- **Capability isolation**: a capability cannot escape its lexical scope.
- **Effect safety**: if a capability represents "I can do IO", capture tracking ensures that the IO authority does not leak.
- **(With separation checking, System Capybara)**: aliasing-XOR-mutation on `ExclusiveCapability`-typed values. Same property as Rust's `&mut`, surfaced through capabilities.

What it does **not** preserve (without Capybara): aliasing constraints on ordinary data. Standard capture checking is about *what references are visible*, not *who can write*.

## §4 Compiler implementation cost

- A separate compiler phase after typing. Implemented as a constraint solver over capture-set variables; the constraint graph is small in practice (one variable per binding).
- Diagnostics: scoped-to-capability messages ("function value captures `log` which is out of scope"). Better than Rust's lifetime errors because the capability name is local and meaningful.
- Migration cost has been the wall: the Scala 3.8 milestone required capture-checking the entire collections library. The OOPSLA'25 *System Capless* paper covers exactly this migration effort and the *reach capabilities* mechanism that made it ergonomic.
- The full Capybara extension (separation checking) adds further per-capability flow analysis; cost is modest because the underlying machinery already exists.

## §5 Production / language adoption status (May 2026)

- Capture checking remains **experimental** (opt-in import / `-Ycc`).
- Scala 3.8 (2025) ships:
  - Capture-checked standard library.
  - Classifier hierarchy.
  - Reach capabilities (System Capless).
- Capybara (separation checking) is research-stage, with a working prototype.
- No major Scala framework requires capture checking yet; experimental adopters include Gears (async library), parts of the Scala compiler itself.

## §6 Mochi adaptation note

Capture checking and Mochi's MEP-15 effect system are **conceptually the same machinery seen from different angles**. MEP-15 attaches `{io, fs, net, time, meta}` to each function; capture checking attaches `{c1, c2, …}` (per-capability references) to each function. Both are propagated bottom-up through the call graph; both are checked against declared upper bounds at signature points.

The mapping is:

| Scala capture checking         | Mochi (MEP-15 + MEP-41)                |
|--------------------------------|-----------------------------------------|
| Capability (`cap`)             | A capability *value* of a `linear` type (per MEP-41). |
| Capture set `^{c, d}`          | EffectSet (currently labelled), generalised to a set of capability-value references. |
| Pure arrow `A -> B`            | `fun` with empty Effects (current). |
| Capture function arrow `A ->{c,d} B` | `fun ! cap(c), cap(d)` (proposed MEP-41 extension to MEP-15 surface). |

Pieces that map cleanly:

- **Capabilities as values**, not as labels. MEP-41 promotes MEP-15's labels to first-class values: `io: IoCap`, `fs: FsCap`, etc. Functions take capability parameters; effect inference is then "does the body refer to a capability the signature did not list?".
- **Separation checking (Capybara)** for handle-mutable types. An `ExclusiveCapability`-equivalent on a Mochi `linear` handle gives aliasing-XOR-mutation.
- **`.only[C]` filtering**. Useful for restricting effect surfaces in MEP-15 (e.g. "this function may touch the FS but not the network").

Incompatible:

- The full capture-set syntax `^{c, d}` everywhere. Verbose; better suited to Scala's denser type surface. Mochi should keep the post-fix `!` from MEP-15 and grow it with capability references rather than label strings.
- Reach capabilities (System Capless). They solve a problem about generic data structures that Mochi does not yet have.

Surface-syntax change for MEP-41: extend MEP-15's `!` clause to accept capability values as well as labels. E.g. `fun open(p: Path, fs: FsCap): File ! fs`. The `fs` after `!` names the capability that authorises the effect.

vm3 tie-in: capability values are normal handle Cells (probably in `ArenaStruct` or a new `ArenaCap` slab). The runtime cost is minimal; the static check does the work.

MEP-16 tie-in: `Option<FsCap>` lets a function gracefully degrade if the capability is absent.

## §7 Open questions for MEP-41

1. Should MEP-41 promote MEP-15's labels to capability values, or leave them as labels and add capabilities separately?
2. How does the Capybara separation-checking extension interact with Mochi's GC? (Likely: not at all; the static check is independent of the runtime.)
3. Is reach-capability machinery worth the complexity for Mochi's current generic surface?
4. Can vm3 share representation between capability values and ordinary structs, or do we need a dedicated `ArenaCap`?

Sources: https://docs.scala-lang.org/scala3/reference/experimental/cc.html ; https://bracevac.org/assets/pdf/scaladays2025_annot.pdf ; OOPSLA 2025 System Capless paper ; Scala Workshop 2025 System Capybara paper ; https://softwaremill.com/understanding-capture-checking-in-scala/ .