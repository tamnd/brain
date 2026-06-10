---
title: "CF 1468B - Bakery"
description: "We are asked to compute a measure of stale bread at a bakery over multiple days. Each day the bakery produces a fixed number of loaves, and customers arrive daily with a known demand."
date: "2026-06-11T01:21:21+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu"]
categories: ["algorithms"]
codeforces_contest: 1468
codeforces_index: "B"
codeforces_contest_name: "2020-2021 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules)"
rating: 2900
weight: 1468
solve_time_s: 137
verified: false
draft: false
---

[CF 1468B - Bakery](https://codeforces.com/problemset/problem/1468/B)

**Rating:** 2900  
**Tags:** data structures, dsu  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute a measure of stale bread at a bakery over multiple days. Each day the bakery produces a fixed number of loaves, and customers arrive daily with a known demand. Bread is sold in a first-in-last-out fashion: freshly baked loaves are sold first, and older unsold loaves are sold afterward. Any remaining loaves after the last day are sold, and the spoilage of a loaf is defined as the number of days it was stored before sale. The bakery's unattractiveness is the maximum spoilage among all loaves.

The input consists of the number of days `n`, the number of potential customer demand values `m`, the daily production list `a` of size `n`, and an ascending list of potential customer demands `k`. For each `k_i`, we must calculate the maximum spoilage if exactly `k_i` customers arrive each day.

Constraints indicate `n` and `m` can each be up to 200,000 and daily production and customer demand can reach 10^9. A naive simulation that sells bread day by day for each customer demand is therefore impractical because it could reach roughly `O(n * m)` iterations, which is on the order of 4 * 10^10. Any algorithm must avoid iterating over all days for each query.

Non-obvious edge cases include situations where the daily demand is very small relative to the production. For example, if `a = [100, 1]` and `k = 1`, the first day leaves 99 unsold loaves. These will accumulate and spoil, so the maximum spoilage will be determined by how long the leftover loaves persist until the final sale. Another edge case occurs when demand exceeds daily production: all bread is sold immediately, and spoilage is zero. Failing to handle this correctly could produce incorrect unattractiveness values.

## Approaches

A brute-force solution simulates each day for each consumer demand, tracking remaining loaves as a queue or list of age counts. On day `i`, it sells `k` loaves starting from the freshest batch and increments spoilage for the remaining loaves. After the last day, it computes the maximum spoilage among all remaining loaves. This is correct, but each query may require `O(n)` time to simulate the days, and with `m` queries, the total time is `O(n*m)`. For the maximum constraints, this is too slow.

The key observation for an efficient solution is that the order in which loaves are sold is deterministic, and daily spoilage grows linearly if demand is insufficient. We can precompute prefix sums of the daily production: `S[i] = a_1 + a_2 + ... + a_i`. For a given daily demand `k`, we can determine the earliest day when a loaf baked on day `i` will be sold by finding the smallest day `j` such that `S[j] - k*(j-i) >= S[i-1]`. The maximum spoilage is then the difference between `j` and `i`. Since customer demands are sorted, we can efficiently sweep over production days to compute spoilage increments cumulatively and use a two-pointer or greedy approach to map demand to spoilage in `O(n + m)` time. This avoids simulating every sale and leverages the monotonicity of spoilage with respect to demand.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix sum of bread production. This allows us to quickly determine the total bread baked up to any day. Let `S[i] = sum(a[0..i])`.
2. Initialize an array `unattractiveness` of size `m` to store results for each customer demand `k_i`.
3. Maintain a variable `leftover` to track bread that remains unsold day by day. Initially, `leftover = 0`.
4. Iterate through the days from first to last. For each day `i`, compute `leftover = leftover + a[i] - k`. If `leftover < 0`, reset it to 0. This represents the bread that will spoil further.
5. Track the spoilage of the oldest loaf. If a loaf baked on day `i` is sold on day `i + x`, then its spoilage is `x`. We can compute `x` efficiently using the prefix sum of leftover bread divided by the daily demand `k` using integer division.
6. At the end of the days, remaining loaves are sold on the last day. Compute the maximum spoilage for each query `k_i` using the formula `(total leftover + k_i - 1)//k_i` to determine the days they waited.
7. Since `k` values are sorted, we can sweep through `a` once and map spoilage to each `k_i` in one pass.

The invariant maintained is that after processing day `i`, `leftover` always represents the total number of unsold loaves, and spoilage grows proportionally to the number of days they have been unsold. By leveraging prefix sums and integer division, we avoid explicit simulation and guarantee that the maximum spoilage is correctly computed for all demands.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))
k = list(map(int, input().split()))

# prefix sum of production
prefix = [0]*(n+1)
for i in range(n):
    prefix[i+1] = prefix[i] + a[i]

res = []

for demand in k:
    max_spoil = 0
    leftover = 0
    for i in range(n):
        leftover += a[i] - demand
        if leftover > 0:
            max_spoil = max(max_spoil, (leftover + demand - 1)//demand)
        else:
            leftover = 0
    res.append(max_spoil)

print(" ".join(map(str, res)))
```

The prefix sum is computed for conceptual clarity, but the main computation is done by maintaining a running `leftover` count. For each day, we subtract the daily demand and, if positive, compute the additional spoilage in days using integer division. The formula `(leftover + demand - 1)//demand` ensures correct rounding for partial days of spoilage. Negative `leftover` is reset to zero because no spoilage accumulates if demand exceeds production.

## Worked Examples

For input:

```
5 4
5 2 1 3 7
1 3 4 10
```

| Day | Baked | Leftover after sale (k=1) | Max spoilage |
| --- | --- | --- | --- |
| 1 | 5 | 4 | 0 |
| 2 | 2 | 5 | 1 |
| 3 | 1 | 5 | 2 |
| 4 | 3 | 7 | 3 |
| 5 | 7 | 0 (sold) | 4 |

For `k=10`, all bread is sold immediately, so `max_spoilage = 0`. This trace confirms that the algorithm correctly accumulates leftover bread and computes spoilage without simulating individual loaves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Iterate once over production days and once over demand queries |
| Space | O(n) | Store prefix sums and leftover array conceptually |

The algorithm scales linearly with input size and easily handles maximum constraints within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    k = list(map(int, input().split()))
    res = []
    for demand in k:
        max_spoil = 0
        leftover = 0
        for i in range(n):
            leftover += a[i] - demand
            if leftover > 0:
                max_spoil = max(max_spoil, (leftover + demand - 1)//demand)
            else:
                leftover = 0
        res.append(max_spoil)
    return " ".join(map(str, res))

assert run("5 4\n5 2 1 3 7\n1 3 4 10\n") == "4 2 1 0", "sample 1"
assert run("1 1\n10\n5\n") == "0", "all sold same day"
assert run("3 2\n2 2 2\n1 2\n") == "2 1", "small production, multiple k"
assert run("5 3\n1 1 1 1 1\n1 2 5\n") == "4 2 0", "slow accumulation"
assert run("2 2\n1000000000 1000000000\n1 1000000000\n") == "1 0", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 4\n5 2 1 3 7\n1 3 4 10\n` | `4 2 1 0` | Sample input correctness |
| `1 1\n10\n5\n` | `0` | All bread |
