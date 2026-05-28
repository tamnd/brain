---
title: "CF 20B - Equation"
description: "We are asked to solve a quadratic equation of the form $Ax^2 + Bx + C = 0$, where $A$, $B$, and $C$ are integers in the"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 20
codeforces_index: "B"
codeforces_contest_name: "Codeforces Alpha Round 20 (Codeforces format)"
rating: 2000
weight: 20
solve_time_s: 65
verified: true
draft: false
---

[CF 20B - Equation](https://codeforces.com/problemset/problem/20/B)

**Rating:** 2000  
**Tags:** math  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to solve a quadratic equation of the form $Ax^2 + Bx + C = 0$, where $A$, $B$, and $C$ are integers in the range $[-10^5, 10^5]$. The goal is to find all real roots of the equation, count them, and print them in ascending order with high precision. If the equation has infinitely many solutions, we should output $-1$. If there are no solutions, we print $0$.

The input coefficients can include zero, which introduces subtleties. For example, if $A = 0$, the equation reduces to linear ($Bx + C = 0$), and if both $A = 0$ and $B = 0$, the equation either has no solution (if $C \neq 0$) or infinitely many solutions (if $C = 0$).

The constraints are small enough that we do not need to worry about algorithmic efficiency beyond simple arithmetic. Computing square roots and performing conditional checks is well within the allowed time. The challenge lies entirely in handling all cases correctly and maintaining numerical precision.

Non-obvious edge cases include the following scenarios. If $A = 0$ and $B = 0$, then the solution depends entirely on $C$. For example, $0x^2 + 0x + 5 = 0$ has no roots, while $0x^2 + 0x + 0 = 0$ has infinitely many roots. Another subtlety arises when the discriminant is zero, producing exactly one root, which must not be duplicated in the output. Negative discriminants produce no real roots. Handling floating-point precision correctly is also necessary to ensure the printed roots have at least five digits after the decimal.

## Approaches

A naive approach would be to try all possible values of $x$ within a range, checking if they satisfy $Ax^2 + Bx + C = 0$ to some precision. This brute-force method is unnecessary, since the quadratic formula gives an exact analytical solution for any quadratic equation, provided we handle degenerate cases correctly. Enumerating $x$ over a large interval would require an unbounded number of operations and could never reliably identify roots with high precision.

The optimal approach relies on standard algebra. For $A \neq 0$, we compute the discriminant $D = B^2 - 4AC$. If $D > 0$, there are two distinct roots given by $(-B - \sqrt{D}) / (2A)$ and $(-B + \sqrt{D}) / (2A)$. If $D = 0$, there is one root $-B / (2A)$. If $D < 0$, there are no real roots. For the linear case ($A = 0$ and $B \neq 0$), there is exactly one root $-C / B$. If both $A$ and $B$ are zero, the solution is either zero roots or infinitely many roots depending on whether $C$ is zero.

The key insight is to treat the linear and quadratic cases separately and use the discriminant for quadratic equations. Careful ordering of conditions ensures that we do not attempt to divide by zero or take the square root of a negative number. Once roots are found, sorting them guarantees ascending order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Range of x) | O(1) | Too slow and imprecise |
| Analytical (discriminant) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers $A$, $B$, and $C$. These coefficients define the equation $Ax^2 + Bx + C = 0$.
2. Check if $A = 0$. If it is, the equation is not quadratic but linear.
3. If $A = 0$ and $B = 0$, check $C$. If $C = 0$, print $-1$ for infinitely many solutions. Otherwise, print $0$ for no solutions.
4. If $A = 0$ but $B \neq 0$, compute the single root $-C / B$, print $1$, and then the root with at least five digits after the decimal.
5. If $A \neq 0$, compute the discriminant $D = B^2 - 4AC$.
6. If $D < 0$, there are no real roots, so print $0$.
7. If $D = 0$, compute the single root $-B / (2A)$ and print $1$ followed by the root.
8. If $D > 0$, compute the two roots $(-B - \sqrt{D}) / (2A)$ and $(-B + \sqrt{D}) / (2A)$. Print $2$ followed by the roots in ascending order.

Why it works: Each case is mutually exclusive and exhaustive. The linear case is handled separately to avoid division by zero. The quadratic formula with discriminant analysis guarantees correct counting and computation of roots, and sorting the two roots ensures ascending order. There are no missing edge cases because every combination of zero/nonzero coefficients is considered.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

A, B, C = map(int, input().split())

if A == 0:
    if B == 0:
        if C == 0:
            print(-1)
        else:
            print(0)
    else:
        x = -C / B
        print(1)
        print(f"{x:.10f}")
else:
    D = B * B - 4 * A * C
    if D < 0:
        print(0)
    elif D == 0:
        x = -B / (2 * A)
        print(1)
        print(f"{x:.10f}")
    else:
        sqrt_D = math.sqrt(D)
        x1 = (-B - sqrt_D) / (2 * A)
        x2 = (-B + sqrt_D) / (2 * A)
        x1, x2 = sorted([x1, x2])
        print(2)
        print(f"{x1:.10f}")
        print(f"{x2:.10f}")
```

The code separates linear and quadratic cases to avoid zero division and correctly handles infinite roots. We use `math.sqrt` only for positive discriminants and sort roots when two are present to ensure ascending order. Printing with `.10f` provides sufficient precision for the problem's requirements.

## Worked Examples

**Sample 1:** `1 -5 6`

| Step | A | B | C | D | Roots | Output |
| --- | --- | --- | --- | --- | --- | --- |
| Input | 1 | -5 | 6 | 25-24=1 | 2, 3 | 2, 2.0, 3.0 |

This shows a standard quadratic with two distinct roots. The algorithm correctly computes discriminant and sorts the roots.

**Custom Sample 2:** `0 0 0`

| Step | A | B | C | Roots | Output |
| --- | --- | --- | --- | --- | --- |
| Input | 0 | 0 | 0 | Infinite | -1 |

This demonstrates the infinite solution case. Linear check catches both coefficients zero and returns `-1`.

**Custom Sample 3:** `0 4 -8`

| Step | A | B | C | Roots | Output |
| --- | --- | --- | --- | --- | --- |
| Input | 0 | 4 | -8 | 2 | 1, 2.0 |

Linear equation case correctly identifies one root.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations, square root, and conditional checks are performed. |
| Space | O(1) | Only a handful of variables used for coefficients and roots. |

The algorithm is well within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        # call the solution
        A, B, C = map(int, input().split())
        if A == 0:
            if B == 0:
                if C == 0:
                    print(-1)
                else:
                    print(0)
            else:
                x = -C / B
                print(1)
                print(f"{x:.10f}")
        else:
            D = B * B - 4 * A * C
            if D < 0:
                print(0)
            elif D == 0:
                x = -B / (2 * A)
                print(1)
                print(f"{x:.10f}")
            else:
                sqrt_D = math.sqrt(D)
                x1 = (-B - sqrt_D) / (2 * A)
                x2 = (-
```
