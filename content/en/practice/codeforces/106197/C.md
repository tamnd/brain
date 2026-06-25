---
title: "CF 106197C - Divisor Lattice"
description: "The problem revolves around the structure formed by all divisors of a given integer when ordered by divisibility."
date: "2026-06-25T10:27:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106197
codeforces_index: "C"
codeforces_contest_name: "Rutgers University Programming Contest Fall 2025 - Open Division"
rating: 0
weight: 106197
solve_time_s: 52
verified: true
draft: false
---

[CF 106197C - Divisor Lattice](https://codeforces.com/problemset/problem/106197/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem revolves around the structure formed by all divisors of a given integer when ordered by divisibility. If you take a number and list every integer that divides it, these divisors naturally form a graph-like structure: each divisor can be connected to “larger” divisors that are obtained by increasing the power of a single prime factor.

More concretely, think of the divisors as points in a grid where each axis corresponds to a prime factor of the number. Each divisor is represented by how many times each prime appears in it. Moving from one divisor to another is only allowed when you increase the exponent of exactly one prime by one step, while keeping all other exponents unchanged. The task is to compute how many such direct “one-step increases” exist in this structure.

The input consists of a single integer, the number whose divisor structure we are analyzing. The output is a single integer representing the number of edges in this divisor graph, where an edge connects two divisors if one can be obtained from the other by multiplying by exactly one prime factor that is still available within the factorization limits.

The main constraint implication is that the number itself can be large enough that enumerating all divisors explicitly is infeasible. Even for moderate values, the number of divisors can grow multiplicatively, and building the full divisor graph would require time proportional to that size. This pushes us toward working directly with the prime factorization instead of enumerating divisors.

A few edge cases expose where naive thinking fails. If the number is prime, for example 13, there are only two divisors, 1 and 13, and exactly one edge between them. A naive approach that assumes more structure might incorrectly count multiple transitions, but only a single prime factor increment is possible.

For a number like 16, which is 2⁴, the divisors are 1, 2, 4, 8, 16. The structure is a simple chain, and there are exactly four edges. Any approach that mistakenly treats divisors as independent combinations rather than exponent increments would miscount the linear structure.

For a mixed number like 12 = 2² · 3¹, the divisor structure is two-dimensional. A naive method that counts only multiplicative choices per divisor but forgets that each state contributes multiple outgoing edges will undercount.

## Approaches

A brute-force approach would explicitly generate all divisors of the number, then for each divisor attempt multiplying by all primes that still keep the result within the original number. This requires enumerating divisors first, which itself takes O(d(n)) time where d(n) is the number of divisors. For each divisor, checking transitions can take up to O(log n), leading to a total cost around O(d(n) log n). In worst cases, such as highly composite numbers, d(n) grows large enough that this becomes infeasible.

The key structural insight is that the divisor set is not arbitrary. Once the number is written in prime factorization form, every divisor corresponds to a choice of exponents for each prime. The graph edges are exactly the increments of these exponent vectors. Instead of constructing the graph, we can count transitions combinatorially.

For a prime factor pᵢ with exponent aᵢ, every divisor can increase its exponent in pᵢ from 0 up to aᵢ − 1. For each such choice, the other primes remain fixed, contributing independent combinations. This turns the problem into summing contributions over dimensions of a Cartesian product, removing any need for explicit enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d(n) log n) | O(d(n)) | Too slow |
| Optimal | O(√n + k²) (or Pollard Rho factorization) | O(k) | Accepted |

Here k is the number of distinct prime factors.

## Algorithm Walkthrough

1. Factorize the input number into its prime powers n = p₁ᵃ¹ · p₂ᵃ² · ... · p_kᵃᵏ.

This is necessary because the entire structure of divisors depends only on these exponents.
2. For each prime factor pᵢ, compute its contribution to edges as aᵢ multiplied by the number of ways to choose exponents for all other primes, which is Π_{j ≠ i} (aⱼ + 1).

This corresponds to fixing a divisor state and counting how many times we can increment the exponent of pᵢ.
3. Accumulate the sum of these contributions over all prime factors.
4. Output the final sum.

The reason step 2 is valid is that each edge corresponds uniquely to choosing a divisor and a prime whose exponent is not yet at its maximum. Every such choice corresponds to exactly one valid adjacent divisor, and no edge is counted twice because the increasing prime exponent uniquely identifies the transition.

### Why it works

Each divisor is fully determined by an exponent vector (x₁, x₂, ..., x_k). An edge exists when we move from one vector to another by increasing exactly one coordinate by 1 while staying within bounds. For a fixed coordinate i, every valid starting vector has xᵢ in [0, aᵢ − 1], and all other coordinates are free within their ranges. This creates exactly aᵢ · Π_{j≠i}(aⱼ+1) valid edges for dimension i. Summing over all dimensions covers every possible edge exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def factorize(n: int):
    res = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            res[d] = res.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        res[n] = res.get(n, 0) + 1
    return res

def solve():
    n = int(input().strip())
    pf = factorize(n)

    exps = list(pf.values())
    k = len(exps)

    ans = 0
    for i in range(k):
        contrib = exps[i]
        for j in range(k):
            if i != j:
                contrib *= (exps[j] + 1)
        ans += contrib

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by factorizing the number using trial division. This is sufficient under the assumption that the input size is moderate; for larger constraints, a faster factorization method would replace this step without changing the rest of the logic.

Once the exponents are extracted, the code directly implements the combinational formula. For each prime exponent, it computes the product of (aⱼ + 1) over all other primes, then multiplies by aᵢ. This mirrors the count of ways to choose a valid divisor state where that prime can still be incremented.

A subtle point is that we never construct divisors or edges explicitly. All counting happens in exponent space, which avoids combinatorial explosion.

## Worked Examples

### Example 1: n = 12

Here 12 = 2² · 3¹, so exponents are [2, 1].

| Step | Prime index i | Contribution formula | Value |
| --- | --- | --- | --- |
| 1 | 2 | 2 * (1 + 1) | 4 |
| 2 | 3 | 1 * (2 + 1) | 3 |

Total answer = 7.

This trace shows how each prime dimension contributes independently, and how the other dimension acts as a multiplicative choice factor.

### Example 2: n = 16

Here 16 = 2⁴, so exponents are [4].

| Step | Prime index i | Contribution formula | Value |
| --- | --- | --- | --- |
| 1 | 2 | 4 | 4 |

Total answer = 4.

This confirms the degenerate one-dimensional case where the divisor lattice becomes a simple chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n + k²) | trial division factorization plus pairwise exponent aggregation |
| Space | O(k) | storage of prime exponents |

The computation is dominated by factorization. After that, the exponent-based aggregation is constant-time per pair of prime factors, which is negligible for typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def factorize(n: int):
        res = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                res[d] = res.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            res[n] = res.get(n, 0) + 1
        return res

    def solve():
        n = int(sys.stdin.readline().strip())
        pf = factorize(n)
        exps = list(pf.values())

        ans = 0
        for i in range(len(exps)):
            cur = exps[i]
            for j in range(len(exps)):
                if i != j:
                    cur *= (exps[j] + 1)
            ans += cur
        return str(ans)

    return solve()

# custom cases
assert run("1") == "0", "edge: no edges"
assert run("2") == "1", "prime case"
assert run("12") == "7", "two-dimensional lattice"
assert run("16") == "4", "single chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | minimal input, no divisors beyond itself |
| 2 | 1 | prime factorization edge case |
| 12 | 7 | interaction between two primes |
| 16 | 4 | single prime power chain |

## Edge Cases

For n = 1, the factorization is empty, so there are no exponent dimensions. The algorithm produces an empty sum and correctly returns 0, matching the fact that the divisor lattice has a single node and no edges.

For a prime number like 17, the factorization has one exponent [1]. The only contribution is 1, which corresponds to the single edge between 1 and 17. The loop handles this cleanly without special cases.

For a number like 2³ · 3², the algorithm explicitly counts contributions from both dimensions. When focusing on 2, there are 3 choices of exponent for 2 transitions and 3 choices for the 3-dimension, giving 3 · 3 = 9 edges contributed by 2. Symmetrically, the 3-dimension contributes 2 · 4 = 8 edges. The sum captures the full grid of transitions without overlap because each edge is uniquely identified by which coordinate changes.
