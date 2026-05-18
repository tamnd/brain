---
title: "Static Python, Cinder, and CPython's Copy-and-Patch JIT"
description: "Meta's typed Python subset that can be AOT-aware, the Cinder JIT, and CPython 3.13+'s experimental copy-and-patch JIT."
tags: ["native-codegen", "aot"]
weight: 120
date: 2026-05-18T18:12:07+07:00
---

## §1 Provenance

- Cinder: https://github.com/facebookincubator/cinder (Meta's CPython fork)
- CinderX (the extension form): https://github.com/facebookincubator/cinderx
- Static Python documentation in-repo: https://github.com/facebookincubator/cinder/blob/cinder/3.8/CinderDoc/static_python.rst
- Meta's "Python 3.12 features" engineering blog (the hooks landing): https://engineering.fb.com/2023/10/05/developer-tools/python-312-meta-new-features/
- CPython JIT PEP 744: https://peps.python.org/pep-0744/
- Copy-and-patch paper: Xu and Kjolstad, "Copy-and-Patch Compilation" (OOPSLA 2021, https://fredrikbk.com/publications/copy-and-patch.pdf)
- Authors: Cinder/Static Python by Meta's Instagram and Python infra teams (Carl Meyer, Itamar Ostricher, Dino Viehland, etc.); CPython 3.13 JIT by Brandt Bucher and Ken Jin building on Xu/Kjolstad's research.

## §2 Architecture

Three related but distinct systems sit under the umbrella "Meta-and-friends are making Python AOT-able":

**Cinder** is Meta's CPython fork. It contains:

- A method-at-a-time JIT compiling Python bytecode to native x86_64.
- Static Python: a stricter typed subset that bypasses Python's dynamic-dispatch overhead.
- An immortal-objects mechanism (PEP 683, upstreamed to 3.12) that decouples reference counting from objects that live forever.
- A parallel garbage collector and lighter-weight frame implementation (not upstream-compatible).

**Static Python** is the most Mochi-relevant piece. It is an experimental alternative bytecode compiler with the following pipeline:

1. Source contains PEP 484/526 type annotations.
2. The Static Python compiler reads those annotations and, where they are "trusted" (annotations on Static Python modules, or on stdlib types it knows the layout of), it emits specialised bytecode that bypasses the regular `LOAD_ATTR` machinery.
3. For attribute access, it computes the slot offset at compile time (Static Python auto-slotifies classes) and emits a single indexed load instead of a dict lookup. For method calls, it uses C-level dispatch. For arithmetic on known primitive types, it emits typed bytecodes that map 1:1 to machine ops in the JIT.
4. The Cinder JIT consumes this bytecode and generates near-native-speed code for the typed paths, falling back to regular Python semantics for untyped escapes.

Static Python is not a separate language; it is a subset of regular Python that the compiler can prove things about. Untyped Python in the same process still works and can call into Static Python freely.

**CinderX** is the same machinery repackaged as a CPython extension module. CinderX 1.x supports CPython 3.10–3.12 with patches to Meta's fork; CinderX shipping for stock CPython 3.14 is the first version that works without any runtime fork.

**CPython's 3.13 experimental JIT** is unrelated to Cinder architecturally but solves an adjacent problem. PEP 744 introduces a JIT using copy-and-patch compilation: a build-time tool (during CPython's own build) compiles a set of micro-ops to per-architecture machine-code templates, and at runtime CPython stitches templates together by patching in concrete operands. There is no traditional optimiser pass; the JIT is essentially a template instantiation engine, which is why it is small and fast to compile. CPython 3.14 (Oct 2025) and 3.15 (in development) continue maturing this JIT alongside the existing specialising adaptive interpreter.

## §3 Targets and platforms (May 2026)

Cinder/CinderX: linux-x86_64 only in production. Meta has not committed to other targets because Instagram runs on Linux/x86_64. The JIT is x86_64-specific.

CPython 3.13+ JIT: Tier-1 (linux-x86_64, linux-aarch64, macos-arm64, windows-x86_64), some Tier-2 platforms, one Tier-3 platform per PEP 744. The copy-and-patch design makes adding architectures easier than a traditional JIT because the per-arch work is "compile this C code with `__attribute__((preserve_none))`", which LLVM does.

Static Python's binary footprint is dominated by CPython itself; Static Python does not produce standalone executables. To get a standalone binary you would combine Static Python with PyInstaller, Nuitka, or a packaging tool. The interesting research thread is whether Static Python's specialised bytecode could feed an AOT compiler that emits native binaries, but no such tool ships in May 2026.

## §4 Runtime

Cinder bundles a modified CPython runtime:

- CPython's reference-counted GC plus Meta's parallel GC (off by default).
- Cinder JIT (method-based, x86_64 only).
- Immortal-object machinery.
- All of CPython's stdlib.

CPython 3.13+ with the JIT bundles a CPython runtime plus a small JIT trampoline; the JIT itself is a few hundred KB of generated machine-code templates compiled into the interpreter.

FFI: CPython's C API for everyone; PyO3 (Rust), pybind11 (C++), ctypes, cffi for higher-level bindings.

Hello-world binary sizes are not meaningful for any of these systems because none of them ship as a standalone executable. CPython itself is roughly 10 MB plus stdlib; a PyInstaller bundle of a trivial app is ~10–30 MB.

## §5 Status (May 2026)

CinderX is "under active development" with weekly PyPI releases. It is used in production at Meta for the Instagram Django service (one of the largest single Django deployments in existence). It is explicitly experimental for external users. The strategic direction is upstream integration where possible (the immortal objects PEP, the watchers, the vectorcall entrypoint hook all landed in 3.12) plus the extension model for the rest.

CPython 3.13's copy-and-patch JIT shipped Oct 2024 marked experimental; 3.14 (Oct 2025) and 3.15 (in development for Oct 2026) keep it experimental but have closed the performance gap with the specialising interpreter while adding speedup on hot numeric loops. PEP 744 explicitly notes the JIT is currently roughly performance-neutral with the existing interpreter but is the foundation for future optimisations.

Performance: Static Python attribute access is reportedly 7x faster than untyped Python in microbenchmarks. End-to-end Instagram production wins are reported in the single-digit percentages, which translates to enormous absolute savings at Meta's scale. CPython 3.13 JIT's wins are modest on average but architecturally significant.

Known limitations: Cinder is x86_64-Linux only; Static Python requires opt-in module-level annotations (`import __static__`) and has its own subtle semantic divergences (immutable modules, auto-slotting). Neither produces a standalone native binary today.

## §6 Mochi adaptation note

Static Python is the closest case study for "typed subset enables native-speed compilation" applied to a dynamic language. Mochi is already statically typed, so most of Static Python's problem is solved by construction. The relevant lessons are subtler:

- The "specialised bytecode for typed paths, fallback for untyped" pattern is what Mochi will need if it ever adds dynamic features (e.g., `any` types, dynamic dispatch). MEP-42 should design the AOT path so that an untyped escape hatch can interop with the typed core.
- Compile-time slot resolution (Static Python's "attribute access is a single indexed load") is what Mochi's `runtime/vm3` accessors already do via the MEP-40 arena. The win is real and should be locked in.
- Auto-slotting and immutable modules are good defaults for any statically-typed language. Mochi already has the equivalent (no monkey-patching of types), so this is a non-issue.
- Copy-and-patch compilation is an interesting middle path between a full LLVM backend and a pure interpreter. The CPython 3.13 JIT shows you can get usable native code out of small, fast-compiling templates with very little engineering. For Mochi, this could be a way to add a JIT to `runtime/vm3` in a future MEP without taking on LLVM as a runtime dependency.
- The Instagram production win pattern (incremental gains compound at scale) reinforces that MEP-42 does not have to deliver Rust-class performance to be valuable; even modest constant-factor wins matter for Mochi's batch and CLI workloads.

Affected Mochi files: long-term `runtime/vm3/jit_cap/` could host a copy-and-patch JIT; near-term, Mochi's existing typed bytecode (MEP-40) is already what Static Python had to engineer.

## §7 Open questions for MEP-42

1. Does Mochi want a fallback execution path for code that escapes the static type system?
2. Is copy-and-patch a serious option for a future Mochi JIT, given it sidesteps LLVM-as-runtime?
3. Should Mochi expose a "static mode" with stricter checks (no `any`, no dynamic import) that enables more aggressive AOT optimisation?
4. The Meta lesson: ship the runtime as an extension, not a fork. Mochi's `runtime/vm3` should stay a library other tools can embed, not become a fork of Go's runtime.