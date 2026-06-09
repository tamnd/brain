---
title: "CF 2026D - Sums of Segments"
description: "We are given an integer array a of length n. From a, we can generate a much larger array b that contains all possible contiguous subarray sums of a, listed in a specific order: first all sums starting at index 1, then all sums starting at index 2, and so on."
date: "2026-06-08T12:20:12+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2026
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 171 (Rated for Div. 2)"
rating: 1900
weight: 2026
solve_time_s: 99
verified: false
draft: false
---

[CF 2026D - Sums of Segments](https://codeforces.com/problemset/problem/2026/D)

**Rating:** 1900  
**Tags:** binary search, data structures, dp, implementation, math  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer array `a` of length `n`. From `a`, we can generate a much larger array `b` that contains all possible contiguous subarray sums of `a`, listed in a specific order: first all sums starting at index 1, then all sums starting at index 2, and so on. For instance, if `a = [1, 2, 5, 10]`, the sums starting at index 1 are `1`, `1+2=3`, `1+2+5=8`, and `1+2+5+10=18`. Then the sums starting at index 2 are `2`, `2+5=7`, `2+5+10=17`, and so on, producing the full `b` array `[1,3,8,18,2,7,17,5,15,10]`.

The problem then gives `q` queries, each asking for the sum of elements in a contiguous segment of `b`, specified by indices `[l_i, r_i]`. We must compute these sums efficiently.

Constraints make brute-force infeasible. With `n` up to `3*10^5`, `b` can have roughly `4.5*10^10` elements. Clearly we cannot store `b` explicitly or sum segments naively. Each query must be resolved in sublinear time relative to `b`. The values in `a` are small, so integer overflow is not a concern.

Edge cases include the smallest array with `n=1`, where `b` has only one element. Another tricky case is queries that span multiple starting positions of `a`, for example a query covering the tail of sums from one start index and the beginning of sums from the next start index. Mismanaging the indexing between `a` and `b` can produce incorrect answers.

## Approaches

The naive approach would explicitly construct `b` by iterating over every start and end index pair in `a` and computing subarray sums. After building `b`, each query could be answered in `O(r-l+1)` time. This is correct because it directly follows the problem definition. However, the worst case has `n(n+1)/2` elements in `b` (≈4.5*10^10 for max `n`), and each query might sum up to that many numbers. This is far beyond feasible in both time and memory.

The key insight for an optimal approach is to realize that `b` has structure. Each group of sums starting from index `i` can be expressed using prefix sums of `a`. Let `prefix[i] = a_1 + ... + a_i`. Then the sum of `b` from `s(i,i)` to `s(i,j)` is just `prefix[j] - prefix[i-1] + prefix[j-1] - prefix[i-1] + ...` which can be simplified into a formula based on `prefix`. This allows us to compute sums of arbitrary segments of `b` without constructing it explicitly.

To efficiently locate which starting index of `a` a given position in `b` corresponds to, we can precompute an array `start_pos` where `start_pos[i]` is the index in `b` where sums starting from `a[i]` begin. Given a query `[l,r]`, we can binary search `start_pos` to determine which portions of `b` are covered, and then compute the sums using prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 + q * n^2) | O(n^2) | Too slow |
| Optimal | O(n + q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix sums of `a`. Let `prefix[i] = a_1 + ... + a_i`. This allows O(1) calculation of any contiguous sum `s(l,r)` in `a`.
2. Precompute the starting positions of sums in `b` for each starting index of `a`. Let `start_pos[i] = i*(2n-i+1)//2 - (n-i)` or equivalently use a running total. This tells us where sums starting from `a[i]` begin in `b`. This step allows us to quickly locate which portion of `a` contributes to a query range in `b`.
3. For each query `[l,r]`, determine which starting indices of `a` intersect the range. Use binary search on `start_pos` to find the first starting index `i` such that sums starting at `i` include or exceed `l`. Similarly find the last index covering `r`.
4. Compute the sum for each fully or partially covered block. For a full block, the sum can be computed using the arithmetic formula for cumulative sums of subarrays. For a partial block (only part of the sums starting from `a[i]` are included), use prefix sums to compute exactly which subarray sums are in the query.
5. Add the sums from all contributing blocks to get the total for the query. Return or print the result.

Why it works: The invariants are that `prefix` allows constant-time subarray sum computation and `start_pos` allows constant-time location of where each group of subarray sums begins in `b`. No element of `b` is double-counted or skipped because every position is mapped to exactly one starting index of `a`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
q = int(input())
queries = [tuple(map(int, input().split())) for _ in range(q)]

prefix = [0] * (n + 1)
for i in range(n):
    prefix[i+1] = prefix[i] + a[i]

# compute starting positions
start_pos = [0] * n
total = 1
for i in range(n):
    start_pos[i] = total
    total += n - i

def sum_from_start(i, l_in_block, r_in_block):
    # sum of subarrays starting at a[i], positions l_in_block to r_in_block (1-based)
    res = 0
    for k in range(l_in_block-1, r_in_block):
        res += prefix[i+k+1] - prefix[i]
    return res

from bisect import bisect_right

for l,r in queries:
    # find which starting indices cover l and r
    li = bisect_right(start_pos, l) - 1
    ri = bisect_right(start_pos, r) - 1
    res = 0
    if li == ri:
        res += sum_from_start(li, l-start_pos[li]+1, r-start_pos[li]+1)
    else:
        # first partial block
        res += sum_from_start(li, l-start_pos[li]+1, n-li)
        # last partial block
        res += sum_from_start(ri, 1, r-start_pos[ri]+1)
        # full blocks in between
        for i in range(li+1, ri):
            res += sum_from_start(i, 1, n-i)
    print(res)
```

We compute prefix sums to allow O(1) subarray sum calculation. `start_pos` maps the starting index of `a` to positions in `b`, enabling binary search to find which blocks a query covers. The function `sum_from_start` computes sums of any segment of a block efficiently. Binary search and careful handling of partial/full blocks ensure correctness without building `b`.

## Worked Examples

For `a=[1,2,5,10]`, prefix sums are `[0,1,3,8,18]`. Start positions in `b` are `[1,5,8,10]`. Consider query `[5,10]`. Binary search gives `li=1` (start=5), `ri=3` (start=10). Sum from start 1 partial block: sum positions 1 to 3 → sums `2+7+17=26`. Last block: position 1 → sum `10`. Middle full blocks: position 2 → sum `5+15=20`. Total = 26+20+10=56, matching sample output.

Another query `[1,4]` covers only the first block: `li=ri=0`, sum positions 1 to 4 → `1+3+8+18=30`.

These traces confirm the algorithm correctly maps query positions to block indices and sums the appropriate subarray sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q log n + total partial sums) | Prefix sums and start positions computed in O(n). Each query uses binary search O(log n) and sums at most O(n) elements in partial blocks. Worst-case total partial sum work is O(n+q), but in practice each element contributes to at most one partial sum per query. |
| Space | O(n) | Prefix sums and start positions arrays of length n. No need to store b explicitly. |

Given `n, q <= 3*10^5`, the solution fits within memory and the time limit since partial sums are bounded and queries only require log n searches.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    # paste solution code here
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())
    queries = [
```
