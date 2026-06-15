---
title: "CF 1068B - LCM"
description: "We are given a single integer $b$, and we conceptually iterate over every positive integer $a$. For each $a$, we compute a value derived from the least common multiple of $a$ and $b$, specifically $frac{mathrm{lcm}(a,b)}{a}$."
date: "2026-06-15T07:53:44+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1068
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 518 (Div. 2) [Thanks, Mail.Ru!]"
rating: 1200
weight: 1068
solve_time_s: 321
verified: true
draft: false
---

[CF 1068B - LCM](https://codeforces.com/problemset/problem/1068/B)

**Rating:** 1200  
**Tags:** math, number theory  
**Solve time:** 5m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $b$, and we conceptually iterate over every positive integer $a$. For each $a$, we compute a value derived from the least common multiple of $a$ and $b$, specifically $\frac{\mathrm{lcm}(a,b)}{a}$. Ivan writes this value on a board, and we are asked how many distinct values appear when $a$ ranges over all positive integers.

The key point is that although $a$ ranges up to $10^{18}$, the expression depends only on how $a$ interacts with the prime structure of $b$. The output is not about summing or maximizing anything, but about counting how many different multiplicative outcomes this ratio can produce.

The constraint $b \le 10^{10}$ suggests that a solution depending only on the prime factorization of $b$ is feasible, since factorizing up to $10^{10}$ is manageable in deterministic $O(\sqrt{b})$ time. Any approach that iterates over all $a \le 10^{18}$ is immediately impossible.

A naive attempt would try to evaluate the expression for many $a$, but this fails in two ways. First, the domain of $a$ is infinite in practical terms. Second, many different $a$ produce the same result, and the duplication structure is highly regular but not obvious without number theory.

A subtle edge case appears when $b = 1$. Then $\mathrm{lcm}(a,1) = a$, so the expression is always $1$, giving exactly one value. Another edge case is when $b$ is prime, where the structure collapses into only two possible outcomes depending on divisibility by that prime.

## Approaches

Start from the definition of the expression. Using the identity

$$\mathrm{lcm}(a,b) = \frac{ab}{\gcd(a,b)},$$

we rewrite the expression as

$$\frac{\mathrm{lcm}(a,b)}{a} = \frac{b}{\gcd(a,b)}.$$

This transforms the problem from something about least common multiples into something purely about gcd values. Now the expression depends only on $\gcd(a,b)$, which must be a divisor of $b$. This immediately reduces the infinite domain of $a$ into a finite set of possible gcd values.

Let $g = \gcd(a,b)$. Then $g \mid b$, and the expression becomes $b/g$. So each value written on the board corresponds exactly to choosing a divisor $g$ of $b$, provided that such a gcd can actually be achieved by some $a$. Every divisor $g$ of $b$ is achievable by taking $a = g \cdot k$ where $k$ is coprime with $b/g$, so no divisors are excluded.

Thus, the set of distinct values written is exactly:

$$\left\{ \frac{b}{d} \mid d \mid b \right\}.$$

Different divisors $d$ produce different values $b/d$, so the number of distinct results is exactly the number of divisors of $b$.

The problem reduces to counting divisors of $b$, which is done via prime factorization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over $a$ | $O(10^{18})$ | $O(1)$ | Too slow |
| Factorization + divisor count | $O(\sqrt{b})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Factorize $b$ into its prime powers. We scan integers up to $\sqrt{b}$, extracting how many times each prime divides $b$. This is sufficient because any composite factor must have a prime factor not exceeding $\sqrt{b}$.
2. For each prime $p$, count its exponent $e$ in the factorization of $b$. This step matters because divisor counting depends only on these exponents, not on the actual value of $b$.
3. Compute the total number of divisors using the formula

$$\tau(b) = \prod (e_i + 1),$$

where each $e_i$ is the exponent of a distinct prime factor.
4. Output this product as the answer, since each divisor corresponds to exactly one distinct value of $\frac{b}{\gcd(a,b)}$.

### Why it works

Every possible value of the expression is uniquely determined by a divisor of $b$, because the expression simplifies to $b/g$ where $g \mid b$. Conversely, every divisor $g$ can be realized as a gcd by constructing $a$ with the appropriate shared prime factors and avoiding additional ones that would increase the gcd. This establishes a one-to-one correspondence between divisors of $b$ and distinct values written on the board.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    b = int(input().strip())
    x = b
    ans = 1

    p = 2
    while p * p <= x:
        if x % p == 0:
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            ans *= (cnt + 1)
        p += 1

    if x > 1:
        ans *= 2

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first factorizes $b$ by trial division. Each time a prime factor is found, it counts its multiplicity and updates the divisor product. If after the loop a remainder greater than 1 remains, that remainder is a prime factor contributing exponent 1, doubling the divisor count.

The subtle point is that we never iterate over $a$. The entire problem collapses into structure inside $b$, and the gcd reformulation removes any dependence on the huge upper bound on $a$.

## Worked Examples

Consider $b = 2$. The divisors are $1, 2$. The expression values are $2/1 = 2$ and $2/2 = 1$.

| Step | Divisor $d$ | $b/d$ |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 1 |

This shows two distinct values, matching the divisor count.

Now consider $b = 12 = 2^2 \cdot 3^1$. Its divisors are determined by exponent choices: for $2^2$, choose exponent 0 to 2; for $3^1$, choose exponent 0 to 1.

| Prime | Exponent | Contribution |
| --- | --- | --- |
| 2 | 2 | 3 choices |
| 3 | 1 | 2 choices |

Total divisors $= 3 \cdot 2 = 6$.

This demonstrates how independent prime contributions combine multiplicatively, reflecting the structure of gcd-based values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{b})$ | trial division factorization up to square root |
| Space | $O(1)$ | only counters and a few variables |

The bound $b \le 10^{10}$ makes $\sqrt{b} \approx 10^5$, which is easily fast enough in Python. The algorithm avoids iterating over $a$ entirely, relying only on arithmetic structure of $b$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    b = int(input().strip())
    x = b
    ans = 1
    p = 2
    while p * p <= x:
        if x % p == 0:
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            ans *= (cnt + 1)
        p += 1
    if x > 1:
        ans *= 2
    print(ans)

# samples
assert run("1\n") == "1"

# custom tests
assert run("2\n") == "2"
assert run("12\n") == "6"
assert run("36\n") == "9"
assert run("49\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest edge case |
| 2 | 2 | prime input |
| 12 | 6 | composite with multiple primes |
| 49 | 3 | repeated prime factor |

## Edge Cases

When $b = 1$, factorization yields no primes, so the divisor count remains 1. The algorithm correctly returns 1 without entering the loop body.

When $b$ is prime, say $13$, the loop finds no factors, and the leftover $x > 1$ triggers multiplication by 2, producing exactly two divisors $1$ and $13$, matching the expected two distinct values of the expression.

When $b$ is a perfect power like $2^k$, the loop repeatedly divides out the same prime and accumulates exponent $k$, producing $k+1$ divisors, which corresponds exactly to the number of achievable gcd values and thus distinct outputs of the original expression.
