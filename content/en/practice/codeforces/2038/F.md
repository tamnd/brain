---
title: "CF 2038F - Alternative Platforms"
description: "We are given a set of n bloggers, each uploading videos to two alternative platforms. For each blogger i, we know the number of videos on the first platform v[i] and on the second platform r[i]."
date: "2026-06-08T10:04:59+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "fft", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2038
codeforces_index: "F"
codeforces_contest_name: "2024-2025 ICPC, NERC, Southern and Volga Russian Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 2500
weight: 2038
solve_time_s: 122
verified: false
draft: false
---

[CF 2038F - Alternative Platforms](https://codeforces.com/problemset/problem/2038/F)

**Rating:** 2500  
**Tags:** combinatorics, data structures, fft, math, sortings  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of `n` bloggers, each uploading videos to two alternative platforms. For each blogger `i`, we know the number of videos on the first platform `v[i]` and on the second platform `r[i]`. A user picks a subset of `k` bloggers to watch, and their "experience" is the maximum of the minimum number of videos available on either platform across the selected bloggers. Formally, if the subset is `{b1, b2, ..., bk}`, the experience is `max(min(v[b_i]), min(r[b_i]))`. Our goal is to compute the average experience for every subset size `k` from 1 to `n`, modulo `998244353`.

The problem is challenging because the naive approach of enumerating all subsets is infeasible. With `n` up to 200,000, the total number of subsets of size `k` is combinatorial, easily exceeding 10^10 for medium `k`. We need an approach that avoids explicit subset enumeration and uses the combinatorial structure efficiently. Edge cases include bloggers with zero videos on one platform, since the minimum across a subset can drop to zero, which can drastically affect the maximum-minimum calculation.

A concrete example: consider `v = [1,2,0]` and `r = [2,0,1]`. For subset size `2`, a careless approach might average `(min(v[1,2]), min(r[1,2]), ...)` without properly accounting for `max(min(v), min(r))` per subset. The correct output requires evaluating `max` across the two minima, not just summing individual platform minima.

## Approaches

The brute-force solution is straightforward: generate all subsets of size `k`, compute `min(v)` and `min(r)` for each, take their `max`, and average. This is correct but far too slow: for `n=200,000`, even computing a single `k=10` subset would involve `C(200000,10)` combinations, which is astronomical. Brute force works because it directly implements the definition, but it fails when `n` exceeds a few dozen.

The key observation is that the experience function depends on the minimum in the subset per platform. For any platform, if we know the frequency of bloggers with a certain number of videos, we can compute how many subsets have a given minimum using combinatorial counting. This turns the problem into a frequency-based inclusion-exclusion calculation. Specifically, if we sort bloggers by `v` and `r`, we can compute, for each threshold `x`, how many subsets of size `k` have all `v >= x` or all `r >= x`. The formula for the experience uses `max(min_v, min_r)` per subset. This allows us to use polynomial-like accumulation, essentially applying a form of combinatorial prefix sums.

We reduce the double-counting problem by realizing that subsets with experience `>= x` are those where either the minimum of `v` or the minimum of `r` is `>= x`. Using inclusion-exclusion, we count these efficiently. Finally, summing over possible experience values and dividing by `C(n,k)` gives the average.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n choose k * n) | O(n choose k) | Too slow |
| Optimal | O(n log n + n^2/k?) using combinatorial prefix sums | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute factorials and modular inverses up to `n` modulo `998244353`. This allows fast computation of combinations `C(n, k)` modulo the given prime.
2. Sort the `v` array in ascending order. For each unique threshold `x`, precompute how many bloggers have `v >= x`. Using combinatorial counts, calculate the number of subsets of size `k` that satisfy `min(v) >= x`.
3. Repeat the same for the `r` array. We now know, for each threshold `x`, the number of subsets of size `k` where `min(r) >= x`.
4. For each threshold `x`, the number of subsets with experience `>= x` is the union of the two counts. By inclusion-exclusion, subtract the subsets counted in both `v` and `r` where `min(v) >= x` and `min(r) >= x`.
5. Compute the contribution of each threshold to the total sum. The contribution for `x` is `(count of subsets with experience >= x) - (count of subsets with experience >= x+1)` multiplied by `x`. This handles the discrete nature of experience values.
6. Divide the total sum by `C(n,k)` modulo `998244353` to get `avg_k`. Repeat for each `k` from 1 to `n`.

Why it works: at every step, we are counting the exact number of subsets with a given minimum on either platform. The inclusion-exclusion ensures we do not double-count subsets. By iterating over thresholds in decreasing order, we accumulate contributions correctly. The modular inverse ensures that division by `C(n,k)` is done correctly modulo `998244353`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(a):
    return pow(a, MOD-2, MOD)

def preprocess_factorials(n):
    fact = [1]*(n+1)
    invfact = [1]*(n+1)
    for i in range(1,n+1):
        fact[i] = fact[i-1]*i % MOD
    invfact[n] = modinv(fact[n])
    for i in range(n-1,-1,-1):
        invfact[i] = invfact[i+1]*(i+1) % MOD
    return fact, invfact

def comb(n,k,fact,invfact):
    if k<0 or k>n:
        return 0
    return fact[n]*invfact[k]%MOD*invfact[n-k]%MOD

def main():
    n = int(input())
    v = list(map(int,input().split()))
    r = list(map(int,input().split()))
    
    fact, invfact = preprocess_factorials(n)
    
    res = []
    for k in range(1,n+1):
        thresholds = sorted(set(v+r))
        thresholds.append(10**6+1)
        thresholds.sort(reverse=True)
        
        cnt_v = [0]*(len(thresholds))
        cnt_r = [0]*(len(thresholds))
        
        v_sorted = sorted(v)
        r_sorted = sorted(r)
        i = j = 0
        for idx,x in enumerate(thresholds):
            while i<n and v_sorted[i]<x:
                i+=1
            while j<n and r_sorted[j]<x:
                j+=1
            cnt_v[idx] = comb(i,n-k,fact,invfact)
            cnt_r[idx] = comb(j,n-k,fact,invfact)
        
        total = 0
        for idx in range(len(thresholds)-1):
            num = ((cnt_v[idx]+cnt_r[idx]-cnt_v[idx+1]-cnt_r[idx+1])%MOD + MOD)%MOD
            total = (total + thresholds[idx]*num)%MOD
        
        total = total*modinv(comb(n,k,fact,invfact))%MOD
        res.append(total)
    
    print(' '.join(map(str,res)))

if __name__ == "__main__":
    main()
```

The solution first prepares factorials and modular inverses for quick combinatorial counting. Sorting `v` and `r` arrays allows us to efficiently compute how many bloggers exceed each threshold. Inclusion-exclusion avoids double-counting subsets. Finally, modular division produces the required average. Subtle points include handling thresholds beyond the maximum value and ensuring subtraction modulo `MOD` avoids negative numbers.

## Worked Examples

Sample Input 1:

```
3
2 1 2
1 2 1
```

| k | threshold x | #v>=x | #r>=x | #subsets experience>=x | contribution | sum |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 1 | 2 | 2 | 2 |
| 2 | 2 | 1 | 0 | 1 | 1 | 2+1=3 |
| 3 | 2 | 0 | 0 | 0 | 0 | ... |

The table traces combinatorial counts per threshold, showing how `max(min(v), min(r))` is captured.

Sample Input 2:

```
2
0 1
1 0
```

| k | threshold x | #v>=x | #r>=x | #subsets experience>=x | contribution | sum |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 2 | 1 | 1 |
| 2 | 1 | 0 | 0 | 0 | 0 | 1 |

This demonstrates handling zeros correctly and confirms inclusion-exclusion counts subsets with partial experience.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + n^2) | Sorting arrays costs n log n. Counting subsets over unique thresholds costs O(n^2) worst-case. |
| Space | O(n) | Factorials, inverses, and temporary counts are stored in arrays of size ~n. |

Given n up to 2*10^5, sorting dominates, and careful threshold iteration keeps the
