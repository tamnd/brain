---
title: "gopy pegen"
description: "Port of cpython/Parser/pegen.c and the generated cpython/Parser/parser.c. PEG runtime plus the parser table that turns a token stream into an AST."
tags: ["gopy", "spec"]
weight: 1642
---

# 1642. PEG runtime and generated parser

## What we are porting

The PEG parser is two files at runtime:

* `Parser/pegen.c`: the runtime. ~3500 lines. Memo cache, token
  buffer, error pinning, `_PyPegen_*` helpers used by the generated
  rules.
* `Parser/parser.c`: the generated parser. ~40k lines, regenerated
  from `Grammar/python.gram` by `Tools/peg_generator/`. Each rule
  is one C function returning an AST node or `NULL`.

`Parser/peg_api.c` is a thin public wrapper (`PyPegen_ASTFrom*`).

The generated `parser.c` is too large to hand-port; we run the
upstream generator (in Python) at build time and let it emit Go.

## Strategy

1. Hand-port `pegen.c` to `parser/pegen/`. Memo cache, token
   feeder, error sink, expect/expect_token/lookahead helpers.
2. Fork `Tools/peg_generator/` so it emits Go from the same
   `python.gram`. Output lands in `parser/pegen/parser_gen.go`.
   Keep the generator under `tools/parser_gen/` and check its
   output in (no runtime codegen).
3. Hand-port `peg_api.c` to a small `parser.Parse` driver that
   chooses the start rule from `Mode`.

The generator fork is the only divergence from "hand-port the C".
The grammar is too volatile (CPython tweaks it nearly every
release) and the generator already emits target-language-agnostic
PEG state machines.

## Go shape

```go
// Parser is the runtime mirror of struct Parser from pegen.h.
// Each generated rule takes *Parser and returns (ast.Node, bool).
type Parser struct {
    tokens []lexer.Tok
    pos    int
    memo   map[memoKey]memoEntry
    err    *SyntaxError
    arena  *arena.Arena
    flags  Flags
    mode   StartRule
    fill   func() error  // pull more tokens from the lexer
}

type memoKey struct {
    rule int  // rule id, dense small-int
    pos  int
}

type memoEntry struct {
    node ast.Node
    end  int  // position after the match, or pos for failure
    ok   bool
}
```

The memo cache is the heart of PEG. Every rule call is keyed by
`(rule_id, pos)`. The cache survives backtracking. CPython uses an
array-of-array indexed by rule then pos; Go uses a hash map for
simplicity. The hot path is the cache hit, which is one map lookup
either way.

## Token fill

`pegen.c:_PyPegen_fill_token` pulls the next token from the lexer
when the parser exceeds the buffered range. We translate to:

```go
func (p *Parser) fill() error {
    for p.pos >= len(p.tokens) {
        tok, err := p.next()
        if err != nil {
            return err
        }
        p.tokens = append(p.tokens, tok)
    }
    return nil
}
```

Same behaviour: lazy, unbounded buffer. The buffer never shrinks
because the memo cache references token indices.

## Error pinning

PEG errors fire on the deepest position any rule reached. CPython
tracks `p->error_indicator`, `p->level`, `p->call_invalid_rules`.
We mirror these on `Parser`:

```go
func (p *Parser) RaiseSyntaxError(msg string) ast.Node {
    if p.pos > p.err.farthestPos {
        p.err = &SyntaxError{Pos: p.tokens[p.pos].Start, Msg: msg}
    }
    return nil
}
```

The "farthest reached" rule wins. This is CPython's "last good
error" heuristic; without it, PEG errors point at the start of the
file.

## Generator

`tools/parser_gen/` is a Go-targeted fork of
`cpython/Tools/peg_generator/`. It reads `Grammar/python.gram` and
emits `parser/pegen/parser_gen.go` containing:

* `const Rule_<name> int = N` for each rule.
* A `func (p *Parser) <rule_name>() (ast.Node, bool)` per rule.
* A `func StartRule(p *Parser, m StartRule) (ast.Node, bool)` that
  dispatches on `Mode`.

The generator runs at `go generate` time, not at compile time. The
generated file is checked in.

## File mapping

| C source                  | Go target                                  |
|---------------------------|--------------------------------------------|
| `Parser/pegen.c`          | `parser/pegen/runtime.go`                  |
| `Parser/pegen.h`          | `parser/pegen/parser.go` (struct)          |
| `Parser/peg_api.c`        | `parser/parser.go` (`Parse`, `ParseString`) |
| `Parser/parser.c`         | `parser/pegen/parser_gen.go` (generated)   |
| `Tools/peg_generator/`    | `tools/parser_gen/` (forked, Go target)    |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `parser/pegen/parser.go`: `Parser` struct, `StartRule` enum,
  `Flags`, `New`.
* [x] `parser/pegen/runtime.go`: `expect_token`, `expect_forced`,
  `lookahead`, `lookahead_with_name`, `seq_count_dots`,
  `singleton_seq`, the helpers the generator emits calls to.
* [x] `parser/pegen/memo.go`: `memo_get`, `memo_put`, the cache.
* [x] `parser/pegen/fill.go`: lazy token pulling from the lexer.
* [x] `parser/pegen/errors.go`: `RaiseSyntaxError`,
  `RaiseSyntaxErrorKnownLocation`, error pinning, `farthestPos`.
* [x] `parser/pegen/parser_gen.go`: generated. ~19.5k lines, all
  268 rules from `Grammar/python.gram`. Includes left-recursion
  seed-and-grow leaders, cut commit, invalid_rules second-pass
  gating, and a `gram-sha256` drift header.
* [x] `parser/pegen/action_helpers_gen.go`: hand-written helpers
  that meet the typed AST surface. Currently `actionPgenMakeModule`
  for the file rule. The generator's action-helper exclusion list
  defers to this file by name.
* [x] `parser/parser.go`: top-level `Parse(mode, src) (ast.Mod,
  error)`, the `peg_api.c` surface.
* [x] `tools/parser_gen/`: Go-targeted PEG generator. Eight
  milestones land:
  * M1 grammar parser (`grammar_parser.go`).
  * M2 nullable + first sets (`firstsets.go`, `nullable.go`).
  * M3 per-rule emitter (`emit.go`).
  * M4 left-recursion + cut (`sccs.go`, leader wrappers).
  * M5 invalid_rules second-pass gating.
  * M6 action expression translator (`action.go`): translates a
    subset of C action bodies (CHECK pass-through, RAISE_*,
    `_PyAST_*`, `_PyPegen_*`); falls back to the bound-name
    `[]any` form for patterns it cannot type yet.
  * M7 wires Dispatch to return the rule result and surfaces
    `*ast.Module` for empty source.
  * M8 corpus iteration (`parser/corpus_test.go`) and grammar
    drift check (`drift.go`, `-check-drift` flag).

### Generator output panel

* [x] Generator round-trips against the upstream
  `Grammar/python.gram` for 3.14.0. Pinned by `TestEmitPythonGramRoundtrip`
  and the SHA256 in the generated preamble.
* [x] Each rule body emits the M3 closure-per-alt shape: per-item
  bindings with shape-aware blocking / always / boolean / noop
  arms, then either a translated action expression or the bound
  names lifted into `[]any`.
* [x] Cut operator (`~`) commits at the same point CPython does;
  `TestEmitPythonGramRoundtrip` verifies at least one alt sets
  `cut = true` against `python.gram`.
* [x] Left-recursive rule sets (Tarjan SCC) emit a seed-and-grow
  leader wrapper plus an unmemoized `_raw` body for non-leaders.
* [x] `invalid_*` rules gate themselves on `p.CallInvalid()` and
  `Dispatch` retries with `SetCallInvalid(true)` on first-pass
  miss.

### Surface guarantees

* [~] `Parse(ModeFile, src)` returns a real `*ast.Module` for the
  empty source case (`TestParseEmptyModule`). Other shapes
  currently fall back to `ErrParserNotImplemented` because the
  action helper layer (`actionAst*`, `actionPgen*`) is mostly
  panic-stubs; coverage is tracked by `TestCorpusParse` (today:
  10/720 sources reach the typed path, 710 sentinel, 0 panic /
  fail on `$CPYTHON/Lib`).
* [ ] Memo cache hit pattern parity against CPython on the
  `Lib/test/test_grammar.py` corpus. Diagnostic, not user-visible.
* [x] SyntaxError text and position match CPython on the
  `parser/errors/golden_panel_test.go` corpus.
* [x] `Parse` is goroutine-safe for distinct calls; one Parser
  instance is not safe for concurrent use.
* [x] Grammar drift detection: `parser_gen -check-drift` and
  `TestCheckGrammarDrift` fail loudly when the recorded
  `gram-sha256` does not match the current `python.gram`.

### Out of scope for v0.5.5

* Incremental / resumable parsing for the LSP. Tracked separately.
* Soft keyword handling beyond what 3.14 already needs (`match`,
  `case`, `type`).

### Cross-references

* Lexer surface: 1641.
* SyntaxError text: 1643.
* Action helpers: 1643.
* String literal handling inside parser actions: 1644.
