---
title: "Copy-and-Patch as a Code-Generation Backend for Mochi"
description: "Stencil-based binary stitching from OOPSLA 2021, now shipping in CPython 3.13/3.14."
tags: ["native-codegen", "backends"]
weight: 60
date: 2026-05-18T18:07:50+07:00
---

## §1 Provenance
- Original paper: Haoran Xu and Fredrik Kjolstad, "Copy-and-patch compilation: a fast compilation algorithm for high-level languages and bytecode," **OOPSLA 2021** (PACMPL Vol. 5 Article 136). Note: the task brief said PLDI 2021; the paper is actually OOPSLA 2021.
- ACM: https://dl.acm.org/doi/10.1145/3485513
- arXiv preprint: https://arxiv.org/abs/2011.13127
- Author page (Fredrik Kjolstad): http://fredrikbk.com/copy-and-patch.html
- Stanford talk slides: https://aha.stanford.edu/sites/g/files/sbiybj20066/files/media/file/aha_050621_xu_copy-and-patch.pdf
- Wikipedia summary: https://en.wikipedia.org/wiki/Copy-and-patch
- PEP 744 (Python JIT): https://peps.python.org/pep-0744/
- LWN follow-up (2025): https://lwn.net/Articles/1029307/
- Real Python writeup: https://realpython.com/python313-free-threading-jit/
- Follow-on research: Deegen (OOPSLA 2026), Partial-Evaluation Templates (CGO 2026), TPDE (CGO 2026).

## §2 Mechanism
The compiler does its hard work **once, at build time**: it takes a library of micro-op implementations (in C or LLVM IR), compiles each one with Clang+LLVM into a "stencil" object file with relocations left unfilled. At runtime, the compiler walks the input bytecode/AST, looks up the stencil for each op, **copies** the machine bytes into a writable page, and **patches** the relocation holes with concrete addresses, literals, and jump targets. The result is native code without ever invoking an instruction selector, register allocator, or assembler at runtime.

Key properties:
- **No IR at runtime**. The "compiler" is a relocation table walker plus a memcpy.
- **No register allocator**. The stencil generator (the offline tool, dubbed "MetaVar" in the paper) explores stencil variants for different register-residency patterns; the runtime picks the right variant.
- **Code quality** is excellent on micro-benchmarks because each stencil was produced by Clang `-O2`. Cross-stencil optimization (constant propagation across ops, etc.) is impossible: that is the price.

Numbers from the paper: 1666 stencils, 35 KB for a Wasm baseline JIT; 98,831 stencils, 17.5 MB for a high-level C-like language compiler.

## §3 Target coverage (May 2026)
Copy-and-patch is a **technique**, not a library, so target coverage equals "whatever LLVM/Clang can produce object files for." Concretely shipping:
- CPython's JIT (Brandt Bucher's implementation, PEP 744) builds stencils with Clang on x86_64 Linux/Windows/macOS, AArch64 Linux/macOS, riscv64 Linux. Windows AArch64 and Wasm are not yet enabled in CPython's JIT.
- Wasm baseline tier (the paper's WaJIT prototype) demonstrated x86_64.

The stencil generation step needs Clang at build time. Once built, the runtime needs zero compiler dependencies (just an executable-memory allocator).

## §4 Production / language adoption status (May 2026)
- **CPython 3.13** (October 2024): experimental JIT, opt-in at build time via `--enable-experimental-jit`. Modest single-digit-percent speedups.
- **CPython 3.14** (October 2025): JIT shipped in Windows and macOS official binaries, **disabled by default**, enabled with `PYTHON_JIT=1`. Still officially experimental; not recommended for production.
- **CPython 3.15** (pre-alpha at May 2026): focus on stack unwinding inside the JIT and thread safety (the free-threading build is moving toward becoming the default, per PEP 779).
- **Microsoft 2025 layoffs**: Microsoft dropped funding for the Faster CPython team days before PyCon US 2025 (https://lwn.net/Articles/1029307/). Bucher and a few others continue the work but momentum took a real hit.
- **WaJIT-style prototypes**: research community continues to explore the approach. Deegen (Haoran Xu's follow-on, OOPSLA 2026) is a "JIT-capable VM generator for dynamic languages."
- Lineage to JSC Baseline and V8 Sparkplug: those are template JITs but hand-coded rather than build-time-extracted; copy-and-patch is the principled generalization.

License: the technique itself is unencumbered. CPython's implementation is PSF-licensed; the paper's MetaVar code is MIT in the Stanford repos.

## §5 Engineering cost for Mochi
- **Binary footprint**: stencils are tiny (~10s of KB to a few MB). Runtime needs no LLVM, no QBE, no assembler.
- **Build complexity**: Mochi build must run Clang once per supported (arch, OS) tuple to generate stencils. We need a small Python or Go script to harvest object files and emit a stencil table (a `.go` file with `[]byte` literals and reloc metadata).
- **License**: technique is free; the Clang dependency at build time is Apache 2.0.
- **Cross-compilation**: We pre-bake one stencil table per (arch, OS) target and ship them all. Cross-compilation at runtime requires the relevant stencil table; the technique itself is target-agnostic.
- **Debugging**: weak. Each stencil's `.debug_line` ranges are tiny and need stitching; CPython has not solved this yet for its JIT.
- **Runtime startup**: zero. First-function compile time is microseconds.

## §6 Mochi adaptation note
This is a **shockingly good fit for vm3**. Mochi already has a typed-op dispatch table in `/Users/apple/github/mochilang/mochi/runtime/vm3/op.go` and a typed Cell handle layout in `/Users/apple/github/mochilang/mochi/runtime/vm3/cell.go`. Each vm3 op is already a small C-equivalent function. The copy-and-patch ramp:
1. Write each vm3 op as a `__attribute__((preserve_none))`-ish C function (one per op) into a new `runtime/vm3/stencils/` tree.
2. At Mochi build time, compile each op with Clang for every (arch, OS) target, extract `.text` + relocations, embed as Go byte literals in generated source.
3. Replace `/Users/apple/github/mochilang/mochi/runtime/jit/vm2jit/lower_amd64.go` and `lower_arm64.go` (currently hand-written assembly with golang-asm) with a stencil stitcher.
4. The page allocator under `runtime/jit/vm2jit/page_*.go` is already in place.

The existing tieredjit (`runtime/jit/tieredjit`) and tracejit (`runtime/jit/tracejit`) infrastructure can target stencil emission as their lower step. This is a strictly higher-quality codegen than golang-asm and **does not require cgo at runtime**: Clang only runs during Mochi's release build.

## §7 Open questions for MEP-42
- **Cross-op optimization gap**: Copy-and-patch cannot const-fold across stencil boundaries. For Mochi's likely workloads (mixed dynamic-ish typed code) this matches Mochi's vm3 design well: each op is already a typed atomic.
- **Stencil count blowup**: 100k stencils (per the paper's high-level case) are too many to manage by hand. For a vm3-style fixed op set with ~200 ops we are well below that.
- **Clang as build dependency**: Mochi releases would need Clang on the release build host. Acceptable for an official release pipeline; awkward for `go get`-style installs.
- **Wasm target**: Wasm is not a copy-and-patch target. (Wasm itself does the patching at the engine level.) Pair with `wasmtime compile`.
- **Hot vs cold code**: Copy-and-patch is a baseline-tier JIT. For Phase 2 a higher-tier optimizer (LLVM, Cranelift) on top is the natural progression, exactly mirroring CPython's roadmap.
- **2025 funding shock**: CPython's JIT lost its corporate sponsor; Mochi adopting the technique should plan to maintain its own stencil tooling rather than depending on PythonLabs.