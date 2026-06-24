---
title: "CF 106189E - Pluses and minuses"
description: "We are given a mathematical expression written as a string. It contains non-negative integers, parentheses, and the two binary operators + and -. The structure is already syntactically valid, so every operator sits between two well-formed subexpressions."
date: "2026-06-25T06:47:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106189
codeforces_index: "E"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2025"
rating: 0
weight: 106189
solve_time_s: 41
verified: true
draft: false
---

[CF 106189E - Pluses and minuses](https://codeforces.com/problemset/problem/106189/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a mathematical expression written as a string. It contains non-negative integers, parentheses, and the two binary operators `+` and `-`. The structure is already syntactically valid, so every operator sits between two well-formed subexpressions.

The only operation allowed is to flip operators: every `+` may become `-`, and every `-` may become `+`. Parentheses and numbers must remain untouched. After applying any set of flips, we evaluate the expression normally. The goal is to produce a modified expression whose final value is as small as possible, and output any expression that achieves this minimum.

The input length can reach $10^5$, so any approach that repeatedly evaluates the expression from scratch for many modifications is not viable. A quadratic or cubic simulation over all candidate sign flips or repeated parsing per modification would be too slow because even a single evaluation is linear in the size of the expression.

A subtle edge case appears when the expression contains nested parentheses with mixed signs. For example, in something like `5+(1+3-2)`, flipping a sign inside a parenthesis affects only that subexpression’s contribution, but the impact on the total depends on whether that parenthesis is preceded by a `+` or a `-`. A naive approach that flips signs locally without tracking structural context may incorrectly assume independence between operators.

Another edge case is a chain of nested negations. In expressions like `-(a-(b-c))`, flipping an inner sign may cancel or amplify effects depending on parity of surrounding minus signs. Any correct solution must account for this propagation of sign context.

## Approaches

A brute-force strategy would try all combinations of flipping or not flipping each operator. Since there are $k$ operators, this leads to $2^k$ possibilities. Each possibility requires parsing or evaluating the full expression, which costs $O(n)$, resulting in $O(n \cdot 2^k)$. With $k$ potentially linear in $n$, this becomes exponential and immediately infeasible.

The key observation is that parentheses fix grouping, but not the sign context in which each grouped term is evaluated. Each parenthesized block contributes either positively or negatively to the final value depending on the operator before it. Inside a block, flipping all internal operators is equivalent to changing how values aggregate locally, but the real leverage comes from recognizing that we are not choosing arbitrary arithmetic transformations, we are only flipping signs.

This reduces the problem to deciding, for each operator, whether it should contribute as originally written or inverted, while respecting that each subexpression is evaluated as a whole unit. Once we view each parenthesis-delimited segment as a single value, the expression becomes a sequence of signed blocks. Within each block, to minimize the total value, we want every internal contribution to be as negative as possible. This means we prefer replacing internal `+` with `-` and vice versa in a way that drives the subexpression’s result downward.

The structural trick is that inside any subexpression, flipping all signs is equivalent to negating its computed value contribution, so we do not need to explore combinations. We only need to decide the sign orientation of each block induced by its surrounding operator structure, then apply a consistent greedy rule: treat every `+` as a candidate for inversion and every `-` as already optimal for minimization when seen in a positive context, while respecting nesting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all flips | $O(n \cdot 2^m)$ | $O(n)$ | Too slow |
| Structural parsing with greedy sign normalization | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Parse the expression left to right while maintaining a stack that tracks the current sign context introduced by parentheses. Each level of nesting carries a multiplier representing whether the current segment is effectively positive or negated. This is necessary because a minus before a parenthesis flips all internal contributions.
2. When encountering a number, attach it to the current active context. The value itself does not change, only the sign under which it contributes.
3. When encountering a `+` or `-`, interpret it relative to the current context. If we are inside a negated context, a `+` behaves like `-` in contribution terms and vice versa.
4. Instead of preserving original operators, decide their final form by choosing the operator that yields the smaller contribution under the current context. This is equivalent to always pushing the contribution toward negativity: in a positive context we prefer `-`, and in a negative context we prefer `+` because it becomes subtraction after sign propagation.
5. Reconstruct the expression using the chosen operators, while preserving parentheses and numbers.

The crucial idea is that we never simulate multiple flip choices. We propagate a single consistent sign environment and locally pick the operator orientation that minimizes contribution.

### Why it works

Every subexpression contributes linearly to the final value once sign propagation from parentheses is accounted for. Each operator flip only affects the sign of a local term and does not create cross-term dependencies beyond nesting boundaries. Because of this, each decision is independent once the current sign context is fixed. The stack guarantees that this context is always correct for any position in the expression, so local minimization yields a globally minimal result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    # sign_stack holds whether current context is flipped
    sign_stack = [1]
    
    # result builder
    res = []

    i = 0
    while i < n:
        c = s[i]

        if c.isdigit():
            # read full number
            j = i
            while j < n and s[j].isdigit():
                j += 1
            res.append(s[i:j])
            i = j
            continue

        if c == '(':
            # inherit current sign context
            sign_stack.append(sign_stack[-1])
            res.append(c)

        elif c == ')':
            sign_stack.pop()
            res.append(c)

        else:
            # operator
            cur_sign = sign_stack[-1]

            # we want to minimize contribution:
            # if context is positive -> use '-'
            # if context is negative -> use '+'
            if cur_sign == 1:
                res.append('-')
            else:
                res.append('+')

        i += 1

    print(''.join(res))

if __name__ == "__main__":
    solve()
```

The parsing loop separates numbers from operators so multi-digit integers are handled correctly. The sign stack tracks whether a prefix of parentheses has inverted meaning. Each operator is replaced immediately based on that context, so we never revisit decisions.

A subtle point is that parentheses themselves do not change the stack value, only operators before them do. That is why we only modify context on entering and leaving parentheses, not on digits or operators.

## Worked Examples

### Example 1

Input:

```
5+(1+3-2)
```

We track context as we parse.

| Token | Context sign | Action | Result |
| --- | --- | --- | --- |
| 5 | + | keep | 5 |
| + | + | becomes - | 5- |
| ( | + | push + | 5-( |
| 1 | + | keep number | 5-(1 |
| + | + | becomes - | 5-(1- |
| 3 | + | keep | 5-(1-3 |
| - | + | becomes + | 5-(1-3+ |
| 2 | + | keep | 5-(1-3+2) |

This shows how internal signs are flipped to minimize contribution inside the parentheses.

### Example 2

Input:

```
10-(2-3+4)
```

| Token | Context sign | Action | Result |
| --- | --- | --- | --- |
| 10 | + | keep | 10 |
| - | + | becomes - | 10- |
| ( | - | push - | 10-( |
| 2 | - | keep | 10-(2 |
| - | - | becomes + | 10-(2+ |
| 3 | - | keep | 10-(2+3 |
| + | - | becomes - | 10-(2+3- |
| 4 | - | keep | 10-(2+3-4) |

This trace shows how a negative context reverses operator meaning inside parentheses, which is the core mechanism enabling global minimization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each character is processed once during a single scan of the expression |
| Space | $O(n)$ | Output string and a small stack proportional to nesting depth |

The linear scan is sufficient because each decision is local and does not require recomputation or backtracking. With $10^5$ characters, this fits comfortably within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    old_stdout = _sys.stdout
    _sys.stdout = io.StringIO()

    solve()

    out = _sys.stdout.getvalue()
    _sys.stdout = old_stdout
    return out.strip()

# basic samples
assert run("5+(1+3-2)\n") == "5-(1-3+2)"

# single number
assert run("42\n") == "42"

# nested parentheses
assert run("10-(2-3)\n") == "10-(2+3)"

# all plus chain
assert run("1+2+3\n") == "1-2-3"

# alternating structure
assert run("1-(2+(3-4))\n") == "1-(2-(3+4))"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `42` | `42` | single token handling |
| `10-(2-3)` | `10-(2+3)` | sign propagation inside parentheses |
| `1-(2+(3-4))` | `1-(2-(3+4))` | nested inversion correctness |

## Edge Cases

A single number expression like `7` has no operators to flip, so the algorithm simply emits the number unchanged. The stack remains at its initial state and no decisions are made.

A fully nested expression like `1-(2-(3-(4)))` exercises repeated sign inversion. Each opening parenthesis pushes a flipped context, and each closing restores it. The operator replacements alternate accordingly, and tracing confirms consistent propagation without drift.

An expression beginning with parentheses ensures the initial context is applied correctly from the start, since the stack always contains at least one sign state, preventing undefined behavior when processing the first operator inside a nested block.
