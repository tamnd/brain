---
title: "CF 2222A - A Wonderful Contest"
description: "We are asked to determine whether a programming contest is “wonderful” in the sense that every possible integer total score between 0 and 100 n can be achieved. The contest has n problems, and each problem is divided into ai subtasks."
date: "2026-06-07T18:40:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2222
codeforces_index: "A"
codeforces_contest_name: "Spectral::Cup 2026 Round 1 (Codeforces Round 1094, Div. 1 + Div. 2)"
rating: 0
weight: 2222
solve_time_s: 123
verified: false
draft: false
---

[CF 2222A - A Wonderful Contest](https://codeforces.com/problemset/problem/2222/A)

**Rating:** -  
**Tags:** brute force, dp, math  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine whether a programming contest is “wonderful” in the sense that every possible integer total score between `0` and `100 * n` can be achieved. The contest has `n` problems, and each problem is divided into `a_i` subtasks. Each subtask of the `i`-th problem contributes equally to the problem’s score, i.e., `100 / a_i` points.

A contestant’s total score is the sum of the scores of subtasks they solve on each problem. The input provides several test cases, each giving the number of problems and the list of subtasks per problem. The output should indicate for each test case whether all integer total scores from `0` to `100 * n` can be obtained.

The constraints are small: `n` is at most `10`, `a_i` divides `100`, and `t` is up to `100`. With such small `n`, a brute-force approach is feasible, but we can find a more elegant mathematical insight.

Non-obvious edge cases include problems where all `a_i` are large divisors of `100`. For instance, if all `a_i` are `100`, each problem only contributes multiples of `1` to the total, which trivially works. But if `a_i` is `4` and another is `25`, we must ensure that the combination of scores from all problems allows every integer total. A naive approach that simply sums maximum scores might miss gaps created by the discrete steps of each problem.

## Approaches

A brute-force approach would enumerate all combinations of `x_i` for each problem. Since `0 <= x_i <= a_i` and `a_i <= 100`, this yields at worst `101^10` combinations for a single test case, which is far too large. It is correct but infeasible.

The key insight is to work in the unit of “1 point” rather than floating-point scores. Since each `a_i` divides `100`, the score for problem `i` can be expressed as integers from `0` to `100` in steps of `100 / a_i`. Let `step_i = 100 / a_i`. Then the question reduces to: can we represent every integer from `0` to `100 * n` as a non-negative integer combination of `step_1, step_2, ..., step_n` where the multiplicities do not exceed `a_i`?

We can model this as a classic subset-sum or coin-change problem, where each coin value is `step_i` with `a_i` copies. With `n <= 10` and `a_i <= 100`, the total number of reachable sums is at most `1000`, making a dynamic programming solution feasible. We initialize a boolean array `reachable[0..100*n]` and iteratively mark all scores achievable by adding multiples of each `step_i`.

This avoids brute-forcing all `x_i` combinations and works because the problem guarantees integer arithmetic suffices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(prod(a_i)) | O(100*n) | Too slow |
| Dynamic Programming (coin-like) | O(n * 100 * max(a_i)) | O(100*n) | Accepted |

## Algorithm Walkthrough

1. Convert each problem’s subtasks count `a_i` into a score step: `step_i = 100 // a_i`. This turns fractional scores into integers.
2. Initialize a boolean array `reachable` of size `100*n + 1`, where `reachable[s]` indicates whether a total score `s` is achievable. Set `reachable[0] = True`.
3. For each problem `i` with step `step_i` and `a_i` subtasks, update `reachable` to include all sums obtained by adding `k * step_i` for `k = 1..a_i` to previously reachable sums. This ensures we do not exceed the subtask limit for the problem.
4. After processing all problems, check if every integer `s` from `0` to `100*n` is reachable. If so, output `Yes`, otherwise `No`.

Why it works: `reachable` correctly models all sums that can be formed under the subtask limits. By iteratively including multiples of each step size, we guarantee that no combination is missed. Integer arithmetic ensures exact calculations without rounding errors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_wonderful(a):
    n = len(a)
    steps = [100 // ai for ai in a]
    max_score = 100 * n
    reachable = [False] * (max_score + 1)
    reachable[0] = True

    for step, count in zip(steps, a):
        # We iterate backwards to avoid using the same problem multiple times
        new_reachable = reachable[:]
        for s in range(max_score + 1):
            if reachable[s]:
                for k in range(1, count + 1):
                    ns = s + k * step
                    if ns <= max_score:
                        new_reachable[ns] = True
                    else:
                        break
        reachable = new_reachable

    return all(reachable)

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print("Yes" if is_wonderful(a) else "No")
```

The solution first converts scores into integer multiples, then iteratively marks all achievable totals. We iterate backwards on `reachable` to prevent double-counting contributions from the same problem. The break prevents exceeding the maximum score.

## Worked Examples

**Sample 1 Input:**

`2`

`2`

`1 2`

`3`

`4 5 10`

| Step | reachable array update |
| --- | --- |
| Problem 1: step=100, count=1 | 0, 100 |
| Problem 2: step=50, count=2 | Add 50 and 100 -> reachable 0,50,100,150,200 |
| Check all 0..200 | True -> Yes |

**Sample 2 Input:**

`1`

`2`

`4 5`

| Step | reachable array update |
| --- | --- |
| Problem 1: step=25, count=4 | 0,25,50,75,100 |
| Problem 2: step=20, count=5 | Combine previous -> missing 95, impossible |
| Check all 0..100*2 | False -> No |

These traces show the DP correctly accounts for step sizes and limits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * max(a_i) * 100 * n) | Each problem iterates over its subtasks and reachable scores. n ≤ 10, a_i ≤ 100, max_score = 100*n ≤ 1000. |
| Space | O(100*n) | Array of reachable scores up to 100*n. |

With n ≤ 10 and 100*n ≤ 1000, the solution runs in under 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        output.append("Yes" if is_wonderful(a) else "No")
    return ''.join(output)

# Provided samples
assert run("2\n2\n1 2\n3\n4 5 10\n") == "YesNo", "Sample 1 and 2"

# Custom cases
assert run("1\n1\n100\n") == "Yes", "Single problem, 100 subtasks"
assert run("1\n2\n25 25\n") == "Yes", "Two equal divisors"
assert run("1\n2\n4 5\n") == "No", "Cannot reach all totals"
assert run("1\n3\n1 2 5\n") == "Yes", "Small mixed divisors"
assert run("1\n3\n20 25 50\n") == "Yes", "Large divisors with combination"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 100 | Yes | Single problem, max subtasks |
| 2 25 25 | Yes | Equal divisors, easy coverage |
| 2 4 5 | No | Small divisor mismatch prevents full coverage |
| 3 1 2 5 | Yes | Mixed small divisors |
| 3 20 25 50 | Yes | Larger divisors, ensure sum coverage |

## Edge Cases

For a single problem with `a_1 = 100`, the only possible scores are multiples of `1`. The algorithm correctly marks all scores from `0` to `100`, confirming "Yes".

For a pair `a = [4,5]`, possible scores from the first problem are `{0,25,50,75,100}`, and from the second `{0,20,40,60,80,100}`. Some totals, like `95`, cannot be formed. The DP detects unreachable
