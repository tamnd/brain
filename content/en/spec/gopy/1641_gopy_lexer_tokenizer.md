---
title: "gopy lexer and tokenizer"
description: "Port of cpython/Parser/lexer/ and cpython/Parser/tokenizer/. Lexer state machine, buffer, token emission, and the four tokenizer drivers (file, string, utf8, readline)."
tags: ["gopy", "spec"]
weight: 1641
---

# 1641. Lexer and tokenizer drivers

## What we are porting

CPython's lexer is split into two layers:

* `Parser/lexer/`: the state machine that consumes bytes and emits
  tokens. `lexer.c` is the FSM, `state.c` owns the per-tokenizer
  state struct, `buffer.c` owns the slidable input buffer.
* `Parser/tokenizer/`: four drivers that feed the lexer from
  different sources. `utf8_tokenizer.c` (in-memory UTF-8 string),
  `string_tokenizer.c` (legacy string with encoding detection),
  `file_tokenizer.c` (FILE\*), `readline_tokenizer.c` (REPL
  callback). `helpers.c` is the shared decode / line-handling
  surface.

Together they are the most stateful part of CPython's parser, with
roughly 6k lines of C. The lexer tracks indentation, parenthesis
depth, type-comment mode, async-aware keywords (3.7+), f-string
nesting, and continuation lines.

## Go translation

Top-level surface lives in `parser/lexer/`:

```go
// State is the per-tokenizer struct. Mirrors struct tok_state from
// Parser/lexer/state.h. Fields renamed from snake_case to Go style.
type State struct {
    buf      *Buffer       // input buffer
    indents  []int         // indent stack
    parens   []byte        // open paren stack: '(' '[' '{' or 0
    line     int           // 1-based
    col      int           // 0-based code-point offset
    mode     Mode          // file, single, eval, fstring
    async    asyncState    // 3.7 keyword tracking
    fstring  []fstringTok  // open f-string contexts
    err      *SyntaxError
}

// Mode mirrors Parser/lexer/state.h:Pegen_*Mode.
type Mode int
const (
    ModeFile Mode = iota
    ModeSingle
    ModeEval
    ModeFunctionType
    ModeFString
)
```

Buffer model in `parser/lexer/buffer.go`:

```go
// Buffer mirrors the buf/cur/inp/end pointer quartet from
// Parser/lexer/buffer.c. We use offsets into a []byte instead of
// raw pointers, but the semantics are identical.
type Buffer struct {
    src []byte
    cur int  // current read offset
    lineStart int
    eof bool
}
```

Token emission lives in `parser/lexer/lexer.go`:

```go
// Tok is the lexer's emitted token. Mirrors struct token from
// Parser/lexer/state.h. Distinct from tokenize.Token (1665) which
// is the public Python-facing surface.
type Tok struct {
    Kind     tokenize.Type
    Bytes    []byte
    Start    Pos
    End      Pos
    Metadata uint32  // packs is_keyword, is_async_keyword, etc.
}

// Next pulls one token. Mirrors tok_get from Parser/lexer/lexer.c.
func (s *State) Next() (Tok, error)
```

## Driver dispatch

Each of the four tokenizer drivers is a thin constructor over
`State`:

```go
// FromUTF8 mirrors utf8_tokenizer.c:_PyTokenizer_FromUTF8.
func FromUTF8(src []byte, mode Mode) *State

// FromString mirrors string_tokenizer.c with encoding detection
// (BOM + PEP 263 cookie).
func FromString(src []byte, mode Mode) (*State, error)

// FromFile mirrors file_tokenizer.c. Wraps an io.Reader and
// handles incremental reads.
func FromFile(r io.Reader, mode Mode) *State

// FromReadline mirrors readline_tokenizer.c. The callback returns
// one line at a time; used by the REPL.
func FromReadline(rl func() (string, error), mode Mode) *State
```

## Indentation, parens, async

The three statefulnesses CPython tracks:

1. Indent stack: `tabsize=8`, `altabsize=1`, error on inconsistent
   tab/space mixing under PEP 8 mode. Same algorithm as
   `tok_get_indent` in `lexer.c`.
2. Paren stack: balances `()`, `[]`, `{}` across logical lines.
   Mismatch yields the same `unmatched ']'` text CPython emits.
3. Async-keyword state: pre-3.7 quirk is gone in 3.14; the field
   stays so we can re-enable for older grammar tests if needed.

## f-string and t-string nesting

f-strings recursively re-enter the lexer with `ModeFString`. The
nesting stack is `fstring []fstringTok`. Each entry tracks the
quote style, the brace depth, and whether we are inside a `:` format
spec. Same structure as `tok->tok_extra_tokens` in CPython 3.12+.

t-strings (PEP 750, 3.14) reuse the same machinery with a different
Tok kind on emission. The nesting algorithm is identical; only the
emitted token type differs.

## Errors

Lexer errors lift to a `*SyntaxError` whose text is verbatim from
`pegen_errors.c`. The mapping table lives in 1643.

## File mapping

| C source                                 | Go target                               |
|------------------------------------------|-----------------------------------------|
| `Parser/lexer/state.h` (struct)          | `parser/lexer/state.go`                 |
| `Parser/lexer/state.c`                   | `parser/lexer/state.go`                 |
| `Parser/lexer/buffer.c`                  | `parser/lexer/buffer.go`                |
| `Parser/lexer/lexer.c`                   | `parser/lexer/lexer.go`                 |
| `Parser/tokenizer/utf8_tokenizer.c`      | `parser/lexer/driver_utf8.go`           |
| `Parser/tokenizer/string_tokenizer.c`    | `parser/lexer/driver_string.go`         |
| `Parser/tokenizer/file_tokenizer.c`      | `parser/lexer/driver_file.go`           |
| `Parser/tokenizer/readline_tokenizer.c`  | `parser/lexer/driver_readline.go`       |
| `Parser/tokenizer/helpers.c`             | `parser/lexer/helpers.go`               |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `parser/lexer/state.go`: `State` struct, `Mode` constants,
  `New`, `Free`. Indent stack, paren stack, f-string mode stack.
  Async-keyword tracking is intentionally not wired: 3.14 made
  `async` / `await` full hard keywords so the pre-3.7 quirk is
  dead code in CPython too.
* [x] `parser/lexer/buffer.go`: collapses to a no-op pair plus
  `reserveBuf`. The C source's pointer rebase dance is unnecessary
  because gopy stores offsets.
* [x] `parser/lexer/lexer.go`: regular-mode FSM (NAME, NUMBER,
  STRING single + triple, OP, NEWLINE/NL, INDENT/DEDENT, comment,
  ENDMARKER), type-comment branch, line continuation, and the
  entry into f-string mode all land. The f-string scanner itself
  sits in `fstring.go`. Async-keyword tracking is N/A on 3.14.
* [x] `parser/lexer/fstring.go`: f-string brace-balance scanner,
  `:`-format-spec mode, conversion specifiers.
* [n] `parser/lexer/driver_utf8.go`: collapsed into driver_string.go
  because Go strings are already UTF-8.
* [x] `parser/lexer/driver_string.go`: in-memory driver with BOM
  + PEP 263 cookie detection. The cookie scanner lives alongside in
  `source.go` and is exercised by `source_test.go`.
* [x] `parser/lexer/driver_file.go`: `io.Reader` driver with
  incremental refill.
* [x] `parser/lexer/driver_readline.go`: REPL driver over a
  `func() (string, error)` callback.
* [x] `parser/lexer/helpers.go`: shared decode / line slicing /
  printable-ASCII filter ports of `helpers.c`.
* [x] `parser/lexer/lexer_test.go`: tokenisation panels including
  type comments. Indent/dedent, paren balance, and f-string nesting
  are pinned by sibling panels under `partest/` (`indent_test.go`,
  `paren_mismatch_test.go`, `fstring_nesting_test.go`,
  `fstring_walrus_test.go`).

### Surface guarantees

* [x] Token kinds match the table generated for 1665. Pinned by
  `parser/lexer/types_test.go` referencing `tokenize.Type`.
* [x] Indent/dedent emission matches CPython on the
  `Lib/test/test_tokenize.py` indentation corpus.
* [x] Paren-mismatch errors quote the same span CPython quotes
  (start of opening, span to current).
* [x] f-string nesting depth panel: 0..6 levels with mixed `:`
  format specs reproduces CPython's emission.
* [x] Encoding detection: UTF-8 BOM, ASCII default, PEP 263 cookies
  on line 1 and line 2, conflicting BOM-vs-cookie error message.
* [x] CRLF, CR, LF line ending normalisation matches CPython.

### Cross-references

* Token table values: 1665.
* SyntaxError text: 1643.
* String literal post-processing: 1644.

### Out of scope for v0.5.5

* Interactive readline. Lands in 1645 alongside v0.9 REPL work.
* `tok->tok_extra_tokens` for COMMENT / NL / ENCODING in
  `extraTokens=true` mode. Surface lands in 1665, lexer side lands
  here in v0.9.

### Out of scope, period

* Free-threaded parser paths. The parser runs under one goroutine.
