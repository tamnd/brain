---
title: "gopy unicode"
description: "Port of cpython/Objects/unicodeobject.c and unicodectype.c. PEP 393 kind-tagged str with the full method surface and Unicode classification tables."
tags: ["gopy", "spec"]
weight: 1677
---

# 1677. Unicode (str)

## What we are porting

Two files, ~17000 lines total. The single largest object port:

* `Objects/unicodeobject.c`: PEP 393 kind-tagged string. Three
  storage kinds (1-byte, 2-byte, 4-byte) chosen at construction
  to fit the largest code point. Method surface (`split`, `join`,
  `find`, `replace`, `format`, `encode`, `decode`,
  `casefold`, etc.). String interning. Codecs registry hooks.
* `Objects/unicodectype.c`: Unicode 16.0 classification tables.
  `is_alnum`, `is_alpha`, `is_decimal`, `is_digit`, `is_lower`,
  `is_upper`, `is_title`, `is_space`, `is_xid_start`,
  `is_xid_continue`, plus `to_lower`, `to_upper`, `to_title`,
  `to_decimal`, `to_digit`. Tables generated from the Unicode
  Character Database.

## Go shape

```go
// Str mirrors PyUnicodeObject. Kind picks the storage width.
type Str struct {
    VarHeader
    kind     Kind  // 1, 2, 4 bytes per code point
    data     []byte  // length = size * kind
    hash     int64
    ascii    bool   // shortcut: kind==1 && all bytes < 0x80
    interned uint8  // 0 = not, 1 = mortal, 2 = immortal
}

type Kind uint8
const (
    Kind1 Kind = 1
    Kind2 Kind = 2
    Kind4 Kind = 4
)
```

CPython 3.12+ also has a "compact" inline-storage variant. We do
not optimise for that yet; the spill cost is one extra slice
header.

## ASCII fast path

`Str.ascii` lets every method short-circuit when both operands are
ASCII. CPython does the same via the `state.ascii` bit on the
header.

## String interning

Python interns short identifier-shaped strings (`__init__`,
`self`, etc.) automatically. We interns the same set CPython
interns: any string passed to `_Py_intern` from the parser plus
the contents of `Lib/keyword.py`. Identity is cheap inside the
interned set; equality stays correct outside it.

## Hashing

SipHash-1-3 over the byte payload (not the code-point sequence;
identical to CPython since the kind layout determines the bytes).
Cached in the `hash` field.

## Codecs

The codecs registry lives in `objects/codecs.go`. v0.4 ships UTF-8,
UTF-16-le/be, UTF-32-le/be, ASCII, latin-1, and the error handlers
(`strict`, `replace`, `backslashreplace`, `xmlcharrefreplace`,
`namereplace`, `surrogateescape`, `surrogatepass`). The
charset-table codecs (cp1252, gb18030, etc.) are stdlib in CPython
too; they ride along once the import system lands (v0.8).

## Unicode tables

`tools/unicode_gen/main.go` reads the Unicode Character Database
and emits `objects/unicode_tables_gen.go`. Same data CPython's
`Tools/unicode/makeunicodedata.py` emits, just typed for Go.

## File mapping

| C source                           | Go target                                |
|------------------------------------|------------------------------------------|
| `Objects/unicodeobject.c`          | `objects/str.go`                         |
| kind layout / construction         | `objects/str_kind.go`                    |
| methods                            | `objects/str_methods.go`                 |
| format / `__format__`              | `objects/str_format.go`                  |
| codecs registry                    | `objects/codecs.go`                      |
| utf-8 codec                        | `objects/codec_utf8.go`                  |
| utf-16/32, ascii, latin-1          | `objects/codec_*.go`                     |
| error handlers                     | `objects/codec_errors.go`                |
| interning                          | `objects/str_intern.go`                  |
| `Objects/unicodectype.c`           | `objects/unicode_ctype.go`               |
| generated tables                   | `objects/unicode_tables_gen.go`          |
| generator                          | `tools/unicode_gen/`                     |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [ ] `objects/str.go`: `Str` struct, `FromString`, `FromBytes`
  (decode UTF-8), `AsString`, length, getitem, iter.
* [ ] `objects/str_kind.go`: `pickKind`, `repack`, `widen`. Kind
  selection on construction matches CPython.
* [ ] `objects/str_methods.go`: split, rsplit, splitlines,
  partition, rpartition, join, find, rfind, index, rindex,
  count, replace, strip, lstrip, rstrip, translate,
  startswith, endswith, expandtabs, center, ljust, rjust, zfill,
  encode, format, format_map, casefold, lower, upper, title,
  swapcase, capitalize, isalnum, isalpha, isascii, isdecimal,
  isdigit, isidentifier, islower, isupper, isnumeric, isprintable,
  isspace, istitle, removeprefix, removesuffix.
* [ ] `objects/str_format.go`: `__format__` over the `[[fill]align]
  [sign][#][0][width][,_][.precision][type]` mini-language.
* [ ] `objects/codecs.go`: registry, `Encode`, `Decode`,
  `LookupCodec`, error-handler registry.
* [ ] `objects/codec_utf8.go`: encode + decode + surrogate
  handling.
* [ ] `objects/codec_utf16.go`, `codec_utf32.go`,
  `codec_ascii.go`, `codec_latin1.go`.
* [ ] `objects/codec_errors.go`: strict, replace, ignore,
  backslashreplace, xmlcharrefreplace, namereplace,
  surrogateescape, surrogatepass.
* [ ] `objects/str_intern.go`: intern set, `Intern`, identity
  guarantees for compile-time-known strings.
* [ ] `objects/unicode_ctype.go`: classification + case-mapping
  predicates.
* [ ] `objects/unicode_tables_gen.go`: generated.
* [ ] `tools/unicode_gen/main.go`: generator from UCD.

### Surface guarantees

* [ ] `hash(str)` matches CPython under PYTHONHASHSEED=0 across
  every kind (1/2/4 byte).
* [ ] `repr(str)` chooses the same quote style and escape style
  CPython does, including `\x`, `\u`, `\U`, `\N{...}`.
* [ ] `'a' in 'banana'` performs the same Boyer-Moore-Horspool
  fallback CPython uses for medium needles.
* [ ] `str.casefold()` matches Unicode 16.0 (German `ß` ->
  `'ss'`, etc.).
* [ ] `'é' == 'é'` is `False` (no auto-NFC).
* [ ] `'a'.encode('utf-8') == b'a'`, surrogate pairs round-trip
  with `surrogatepass`.
* [ ] `str.isidentifier()` follows the XID_Start / XID_Continue
  rules from PEP 3131.
* [ ] Interned identity: every keyword in `keyword.kwlist` is
  interned and returns the same object.

### Cross-references

* Hash key: 1661.
* Bytes <-> str round-trip: 1676.
* Format mini-language: 1660.
* `\N{...}` lookup table also used by 1644.

### Out of scope

* Locale-aware case mapping (full Turkish, etc.). Stdlib.
* normalize() (NFD / NFC / NFKD / NFKC). Lives in
  `unicodedata` stdlib module.
* The `_string` extension module. Stdlib bridge.
