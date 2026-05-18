---
title: "MSWasm — Memory-Safe WebAssembly"
description: "A WebAssembly extension that replaces linear memory with segments and handles. Handles are unforgeable, typed pointers carrying bounds and provenance — closely modelled on CHERI capabilities but pure software."
tags: ["memory-safety", "runtime"]
weight: 90
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- Michael, Gollamudi, Bosamiya, Johnson, Denlinger, Disselkoen, Watt, Parno, Patrignani, Vassena, Stefan. **"MSWasm: Soundly Enforcing Memory-Safe Execution of Unsafe Code."** *POPL 2023*, PACMPL Vol. 7, Article 15 (not OOPSLA 2023; the prompt is in error).
- Earlier position paper: Disselkoen et al., "Progressive Memory Safety for WebAssembly," 2019.
- Follow-up: **Iris-MSWasm**, OOPSLA 2024 — Legoupil, Watt, Patrignani, Stefan, et al. — a fully mechanised foundation in Iris. https://dl.acm.org/doi/10.1145/3689722.
- Toolchain: https://github.com/PLSysSec/ms-wasm (rWasm AOT compiler, mswasm-graal JIT, mswasm-llvm C→MSWasm).
- Paper PDFs:
  - https://cseweb.ucsd.edu/~dstefan/pubs/michael:2023:mswasm.pdf
  - https://arxiv.org/pdf/2208.13583

## §2 Mechanism

MSWasm extends Wasm with three things:

1. **Segments.** Linear regions of memory, allocated dynamically, that can only be accessed through handles. Each segment has a unique **segment id**. Bytes in segment memory carry a **tag** distinguishing "raw byte" from "part of a handle." Reading a half-handle as a byte (or vice versa) traps.
2. **Handles.** A handle is a 4-tuple `(base, offset, bound, id)`. Operationally a fat pointer, like a CHERI capability:
   - `base` and `bound` define the segment span the handle can address.
   - `offset` is the current position inside the span.
   - `id` uniquely identifies the original allocation; freeing one handle with id X kills all handles with id X (catches temporal-safety leaks).
   - The 1.4 ABI choices for how to physically encode the handle (16 bytes, 32 bytes, packed bits…) are deliberately left to the compiler backend.
3. **New instructions.** `τ.segload`, `τ.segstore`, `slice` (restrict bounds), `handle.add` (shift offset), `segalloc`, `segfree`. None of these can *grow* a handle's authority — only restrict it.

Bounds checks happen on every `segload`/`segstore`. Temporal safety comes from a runtime allocator that records live handle ids; `segfree(h)` retires the id; any later `segload` using a handle with retired id traps.

The paper proves soundness in a linear-resource calculus and uses a novel "colored memory locations" abstraction to give compiler-backend-independent memory safety. Iris-MSWasm later mechanised this in Coq.

Implementations:
- **Pure software**: every handle is 16 bytes; every memory access does an explicit bounds check. Overhead 22-198% depending on what's enforced.
- **Hardware capabilities (Arm CHERI)**: handles map to CHERI capabilities; bounds checks are hardware-enforced. Overhead drops to ~51%.

## §3 Memory-safety property

Robust spatial safety (no OOB read/write across segment boundaries) **plus** temporal safety (no UAF via stale handles) **plus** provenance (you can't forge a handle from raw bytes — the byte tag enforces this).

This is the strongest memory-safety property of any Wasm proposal to date, and the POPL 2023 paper proves it formally.

## §4 Production status (May 2026)

- MSWasm is **not** in mainstream Wasm engines. No browser supports it. The reference implementations (rWasm, mswasm-graal) are research artefacts.
- The CG-level WebAssembly standards track has not adopted MSWasm; the closest mainstream-track work is the **memory64** and **multiple memories** proposals (see file 10), which provide weaker but cheaper abstractions.
- However: MSWasm is *influencing* the standards track. The "segmented memory" CG discussions and the proposed "wasm-pointers" or "fat-pointers" proposals draw heavily from MSWasm. Iris-MSWasm gave the proposal the formal credibility to be taken seriously.
- Industrial CHERI deployments (Microsoft CHERIoT, Arm Morello) are the most likely first home for MSWasm-style memory safety in production.

## §5 Cost

- **Throughput.** Software-only: 22% slowdown for spatial-only enforcement on PolyBenchC; 198% for full spatial+temporal. Hardware-assisted (CHERI): 51.7%.
- **Memory.** Handles are 16 bytes (vs 4 bytes for a Wasm32 pointer), so handle-rich data structures pay 4× pointer overhead.
- **Binary size.** New opcodes are short; the compiler-emitted bounds-check sequences inflate code by ~5-10%.

The numbers explain why mainstream Wasm hasn't shipped this: 22% is too much for general use, 198% is unthinkable, and CHERI hardware is not deployed at scale.

## §6 Mochi adaptation note

MSWasm's lessons map *exactly* onto vm3's handle ABI (MEP-40 §6.1):

| MSWasm concept | vm3 equivalent |
|---|---|
| Segment | Per-type arena (`kArenaList`, `kArenaString`, etc.) |
| Handle (base, offset, bound, id) | `Cell{arena_tag, generation, slab_index}` |
| Handle `id` | The `(arena_tag, slab_index)` pair |
| Generation field for use-after-free detection | The 12-bit `generation` on the Cell |
| Byte-tag distinguishing handle from data | Mochi has typed slots in the register banks, so this is implicit |
| `segload`/`segstore` bounds check | List/string accessor methods (`StringBytes`, `ListGet`, etc.) bounds-check today |

So vm3's Cell *is* a software MSWasm handle, restricted to a fixed-size base+id (we don't store `bound` because each slab entry has a fixed structure). What we lack:

1. **Sub-handle slicing with bounded authority.** Today a Mochi `list[T]` slice is a fresh allocation. MSWasm's `slice` instruction restricts a handle in place. If we adopt Roc-style seamless slices (file 02), we should think of them as MSWasm-style restricted handles: same `(arena_tag, slab_index)`, plus packed `(start, len)`. The generation must match the parent's at deref time. This *also* gives us MSWasm's temporal safety on slices for free.
2. **Explicit memory-safety claims for vm3.** Right now MEP-40 §9 talks about reclamation, not memory safety. MEP-41 should claim, with a precise statement: "vm3 enforces spatial safety on all handle dereferences via accessor-layer bounds checks, and temporal safety via the generation field." That's the MSWasm property, written in our language.
3. **Iris-MSWasm-style mechanisation (long-horizon).** Not in scope for MEP-41, but the OOPSLA 2024 follow-up shows it is *possible* to formally mechanise this kind of memory-safety property. A future MEP-50 could attempt the same for vm3.

There's *no conflict* with Mochi's design ethos. We're already most of the way there; MEP-41 just needs to write down the invariant.

## §7 Open questions for MEP-41

- Should we add an explicit "byte-tag" pattern to vm3? Probably no — we never store handles inside slab backing slices; they only live in the typed register banks. The byte-tag invariant holds *by construction*.
- The MSWasm 198% software overhead is the warning shot. How do we keep vm3's accessor-layer bounds checks cheap? Answer: rely on compiler3's static type info to elide checks on provably-in-bounds accesses, fall back to runtime check.
- Is the generation field 12 bits *enough* for the lifetime of a long-running Mochi process? At 4096 reuses-per-slot before wrap, a hot slot could wrap in seconds. Need to either widen the generation field or rate-limit slot reuse.
- Does adopting an MSWasm-shaped memory-safety claim affect Mochi's FFI story? If C code can mint raw pointers into our backing slices, the invariant breaks. The MEP needs to say: no FFI dereferences into arena backing.

## Sources

- [MSWasm POPL 2023 paper (UCSD mirror)](https://cseweb.ucsd.edu/~dstefan/pubs/michael:2023:mswasm.pdf)
- [MSWasm arXiv preprint](https://arxiv.org/pdf/2208.13583)
- [Iris-MSWasm OOPSLA 2024](https://dl.acm.org/doi/10.1145/3689722)
- [MSWasm toolchain (PLSysSec/ms-wasm)](https://github.com/PLSysSec/ms-wasm)
- [Position Paper: Progressive Memory Safety for WebAssembly](https://cseweb.ucsd.edu/~dstefan/pubs/disselkoen:2019:ms-wasm.pdf)