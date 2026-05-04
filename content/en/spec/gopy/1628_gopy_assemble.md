---
title: "gopy assemble"
description: "Detailed port plan for cpython/Python/assemble.c (~800 lines) to compile/assemble.go. Sequence-to-Code conversion, line table varint format, exception table varint format, co_consts/names/varnames/freevars/cellvars layout, fastlocalskinds, comprehensive test plan."
tags: ["gopy", "spec"]
weight: 1628
---

# 1628. Assemble

Port of `cpython/Python/assemble.c` (802 lines) to
`gopy/compile/assemble.go`. This spec is the detailed source-of-truth
for section 8 of 1620.

## What assemble does

Assemble takes the optimised `instrseq.Sequence` from flowgraph (1627)
plus the per-unit metadata from codegen (1626) and produces a final
`*objects.Code` ready to hand to the VM (1630) or to marshal to a
`.pyc` file (1623).

The work is mostly serialisation. There are no further optimisations.
Three byte streams come out:

1. `co_code`: instruction stream packed as `_Py_CODEUNIT` (one byte
   opcode + one byte oparg, with EXTENDED_ARG widening for args > 255).
2. `co_linetable`: PEP 626 location table in the 3.14 varint encoding.
3. `co_exceptiontable`: PEP 657 exception handler table in varint form.

Plus the materialised pools:

- `co_consts`: tuple of constant objects.
- `co_names`: tuple of identifier strings (LOAD_GLOBAL / LOAD_ATTR targets).
- `co_varnames`: tuple of local variable names (parameters first).
- `co_freevars`: tuple of names captured from outer scopes.
- `co_cellvars`: tuple of names that are cells in this scope.
- `co_localsplusnames` and `co_localspluskinds`: 3.11+ flat layout.
- `co_qualname`, `co_name`, `co_filename`, `co_firstlineno`,
  `co_argcount`, `co_posonlyargcount`, `co_kwonlyargcount`,
  `co_stacksize`, `co_flags`, `co_nlocals`.

Boundary contract:

```
Input:
  *instrseq.Sequence (post-flowgraph)
  *flowgraph.Info (max stackdepth, exception table entries)
  *codegen.Unit (consts, names, varnames, freevars, cellvars, flags)
  filename string

Output:
  *objects.Code (ready for marshal or VM)
```

## File layout

`compile/assemble.go` is small enough to fit in two files:

| Go file                  | CPython lines  | Contents                                               |
|--------------------------|----------------|--------------------------------------------------------|
| `assemble.go`            | 1-200, 460-779 | `Assembler` struct, init, `Assemble` public entry, code-stream emit, code object construction |
| `assemble_locations.go`  | 196-368        | location-info varint emit (PEP 626 4-bit panel)        |
| `assemble_exceptions.go` | 89-194         | exception-table varint emit (PEP 657 panel)            |
| `assemble_consts.go`     | 457-573        | co_consts dedup, co_names / co_varnames materialisation |

Each function carries `// CPython: assemble.c:L<n> <name>`.

## Public surface

```go
package compile

// Assemble builds a final Code object from the post-flowgraph Sequence
// plus per-unit metadata.
func Assemble(seq *instrseq.Sequence, fg *flowgraph.Info, unit *Unit, filename string) (*objects.Code, error)

// Assembler is the per-call state. Public only so tests can drive
// individual phases.
type Assembler struct {
    Filename     string
    FirstLineno  int
    InstrSize    int          // byte length of the code stream
    Code         []byte       // co_code
    LineTable    []byte       // co_linetable
    ExceptionTable []byte     // co_exceptiontable
}
```

The `Unit` type is the same struct codegen produced (1626 spec). It
already carries every list assemble needs.

## Code stream emission

`writeInstr` (assemble.c:369-411) packs each instruction into the
`_Py_CODEUNIT` format. CPython 3.14:

```
| opcode (1 byte) | oparg (1 byte) | inline cache (variable) |
```

Opargs > 255 widen via EXTENDED_ARG prefixes; up to three prefixes
gives a 32-bit oparg. The number of cache lines per opcode is fixed
per opcode (the table is in `compile/opcodes_gen.go` from the 1620
section 4 generator).

Algorithm:

```go
func (a *Assembler) emitInstr(instr *Instr) error {
    arg := instr.Oparg
    extended := []int{}
    for arg > 0xff {
        extended = append([]int{arg & 0xff}, extended...)
        arg >>= 8
    }
    for _, ea := range extended {
        a.Code = append(a.Code, EXTENDED_ARG, byte(ea))
    }
    a.Code = append(a.Code, byte(instr.Opcode), byte(arg & 0xff))
    // pad inline caches with zero bytes
    caches := opmeta.CacheCount(instr.Opcode)
    for i := 0; i < caches; i++ {
        a.Code = append(a.Code, 0, 0) // each cache entry is one CODEUNIT
    }
    return nil
}
```

Line and exception entries reference byte offsets into `co_code` so
they emit *after* the code stream is finalised.

## Line table (PEP 626)

The location table is a varint stream with a 4-bit "code" field
selecting one of five record formats. CPython:
assemble.c:196-336.

Record formats (3.14):

- **Code 0-9**: short form, 1-line span, fits in two bytes.
- **Code 10**: one-line form, line delta in next varint, columns in
  next two varints.
- **Code 11**: no-column form (start_line and end_line, no columns).
- **Code 13**: long form (full lineno / col / end_lineno / end_col as
  signed varints).
- **Code 15**: no-location.

Encoding helpers:

```go
func writeLocByte(a *Assembler, b byte) { a.LineTable = append(a.LineTable, b) }

func writeVarint(a *Assembler, v uint32) {
    for v >= 0x40 {
        writeLocByte(a, byte(v) & 0x3f | 0x40)
        v >>= 6
    }
    writeLocByte(a, byte(v) & 0x3f)
}

func writeSignedVarint(a *Assembler, v int32) {
    if v < 0 {
        writeVarint(a, uint32(-v) << 1 | 1)
    } else {
        writeVarint(a, uint32(v) << 1)
    }
}
```

`writeLocationInfoEntry` (assemble.c:286-322) picks the smallest form:

```go
func writeLocInfoEntry(a *Assembler, loc ast.Pos, isize int) {
    if loc == nil || loc.Lineno < 0 {
        writeLocInfoNone(a, isize); return
    }
    lineDelta := loc.Lineno - a.lineCursor
    sameLine := loc.EndLineno == loc.Lineno
    if sameLine && loc.ColOffset >= 0 && loc.EndColOffset >= 0 &&
       loc.ColOffset < 80 && (loc.EndColOffset - loc.ColOffset) < 16 &&
       lineDelta == 0 && isize <= 8 {
        writeLocInfoShortForm(a, isize, loc.ColOffset, loc.EndColOffset)
    } else if sameLine && loc.ColOffset >= 0 && loc.EndColOffset >= 0 &&
              isize <= 8 && lineDelta >= 0 && lineDelta < 8 {
        writeLocInfoOnelineForm(a, isize, lineDelta, loc.ColOffset, loc.EndColOffset)
    } else if loc.ColOffset == -1 && loc.EndColOffset == -1 {
        writeLocInfoNoColumn(a, isize, lineDelta)
    } else {
        writeLocInfoLongForm(a, loc, isize)
    }
    a.lineCursor = loc.Lineno
}
```

Test panel: `compile/assemble_loc_test.go`. Required cases:

- [ ] all-same-line range (short form)
- [ ] one-line delta (oneline form)
- [ ] no-column (no-column form)
- [ ] full long form
- [ ] none / -1 sentinel
- [ ] every record at a code-stream offset that crosses an isize boundary

## Exception table (PEP 657)

Varint records: `start_offset / end_offset / target_offset / depth_lasti`.
CPython: assemble.c:106-194.

```
struct ExceptHandler {
    Start  uint32  // byte offset into co_code, inclusive
    End    uint32  // byte offset into co_code, exclusive
    Target uint32  // byte offset of the handler entry
    Depth  uint8   // stack depth
    Lasti  bool    // PEP 657 push-lasti bit
}

byte 0 of each entry has the MSB set; subsequent bytes do not (so a
parser can find entry boundaries).
```

`assembleExceptionTableEntry` collapses adjacent runs that share
target / depth / lasti into a single entry. The ordering is by start
offset ascending.

Tests in `compile/assemble_except_test.go`:

- [ ] single entry (try-except)
- [ ] two entries with shared target (or-pattern)
- [ ] nested try (entries with same handler but different depth)
- [ ] try in generator (lasti=true)
- [ ] empty table (function with no exception handlers)

## Pool materialisation

### co_consts

`Unit.Consts` is already deduped by codegen (1626) and trimmed by
flowgraph's `removeUnusedConsts` (1627). Assemble just freezes it into
a tuple. CPython freezes via `PyTuple_Pack`; we use a `[]any` and let
the marshal package (1623) handle wire encoding.

### co_names / co_varnames / co_freevars / co_cellvars

Each is a deduplicated insertion-ordered string list. `Unit` already
carries them in the right order (codegen built them). Assemble copies
the slice into the Code object.

### co_localsplus and co_localspluskinds

Flat layout (3.11+). For a function with `argcount=2`, `kwonly=0`,
`varargs=0`, `varkw=0`, two cells, one free var:

```
co_localsplus = [arg0, arg1, local0, local1, cell0, cell1, free0]
co_localspluskinds = [
    FAST_LOCAL,        // arg0
    FAST_LOCAL,        // arg1
    FAST_LOCAL,        // local0
    FAST_LOCAL,        // local1
    FAST_CELL,         // cell0
    FAST_CELL,         // cell1
    FAST_FREE,         // free0
]
```

`FAST_HIDDEN` bit is OR'd in for synthetic locals (lambda implicit
arg, comprehension `.0` parameter). The flag values match CPython's
`pycore_code.h`:

```go
const (
    FastLocal  uint8 = 0x20
    FastCell   uint8 = 0x40
    FastFree   uint8 = 0x80
    FastHidden uint8 = 0x10
)
```

CPython: assemble.c:483-572.

## Code object construction

`AssembleCodeObject` (assemble.c:574-672) packs everything into a
`PyCodeObject`:

```go
return &objects.Code{
    Argcount:        unit.Argcount,
    PosOnlyArgCount: unit.PosOnlyArgCount,
    KwOnlyArgCount:  unit.KwOnlyArgCount,
    NLocals:         len(unit.VarNames),
    Stacksize:       fg.MaxStackDepth,
    Flags:           unit.Flags,
    Code:            a.Code,
    Consts:          unit.Consts,
    Names:           unit.Names,
    LocalsPlusNames: localsplusnames,
    LocalsPlusKinds: localspluskinds,
    Filename:        filename,
    Name:            unit.Name,
    Qualname:        unit.Qualname,
    Firstlineno:     unit.FirstLineno,
    Linetable:       a.LineTable,
    ExceptionTable:  a.ExceptionTable,
}
```

`objects.Code` is owned by the 1700-series spec (objects). For v0.5
we only need a shape that 1623 marshal can serialise. Mark the
`objects.Code` struct as a forward declaration in the 1620 spec; the
full port lands when objects/codeobject.c is in scope.

## Comprehensive test plan

### Layer 1: Per-pass unit

For every function in this spec, one unit test under
`compile/assemble_*_test.go`:

| Function                       | Test file                       | Cases |
|--------------------------------|---------------------------------|-------|
| `assembleInit`                 | assemble_test.go                | initial state, firstlineno propagation |
| `emitInstr`                    | assemble_emit_test.go           | each oparg width (0/1/2/3 EXTENDED_ARG), every opcode family |
| `writeVarint` / `writeSignedVarint` | assemble_varint_test.go    | zero, small, max-1-byte, max-2-byte, negative, max int32 |
| `writeLocInfoShortForm`        | assemble_loc_test.go            | columns 0-79, isize 1-8 |
| `writeLocInfoOnelineForm`      | assemble_loc_test.go            | line-delta 1-7, columns |
| `writeLocInfoLongForm`         | assemble_loc_test.go            | every signed range |
| `writeLocInfoNoColumn`         | assemble_loc_test.go            | line-delta only |
| `writeLocInfoNone`             | assemble_loc_test.go            | -1 lineno |
| `writeLocInfoEntry` dispatcher | assemble_loc_test.go            | every form picked correctly |
| `assembleEmitExceptionTable`   | assemble_except_test.go         | single, multiple, nested, lasti, empty |
| `assembleEmitExceptionTableItem` | assemble_except_test.go       | varint MSB encoding |
| `assembleConsts`               | assemble_consts_test.go         | dedup int, float, str, bytes, tuple, frozenset, complex |
| `assembleLocalsplus`           | assemble_localsplus_test.go     | function, method, class, generator, comprehension scope |
| `Assemble` driver              | assemble_driver_test.go         | end-to-end on a hand-built Unit |

### Layer 2: Round-trip vs CPython linetable

`compile/assemble_loc_parity_test.go` (//go:build cpython): for the
parity corpus (~120 snippets), assert `co_linetable` byte-equal.

### Layer 3: Round-trip vs CPython exception table

`compile/assemble_except_parity_test.go` (//go:build cpython): for
every snippet involving try/except/finally/with/match in the parity
corpus, assert `co_exceptiontable` byte-equal.

### Layer 4: Marshal parity (full)

`compile/marshal_parity_test.go` (//go:build cpython): for the parity
corpus, marshal both CPython and gopy code objects and assert
`marshal.dumps(co)` byte-equal. This is the gate test for v0.5.

The corpus is shared with 1626 and 1627 (single source of truth at
`compile/testdata/parity_corpus/*.py`).

## Lint and refactor budget

`writeLocationInfoEntry` is the only function over the cyclomatic
limit. Split into:

- `pickLocFormat(loc, isize, lineCursor) locFormat`
- `writeLocByForm(a, form, loc, isize)`

Everything else is straight-line varint emission and stays under the
limit naturally.

## Citation policy

Same as 1626 and 1627. Every Go function gets `// CPython:
assemble.c:L<n> <name>`. Helpers split for lint carry `(extracted
helper)`.

## Order of work

1. Skeleton: `Assembler` struct, `Assemble` public entry that returns
   nil. Tests for the empty path.
2. `emitInstr`: one opcode at a time, with EXTENDED_ARG widening,
   verified by golden bytes.
3. Varint helpers: stand-alone tests against hand-computed bytes.
4. Line table: short / oneline / long / no-column / none, in that
   order. Layer 2 parity gates this.
5. Exception table: single, then multi, then nested. Layer 3 parity
   gates this.
6. Pool materialisation: consts, names, localsplus.
7. Final `Assemble` driver wires all pieces.
8. Cross-check with 1626 + 1627 outputs on the parity corpus.

Each step lands as one PR. Assemble is "done" when Layer 4 marshal
parity passes for the entire corpus.
