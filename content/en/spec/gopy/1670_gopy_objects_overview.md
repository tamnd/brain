---
title: "gopy objects overview"
description: "Top-level overview of the gopy Objects port. Ports cpython/Objects/ to Go with 100% behavioural compatibility. Lives in the 1670-1689 block of the 1600 spec series."
tags: ["gopy", "spec"]
weight: 1670
---

# 1670. gopy: Porting CPython's `Objects/` to Go

## Goal

The 1670-1689 block covers the port of `cpython/Objects/` (about
112k lines of C across 47 .c files). It runs alongside the rest of
the 1600 series and together they form the gopy interpreter core.

This block was previously the 1700 series; the renumber keeps the
whole port under one spec folder. Old references to "1700" point
here.

Same rule as 1600: 100% behavioural compatibility with CPython 3.14.
Same data shapes, same protocol semantics, same error messages.
Only naming and surface API style move to Go conventions.

The Objects port is the most behaviour-rich part of CPython. The
dict probing sequence, the unicode kind layout, the type-mro caching,
the exception args slot, the descriptor protocol: each of these is
observable through normal Python code, so each needs to round-trip
exactly.

## Sources of truth

| Concern                    | Source                                                |
|----------------------------|-------------------------------------------------------|
| Object protocol            | `Include/object.h`, `Include/cpython/object.h`        |
| Type slots                 | `Include/cpython/typeobject.h`                        |
| Per-type semantics         | `Objects/<type>object.c`                              |
| Abstract protocols         | `Objects/abstract.c`                                  |
| Refcount and lifecycle     | `Objects/object.c`                                    |
| Allocator (deferred)       | `Objects/obmalloc.c`                                  |

## Spec files in this block

| #    | File                                            | Focus                                              | Phase |
|------|-------------------------------------------------|----------------------------------------------------|-------|
| 1670 | `1670_gopy_objects_overview.md`                 | This file                                          | meta  |
| 1671 | `1671_gopy_object_protocol.md`                  | `Object` interface, Header, VarHeader, refcount    | v0.2  |
| 1672 | `1672_gopy_type.md`                             | `Type`, slots, MRO, lookup                         | v0.2  |
| 1673 | `1673_gopy_long.md`                             | `longobject.c` (PyLong, small-int cache, parsing)  | v0.2  |
| 1674 | `1674_gopy_float_complex.md`                    | `floatobject.c`, `complexobject.c`                 | v0.2 / v0.6 |
| 1675 | `1675_gopy_bool_none.md`                        | `boolobject.c`, None / NotImplemented singletons   | v0.2  |
| 1676 | `1676_gopy_bytes.md`                            | `bytesobject.c`, `bytearrayobject.c`, `bytes_methods.c` | v0.4 |
| 1677 | `1677_gopy_unicode.md`                          | `unicodeobject.c`, `unicodectype.c`                | v0.4  |
| 1678 | `1678_gopy_tuple.md`                            | `tupleobject.c`                                    | v0.2  |
| 1679 | `1679_gopy_list.md`                             | `listobject.c`                                     | v0.2  |
| 1680 | `1680_gopy_dict.md`                             | `dictobject.c`, `odictobject.c`                    | v0.2  |
| 1681 | `1681_gopy_set.md`                              | `setobject.c` (set, frozenset)                     | v0.4  |
| 1682 | `1682_gopy_slice_range.md`                      | `sliceobject.c`, `rangeobject.c`                   | v0.2  |
| 1683 | `1683_gopy_abstract.md`                         | `abstract.c` (PyObject_*, PyNumber_*, PySequence_*, PyMapping_*, PyIter_*) | v0.2+ |
| 1684 | `1684_gopy_call.md`                             | `call.c`, vectorcall                               | v0.6  |
| 1685 | `1685_gopy_descr_method.md`                     | `descrobject.c`, `methodobject.c`, `classobject.c`, `funcobject.c` | v0.4 / v0.7 |
| 1686 | `1686_gopy_exceptions.md`                       | `exceptions.c` (BaseException + the full hierarchy) | v0.3  |
| 1687 | `1687_gopy_code_frame_gen.md`                   | `codeobject.c`, `frameobject.c`, `genobject.c`, `cellobject.c` | v0.5 / v0.6 |
| 1688 | `1688_gopy_module_misc.md`                      | `moduleobject.c`, `namespaceobject.c`, `structseq.c`, `capsule.c`, `iterobject.c`, `enumobject.c` | v0.7 |
| 1689 | `1689_gopy_obj_misc.md`                         | `weakrefobject.c`, `memoryobject.c`, `fileobject.c`, `picklebufobject.c`, `typevarobject.c`, `unionobject.c`, `genericaliasobject.c`, `interpolationobject.c`, `templateobject.c`, `obmalloc.c` (stub) | v0.7+ |

## Phasing

| Phase | Specs that ship                                              |
|-------|--------------------------------------------------------------|
| v0.2  | 1671, 1672, 1673, 1674 (float only), 1675, 1678, 1679, 1680, 1682, 1683 (subset) |
| v0.3  | 1686 (BaseException + KeyError + the gating hierarchy)       |
| v0.4  | 1676, 1677, 1681, 1685 (descriptor protocol minus tp_new)    |
| v0.5  | 1687 (code object only; frame/gen wait on v0.6)              |
| v0.6  | 1674 (complex), 1684, 1687 (frame, gen)                      |
| v0.7  | 1685 (tp_new / tp_init / tp_alloc), 1688, 1689 (subset)      |
| v0.10 | 1689 (weakref, memoryview, etc.) round out alongside cycle GC|

## Compatibility floors

Items that must match CPython exactly, gating each release:

1. `repr(obj)` for every concrete type. Float repr uses
   shortest-roundtrip dtoa.
2. `hash(int)`, `hash(float)`, `hash(str)`, `hash(bytes)`,
   `hash(tuple)`, `hash(frozenset)`, `hash(None)`. SipHash-1-3 keyed
   from PYTHONHASHSEED.
3. Dict iteration order: insertion order; same probing sequence as
   `lookdict_unicode_nodummy` / `lookdict_split`.
4. List growth pattern: same `list_resize` curve.
5. Tuple identity for empty tuple: `() is ()` returns `True`.
6. Small-int caching: `-5..256` are cached singletons.
7. None, True, False, NotImplemented, Ellipsis are singletons.
8. Exception args slot byte-equal CPython for every constructor in
   the hierarchy.
9. `type.__mro__` matches CPython's C3 linearisation.
10. Descriptor protocol order: data descriptors beat instance dict
    beat non-data descriptors (CPython `type_getattro` ordering).

## Test strategy

`objtest/` carries the cross-cut gates per phase:

* v0.2: `TestGateBuildDict`, `TestGateHashTuple`, `TestGateIterList`.
* v0.3: exception construction + str round-trip panel.
* v0.4: unicode kind round-trip; bytes hash parity.
* v0.5: code-object equality panel against `compile.Compile`.
* v0.6: frame creation + generator close.

Each per-type spec carries its own per-type tests; this overview
only lists the cross-cut gates.

## v0.5 status checklist

This block did not gate v0.5 (compile pipeline); it gates v0.2.
Tracking v0.5-relevant Objects work here for visibility:

* [x] Object header + refcount placeholder shipped via `objects/`
  (per project memory; replaced by the full v0.2 port).
* [x] Code object stub used by `compile.Compile` (`compile/code.go`).
* [ ] Code object port to `Objects/code.go` proper. Lands in v0.5.5
  alongside the parser handover.
* [ ] Frame object + generator object. Lands in v0.6.

## Block-level checklist

Status: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Cross-cut artefacts

* [x] `objects/` package skeleton (header, type, placeholder hash).
* [x] `objtest/` v0.2 gate harness scaffold.
* [ ] `compat/` golden tests for repr / hash / dict-iter parity.

### Per-spec progress (one row per sub-spec)

| Spec | Status | Notes (audited 2026-05-06)                          |
|------|--------|-----------------------------------------------------|
| 1671 | [~]    | Header + refcount + Object interface shipped; repr.go / hash.go (SipHash key) / identity.go pending |
| 1672 | [~]    | Type + v0.2 slot subset + trivial-base MRO shipped; method-bundle split, type_repr, descriptor-aware getattro pending |
| 1673 | [~]    | Int struct on math/big shipped; arithmetic, bitwise, parse, cache, hash/repr/format pending |
| 1674 | [~]    | Float struct + basic arithmetic shipped; pystrtod repr, float_parse, complex (v0.6) pending |
| 1675 | [~]    | bool + None shipped; NotImplemented and Ellipsis singletons pending |
| 1676 | [ ]    | bytes / bytearray / bytes_methods all pending (v0.4) |
| 1677 | [~]    | strstub.go placeholder shipped; PEP 393 str, methods, format, codecs/intern pending (v0.4) |
| 1678 | [~]    | Tuple struct + empty-tuple singleton shipped; hash, repr, count/index, richcompare pending |
| 1679 | [~]    | List struct + Append/Pop shipped; CPython resize curve, Timsort, methods, richcompare pending |
| 1680 | [~]    | Dict struct + probing shipped; four lookdict variants, mutate, views, split-table, odict pending |
| 1681 | [x]    | Set + frozenset shipped (#233); set_ops algebra and frozenset XOR hash pending |
| 1682 | [~]    | Slice + Range structs shipped; slice_indices, range_iter, Ellipsis pending |
| 1683 | [~]    | abstract subset (Length/GetItem/RichCmp/Hash/Repr/Add/Sub/Mul/Iter) shipped; bitwise/MatMul/Index, mapping protocol, slice ops pending |
| 1684 | [~]    | call.go minimal (Call/CallNoArgs/CallOneArg) shipped; full vectorcall, *args/**kwargs unpacking pending (v0.6) |
| 1685 | [~]    | Function/Cell minimal shipped; descr.go, property, cfunction (METH_*), bound method, full Function pending (v0.4 + v0.7) |
| 1686 | [~]    | BaseException + LookupError/KeyError/IndexError + ImportError shipped (#232); Simple/Arithmetic/OS/Syntax/Unicode/Warning/Group pending |
| 1687 | [~]    | Code (scaffold) + Cell + Generator (minimal) shipped; full code repr/hash, frame, frame_locals, gen full, coroutine, async_gen pending (v0.6) |
| 1688 | [~]    | Module shipped (#231); namespace, structseq, seqiter/enum, capsule pending (v0.7) |
| 1689 | [ ]    | weakref / memoryview / file / typevar / union / templates all pending (v0.7+ / v0.10) |

## Out of scope

* `obmalloc.c` small-block pool: Go's allocator handles this. We
  ship a stub in 1689 that records the public API surface but
  delegates to `make` / `new`.
* C extension ABI (PyObject* layout exposed to .so files). gopy does
  not load C extensions; see 1600 §Compatibility floors.
* Free-threaded reader paths (`ob_tid`, `ob_mutex`, etc.). Land in
  v0.14 alongside `gc/freethreading.go`.
