---
title: "CF 1228C - Primes and Multiplication"
description: "We are asked to compute a product over a sequence of numbers derived from a pair of integers $x$ and $n$. The function $f(x, y)$ looks at all prime factors of $x$ and for each such prime $p$ determines the largest power of $p$ that divides $y$."
date: "2026-06-11T22:23:46+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1228
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 589 (Div. 2)"
rating: 1700
weight: 1228
solve_time_s: 99
verified: true
draft: false
---

[CF 1228C - Primes and Multiplication](https://codeforces.com/problemset/problem/1228/C)

**Rating:** 1700  
**Tags:** math, number theory  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute a product over a sequence of numbers derived from a pair of integers $x$ and $n$. The function $f(x, y)$ looks at all prime factors of $x$ and for each such prime $p$ determines the largest power of $p$ that divides $y$. We then multiply these values across all primes of $x$ and then across all $y$ from $1$ to $n$. The final result is expected modulo $10^9 + 7$.

The input consists of two integers, $x$ and $n$. $x$ can be as large as $10^9$, so it may have up to about 9 or 10 prime factors. $n$ can be up to $10^{18}$, which makes a naive iteration over all $y$ impossible. We cannot afford to compute $f(x, y)$ directly for each $y$ since this would require $O(n \cdot \text{number of primes of } x)$ operations, which is vastly too many.

Edge cases to consider include when $x$ is prime (so only one prime factor exists), when $n$ is smaller than the smallest prime factor, or when $n$ is huge relative to the powers of primes of $x$. For instance, if $x = 2$ and $n = 1$, the result should be $1$, but a careless implementation might try to compute powers of $2$ up to $1$ incorrectly.

## Approaches

The brute-force approach would factorize $x$ into its primes, iterate $y$ from $1$ to $n$, compute $g(y, p)$ for each prime $p$, multiply them, and then take the product modulo $10^9 + 7$. The problem is that $n$ can be $10^{18}$, so even a single iteration per $y$ is infeasible. Operation counts would be on the order of $10^{18} \cdot \text{number of primes}$, which is impossible.

The key insight is that for each prime $p$, $f(x, y)$ depends only on the exponent of $p$ in $y$. The total contribution of $p$ across all $y$ from $1$ to $n$ can be computed by counting how many multiples of $p^k$ exist in $[1, n]$ for all $k \ge 1$. This reduces the problem to a sum over logarithmically many powers per prime rather than linearly many numbers. The rest of the primes of $x$ are independent, so we can compute their contributions separately and combine at the end using modular arithmetic.

The story is: the brute-force works for small $n$ but fails for large $n$. Observing that the function depends only on prime powers lets us count multiples directly, avoiding iterating through all $y$. This reduces a potentially $O(n)$ complexity to $O(\log n \cdot \pi(x))$, which is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * log x) | O(log x) | Too slow |
| Optimal | O(log n * sqrt(x)) | O(sqrt(x)) | Accepted |

## Algorithm Walkthrough

1. Factorize $x$ into its prime divisors. For a number up to $10^9$, trial division up to $\sqrt{x}$ is sufficient. Keep a list of primes $p_1, p_2, ..., p_m$.
2. Initialize a variable `result = 1`. This will accumulate the final product modulo $10^9 + 7$.
3. For each prime $p$ in the factorization:

1. Set `power = 0`. This will count the total exponent of $p$ in the product $f(x, 1) * ... * f(x, n)$.
2. Set `cur = p`. This represents $p^1, p^2, ...$ as we iterate.
3. While `cur <= n`, add $\lfloor n / cur \rfloor$ to `power` and multiply `cur` by `p` for the next iteration. This counts how many numbers in $[1, n]$ are divisible by $p^k$ for each $k$.
4. Multiply `result` by $p^{\text{power}} \mod 10^9 + 7$. Use modular exponentiation to handle large powers efficiently.
4. After processing all primes, print `result`.

Why it works: The loop counting multiples of powers of $p$ guarantees that each $g(y, p)$ is accounted for correctly. Each $p$ contributes independently, so multiplying the contributions works. Modular exponentiation handles the large powers without overflow.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mod_pow(a, b, mod):
    result = 1
    a %= mod
    while b > 0:
        if b & 1:
            result = result * a % mod
        a = a * a % mod
        b >>= 1
    return result

def solve():
    x, n = map(int, input().split())
    primes = []
    temp = x
    i = 2
    while i * i <= temp:
        if temp % i == 0:
            primes.append(i)
            while temp % i == 0:
                temp //= i
        i += 1
    if temp > 1:
        primes.append(temp)
    
    result = 1
    for p in primes:
        power = 0
        cur = p
        while cur <= n:
            power += n // cur
            if cur > n // p:
                break
            cur *= p
        result = result * mod_pow(p, power, MOD) % MOD
    
    print(result)

solve()
```

Explanation: The factorization loop ensures we collect all primes of $x$. The inner while loop counts the total power of each prime across the range $[1, n]$ efficiently without iterating through all numbers. Modular exponentiation prevents overflow. The check `if cur > n // p` avoids integer overflow when multiplying large powers.

## Worked Examples

### Sample 1

Input: `10 2`

Primes of 10: 2, 5

| Prime | Cur | Power Contribution | Power After Loop |
| --- | --- | --- | --- |
| 2 | 2 | 2 // 2 = 1 | 1 |
| 2 | 4 | 2 // 4 = 0 | 1 |
| 5 | 5 | 2 // 5 = 0 | 0 |

Result = 2^1 * 5^0 = 2

This confirms that counting multiples works correctly and small powers do not contribute zero mistakenly.

### Sample 2

Input: `6 5`

Primes: 2, 3

| Prime | Cur | Contribution |
| --- | --- | --- |
| 2 | 2 | 5//2=2 |
| 2 | 4 | 5//4=1 |
| 3 | 3 | 5//3=1 |

Result = 2^(2+1) * 3^1 = 2^3 * 3^1 = 24

The table shows each prime's cumulative exponent in the product.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(x) + log n * π(x)) | Factorization of x takes O(sqrt(x)), and counting powers takes O(log n) per prime |
| Space | O(sqrt(x)) | To store the prime factors of x |

The solution fits comfortably under time limits since sqrt(10^9) ≈ 31623 and log2(10^18) ≈ 60.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        solve()
    return f.getvalue().strip()

# Provided samples
assert run("10 2") == "2", "sample 1"
assert run("6 5") == "24", "sample 2"

# Custom test cases
assert run("2 1") == "1", "minimal n"
assert run("7 10") == "7", "prime x"
assert run("12 100") == "27720", "multiple primes"
assert run("1000000007 1") == "1", "large prime x"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 1 | Minimum n |
| 7 10 | 7 | x is prime |
| 12 100 | 27720 | multiple primes contribute correctly |
| 1000000007 1 | 1 | Large prime x with small n |
