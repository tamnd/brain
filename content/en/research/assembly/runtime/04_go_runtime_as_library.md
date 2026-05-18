---
title: "The Go Runtime as a Library"
description: "cgo, c-shared, c-archive: keep vm3 in Go and call into it from native code."
tags: ["native-codegen", "runtime"]
weight: 40
date: 2026-05-18T18:08:55+07:00
---

## §1 Provenance

- cgo package docs: https://pkg.go.dev/cmd/cgo
- runtime/cgo: https://pkg.go.dev/runtime/cgo and https://go.dev/src/runtime/cgo/
- Build mode docs: https://pkg.go.dev/cmd/go#hdr-Build_modes
- Cgo cost analysis (Cockroach Labs): https://www.cockroachlabs.com/blog/the-cost-and-complexity-of-cgo/
- Go 1.22 release notes: https://go.dev/doc/go1.22
- License: BSD 3-clause (Go itself).
- Maintained by the Go team at Google plus a large community.

## §2 Mechanism / function

Go supports three relevant cross-language build modes:

`-buildmode=c-archive` produces a static library (`.a` on Unix, `.lib` on Windows) that exposes Go-defined functions as C-callable symbols. The Go runtime (scheduler, GC, goroutines) is initialized lazily on first call. The archive can be linked into any C/C++ program.

`-buildmode=c-shared` produces a shared object (`.so` / `.dylib` / `.dll`) with the same calling convention. Useful for plug-ins and for `dlopen` from other languages (Python, Ruby, etc.).

`-buildmode=exe` (default) plus `import "C"` lets a Go program call C and vice versa within the same binary.

In every cgo direction, each call crosses a "system stack" boundary: the Go runtime maintains small goroutine stacks (typically 2 KB grow-on-demand), while C expects a real OS thread stack (typically 8 MB on Linux). cgo switches stacks at every transition.

`runtime/cgo` is the package that implements the switch: `_cgo_init`, `cgocall`, `cgocallback`, `x_cgo_getstackbound`. On a c-archive load, `_cgo_init` is called once per process; `runtime.rt0_go` then runs the usual Go init sequence (scheduler bring-up, GC init, package init functions). This is the famous "Go runtime startup".

## §3 Platform coverage (May 2026)

c-archive and c-shared support all of Go's tier-1 ports:

- linux/{amd64, arm64, arm, 386, ppc64le, riscv64, s390x}
- darwin/{amd64, arm64}
- windows/{amd64, arm64, 386}
- freebsd/{amd64, arm64}
- openbsd, netbsd

Less complete on android/ios but works via the gomobile flow.

Any host that can compile Go can build a c-archive for any supported target via `GOOS=... GOARCH=... go build -buildmode=c-archive`. cgo cross-compilation requires a target-aware C compiler (typically `zig cc -target ...` does the trick).

## §4 Current status (May 2026)

Go 1.24 (early 2025) and Go 1.25 (August 2025) continued the trend of making cgo faster and more correct, but cgo overhead remains a known cost. The Go 1.22.5 (July 2024) cgo regression (https://github.com/golang/go/issues/68587) revealed that per-call cgo cost can balloon when glibc's `pthread_getattr_np` parses `/proc/self/maps` via `sscanf`, taking 76% of the call time in pathological c-shared callers. Fixes have improved this but not eliminated it.

Per-call overhead in steady state, May 2026: roughly 50 to 200 ns per cgo call on x86_64-linux, depending on direction (Go-calls-C vs C-calls-Go) and on whether goroutine stack growth is triggered. Pure Go calls are roughly 1 to 2 ns. So cgo is roughly 50x to 100x slower than a native Go call.

Runtime startup cost: the Go runtime initializes in roughly 1 to 5 ms on a modern machine, dominated by `runtime.schedinit` and GC bring-up. For a long-running server this is irrelevant; for a CLI tool invoked many times per second it is the dominant cost.

Production users: lots of Go-written shared libraries are deployed. Notable examples include the `kubectl` plug-in surface, `tailscale`'s embedded library form, several CGo-loaded Go modules used inside Python and Rust ecosystems.

## §5 Engineering cost for Mochi

This is the path of least resistance. Mochi already has vm3 implemented in Go. If we keep vm3 in Go and emit native code that calls into it via cgo, we get:

- All of Go's GC, goroutine scheduler, channels, network poller, file I/O for free.
- The Mochi standard library can keep its existing Go implementation.
- We only need a thin native-code surface: roughly "call this Mochi function with these args".

The costs:

- Every Mochi-to-vm3 call is a cgo call. If Mochi-emitted native code is doing fine-grained work and calling back into vm3 frequently, the cgo cost dominates.
- The startup cost is unavoidable: ~3 ms before the first native instruction runs.
- The output binary must include the Go runtime (~1.5 MB minimum) plus all imported Go packages.
- cgo on Windows historically lagged; today it works but with some caveats around signal handling and SEH exceptions.
- Cross-compile is harder. We need a C cross-compiler for the target, plus matching headers.

This pattern is a Phase 1 stepping stone, not a Phase 2 destination. The Phase 2 plan should aim for "native code that does not need the Go runtime at all", which means rewriting the runtime helpers in either Mochi-compiled C or freestanding code (see `runtime/05_no_libc_freestanding.md`).

## §6 Mochi adaptation note

For MEP-42 Phase 1, the recommended scaffolding:

1. Build `runtime/vm3` as a c-archive: `go build -buildmode=c-archive -o libmochivm3.a ./runtime/vm3/...`.
2. The Mochi-emitted native code calls a small surface: `mochi_run_bytecode`, `mochi_alloc`, `mochi_free`, etc., exported with `//export` directives.
3. The native code does what is convenient natively (arithmetic, hot loops, register-allocated locals) and calls back into vm3 for things that need the Go runtime (GC-managed allocation, channel ops, network I/O).
4. The link step uses the platform's `cc` driver to combine our native `.o` files with the Go c-archive.
5. The relevant Mochi files are `runtime/vm3/vm.go`, `runtime/vm3/program.go`, and a new `runtime/vm3/export.go` that adds `//export` shims.

Phase 2 might move the runtime out of Go entirely. Phase 1 keeps it.

The `tools/cosmo/cosmo.go` precedent of "drive an external toolchain" applies; the new path is "drive `go build -buildmode=c-archive` plus the platform `cc`".

## §7 Open questions for MEP-42

- Do we accept the ~3 ms startup cost in Phase 1? For a compiler that builds programs many times per second this is real, but for end-user programs it is invisible.
- How much of the Mochi runtime do we want to call from native code vs from vm3? The cgo cost suggests "as little as possible".
- Do we expose Mochi functions as C-callable symbols for embedding Mochi in other apps? (c-shared use case.)
- Phase 2: do we rewrite vm3 internals in Mochi-or-Rust-or-C so we can drop the Go runtime dependency entirely?

Sources:
- [runtime/cgo package](https://pkg.go.dev/runtime/cgo)
- [Go build modes](https://pkg.go.dev/cmd/go#hdr-Build_modes)
- [The Cost and Complexity of Cgo (Cockroach Labs)](https://www.cockroachlabs.com/blog/the-cost-and-complexity-of-cgo/)
- [Go 1.22 release notes](https://go.dev/doc/go1.22)
- [Go issue 68587: cgo perf regression in 1.22.5](https://github.com/golang/go/issues/68587)
- [Go cmd/link c-archive issue 54331](https://github.com/golang/go/issues/54331)