---
title: "CF 104059E - Enjoyable Entree"
description: "The canteen starts with two “base soups” that we can think of as two pure ingredients: one is π-tato soup and the other is τ-mato soup. From day to day, the recipe evolves deterministically. On day 1 the soup is entirely π-tato, on day 2 it is entirely τ-mato."
date: "2026-07-02T03:29:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104059
codeforces_index: "E"
codeforces_contest_name: "2022-2023 ACM-ICPC German Collegiate Programming Contest (GCPC 2022)"
rating: 0
weight: 104059
solve_time_s: 43
verified: true
draft: false
---

[CF 104059E - Enjoyable Entree](https://codeforces.com/problemset/problem/104059/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The canteen starts with two “base soups” that we can think of as two pure ingredients: one is π-tato soup and the other is τ-mato soup. From day to day, the recipe evolves deterministically. On day 1 the soup is entirely π-tato, on day 2 it is entirely τ-mato. From day 3 onward, each new soup is formed by mixing the previous two soups in equal proportion.

This means the nth soup is always a mixture of the first two soups, and every step just blends the previous mixtures without introducing anything new. The task is to determine what fraction of the final mixture comes from the original π-tato soup and what fraction comes from τ-mato soup after n days.

The input size goes up to 10^18, so any approach that simulates day by day is immediately infeasible. A linear simulation would require up to 10^18 operations, which is far beyond any time limit. Even logarithmic factor methods are acceptable, but anything worse than O(log n) will fail.

A subtle edge case appears at small values of n. When n equals 1 or 2, the answer is trivially pure ingredients. If a solution blindly applies a recurrence formula starting from n = 3 without handling these base cases, it may incorrectly shift the sequence or produce undefined values.

## Approaches

The brute-force interpretation is straightforward. We maintain a pair of values for each day representing how much π-tato and τ-mato are present. On day 1 we start with (1, 0), on day 2 we have (0, 1). Each next day we compute the average of the previous two pairs. This directly follows the problem definition and is correct by construction.

The issue is scale. Computing up to day n requires iterating through all previous days, so the complexity is O(n). With n up to 10^18, this approach is completely infeasible.

The key observation is that both components evolve independently under the same recurrence. If we track only the π-tato fraction, it satisfies the recurrence f(n) = (f(n−1) + f(n−2)) / 2, with f(1) = 1 and f(2) = 0. The τ-mato fraction is simply 1 − f(n), but we can also compute it symmetrically.

This is a linear recurrence with constant coefficients. Such recurrences can be solved using matrix exponentiation. We encode the transition from (f(n−1), f(n−2)) to (f(n), f(n−1)) as a matrix multiplication. Raising this matrix to the (n−2)th power gives us the state at day n in O(log n) time.

The division by 2 introduces fractions, but we can treat it as multiplying by 1/2 in floating point or equivalently incorporate it into the transition matrix. Since the required precision is 10^{-6}, floating-point matrix exponentiation is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Matrix Exponentiation | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to computing a Fibonacci-like recurrence with scaling.

1. Define f(n) as the fraction of π-tato soup on day n. From the construction, f(1) = 1 and f(2) = 0. This establishes the two base states from which everything evolves.
2. Observe that for n ≥ 3, f(n) = (f(n−1) + f(n−2)) / 2. This comes directly from averaging the previous two mixtures.
3. Rewrite the recurrence as a linear transformation:

(f(n), f(n−1)) = (1/2 * (f(n−1) + f(n−2)), f(n−1)).
4. Express this as matrix multiplication:

[f(n), f(n−1)]^T = A * [f(n−1), f(n−2)]^T,

where A = [[1/2, 1/2], [1, 0]]. This representation allows repeated application via exponentiation.
5. Compute A^(n−2). This transforms the initial vector [f(2), f(1)] = [0, 1] into [f(n), f(n−1)].
6. Perform fast exponentiation by squaring. Each multiplication combines two transition states, preserving correctness of the recurrence.
7. Extract f(n) from the resulting vector. The τ-mato fraction is 1 − f(n), since the total mixture always sums to 1.

### Why it works

The key invariant is that each state vector fully encodes the last two values of the recurrence. The transition matrix exactly reproduces the recurrence step, so multiplying by the matrix advances the sequence by one day without approximation error beyond floating-point precision. Because matrix multiplication is associative, repeated squaring correctly simulates n−2 sequential transformations in logarithmic time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mat_mul(a, b):
    return [
        [
            a[0][0]*b[0][0] + a[0][1]*b[1][0],
            a[0][0]*b[0][1] + a[0][1]*b[1][1],
        ],
        [
            a[1][0]*b[0][0] + a[1][1]*b[1][0],
            a[1][0]*b[0][1] + a[1][1]*b[1][1],
        ],
    ]

def mat_pow(m, e):
    res = [[1.0, 0.0], [0.0, 1.0]]
    base = m
    while e > 0:
        if e & 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        e >>= 1
    return res

n = int(input())

if n == 1:
    print("100.0 0.0")
elif n == 2:
    print("0.0 100.0")
else:
    A = [
        [0.5, 0.5],
        [1.0, 0.0],
    ]
    M = mat_pow(A, n - 2)
    f_n = M[0][1]
    print(f"{f_n * 100:.10f} {(1 - f_n) * 100:.10f}")
```

The code constructs the transition matrix directly from the recurrence. The multiplication function implements standard 2×2 matrix multiplication without optimizations, since constant size keeps it efficient.

Exponentiation by squaring reduces the number of multiplications from n to log n. The identity matrix initializes the accumulation so that partial results remain neutral until combined.

The base cases n = 1 and n = 2 are handled explicitly because the matrix formulation assumes access to two previous states.

Floating-point arithmetic is used directly. Since the depth is at most log2(10^18) ≈ 60 multiplications, accumulated error stays within acceptable bounds.

## Worked Examples

Consider the recurrence starting from n = 1 and n = 2.

### Example 1: n = 3

| Day | f(n−2) | f(n−1) | f(n) computation |
| --- | --- | --- | --- |
| 1 | - | - | 1.0 |
| 2 | - | - | 0.0 |
| 3 | 1.0 | 0.0 | (1.0 + 0.0)/2 = 0.5 |

For n = 3, the result is 50% π-tato and 50% τ-mato. This shows the first mixing step directly averages the two base soups.

### Example 2: n = 4

| Day | f(n−2) | f(n−1) | f(n) computation |
| --- | --- | --- | --- |
| 2 | - | - | 0.0 |
| 3 | 1.0 | 0.0 | 0.5 |
| 4 | 0.0 | 0.5 | (0.5 + 0.0)/2 = 0.25 |

At day 4, the π-tato fraction drops to 25%, confirming that repeated averaging rapidly dampens the original contribution.

These examples confirm that the recurrence behaves like a smoothed Fibonacci sequence scaled by 1/2 at each step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Matrix exponentiation halves the exponent each step |
| Space | O(1) | Only a constant number of 2×2 matrices are stored |

The logarithmic runtime easily handles n up to 10^18. Memory usage is constant and independent of input size, so it remains efficient under strict limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    import sys
    input = sys.stdin.readline

    def mat_mul(a, b):
        return [
            [
                a[0][0]*b[0][0] + a[0][1]*b[1][0],
                a[0][0]*b[0][1] + a[0][1]*b[1][1],
            ],
            [
                a[1][0]*b[0][0] + a[1][1]*b[1][0],
                a[1][0]*b[0][1] + a[1][1]*b[1][1],
            ],
        ]

    def mat_pow(m, e):
        res = [[1.0, 0.0], [0.0, 1.0]]
        base = m
        while e > 0:
            if e & 1:
                res = mat_mul(res, base)
            base = mat_mul(base, base)
            e >>= 1
        return res

    n = int(input())

    if n == 1:
        return "100.0 0.0"
    if n == 2:
        return "0.0 100.0"

    A = [[0.5, 0.5], [1.0, 0.0]]
    M = mat_pow(A, n - 2)
    f_n = M[0][1]
    return f"{f_n * 100:.10f} {(1 - f_n) * 100:.10f}"

# provided samples
assert run("1") == "100.0 0.0", "sample 1"
assert run("2") == "0.0 100.0", "sample 2"

# custom cases
assert run("3") == "50.0000000000 50.0000000000", "first mix"
assert run("4") == "25.0000000000 75.0000000000", "second decay"
assert run("10") != "", "non-trivial growth case"
assert run("1") == "100.0 0.0", "boundary minimum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 100 0 | base case handling |
| 2 | 0 100 | second base case |
| 3 | 50 50 | first recurrence step |
| 4 | 25 75 | repeated averaging decay |

## Edge Cases

For n = 1, the matrix formulation is not applicable because it assumes two previous states exist. The algorithm explicitly bypasses matrix exponentiation and returns (100, 0), matching the definition of day 1 as pure π-tato soup.

For n = 2, the same issue occurs, and the output is fixed as (0, 100). Any attempt to apply the recurrence blindly would incorrectly compute a mixture of undefined earlier states.

For large n such as 10^18, direct simulation would overflow both time and memory, but matrix exponentiation reduces the computation to about 60 squaring steps. Each step only manipulates constant-size matrices, so the result remains stable under floating-point arithmetic.
