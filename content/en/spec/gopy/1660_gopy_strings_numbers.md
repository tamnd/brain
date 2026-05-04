---
title: "gopy strings and numbers"
description: "Locale-independent string and number conversion. Ports pyctype.c, pystrcmp.c, mystrtoul.c, pystrtod.c, dtoa.c, pystrhex.c, pymath.c, pyfpe.c, formatter_unicode.c."
tags: ["gopy", "spec"]
weight: 1660
---

# 1660. Strings and numbers

## What we are porting

Eight files from `cpython/Python/`:

| C source                | Lines | Go target                       |
|-------------------------|-------|---------------------------------|
| `pyctype.c`             |  215  | `pystrconv/ctype.go`            |
| `pystrcmp.c`            |   31  | `pystrconv/cmp.go`              |
| `mystrtoul.c`           |  297  | `pystrconv/strtoul.go`          |
| `pystrtod.c`            | 1286  | `pystrconv/strtod.go`           |
| `dtoa.c`                | 2843  | `pystrconv/dtoa.go` (see below) |
| `pystrhex.c`            |  171  | `pystrconv/hex.go`              |
| `pymath.c`              |   19  | `pymath/pymath.go`              |
| `pyfpe.c`               |   ~5  | `pymath/fpe.go`                 |
| `formatter_unicode.c`   | 1726  | `format/format.go`              |

Together they form the bedrock that `int.__repr__`, `float.__repr__`,
`int.__str__`, `float.__str__`, `format()`, `f"{x:.2f}"`,
`int(s, base)`, `float(s)`, and `bytes.hex()` all dispatch through.
Nothing here depends on the runtime, the parser, or the VM. Everything
here is callable from Go directly and tested with table-driven inputs.

## pyctype: locale-independent ctype

`cpython/Python/pyctype.c` ships a 256-entry bitmask table plus
toupper/tolower lookup tables. The behaviour is fixed by
`cpython/Include/cpython/pyctype.h`:

```
PY_CTF_LOWER  0x01
PY_CTF_UPPER  0x02
PY_CTF_ALPHA  PY_CTF_LOWER | PY_CTF_UPPER
PY_CTF_DIGIT  0x04
PY_CTF_ALNUM  PY_CTF_ALPHA | PY_CTF_DIGIT
PY_CTF_SPACE  0x08
PY_CTF_XDIGIT 0x10
```

`Py_ISSPACE` matches `' '`, `\t`, `\n`, `\v`, `\f`, `\r`. `Py_ISDIGIT`
is `'0'..'9'`. `Py_ISXDIGIT` is digits plus `'a'..'f'` and `'A'..'F'`.
`Py_TOLOWER`/`Py_TOUPPER` are ASCII-only and locale-independent.

Go translation skips the literal 256-entry table because computing the
flags from the byte is faster than a memory load and trivially
auditable. The exhaustive 0..255 round-trip test guarantees the
byte-for-byte equivalence with the original tables.

```go
func Flags(c byte) uint32
func IsLower(c byte) bool
func IsUpper(c byte) bool
func IsAlpha(c byte) bool
func IsDigit(c byte) bool
func IsXDigit(c byte) bool
func IsAlnum(c byte) bool
func IsSpace(c byte) bool
func ToLower(c byte) byte
func ToUpper(c byte) byte
```

## pystrcmp: case-insensitive ASCII compare

`cpython/Python/pystrcmp.c` has two functions, `PyOS_mystricmp` and
`PyOS_mystrnicmp`, both ASCII case-folding. They are used by the
config parser, the float repr, and a handful of other locale-sensitive
spots that explicitly want the locale-free behaviour.

```go
func CompareInsensitive(a, b string) int
func CompareInsensitiveN(a, b string, size int) int
```

## mystrtoul: integer parsing

`cpython/Python/mystrtoul.c` is the fast path for `int(s, base)`. It
handles base 0 (auto-detect from `0x`, `0o`, `0b` prefixes), bases
2..36, leading whitespace, optional `+`/`-` sign, underscores between
digits (PEP 515), and overflow detection. Returns the parsed value
plus the number of bytes consumed.

```go
type IntParseError int
const (
    IntOK IntParseError = iota
    IntInvalid
    IntOverflow
)

// ParseUint mirrors PyOS_strtoul.
func ParseUint(s string, base int) (val uint64, n int, err IntParseError)

// ParseInt mirrors PyOS_strtol.
func ParseInt(s string, base int) (val int64, n int, err IntParseError)
```

## pystrtod and dtoa: float parsing and formatting

This is the heaviest file in the v0.4 batch. `dtoa.c` is David Gay's
2843-line bignum-arithmetic implementation of `strtod` and `dtoa`.
`pystrtod.c` wraps it with the Python-specific surface
(`PyOS_string_to_double`, `PyOS_double_to_string`, the `'r'`/`'g'`/`'e'`
format codes, the locale-independent decimal point, the inf/nan/hex
literal recognition).

### dtoa decision

CPython links David Gay's `dtoa.c` directly. Go's standard library
contains its own pure-Go float parser/formatter (`strconv`) using
Ryu/Grisu plus a bignum fallback for the round-trip-tight cases. Both
are bit-correct under IEEE 754 round-to-nearest-even. They produce
**the same `uint64` bit pattern for any input string CPython accepts**
because correct round-to-nearest is unique.

v0.4 implements `pystrconv/strtod.go` as a thin wrapper over Go's
`strconv.ParseFloat` with CPython-specific input pre-processing:

* Reject `nan(123)` parenthesised payload form (Go accepts it).
* Reject leading whitespace inside the number (Go strconv rejects it
  too; the CPython entry already strips outer whitespace).
* Honour the `'_'` digit separator the same way as int parsing.
* Treat `inf` / `infinity` case-insensitively.

`pystrconv/dtoa.go` is a wrapper over `strconv.AppendFloat('r', -1)`
for shortest round-trip, with explicit format codes:

* `'r'` (repr), `'s'` (str), `'g'` (general), `'e'` (exponent),
  `'f'` (fixed), `'%'` (percent).
* `'r'` calls `AppendFloat(buf, f, 'g', -1, 64)`.
* The output sign for negative zero matches CPython's
  `0/-0/0.0/-0.0` rules.

A faithful 1:1 dtoa.c port is **out of scope** for v0.4. It is tracked
as a follow-up issue: the wrapper is bit-correct (the gate test pins
that), but the source-shape parity is not as direct as the rest of the
port. The wrapper carries a doc comment naming each `dtoa.c` function
it stands in for so the eventual replacement is mechanical.

### Surface

```go
// ParseFloat mirrors PyOS_string_to_double.
func ParseFloat(s string) (float64, error)

// FormatFloat mirrors PyOS_double_to_string. code is one of
// 'r', 's', 'g', 'e', 'f', '%'. precision is -1 for the
// format-default.
func FormatFloat(f float64, code byte, precision int, flags FormatFlag) string

type FormatFlag uint32
const (
    FlagAddDotZero FormatFlag = 1 << iota
    FlagAlternate
    FlagAlwaysSign
    FlagSpaceSign
)
```

## pystrhex: bytes-to-hex

Direct port. Three entry points (`Hex`, `HexBytes`, `HexWithSep`) feed
`bytes.hex()`, `binascii.hexlify`, `memoryview.hex()`. Right-grouped
default; negative `bytesPerGroup` switches to left-grouped.

## pymath and pyfpe

`pymath.c` is a 19-line file: it defines `_Py_dg_stdnan`,
`_Py_dg_infinity`, and `_Py_log1p` if the C math library lacks one.
The Go target uses `math.NaN()`, `math.Inf(1)`, and `math.Log1p`
directly, so the port is a thin file with the sentinels exposed at the
package level for downstream code that wants the same names as
CPython.

`pyfpe.c` is essentially empty in modern CPython (the FP exception
machinery was removed in 3.10). The Go target preserves the file
so the source-shape mapping stays one-to-one.

## formatter_unicode: format mini-language

`cpython/Python/formatter_unicode.c` implements the format-spec
mini-language for `format(value, spec)` and f-strings:

```
[[fill]align][sign][#][0][width][,][.precision][type]
```

This is a sizable port: 1726 lines of C with several mode-specific
sub-formatters (int, long, float, complex, bytes, str). v0.4 ships:

* The format-spec parser (`parse_internal_render_format_spec`).
* String formatter (`format_string_internal`).
* Int formatter (`format_long_internal`) including grouping
  (`,` / `_`) and the `b`/`o`/`d`/`x`/`X`/`c` type codes.
* Float formatter (`format_float_internal`) including
  `e`/`E`/`f`/`F`/`g`/`G`/`%` type codes, leveraging
  `pystrconv.FormatFloat` underneath.

`format_complex_internal` rides along when complex lands (no v0.4
caller forces it; defer until needed).

```go
type Spec struct {
    Fill      rune
    Align     byte // '<', '>', '=', '^', or 0
    Sign      byte // '+', '-', ' ', or 0
    Alt       bool
    Zero      bool
    Width     int
    Thousands byte // ',', '_', or 0
    Precision int  // -1 == unset
    Type      byte
}

// ParseSpec parses a format spec mini-language string.
func ParseSpec(s string) (Spec, error)

// FormatString renders a string under spec.
func FormatString(s string, spec Spec) (string, error)

// FormatInt renders an integer (any signed/unsigned width via *big.Int)
// under spec.
func FormatInt(v *big.Int, spec Spec) (string, error)

// FormatFloat renders a float under spec.
func FormatFloat(v float64, spec Spec) (string, error)
```

## Test strategy

Each function gets a table-driven test rooted in CPython output. For
the round-trip-critical pieces (`ParseFloat`, `FormatFloat`,
`Hash` over a known seed) the gate runs the bit-pattern comparison
against pre-computed CPython references to catch any divergence.
