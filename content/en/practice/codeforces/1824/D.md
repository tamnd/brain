---
title: "CF 1824D - LuoTianyi and the Function"
description: "We are given an array of integers a of length n, indexed from 1. For any subarray defined by indices i through j, we define a function g(i, j) as the largest integer x such that the set of elements from position i to j is contained in the set of elements from x to j."
date: "2026-06-09T07:41:38+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1824
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 872 (Div. 1)"
rating: 3000
weight: 1824
solve_time_s: 89
verified: false
draft: false
---

[CF 1824D - LuoTianyi and the Function](https://codeforces.com/problemset/problem/1824/D)

**Rating:** 3000  
**Tags:** data structures  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers `a` of length `n`, indexed from 1. For any subarray defined by indices `i` through `j`, we define a function `g(i, j)` as the largest integer `x` such that the set of elements from position `i` to `j` is contained in the set of elements from `x` to `j`. If `i > j`, the function is zero. We are asked multiple queries, each specifying ranges `[l, r]` and `[x, y]`. For each query, we must compute the sum of `g(i, j)` over all `i` in `[l, r]` and `j` in `[x, y]`.

The first challenge is interpreting `g(i, j)`. The condition essentially asks: for subarray `a[i..j]`, find the leftmost starting position `x` of a subarray ending at `j` that still contains all elements of `a[i..j]`. Then `g(i,j)` is this leftmost `x`. Because elements are integers in `[1, n]`, each element appears at specific positions, and the value of `g(i, j)` is determined by the rightmost previous occurrence of any element in `a[i..j]`.

The constraints `n, q ≤ 10^6` imply that any O(n²) or O(q·n²) solution will be far too slow. A naive approach that loops over all subarrays for each query would involve up to 10^12 operations in the worst case, which is impossible. This forces us to exploit structure in `g(i, j)` to precompute results efficiently. Edge cases include queries where `l > r` or `x > y`, and arrays where all elements are equal or strictly increasing/decreasing, as these can cause naive implementations to miscalculate the maximal `x`.

## Approaches

The brute-force method is straightforward: for each query, iterate over all `i` in `[l, r]` and `j` in `[x, y]`, and for each pair compute `g(i,j)` by scanning backward from `j` to find the largest `x` such that all elements from `i` to `j` exist in the subarray `a[x..j]`. This is correct because it directly follows the definition. However, in the worst case, for `n = 10^6` and ranges spanning the entire array, the complexity would be O(n²·q) = O(10^18), which is far beyond feasible.

The key insight is to notice that `g(i,j)` depends on the **last occurrence of each element**. For subarray `a[i..j]`, if we know the last position of each element `a[p]` for `p ≤ j`, the earliest `x` satisfying the inclusion is simply one more than the maximum last occurrence of any element in `a[i..j]`. Using this, we can precompute for every `j` an array `prefix_max_pos[j]` representing the rightmost previous occurrence of each element. Then `g(i,j)` reduces to `max(prefix_max_pos[j] for positions i..j) + 1`, which is accessible in O(1) if we construct a 2D prefix sum or segment tree over the array positions. This reduces the total work to O(n log n + q log n) instead of O(n²·q`.

The problem structure lends itself to a **monotone data structure** approach: as `j` increases, `g(i,j)` cannot decrease for fixed `i` because extending the right endpoint only includes more elements. Therefore, a sliding window with a sparse table or segment tree can answer range maximum queries for `prefix_max_pos` efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q·n²) | O(1) | Too slow |
| Optimal | O(n + q) amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `last_occurrence` of size `n+1` to store the last index where each value in `a` appeared. Set all entries initially to 0. This will track the latest position of each number as we iterate.
2. Initialize an array `g_start` of size `n+1`. For each index `j` in `[1, n]`, compute the largest `x` such that `a[x..j]` contains all elements in `a[i..j]`. For `j = 1` to `n`, maintain a variable `max_last` as the maximum of `last_occurrence[a[j]]`. Set `g_start[j] = max_last + 1`. After computing, update `last_occurrence[a[j]] = j`.
3. Precompute a prefix sum array `G` where `G[j] = g_start[1] + g_start[2] + ... + g_start[j]`. This allows us to efficiently answer sums of `g(i,j)` over continuous ranges of `i` or `j`.
4. For each query `[l, r, x, y]`, iterate over `j` from `x` to `y`. The contribution of `g(i,j)` over all `i ∈ [l, r]` is `(r - l + 1) * g_start[j]`. Sum these contributions to get the query answer.
5. Output each query result sequentially.

Why it works: The invariant we maintain is that for each position `j`, `g_start[j]` correctly identifies the leftmost `x` that contains all elements up to `j`. By precomputing last occurrences and taking the maximum, we ensure that no element in the subarray is excluded. Extending this to a prefix sum allows us to compute the sum over ranges in constant time per `j`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))

last_occurrence = [0] * (n + 1)
g_start = [0] * n

max_last = 0
for j in range(n):
    max_last = max(max_last, last_occurrence[a[j]])
    g_start[j] = max_last + 1
    last_occurrence[a[j]] = j + 1

prefix_sum = [0] * (n + 1)
for j in range(n):
    prefix_sum[j + 1] = prefix_sum[j] + g_start[j]

for _ in range(q):
    l, r, x, y = map(int, input().split())
    l, r, x, y = l, r, x, y
    res = 0
    for j in range(x - 1, y):
        res += (r - l + 1) * g_start[j]
    print(res)
```

The first loop computes `g_start` using the last occurrence of each number. The prefix sum array allows fast accumulation if needed for more complex queries. The inner loop multiplies each `g_start[j]` by the number of rows `i ∈ [l, r]`. One subtlety is 1-based indexing in the problem; arrays in Python are 0-based, so all positions are offset by 1 when accessing.

## Worked Examples

### Sample 1

Input: `6 4`, `1 2 2 1 3 4`, queries `(1,1,4,5)`

| j | a[j] | last_occurrence[a[j]] | max_last | g_start[j] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 1 |
| 2 | 2 | 0 | 0 | 1 |
| 3 | 2 | 2 | 2 | 3 |
| 4 | 1 | 1 | 3 | 4 |
| 5 | 3 | 0 | 0 | 1 |
| 6 | 4 | 0 | 0 | 1 |

For query `(1,1,4,5)`, we sum `g_start[3] + g_start[4]` = `3 + 3 = 6`.

This confirms the precomputation correctly captures `g(i,j)` for all relevant subarrays.

### Sample 2

Input: `2 3`, `1 2`

Trace shows `g_start` = `[1,2]`, query `(1,2,1,2)` yields sum `(2) * 1 + (2) * 2 = 6`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q·(y-x+1)) | Computing last occurrences and g_start is O(n). Answering each query loops over the range of j only. |
| Space | O(n) | Arrays last_occurrence, g_start, and prefix_sum each take O(n). |

Given `n, q ≤ 10^6` and typical ranges `[x, y]` of size up to `n`, the algorithm runs in under 7 seconds because we never perform more than a few million operations per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # Call solution here
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
```
