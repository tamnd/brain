---
title: "Code Signing and Notarization"
description: "Gatekeeper, notarytool, SmartScreen, Authenticode, and the real cost of shipping a desktop binary."
tags: ["native-codegen", "runtime"]
weight: 80
date: 2026-05-18T18:15:20+07:00
---

## §1 Provenance

- Apple developer doc, "Notarizing macOS software before distribution": https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
- Apple Developer ID program: https://developer.apple.com/developer-id/
- Microsoft Trusted Signing (formerly Azure Code Signing): https://learn.microsoft.com/en-us/azure/trusted-signing/
- Microsoft Authenticode Signing PE files: https://learn.microsoft.com/en-us/windows-hardware/drivers/install/authenticode
- Moonbase, "Code signing audio plugins in 2025": https://moonbase.sh/articles/code-signing-audio-plugins-in-2025-a-round-up/
- Reverse Society, "Complete Guide to Notarizing macOS Apps with notarytool": https://tonygo.tech/blog/2023/notarization-for-macos-app-with-notarytool

## §2 Mechanism / function

Three OS-level gatekeeping systems shape what users see when they double-click a downloaded binary:

macOS Gatekeeper checks every executable downloaded from a browser or messaging app. It enforces:

- A valid Developer ID Application signature from an Apple-issued certificate.
- A notarization ticket from Apple's notarization service, proving Apple has scanned the binary.
- Hardened Runtime entitlements (the binary cannot inject code, disable memory protections, etc., unless explicitly entitled).
- A secure timestamp.

The `codesign` tool signs the binary. `xcrun notarytool` submits the signed binary to Apple, which returns a ticket. `xcrun stapler staple` attaches the ticket so Gatekeeper can verify offline. `spctl --assess` validates the full chain.

Windows SmartScreen uses Microsoft's URL and file reputation database. A binary signed with an EV (Extended Validation) Code Signing certificate, or via Microsoft Trusted Signing, bypasses the warning. A binary signed with a regular Authenticode certificate (the cheaper "OV" tier) now provides essentially no benefit, since Microsoft changed the rules in June 2023 to require EV for SmartScreen reputation. A binary with no signature gets the loudest warning.

Authenticode is the underlying PE signature format (since Windows NT 4.0). The `signtool` utility signs the binary using a certificate from a recognized Certificate Authority (DigiCert, Sectigo, GlobalSign). The signature is appended to the PE as a `WIN_CERTIFICATE` blob.

Linux: no OS-level equivalent. Distribution-level signing exists (`rpm-sign` for RPMs, `debsigs` for Debian packages, the per-archive signatures Arch and Alpine use) but a downloaded raw ELF is just trusted by the user. Snap and Flatpak have their own signing.

## §3 Platform coverage (May 2026)

macOS: every macOS release since Catalina (10.15, 2019) requires notarization for downloaded binaries. iOS / iPadOS / tvOS / watchOS / visionOS all require App Store distribution or, on macOS only, Developer ID + notarization.

Windows: SmartScreen is enabled by default on Windows 10 and 11. Authenticode signing applies to PE binaries (`.exe`, `.dll`, `.sys`, `.msi`).

Linux: each distro has its own package signing. For loose binaries, no signing is required (and no OS dialog is presented). AppImage, Snap, Flatpak each have their own signing semantics.

## §4 Current status (May 2026)

macOS notarization:

- `notarytool` replaced `altool` on November 1, 2023. `altool` no longer accepts submissions.
- Hardened Runtime is now required for new submissions.
- Stapling is required for apps and installer packages but is not possible for unbundled command-line binaries. CLI binaries get notarized but cannot have the ticket stapled; Gatekeeper checks them online.
- Typical notarization turnaround: under 5 minutes. Occasional Apple-side outages (February 2026 saw multi-hour delays per Apple Developer Forum reports).
- Apple Developer Program membership: USD 99 per year. Required for a Developer ID certificate.

Windows signing:

- EV Code Signing required for SmartScreen reputation since June 2023.
- EV certificates require a hardware token (HSM) compliant with FIPS 140 Level 2. This forbids fully-cloud CI signing of the traditional kind.
- Microsoft Trusted Signing (https://learn.microsoft.com/en-us/azure/trusted-signing/) is Microsoft's cloud-based alternative: signing happens in Azure, no hardware token required, prices are lower (USD 9 to 100 per month tier).
- Trusted Signing eligibility: US and Canada organizations with three or more years of verifiable business history; also individual developers in those regions.
- `jsign` (https://github.com/ebourg/jsign) is a Java-based open-source signer that supports Trusted Signing from Linux and macOS CI hosts.

Linux:

- RPM-based distros use GPG signatures, validated by `dnf` / `yum`.
- Debian uses GPG signatures, validated by `apt` / `dpkg`.
- AppImage can be signed with GPG, but most are not.
- Snap and Flatpak each have their own enforcement.

## §5 Engineering cost for Mochi

Mochi binaries that ship to end users need to grapple with this:

macOS:

- Mochi distribution itself needs Apple Developer ID + notarization. Costs USD 99/year plus the engineering time to set up the signing pipeline.
- For Mochi-COMPILED user binaries: we cannot sign on the user's behalf. Either the user has their own Developer ID, or their binaries are unsigned (and only runnable by the user themselves via "Open Anyway" or `xattr -d com.apple.quarantine`).
- Mochi can ship a `mochi build --sign --notarize` helper that wraps `codesign` and `notarytool` for users who have their own credentials.

Windows:

- Same story. Mochi the toolchain should be EV-signed or Trusted-Signing-signed for SmartScreen.
- For user-built binaries, document the path (signtool or jsign).

Linux:

- Mochi distribution: optionally provide signed `.rpm` and `.deb` packages alongside raw tarballs.
- User binaries: nothing needed at OS level.

Cosmopolitan / APE binaries (see `runtime/03_cosmopolitan_libc.md`) hit signing pain hardest. The polyglot format is not a clean Mach-O bundle, so notarization is awkward. Cosmo users typically distribute "Linux first, runs on Mac as a bonus" rather than signing for macOS Gatekeeper.

## §6 Mochi adaptation note

Mochi's signing story:

1. The Mochi toolchain distribution: invest in Apple Developer ID (USD 99/year) and Microsoft Trusted Signing (USD ~10/month). Ship signed binaries. This is mandatory if we want users to install Mochi without warnings.
2. Provide `mochi build --sign --notarize` as a thin wrapper around platform tools. The user supplies their own certificate.
3. Document the manual `codesign`/`notarytool`/`signtool` flow in `docs/distribution.md`.
4. Provide CI examples (GitHub Actions, GitLab CI) that show how to sign with hosted secrets.
5. Relevant Mochi files: a new `tools/sign` package, paired with `tools/cosmo` for the alternative APE flow.

The Mochi project itself faces a meta-question: who holds the signing keys? Recommendation: the project's release engineer (currently a small team) keeps EV tokens and Apple Developer keys in HSMs.

## §7 Open questions for MEP-42

- Do we ship signed Mochi releases for macOS and Windows? Recommendation: yes, this is table-stakes.
- Do we provide a free signing service for Mochi users? Probably not (Apple and Microsoft would view this as abuse).
- Do we recommend a specific CA? Microsoft Trusted Signing is the cheapest path on Windows. DigiCert and Sectigo are the established choices.
- For Linux, do we sign tarballs with GPG and publish keys? Recommended: yes, low cost.
- For Cosmopolitan output, what do we tell macOS users? "Right-click, Open" is the practical answer.

Sources:
- [Apple: Notarizing macOS software before distribution](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
- [Apple Developer ID](https://developer.apple.com/developer-id/)
- [Microsoft Trusted Signing](https://learn.microsoft.com/en-us/azure/trusted-signing/)
- [Microsoft: Authenticode signing of PE files](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/authenticode)
- [Moonbase: Code signing audio plugins in 2025](https://moonbase.sh/articles/code-signing-audio-plugins-in-2025-a-round-up/)
- [Reverse Society: notarytool guide](https://tonygo.tech/blog/2023/notarization-for-macos-app-with-notarytool)
- [DigiCert: Code Signing for Mac Developers (2026 guide)](https://comparecheapssl.com/digicert-code-signing-for-mac-developers-a-complete-guide/)