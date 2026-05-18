---
title: "Sparkplug: V8's Non-Optimizing Baseline JavaScript Compiler"
description: "A single-pass, IR-free transpiler from Ignition bytecode to native machine code, designed to add a fast tier between an interpreter and an optimizer with minimal engineering cost."
tags: ["native-codegen", "naive"]
weight: 10
date: 2026-05-18T18:03:33+07:00
---

## §1 Provenance

- Designer: Leszek Swirski (V8 team, Google).
- Released: V8 v9.1, May 2021.
- Primary source: V8 blog post "Sparkplug, a non-optimizing JavaScript compiler" (https://v8.dev/blog/sparkplug).
- Source code: V8 source tree under `src/baseline/` (https://chromium.googlesource.com/v8/v8/).
- Related research framing: Ben L. Titzer, "Whose Baseline Compiler Is It Anyway?" CGO 2024 (https://dl.acm.org/doi/10.1109/CGO57630.2024.10444855), arXiv preprint https://arxiv.org/pdf/2305.13241.
- Lineage references: V8 Full-Codegen (2008+, retired around v5.9 in 2017) and Crankshaft (also retired in the same window). HotSpot template interpreter (~2002) is the conceptual ancestor.

## §2 Technique / contribution

Sparkplug is a one-shot, single-pass compiler that walks Ignition bytecode and emits a fixed sequence of x86-64 or arm64 instructions for each opcode. It does not build an IR, perform liveness analysis, or run a register allocator. The full compiler is structured as `for each bytecode op: switch (op) { case kAdd: emitAddTemplate(); ...}`.

Two design decisions make it shockingly cheap:

1. **Frame-compatible with Ignition.** A Sparkplug stack frame stores the same register values, in the same slots, as the interpreter would have. This means Ignition and Sparkplug can OSR into each other trivially. Debugger, profiler, stack-walker, and exception-handler code paths are unchanged.
2. **Slow paths delegated to shared builtins.** Anything complex (property access miss, allocation, IC miss) becomes a call to a pre-built runtime stub. Sparkplug never emits the full semantics inline.

Shape of generated code for an Ignition `Add r1` (pseudo-x86-64):

```
mov  rax, [rbp - accum_slot]   ; load accumulator
mov  rdx, [rbp - r1_slot]      ; load operand
; smi-fastpath
mov  rcx, rax
or   rcx, rdx
test rcx, 1
jnz  slow_add_stub             ; tagged-pointer? jump out of line
add  rax, rdx
jo   slow_add_stub
mov  [rbp - accum_slot], rax
```

Local peephole optimization is applied (e.g., constant fold of consecutive loads), but nothing global.

## §3 Where it shines, where it fails

**Shines:**
- Compiles ~10x faster than TurboFan because there is no IR allocation or graph rewrite.
- Produces code that runs ~5x to ~10x faster than Ignition by removing dispatch overhead alone.
- Cheap to maintain: each bytecode op gets one template function.
- Trivial OSR thanks to frame compatibility.

**Fails:**
- No register allocation across bytecodes, so values bounce through frame slots.
- Cannot speculate on type (V8 leaves that to Maglev and TurboFan).
- Branch shape is fixed per op, so cold paths still pay full Smi-check cost.
- Code-quality ceiling: V8 reports only 5-15% wall-clock gain on Speedometer and browsing benchmarks vs interpreter alone.

Compile-time profile: linear in bytecode length, no allocation hotspots, code-gen rate measured in tens of MB/s of machine code emitted.

## §4 Status (May 2026)

- Sparkplug ships in every V8 release since 9.1 (Chrome, Node, Deno, Edge). Still the active baseline tier.
- Joined by **Maglev** (V8, 2023+) as a mid-tier between Sparkplug and TurboFan. Sparkplug was not deprecated: Maglev sits above it.
- Cited as the design touchstone in Titzer 2024 ("Whose Baseline Compiler Is It Anyway?") which compares Liftoff, sm-base, and Sparkplug.
- The "frame-compatible baseline" pattern has been picked up by every new VM baseline written since.

## §5 Engineering cost for Mochi

A Mochi-equivalent of Sparkplug would be a compiler3-only addition layered on top of vm3:

- One Go file per opcode family (`sparkplug_arith.go`, `sparkplug_loadstore.go`, etc.), each exposing `emit<Op>(asm *Assembler, ip *vm3.Inst)`.
- A small in-process assembler (~3,000 LOC for one ISA). Pure Go, no cgo.
- A frame layout that mirrors `runtime/vm3/frame.go` register banks bit-for-bit, so on-stack replacement is a no-op.
- Slow-path stubs reuse the existing `runtime/vm3` opcode implementations as runtime functions (we already have them, we just `call`/`jmp` to them).
- Estimated cost: ~6 weeks of engineering for x86-64 alone, +3 weeks per additional ISA, +2 weeks for OSR/debugger integration.

Importantly, this can ship per-platform: arm64 macOS and x86-64 linux first, the rest as time permits.

## §6 Mochi adaptation note

Map to existing Mochi files:

- `runtime/vm3/op.go` defines the opcode set. Sparkplug-Mochi's per-op emit functions key off this enum.
- `runtime/vm3/frame.go` defines the three-bank register file. The Sparkplug frame would mirror this exactly so vm3 interpreter and Sparkplug code share the same `Frame` layout.
- `runtime/vm3/cell.go` (8-byte handle Cell) is the value the assembler moves around. Smi/tag checks become a single `test` against the discriminator bits.
- `compiler3/emit/` is where the per-op templates live. Add a sibling package `compiler3/baseline/`.
- Slow-path stubs are simply calls back into `runtime/vm3` opcode handlers, called via Go `cgo` thunks or pre-compiled trampolines.

## §7 Open questions for MEP-42

- Do we want Sparkplug-style frame compatibility, or do we want vm3-native register lifetime tracking from day one? Frame compatibility costs runtime perf but saves engineering.
- How aggressive should slow-path inlining be? Sparkplug never inlines; do we?
- Should Mochi-Sparkplug emit position-independent code (PIC) so we can mmap once and reuse? V8 does, but it is harder than non-PIC.
- Calling convention: do we adopt the System V AMD64 ABI for stubs, or invent a Mochi-internal one that's friendlier to our typed arenas?
- Tier-up policy: at what call-count or loop-iteration count do we tier from vm3 interpreter to Mochi-Sparkplug?

## §8 References

- V8 Blog, "Sparkplug, a non-optimizing JavaScript compiler" (https://v8.dev/blog/sparkplug).
- Ben L. Titzer, "Whose Baseline Compiler Is It Anyway?" CGO 2024 (https://arxiv.org/pdf/2305.13241).
- V8 source code, `src/baseline/` directory in Chromium tree.
- Yan Guly, "Sparkplug, V8 baseline JavaScript compiler" walkthrough (https://medium.com/@yanguly/sparkplug-v8-baseline-javascript-compiler-758a7bc96e84).