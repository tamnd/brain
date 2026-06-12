---
title: "CF 906D - Power Tower"
description: "We are asked to compute a \"power tower\" modulo a given number. Conceptually, imagine a sequence of rocks, each with a positive integer power."
date: "2026-06-12T23:21:08+07:00"
tags: ["codeforces", "competitive-programming", "chinese-remainder-theorem", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 906
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 454 (Div. 1, based on Technocup 2018 Elimination Round 4)"
rating: 2700
weight: 906
solve_time_s: 887
verified: true
draft: false
---

[CF 906D - Power Tower](https://codeforces.com/problemset/problem/906/D)

**Rating:** 2700  
**Tags:** chinese remainder theorem, math, number theory  
**Solve time:** 14m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute a "power tower" modulo a given number. Conceptually, imagine a sequence of rocks, each with a positive integer power. To construct the tower from rocks numbered _l_ through _r_, we start from the top rock _r_ and work down to _l_, repeatedly raising the current rock's power to the power of the tower above it. Formally, if we have rocks $w_l, w_{l+1}, \dots, w_r$, the cumulative power is

$$w_l^{w_{l+1}^{\dots^{w_r}}} \mod m$$

The input gives the number of rocks $n$, the modulus $m$, the powers of each rock in sequence, and $q$ queries asking for the cumulative power of a subrange of rocks.

Constraints tell us $n$ and $q$ can reach $10^5$ and rock powers and the modulus can be up to $10^9$. A naive solution that evaluates the exponentiation directly would produce astronomically large numbers and is infeasible. Even Python's arbitrary-precision arithmetic would be too slow for repeated computations over $10^5$ queries. This implies we need a solution that avoids computing full powers and instead uses properties of modular arithmetic.

Non-obvious edge cases include when $m = 1$, in which the result is always 0, and sequences where powers are 1, which can collapse the tower quickly. Another tricky case arises when consecutive powers are very large, for instance $2^{2^{30}}$, where direct computation will overflow even 64-bit integers. Handling these cases correctly requires careful use of modular reduction and Euler's theorem.

## Approaches

The brute-force approach iterates over the tower from top to bottom, computing the nested exponentiation modulo $m$. Specifically, for each query, one could compute:

```
result = w_r
for i in range(r-1, l-1, -1):
    result = w_i ** result % m
```

This is correct mathematically but infeasible in practice. Even one query could involve exponentiating numbers as large as 10^9^{10^9}, which is astronomically expensive. With up to $10^5$ queries, the complexity is exponential in the length of the subarray, which is untenable.

The key insight for optimization is that modular exponentiation has a recursive property governed by Euler's theorem. If $a$ and $m$ are coprime, $a^{\phi(m)} \equiv 1 \mod m$, where $\phi$ is Euler's totient function. This allows us to reduce the exponent modulo $\phi(m)$ at each step, drastically reducing the size of intermediate powers while preserving correctness. If $a$ and $m$ are not coprime, we must carefully handle the reduction to avoid losing the correct modulo behavior, typically by bounding exponents and adding $\phi(m)$ when necessary.

This transforms the problem into a recursive computation that descends through the tower, reducing exponents at each step using the totient chain until reaching the bottom. This approach is efficient even for large powers and large $m$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * (r-l+1) * exponentiation) | O(1) | Too slow |
| Optimal | O(n log m + q log m) | O(log m) recursion depth | Accepted |

## Algorithm Walkthrough

1. Precompute a totient chain for the modulus. Starting from $m$, repeatedly compute $\phi(m_i)$ until reaching 1. This allows exponent reduction at each level of recursion.
2. Define a recursive function `tower(l, r, mod)` that computes $w_l^{w_{l+1}^{\dots^{w_r}}} \mod mod$. If `l == r`, return $w_l \mod mod$. Otherwise, compute `next_exp = tower(l+1, r, phi(mod))`.
3. Use modular exponentiation with exponent `next_exp`. If the exponent exceeds `phi(mod)` or is larger than necessary due to non-coprime situations, adjust it by adding `phi(mod)` to handle overflow correctly.
4. For each query, call `tower(l, r, m)` and output the result.

Why it works: The totient reduction guarantees that for each level, we replace a potentially huge exponent with a much smaller equivalent modulo $\phi(m)$, while Euler's theorem ensures the result modulo $m$ remains correct. Recursively applying this down the tower preserves the correctness invariant.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(200000)

def phi(n):
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 1
    if n > 1:
        result -= result // n
    return result

def mod_pow(a, b, mod):
    result = 1
    a %= mod
    while b > 0:
        if b & 1:
            result = result * a % mod
        a = a * a % mod
        b >>= 1
    return result

def tower(l, r, mod):
    if mod == 1:
        return 0
    if l == r:
        return w[l] % mod
    next_exp = tower(l+1, r, phis[mod])
    if next_exp >= phis[mod]:
        next_exp = next_exp % phis[mod] + phis[mod]
    return mod_pow(w[l], next_exp, mod)

n, m = map(int, input().split())
w = [0] + list(map(int, input().split()))
phis = {}

def build_phi_chain(x):
    if x in phis:
        return phis[x]
    if x == 1:
        phis[x] = 1
    else:
        phis[x] = phi(x)
    return phis[x]

def prepare_phis(x):
    build_phi_chain(x)
    current = x
    while current != 1:
        current = phis[current]
        build_phi_chain(current)

prepare_phis(m)

q = int(input())
for _ in range(q):
    l, r = map(int, input().split())
    print(tower(l, r, m))
```

This solution starts by precomputing the totient chain for the modulus to enable efficient recursive exponent reduction. `mod_pow` performs fast modular exponentiation. The recursive `tower` function computes the power tower modulo `mod`, adjusting exponents as needed to account for values exceeding the totient. Each query invokes `tower` directly.

## Worked Examples

### Sample Input 1

```
6 1000000000
1 2 2 3 3 3
8
1 1
1 6
2 2
2 3
2 4
4 4
4 5
4 6
```

| Query | l | r | Computed tower | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 6 | 1^{2^{2^{3^{3^3}}}} mod 1e9 | 1 |
| 3 | 2 | 2 | 2 | 2 |
| 4 | 2 | 3 | 2^2 = 4 | 4 |
| 5 | 2 | 4 | 2^{2^3} = 2^8 = 256 | 256 |
| 6 | 4 | 4 | 3 | 3 |
| 7 | 4 | 5 | 3^3 = 27 | 27 |
| 8 | 4 | 6 | 3^{3^3} mod 1e9 = 597484987 | 597484987 |

This trace shows how the totient chain and recursion reduce the massive exponents to manageable computations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log m * log max w_i) | Each query descends through the tower, reducing modulo the totient chain, with fast modular exponentiation for each level |
| Space | O(n + log m) | Array of powers plus recursion stack limited by totient chain length |

This fits within the limits, as $log m \le 30$ for $m \le 10^9$, and $q \le 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # Call the solution function
    exec(open('power_tower.py').read())
    return output.getvalue().strip()

# Provided sample
assert run("""6 1000000000
1 2 2 3 3 3
8
1 1
1 6
2 2
2 3
2 4
4 4
4 5
4 6""") == """1
1
2
4
256
3
27
597484987"""

# Custom cases
assert run("1
```
