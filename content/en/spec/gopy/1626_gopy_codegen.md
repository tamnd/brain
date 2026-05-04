---
title: "gopy codegen"
description: "Detailed port plan for cpython/Python/codegen.c (~6500 lines) to compile/codegen.go. Statement and expression visitors, frame block stack, pattern matching panel, with-statement state machine, deferred annotations, PEP 695 type-parameter codegen, comprehensive test plan."
tags: ["gopy", "spec"]
weight: 1626
---

# 1626. Codegen

Port of `cpython/Python/codegen.c` (6483 lines) to `gopy/compile/codegen.go`.
This spec is the detailed source-of-truth for section 6 of 1620. The
1620 file keeps the cross-cutting view; the per-visitor and per-opcode
detail lives here.

## What codegen does

Codegen takes a fully-resolved scope (a `symtable.Entry`) plus the AST
nodes that belong to that scope, and produces an `instrseq.Sequence` of
labelled instructions. It does *not* produce a finished code object;
that is the assembler's job (1628). It does *not* run any optimisation
passes; that is the flowgraph's job (1627).

Boundary contract:

```
Input:
  ast.Mod plus per-scope ast nodes (FunctionDef, ClassDef, Lambda, ...)
  *symtable.Table (so each Name lookup resolves to LOCAL/CELL/FREE/GLOBAL)
  *future.Features (annotations PEP 649 and division flags)
  *compileContext (filename, optimisation level, c_flags)

Output (per scope):
  *instrseq.Sequence (labelled, no jump deltas yet)
  unitState: name, qualname, scope kind, argcount, posonly, kwonly,
             firstlineno, fblock stack at end, free-vars list,
             cell-vars list, fasthidden bitset, deferred-annotation list
```

The driver (1620 / `compile/compiler.go`) walks the symtable top-down
and calls codegen once per `Entry`, collecting one Sequence per scope.

## File layout

`compile/codegen.go` is large enough to be split into focused sibling
files. Mirror the `symtable/build_*.go` pattern:

| Go file                    | CPython lines  | Contents                                                                                          |
|----------------------------|----------------|---------------------------------------------------------------------------------------------------|
| `codegen.go`               | 1-250, 4933+   | `unit` struct, `compiler` struct, entry/leave scope, helper addops, public entry points           |
| `codegen_stmt.go`          | 2991-3110      | `visitStmt` plus the simple statement visitors (Pass / Break / Continue / Delete / Assert / etc.) |
| `codegen_stmt_funclike.go` | 1311-1727      | Function / Lambda / Class / TypeAlias bodies; closure construction; type-param bodies             |
| `codegen_stmt_control.go`  | 2043-2289      | If / For / AsyncFor / While / Return                                                              |
| `codegen_stmt_try.go`      | 2293-2792      | Try / TryStar / Finally / Except / unwind_fblock_stack                                            |
| `codegen_stmt_with.go`     | 4940-5172      | With / AsyncWith / with_except_finish state machine                                               |
| `codegen_stmt_match.go`    | 5736-6473      | Match plus all 11 pattern visitors (or, as, mapping, sequence, class, singleton, value, etc.)     |
| `codegen_stmt_import.go`   | 2793-2931      | Import / ImportFrom / star-import emit                                                            |
| `codegen_expr.go`          | 5172-5345      | `visitExpr` dispatch                                                                              |
| `codegen_expr_simple.go`   | 3290-3623      | BoolOp / BinOp / UnaryOp / List / Tuple / Set / Dict / Compare / IfExp                            |
| `codegen_expr_call.go`     | 4017-4769      | Call / Keyword / kwargs splat / star-args panel                                                   |
| `codegen_expr_str.go`      | 4061-4196      | JoinedStr / TemplateStr / FormattedValue / Interpolation                                          |
| `codegen_expr_name.go`     | 3179-3289      | `nameop` (LOAD_FAST / STORE_NAME / DELETE_DEREF / LOAD_GLOBAL / etc.)                             |
| `codegen_expr_ann.go`      | 5420-5546      | Annotation expressions, AnnAssign, deferred panel                                                 |
| `codegen_expr_sub.go`      | 5547-5669      | Subscript / Slice / two-part slice                                                                |
| `codegen_comp.go`          | 4770-4932      | sync/async comprehension generators, genexp/listcomp/setcomp/dictcomp drivers                     |
| `codegen_aug.go`           | 5345-5419      | AugAssign panel                                                                                   |
| `codegen_fblock.go`        | 518-647        | Frame block stack: types, push/pop, unwind                                                        |
| `codegen_addop.go`         | 254-461        | addop_i / addop_j / addop_name / addop_o / addop_load_const                                       |
| `codegen_anno.go`          | 666-846        | Annotation scope setup / leave / deferred body / process deferred                                 |
| `codegen_helpers.go`       | 1810-1978      | jump_if, addcompare, check_compare, infer_type                                                    |
| `codegen_pattern.go`       | 5728-6353      | Pattern helpers and dispatch                                                                      |

Each file gets a header: `// Port of cpython/Python/codegen.c L<a>-L<b>`.
Every exported and unexported function gets the standard
`// CPython: codegen.c:L<n> codegen_<name>` citation.

## Public surface

```go
package compile

// Codegen drives the per-scope visitor. The caller (1620 driver) walks
// the symtable and invokes Codegen once per entry. unitOut is filled in
// with everything the assembler needs in 1628.
func Codegen(c *Compiler, sc *symtable.Entry, mod ast.Mod) (*Unit, error)

// Unit is the per-scope handoff. Equivalent to CPython's compiler_unit
// minus the bookkeeping the flowgraph and assemble stages own.
type Unit struct {
    Name              string
    Qualname          string
    ScopeType         symtable.BlockType
    Argcount          int
    PosOnlyArgCount   int
    KwOnlyArgCount    int
    FirstLineno       int
    Flags             uint32  // CO_OPTIMIZED, CO_NEWLOCALS, CO_VARARGS, ...
    Seq               *instrseq.Sequence
    Consts            []any   // ordered, deduped by EqualConst
    Names             []string
    VarNames          []string
    FreeVars          []string
    CellVars          []string
    FastHidden        map[string]bool
    DeferredAnnotations []deferredAnnotation
}

// CompileFlags re-exports the bits the codegen needs from co_flags.
const (
    CO_OPTIMIZED         = 0x0001
    CO_NEWLOCALS         = 0x0002
    CO_VARARGS           = 0x0004
    CO_VARKEYWORDS       = 0x0008
    CO_NESTED            = 0x0010
    CO_GENERATOR         = 0x0020
    CO_COROUTINE         = 0x0100
    CO_ITERABLE_COROUTINE = 0x0200
    CO_ASYNC_GENERATOR   = 0x0400
    CO_HAS_DOCSTRING     = 0x4000000
    CO_METHOD            = 0x8000000
)
```

`Compiler` is the long-lived driver state (filename, optimisation
level, future flags, the symtable). `unit` is per-scope and stacked: a
nested function pushes a fresh unit, emits its body, pops, and the
outer scope receives a `MAKE_FUNCTION` referencing the new code object
slot.

## Frame block stack

CPython tracks unwinding for `break` / `continue` / `return` / `try`
through a stack of `fblockinfo`. Each entry tags the kind of frame
(LOOP, TRY, FINALLY, WITH, ASYNC_WITH, EXCEPTION_HANDLER, EXCEPTION_GROUP_HANDLER,
HANDLER_CLEANUP, POP_VALUE) and carries jump targets and a `datum` slot
for the original AST node.

Go form:

```go
type fblockKind int

const (
    fblockWhileLoop fblockKind = iota + 1
    fblockForLoop
    fblockTryExcept
    fblockFinallyTry
    fblockFinallyEnd
    fblockWith
    fblockAsyncWith
    fblockHandlerCleanup
    fblockPopValue
    fblockExceptionHandler
    fblockExceptionGroupHandler
    fblockAsyncComprehensionGenerator
    fblockStopIteration
)

type fblock struct {
    Kind    fblockKind
    Block   instrseq.Label   // entry label
    Exit    instrseq.Label   // exit label
    Datum   ast.Node         // original AST node, for codegen_unwind_fblock
    Generator bool           // for-loop hoists DELETE_FAST of iter var
}

type unit struct {
    // ...
    fblocks []fblock
}
```

Push and pop never reorder; `unwindFblockStack` walks `fblocks` from
top down emitting POP_BLOCK / POP_TOP / END_FINALLY as appropriate.
Mirror codegen.c:518-647 line-for-line.

## Statement visitor coverage

Every `ast.Stmt` kind must dispatch through `visitStmt`. The list:

- [x] FunctionDef (1390)
- [x] AsyncFunctionDef (1390 with is_async=1)
- [ ] ClassDef (1623)
- [ ] TypeAlias (1727)
- [x] Return (2191)
- [ ] Delete (2880 path inside visit_stmt)
- [x] Assign (in visit_stmt 3060+)
- [ ] AugAssign (5346)
- [ ] AnnAssign (5476)
- [x] For (2071)
- [ ] AsyncFor (2117)
- [x] While (2165)
- [x] If (2043)
- [ ] With (5167)
- [ ] AsyncWith (5070)
- [ ] Match (6459)
- [ ] Raise (codegen_raise inside visit_stmt)
- [ ] Try (2774)
- [ ] TryStar (2782)
- [ ] Assert (2932)
- [ ] Import (2835)
- [ ] ImportFrom (2881)
- [x] Global (no-op at codegen)
- [x] Nonlocal (no-op at codegen)
- [x] ExprStmt (2962)
- [x] Pass (no-op)
- [x] Break (2232)
- [x] Continue (2248)

The dispatch in `visitStmt` is a switch on the concrete type of
`ast.Stmt`. Match the order in codegen.c:2991-3166 for cite-friendly
diffs. `Global` and `Nonlocal` are no-ops in codegen because symtable
already lifted them; document this with a `// CPython: codegen.c:Lxxxx
no-op, scope already resolved by symtable` line.

## Expression visitor coverage

`visitExpr` switches on `ast.Expr`. The list:

- [x] BoolOp (3290)
- [x] NamedExpr (walrus, in visit_expr 5174)
- [x] BinOp (in visit_expr 5180+)
- [x] UnaryOp (in visit_expr)
- [x] Lambda (1999)
- [x] IfExp (1979)
- [x] Dict (3497)
- [x] Set (3467)
- [ ] ListComp (4901)
- [ ] SetComp (4911)
- [ ] DictComp (4922)
- [ ] GeneratorExp (4891)
- [x] Await (in visit_expr)
- [x] Yield (visit_expr + addop_yield 3168)
- [x] YieldFrom (visit_expr + add_yield_from 472)
- [x] Compare (3552)
- [x] Call (4036)
- [x] FormattedValue (4165)
- [ ] Interpolation (4133)
- [x] JoinedStr (4104)
- [ ] TemplateStr (4061)
- [x] Constant (in visit_expr)
- [x] Attribute (in visit_expr; LOAD_ATTR / LOAD_METHOD selection)
- [x] Subscript (5548)
- [x] Starred (only in target context; raises in load context)
- [x] Name (3186)
- [x] List (3431)
- [x] Tuple (3449)
- [x] Slice (5609)

## Special panels

### LOAD/STORE name selection (`codegen_nameop` 3186)

The hottest helper. Matches CPython exactly:

| symtable scope | ctx=Load           | ctx=Store         | ctx=Del          |
|----------------|--------------------|-------------------|------------------|
| Local (function) | LOAD_FAST        | STORE_FAST        | DELETE_FAST      |
| Local (module)   | LOAD_NAME        | STORE_NAME        | DELETE_NAME      |
| Local (class)    | LOAD_NAME        | STORE_NAME        | DELETE_NAME      |
| Cell             | LOAD_DEREF       | STORE_DEREF       | DELETE_DEREF     |
| Free             | LOAD_DEREF       | STORE_DEREF       | DELETE_DEREF     |
| GlobalImplicit   | LOAD_GLOBAL      | STORE_GLOBAL      | DELETE_GLOBAL    |
| GlobalExplicit   | LOAD_GLOBAL      | STORE_GLOBAL      | DELETE_GLOBAL    |

Class-mediated free var (`__class__`, `__classdict__`,
`__conditional_annotations__`) takes a special path that emits
`LOAD_DEREF` plus `LOAD_FROM_DICT_OR_DEREF`. See codegen.c:3179-3287.

### Super-instructions

CPython picks fused opcodes when arg shape matches:

- `LOAD_FAST_LOAD_FAST` after `LOAD_FAST` then `LOAD_FAST`
- `STORE_FAST_LOAD_FAST` after `STORE_FAST` then `LOAD_FAST`
- `STORE_FAST_STORE_FAST` after two `STORE_FAST` in a row
- `LOAD_CONST_IMMORTAL` for cached small ints / interned strings
- `LOAD_FAST_BORROW`, `LOAD_FAST_BORROW_LOAD_FAST_BORROW` for known-non-escape reads

The selection happens in `instr_sequence` write-back, not in codegen
visitors. Defer the implementation to the flowgraph (1627) but
document the contract so codegen does not pre-fuse.

### MAKE_FUNCTION / closure construction (`codegen_make_closure` 923)

`MAKE_FUNCTION` takes the code object on the stack and a `flags`
oparg. The visitor fills `co_freevars`, defaults, kwdefaults, and
annotations onto the stack first per the CPython oparg spec:

- bit 0x01: defaults tuple
- bit 0x02: kwonly defaults dict
- bit 0x04: annotations function (PEP 649) or annotation dict (legacy)
- bit 0x08: closure cell tuple

Closure construction:

1. For each name in `co_freevars` of the inner code, push the matching
   cell from the outer scope: `LOAD_FAST` if Cell, `LOAD_DEREF` if Free.
2. `BUILD_TUPLE` with that count.
3. `MAKE_FUNCTION` with bit 0x08 set.

CPython: codegen.c:923-961.

### Cell / free-var prologue (`MAKE_CELL` / `COPY_FREE_VARS`)

At function entry, before the first user instruction:

- For each name in `co_cellvars` whose flag has DEF_PARAM, emit
  `MAKE_CELL` to box the parameter slot.
- If `co_freevars` is non-empty, emit `COPY_FREE_VARS n` to copy the
  cell tuple from the function object into the local cells.

This is emitted by `codegen_function_body` after `RESUME 0` and before
the docstring / first body statement. CPython: codegen.c:1311-1389.

### Match panel

`Match` plus the eleven `Pattern*` kinds. Use a `patternContext` struct
to track:

- `stores`: names bound by patterns in the current alternative (so `or`
  branches can verify identical names).
- `allowIrrefutable`: false at the top of `or`, true elsewhere.
- `failPop`: number of values pushed by sub-patterns that need POP on
  fail.
- `onTop`: number of values pushed by the dispatcher that the pattern
  must consume.

```go
type patternContext struct {
    Stores         []string
    AllowIrrefutable bool
    FailPop        []instrseq.Label
    OnTop          int
}
```

Each pattern visitor (`codegen_pattern_*`) is mechanical. The hard
ones:

- [ ] PatternMatchOr: alternatives with shared bindings, fail-pop unification
- [ ] PatternMatchClass: positional / keyword via `MATCH_CLASS` and `__match_args__`
- [ ] PatternMatchMapping: `MATCH_MAPPING` plus `MATCH_KEYS`, rest `**` capture
- [ ] PatternMatchSequence: `MATCH_SEQUENCE`, length check, slice-out star

CPython: codegen.c:5728-6473. Tests under `compile/codegen_match_test.go`.

### With statement state machine

`with` and `async with` both lower to:

```
SETUP_WITH       -> push exit fblock
<context expr>
CALL on __enter__
<body>
LOAD_CONST None x3
CALL on __exit__
... or on exception path:
WITH_EXCEPT_START
... etc.
```

The state machine tracks how many context managers are open and how
many to clean up on exception. Both with and async-with use
`codegen_with_inner` recursively per item. CPython: codegen.c:4940-5172.

### Deferred annotations (PEP 649)

When `from __future__ import annotations` is *not* set and the
ANNOTATIONS feature is the 3.14 default, function and class
annotations compile to a separate inner code object that runs lazily
on `__annotations__` access. The visitor records these in
`unit.DeferredAnnotations`; the driver emits one `__annotations__`
function per outer scope at end-of-block. CPython: codegen.c:666-846,
1081-1145, 5476-5546.

### PEP 695 type parameters

`class C[T, *Ts, **P]:` and `def f[T](...):` and `type X[T] = ...`
each create an extra inner scope (`TypeParametersBlock`) that:

1. Builds the TypeVar / TypeVarTuple / ParamSpec objects.
2. `BUILD_TUPLE` of the type-param objects.
3. Calls into the actual function or class body with the tuple as a
   first positional arg.
4. The outer code receives the tuple via `LOAD_FAST .type_params`.

CPython: codegen.c:1195-1310, 1505-1622, 1700-1810.

## Comprehensive test plan

Tests live in `compile/codegen_*_test.go`. Each test file mirrors the
visitor file. Tests at this layer use hand-built AST inputs and assert
the produced instruction sequence against a golden form printed by a
disassembler that we ship alongside (`compile/dis.go`, task #51).

Three test layers:

### Layer 1: Unit (no CPython dependency)

For every visitor, two tests minimum:

- a happy-path AST that exercises every branch of the visitor
- a syntax-error input that asserts the exact error message string

```go
func TestCodegenForLoop(t *testing.T) {
    // for i in [1, 2]: pass
    src := module(forStmt(...))
    code := compileMust(t, src)
    want := []string{
        "RESUME 0",
        "LOAD_CONST (1, 2)",
        "GET_ITER",
        "FOR_ITER L1",
        "STORE_FAST i",
        "JUMP L0",
        "L1: END_FOR",
        "L2: LOAD_CONST None",
        "RETURN_VALUE",
    }
    assertDis(t, code, want)
}
```

Coverage table (every checkbox below maps one visitor + one test):

| Visitor                        | Test file                          | Cases |
|--------------------------------|------------------------------------|-------|
| visit_stmt FunctionDef         | codegen_func_test.go               | empty body, single return, generator, async, decorators, defaults, kwonly, posonly, varargs, varkw, type-params |
| visit_stmt ClassDef            | codegen_class_test.go              | empty class, with bases, with kwargs, with decorators, with type-params, with __init_subclass__ |
| visit_stmt TypeAlias           | codegen_typealias_test.go          | simple alias, with type-params, defaults, bound |
| visit_stmt Return              | codegen_return_test.go             | bare return, return value, return in generator (raises) |
| visit_stmt Assign              | codegen_assign_test.go             | single, multi-target, tuple-unpack, starred-unpack, attribute, subscript |
| visit_stmt AugAssign           | codegen_aug_test.go                | name, attr, subscript, every binop |
| visit_stmt AnnAssign           | codegen_annassign_test.go          | with value, without value, simple vs not, deferred |
| visit_stmt For                 | codegen_for_test.go                | tuple unpack target, with else, with break, with continue, nested |
| visit_stmt AsyncFor            | codegen_asyncfor_test.go           | basic, with else, in async function |
| visit_stmt While               | codegen_while_test.go              | basic, with else, with break, with continue |
| visit_stmt If                  | codegen_if_test.go                 | if-only, if-else, elif chain, constant fold |
| visit_stmt With                | codegen_with_test.go               | single ctx, multiple, with as, nested |
| visit_stmt AsyncWith           | codegen_asyncwith_test.go          | single, multiple, exception path |
| visit_stmt Match               | codegen_match_test.go              | one per pattern kind, or-pattern, guard, capture, irrefutable check |
| visit_stmt Raise               | codegen_raise_test.go              | bare, exc, exc from |
| visit_stmt Try                 | codegen_try_test.go                | try-except, try-finally, try-except-finally, try-except-else, multiple handlers, bare except |
| visit_stmt TryStar             | codegen_trystar_test.go            | basic, multiple handlers, with finally |
| visit_stmt Assert              | codegen_assert_test.go             | bare, with msg, optimised away under -O |
| visit_stmt Import              | codegen_import_test.go             | simple, dotted, as |
| visit_stmt ImportFrom          | codegen_importfrom_test.go         | name, dotted, star, as |
| visit_stmt Break               | codegen_break_test.go              | in loop, in nested loop, in try-finally |
| visit_stmt Continue            | codegen_continue_test.go           | in loop, in nested loop, in try-finally |
| visit_stmt ExprStmt            | codegen_exprstmt_test.go           | docstring placement, plain expr (POP_TOP), interactive (PRINT_EXPR) |
| visit_expr BoolOp              | codegen_boolop_test.go             | and / or, two operands, three operands, short-circuit |
| visit_expr NamedExpr (walrus)  | codegen_walrus_test.go             | basic, in comprehension, in lambda, retarget |
| visit_expr BinOp               | codegen_binop_test.go              | every op, type-inferred specialization |
| visit_expr UnaryOp             | codegen_unaryop_test.go             | not / -/~/+ |
| visit_expr Lambda              | codegen_lambda_test.go             | empty, with args, with defaults |
| visit_expr IfExp               | codegen_ifexp_test.go              | basic, nested |
| visit_expr Dict                | codegen_dict_test.go               | empty, simple, with double-star, mixed |
| visit_expr Set                 | codegen_set_test.go                | empty (raises, list comp instead), simple, with star |
| visit_expr ListComp            | codegen_listcomp_test.go           | basic, with if, with multiple for, with walrus |
| visit_expr SetComp             | codegen_setcomp_test.go            | basic, with if, nested |
| visit_expr DictComp            | codegen_dictcomp_test.go           | basic, with if |
| visit_expr GeneratorExp        | codegen_genexp_test.go             | basic, with if, async |
| visit_expr Await               | codegen_await_test.go              | in async, error in sync |
| visit_expr Yield               | codegen_yield_test.go              | bare, with value, in async generator |
| visit_expr YieldFrom           | codegen_yieldfrom_test.go          | basic, in coroutine raises |
| visit_expr Compare             | codegen_compare_test.go             | one op, chained, every cmpop |
| visit_expr Call                | codegen_call_test.go               | positional, keyword, star, doublestar, method, super, every CALL_INTRINSIC variant |
| visit_expr FormattedValue      | codegen_fstring_test.go            | conv flags, format spec, in joinedstr |
| visit_expr Interpolation       | codegen_interp_test.go             | new in 3.14: t-string |
| visit_expr JoinedStr           | codegen_joinedstr_test.go          | empty, single, multi, mixed const+formatted |
| visit_expr TemplateStr         | codegen_templatestr_test.go        | t-string PEP 750 panel |
| visit_expr Constant            | codegen_const_test.go              | int, float, str, bytes, None, True, False, complex |
| visit_expr Attribute           | codegen_attribute_test.go          | LOAD_ATTR vs LOAD_METHOD, store, del |
| visit_expr Subscript           | codegen_subscript_test.go          | int, slice, tuple, store, del |
| visit_expr Starred             | codegen_starred_test.go            | in target, in call, in load context (raises) |
| visit_expr Name                | codegen_name_test.go               | LOCAL/CELL/FREE/GLOBAL_EXPLICIT/GLOBAL_IMPLICIT, class scope mediation, __class__ free var |
| visit_expr List                | codegen_list_test.go               | empty, single, with star |
| visit_expr Tuple               | codegen_tuple_test.go              | empty, single, all-const folds to LOAD_CONST tuple |
| visit_expr Slice               | codegen_slice_test.go              | one part, two parts, three parts |

### Layer 2: Cross-check vs CPython

Build the same AST in CPython via `ast.parse`, compile with
`compile()`, and assert `dis.dis` text equality with our output.
Tagged `//go:build cpython`. One driver test per visitor coverage row.

### Layer 3: Marshal parity

`marshal.dumps(code)` byte-equal to `gopy/marshal.Dumps(unit.Code)` for
~50 hand-picked source snippets covering every opcode emitted in 3.14.
This layer crosses the assemble boundary (1628), so it lives in
`compile/marshal_parity_test.go` and depends on tasks #47, #48, #49.

## Lint, complexity, and refactor budget

Same rules as symtable: cognitive ≤30, cyclomatic ≤20. The largest
CPython visitors that overflow if ported as-is:

- `codegen_visit_stmt` (170 lines, 27 cases): split by category
  matching `symtable/build_visit.go` (`visitStmtDef`, `visitStmtControl`,
  `visitStmtSimple`).
- `codegen_visit_expr` (170 lines, 28 cases): split into
  `visitExprComp`, `visitExprBuild`, `visitExprLeaf`.
- `codegen_pattern_class` (60+ lines, deeply nested): extract
  `patternClassPositional`, `patternClassKeyword`, `patternClassFinish`.
- `codegen_try_except` (180 lines): extract `tryExceptHandlerEntry`,
  `tryExceptHandlerBody`, `tryExceptCleanup`.
- `codegen_with_inner` and `codegen_async_with_inner`: extract the
  exit-handler emit into a helper used by both.

Use the same helper-function naming as `symtable/build_visit.go`:
verbs that describe the work, not the position in the file.

## Citation policy

Every Go function carries `// CPython: codegen.c:L<n> codegen_<name>`.
Helpers extracted to satisfy lint carry both: `// CPython:
codegen.c:L<n> codegen_<name> (extracted helper)` so a reader can
trace back to the un-split source.

## Order of work

1. [x] Skeleton: `Codegen` entry, `Unit` struct, `Compiler` driver,
   addop helpers, name-op dispatch (LOAD_FAST / LOAD_DEREF /
   LOAD_GLOBAL / LOAD_NAME by symtable scope). Tests assert the error
   path so the harness compiles. Landed as `compile/codegen.go`,
   `compile/codegen_addop.go`, `compile/codegen_stmt.go`,
   `compile/codegen_expr.go`, `compile/codegen_expr_name.go`.
2. [x] `Pass`, `ExprStmt`, `Constant`, `Name` (LOAD/STORE),
   `Return`, `Assign`. Smallest module compiles end-to-end.
   `compile/codegen_test.go` covers empty module, pass, expr-stmt
   pop, module-level assign, name load, const dedup. fblock stack
   stub will land alongside step 3.
3. [x] Control flow: `If`, `For`, `While`, `Break`, `Continue`.
   Landed as `compile/codegen_fblock.go`, `compile/codegen_stmt_control.go`,
   `compile/codegen_control_test.go`. Break / continue out-of-loop
   error paths covered.
4. [x] Functions: `FunctionDef`, `AsyncFunctionDef`, `Lambda`,
   defaults, kwonly defaults, varargs / varkeyword flags, decorator
   chain, closure (free / cell vars). Inner code object held as a
   `*Unit` const placeholder; assemble (1628) translates it to a
   real code object. Landed as
   `compile/codegen_stmt_funclike.go`, `compile/codegen_funclike_test.go`.
5. [x] Expression panel: `BoolOp`, `BinOp`, `UnaryOp`, `Compare`,
   `IfExp`, `List`, `Tuple`, `Set`, `Dict`, `Attribute`, `Subscript`,
   `Slice`, `Call`. Landed as `compile/codegen_expr_op.go`,
   `compile/codegen_expr_container.go`, `compile/codegen_expr_call.go`,
   `compile/codegen_expr_test.go`.
6. [x] Misc statements: `Delete`, `AugAssign`, `AnnAssign`, `Raise`,
   `Assert`, `Import`, `ImportFrom`. Landed as
   `compile/codegen_stmt_misc.go` and `compile/codegen_stmt_misc_test.go`.
7. [x] Misc expressions: `NamedExpr`, `Yield`, `YieldFrom`, `Await`,
   `JoinedStr`, `FormattedValue`. Landed as
   `compile/codegen_expr_misc.go` and `compile/codegen_expr_misc_test.go`.
8. [x] Assignment targets: Attribute, Subscript, Tuple / List unpack
   (UNPACK_SEQUENCE), Tuple / List with `*rest` (UNPACK_EX). Landed as
   `compile/codegen_assign_test.go` plus the extension to `assignTo`
   in `compile/codegen_stmt.go`.
9. [x] Classes: `ClassDef`, bases, keyword args (metaclass), decorator
   chain. Inner body opens with __name__/__module__ + __qualname__
   prologue; full PEP 695 / __classcell__ / static-attributes panels
   land alongside super(). Landed as `compile/codegen_class.go` and
   `compile/codegen_class_test.go`.
9. Comprehensions: `ListComp`, `SetComp`, `DictComp`, `GeneratorExp`.
10. With / Try / TryStar: full unwind panel.
11. Match: pattern visitors.
12. PEP 695 type parameters.
13. Deferred annotations (PEP 649).
14. Super-instruction emission contract with the flowgraph.

Each step lands as one PR with the matching test row from the table
above ticked. The codegen package is not "done" until every checkbox
in the visitor coverage table is green and Layer 2 cross-check passes.
