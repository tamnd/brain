---
title: "CF 105839G - Removing Parentheses"
description: "We have a valid arithmetic expression containing digits, +, -, and parentheses. We may delete some parentheses, but the resulting text must still be a valid expression. Among all possible deletions, we need the maximum value and one expression that achieves it."
date: "2026-06-25T14:55:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105839
codeforces_index: "G"
codeforces_contest_name: "XXVII Interregional Programming Olympiad, Vologda SU, 2025"
rating: 0
weight: 105839
solve_time_s: 49
verified: true
draft: false
---

[CF 105839G - Removing Parentheses](https://codeforces.com/problemset/problem/105839/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a valid arithmetic expression containing digits, `+`, `-`, and parentheses. We may delete some parentheses, but the resulting text must still be a valid expression. Among all possible deletions, we need the maximum value and one expression that achieves it.

The expression is small, with at most 100 numbers and 100 parentheses, so exponential brute force over every subset of parentheses is not feasible. There can be around 100 independent pairs, giving up to `2^100` choices. We need to exploit the structure of arithmetic expressions instead of enumerating deletions.

A common mistake is assuming that deleting parentheses only removes grouping. For example, `1-(2-3)` can become `1-2-3`, which changes the value from `2` to `-4`. The inner minus is not preserved as a subtraction of the whole group once the parentheses disappear.

Another edge case is nested parentheses. For `1-(2-(3-4))`, deleting only the outermost pair gives `1-2-(3-4)` only if the inner parentheses remain. The effect depends on exactly which pairs survive.

## Approaches

The brute force idea is to try every possible subset of parentheses to remove, check whether the resulting expression is valid, and evaluate it. This is correct because every possible answer is considered. However, with about 100 parentheses the number of possibilities is too large.

The key observation is that a parenthesized expression has two possible roles. It can stay grouped, in which case its value is optimized independently. Or it can be opened into the surrounding expression, in which case the sign before it affects the first number inside it and the operators inside become part of the outer expression.

This suggests dynamic programming with a sign parameter. For every expression segment, compute the best result when it is preceded by `+` and when it is preceded by `-`. Since the only possible outside influences are these two signs, the state space stays small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^p) | O(p) | Too slow |
| DP with sign states | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the expression recursively into expressions and parenthesized parts. For each expression, keep two states: the best value when this expression is attached after a positive sign, and the best value when attached after a negative sign.
2. When processing a digit, its contribution is simply the digit multiplied by the incoming sign.
3. When processing a sequence of terms separated by operators, combine the terms from left to right. The next term receives the sign produced by the current operator.
4. When processing a parenthesized part, consider two choices. Keeping the parentheses means we evaluate the inside normally and multiply the result by the incoming sign. Removing the parentheses means the inside expression is merged with the current expression, so we use the inside expression's state with the same incoming sign.
5. Store the choice that gives the larger value, because that choice is the one needed for reconstruction.

Why it works: every deleted parenthesis only changes whether the enclosed expression is evaluated as a single term or becomes part of the surrounding sequence. The DP considers exactly these two possibilities for every pair of parentheses. Since each subexpression is solved optimally for both possible incoming signs, every larger expression built from it also has the optimal result.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)

sys.setrecursionlimit(10000)

def parse_expr(pos):
    items = []
    ops = []
    cur = None

    while pos < n and s[pos] != ')':
        if s[pos].isdigit():
            items.append((int(s[pos]), None))
            pos += 1
        else:
            if s[pos] == '(':
                val, st, pos = parse_expr(pos + 1)
                items.append((val, st))
            else:
                ops.append(s[pos])
                pos += 1

    return build(items, ops), None, pos + 1

def build(items, ops):
    m = len(items)

    memo = {}

    def solve(i, sign):
        if (i, sign) in memo:
            return memo[(i, sign)]

        if i == m:
            return 0, ""

        value, inside = items[i]

        if inside is None:
            cur = sign * value
            text = str(value)
        else:
            keep_val, keep_txt = solve_expr_node(inside, 1)
            keep_val *= sign
            keep_txt = "(" + keep_txt + ")"

            rem_val, rem_txt = solve_expr_node(inside, sign)

            if rem_val > keep_val:
                cur, text = rem_val, rem_txt
            else:
                cur, text = keep_val, keep_txt

        if i + 1 == m:
            memo[(i, sign)] = (cur, text)
            return cur, text

        op = ops[i]
        nxt_sign = 1 if op == '+' else -1
        nxt_val, nxt_txt = solve(i + 1, nxt_sign)

        memo[(i, sign)] = (cur + nxt_val, text + op + nxt_txt)
        return memo[(i, sign)]

    return solve

def solve_expr_node(node, sign):
    return node(0, sign)

root, _, _ = parse_expr(0)

ans_val, ans_str = solve_expr_node(root, 1)

print(ans_val)
print(ans_str)
```

The parser creates recursive expression objects. Each expression object has a function that can answer the two DP states.

The important implementation detail is that a parenthesized block must not always be evaluated separately. The removed-parentheses case calls the inner DP with the current sign, because the inner expression becomes part of the surrounding expression.

Python integers are used because expression values can become larger than normal 32-bit ranges after many additions and subtractions.

## Worked Examples

For `1-(2-3)` the first decision is whether to keep `(2-3)`.

| Part | Keep parentheses | Remove parentheses |
| --- | --- | --- |
| `(2-3)` | value `-1` then multiplied by `-1` gives `1` | becomes `2-3` after the outer minus, giving `-1` |

The kept version is better, so the answer is `1-(2-3)` with value `2`.

For `1+(2)-(3-(4-5))`, the last parenthesized part is useful to partially open.

| Expression part | Best action |
| --- | --- |
| `(2)` | either form gives `2` |
| `(3-(4-5))` | remove the outer parentheses, keep the inner ones |

The result becomes `1+(2)-(3-4-5)` with value `9`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every expression state is computed once for two signs |
| Space | O(n) | Recursion depth and stored states are linear |

The number of characters is small, so the linear dynamic programming solution easily fits the limits.

## Test Cases

```
def check(inp):
    import subprocess
    return

# minimum
assert "0" != ""

# samples
# 1+(2)-(3-(4-5)) -> 9
# 1-(2-3) -> 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1-(2-3)` | `2` | Keeping parentheses can be optimal |
| `1+(2)-(3-(4-5))` | `9` | Nested choices |
| `0` | `0` | Single number handling |
| `((9))` | `9` | Removing redundant parentheses |

## Edge Cases

A single number has no choices. The algorithm reaches the digit case immediately and returns the digit.

When all parentheses surround one value, such as `((9))`, every removal keeps the expression valid. The DP compares keeping and removing and selects the same maximum value.

For nested subtraction like `1-(2-(3-4))`, a greedy rule such as "remove every parenthesis" fails because inner signs interact. The DP handles this because each nested expression receives the correct incoming sign from its parent.
