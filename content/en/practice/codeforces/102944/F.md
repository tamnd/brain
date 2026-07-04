---
title: "CF 102944F - Flint"
description: "We are given a small collection of positive integers. From this collection, we consider every possible non-empty subset and compute the greatest common divisor of the numbers inside that subset. A subset is considered “valid” if this gcd equals exactly 1."
date: "2026-07-04T07:36:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102944
codeforces_index: "F"
codeforces_contest_name: "UMPT 2020-2021 Team Tryout Contest"
rating: 0
weight: 102944
solve_time_s: 40
verified: true
draft: false
---

[CF 102944F - Flint](https://codeforces.com/problemset/problem/102944/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small collection of positive integers. From this collection, we consider every possible non-empty subset and compute the greatest common divisor of the numbers inside that subset. A subset is considered “valid” if this gcd equals exactly 1. The task is to count how many such valid subsets exist.

The input size is small, with at most 100 numbers, but each number can be as large as 10^9. The size constraint is the key signal: enumerating all subsets is possible in principle since 2^100 is too large, but 100 is small enough to allow exponential methods with compression or inclusion-exclusion over values derived from the numbers, especially divisors.

A naive interpretation would try to iterate over all subsets and compute gcd directly. That already suggests the core difficulty: the subset space is exponential, but the gcd operation has structure that can be exploited.

A subtle edge case appears when all numbers share a common factor greater than 1. For example, if all numbers are even, then every subset has gcd at least 2, so the answer must be 0. Any approach that does not properly enforce gcd collapsing behavior will incorrectly count subsets that never actually reach 1.

Another corner case occurs when the array contains a single element equal to 1. The only subset is {1}, whose gcd is 1, so the answer is 1. This is the minimal sanity check that any method must satisfy.

## Approaches

The brute-force idea is straightforward. We iterate over every non-empty subset of the array, compute its gcd by folding through its elements, and increment the answer if the result equals 1. This is correct because it directly follows the definition of the problem.

However, the number of subsets is 2^N. With N = 100, this is around 10^30 subsets, which is far beyond any computational limit. Even if gcd computation is fast, the sheer number of subsets makes this approach impossible.

The key observation is that gcd structure interacts well with divisors rather than subsets. Instead of grouping subsets by their gcd value after construction, we reverse the perspective: fix a value d and count how many subsets have all elements divisible by d. Any such subset has gcd divisible by d, and if we carefully account for overcounting, we can recover the exact number of subsets with gcd exactly equal to d. This is a standard inclusion-exclusion over divisors idea, but here it becomes especially clean because N is small and values are large.

We proceed by counting, for each integer d, how many array elements are divisible by d. If k elements are divisible by d, then there are 2^k - 1 non-empty subsets composed only of multiples of d. Let f(d) denote this count. However, f(d) counts all subsets whose gcd is a multiple of d, not exactly equal to d. We then subtract contributions of multiples of d using a descending sieve over divisors, producing the exact number of subsets whose gcd is exactly d.

Finally, we sum the value corresponding to d = 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N · 2^N) | O(1) | Too slow |
| Divisor DP + Inclusion-Exclusion | O(N √A + D log D) | O(D) | Accepted |

Here D is the number of distinct divisors appearing among the input values, which is small because we only generate divisors of each number.

## Algorithm Walkthrough

We avoid enumerating subsets entirely and instead count by divisor classes.

1. For each number in the array, enumerate all of its divisors. For every divisor d, increase a frequency counter cnt[d] by 1. This step builds a mapping from a divisor to how many array elements are divisible by it. The reason this works is that any subset whose elements are all divisible by d is formed only from these cnt[d] elements.
2. For every divisor d that appears in cnt, compute the number of non-empty subsets formed from those elements, which is f(d) = 2^{cnt[d]} - 1. This represents all subsets whose elements are all multiples of d, meaning their gcd is at least d.
3. Sort all divisors in descending order. We want to remove overcounting from multiples. If a subset has gcd exactly equal to a larger multiple of d, it was incorrectly included in f(d), so we subtract those contributions.
4. Process divisors in decreasing order. Maintain an array g[d] initially set to f(d). For each d, iterate over all multiples m = 2d, 3d, ..., and subtract g[m] from g[d]. This ensures that after processing, g[d] represents subsets whose gcd is exactly d.
5. The final answer is g[1].

### Why it works

Each non-empty subset has a unique gcd value. For any fixed d, f(d) counts all subsets whose gcd is a multiple of d. These subsets are partitioned by their exact gcd values, all of which are multiples of d. The subtraction step is effectively Möbius inversion over the divisor lattice, ensuring each subset is assigned exactly once to its true gcd value. Because the divisor relation forms a partial order, processing from large to small guarantees that when we subtract, all larger contributions are already finalized.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def get_divisors(x):
    divs = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            divs.append(i)
            if i * i != x:
                divs.append(x // i)
        i += 1
    return divs

def modpow(a, e):
    res = 1
    while e:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

n = int(input())
a = list(map(int, input().split()))

cnt = {}
for x in a:
    for d in get_divisors(x):
        cnt[d] = cnt.get(d, 0) + 1

vals = sorted(cnt.keys(), reverse=True)

f = {}
g = {}

for d in vals:
    c = cnt[d]
    f[d] = (modpow(2, c) - 1) % MOD
    g[d] = f[d]

for d in vals:
    for m in vals:
        if m > d and m % d == 0:
            g[d] = (g[d] - g[m]) % MOD

print(g.get(1, 0) % MOD)
```

The solution begins by building divisor frequencies. For each number, we enumerate its divisors in O(√aᵢ), which is sufficient for aᵢ up to 10^9. This is the only step that touches raw input values directly.

Next, we compute 2^k - 1 for each divisor count. This represents all subsets composed exclusively of numbers divisible by that divisor. The modular exponentiation is necessary because k can be up to 100.

Finally, we correct overcounting by subtracting contributions of larger gcd values. The nested loop over divisors is acceptable because the number of distinct divisors across all numbers remains small in practice under these constraints.

## Worked Examples

### Example 1

Input:

```
3
2 3 5
```

Every number is prime and distinct, so only singleton subsets matter for gcd 1.

| Step | cnt | f(d) | g(d) |
| --- | --- | --- | --- |
| d=5 | 1 | 1 | 1 |
| d=3 | 1 | 1 | 1 |
| d=2 | 1 | 1 | 1 |
| d=1 | 3 | 7 | 4 |

The final value g(1) = 4 corresponds to all subsets except those whose gcd is not 1. The valid subsets are all except the empty set and any subset whose gcd is >1.

This trace shows how inclusion-exclusion separates gcd classes even when all numbers are pairwise coprime.

### Example 2

Input:

```
3
2 4 8
```

All numbers are powers of 2, so no subset can have gcd 1.

| Step | cnt | f(d) | g(d) |
| --- | --- | --- | --- |
| d=8 | 1 | 1 | 1 |
| d=4 | 2 | 3 | 2 |
| d=2 | 3 | 7 | 4 |
| d=1 | 3 | 7 | 0 |

Here every subset is counted under some power-of-2 gcd class, and everything cancels out at d = 1, confirming that no subset reaches gcd 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N √A + D²) | divisor enumeration plus divisor-multiple corrections |
| Space | O(D) | storage for divisor counts and DP tables |

The constraints N ≤ 100 keep divisor enumeration trivial, and D remains manageable because each number contributes at most about 100 divisors. This makes the solution comfortably fit within limits.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def get_divisors(x):
        divs = []
        i = 1
        while i * i <= x:
            if x % i == 0:
                divs.append(i)
                if i * i != x:
                    divs.append(x // i)
            i += 1
        return divs

    def modpow(a, e):
        res = 1
        while e:
            if e & 1:
                res = (res * a) % MOD
            a = (a * a) % MOD
            e >>= 1
        return res

    n = int(input())
    a = list(map(int, input().split()))

    cnt = {}
    for x in a:
        for d in get_divisors(x):
            cnt[d] = cnt.get(d, 0) + 1

    vals = sorted(cnt.keys(), reverse=True)

    f = {}
    g = {}

    for d in vals:
        f[d] = (modpow(2, cnt[d]) - 1) % MOD
        g[d] = f[d]

    for d in vals:
        for m in vals:
            if m > d and m % d == 0:
                g[d] = (g[d] - g[m]) % MOD

    return str(g.get(1, 0) % MOD)

# sample-like
assert run("3\n2 3 5\n") == "4"

# single element 1
assert run("1\n1\n") == "1"

# all same even number
assert run("3\n2 2 2\n") == "0"

# powers of two
assert run("3\n2 4 8\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2 3 5 | 4 | basic inclusion-exclusion correctness |
| 1 1 | 1 | minimal edge case |
| 3 2 2 2 | 0 | shared gcd > 1 eliminates valid subsets |
| 3 2 4 8 | 0 | no subset can reach gcd 1 |

## Edge Cases

When all values share a common divisor greater than 1, every subset’s gcd is at least that divisor. For input `2 2 2`, the divisor counts produce f(2)=7 and f(1)=7, but subtraction removes all contributions at d=1, leaving zero valid subsets. The algorithm correctly collapses everything into higher gcd classes before reaching 1.

When the array contains a single element equal to 1, cnt[1]=1 and f(1)=1. No larger divisor exists to subtract from it, so g(1)=1 directly. The algorithm handles this without any special casing because divisor enumeration naturally includes 1 for every number.
