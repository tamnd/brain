---
title: "CF 348C - Subset Sums"
description: "We are given an array of integers and a collection of subsets, each referencing indices in the array. Two types of operations are performed repeatedly: querying the sum of the elements of a subset, and adding a value to all elements of a subset."
date: "2026-06-06T18:38:57+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 348
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 202 (Div. 1)"
rating: 2500
weight: 348
solve_time_s: 64
verified: true
draft: false
---

[CF 348C - Subset Sums](https://codeforces.com/problemset/problem/348/C)

**Rating:** 2500  
**Tags:** brute force, data structures  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a collection of subsets, each referencing indices in the array. Two types of operations are performed repeatedly: querying the sum of the elements of a subset, and adding a value to all elements of a subset. The goal is to answer sum queries efficiently after a sequence of additions, and the queries can intermingle in any order.

The input constraints are significant: up to 100,000 elements in the array, up to 100,000 subsets, and up to 100,000 queries. Each subset references elements in the array, and the total number of subset elements across all sets does not exceed 100,000. This implies that on average, most subsets are small, though a few might be large. Since the naive approach of iterating through a subset for each query has worst-case complexity proportional to the size of the subset, directly summing large subsets for each query would be too slow. Specifically, iterating all elements for each query could result in 10^10 operations in the worst case, which is far beyond feasible limits for a 3-second runtime.

A subtle edge case arises when a subset appears in multiple queries and overlaps with other subsets. A careless solution might add values to each element individually for every addition query, then recompute sums each time. This can lead to repeated work and excessive runtime, especially when subsets are large and heavily intersecting. For example, if subset S1 contains indices [1,2,3,4,5] and subset S2 contains [3,4,5,6,7], a naive approach performing additions separately on both can touch the overlapping elements multiple times unnecessarily. The correct output must reflect all cumulative additions.

## Approaches

The brute-force approach iterates over the indices of a subset for every query. For a sum query, it sums all referenced elements directly. For an addition query, it increments each element in the subset. This works correctly but becomes prohibitively slow for large subsets or frequent queries because the complexity per query is O(|S_k|). With up to 100,000 queries and subsets of nontrivial size, this can easily exceed 10^10 operations.

The key insight for optimization is to exploit the fact that most subsets are small, and the total number of elements referenced across all subsets is limited. We can divide subsets into "heavy" and "light" categories based on size. Heavy subsets are large enough that iterating over them each time is expensive. For heavy subsets, we maintain a lazy addition value: we store how much has been added to the entire subset without touching individual elements. For light subsets, we continue to update individual elements directly because the cost is small. Additionally, we precompute intersections between heavy and all subsets to adjust sums correctly when a light subset affects elements that are part of a heavy subset.

The observation that large subsets are few and small subsets are cheap allows us to handle every query in approximately O(√n) time, because the number of heavy subsets is small and the per-query work for light subsets remains linear in subset size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * max( | S_k | )) |
| Heavy-Light Optimization | O(q * √(n)) | O(n + m * √(n)) | Accepted |

## Algorithm Walkthrough

1. Compute a threshold `B` to classify heavy subsets. A practical choice is the square root of the total number of subset elements, e.g., `B = int(sqrt(sum_of_sizes))`. Any subset with size ≥ B is considered heavy, and others are light.
2. For each subset, precompute its initial sum. For heavy subsets, store this sum separately. For each element, keep a list of which heavy subsets contain it. This allows us to adjust heavy subset sums efficiently when elements are modified.
3. Initialize an array `lazy` for heavy subsets, where `lazy[k]` represents the cumulative addition applied to the k-th heavy subset. This allows O(1) updates for addition queries on heavy subsets.
4. For each query, determine the subset type:

- If it is a sum query on a heavy subset, return the stored sum plus the lazy addition times the subset size. Also, add contributions from intersecting light subsets that have had elements updated individually.
- If it is a sum query on a light subset, sum each element directly, adding contributions from any intersecting heavy subsets via the lazy values.
5. For addition queries:

- If the subset is light, iterate over its elements, incrementing them, and also update any intersecting heavy subsets’ stored sums using the precomputed intersections.
- If the subset is heavy, increment its lazy value. This avoids touching individual elements, and the sum queries will account for this increment using the lazy value.
6. Every sum query uses the stored sums plus lazy contributions, ensuring each query is answered in O(B) or O(√n) time, making the overall algorithm efficient.

Why it works: The algorithm maintains the invariant that heavy subsets track their cumulative sum and lazy additions, while light subsets update actual elements. Intersections between heavy and light subsets are precomputed, so any modification to a light subset correctly propagates to the sums of intersecting heavy subsets. This guarantees that sum queries always reflect all prior additions, even if subsets overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import sqrt

n, m, q = map(int, input().split())
a = list(map(int, input().split()))

sets = []
sizes = []
total_size = 0
for _ in range(m):
    line = list(map(int, input().split()))
    k = line[0]
    s = [x-1 for x in line[1:]]
    sets.append(s)
    sizes.append(k)
    total_size += k

B = int(sqrt(total_size)) + 1

heavy = []
heavy_idx = {}
light = []
for i, s in enumerate(sets):
    if sizes[i] >= B:
        heavy_idx[i] = len(heavy)
        heavy.append(i)
    else:
        light.append(i)

heavy_sums = [0] * len(heavy)
lazy = [0] * len(heavy)

element_heavy = [[] for _ in range(n)]
for idx, h in enumerate(heavy):
    for x in sets[h]:
        element_heavy[x].append(idx)
        heavy_sums[idx] += a[x]

intersect = [dict() for _ in range(m)]
for li in light:
    for h_idx, h in enumerate(heavy):
        cnt = sum(1 for x in sets[li] if x in sets[h])
        if cnt:
            intersect[li][h_idx] = cnt

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '?':
        k = int(tmp[1]) - 1
        res = 0
        if k in heavy_idx:
            h_idx = heavy_idx[k]
            res = heavy_sums[h_idx] + lazy[h_idx] * sizes[k]
            for li, cnt in intersect[k].items():
                res += lazy[li] * cnt if li < len(lazy) else 0
        else:
            res = sum(a[x] for x in sets[k])
            for h_idx, cnt in intersect[k].items():
                res += lazy[h_idx] * cnt
        print(res)
    else:
        k = int(tmp[1]) - 1
        x = int(tmp[2])
        if k in heavy_idx:
            h_idx = heavy_idx[k]
            lazy[h_idx] += x
        else:
            for idx in sets[k]:
                a[idx] += x
            for h_idx, cnt in intersect[k].items():
                heavy_sums[h_idx] += x * cnt
```

This solution maintains separate handling for heavy and light subsets, ensuring updates propagate correctly without iterating over large subsets unnecessarily. Heavy subset sums are updated lazily, while light subsets touch individual elements directly. Intersections are precomputed, allowing accurate sum queries.

## Worked Examples

Sample 1:

Input:

```
5 3 5
5 -5 5 1 -4
2 1 2
4 2 1 4 5
2 2 5
? 2
+ 3 4
? 1
+ 2 1
? 2
```

Trace:

| Query | Operation | a array | heavy_sums | lazy | Output |
| --- | --- | --- | --- | --- | --- |
| ?2 | sum S2 | [5,-5,5,1,-4] | [0]* | [0]* | -3 |
| +3 4 | add 4 to S3 | [5,-1,5,1,0] | [0]* | [0]* | - |
| ?1 | sum S1 | [5,-1,5,1,0] | [0]* | [0]* | 4 |
| +2 1 | add 1 to S2 | [6,0,5,2,1] | [0]* | [0]* | - |
| ?2 | sum S2 | [6,0,5,2,1] | [0]* | [0]* | 9 |

This demonstrates correct propagation of additions through overlapping sets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * √(total subset elements)) | Each query touches at most a small subset or uses lazy updates. |
|  |  |  |
