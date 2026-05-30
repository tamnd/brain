---
title: "CF 486A - Calculating Function"
description: "We are given a single positive integer and asked to evaluate a function built by alternating addition and subtraction of consecutive integers starting from 1. The sequence begins by subtracting 1, then adding 2, subtracting 3, adding 4, and so on until we reach n."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 486
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 277 (Div. 2)"
rating: 800
weight: 486
solve_time_s: 649
verified: false
draft: false
---

[CF 486A - Calculating Function](https://codeforces.com/problemset/problem/486/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 10m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single positive integer and asked to evaluate a function built by alternating addition and subtraction of consecutive integers starting from 1. The sequence begins by subtracting 1, then adding 2, subtracting 3, adding 4, and so on until we reach n. The sign of each term depends entirely on its position in the sequence: odd-positioned terms contribute negatively and even-positioned terms contribute positively.

The input is just one integer, so the task reduces to computing a deterministic arithmetic expression in an efficient way. The output is a single integer value representing the final result of this alternating sum.

The constraint is extremely large, up to 10^15. This immediately rules out any approach that iterates from 1 to n. Even a linear scan would require 10^15 operations, which is far beyond any feasible time limit. The solution must therefore run in constant time or logarithmic time at worst, though the structure strongly suggests a closed-form expression.

A subtle edge case appears when n is small or when parity changes behavior. For example, if n = 1, the result is simply -1. If n = 2, we get -1 + 2 = 1. If n = 3, we get -1 + 2 - 3 = -2. A naive implementation that assumes the sum is always non-negative or ignores alternating signs will fail immediately on these small cases.

Another common pitfall is mishandling integer division when deriving a formula. Since the pattern depends on pairs of terms, incorrect grouping can produce off-by-one errors when n is odd.

## Approaches

A direct brute-force approach evaluates the expression term by term. We maintain a running sum and alternate the sign as we iterate from 1 to n. This is straightforward and correct because it directly follows the definition of the function. However, its runtime grows linearly with n, requiring up to 10^15 additions in the worst case, which is computationally impossible.

The key observation is that the expression naturally groups into pairs: (-1 + 2), (-3 + 4), (-5 + 6), and so on. Each full pair contributes exactly +1. This transforms a long alternating sequence into a simple count of how many complete pairs exist, plus possibly one leftover term if n is odd.

If n is even, every number is part of a complete pair, and the result is simply n/2. If n is odd, we have one extra negative term at the end, reducing the total by (n + 1)/2 compared to the even case, which simplifies to a clean formula as well. This pairing structure eliminates the need for iteration entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Pairing Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the result based on whether n is even or odd.

1. Read the integer n from input. This value determines how many alternating terms are included in the sum.
2. Check whether n is divisible by 2. This determines whether the sequence ends on a positive or negative term.
3. If n is even, compute n // 2. This works because every pair (-1 + 2), (-3 + 4), and so on sums to +1, and there are exactly n/2 such pairs.
4. If n is odd, compute -(n // 2 + 1). The first n//2 pairs contribute +1 each, but the final unpaired term is -(n), which shifts the sum downward to this compact expression.

Why it works: the sequence partitions cleanly into disjoint adjacent pairs of the form (2k-1, 2k), each contributing +1. When n is even, there are no leftover elements, so the sum is exactly the number of pairs. When n is odd, one extra negative term remains, and subtracting its contribution from the paired total produces the final closed form. The structure guarantees that no term overlaps or is double-counted, so the decomposition is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

if n % 2 == 0:
    print(n // 2)
else:
    print(-(n // 2 + 1))
```

The code directly implements the parity-based formula. The key implementation detail is integer division using `//`, which ensures correct floor behavior in Python for both even and odd cases. The branch structure avoids constructing or iterating over the sequence entirely, which is essential given the input size.

The even case returns the number of full contributing pairs. The odd case correctly accounts for the final negative term by shifting the result downward by one additional unit beyond the number of complete pairs.

## Worked Examples

### Example 1: n = 4

| Step | n | Parity | Computation | Result |
| --- | --- | --- | --- | --- |
| 1 | 4 | even | 4 // 2 | 2 |

The sequence is -1 + 2 - 3 + 4, which groups as (-1 + 2) + (-3 + 4). Each pair contributes +1, giving a total of 2, matching the formula.

### Example 2: n = 5

| Step | n | Parity | Computation | Result |
| --- | --- | --- | --- | --- |
| 1 | 5 | odd | -(5 // 2 + 1) | -3 |

The sequence is -1 + 2 - 3 + 4 - 5. The first two pairs contribute +2, and the final -5 reduces the total to -3. The formula captures this directly.

These examples confirm that pairing fully accounts for the structure and that the odd case correctly handles the trailing negative term.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic and a parity check are performed |
| Space | O(1) | No additional data structures are used |

The solution is constant time and constant memory, which easily satisfies the constraint up to 10^15.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline().strip())
    if n % 2 == 0:
        return str(n // 2)
    else:
        return str(-(n // 2 + 1))

def run(inp: str) -> str:
    return solve(inp)

# provided samples
assert run("4\n") == "2", "sample 1"
assert run("5\n") == "-3", "sample 2"

# minimum input
assert run("1\n") == "-1", "n = 1"

# small even
assert run("2\n") == "1", "n = 2"

# larger odd
assert run("9\n") == "-5", "odd case check"

# large even sanity
assert run("1000000000000000\n") == str(1000000000000000 // 2), "large even"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | -1 | minimum boundary |
| 2 | 1 | smallest even case |
| 9 | -5 | odd structure correctness |
| 10^15 | 5e14 | large constraint handling |

## Edge Cases

For n = 1, the computation has only a single term. The algorithm classifies it as odd, so it computes -(1 // 2 + 1) = -1. The sequence definition also gives -1, confirming correctness.

For n = 2, the sequence is -1 + 2. The algorithm uses the even branch, producing 2 // 2 = 1, which matches the direct evaluation.

For n = 3, we have -1 + 2 - 3 = -2. The algorithm computes -(3 // 2 + 1) = -(1 + 1) = -2, correctly accounting for the leftover negative term after one complete pair.

These traces show that both parity branches align exactly with the structure of the sequence and handle incomplete pairing without error.
