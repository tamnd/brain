---
title: "Wasm Baseline Compilers: Liftoff, RabaldrMonkey, Winch"
description: "A converged design pattern across three independent implementations: per-opcode template emission, a virtual operand stack with lazy register promotion, no IR, no global optimization. The current state of the art in \"fast and simple\" Wasm code generation."
tags: ["native-codegen", "naive"]
weight: 50
date: 2026-05-18T18:06:46+07:00
---

## §1 Provenance

- **V8 Liftoff** (Clemens Backes et al.), 2018+. V8 blog: https://v8.dev/blog/liftoff. Source: https://chromium.googlesource.com/v8/v8/+/refs/heads/master/src/wasm/baseline/liftoff-compiler.cc.
- **SpiderMonkey RabaldrMonkey** (a.k.a. sm-base, Lars T. Hansen et al.), 2017+. Source in mozilla-central `js/src/wasm/WasmBaselineCompile.cpp`.
- **Wasmtime Winch** (Bytecode Alliance, lead by Saul Cabrera at Shopify and Chris Fallin), 2023+. RFC: https://github.com/bytecodealliance/rfcs/blob/main/accepted/wasmtime-baseline-compilation.md. README: https://github.com/bytecodealliance/wasmtime/blob/main/winch/README.md.
- Comparative study: Ben L. Titzer, "Whose Baseline Compiler Is It Anyway?" CGO 2024, https://dl.acm.org/doi/10.1109/CGO57630.2024.10444855, arXiv https://arxiv.org/pdf/2305.13241.

## §2 Technique / contribution

The Wasm baseline pattern is:

1. **Single pass over Wasm bytecode** in source order.
2. **Per-opcode template**: each `wasm::Op` emits a canned sequence of native instructions. No IR.
3. **Virtual operand stack**: rather than always materializing values into the real Wasm operand stack in memory, the compiler keeps an abstract stack of `(slot_kind, slot_value)`. Slot kinds are `Register(r)`, `Stack(off)`, `Constant(c)`, `Memory(ptr)`. Values move to physical registers only when used.
4. **Lazy spill**: when running out of registers, spill the least-recently-used virtual slot to a fixed memory stack frame.
5. **Constant propagation locally**: if the top of the operand stack is `Constant(c)`, op emit can fold against it (`i32.add` of a constant becomes `lea` with a displacement).

**Shape of emitted code for Wasm `i32.add`:**

```
;; assume virtual stack = [..., Register(rax), Constant(0x10)]
;; native emit:
add eax, 0x10
;; virtual stack -> [..., Register(rax)]
```

If both operands were in registers:
```
add ecx, eax   ; or pick whichever is dst
```

If one was spilled:
```
mov ebx, [rbp - 16]
add eax, ebx
```

This "multi-register-allocation" trick (one virtual slot can name multiple physical registers) is what Titzer 2024 identifies as the key code-quality win over straight templates.

Wasm baseline compilers do not need type feedback because Wasm is already statically typed. They do not need IC slots because there is no dynamic dispatch in Wasm MVP. This is why they are smaller than JS baselines.

## §3 Where it shines, where it fails

**Shines:**
- Compile speed: tens of MB of machine code per second. Liftoff compiles 39.5 MB of Wasm in seconds versus 30+ seconds for TurboFan.
- Code quality: ~1.1x to 1.5x slower than the optimizing tier (Sightglass benchmarks, per Bytecode Alliance RFC), at 15-20x faster compile speed.
- Predictable: linear in input size, no surprise super-linear passes.
- Streaming-friendly: Liftoff can begin executing the first function before the rest of the module has been parsed.

**Fails:**
- No cross-function optimization, no inlining.
- Spill choices are local, so loops with many live variables produce thrashy code.
- No SIMD scheduling, no vectorization.
- Per-ISA backend is still ~5,000 LOC, which is non-trivial.

## §4 Status (May 2026)

- **Liftoff**: V8's default Wasm baseline since 2018. Mature, widely deployed in Chrome/Edge/Node.
- **sm-base (RabaldrMonkey)**: Firefox's default Wasm baseline.
- **Winch**: Wasmtime's baseline, marked production-ready for x86-64 in Wasmtime 21 (mid-2024), arm64 stabilizing through 2025. Now the default startup tier for many Wasm-on-server deployments.
- Titzer 2024 paper compared Liftoff, sm-base, and his research compiler "Wizard" and found Liftoff's multi-register-allocation strategy reduces emitted code size by ~12% over naive templates.
- The Cranelift/Winch split (optimizing vs baseline) inspired similar splits in newer engines.

## §5 Engineering cost for Mochi

Mochi's bytecode is not Wasm, but vm3's design is very Wasm-like: typed stack/register model, no dynamic dispatch in the hot path, statically known operand types.

A Mochi-Liftoff would cost:

- 1 week: virtual-stack abstraction (Go struct + slot enum).
- 3 weeks: per-op emit functions for the ~100 Mochi ops, x86-64 only.
- 2 weeks: spill management and frame layout.
- 2 weeks: control flow (forward branches, loop backedges, label resolution).
- 2 weeks: function call lowering with our calling convention.
- 4 weeks per additional ISA (arm64 next; riscv64 later).

Total: ~10 weeks for an x86-64 Mochi-Liftoff.

This is more work than copy-and-patch but produces significantly better code (constants are folded, registers track across ops).

## §6 Mochi adaptation note

- `runtime/vm3/op.go`: enumerates the opcodes that need templates.
- `runtime/vm3/frame.go`: the three-bank register file (int, float, ptr) maps naturally to three groups of physical registers that the virtual stack can promote into.
- `runtime/vm3/arenas.go`: arena base pointers occupy fixed callee-save registers (e.g., R12-R14 on x86-64).
- `compiler3/regalloc/` provides a stub regalloc package; the virtual-stack approach replaces it entirely (no live-range analysis needed).
- `compiler3/emit/` is the natural home for the per-op template functions.
- `compiler3/ir/` provides the typed ops that drive the template selection.

Mochi can do better than Wasm baselines because Mochi has the **typed arena layout** known at compile time. We can emit one template per (op, arena-tuple) combination, eliminating arena-base lookups for known-typed operands.

## §7 Open questions for MEP-42

- Virtual-stack data structure: `[]Slot` with O(n) pop, or a fixed-size circular buffer? Liftoff uses a fixed buffer.
- Spill choice: LRU (Liftoff), random (RabaldrMonkey), or live-range-driven (more like an optimizing pass)?
- Do we track per-slot type info beyond what Mochi IR already encodes? Constants? Ranges?
- Tier-up policy: how do we decide when to recompile a hot function with an optimizing backend?
- Code cache eviction: when the baseline buffer fills, what do we discard?

## §8 References

- V8 Blog, "Liftoff: a new baseline compiler for WebAssembly in V8" (https://v8.dev/blog/liftoff).
- V8 Docs, "WebAssembly compilation pipeline" (https://v8.dev/docs/wasm-compilation-pipeline).
- Wasmtime Winch README (https://github.com/bytecodealliance/wasmtime/blob/main/winch/README.md).
- Wasmtime baseline RFC (https://github.com/bytecodealliance/rfcs/blob/main/accepted/wasmtime-baseline-compilation.md).
- Ben Titzer, "Whose Baseline Compiler Is It Anyway?" CGO 2024 (https://arxiv.org/pdf/2305.13241).
- Bytecode Alliance 2023 retrospective (https://bytecodealliance.org/articles/wasmtime-and-cranelift-in-2023).