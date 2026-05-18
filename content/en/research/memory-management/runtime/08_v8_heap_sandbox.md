---
title: "V8 Sandbox"
description: "A purely software in-process sandbox for the V8 JS heap. Ban raw pointers, replace with offsets into a 1 TB sandbox region and indices into out-of-sandbox pointer tables. About 1% perf cost, enabled by default in Chrome 123. Every modern JIT is moving this direction."
tags: ["memory-safety", "runtime"]
weight: 80
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Designer:** Samuel Groß (formerly Google Project Zero, now leads V8 Security at Google).
- Talk: "The V8 Heap Sandbox," OffensiveCon 2024 — https://saelo.github.io/presentations/offensivecon_24_the_v8_heap_sandbox.pdf.
- Workshop paper: Groß, "The V8 Sandbox," MoreVMs 2025 (Programming 2025).
- Official blog: https://v8.dev/blog/sandbox.
- README: https://chromium.googlesource.com/v8/v8.git/+/refs/heads/main/src/sandbox/README.md.
- Rollout: enabled by default Chrome 123 (April 2024) on Linux/Windows/macOS/ChromeOS/Android, 64-bit only.
- Inclusion in Chrome's Vulnerability Reward Program (VRP): announced 2025; sandbox no longer "experimental."

## §2 Mechanism

The threat model assumes the attacker has a *write-anywhere* primitive inside the V8 heap (typically the outcome of a JIT type confusion). Goal: make that primitive useless for escaping the V8 heap.

The mechanism: **ban every raw pointer or 64-bit size from data the attacker can corrupt.** Specifically:

1. **The sandbox region.** A 1 TB virtual-address-space reservation. All V8 HeapObjects live inside. References between HeapObjects are 32-bit offsets from the sandbox base (`Tagged_t`), enabled by pointer compression (see file 12).
2. **External pointer table (EPT).** Any pointer to memory outside the sandbox (e.g. an `ArrayBuffer`'s backing store) is stored as a 32-bit **handle** into the EPT — a flat array of 64-bit entries, allocated outside the sandbox. A heap object holds the handle; dereferencing means `EPT[handle].pointer`.
3. **Trusted heap / trusted space.** Some HeapObjects are too sensitive to live inside the sandbox: bytecode arrays, JIT-compiled code metadata, anything whose corruption would yield PC control. These are allocated in **trusted space** outside the sandbox, and referenced from inside via the **trusted pointer table** (TPT) — same indirection-table pattern as EPT.
4. **Code pointer table (CPT).** A specialisation: each entry is `(Code object pointer, entrypoint pointer)`. `JSFunction → CPT entry → entrypoint`. Replaces a direct compressed pointer to the Code object, restoring ~all of the perf lost to code-pointer sandboxing.
5. **Sandbox-compatible sizes.** Sizes are stored as 32-bit values bounded by the sandbox max (32 GB), preventing the classic "tamper with size to do OOB read."

Net effect: an attacker who controls a write-anywhere primitive inside the sandbox can corrupt only sandbox-resident memory. PC, function tables, JIT code, and external buffers are reached only through pointer tables, whose entries are verified on every dereference (tag/type checks; the table is in RX-or-RW-but-not-corruptible memory).

## §3 Memory-safety property

The V8 Sandbox is a **mitigation, not a guarantee**. The threat model accepts that V8 will continue to have type-confusion bugs (most are JIT logic bugs, not memory-safety bugs). The sandbox limits *blast radius*: a successful in-heap corruption no longer trivially yields process-wide R/W.

It is *not* memory safety in the Rust/Cyclone/WUFFS sense. There is still memory corruption; it is just contained. Samuel Groß's own framing: "current memory-safety technologies are largely inapplicable to optimizing JS engines... the sandbox is therefore a necessary step toward memory safety."

## §4 Production status (May 2026)

- Default-enabled in Chrome 123+ on 64-bit (Android, ChromeOS, Linux, macOS, Windows). Hundreds of millions of installs.
- Included in Chrome VRP — Google now pays out for sandbox-bypass research. That signals "production hardened security boundary."
- 16 zero-days affecting V8 between 2021-2023 informed the design.
- Recent V8 exploits (post-March 2024) have to bypass the sandbox to be useful. Empirically this raises the bar (more bug chains, more primitives required); not a panacea.
- MoreVMs 2025 paper documents lessons learned and the remaining gaps.

## §5 Cost

- **Throughput.** ~1% on Speedometer and JetStream. The cost comes from:
  - One extra memory load per external-pointer dereference (table indirection).
  - Shift-add (typically `base + zext32(offset)`) for every in-heap pointer load.
- **Memory.** Modest. EPT and CPT are arrays sized to the live external-pointer set; pointer tables are compactible (V8 implements EPT compaction).
- **Virtual address space.** 1 TB per V8 isolate group (see file 12 on multi-cage mode for the tradeoff).
- **Code complexity.** Substantial. Every V8 codegen path now distinguishes "compressed pointer," "external pointer (= EPT handle)," "indirect pointer (= TPT handle)," "code pointer (= CPT handle)." The README documents this carefully.

## §6 Mochi adaptation note

This is the topic with the most to teach vm3, because the architecture **already incidentally implements much of the V8 sandbox model**:

| V8 Sandbox concept | vm3 equivalent (MEP-40) |
|---|---|
| Compressed heap pointer (32-bit offset) | `Cell.slabIndex` (32-bit) into typed arena |
| External pointer table | We don't ship any external pointers; backing slices are Go-rooted |
| Indirect pointer / trusted pointer table | Handle → arena → backing slice. Handle is *itself* the indirection. |
| Trusted space (bytecode, code metadata) | `vm.code` byte slice + per-function metadata are Go-managed, never referenced through the Cell at all |
| Code pointer table | Function tables in `compiler3` IR; JIT (Phase 5) will need its own equivalent |
| Sandbox-compatible sizes | Lengths are stored in Go `int` / slice headers, untouchable by Mochi code |

So Mochi gets the V8 sandbox's structural win *for free* by being a Go-hosted bytecode VM. The "compressed pointer" is the slab index; the "indirect pointer table" is the arena's backing slice; the "trusted space" is anything Go owns.

The smallest additions worth making explicit in MEP-41:

1. **Generation-tag check on every handle deref (MEP-40 §6.1).** Already planned. This is the ABA defence: if a slot is freed and re-issued, the 12-bit generation differs and the deref traps. This is exactly what V8's TPT slot-version field does.
2. **Reserve a "trusted handle" arena tag.** Currently we have 4 arena tag bits (16 tags), 11-12 used. Reserve tag 15 for "trusted reference into Go-owned metadata not accessible from Mochi code." Sets the boundary clearly for JIT-emitted accessors.
3. **JIT must use indirect calls through a code table (MEP-40 Phase 5, vm3jit).** Don't emit raw code pointers into compiled bytecode. Every Mochi-level callable is a `(funcID, generation)` that the JIT resolves through a host-owned function table. This is the V8 CPT pattern and prevents a bytecode-corruption bug from steering execution.

No design conflict — in fact, MEP-41 should claim the V8 sandbox model as **architectural validation** for vm3's handle-based ABI.

## §7 Open questions for MEP-41

- Do we need an *explicit* sandbox-region boundary (V8-style: "everything inside this 1 TB virtual block is the sandbox; everything outside is not"), or is "all data is Go-owned" sufficient? The latter only works if no JIT escape can scribble into Go memory.
- vm3jit emits machine code. That code reads/writes Go slice headers (the backing storage). If a Mochi bug yields write-anywhere *inside Go memory*, the sandbox is gone. What's the JIT's bounds-check discipline?
- Should we publish a written threat model — what attackers can do, what the sandbox prevents — analogous to V8's blog post? It would clarify the JIT design for Phase 5.
- Is it worth the engineering cost to emulate the EPT explicitly even though Go gives us indirection for free, just for clarity in audits?

## Sources

- [The V8 Heap Sandbox (OffensiveCon 2024, Samuel Groß)](https://saelo.github.io/presentations/offensivecon_24_the_v8_heap_sandbox.pdf)
- [The V8 Sandbox (V8 blog)](https://v8.dev/blog/sandbox)
- [V8 Sandbox README (Chromium source)](https://chromium.googlesource.com/v8/v8.git/+/refs/heads/main/src/sandbox/README.md)
- [Google Chrome Adds V8 Sandbox (The Hacker News)](https://thehackernews.com/2024/04/google-chrome-adds-v8-sandbox-new.html)
- [The V8 Sandbox (MoreVMs 2025)](https://2025.programming-conference.org/details/MoreVMs-2025-papers/3/The-V8-Sandbox)
- [Breaking V8 Sandbox with Trusted Pointer Table (HITCON write-up)](https://mem2019.github.io/jekyll/update/2024/07/14/HITCON.html)