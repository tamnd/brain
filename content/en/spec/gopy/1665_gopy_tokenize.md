---
title: "gopy tokenize"
description: "Public TokenizerIter wrapper. Ports Python-tokenize.c. The actual lexer lives in cpython/Parser/tokenizer/ and is covered by the parser spec series."
tags: ["gopy", "spec"]
weight: 1665
---

# 1665. Tokenize

## What we are porting

One file from `cpython/Python/`:

| C source                | Lines | Go target               |
|-------------------------|-------|-------------------------|
| `Python-tokenize.c`     |   445 | `tokenize/tokenize.go`  |

`Python-tokenize.c` is the Python-visible wrapper around the lexer. It
exposes the `_tokenize.TokenizerIter` class that `tokenize.tokenize()`
in the stdlib delegates to. The actual lexer (state machine, indent
tracking, f-string handling, encoding detection) lives in
`cpython/Parser/tokenizer/` and is in the parser spec series.

This spec is small on purpose. It covers only the iterator surface and
its mapping to a Go iterator. The lexer port underneath is tracked
elsewhere; v0.9 wires this module through the import system.

## What the wrapper does

`tokenizeriter_new` constructs a `tokenizeriterobject` from:

* a readline callable (`io.TextIO.readline`-shaped), or
* a source string (`source` keyword), with optional `extra_tokens`
  flag.

`tokenizeriter_next` advances the underlying `struct tok_state*` one
token at a time and returns a 5-tuple
`(type, string, start, end, line)`. The `type` value is one of the
constants exported from `token.h` (NAME=1, NUMBER=2, STRING=3, OP=54,
etc.). When `extra_tokens=False` the wrapper filters out COMMENT, NL,
ENCODING, and NEWLINE-at-EOF.

The wrapper also handles:

* Encoding detection on byte input. The first physical line is parsed
  for `coding:` BOM or PEP 263 cookie.
* SyntaxError lifting. A lexer error becomes a Python SyntaxError with
  the right offset, end-offset, and source line.
* `tok->cur` to source-line slicing for the `line` field of every
  token.

## Go shape

```go
package tokenize

type Type int

const (
    ENDMARKER Type = iota
    NAME
    NUMBER
    STRING
    NEWLINE
    INDENT
    DEDENT
    LPAR
    // ... full set generated from cpython/Grammar/Tokens.
)

type Pos struct{ Line, Col int }

type Token struct {
    Type   Type
    Value  string
    Start  Pos
    End    Pos
    Line   string
}

// Iter is the Go-side TokenizerIter equivalent. Next returns
// io.EOF when the stream is exhausted.
type Iter struct {
    // unexported handle into the lexer state
}

func New(src string, extraTokens bool) *Iter
func NewReadline(rl func() (string, error), extraTokens bool) *Iter

func (it *Iter) Next() (Token, error)
```

The lexer state behind `Iter` is the Go port of
`cpython/Parser/tokenizer/`. v0.5 stubs this with a parser-side
lexer skeleton sufficient for the pipeline gate; the public surface in
this package is stable across that change.

Token type constants are generated from `cpython/Grammar/Tokens` by
`tools/tokens_go` and emitted into `tokenize/types_gen.go`. The
generator is shared with the parser spec.

## Stdlib bridge

Python's `tokenize.tokenize(readline)` is implemented in
`Lib/tokenize.py` and calls `_tokenize.TokenizerIter`. Once v0.9
wires the import system through frozen modules, our `tokenize/`
package backs that import via a Go module exposing `TokenizerIter`
through the `objects.Module` protocol.

## Errors

The wrapper preserves CPython's exact SyntaxError strings. Cases:

* Unterminated string literal.
* Inconsistent indentation.
* Unmatched bracket.
* Encoding declaration mismatch.
* Tab/space mixing under `-tt`.

Each is reproduced verbatim from `Python-tokenize.c` plus the lexer
error path.

## Gate

Round-trip tokenize a panel of source files (`test_tokenize.py`
fixtures from CPython) and assert the token stream matches what
CPython's `tokenize.tokenize` produces, byte-for-byte on the value
field and exact on type plus position. The gate lives in
`tokenize/tokenize_test.go` and ships with v0.9 once the import
plumbing exists; v0.5 adds the package skeleton plus a Go-only unit
test of the iterator contract.

## Out of scope

* The lexer state machine itself (Parser/tokenizer/). Separate spec.
* `untokenize`. Lives in `Lib/tokenize.py`, ported as part of the
  stdlib effort.
* Async tokenization. Not a CPython surface.

## v0.5 checklist

This is the implementation contract. Each box maps to a test in 1625
§16.

### Files

* [x] `token/token.go`: hand-written `Type` declaration plus
  `String()` method that delegates to the generated `tokenNames`
  table. Lives in its own package to mirror CPython's
  `pycore_token.h` / `Lib/token.py` split and avoid an import cycle
  with the parser's lexer.
* [x] `tools/tokens_go/main.go`: generator that reads
  `Include/internal/pycore_token.h` (the `#define NAME N` lines) and
  `Lib/token.py` (the `NAME = N` lines), filters
  `N_TOKENS`/`NT_OFFSET`/`ENCODING_OFFSET`, and emits `token/types_gen.go`.
* [x] `token/types_gen.go`: 69 token kinds (ENDMARKER=0..ENCODING=68)
  plus `NTokens=69` and the `tokenNames` table.
* [x] `tokenize/tokenize.go`:
  * [x] `Pos struct{ Line, Col int }`.
  * [x] `Token struct{ Type token.Type; Value string; Start, End Pos; Line string }`.
        (`Line` is left empty; full source-line slicing tracked under
        the v0.9 surface guarantee below.)
  * [x] `Iter` opaque struct holding the underlying `*lexer.State`.
  * [x] `New(src string, extraTokens bool) *Iter` — wires
        `lexer.FromString` plus `SetExtraTokens`.
  * [x] `NewReadline(rl func() (string, error), extraTokens bool) *Iter`
        — wires `lexer.FromReadline` with a `[]byte`/`string` adapter.
  * [x] `(it *Iter) Next() (Token, error)` returning `io.EOF` after
        the lexer's ENDMARKER lands.
* [x] `tokenize/tokenize_test.go`: ENDMARKER-then-EOF, simple
  assignment kinds, readline driver smoke. The numeric/Type.String
  panel moved to `token/token_test.go` along with the constants.

### Surface guarantees

* [x] Numeric values of `Type` constants match
  `cpython/Include/internal/pycore_token.h` and `cpython/Lib/token.py`
  one-to-one. Pinned by `TestTypeNumericValues`.
* [ ] `extraTokens=false` filters COMMENT, NL, ENCODING, and the
  trailing NEWLINE-at-EOF (CPython parity). (v0.9.)
* [ ] Encoding detection on byte input recognises BOM and PEP 263
  cookies. (v0.9.)
* [ ] Lexer errors lift to a Go `*SyntaxError` whose `Error()` string
  is verbatim from `Python-tokenize.c` plus the lexer error path. (v0.9.)
* [ ] `tok->cur` slicing for the `Line` field of every token. (v0.9.)

### Stdlib bridge (v0.9, tracked here)

* [ ] `objects.Module` shim that exposes `TokenizerIter` so
  `Lib/tokenize.py` works once the import system is wired.

### Out of scope for v0.5

* The actual lexer state machine. Tracked under `Parser/tokenizer/`.
* `untokenize`. Stdlib effort.
