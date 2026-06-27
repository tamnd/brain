---
title: "CF 105006I - Corgi Counting"
description: "We are given a collection of corgis, each assigned a 22-bit integer personality value. If we pick any subset of these corgis, every pair inside that subset contributes a “happiness” equal to the bitwise AND of their personalities."
date: "2026-06-28T03:13:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105006
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 03-01-24 Div. 1 (Advanced)"
rating: 0
weight: 105006
solve_time_s: 61
verified: false
draft: false
---

[CF 105006I - Corgi Counting](https://codeforces.com/problemset/problem/105006/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of corgis, each assigned a 22-bit integer personality value. If we pick any subset of these corgis, every pair inside that subset contributes a “happiness” equal to the bitwise AND of their personalities. The total happiness of a subset is the sum of these pairwise AND values. The task is to sum this quantity over every possible subset of corgis.

A direct way to interpret this is that every pair of indices contributes multiple times: once for every subset that contains both elements of the pair. Instead of thinking about subsets first, it is more useful to think about how often a fixed pair appears across all subsets.

The constraints are large, with up to 200000 elements and values up to 2²². This immediately rules out any solution that iterates over subsets or even over all pairs directly if each pair requires heavy work. There are roughly 2×10^10 subsets, and 2×10^10 pairs across all subsets as well, so any subset enumeration is impossible. Even O(n²) is borderline too large for n = 2×10^5.

A naive approach would compute for each subset its internal pair sum, leading to exponential time. Even summing over all pairs once and then multiplying by a fixed factor ignores subset structure and fails, because each pair is not counted equally across subsets unless we carefully account for combinatorics.

A subtle pitfall is assuming linearity over subsets without tracking multiplicity. For example, with values [1, 2], the pair (1,2) contributes only when both are chosen, which happens in exactly one subset, not in all subsets containing either element.

## Approaches

The key idea is to reverse the order of summation. Instead of summing over subsets first, we sum over pairs first, and for each pair determine how many subsets contain it.

Fix two indices i < j. The pair (i, j) appears in exactly those subsets that include both elements, while the remaining n − 2 elements are arbitrary. Therefore, each pair contributes its AND value multiplied by 2^(n−2). This reduces the entire problem to computing:

sum over all pairs (p_i & p_j), then multiply by 2^(n−2).

Now the problem becomes computing the sum of bitwise AND over all pairs. This is a classic bit decomposition trick. Each bit can be treated independently. For each bit b, we count how many numbers have this bit set. If cnt[b] elements have bit b set, then there are cnt[b] choose 2 pairs contributing that bit, and each such pair contributes 2^b to the AND sum.

So the total pairwise AND sum is:

sum over b: (cnt[b] * (cnt[b] − 1) / 2) * 2^b

Finally multiply by 2^(n−2).

This reduces the problem to counting bits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(n · 2^n) | O(1) | Too slow |
| Pair counting with bit decomposition | O(n · 22) | O(22) | Accepted |

## Algorithm Walkthrough

1. Count how many times each bit from 0 to 21 appears across all values. This isolates contributions per bit, since AND operates independently on each bit.
2. For each bit b, compute cnt[b] * (cnt[b] − 1) // 2. This gives the number of unordered pairs where both numbers have bit b set. The reason this works is that a bit contributes to the AND only when both endpoints have it.
3. Multiply each pair count by 2^b to account for the value of that bit in the final sum.
4. Sum these contributions over all bits to obtain the total sum of p_i & p_j over all unordered pairs.
5. Multiply the result by 2^(n−2), because each fixed pair appears in exactly 2^(n−2) subsets. Every subset containing both endpoints can freely choose any of the remaining elements.
6. Return the result modulo 998244353.

### Why it works

The correctness rests on two independent decompositions. First, each pair’s contribution across all subsets is uniform and depends only on how many subsets contain both endpoints, which is exactly 2^(n−2). Second, bitwise AND is additive over bits, meaning the contribution of each bit can be counted separately without interference from other bits. Since both transformations preserve exact total contribution, the final formula matches the original definition.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modpow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

n = int(input())
a = list(map(int, input().split()))

B = 22
cnt = [0] * B

for x in a:
    for b in range(B):
        if x & (1 << b):
            cnt[b] += 1

pair_and_sum = 0
for b in range(B):
    c = cnt[b]
    pair_and_sum += (c * (c - 1) // 2) % MOD * ((1 << b) % MOD)
    pair_and_sum %= MOD

if n >= 2:
    pair_and_sum *= modpow(2, n - 2)
    pair_and_sum %= MOD
else:
    pair_and_sum = 0

print(pair_and_sum)
```

The implementation first compresses all information into bit counts, avoiding any pair enumeration. The modular exponentiation computes the subset multiplicity factor 2^(n−2) efficiently. The multiplication is deferred until after the pairwise sum to avoid repeated modular operations.

One subtle detail is handling n < 2, where no pairs exist and the result must be zero. Another is keeping all intermediate values under modulo 998244353 while still using integer arithmetic for combinations, since cnt[b] choose 2 fits safely in Python integers before reduction.

## Worked Examples

### Sample 1

Input:

```
3
1 2 3
```

Bit counts:

bit 0: {1, 3} → 2

bit 1: {2, 3} → 2

| Bit | cnt | pairs cntC2 | contribution |
| --- | --- | --- | --- |
| 0 | 2 | 1 | 1 |
| 1 | 2 | 1 | 2 |

Pair sum = 3.

Multiply by 2^(3−2) = 2 → result = 6.

This confirms that each pair is counted once per subset containing it.

### Sample 2

Input:

```
5
3 5 2 1 2
```

Bit counts:

bit 0: 3 elements

bit 1: 3 elements

| Bit | cnt | cntC2 | contribution |
| --- | --- | --- | --- |
| 0 | 3 | 3 | 3 |
| 1 | 3 | 3 | 6 |

Pa
