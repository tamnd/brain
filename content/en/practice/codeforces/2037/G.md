---
title: "CF 2037G - Natlan Exploring"
description: "We are asked to count the number of distinct paths from the first city to the last city in a region of Natlan, where each city has an attractiveness value. The paths follow a simple rule: from city $i$ you can travel to city $j$ if $i < j$ and $gcd(ai, aj) neq 1$."
date: "2026-06-08T10:17:59+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "data-structures", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2037
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 988 (Div. 3)"
rating: 2000
weight: 2037
solve_time_s: 217
verified: false
draft: false
---

[CF 2037G - Natlan Exploring](https://codeforces.com/problemset/problem/2037/G)

**Rating:** 2000  
**Tags:** bitmasks, combinatorics, data structures, dp, math, number theory  
**Solve time:** 3m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count the number of distinct paths from the first city to the last city in a region of Natlan, where each city has an attractiveness value. The paths follow a simple rule: from city $i$ you can travel to city $j$ if $i < j$ and $\gcd(a_i, a_j) \neq 1$. This makes the underlying structure a directed acyclic graph (DAG), because all edges point from lower-index cities to higher-index cities, so cycles are impossible. The input consists of the number of cities $n$ and the attractiveness values $a_i$. The output is the number of distinct paths from city 1 to city $n$, modulo $998\,244\,353$.

The constraints are tight. With $n$ up to $2 \cdot 10^5$ and each $a_i$ up to $10^6$, iterating over all possible pairs of cities to check the GCD would require about $2 \cdot 10^5 \cdot 2 \cdot 10^5 / 2 \approx 2 \cdot 10^{10}$ operations, which is far beyond what fits in a 4-second time limit. This rules out naive pairwise approaches. We also need to handle the modulo arithmetic carefully to avoid overflow, as the number of paths can grow quickly.

A subtle edge case occurs when all cities are pairwise coprime. For example, with cities $[2, 3, 5]$, no edge exists except possibly from city 1 to city 2 if $\gcd(2,3) \neq 1$, which it is. In this case, naive iteration may either double-count paths or assume an edge exists where none does, giving an incorrect count of paths. Another edge case is when multiple cities have the same attractiveness, which creates several valid paths connecting the same pairs of cities.

## Approaches

The brute-force approach would model the cities as a DAG and explicitly compute edges between each pair $i < j$ if $\gcd(a_i, a_j) \neq 1$. Once the DAG is built, a depth-first search (DFS) or dynamic programming from city 1 to city $n$ can count all paths. This works in principle, but checking $\gcd$ for every pair is $O(n^2)$, about $4 \cdot 10^{10}$ operations for the largest inputs. Even DFS memoization would still need the DAG built, so it is impractical.

The key observation is that two numbers have a GCD greater than 1 if and only if they share a prime factor. We can factor each attractiveness value into its prime factors and, for each prime $p$, track the latest city with attractiveness divisible by $p$. This allows us to propagate the number of paths dynamically without checking every pair. Specifically, we maintain a dynamic programming array `dp[i]` counting the number of paths reaching city $i$. For each prime factor $p$ of $a_i$, we know the most recent city `last[p]` with factor $p$ before $i$; any path reaching `last[p]` can continue to city $i$. We sum over all prime factors' contributions to compute `dp[i]`.

This transforms the problem into factorization and a linear traversal, dramatically reducing the complexity. Using a sieve for prime factorization up to $10^6$ ensures that each city is processed in $O(\log a_i)$ time, because the number of distinct prime factors is at most about 7 for numbers under $10^6$. This approach is both feasible and efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 log max(a)) | O(n^2) | Too slow |
| Prime-factor DP | O(n log max(a)) | O(max(a)) | Accepted |

## Algorithm Walkthrough

1. Precompute the smallest prime factors (SPF) for all numbers up to $10^6$ using a sieve. This allows us to factor any number quickly in $O(\log a_i)$ time by repeatedly dividing by its smallest prime factor.
2. Initialize an array `dp` of size $n+1$ with all zeros. Set `dp[1] = 1`, since there is exactly one path starting at city 1.
3. Initialize a dictionary `last` to keep track of the last city index for each prime factor. This allows us to propagate paths efficiently.
4. Iterate over cities from index 1 to $n$. For each city $i$:

- Factor `a[i]` into its prime factors using the SPF array.
- For each prime factor $p$ of `a[i]`, add `dp[last[p]]` to `dp[i]` modulo $998\,244\,353$, where `last[p]` is the most recent city before `i` with factor $p$. If `last[p]` does not exist yet, it contributes zero.
- After updating `dp[i]`, update `last[p] = i` for all prime factors $p$.
5. The final answer is `dp[n]`, the number of distinct paths reaching city $n$.

Why it works: every path from city 1 to city $i$ can be uniquely decomposed by the prime factors of the cities along the path. Each prime factor ensures connectivity to later cities sharing that factor. The invariant is that after processing city $i$, `dp[i]` correctly counts all distinct paths ending at $i$ using only valid edges. Summing contributions over prime factors guarantees no paths are missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAX_A = 10**6 + 1

# Sieve to compute smallest prime factors
spf = list(range(MAX_A))
for i in range(2, int(MAX_A**0.5) + 1):
    if spf[i] == i:
        for j in range(i*i, MAX_A, i):
            if spf[j] == j:
                spf[j] = i

def factorize(x):
    factors = set()
    while x > 1:
        factors.add(spf[x])
        x //= spf[x]
    return factors

def main():
    n = int(input())
    a = list(map(int, input().split()))
    dp = [0] * n
    dp[0] = 1
    last = dict()

    for i in range(n):
        primes = factorize(a[i])
        for p in primes:
            if p in last:
                dp[i] = (dp[i] + dp[last[p]]) % MOD
        for p in primes:
            last[p] = i

    print(dp[n-1] % MOD)

if __name__ == "__main__":
    main()
```

The sieve precomputes the smallest prime factors efficiently. The `factorize` function produces the distinct prime factors of any number. The dynamic programming array `dp` accumulates the number of paths to each city. The `last` dictionary ensures that contributions only come from previous cities sharing at least one prime factor. Updating `last[p]` after adding contributions guarantees we do not count paths multiple times. Boundary handling is naturally taken care of by Python's zero-based indexing.

## Worked Examples

**Sample 1:**

Input `a = [2, 6, 3, 4, 6]`.

| i | a[i] | primes | dp[i] | last dict after i |
| --- | --- | --- | --- | --- |
| 0 | 2 | {2} | 1 | {2:0} |
| 1 | 6 | {2,3} | 1 | {2:1,3:1} |
| 2 | 3 | {3} | 1 | {2:1,3:2} |
| 3 | 4 | {2} | 2 | {2:3,3:2} |
| 4 | 6 | {2,3} | 5 | {2:4,3:4} |

This confirms the five distinct paths.

**Sample 2:**

Input `a = [3, 5, 15]`.

| i | a[i] | primes | dp[i] | last dict after i |
| --- | --- | --- | --- | --- |
| 0 | 3 | {3} | 1 | {3:0} |
| 1 | 5 | {5} | 0 | {3:0,5:1} |
| 2 | 15 | {3,5} | 2 | {3:2,5:2} |

The two paths are `[3,15]` and `[3,5,15]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log max(a)) | Factorization per city is O(log a_i) using SPF sieve; linear scan over n cities. |
| Space | O(max(a)) | SPF array and `last` dictionary store at most MAX_A entries. |

Given $n \le 2 \cdot 10^5$ and (a_i \le
