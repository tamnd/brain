---
title: "gopy vm overview"
description: "Top-level overview of the gopy VM (Tier-1 bytecode interpreter) port. Covers ceval, ceval_macros, ceval_gil, frame, stackrefs, and the bytecodes DSL output. Lives in the 1630-1639 block."
tags: ["gopy", "spec"]
weight: 1630
---

# 1630. gopy: Porting CPython's Tier-1 interpreter to Go

## Goal

The 1630-1639 block covers the port of CPython's Tier-1 bytecode
interpreter: `ceval.c`, `ceval_macros.h`, `ceval_gil.c`, `frame.c`,
`stackrefs.c`, plus the bytecode generator output that lives at
`Python/generated_cases.c.h` (regenerated from `Python/bytecodes.c`).
About 35k lines of C across the runtime files plus another ~30k in
the generated dispatch table.

The output of this block is a Go function

```go
vm.Eval(state.Thread, *frame.Frame) (object.Object, error)
```

that takes a frame and runs its code object to completion (or to a
yield, await, or unhandled exception).

Same rule as the rest of 1600: 100% behavioural compatibility with
CPython 3.14. Same opcodes, same oparg encoding, same exception
table semantics, same eval-breaker behaviour, same trace event
ordering. Only naming and surface API style move to Go conventions.

## Why this block exists

v0.5.5 ships a full parser plus the v0.5 compile pipeline. We can
turn source into a `*objects.Code` today, but the code object has no
runtime. v0.6 gives it one: a switch-dispatched bytecode loop that
matches CPython opcode-for-opcode.

Specialization (PEP 659), the Tier-2 trace optimizer, JIT, and the
PEP 669 monitoring hooks are deliberately deferred. v0.6 ships the
unspecialized interpreter. The specializer's adaptive variant
opcodes are present in the dispatch table but reduce to their
unspecialized base case (`LOAD_ATTR_INSTANCE_VALUE` falls back to
`LOAD_ATTR`). Monitoring callouts are stubbed to no-ops. This keeps
the v0.6 surface narrow enough to land cleanly while leaving the
extension points open for v0.11+.

## Sources of truth

| Concern                          | Source                                         |
|----------------------------------|------------------------------------------------|
| Bytecode ISA (DSL)               | `Python/bytecodes.c`                           |
| Generated dispatch handlers      | `Python/generated_cases.c.h` (from DSL)        |
| Computed-goto target table       | `Python/opcode_targets.h`                      |
| Eval loop entry, unwind, trampoline | `Python/ceval.c`                            |
| Dispatch macros, stack helpers   | `Python/ceval_macros.h`                        |
| GIL acquire/release, eval breaker | `Python/ceval_gil.c`                          |
| Frame layout, push/pop, locals   | `Python/frame.c`                               |
| Tagged stack reference values    | `Python/stackrefs.c`                           |
| Intrinsic dispatch (INTRINSIC_1/2) | `Python/intrinsics.c`                        |
| Opcode constants and metadata    | `Include/internal/pycore_opcode_metadata.h`    |
| Stack effect tables              | `Include/internal/pycore_uop_metadata.h`       |

## Spec files in this block

| #    | File                                | Focus                                                  | Phase |
|------|-------------------------------------|--------------------------------------------------------|-------|
| 1621 | `1621_gopy_bytecodes_dsl.md`        | bytecodes.c DSL parser and Go-emitting generator       | v0.6  |
| 1630 | `1630_gopy_vm_overview.md`          | This file                                              | meta  |
| 1635 | `1635_gopy_intrinsics.md`           | intrinsics.c (INTRINSIC_1 / INTRINSIC_2 dispatch)      | v0.6  |
| 1636 | `1636_gopy_eval_loop.md`            | ceval.c, ceval_macros.h, opcode dispatch loop          | v0.6  |
| 1637 | `1637_gopy_frame.md`                | frame.c, frame layout, locals, push/pop, generator state | v0.6 |
| 1638 | `1638_gopy_stackref.md`             | stackrefs.c, tagged stack values, borrow tracking      | v0.6  |
| 1639 | `1639_gopy_eval_gil.md`             | ceval_gil.c, GIL, eval breaker, signal pending bits    | v0.6  |

Cross-block dependencies:

* 1684 (`call.c`, vectorcall) lands alongside the eval loop.
  CALL / CALL_FUNCTION_EX / CALL_KW go through vectorcall; without
  it the interpreter cannot invoke functions.
* 1687 (codeobject, frameobject, genobject, cellobject) lands
  alongside the eval loop. Frame storage and code metadata are the
  inputs the eval loop reads.
* 1685 (descrobject, methodobject, funcobject) supplies the
  callable object types CALL dispatches into.

These three are tracked in the Objects block (1670-1689) and gate
v0.6 on the object side.

## Phasing

| Phase  | Specs that ship                                                |
|--------|----------------------------------------------------------------|
| v0.6.0 | 1621, 1630, 1635, 1636, 1637, 1638, 1639                       |
| v0.6.1 | bug fix and golden refresh; no new specs                       |

v0.6.0 is the interpreter handover release. After it lands,
`gopy -c "print(1+2)"` runs end-to-end through Parse, Compile, and
Eval, and produces the literal string `3\n` on stdout.

## Compatibility floors

Items that gate the VM block:

1. Opcode numeric values match
   `Include/internal/pycore_opcode_metadata.h` one-to-one. Pinned
   by `vm/opcodes_gen_test.go`.
2. Stack effects per opcode match the generator output. Pinned by
   `vm/stack_effects_test.go`.
3. Exception table walk produces the same handler entry CPython
   would, for every entry in the v0.5 disassembly golden corpus.
   Pinned by `vm/exception_table_test.go`.
4. Line-number table walk produces the same `co_positions` tuple
   CPython does for every bytecode offset. Pinned by
   `vm/positions_test.go`.
5. Eval-breaker bits fire on the same instruction boundaries
   CPython fires them on. Pinned by `vm/eval_breaker_test.go`.
6. Generator / coroutine state transitions (`SEND`, `YIELD_VALUE`,
   `RESUME`, `RETURN_GENERATOR`) match CPython's frame-resume
   semantics. Pinned by `vm/gen_state_test.go`.

## Test strategy

`vmtest/` carries the cross-cut gate per phase:

* v0.6.0: `TestGateEvalArith`, `TestGateEvalCall`,
  `TestGateEvalIfElse`, `TestGateEvalLoop`,
  `TestGateEvalException`, `TestGateEvalGenerator`,
  `TestGateEvalAsync` round-trip source through
  `parser.ParseString`, `compile.Compile`, `vm.Eval` and assert
  the printed output (or the raised exception type plus message)
  matches CPython byte-for-byte.
* `vmtest/dis_parity` runs the v0.5 disassembly golden corpus
  through Eval and pins the trace event sequence (instruction
  offsets visited, locals at each `RESUME`) against a CPython
  reference run.
* `vmtest/cpython_smoke_test.go` runs a curated panel of expressions
  through `python3 -c "print(<src>)"` and through the gopy
  parser->compile->eval pipeline, asserting the rendered top-level
  value matches byte-for-byte. Cases skip when the gopy panel still
  has a known v0.6 gap (parser rule body not yet emitted, str + str
  not yet wired). Future v0.7 work expands this to the
  `test_grammar`, `test_compile`, `test_exceptions`,
  `test_generators` source files once the parser action emitter
  closes its remaining holes.

Each per-file spec carries its own per-file tests; this overview
only lists the cross-cut gates.

## Block-level checklist

Status: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Cross-cut artefacts

* [x] `vm/` package skeleton: `Eval`, `EvalCode` entry points
  in `vm/eval.go`; `evalState` for per-call state; thread-state
  hookup via `vm/threadstate.go`.
* [x] `vmtest/` v0.6 gate harness: `vmtest/gate_test.go` panel
  (Constant, Arithmetic, IfElse, ListBuild, FString) plus
  `vmtest/smoke_test.go::TestSmokeReleaseV06`. The
  `gopy -c "print(1+2)"` release gate prints `3` end-to-end.
* [ ] `vmtest/cpython_smoke`: curated CPython test panel
  (`test_grammar`, `test_compile`, `test_exceptions`,
  `test_generators`) running under gopy with a known-failure list.

### Per-spec progress (one row per sub-spec)

| Spec | Status | Notes                                                |
|------|--------|------------------------------------------------------|
| 1621 | [~]    | DSL parser shipped, action translator partial       |
| 1630 | [~]    | this overview, cpython_smoke pending                |
| 1635 | [x]    | tables shipped, helpers stubbed for prereqs         |
| 1636 | [~]    | eval loop + most opcodes shipped, gen/async pending |
| 1637 | [x]    | frame struct + chunk + suspend/resume + clear       |
| 1638 | [x]    | stackref + sentinels (Sizeof pin pending)           |
| 1639 | [x]    | GIL + breaker + pending + signal bridge             |

### Cross-block gates (Objects side)

* [x] 1684 `call.go` vectorcall protocol shipped (CALL / CALL_KW
  / CALL_FUNCTION_EX go through it). Pinned by task #191 and
  the call panel in `vm/eval_simple.go`.
* [~] 1685 `funcobject.go`, `methodobject.go`, `descrobject.go`:
  Function and methodobject ported (#191); `descrobject.go`
  pending. Method-resolution / `LOAD_SUPER_ATTR` blocks on the
  descrobject port.
* [~] 1687 `codeobject.go`: `objects.Code` carries `Stacksize`,
  `Varnames`, `Cellvars`, `Freevars`, `Consts`, `Names`,
  `Code`, `ExceptionTable`. The named accessors (`NLocalsPlus`,
  `NLocals`, `NCells`, `NFree`) live as helpers on the frame
  side. `frameobject.go`, `genobject.go`, `cellobject.go` are
  pending; the eval-side suspend/resume is already wired.

### Tooling

* [x] `tools/bytecodes_gen`: Go-targeted regenerator for
  `vm/opcodes_gen.go` from `Python/bytecodes.c`. Records a
  `bytecodes-sha256` header so a CPython rebase that skips
  regeneration fails CI. Drift check pinned by `drift_test.go`.
  Detail in 1621.

## Out of scope

* `Python/specialize.c`: PEP 659 adaptive specialization. Lives in
  1631 at v0.11.
* `Python/optimizer*.c`: Tier-2 trace projector and abstract
  interpreter. Lives in 1632 at v0.12.
* `Python/jit.c`: copy-and-patch JIT. Lives in 1633, indefinitely
  deferred.
* `Python/instrumentation.c`, `Python/legacy_tracing.c`: PEP 669
  monitoring and `sys.settrace`/`sys.setprofile`. Lives in 1634 at
  v0.9.
* Free-threaded eval loop paths. Lives in v0.14.
