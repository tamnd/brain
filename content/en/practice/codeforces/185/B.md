---
title: "CF 185B - Mushroom Scientists"
description: "We are asked to find a point in three-dimensional space, with non-negative coordinates, such that the sum of the coordinates does not exceed a given value $S$."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 185
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 118 (Div. 1)"
rating: 1800
weight: 185
solve_time_s: 79
verified: true
draft: false
---

[CF 185B - Mushroom Scientists](https://codeforces.com/problemset/problem/185/B)

**Rating:** 1800  
**Tags:** math, ternary search  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find a point in three-dimensional space, with non-negative coordinates, such that the sum of the coordinates does not exceed a given value $S$. The “distance” of this point is defined not by the usual Euclidean metric, but by the mushroom scientists’ metric: $x^a \cdot y^b \cdot z^c$, where $a$, $b$, and $c$ are given non-negative integers. Our goal is to maximize this value.

The inputs are $S$, a non-negative integer up to 1000, and the exponents $a$, $b$, and $c$, each also up to 1000. This means the feasible region for the coordinates is the tetrahedron formed by the non-negative octant of $\mathbb{R}^3$ cut by the plane $x + y + z = S$. The large exponents suggest that even small changes in coordinates can produce huge differences in the product, so we must be precise with floating-point arithmetic.

An edge case arises when one or more of the exponents is zero. For instance, if $a = 0$, then the function does not depend on $x$ at all, so any $x$ within the allowed range yields the same contribution. A naive approach that blindly distributes $S$ evenly among coordinates would fail for such inputs. For example, if $S=3$ and $a=0, b=1, c=2$, then $x$ can be any value from 0 to 3, but to maximize $y^b \cdot z^c = y \cdot z^2$, the optimal choice is $y=1, z=2$, not an even split.

Another subtle case occurs when multiple exponents are equal or zero. We must handle ties carefully, since multiple distributions of $S$ may achieve the same maximum value.

## Approaches

The brute-force approach would enumerate all triples $(x, y, z)$ such that $x + y + z \le S$, evaluating the function for each. With $S \le 1000$ and allowing a reasonable step size of 1, this leads to about $O(S^3) = 10^9$ evaluations, which is too large. Even coarser discretizations risk missing the exact optimal values, especially because the function is highly sensitive to coordinate changes for large exponents.

The key insight comes from recognizing that the function $f(x, y, z) = x^a y^b z^c$ is continuous and unimodal along any line in the positive orthant. If we take the natural logarithm, we get $\ln f(x, y, z) = a \ln x + b \ln y + c \ln z$. This is a concave function with respect to $(x, y, z)$ over the feasible region. For such functions constrained by a plane, the maximum occurs at the boundary, and specifically, the Karush-Kuhn-Tucker (KKT) conditions give the solution: the ratio of each variable to its exponent must be the same, i.e., $x : y : z = a : b : c$. We scale this ratio so that $x + y + z = S$. Zero exponents correspond to coordinates that should be zero, because they do not contribute to the product.

This observation allows us to reduce the three-dimensional optimization problem to a simple arithmetic computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(S^3) | O(1) | Too slow |
| Ratio Scaling via KKT | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input values $S$, $a$, $b$, $c$. These define the total available sum and the exponents of each coordinate in the mushroom metric.
2. Count the sum of positive exponents: $total = a + b + c$. This will be used to scale each coordinate proportionally. If all exponents are zero, set the output arbitrarily to $(0, 0, 0)$, since the product is always 1.
3. For each coordinate corresponding to a positive exponent, compute its value as $coordinate = S \cdot \frac{exponent}{total}$. This distributes $S$ in proportion to the exponents. For coordinates whose exponent is zero, set them to 0.
4. Print the resulting coordinates with sufficient precision (at least 6 decimal places), ensuring that the sum does not exceed $S$ and that the floating-point error does not affect the logarithmic comparison.

Why it works: By taking logarithms, the problem reduces to a linear combination of $\ln x$, $\ln y$, and $\ln z$ weighted by $a, b, c$. For a concave function with a linear constraint $x + y + z = S$, the maximum occurs when the gradients are aligned with the constraint plane, which exactly corresponds to the proportional distribution rule derived above. Zero exponents correctly yield zero coordinates because increasing them does not increase the product.

## Python Solution

```python
import sys
input = sys.stdin.readline

S = int(input())
a, b, c = map(int, input().split())

total = a + b + c

if total == 0:
    print("0.0 0.0 0.0")
else:
    x = S * a / total if a > 0 else 0.0
    y = S * b / total if b > 0 else 0.0
    z = S * c / total if c > 0 else 0.0
    print(f"{x:.9f} {y:.9f} {z:.9f}")
```

The code starts by reading the input values. We then compute the sum of positive exponents to scale the coordinates. If all exponents are zero, we output zeros. Otherwise, each coordinate with a positive exponent receives a proportional share of $S$. We use nine decimal places to satisfy the logarithmic tolerance requirement.

## Worked Examples

**Sample 1**: $S = 3$, $a = 1, b = 1, c = 1$

| Step | total | x | y | z |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3*1/3 = 1.0 | 3*1/3 = 1.0 | 3*1/3 = 1.0 |

Explanation: Each exponent is equal, so the sum $S$ is evenly split.

**Custom Sample 2**: $S = 3$, $a = 0, b = 1, c = 2$

| Step | total | x | y | z |
| --- | --- | --- | --- | --- |
| 1 | 3 | 0.0 | 3*1/3 = 1.0 | 3*2/3 = 2.0 |

Explanation: $x$ has zero exponent, so it does not contribute. The remaining sum is split proportionally between $y$ and $z$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations are needed, independent of $S$ or exponents |
| Space | O(1) | Only a few variables are stored |

Since $S \le 1000$ and exponents $\le 1000$, the arithmetic is safe, and the algorithm runs instantly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    S = int(sys.stdin.readline())
    a, b, c = map(int, sys.stdin.readline().split())
    total = a + b + c
    if total == 0:
        return "0.0 0.0 0.0"
    x = S * a / total if a > 0 else 0.0
    y = S * b / total if b > 0 else 0.0
    z = S * c / total if c > 0 else 0.0
    return f"{x:.9f} {y:.9f} {z:.9f}"

# Provided sample
assert run("3\n1 1 1\n") == "1.000000000 1.000000000 1.000000000", "sample 1"

# Custom cases
assert run("3\n0 1 2\n") == "0.000000000 1.000000000 2.000000000", "zero exponent"
assert run("10\n5 0 5\n") == "5.000000000 0.000000000 5.000000000", "middle zero"
assert run("1000\n0 0 0\n") == "0.0 0.0 0.0", "all zero exponents"
assert run("6\n3 1 2\n") == "3.000000000 1.000000000 2.000000000", "unequal exponents"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n1 1 1 | 1 1 1 | Even distribution when |
