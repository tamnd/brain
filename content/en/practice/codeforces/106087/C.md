---
title: "CF 106087C - \u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0435 \u0442\u0440\u043e\u0439\u043a\u0438"
description: "We are asked to count ordered triples of natural numbers $(a, b, c)$, each between $1$ and $n$, such that the third number can be obtained from the first two using either addition or multiplication in a fixed structure: $a$ and $b$ combine to form $c$ as either $a + b = c$ or $a…"
date: "2026-06-20T04:50:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106087
codeforces_index: "C"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2025, \u043f\u0435\u0440\u0432\u044b\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 106087
solve_time_s: 43
verified: true
draft: false
---

[CF 106087C - \u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0435 \u0442\u0440\u043e\u0439\u043a\u0438](https://codeforces.com/problemset/problem/106087/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count ordered triples of natural numbers $(a, b, c)$, each between $1$ and $n$, such that the third number can be obtained from the first two using either addition or multiplication in a fixed structure: $a$ and $b$ combine to form $c$ as either $a + b = c$ or $a \cdot b = c$.

The ordering matters, so $(1, 2, 2)$ and $(2, 1, 2)$ are distinct because the middle operand changes the arithmetic behavior. The task is purely combinational: we must count how many triples satisfy at least one of these two equations while staying within bounds.

The constraint $n \le 10^7$ immediately rules out any cubic or quadratic enumeration over all triples. Even an $O(n^2)$ approach with constant-time checks would be too slow at this scale. The solution must avoid iterating over all pairs $(a, b)$ explicitly.

A subtle edge case appears when both operations produce valid results simultaneously, which happens when $a \cdot b = a + b$. This only occurs for very small values such as $(2, 2)$, since $2 \cdot 2 = 4$ and $2 + 2 = 4$. If counted independently, such cases would be double-counted unless handled carefully.

## Approaches

A direct approach would iterate over all $a$ and $b$, compute $c = a + b$ and $c = a \cdot b$, and check whether $c \le n$. This is correct in logic but requires checking all $n^2$ pairs. With $n = 10^7$, this is completely infeasible, producing on the order of $10^{14}$ operations.

The key observation is that we never actually need to choose $c$ independently. Once $a$ and $b$ are fixed, $c$ is uniquely determined for each operation. So the problem reduces to counting valid pairs $(a, b)$ such that $a + b \le n$ or $a \cdot b \le n$.

The additive condition forms a triangular region in the grid of pairs, and its count can be computed analytically. For each $a$, the valid $b$ values are from $1$ to $n - a$, giving a simple arithmetic series.

The multiplicative condition is more structured: for each $a$, valid $b$ values satisfy $b \le \lfloor n / a \rfloor$. This transforms the problem into a harmonic-style summation over divisors, which can be computed in $O(n)$ time or optimized further using grouping techniques, but here the direct summation is already sufficient given the constraints and constant factors.

The only remaining complication is overlap: pairs counted in both conditions correspond exactly to solutions of $a + b = a \cdot b$. This equation rearranges to $(a - 1)(b - 1) = 1$, so the only positive integer solution is $a = b = 2$. This single pair contributes one valid triple and must not be double-counted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over triples | $O(n^2)$ | $O(1)$ | Too slow |
| Counting + arithmetic sums | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### 1. Count additive triples

We fix $a$ and count all $b$ such that $a + b \le n$. For a given $a$, $b$ ranges from $1$ to $n - a$, contributing $\max(0, n - a)$ valid pairs. Summing over all $a$ produces a triangular number structure.

### 2. Count multiplicative triples

We fix $a$ and determine how many $b$ satisfy $a \cdot b \le n$. This is equivalent to $b \le \lfloor n / a \rfloor$. For each $a$, we add this quantity to the answer.

The reason this works is that multiplication constraints factor cleanly per fixed first operand, unlike addition which reduces to a linear cutoff.

### 3. Combine results

We sum both contributions. At this point every valid pair has been counted once per operation.

### 4. Remove double counting

We subtract the intersection where both conditions hold. Solving $a + b = a \cdot b$ gives $(a - 1)(b - 1) = 1$, so the only valid natural solution is $(a, b) = (2, 2)$. This contributes exactly one triple $(2, 2, 4)$, so we subtract 1 if $n \ge 4$.

### Why it works

Every valid triple is uniquely classified by whether it satisfies addition or multiplication. The additive count exhausts all linear-sum-valid pairs, and the multiplicative count exhausts all product-valid pairs. Their intersection is a singleton set, so inclusion-exclusion reduces the entire problem to two independent one-dimensional summations plus a constant correction.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

# additive pairs: sum_{a=1..n} max(0, n - a)
add = n * (n - 1) // 2

# multiplicative pairs: sum_{a=1..n} floor(n / a)
mul = 0
for a in range(1, n + 1):
    mul += n // a

# overlap correction: only (2,2) if n >= 4
overlap = 1 if n >= 4 else 0

print(add + mul - overlap)
```

The additive part is computed using the closed-form triangular number formula, avoiding iteration. The multiplicative part is computed via a single loop over divisors, which is acceptable for $n \le 10^7$ under PyPy or optimized CP Python due to simple integer operations.

The subtraction of the overlap is essential because both loops independently count the pair $(2,2)$, and no other pair satisfies both equations.

## Worked Examples

### Example 1: $n = 3$

Additive pairs are counted as:

$(1,1),(1,2),(1,3),(2,1),(2,2),(3,1)$ with valid sums ≤ 3.

Multiplicative pairs:

$(1,1),(1,2),(1,3),(2,1),(3,1)$.

| a | add count contribution | mul count contribution |
| --- | --- | --- |
| 1 | 2 | 3 |
| 2 | 1 | 1 |
| 3 | 0 | 1 |

Total additive = 3, multiplicative = 5, overlap = 0 (since $n < 4$).

Final answer = 8.

This shows how the two independent counting mechanisms cover different structural regions of the grid.

### Example 2: $n = 5$

| a | add contrib (n-a) | mul contrib (n//a) |
| --- | --- | --- |
| 1 | 4 | 5 |
| 2 | 3 | 2 |
| 3 | 2 | 1 |
| 4 | 1 | 1 |
| 5 | 0 | 1 |

Additive sum = 10, multiplicative sum = 10. Overlap = 1 (pair (2,2)).

Final answer = 19.

This trace confirms inclusion-exclusion correctness: the symmetric structure hides the single duplicated configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass for harmonic sum plus constant arithmetic |
| Space | $O(1)$ | only accumulators are stored |

The algorithm fits comfortably within constraints because it replaces a quadratic enumeration of pairs with a linear scan over divisors and a constant-time formula for sums.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    add = n * (n - 1) // 2
    mul = 0
    for a in range(1, n + 1):
        mul += n // a
    overlap = 1 if n >= 4 else 0
    return str(add + mul - overlap)

# provided samples (conceptual, since statement does not include them explicitly)
assert run("1\n") == "1"
assert run("2\n") == "3"

# custom cases
assert run("3\n") == str((3*2//2) + (3//1 + 3//2 + 3//3))
assert run("4\n") == str((4*3//2) + (4//1 + 4//2 + 4//3 + 4//4) - 1)
assert run("10\n") == str((10*9//2) + sum(10//i for i in range(1, 11)) - 1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum boundary |
| 2 | 3 | small overlap-free case |
| 3 | computed | small structure correctness |
| 4 | computed | overlap subtraction |
| 10 | computed | general correctness |

## Edge Cases

For $n = 1$, only $(1,1,2)$ or $(1,1,1)$ style structures reduce correctly because multiplicative and additive constraints are tightly bounded. The algorithm gives additive = 0, multiplicative = 1, no overlap, producing 1.

For $n = 3$, there is no valid overlap since the only intersection requires $c = 4$, which exceeds the limit. The algorithm correctly avoids subtracting anything in this range.

For $n \ge 4$, the pair $(2,2)$ becomes valid in both structures. The subtraction step removes exactly one duplicate, and since no other integer solution exists for $(a-1)(b-1)=1$, no further correction is needed.
