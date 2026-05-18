---
title: "POPL 2024 and 2025: Compiler-Construction Papers"
description: "Recent foundational work from POPL and its co-located CPP (Certified Programs and Proofs) workshop on verified compilation, secure calling conventions, and packet-filter codegen. Less directly applicable to a \"naive emitter\" than PLDI, but instructive for the verification story MEP-42 may eventually want."
tags: ["native-codegen", "papers"]
weight: 20
date: 2026-05-18T18:11:03+07:00
---

## §1 Provenance

- POPL 2024: 51st ACM SIGPLAN Symposium on Principles of Programming Languages, London, UK, Jan 17-19 2024. Proceedings in PACMPL vol 8, no POPL: https://dl.acm.org/toc/pacmpl/2024/8/POPL.
- POPL 2025: 52nd edition, Denver, CO, USA, Jan 19-25 2025. Proceedings in PACMPL vol 9, no POPL: https://dl.acm.org/toc/pacmpl/2025/9/POPL.
- Co-located: CPP 2024, CPP 2025 (Certified Programs and Proofs); PriSC 2024 (Principles of Secure Compilation).

## §2 Technique / contribution

### 1. PfComp: A Verified Compiler for Packet Filtering Leveraging Binary Decision Diagrams (CPP 2024 at POPL 2024)
- Authors: Clément Chavanon, Frédéric Besson, Tristan Ninet (Inria Rennes).
- Site: https://popl24.sigplan.org/details/CPP-2024-papers/15/.
- Idea: Compile stateless firewall policies to BDDs, optimize the BDD shape, then lower to Clight (CompCert's intermediate C-like IR). Prove the whole pipeline correct in Coq, extract to OCaml.
- Result: Generated code outperforms sequential rule evaluation for large rule sets.
- Mochi relevance: PfComp's "compile DSL to CompCert-IR" pattern is a possible AOT path for Mochi-as-DSL embedded in C tooling. Not phase-1, but worth noting.

### 2. Secure Calling Conventions for CHERI Capability Machines in Practice (PriSC 2024 at POPL 2024)
- Authors: Storme, Huyghebaert, Keuchel, Van Strydonck, Devriese.
- Site: https://popl24.sigplan.org/details/prisc-2024-papers/6/.
- Idea: Formalize and implement secure calling conventions for CHERI machines, focused on temporal memory safety and well-bracketed control flow.
- Mochi relevance: CHERI may be a Mochi target in the future. The secure-calling-convention story matters for sandbox-style deployments (e.g., Mochi-as-WASI-replacement).

### 3. Formally Verified Hardening of C Programs Against Hardware Fault Injection (CPP 2025 at POPL 2025)
- Authors: Basile Pesin, Sylvain Boulmé, David Monniaux, Marie-Laure Potet (VERIMAG, Grenoble).
- Site: https://popl25.sigplan.org/details/CPP-2025-papers/10/.
- Idea: Insert control-flow checks and redundancies into CompCert-compiled code to defend against fault injection (laser, EM). Prove the hardening preserves semantics and provides the desired protection.
- Mochi relevance: nothing immediate. Useful for hardened-target Mochi deployment (smartcards, secure enclaves) in the distant future.

### 4. Compiler Correctness Workshops (general POPL trend)
- CPP 2024-2025 saw increased attention to verified compiler passes: register allocation in CompCert, instruction selection in CakeML, and integer-overflow analyses.
- Worth tracking via the POPL co-located workshops page.

### 5. Veri-CHERI and adjacent work
- POPL 2024-2025 had several PriSC papers building toward proven sandboxing for both managed (Wasm) and unmanaged (CHERI-C) settings.
- These intersect with MEP-42's "secure baseline JIT" question if we ever go down that road.

### 6. CertiKOS, CompCert and CakeML talks
- POPL 2024-2025 keynotes and invited talks repeatedly featured CompCert (Xavier Leroy) and CakeML (Magnus Myreen) as the canonical verified-compiler references.
- For MEP-42, the practical takeaway: verified compilation is feasible in principle, but adds an order of magnitude of effort. Not for phase 1.

## §3 Where it shines, where it fails

POPL is the wrong venue to look for fast-and-dirty emitter techniques. POPL papers tend to be 10x more work to implement and deliver verification guarantees that we are not paying for in a phase-1 baseline.

**Useful patterns from POPL 2024-2025:**
- Use of CompCert/Clight as an intermediate target. Lets us inherit CompCert's verified backend essentially for free if we are willing to emit Clight-shaped C.
- The BDD-based PfComp pattern shows that DSL-to-Clight is a viable cheap-correctness path.
- The PriSC line tells us that calling conventions are formally tractable; if we want to specify Mochi's CC in a paper, the templates exist.

**What POPL does not give us:**
- A baseline JIT design. That belongs to CGO and PLDI.
- Cheap codegen tricks. POPL tends to be about correctness, not speed.

## §4 Status (May 2026)

- All papers cited are published in PACMPL with stable DOIs.
- CompCert is in its 3.x line as of 2025, still actively maintained.
- CakeML had a major update in 2024 with improved register allocation proof.
- CHERI Morello (Arm's CHERI dev board) is shipping; PriSC papers are increasingly evaluated on real silicon.

## §5 Engineering cost for Mochi

For phase-1 MEP-42: zero. None of these techniques are required.

For a hypothetical "Verified Mochi" effort:
- Targeting CompCert Clight: ~6 months (rewrite compiler3 in OCaml or use C-via-textual-bridge).
- Verifying our own backend in Coq or Lean: ~24+ months. Major research project.
- BDD-based optimization for Mochi's pattern-match constructs: ~3-6 weeks. Tractable.

## §6 Mochi adaptation note

- `compiler3/ir/` could lower to Clight as an alternative backend. This is an attractive "verified Mochi" path that costs less than rolling our own verified backend.
- `compiler3/opt/` is where a PfComp-style BDD pass for Mochi `match` expressions would go.
- `runtime/vm3/cell.go` and the arena model do not have a verified counterpart yet; would need new Coq/Lean development.

## §7 Open questions for MEP-42

- Do we want verifiability as a phase-2 or phase-3 goal? If yes, CompCert-Clight is the cheapest path.
- For CHERI/Morello support: phase-3 or later.
- Pattern-matching codegen: should we adopt the BDD strategy from PfComp for Mochi's `match` construct?
- Calling-convention specification: do we want a paper-quality formal CC, or is "matches System V" enough?

## §8 References

- POPL 2024 papers: https://popl24.sigplan.org/track/POPL-2024-popl-research-papers.
- POPL 2025 papers: https://popl25.sigplan.org/track/POPL-2025-popl-research-papers.
- PACMPL POPL 2024 issue: https://dl.acm.org/toc/pacmpl/2024/8/POPL.
- PACMPL POPL 2025 issue: https://dl.acm.org/toc/pacmpl/2025/9/POPL.
- CPP 2024: https://popl24.sigplan.org/home/CPP-2024.
- CPP 2025: https://popl25.sigplan.org/home/CPP-2025.
- CompCert: https://compcert.org/.
- CakeML: https://cakeml.org/.