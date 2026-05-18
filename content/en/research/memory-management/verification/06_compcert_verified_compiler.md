---
title: "CompCert and the Verified-Compiler Toolchain"
description: "The production-grade formally verified C compiler, the CompCertO / Owlang line, and why it matters for JIT verification."
tags: ["memory-safety", "verification"]
weight: 60
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance
- Leroy. **"Formal verification of a realistic compiler"**, CACM 2009; full development https://compcert.org ; source https://github.com/AbsInt/CompCert
- ACM Software System Award 2022, ACM SIGPLAN Programming Languages Software Award.
- CompCertO line: Koenig & Shao, **"CompCertO: Compiling Certified Open C Components"**, PLDI 2021; Zhang, Wang, Wu, Koenig, Shao, **"Fully Composable and Adequate Verified Compilation with Direct Refinements between Open Modules"**, POPL 2024.
- CompCertOC (PLDI 2025): verified compilation of multi-threaded programs with shared stacks. https://jhc.sjtu.edu.cn/~yutingwang/files/papers/pldi25-tr.pdf
- 3D Refinement Algebra (POPL 2025): https://jhc.sjtu.edu.cn/~yutingwang/files/papers/popl25.pdf
- **Owlang** (Oct 2025 arXiv 2510.10015): "End-to-end Compositional Verification of Program Safety through Verified and Verifying Compilation" — verified compilation of an ownership language inspired by Rust, on top of CompCertO.
- VST (Princeton Verified Software Toolchain) uses CompCert: https://github.com/PrincetonUniversity/VST
- 2025 industry use: Cornell used CompCert's `clightgen` to verify the modular-inverse routine in `libsecp256k1` for Bitcoin.

## §2 Claim or Mechanism
CompCert is a C compiler whose entire backend (16 passes, 10 intermediate languages) is **mechanically proven correct in Coq**: the generated assembly behaves exactly as the source C semantics prescribes. The theorem covers a substantial subset of C99 plus standard optimisations and targets PowerPC, ARM, x86, and RISC-V.

CompCertO extends CompCert from whole-program compilation to *open* modules with direct refinements, so that one can verify a C module and link it against another verified language's output. CompCertOC (PLDI 2025) extends this to concurrent programs with shared stacks. The 3D Refinement Algebra (POPL 2025) unifies these refinements.

**Owlang** is the 2025 capstone: a small Rust-inspired ownership language compiled through CompCertO's chain. The Owlang frontend performs *ownership checking* (a fragment of the borrow checker) and the full compilation chain preserves "open safety", a modular invariant-based definition of safety that composes at module boundaries. Crucially, the proof says: there can be no temporal memory error after ownership checking, *all the way down to assembly*.

For JIT verification, the analogous work is **FM-JIT** (Barrière et al.) which uses CompCert's verified backend to generate native code dynamically. The JIT calls CompCert's backend on translated RTL to produce x86 code, installs it in an executable memory page, and the impure parts (memory permissions, code installation) are factored into specified primitives. FM-JIT is the strongest existence proof for **verified just-in-time compilation**.

## §3 Scope and Limits
**Covered.** A formally large subset of C99 (CompCert C), most standard optimisations, three or four ISAs. CompCertO extends to module-level composition; CompCertOC to threads with shared stacks; Owlang to a Rust-like ownership frontend. FM-JIT covers a model JIT with dynamic native-code generation.

**Not covered.** CompCert does not verify the C standard library, the OS, the linker, or the hardware. CompCert is *miscompilation-free* but not *bug-free* against an unverified spec. CompCert covers neither all of C nor the LLVM tooling that real industry uses (LLVM has only nascent formal-semantics work). Concurrency in C11/C++11 relaxed-memory models is partially covered (Compositional CompCert, CompCertOC). FM-JIT is a model JIT, not a production engine; it does not yet match V8 or HotSpot in feature coverage.

## §4 May 2026 Status
**Production-grade in safety-critical aerospace/automotive.** AbsInt sells a commercial CompCert with maintenance; it is used in aviation, rail, automotive, and nuclear contexts where DO-178C / IEC 61508 / EN 50128 certification matters. Open-source CompCert remains an active research target with multiple PhD-thesis-scale extensions.

The CompCertO / CompCertOC / 3D-refinement / Owlang line (2021-2025) is a sustained research arc producing tier-1 PLDI / POPL papers each year. Owlang specifically (Oct 2025) is the first verified compiler from a Rust-like ownership language down to assembly with **end-to-end memory-safety preservation including the borrow-check guarantee**.

FM-JIT and the related verified-JIT line have not yet reached production but are the closest extant work to "verify Mochi's vm3jit". The CakeML group's PLDI 2024 keynote called out JIT verification as an open research direction.

## §5 Cost
CompCert itself is roughly **100 000 lines of Coq** for the verified backend, accumulated over ~20 years. Per-pass extensions in the CompCertO/OC/Owlang line are typically 1-3 PhD-years. This is unaffordable for normal development; the value proposition is that the result is *paid for once* and reused.

For applications: verifying a single non-trivial C function on top of CompCert with VST is on the order of weeks of expert effort. The Cornell `libsecp256k1` modular-inverse verification was a multi-person-month effort.

## §6 Mochi Adaptation Note
CompCert and its descendants are the **gold standard Mochi will not meet, and need not pretend to meet**, in MEP-41. The relevant adaptation:

- vm3jit is unverified machine-code generation. CompCert / FM-JIT show what verified equivalents look like; MEP-41 should *acknowledge* the gap and *not* claim memory-safety guarantees that depend on JIT-code correctness. The MEP-41 safety story has to bottom out at: "the JIT is part of the trusted runtime; bugs in the JIT can violate memory safety; we mitigate by fuzzing, by `unsafe`-Go review, and by the optional ability to disable the JIT."
- Owlang's "open safety" framing is *exactly* what Mochi wants: a composable safety property preserved across module boundaries, including modules written in different languages. MEP-41 should adopt the Owlang vocabulary informally even though Mochi has no verified compiler. The relevant invariant for Mochi: every Cell handed across an FFI boundary preserves the (arena_tag, generation) integrity.
- For long-term roadmapping: if Mochi ever wants to claim end-to-end formal verification, FM-JIT + Owlang + CompCertO is the architectural template. That is several MEPs away.
- For *now*: MEP-41 should state plainly that Mochi's TCB includes the Go compiler, the Go runtime (specifically the GC), the Mochi vm3 mark-sweep, and the vm3jit, and that the verification claim is "type safety of the bytecode language assuming the runtime is correct", not "end-to-end machine-code correctness".

## §7 Open Questions for MEP-41
1. Should MEP-41 explicitly distinguish between "type safety of source Mochi" (in scope) and "compiler/runtime correctness" (out of scope, treated as a TCB)?
2. The FM-JIT model factors the impure JIT into specified primitives. Should vm3jit's interface be documented as a small set of *specified primitives* (allocate-exec-page, install-code, flush-i-cache) even though they are unverified? Cheap documentation that maps to the FM-JIT pattern.
3. Owlang's ownership-checker pass is a *frontend* check, not a backend invariant. Mochi's analogue is bytecode verification — should MEP-41 elevate the vm3 bytecode verifier to a "named, separately-discussable component" the way Owlang elevates its checker?
4. Should Mochi sign up to the long-term plan of producing a verified vm3 in a future MEP, with FM-JIT + CompCertO as the template? Or is it more honest to declare verification out of scope permanently and lean on memory-safe-by-construction at the Mochi-source layer?