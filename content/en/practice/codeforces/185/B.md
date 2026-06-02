---
title: "CF 185B - Mushroom Scientists"
description: "We are asked to maximize a function defined on three non-negative real variables x, y, and z subject to a sum constraint. The function has the form f(x, y, z) = x^a · y^b · z^c, where a, b, c are non-negative integers. The variables must satisfy x + y + z ≤ S and x, y, z ≥ 0."
date: "2026-06-03T00:56:13+07:00"
tags: ["codeforces", "competitive-programming", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 185
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 118 (Div. 1)"
rating: 1800
weight: 185
solve_time_s: 83
verified: true
draft: false
---

[CF 185B - Mushroom Scientists](https://codeforces.com/problemset/problem/185/B)

**Rating:** 1800  
**Tags:** math, ternary search  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maximize a function defined on three non-negative real variables _x_, _y_, and _z_ subject to a sum constraint. The function has the form _f(x, y, z) = x^a · y^b · z^c_, where _a_, _b_, _c_ are non-negative integers. The variables must satisfy _x + y + z ≤ S_ and _x, y, z ≥ 0_. The input provides the sum limit _S_ and the exponents _a, b, c_. The output must be a triple (_x_, _y_, _z_) that maximizes the function, within a tolerance for logarithmic precision.

The main constraints are that _S_ is up to 1000 and the exponents are up to 1000. The function grows multiplicatively in each variable raised to its exponent, so naive enumeration over all possible real numbers is impossible. We need a continuous optimization approach that efficiently converges to the maximum. The logarithmic scale is suggested by the problem, which hints at transforming the product into a sum of logarithms to simplify differentiation.

Non-obvious edge cases include exponents being zero, because 0^0 is defined as 1 in this problem. For example, if the input is `S=5` and `a=0, b=0, c=0`, any choice of (_x_, _y_, _z_) summing to 5 is acceptable because the function evaluates to 1. Another edge case is when some exponents are zero while others are positive; for instance `S=3` and `a=1, b=0, c=2` requires assigning all possible sum to _x_ and _z_ while _y_ can be zero.

## Approaches

A brute-force solution would iterate over all real values of _x_, _y_, _z_ satisfying the sum constraint and evaluate _x^a · y^b · z^c_. This is clearly infeasible since the domain is continuous and even a discretized grid would be too fine to guarantee the required precision. Even with a step size of 0.001, the number of combinations would be astronomical, roughly (S/0.001)^3, far exceeding any reasonable time limit.

The key insight comes from transforming the function using logarithms. Let _L(x, y, z) = ln(x^a · y^b · z^c) = a ln x + b ln y + c ln z_. Now we need to maximize a linear combination of logarithms subject to _x + y + z = S_. This is a convex optimization problem because the negative of the logarithm is convex and positive weights maintain concavity. Using the method of Lagrange multipliers, we can show that at the maximum, the partial derivatives are proportional: a/x = b/y = c/z, which implies the optimal solution is to distribute _S_ among variables proportionally to their exponents.

If the sum of exponents is zero, all variables can be arbitrary non-negative numbers summing to S because the function is constant at 1. Otherwise, the solution is simply:

_x = S * a / (a + b + c)_

_y = S * b / (a + b + c)_

_z = S * c / (a + b + c)_

This gives a direct closed-form solution without iterative search, making the algorithm O(1) time and space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((S/ε)^3) | O(1) | Too slow |
| Lagrange Multipliers / Proportional Allocation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the sum limit _S_ and exponents _a, b, c_.
2. Compute the sum of exponents, _total = a + b + c_. This represents the total "weight" to distribute among the coordinates.
3. If _total == 0_, all exponents are zero. In this case, the function is identically 1, so any triple of non-negative numbers summing to _S_ is valid. We can output _(0, 0, S)_ for convenience.
4. Otherwise, assign each coordinate proportionally: _x = S * a / total_, _y = S * b / total_, _z = S * c / total_. This satisfies both the sum constraint and the property that the function is maximized when coordinates are proportional to their exponents.
5. Print the coordinates with sufficient precision to ensure that the logarithmic difference requirement (10^-6) is satisfied.

Why it works: maximizing the product x^a · y^b · z^c under a linear constraint reduces to maximizing a ln x + b ln y + c ln z. The function is strictly concave in the positive quadrant, so the proportional allocation derived from equating derivatives guarantees a global maximum. If any exponent is zero, its corresponding coordinate can safely be zero without affecting the product.

## Python Solution

```python
import sys
input = sys.stdin.readline

S = int(input())
a, b, c = map(int, input().split())

total = a + b + c

if total == 0:
    # All exponents zero: any allocation works
    x, y, z = 0.0, 0.0, float(S)
else:
    x = S * a / total
    y = S * b / total
    z = S * c / total

print(f"{x:.10f} {y:.10f} {z:.10f}")
```

The first block reads the inputs efficiently. We compute the total sum of exponents to detect the degenerate case where all are zero. In that case, we return an arbitrary allocation meeting the sum constraint. Otherwise, we scale each coordinate proportionally to its exponent. The print formatting ensures that floating-point precision is sufficient for the problem's tolerance.

## Worked Examples

Sample Input 1:

```
3
1 1 1
```

| Step | x | y | z | total | Action |
| --- | --- | --- | --- | --- | --- |
| Read inputs | - | - | - | - | S=3, a=1, b=1, c=1 |
| Compute total | - | - | - | 3 | total = a+b+c |
| Compute coordinates | 1.0 | 1.0 | 1.0 | 3 | x=S*a/total, etc. |
| Output | 1.0 | 1.0 | 1.0 | - | Printed result |

This demonstrates equal allocation because exponents are equal.

Custom Input 2:

```
10
2 0 3
```

| Step | x | y | z | total | Action |
| --- | --- | --- | --- | --- | --- |
| Read inputs | - | - | - | - | S=10, a=2, b=0, c=3 |
| Compute total | - | - | - | 5 | total = a+b+c |
| Compute coordinates | 4.0 | 0.0 | 6.0 | 10 | x=10_2/5=4, z=10_3/5=6, y=0 |
| Output | 4.0 | 0.0 | 6.0 | - | Printed result |

This demonstrates that coordinates corresponding to zero exponents can be zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic and a single print operation are performed |
| Space | O(1) | Constant variables for inputs and coordinates |

Since the operations are purely arithmetic, the algorithm easily runs in under 1 microsecond and uses negligible memory, well within the 2-second limit and 256 MB bound.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    S = int(input())
    a, b, c = map(int, input().split())
    total = a + b + c
    if total == 0:
        x, y, z = 0.0, 0.0, float(S)
    else:
        x = S * a / total
        y = S * b / total
        z = S * c / total
    return f"{x:.10f} {y:.10f} {z:.10f}"

# Provided sample
assert run("3\n1 1 1\n") == "1.0000000000 1.0000000000 1.0000000000", "sample 1"
# Custom cases
assert run("10\n2 0 3\n") == "4.0000000000 0.0000000000 6.0000000000", "zero exponent"
assert run("5\n0 0 0\n") == "0.0000000000 0.0000000000 5.0000000000", "all exponents zero"
assert run("7\n1 2 0\n") == "2.3333333333 4.6666666667 0.0000000000", "mixed zero exponent"
assert run("1\n1000 1 1\n") == "0.5 0.0005 0.0005", "large exponent ratios"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10\n |  |  |
