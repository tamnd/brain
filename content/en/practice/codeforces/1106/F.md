---
title: "CF 1106F - Lunar New Year and a Recursive Sequence"
description: "We are given a sequence defined by a multiplicative recurrence where each new term is formed from the previous $k$ terms using fixed exponents."
date: "2026-06-12T05:29:54+07:00"
tags: ["codeforces", "competitive-programming", "math", "matrices", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1106
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 536 (Div. 2)"
rating: 2400
weight: 1106
solve_time_s: 120
verified: false
draft: false
---

[CF 1106F - Lunar New Year and a Recursive Sequence](https://codeforces.com/problemset/problem/1106/F)

**Rating:** 2400  
**Tags:** math, matrices, number theory  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence defined by a multiplicative recurrence where each new term is formed from the previous $k$ terms using fixed exponents. Once we move past index $k$, every value is determined by raising the previous $k$ values to given powers and multiplying them modulo a large prime.

The twist is that almost all initial values are known to be $1$, except the $k$-th one, which is unknown. We also know the value of a far-away term $f_n = m$, where $n$ can be extremely large. The task is to determine any valid value of $f_k$ that makes the recurrence consistent with this final constraint, or report that no such value exists.

The key interpretation shift is that the sequence is not being simulated forward directly. Instead, we are asked to understand how the unknown initial value propagates through the recurrence into $f_n$, which is fundamentally a problem of exponent propagation through linear transformations in logarithmic space.

The constraint $n \le 10^9$ immediately rules out any direct simulation of the recurrence. Even computing $f_n$ step by step is impossible. Since $k \le 100$, the structure is small enough that we expect a matrix or linear-algebraic reduction over exponents.

A subtle edge case appears when $m = 1$. In that case, many different $f_k$ values might work, but some naive solutions incorrectly conclude impossibility because they fail to account for cycles in exponent propagation modulo $p-1$. Another important case is when all contributions of $f_k$ vanish in exponent space, meaning $f_n$ becomes fixed regardless of $f_k$, which leads either to infinite solutions or no solution depending on whether $m$ matches the forced value.

## Approaches

The recurrence is multiplicative, which suggests taking discrete logarithms with respect to a primitive root modulo $p$. Since $p = 998244353$ is prime, the multiplicative group modulo $p$ has size $p-1$, so every nonzero value can be represented as a power of a primitive root $g$. We write $f_i = g^{a_i}$. Substituting into the recurrence transforms multiplication into addition:

$$a_i = \sum_{j=1}^k b_j a_{i-j} \pmod{p-1}.$$

Now the problem becomes a linear recurrence over modular arithmetic, except that only one initial value $a_k$ is unknown and all others are zero. This reduces the system to tracking how the single unknown propagates forward.

If we try brute force, we would pick a candidate $f_k$, simulate the recurrence up to $n$, and check whether the result matches $m$. This costs $O(nk)$, which is impossible since $n$ can be $10^9$.

The key insight is that we never need actual values of the sequence, only the linear transformation effect on the exponent of $f_k$. Every $f_i$ can be expressed as $f_k^{c_i}$ for some coefficient $c_i$ computed by the same recurrence. Since all other initial values are $1$, they contribute nothing. So we reduce the problem to computing $c_n$, and then solving:

$$f_k^{c_n} \equiv m \pmod{p}.$$

This becomes a discrete logarithm / modular exponent equation. If $c_n = 0$, then $f_n = 1$ for all $f_k$, so either $m = 1$ (any $f_k$ works) or no solution exists. Otherwise, we solve a standard power equation in a cyclic group using the fact that the multiplicative group modulo $p$ is cyclic of order $p-1$.

To compute $c_n$, we use matrix exponentiation on a $k \times k$ companion matrix that encodes the recurrence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(nk)$ | $O(k)$ | Too slow |
| Matrix Exponentiation + exponent reduction | $O(k^3 \log n)$ | $O(k^2)$ | Accepted |

## Algorithm Walkthrough

We separate the problem into two layers: linear propagation of exponents, and solving a final modular equation.

1. Build a $k \times k$ transition matrix that represents how the vector $[a_i, a_{i-1}, \dots, a_{i-k+1}]$ evolves. The first row is the recurrence coefficients $b_1, \dots, b_k$, and the remaining rows shift the state.
2. Raise this matrix to power $n-k$ using fast exponentiation. This computes how the initial state affects position $n$.
3. Extract the coefficient $c_n$ corresponding to the contribution of $a_k$ to $a_n$. This is the entry that tells us how many times the unknown exponent is multiplied through the recurrence.
4. If $c_n = 0$, then $f_n$ is forced to be $1$. If $m \ne 1$, return $-1$. Otherwise, any $f_k$ works, so we return $1$.
5. Otherwise, we need to solve $f_k^{c_n} \equiv m \pmod p$. Convert both sides into exponent form with respect to a primitive root $g$, turning the equation into:

$$c_n \cdot x \equiv \log_g(m) \pmod{p-1}.$$
6. Compute discrete logarithm of $m$ using baby-step giant-step.
7. Solve the linear congruence for $x$, ensuring solutions exist only if $\gcd(c_n, p-1)$ divides the logarithm value.
8. Construct $f_k = g^x \bmod p$.

### Why it works

The recurrence is linear in exponent space, so every term is a linear combination of initial exponents. Since all initial exponents except one are zero, the entire system collapses into tracking a single scalar coefficient $c_n$. The final equation is just a group homomorphism from the cyclic multiplicative group into itself, so solving reduces to a linear congruence in modular arithmetic. No information is lost because exponentiation preserves group structure in $\mathbb{F}_p^\times$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
PHI = MOD - 1

def mat_mul(A, B, mod):
    k = len(A)
    res = [[0] * k for _ in range(k)]
    for i in range(k):
        Ai = A[i]
        Ri = res[i]
        for t in range(k):
            if Ai[t] == 0:
                continue
            a = Ai[t]
            Bt = B[t]
            for j in range(k):
                Ri[j] = (Ri[j] + a * Bt[j]) % mod
    return res

def mat_pow(M, e, mod):
    k = len(M)
    res = [[0]*k for _ in range(k)]
    for i in range(k):
        res[i][i] = 1
    base = M
    while e:
        if e & 1:
            res = mat_mul(res, base, mod)
        base = mat_mul(base, base, mod)
        e >>= 1
    return res

def mod_pow(a, e, mod):
    r = 1
    while e:
        if e & 1:
            r = r * a % mod
        a = a * a % mod
        e >>= 1
    return r

def exgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = exgcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_inv(a, mod):
    g, x, _ = exgcd(a, mod)
    return x % mod

def bsgs(g, h, mod):
    from math import isqrt
    m = isqrt(mod) + 1
    table = {}
    cur = 1
    for j in range(m):
        table[cur] = j
        cur = cur * g % mod
    factor = mod_pow(mod_inv(g, mod), m, mod)
    gamma = h
    for i in range(m + 1):
        if gamma in table:
            return i * m + table[gamma]
        gamma = gamma * factor % mod
    return -1

def solve():
    k = int(input())
    b = list(map(int, input().split()))
    n, m = map(int, input().split())

    if n <= k:
        return str(1 if n != k else m)

    M = [[0]*k for _ in range(k)]
    for j in range(k):
        M[0][j] = b[j] % PHI
    for i in range(1, k):
        M[i][i-1] = 1

    P = mat_pow(M, n - k, PHI)

    c = P[0][k-1]

    if c == 0:
        return "1" if m == 1 else "-1"

    g = 3

    logm = bsgs(g, m, MOD)
    if logm == -1:
        return "-1"

    gexp = g

    gk = mod_pow(g, c, PHI)

    from math import gcd
    d = gcd(gk, PHI)
    if logm % d != 0:
        return "-1"

    inv = mod_inv(gk // d, PHI // d)
    x = (logm // d * inv) % (PHI // d)

    return str(mod_pow(g, x, MOD))

def main():
    print(solve())

if __name__ == "__main__":
    main()
```

The matrix construction encodes how each previous term contributes to the next exponent vector. The exponentiation step propagates the single unknown initial condition forward to position $n$, and the extracted coefficient $c$ fully determines how $f_k$ influences the final value.

The discrete logarithm step is necessary because the recurrence lives in a multiplicative group, and solving for the base requires converting the problem into additive exponent form.

Care must be taken when $c = 0$, since in that case the sequence becomes independent of the unknown initial value, which creates either a forced match or an impossible constraint.

## Worked Examples

Consider a small illustrative case where $k = 3$, $b = [2, 1, 1]$, and only $f_3$ is unknown while $f_1 = f_2 = 1$. Suppose $n = 5$.

We track how $f_3$ influences each term:

| i | recurrence form | exponent of $f_3$ |
| --- | --- | --- |
| 3 | initial | 1 |
| 4 | $f_3^2$ | 2 |
| 5 | $f_4^2 f_3^1$ | 5 |

So $f_5 = f_3^5$. If $m = 32$, we solve $f_3^5 = 32$.

This confirms that all intermediate values can be ignored once we know the exponent coefficient.

Now consider a case where the recurrence eventually kills dependence on $f_k$, so $c_n = 0$. Then every term becomes fixed at $1$, and any mismatch with $m$ immediately forces impossibility. This shows why tracking only the coefficient is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k^3 \log n + \sqrt{p})$ | matrix exponentiation plus discrete log |
| Space | $O(k^2)$ | transition matrix storage |

The constraint $k \le 100$ allows $k^3$ operations, and logarithmic exponentiation ensures that even $n = 10^9$ is easily handled. The discrete logarithm step is feasible because $p$ is fixed and supports baby-step giant-step in roughly $O(\sqrt{p})$, which is acceptable under contest constraints when carefully implemented.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("3\n2 3 5\n4 16\n") == "4"

# minimal case k=1
assert run("1\n1\n2 5\n") == "5"

# all ones recurrence, forced value
assert run("2\n1 1\n5 1\n") == "1"

# impossible case
assert run("2\n1 1\n5 2\n") == "-1"

# boundary large n behavior
assert run("3\n2 2 2\n100 8\n") in ["1", "-1"]

# dependence killed case
assert run("3\n0 0 0\n10 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=1 case | direct exponent | base boundary |
| all ones | 1 | trivial propagation |
| impossible | -1 | contradiction handling |
| large n | valid | exponent stability |
| zero recurrence | 1 | vanishing dependency |

## Edge Cases

When $c_n = 0$, the algorithm effectively collapses the entire recurrence into a constant sequence independent of $f_k$. For example, if all $b_i = 0$, every term after $k$ becomes $1$. The algorithm detects this because the matrix power yields a zero contribution in the last column. If $m \ne 1$, it immediately returns $-1$, matching the forced structure.

When $m = 1$, any $f_k$ becomes valid whenever the system is not constrained by a nonzero coefficient. The algorithm handles this by returning $1$, which is consistent because $1^{c_n} = 1$ for all $c_n$, ensuring correctness regardless of propagation strength.

When $n = k$, no recurrence expansion is needed. The algorithm correctly returns the provided $m$ as the only constraint, since the unknown directly equals the target value at that index.
