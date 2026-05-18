---
title: "Cranelift Internals: ISLE, Proof-Carrying Code, and the Portable Backend Story"
description: "The most actively researched mid-tier compiler backend of the 2020s. ISLE for instruction selection, proof-carrying code for Wasm-sandbox memory accesses, and VeriISLE for verified instruction-lowering rules. Where the \"design and implementation of a portable codegen framework\" line of work currently lives."
tags: ["native-codegen", "papers"]
weight: 40
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- Cranelift project (Bytecode Alliance, lead Chris Fallin): https://cranelift.dev/. Source: https://github.com/bytecodealliance/wasmtime/tree/main/cranelift.
- ISLE blog post (Chris Fallin, Jan 20 2023): "Cranelift's Instruction Selector DSL, ISLE: Term-Rewriting Made Practical", https://cfallin.org/blog/2023/01-20/cranelift-isle/.
- "A New Backend for Cranelift, Part 1: Instruction Selection" (Chris Fallin, Sept 18 2020): https://cfallin.org/blog/2020/09/18/cranelift-isel-1/.
- ISLE language reference: https://github.com/bytecodealliance/wasmtime/blob/main/cranelift/isle/docs/language-reference.md.
- Bytecode Alliance 2023 retrospective: https://bytecodealliance.org/articles/wasmtime-and-cranelift-in-2023.
- VeriISLE (Monica Pardeshi, CMU thesis 2023): http://reports-archive.adm.cs.cmu.edu/anon/2023/CMU-CS-23-126.pdf.
- VeriWasm (prior work on sandbox proofs): "VeriWasm: Verified Mitigation of Speculative Side Channels", USENIX Security 2022.

## §2 Technique / contribution

### Cranelift architecture
- CLIF: the high-level IR. SSA, machine-independent.
- Vcode + MachInst: per-target IR layer. Vcode is the per-block machine-instruction list; MachInst is the per-target instruction definition.
- ISLE: instruction-lowering rules from CLIF to MachInst. A DSL.
- MachBuffer: the actual code emission buffer, with label/fixup tracking and branch-shortening peephole.

### ISLE (Instruction Selection Lowering Expressions)
- Statically-typed, term-rewriting language. Rules are of the form `(rule (Op args) (impl args))`.
- The ISLE meta-compiler compiles rules into a single decision tree in generated Rust, sharing work between overlapping rules and respecting user priorities.
- Used for both per-target instruction selection (4 architectures: x86-64, aarch64, s390x, riscv64) and machine-independent rewrites.
- Designed to be **dual-use**: the same rules drive the compiler and serve as the spec for formal verification.

### Proof-carrying code (PCC) in Cranelift
- The goal: prove every Wasm memory access stays within its sandbox.
- Implementation (lead: Chris Fallin): each load/store carries a static fact about its bounds. The compiler propagates these facts through optimization passes. At emit time, the prover checks the fact still holds.
- Trade-off: small compile-time cost, large security win for Wasm-as-sandbox use cases.
- Distinct from translation validation (which compares output to an oracle). PCC carries the proof through the pipeline.

### VeriISLE (Pardeshi 2023, CMU)
- A modular verifier for ISLE rules. Adds annotations to ISLE rules expressing the semantics of each term.
- Uses an SMT solver (Bitwuzla, Z3) to discharge correctness proofs of individual lowering rules.
- Demonstrated reproducing 3 known Cranelift bugs (one CVE-9.9), found 2 new bugs, and identified an underspecified compiler invariant.
- Establishes ISLE as a verification-friendly DSL.

## §3 Where it shines, where it fails

**Shines:**
- The ISLE DSL is small, fast to write, fast to verify. Cranelift's 4-architecture support is largely declarative.
- PCC gives meaningful security guarantees with bounded compile-time overhead.
- The whole stack is in Rust, single language, no FFI quirks.
- Active development: Cranelift improvements ship every Wasmtime release.

**Fails:**
- Not naive. Cranelift is an optimizing compiler, not a baseline one. The whole point of Winch (the Wasmtime baseline) is to *avoid* Cranelift's compile-time cost.
- Rust-only. Reusing Cranelift from Go would require IPC or cgo.
- PCC infrastructure adds non-trivial complexity to the IR layer.
- ISLE has its own learning curve (term-rewriting paradigm with Prolog-style backtracking).

## §4 Status (May 2026)

- Cranelift is the production codegen for Wasmtime, Lucet (deprecated), and several Rust-based VMs (e.g., the SpiderMonkey replacement experiment, GraalVM Native Image alternative).
- ISLE has been adopted for all four Cranelift backends as of 2023.
- PCC is now enabled by default in Wasmtime for Wasm linear-memory accesses.
- VeriISLE has been demonstrated; full integration into Cranelift's CI is in progress.
- Cranelift was named "Best Wasm Toolchain 2024" by several developer surveys.

## §5 Engineering cost for Mochi

Reusing Cranelift directly from Mochi: ~6 weeks via subprocess (run `cranelift-compile` over a Mochi-emitted CLIF text), or ~12 weeks via cgo/FFI bindings to libcranelift.

Adopting **just ISLE** as our DSL: ~3 weeks to write Mochi's per-op lowering as ISLE rules, then use Cranelift's ISLE compiler to generate a Rust-based code emitter. Note: this only helps if we're willing to depend on Rust.

For pure-Go Mochi, the lesson from Cranelift is **architectural**: split your backend into a per-target lowering DSL and a target-agnostic optimizer. We can do this in pure Go without ISLE:

- Define a Mochi lowering rule type in Go.
- Write per-op rules as Go literals or as a data file.
- A small Go pattern-matcher selects rules.

This is ~5 weeks of work and gives us Cranelift's modularity without the Rust dependency.

## §6 Mochi adaptation note

- `compiler3/ir/` is the analog of Cranelift's CLIF.
- A new `compiler3/lower/` package would host the per-op lowering DSL.
- A new `compiler3/emit/` per-target backend uses the lowering output.
- `runtime/vm3/` provides the calling-convention and arena hooks that lowered code calls.
- PCC ideas could carry through `compiler3/opt/` if we ever want sandbox-style guarantees.

## §7 Open questions for MEP-42

- Do we want to write our own ISLE-like DSL or use ad-hoc Go switch statements?
- Is PCC a phase-2 add for Mochi-as-sandbox use cases?
- Should Mochi adopt the Cranelift "split CLIF/MachInst" architecture from day one, or evolve to it?
- For verification: do we want to follow VeriISLE's lead and design our DSL to be verifier-friendly from the start?
- Multi-target shape: should Mochi emit a Cranelift-IR backend as one of several emitters, alongside QBE and direct-asm?

## §8 References

- Chris Fallin's blog: https://cfallin.org/.
- "Cranelift's ISLE: Term-Rewriting Made Practical": https://cfallin.org/blog/2023/01-20/cranelift-isle/.
- "A New Backend for Cranelift, Part 1: Instruction Selection": https://cfallin.org/blog/2020/09/18/cranelift-isel-1/.
- ISLE language reference: https://github.com/bytecodealliance/wasmtime/blob/main/cranelift/isle/docs/language-reference.md.
- Bytecode Alliance retrospective: https://bytecodealliance.org/articles/wasmtime-and-cranelift-in-2023.
- VeriISLE CMU technical report: http://reports-archive.adm.cs.cmu.edu/anon/2023/CMU-CS-23-126.pdf.
- Wasmtime Cranelift crate: https://crates.io/crates/cranelift.