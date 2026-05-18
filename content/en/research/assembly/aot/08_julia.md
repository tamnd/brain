---
title: "Julia"
description: "JIT-first scientific language adding a real AOT path via juliac and a trimming-based static binary mechanism."
tags: ["native-codegen", "aot"]
weight: 80
date: 2026-05-18T18:08:55+07:00
---

## §1 Provenance

- Project home: https://julialang.org/
- Source: https://github.com/JuliaLang/julia
- AOT devdocs: https://docs.julialang.org/en/v1/devdocs/aot/
- PackageCompiler.jl: https://github.com/JuliaLang/PackageCompiler.jl, docs at https://julialang.github.io/PackageCompiler.jl/dev/
- JuliaC.jl driver: https://github.com/JuliaLang/JuliaC.jl
- LWN coverage of the 1.12 binary-size work: https://lwn.net/Articles/1006117/
- JuliaCon 2024 talk "New ways to compile Julia" by Jeff Bezanson and Gabriel Baraldi (slides linked from https://juliahub.com/blog/new-ways-to-compile-julia-blog).
- Foundational paper: Bezanson, Edelman, Karpinski, Shah, "Julia: A Fresh Approach to Numerical Computing" (SIAM Review, 2017).

## §2 Architecture

Julia's traditional pipeline is JIT-first:

1. Parse Julia source → lowered IR.
2. On first call with concrete argument types, run type inference, lower to Julia SSA IR, then to LLVM IR.
3. LLVM optimises and emits machine code into the process. Cache the compiled method instance keyed by argument types.

The AOT pipeline reuses the same machinery but applies it ahead of time:

1. The user calls `Base.Experimental.@compile_workload begin ... end` or supplies a precompile script. The compiler traces method dispatches and records every concrete method/type pair invoked.
2. `jl_create_native` runs codegen on each recorded method, producing LLVM modules.
3. `jl_create_system_image` serialises the type universe, method tables, and native code into a "system image" (.so/.dylib/.dll). This is the PackageCompiler/sysimg flow.
4. The new `juliac` driver layers on top: it accepts a `@main(args::Vector{String})` entry point and produces a self-contained native executable plus library bundle, with a `--trim=safe|unsafe` flag that aggressively prunes everything the entry point cannot reach. Without trim, sysimages embed ~150 MB of Julia runtime + LLVM + stdlib; with trim, hello-world drops to a few MB.

The AOT model is whole-program closed-world after trimming, but base Julia is open-world (multiple dispatch can be extended at runtime). Trim mode therefore forbids `eval`, dynamic method definition, and any unannotated reflection.

## §3 Targets and platforms (May 2026)

Tier-1: linux-x86_64-gnu, linux-x86_64-musl, linux-aarch64, macos-x86_64, macos-arm64, windows-x86_64, freebsd-x86_64. Cross-compile via the standard LLVM cross paths; PackageCompiler historically requires that the build host match the target OS/ISA because the trace is dynamic. JuliaC's bundling step copies required artefacts (libjulia, libLLVM, libopenlibm, etc.) into `build/bin` and `build/lib`, linking with relative rpath (`@loader_path/../lib`, `$ORIGIN/../lib`).

Static linking is partial: the Julia runtime is shipped as `libjulia-internal.so`. Trim mode reduces but does not eliminate the shared library footprint.

## §4 Runtime

Embedded in every Julia binary:

- A non-moving mark-and-sweep generational GC (since Julia 1.10 added the multi-generational design; ongoing work on a parallel/concurrent collector).
- libuv-based I/O and task scheduler (Julia tasks are M:N green threads).
- libLLVM (still embedded for runtime codegen, unless juliac trimming explicitly disables it).
- The MethodTable and type system, used at runtime even for AOT'd code unless trim mode removes them.

FFI: `ccall((:fname, "libfoo"), Cint, (Cstring,), arg)` is the workhorse; first-class, no marshalling, zero overhead.

Hello-world binary sizes have been the dominant Julia complaint and the dominant 2024–2025 engineering target. Pre-trim PackageCompiler: roughly 150 MB. JuliaC 1.12 with `--trim=safe`: roughly 5–20 MB depending on stdlib use. Still larger than Native Image or .NET NativeAOT because libLLVM and the Julia type system are heavy.

## §5 Status (May 2026)

Julia 1.12 (mid-2025) shipped juliac as the first officially supported small-binary path. Julia 1.13 is in development; the LWN piece notes that 1.12 "will finally include the ability to generate static binaries of a reasonable size, appropriate for distribution." JuliaC.jl is the CLI front-end and is actively maintained (https://github.com/JuliaLang/JuliaC.jl).

Production users of the AOT path remain small (the JIT mode dominates Julia deployments). The audience for juliac is people shipping CLI tools and embedding Julia into other systems. Known issue: PackageCompiler 2.x has not yet caught up with Julia 1.12's strip-metadata semantics (https://discourse.julialang.org/t/aot-compilation-error-on-julia-1-12-due-to-strip-metadata-or-filter-stdlibs/133218), which is the kind of friction expected during the AOT transition.

Performance: AOT'd Julia matches JIT'd Julia per-method (same LLVM backend, same code). What you give up is on-the-fly specialisation for new type combinations: anything not traced at build time falls back to the interpreter (slow) or fails (in strict trim mode).

Known limitations: trim mode is still labelled experimental in 1.12; not all stdlib code is trim-clean; `--trim=unsafe` produces smaller binaries but can break libraries that depend on runtime reflection; libLLVM remains the largest single contributor to binary size.

## §6 Mochi adaptation note

Julia is the cautionary tale that motivates MEP-42's design. Julia spent years on its AOT story precisely because it started open-world; Mochi is already closed-world by construction and avoids most of Julia's pain.

Useful patterns even so:

- The `@main(args::Vector{String})` entry-point convention is a clean rendezvous point for the AOT driver. Mochi can adopt an explicit annotation or rule that the compiled artefact's entry is a function with a specific signature.
- The "trace then compile" idea (build-time workloads that exercise method dispatch) is an interesting middle-ground if Mochi ever adds open-world dynamic dispatch. For now Mochi does not need it.
- Bundling layout (`bin/`, `lib/`, relative rpaths) is the right answer for any AOT binary that ships with sibling shared libraries. Mochi should adopt the same convention when its `runtime/vm3` libraries need to ship alongside the executable.
- The trim-safe vs trim-unsafe split is a useful UX. Mochi can offer `--trim=safe` (no semantic change, may produce trim warnings) and `--trim=aggressive` (deletes anything unreachable, may break reflection).
- The lesson: do not bundle a JIT-time optimiser (libLLVM) into the runtime if you can avoid it. Mochi's `runtime/vm3` should not embed LLVM; codegen happens at build time and stays out of the shipped binary.

Affected Mochi files: `compiler3/trim.go` (new, mirrors ILC trim), `runtime/vm3/image.go` (for system-image-style snapshots), bundling layout for `mochi build --bundle`.

## §7 Open questions for MEP-42

1. Closed-world only, or do we allow a "JIT escape hatch" the way Julia does?
2. Trim levels: `safe`, `aggressive`, `none`?
3. Bundle layout: single executable, or `bin/` + `lib/` like JuliaC?
4. Do we expose a "precompile workload" mechanism, even though Mochi doesn't strictly need one?
5. Julia's hard-won lesson: do not embed the optimiser in the runtime. Mochi should commit to this from MEP-42.