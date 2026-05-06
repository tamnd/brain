---
title: "gopy marshal"
description: "Port of cpython/Python/marshal.c (2163 lines) to the marshal/ package. Full type-tag dispatch, TYPE_LONG arbitrary-precision encoding, FLAG_REF back-reference dedup, TYPE_CODE read/write, and .pyc file header. Gates the v0.8 milestone."
tags: ["gopy", "spec"]
weight: 1690
---

# 1690. marshal (Python/marshal.c)

## What we are porting

`Python/marshal.c` (2163 lines): the binary serialisation format that
Python uses for .pyc bytecode files, `marshal.dumps` / `marshal.loads`,
and the compile-time constant pool. Every .pyc file is a 16-byte header
followed by a marshalled code object.

The existing `marshal/marshal.go` skeleton (v0.5) handles None, bool,
int (TYPE_INT), float (binary), str, bytes, tuple, and list. The
following are missing and must land in v0.8:

* TYPE_LONG: arbitrary-precision integers encoded as base-2^15 limbs.
* FLAG_REF (0x80 on any tag): back-reference dedup that lets cyclic or
  repeated objects be stored once and referred to by index.
* TYPE_INTERNED / TYPE_ASCII_INTERNED / TYPE_SHORT_ASCII_INTERNED:
  interned string variants used heavily in code objects.
* TYPE_CODE: the full code-object round-trip needed to run .pyc files.
* TYPE_COMPLEX / TYPE_BINARY_COMPLEX: complex number encoding.
* TYPE_SET / TYPE_FROZENSET: set types.
* TYPE_DICT: dictionary.
* .pyc file header: 16 bytes of magic + flags + source stamp +
  marshal blob, validated on read.

The v0.8 gate is `import json; json.dumps({"a": 1})`, which requires
loading a .pyc file containing a code object for `json/__init__.py`.

## Key CPython functions

| C item | Location |
|---|---|
| `w_object` main write dispatch | `Python/marshal.c:459` |
| `w_complex_object` FLAG_REF wrap | `Python/marshal.c:356` |
| `w_long` TYPE_LONG encode | `Python/marshal.c:201` |
| `w_short_pstring` / `w_pstring` | `Python/marshal.c:168` |
| `r_object` main read dispatch | `Python/marshal.c:1159` |
| `r_object` FLAG_REF read path | `Python/marshal.c:1022` |
| `r_long` TYPE_LONG decode | `Python/marshal.c:937` |
| `PyMarshal_ReadLastObjectFromFile` | `Python/marshal.c:1807` |
| `PyMarshal_WriteObjectToString` | `Python/marshal.c:1928` |
| `PyMarshal_ReadObjectFromString` | `Python/marshal.c:1876` |

Type tags (full set, matching `Python/marshal.c:58-110`):

| Tag | Char | Notes |
|-----|------|-------|
| TYPE_NULL | `'0'` | |
| TYPE_NONE | `'N'` | |
| TYPE_FALSE | `'F'` | |
| TYPE_TRUE | `'T'` | |
| TYPE_STOPITER | `'S'` | |
| TYPE_ELLIPSIS | `'.'` | |
| TYPE_INT | `'i'` | 32-bit signed |
| TYPE_INT64 | `'I'` | 64-bit signed (Python 2 compat) |
| TYPE_FLOAT | `'f'` | ASCII float |
| TYPE_BINARY_FLOAT | `'g'` | IEEE 754 little-endian double |
| TYPE_LONG | `'l'` | base-2^15 limbs |
| TYPE_STRING | `'s'` | bytes |
| TYPE_TUPLE | `'('` | |
| TYPE_SMALL_TUPLE | `')'` | 1-byte length prefix |
| TYPE_LIST | `'['` | |
| TYPE_DICT | `'{'` | |
| TYPE_CODE | `'c'` | code object |
| TYPE_UNICODE | `'u'` | |
| TYPE_SHORT_ASCII | `'z'` | 1-byte length prefix |
| TYPE_SHORT_ASCII_INTERNED | `'Z'` | interned |
| TYPE_ASCII | `'a'` | 4-byte length prefix |
| TYPE_ASCII_INTERNED | `'A'` | interned |
| TYPE_REF | `'r'` | back-reference |
| TYPE_COMPLEX | `'y'` | ASCII re+im |
| TYPE_BINARY_COMPLEX | `'Y'` | two IEEE 754 doubles |
| TYPE_SET | `'<'` | |
| TYPE_FROZENSET | `'>'` | |

FLAG_REF = 0x80 ORed onto any tag byte. When writing: if the object
has been registered for reference tracking, OR its reference count is
greater than 1, set FLAG_REF and record an index in the ref table
before recursing. On reading: if FLAG_REF bit is set, pre-allocate a
slot in the decoder ref list, fill in the decoded object after
construction. TYPE_REF `'r'` reads a 4-byte index and returns the
stored object.

TYPE_LONG encoding (`Python/marshal.c:201`): the absolute value is
split into base-2^15 digits in little-endian order. The digit count is
stored as a signed 32-bit integer; negative count signals a negative
number. Each digit is a uint16 in little-endian.

.pyc header (16 bytes, `Python/importlib/_bootstrap_external.py`):

```
uint32 magic_number   // PYC_MAGIC_NUMBER_TOKEN for 3.14, pinned as const
uint32 bit_flags      // bit 0: checked; bit 1: source-hash mode
uint32 field2         // source mtime (timestamp mode) or source_hash[0:4] (hash mode)
uint32 field3         // source size (timestamp mode) or source_hash[4:8] (hash mode)
// followed immediately by the marshalled code object
```

## Go shape

```go
// WriteCodeToString marshals a code object to bytes at the given version.
// CPython: Python/marshal.c:1928 PyMarshal_WriteObjectToString
func WriteCodeToString(code *objects.Code, version int) ([]byte, error)

// ReadCodeFromBytes unmarshals a code object from raw marshal bytes (no pyc header).
// CPython: Python/marshal.c:1876 PyMarshal_ReadObjectFromString
func ReadCodeFromBytes(data []byte) (*objects.Code, error)

// WritePyc writes a complete .pyc file: 16-byte header then marshalled code.
// flags: bit 0 = checked, bit 1 = source-hash mode.
// sourceHash is used when bit 1 is set; mtime+size when bit 1 is clear.
func WritePyc(w io.Writer, code *objects.Code, flags uint32, mtime uint32, size uint32, sourceHash uint64) error

// ReadPyc reads and validates a .pyc file header then returns the code object.
// Returns an error if the magic number does not match or the source stamp is stale.
func ReadPyc(r io.Reader, expectedMtime uint32, expectedSize uint32, expectedSourceHash uint64) (*objects.Code, error)

// Dumps serialises obj to bytes (marshal.dumps equivalent).
// CPython: Python/marshal.c:1928 PyMarshal_WriteObjectToString
func Dumps(obj objects.Object, version int) ([]byte, error)

// Loads deserialises bytes to an object (marshal.loads equivalent).
// CPython: Python/marshal.c:1876 PyMarshal_ReadObjectFromString
func Loads(data []byte) (objects.Object, error)
```

## File mapping

| C source | Go target |
|---|---|
| `Python/marshal.c` `w_object` full dispatch | `marshal/write.go` (replaces encoder in marshal.go) |
| `Python/marshal.c` `r_object` full dispatch | `marshal/read.go` (replaces decoder in marshal.go) |
| `Python/marshal.c:201` TYPE_LONG encode/decode | `marshal/long.go` |
| `Python/marshal.c:356` FLAG_REF writer, ref table | `marshal/refs.go` |
| `Python/marshal.c:1022` FLAG_REF reader | `marshal/refs.go` |
| `Python/marshal.c:1807` pyc header read | `marshal/pyc.go` |
| `Python/marshal.c:1928` pyc header write | `marshal/pyc.go` |
| Existing skeleton | `marshal/marshal.go` (shrinks to package doc + Dumps/Loads wrappers) |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### TYPE_LONG (marshal/long.go)

* [ ] `writeLong`: split `*big.Int` absolute value into base-2^15 uint16
  limbs, little-endian. Emit signed 32-bit count (negative = negative
  number). CPython: `Python/marshal.c:201 w_long`.
* [ ] `readLong`: read signed 32-bit count, read `|count|` uint16 limbs,
  reconstruct `*big.Int`, apply sign from count sign.
  CPython: `Python/marshal.c:937 r_long`.
* [ ] Zero `big.Int` encodes as count=0 with no limbs.
* [ ] Negative numbers encode as negative count (not two's complement).
* [ ] Round-trip property: `readLong(writeLong(n)) == n` for arbitrary
  `*big.Int`.

### FLAG_REF (marshal/refs.go)

* [ ] `writerRefs`: map from `objects.Object` identity to pre-assigned
  32-bit index. Populated during `w_complex_object` when an object is
  seen more than once or is flagged for interning.
  CPython: `Python/marshal.c:356 w_complex_object`.
* [ ] Write path: before writing a compound object, check if it needs a
  ref slot; if so, OR FLAG_REF (0x80) onto the tag byte and record
  `len(refs)` as the slot index.
* [ ] `readerRefs`: growable slice of `objects.Object`, indexed by
  order of first appearance.
* [ ] Read path: if FLAG_REF bit is set on the tag, pre-allocate slot
  (`append(refs, nil)`) before decoding; after decoding, store the
  result at that slot. CPython: `Python/marshal.c:1022`.
* [ ] TYPE_REF (`'r'`): read 4-byte little-endian index, return
  `refs[index]`. Error if index out of range.
  CPython: `Python/marshal.c:1159` REF arm.

### TYPE_INTERNED string variants (marshal/write.go, marshal/read.go)

* [ ] Write TYPE_SHORT_ASCII_INTERNED (`'Z'`) for interned strings
  shorter than 256 bytes. CPython: `Python/marshal.c:459 w_object`
  unicode arm.
* [ ] Write TYPE_ASCII_INTERNED (`'A'`) for interned strings >= 256
  bytes. CPython: `Python/marshal.c:459 w_object`.
* [ ] Write TYPE_SHORT_ASCII (`'z'`) for non-interned ASCII strings
  shorter than 256 bytes.
* [ ] Write TYPE_ASCII (`'a'`) for non-interned ASCII strings >= 256
  bytes.
* [ ] Write TYPE_UNICODE (`'u'`) for non-ASCII strings (UTF-8 encoded,
  4-byte length).
* [ ] Read path: TYPE_ASCII_INTERNED and TYPE_SHORT_ASCII_INTERNED add
  the decoded string to the interned-string table (the decoder's
  `strings` slice). CPython: `Python/marshal.c:1159` string arms.

### TYPE_CODE (marshal/write.go, marshal/read.go)

* [ ] Write TYPE_CODE: emit tag, then all `objects.Code` fields in the
  exact CPython order (`Python/marshal.c:459 w_object` code arm):
  argcount, posonlyargcount, kwonlyargcount, stacksize, flags,
  code (bytes), consts (tuple), names (tuple), localsplusnames (tuple),
  localspluskinds (bytes), filename (str), name (str), qualname (str),
  firstlineno (int), linetable (bytes), exceptiontable (bytes).
* [ ] Read TYPE_CODE: reconstruct `objects.Code` from the same field
  sequence. CPython: `Python/marshal.c:1159` code arm.
* [ ] Field order must match CPython 3.14 exactly; any mismatch
  produces an unreadable .pyc file.
* [ ] CODE_FIELD_COUNT constant (16 for 3.14) guards against accidental
  field reordering in the writer.

### TYPE_COMPLEX (marshal/write.go, marshal/read.go)

* [ ] Write TYPE_BINARY_COMPLEX (`'Y'`): real then imag, each as
  IEEE 754 little-endian double (8 bytes each).
  CPython: `Python/marshal.c:459 w_object` complex arm.
* [ ] Read TYPE_BINARY_COMPLEX: two 8-byte IEEE 754 doubles.
  CPython: `Python/marshal.c:1159` binary-complex arm.
* [n] TYPE_COMPLEX ASCII form (`'y'`): deferred to v0.9 with full
  complex number support.

### TYPE_SET / TYPE_FROZENSET (marshal/write.go, marshal/read.go)

* [ ] Write TYPE_SET (`'<'`): 4-byte count then each element.
  CPython: `Python/marshal.c:459 w_object` set arm.
* [ ] Write TYPE_FROZENSET (`'>'`): same layout.
* [ ] Read TYPE_SET / TYPE_FROZENSET: count then elements, reconstruct
  `*objects.Set` or `*objects.FrozenSet`.
  CPython: `Python/marshal.c:1159` set/frozenset arm.
* [ ] Empty frozenset uses FLAG_REF dedup (CPython interns it).

### TYPE_DICT (marshal/write.go, marshal/read.go)

* [ ] Write TYPE_DICT (`'{'`): interleaved key, value pairs terminated
  by a NULL byte (the `w_object(NULL)` sentinel).
  CPython: `Python/marshal.c:459 w_object` dict arm.
* [ ] Read TYPE_DICT: read key/value pairs until NULL sentinel is read.
  CPython: `Python/marshal.c:1159` dict arm.

### .pyc header (marshal/pyc.go)

* [ ] `MagicNumber` constant pinned to CPython 3.14's
  `PYC_MAGIC_NUMBER_TOKEN` value (3495 * 10 + 13 = 34963, stored as
  `magic | (b'\r\n' << 16)`). CPython: `Python/import.c` magic
  generation and `Lib/importlib/_bootstrap_external.py`.
* [ ] `WritePyc`: write 4 uint32s (magic, flags, field2, field3) then
  call `WriteCodeToString` and write the blob.
* [ ] `ReadPyc`: read 4 uint32s; reject on magic mismatch (raise
  `ImportError`); validate timestamp or source-hash depending on
  bit 1 of flags; then call `ReadCodeFromBytes`.
* [ ] Timestamp mode (flags bit 1 clear): field2 = source mtime,
  field3 = source size. Stale if either mismatches.
* [ ] Source-hash mode (flags bit 1 set): field2/field3 = 64-bit
  source hash split little-endian. Stale if hash mismatches.
* [ ] Unchecked mode (flags bit 0 clear): skip validation entirely.
  CPython: `Lib/importlib/_bootstrap_external.py _validate_bytecode_header`.

### Write dispatch completeness (marshal/write.go)

* [ ] `w_object` handles all 27 type tags listed in the type-tag table.
* [x] TYPE_NONE, TYPE_TRUE, TYPE_FALSE: already in skeleton.
* [x] TYPE_INT (32-bit): already in skeleton.
* [ ] TYPE_INT64: emit when int fits in int64 but not int32
  (Python 2 compat path). CPython: `Python/marshal.c:459`.
* [x] TYPE_BINARY_FLOAT: already in skeleton.
* [x] TYPE_STRING (bytes): already in skeleton.
* [x] TYPE_SMALL_TUPLE / TYPE_TUPLE: already in skeleton.
* [x] TYPE_LIST: already in skeleton.
* [ ] TYPE_LONG: delegate to `marshal/long.go writeLong`.
* [ ] TYPE_DICT: as above.
* [ ] TYPE_CODE: as above.
* [ ] TYPE_BINARY_COMPLEX: as above.
* [ ] TYPE_SET / TYPE_FROZENSET: as above.
* [ ] TYPE_ELLIPSIS (`'.'`): singleton write.
* [ ] TYPE_STOPITER (`'S'`): singleton write.
* [ ] TYPE_NULL (`'0'`): internal sentinel; never called from user code.

### Read dispatch completeness (marshal/read.go)

* [ ] `r_object` handles all 27 type tags.
* [x] TYPE_NONE, TYPE_TRUE, TYPE_FALSE: already in skeleton.
* [x] TYPE_INT: already in skeleton.
* [ ] TYPE_INT64: read 8 bytes, return `*objects.Long`.
* [x] TYPE_BINARY_FLOAT: already in skeleton.
* [ ] TYPE_FLOAT ASCII form: parse ASCII float string.
  CPython: `Python/marshal.c:1159` float arm.
* [x] TYPE_STRING (bytes): already in skeleton.
* [x] TYPE_SMALL_TUPLE, TYPE_TUPLE: already in skeleton.
* [x] TYPE_LIST: already in skeleton.
* [ ] TYPE_UNICODE (`'u'`): 4-byte length, UTF-8 bytes.
* [ ] TYPE_SHORT_ASCII, TYPE_ASCII: as above (non-interned).
* [ ] TYPE_SHORT_ASCII_INTERNED, TYPE_ASCII_INTERNED: intern on read.
* [ ] TYPE_LONG: delegate to `marshal/long.go readLong`.
* [ ] TYPE_DICT: as above.
* [ ] TYPE_CODE: as above.
* [ ] TYPE_BINARY_COMPLEX: as above.
* [ ] TYPE_SET / TYPE_FROZENSET: as above.
* [ ] TYPE_REF: index into ref slice.
* [ ] TYPE_ELLIPSIS: return `objects.Ellipsis`.
* [ ] TYPE_STOPITER: return `objects.StopIteration` singleton.
* [ ] TYPE_NULL: return nil (internal sentinel).

### Tests

* [ ] `marshal/marshal_test.go`: `Dumps` then `Loads` round-trip for
  every supported type tag (None, bool, int, big.Int, float, bytes,
  str, tuple, list, dict, set, frozenset, code object).
* [ ] `marshal/marshal_test.go`: byte-for-byte match against
  `python3 -c "import marshal, sys; sys.stdout.buffer.write(marshal.dumps(42))"` for
  int, float, str, bytes, and a simple tuple.
* [ ] `marshal/marshal_test.go`: code-object round-trip: compile a
  trivial Python source, marshal the code object, unmarshal it, verify
  `co_consts`, `co_names`, `co_filename`, `co_firstlineno`.
* [ ] `marshal/long_test.go`: round-trip for `big.Int` values 0,
  1, -1, 2^15, 2^31, 2^63, 2^128, -(2^128).
* [ ] `marshal/refs_test.go`: object shared between two tuple slots is
  written once with FLAG_REF and read back as the same pointer.
* [ ] `marshal/pyc_test.go`: `WritePyc` then `ReadPyc` round-trip in
  timestamp mode; source-hash mode; stale-magic rejection; stale-mtime
  rejection.

## Cross-references

* Code object definition: 1687 (`objects/code.go`). The marshal writer
  reads every field of `objects.Code`; the reader constructs one.
* Import system that reads .pyc files: 1691 (`imp/loader.go` calls
  `marshal.ReadPyc`).
* Compile pipeline that produces Code objects: 1620 series.
* objects/set.go, objects/dict.go: 1680, 1681 (needed by TYPE_SET,
  TYPE_FROZENSET, TYPE_DICT read paths).

## Out of scope

* TYPE_COMPLEX ASCII form (`'y'`). Lands in v0.9 with full complex
  numbers.
* TYPE_FRAME, TYPE_ELLIPSIS, TYPE_STOPITER object construction. The
  tags are written; the resulting objects land with their respective
  types in later phases.
* Pickle compatibility differences for marshal version < 4 interning
  behaviour.
* The `marshal` Python module surface (`marshal.version`,
  `marshal.MAGIC_NUMBER`). Lands with the stdlib bridge.
* Free-threaded write-barrier integration. gopy is single-threaded
  through v0.10.
