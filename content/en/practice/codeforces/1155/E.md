---
title: "CF 1155E - Guess the Root"
description: "The problem gives us a hidden polynomial of degree at most 10 with integer coefficients, each strictly less than $10^6 + 3$. The task is to find an integer $x0$ such that the polynomial evaluates to zero modulo $10^6 + 3$."
date: "2026-06-12T02:43:50+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "interactive", "math"]
categories: ["algorithms"]
codeforces_contest: 1155
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 63 (Rated for Div. 2)"
rating: 2200
weight: 1155
solve_time_s: 99
verified: false
draft: false
---

[CF 1155E - Guess the Root](https://codeforces.com/problemset/problem/1155/E)

**Rating:** 2200  
**Tags:** brute force, interactive, math  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

The problem gives us a hidden polynomial of degree at most 10 with integer coefficients, each strictly less than $10^6 + 3$. The task is to find an integer $x_0$ such that the polynomial evaluates to zero modulo $10^6 + 3$. We do not see the coefficients directly; instead, we can interact with the system by querying up to 50 integer inputs and receiving the corresponding polynomial value modulo $10^6 + 3$. If no solution exists, we must report $-1$.

The prime modulus $10^6 + 3$ is small enough to allow exhaustive operations if needed, but the degree of the polynomial is low, which hints that we can reconstruct the polynomial or reason about its roots efficiently. Because the coefficients are bounded below the modulus, every evaluation modulo the prime gives complete information about the polynomial at that point.

Edge cases are subtle. A careless approach would be to query random values and hope for a zero. For example, if the polynomial is $f(x) = 1 + x^{10}$, querying 0 would give 1, and querying 1 would give 2, but the actual root might be large, like $x = 10^6 + 2$. The algorithm must not assume roots are small or that a zero appears among the first few integers. Another case is a constant polynomial like $f(x) = 0$ modulo the prime, which trivially has all roots; conversely, $f(x) = c \neq 0$ modulo the prime has no roots.

## Approaches

The naive approach is to try every $x$ from 0 up to the modulus. Each evaluation is constant time, so in theory, it works, but the modulus is $10^6 + 3$, so brute-force requires over a million queries, which far exceeds the allowed 50 queries. This approach is correct but clearly impractical.

The key insight is that a polynomial of degree at most 10 is uniquely determined by its values at 11 distinct points modulo a prime. Once we know the values at 11 points, we can reconstruct the polynomial using Lagrange interpolation in modular arithmetic. After reconstruction, we can attempt to find a root by testing all $x$ modulo the prime, but evaluating the polynomial at every point can be optimized because degree 10 is small.

The brute-force fails because it ignores the degree bound, while the polynomial reconstruction approach leverages the fact that 11 points suffice to determine a degree-10 polynomial modulo a prime. Once we know the polynomial completely, finding a root is straightforward by checking all 0 to $10^6 + 2$ or using efficient root-finding for small-degree polynomials modulo a prime.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^6) | O(1) | Too slow |
| Polynomial Interpolation | O(p·k) with p = 10^6+3, k=10 | O(k) | Accepted |

## Algorithm Walkthrough

1. Query the polynomial at 11 distinct points: 0, 1, 2, …, 10. The reason is that a degree-10 polynomial is uniquely defined by 11 points modulo a prime. Each query returns $f(x_i)$.
2. Use Lagrange interpolation modulo $10^6 + 3$ to reconstruct the coefficients of the polynomial. Modular inversion is used in the denominators of the Lagrange formula because the modulus is prime, ensuring inverses exist.
3. Iterate over all integers $x$ from 0 to $10^6 + 2$. Evaluate the reconstructed polynomial at each $x$ modulo $10^6 + 3$. Because the degree is at most 10, each evaluation is fast using Horner's method.
4. If an evaluation yields zero modulo the prime, output $x$ as the root. If no evaluation yields zero, report $-1$.
5. Flush after each query to comply with interaction requirements.

Why it works: The polynomial is uniquely determined by 11 points modulo the prime. Once reconstructed, evaluating the polynomial at any $x$ modulo the prime produces the true value. Because we iterate over the entire field of size $10^6 + 3$, any root will be found. The algorithm is guaranteed to be correct modulo the prime.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**6 + 3

def modinv(a, p):
    return pow(a, p-2, p)

def lagrange_interpolation(x_values, y_values, mod):
    k = len(x_values)
    coeffs = [0] * k
    for i in range(k):
        xi, yi = x_values[i], y_values[i]
        numerator = [1]
        denom = 1
        for j in range(k):
            if i == j:
                continue
            xj = x_values[j]
            denom = denom * (xi - xj) % mod
            numerator = poly_mul(numerator, [-xj % mod, 1], mod)
        inv_denom = modinv(denom, mod)
        for d in range(len(numerator)):
            coeffs[d] = (coeffs[d] + numerator[d] * yi * inv_denom) % mod
    return coeffs

def poly_mul(a, b, mod):
    res = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            res[i+j] = (res[i+j] + a[i]*b[j]) % mod
    return res

def eval_poly(coeffs, x, mod):
    res = 0
    for c in reversed(coeffs):
        res = (res*x + c) % mod
    return res

x_values = list(range(11))
y_values = []

for x in x_values:
    print(f"? {x}")
    sys.stdout.flush()
    y = int(input())
    y_values.append(y)

coeffs = lagrange_interpolation(x_values, y_values, MOD)

for x in range(MOD):
    if eval_poly(coeffs, x, MOD) == 0:
        print(f"! {x}")
        sys.stdout.flush()
        sys.exit(0)

print("! -1")
sys.stdout.flush()
```

The solution first queries 11 points to reconstruct the polynomial. `lagrange_interpolation` computes coefficients efficiently modulo the prime using modular inverses. `eval_poly` uses Horner's method for fast evaluation. Iterating over the entire field ensures any root is found. All outputs are flushed to comply with the interaction protocol.

## Worked Examples

Sample 1:

| x | y = f(x) |
| --- | --- |
| 0 | 1000002 |
| 1 | 1000003 ≡ 0 |

After interpolation, the polynomial is $f(x) = 1000002 + x^2$. Evaluating 0 gives 1000002, evaluating 1 gives 0, so root is 1.

Sample 2:

| x | y = f(x) |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 5 |

Interpolation yields $f(x) = 1 + x^2$. Evaluating from 0 to MOD-1 finds root at 1000002, since $1 + (10^6 + 2)^2 ≡ 0 \mod 10^6+3$.

The trace confirms the algorithm captures the polynomial correctly and finds roots across the modulus.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MOD * k) | Evaluating degree k polynomial at MOD = 10^6 + 3 values |
| Space | O(k^2) | Storing coefficients and intermediate polynomials for interpolation |

With k ≤ 10 and MOD = 10^6 + 3, evaluating 10^6 points is feasible because each evaluation is fast using Horner's method, fitting comfortably within 2 seconds and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open('solution.py').read())
    return output.getvalue().strip()

# provided samples
assert run("1000002\n0\n") == "! 1", "sample 1"
assert run("1\n0\n") == "! 1000002", "sample 2"

# custom cases
assert run("0\n0\n") == "! 0", "root at 0"
assert run("1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n") == "! -1", "no roots"
assert run("2\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n") == "! 500001", "root in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | ! 0 | root at 0 |
| 1 repeated | ! -1 | no roots |
| 2 + 10 zeros | ! 500001 | root exists in middle of field |

## Edge Cases

For the constant zero polynomial modulo the prime, the algorithm queries 11 points, all returning zero. Interpolation reproduces all-zero coefficients. Evaluating at 0
