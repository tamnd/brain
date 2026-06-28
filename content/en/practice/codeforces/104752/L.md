---
title: "CF 104752L - Lucia's Treasure"
description: "We are given a single positive integer $X$, and we are asked to construct a number that satisfies two conditions at the same time. First, it must be divisible by $X$. Second, it must be a perfect square, meaning its prime factorization has all exponents even."
date: "2026-06-28T23:00:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104752
codeforces_index: "L"
codeforces_contest_name: "Concurso de programaci\u00f3n ANIEI 2023"
rating: 0
weight: 104752
solve_time_s: 59
verified: true
draft: false
---

[CF 104752L - Lucia's Treasure](https://codeforces.com/problemset/problem/104752/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single positive integer $X$, and we are asked to construct a number that satisfies two conditions at the same time. First, it must be divisible by $X$. Second, it must be a perfect square, meaning its prime factorization has all exponents even.

Another way to think about the task is that we are allowed to multiply $X$ by some positive integer $k$, and we want the smallest possible value of $X \cdot k$ such that the result becomes a perfect square.

The constraint $X \le 10^9$ implies that we cannot afford any algorithm that depends on iterating through multiples or searching upward for squares. A naive scan like checking $X, 2X, 3X,\dots$ and testing each for being a square would be far too slow in the worst case, since the smallest square multiple might be much larger than $X$, especially when $X$ has many distinct prime factors.

A less obvious difficulty appears when $X$ is square-free or close to square-free. For example, when $X = 30$, the answer is $900$, which is already 30 times larger than $X$. If we tried to search linearly, we would quickly exceed any reasonable time limit.

The key edge case structure is that the answer is not derived from additive or divisibility patterns, but from the parity of exponents in the prime factorization. Any naive method that ignores factorization will fail on cases like $X = 12$, where the answer is $36$, not $12$ or $24$, and the correct multiplier is not obvious without structural reasoning.

## Approaches

A brute-force approach starts from $X$ and checks $X \cdot 1, X \cdot 2, X \cdot 3,\dots$, testing whether each value is a perfect square. Each check requires computing an integer square root or verifying whether the square of an integer equals the number. In the worst case, the correct answer could be far away, so this degenerates into scanning a large range of integers, easily exceeding $10^9$ operations.

The structural observation comes from prime factorization. A number is a perfect square if and only if every prime exponent in its factorization is even. If we write $X$ as a product of primes with exponents, we can see exactly which primes violate this condition. Each prime with an odd exponent must be paired with one more copy of itself to make the exponent even. That means we only need to multiply $X$ by a minimal factor that fixes parity of all exponents.

This turns the problem into a deterministic construction: factorize $X$, collect all primes whose exponent is odd, and multiply them together once. That product is exactly the smallest number that turns all exponents even, producing the minimal square multiple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k \sqrt{X})$ or worse | $O(1)$ | Too slow |
| Optimal | $O(\sqrt{X})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Factorize $X$ by testing divisors up to $\sqrt{X}$. For each divisor $p$, repeatedly divide $X$ by $p$ to count its exponent. This is necessary because prime structure determines square-ness.
2. Maintain a running result initialized to 1. This variable will store the smallest multiplier needed to correct parity of exponents.
3. For each prime factor $p$, check how many times it divides $X$. If its exponent is odd, multiply the result by $p$. This fixes the parity because adding one copy of $p$ turns an odd exponent into an even one.
4. After processing all primes up to $\sqrt{X}$, if the remaining $X$ is greater than 1, it is a prime factor with exponent 1. This is always odd, so multiply the result by this leftover prime.
5. Return the original $X$ multiplied by the computed correction factor, which is guaranteed to be a perfect square.

The reasoning behind step 4 is important: any prime larger than $\sqrt{X}$ cannot appear twice, so its exponent must be exactly 1. That automatically makes it odd.

### Why it works

Every integer has a unique prime factorization. A number is a perfect square if and only if all exponents in this factorization are even. The algorithm constructs the minimal multiplier that makes all exponents even by independently correcting each odd exponent exactly once. No interaction exists between different primes, so minimizing the multiplier reduces to local parity fixes. Since we only add each odd prime factor once, the resulting product is the smallest possible correction factor.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x = int(input().strip())
    original = x
    res = 1

    i = 2
    while i * i <= x:
        if x % i == 0:
            cnt = 0
            while x % i == 0:
                x //= i
                cnt += 1
            if cnt % 2 == 1:
                res *= i
        i += 1

    if x > 1:
        res *= x

    print(original * res)

if __name__ == "__main__":
    solve()
```

The solution relies on a standard trial division factorization loop. The variable `res` accumulates exactly the primes that appear an odd number of times in the factorization of the original input.

A subtle point is that we must preserve the original value of $X$ before factorization reduces it to 1. The final multiplication uses that original value, because `x` becomes the reduced remainder during factorization.

## Worked Examples

### Example 1: $X = 12$

We factorize $12 = 2^2 \cdot 3^1$.

| Step | Prime | Exponent | Odd? | Result multiplier |
| --- | --- | --- | --- | --- |
| Start | - | - | - | 1 |
| Process 2 | 2 | 2 | No | 1 |
| Process 3 | 3 | 1 | Yes | 3 |

Final value is $12 \cdot 3 = 36$.

This shows how only primes with odd exponent contribute to the multiplier.

### Example 2: $X = 16$

We factorize $16 = 2^4$.

| Step | Prime | Exponent | Odd? | Result multiplier |
| --- | --- | --- | --- | --- |
| Start | - | - | - | 1 |
| Process 2 | 2 | 4 | No | 1 |

Final value is $16 \cdot 1 = 16$.

This confirms that already-perfect squares remain unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{X})$ | trial division up to square root of X |
| Space | $O(1)$ | only a few integers stored |

The bound $X \le 10^9$ makes $\sqrt{X} \le 31623$, which is easily fast enough in Python within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    x = int(input().strip())
    original = x
    res = 1

    i = 2
    while i * i <= x:
        if x % i == 0:
            cnt = 0
            while x % i == 0:
                x //= i
                cnt += 1
            if cnt % 2 == 1:
                res *= i
        i += 1

    if x > 1:
        res *= x

    return str(original * res)

# provided samples
assert run("3\n") == "9", "sample 1"
assert run("16\n") == "16", "sample 2"
assert run("12\n") == "36", "sample 3"

# custom cases
assert run("1\n") == "1", "minimum case"
assert run("2\n") == "4", "prime input"
assert run("18\n") == "36", "mixed exponents"
assert run("49\n") == "49", "already square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest boundary |
| 2 | 4 | single prime exponent correction |
| 18 | 36 | multiple factors with odd exponent mix |
| 49 | 49 | already perfect square stability |

## Edge Cases

For $X = 1$, the factorization loop does nothing and `res` remains 1, so the output is $1$. The algorithm correctly treats 1 as a perfect square.

For a prime number like $X = 2$, factorization yields exponent 1, so `res` becomes 2 and the result is $2 \cdot 2 = 4$, which is the smallest square multiple.

For a number like $X = 18 = 2 \cdot 3^2$, only prime 2 has an odd exponent. The algorithm multiplies by 2, producing $36$, and no smaller square multiple exists because any square must contain at least $2^2$.

For a perfect square like $X = 49$, all exponents are even, so `res = 1` and the output remains unchanged.
