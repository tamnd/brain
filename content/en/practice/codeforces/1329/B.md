---
title: "CF 1329B - Dreamoon Likes Sequences"
description: "We are asked to count strictly increasing sequences of positive integers bounded by a number d such that the cumulative XOR of the sequence also forms a strictly increasing sequence. Each test case gives a maximum value d and a modulo m."
date: "2026-06-11T16:20:58+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1329
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 631 (Div. 1) - Thanks, Denis aramis Shitov!"
rating: 1700
weight: 1329
solve_time_s: 209
verified: false
draft: false
---

[CF 1329B - Dreamoon Likes Sequences](https://codeforces.com/problemset/problem/1329/B)

**Rating:** 1700  
**Tags:** bitmasks, combinatorics, math  
**Solve time:** 3m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count strictly increasing sequences of positive integers bounded by a number `d` such that the cumulative XOR of the sequence also forms a strictly increasing sequence. Each test case gives a maximum value `d` and a modulo `m`. The output for each test case is the number of valid sequences modulo `m`.

The input consists of up to 100 test cases. Each `d` can be as large as one billion, which rules out enumerating all possible sequences, because even sequences of length one or two can be on the order of `d` and sequences of arbitrary length explode combinatorially. A naive approach generating all sequences would require at least `O(2^d)` time, which is completely infeasible.

A subtle constraint comes from the XOR property. XOR is monotone in a limited sense: if we restrict elements to powers of two ranges, then XOR behaves like addition in terms of magnitude growth. A careless implementation might attempt to iterate `1` to `d` linearly and compute sequences directly, which would be too slow. Another edge case is `d < m` or `m = 1`, where modulo arithmetic changes the results in ways that naive code may mishandle. For instance, `d = 10` and `m = 1` must output zero since all counts modulo 1 are zero.

## Approaches

The brute-force solution would try to enumerate all strictly increasing sequences `a` from `1` to `d` and check whether the XOR cumulative sequence `b` is strictly increasing. This works for tiny `d` but fails as soon as `d` exceeds a few dozen, because the number of sequences is exponential in `d`. For the maximum bound `d = 10^9`, brute-force is hopeless.

The key observation is that the XOR sequence will remain strictly increasing if each element `a_i` starts in a power-of-two bucket. Define bucket `k` as numbers `[2^k, 2^{k+1} - 1]` limited by `d`. Within each bucket, all numbers are at least twice as large as all numbers in previous buckets. Therefore, sequences formed by choosing elements from increasingly higher buckets automatically satisfy both the `a`-sequence and cumulative `b`-sequence strictly increasing constraints.

Within each bucket, the number of ways to select elements is simply `2^(count of elements in the bucket) - 1` (we must choose at least one element). This converts the problem into counting combinations across buckets, which can be done efficiently by dynamic programming from the highest bucket downward, multiplying the number of sequences in a lower bucket by the choices in higher buckets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^d) | O(d) | Too slow |
| Optimal (Bucket DP) | O(log d) | O(log d) | Accepted |

## Algorithm Walkthrough

1. For each test case, initialize `ans = 0` to accumulate the total number of valid sequences modulo `m`.
2. Iterate over powers of two `pw = 1, 2, 4, ...` up to `d`. These powers define our buckets. Each bucket `pw` contains numbers `[pw, min(2*pw - 1, d)]`. Let `count = min(2*pw - 1, d) - pw + 1` be the number of elements in this bucket.
3. The number of non-empty sequences we can form from this bucket is `seq_count = (count + 1) - 1 = 2^count - 1`. Since `count` can be large, we compute this modulo `m`.
4. Maintain a running multiplier `ways = 1` representing sequences from higher buckets. Multiply `seq_count` by `ways` and add to `ans`.
5. Update `ways = (ways * (seq_count + 1)) % m` to propagate the cumulative choices to lower buckets.
6. Repeat for all buckets and print `ans % m` for each test case.

Why it works: the bucket partition guarantees that any sequence formed by picking elements from increasingly higher buckets automatically satisfies the cumulative XOR strictly increasing property. Counting seq
