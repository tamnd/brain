---
title: "CF 104764D - Jelly Swarm"
description: "We are given a set of distinct points on a line, each representing the position of a jellyfish. We must choose exactly K of these points and measure how “spread out” that chosen subset is."
date: "2026-06-28T21:11:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104764
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104764
solve_time_s: 74
verified: false
draft: false
---

[CF 104764D - Jelly Swarm](https://codeforces.com/problemset/problem/104764/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of distinct points on a line, each representing the position of a jellyfish. We must choose exactly K of these points and measure how “spread out” that chosen subset is. The measure of spread is the maximum distance between any two selected points, which is simply the difference between the largest and smallest chosen positions.

The task is to pick K positions so that this range is as small as possible, then output that minimum possible range.

The constraint N up to 2×10^5 immediately rules out any solution that tries all subsets of size K, since that would involve roughly $\binom{N}{K}$ combinations. Even checking all pairs of subsets would explode far beyond feasible limits. Anything worse than O(N log N) or O(N) after sorting is unlikely to pass comfortably.

A subtle point is that the positions are not ordered in input. Any reasoning about intervals depends on sorted order. Another important edge case is when K equals 1. In that case, the answer is always 0 because a single point has no distance to another point.

A common incorrect approach is to assume that choosing points around the median or using some greedy expansion from an arbitrary point is sufficient. For example, if points are `[1, 2, 100, 101, 102]` and K = 3, starting from 100 might suggest `[100, 101, 102]` with range 2, which is optimal, but starting from 2 might incorrectly pick `[1, 2, 100]` giving range 99. Any non-sorted or non-window-based heuristic can easily miss the optimal cluster.

Another failure case appears when clusters are not globally dense but locally dense. For instance `[1, 10, 11, 12, 20]` with K = 3 clearly has optimal window `[10, 11, 12]` with range 2. Any strategy that tries to balance spacing globally will fail here unless it explicitly evaluates contiguous groups in sorted order.

## Approaches

The brute-force idea is straightforward: choose every subset of size K, compute the difference between its maximum and minimum element, and take the minimum. This is correct because it evaluates the exact definition of the problem. However, the number of subsets is enormous. Even for N = 200, the number of combinations is already astronomically large, and here N is 200,000. The brute-force approach degenerates into an infeasible combinatorial explosion.

The key observation is that once the points are sorted, any optimal selection of K points must lie in a contiguous block of the sorted array. If we pick K points that are not contiguous in sorted order, there is always a way to replace a larger gap element with a closer intermediate point and not worsen the answer. This reduces the problem to checking only windows of length K in the sorted array.

So the task becomes scanning all consecutive segments of size K and computing the difference between the last and first element in each segment, then taking the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^K) | O(K) | Too slow |
| Optimal | O(N log N) | O(1) extra (or O(N)) | Accepted |

## Algorithm Walkthrough

1. Sort the array of positions in non-decreasing order. This transforms the problem into a structured line where local segments correspond to candidate clusters. Sorting is necessary because “closeness” is only meaningful when points are ordered.
2. Initialize a variable `answer` with a large value. This will store the best (minimum) range found across all valid groups.
3. Iterate over all indices `i` from `0` to `N - K`. Each `i` defines a window starting at `a[i]` and ending at `a[i + K - 1]`. Every such window represents a candidate group of exactly K jellyfish.
4. For each window, compute the range `a[i + K - 1] - a[i]`. This directly gives the maximum distance between any two points in that group because the array is sorted.
5. Update `answer` with the minimum value encountered across all windows.
6. Output `answer`.

The reason we only consider consecutive windows is that any optimal set of K points can be transformed into a contiguous block without increasing its span. If a chosen set skips an intermediate point, replacing a far endpoint with a closer intermediate one never increases the range.

## Why it works

After sorting, any chosen subset of K elements has a minimum and maximum defined by their positions in the sorted array. If the subset is not contiguous, there exists at least one element between its minimum and maximum that is not included. Swapping a distant chosen element with a closer unchosen element inside the same interval can only reduce or preserve the span. Repeating this process compresses any optimal subset into a contiguous window without increasing its maximum distance. This guarantees that the optimal solution must appear among sliding windows of length K.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    if k == 1:
        print(0)
        return
    
    ans = 10**18
    
    for i in range(n - k + 1):
        ans = min(ans, a[i + k - 1] - a[i])
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The sorting step is essential because without it, the difference between endpoints of a window would not correspond to actual geometric proximity. The loop over `n - k + 1` windows ensures every contiguous group is checked exactly once. The subtraction `a[i + k - 1] - a[i]` captures the full diameter of the window.

A small subtlety is the `k == 1` case, which avoids unnecessary computation and correctly outputs zero. Although the loop would also handle it safely, explicitly returning makes the logic cleaner and avoids edge confusion.

## Worked Examples

### Example 1

Input: `N=5, K=3, a=[8, 6, 15, 5, 10]`

After sorting: `[5, 6, 8, 10, 15]`

| i | Window | Range |
| --- | --- | --- |
| 0 | [5, 6, 8] | 3 |
| 1 | [6, 8, 10] | 4 |
| 2 | [8, 10, 15] | 7 |

Minimum range is 3.

This trace shows how the optimal cluster emerges purely from local density, specifically the first three elements.

### Example 2

Input: `N=7, K=4, a=[1, 2, 4, 5, 6, 7, 9]`

Sorted already.

| i | Window | Range |
| --- | --- | --- |
| 0 | [1, 2, 4, 5] | 4 |
| 1 | [2, 4, 5, 6] | 4 |
| 2 | [4, 5, 6, 7] | 3 |
| 3 | [5, 6, 7, 9] | 4 |

Minimum range is 3.

This demonstrates that the optimal segment may not start at the beginning and requires scanning all windows.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | sorting dominates, sliding window is linear |
| Space | O(1) extra | sorting in-place aside from input storage |

The constraints allow up to 200,000 elements, and O(N log N) sorting plus a single linear scan fits comfortably within typical limits. Memory usage stays linear and only stores the input array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import builtins

    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    if k == 1:
        return "0"

    ans = 10**18
    for i in range(n - k + 1):
        ans = min(ans, a[i + k - 1] - a[i])

    return str(ans)

# provided samples (formatted correctly)
assert run("5 3\n2 8 6 15 5\n") == "3", "sample 1"
assert run("7 4\n1 2 4 5 6 7 9\n") == "3", "sample 2"

# custom cases
assert run("1 1\n100\n") == "0", "single element"
assert run("5 2\n1 100 200 300 400\n") == "99", "small pair window"
assert run("6 3\n1 2 3 100 101 102\n") == "2", "two clusters"
assert run("5 5\n10 20 30 40 50\n") == "40", "all elements chosen"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | K = 1 edge case |
| sparse array pairs | 99 | correct window difference |
| two clusters | 2 | local optimal grouping |
| all elements | 40 | full range selection |

## Edge Cases

For K = 1, consider input `N=4, K=1, a=[10, 100, 1000, 10000]`. After sorting, any single window has zero range. The algorithm immediately returns 0, matching the definition since max minus min over a single element is always zero.

For a tightly clustered group hidden inside sparse values, consider `[1, 2, 3, 100, 101]` with K = 3. The sorted windows produce ranges 2, 98, and 2. The algorithm evaluates each contiguous block and correctly identifies that both `[1,2,3]` and `[100,101,?]` style clusters must be checked, and the minimum remains 2.
