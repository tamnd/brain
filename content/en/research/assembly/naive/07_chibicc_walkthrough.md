---
title: "chibicc: A Minimal C Compiler as a Mochi Backend Reference"
description: "Rui Ueyama's ~10k LOC C compiler that emits x86-64 GAS assembly directly from a recursive-descent parser. The clearest published example of a single-pass codegen pipeline that produces correct code with no IR, no SSA, no register allocator. The right educational template for a \"naive AOT\" pass of MEP-42."
tags: ["native-codegen", "naive"]
weight: 70
date: 2026-05-18T18:07:50+07:00
---

## §1 Provenance

- Author: Rui Ueyama (Google, prior author of 8cc and the current LLVM lld linker).
- Repository: https://github.com/rui314/chibicc.
- Companion book: "Compiler Book" (Japanese), https://www.sigbus.info/compilerbook (English translation pending).
- License: MIT.
- Status: feature-complete for most C11; ~11.6k GitHub stars, ~1k forks as of 2025.
- Self-hosting: chibicc compiles itself, plus real-world programs like Git, SQLite, and libpng with their test suites passing.

## §2 Technique / contribution

The pipeline is the most readable canonical realization of:

```
tokenize.c       -> tokens
preprocess.c     -> macro-expanded tokens
parse.c          -> typed AST (recursive descent)
codegen.c        -> x86-64 GAS assembly text
```

That's it. No intermediate representation between AST and assembly. No SSA, no liveness, no graph coloring. Each AST node has a direct emit function.

**Shape of codegen** (paraphrased from `codegen.c`):

```c
void gen_expr(Node *node) {
    switch (node->kind) {
    case ND_NUM:
        println("  mov $%d, %%rax", node->val);
        return;
    case ND_VAR:
        gen_addr(node);
        load(node->ty);
        return;
    case ND_ADD:
        gen_expr(node->rhs);
        push();
        gen_expr(node->lhs);
        pop("%rdi");
        println("  add %%rdi, %%rax");
        return;
    ...
    }
}
```

The "register allocator" is the **runtime stack**. Every intermediate value is pushed to memory and popped back. This is dumb, fast to write, and produces correct code.

**Key design choices:**
- One result register convention: `%rax` holds the current expression value, period.
- Function args go in `%rdi, %rsi, %rdx, %rcx, %r8, %r9` per the System V ABI.
- All locals live in stack slots, never in registers across statements.
- Memory: `calloc` for everything, `free` never called. Memory dies when the compiler process exits.
- Output: GAS-syntax assembly text to stdout; the user pipes it to `gcc -xassembler -` to assemble and link.

## §3 Where it shines, where it fails

**Shines:**
- Smallest credible C compiler (~10k LOC) that handles non-trivial programs.
- Commit history is the walkthrough: each commit adds one feature with a small, readable diff.
- No build-time dependency beyond a C compiler.
- Cross-platform by virtue of shelling out to `gcc` for assembly and linkage.

**Fails:**
- Generated code is "probably twice or more slower than GCC's output" per Ueyama's README.
- No optimization pass exists yet (planned, never landed).
- x86-64 only; no portability to arm64/riscv64.
- Memory leak by design (fine for a short-lived compiler, not for a JIT).

## §4 Status (May 2026)

- Repository is healthy. Last meaningful update was 2023, but the design is stable.
- Numerous forks: `stormalf/chibicc` (extended features), `lynn/chibicc` (retargeted to Uxn VM), `pokotsun/chibicc` (per-section book exercise).
- Widely used as the textbook example in modern compiler courses (CMU 15-411, MIT 6.035 lab references).
- Ueyama's "mold" linker draws on the same minimalist philosophy.
- Not a research artifact, no follow-up papers. It is an existence proof.

## §5 Engineering cost for Mochi

A chibicc-style backend for Mochi would mean:

1. Add `compiler3/emit/asm_x86_64.go` (~3000 LOC).
2. Add `compiler3/emit/asm_arm64.go` (~3500 LOC; ARM has more instruction quirks).
3. Walk `compiler3/ir/` node by node, emitting assembly text.
4. Shell out to `cc` (system compiler) for assembly and linkage. On macOS this is Apple clang; on Linux it is whatever `cc` resolves to; on Windows we need `cl.exe` or `clang-cl`.

Estimated cost:
- 4 weeks: x86-64 emitter for full Mochi IR.
- 4 weeks: arm64 emitter.
- 1 week: linker/driver wrapper.
- 2 weeks: corpus testing.

Total: ~11 weeks for two architectures.

The output binary will be 3-10x slower than vm3 interpreted for hot loops (because the stack-push/pop discipline is brutal), but it works. We can later replace the stack discipline with a real register allocator without changing the emitter API.

## §6 Mochi adaptation note

- `compiler3/ir/` provides typed nodes that map to chibicc's AST nodes.
- `compiler3/emit/` is where the per-node emit functions go.
- `runtime/vm3/cell.go` defines the value layout; emitted code loads and stores 8-byte Cell values.
- `runtime/vm3/arenas.go` is the runtime that the emitted binary links against. The binary must call `vm3.AllocInt`, `vm3.AllocString`, etc. for new values.

The key insight from chibicc for Mochi: **start with `cc` as the assembler/linker.** Do not write our own. The system toolchain on every reachable platform already handles ELF/Mach-O/COFF, DWARF debug info, dynamic linking, position-independent code. We can replace it later if we want a zero-dependency Mochi binary.

This is the cheapest possible path to "Mochi source -> native binary on every reachable platform" which is exactly the MEP-42 charter.

## §7 Open questions for MEP-42

- How much of the system toolchain do we tolerate? Always-shell-out is simplest. Pure-Go assembler is more portable but more work.
- chibicc uses pure stack discipline. Should Mochi's first pass do the same, or skip ahead to a tree-walk register assigner?
- Calling convention: System V on Linux/macOS, MS x64 on Windows. Two prologue templates, or wrap with a portable shim?
- DWARF debug info: do we emit it in the first pass? chibicc does not.
- chibicc never calls `free`. Mochi compiler3 should be arena-allocated for the same reason: simplicity and speed.

## §8 References

- chibicc on GitHub: https://github.com/rui314/chibicc.
- Ueyama's "Compiler Book" (Japanese): https://www.sigbus.info/compilerbook.
- Internet Archive mirror of chibicc: https://archive.org/details/github.com-rui314-chibicc_-_2020-10-03_04-42-44.
- Ueyama's mold linker (same author, same minimalist philosophy): https://github.com/rui314/mold.
- 8cc, Ueyama's earlier C compiler: https://github.com/rui314/8cc.