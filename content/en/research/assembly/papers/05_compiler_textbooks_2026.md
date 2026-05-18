---
title: "Compiler Textbooks Relevant to a Naive Mochi Backend (2022-2026)"
description: "The published material a Mochi engineer should keep open while implementing MEP-42 phase 1. Cooper/Torczon 3rd ed for the canonical theory, Nystrom for a hands-on bytecode compiler walkthrough, Appel for the verified-compiler-curious, plus 2024-2026 course materials covering naive backends."
tags: ["native-codegen", "papers"]
weight: 50
date: 2026-05-18T18:13:12+07:00
---

## §1 Provenance

- Cooper, Torczon, *Engineering a Compiler*, 3rd ed, Morgan Kaufmann, Nov 21 2022. ISBN 978-0-12-815412-0. Won the TAA Textbook Excellence Award 2024.
  - Publisher page: https://shop.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0.
  - ScienceDirect: https://www.sciencedirect.com/book/9780128154120/engineering-a-compiler.
- Nystrom, Robert, *Crafting Interpreters*, Genever Benning, 2021. Free online: https://craftinginterpreters.com/.
- Appel, Andrew W., *Modern Compiler Implementation in ML* (1998) / *Java* (2002) / *C* (1998). Cambridge UP. Long-running canonical textbook. https://www.cs.princeton.edu/~appel/modern/.
- Aho, Lam, Sethi, Ullman, *Compilers: Principles, Techniques, and Tools*, 2nd ed (the Dragon Book), Addison-Wesley, 2006.
- Wirth, Niklaus, *Compiler Construction*, free PDF: https://people.inf.ethz.ch/wirth/CompilerConstruction/.
- Muchnick, Steven, *Advanced Compiler Design and Implementation*, Morgan Kaufmann, 1997.
- 2024-2026 course materials: CMU 15-411 (Compiler Design), MIT 6.035, Stanford CS143/CS343 lecture notes (publicly available).

## §2 Technique / contribution

### Cooper & Torczon 3rd ed (2022)
Restructured from the 2nd ed: separate chapters on semantic elaboration, runtime support for naming and addressability, and code shape. The order of chapters that matters to MEP-42:

- Ch 7: Code Shape (how AST patterns translate to target ops).
- Ch 11: Instruction Selection (tile-based matching, dynamic programming).
- Ch 12: Instruction Scheduling (list scheduling, software pipelining).
- Ch 13: Register Allocation (graph coloring, linear scan, plus new coverage of local bottom-up allocation).

The book reflects the authors' own decades of research at Rice on graph-coloring allocation, live-range splitting, and rematerialization.

### Nystrom, Crafting Interpreters (2021, free online)
- Two interpreters end to end: a tree-walking one in Java (jlox) and a bytecode VM in C (clox).
- The clox compiler is a Pratt-parser-driven single-pass compiler that emits bytecode directly. No AST.
- Pratt parsing chapter is widely cited as the clearest published explanation.
- NaN-boxing, Lua-style upvalues, and a simple mark-and-sweep GC are all covered.
- Most practically: clox demonstrates the engineering of a single-pass compiler in ~3000 LOC.

### Appel, Modern Compiler Implementation
- The "Tiger language" running example takes you from lexer through register allocation in three editions (ML, Java, C).
- The register-allocation chapter is the standard introduction to graph coloring with iterated coalescing.
- Pairs naturally with CompCert (Appel's framework underpins much verified compiler work).

### Wirth, Compiler Construction
- The Oberon-2 reference compiler in ~3000 LOC of Oberon source.
- Single-pass design, recursive descent, direct emit.
- Free PDF, demonstrates "one person can build a compiler" thesis.

### 2024-2026 course materials
- CMU 15-411: https://www.cs.cmu.edu/~janh/courses/411/. Project: build a C0 compiler. Covers SSA register allocation, linear scan, instruction selection.
- MIT 6.035: https://6.035.csail.mit.edu/. Project: build a Decaf compiler.
- Stanford CS343/CS242: lecture notes on compiler design, includes baseline JIT material.
- UWaterloo CS444: compiler construction with focus on object-oriented backends.

## §3 Where each book shines, where it fails

### Cooper/Torczon
- **Shines**: theory + practice balance. The register allocation chapter alone is worth the book.
- **Fails**: light on JIT-specific topics. No coverage of inline caches or template JITs.

### Nystrom
- **Shines**: hands-on, free, with full source. The clox VM is essentially a small Mochi vm3 prototype.
- **Fails**: no native codegen at all. Stops at bytecode VM.

### Appel
- **Shines**: rigorous treatment of register allocation, instruction selection via tree-pattern matching.
- **Fails**: dated examples (Tiger is from 1990s pedagogy). The ML edition is the cleanest; the Java edition shows its age.

### Wirth
- **Shines**: proves you can build a real compiler in a textbook-sized codebase.
- **Fails**: targets only Wirth's own RISC ISA; cross-arch advice is minimal.

### Modern course materials
- **Shines**: free, current, well-tested in classroom environments.
- **Fails**: typically target a teaching language (C0, Decaf) that's smaller than Mochi.

## §4 Status (May 2026)

- Cooper/Torczon 3rd ed is the dominant graduate textbook. Award-winning, recently revised.
- Nystrom continues to update *Crafting Interpreters* online; the book has become the de facto on-ramp for hobby language implementers.
- Appel's series is still in print but not updated; ML edition (1998) is the most-recommended.
- Dragon Book is widely considered outdated for modern practitioners; useful for parsing theory only.
- Wirth's book remains a niche but inspirational reference.
- CMU 15-411 and MIT 6.035 update their materials yearly; both maintain GitHub repos with student starter code.

## §5 Engineering cost for Mochi

Zero direct integration cost. These are reference materials.

But: organizing a Mochi study cycle around these books would be a force-multiplier. Suggested reading list for the MEP-42 implementation team:

1. Nystrom Ch 14-30 (Part III, the C clox bytecode VM): 2 weeks.
2. Cooper/Torczon Ch 7, 11, 13: 3 weeks.
3. chibicc source walk (1 commit per day): 3 weeks.
4. Liftoff + Sparkplug source skim with V8 blog posts: 2 weeks.

Total reading: ~10 weeks for the team. Pays for itself in fewer design dead ends.

## §6 Mochi adaptation note

- `runtime/vm3/` is structurally close to Nystrom's clox: stack-based bytecode VM with typed values.
- `compiler3/ir/` should be informed by Cooper/Torczon Ch 4 (Intermediate Representations).
- `compiler3/regalloc/` lifts directly from Cooper/Torczon Ch 13 and Appel's chapter on coloring.
- `compiler3/emit/` borrows shape from chibicc's `codegen.c`.

## §7 Open questions for MEP-42

- Do we adopt a standard textbook IR shape (e.g., SSA), or stay with the vm3 stack-machine bytecode through the whole pipeline?
- Should we publish a Mochi-flavored "Crafting Interpreters" companion as documentation?
- How much of the textbook material do we want in our internal design docs vs links to external sources?

## §8 References

- Cooper/Torczon 3rd ed: https://shop.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0.
- Crafting Interpreters: https://craftinginterpreters.com/.
- Crafting Interpreters table of contents: https://craftinginterpreters.com/contents.html.
- Appel's Modern Compiler Implementation: https://www.cs.princeton.edu/~appel/modern/.
- Wirth Compiler Construction PDF: https://people.inf.ethz.ch/wirth/CompilerConstruction/.
- CMU 15-411 course page: https://www.cs.cmu.edu/~janh/courses/411/.
- chibicc (companion to Ueyama's Japanese book): https://github.com/rui314/chibicc.
- Nystrom's "Crafting Crafting Interpreters" post-mortem: https://journal.stuffwithstuff.com/2020/04/05/crafting-crafting-interpreters/.