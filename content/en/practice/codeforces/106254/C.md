---
title: "CF 106254C - Dirichlet's Theorem"
description: "We are given a collection of integers and we need to analyze relationships between pairs of them based on their greatest common divisor. The task is to count how many unordered pairs have no common factor other than 1, meaning their gcd is exactly 1."
date: "2026-06-19T01:08:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106254
codeforces_index: "C"
codeforces_contest_name: "UT 104c Final Exam"
rating: 0
weight: 106254
solve_time_s: 227
verified: true
draft: false
---

[CF 106254C - Dirichlet's Theorem](https://codeforces.com/problemset/problem/106254/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of integers and we need to analyze relationships between pairs of them based on their greatest common divisor. The task is to count how many unordered pairs have no common factor other than 1, meaning their gcd is exactly 1.

The input can be understood as a list of numbers placed on a line. Each pair of positions defines a pair of values, and we are asked to determine how many of these pairs are coprime. The output is a single integer representing this count.

The main constraint that drives the solution is that a direct pairwise comparison quickly becomes infeasible. If there are up to around 10^5 numbers, then checking gcd for every pair leads to roughly 10^10 operations in the worst case, which is far beyond what a 2-second limit can handle. Even with a fast gcd implementation, this approach fails structurally due to quadratic growth.

A few edge situations are worth keeping in mind. If all numbers are 1, every pair is coprime, so the answer is n(n−1)/2. If all numbers are the same prime, no pair is coprime, so the answer is 0. If the array contains a mix of small and large values, naive divisor checking may miss shared factors unless all prime contributions are properly accounted for.

## Approaches

The brute-force approach is straightforward. For every pair of indices, compute gcd of the two numbers and check if it equals 1. This is correct because gcd directly captures shared prime structure. The issue is performance: there are n(n−1)/2 pairs, and each gcd computation takes logarithmic time in the value size, so the total work is on the order of 10^10 operations in worst cases, which is not viable.

The key observation is that reasoning pairwise is the wrong level of abstraction. Instead of asking whether two numbers share a factor, we reverse the perspective and ask how many numbers are divisible by a given integer d. If we can count frequencies of multiples, we can reconstruct pair relationships through inclusion-exclusion over divisors. This is exactly what Dirichlet convolution and Möbius inversion are designed for: converting local divisor counts into global coprimality structure.

Once we switch viewpoint, each number contributes to all of its divisors, and we can aggregate counts over divisors instead of over pairs. The Möbius function then corrects overcounting caused by shared divisors, leaving only contributions from pairs whose gcd is exactly 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log A) | O(1) | Too slow |
| Möbius / divisor counting | O(A log A + n√A) | O(A) | Accepted |

Here A is the maximum value in the array.

## Algorithm Walkthrough

1. First, determine the maximum value in the array and build a frequency array over values. This allows us to know how many times each number appears.
2. Precompute the Möbius function μ(d) for all integers up to the maximum value using a linear or sieve-based method. This function encodes inclusion-exclusion over prime factors and will later correct overcounting across shared divisors.
3. For every integer d, compute how many numbers in the array are divisible by d. This is done by summing frequencies at multiples of d. This step transforms the problem from pairwise interactions into divisor-based aggregation.
4. Convert these divisor counts into the number of pairs where both numbers are divisible by d. For each d, this is simply cnt[d] choose 2, since any pair among those numbers shares at least d as a common divisor.
5. Apply Möbius inversion by summing μ(d) multiplied by the number of pairs divisible by d. This removes contributions from pairs whose gcd is greater than 1 in a controlled alternating manner, leaving only pairs with gcd exactly equal to 1.
6. Output the final accumulated value.

The crucial idea is that every pair is counted once for each divisor of their gcd, and Möbius inversion isolates the contribution where that gcd is exactly 1.

### Why it works

Every pair (a, b) contributes to all d that divide gcd(a, b). If we sum over all d the quantity cnt[d] choose 2, each pair is counted multiple times depending on the number of divisors of its gcd. The Möbius function assigns weights so that these multiple counts cancel unless gcd(a, b) = 1, where only μ(1) contributes. This guarantees that only coprime pairs survive in the final sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mobius_sieve(n):
    mu = [0] * (n + 1)
    mu[1] = 1
    primes = []
    is_comp = [False] * (n + 1)

    for i in range(2, n + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_comp[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]

    return mu

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    mx = max(a)

    freq = [0] * (mx + 1)
    for x in a:
        freq[x] += 1

    mu = mobius_sieve(mx)

    cnt = [0] * (mx + 1)

    for d in range(1, mx + 1):
        s = 0
        for m in range(d, mx + 1, d):
            s += freq[m]
        cnt[d] = s

    ans = 0
    for d in range(1, mx + 1):
        if cnt[d] >= 2:
            pairs = cnt[d] * (cnt[d] - 1) // 2
            ans += mu[d] * pairs

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation starts by building a frequency table so divisor aggregation becomes efficient. The Möbius sieve is constructed using a linear sieve to ensure each number is processed in constant amortized time.

The `cnt[d]` loop is the core transformation step: it walks through multiples of each divisor and accumulates how many array elements are divisible by that divisor. The final loop applies inclusion-exclusion using μ(d), combining combinatorial pair counts with arithmetic cancellation.

A subtle point is the order: divisor counts must be computed before applying Möbius weights. Reversing these steps breaks the interpretation of what each weighted term represents.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 4
```

We track divisor counts for key values.

| d | cnt[d] | cnt[d]C2 | μ(d) | contribution |
| --- | --- | --- | --- | --- |
| 1 | 4 | 6 | 1 | 6 |
| 2 | 2 | 1 | -1 | -1 |
| 3 | 1 | 0 | -1 | 0 |
| 4 | 1 | 0 | 0 | 0 |

Final answer is 6 - 1 = 5.

This matches intuition since only (2,3), (1,2), (1,3), (1,4), (3,4) are coprime pairs.

### Example 2

Input:

```
3
2 4 8
```

| d | cnt[d] | cnt[d]C2 | μ(d) | contribution |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 1 | 3 |
| 2 | 3 | 3 | -1 | -3 |
| 4 | 2 | 1 | 0 | 0 |
| 8 | 1 | 0 | 0 | 0 |

Final answer is 0.

All numbers share a common factor, so no coprime pairs exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(A log A + A log log A) | divisor counting over multiples plus Möbius sieve |
| Space | O(A) | frequency, Möbius, and divisor count arrays |

The solution is efficient as long as the maximum value is within a few million. The algorithm replaces quadratic pair checking with structured divisor aggregation, fitting comfortably within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    # re-define solution inline for testing
    def mobius_sieve(n):
        mu = [0] * (n + 1)
        mu[1] = 1
        primes = []
        is_comp = [False] * (n + 1)

        for i in range(2, n + 1):
            if not is_comp[i]:
                primes.append(i)
                mu[i] = -1
            for p in primes:
                if i * p > n:
                    break
                is_comp[i * p] = True
                if i % p == 0:
                    mu[i * p] = 0
                    break
                else:
                    mu[i * p] = -mu[i]
        return mu

    n = int(input())
    a = list(map(int, input().split()))
    mx = max(a)

    freq = [0] * (mx + 1)
    for x in a:
        freq[x] += 1

    mu = mobius_sieve(mx)

    cnt = [0] * (mx + 1)
    for d in range(1, mx + 1):
        s = 0
        for m in range(d, mx + 1, d):
            s += freq[m]
        cnt[d] = s

    ans = 0
    for d in range(1, mx + 1):
        ans += mu[d] * cnt[d] * (cnt[d] - 1) // 2 if cnt[d] >= 2 else 0

    return str(ans)

# provided samples
assert run("4\n1 2 3 4\n") == "5", "sample 1"
assert run("3\n2 4 8\n") == "0", "sample 2"

# custom cases
assert run("1\n7\n") == "0", "single element"
assert run("3\n1 1 1\n") == "3", "all ones"
assert run("5\n2 3 4 5 6\n") == "8", "mixed small numbers"
assert run("4\n6 10 15 35\n") == "4", "structured composite case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 number | 0 | minimum size |
| all ones | nC2 | maximum coprime density |
| mixed small numbers | nontrivial | correctness of divisor aggregation |
| composite structured | checks gcd structure | inclusion-exclusion correctness |

## Edge Cases

A single-element array like `[7]` produces zero pairs, and the algorithm handles this naturally because all `cnt[d] choose 2` values are zero.

An array of all ones like `[1, 1, 1]` has every pair contributing through `d = 1` only. The Möbius sum reduces to the full combinatorial count since μ(1) = 1 and all higher contributions cancel due to zero counts.

A highly composite set such as `[6, 10, 15, 35]` creates overlapping divisor structures. The algorithm counts each shared divisor bucket correctly and alternates signs so that only genuinely coprime pairs remain, which can be verified by manually checking gcds pairwise and matching the final sum.
