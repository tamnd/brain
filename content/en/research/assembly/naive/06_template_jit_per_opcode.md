---
title: "The Per-Opcode Template JIT Pattern"
description: "The general pattern that Sparkplug, Liftoff, JSC Baseline, and the HotSpot template interpreter all instantiate. Per-op native template, fixed register convention, stub calls for slow paths, optional inline caches as patchable code regions. Specifically considered here as an engineering implementation in pure Go without cgo."
tags: ["native-codegen", "naive"]
weight: 60
date: 2026-05-18T18:06:46+07:00
---

## §1 Provenance

- HotSpot Template Interpreter (Sun Microsystems, ~2002+): the urtext of this pattern. See "The Java HotSpot Performance Engine Architecture" (https://www.oracle.com/java/technologies/whitepaper.html).
- Erlang BEAM (Ericsson, 1998+): the JIT in OTP 24+ (BeamAsm, https://www.erlang.org/blog/a-first-look-at-the-jit/) is template-style, written in C++ over asmjit.
- Lua/LuaJIT 2.x interpreter (Mike Pall): the interpreter is itself a hand-written assembler with one template per op. JIT is trace-based, but interpreter design is template.
- Sparkplug (V8, 2021), Liftoff (V8, 2018), JSC Baseline (Apple, ~2008): see neighbor docs 01, 02, 05.
- General writeup: Anton Ertl, "The Structure and Performance of Efficient Interpreters" JILP 5 (2003), https://www.complang.tuwien.ac.at/papers/ertl%26gregg03jilp.pdf.

## §2 Technique / contribution

The pattern has these load-bearing elements:

1. **Fixed register convention.** Choose ~3-6 callee-save registers as "VM registers": typically PC, frame-pointer, accumulator, scratch1, scratch2. Caller-save registers are free for templates to clobber within a single op.

2. **One emit function per opcode.** Each function takes the current `EmitContext` and the decoded operands, and emits a short native sequence (typically 5-30 bytes per op).

3. **Slow-path stubs.** When an op needs heavyweight semantics (allocation, type miss, GC barrier), the template emits a single `call slow_path_stub` to a pre-compiled function. The stub uses the same VM-register convention so it can clobber freely.

4. **Inline cache slots (optional).** A patch site is a few NOPs that get rewritten on first execution with a fast-path check + jump. JSC and V8 use this heavily; copy-and-patch and Liftoff do not.

5. **Per-arch backend.** The emit functions are ISA-specific. Code-quality work is per-arch; the rest of the framework is shared.

**Pure-Go implementation outline (no cgo):**

```go
type Emitter struct {
    buf  []byte   // mmap'd RWX region
    pos  int
    labels map[Label]int
}

func (e *Emitter) emit_load(arena_reg, dst_reg, slot int) {
    // mov dst_reg, [arena_reg + slot*8]
    e.emitREX(0, dst_reg, arena_reg)
    e.emitByte(0x8B)
    e.emitModRM(0x80, dst_reg & 7, arena_reg & 7)
    e.emitInt32(int32(slot * 8))
}
```

The full set of x86-64 instruction encodings is ~3,000 LOC of pure Go. ARM64 is similar (instructions are fixed 32-bit so encoding is simpler in some ways, harder in others due to immediate quirks).

For mmap and mprotect:
```go
import "golang.org/x/sys/unix"

func allocExec(size int) ([]byte, error) {
    return unix.Mmap(-1, 0, size,
        unix.PROT_READ|unix.PROT_WRITE|unix.PROT_EXEC,
        unix.MAP_PRIVATE|unix.MAP_ANON)
}
```

On Apple Silicon (arm64 macOS) we must use `MAP_JIT` plus `pthread_jit_write_protect_np()` flips to switch between writable and executable. On Linux any sane W^X discipline works.

## §3 Where it shines, where it fails

**Shines:**
- Tiny runtime footprint: emitter + handler set fits in ~10K LOC for one ISA.
- Compile speed: ~10-50 MB/s of machine code.
- Each op template can be tuned by hand for a hot path.
- Pure Go implementation needs no toolchain at runtime.
- Predictable: no LLVM black-box performance cliffs.

**Fails:**
- Cross-op optimization is zero (per-op only).
- Hand-written templates rot when the ISA grows new addressing modes or instructions.
- IC management is genuinely hard to get right (atomic patches, instruction cache flush, concurrent execution).
- Generated code is 2-5x slower than an optimizing backend.

## §4 Status (May 2026)

- BEAM's BeamAsm is the most recent production deployment (OTP 24, 2021), using asmjit for x86-64 and arm64. It is the default in Erlang/Elixir releases.
- Sparkplug, JSC Baseline, Liftoff, sm-base, and Winch are all production template JITs.
- Pure-Go template JITs are rarer. Notable: `github.com/twitchyliquid64/golang-asm` (a fork of Go runtime's internal asm) and `github.com/modern-go/gls`. Neither is a full Mochi-ready toolkit.
- Titzer 2024 (CGO) is the current state-of-the-art analytical comparison.

## §5 Engineering cost for Mochi

A pure-Go, no-cgo template JIT for Mochi:

- 2 weeks: pick or fork a Go x86-64 assembler library. The Go runtime's internal `cmd/internal/obj/x86` is GPL-incompatible with Mochi's MIT-style license; we likely need a from-scratch encoder or a fork of golang-asm.
- 3 weeks: per-op template emit functions for the ~100 Mochi ops, x86-64.
- 1 week: mmap/mprotect plumbing for Linux, macOS, Windows.
- 1 week: macOS arm64 JIT-write-protect ergonomics.
- 2 weeks: slow-path stub library (reuse vm3 op handlers via Go function pointers).
- 2 weeks: smoke tests against `compiler3/corpus/`.

Total: ~11 weeks for an x86-64 template JIT. arm64 adds ~6 weeks (encoder + per-op).

Inline caches add another 4-6 weeks if we want them. For MEP-42 phase 1, skip ICs.

## §6 Mochi adaptation note

- `runtime/vm3/op.go`: each Op needs an emit function.
- `runtime/vm3/cell.go`: Cell is a `uint64` that the templates load and store.
- `runtime/vm3/frame.go`: the three-bank register file dictates which physical registers we reserve. Suggested mapping (x86-64 System V):
  - R12 = int arena base
  - R13 = float arena base
  - R14 = pointer arena base
  - R15 = frame pointer
  - rbx = current Cell accumulator
- `runtime/vm3/arenas.go`: the arena base loads in the function prologue use these regs.
- `compiler3/emit/` is a natural home for the emit functions; we add a sibling `compiler3/jit/` for the runtime.

**Pure-Go-no-cgo is a major Mochi constraint.** It means we cannot rely on LLVM at runtime. Template JIT is the natural fit; copy-and-patch needs Clang at build time, which is acceptable.

## §7 Open questions for MEP-42

- Do we fork golang-asm or write from scratch?
- Slow-path stubs as Go function calls or as pre-compiled native stubs? Go ABI prevents direct calls from JIT'd code without an asm trampoline.
- Goroutine-safe codegen: the Mochi runtime is goroutine-heavy. Code cache writes must be protected.
- macOS arm64 JIT entitlement: this requires an entitlement plist on signed binaries. Do we ship pre-signed binaries or document a workaround?
- Code cache size limit: how do we cap memory growth?
- Tier-up trigger: function call count threshold?
- Per-op vs super-op templates: pre-fuse common pairs like `load+add+store`?

## §8 References

- HotSpot Template Interpreter: https://www.oracle.com/java/technologies/whitepaper.html.
- BeamAsm (Erlang JIT): https://www.erlang.org/blog/a-first-look-at-the-jit/.
- LuaJIT 2.x source: https://github.com/LuaJIT/LuaJIT.
- Anton Ertl, "The Structure and Performance of Efficient Interpreters" JILP 5 (2003): https://www.complang.tuwien.ac.at/papers/ertl%26gregg03jilp.pdf.
- Apple, "Porting Just-In-Time Compilers to Apple Silicon" (https://developer.apple.com/documentation/apple-silicon/porting-just-in-time-compilers-to-apple-silicon).