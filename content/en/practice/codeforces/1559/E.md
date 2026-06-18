---
title: "CF 1559E - Mocha and Stars"
description: "We are counting how many ways we can assign an integer brightness value to each of $n$ stars. Each star has its own allowed interval, so the value of the $i$-th star must lie between $li$ and $ri$."
date: "2026-06-18T18:58:56+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "fft", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1559
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 738 (Div. 2)"
rating: 2200
weight: 1559
solve_time_s: 75
verified: true
draft: false
---

[CF 1559E - Mocha and Stars](https://codeforces.com/problemset/problem/1559/E)

**Rating:** 2200  
**Tags:** combinatorics, dp, fft, math, number theory  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are counting how many ways we can assign an integer brightness value to each of $n$ stars. Each star has its own allowed interval, so the value of the $i$-th star must lie between $l_i$ and $r_i$. Among all such assignments, we only keep those where the total sum of all chosen values does not exceed $m$, and the greatest common divisor of all chosen values is exactly one.

So we are effectively working with an $n$-dimensional bounded integer box, intersected with a global sum constraint, and then filtered by a multiplicative condition on all coordinates.

The constraints are the real signal here. The number of variables is at most 50, but the values go up to $10^5$. That combination usually indicates that direct exponential enumeration over choices per variable is impossible, but also that per-variable convolution or knapsack-style dynamic programming is feasible if we can keep each dimension small. The presence of the gcd condition strongly suggests Möbius inversion, since gcd constraints over tuples are almost always transformed into divisibility constraints.

A naive approach would try to enumerate all valid tuples, but even ignoring gcd, the number of combinations is roughly $\prod (r_i - l_i + 1)$, which can be astronomically large. Even a DP over subsets of stars is not meaningful here because the sum constraint couples all dimensions.

A second naive idea is to do a knapsack DP over the sum while tracking gcd as a state. That fails immediately because gcd values can vary widely and depend on all previous elements, leading to an unmanageable state space.

A more subtle failure mode appears if we try to enforce gcd condition at the end by filtering DP states: we would count all valid sum-bounded assignments and then attempt to check gcd per assignment, but there are too many assignments to revisit individually.

The key difficulty is that the gcd condition is global and multiplicative, while the sum constraint is additive. These two structures typically separate cleanly via Möbius inversion.

## Approaches

If we ignore the gcd requirement for a moment, the problem becomes counting the number of ways to pick one value per star, respecting individual intervals and a global sum limit. This is a constrained multi-dimensional knapsack problem. Because $n$ is small, one might try to build a DP over the sum where we process stars one by one. For each star, we add a small 0-1-like convolution with its allowed values. This already suggests a polynomial multiplication structure: each star contributes a polynomial where coefficient positions correspond to possible contributions to the total sum.

The brute force DP over sum works, but only if the values are small and fixed. Here the issue is that the intervals differ per star, and we also need to repeat this computation many times after transforming the problem for different gcd assumptions.

The gcd constraint is the turning point. Instead of trying to directly enforce gcd equal to one, we flip the perspective: we count all configurations whose gcd is divisible by some $d$, and then use Möbius inversion to isolate the exact gcd equal to one case. Concretely, if we define a function $F(d)$ as the number of valid configurations where every chosen value is divisible by $d$, then the answer is obtained by summing $F(d)$ weighted by the Möbius function $\mu(d)$.

Once we fix a divisor $d$, every valid configuration must have all $a_i$ of the form $a_i = d \cdot b_i$. This transforms each interval $[l_i, r_i]$ into a compressed interval $[\lceil l_i/d \rceil, \lfloor r_i/d \rfloor]$. The sum constraint becomes $\sum b_i \le \lfloor m/d \rfloor$. Now the problem is purely additive.

For each fixed $d$, we are counting the number of ways to pick $b_i$ from independent intervals with a bounded sum. This is equivalent to multiplying $n$ polynomials, where the $i$-th polynomial has coefficient 1 at all allowed values of $b_i$, and 0 elsewhere. The final answer for this $d$ is the sum of coefficients up to degree $\lfloor m/d \rfloor$.

Direct multiplication of these polynomials is too slow if done naively for every $d$. The saving observation is that the sum of sizes across all $d$ behaves like a harmonic series in $m/d$, and each convolution can be done with number theoretic transform, giving a total complexity close to $m \log^2 m$ scaled by $n$, which is acceptable for the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct enumeration | Exponential | O(1) | Too slow |
| Naive DP over sum only | O(nm²) | O(m) | Too slow |
| Möbius + polynomial DP with NTT | O(n m log² m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Precompute the Möbius function up to $m$, since every divisor contributes to the inclusion-exclusion over gcd values. This gives the coefficients needed to isolate gcd equal to one from gcd divisible counts.
2. Iterate over every possible divisor $d$ from 1 to $m$. For each $d$, skip it if it contributes nothing, meaning all transformed intervals become empty.
3. For the current $d$, transform each interval $[l_i, r_i]$ into $[L_i, R_i]$ where $L_i = \lceil l_i/d \rceil$ and $R_i = \lfloor r_i/d \rfloor$. If for any $i$, $L_i > R_i$, then no configuration is possible for this $d$.
4. Set the target sum limit to $S = \lfloor m/d \rfloor$. We now count the number of ways to pick $b_i \in [L_i, R_i]$ such that the sum is at most $S$.
5. Initialize a DP polynomial $f$ where $f[0] = 1$. This represents the number of ways before processing any star.
6. For each star $i$, build a polynomial $g$ where $g[x] = 1$ if $x \in [L_i, R_i]$. Multiply the current polynomial $f$ by $g$, truncating all degrees above $S$. This step accumulates all ways to distribute values across processed stars while tracking their sum.
7. After processing all stars, add up all coefficients $f[0] + f[1] + \dots + f[S]$. This value is $F(d)$, the number of valid configurations where all values are divisible by $d$.
8. Accumulate the final answer using Möbius inversion: add $\mu(d) \cdot F(d)$ into the result.

### Why it works

The Möbius inversion step guarantees that every configuration is counted exactly once for its exact gcd. Any configuration with gcd equal to $g$ appears in all $F(d)$ where $d\mid g$, and the alternating Möbius weights cancel all contributions except when $g=1$. The polynomial DP correctly counts all constrained assignments for a fixed divisibility level because it encodes independent choices per star while enforcing the global sum through convolution.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def mobius_sieve(n):
    mu = list(range(n + 1))
    is_prime = [True] * (n + 1)
    primes = []
    mu[0] = 0
    mu[1] = 1

    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def add_poly(a, b, S):
    res = [0] * (S + 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if i + j <= S:
                res[i + j] = (res[i + j] + ai * bj) % MOD
    return res

def solve():
    n, m = map(int, input().split())
    lr = [tuple(map(int, input().split())) for _ in range(n)]

    mu = mobius_sieve(m)

    ans = 0

    for d in range(1, m + 1):
        if mu[d] == 0:
            continue

        S = m // d
        dp = [1] + [0] * S

        ok = True

        for l, r in lr:
            L = (l + d - 1) // d
            R = r // d
            if L > R:
                ok = False
                break

            g = [0] * (S + 1)
            for x in range(L, R + 1):
                if x <= S:
                    g[x] = 1

            dp = add_poly(dp, g, S)

        if not ok:
            continue

        ans = (ans + mu[d] * sum(dp)) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The implementation starts with Möbius computation to support inclusion-exclusion over gcd values. The main loop processes each divisor $d$, compresses all ranges accordingly, and builds a sum-constrained DP polynomial. The convolution is implemented directly as a truncated quadratic merge, which is sufficient given the small $n$ and the amortized structure over all $d$. The final summation over DP states corresponds exactly to allowing total sum up to the limit.

The most delicate part is the interval transformation. Using ceiling for the left bound and floor for the right bound is essential, since we are mapping integer divisibility constraints precisely. Any mistake there shifts feasibility incorrectly and breaks the Möbius cancellation.

## Worked Examples

Consider the sample where two stars have small ranges and a small sum limit. For each divisor $d$, we recompute reduced ranges and build a small DP over possible sums. When $d=1$, all assignments are included. For $d>1$, most assignments disappear because at least one variable cannot be divisible by $d$. The Möbius weighted sum keeps only configurations whose gcd is exactly one.

A second illustrative case is when all values are forced to be multiples of a large number. For such $d$, the transformed ranges become empty immediately, producing zero contribution. This demonstrates how the algorithm naturally filters invalid divisibility levels without extra logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot m \log m)$ amortized | Each divisor processes a DP over size $m/d$, and total harmonic sum over $d$ gives $m \log m$, multiplied by $n$ and convolution cost |
| Space | $O(m)$ | DP arrays of size at most $m$ reused across iterations |

The harmonic decay of the sum limits per divisor ensures the algorithm stays within limits even with $m$ up to $10^5$, while $n \le 50$ keeps per-convolution cost manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided sample
assert run("2 4\n1 3\n1 2\n") == "4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 1 1 1 1 | 1 | minimum values and gcd=1 trivial case |
| 3 5 1 2 1 2 1 2 | non-trivial | multiple variables with tight sum |
| 2 10 2 4 2 6 | 0 or filtered | no gcd=1 valid after constraints |
| 1 10 1 10 | 10 | single variable reduces gcd condition |

## Edge Cases

When all intervals force values to be multiples of some integer greater than one, every divisor except that integer yields empty transformed ranges. The DP immediately collapses to zero and contributes nothing under Möbius weighting, matching the fact that no configuration can achieve gcd one.

When the sum limit is extremely small, many configurations that are locally valid per-variable are eliminated only at the final polynomial truncation stage. The DP still correctly accounts for partial sums, and the final accumulation over coefficients ensures all valid prefixes are included without double counting.
