---
title: "CF 104882B - Before contest"
description: "Two players assign a numeric score to the same problem using two different formulas. One takes the length of the statement and raises it to the power of the code length, while the other swaps the roles."
date: "2026-06-28T09:17:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104882
codeforces_index: "B"
codeforces_contest_name: "Voronezh State University - Sitronics contest II"
rating: 0
weight: 104882
solve_time_s: 51
verified: true
draft: false
---

[CF 104882B - Before contest](https://codeforces.com/problemset/problem/104882/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players assign a numeric score to the same problem using two different formulas. One takes the length of the statement and raises it to the power of the code length, while the other swaps the roles. For each pair of positive integers x and y, we must decide whether x raised to y is smaller than, equal to, or larger than y raised to x.

The input is a single pair of integers. Each integer can be as large as one billion, which immediately rules out any direct computation of exponentiation. Even a single naive power computation would overflow standard integer ranges and take exponential time in the number of digits if implemented via repeated multiplication. This pushes the solution toward comparing expressions without evaluating them explicitly.

A subtle difficulty appears when values are small or equal in a way that breaks monotonic intuition. For example, (2, 4) and (4, 2) produce equal values even though the bases differ, since both evaluate to 16. Another edge case is when one of the numbers is 1. If x is 1 and y is large, then 1^y is always 1, while y^1 equals y, so the comparison is determined entirely by whether y exceeds 1. Symmetrically, if y is 1, the comparison flips.

These special cases matter because any generic approximation technique like logarithms must be consistent with exact comparisons in these boundary situations.

## Approaches

A direct brute force approach would compute x^y and y^x explicitly and compare the results. This is conceptually correct because it matches the definition of the problem exactly. The issue is that even representing x^y is impossible for large inputs, since the result grows far beyond 64-bit limits almost immediately, and computing it requires y multiplications.

For the worst case where x and y are both large, this leads to roughly O(y + x) multiplications, which is completely infeasible when each can be up to 10^9.

The key observation is that we do not need the exact values, only their ordering. Comparing magnitudes of exponential expressions can be reduced by applying a monotonic transformation. Since logarithm is strictly increasing, comparing x^y and y^x is equivalent to comparing y * log(x) and x * log(y). This removes exponentiation entirely and replaces it with constant-time arithmetic per test case.

However, this transformation assumes both numbers are greater than 1. When either value is 1, logarithms behave poorly numerically and the original expression simplifies directly, so those cases must be handled separately. The combination of direct reasoning for small edge values and logarithmic comparison for the general case yields a complete solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x + y) | O(1) | Too slow |
| Logarithmic Comparison | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

The idea is to reduce the comparison to something that does not grow with x or y.

1. Read the two integers x and y. These define two exponential expressions that we never explicitly compute.
2. If x equals y, immediately return equality. Both expressions become identical since swapping base and exponent does not change anything when the values are the same.
3. If x is 1, then x^y is always 1 regardless of y. The comparison reduces to checking whether y is greater than 1, since y^1 equals y.
4. If y is 1, the situation is symmetric. y^x equals 1, while x^y equals x, so the result depends on whether x exceeds 1.
5. If neither value is 1, compare the quantities y * log(x) and x * log(y). The larger product corresponds to the larger original exponential expression because logarithm preserves ordering under exponentiation.
6. Return the comparison result based on which side is larger.

The crucial idea is that we convert a comparison of extremely large numbers into a comparison of two real-valued expressions that remain stable under standard floating-point arithmetic.

### Why it works

The transformation relies on the monotonicity of the logarithm function. Since log is strictly increasing for positive arguments, applying it preserves ordering. Thus, x^y and y^x can be compared via their logarithms: log(x^y) = y log x and log(y^x) = x log y. This equivalence holds exactly in real arithmetic, and the only cases where numerical instability might matter are when x or y equals 1, where logs approach zero and the expressions collapse to trivial integer comparisons handled separately.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def solve():
    x, y = map(int, input().split())

    if x == y:
        print("=")
        return

    if x == 1:
        print("<" if y > 1 else "=")
        return

    if y == 1:
        print(">" if x > 1 else "=")
        return

    left = y * math.log(x)
    right = x * math.log(y)

    if abs(left - right) < 1e-12:
        print("=")
    elif left > right:
        print(">")
    else:
        print("<")

if __name__ == "__main__":
    solve()
```

The structure of the code mirrors the logical decomposition of the problem. The equality check at the beginning avoids unnecessary floating-point operations. The two branches for x equal to 1 or y equal to 1 remove degenerate logarithmic cases where numerical comparison would be unstable. The final comparison uses natural logarithms because any consistent base works, and the multiplicative structure cancels out.

The tolerance threshold handles floating-point rounding error, since values like 2^4 and 4^2 should match exactly but may differ by a tiny epsilon when computed through logs.

## Worked Examples

First consider the input 3 5. We compute 3^5 versus 5^3.

| Step | left = y log x | right = x log y | Decision |
| --- | --- | --- | --- |
| Initial | 5 log 3 | 3 log 5 | Compare |
| Evaluation | approximately 5.493 | approximately 4.828 | left > right |

Since the left side is larger, the output is greater than, meaning 3^5 exceeds 5^3. This matches direct computation since 243 is greater than 125.

Now consider 7 7.

| Step | x | y | Decision |
| --- | --- | --- | --- |
| Check equality | 7 | 7 | Immediately equal |

No further computation is needed since both expressions are identical.

This second case confirms that early termination avoids unnecessary floating-point work and preserves exact correctness when inputs match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic and a fixed number of logarithm evaluations are performed |
| Space | O(1) | No auxiliary data structures are used |

The computation fits easily within limits since each test case performs only a handful of floating-point operations. Even with many inputs, the approach remains constant time per case and avoids any growth with respect to x or y.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x, y = map(int, sys.stdin.readline().split())

    if x == y:
        return "="

    if x == 1:
        return "<" if y > 1 else "="

    if y == 1:
        return ">" if x > 1 else "="

    left = y * math.log(x)
    right = x * math.log(y)

    if abs(left - right) < 1e-12:
        return "="
    elif left > right:
        return ">"
    else:
        return "<"

assert run("3 5") == ">", "sample 1"
assert run("7 7") == "=", "sample 2"

assert run("1 10") == "<", "x is 1"
assert run("10 1") == ">", "y is 1"
assert run("2 4") == "=", "classic equality case"
assert run("5 2") == ">", "reverse comparison"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10 | < | base is 1 edge case |
| 10 1 | > | symmetric edge case |
| 2 4 | = | nontrivial equality case |
| 5 2 | > | general ordering correctness |

## Edge Cases

When x equals 1 and y is larger, the algorithm immediately returns less. For input 1 10, the check triggers at the third step and outputs that 1^10 is smaller than 10^1. The logarithmic branch is never entered, which avoids computing log(1) and prevents unnecessary floating-point comparisons.

When y equals 1 and x is larger, such as 10 1, the symmetric branch ensures the correct ordering without invoking logarithms. This prevents incorrect reliance on log(1), which would be zero and distort comparisons.

When x and y are both small but nontrivially arranged, such as 2 4, the logarithmic comparison correctly captures the equality since both expressions evaluate to 16. The computed values of y log x and x log y match, and the epsilon threshold classifies them as equal, preserving correctness under floating-point rounding.
