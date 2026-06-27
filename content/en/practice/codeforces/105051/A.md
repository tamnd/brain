---
title: "CF 105051A - \u0412\u044b\u0431\u043e\u0440\u044b \u0432 \u0420\u0418\u041b\u0418"
description: "Three candidates are receiving votes in an election. The first candidate currently has a votes, the second has b, and the third has c. More votes may still arrive, but only additional votes for the first candidate matter."
date: "2026-06-28T00:35:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105051
codeforces_index: "A"
codeforces_contest_name: "2023-2024 \u0424\u0438\u043d\u0430\u043b \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb"
rating: 0
weight: 105051
solve_time_s: 47
verified: true
draft: false
---

[CF 105051A - \u0412\u044b\u0431\u043e\u0440\u044b \u0432 \u0420\u0418\u041b\u0418](https://codeforces.com/problemset/problem/105051/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

Three candidates are receiving votes in an election. The first candidate currently has `a` votes, the second has `b`, and the third has `c`. More votes may still arrive, but only additional votes for the first candidate matter.

The task is to determine the smallest number of extra votes that must be given to the first candidate so that, after adding these votes, the first candidate holds at least half of all votes cast. “At least half” means that if we denote the final vote counts as `A`, `B`, and `C`, then `A` must satisfy `A ≥ (A + B + C) / 2`, or equivalently `2A ≥ A + B + C`.

The input sizes go up to `10^9`, which rules out any simulation of adding votes one by one. Any solution must be constant time, since even linear iteration over possible additional votes would be too slow.

A subtle point is how to interpret “50% of votes.” Since votes are integers, we are not dealing with rounding. The condition is purely arithmetic: the first candidate must have at least half of the total sum, not strictly more and not rounded.

A naive mistake is to think we need to “simulate until majority,” incrementing vote counts step by step. That would fail immediately under large constraints, and even small cases would be unnecessarily slow.

Another common incorrect interpretation is to compare against the maximum of the other candidates instead of the total. For example, ensuring `a+x ≥ max(b, c)` is not sufficient because the requirement is about the combined total, not pairwise dominance.

## Approaches

A brute-force approach would try increasing the number of extra votes `x` starting from zero and checking each time whether the first candidate reaches at least half of the total votes. Each check requires recomputing totals and verifying the inequality, so it costs O(1), but in the worst case `x` could grow up to around `b + c`, making the overall complexity O(b + c). With values up to `10^9`, this is completely infeasible.

The key observation is that the condition can be rewritten algebraically. After adding `x` votes, the first candidate has `a + x`, and the total is `a + b + c + x`. The requirement becomes:

`2(a + x) ≥ a + b + c + x`

Expanding and simplifying removes the dependency on the evolving total and reduces the problem to a direct inequality in `x`. This transforms the task into computing a single expression instead of searching.

The structure of the problem is linear because adding a vote increases both the numerator and denominator in a predictable way. This monotonicity guarantees that once the condition becomes true, it stays true, which is why solving the inequality directly gives the exact minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(b + c) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We want the smallest number of extra votes `x` such that the first candidate has at least half of the total votes after adding them.

1. Compute the current vote totals for all candidates. The total before adding new votes is `S = a + b + c`.
2. Assume we add `x` votes to the first candidate, so its new count becomes `a + x`, and the total becomes `S + x`.
3. Translate the condition “at least half” into an inequality: `2(a + x) ≥ S + x`. This removes division and avoids floating-point reasoning.
4. Expand the inequality to isolate `x`. This gives `2a + 2x ≥ a + b + c + x`.
5. Simplify by collecting terms: `a + x ≥ b + c`.
6. Solve for `x`, yielding `x ≥ (b + c - a)`.
7. Since `x` cannot be negative, take `x = max(0, b + c - a)`.

Why it works

The inequality captures exactly the point where the first candidate’s share crosses or reaches half of the total. The transformation removes the dynamic dependency between numerator and denominator and reduces everything to a single linear constraint. Because the left-hand side grows faster than the right-hand side as `x` increases, the smallest integer satisfying the inequality is exactly the threshold computed above, and any smaller value fails the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input().strip())
b = int(input().strip())
c = int(input().strip())

x = b + c - a
if x < 0:
    x = 0

print(x)
```

The implementation directly applies the derived formula. Each input is read independently, and no additional processing is required.

The only subtlety is ensuring the result is not negative. If the first candidate already has enough votes to satisfy the condition, the computed value becomes negative, and we clamp it to zero.

## Worked Examples

### Example 1

Input:

```
7
15
9
```

We compute `x = b + c - a = 15 + 9 - 7 = 17`.

| Step | a + x | total (a+b+c+x) | condition check |
| --- | --- | --- | --- |
| 0 | 7 | 31 | 14 < 31 |
| 17 | 24 | 48 | 48 ≥ 48 |

This shows that 17 is the first point where the candidate reaches exactly half of the total votes.

### Example 2

Input:

```
491
257
145
```

Compute `x = 257 + 145 - 491 = -89`, so `x = 0`.

| Step | a + x | total | condition check |
| --- | --- | --- | --- |
| 0 | 491 | 893 | 982 ≥ 893 |

The first candidate already exceeds half of the total votes, so no additional votes are needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations on three integers |
| Space | O(1) | No auxiliary data structures used |

The constraints allow values up to `10^9`, but since the solution is purely arithmetic, there is no risk of overflow in Python and no performance concerns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a = int(input().strip())
    b = int(input().strip())
    c = int(input().strip())

    x = b + c - a
    if x < 0:
        x = 0
    return str(x)

# provided samples
assert run("7\n15\n9\n") == "17"
assert run("491\n257\n145\n") == "0"

# custom cases
assert run("0\n1\n1\n") == "2"
assert run("10\n0\n0\n") == "0"
assert run("5\n100\n0\n") == "95"
assert run("100\n50\n49\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 1 1 | 2 | minimum case where first starts at zero |
| 10 0 0 | 0 | already absolute majority |
| 5 100 0 | 95 | large imbalance requiring many votes |
| 100 50 49 | 0 | boundary where majority already holds |

## Edge Cases

When the first candidate already has enough votes, the derived expression `b + c - a` becomes negative. For input like `a = 100, b = 50, c = 49`, the formula gives `-1`, but the correct answer is `0`. The clamping step ensures correctness.

For input where `a = 0`, such as `0, 1, 1`, the formula gives `2`, and verifying step-by-step shows that with two added votes the first candidate reaches exactly half of the total votes.

Large values near `10^9` behave identically because the solution only depends on sums and differences, not on iterative simulation or scaling behavior.
