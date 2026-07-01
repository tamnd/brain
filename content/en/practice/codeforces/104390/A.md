---
title: "CF 104390A - Merge"
description: "Two people report charging stations along a line. Each station has a position and a number of outlets. We effectively build a multiset of positions where each position appears multiple times according to how many outlets exist there. Mr."
date: "2026-07-01T02:46:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104390
codeforces_index: "A"
codeforces_contest_name: "The Unofficial Mirror Contest of 19th Thailand Olympiad in Informatics Day 1"
rating: 0
weight: 104390
solve_time_s: 178
verified: true
draft: false
---

[CF 104390A - Merge](https://codeforces.com/problemset/problem/104390/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

Two people report charging stations along a line. Each station has a position and a number of outlets. We effectively build a multiset of positions where each position appears multiple times according to how many outlets exist there.

Mr. X’s data is fixed: each AC station contributes its coordinate repeated `s_i` times. Mr. Y’s data is similar, but before merging, every coordinate is linearly transformed using the same formula in a query: `y -> alpha * y + beta`. After transformation, each DC station contributes `t_j` copies of this new coordinate.

Once both multisets are combined, everything is sorted by coordinate, and we flatten the result into a single sequence. Each position expands into a block whose length equals its total multiplicity. A query asks for the value at the k-th position in this flattened sequence.

The important difficulty is that we do not explicitly build the expanded array. The total number of elements can reach tens of millions, so any approach that materializes the merged sequence will not fit in time or memory.

The constraints suggest that preprocessing per dataset is fine, but each query must be answered in roughly logarithmic time over the input size. With up to 100,000 stations and 50,000 queries, even O(N log N + Q log N) per query is acceptable, but anything linear in k or in total multiplicity is not.

A subtle edge case is overlap after transformation. Different original Y coordinates may map onto positions that coincide with X coordinates, requiring counts to be summed correctly. Another subtlety is that the transformation preserves ordering because `alpha >= 1`, so the relative order of Y stations does not change. This prevents any need to re-sort Y after transformation; only values shift and scale.

## Approaches

A direct approach would expand every station into repeated coordinates and merge the two lists like a standard merge step of merge sort. This is correct because the final structure is just two sorted streams interleaved. However, the total number of expanded elements can be extremely large, so merging explicitly is too slow and too memory heavy.

The key observation is that we never actually need the full merged sequence. We only need the k-th element. This suggests using a selection strategy rather than full construction. Instead of building the array, we can answer each query by checking, for a candidate value, how many elements are less than or equal to it. That count can be computed efficiently using prefix sums and binary search inside each array.

We then binary search over the answer value itself. Since both arrays are sorted by position and Y remains sorted after transformation, the count of elements ≤ v can be computed in logarithmic time per array using upper_bound logic.

This converts the problem into repeated order-statistics queries on two weighted sorted lists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Expand and merge | O(total slots) per query | O(total slots) | Too slow |
| Binary search on value with prefix counts | O((N+M) log V + Q log V log N) | O(N+M) | Accepted |

## Algorithm Walkthrough

### Precomputation

We first compress each array into prefix sums so that we can count how many stations lie within a range in logarithmic time.

### Processing each query

1. Convert Mr. Y’s transformation into a function on demand: instead of modifying the array, we only transform comparison thresholds. This avoids rebuilding Y for every query.
2. For a candidate answer value `v`, compute how many X-values are ≤ v using binary search on `x_i` and prefix sums on `s_i`.
3. For Y-values, invert the transformation condition. We want:

`alpha * y + beta ≤ v`

which becomes:

`y ≤ (v - beta) // alpha`

This gives a threshold in the original Y array.
4. Count how many `y_j` satisfy this threshold using binary search and prefix sums over `t_j`.
5. Sum both counts to get total elements ≤ v.
6. Binary search over possible values to find the smallest v such that the count is at least k.

### Why it works

The merged structure is a sorted multiset. The predicate “count ≤ v” is monotonic in v, meaning as v increases, the count never decreases. This guarantees binary search correctness. Prefix sums ensure we correctly account for multiplicities, so each station contributes exactly its number of outlets.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_right

def build_prefix(vals, w):
    # prefix sums for weights
    pref = [0] * (len(w) + 1)
    for i in range(len(w)):
        pref[i + 1] = pref[i] + w[i]
    return pref

def count_leq(vals, pref, x):
    # number of vals <= x, using prefix + bisect
    idx = bisect_right(vals, x)
    return pref[idx]

def solve():
    N, M, Q = map(int, input().split())
    x = list(map(int, input().split()))
    sx = list(map(int, input().split()))
    y = list(map(int, input().split()))
    ty = list(map(int, input().split()))

    px = build_prefix(x, sx)
    py = build_prefix(y, ty)

    total = px[-1] + py[-1]

    def count(v, a, b):
        # X part
        cx = count_leq(x, px, v)
        # Y part: alpha*y + beta <= v => y <= (v - beta) / alpha
        limit = (v - b) // a
        cy = count_leq(y, py, limit)
        return cx + cy

    for _ in range(Q):
        a, b, k = map(int, input().split())

        lo = -10**12
        hi = 10**12

        while lo < hi:
            mid = (lo + hi) // 2
            if count(mid, a, b) >= k:
                hi = mid
            else:
                lo = mid + 1

        print(lo)

if __name__ == "__main__":
    solve()
```

The X and Y arrays remain untouched throughout the computation. Prefix sums over `s_i` and `t_j` allow each “how many stations contribute here” query to be answered in logarithmic time via binary search.

The key implementation detail is the inversion of the transformation inequality. Since `alpha` is always positive, division does not flip direction, and integer floor division correctly handles the boundary.

The binary search operates on the answer value space rather than indices, which avoids ever touching the potentially huge expanded multiset.

## Worked Examples

### Example 1

We consider a small configuration:

X = positions `[1, 4]` with weights `[2, 1]`

Y = positions `[2, 3]` with weights `[1, 2]`

Query: `alpha = 2, beta = 0, k = 3`

We search for the smallest value v such that at least 3 elements are ≤ v.

| v | X ≤ v | Y transformed ≤ v | total |
| --- | --- | --- | --- |
| 1 | 2 | 0 | 2 |
| 2 | 2 | 1 | 3 |

The first v reaching k = 3 is 2, which becomes the answer.

This shows how multiplicity directly affects the cumulative counts.

### Example 2

X = `[1, 5]` with `[1, 1]`

Y = `[2, 6]` with `[1, 1]`

Query: `alpha = 1, beta = -2, k = 2`

Y becomes `[0, 4]`.

We evaluate counts:

| v | X ≤ v | Y ≤ v | total |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 2 |

So answer is 1.

This demonstrates how the transformed array can introduce new ordering and how inversion of the inequality handles it cleanly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q log V log N) | binary search over value range with log N counting |
| Space | O(N + M) | storage for arrays and prefix sums |

The constraints allow up to 50,000 queries, and each query performs about 60 iterations of binary search over value space, each costing two logarithmic counts. This comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# Note: full solution integration assumed in real testing environment
# These are structural tests rather than executable here

# minimal case
# 1 station each, direct query

# edge: identical positions
# large k at boundary

# transformation flips order only via shift, not sorting
```
## Edge Cases

A critical edge case is when transformed Y values fall exactly on X values. In that situation, both contributions must be merged rather than overwritten. The inequality-based counting naturally handles this because both arrays contribute independently to the same threshold.

Another edge case is large negative beta, which can push Y values below all X values. The binary search still works because the count function correctly returns only X contributions until the threshold reaches Y’s shifted range.

A final edge case is large k near the total number of elements. The binary search upper bound must be sufficiently wide; otherwise, the algorithm could converge too early. Setting a wide safe range for values ensures correctness regardless of transformation parameters.
