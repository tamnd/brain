---
title: "CF 2205B - Simons and Cakes for Success"
description: "We are asked to help Simons divide cakes among his friends. More formally, for a given number of friends $n$, we need to find the smallest positive integer $k$ such that $k^n$ is divisible by $n$. The input consists of multiple test cases, each specifying the number of friends."
date: "2026-06-07T19:50:09+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2205
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1083 (Div. 2)"
rating: 800
weight: 2205
solve_time_s: 141
verified: true
draft: false
---

[CF 2205B - Simons and Cakes for Success](https://codeforces.com/problemset/problem/2205/B)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to help Simons divide cakes among his friends. More formally, for a given number of friends $n$, we need to find the smallest positive integer $k$ such that $k^n$ is divisible by $n$. The input consists of multiple test cases, each specifying the number of friends. The output for each case is the minimum $k$ that satisfies the divisibility condition.

The constraints allow $n$ to be as large as $10^9$ and the number of test cases up to 100. Any algorithm that attempts to compute $k^n$ directly for all $k$ up to $n$ would be far too slow, since exponentiation with large numbers is expensive and iterating up to $10^9$ is impractical. The challenge is therefore to determine a method that works without brute-forcing powers.

A naive approach would check $k=1,2,3,\dots$ and test if $k^n \mod n = 0$. For small $n$, this works, but for $n\sim 10^9$, it would require billions of iterations. Also, $1^n$ is always 1, which fails when $n>1$, so this is a common pitfall for careless implementations.

Another subtle case is when $n$ is prime or a power of a prime. For example, $n=8$ requires $k=2$ because $2^3 = 8$ divides $2^8 = 256$. Misunderstanding the structure of $n$ often leads to overestimating $k$.

## Approaches

The brute-force method iterates $k=1,2,3,\dots$ and checks if $n$ divides $k^n$. Each check involves modular exponentiation, which is $O(\log n)$. In the worst case, $k$ can be as large as $n$, giving $O(n \log n)$. For $n \sim 10^9$, this is too slow.

The key insight comes from factorization. Let $n$ have prime factorization $n = p_1^{a_1} p_2^{a_2} \dots p_m^{a_m}$. To have $k^n$ divisible by $n$, each prime $p_i$ must appear in $k^n$ with at least exponent $a_i$. In other words, the multiplicity of $p_i$ in $k$ must be at least $\lceil a_i / n \rceil = 1$ because $a_i/n < 1$. Therefore, the minimal $k$ is obtained by multiplying the distinct prime factors of $n$.

This reduces the problem to prime factorization of $n$, which is efficient for the given constraints because $n \le 10^9$. We can factorize using trial division up to $\sqrt{n}$, which requires at most about 31,622 iterations per test case. Multiplying the distinct primes gives the minimal $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(1) | Too slow |
| Factorization & Product of Primes | O(√n) | O(√n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$.
3. Initialize an empty list for prime factors.
4. Iterate $d$ from 2 up to $\sqrt{n}$. If $d$ divides $n$, add $d$ to the list of prime factors. Then divide $n$ by $d$ repeatedly until it is no longer divisible. This extracts the highest power of $d$ in $n$ while recording only the distinct prime.
5. If after the loop $n>1$, it is itself a prime factor, add it to the list.
6. Compute $k$ as the product of all distinct prime factors.
7. Print $k$.

Why it works: Each prime factor of $n$ must appear in $k$, otherwise $k^n$ cannot supply enough multiples of that prime to divide $n$. Including each distinct prime exactly once produces the minimal $k$, since adding higher powers would unnecessarily increase $k$.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def minimal_k(n):
    original_n = n
    k = 1
    for d in range(2, int(n**0.5)+1):
        if n % d == 0:
            k *= d
            while n % d == 0:
                n //= d
    if n > 1:
        k *= n
    return k

t = int(input())
for _ in range(t):
    n = int(input())
    print(minimal_k(n))
```

The solution defines a function `minimal_k` to factorize $n$ and compute the product of distinct primes. The outer loop reads all test cases. Using `int(n**0.5)` ensures trial division only goes up to the square root. The inner loop divides $n$ by the factor repeatedly to remove all powers, avoiding duplicate multiplication.

## Worked Examples

### Sample 1: n = 8

| Step | n remaining | Factor found | k |
| --- | --- | --- | --- |
| 2 | 8 | 2 | 1*2 = 2 |
| 2 | 4 | - | 2 |
| 2 | 2 | - | 2 |
| 2 | 1 | - | 2 |
| Finished | 1 | - | 2 |

We see that `2^8 = 256` and 8 divides 256, confirming correctness.

### Sample 2: n = 12

| Step | n remaining | Factor found | k |
| --- | --- | --- | --- |
| 2 | 12 | 2 | 2 |
| 2 | 6 | - | 2 |
| 2 | 3 | - | 2 |
| 3 | 3 | 3 | 2*3 = 6 |
| Finished | 1 | - | 6 |

`6^12` is divisible by 12, and 6 is minimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t√n) | Each test case factorizes up to √n, t ≤ 100 |
| Space | O(√n) | Stores at most distinct primes up to √n |

For the maximum $n=10^9$ and $t=100$, total operations ≈ 100 * 31,622 ≈ 3.16 million, which fits comfortably under 1-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    input = sys.stdin.readline

    def minimal_k(n):
        k = 1
        for d in range(2, int(n**0.5)+1):
            if n % d == 0:
                k *= d
                while n % d == 0:
                    n //= d
        if n > 1:
            k *= n
        return k

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        res.append(str(minimal_k(n)))
    return "\n".join(res)

# provided samples
assert run("4\n8\n12\n369\n55635800\n") == "2\n6\n123\n2090", "sample 1"

# custom cases
assert run("3\n2\n3\n5\n") == "2\n3\n5", "primes"
assert run("2\n4\n16\n") == "2\n2", "powers of two"
assert run("2\n18\n20\n") == "6\n10", "composite numbers with multiple primes"
assert run("1\n1000000000\n") == "10", "large n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2,3,5 | 2,3,5 | minimal k for prime n |
| 4,16 | 2,2 | powers of 2 handled correctly |
| 18,20 | 6,10 | multiple primes combined correctly |
| 1e9 | 10 | large n performance |

## Edge Cases

For $n=2$, the algorithm finds 2 as the only prime factor. For $n$ prime, $k=n$. For powers of a prime like 16, the algorithm finds 2, the distinct prime, which is correct since $2^{16}$ divisible by 16. In each case, the multiplication of distinct primes produces the minimal $k$, demonstrating that the factorization-based approach handles all non-obvious edge cases correctly.
