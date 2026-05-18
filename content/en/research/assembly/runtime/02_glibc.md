---
title: "glibc"
description: "The default Linux libc, and the reasons \"fully static linking\" is officially unsupported."
tags: ["native-codegen", "runtime"]
weight: 20
date: 2026-05-18T18:07:50+07:00
---

## §1 Provenance

- Project home: https://www.gnu.org/software/libc/
- Git: https://sourceware.org/git/glibc.git
- Manual: https://sourceware.org/glibc/manual/
- License: LGPLv2.1+ (with some headers under more permissive terms; some test files under GPL).
- Maintainers: a steering committee under the GNU project. Notable contributors include Florian Weimer (Red Hat), Adhemerval Zanella (Linaro), Carlos O'Donell (Red Hat), Siddhesh Poyarekar.

## §2 Mechanism / function

glibc is the C library that ships with every mainstream Linux distribution that is not Alpine-shaped. It implements ISO C, POSIX, the Single UNIX Specification, X/Open, and a large set of GNU-specific extensions. It is the de facto reference for "what a Linux C program expects".

Architecture choices that are relevant for distribution and static linking:

- The NSS (Name Service Switch) framework loads pluggable backends via `dlopen` at runtime. `getpwnam`, `getgrgid`, `getaddrinfo`, and friends all consult `/etc/nsswitch.conf` and then `dlopen` the requested module (`libnss_files.so`, `libnss_systemd.so`, `libnss_ldap.so`, etc.).
- Locale data lives in `/usr/lib/locale/locale-archive` and is `mmap`ed at runtime.
- Timezone data lives in `/usr/share/zoneinfo` and is read by `tzset`.
- `iconv` modules are loaded from `/usr/lib/gconv/`.
- `libc.so.6` is symbol-versioned via `.symver` directives. A program compiled against glibc 2.40 will not run on a system with glibc 2.34. This is the famous "glibc version skew" problem.

This design makes glibc extensible at the system level but makes it hostile to portable static linking.

## §3 Platform coverage (May 2026)

Linux is the primary target. The list of glibc ports is at https://sourceware.org/glibc/wiki/PortStatus and includes essentially every Linux architecture in use: x86_64, i386, AArch64, ARM (multiple flavors), MIPS, PowerPC, RISC-V, s390x, LoongArch64. The Hurd port still exists for GNU/Hurd.

glibc does not run on macOS, Windows, BSDs, or any non-Linux kernel (except Hurd). For those you would use the platform libc.

## §4 Current status (May 2026)

The current stable line is the glibc 2.41 / 2.42 series. glibc releases roughly twice a year (February and August). Active development happens on the master branch with feature work landing continuously.

Production use: Ubuntu, Debian, Fedora, RHEL, CentOS Stream, openSUSE, Arch, Gentoo, Manjaro, every "standard" Linux distribution. Effectively every "non-Alpine, non-musl" Linux user is using glibc.

Notable 2025 events:

- The May 2025 GNU C Library security advisory roundup (https://seclists.org/oss-sec/2025/q2/161) catalogued several CVEs; nothing critical for Mochi but a reminder that static glibc is a fragile distribution model.
- Ongoing Red Hat work to make NSS files-and-DNS backends compile in (no `dlopen` for the common path), documented at https://developers.redhat.com/articles/2023/08/31/how-we-ensure-statically-linked-applications-stay-way.
- The `--enable-static-nss` configure option has been progressively gutted; it is now effectively a no-op because the relevant backends are compiled in.

## §5 Engineering cost for Mochi

The portability picture is mixed.

Dynamic linking against the host glibc: easy, but the resulting binary requires that glibc version or newer on the target. A Mochi binary built on Ubuntu 24.04 (glibc 2.39) will not run on RHEL 8 (glibc 2.28). This is a real, common deployment failure.

Static linking against glibc: officially supported only with caveats. The linker emits warnings like "Using 'getaddrinfo' in statically linked applications requires at runtime the shared libraries from the glibc version used for linking" (cataloged at https://linuxvox.com/blog/why-would-it-be-impossible-to-fully-statically-link-an-application/). The result is a binary that is "static" but still loads `.so` files at runtime through `dlopen`, defeating the purpose.

Static-PIE with glibc: supported on x86_64 (binutils 2.29+), aarch64 (binutils 2.30+), i386, x32. ARMv7 historically not. See glibc PortStatus wiki.

Versioning: the `glibc-compat-version` ABI problem is documented to death. Common mitigations:

- Build on the oldest distro you support (the "build on CentOS 7" pattern Rust used until 2024).
- Use `__GLIBC_PREREQ` macros and avoid newer symbols.
- Use the `polyfill-glibc` or `zig cc -target x86_64-linux-gnu.2.17` mechanisms to back-rev the required symbol version.
- Ship a Docker container.

For Mochi specifically, the cost is "every Mochi binary that links glibc is bound to a glibc version". This is a portability ceiling.

License: LGPLv2.1+. Dynamic linking is fine for proprietary apps. Static linking against glibc has a clause that requires source availability or relinkable object files; this would constrain Mochi binaries' license profile if we ever did fully static glibc.

## §6 Mochi adaptation note

The pragmatic Mochi position:

- Default Linux native build: link against the host glibc dynamically. Document the resulting glibc-version dependency.
- For `mochi build --portable` or `mochi build --musl`, use musl instead (see `01_musl_static.md`).
- We do not attempt full-static glibc; the warnings are real and the binary is fragile.
- Mochi's runtime is pure Go on the VM side. When we emit native code, the C library surface we need is small: `malloc`/`free`, `read`/`write`, `mmap`, `clock_gettime`, a handful of syscalls. The freestanding pattern (see `runtime/05_no_libc_freestanding.md`) lets us bypass libc entirely for syscalls.
- If we keep cgo-style integration (call Mochi from a Go-hosted runtime), glibc compatibility is implicit because Go ships its own statically-linked layer.

The relevant Mochi files: `runtime/vm3/memory.go` (our memory model) and `runtime/cosmo/Makefile` (the precedent for "shell out to a libc-specific toolchain").

## §7 Open questions for MEP-42

- Do we commit to a minimum glibc version for the default dynamic Linux build? My suggestion: glibc 2.31 (Ubuntu 20.04, RHEL 9 baseline). Anything older is opt-in.
- Do we ever statically link glibc? My suggestion: no. Use musl when static is needed.
- Do we use `zig cc -target ...gnu.X.Y` to back-rev the symbol requirements? It works and is widely deployed (used by Bun, Uber, many production tools).
- LGPLv2.1+ implications: dynamic linking is unconstrained; we never statically embed glibc into a redistributed binary.

Sources:
- [GNU glibc home](https://www.gnu.org/software/libc/)
- [Why Fully Static Linking is Impossible (linuxvox)](https://linuxvox.com/blog/why-would-it-be-impossible-to-fully-statically-link-an-application/)
- [Red Hat: How we ensure statically linked applications stay that way](https://developers.redhat.com/articles/2023/08/31/how-we-ensure-statically-linked-applications-stay-way)
- [Chris's wiki: Linux Static Linking vs glibc](https://utcc.utoronto.ca/~cks/space/blog/linux/LinuxStaticLinkingVsGlibc)
- [glibc security advisories 2025-05](https://seclists.org/oss-sec/2025/q2/161)
- [Proposal: Deprecate static dlopen](https://patchwork.ozlabs.org/project/glibc/patch/a17d9928-f6a7-0b17-726d-10381478e713@redhat.com/)