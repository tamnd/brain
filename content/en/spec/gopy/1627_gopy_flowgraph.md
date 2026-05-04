---
title: "gopy flowgraph"
description: "Detailed port plan for cpython/Python/flowgraph.c (~4200 lines) to compile/flowgraph.go. CFG construction, optimization passes (jump threading, dead-code, const fold, swaptimize, super-instructions), stackdepth, exception handler labelling, comprehensive test plan."
tags: ["gopy", "spec"]
weight: 1627
---

# 1627. Flowgraph

Port of `cpython/Python/flowgraph.c` (4165 lines) to
`gopy/compile/flowgraph.go`. This spec is the detailed source-of-truth
for section 7 of 1620.

## What flowgraph does

Flowgraph takes a flat `instrseq.Sequence` from codegen (1626),
converts it to a control-flow graph of basic blocks, runs ~25
optimisation and bookkeeping passes over the graph, and converts the
graph back to a Sequence ready for assembly (1628).

The optimisations are *not* peephole only. Jump threading, dead block
elimination, const folding, super-instruction selection, exception
handler labelling, and stackdepth verification all run here. CPython
runs these in one fixed order; the Go port matches that order
line-for-line.

Boundary contract:

```
Input:
  *instrseq.Sequence (flat list of pseudo-instructions plus labels)
  consts []any        (the constants pool the codegen built)
  nlocals int         (the function's local count)
  firstlineno int

Output:
  *instrseq.Sequence (same shape, but labels resolved, NOPs gone,
                      pseudo-ops lowered, super-instructions fused,
                      stackdepth annotated, exception targets set)
  *flowgraphInfo {
      MaxStackDepth int
      ExceptionTable []ExceptHandlerEntry
      Consts []any        (possibly trimmed by remove_unused_consts)
      Localsplus int      (cellvars + freevars + nlocals)
  }
```

## File layout

`compile/flowgraph.go` is too large for one file. Split mirroring the
visitor split in symtable and codegen:

| Go file                       | CPython lines  | Contents                                                  |
|-------------------------------|----------------|-----------------------------------------------------------|
| `flowgraph.go`                | 1-460          | `BasicBlock`, `Instr`, `Builder` types and helpers, public entry points |
| `flowgraph_build.go`          | 460-665        | `FromSequence`, `ToSequence`, `JumpLabelsToTargets`       |
| `flowgraph_check.go`          | 503-620        | `noRedundantNops`, `noRedundantJumps`, `checkCfg`         |
| `flowgraph_normalize.go`      | 535-602        | `normalizeJumps`, `normalizeJumpsInBlock`                 |
| `flowgraph_excepthandler.go`  | 668-994        | `markExceptHandlers`, `labelExceptionTargets`, except-stack panel |
| `flowgraph_stackdepth.go`     | 768-885        | `getStackEffects`, `calculateStackdepth`                  |
| `flowgraph_unreachable.go`    | 996-1158       | `removeUnreachable`, `removeRedundantNops*`, `removeRedundantJumps` |
| `flowgraph_inline.go`         | 1192-1262      | `basicblockInlineSmallOrNoLinenoBlocks`                   |
| `flowgraph_jumpthread.go`     | 1264-1290      | `jumpThread`                                              |
| `flowgraph_constfold.go`      | 1287-1980      | `loadsConst`, `getConstValue`, `addConst`, fold panels    |
| `flowgraph_swaptimize.go`     | 1981-2167      | `swaptimize`, `applyStaticSwaps`                          |
| `flowgraph_optblock.go`       | 2169-2528      | `basicblockOptimizeLoadConst`, `optimizeBasicBlock`       |
| `flowgraph_optcfg.go`         | 2529-2570      | `optimizeCfg`, `removeRedundantNopsAndJumps`              |
| `flowgraph_super.go`          | 2572-2635      | `makeSuperInstruction`, `insertSuperinstructions`         |
| `flowgraph_loadfast.go`       | 2637-3060      | `optimizeLoadFast`, ref stack panel                       |
| `flowgraph_locals.go`         | 3062-3320      | `scanBlockForLocals`, `fastScanManyLocals`, uninitialized-load checks |
| `flowgraph_consts.go`         | 3174-3270      | `removeUnusedConsts`                                      |
| `flowgraph_temp.go`           | 3323-3485      | `markWarm`, `markCold`, `pushColdBlocksToEnd`             |
| `flowgraph_pseudo.go`         | 3485-3640      | `convertPseudoConditionalJumps`, `convertPseudoOps`, `duplicateExitsWithoutLineno` |
| `flowgraph_optimize.go`       | 3659-4126      | top-level `OptimizeCodeUnit` driver                       |

Each function gets `// CPython: flowgraph.c:L<n> <name>`.

## Public surface

```go
package compile

// Optimize runs every flowgraph pass on a Sequence in the same order
// as cpython/Python/flowgraph.c:_PyCfg_OptimizeCodeUnit.
func Optimize(seq *instrseq.Sequence, consts *[]any, nlocals, firstlineno int) (*Info, error)

// FromSequence builds a CFG from a flat instruction sequence.
func FromSequence(seq *instrseq.Sequence) (*Builder, error)

// ToSequence flattens a CFG back to a Sequence.
func (b *Builder) ToSequence() (*instrseq.Sequence, error)

// Info is the per-pass metadata the assembler consumes.
type Info struct {
    MaxStackDepth  int
    ExceptionTable []ExceptHandler
    Consts         []any
    LocalsPlus     int
    NLocals        int
    NCellvars      int
    NFreevars      int
}

type ExceptHandler struct {
    Start, End, Target int  // bytecode offsets, filled by 1628
    Depth              int  // stack depth at handler entry
    Lasti              bool // CO_FAST_HIDDEN handler bit
}

type BasicBlock struct {
    Instrs   []Instr
    Next     *BasicBlock // fall-through
    Label    int
    StartDepth int       // -1 until calculateStackdepth runs
    Predecessors int
    Visited  bool
    Cold     bool        // mark_cold output
    Warm     bool        // mark_warm output
    ExceptHandler bool
    Reachable bool
}

type Instr struct {
    Opcode  int
    Oparg   int
    Loc     ast.Pos
    Target  *BasicBlock // if has_jump
    ExceptStack *ExceptStack
}
```

## CFG construction

`FromSequence` walks the flat instruction list, splits at every label
target, and returns a doubly-linked list of basic blocks.

Algorithm (flowgraph.c:3923-3987):

1. Pre-scan to find every label target. Each becomes a block boundary.
2. Each block ends at the next label, or at a terminator
   (RETURN_VALUE / RAISE_VARARGS / RERAISE / unconditional JUMP).
3. Conditional jumps and unconditional jumps record a Target pointer.
4. Fall-through is the `Next` link.
5. The first block is the entry block; flowgraph never reorders it.

`ToSequence` (flowgraph.c:3988-4025) walks blocks in stored order,
emits each instruction, inserts `JUMP_FORWARD` for fall-through gaps
that the optimiser opened, and resolves Target pointers to label IDs.

## Pass order

Mirror `_PyCfg_OptimizeCodeUnit` exactly. Document each pass with a
`// PASS N: <name>` block in `flowgraph_optimize.go`.

```go
func Optimize(seq *instrseq.Sequence, consts *[]any, nlocals, firstlineno int) (*Info, error) {
    g, err := FromSequence(seq)
    if err != nil { return nil, err }

    // PASS 1: translate symbolic jump labels to block targets.
    if err := g.translateJumpLabelsToTargets(); err != nil { return nil, err }

    // PASS 2: mark exception handler entry blocks (SETUP_FINALLY etc.).
    if err := g.markExceptHandlers(); err != nil { return nil, err }

    // PASS 3: label every block with its exception target.
    if err := g.labelExceptionTargets(); err != nil { return nil, err }

    // PASS 4: convert pseudo conditional jumps to real CONDOP forms.
    if err := g.convertPseudoConditionalJumps(); err != nil { return nil, err }

    // PASS 5: optimise. Iterates per-block until no more changes.
    if err := g.optimizeCfg(consts, nlocals); err != nil { return nil, err }

    // PASS 6: fast-paths for unused consts and uninitialised loads.
    if err := g.removeUnusedConsts(consts); err != nil { return nil, err }
    if err := g.addChecksForLoadsOfUninitializedVariables(nlocals); err != nil { return nil, err }

    // PASS 7: insert super-instructions (LOAD_FAST_LOAD_FAST etc.).
    if err := g.insertSuperinstructions(); err != nil { return nil, err }

    // PASS 8: lower remaining pseudo-ops to real opcodes.
    if err := g.convertPseudoOps(); err != nil { return nil, err }

    // PASS 9: cold-block hoist (push cold paths to function end).
    if err := g.pushColdBlocksToEnd(); err != nil { return nil, err }

    // PASS 10: ensure every exit block has a lineno.
    if err := g.duplicateExitsWithoutLineno(); err != nil { return nil, err }

    // PASS 11: stackdepth analysis.
    info := &Info{}
    info.MaxStackDepth, err = g.calculateStackdepth()
    if err != nil { return nil, err }

    // PASS 12: rebuild the sequence.
    out, err := g.ToSequence()
    if err != nil { return nil, err }
    *seq = *out
    return info, nil
}
```

`optimizeCfg` is itself a fixed-point loop (flowgraph.c:2552-2570):

```
do:
  for each block:
    optimizeBasicBlock(block, consts, nlocals)   // const fold, jump thread,
                                                  // swaptimize, load_fast opt
  remove_unreachable
  remove_redundant_nops_and_jumps
  inline_small_or_no_lineno_blocks
while changed
```

## Optimisation panel coverage

Each entry below is one Go function, one CPython line range, one test
file under `compile/flowgraph_*_test.go`.

- [ ] `translateJumpLabelsToTargets` (635-666): every label resolves to a block; orphan labels error.
- [ ] `markExceptHandlers` (668-691): SETUP_* and CLEANUP_* set `ExceptHandler` bit.
- [ ] `labelExceptionTargets` (886-994): each instruction records the topmost active handler.
- [ ] `pushExceptBlock` / `popExceptBlock` / `exceptStackTop` (693-715): except-stack lifecycle.
- [ ] `getStackEffects` (768-790): every opcode's stack effect; mirrored from `opcode_metadata` table.
- [ ] `calculateStackdepth` (809-884): forward dataflow on stack height; rejects negative depth.
- [ ] `removeUnreachable` (996-1042): blocks with `Predecessors == 0` are deleted (except entry).
- [ ] `basicblockRemoveRedundantNops` (1044-1102): drop NOPs unless used for line-number anchoring.
- [ ] `removeRedundantJumps` (1158-1191): jump-to-next-block becomes nothing.
- [ ] `basicblockInlineSmallOrNoLinenoBlocks` (1210-1262): merge tiny successors with sole-predecessor relation.
- [ ] `jumpThread` (1264-1286): `JUMP A; A: JUMP B` becomes `JUMP B`.
- [ ] `loadsConst` / `getConstValue` (1287-1322): identify LOAD_CONST family.
- [ ] `addConst` (1323-1365): dedup constants via const_cache (a Go `map[any]int` keyed by EqualConst rule).
- [ ] `foldTupleOfConstants` (1454-1507): `LOAD_CONST a; LOAD_CONST b; BUILD_TUPLE 2` collapses.
- [ ] `foldConstantIntrinsicListToTuple` (1509-1597): list intrinsic + LIST_TO_TUPLE collapses.
- [ ] `optimizeListsAndSets` (1598-1673): all-const list/set literal becomes a frozen LOAD_CONST.
- [ ] `evalConstBinop` / `foldConstBinop` (1791-1893): const folding of safe binops only (1675-1789 are the safety predicates).
- [ ] `evalConstUnaryop` / `foldConstUnaryop` (1894-1980): same for unary.
- [ ] `swaptimize` (1981-2092): cancel sequences of SWAP that are no-ops.
- [ ] `applyStaticSwaps` (2117-2167): commute SWAP through known-pure ops.
- [ ] `basicblockOptimizeLoadConst` (2169-2300): per-block constant optimisation.
- [ ] `optimizeBasicBlock` (2311-2528): the per-block driver.
- [ ] `removeRedundantNopsAndJumps` (2529-2551): post-pass cleanup.
- [ ] `makeSuperInstruction` / `insertSuperinstructions` (2572-2635): LOAD_FAST_LOAD_FAST, STORE_FAST_LOAD_FAST, etc.
- [ ] `optimizeLoadFast` (2637-3060): full ref-stack analysis to choose `LOAD_FAST_BORROW`.
- [ ] `scanBlockForLocals` / `fastScanManyLocals` (3062-3173): bitmask of locals that may be uninitialised.
- [ ] `removeUnusedConsts` (3174-3270): trim the consts list.
- [ ] `addChecksForLoadsOfUninitializedVariables` (3273-3320): emit LOAD_FAST_CHECK where required.
- [ ] `markWarm` / `markCold` (3323-3402): cold-path detection.
- [ ] `pushColdBlocksToEnd` (3404-3484): cold blocks hoist below the warm body.
- [ ] `convertPseudoConditionalJumps` (3485-3519): POP_JUMP_IF_FALSE_OR_POP etc.
- [ ] `convertPseudoOps` (3520-3542): RESUME pseudo, LOAD_BUILD_CLASS pseudo, etc.
- [ ] `duplicateExitsWithoutLineno` (3563-3640): every RETURN_VALUE block has a lineno.

## Const cache

CPython uses a `PyDict` keyed by a tuple `(type(obj), <serialised
contents>)`. The Go port uses:

```go
type constKey struct {
    Tag  string  // "int", "float", "str", "bytes", "tuple", "frozenset", "complex", ...
    Hash uint64  // FNV of repr; collisions resolved by a slice of (key, idx)
}

type constCache struct {
    keys []constKey
    vals []int        // index into the consts pool
    objs []any        // backing values (for collision compare)
}
```

`addConst` returns the index. Equality follows
`compile.c:compiler_add_const`'s rules:

- ints: identical numeric value
- floats: identical bit pattern (so `+0.0 != -0.0` and `NaN == NaN` only when bits match)
- strings: identical bytes
- bytes: identical bytes
- tuples / frozensets: recursively
- code objects: never deduped

Test panel: `compile/flowgraph_constcache_test.go`.

## Stack effects table

`getStackEffects` is hand-written from the metadata table. The
opcodes generator (1620 section 4) already produces the static table
from `pycore_opcode_metadata.h`; flowgraph imports it via:

```go
import "github.com/tamnd/gopy/compile/internal/opmeta" // generated
// effects, jumpEffects := opmeta.StackEffects(opcode, oparg)
```

Note: keep the table generation co-located with the opcodes generator,
not flowgraph. Flowgraph only consumes.

## Comprehensive test plan

Tests live in `compile/flowgraph_*_test.go`. Layered like 1626 codegen
testing.

### Layer 1: Per-pass unit

For every pass listed in "Pass order" and every entry in the
"Optimisation panel coverage" list, ship a unit test that:

1. Builds a small CFG by hand (programmatic basicblock construction).
2. Runs the single pass under test.
3. Asserts the post-pass CFG state via `dumpGraph` text equality.

Example skeleton:

```go
func TestRemoveUnreachable(t *testing.T) {
    // entry -> A -> RETURN_VALUE
    //              B is orphan
    g := buildCfg(t,
        block("entry").jump("A"),
        block("A").nop().ret(),
        block("B").nop().ret(),
    )
    if err := g.removeUnreachable(); err != nil { t.Fatal(err) }
    assertBlocks(t, g, []string{"entry", "A"})
}
```

Required tests (one per checkbox above): 31 unit tests for the panel,
plus 12 driver tests for each pass step in `Optimize`.

### Layer 2: Round-trip vs Sequence

For every test in `compile/codegen_*_test.go` (Layer 1 of 1626), build
the Sequence, call `Optimize`, and assert:

- The Sequence is well-formed (every label resolves, no leaked NOPs
  except line anchors).
- `Info.MaxStackDepth` matches CPython's `co_stacksize` for the
  equivalent Python source.

### Layer 3: Cross-check vs CPython

Tagged `//go:build cpython`. Compile a corpus of ~120 hand-picked
Python snippets in CPython 3.14 and gopy. Assert:

- `dis.dis(co).getvalue()` is identical (except for memory addresses).
- `co.co_stacksize` is identical.
- `co.co_lnotab` / `co.co_linetable` is identical.
- `co.co_exceptiontable` is identical.

The corpus lives at `compile/testdata/parity_corpus/*.py` and is the
same corpus that 1628 (assemble) uses for marshal-parity.

### Layer 4: Fuzz

`compile/flowgraph_fuzz_test.go` builds random valid Sequences (random
opcodes obeying the stack-effect table) and asserts `Optimize` is
idempotent: running it twice produces the same output.

## Lint and refactor budget

The flowgraph passes are notoriously branchy. Functions over 30
cognitive complexity that need pre-emptive splitting:

- `optimizeBasicBlock` (200 lines, dozens of cases): split into per-op
  helpers (`optBasicBlockJump`, `optBasicBlockBuildOp`, `optBasicBlockConstFamily`, ...).
- `optimizeLoadFast` (400+ lines, deep nesting): split into
  `loadFastInitRefs`, `loadFastVisitInstr` (per opcode group),
  `loadFastFinalizeBlock`.
- `addChecksForLoadsOfUninitializedVariables` (50 lines, three
  intertwined loops): split scan / propagate / emit phases.
- `eval_const_binop` / `eval_const_unaryop`: one helper per safe
  operator; the dispatcher just routes.

Use the same naming policy as symtable: verbs that describe the work,
not "Step1" / "Helper". Each split helper carries `// CPython:
flowgraph.c:L<n> <orig> (extracted helper)`.

## Citation policy

Same as 1626. Every Go function gets `// CPython: flowgraph.c:L<n>
<name>`. Helpers split for lint carry `(extracted helper)`.

## Order of work

1. Skeleton: types, FromSequence, ToSequence, public Optimize that
   runs nothing.
2. translateJumpLabelsToTargets, removeUnreachable, basic round-trip
   test.
3. calculateStackdepth (lots of tests; gates everything else).
4. markExceptHandlers, labelExceptionTargets.
5. removeRedundantNops, removeRedundantJumps,
   basicblockInlineSmallOrNoLinenoBlocks.
6. jumpThread.
7. Const fold panel: addConst, foldTupleOfConstants,
   foldConstantIntrinsicListToTuple, optimizeListsAndSets,
   evalConstBinop, evalConstUnaryop.
8. swaptimize, applyStaticSwaps.
9. optimizeBasicBlock + optimizeCfg fixed-point loop.
10. removeUnusedConsts, addChecksForLoadsOfUninitializedVariables.
11. insertSuperinstructions.
12. optimizeLoadFast (largest single port).
13. markWarm/markCold/pushColdBlocksToEnd.
14. convertPseudoConditionalJumps, convertPseudoOps,
    duplicateExitsWithoutLineno.
15. Final OptimizeCodeUnit driver.

Each step lands as one PR. Flowgraph is "done" when Layer 2 round-trip
passes for every codegen test and Layer 3 cross-check passes for the
parity corpus.
