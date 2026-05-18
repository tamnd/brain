---
title: "Inko — Singly-Owned Values"
description: "Single ownership with deterministic destruction, multiple simultaneous borrows allowed, runtime borrow-count enforcement. No GC, no compile-time borrow checker, no lifetime variables. Concurrency uses `uni T` (unique values) for safe inter-process transfer."
tags: ["memory-safety", "ownership"]
weight: 120
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Author**: Yorick Peterse.
- **Project home**: https://inko-lang.org/ . Repo: https://github.com/inko-lang/inko (MIT license).
- **Memory management reference**: https://docs.inko-lang.org/manual/latest/getting-started/memory-management/ . Versioned: https://docs.inko-lang.org/manual/v0.13.2/getting-started/memory-management/ .
- **Comparison page**: https://docs.inko-lang.org/manual/master/getting-started/compared/ .
- **Funded by**: NLnet, https://nlnet.nl/project/Inko/ .
- **Release notes**:
  - 0.10.0 (2022) introduced the ownership model.
  - 0.18.1 (2025) latest stable. https://inko-lang.org/news/inko-0-18-1-is-released/ .
- **Theoretical foundation**: cites Servetto et al., "Ownership You Can Count On: A Hybrid Approach to Safe Explicit Memory Management".
- **External essay**: Dusty Phillips, "Understanding Inko Memory Management Through Data Structures" (2023).

## §2 Core type discipline

Inko has four reference categories:

- **Owned reference** (default): the value's single owner. Drop runs at scope exit.
- **Immutable borrow** `ref T`: read-only alias; multiple may co-exist.
- **Mutable borrow** `mut T`: writable alias; multiple may co-exist.
- **Unique value** `uni T`: invariant "only one reference exists, the value itself"; sendable between processes.

Annotation surface: `T`, `ref T`, `mut T`, `uni T` at type positions. Function parameters and return types decide the convention. No lifetime variables; no compile-time borrow graph.

Judgement form, partially runtime: when a value is owned, it has a per-instance **borrow counter**. Borrows increment it; the counter decrements when the borrow goes out of scope. Moves are statically rejected while the counter is non-zero; drops at scope exit assert the counter is zero (drop-with-outstanding-borrows is a runtime panic).

Principal example — borrowing while moving (rejected by Rust, accepted by Inko):

```inko
let xs = [1, 2, 3]
let r = ref xs           # borrow counter ++
move_to_helper(xs)       # error: cannot move xs while borrowed
                         # but multiple `ref xs` are fine concurrently
```

For concurrency, the `uni T` discipline applies: only `uni T` values (or copyable value types) may be sent between processes (Inko's lightweight green-threaded actors).

## §3 Memory-safety invariant

- **No use-after-free**: drop is deterministic at scope exit; outstanding borrows trap at drop time (runtime check) rather than allow UAF.
- **No double-free**: the single owner drops once.
- **No data race**: the inter-process barrier requires `uni T` or value types; aliasing across processes is impossible.
- **No iterator invalidation in the dangerous sense**: mutating-while-borrowed traps at runtime rather than corrupting memory.

What is dropped vs Rust: aliasing-XOR-mutation is **not** enforced statically. You can hold multiple `mut T` borrows simultaneously. The cost is that some bugs (logical races over a shared mutable structure) are detected by the borrow counter at runtime rather than by the compiler.

## §4 Compiler implementation cost

- The Inko compiler does not have a borrow checker in the Rust sense. It performs move-analysis (forbid moving while statically-known borrows are live) and emits borrow-count increments/decrements for runtime checking.
- LLVM-based codegen; the borrow counter is a single word per heap-allocated value.
- Compiler is small relative to Rust's; the discipline is simple to teach.
- Diagnostics: borrow-count errors are runtime panics with file:line, not compile-time messages. The teaching story is "you'll find these bugs in dev, not in prod" — analogous to Vale's stance on gen-check failures.

Per-heap-object overhead: one extra word for the borrow count. Inline (stack) types skip the heap counter and use a per-borrowed-field count instead (see 0.18 inline-types release notes).

## §5 Production / language adoption status (May 2026)

- Inko is **production-targeted but pre-1.0**. Releases continue (latest 0.18.x in 2025).
- Backers: NLnet grant funding.
- Platform support: Linux, macOS, FreeBSD; LLVM backend.
- No major industrial users publicly known. The community is small and active.
- Influence on related work: cited as the "runtime-checked borrow counter" alternative in many ownership surveys.

## §6 Mochi adaptation note

Inko is the **closest fit** to Mochi's runtime philosophy. Both:

- Are GC-free at the user-visible layer (Inko uses single ownership + deterministic drop; Mochi uses arenas + generation checks).
- Detect violations dynamically rather than statically where it is awkward to do so statically.
- Accept "some safety bugs are runtime panics" as the price for a simpler surface.

What MEP-41 should steal:

- **The four-reference vocabulary**: owned, `ref` (immutable borrow), `mut` (mutable borrow), `uni` (unique, sendable). Apply on parameters. The check at call sites:
  - `owned T` parameter: caller must transfer the binding.
  - `ref T`: read-only view; multiple allowed.
  - `mut T`: mutable view; multiple allowed concurrently, like Inko.
  - `uni T`: requires the caller to pass a non-aliased handle (vm3 can statically check `flagShared == 0`, or fall back to a runtime gen-bump-and-check).
- **Runtime borrow counter on linear / unique resources**. vm3 already has the `flags` byte on every slab entry (`flagAlive`, `flagShared` — see `arenas.go:40`). Adding a `borrowCount` field is one byte/slot or a side-table; the runtime decrements on scope exit; the JIT can elide the counter for handles it has proven non-escaping.
- **`uni T` for goroutine boundaries**. The same machinery that buys Pony's `iso` (file 06) buys Inko's `uni`. Simpler vocabulary, less staging.
- **Deterministic destructors**. A `dispose` method on a `linear`/`uni` type, called at scope exit by the VM, gives Mochi the file-handle-close-on-scope-exit story without a GC dependency.

Incompatible pieces:

- The lack of compile-time aliasing-XOR-mutation. Mochi can choose to layer Inko's runtime model first and add static checks later, or stay with the pure runtime model. The runtime model is the lower-risk default for MEP-41 v1.
- Inko's per-process actor model. Mochi rides on Goroutines; the analogue is goroutine-local arenas, not actors.

Surface-syntax change MEP-41 should adopt: the keyword set `ref` / `mut` / `uni` on parameters, plus a `dispose` block on `nocopy struct`s. Default parameter convention is value-copy (existing behaviour). Annotations layer in.

vm3 tie-in: borrow counter lives in `flags` byte (1 bit "is borrowed" or full 8-bit count). On scope exit the bytecode emits `BORROW_END` to decrement. The JIT can elide for proven-non-escaping handles, the way MEP-39 already elides bounds checks.

MEP-15 tie-in: a `dispose` block is a structured effect at scope exit. The effect set propagates as if the body of `dispose` ran in sequence; MEP-15 needs no change.

MEP-16 tie-in: `Option<File>` drops the file when set to `None`. The dispose is automatic; no force-unwrap needed.

## §7 Open questions for MEP-41

1. Runtime borrow counter vs static check: which goes first? Inko proves runtime is shippable.
2. Does Mochi want full deterministic destruction (RAII-style) or only opt-in via `dispose`?
3. How does the borrow counter interact with the JIT's deopt path (MEP-39 §6.16)?
4. Inko's "move while borrowed is forbidden" — should MEP-41 reject that statically (Mochi can; static reachability of the binding is decidable), or runtime-trap like Inko?

Sources: https://inko-lang.org/ ; https://docs.inko-lang.org/manual/latest/getting-started/memory-management/ ; https://docs.inko-lang.org/manual/master/getting-started/compared/ ; https://dusty.phillips.codes/2023/06/26/understanding-inko-memory-management-through-data-structures/ ; https://inko-lang.org/news/inko-0-18-1-is-released/ ; NLnet project page.