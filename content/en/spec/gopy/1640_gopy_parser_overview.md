---
title: "gopy parser overview"
description: "Top-level overview of the gopy Parser port. Covers the PEG parser, lexer, tokenizer drivers, string literal parser, error helpers, and readline. Lives in the 1640-1645 block of the 1600 spec series."
tags: ["gopy", "spec"]
weight: 1640
---

# 1640. gopy: Porting CPython's `Parser/` to Go

## Goal

The 1640-1645 block covers the port of `cpython/Parser/`: the
PEG-driven Python parser, the lexer state machine, the tokenizer
drivers, the string literal parser, the error helpers, and
interactive readline. About 30k lines of C across roughly 18 files.

The output of this block is a Go function that takes source text
(or a readline callback) and returns an `*ast.Module` ready for the
compile pipeline (1620 series).

Same rule as the rest of 1600: 100% behavioural compatibility with
CPython 3.14. Same tokens, same SyntaxError strings, same recovery
points, same line-table positions. Only naming and surface API
style move to Go conventions.

## Why this block exists

v0.5 shipped the compile pipeline against hand-built AST modules.
v0.5 has no parser. To run real Python source we need:

1. A lexer that turns bytes into tokens with positions.
2. A PEG parser that turns tokens into an AST.
3. The error helpers that produce CPython-identical SyntaxError
   strings (the most user-visible part of the parser).

This block fills that gap. It gates v0.5.5 (parser handover into
the v0.5 compile pipeline) and v0.9 (full tokenize.py surface).

## Sources of truth

| Concern                         | Source                                      |
|---------------------------------|---------------------------------------------|
| Token table                     | `Grammar/Tokens`, `Parser/token.c`          |
| Lexer state                     | `Parser/lexer/lexer.c`, `state.c`, `buffer.c` |
| Tokenizer drivers               | `Parser/tokenizer/*.c`                      |
| PEG runtime                     | `Parser/pegen.c`, `peg_api.c`               |
| Generated parser                | `Parser/parser.c` (from `Grammar/python.gram`) |
| Action helpers                  | `Parser/action_helpers.c`                   |
| Error helpers                   | `Parser/pegen_errors.c`                     |
| String literal parser           | `Parser/string_parser.c`                    |
| Interactive readline            | `Parser/myreadline.c`                       |

## Spec files in this block

| #    | File                                | Focus                                                  | Phase |
|------|-------------------------------------|--------------------------------------------------------|-------|
| 1640 | `1640_gopy_parser_overview.md`      | This file                                              | meta  |
| 1641 | `1641_gopy_lexer_tokenizer.md`      | `Parser/lexer/`, `Parser/tokenizer/`, lexer state machine | v0.9 |
| 1642 | `1642_gopy_pegen.md`                | `pegen.c`, `parser.c`, PEG runtime + generated tables  | v0.9 |
| 1643 | `1643_gopy_parser_errors.md`        | `pegen_errors.c`, `action_helpers.c`, `peg_api.c`, `token.c` | v0.9 |
| 1644 | `1644_gopy_string_parser.md`        | `string_parser.c` (f-string / t-string / bytes literals) | v0.9 |
| 1645 | `1645_gopy_myreadline.md`           | `myreadline.c`, interactive line editing               | v0.9+ |

## Phasing

| Phase  | Specs that ship                                         |
|--------|---------------------------------------------------------|
| v0.5.5 | 1641 (subset enough for the compile gate), 1642 (PEG runtime + parser table loader), 1643 (error helpers), 1644 |
| v0.9   | 1641 full panel, 1645 (readline)                        |

v0.5.5 is the parser handover release. It exists so v0.5's
disassembly goldens get re-pinned against parsed source instead of
hand-built AST nodes, closing the loop between source text and
`compile.Compile`.

## Compatibility floors

Items that gate the parser block:

1. Token kinds and numeric values match `Include/internal/pycore_token.h`
   one-to-one. Pinned by `tokenize/types_test.go`.
2. SyntaxError messages byte-equal CPython for every diagnostic in
   `pegen_errors.c`. Pinned by `parser/errors_panel_test.go`.
3. Position tracking (lineno, col_offset, end_lineno, end_col_offset)
   matches CPython for every AST node. Pinned by
   `parser/position_test.go`.
4. f-string and t-string parsing produces the same `JoinedStr` /
   `TemplateStr` nesting CPython does. Pinned by
   `parser/fstring_test.go`.
5. PEG memoization cache hit pattern matches CPython on the
   `Lib/test/test_grammar.py` corpus. Diagnostic only; not
   user-observable.
6. Recovery on incomplete input matches CPython's `E_INTERACT_STOP`
   behaviour for the REPL.

## Test strategy

`partest/` carries the cross-cut gate per phase:

* v0.5.5: `TestGateParseEmpty`, `TestGateParseAssign`,
  `TestGateParseDef`, `TestGateParseFString` round-trip source ->
  AST -> code object -> disassembly text against the v0.5 goldens.
* v0.9: full `Lib/test/test_grammar.py` panel; `partest/errors`
  pins the SyntaxError corpus.

Each per-file spec carries its own per-file tests; this overview
only lists the cross-cut gates.

## Block-level checklist

Status: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Cross-cut artefacts

* [x] `parser/` package skeleton: `Parse`, `ParseString` ship in
  `parser/parser.go`. `ParseFile` / `ParseInteractive` deferred until
  the action surface is fully typed (the file/reader split is already
  expressed by `Parse(io.Reader)` and `ParseString`).
* [~] `partest/` v0.5.5 gate harness: `partest/gate_harness_test.go`
  rounds source through `parser.ParseString` and `compile.Compile`.
  The empty-source case lights up end-to-end today; the assign /
  def / if-else / comprehension / async_def subtests skip per case
  with `action surface not yet typed for this shape` as the
  generator emits panic-stubs for their action helpers. Each case
  flips to a real assertion when its action surface ports.
* [x] `partest/errors` panel: `partest/errors_panel_test.go` plus the
  CPython byte-parity panel under `parser/errors/golden_panel_test.go`.

### Per-spec progress (one row per sub-spec)

| Spec | Status | Notes                                                |
|------|--------|------------------------------------------------------|
| 1641 | [~]    | regular FSM + fstring + type comments + drivers ship; async-keyword path is dead in 3.14 and is not wired |
| 1642 | [~]    | runtime [x]; generator [x] (all 268 rules emit, cut + invalid_rules + left-recursion); action surface partial |
| 1643 | [~]    | SyntaxError panel [x]; action_helpers panel [~] (~35 helpers ported, generator emits panic-stubs for the rest) |
| 1644 | [x]    | string literal parser (f-string, t-string, bytes)    |
| 1645 | [n]    | myreadline (deferred to v0.9+)                       |

### Tooling

* [x] `tools/parser_gen`: Go-targeted regenerator for
  `parser/pegen/parser_gen.go` from `Grammar/python.gram`. Ships the
  full M1-M8 panel: grammar parser, nullable + first sets,
  per-rule emitter, left-recursion + cut, invalid_rules second pass,
  action expression translator, drift check, corpus iteration.
  Records a `gram-sha256` header so a CPython rebase that skips
  regeneration fails CI.

## Out of scope

* The `Tools/peg_generator/` Python implementation itself. We
  consume its output, not the generator. (CPython does the same:
  the generator is build-time, the runtime only sees `parser.c`.)
* `asdl_c.py`. The AST-node generator. Already covered by 1620
  series for the Go side; we do not need a Go port of `asdl_c.py`
  itself.
* Free-threaded parser paths. The parser is single-threaded in
  CPython too.
