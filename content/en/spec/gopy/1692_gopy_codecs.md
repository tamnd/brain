---
title: "gopy codecs"
description: "Port of cpython/Python/codecs.c (1708 lines) to the codecs/ package. Codec registry, error-handler registry, Encode/Decode entry points, and the three built-in codecs (utf-8, ascii, latin-1) needed by the import source reader."
tags: ["gopy", "spec"]
weight: 1692
---

# 1692. codecs (Python/codecs.c)

## What we are porting

`Python/codecs.c` (1708 lines): the codec registry and the
encode/decode dispatch layer that `str.encode()`, `bytes.decode()`,
and the import system's source-file reader all call into.

CPython's codec system is lookup-driven. Encodings are registered as
search functions via `codecs.register(search_fn)`. Each search
function is called with a normalised encoding name and returns either
`None` (not handled) or a `CodecInfo` four-tuple
`(encode, decode, incrementalencoder, incrementaldecoder)`.

For gopy v0.8, three built-in codecs must be available before the
import source reader can open `.py` files:

* `utf-8` / `utf_8` / `utf8` (any normalisation): the default source
  encoding.
* `ascii`: for source files declared with `# -*- coding: ascii -*-`.
* `latin-1` / `iso-8859-1` / `latin_1`: byte-identity mapping.

The codec registry lives on the interpreter state as
`interp->codecs.search_path` (a list of callables).

### Key CPython functions

| Function | Location |
|---|---|
| `PyCodec_Register` | `Python/codecs.c:31` |
| `_PyCodec_Lookup` | `Python/codecs.c:141` |
| `_PyCodec_LookupBuiltin` | `Python/codecs.c:92` |
| `codec_register` (Python-level) | `Python/codecs.c:57` |
| `PyCodec_Encode` | `Python/codecs.c:491` |
| `PyCodec_Decode` | `Python/codecs.c:504` |
| `_PyCodec_EncodeInternal` | `Python/codecs.c:435` |
| `_PyCodec_DecodeInternal` | `Python/codecs.c:458` |
| `PyCodec_RegisterError` | `Python/codecs.c:625` |
| `PyCodec_LookupError` | `Python/codecs.c:654` |
| `PyCodec_StrictErrors` | `Python/codecs.c:785` |
| `PyCodec_IgnoreErrors` | `Python/codecs.c:812` |
| `PyCodec_ReplaceErrors` | `Python/codecs.c:882` |
| `PyCodec_XMLCharRefReplaceErrors` | `Python/codecs.c:960` |
| `PyCodec_BackslashReplaceErrors` | `Python/codecs.c:1058` |
| `PyCodec_NameReplaceErrors` | `Python/codecs.c:1131` |
| `normalise_encoding` | `Python/codecs.c:125` |

### Name normalisation

`Python/codecs.c:125 normalise_encoding`: convert to lower-case,
replace hyphens and spaces with underscores, collapse leading/trailing
underscores. `"UTF-8"` normalises to `"utf_8"`. `"iso-8859-1"`
normalises to `"iso_8859_1"`.

## Go shape

```go
// CodecInfo holds the encode and decode functions for one codec.
// Mirrors the essential two slots of the CPython four-tuple CodecInfo.
// CPython: Python/codecs.c:141 _PyCodec_Lookup return value.
type CodecInfo struct {
    // Encode converts a string to bytes.
    // Returns (result object, bytes consumed, error).
    Encode func(obj objects.Object, errors string) (objects.Object, int, error)
    // Decode converts bytes to a string.
    // Returns (result object, bytes consumed, error).
    Decode func(obj objects.Object, errors string) (objects.Object, int, error)
}

// SearchFunc is a function that maps a normalised encoding name to
// a CodecInfo, or returns (nil, false) if it does not handle that name.
// Mirrors a Python-level search_function callable.
type SearchFunc func(encoding string) (*CodecInfo, bool)

// Register appends a search function to the codec search path.
// CPython: Python/codecs.c:31 PyCodec_Register
func Register(fn SearchFunc) error

// Lookup normalises the encoding name and walks the registered search
// functions until one returns a CodecInfo.
// Returns LookupError if no codec is found.
// CPython: Python/codecs.c:141 _PyCodec_Lookup
func Lookup(encoding string) (*CodecInfo, error)

// Encode encodes obj using the named codec and error handler.
// CPython: Python/codecs.c:491 PyCodec_Encode
func Encode(obj objects.Object, encoding, errors string) (objects.Object, error)

// Decode decodes obj using the named codec and error handler.
// CPython: Python/codecs.c:504 PyCodec_Decode
func Decode(obj objects.Object, encoding, errors string) (objects.Object, error)

// RegisterError registers a named error handler.
// CPython: Python/codecs.c:625 PyCodec_RegisterError
func RegisterError(name string, handler ErrorHandler) error

// LookupError returns the named error handler.
// Returns LookupError if not found.
// CPython: Python/codecs.c:654 PyCodec_LookupError
func LookupError(name string) (ErrorHandler, error)

// ErrorHandler is the Go type for a codec error callback.
// It receives the encode/decode error and returns a replacement
// (result string or bytes, resume position).
type ErrorHandler func(err error) (replacement objects.Object, pos int, rerr error)
```

## File mapping

| C source | Go target |
|---|---|
| `Python/codecs.c:31` `PyCodec_Register` | `codecs/registry.go` |
| `Python/codecs.c:141` `_PyCodec_Lookup` | `codecs/registry.go` |
| `Python/codecs.c:125` `normalise_encoding` | `codecs/registry.go` |
| `Python/codecs.c:491` `PyCodec_Encode` | `codecs/codec.go` |
| `Python/codecs.c:504` `PyCodec_Decode` | `codecs/codec.go` |
| `Python/codecs.c:435` `_PyCodec_EncodeInternal` | `codecs/codec.go` |
| `Python/codecs.c:458` `_PyCodec_DecodeInternal` | `codecs/codec.go` |
| `Python/codecs.c:625` `PyCodec_RegisterError` | `codecs/errors.go` |
| `Python/codecs.c:654` `PyCodec_LookupError` | `codecs/errors.go` |
| `Python/codecs.c:785` `PyCodec_StrictErrors` | `codecs/errors.go` |
| `Python/codecs.c:812` `PyCodec_IgnoreErrors` | `codecs/errors.go` |
| `Python/codecs.c:882` `PyCodec_ReplaceErrors` | `codecs/errors.go` |
| `Python/codecs.c:960` `PyCodec_XMLCharRefReplaceErrors` | `codecs/errors.go` |
| `Python/codecs.c:1058` `PyCodec_BackslashReplaceErrors` | `codecs/errors.go` |
| `Python/codecs.c:1131` `PyCodec_NameReplaceErrors` | `codecs/errors.go` |
| Built-in utf-8, ascii, latin-1 implementations | `codecs/builtin.go` |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### codecs/registry.go

* [ ] `searchPath`: package-level slice of `SearchFunc`, protected by a
  mutex for future thread safety. Initially empty; seeded by `init()`.
  CPython: `Python/codecs.c:141` `interp->codecs.search_path`.
* [ ] `normalizeEncoding(name string) string`: lower-case, replace `-`
  and ` ` with `_`. CPython: `Python/codecs.c:125 normalise_encoding`.
* [ ] `lookupCache`: `map[string]*CodecInfo` keyed by normalised name,
  cleared when a new search function is registered.
  CPython: `Python/codecs.c:141` `interp->codecs.search_cache`.
* [ ] `Register(fn SearchFunc) error`: append to `searchPath`, clear
  `lookupCache`. CPython: `Python/codecs.c:31 PyCodec_Register`.
* [ ] `Lookup(encoding string) (*CodecInfo, error)`: normalise name,
  check `lookupCache`, walk `searchPath`, populate cache on hit,
  return `LookupError` on miss.
  CPython: `Python/codecs.c:141 _PyCodec_Lookup`.
* [ ] `init()` in `codecs/registry.go`: call `Register` with the
  built-in search function from `codecs/builtin.go` that handles
  `utf_8`, `ascii`, `latin_1` (and their common aliases).

### codecs/errors.go

* [ ] `errorHandlers`: `map[string]ErrorHandler`, seeded by `init()`.
  CPython: `Python/codecs.c:625` `interp->codecs.error_registry`.
* [ ] `RegisterError(name string, handler ErrorHandler) error`: insert
  into `errorHandlers`. CPython: `Python/codecs.c:625 PyCodec_RegisterError`.
* [ ] `LookupError(name string) (ErrorHandler, error)`: look up
  `errorHandlers[name]`, return `LookupError` if absent.
  CPython: `Python/codecs.c:654 PyCodec_LookupError`.
* [ ] `strictErrors`: raise `UnicodeEncodeError` or `UnicodeDecodeError`
  immediately. CPython: `Python/codecs.c:785 PyCodec_StrictErrors`.
* [ ] `ignoreErrors`: return an empty string / empty bytes replacement
  and advance past the bad range.
  CPython: `Python/codecs.c:812 PyCodec_IgnoreErrors`.
* [ ] `replaceErrors` (encode): replace each un-encodable codepoint with
  `?` (0x3F). (Decode): replace each bad byte sequence with U+FFFD.
  CPython: `Python/codecs.c:882 PyCodec_ReplaceErrors`.
* [ ] `xmlcharrefreplace`: replace un-encodable codepoints with
  `&#N;` decimal entity references.
  CPython: `Python/codecs.c:960 PyCodec_XMLCharRefReplaceErrors`.
* [ ] `backslashreplace`: replace un-encodable or un-decodable ranges
  with `\xNN`, `\uNNNN`, or `\UNNNNNNNN` escape sequences.
  CPython: `Python/codecs.c:1058 PyCodec_BackslashReplaceErrors`.
* [ ] `namereplace`: replace un-encodable codepoints with
  `\N{UNICODE NAME}`. CPython: `Python/codecs.c:1131 PyCodec_NameReplaceErrors`.
* [ ] `init()` in `codecs/errors.go`: seed `errorHandlers` with
  `"strict"`, `"ignore"`, `"replace"`, `"xmlcharrefreplace"`,
  `"backslashreplace"`, `"namereplace"`, `"surrogateescape"` (stub),
  `"surrogatepass"` (stub).

### codecs/codec.go

* [ ] `Encode(obj objects.Object, encoding, errors string) (objects.Object, error)`:
  call `Lookup(encoding)`, then `info.Encode(obj, errors)`.
  CPython: `Python/codecs.c:491 PyCodec_Encode` via
  `Python/codecs.c:435 _PyCodec_EncodeInternal`.
* [ ] `Decode(obj objects.Object, encoding, errors string) (objects.Object, error)`:
  call `Lookup(encoding)`, then `info.Decode(obj, errors)`.
  CPython: `Python/codecs.c:504 PyCodec_Decode` via
  `Python/codecs.c:458 _PyCodec_DecodeInternal`.
* [ ] Both entry points must call `LookupError(errors)` if the codec
  signals a partial error and re-invoke the error handler in a loop
  until all input is consumed or an error is raised.
  CPython: `Python/codecs.c:435 _PyCodec_EncodeInternal` handler loop.
* [ ] Return type is the first element of the codec result tuple (the
  encoded/decoded object); discard the integer consumed count at this
  level. CPython: `Python/codecs.c:491` result extraction.

### codecs/builtin.go

* [ ] `utf8Codec`: `CodecInfo` backed by Go's `unicode/utf8` package.
  * Encode: `[]byte(s)` for a valid UTF-8 `*objects.Str`; invoke error
    handler for surrogates depending on the `errors` mode.
  * Decode: `string(b)` after validating UTF-8 with
    `utf8.Valid`; invoke error handler on invalid byte sequences.
* [ ] `asciiCodec`: reject any byte > 0x7F on decode, any codepoint >
  0x7F on encode. Invoke the error handler for offending ranges.
* [ ] `latin1Codec`: byte-identity mapping (codepoint N maps to byte N
  for 0..255). No error handler needed for encode; every Python
  codepoint <= 255 is representable.
* [ ] `builtinSearch(name string) (*CodecInfo, bool)`: return the
  appropriate `CodecInfo` for the following normalised names:
  `utf_8`, `utf8`, `u8`, `ascii`, `us_ascii`, `646`,
  `latin_1`, `latin1`, `iso8859_1`, `iso_8859_1`, `iso_8859_1_`,
  `8859`. Return `(nil, false)` for anything else.
* [ ] `init()` in `codecs/builtin.go`: call `Register(builtinSearch)`.

### Surface guarantees

* [ ] `codecs.Encode(objects.NewStr("hello"), "utf-8", "strict")` returns
  `b"hello"` as `*objects.Bytes`.
* [ ] `codecs.Decode(objects.NewBytes([]byte{104,101,108,108,111}), "utf-8", "strict")`
  returns `"hello"` as `*objects.Str`.
* [ ] Encoding `"\xff"` with `"ascii"` and `errors="strict"` returns
  a `UnicodeEncodeError`.
* [ ] Encoding `"\xff"` with `"ascii"` and `errors="ignore"` returns
  `b""`.
* [ ] Encoding `"\xff"` with `"ascii"` and `errors="replace"` returns
  `b"?"`.
* [ ] Decoding `b"\xff"` with `"utf-8"` and `errors="replace"` returns
  `"�"`.
* [ ] `codecs.Lookup("UTF-8")` and `codecs.Lookup("utf_8")` and
  `codecs.Lookup("utf8")` all return the same `*CodecInfo`.
* [ ] `RegisterError` / `LookupError` round-trip: a custom handler
  registered under `"myhandler"` is returned by `LookupError("myhandler")`.
* [ ] Registering a new search function clears the lookup cache so
  subsequent `Lookup` calls invoke all registered functions.

### Tests

* [ ] `codecs/codecs_test.go`:
  * `Encode("hello", "utf-8", "strict")` matches `b"hello"`.
  * `Encode("hello", "ascii", "strict")` matches `b"hello"`.
  * `Encode("é", "latin-1", "strict")` matches `b"\xe9"`.
  * `Decode(b"hello", "utf-8", "strict")` matches `"hello"`.
  * `Encode("Ā", "ascii", "strict")` returns `UnicodeEncodeError`.
  * `Encode("Ā", "ascii", "ignore")` returns `b""`.
  * `Encode("Ā", "ascii", "replace")` returns `b"?"`.
  * `Encode("Ā", "ascii", "xmlcharrefreplace")` returns `b"&#256;"`.
  * `Encode("Ā", "ascii", "backslashreplace")` returns `b"\\u0100"`.
  * `Decode(b"\xff", "utf-8", "replace")` returns `"�"`.
  * `Decode(b"\xff", "utf-8", "ignore")` returns `""`.
* [ ] `codecs/errors_test.go`:
  * `RegisterError("myhandler", fn)` then `LookupError("myhandler")` returns `fn`.
  * `LookupError("nonexistent")` returns an error.
  * `LookupError("strict")` returns the built-in strict handler.
* [ ] `codecs/registry_test.go`:
  * `Lookup("UTF-8")` succeeds.
  * `Lookup("utf_8")` succeeds and returns same codec as `"UTF-8"`.
  * `Lookup("unknown-encoding-xyz")` returns an error.
  * Custom `Register` adds a new codec; subsequent `Lookup` finds it.
  * Registering a new function clears the cache; re-lookup calls the
    new function.

## Cross-references

* `str.encode` and `bytes.decode` methods on `objects.Str` and
  `objects.Bytes` call `codecs.Encode` / `codecs.Decode`: 1676, 1677.
* Import source reader uses `codecs.Decode("utf-8", ...)` to read
  `.py` files: 1691 (`imp/loader.go`).
* `UnicodeEncodeError` / `UnicodeDecodeError` exception types: 1686.
* The `codecs` stdlib module (Python surface) bridges through the
  import system: 1691. That bridge is not part of this spec.

## Out of scope

* Incremental encoder / decoder interface (`IncrementalEncoder`,
  `IncrementalDecoder`). Needed by `io.TextIOWrapper`; deferred to
  the io/ port.
* `StreamReader` / `StreamWriter`. Same deferral.
* Charmap-based codecs (`cp1252`, `cp437`, `cp850`, etc.). Deferred
  to the encodings/ stdlib bridge.
* UTF-16 and UTF-32 with BOM handling. Deferred.
* `surrogateescape` and `surrogatepass` full implementations. Stubbed
  (raise NotImplementedError) until the io/ port needs them.
* The `encodings/` stdlib package lookup path. That requires the import
  system (1691) to load Python source; it is a follow-on task after
  v0.8.
* The `codecs` Python module's `open()`, `iterencode()`,
  `iterdecode()` functions. Stdlib bridge, not part of
  `Python/codecs.c`.
