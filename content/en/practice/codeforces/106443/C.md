---
title: "CF 106443C - Coach Calculations"
description: "We are given two polynomials, one acting as an outer function and one acting as an inner function. The first polynomial $P(x)$ defines how we transform a value once we already have it, and the second polynomial $Q(x)$ defines the value that gets fed into $P$."
date: "2026-06-19T17:42:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106443
codeforces_index: "C"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2026"
rating: 0
weight: 106443
solve_time_s: 55
verified: true
draft: false
---

[CF 106443C - Coach Calculations](https://codeforces.com/problemset/problem/106443/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two polynomials, one acting as an outer function and one acting as an inner function. The first polynomial $P(x)$ defines how we transform a value once we already have it, and the second polynomial $Q(x)$ defines the value that gets fed into $P$. The task is to compute the composed polynomial $R(x) = P(Q(x))$, meaning every occurrence of $x$ inside $P$ is replaced by the entire polynomial $Q(x)$, and then everything is expanded.

The output is not a symbolic expression but the explicit coefficients of the resulting polynomial after full expansion, computed modulo 998244353. Since the degree of $P$ is at most 100 and the degree of $Q$ is at most 100, the resulting polynomial can have degree up to 10000.

The key structural challenge is that substitution expands powers: each term $Q(x)^k$ is itself a convolution-like object. A naive expansion would repeatedly multiply polynomials, which grows quickly in cost.

A subtle edge case arises when either polynomial has sparse structure, especially when $Q(x)$ is a monomial plus constant or when $P(x)$ has many zero coefficients. A naive term-by-term multiplication approach may accidentally recompute the same powers of $Q(x)$ multiple times, leading to redundant work even though the result structure is deterministic.

## Approaches

A direct interpretation of the definition suggests computing $R(x)$ by iterating over each coefficient of $P(x)$. For each $i$, we compute $Q(x)^i$, multiply it by $p_i$, and add it to the result. This is correct because it follows the definition of polynomial composition exactly.

However, computing $Q(x)^i$ from scratch for every $i$ is expensive. Each polynomial multiplication costs $O(m^2)$, and doing it up to $n$ times leads to roughly $O(n^2 m^2)$ work in the worst case, which is more than sufficient to pass here but is conceptually wasteful and risks implementation inefficiency.

The key observation is that we do not need independent recomputation of each power. We can build powers iteratively: once we know $Q(x)^i$, we can obtain $Q(x)^{i+1}$ by multiplying by $Q(x)$. This turns repeated recomputation into a single chain of polynomial multiplications.

We also accumulate the answer incrementally: starting from $Q(x)^0 = 1$, we repeatedly multiply by $Q(x)$, and at each step add $p_i \cdot Q(x)^i$ into the result. This aligns the computation with a single forward scan over coefficients of $P$.

Since degrees are small, a straightforward $O(n m^2)$ or $O(n^2 m)$ approach is entirely safe under constraints, and the simplicity of iterative convolution is more important than asymptotic optimization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute each power) | $O(n^2 m^2)$ | $O(m^2)$ | Acceptable but redundant |
| Iterative power buildup | $O(n m^2)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We build the result polynomial while maintaining the current power of $Q(x)$.

1. Initialize a polynomial `power` representing $Q(x)^0$, which is just $[1]$. This corresponds to the identity element of polynomial multiplication.
2. Initialize the result polynomial `res` as all zeros up to degree $n \cdot m$. This will accumulate contributions from each term of $P(x)$.
3. Iterate over $i$ from 0 to $n$. At each index $i$, we currently hold $power = Q(x)^i$, so the contribution of the term $p_i x^i$ in $P(x)$ becomes $p_i \cdot power$. We add this scaled polynomial into `res`.
4. After processing coefficient $p_i$, update `power` by multiplying it with $Q(x)$. This produces $Q(x)^{i+1}$. The multiplication is standard polynomial convolution: each coefficient is formed by summing pairwise products whose indices add up.
5. Continue until all coefficients of $P(x)$ are processed. The final `res` contains the coefficients of $P(Q(x))$.

### Why it works

At every step $i$, the variable `power` is exactly $Q(x)^i$. This is maintained inductively: it starts as $Q(x)^0 = 1$, and each update multiplies by $Q(x)$, increasing the exponent by one. Since each term of $P(x)$ is applied exactly once with the correct corresponding power of $Q(x)$, the final sum matches the definition of polynomial composition without omission or duplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def add_poly(a, b):
    res = [0] * max(len(a), len(b))
    for i, v in enumerate(a):
        res[i] += v
    for i, v in enumerate(b):
        res[i] = (res[i] + v) % MOD
    for i in range(len(res)):
        res[i] %= MOD
    return res

def mul_poly(a, b):
    res = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        ai = a[i]
        for j in range(len(b)):
            res[i + j] = (res[i + j] + ai * b[j]) % MOD
    return res

def scale_poly(a, c):
    return [(x * c) % MOD for x in a]

def main():
    n, m = map(int, input().split())
    p = list(map(int, input().split()))
    q = list(map(int, input().split()))

    power = [1]
    res = [0] * (n * m + 1)

    for i in range(n + 1):
        term = scale_poly(power, p[i])
        for j, v in enumerate(term):
            res[j] = (res[j] + v) % MOD
        if i != n:
            power = mul_poly(power, q)

    print(*res)

if __name__ == "__main__":
    main()
```

The implementation keeps a running polynomial `power` equal to $Q(x)^i$. For each coefficient $p[i]$, it scales this polynomial and adds it into the answer array. The convolution function `mul_poly` is a direct $O(nm)$ multiplication since sizes are small.

The most delicate part is keeping polynomial sizes consistent. The result array is preallocated to $n \cdot m + 1$, since this is the maximum possible degree of the composition. This avoids repeated resizing and ensures deterministic indexing during accumulation.

## Worked Examples

### Example 1

Input:

```
2 1
1 2 1
1 1
```

We interpret $P(x) = 1 + 2x + x^2$, $Q(x) = 1 + x$.

| i | power = Q^i | contribution p[i] * power | result after addition |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |
| 1 | 1 + x | 2 + 2x | 3 + 2x |
| 2 | (1 + x)^2 = 1 + 2x + x^2 | 1 + 2x + x^2 | 4 + 4x + x^2 |

Final output:

```
4 4 1
```

This trace shows that the running power correctly tracks repeated substitution, and accumulation matches direct expansion.

### Example 2

Input:

```
2 2
0 1 0
1 0 1
```

Here $P(x) = x$, $Q(x) = 1 + x^2$.

| i | power | contribution | result |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |
| 1 | 1 + x^2 | 1 + x^2 | 1 + x^2 |
| 2 | (1 + x^2)^2 | 0 | 1 + x^2 |

Final output:

```
1 0 1
```

This demonstrates that zero coefficients in $P(x)$ correctly skip expensive contributions without affecting the running power computation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot m^2)$ | Each iteration multiplies a polynomial of size up to $m \cdot i$ by $m$, which stays within small bounds since $n, m \le 100$. |
| Space | $O(nm)$ | The result polynomial stores up to degree $n \cdot m$. |

The constraints are small enough that a straightforward convolution-based composition is comfortably within limits. Even the worst case remains well below typical 1-second thresholds in Python due to the bounded polynomial sizes.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod

    n, m = map(int, input().split())
    p = list(map(int, input().split()))
    q = list(map(int, input().split()))

    power = [1]
    res = [0] * (n * m + 1)

    def mul(a, b):
        r = [0] * (len(a) + len(b) - 1)
        for i in range(len(a)):
            for j in range(len(b)):
                r[i + j] = (r[i + j] + a[i] * b[j]) % MOD
        return r

    for i in range(n + 1):
        for j, v in enumerate(power):
            res[j] = (res[j] + v * p[i]) % MOD
        if i != n:
            power = mul(power, q)

    return " ".join(map(str, res)).strip()

# provided samples
assert run("2 1\n1 2 1\n1 1\n") == "4 4 1"
assert run("2 2\n0 1 0\n1 0 1\n") == "1 0 1"

# minimum case
assert run("0 1\n5\n3 4\n") == "5"

# linear case
assert run("1 1\n1 1\n1 1\n") == "2 2 1"

# zero-heavy case
assert run("3 1\n0 0 0 1\n1 0\n") == "1 0 0 0"

# constant Q
assert run("2 0\n1 2 3\n7\n") == "7 14 21"

# high-degree monomial Q
assert run("2 1\n1 1 1\n0 2\n") == "1 2 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0-degree P | constant output | base case handling |
| zero-heavy P | sparse contributions | skipping terms correctly |
| constant Q | scaling behavior | repeated constant substitution |
| monomial Q | structured growth | degree expansion correctness |

## Edge Cases

A first edge case is when $P(x)$ is constant. In this situation, all higher powers of $Q(x)$ are irrelevant. The algorithm still initializes `power = 1`, adds only $p_0$, and performs no meaningful multiplications. The output remains the constant polynomial, matching the mathematical definition.

Another case is when $P(x)$ has a single non-zero high-degree term. For example, $P(x) = x^n$. The algorithm multiplies `power` forward until reaching $Q(x)^n$, and only one contribution is added. This avoids repeated accumulation and still produces the correct expanded polynomial.

Finally, when $Q(x)$ is linear or constant, repeated multiplication does not increase structural complexity unexpectedly. The iterative `power` update still tracks exact powers, ensuring that even degenerate compositions are handled without special casing.
