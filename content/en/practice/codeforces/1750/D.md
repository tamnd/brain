---
title: "CF 1750D - Count GCD"
description: "We are asked to count arrays $b$ that match a sequence of prefix greatest common divisors. Concretely, for each position $i$, the GCD of the first $i$ elements of $b$ must equal $ai$. Each element $bi$ must be an integer between 1 and $m$."
date: "2026-06-09T15:06:18+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1750
codeforces_index: "D"
codeforces_contest_name: "CodeTON Round 3 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1800
weight: 1750
solve_time_s: 80
verified: true
draft: false
---

[CF 1750D - Count GCD](https://codeforces.com/problemset/problem/1750/D)

**Rating:** 1800  
**Tags:** combinatorics, math, number theory  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count arrays $b$ that match a sequence of prefix greatest common divisors. Concretely, for each position $i$, the GCD of the first $i$ elements of $b$ must equal $a_i$. Each element $b_i$ must be an integer between 1 and $m$. The output is the number of such arrays modulo $998{,}244{,}353$.

The input consists of multiple test cases. Each test case has an integer $n$ for the length of the array and an integer $m$ for the maximum allowed value. Then $n$ integers $a_1, \dots, a_n$ specify the required prefix GCDs.

The constraints tell us $n$ can be up to $2\cdot 10^5$ and $m$ up to $10^9$. Since the sum of $n$ across test cases is bounded by $2\cdot 10^5$, we need a solution that is roughly linear in $n$ per test case. A naive approach that enumerates all possible arrays $b$ is impossible because $m^n$ is astronomically large. Any solution iterating over all values of $b_i$ explicitly is infeasible.

A non-obvious edge case occurs when the sequence $a$ is not non-increasing in the sense of divisibility. For example, if $a = [2,3]$, there is no possible $b$ because $\gcd(b_1) = 2$ and $\gcd(b_1,b_2) = 3$ cannot happen-3 does not divide 2. A careless solution that ignores divisibility checks would incorrectly try to compute valid $b_2$ and produce a non-zero count.

Another subtlety is when $a_i$ equals $a_{i-1}$. In that case, $b_i$ must be a multiple of $a_i$, but no additional constraints arise from the previous GCD, so the count includes all multiples of $a_i$ up to $m$ that preserve the GCD.

## Approaches

The brute-force approach is to enumerate every possible $b_1$ in $[1,m]$, then for each $b_1$ every possible $b_2$ in $[1,m]$, and so on, computing the prefix GCD at each step. This would take $O(m^n)$, which is infeasible since $m$ can be $10^9$ and $n$ up to $2\cdot 10^5$.

The key observation is that the prefix GCDs impose strong divisibility constraints. Specifically, each $b_i$ must be a multiple of $a_i$, and for the GCD to drop from $a_{i-1}$ to $a_i$, $b_i$ must satisfy $\gcd(b_i, a_{i-1}) = a_i$. This is equivalent to counting integers $x$ such that $1 \le x \le \frac{m}{a_i}$ and $\gcd(x, \frac{a_{i-1}}{a_i}) = 1$. Here, we rescale by $a_i$ to reduce the problem to counting integers coprime to a given number. Using the Euler totient function $\phi(k)$, we can compute the number of integers up to $t$ that are coprime to $k$ efficiently.

This observation allows a linear scan through the array $a$, computing $\phi(a_{i-1}/a_i)$ for each step, giving an $O(n \sqrt{a_{i-1}/a_i})$ or faster per test case solution. If any $a_i$ does not divide $a_{i-1}$, the answer is immediately 0.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n) | O(n) | Too slow |
| Optimal | O(n log n) amortized | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $t$, the number of test cases, and iterate over them.
2. For each test case, read $n$ and $m$, then the array $a$.
3. Initialize a variable `ans = 1` to hold the product of valid choices modulo $998244353$.
4. If $a_0 > m$, set `ans = 0` because the first element cannot exceed $m$.
5. Iterate over $i$ from 1 to $n-1$:

1. Check if $a_{i-1}$ is divisible by $a_i$. If not, set `ans = 0` and break.
2. Compute $k = a_{i-1} / a_i$. The number of integers $b_i = a_i \cdot x$ such that $1 \le b_i \le m$ and $\gcd(b_i, a_{i-1}) = a_i$ is equal to the number of integers $x \le m / a_i$ that are coprime with $k$.
3. Factorize $k$ into its prime factors.
4. Use inclusion-exclusion on the prime factors to count integers $x \le m / a_i$ coprime to $k$.
5. Multiply this count into `ans` modulo $998244353$.
6. Output `ans`.

Why it works: the invariant is that at step $i$, we maintain the number of arrays $b_1 \dots b_i$ that satisfy the prefix GCD constraints. Divisibility ensures the GCD can drop from $a_{i-1}$ to $a_i$, and scaling by $a_i$ reduces counting to coprime integers. Inclusion-exclusion precisely counts integers that are coprime to $k$, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

def prime_factors(x):
    i = 2
    factors = set()
    while i * i <= x:
        if x % i == 0:
            factors.add(i)
            while x % i == 0:
                x //= i
        i += 1
    if x > 1:
        factors.add(x)
    return list(factors)

def count_coprime(n, primes):
    # Inclusion-Exclusion to count numbers <= n coprime with product of primes
    res = 0
    m = len(primes)
    for mask in range(1, 1 << m):
        prod = 1
        bits = 0
        for i in range(m):
            if mask & (1 << i):
                prod *= primes[i]
                bits += 1
        cnt = n // prod
        if bits % 2 == 1:
            res += cnt
        else:
            res -= cnt
    return n - res

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    if a[0] > m:
        print(0)
        continue
    ans = 1
    for i in range(1, n):
        if a[i-1] % a[i] != 0:
            ans = 0
            break
        k = a[i-1] // a[i]
        x_max = m // a[i]
        if k == 1:
            cnt = x_max
        else:
            primes = prime_factors(k)
            cnt = count_coprime(x_max, primes)
        ans = ans * cnt % MOD
    print(ans)
```

The `prime_factors` function efficiently factorizes a number by trial division. `count_coprime` uses inclusion-exclusion over these primes to count integers up to a limit that are coprime to the factorization. Multiplying these counts respects the independence of choices at each position, ensuring the correct total count modulo $998244353$.

## Worked Examples

### Example 1

Input: `3 5\n4 2 1`

| i | a[i] | a[i-1] | k = a[i-1]/a[i] | x_max = m//a[i] | primes | count_coprime | ans |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | - | - | 5//4=1 | - | 1 | 1 |
| 2 | 2 | 4 | 2 | 5//2=2 | [2] | 2-1=1 | 1 |
| 3 | 1 | 2 | 2 | 5//1=5 | [2] | 5-2=3 | 3 |

This matches the sample output 3.

### Example 2

Input: `2 1\n1 1`

| i | a[i] | a[i-1] | k | x_max | primes | count_coprime | ans |

|---|
