---
title: "GraalVM Native Image"
description: "Closed-world AOT compilation that turns a managed JVM application into a self-contained native executable."
tags: ["native-codegen", "aot"]
weight: 10
date: 2026-05-18T18:05:41+07:00
---

## §1 Provenance

- Project home: https://www.graalvm.org/ (Native Image reference manual at https://www.graalvm.org/latest/reference-manual/native-image/).
- Source repository: https://github.com/oracle/graal (the Native Image / SubstrateVM tree lives at https://github.com/oracle/graal/tree/master/substratevm).
- Foundational paper: Wuerthinger et al., "Initialize Once, Start Fast: Application Initialization at Build Time" (OOPSLA 2019). Earlier "One VM to Rule Them All" (Onward! 2013) describes the Truffle/Graal partial-evaluation pipeline that became the rest of GraalVM.
- Release calendar: https://www.graalvm.org/release-calendar/. Current line in May 2026 is the 25.x branch backed by JDK 25 (GA 16 Sep 2025), with monthly feature releases starting at 25.1. See https://www.graalvm.org/release-notes/JDK_25/ and the InfoWorld coverage at https://www.infoworld.com/article/4061937/graalvm-25-arrives-backed-by-jdk-25.html. Authors: Oracle Labs (Thomas Wuerthinger, Christian Wimmer, Codrut Stancu, Doug Simon, Lukas Stadler, et al.).

## §2 Architecture

Native Image is a closed-world AOT pipeline. The build receives an entry-point class and an explicit classpath/modulepath. It then:

1. Loads classes through SubstrateVM's own class-loading layer and runs a points-to analysis to compute every reachable method, field, type, and resource (the "universe").
2. Initializes a configurable set of classes at build time, snapshotting their heap into the image. Reflection, JNI, resources, and dynamic proxies must be declared via reachability metadata (META-INF/native-image/...) or discovered with the tracing agent. Recent releases ship a new agent that runs inside the native image itself (instead of on HotSpot) so the metadata reflects actual SubstrateVM behaviour.
3. Lowers the reachable methods through the Graal compiler IR (a sea-of-nodes graph). The same Graal backend used for HotSpot JIT runs in AOT mode against this closed graph. GraalVM 25 enables Whole-Program Sparse Conditional Constant Propagation by default for sharper points-to, and ships an XGBoost-based static profile inference model on top of the earlier Graal Neural Network profiler (-O3).
4. Emits native object code for the host triple, links it together with the SubstrateVM runtime (GC, scheduler, monitors, stack walker, JFR, etc.) into a single ELF/Mach-O/PE executable, optionally as a shared library (--shared) usable from C.

The pipeline is whole-program closed-world by design. Open-world dynamics (custom classloaders, arbitrary reflection, agent attach) are deliberately out of scope or limited to declared metadata.

## §3 Targets and platforms (May 2026)

Tier-1 targets: linux-amd64, linux-aarch64, darwin-amd64, darwin-arm64, windows-amd64. Linux musl static builds are supported with --static --libc=musl, producing fully static ELF binaries that have no glibc dependency.

Cross-compilation is officially limited: Native Image is host-target by default and Oracle recommends running the builder on the same OS/ISA as the target. Cross builds are usually done by running the builder inside a matching container (e.g. linux/arm64 Docker on a developer Mac). There is no Zig-style "single-binary cross compiler"; SubstrateVM relies on the host C toolchain to link.

Linking modes: dynamic against system libc by default; --static or --static-nolibc for fully static; --shared to emit a libfoo.so/.dylib/.dll with C-callable entry points (@CEntryPoint).

## §4 Runtime

A Native Image carries a trimmed JDK runtime built into SubstrateVM. The bundled pieces are:

- A garbage collector. Default is "Serial GC" (a generational stop-the-world copying collector); G1 is available in Oracle GraalVM since 23. There is also an Epsilon (no-op) GC for short-lived workloads.
- A thread runtime built on platform threads and an internal scheduler; virtual threads from Project Loom work on SubstrateVM.
- Substrate class metadata, exception tables, JIT-style deoptimization metadata when using --pgo, JFR, and (optionally) the truffle polyglot engine if Truffle languages are linked in.
- FFI through the Foreign Function and Memory API (FFM) and through Native Image's @CFunction/@CEntryPoint, plus legacy JNI.

Hello-world binary sizes in May 2026 are roughly 8–12 MB stripped for a CLI on linux-amd64 with the default GC, and 4–6 MB with --gc=epsilon plus aggressive trimming and UPX. Static musl builds add about 1 MB. Compared to a JVM-on-HotSpot deployment (≥40 MB JDK alone), this is small; compared to a Go or Rust hello-world (1–3 MB) it is still large because SubstrateVM bundles a JDK.

## §5 Status (May 2026)

GraalVM 25 (Sep 2025) is the current LTS-aligned line; releases now cadence monthly. Production users include Spring Boot 3 (first-class Native Image support), Micronaut, Quarkus, Helidon, and Oracle's own cloud services. Adoption is heavily concentrated in JVM microservices that want sub-100 ms cold start and ~50 MB RSS rather than the JVM's 1–2 s cold start.

Peak throughput historically trailed the C2/Graal JIT by 10–25 percent on long-running workloads, because the AOT compiler does not see runtime profiles. Profile-Guided Optimization (--pgo) and the new ML-based static profiler narrow that gap; -O3 with PGO has reached parity on several benchmark microservices.

Known limitations: closed-world is strict; libraries that synthesize bytecode at runtime (Byte Buddy, classic Hibernate) need workarounds; agent runs are mandatory for complex apps; build times for large applications are minutes, not seconds. Oracle has also shifted strategy, winding down GraalVM in the Java SE product but keeping it active as a standalone product and as Community Edition (see https://adtmag.com/articles/2025/09/30/oracle-shifts-graalvm-focus-away-from-java.aspx).

## §6 Mochi adaptation note

Mochi is already a closed-world compiler (the user passes a root file and the compiler walks the module graph). The Native Image pattern is the closest production exemplar of what Mochi-to-native should look like:

- Mochi could keep `compiler3` as the IR producer, but introduce a SubstrateVM-style "image writer" pass after `runtime/vm3` finalisation that snapshots the heap of constant values into a read-only data section of the binary, the way Native Image snapshots build-time-initialised classes. This eliminates startup work.
- The reachability-metadata pattern (declared reflection/resource config in JSON) is a clean way for Mochi to support `runtime/import` or dataset embedding without giving up closed-world analysis.
- The two-mode runtime (Serial GC vs Epsilon) is a useful template: Mochi can ship a default arena-or-tracing GC plus an opt-in `--gc=none` for short-lived CLIs.
- Build-time class initialization maps neatly onto Mochi's compile-time `let` evaluation; the binary carries pre-evaluated constants the same way.

Affected Mochi areas: `runtime/vm3` would need a serializable image format for its arena, and `compiler3` would gain a "native emit" stage feeding either LLVM or the system C compiler.

## §7 Open questions for MEP-42

1. Does Mochi want strict closed-world (banning runtime `eval`/dynamic import in compiled mode) or a tracing-agent escape hatch?
2. Static-libc by default (musl), or rely on the host glibc?
3. Should MEP-42 expose a `--shared` mode emitting a C-callable Mochi library, mirroring Native Image's @CEntryPoint?
4. How aggressive should build-time evaluation be? Native Image's "initialize at build time" caused well-known portability bugs; Mochi must decide where to draw the line.
5. PGO: do we want a `mochi run --collect-profile` mode that feeds `mochi build --pgo`, mirroring Native Image's profile pipeline?