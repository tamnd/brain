---
title: "Apple Universal Binaries"
description: "Fat Mach-O wrapping arm64 + x86_64, the lipo tool, and the end of x86_64 support."
tags: ["native-codegen", "runtime"]
weight: 60
date: 2026-05-18T18:13:12+07:00
---

## §1 Provenance

- Apple developer doc, "Building a universal macOS binary": https://developer.apple.com/documentation/apple-silicon/building-a-universal-macos-binary
- WWDC 2020 introduction (transition keynote, session 102): https://developer.apple.com/videos/play/wwdc2020/102/
- Universal binary background: https://en.wikipedia.org/wiki/Universal_binary
- `lipo(1)` man page: shipped with Xcode command-line tools (no canonical web URL; check `man lipo` on a Mac).
- The Future of Intel Macs (Eclectic Light, July 2025): https://eclecticlight.co/2025/07/04/whats-the-future-for-your-intel-mac/

## §2 Mechanism / function

A Mach-O "fat" or "universal" binary is a wrapper that contains multiple independent Mach-O images, one per architecture, prefixed by a small header that lets the macOS loader pick the right slice at execution time. The format predates Apple Silicon (it was used during the PowerPC-to-Intel transition in 2006) and was rebranded "Universal 2" when Apple added arm64 to the mix at WWDC 2020.

The fat header (`struct fat_header` in `<mach-o/fat.h>`) lists:

- Magic number (`FAT_MAGIC` = 0xCAFEBABE, or `FAT_MAGIC_64` for 64-bit offsets).
- Number of fat_arch entries.
- Each entry contains a CPU type, a CPU subtype, a file offset into the fat binary, a size, and an alignment.

At `execve`, the kernel reads the fat header, walks the entries, picks the one matching the running CPU, and treats only that slice as the Mach-O to load.

The `lipo` tool is the userspace utility for building, splitting, and inspecting fat binaries:

- `lipo -create x86_64/foo arm64/foo -output universal/foo` concatenates two thin Mach-O images into a fat binary.
- `lipo -thin arm64 universal/foo -output arm64/foo` extracts a single architecture.
- `lipo -info universal/foo` prints the architecture list.
- `lipo -archs universal/foo` prints just the architecture names.
- `lipo -remove x86_64 universal/foo -output arm64/foo` removes one architecture.

`lipo` works on both executable Mach-O files and static archives (`.a`).

## §3 Platform coverage (May 2026)

Fat Mach-O is exclusive to Apple platforms: macOS, iOS, iPadOS, tvOS, watchOS, visionOS.

Architectures supported in `fat_arch`:

- arm64, arm64e (Apple Silicon Macs; arm64e is the pointer-authentication variant used by Apple's own binaries).
- arm64_32 (Apple Watch).
- x86_64, x86_64h (Haswell-and-newer Intel optimized).
- i386 (Intel 32-bit; effectively retired).
- armv7, armv7s, armv7k (older iOS and Apple Watch).

Apple does not officially document the format for use outside Apple platforms. There is no Linux or Windows equivalent; the closest analog is the FreeBSD `crunchgen` static-multicall pattern, which is unrelated.

## §4 Current status (May 2026)

macOS 26 (the "Tahoe" release, fall 2025) is widely expected to be the last macOS release with first-class Intel Mac support. Apple has not formally announced a final cutoff, but ecosystem signals point in one direction:

- Major third-party vendors have started shipping arm64-only macOS builds (per https://eclecticlight.co/2025/07/04/whats-the-future-for-your-intel-mac/).
- macOS Sequoia (2024) and Tahoe (2025) did introduce some new features that exclude older Intel hardware.
- T2 chip firmware updates are expected to end with macOS 26.
- Xcode 29 may drop x86_64 entirely; Apple has not committed but the path is well telegraphed.

Today (May 2026), Universal 2 binaries (arm64 + x86_64) remain the recommended distribution format for macOS apps that want to support both Apple Silicon and Intel Macs. The recommendation will reverse within a year or two, with arm64-only becoming the new default.

`lipo` itself is not deprecated. It will continue to exist as a tool for inspecting and slicing Mach-O fat binaries. The use case (combining x86_64 + arm64) is the one fading.

## §5 Engineering cost for Mochi

For Mochi's macOS native target:

- Phase 1: build arm64 and x86_64 separately, then `lipo -create` them into a universal binary. Standard pattern; cheap.
- Phase 2: build arm64 only by default. Treat universal as an opt-in (`mochi build --universal`).
- The Mochi compiler runs on the host; cross-host compile (Linux build host targeting macOS) requires either `osxcross` or Zig's bundled macOS SDK. Cross-compile to arm64 is the easy case; x86_64 cross-compile is the same setup.
- Code signing must happen on the universal binary AFTER `lipo -create`, not on the per-arch slices. `codesign` on a universal Mach-O signs each slice's `__LINKEDIT`.
- Notarization works on the universal binary (see `08_signing_notarization.md`).
- License: nothing; Apple tools are free with Xcode.

The cost is minimal. For Mochi we essentially need to:

1. Build for arm64-apple-darwin and x86_64-apple-darwin.
2. Run `lipo -create`.
3. Sign and notarize.

## §6 Mochi adaptation note

Mochi's macOS path:

1. `compiler3/emit` already produces native code per target. The build driver runs the compiler twice (once per arch), then `lipo`.
2. A small `tools/mac/universal.go` package wraps `lipo` invocation, similar to `tools/cosmo/cosmo.go`.
3. The Mochi build command `mochi build --universal` runs the two-arch build and produces a single fat output.
4. Default in Phase 1: build for the host arch only. Universal is opt-in.
5. Default in Phase 2 (after Apple drops Intel): arm64 only.

The Mochi standard library statically linked into the binary contributes equally to both slices, so a universal binary is roughly 2x the size of a single-arch one. We document this.

## §7 Open questions for MEP-42

- Do we default to universal on macOS? Recommendation: no, default to host arch only. Document the `--universal` flag.
- When do we drop x86_64 entirely? Recommendation: when Apple does (likely Xcode 29 or 30).
- Do we ever need arm64e support? arm64e uses pointer authentication and is only for Apple's first-party binaries (App Store apps cannot use arm64e). Skip.
- For static archives we distribute (a future `.mochilib` artifact?), do we ship universal or per-arch? Per-arch is simpler.

Sources:
- [Apple: Building a universal macOS binary](https://developer.apple.com/documentation/apple-silicon/building-a-universal-macos-binary)
- [Wikipedia: Universal binary](https://en.wikipedia.org/wiki/Universal_binary)
- [Eclectic Light: What's the future for your Intel Mac?](https://eclecticlight.co/2025/07/04/whats-the-future-for-your-intel-mac/)
- [Indie Hackers: Building a universal binary](https://www.indiehackers.com/product/softmeter-application-analytics/building-a-macos-universal-binary-arm64-x86-64--MMXBITKA6c7x4Efmalv)
- [WWDC 2020: Apple silicon transition](https://developer.apple.com/videos/play/wwdc2020/102/)