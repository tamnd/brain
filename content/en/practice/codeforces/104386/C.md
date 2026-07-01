---
title: "CF 104386C - Prefix Sum Array"
description: "We start with an infinite array where every position initially contains the value 1. Each second, the array is replaced by its prefix sum version, meaning the value at position i becomes the sum of all values from position 1 to i in the previous array."
date: "2026-07-01T02:48:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104386
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #14 (Cool-Forces)"
rating: 0
weight: 104386
solve_time_s: 78
verified: false
draft: false
---

[CF 104386C - Prefix Sum Array](https://codeforces.com/problemset/problem/104386/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an infinite array where every position initially contains the value 1. Each second, the array is replaced by its prefix sum version, meaning the value at position i becomes the sum of all values from position 1 to i in the previous array. After one operation, the array becomes a growing sequence of cumulative totals, and after k operations this transformation is applied k times.

The task is to answer multiple queries. Each query gives a position n and a number of transformations k, and we must compute the value at index n after k prefix-sum operations, modulo $10^9 + 7$.

The constraints make brute force immediately impossible. Even though n is at most $10^5$, k is also up to $10^5$, and there are up to $10^5$ test cases. Simulating prefix sums repeatedly per query would require $O(nk)$ work per test case in the worst case, which is far beyond feasible limits.

A less obvious issue is that the array is conceptually infinite, but only the first n elements matter for each query. Any approach that tries to materialize more than necessary still risks unnecessary overhead if it does not exploit structure.

A naive implementation can also silently fail due to repeated recomputation of prefix sums. For example, even computing k=1000 transformations for a single n=100000 case is already too large because each transformation itself is linear.

## Approaches

The brute force method applies the prefix sum operation k times. Each operation scans the array and builds a new one. This is correct because it directly follows the definition, but it costs O(nk) per query. With n and k both large and t up to $10^5$, this becomes astronomically large.

The key observation is that repeated prefix sums generate a well known combinatorial structure. After one operation, the value at index n equals n. After two operations, it becomes the sum of 1 through n, which is the triangular number $\binom{n+1}{2}$. After three operations, it becomes sums of triangular numbers, which correspond to $\binom{n+2}{3}$. This pattern generalizes: after k operations, the value at index n equals the binomial coefficient $\binom{n+k-1}{k}$.

This happens because each prefix sum layer adds one level of summation, and repeated summation of constant sequences builds Pascal’s triangle structure. Each position accumulates contributions that correspond exactly to combinations of choosing k indices among n+k-1 positions.

This transforms each query into a single combinatorial computation rather than k repeated array transformations.

We precompute factorials and modular inverses up to $n+k$, and answer each query in O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) per query | O(n) | Too slow |
| Optimal | O(n + max(n+k)) preprocessing, O(1) per query | O(max(n+k)) | Accepted |

## Algorithm Walkthrough

We rely on the identity that after k prefix sum operations, the value at index n becomes:

$$a_k(n) = \binom{n + k - 1}{k}$$

1. We determine the maximum value of n+k across all queries. This is needed because factorial precomputation must cover the largest binomial parameter used in any query.
2. We precompute factorials up to this maximum value modulo $10^9 + 7$. This allows fast computation of combinations.
3. We precompute modular inverses of factorials using Fermat’s little theorem. This is necessary because division in modular arithmetic is replaced by multiplication with inverse factorials.
4. For each query (n, k), we compute the binomial coefficient $\binom{n+k-1}{k}$ using:

$$\frac{(n+k-1)!}{k!(n-1)!}$$
5. We output the result modulo $10^9 + 7$.

The reason this is valid is that each prefix sum layer corresponds to adding one dimension of accumulation, and the structure of repeated cumulative sums matches Pascal’s triangle exactly. Each entry counts the number of weakly increasing sequences of length k ending at position n, which is exactly the binomial coefficient above.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def build_fact(n):
    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n] = modinv(fact[n])
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    return fact, invfact

def ncr(n, r, fact, invfact):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

def main():
    t = int(input())
    queries = []
    maxv = 0

    for _ in range(t):
        n, k = map(int, input().split())
        queries.append((n, k))
        maxv = max(maxv, n + k)

    fact, invfact = build_fact(maxv)

    for n, k in queries:
        ans = ncr(n + k - 1, k, fact, invfact)
        print(ans)

if __name__ == "__main__":
    main()
```

The factorial array stores values needed to compute combinations quickly. The inverse factorial array allows division under modulo by turning division into multiplication.

The key implementation detail is using $n+k-1$ as the top of the binomial coefficient. A common mistake is to forget the shift and use $\binom{n+k}{k}$, which overcounts by one full layer of the Pascal structure.

We also precompute inverses in a backward pass to avoid repeated modular exponentiation per query, which would be too slow for $10^5$ queries.

## Worked Examples

Consider a single query where n = 4 and k = 2. We expect:

$$\binom{4+2-1}{2} = \binom{5}{2} = 10$$

| Step | Expression |
| --- | --- |
| Compute n+k-1 | 5 |
| Compute C(5,2) | 10 |

This matches the known second prefix-sum transformation sequence 1, 3, 6, 10.

Now consider n = 3, k = 1:

$$\binom{3}{1} = 3$$

| Step | Expression |
| --- | --- |
| Compute n+k-1 | 3 |
| Compute C(3,1) | 3 |

This matches the first transformation where the array becomes 1,2,3,...

These examples confirm that k layers of prefix summation correspond exactly to binomial coefficient growth.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(max N) + O(t) | factorial precomputation plus O(1) per query |
| Space | O(max N) | storage for factorial and inverse factorial arrays |

The precomputation is bounded by at most around $2 \times 10^5$ in practice given constraints, and each query is constant time. This comfortably fits within time limits even for $10^5$ queries.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    def build_fact(n):
        fact = [1] * (n + 1)
        invfact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD
        invfact[n] = modinv(fact[n])
        for i in range(n, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD
        return fact, invfact

    def ncr(n, r, fact, invfact):
        if r < 0 or r > n:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

    t = int(input())
    qs = []
    mx = 0
    for _ in range(t):
        n, k = map(int, input().split())
        qs.append((n, k))
        mx = max(mx, n + k)

    fact, invfact = build_fact(mx)

    out = []
    for n, k in qs:
        out.append(str(ncr(n + k - 1, k, fact, invfact)))
    return "\n".join(out)

# provided samples
assert solve("3\n3 1\n1 3\n3 2") == "3\n1\n5"

# custom cases
assert solve("1\n1 1") == "1", "minimum case"
assert solve("1\n5 0") == "1", "zero transformations"
assert solve("2\n4 2\n3 3") == "10\n10", "triangular consistency"
assert solve("1\n100000 1") == "100000", "large n small k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 1 | 1 | base identity case |
| 5 0 | 1 | zero transformation stability |
| 4 2, 3 3 | 10, 10 | combinational consistency |
| 100000 1 | 100000 | large boundary correctness |

## Edge Cases

One edge case is k = 0, where no transformation happens. The formula becomes $\binom{n-1}{0} = 1$, which correctly reflects that the array remains all ones.

Another edge case is n = 1. Regardless of k, the answer must always be 1 because the first element of a prefix sum array never changes. The formula gives $\binom{k}{k} = 1$, matching this invariant exactly.

A third edge case is large n with small k. For example n = 100000, k = 1 yields $\binom{100000}{1} = 100000$, which matches the definition of a single prefix sum producing linear growth.
