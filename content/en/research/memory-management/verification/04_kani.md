---
title: "Kani"
description: "AWS's bit-precise bounded model checker for Rust, deployed in CI on Firecracker and the standard library."
tags: ["memory-safety", "verification"]
weight: 40
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Project: https://github.com/model-checking/kani ; documentation https://model-checking.github.io/kani/getting-started.html
- Owned by AWS, open source under MIT/Apache-2.0. Built on the CBMC backend (CPROVER).
- Production-use case study: AWS Open Source Blog, **"Using Kani to Validate Security Boundaries in AWS Firecracker"**, 2023, https://model-checking.github.io/kani-verifier-blog/2023/08/31/using-kani-to-validate-security-boundaries-in-aws-firecracker.html
- Rust standard-library verification initiative (AWS-sponsored, hosted by the Rust Foundation): https://aws.amazon.com/blogs/opensource/verify-the-safety-of-the-rust-standard-library/
- ESBMC integration via Goto-Transcoder (Rust Foundation announcement, 2024-2025): https://rustfoundation.org/media/expanding-the-rust-formal-verification-ecosystem-welcoming-esbmc/
- Releases through 2025-2026 (Kani 0.61 through 0.66) tracked at https://github.com/model-checking/kani/releases

## §2 Claim or Mechanism
Kani is a **bit-precise bounded model checker**. The user writes a proof harness, similar to a property-based test harness, that ends with assertions or function contracts. Kani encodes the harness plus the Rust code into a CBMC goto-program, converts that to an SMT formula, and dispatches to a solver (the default is MiniSat, with optional bitwuzla/cvc5/z3 via the `solver` attribute as of Kani 0.66).

Kani proves three kinds of properties:
- **Memory safety / undefined behaviour**: out-of-bounds accesses, use-after-free, double-free, invalid pointer arithmetic, alignment violations, type-punning UB. This is the primary value-add for `unsafe` Rust.
- **Arithmetic overflow and unwrap panics**: automatic checks on integer arithmetic and on `Option::unwrap` / `Result::unwrap`.
- **User assertions and function contracts**: `kani::assert`, `requires` / `ensures` contracts, and (new in 0.66) loop invariants for `while-let`.

Because it is bounded, Kani can *prove* properties up to a fixed loop unroll / structural bound. Beyond the bound, Kani reports "unknown". This is qualitatively weaker than Verus or Creusot, but the proofs are fully automatic — no annotations beyond the harness.

## §3 Scope and Limits
**Covered.** Both safe and unsafe Rust. Many of Kani's high-value cases are *unsafe blocks* in well-trusted libraries (the Rust standard library, vector-SIMD code, Firecracker's VMM, s2n-quic). Concurrency support is limited.

**Not covered.** Loops with large or unbounded bounds; deep recursion; concurrency at full generality; high-performance code paths where the symbolic explosion makes solving infeasible. Kani's guarantees are conditional on the bound — properties below the bound are proven; above the bound are not even claimed.

The trust base is `rustc`, CBMC, the SMT solver, and Kani's own MIR-to-goto translation. Kani is *not* foundational and produces no Coq / HOL artifact.

## §4 May 2026 Status
**Production-deployed inside AWS.** Firecracker (the Rust microVM monitor that backs AWS Lambda, Fargate and parts of AWS Analytics) runs **27 Kani harnesses across 3 verification suites in CI**, completing in roughly 15 minutes per CI run, on every code change. The s2n-quic QUIC implementation also runs Kani in CI. The Rust standard library verification contest (sponsored by AWS, run by the Rust Foundation) has produced an ongoing stream of verified safety harnesses for the std `core` modules, and as of 2024-2025 the ESBMC bounded model checker has been added as an alternative backend through Goto-Transcoder.

Kani has a monthly release cadence and tracks the Rust nightly toolchain. As of 0.66 (toolchain 2025-11-21) it offers `BoundedArbitrary`, loop invariants for `while-let`, autoharness improvements that apply std heuristics automatically, and runs CBMC 6.5.0.

## §5 Cost
**Engineer cost is dominated by writing harnesses, not by solver time.** A Firecracker engineer reports that the 27 harnesses took weeks of effort, mostly to set up the right abstraction of the VMM state. Solver time is bounded (15 minutes for the full Firecracker suite). Compared to Verus or Creusot, Kani requires no specification language — just assertions — so the entry cost is much lower. Compared to fuzzers, Kani gives a true proof up to its bound rather than a probabilistic coverage signal.

Per the AWS published vision, Kani sits in the *middle* of a spectrum: cheaper than Creusot / Prusti, more expressive than MIRAI, more rigorous than fuzzing and sanitizers.

## §6 Mochi Adaptation Note
Kani is the most directly relevant verification tool for Mochi's *threat model*, even though Mochi is Go-hosted and Kani targets Rust. Why:

- Kani's "automatic UB / memory-safety check on each CI run" pattern is exactly the discipline MEP-41 should aspire to for the vm3 runtime, even if implemented with Go's built-in race detector + `go test -race -fuzz`, Mochi's own fuzzers, and `unsafe`-Go review rather than CBMC. The point is that the *cadence* (every commit) and *posture* (look for UB, not just functional correctness) is what's transferable.
- If Mochi ever migrates a critical runtime fragment (mark-sweep, JIT) to Rust, Kani is the right CI tool. MEP-41 should mention this as a recoverable option, not a current commitment.
- Kani's recent CHERI / temporal-safety integration work (CPP 2025 CHERI memory model) is a leading indicator that bounded model checking is converging on the same per-allocation generation-tag invariant Mochi uses for Cells. MEP-41 should note the convergence: the 4-bit-tag / 12-bit-generation Cell representation is conceptually a stripped-down CHERI capability.
- AWS's vision (familiar tests → MIRI/sanitizers → fuzzing/PBT → Kani/MIRAI → Creusot/Prusti) is a useful template for the Mochi maturity ladder. MEP-41 can place Mochi at the "MIRI/sanitizers + fuzzing" rung today and articulate Kani-equivalent CI as a future MEP target.

## §7 Open Questions for MEP-41
1. Should Mochi commit to a Go-equivalent of "Kani-style CI on the runtime", i.e. a *bounded* exhaustive fuzz over a small number of Cell-creation/free/access sequences, run on every PR?
2. If a Rust-hosted re-implementation of vm3 is *ever* considered (cf. CompCertO/Owlang), Kani should be the verification baseline; MEP-41 can pre-commit to that without committing to the port itself.
3. The Firecracker model — 27 small harnesses each checking one invariant — is much more tractable than "verify the whole VM". MEP-41 should enumerate the candidate invariants (Cell tag well-formedness, generation monotonicity, no double-free across mark-sweep, JIT permission flip is atomic) that Mochi *could* prove if asked.
4. Should Mochi enroll in the AWS Rust standard-library verification ecosystem signal — i.e., adopt Kani's harness vocabulary in documentation? Cheap to do, makes Mochi legible to the AWS / Rust Foundation community.