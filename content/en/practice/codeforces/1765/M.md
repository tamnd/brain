---
title: "CF 1765M - Minimum LCM"
description: "We are asked to split a given integer n into two positive parts a and b so that their sum stays fixed at n. Among all such splits, we want the pair that makes the least common multiple of a and b as small as possible."
date: "2026-06-09T13:16:04+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1765
codeforces_index: "M"
codeforces_contest_name: "2022-2023 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Preferably Teams)"
rating: 1000
weight: 1765
solve_time_s: 86
verified: true
draft: false
---

[CF 1765M - Minimum LCM](https://codeforces.com/problemset/problem/1765/M)

**Rating:** 1000  
**Tags:** math, number theory  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to split a given integer `n` into two positive parts `a` and `b` so that their sum stays fixed at `n`. Among all such splits, we want the pair that makes the least common multiple of `a` and `b` as small as possible.

So the input is just a sequence of test cases, each providing a single number `n`. For each `n`, we conceptually place a cut that breaks `n` into two positive integers, and we measure how “compatible” the pair is using LCM. The goal is to find the split where this compatibility measure is minimized.

The constraint `n ≤ 10^9` means we cannot try all possible splits for a single test case in a naive way up to `n/2` and expect it to pass in the worst case if we do anything expensive per split. A linear scan per test case would already be borderline at 10^9 across multiple cases, but more importantly, it signals that the solution must reduce the problem to something like factorization or logarithmic checks.

A subtle edge case is when `n` is small, especially `n = 2`. In that case, the only split is `1 + 1`, so any formula that relies on divisors or largest proper divisors must still handle the fact that the “best divisor” might be `1`. Another edge case is odd numbers like `n = 9`, where intuition might suggest balanced splits like `4 + 5`, but those are not necessarily optimal under LCM; in fact, more structured pairs like `3 + 6` perform better. This shows that symmetry alone is not the correct heuristic.

## Approaches

A direct approach is to try every pair `(a, b)` such that `a + b = n`, compute `lcm(a, b)`, and take the minimum. Since there are roughly `n` choices for `a`, this leads to `O(n)` work per test case. With `n` up to `10^9`, this is completely infeasible.

The key structure comes from rewriting the LCM expression. For any pair `(a, b)`, we can express `a = g x` and `b = g y`, where `g = gcd(a, b)` and `x` and `y` are coprime. The sum constraint becomes `g(x + y) = n`, so `g` must divide `n`. This changes the problem from searching over all splits to searching over divisors of `n`.

Once the sum is fixed in terms of `x + y = n / g`, the product `x * y` determines the LCM as `lcm(a, b) = g * x * y`. For a fixed sum, the product `x * y` is minimized when one value is `1` and the other is `k - 1`. This pushes the LCM to `g * (k - 1)` which simplifies to `n - g`.

Now the objective becomes extremely simple: maximize `g` under the constraint that `g` is a proper divisor of `n`. The best possible `g` is the largest divisor smaller than `n`, which is obtained by dividing `n` by its smallest prime factor.

Brute force works by enumerating all splits, but fails because it ignores the divisor structure. The observation that LCM depends on gcd and sum reduces the problem to finding a single prime factor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test | O(1) | Too slow |
| Prime factor based | O(√n) per test | O(1) | Accepted |

## Algorithm Walkthrough

We now translate the reasoning into a direct procedure.

1. For each test case, read `n`. The goal is to determine a split where the implicit gcd structure is maximized.
2. Find the smallest prime factor `p` of `n`. This is enough because dividing `n` by `p` gives the largest proper divisor of `n`.
3. Compute `g = n / p`. This value represents the best possible gcd for a valid pair `(a, b)`.
4. Construct the pair as `a = g` and `b = n - g`. This guarantees that `a + b = n` and that the gcd structure aligns with the optimal factorization.
5. Output `(a, b)` in any order.

The reason this construction works is that once we fix `g` as a divisor of `n`, the remaining sum splits into `(1, k - 1)` at the level of reduced variables, which minimizes the internal product and therefore minimizes the LCM.

### Why it works

Any valid pair can be written as `(g x, g y)` with `x + y = n / g`. The LCM becomes `g x y`. For fixed `g`, minimizing LCM reduces to minimizing `x y`, which is minimized at extreme imbalance `(1, k - 1)`. The remaining freedom is choosing `g`. Since the final expression simplifies to `n - g`, maximizing `g` gives the optimal solution, and the largest proper divisor of `n` is exactly `n` divided by its smallest prime factor.

## Python Solution

```python
import sys
input = sys.stdin.readline

def smallest_prime_factor(n: int) -> int:
    if n % 2 == 0:
        return 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return d
        d += 2
    return n

t = int(input())
for _ in range(t):
    n = int(input())
    p = smallest_prime_factor(n)
    g = n // p
    a = g
    b = n - g
    print(a, b)
```

The helper function computes the smallest prime factor efficiently by checking divisibility up to `sqrt(n)`. Once we find it, we immediately derive the optimal gcd candidate `g`.

The construction `b = n - g` is intentional: it avoids any recomputation of the complementary structure and directly enforces the sum constraint.

A common mistake is to return `(g, g)`, but that only works when `n` is even and `g = n/2`. The correct formula always preserves the sum condition through subtraction.

## Worked Examples

Consider `n = 9`.

| Step | n | smallest prime factor p | g = n/p | a | b |
| --- | --- | --- | --- | --- | --- |
| init | 9 | - | - | - | - |
| factor | 9 | 3 | - | - | - |
| compute | 9 | 3 | 3 | 3 | 6 |

This produces `(3, 6)`. Other splits like `(4, 5)` or `(1, 8)` yield larger LCM values because they correspond to smaller effective gcd structure, which increases the expression `n - g`.

Now consider `n = 10`.

| Step | n | smallest prime factor p | g = n/p | a | b |
| --- | --- | --- | --- | --- | --- |
| init | 10 | - | - | - | - |
| factor | 10 | 2 | - | - | - |
| compute | 10 | 2 | 5 | 5 | 5 |

This gives a symmetric split, which is optimal because the largest proper divisor is exactly `5`.

These examples confirm that the algorithm naturally shifts between symmetric and asymmetric splits depending on whether `n` has a small prime factor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) per test | smallest prime factor search up to √n |
| Space | O(1) | only a few variables used |

The constraints allow up to 100 test cases, and each `n` is at most `10^9`. A square root factorization per test case is easily fast enough within time limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def spf(n):
        if n % 2 == 0:
            return 2
        d = 3
        while d * d <= n:
            if n % d == 0:
                return d
            d += 2
        return n

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        p = spf(n)
        g = n // p
        out.append(f"{g} {n - g}")
    return "\n".join(out)

# provided samples
assert solve("4\n2\n9\n5\n10\n") == "1 1\n3 6\n1 4\n5 5"

# minimum case
assert solve("1\n2\n") == "1 1"

# prime n
assert solve("1\n7\n") == "1 6"

# even composite
assert solve("1\n12\n") in ["6 6"]

# power of two
assert solve("1\n16\n") == "8 8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 1 1 | smallest boundary |
| 7 | 1 6 | prime behavior |
| 12 | 6 6 | composite even split |
| 16 | 8 8 | power of two symmetry |

## Edge Cases

For `n = 2`, the algorithm finds smallest prime factor `2`, so `g = 1` and outputs `(1, 1)`, which is the only valid split.

For a prime `n`, say `n = 7`, the smallest prime factor is `7`, so `g = 1` and the result becomes `(1, 6)`. This matches the fact that no non-trivial divisor structure exists, so the solution degenerates to extreme imbalance.

For powers of two like `n = 16`, the smallest prime factor is `2`, so `g = 8`, producing `(8, 8)`. This shows the algorithm naturally detects when symmetric splits are optimal because the largest proper divisor is exactly half of `n`.
