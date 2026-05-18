---
title: "Memory Management"
description: "Research substrate for Mochi MEP-41 (May 2026). A 57-file deep dive into memory-safety advances from 2023 to mid-2026: capability hardware, generational references, ownership systems, runtime techniques, formal verification, and industry policy (CISA / NSA / ONCD)."
tags: ["memory-safety", "research", "mep-41"]
weight: 1
cascade:
  type: docs
date: 2026-05-18T17:00:00+07:00
---

Background research for [Mochi MEP-41](https://mochi-lang.dev/docs/mep/mep-0041): the memory-safety positioning that frames Mochi's vm3 runtime as a Vale generational reference machine, an MSWasm capability ABI, and a kalloc_type / xzone typed allocator, all under one roof.

Each subsection drills into one thread of the 2023-2026 memory-safety landscape. Every file has a §1 Provenance with canonical URLs, a §2 Mechanism, a §3 status as of May 2026, an engineering-cost section, a Mochi adaptation note, and §7 open questions.

## Sections

1. [Overview](overview/) — the 12-thread sweep across hardware, runtime, ownership, verification, and industry policy.
2. [Hardware](hardware/) — CHERI, Morello, CHERIoT 1.0, MTE, Apple MIE (iPhone 17, Sept 2025), PAC/BTI, Intel CET, MarkUs, Scudo.
3. [Ownership](ownership/) — Rust+Polonius, Vale, Hylo, Mojo, Austral, Pony, Verona, Swift, OxCaml, Linear Haskell, Scala 3, Inko.
4. [Runtime](runtime/) — Perceus, Roc, Lobster, ZGC, MMTk LXR, JSC Riptide, V8 Oilpan, V8 Sandbox, MSWasm, WasmGC, JIT hardening.
5. [Verification](verification/) — RustBelt/Iris, Verus, Creusot, Kani, Aeneas, CompCert, CakeML, capability-machine logics.
6. [Industry](industry/) — Microsoft 70%, Google/Android Rust crossover, CISA Secure-by-Design (Jan 2026 deadline), NSA CSI, ONCD, DoD SWFT, EU CRA.
