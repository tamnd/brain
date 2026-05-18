---
title: "Lobster — Compile-Time Reference Counting"
description: "A pragmatic language by Wouter van Oortmerssen that elides 95% of refcount ops at compile time through flow-typed lifetime analysis. Cycles handled by a cleanup at program exit."
tags: ["memory-safety", "runtime"]
weight: 30
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Lobster language.** Wouter van Oortmerssen (the same author as Amiga-E, CryEngine's FlatBuffers, and several earlier ownership-RC experiments).
- Talk: "Compile-time reference counting & Lifetime analysis in Lobster," r/ProgrammingLanguages Meetup, Nov 22 2020, https://www.youtube.com/watch?v=WUkYIdv9B8c.
- Reference manual: https://aardappel.github.io/lobster/language_reference.html.
- Project site: https://strlen.com/lobster/.
- Prior art the author cites: his own "ownership reference counting" (June 2004) and the academic *Reference Escape Analysis* paper (Park & Goldberg, *SIGPLAN Notices* 26-9, 1991, https://dl.acm.org/doi/10.1145/115866.115883).

## §2 Mechanism

Lobster's compiler does flow-sensitive lifetime analysis on the AST. Every refcounted value has a known "owner" at every program point. The compiler then:

1. **Elides `inc` on move.** When ownership transfers (assignment, function-arg pass) without aliasing, no refcount op is emitted. This is the "moved-from doesn't need destruct" property.
2. **Elides `dec` on consumed values.** A value passed into a sink (e.g. the receiver of a method that drops it) is not separately dec'd.
3. **Elides everything for non-escaping function values.** Lobster's closures are non-capturing — they are bare code pointers; free variables must still be in scope at the call site. This makes them zero-cost and removes a whole class of allocations.
4. **Inserts `dec` at the lexical scope exit** for local owners that haven't been moved out.

Cycle detection runs once at program exit, doing a single mark-sweep over what's left. Cycles never break correctness; they merely accumulate until shutdown. The author argues this is fine for game-style programs (Lobster's target domain).

The author claims ~95% of refcount operations are removed by the analysis. The remaining 5% (the ones that can't be statically resolved — usually heterogeneous container elements) run at runtime as ordinary RC.

## §3 Memory-safety property

Spatial + temporal safety from RC + bounds checks. No UAF because RC drops happen at known lexical points. No double-free because moves are tracked.

The compile-time analysis doesn't *add* safety on top of what RC provides — it just removes the runtime cost. Cycles are not collected during execution, so genuinely leaking programs leak until exit; this is a memory-pressure issue, not a safety one.

## §4 Production status (May 2026)

Lobster is single-author, MIT-licensed, actively maintained on GitHub (`aardappel/lobster`). It has a real user base in game-jam and educational contexts but no industrial deployments visible from public sources. It is most useful as an existence proof: a single person can build a language whose memory management is fast, predictable, and correctness-checked at compile time without going full Rust.

No mainstream benchmark suite published. The author has shared microbenchmarks where Lobster's compiled C++ output approaches Lua-JIT in scripting workloads and matches naive C++ in tight loops.

## §5 Cost

- **Throughput.** Comparable to Lua or modern Python for the interpreted backend; close to naive C++ for the LLVM/C++ backend, because the RC ops vanish.
- **Memory.** Low. The runtime is tiny (a header + a small allocator).
- **Latency.** Predictable — no GC pauses ever, except a single cleanup at exit.
- **Compile time.** Slightly increased by lifetime analysis but Lobster compiles fast in absolute terms.
- **Hidden cost.** AST-based analysis is "limiting/complex" — Rust moved to CFG-based NLL for the same reason. Lobster's author concedes it's flow-typed but acknowledges the limitation.

## §6 Mochi adaptation note

Lobster's lesson for vm3 is the *bound*: how much RC traffic can be statically eliminated. If even half of vm3's planned `OP_DUP_HANDLE` / `OP_DROP_HANDLE` ops can be elided at compile time, the steady-state alloc overhead from MEP-40 Phase 1 (1.4-1.7× of `make()`) drops further.

Concrete smallest patch:

1. **Compiler3 ownership pass (MEP-40 §7.3).** Add an `ownership.go` pass that runs after type-driven lowering. For each IR value, compute:
   - `consumed_by_call`: is this value passed by-value into a function whose body consumes it?
   - `escapes_scope`: does this value flow into a global / closure capture / longer-lived parent?
   - `aliased`: are there multiple live names for this slot at the same program point?
2. **Emit-time elision.** When a `Last-Use(x)` node has `consumed_by_call && !aliased`, do not emit `OP_DROP_HANDLE`; the callee will drop. When two adjacent uses are `(Use, Move)` with no intervening alias, do not emit `OP_DUP_HANDLE`.
3. **Non-capturing closures.** Mochi already distinguishes closures with captures from those without; the former allocate a `kArenaClosure` cell. Adopt Lobster's stricter rule: in tight inner loops, prefer non-escaping function literals (no closure cell at all). This is a compiler hint, not a language change.

There is no Go-hosting conflict. Go's GC is unaffected because we are not changing what's on the heap, only how often the slab `Free` path runs.

## §7 Open questions for MEP-41

- Should Mochi's analysis be AST-based (like Lobster) or CFG-based (like Rust NLL)? CFG is more accurate but is a larger lift for compiler3.
- What fraction of `dup`/`drop` ops in the Mochi corpus *can* be statically eliminated? Need a measurement before committing to the pass.
- Does the "cycle collector runs only at exit" trade-off work for long-running Mochi server processes (web handlers, daemons)? Maybe an opt-in periodic cycle pass is needed.
- Lobster non-escaping closures are a language-level restriction. Mochi closures today *do* escape (used in `map`, `filter`, `reduce` pipelines and stored in lambdas). Can we get the win for the *common* case by detecting non-escape statically?

## Sources

- [Lobster — strlen.com (author's site)](https://strlen.com/lobster/)
- [Lobster Language Reference](https://aardappel.github.io/lobster/language_reference.html)
- [Compile-time RC and Lifetime Analysis in Lobster (YouTube talk)](https://www.youtube.com/watch?v=WUkYIdv9B8c)
- [Reference Escape Analysis (Park & Goldberg, 1991)](https://dl.acm.org/doi/10.1145/115866.115883)
- [Language Design Overview — Wouter van Oortmerssen](https://strlen.com/language-design-overview/)