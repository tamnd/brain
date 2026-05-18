---
title: "Classical Single-Pass Code Generation"
description: "Tree-walk to tuples to native assembly. The textbook recipe from the Dragon Book and Cooper/Torczon, still the right starting point when you want correctness before performance."
tags: ["native-codegen", "naive"]
weight: 40
date: 2026-05-18T18:05:41+07:00
---

## §1 Provenance

- Aho, Sethi, Ullman, "Compilers: Principles, Techniques and Tools" (the Dragon Book), 1st ed 1986, 2nd ed (Aho, Lam, Sethi, Ullman) 2006. ISBN 0-321-48681-1.
- Cooper, Torczon, "Engineering a Compiler," 3rd ed, Morgan Kaufmann, Nov 2022 (ISBN 978-0-12-815412-0). Won the TAA Textbook Excellence Award in 2024.
  - Publisher page: https://shop.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0.
  - ScienceDirect TOC: https://www.sciencedirect.com/book/9780128154120/engineering-a-compiler.
- Muchnick, "Advanced Compiler Design and Implementation," 1997 (still cited).
- Wirth, "Compiler Construction" (free PDF from ETH).

## §2 Technique / contribution

"Single-pass" here means: in one traversal of the AST or IR, generate target code directly, no separate optimization pass.

**Pipeline shape:**

```
source --lex--> tokens --parse--> AST --typecheck--> annotated AST
       --walk--> instruction tuples --emit--> assembly text
```

The walk is the canonical recursive descent. For an expression `a + b * c`, you:
1. Walk the `+` node.
2. Recurse left, emit `mov r1, [a]`.
3. Recurse right's `*`, emit `mov r2, [b]; imul r2, [c]`.
4. Emit `add r1, r2; mov [tmp], r1`.

**Register allocation choices** (Cooper/Torczon Chapter 13):
- **Local, next-use**: track which temporaries are used next; spill the temporary used furthest in the future. O(n) per basic block.
- **Tree-walk**: assign registers during AST traversal using a simple stack discipline; spill when stack exceeds physical registers.
- **Stack machine emit**: skip registers entirely and push/pop. Slowest at runtime but trivially correct.

**Calling conventions** are punted to the platform ABI (System V AMD64 ABI for Linux/macOS x86-64; AAPCS64 for arm64). The compiler emits `call f` and lets the platform tools resolve.

## §3 Where it shines, where it fails

**Shines:**
- Smallest possible compiler. A complete single-pass C-ish backend is ~2000 LOC.
- Compile time is linear in source size with tiny constants.
- Easy to debug: emit pretty-printed asm and read it.
- Pedagogically clear; well-trodden path.

**Fails:**
- Code quality is 3-10x slower than -O2.
- No common subexpression elimination, no dead code elimination, no loop hoisting.
- Spill-heavy on register-poor ISAs (x86 in 32-bit mode was a nightmare; x86-64 with 16 GPRs is fine).
- Cannot exploit SIMD or any hardware feature beyond what the AST shape suggests.

Compile time profile: O(n) source lines, ~100,000-1,000,000 lines/sec for a hand-written emitter.

## §4 Status (May 2026)

- Universal default for educational compilers (e.g., chibicc, Wirth's Oberon-2 compiler, ML/Camlight).
- Used in production by **Go's compiler in its early days** (Go 1.0-1.4 single-pass walk, replaced by SSA in 1.7).
- Cooper/Torczon 3rd ed is the modern textbook of record; refreshed Sept 2022, won TAA award 2024.
- Newer treatments: Appel's "Modern Compiler Implementation" series (ML/Java/C versions), Crafting Interpreters (Nystrom, free at https://craftinginterpreters.com/) for a clox-style single-pass bytecode compiler.
- No "deprecation" because it is the floor of compiler engineering.

## §5 Engineering cost for Mochi

A single-pass Mochi backend that emits x86-64 GAS or NASM assembly text:

- 1 week: bootstrap an `EmitContext` with a label allocator, a tiny string-table for symbols, a spill-slot allocator.
- 2 weeks: per-op emit functions, one per `compiler3/ir/Op`. Each function reads operands from `Cell`s and emits 1-10 instructions.
- 1 week: function prologue/epilogue, calling convention plumbing.
- 1 week: shell out to GNU `as` and `ld` (or `cc` for linkage). On macOS, use the system `clang -c -o`.
- 1 week: smoke tests against the corpus in `compiler3/corpus/`.

Total: ~6 weeks for a working x86-64 backend that produces correct (but slow) binaries.

This is the cheapest possible Mochi-to-native path. The output binary will be 5-10x slower than vm3 interpreted for hot loops (because of frame-slot bouncing), but for cold startup it can be 20x faster.

## §6 Mochi adaptation note

- `compiler3/ir/` already has a typed IR. Walk it node by node.
- `compiler3/regalloc/` exists as a stub. A naive next-use allocator goes here; later we can replace with linear-scan or graph-coloring without touching the emitter.
- `compiler3/emit/` is the natural home for the per-op emit functions.
- `runtime/vm3/cell.go` defines Cell, which the emitted code manipulates as `uint64_t` values.
- `runtime/vm3/arenas.go` provides the typed arena pointers that the emitted code dereferences. Reserve a callee-save register (R15) as the "arena base" pointer.

The single-pass approach is the right starting point for **AOT** specifically. For JIT, copy-and-patch wins on simplicity.

## §7 Open questions for MEP-42

- Do we emit assembly text and shell out to `as`, or do we link directly via a Go assembler library?
- If we shell out, can we tolerate the dependency on the platform toolchain (`cc` on macOS, `as`+`ld` on linux, `link.exe` on Windows)?
- What's the spill strategy when we run out of registers? Stack slot? Arena handle?
- Calling convention: System V vs AAPCS64 vs Mochi-internal?
- Do we support inline assembly in Mochi source, the way C does? If so, this affects the IR shape.
- Debug info: do we emit DWARF in the first pass, or punt to MEP-44?

## §8 References

- Cooper, Torczon, "Engineering a Compiler," 3rd ed, 2022 (https://shop.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0).
- Aho, Lam, Sethi, Ullman, "Compilers: Principles, Techniques, and Tools," 2nd ed, 2006.
- Bob Nystrom, "Crafting Interpreters," free at https://craftinginterpreters.com/.
- Andrew Appel, "Modern Compiler Implementation in ML/Java/C," Cambridge UP.
- Niklaus Wirth, "Compiler Construction," 2005 free PDF, https://people.inf.ethz.ch/wirth/CompilerConstruction/.