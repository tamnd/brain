---
title: "gopy string parser"
description: "Port of cpython/Parser/string_parser.c. Decodes Python string, bytes, f-string, and t-string literals into AST nodes. Handles escape sequences, prefixes, and f-string interpolation re-entry."
tags: ["gopy", "spec"]
weight: 1644
---

# 1644. String literal parser

## What we are porting

`Parser/string_parser.c` (~2000 lines) is the post-tokenizer
that turns a STRING / FSTRING_* token sequence into one of:

* `ast.Constant{Value: str|bytes}` for plain string and bytes
  literals.
* `ast.JoinedStr{Values: [Constant | FormattedValue]}` for
  f-strings (`f"..."`).
* `ast.TemplateStr{Values: [Constant | Interpolation]}` for
  t-strings (`t"..."`, PEP 750, 3.14).

It owns escape sequence decoding (`\n`, `\xHH`, `\uHHHH`,
`\UHHHHHHHH`, `\N{NAME}`, octal, raw mode), prefix handling
(`r`, `b`, `u`, `f`, `t`, plus combos like `rb`, `Rf`), implicit
concatenation of adjacent literals, and the recursive re-entry into
the parser for `{expr}` inside f-strings.

## Why this is its own spec

Two reasons:

1. The escape-decode logic is the longest hand-traceable
   per-character switch in CPython's parser. It is easy to get
   wrong in subtle ways (`\N{NAME}` lookup against the unicode
   data table, `\xHH` exact two-digit requirement, `\NNN` with
   octal-only digits, raw-mode passthrough preserving the
   backslash).
2. f-string `{expr}` re-enters the parser. Getting the brace
   balance, format spec, conversion (`!r`, `!s`, `!a`), and
   nested f-string handling right is grammar-shaped, not
   tokenizer-shaped, so it lives in `parser/string` rather than
   the lexer.

## Go shape

```go
// Parse decodes a slice of STRING-family tokens into an AST node.
// Mirrors _PyPegen_concatenate_strings from string_parser.c.
//
// The slice may contain implicitly-concatenated literals
// ("a" "b") which Parse joins per CPython's rules: if any are
// f-strings or t-strings, the result is a JoinedStr/TemplateStr.
// If any are bytes, all must be bytes.
func Parse(toks []lexer.Tok) (ast.Expr, error)

// DecodeString applies escape sequences to a single literal.
// Mirrors decode_unicode_with_escapes from string_parser.c.
func DecodeString(raw []byte, prefix Prefix) (string, error)

// DecodeBytes applies escape sequences to a bytes literal.
func DecodeBytes(raw []byte, prefix Prefix) ([]byte, error)

// Prefix is the parsed prefix flags. b/u/f/t and r combinations.
type Prefix struct {
    Bytes    bool
    Raw      bool
    FString  bool
    TString  bool
    Unicode  bool  // legacy 'u'; mostly a no-op
}
```

## f-string re-entry

`{expr}` inside an f-string is re-parsed by the main PEG parser in
`Mode = ModeFString`. The string parser carves the substring,
hands it to `parser.Parse`, and folds the resulting expression
into the JoinedStr.

Format specs (`{x:.2f}`) and conversions (`{x!r}`) are parsed
inline; they are not full Python expressions.

```go
// ParseFStringInterp parses one {...} block and returns the
// FormattedValue. Mirrors fstring_compile_expr from
// string_parser.c.
func ParseFStringInterp(raw []byte, openLine, openCol int) (
    *ast.FormattedValue, error)
```

## t-string re-entry

t-strings (PEP 750) follow the same re-entry shape but yield
`ast.Interpolation` instead of `ast.FormattedValue`. The
`Template` runtime object is built by the runtime, not the
parser; the parser just produces the AST.

## Implicit concatenation rules

CPython rules, faithfully:

1. Adjacent string literals (no comma) concatenate at parse time.
2. `b"a" "b"` is an error: cannot mix bytes and str.
3. `"a" f"b"` joins into one JoinedStr; the plain `"a"` becomes a
   leading Constant value.
4. `f"a" t"b"` is an error: cannot mix f-string and t-string.
5. Raw and non-raw freely mix: `r"\n" "x"` -> `"\\nx"`.

## File mapping

| C source                      | Go target                                |
|-------------------------------|------------------------------------------|
| `Parser/string_parser.c`      | `parser/string/parse.go`                 |
| `Parser/string_parser.h`      | (folded into the same file)              |
| escape decode subset          | `parser/string/decode.go`                |
| f-string interp re-entry      | `parser/string/fstring.go`               |
| t-string interp re-entry      | `parser/string/tstring.go`               |
| concatenation rule            | `parser/string/concat.go`                |
| `\N{...}` unicode-name lookup | `parser/string/charname.go`              |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [x] `parser/string/parse.go`: top-level `Parse(toks)` entry, the
  prefix-flags decoder, the `Prefix` struct.
* [x] `parser/string/decode.go`: escape-sequence panel for
  string and bytes literals.
* [x] `parser/string/fstring.go`: f-string brace-balance scanner,
  format-spec parser, conversion parser, re-entry into
  `parser.Parse`.
* [x] `parser/string/tstring.go`: t-string brace-balance scanner,
  Interpolation node assembly.
* [x] `parser/string/concat.go`: implicit-concat rule with the
  bytes/str/f/t mixing checks.
* [x] `parser/string/charname.go`: `\N{...}` lookup against the
  Unicode name table. Reads the same generator output the
  unicode object will use (1677).
* [x] `parser/string/parse_test.go`: per-escape panel pinned to
  CPython output.

### Escape sequence panel

* [x] `\n`, `\t`, `\r`, `\v`, `\b`, `\f`, `\a`, `\0`, `\\`, `\'`,
  `\"`.
* [x] `\xHH`: exactly two hex digits, error otherwise.
* [x] `\uHHHH`: exactly four hex digits, str only.
* [x] `\UHHHHHHHH`: exactly eight hex digits, str only.
* [x] `\N{NAME}`: Unicode name lookup, str only.
* [x] `\NNN`: 1 to 3 octal digits.
* [x] Raw mode: keep the backslash, do not decode.
* [x] Bytes mode: reject `\u`, `\U`, `\N{...}`.
* [x] Unknown escape: warn under `-W default::SyntaxWarning`.

### f-string panel

* [x] Plain `f"x"` with no `{}` collapses to one Constant.
* [x] `{expr}` re-enters the main parser.
* [x] Format spec `{x:.2f}` parses the `.2f` as a Constant suffix
  (or, with nested `{}`, as another JoinedStr).
* [x] Conversion `{x!r}`, `{x!s}`, `{x!a}` lifts to
  `FormattedValue.Conversion`.
* [x] `{{` and `}}` escape to literal `{` and `}`.
* [x] Nested f-strings: 3.12+ allows arbitrary nesting; pin the
  3.14 limit.
* [x] Walrus inside `{expr}`.
* [x] Multiline f-strings.
* [x] `f"...{x = }"` debug syntax.

### t-string panel

* [x] Plain `t"x"` with no `{}` collapses to one Constant inside
  the TemplateStr.
* [x] `{expr}` lifts to `Interpolation`.
* [x] Same conversion / format-spec syntax as f-strings.
* [x] Mixing rule: cannot implicitly concatenate t-strings with
  f-strings.

### Cross-references

* Token feed: 1641.
* Re-entry into PEG: 1642.
* SyntaxError text: 1643.
* `\N{...}` lookup table: 1677 (unicode object).

### Out of scope

* The `template`/`interpolation` runtime objects (`Template`,
  `Interpolation`). They live in 1689.
