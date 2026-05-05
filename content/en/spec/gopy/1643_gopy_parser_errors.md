---
title: "gopy parser errors and helpers"
description: "Port of cpython/Parser/pegen_errors.c, action_helpers.c, peg_api.c, and token.c. SyntaxError text panel, AST construction helpers, and the token table."
tags: ["gopy", "spec"]
weight: 1643
---

# 1643. Parser errors, action helpers, token table

## What we are porting

Three small-to-medium files plus the token table:

* `Parser/pegen_errors.c` (~1500 lines): every SyntaxError text
  the parser emits. Most of CPython's user-visible parser quality
  lives here: "expected ':'", "cannot assign to ...", "did you
  mean :=?".
* `Parser/action_helpers.c` (~1500 lines): the helpers the
  generated parser calls in rule actions to build AST nodes.
  `_PyPegen_singleton_seq`, `_PyPegen_seq_insert_in_front`,
  `_PyPegen_join_names_with_dot`, etc.
* `Parser/peg_api.c` (~200 lines): the public C entry points
  (`PyPegen_ASTFromString`, `PyPegen_ASTFromFile`). Most of this
  becomes one Go function on `parser.Parse` (1642), but the
  diagnostic-flush logic lands here.
* `Parser/token.c` (~250 lines): the token name table. CPython
  generates this from `Grammar/Tokens`; we already generate the
  matching `tokenize/types_gen.go` (1665), so this file becomes a
  formality.

## SyntaxError panel (the bulk of the work)

Every diagnostic in `pegen_errors.c` becomes one entry in
`parser/errors/messages.go`:

```go
// MsgInvalidAssignment is emitted when the LHS of `=` is not an
// assignable target. Mirrors _PyPegen_raise_syntax_error_known_location
// from pegen_errors.c at the "cannot assign to %s" call site.
const MsgInvalidAssignment = "cannot assign to %s"
```

The point is byte parity: when a Python user feeds gopy a broken
program, the SyntaxError they see should be indistinguishable from
CPython's. The set is closed (CPython freezes new error text per
release), so we transcribe it once and pin it via golden tests.

## Action helpers

The generated parser calls helpers like:

```go
// SingletonSeq wraps one node into a one-element list.
// Mirrors _PyPegen_singleton_seq from action_helpers.c.
func SingletonSeq(n ast.Node) []ast.Node

// JoinNamesWithDot turns ["a", "b", "c"] into "a.b.c".
// Mirrors _PyPegen_join_names_with_dot.
func JoinNamesWithDot(names []*ast.Name) string

// SetExprContext walks a Name/Tuple/List/Starred tree and stamps
// each node's expr_context to Store/Del. Mirrors
// _PyPegen_set_expr_context.
func SetExprContext(e ast.Expr, ctx ast.ExprContext) ast.Expr
```

These are mechanical translations: each helper is one or two
dozen lines of Go. About 60 helpers total.

## Token table

`Parser/token.c` defines `_PyParser_TokenNames[]`. We already
generate this in `tokenize/types_gen.go` (1665). The duplication is
intentional: the parser side reads its own copy so the lexer and
parser do not share runtime state.

## Error injection points

CPython's parser invokes the error builder at these moments:

1. Forced expect (`expect_forced_token`): "expected ','"-style.
2. Invalid rule fallback: when `call_invalid_rules` is on, the
   second pass produces the user-friendly text.
3. Tokenizer surfacing: lexer errors flow through
   `_PyPegen_tokenize_full_source_to_check_for_errors` then into
   the same SyntaxError builder.
4. Indent/dedent issues: `pegen_errors.c:_PyPegen_check_tokenizer_errors`.

The Go side groups these into one `parser/errors/builder.go` with
a small constructor table.

## File mapping

| C source                                | Go target                                |
|-----------------------------------------|------------------------------------------|
| `Parser/pegen_errors.c`                 | `parser/errors/messages.go`              |
|                                         | `parser/errors/builder.go`               |
|                                         | `parser/errors/invalid_rules.go`         |
| `Parser/action_helpers.c`               | `parser/pegen/actions.go`                |
| `Parser/peg_api.c`                      | folded into `parser/parser.go` (1642)    |
| `Parser/token.c`                        | folded into `tokenize/types_gen.go` (1665) |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `parser/errors/messages.go`: every SyntaxError string from
  `pegen_errors.c` as a `Msg*` constant. ~120 entries.
* [x] `parser/errors/builder.go`: `Raise`, `RaiseAt`, `RaiseRange`
  helpers that wrap a `*SyntaxError` with the right position.
* [x] `parser/errors/invalid_rules.go`: the second-pass
  user-friendly diagnostics (`call_invalid_rules` mode).
* [x] `parser/errors/tokenizer_errors.go`: lexer-side error lift
  (indent inconsistency, unexpected EOF in string, etc.).
* [~] `parser/pegen/actions.go` plus `arguments.go`,
  `comprehension.go`, `extras.go`, `fstring.go`: the action helper
  surface. ~35 functions across the five files cover the panel the
  v0.5.5 grammar exercises (sequences, name joins, expr-context,
  f-string assembly, arguments). The remaining `_PyPegen_*` /
  `_PyAST_*` helpers the generator references are emitted as
  panic-stubs in `parser_gen.go` and replaced one-by-one as the
  typed AST surface fills in (gated by
  `parser/pegen/action_helpers_gen.go`'s exclusion list).
* [x] `parser/errors/messages_test.go`: golden panel pinning every
  `Msg*` to its CPython text. Refresh via `go test -update`.

### SyntaxError byte-parity panel

* [x] "expected ':'" family (forced expect).
* [x] "cannot assign to ..." family (invalid LHS).
* [x] "did you mean := ?" hint.
* [x] Indent / dedent inconsistency.
* [x] Unmatched / mismatched paren.
* [x] Unterminated string literal (single-line and triple-quoted).
* [x] f-string nesting errors.
* [x] PEP 695 type-param errors.
* [x] Match-statement pattern errors.
* [x] Walrus inside comprehension iterable.
* [x] Star-expression placement.

### Action helper panel

* [x] `SingletonSeq`, `SeqInsertInFront`, `SeqAppend`,
  `SeqFlatten`.
* [x] `JoinNamesWithDot`, `SeqLastItem`, `SeqFirstItem`.
* [x] `SetExprContext` over Name / Tuple / List / Starred /
  Attribute / Subscript.
* [x] `MakeArguments`, `EmptyArguments`.
* [x] `KeyValuePairs`, `KeywordOrStarred` splitter.
* [x] `ConcatenateStrings` (joins adjacent string literals).
* [x] f-string / t-string assembly helpers.
* [x] Comprehension-from-generators helpers.
* [~] Per-rule `actionAst*` / `actionPgen*` helpers that build
  typed AST nodes. `actionPgenMakeModule` ships (the entry point
  for the file rule); the rest are panic-stubs emitted by the
  generator and filled in lazily as the corpus coverage gate
  (`parser/corpus_test.go`) demands.

### Out of scope

* Suggestion-style "did you mean ...?" beyond what
  `pegen_errors.c` already produces. The richer suggestion
  surface (Levenshtein keyword search) lives in `errors/suggest`
  (1611).
