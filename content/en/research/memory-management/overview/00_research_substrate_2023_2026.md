---
title: "MEP-41 Research Substrate: Memory Safety Advances 2023–May 2026"
description: "MEP-41 Research Substrate: Memory Safety Advances 2023–May 2026"
tags: ["memory-safety", "overview"]
weight: 0
date: 2026-05-18T17:00:00+07:00
---

A literature/systems review across 12 threads, with concrete adaptation notes for the vm3 handle/arena/generation model. Each topic includes canonical name + venue/year, core mechanism, production status, and a Mochi adaptation hook.

This file is the broad overview produced by the parallel research sweep. Per-system deep-dive files live alongside it in:

- `hardware/` — CHERI, Morello, CHERIoT, MTE, MIE, PAC/BTI, CET, MarkUs, Scudo, LAM.
- `ownership/` — Rust+Polonius, Vale, Hylo, Mojo, Austral, Pony, Verona, Swift, OxCaml, Linear Haskell, Scala 3, Inko.
- `runtime/` — Perceus, Roc, Lobster, ZGC, MMTk LXR, JSC Riptide, V8 Oilpan, V8 Sandbox, MSWasm, Wasm segmented memory, WasmGC, V8 cage, W^X / JIT hardening, Spectre/JIT, Scudo-in-ART.
- `verification/` — RustBelt/Iris, Verus, Creusot, Kani, Aeneas, CompCert, CakeML, Stacked/Tree Borrows, separation logic for managed heaps, capability-machine logics.
- `industry/` — MSRC 70%, Google/Android Rust, CISA Secure-by-Design (Jan 2026 deadline), NSA, ONCD, DoD, EU CRA, Chrome CVE data, curl, UAF landscape.

---

## §1. Hardware Capability Machines (CHERI / Morello / CHERIoT / Codasip)

**Arm Morello (2022 prototype, still research as of 2025).** Morello is Arm's 7nm Neoverse-N1-derived prototype board implementing CHERI 128-bit capabilities (address + bounds + permissions + 1 tag bit out-of-band). Arm has publicly stated there is no roadmap to include Morello in any commercial Arm product; the boards are distributed via the CHERI Alliance and the UK Digital Security by Design programme. Active research continues: PLDI 2025 published "Morello-Cerise: A Proof of Strong Encapsulation for the Arm Morello Capability Hardware Architecture" (a full-scale sequential model of the Morello ISA showing robust encapsulation even in the presence of arbitrary untrusted code).
URLs: https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/cheri-morello.html , https://pldi25.sigplan.org/details/pldi-2025-papers/80/Morello-Cerise , https://ctsrd-cheri.github.io/morello-early-performance-results/introduction/index.html

**CHERIoT (Microsoft Research, now multi-company).** Embedded RISC-V variant providing object-granularity spatial safety, deterministic use-after-free, and lightweight compartments at <256KiB SRAM. **CHERIoT 1.0 specification was released November 3, 2025**; the SOSP'25 paper "CHERIoT RTOS: An OS for Fine-Grained Memory-Safe Compartments on Low-Cost Embedded Devices" describes a co-designed OS where compartmentalization and memory safety are first-class. Sonata boards ship from Mouser.
URLs: https://cheriot.org/sail/specification/release/2025/11/03/cheriot-1.0.html , https://github.com/microsoft/cheriot-rtos , https://www.microsoft.com/en-us/research/publication/cheriot-rtos-an-os-for-fine-grained-memory-safe-compartments-on-low-cost-embedded-devices/

**Codasip CHERI-RISC-V — first commercial silicon path.** April 2025: Codasip Prime + X730 64-bit RISC-V CHERI application CPU shipped on FPGA. **November 19, 2025: Codasip licensed its 700-family CHERI-enabled CPU to EnSilica for a quantum-resilient COTS microcontroller**, the first announced mass-distribution CHERI-RISC-V part.
URLs: https://codasip.com/press-release/2025/04/29/codasip-prime-launch/ , https://codasip.com/press-release/2025/11/19/codasip-ensilica-for-cheri-enabled-cpu/

**What CHERI enforces that vm3 can mimic:** unforgeable references (no integer→pointer cast), spatial bounds, permissions (read/write/execute/load-capability) carried with the reference, and revocation via tags that survive memory reuse.

**Mochi adaptation:** vm3's 8-byte handle is already a CHERI-style fat pointer in spirit. Allocate spare bits in the handle for *permission flags* (read/write, frozen, sealed-for-FFI), and treat handle integrity as an invariant the bytecode verifier enforces. The verifier should refuse any instruction that synthesizes a Cell from raw bytes. Sealing (CHERIoT-style "sealed capabilities" usable only by a designated compartment) maps directly to FFI: when handing a handle to a Go library, swap its tag for a sealed variant that only the matching unseal opcode can re-open.

---

## §2. Arm Memory Tagging Extension (MTE) and Apple MIE

**Arm MTE basics (Armv8.5).** Each 16-byte memory granule carries a 4-bit hardware tag; pointers carry a 4-bit "key" in their top byte; loads/stores fault on mismatch. SYNC mode is precise; ASYNC and asymmetric modes trade precision for throughput. Tag-collision probability is 1/16 per access.
URL: https://developer.android.com/ndk/guides/arm-mte

**Pixel 8/9 deployment (2023–2025).** Pixel 8 is the first phone with user-toggleable MTE in Developer Options; Android 13+ supports the feature. Real exploits against MTE-enabled kernels have been demonstrated (CVE-2023-6241 on Mali GPUs, CVE-2025-0072 fixed in r54p0 May 2025, both relied on driver-side bypasses outside the MTE perimeter).
URLs: https://source.android.com/docs/security/test/memory-safety/arm-mte , https://github.blog/security/vulnerability-research/bypassing-mte-with-cve-2025-0072/

**Apple Memory Integrity Enforcement (MIE), iPhone 17 / A19, Sept 9 2025.** The single largest deployment milestone. MIE = Enhanced MTE (EMTE, ratified with Arm in 2022) + secure typed allocators (kalloc_type from iOS 15, xzone malloc from iOS 17) + **Tag Confidentiality Enforcement** (an explicit defense against Spectre-style tag leakage). Runs in *synchronous* mode kernel-wide and across 70+ userland processes, always-on, not user-toggleable. Apple credits it with breaking essentially every recent mercenary-spyware exploit chain.
URL: https://security.apple.com/blog/memory-integrity-enforcement/

**Mochi adaptation:** MIE's three pillars correspond beautifully to vm3. The 12-bit generation in vm3's handle is already a software-MTE "key"; the slot's stored generation is the "tag." Tag Confidentiality Enforcement is the lesson worth stealing: never let user code observe a raw generation number (or compute differences between them), because generation churn becomes a side channel that lets an attacker race a stale handle. Treat generation values as **opaque, attacker-unobservable secrets**, only the runtime can compare them. Pair this with a *typed allocator* (one arena per Mochi type, like kalloc_type/xzone) so that even a generation collision can't land on a type-confused slot.

---

## §3. Rust-family Ownership and Borrowing

**Polonius "Alpha" (Rust 2025h2 goal, stabilization targeted 2026).** Switches from NLL's "lifetimes as sets of points" to "origins as sets of loans." Accepts a superset of NLL (closes NLL problem case #3, enables lending iterators) at a budgeted 10–20% compile-time cost. Currently passes nearly all in-tree tests and crater runs; final blocker is one known soundness issue and diagnostics.
URLs: https://rust-lang.github.io/rust-project-goals/2025h2/polonius.html , https://rust-lang.github.io/rust-project-goals/2026/polonius.html , https://github.com/rust-lang/polonius

**Vale (most directly relevant to vm3).** Vale invented **generational references**: every object stores a "current generation" int that is bumped on free; every reference remembers the target generation; dereference inserts a runtime check `ref.gen == obj.gen`. *This is mathematically the same thing vm3 already does.* Vale's roadmap layers two optimizations on top: (a) **Region Borrow Checking**, a Rust-like checker that proves a region of objects can't be freed during a scope, eliding the gen-check; (b) **Hybrid-Generational Memory**, "scope tethering" that pins an object's generation across a known-live scope and uses static analysis to elide the rest. Vale also exposes **Fearless FFI**: because generations aren't refcounts, handing a reference to a C function can't corrupt your memory model.
URLs: https://verdagon.dev/blog/generational-references , https://vale.dev/vision/safety-generational-references , https://vale.dev/roadmap , https://verdagon.dev/blog/zero-cost-memory-safety-regions-part-1-immutable-borrowing

**Hylo (formerly Val).** "Mutable value semantics." The interesting mechanism is **subscripts**, a callable that *projects* (`yield`s) a reference into a containing value rather than returning it. Variants: `let`, `inout`, `sink`, `set`. Calls are bracket-syntax (`a[i]`) and the projection is mutability-tracked through the callsite. Hylo had a major design talk "Designing Hylo" at ECOOP/PLSS 2025.
URLs: https://hylo-lang.org/ , https://docs.hylo-lang.org/language-tour/subscripts , https://2025.ecoop.org/details/plss-2025-papers/12/Designing-Hylo-a-programming-language-for-safe-systems-programming

**Mojo (2024–2026).** Argument conventions are `read` (immutable ref), `mut` (mutable ref), `var` (owned, used with `^` transfer). Lifetimes are tracked as compiler-internal **origins** with `ImmutOrigin`/`MutOrigin`/`MutExternalOrigin` (for FFI memory not managed by Mojo)/`MutAnyOrigin` (escape hatch that disables ASAP destruction). Uses ASAP destruction (after every sub-expression). Path to Mojo 1.0 published Dec 5 2025; targeting late northern summer 2026.
URLs: https://docs.modular.com/mojo/manual/values/ownership/ , https://docs.modular.com/mojo/manual/values/lifetimes/

**Austral.** Pure linear types (not affine, unlike Rust) + capability-based effects. The linear checker is ~600 lines of OCaml. Functions take an explicit capability argument (e.g., `RootCap`) and *cannot* perform an effect (alloc, I/O) without it; capabilities are linear themselves, so the call graph statically tracks who can do what.
URLs: https://austral-lang.org/ , https://borretti.me/article/introducing-austral , https://borretti.me/article/how-australs-linear-type-checker-works

**Mochi adaptation:** Vale is the *most important reference for MEP-41*. vm3 should explicitly position itself as "Vale's generational references, but as a VM rather than a static compiler." Borrow two ideas: (1) **region borrowing**, if a function statically owns the only reference path into an arena slab during its execution, the verifier can elide gen-checks for that scope; (2) **scope tethering**, when a handle is held in a stack-local slot, the runtime can pin its generation for the duration of the frame, turning each subsequent deref into a no-op. The Polonius "origins as sets of loans" framing is a cleaner mental model than NLL for documenting MEP-41's borrow rules.

---

## §4. Capability-Based Reference Systems for Managed Runtimes (Pony, Verona, Inko)

**Pony reference capabilities.** Six caps, each a *pair* of local and global aliasing guarantees: `iso` (unique, sendable), `trn` (write-unique locally, has read-only aliases), `ref` (default mutable, actor-local), `val` (immutable, sendable), `box` (read-only, may have mutable aliases locally), `tag` (identity-only, sendable). `recover` blocks let you upgrade between caps when the source restrictions are met. Only `iso`, `val`, `tag` are sendable across actors, the entire data-race-freedom proof falls out of this matrix.
URLs: https://tutorial.ponylang.io/reference-capabilities/reference-capabilities.html , https://tutorial.ponylang.io/reference-capabilities/capability-matrix.html

**Project Verona (Microsoft Research), extremely active 2024–2025.** Memory is divided into **regions**, each reachable through a single `iso` sentinel. Concurrent access is mediated by **cowns** (concurrent owners) acquired atomically by **behaviours** (the unit of scheduled work), *Behaviour-Oriented Concurrency*. Key 2024–2025 papers: "Reference Capabilities for Flexible Memory Management" (OOPSLA 2024), "When Concurrency Matters: Behaviour-Oriented Concurrency" (OOPSLA 2024), "Dynamic Region Ownership for Concurrency Safety" (PLDI 2025, co-authored with Guido van Rossum / Brandt Bucher / Eric Snow, *strongly suggesting CPython collaboration on free-threading*). The Verona runtime (`verona-rt`) outperforms actor-based models in 17/22 Savina benchmarks.
URLs: https://microsoft.github.io/verona/publications.html , https://github.com/microsoft/verona-rt

**Inko.** Single-ownership + lightweight runtime reference counting, no GC, no compile-time borrow checker. Inspired by the "Ownership You Can Count On" paper. Mixes the ergonomic feel of Swift refcounting with move semantics; if you use a stale reference, you get a deterministic runtime panic, not undefined behavior.
URLs: https://inko-lang.org/ , https://inko-lang.org/papers/ownership.pdf

**Mochi adaptation:** Pony's six-capability matrix is overkill for a single-threaded VM, but the *encoding* (each capability = pair of local/global guarantees) is the right way to document Mochi's reference rules in MEP-41. For Mochi's eventual concurrency story, Verona's region+cown+behaviour model is a better fit than the actor model, it lets you transfer a *region of handles* (an arena slab) atomically without breaking the generation invariant within. Inko's lesson is the most pragmatic: if your runtime can detect stale-reference use and panic deterministically, you do *not* need static linearity to claim memory safety.

---

## §5. Move-Only and Uniqueness in Mainstream Languages

**Swift (`borrowing`/`consuming`/`inout`, `~Copyable`).** SE-0377 added the keywords; SE-0390 made `~Copyable` types real (Swift 5.9, late 2023). WWDC24's SE-0432 added borrowing/consuming pattern matching on noncopyable enums, the missing piece for switch on linear sum types.
URLs: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0377-parameter-ownership-modifiers.md , https://github.com/swiftlang/swift-evolution/blob/main/proposals/0432-noncopyable-switch.md , https://developer.apple.com/videos/play/wwdc2024/10170/

**OCaml 5 + OxCaml modes (Jane Street, going public 2025).** Jane Street's `OxCaml` branch (open-sourced July 2025) ships a *modal type system* with axes: `locality` (local/global, in production at JS for >1 year), `uniqueness` (recently merged into the compiler), `linearity`, `yielding` (controls whether a callee can perform effects up-stack), and a planned `sync` axis. The uniqueness mode + a future "overwrite on unique" optimization will give OCaml in-place updates without an unsafe escape hatch. Jane Street's production servers run OCaml 5 (announced at ICFP/SPLASH 2025).
URLs: https://oxcaml.org/documentation/modes/intro/ , https://blog.janestreet.com/oxidizing-ocaml-parallelism/ , https://blog.janestreet.com/oxidizing-ocaml-ownership/ , https://blog.janestreet.com/oxidizing-ocaml-locality/ , https://anil.recoil.org/notes/icfp25-ocaml5-js-docker

**Scala 3 capture checking ("Caprese", Odersky).** Capture sets are first-class types `T^{cap1, cap2}`. Significantly improved in Scala 3.8 (RC3 used in Scala Days 2025 demos); the Scala 3 compiler itself now passes capture checking (PR #16292). Notable 2026 application: "OPAW: Tracking Capabilities for Safer Agents" uses Scala 3 capture checking as a *type-level sandbox for LLM-generated tool calls*.
URLs: https://github.com/scala/scala3/pull/16292 , https://scaladays.org/editions/2025/talks/the-first-steps-towards-practical , https://scaladays.org/editions/2025/talks/hands-on-capture-checking , https://blog.georgovassilis.com/2026/03/13/opaw-tracking-capabilities-for-safer-agents/

**Linear Haskell (GHC).** Linearity attached to the *arrow* (`%1 ->`) rather than to types. Multiplicity polymorphism lets a single library work for both linear and unrestricted callers. Still marked experimental in GHC 9.x, but Bartosz Milewski (Feb 2024) and POPL 2025's "Affect: An Affine Type and Effect System" show continued momentum.
URLs: https://simon.peytonjones.org/linear-haskell/ , https://bartoszmilewski.com/2024/02/07/linear-lenses-in-haskell/ , https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/linear_types.html

**Mochi adaptation:** OxCaml's *modes-as-orthogonal-axes* is the cleanest way to layer optional restrictions on top of vm3 without forking the type system. Mochi could ship a "default" mode where every handle is freely copyable (the current world), and opt-in modes `unique` (single owner, enables in-place arena update) and `local` (cannot escape the current call frame, enables scope-tethered gen-check elision). Each mode is purely a verifier check; the bytecode is unchanged. Swift's borrowing/consuming/inout vocabulary will be familiar to Mochi users and worth reusing verbatim.

---

## §6. Static Analysis / Region Inference / RC-with-Reuse (Koka, Roc, Lobster)

**Koka + Perceus + FBIP.** Perceus is precise (garbage-free) compile-time-inserted reference counting with **reuse analysis**: pattern-matching deconstruction immediately reuses the freed cell for the next allocation, turning purely functional `map` into in-place mutation when the input is unique. Recent papers: "Frame-limited reuse in Perceus," the "Fully In-Place (FIP) Calculus" (provably no allocation, constant stack), and "Tail Recursion Modulo Context: An equational approach" (Leijen and Lorenzen, JFP October 2025) which extends TRMC to nonlinear control (effect handlers / shift-reset). ICFP'25 distinguished paper: "First-order Laziness" by Lorenzen et al. Koka v3.1.3 released July 2025.
URLs: https://dl.acm.org/doi/10.1145/3453483.3454032 , https://www.microsoft.com/en-us/research/publication/perceus-garbage-free-reference-counting-with-reuse/ , https://koka-lang.github.io/koka/doc/book.html

**Roc.** Compile-time reference counting derived from Perceus, with "Reference Counting with Reuse in Roc" (Folkertsma, Utrecht University thesis) and "Reference Counting with Frame-Limited Reuse." Cycles are *prohibited by language design* (no direct mutation). Roc is rewriting its compiler in Zig as of early 2025; still pre-1.0 (alpha4, Aug 2024).
URLs: https://studenttheses.uu.nl/bitstream/handle/20.500.12932/44634/Reference_Counting_with_Reuse_in_Roc.pdf , https://www.roc-lang.org/functional

**Mochi adaptation:** vm3 is *handle-indexed and mark-sweep*, but the Perceus reuse insight transfers: when the verifier knows a slot is dead after this instruction *and* the next allocation has the same type/size, emit a single SUPER-op `freeAndAlloc` that flips the generation, leaves the slab pointer alone, and returns the same handle index. This is reuse without RC, paid for at JIT time. The "Fully In-Place" calculus from Lorenzen/Leijen is the right academic anchor for proving that Mochi pattern-matches can reuse arena slots safely.

---

## §7. Sandboxed Memory for Runtime Extensions

**MSWasm (POPL 2023; OOPSLA 2024 follow-up).** Extends Wasm with a *segment memory* distinct from linear memory, accessible only via unforgeable **handle** values (base, offset, bound, valid bit, id). Tagged-byte storage in segment memory prevents handle forgery from numeric writes. Compilers: rWasm (AOT), mswasm-graal (JIT on GraalVM), mswasm-llvm (CHERI-LLVM fork). Software overhead 22% (spatial only) to 198% (full); hardware MTE/CHERI brings this near zero. **Iris-MSWasm** (SPLASH/OOPSLA 2024) gave a full Coq mechanization of MSWasm 1.0 and a separation-logic proof of robust capability safety.
URLs: https://cseweb.ucsd.edu/~dstefan/pubs/michael:2023:mswasm.pdf , https://github.com/PLSysSec/ms-wasm , https://dl.acm.org/doi/10.1145/3689722

**V8 Sandbox / Heap Sandbox.** Software-only intra-process isolation: all pointers within the V8 heap are replaced by 32-bit offsets (enabled by pointer compression) or by indices into out-of-sandbox pointer tables. **Trusted Space** (bytecode containers, JIT metadata) lives outside the sandbox behind a second indirection. **Code Pointer Sandbox** replaces direct code pointers with an index into a code-pointer table. Started rolling into Chrome 103 (sandboxed pointers); fully default in 2024. Real-world overhead ~1%; 2025 exploitation now requires a sandbox-escape primitive on top of the original UAF/OOB, the bar is dramatically higher.
URLs: https://v8.dev/blog/sandbox , https://v8.dev/blog/pointer-compression , https://chromium.googlesource.com/v8/v8.git/+/refs/heads/main/src/sandbox/README.md , https://saelo.github.io/presentations/offensivecon_24_the_v8_heap_sandbox.pdf

**RLBox (Firefox).** Compile C library to Wasm, then wasm2c back to native C, fed through Clang. Memory isolation enforced by the Wasm sandbox; cross-boundary calls go through `invoke_sandbox_function()`; all return values and callback parameters are **tainted** (a compile-time tag the consuming code must explicitly sanitize). Ships in Firefox 95+ isolating Graphite, Hunspell, Ogg, Expat, Woff2. Still in active use in 2025; Mozilla pays bug bounties for sandbox bypasses even without a vulnerability in the isolated library.
URLs: https://rlbox.dev/ , https://hacks.mozilla.org/2021/12/webassembly-and-back-again-fine-grained-sandboxing-in-firefox-95/ , https://www.usenix.org/system/files/sec20-narayan.pdf

**Mochi adaptation:** MSWasm is the closest existing standard to what vm3 already is, a handle-indexed segment memory with tagged forgery prevention. The MEP-41 spec should explicitly cite MSWasm and adopt its handle field layout (`base, offset, bound, valid, id`) as the *normative description* of a Mochi cell, with Iris-MSWasm as the formal model to point at. From V8's sandbox, steal the **trusted-space** idea: vm3 metadata (function tables, type descriptors, JIT'd code) should live in a *separate* arena that user code's handles physically cannot index into, even with a forged generation. RLBox's *taint type* is the right pattern for Go FFI returns: any Go-returned value that re-enters Mochi must carry a static "untrusted" mark that forces sanitization before it can be stored in a typed slot.

---

## §8. GC and Lifetime Advances for VMs

**ZGC (Generational, default in Java 25).** Sub-millisecond stop-the-world pause times via colored pointers + load/store barriers, now generational since JEP 439 (JDK 21). Java 25 ships Generational ZGC as the *only* ZGC flavor. Netflix runs >50% of critical streaming services on JDK 21 + Generational ZGC; pause times 20–30µs better than non-generational at P99; 4× throughput on Cassandra at 25% the heap. Trade-off: no compressed oops (15–30% memory overhead vs G1) and 5–10% extra CPU.
URLs: https://openjdk.org/jeps/439 , https://wiki.openjdk.org/spaces/zgc/pages/34668579/Main , https://netflixtechblog.com/bending-pause-times-to-your-will-with-generational-zgc-256629c9386b , https://andrewbaker.ninja/2025/12/03/deep-dive-pauseless-garbage-collection-in-java-25/

**MMTk + LXR.** MMTk is a host-language-agnostic Rust GC toolkit; LXR is its hybrid RC+SATB-tracing collector with **temporal coarsening** (amortizes RC over many writes), **2-bit RC slots** (stuck objects fall back to SATB), and synchronous-increment + async-decrement pauses. Stop-the-world LXR beats industrial concurrent GCs on tail latency (PLDI'22 result, increasingly cited). 2024–2025 adoption: **Ruby 3.4 ships MMTk integration** (currently only MarkSweep; Immix and LXR planned); **Julia** integrating MMTk (JuliaCon 2025).
URLs: https://danglingpointers.substack.com/p/low-latency-high-throughput-garbage , https://www.mmtk.io/status , https://railsatscale.com/2025-01-08-new-for-ruby-3-4-modular-garbage-collectors-and-mmtk/ , https://railsatscale.com/2025-09-16-reworking-memory-management-in-cruby/paper.pdf

**JavaScriptCore Riptide.** Retreating-wavefront concurrent collector with space-time scheduler that throttles the mutator if allocation outpaces collection. Mostly-concurrent, generational via sticky mark bits, non-compacting, segregated storage. Foundational design from 2017 remains the architecture in 2025.
URLs: https://webkit.org/blog/7122/introducing-riptide-webkits-retreating-wavefront-concurrent-garbage-collector/ , https://webkit.org/blog/12967/understanding-gc-in-jsc-from-scratch/

**Static Hermes / Hermes V1 (React Native 0.82, 2025).** Two LLVM backends: bytecode and native. Optional sound type annotations compile to direct field access on typed classes (shape-aware). React Native 0.82 makes Hermes V1 experimentally available; "static" optimizations (typed compilation, JIT) still ramping. AArch64 JIT shipped 2024 (template-interpreter style).
URLs: https://github.com/facebook/hermes , https://speakerdeck.com/tmikov2023/optimizing-with-static-hermes-chain-react-2024 , https://blog.swmansion.com/welcoming-the-next-generation-of-hermes-67ab5679e184

**WasmGC.** **Baseline in all browsers as of late 2024** (Chrome 119, Firefox 120, Safari 18.2). Part of Wasm 3.0 (September 2025). Real production: Google Sheets calculation worker runs 2× faster than JS via WasmGC. Kotlin/Wasm and Dart/Flutter are early adopters. .NET passed because the GC integration is too tight to their runtime. Toolchain limitation: LLVM does not target WasmGC.
URLs: https://developer.chrome.com/blog/wasmgc , https://web.dev/blog/wasmgc-wasm-tail-call-optimizations-baseline , https://v8.dev/blog/wasm-gc-porting

**Java Valhalla / JEP 401 (Value Classes and Objects).** Early-access build of JEP 401 released October 2025; `value class` removes identity. Two optimizations: **heap flattening** (value objects inlined into containing objects and arrays, always read/written atomically) and **scalarization** (no allocation in JIT'd code). Some JDK classes (`Integer`, `LocalDate`) become value classes under preview. Null-restricted types are a separate JEP. Still preview.
URLs: https://openjdk.org/projects/valhalla/value-objects , https://inside.java/2025/10/27/try-jep-401-value-classes/ , https://inside.java/2025/10/31/jvmls-jep-401/

**Wasm shared-everything threads (proposal).** Adds release-acquire memory order (vs the current SC-only), shared tables, and **shared GC structs** so WasmGC + threads can coexist. `ThreadBoundData` JS API bridges shared GC objects to unshared DOM nodes safely.
URL: https://github.com/WebAssembly/shared-everything-threads/blob/main/proposals/shared-everything-threads/Overview.md

**Mochi adaptation:** Since vm3 piggybacks on Go's GC for backing storage, you do *not* need to reinvent any of this. But two ideas matter: (1) **Generational ZGC's colored-pointer scheme** is a strong reference for documenting how vm3's metadata bits (generation, type tag, mutability) fit alongside the slab index in a single 8-byte handle, call out the precedent explicitly. (2) **MMTk's modular GC interface** is the gold-standard architecture: even though Mochi will start with a single mark-sweep, MEP-41 should describe the slot lifetime API as a *trait* the VM can implement multiple ways (immediate-free, quarantine, mark-sweep, future LXR-style hybrid RC) so the design is not over-fitted to today's collector. (3) Valhalla's **flattened value classes** are exactly the pattern Mochi needs for small-record types, inline them into the containing arena slot instead of allocating a separate cell.

---

## §9. Formal Verification of Memory Safety

**RustBelt (POPL 2018, foundational).** Iris-based Coq proof of semantic soundness for λRust + a corpus of unsafe Rust libraries. Foundation for everything below.
URL: https://plv.mpi-sws.org/rustbelt/

**RefinedRust (PLDI 2024).** Foundational semi-automated functional-correctness verification of *both safe and unsafe* Rust, with a refinement type system proven sound (in Rocq) against a RustBelt-based model. Uses RustHorn-style prophecy variables ("borrow names") to reason about `&mut T`.
URL: https://iris-project.org/pdfs/2024-pldi-refinedrust.pdf

**Aeneas.** Translates safe Rust MIR to pure λ-calculus via the LLBC intermediate language; backends for F*, Coq, HOL4, **Lean**. ICFP 2024 added a soundness proof for the symbolic borrow-checker (`Sound Borrow-Checking for Rust via Symbolic Semantics`). **Industrially used in Microsoft's port of SymCrypt from C to verified Rust.**
URLs: https://aeneasverif.github.io/ , https://github.com/AeneasVerif/aeneas , https://lean-lang.org/use-cases/aeneas/ , https://arxiv.org/abs/2206.07185

**Verus.** Rust-syntax superset with `forall/exists/requires/ensures`, discharged via Z3. Verifies unsafe code, monomorphic only.
URL: https://verus-lang.github.io/verus/guide/

**Creusot.** Deductive verification for safe Rust via the Pearlite specification language.

**Kani.** Bounded model checking; verifies a subset of Rust UB and user assertions. Used on Firecracker, s2n-quic, Hifitime.

**AWS Standard Library Verification Effort.** Cross-tool effort to verify the Rust stdlib using Verus + Creusot + Kani; bedrock community goal.
URL: https://rust-lang.github.io/rust-project-goals/2024h2/std-verification.html

**Iris-Wasm / Iris-MSWasm.** Separation logic for full Wasm 1.0 and MSWasm; gives robust capability safety proofs (OOPSLA 2024).

**hax.** Cross-prover (F*, Coq, EasyCrypt, Lean) verification of security-critical Rust (2025 paper).
URL: https://eprint.iacr.org/2025/142.pdf

**Mochi adaptation:** vm3 is small enough that an Iris-style separation-logic model is realistic for MEP-41 *future work*. The most cite-able analog is **Iris-MSWasm**, since MSWasm's handle semantics is morally identical to vm3's. Stake out the formal-correctness story: define a small λ-calculus model of vm3 (call it λvm3), describe handle/arena/generation operationally, and explicitly note in MEP-41 §7 ("future work") that this can be lifted to Iris in the style of Iris-MSWasm. For an industrial story, point at Aeneas + SymCrypt, that's the existing proof that "Rust verification used in production for memory-safety-critical code" is real, not aspirational.

---

## §10. Spectre / Transient-Execution Mitigations for VMs

**V8's published retreat from pure-software mitigation.** The V8 team concluded that *software-only* Spectre mitigations have unbounded complexity and ongoing maintenance cost (e.g., later compiler optimizations have silently undone earlier mitigations). Timer-resolution reduction + SharedArrayBuffer disabling were emergency measures; they explicitly state that *some Spectre variants (especially v4) are infeasible to mitigate in software*. The strategy pivoted toward the V8 sandbox (process-internal isolation) so Spectre-leaked secrets can't reach OS resources.
URL: https://v8.dev/blog/spectre

**Switchpoline (ASIA CCS 2024).** ARMv8 JIT mitigation that rewrites indirect branches into direct branches. 1.8% mean SPEC CPU 2017 overhead, 5µs JIT cost per new target.
URL: https://www.misc0110.net/files/switchpoline_asiaccs24.pdf

**SpecASan (ISCA 2025).** Uses ARM MTE to extend tag-checking into the *speculative* execution path, speculative loads that fail MTE check are delayed until commit. Closes a class of Spectre leaks while preserving speculation perf.
URL: https://dl.acm.org/doi/10.1145/3695053.3731119

**"Do You Even Lift?" (POPL 2025).** Compiler-level theorem stating which Spectre-safe properties survive lowering through optimization passes.

**Branch Privilege Injection (USENIX Security 2025).** New Spectre v2 variant; mitigation landscape now requires IBPB + IBRS + retpoline + RSB Stuffing + STIBP per microarchitecture.

**Mochi adaptation:** This is the most important "what you don't have to build" thread. *vm3 is hosted on Go and currently has no JIT.* As long as that holds, Mochi's Spectre exposure is whatever Go's compiler emits, which means MEP-41 can punt to the Go team's mitigation story. When a JIT does land, the V8-team lesson is the only one to internalize: **do not invest in JIT-emitted Spectre defenses; instead make the runtime sandbox stronger so a Spectre leak is bounded to the user-Mochi heap.** This argues for committing to a CHERI/MSWasm-style handle model up front: *if a future Spectre leaks raw bytes from a Mochi arena, those bytes are still nothing without a forgeable handle to interpret them.*

---

## §11. Industry Surveys and Policy

**Microsoft "~70%" reaffirmed.** November 2025 Microsoft SFI Report restates that 70% of CVE-assigned vulnerabilities Microsoft resolves are memory-safety. Surface is shipping Rust-based UEFI firmware and Rust Windows drivers. ICSE 2025 Microsoft Research paper on LLM-assisted memory-safety annotation/Rust porting.
URL: https://blogs.windows.com/windowsexperience/2025/11/10/advancing-security-with-windows-and-surface-microsoft-sfi-report-nov-2025/

**Android: under 20% memory-safety bugs (Nov 2025).** From 76% in 2019 → expected 24% by end-of-2024 → under 20% in 2025 (first time ever). Absolute counts: 223 in 2019 → <50 in 2024. **"1000× reduction in memory-safety vulnerability density"** in Rust code vs C/C++. Rust changes have 4× lower rollback rate and 25% less code-review time. First near-miss Rust memory-safety bug (linear overflow in CrabbyAVIF, CVE-2025-48530) was rendered non-exploitable by Scudo guard pages.
URLs: https://security.googleblog.com/2025/11/rust-in-android-move-fast-fix-things.html , https://thehackernews.com/2025/11/rust-adoption-drives-android-memory.html

**CISA roadmap deadline: January 1, 2026.** Joint guide "The Case for Memory Safe Roadmaps" (CISA + NSA + FBI + Five Eyes); requires software manufacturers to publish a memory-safety roadmap by **Jan 1, 2026**. Exempts products with EOL before Jan 1, 2030. June 2025: CISA + NSA additional joint guide on MSL adoption.
URLs: https://www.cisa.gov/case-memory-safe-roadmaps , https://www.cisa.gov/news-events/alerts/2025/06/24/new-guidance-released-reducing-memory-related-vulnerabilities , https://www.cisa.gov/news-events/news/cisa-nsa-fbi-and-international-cybersecurity-authorities-publish-guide-case-memory-safe-roadmaps

**NSA "Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development" (June 23, 2025, U/OO/172709-25).** Endorses memory-safe-by-construction or hardware capabilities (CHERI); emphasizes language-level protections over developer discipline.
URL: https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF

**EU Cyber Resilience Act (CRA).** Cybersecurity requirements for digital products on the EU market by 2027.

**Mochi adaptation:** The policy environment hands MEP-41 its motivation paragraph for free. Mochi is *already* memory-safe by construction (no `unsafe` in user code) and Go-hosted; MEP-41 should frame itself as "the artifact that lets Mochi credibly claim compliance with the CISA Jan-2026 roadmap and NSA June-2025 guidance without hand-waving." Borrow the *1000× density-reduction framing* from Google Android, that's the rhetorical hook for why "memory safety" is worth a numbered MEP.

---

## §12. Use-After-Free Defenses (most relevant to vm3's generation tags)

**MarkUs (Ainsworth and Jones, 2020) and its 2024 evaluation.** Quarantine + GC-style liveness check: freed memory cannot be reused until no pointers reach it. CAMP (USENIX Security 2024) measured ~10% overhead but found MarkUs missed 6 of 14 real-world UAF CVEs.
URL: https://users.cs.northwestern.edu/~simonec/files/Research/papers/MODERN_USENIXSECURITY_2024.pdf

**MiraclePtr / BackupRefPtr (Chrome).** Reference-counted `raw_ptr<T>` on PartitionAlloc; quarantines + poisons (0xEF…EF) freed memory while any `raw_ptr` still exists. Fully rolled out across all platforms June 2023. As of July 2024, UAFs protected by MiraclePtr are *no longer treated as security vulnerabilities* by Chrome VRP. 5–6.5% memory overhead. May 2024 saw a $100,115 bypass (race on 29-bit refcount overflow); the bypass requires a separate race-condition primitive, so the bar is enormous.
URLs: https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md , https://security.googleblog.com/2022/09/use-after-freedom-miracleptr.html , https://www.securityweek.com/google-improves-chrome-protections-against-use-after-free-bug-exploitation/

**Scudo Hardened Allocator (default on Android since 11, Fuchsia).** Heap chunks have headers protected by checksum; primary/secondary class split; integrates GWP-ASan (probabilistic guard-page sampler, 1/5000 by default, ~70 KiB extra RAM per process). MTE-aware: uses `PROT_MTE` and random-tag per allocation. USENIX WOOT 2024 showed two exploitation techniques against Scudo; one was patched, the other is fundamental to large-chunk handling.
URLs: https://llvm.org/docs/ScudoHardenedAllocator.html , https://source.android.com/docs/security/test/scudo , https://llvm.org/docs/GwpAsan.html , https://www.usenix.org/conference/woot24/presentation/mao

**GWP-ASan in production (Trail of Bits, Dec 16 2025).** Recommended for exploit detection in production, not just bug-finding.
URL: https://blog.trailofbits.com/2025/12/16/use-gwp-asan-to-detect-exploits-in-production-environments/

**Generation-tagging deployed in the wild.** vm3's 12-bit generation tag has direct precedent in: Vale's generational references (covered in §3), MIE's 4-bit hardware tag (§2), and conceptually in MiraclePtr's deferred-reuse quarantine (every "quarantined" slot is functionally a slot with a not-yet-incremented generation).

**Mochi adaptation:** vm3 sits in the sweet spot of this literature. The MEP-41 design should explicitly enumerate:

1. **Generation width budget.** 12 bits = 1/4096 collision probability per stale access. MIE uses 4 bits hardware (1/16); software can afford more. Document the tradeoff and consider 16 bits.
2. **Quarantine on free.** Instead of immediately reissuing a slot after a generation bump, optionally hold it in a per-arena free-list ring buffer of length N. This is MiraclePtr/MarkUs in software, free given that the slab is already managed.
3. **Probabilistic guard pages (GWP-ASan analog).** Allocate every Nth handle into a *guard slab* whose Cell layout is one-per-slot with a poisoned neighbor; any out-of-bounds index immediately faults. Cheap in Go since arenas are software-managed.
4. **Type-segregated arenas (Apple xzone analog).** One arena per Mochi type prevents type-confusion even on a generation collision. This is *already* implied by vm3's "typed Go-allocated arenas", MEP-41 should call this out explicitly as a security property, not just an allocator-efficiency property.
5. **Generation as side-channel-protected secret (Apple TCE analog).** Forbid user code from observing or comparing raw generation numbers; only the runtime's deref opcode does the compare. This is the *single most novel* contribution MEP-41 can stake out, nobody else cleanly applies the Tag Confidentiality Enforcement lesson to a software handle scheme.
6. **The CrabbyAVIF lesson (Nov 2025).** Even in a "memory-safe" language, a linear arithmetic bug in a parser can produce a writable out-of-bounds index; defense in depth (Scudo guard pages, generation bumps, type-segregated arenas) is what kept Android safe. Mochi should not assume static type safety obviates *runtime* defense in depth.

---

## Closing meta-observations for MEP-41

Three threads dominate everything else and should anchor the document:

1. **The generational-reference idea (Vale, MIE, MiraclePtr) is converging across hardware, browsers, and academic languages simultaneously.** vm3 is independently arriving at the same answer. MEP-41 is well-positioned to cite all three as prior art and claim Mochi as the first *VM* (vs hardware, allocator, or compiler) to do this cleanly.

2. **Modes / capabilities as orthogonal axes (OxCaml, Scala Caprese, Pony) is the right design vocabulary for layering optional safety on top of the base VM** without forking the type system.

3. **The CISA Jan 1, 2026 deadline + Apple MIE shipping + Android <20% memory bugs makes Q1–Q2 2026 the right window to publish.** The policy and industry tailwind is unusually strong; MEP-41 should land while the framing is fresh.