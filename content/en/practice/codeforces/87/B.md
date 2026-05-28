---
title: "CF 87B - Vasya and Types"
description: "The language in this problem has only two real base types, void and errtype. Every other type is defined through typedef, and every query asks us to evaluate a type expression with typeof. A type expression is built from a base name plus some number of and & operators."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 87
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 73 (Div. 1 Only)"
rating: 1800
weight: 87
solve_time_s: 116
verified: true
draft: false
---

[CF 87B - Vasya and Types](https://codeforces.com/problemset/problem/87/B)

**Rating:** 1800  
**Tags:** implementation, strings  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The language in this problem has only two real base types, `void` and `errtype`. Every other type is defined through `typedef`, and every query asks us to evaluate a type expression with `typeof`.

A type expression is built from a base name plus some number of `*` and `&` operators. The rules are intentionally different from C.

Appending `*` means “pointer to”. Appending `&` means “dereference”. Dereferencing decreases the pointer depth by one. If we try to dereference plain `void`, the result becomes `errtype`.

The special type `errtype` is absorbing. Once an expression becomes `errtype`, adding `*` or `&` keeps it equal to `errtype`.

The key detail is operator priority. Dereference has lower priority than pointer creation. That means:

```
&T* = T
```

not

```
(&T)*
```

So when we parse a type expression, all `*` operators conceptually happen before all `&` operators.

The input is a sequence of operations processed in order. A `typedef A B` operation stores the current meaning of `A` into the name `B`. Future redefinitions of names used inside `A` do not retroactively affect `B`.

A `typeof A` query asks us to evaluate `A` right now and print its canonical form:

```
void*****
```

or `errtype`.

The constraints are tiny. There are at most 100 operations, and every operator string contains at most 10 explicit `*` and `&` symbols. Even if typedef chains become long, the total amount of work stays very small. Any solution with linear or quadratic processing per query easily fits.

The tricky part is not performance, it is faithfully modeling the type system.

One common mistake is evaluating operators from left to right instead of respecting precedence.

Consider:

```
typedef void* p
typeof &p*
```

A careless implementation might interpret this as:

```
(&p)*
```

which becomes:

```
(&void*)* = void*
```

But the language defines:

```
&p* = &(void**) = void*
```

The correct result is `void*`.

Another subtle case is typedef snapshot semantics.

Consider:

```
typedef void* a
typedef a b
typedef void a
typeof b
```

The correct output is:

```
void*
```

because `b` stores the meaning of `a` at definition time. It does not reference `a` dynamically.

Another dangerous edge case is propagation of `errtype`.

Consider:

```
typedef &void bad
typeof bad*****
```

Dereferencing `void` immediately produces `errtype`, and once that happens, every later operator still leaves it as `errtype`.

The correct output is:

```
errtype
```

A naive implementation that keeps a negative pointer depth or tries to continue manipulating `void` after failure can silently produce wrong answers.

## Approaches

The brute-force idea is to represent every type literally as a string such as:

```
void****
```

Then, for every query, repeatedly expand typedef names until we reach a concrete type. After that, apply all operators one by one.

This works because the language semantics are simple, and the constraints are tiny. Even if a type expands through several typedef layers, there are only 100 operations total.

The problem with this representation is that it encourages incorrect parsing. The precedence rule between `*` and `&` becomes awkward when manipulating raw strings. It is easy to accidentally process operators in textual order instead of semantic order.

The important observation is that every valid non-error type is completely determined by one integer: the number of pointer layers on top of `void`.

For example:

```
void      -> depth 0
void*     -> depth 1
void***   -> depth 3
```

Dereferencing decreases depth by one. Pointer creation increases depth by one.

If depth would become negative, the result becomes `errtype`.

This transforms the whole problem into integer arithmetic.

When parsing an expression:

```
&&name***
```

the operator precedence means:

```
((name***)) with two dereferences afterward
```

So we only need:

```
final_depth = base_depth + stars - amps
```

If the base type is already `errtype`, or the final depth becomes negative, the result is `errtype`.

This representation also naturally handles typedef snapshot semantics. When defining a new type name, we simply store its evaluated integer depth at that moment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² · L) | O(n · L) | Accepted but error-prone |
| Optimal | O(n · L) | O(n) | Accepted |

Here, `L` is the maximum expression length.

## Algorithm Walkthrough

1. Create a dictionary storing the meaning of every known type.

We represent:

```
void -> 0
errtype -> -1
```

Any non-negative integer means the number of `*` symbols on top of `void`. The value `-1` represents `errtype`.
2. For every operation, split the line into tokens.

Operations are either:

```
typedef A B
```

or:

```
typeof A
```
3. To evaluate a type expression, separate it into three parts:

the leading `&` symbols,

the trailing `*` symbols,

and the core type name.

For example:

```
&&ptr***
```

becomes:

```
amps = 2
name = ptr
stars = 3
```
4. Look up the current meaning of the core type name.

If the name does not exist, treat it as `errtype`.
5. If the base type is already `errtype`, return `errtype` immediately.

The language defines:

```
errtype* = errtype
&errtype = errtype
```
6. Otherwise compute:

```
depth = base_depth + stars - amps
```

This exactly matches the precedence rule that all `*` operators apply before all `&` operators.
7. If `depth < 0`, return `errtype`.

Negative depth means we tried to dereference plain `void`.
8. For a `typedef`, store the evaluated depth under the new name.

This stores the fully evaluated snapshot of the type at definition time.
9. For a `typeof`, print:

```
errtype
```

if the result is `-1`, otherwise print:

```
void + '*' * depth
```

### Why it works

The invariant is that every stored type name always maps to its fully evaluated canonical form.

A non-error type is represented only by its pointer depth above `void`. Since the language operations only increase or decrease pointer depth, this representation captures all necessary information.

Operator precedence is preserved because every expression is evaluated as:

```
base + all pointers - all dereferences
```

which is exactly equivalent to the language rule that dereference has lower priority than pointer creation.

Because typedef stores evaluated depths rather than symbolic references, later redefinitions cannot affect previously defined types.

## Python Solution

```python
import sys
input = sys.stdin.readline

def evaluate(expr, types):
    amps = 0
    i = 0

    while i < len(expr) and expr[i] == '&':
        amps += 1
        i += 1

    stars = 0
    j = len(expr) - 1

    while j >= i and expr[j] == '*':
        stars += 1
        j -= 1

    name = expr[i:j + 1]

    if name not in types:
        return -1

    base = types[name]

    if base == -1:
        return -1

    depth = base + stars - amps

    if depth < 0:
        return -1

    return depth

def solve():
    n = int(input())

    types = {
        "void": 0,
        "errtype": -1
    }

    out = []

    for _ in range(n):
        parts = input().split()

        if parts[0] == "typedef":
            expr = parts[1]
            new_name = parts[2]

            types[new_name] = evaluate(expr, types)

        else:
            expr = parts[1]

            result = evaluate(expr, types)

            if result == -1:
                out.append("errtype")
            else:
                out.append("void" + "*" * result)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `evaluate` function implements the entire type system.

It first counts leading `&` symbols and trailing `*` symbols. Everything in the middle is the actual type name. This parsing method directly matches the language grammar and automatically respects operator precedence.

The dictionary stores evaluated depths instead of symbolic expressions. This is the implementation detail that preserves typedef snapshot semantics. If a type is later redefined, previously stored entries remain unchanged because they already contain their final integer depth.

The special value `-1` represents `errtype`. Using a single sentinel value makes all propagation rules simple. As soon as evaluation reaches `-1`, every future operation stays `-1`.

The most common implementation mistake is processing operators in textual order. This solution avoids that entirely by converting the expression into:

```
base + stars - amps
```

Another subtle point is handling undefined names. The statement says they immediately become `errtype`, so the evaluator returns `-1` when a name is absent from the dictionary.

## Worked Examples

### Sample 1

Input:

```
5
typedef void* ptv
typeof ptv
typedef &&ptv node
typeof node
typeof &ptv
```

Trace:

| Operation | Base Type | Stars | Amps | Result Depth | Stored / Output |
| --- | --- | --- | --- | --- | --- |
| typedef void* ptv | 0 | 1 | 0 | 1 | ptv = 1 |
| typeof ptv | 1 | 0 | 0 | 1 | void* |
| typedef &&ptv node | 1 | 0 | 2 | -1 | node = errtype |
| typeof node | errtype | 0 | 0 | errtype | errtype |
| typeof &ptv | 1 | 0 | 1 | 0 | void |

The third operation demonstrates dereferencing too many times. `ptv` equals `void*`, so `&&ptv` tries to dereference twice and falls below zero depth.

### Custom Example

Input:

```
6
typedef void** a
typedef &a b
typedef b* c
typeof a
typeof b
typeof c
```

Trace:

| Operation | Base Type | Stars | Amps | Result Depth | Stored / Output |
| --- | --- | --- | --- | --- | --- |
| typedef void** a | 0 | 2 | 0 | 2 | a = 2 |
| typedef &a b | 2 | 0 | 1 | 1 | b = 1 |
| typedef b* c | 1 | 1 | 0 | 2 | c = 2 |
| typeof a | 2 | 0 | 0 | 2 | void** |
| typeof b | 1 | 0 | 0 | 1 | void* |
| typeof c | 2 | 0 | 0 | 2 | void** |

This example confirms that typedef stores evaluated values. `b` becomes `void*`, and `c` becomes `void**` independently of later changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L) | Each operation scans its expression once |
| Space | O(n) | The dictionary stores at most one entry per typedef |

Here, `L` is the maximum expression length.

With at most 100 operations and very short expressions, the running time is tiny. The solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def evaluate(expr, types):
        amps = 0
        i = 0

        while i < len(expr) and expr[i] == '&':
            amps += 1
            i += 1

        stars = 0
        j = len(expr) - 1

        while j >= i and expr[j] == '*':
            stars += 1
            j -= 1

        name = expr[i:j + 1]

        if name not in types:
            return -1

        base = types[name]

        if base == -1:
            return -1

        depth = base + stars - amps

        if depth < 0:
            return -1

        return depth

    n = int(input())

    types = {
        "void": 0,
        "errtype": -1
    }

    out = []

    for _ in range(n):
        parts = input().split()

        if parts[0] == "typedef":
            types[parts[2]] = evaluate(parts[1], types)
        else:
            result = evaluate(parts[1], types)

            if result == -1:
                out.append("errtype")
            else:
                out.append("void" + "*" * result)

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""5
typedef void* ptv
typeof ptv
typedef &&ptv node
typeof node
typeof &ptv
"""
) == "void*\nerrtype\nvoid"

# minimum input
assert run(
"""1
typeof void
"""
) == "void"

# undefined type
assert run(
"""1
typeof abc
"""
) == "errtype"

# typedef snapshot semantics
assert run(
"""4
typedef void* a
typedef a b
typedef void a
typeof b
"""
) == "void*"

# errtype propagation
assert run(
"""3
typedef &void bad
typedef bad***** x
typeof x
"""
) == "errtype"

# precedence check
assert run(
"""2
typedef void* p
typeof &p*
"""
) == "void*"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `typeof void` | `void` | Smallest valid query |
| `typeof abc` | `errtype` | Undefined type handling |
| Redefining `a` after defining `b` | `void*` | Typedef snapshot semantics |
| Using `bad*****` after error | `errtype` | errtype propagation |
| `typeof &p*` | `void*` | Correct operator precedence |

## Edge Cases

Consider undefined types:

```
1
typeof abc
```

The evaluator extracts:

```
name = abc
```

Since `abc` is absent from the dictionary, evaluation immediately returns `-1`, which prints as:

```
errtype
```

This matches the statement that unknown types automatically become `errtype`.

Now consider excessive dereferencing:

```
2
typedef void p
typeof &p
```

`p` has depth `0`. The query applies one dereference:

```
0 - 1 = -1
```

Negative depth is invalid, so the result becomes:

```
errtype
```

The algorithm handles this cleanly through the `depth < 0` check.

Finally, consider typedef redefinition:

```
5
typedef void* a
typedef a b
typedef void a
typeof a
typeof b
```

The trace is:

| Step | a | b |
| --- | --- | --- |
| after first typedef | 1 | not defined |
| after second typedef | 1 | 1 |
| after redefining a | 0 | 1 |

Outputs become:

```
void
void*
```

because the algorithm stores fully evaluated depths inside the dictionary. `b` keeps the old value even after `a` changes.
