---
title: "Nim"
description: "Static, GC-by-default systems language that emits C (or C++, JavaScript, LLVM) and inherits the host toolchain's optimiser."
tags: ["native-codegen", "aot"]
weight: 50
date: 2026-05-18T18:08:55+07:00
---

## §1 Provenance

- Project home: https://nim-lang.org/
- Source: https://github.com/nim-lang/Nim
- Memory management reference: https://nim-lang.org/docs/mm.html
- 2.2.0 release announcement: https://nim-lang.org/blog/2024/10/02/nim-220-2010.html
- Roadmap RFC: https://github.com/nim-lang/RFCs/issues/556
- Nimony (next-gen compiler): https://github.com/nim-lang/nimony
- NIFC dialect specification: https://github.com/nim-lang/nimony/blob/master/doc/nifc-spec.md
- Author: Andreas Rumpf (Araq). Project started 2008; Nim 1.0 in 2019, Nim 2.0 in Aug 2023.

## §2 Architecture

The classical Nim pipeline (still the production pipeline as of 2.2.x in May 2026):

1. Parser → AST.
2. Sem pass performs type inference, generics instantiation, macro expansion (macros are Nim code that runs at compile time), and template expansion.
3. The mid-end runs transformations: closure conversion, iterator inlining, destructor injection (for ARC/ORC), and overall lowering.
4. The backend emits portable C source by default, optionally C++, JavaScript, or Objective-C. The choice is per-compile via `nim c|cpp|js|objc`.
5. Nim invokes the host C compiler (gcc, clang, vcc, tcc) to compile and link.

There is no LLVM frontend shipped by Nim itself; LLVM is accessed only indirectly via clang. The "compile to C, let cc handle the rest" pattern keeps the Nim distribution small (a few MB), defers optimisation entirely to the host toolchain, and gives Nim instant access to every platform the host C compiler supports.

The new Nimony compiler (in heavy development, target autumn 2025/2026 production) splits the pipeline further. It introduces NIF (a Lisp-like text format for compiler IR), NIFC (a C-like dialect of NIF), Nifler (frontend isolation tool), Hexer (a lowerer that resolves closures, iterators, and memory management), and a NIFC-to-C codegen, with a parallel native NIFC backend in development. The goal is incremental compilation, parallel builds, and an order-of-magnitude reduction in compiler bug count.

## §3 Targets and platforms (May 2026)

Any platform with a C compiler. Officially tested: linux-amd64/arm64/armv7/risc-v, windows-amd64, macos-amd64/arm64, freebsd, openbsd, netbsd, haiku, android, iOS via cross-compile, plus AVR and ARM Cortex-M via embedded crosses. The JavaScript backend targets the browser and Node.

Cross-compilation is delegated to the host C compiler: `nim c --cpu=arm64 --os=linux --cc=clang -t:'--target=aarch64-linux-gnu' app.nim`. With `zig cc` plugged in via `--cc:gcc --gcc.exe:'zig cc' --gcc.linkerexe:'zig cc'`, Nim becomes a fully self-contained cross-compiler.

Static vs dynamic: musl static builds are routine; glibc-linked is dynamic by default; Windows MSVC and MinGW are both supported.

## §4 Runtime

Memory management is selectable via `--mm:`:

- `--mm:orc` (default since 2.0): reference counting plus a "trial deletion" cycle collector. Cycles handled, no tracing, deterministic latency.
- `--mm:arc`: reference counting only, no cycle collector. Smaller code, faster, but leaks cycles. Recommended when you control the data shapes.
- `--mm:atomicArc`: thread-safe ARC, the only memory management strategy under active development for Nimony.
- `--mm:none`: manual.
- Legacy GCs (refc, markandsweep, boehm, go) still selectable but deprecated.

The Nim runtime is tiny: a few KB of C code for the GC hooks, exception machinery, and string/seq primitives. FFI is direct C call with the `importc` pragma; calling C is essentially free. C++ classes are reachable via the `importcpp` pragma. JavaScript interop via `importjs`.

Hello-world size on linux-x86_64 with `nim c -d:release --opt:size --passL:-s`: about 50–80 KB statically linked against musl, 25 KB dynamically linked against glibc with no GC and `--mm:none`. With ORC enabled and a few stdlib uses, expect ~150 KB. Comparable to Zig, smaller than Crystal.

## §5 Status (May 2026)

Nim 2.2.0 (Oct 2024) is the stable release; 2.2.x patches continue. Nim 2.4 is in beta. The big strategic move is Nimony, which the maintainers position as Nim 3.0. Production users include Status.im (the Ethereum client), Faststream, NimSkull (a fork), and a substantial embedded systems community.

Performance: typically within 5–15 percent of optimised C because the host compiler does the heavy lifting on Nim's generated C source. ARC/ORC are competitive with Rust's reference-counting patterns for the workloads they suit.

Known limitations: documentation is patchy; the standard library has uneven quality; the C backend produces hard-to-read C source (a maintenance hazard if you have to debug it); some ARC/ORC-specific codegen bugs persisted into 2.2 (open issues #24586, #24578, etc.); compile times for heavy generic/macro code can be slow.

## §6 Mochi adaptation note

Nim is the canonical example of "compile to C, ship small" that Mochi should weigh against the LLVM (Crystal) and self-hosted backend (Zig) routes. Patterns to copy:

- Compile to C as the v1 backend. Mochi can emit portable C from `compiler3` and use the host toolchain. Pros: tiny Mochi distribution, instant platform coverage. Cons: harder debugging, no FFI back into Go without C glue.
- ARC/ORC as a GC option. MEP-42 could ship a deterministic reference-counted allocator alongside the existing arena, mirroring Nim's `--mm:arc` for predictable-latency workloads.
- Per-build memory-management switch: `mochi build --gc=arc|orc|tracing|none`. This decouples the GC decision from the language semantics and is exactly what Nim does.
- NIFC as a model for Mochi's IR-at-rest format. If Mochi wants incremental compilation, an explicit textual IR (Nim's NIF/NIFC) is easier to debug and tool than serialised binary IR.
- Nimony's split of "frontend shielding tool" (Nifler) + "lowerer" (Hexer) + "backend" (NIFC gen) is a cleaner architecture than today's monolithic compilers; if MEP-42 grows MEP-43+ (incremental, IDE tooling), this is the shape to head toward.

Affected Mochi files: `compiler3/backend_c/` (new), `runtime/vm3/arc.go` (new RC allocator), and a textual IR specification document.

## §7 Open questions for MEP-42

1. Is "emit C" an acceptable v1 backend for Mochi, or does the spec demand direct native emission?
2. Which GC modes does Mochi expose? ARC, ORC, tracing, arena, none (pick a subset).
3. Do we adopt a textual IR (NIF-style) now, or defer to a later MEP?
4. How do we integrate with the host C compiler portably? Configure once, ship across platforms?
5. Nim has no managed FFI shim for stdlib; everything goes through importc. Mochi's Go-stdlib FFI may need its own pattern.