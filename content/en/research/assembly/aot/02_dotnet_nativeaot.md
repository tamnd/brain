---
title: ".NET NativeAOT"
description: "Microsoft's production successor to CoreRT: trimmed CoreCLR plus RyuJIT-as-AOT, shipping single-file native binaries."
tags: ["native-codegen", "aot"]
weight: 20
date: 2026-05-18T18:05:41+07:00
---

## §1 Provenance

- Official overview: https://learn.microsoft.com/dotnet/core/deploying/native-aot/
- ASP.NET Core integration: https://learn.microsoft.com/aspnet/core/fundamentals/native-aot
- Source: the runtime/ILC compiler lives in https://github.com/dotnet/runtime under `src/coreclr/tools/aot/`.
- Lineage: CoreRT (research project, 2014–2020, archived at https://github.com/dotnet/corert) was renamed and rebooted as NativeAOT, shipped GA in .NET 7 (Nov 2022), expanded in .NET 8 (Nov 2023), .NET 9 (Nov 2024), and .NET 10 (Nov 2025).
- Authors: the .NET runtime team at Microsoft (Jan Kotas, Michal Strehovský, et al.). Key design talks: dotnetConf 2022 and 2024 "Native AOT" sessions on Microsoft Learn.

## §2 Architecture

NativeAOT is a whole-program AOT pipeline that reuses much of the regular .NET compiler stack:

1. Source → IL: the C# (or F#, VB) compiler produces ECMA-335 IL exactly as in JIT mode.
2. ILC (the AOT driver) loads the assembly graph, runs IL trimming to remove unreachable code, and resolves all generic instantiations. Unlike JIT mode, every reified generic must be visible at link time; reflection-only paths must be annotated with `[DynamicallyAccessedMembers]` or replaced by source generators.
3. ILC invokes the same RyuJIT codegen used at runtime in JIT mode, but in AOT mode and with the closed type universe. The codegen produces native object code for the target.
4. The object code is linked with a trimmed CoreCLR runtime (GC, type loader stub, exception unwinder, thread pool) into a single static executable on Linux/macOS, or a single PE on Windows.

The IR pipeline is the same RyuJIT internal IR used by JIT, which means AOT and JIT performance characteristics are nearly identical at the instruction level. The whole-program work happens before codegen, in ILC, and is closed-world by construction.

## §3 Targets and platforms (May 2026)

Tier-1 targets in .NET 10: linux-x64, linux-arm64, linux-musl-x64, linux-musl-arm64, win-x64, win-arm64, osx-x64, osx-arm64. iOS, tvOS, and Mac Catalyst use NativeAOT as the default registrar mechanism since .NET 9 (managed-static registrar). Android support for NativeAOT is shipping as preview in .NET 10. WebAssembly has a separate AOT path (Wasm AOT, distinct from NativeAOT).

Cross-compilation is supported with `dotnet publish -r <rid>`; the ILC for the target RID is fetched as a NuGet package, and the system linker (lld, link.exe, ld64) for the target must be on PATH. There is no Zig-style polyglot driver, but the RID matrix is comprehensive.

Static linking: NativeAOT produces a single executable; static linking against musl libc is the standard story on linux-musl-* RIDs. Dynamic linking against glibc is default on the non-musl Linux RIDs.

## §4 Runtime

A NativeAOT binary embeds:

- The CoreCLR garbage collector (server or workstation), the same generational concurrent GC used in JIT mode. There is no option to omit it; managed memory is mandatory.
- The CoreCLR threadpool, EventPipe/diagnostics, exception unwinder, and a slimmed type loader (no runtime IL parsing).
- A trimmed BCL (System.Private.CoreLib and friends), aggressively pruned by ILink/ILC.
- P/Invoke for FFI; LibraryImportAttribute (source-generated marshalling) is the recommended path. COM and CCW interop on Windows works for built-in scenarios.

Hello-world sizes on May 2026 .NET 10 are roughly 1.3 MB stripped on Linux-x64 (with `PublishTrimmed=true, StripSymbols=true, IlcOptimizationPreference=Size`), up to 9 MB for the default unstripped Windows UWP-style executable noted in Microsoft's blog post. ASP.NET Core minimal-API binaries land near 8–10 MB. Compared to framework-dependent .NET, this is much smaller; compared to Go, comparable; compared to Rust, slightly larger because the GC is bundled.

## §5 Status (May 2026)

.NET 10 (Nov 2025) made NativeAOT the recommended deployment model for new ASP.NET Core minimal APIs, gRPC services, and CLI tools (see Andrew Lock's series on .NET 10 NativeAOT tool packaging at https://andrewlock.net/exploring-dotnet-10-preview-features-7-packaging-self-contained-and-native-aot-dotnet-tools-for-nuget/). Production users include Azure Functions (Isolated Worker AOT), Bing, parts of Microsoft Defender, and many third-party CLI tools (NuGet, gh-style).

Performance: peak throughput is within ~5 percent of JIT for steady-state workloads (no on-stack replacement, no tiered profile re-jit), startup is 5–20x faster than JIT, RSS is roughly halved.

Known limitations: System.Linq.Expressions runs interpreted (slower), heavy reflection libraries (older Newtonsoft.Json paths, classic WCF) need replacement or source-generated alternatives, EF Core's runtime model builder needs the AOT-friendly pipeline, and any plugin model that loads assemblies at runtime is unsupported. The .NET 10 `MobileAggressiveAttributeTrimming` regression (dotnet/macios#22065) is an example of the ongoing trim-warning friction.

## §6 Mochi adaptation note

NativeAOT is the most directly relevant case study for Mochi because Mochi is also a typed managed language hosted on a richer runtime. Concrete things to copy:

- The "trim then codegen" split. Mochi can keep `compiler3` as the IL producer, then add an ILC-style trimmer that walks `runtime/vm3` reachability with the program's `main` as the root, dropping unreachable functions and stdlib symbols before native emit.
- The annotation-driven escape hatch (`[DynamicallyAccessedMembers]`). MEP-42 will need a way for Mochi users to say "this name is referenced via reflection" without disabling trimming everywhere; an attribute or a JSON descriptor mirrors the .NET pattern.
- Source generators replacing runtime reflection. Mochi's macro/codegen story (`runtime/vm3` builtins for `json`, `yaml`, `sql`) could be moved to compile-time generation, the way System.Text.Json moved from reflection to source-generated `JsonSerializerContext`.
- Single-file deployment with a baked-in GC. Mochi's MEP-40 already has an arena allocator in `runtime/vm3`; NativeAOT shows that bundling a generational GC plus the language runtime into one ELF is viable.

Affected Mochi areas: `compiler3/trim.go` (new), `runtime/vm3/image.go` (new), and the existing FFI shims to Go's stdlib must be re-cast so they survive trimming.

## §7 Open questions for MEP-42

1. Does Mochi force trimming for native builds (NativeAOT model) or make it opt-in?
2. Source-generated alternatives for `json`/`yaml`/`sql`/`http`: who owns them and when are they invoked?
3. Do we need an analyser pass that reports "this call uses runtime reflection and will break under AOT", à la `IL2026` warnings?
4. How do we expose Mochi's FFI to Go's stdlib if Go itself is not embedded? The answer determines whether NativeAOT (single managed runtime) or Mono AOT (mixed embedding) is the better template.