---
title: "CF 1236B - Alice and the List of Presents"
description: "We are given several kinds of items, where each kind is unlimited in supply. We also have several distinct boxes, each belonging to a different friend, so boxes are labeled and cannot be swapped. For each kind of item, Alice chooses a subset of boxes to place that kind into."
date: "2026-06-13T19:17:37+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1236
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 593 (Div. 2)"
rating: 1500
weight: 1236
solve_time_s: 371
verified: true
draft: false
---

[CF 1236B - Alice and the List of Presents](https://codeforces.com/problemset/problem/1236/B)

**Rating:** 1500  
**Tags:** combinatorics, math  
**Solve time:** 6m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several kinds of items, where each kind is unlimited in supply. We also have several distinct boxes, each belonging to a different friend, so boxes are labeled and cannot be swapped.

For each kind of item, Alice chooses a subset of boxes to place that kind into. Inside any single box, she is not allowed to place more than one item of the same kind, but that restriction is automatically satisfied because a kind is either placed into a box or not placed there. The key constraint is that every kind must appear in at least one box, so no kind is completely unused.

So the problem reduces to counting how many ways we can assign to each of the n kinds a non-empty subset of the m labeled boxes.

Each kind is independent in terms of choice, but the global requirement “every kind is used at least once somewhere” is already enforced per-kind, so there is no coupling between different kinds. The subtlety is not interaction between kinds, but correctly interpreting that each kind chooses a subset of boxes, and all subsets must be non-empty.

The input sizes go up to 10^9, so any approach that enumerates subsets, iterate over boxes, or uses dynamic programming over n or m is impossible. Even O(n) or O(m) per test case is too large. The solution must reduce everything to a closed-form expression computable in logarithmic time using modular exponentiation.

A common failure case is interpreting the condition incorrectly as assigning each box a subset of kinds independently, which leads to counting (2^n - 1)^m or similar incorrect expressions. Another mistake is forgetting that empty selection per kind is disallowed, which would incorrectly include zero assignments.

## Approaches

Start by focusing on a single kind. For one fixed kind, we decide in which boxes it appears. Since there are m distinct boxes, every box is either chosen or not chosen for this kind. That gives 2^m possible subsets. However, the empty subset is forbidden because every kind must appear in at least one box, so the number of valid choices for one kind is 2^m - 1.

Now consider multiple kinds. Each kind makes its own independent choice of a non-empty subset of boxes. Since choices for different kinds do not interfere with each other, we multiply the number of choices across all n kinds. That gives (2^m - 1)^n.

This is the key structural simplification: the problem is not about distributing objects across boxes, but about assigning to each type a subset of containers. The independence of types collapses the combinatorics into a simple power expression.

The brute-force idea would be to iterate over all subsets of boxes for each kind and then enforce global constraints. That would be O(2^m * n), which is impossible even for m = 20, let alone 10^9. The observation that each kind is independent removes any need for enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of subsets | O(n · 2^m) | O(1) | Too slow |
| Closed form with modular exponentiation | O(log n + log m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that for a fixed kind, every box independently decides whether it contains that kind. This gives 2^m possible assignments for one kind.
2. Exclude the case where no box contains the kind, since every kind must appear at least once. This reduces the count to 2^m − 1.
3. Treat each kind independently because choices for different kinds do not affect each other. This independence allows multiplication of possibilities across all kinds.
4. Raise the per-kind count to the power n, giving (2^m − 1)^n.
5. Compute 2^m modulo MOD using fast binary exponentiation.
6. Subtract 1 carefully under modulo arithmetic to avoid negative values.
7. Raise the result to power n using modular exponentiation again.

Why it works: each valid configuration is uniquely determined by independently selecting, for each kind, a non-empty subset of boxes. There is a bijection between global configurations and tuples of n non-empty subsets of an m-element set. Since the Cartesian product structure holds exactly, multiplication of counts is exact and no overcounting occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modexp(a, e):
    res = 1
    a %= MOD
    while e > 0:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

n, m = map(int, input().split())

# number of non-empty subsets of boxes for one kind
base = modexp(2, m) - 1
base %= MOD

# total ways
ans = modexp(base, n)

print(ans)
```

The solution first computes 2^m modulo MOD using fast exponentiation. The subtraction of 1 removes the empty subset and must be done modulo MOD to avoid negative values. The resulting base represents valid choices for one kind. Then the second exponentiation raises this base to n, reflecting independent assignment of subsets for each kind.

A common implementation pitfall is forgetting to take modulo after subtraction, which can produce negative intermediate values and break subsequent exponentiation. Another subtle issue is assuming Python’s built-in pow alone is enough without handling the minus one carefully under modulo arithmetic.

## Worked Examples

### Example 1

Input:

```
1 3
```

Here n = 1 and m = 3. For the single kind, all non-empty subsets of 3 boxes are valid.

| Step | Value |
| --- | --- |
| 2^m | 8 |
| 2^m - 1 | 7 |
| (2^m - 1)^n | 7 |

Output is 7.

This confirms the interpretation that we are simply choosing a non-empty subset of boxes for the only kind.

### Example 2

Input:

```
2 2
```

Now n = 2, m = 2.

| Step | Value |
| --- | --- |
| 2^m | 4 |
| 2^m - 1 | 3 |
| (2^m - 1)^n | 9 |

Each of the two kinds independently chooses one of three non-empty subsets of {box1, box2}.

This confirms independence across kinds and shows multiplicative structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n + log m) | Two modular exponentiations using binary exponentiation |
| Space | O(1) | Only a constant number of variables are maintained |

The constraints n, m ≤ 10^9 make direct iteration impossible, but exponentiation in logarithmic time is easily fast enough under a 1 second limit.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def modexp(a, e):
    res = 1
    a %= MOD
    while e > 0:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    base = modexp(2, m) - 1
    base %= MOD
    return str(modexp(base, n))

# provided samples
assert solve("1 3\n") == "7"

# minimum edge case
assert solve("1 1\n") == "1"

# symmetric case
assert solve("2 2\n") == "9"

# larger small case
assert solve("3 2\n") == str(pow((pow(2,2,MOD)-1),3,MOD))

# large exponent sanity check
assert solve("10 10\n") == str(pow((pow(2,10,MOD)-1),10,MOD))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimal configuration correctness |
| 2 2 | 9 | independence across kinds |
| 3 2 | computed | exponentiation correctness |
| 10 10 | computed | large value stability |

## Edge Cases

When m = 1, each kind can only be placed into the single box, so there is exactly one valid subset. The formula gives 2^1 − 1 = 1, and raising to n keeps it 1, matching the intuition that all kinds must go into the only available box.

When n = 1, the problem reduces to selecting any non-empty subset of boxes for a single kind. The formula correctly yields 2^m − 1. For example, with m = 3, the result is 7, matching all possible placements.

A potential failure case is forgetting the subtraction of 1 for empty subsets. If one incorrectly uses 2^(m·n), it overcounts configurations where some kinds are never placed. The correct structure enforces per-kind non-emptiness, which is why the subtraction must happen before exponentiation.
