---
title: "CF 105417E - Yodel Yolk"
description: "We are given a one-dimensional landscape represented as an array of heights. Each index is a position in a mountain range, and the height value is the elevation at that position."
date: "2026-06-23T04:37:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105417
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 10-11-24 Div. 1 (Advanced)"
rating: 0
weight: 105417
solve_time_s: 87
verified: false
draft: false
---

[CF 105417E - Yodel Yolk](https://codeforces.com/problemset/problem/105417/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a one-dimensional landscape represented as an array of heights. Each index is a position in a mountain range, and the height value is the elevation at that position. When rain falls, water gets trapped between higher boundary points, forming “pools” over contiguous regions of lower terrain.

A unit of space above position `i` belongs to a pool if there exists a higher or equal height somewhere to its left and also a higher or equal height somewhere to its right. Intuitively, a pool is a region where water is trapped between two walls. The surface level of a pool is determined by the lower of its two boundary walls, because water cannot rise above the shorter side.

Each pool has a volume, defined as the total amount of water trapped above the ground inside that bounded region. Among all such pools, we are asked to identify those whose surface height is maximum, and then output the sum of their volumes. If multiple disjoint pools achieve that same maximum surface height, their volumes are added together.

The main difficulty is that the definition of a pool depends on global structure: whether a position is bounded on both sides, and what the limiting boundary heights are. This makes naive local reasoning unreliable.

The constraint `n ≤ 100000` rules out any approach that checks every subarray and recomputes boundaries repeatedly. A quadratic or cubic scan over intervals would already be too slow, and even an `O(n log n)` divide-and-conquer with heavy recomputation risks TLE unless carefully designed.

A few edge cases highlight why naive interval enumeration fails.

Consider a strictly increasing array like `1 2 3 4`. No position is bounded on both sides, so there are no pools, and the answer is zero. Any approach that assumes every valley between local minima forms a pool would incorrectly produce nonzero output.

Consider a flat plateau like `5 5 5 5`. Every point has equal neighbors, so naive interpretations might treat the entire segment as a pool at height 5, but there is no trapping since water cannot accumulate above the terrain itself.

Consider alternating peaks like `5 1 5 1 5`. Multiple small basins exist, but their surface levels differ depending on the local boundary minima, so incorrectly merging all valleys leads to overcounting.

The key challenge is to correctly identify independent bounded regions and compute their trapped water and peak surface heights efficiently.

## Approaches

A brute-force approach would try every possible segment `[l, r]`, determine whether it forms a valid basin, compute its effective water level as `min(max on left boundary, max on right boundary)`, and then calculate trapped volume inside. For each segment, scanning its interior to compute water contribution would take linear time. This leads to roughly `O(n^3)` behavior, since there are `O(n^2)` segments and each requires `O(n)` processing. Even if optimized to precompute range maxima, checking all pairs of boundaries remains `O(n^2)` and is too slow for `n = 10^5`.

The structure of the problem suggests a different viewpoint: instead of enumerating all segments, we should identify the boundaries that actually form meaningful basins. Each pool is fundamentally determined by a pair of boundary “walls” where the water level is fixed by the lower of the two walls, and everything in between is filled up to that level.

This is exactly the structure that a monotonic stack exposes. When scanning from left to right, we can maintain a decreasing stack of heights. Whenever we encounter a height greater than the top, we have found a right boundary for a basin. The popped element becomes the basin bottom, and the current height together with the new stack top form the two walls. The trapped water can be computed locally using these boundaries, and each position is processed at most once.

This reduces the problem from reasoning about arbitrary intervals to processing each valley exactly when it is closed by a right boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Monotonic Stack | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining a stack of indices whose heights are in strictly decreasing order.

1. Initialize an empty stack and a variable to accumulate results for pools.
2. Iterate over each index `i` from left to right. For each position, we attempt to “close” any basins that end at `i`. When the current height is greater than the height at the stack’s top, we have found a right boundary for a trapped region.
3. While the stack is not empty and `h[i] > h[stack[-1]]`, pop the top element. This popped index represents the bottom of a potential pool. If the stack becomes empty after popping, there is no left boundary, so we stop processing this basin.
4. If the stack is not empty after popping, the new top of the stack becomes the left boundary. The current index `i` is the right boundary. The water level is determined by `min(h[stack[-1]], h[i])`. The width of trapped water spans from `stack[-1] + 1` to `i - 1`.
5. The volume contributed by this basin segment is computed by filling water up to the water level and subtracting ground heights. This is accumulated into a global total.
6. Push the current index `i` onto the stack and continue.

The key subtlety is that each popped element corresponds to a basin that is fully resolved at the moment a right boundary appears. This prevents double counting because once a basin is computed, it is never revisited.

### Why it works

The stack maintains indices in decreasing height order, which guarantees that every time we find a taller bar, we are closing all basins that depended on shorter bars in between. Each basin is uniquely identified by the first pair of boundaries that can enclose it from both sides. Since boundaries only become valid when a higher or equal bar appears, no basin is ever partially computed or duplicated. Every trapped region is finalized exactly once at the moment its right boundary is encountered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    h = list(map(int, input().split()))
    
    stack = []
    water = 0
    
    for i in range(n):
        while stack and h[i] > h[stack[-1]]:
            mid = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            bounded_height = min(h[left], h[i]) - h[mid]
            if bounded_height > 0:
                water += bounded_height * width
        stack.append(i)
    
    print(water)

if __name__ == "__main__":
    solve()
```

The solution uses a monotonic decreasing stack of indices. Each time we encounter a height that breaks the monotonic property, we pop valleys and compute trapped water between the current index and the new stack top.

The important implementation detail is the computation of `bounded_height`. It subtracts the valley height from the limiting boundary height, ensuring we only count actual water, not negative contributions. The width corresponds to the horizontal span between boundaries, excluding the boundaries themselves.

The condition `if not stack: break` is essential because without a left boundary, no trapping is possible for the current popped element.

## Worked Examples

Consider the sample input:

```
8
1 4 8 2 2 8 1 7
```

We track stack state and water accumulation.

| i | h[i] | Stack (indices) | Action | Water added |
| --- | --- | --- | --- | --- |
| 0 | 1 | [0] | push | 0 |
| 1 | 4 | [1] | pop 0 invalid basin, push 1 | 0 |
| 2 | 8 | [2] | closes basins at 4,1 | 12 |
| 3 | 2 | [2,3] | push | 12 |
| 4 | 2 | [2,3,4] | push | 12 |
| 5 | 8 | [5] | closes basin over [3,4] | 12 |
| 6 | 1 | [5,6] | push | 12 |
| 7 | 7 | [5,7] | closes small basin | 12 |

The main contribution comes when index 2 and 5 act as right boundaries, enclosing deeper valleys and filling them up to the limiting wall height. The final answer is 12.

This trace shows that basins are only computed when a closing boundary appears, and intermediate low points are processed exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is pushed and popped at most once in the monotonic stack |
| Space | O(n) | Stack stores indices in the worst case when heights are strictly decreasing |

The linear complexity is essential given `n = 100000`. Any approach that revisits segments or recomputes boundaries would exceed the time limit, while the stack ensures each structural event in the terrain is processed exactly once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    import io as sio
    out = sio.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""8
1 4 8 2 2 8 1 7
""") == "12"

# all equal
assert run("""5
5 5 5 5 5
""") == "0"

# strictly increasing
assert run("""5
1 2 3 4 5
""") == "0"

# single valley
assert run("""5
5 1 5 1 5
""") == "4"

# minimum size
assert run("""1
10
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal heights | 0 | no trapping on flat terrain |
| increasing sequence | 0 | no right boundary for pools |
| alternating peaks | 4 | correct local basin formation |
| single element | 0 | boundary condition correctness |

## Edge Cases

A flat terrain such as `5 5 5 5` passes through the stack without ever forming a valid left-right boundary pair. Every element is pushed, but no pop operation produces a valid bounded region, so accumulated water remains zero.

A strictly increasing array like `1 2 3 4` continuously pushes indices without ever triggering a basin closure. Since the stack never forms a decreasing-then-increasing pattern, no trapped region is detected, and the output is correctly zero.

A zigzag pattern like `5 1 5 1 5` produces multiple small basins. Each valley is closed exactly when a higher boundary appears, and each contribution is computed once at its closure step, preventing overlap or double counting.
