---
title: "gopy compile golden tests"
description: "Disassembly-golden corpus for the v05test gate. Each fixture is a Go-built AST plus a checked-in .golden file with the expected dis.dis output. Refresh via `go test -update`."
tags: ["gopy", "spec"]
weight: 1629
---

# 1629. Compile golden tests

This spec lives next to 1625 (the broad v0.5 testing strategy) but
narrows to one thing: the disassembly-golden corpus that pins the
output of the full compile pipeline (`symtable -> codegen -> flowgraph
-> assemble`) for a curated panel of programs.

The marshal-byte parity gate against host CPython lands in v0.8 with
the import system. Until then the disassembly text *is* the gate: it
captures opcode names, opargs (after EXTENDED_ARG recombination),
nested code objects, and emit order. A change in any of those flips
the diff.

## Why disassembly text, not marshal bytes

* Marshal-equivalent bytes need a code-object encoder that mirrors
  CPython's `w_object` PyCode arm. That arm depends on TYPE_LONG for
  `co_firstlineno` etc., on the REF de-dup table, on tuple/frozenset
  parity for `co_consts`, and on the line/exception tables already
  matching byte-for-byte. Each piece is a separate v0.8 follow-on.
* Disassembly text round-trips through `compile.Disassemble`, which
  is the same surface a future `dis.dis` will sit behind. Locking it
  now means we catch drift in opcode emission, oparg widening, and
  nested-code traversal before the marshal layer arrives.
* We have no parser. Every fixture builds its AST in Go, which keeps
  the corpus self-contained: a fixture that wants to exercise a
  syntax form spells the AST literally, no `python -c` round-trip.

## Layout

```
v05test/
├── gate_test.go          # structural panel (unchanged)
├── golden_test.go        # the runner described here
└── testdata/
    └── golden/
        ├── empty_module.golden
        ├── simple_assign.golden
        ├── binary_add.golden
        ├── load_after_store.golden
        ├── if_pass.golden
        ├── while_pass.golden
        ├── def_add_one.golden
        ├── async_def_pass.golden
        ├── class_pass.golden
        └── type_alias.golden
```

Each `.golden` file is the literal output of `compile.Disassemble`
on the fixture's compiled module.  The runner reads the file at test
time and compares with `==`. A mismatch dumps the unified diff.

## Refresh contract

`go test ./v05test/ -update -run TestGolden` rewrites every golden
in place. The `-update` flag is a `flag.Bool` registered by the test
file via `flag.Bool("update", false, ...)`. There is no separate
generator binary: the test *is* the generator.

The expected workflow is:

1. Edit codegen / flowgraph / assemble.
2. Run the gate. If a golden diffs, inspect the diff and decide:
   either the change is intended (re-run with `-update`) or
   unintended (fix the code).
3. Commit the .go change and the regenerated .golden in the same
   commit so future bisects line up.

## Fixture rules

* **Self-contained AST**: each fixture is a Go function that returns
  a `*ast.Module` built from the helpers already in `gate_test.go`
  (`module`, `nameLoad`, `nameStore`, `cnst`, `findInnerCode`).
* **No parser**: never call out to the host CPython, never read a
  `.py` source file. The test must run on a hermetic builder.
* **One concept per fixture**: an `if` fixture exercises only `if`;
  a `def` fixture only `def`. Compounding hides regressions.
* **Stable across cosmetic refactors**: a fixture that assigns
  `x = 1` does not also store the int constant 0 to `__doc__` or
  pull in import machinery. The corpus minimises noise so a real
  bytecode delta shows up clean in the diff.

## Panel

Every entry below is one .golden file. The leftmost column is the
filename stem; the source column is the literal Python the AST
spells.

| Stem                | Source                              | Pins                              |
|---------------------|-------------------------------------|-----------------------------------|
| `empty_module`      | (empty)                             | implicit `LOAD_CONST None / RETURN_VALUE` trailer |
| `simple_assign`     | `x = 1`                             | `LOAD_CONST` + `STORE_NAME`       |
| `binary_add`        | `a = 1 + 2`                         | flowgraph int-int fold to constant 3 |
| `load_after_store`  | `x = 1\nx`                          | `STORE_NAME` then `LOAD_NAME` round-trip |
| `if_pass`           | `if x: pass`                        | `POP_JUMP_IF_FALSE` shape         |
| `while_pass`        | `while x: pass`                     | back-edge JUMP threading          |
| `def_add_one`       | `def f(x): return x + 1`            | nested code in Consts, MAKE_FUNCTION + LOAD_FAST |
| `async_def_pass`    | `async def f(): pass`               | CoCoroutine on the inner Code     |
| `class_pass`        | `class C: pass`                     | LOAD_BUILD_CLASS + CALL count     |
| `type_alias`        | `type X = int`                      | INTRINSIC_TYPEALIAS argument      |

Two fixtures are deferred behind the same gap that holds the structural
panel back (`TestGateTryExcept`, `TestGateComprehension`): the linear
stack-depth analyser cannot seed handler entry from an exception edge
or comprehension back-edge. Both fixtures land here once the CFG-based
analyser ships.

## Test-runner shape

```go
//go:generate go test -update -run TestGolden ./...

var update = flag.Bool("update", false,
    "rewrite v05test/testdata/golden/*.golden files in place")

type goldenCase struct {
    name string
    mod  *ast.Module
}

func goldenPanel() []goldenCase { /* the table above */ }

func TestGolden(t *testing.T) {
    for _, tc := range goldenPanel() {
        t.Run(tc.name, func(t *testing.T) {
            co, err := compile.Compile(tc.mod, "<gate>", 0)
            if err != nil {
                t.Fatalf("Compile: %v", err)
            }
            got := compile.Disassemble(co)
            path := filepath.Join("testdata", "golden", tc.name+".golden")
            if *update {
                if err := os.WriteFile(path, []byte(got), 0o644); err != nil {
                    t.Fatal(err)
                }
                return
            }
            want, err := os.ReadFile(path)
            if err != nil {
                t.Fatalf("read %s: %v (run with -update to create)", path, err)
            }
            if got != string(want) {
                t.Fatalf("disassembly diff for %s:\n--- want\n%s\n+++ got\n%s",
                    tc.name, want, got)
            }
        })
    }
}
```

Two things to note about the shape:

* **One test, many subtests**: `t.Run` per fixture gives readable
  per-fixture pass/fail without a per-fixture `_test.go` file.
* **`-update` writes everything**: a single command refreshes all
  goldens after a deliberate codegen change. No flag means strict
  compare; CI never has `-update` in its argv.

## CI integration

The existing `test` job runs `go test -race -count=1 ./...` which
includes the golden runner. CI does not pass `-update`, so any
unmerged code change that flips bytecode flags the gate.

The `lint` job runs `golangci-lint run`. The runner has no special
needs there beyond the rest of the codebase.

## Gate

* [ ] `v05test/golden_test.go` runner with `-update`.
* [ ] All ten fixtures in the panel emit a checked-in .golden.
* [ ] `go test ./v05test/` is green without `-update`.
* [ ] `go test ./v05test/ -update` rewrites every .golden in one go
  and the result diffs to nothing immediately after.

## Out of scope for v0.5

* Marshal-byte parity against CPython. v0.8.
* Source-text fixtures. Pending the parser port.
* Negative goldens (compile errors): the panel is positive cases
  only. Error-message fixtures live alongside the validator panel
  in `ast/validate_panel_test.go`.
* Property tests over random ASTs. Would need a generator that
  respects symtable invariants; deferred.
