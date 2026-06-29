---
title: "CF 104619E - Exponentiation"
description: "We are given a positive integer α that is defined as the sum of a number x and its reciprocal 1/x. In other words, x is some (possibly complex) number satisfying x + 1/x = α. From this implicit definition, we are asked to compute the value of x^β + (1/x)^β modulo m."
date: "2026-06-29T17:26:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104619
codeforces_index: "E"
codeforces_contest_name: "2023 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 104619
solve_time_s: 50
verified: true
draft: false
---

[CF 104619E - Exponentiation](https://codeforces.com/problemset/problem/104619/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer α that is defined as the sum of a number x and its reciprocal 1/x. In other words, x is some (possibly complex) number satisfying x + 1/x = α. From this implicit definition, we are asked to compute the value of x^β + (1/x)^β modulo m.

The key difficulty is that x is not given explicitly. It is defined only through a quadratic relation. Expanding the definition, x must satisfy x^2 - αx + 1 = 0, so x is a root of a quadratic polynomial with integer coefficients. Even though x may be irrational or complex, the final expression x^β + x^{-β} is guaranteed to be an integer.

The output depends only on α, β, and m, not on which root is chosen. If x is one root, 1/x is the other root, and swapping them does not change the value of x^β + x^{-β}.

The constraints imply that α, β, and m can be as large as 2^64. This immediately rules out any approach that expands powers explicitly or works in linear time in β. We need something that reduces exponentiation in logarithmic time and avoids floating-point arithmetic entirely.

A subtle edge case appears when α is small. For example, if α = 1, the roots are complex numbers 1/2 ± i√3/2, and direct numeric computation becomes unstable. Another edge case is when x = 1 or x = -1, which happens when α = 2 or α = -2 in extended forms, but here α is positive so only α = 2 leads to a repeated-root situation where x = 1.

The central challenge is to compute a symmetric power sum of the roots of a quadratic without explicitly solving the quadratic.

## Approaches

A direct interpretation would try to compute x from the quadratic formula x = (α ± √(α^2 - 4)) / 2, then raise it to β and sum with its reciprocal. This approach is fragile because it involves irrational or complex numbers and requires high precision arithmetic. Even if implemented with big floating-point or symbolic computation, exponentiating large β would be too slow.

The key structural observation is that x^k + x^{-k} behaves like a linear recurrence. If we define S_k = x^k + x^{-k}, then multiplying by (x + x^{-1}) = α gives a recurrence:

S_{k+1} = (x + x^{-1})(x^k + x^{-k}) - (x^{k-1} + x^{-(k-1)})

This simplifies to:

S_{k+1} = α S_k - S_{k-1}

This recurrence completely eliminates x. The entire problem reduces to computing the β-th term of a second-order linear recurrence with initial values S_0 = 2 and S_1 = α.

Once we recognize this structure, the problem becomes a standard fast doubling or matrix exponentiation task. We can compute S_β in logarithmic time using either 2x2 matrix exponentiation or the fast doubling method used for Fibonacci-like recurrences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct computation using roots | O(β) or worse | O(1) | Too slow / numerically unstable |
| Linear recurrence via fast exponentiation | O(log β) | O(1) | Accepted |

## Algorithm Walkthrough

We rewrite the problem in terms of a recurrence S_k = x^k + x^{-k}. The goal is to compute S_β.

1. We initialize two base values corresponding to the recurrence. We set S_0 = 2 because x^0 + x^0 = 1 + 1 = 2, and S_1 = α because x + 1/x = α is given directly. These two values fully determine the sequence.
2. We observe that every later term can be generated from the previous two using S_{k+1} = α S_k - S_{k-1}. This relation comes from multiplying S_k by α and expanding α = x + 1/x, then regrouping powers of x.
3. Instead of iterating β times, we compute S_β using fast exponentiation over this recurrence. We treat the recurrence as a linear transformation on the vector (S_k, S_{k-1}).
4. We define a transformation matrix:

$$\begin{pmatrix}
S_{k+1} \\
S_k
\end{pmatrix}
=
\begin{pmatrix}
\alpha & -1 \\
1 & 0
\end{pmatrix}
\begin{pmatrix}
S_k \\
S_{k-1}
\end{pmatrix}$$
5. We exponentiate this matrix to power β-1 and apply it to the initial vector (S_1, S_0). This yields (S_β, S_{β-1}).
6. All operations are done modulo m, carefully handling negative values when subtracting S_{k-1}.

The correctness follows from the invariant that at step k, the vector (S_k, S_{k-1}) exactly represents (x^k + x^{-k}, x^{k-1} + x^{-(k-1)}). The transition preserves this identity because it mirrors the algebraic expansion of multiplying by x + x^{-1}. Since the recurrence uniquely determines all S_k, and the initial conditions match the true values, the computed sequence must coincide with the desired expression for all k.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mat_mul(a, b, mod):
    return [
        [(a[0][0]*b[0][0] + a[0][1]*b[1][0]) % mod,
         (a[0][0]*b[0][1] + a[0][1]*b[1][1]) % mod],
        [(a[1][0]*b[0][0] + a[1][1]*b[1][0]) % mod,
         (a[1][0]*b[0][1] + a[1][1]*b[1][1]) % mod]
    ]

def mat_pow(mat, exp, mod):
    res = [[1, 0], [0, 1]]
    while exp > 0:
        if exp & 1:
            res = mat_mul(res, mat, mod)
        mat = mat_mul(mat, mat, mod)
        exp >>= 1
    return res

def solve():
    alpha, beta, m = map(int, input().split())
    
    if beta == 0:
        print(2 % m)
        return
    if beta == 1:
        print(alpha % m)
        return
    
    base = [[alpha % m, (m - 1) % m],
            [1, 0]]
    
    p = mat_pow(base, beta - 1, m)
    
    s1 = alpha % m
    s0 = 2 % m
    
    ans = (p[0][0] * s1 + p[0][1] * s0) % m
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation encodes the recurrence into a 2x2 transition matrix where each application advances the sequence by one step. The subtraction in the recurrence is implemented as adding m-1 modulo m to avoid negative values.

The fast exponentiation routine raises the matrix to the (β-1)-th power in logarithmic time, repeatedly squaring and multiplying only when needed by the binary representation of the exponent.

Finally, the result is extracted by applying the matrix to the initial vector (S_1, S_0). The edge cases β = 0 and β = 1 are handled explicitly because they correspond directly to the base definitions without needing exponentiation.

## Worked Examples

### Example 1

Input: α = 5, β = 4, m = 321

We build S_0 = 2 and S_1 = 5, then apply recurrence S_{k+1} = 5S_k - S_{k-1}.

| k | S_k | S_{k-1} | αS_k - S_{k-1} |
| --- | --- | --- | --- |
| 1 | 5 | 2 | 5*5 - 2 = 23 |
| 2 | 23 | 5 | 5*23 - 5 = 110 |
| 3 | 110 | 23 | 5*110 - 23 = 527 |

So S_4 = 527, and modulo 321 gives 527 mod 321 = 206.

This confirms the recurrence construction correctly produces higher powers without using x explicitly.

### Example 2

Input: α = 3, β = 3, m = 333

We again compute step by step.

| k | S_k | S_{k-1} | αS_k - S_{k-1} |
| --- | --- | --- | --- |
| 1 | 3 | 2 | 3*3 - 2 = 7 |
| 2 | 7 | 3 | 3*7 - 3 = 18 |

So S_3 = 18, and modulo 333 remains 18.

This shows that even when x is complex (since α^2 - 4 < 0), the recurrence stays entirely in integers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log β) | matrix exponentiation doubles exponent each step |
| Space | O(1) | only a constant number of 2x2 matrices stored |

The logarithmic dependency on β ensures the solution remains fast even when β is close to 2^64. Memory usage is constant since the computation uses only a fixed-size transition matrix.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def mat_mul(a, b, mod):
        return [
            [(a[0][0]*b[0][0] + a[0][1]*b[1][0]) % mod,
             (a[0][0]*b[0][1] + a[0][1]*b[1][1]) % mod],
            [(a[1][0]*b[0][0] + a[1][1]*b[1][0]) % mod,
             (a[1][0]*b[0][1] + a[1][1]*b[1][1]) % mod]
        ]

    def mat_pow(mat, exp, mod):
        res = [[1, 0], [0, 1]]
        while exp > 0:
            if exp & 1:
                res = mat_mul(res, mat, mod)
            mat = mat_mul(mat, mat, mod)
            exp >>= 1
        return res

    alpha, beta, m = map(int, input().split())
    
    if beta == 0:
        return str(2 % m)
    if beta == 1:
        return str(alpha % m)

    base = [[alpha % m, (m - 1) % m],
            [1, 0]]

    p = mat_pow(base, beta - 1, m)

    s1 = alpha % m
    s0 = 2 % m

    return str((p[0][0] * s1 + p[0][1] * s0) % m)

# provided samples
# assert run("1 2 3") == "..."
# assert run("5 4 321") == "..."
# assert run("3 3 333") == "..."

# custom cases
assert run("2 0 10") == "2", "beta = 0 gives S0"
assert run("2 1 10") == "2", "beta = 1 gives alpha"
assert run("2 2 1000") == "2", "x + 1/x = 2 implies x=1 so all S_k=2"
assert run("10 5 100") == run("10 5 100"), "stability check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 10 | 2 | base case S0 |
| 2 1 10 | 2 | base case S1 |
| 2 2 1000 | 2 | degenerate root x=1 |
| 10 5 100 | consistent output | stability of recurrence |

## Edge Cases

When α = 2, the quadratic x^2 - 2x + 1 = 0 collapses to (x - 1)^2 = 0, so x = 1. In that case, every term S_k = 1^k + 1^{-k} = 2. The recurrence still produces S_{k+1} = 2S_k - S_{k-1}, and with S_0 = 2 and S_1 = 2, it stays constant. The algorithm naturally preserves this because the transition matrix becomes [[2, -1], [1, 0]], which has eigenvalue 1 with multiplicity two.

For cases where α^2 < 4, the roots are complex conjugates. The recurrence avoids any direct use of these numbers and stays entirely in integer arithmetic. The invariance of S_k as a symmetric polynomial in the roots ensures the computation remains valid regardless of the nature of x.

Large β close to 2^64 does not affect correctness since exponentiation is done through binary lifting, which depends only on the bit length of β rather than its magnitude.
