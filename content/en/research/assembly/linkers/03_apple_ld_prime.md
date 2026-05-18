---
title: "Apple's New Linker (ld_prime / ld_new)"
description: "The closed-source Mach-O linker that ships in Xcode 15 and later."
tags: ["native-codegen", "linkers"]
weight: 30
date: 2026-05-18T18:04:37+07:00
---

## §1 Provenance

- Apple toolchain (closed source for the new linker). The older `ld64` is at https://github.com/apple-oss-distributions/ld64 but Apple has not released source for `ld_prime` / `ld_new` (confirmed by community probing of opensource.apple.com, see https://developer.apple.com/forums/thread/749558).
- WWDC 2023 session that introduced the new linker: "Meet mergeable libraries" (session 10268, https://developer.apple.com/videos/play/wwdc2023/10268/).
- Community write-ups: Wade Tregaskis's `ld_prime` series at https://wadetregaskis.com/tags/ld_prime/.
- "The new linker in Xcode 15" talk by Yuta Saito (kateinoigakukun): https://speakerdeck.com/kateinoigakukun/the-new-linker-in-xcode-15.

## §2 Mechanism / function

`ld_prime` (Apple's internal name; the Xcode 15 release renamed the flag to `-ld_new`) is a from-scratch Mach-O linker that replaces the long-lived `ld64`. It was rewritten specifically to:

- Parallelize symbol resolution and relocation application. Apple measured roughly 2x to 5x speedups on representative iOS/macOS app links versus `ld64`.
- Natively support "mergeable libraries", a new Mach-O concept that lets multiple static libs be linked together as if they were one dynamic library at runtime, getting the best of both worlds (build-time link culling, runtime sharing).
- Emit Apple's chained-fixups format by default. Chained-fixups (https://github.com/apple-oss-distributions/dyld/blob/main/doc/dyld-fixups.md) replace the older rebase/bind opcodes with a more compact, page-local linked list. This makes both link time and dyld startup time faster, especially on cold caches.
- Better handle large Mach-O binaries with many `__TEXT` segments and many dylibs.

The Apple driver `ld` chooses between the two implementations via `-ld_classic` (force the old ld64) or `-ld_new` (force ld_prime). When neither is specified, `ld` picks `ld_new` for arm64, arm64e, x86_64; older architectures (armv6, armv7, armv7s, i386, armv6m, armv7k, armv7m, armv7em) still fall through to `ld_classic`.

## §3 Platform coverage (May 2026)

Mach-O only. arm64, arm64e, x86_64. Targets macOS, iOS, iPadOS, tvOS, watchOS, visionOS, and the new visionOS simulator.

Closed source. No way to run on a non-Apple host. Apple's official cross-compile story is "use a Mac" or "use Xcode Cloud".

## §4 Current status (May 2026)

`ld_prime` debuted in Xcode 15 (June 2023, GA September 2023). Xcode 16 (2024) deprecated `-ld_classic`. Xcode 16.4 ships `PROGRAM:ld PROJECT:ld-1167.5` (April 2025 build, see https://developer.apple.com/forums/thread/788064). Xcode 17 is the May 2025 release.

The Xcode 26 timeline (Apple jumped Xcode versioning to align with the year in 2025) saw further linker rework. Several legacy flag combinations were removed. Mergeable libraries are now the default for new Swift package products.

The old `ld64` is still in the toolchain but only for the legacy architectures listed in §2. For everything Mochi cares about (Apple Silicon Macs, modern iOS devices), the path is `ld_prime`.

Production use: every Mac and iOS app built with Xcode 15+ uses `ld_prime` by default. This makes it the most-used Mach-O linker on the planet.

## §5 Engineering cost for Mochi

- We do not have a choice on the host: if Mochi is building a native binary on macOS, the system `ld` is `ld_prime` (or wraps it). Apple does not let us swap in `ld64.lld` as the system linker without explicit flags.
- No license cost (it ships with Xcode, which is free).
- Cgo not relevant; we invoke `ld` or `clang -fuse-ld=...` as a subprocess.
- The closed-source nature means we cannot embed it, cannot debug it when it misbehaves, cannot port it. We are at Apple's mercy for bug fixes.
- We cannot cross-link a macOS binary from Linux using `ld_prime`. For cross-host Mac builds, we must use `ld64.lld` (see `01_lld.md`).
- Code signing pairing: `ld_prime` cooperates closely with the Mach-O code-signature placeholder (`__LINKEDIT` slot for the LC_CODE_SIGNATURE blob). When we later run `codesign`, the linker has already left space. `ld64.lld` does this too but lags a release or two on new signing flavors.

## §6 Mochi adaptation note

For the macOS native target, Mochi's `tools/linkers` selection logic should be:

- If running on Darwin (`runtime.GOOS == "darwin"`), invoke the system `clang` with the platform's `ld` and pass our object files. Do not try to force `-ld_new` or `-ld_classic`; let `clang` pick.
- If running on Linux or Windows targeting Darwin, use `ld64.lld` and ship our own Mach-O writer or rely on LLD. We cannot use `ld_prime` here.
- The `runtime/cosmo/Makefile` already deals with the "shell out to the host toolchain" pattern; mirror that.
- For Mochi standard library distributed as a static archive (`.a`), nothing special: `ld_prime` handles archives identically to `ld64`.

If Mochi later wants mergeable libraries (Phase 2 question), the format is documented in WWDC 2023 session 10268, and we can emit it ourselves into the Mach-O.

## §7 Open questions for MEP-42

- Do we ever recommend `-ld_classic` for users on legacy Mochi build pipelines? Answer is probably no, given Apple's deprecation.
- Do we expose the choice via a Mochi build flag, or is it always implicit per-host?
- Cross-host Mac builds: we ship `ld64.lld`? Or do we tell users "build on a Mac"? This is a major Phase 2 decision.
- How do we handle Apple's roughly-yearly Mach-O format tweaks (chained fixups, mergeable libraries, new __DATA_CONST flavors)? We follow `ld_prime` and document the minimum macOS deployment target.

Sources:
- [Apple Developer: ld_prime tag forum](https://developer.apple.com/forums/tags/linker)
- [Wade Tregaskis ld_prime posts](https://wadetregaskis.com/tags/ld_prime/)
- [Yuta Saito, "The new linker in Xcode 15"](https://speakerdeck.com/kateinoigakukun/the-new-linker-in-xcode-15)
- [WWDC 2023 session 10268: Meet mergeable libraries](https://developer.apple.com/videos/play/wwdc2023/10268/)
- [Xcode 15 linker forum threads](https://developer.apple.com/forums/thread/731089)
- [Where is the ld_prime source? (Apple Developer Forums)](https://developer.apple.com/forums/thread/749558)
- [Xcode 26 Link Error thread](https://developer.apple.com/forums/thread/788064)