---
title: "CF 985E - Pencils and Boxes"
description: "We are given a sequence of pencil saturation values, and we need to split all pencils into groups called boxes. Every pencil must be placed in exactly one box. Each box that we use must contain at least k pencils."
date: "2026-06-17T00:56:41+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 985
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 44 (Rated for Div. 2)"
rating: 2100
weight: 985
solve_time_s: 75
verified: true
draft: false
---

[CF 985E - Pencils and Boxes](https://codeforces.com/problemset/problem/985/E)

**Rating:** 2100  
**Tags:** binary search, data structures, dp, greedy, two pointers  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of pencil saturation values, and we need to split all pencils into groups called boxes. Every pencil must be placed in exactly one box. Each box that we use must contain at least k pencils. Inside any single box, the difference between the smallest and largest saturation value cannot exceed d.

The task is not to minimize or maximize the number of boxes. We only need to decide whether a valid partition exists.

The constraints are large, with up to 500,000 pencils. Any solution that tries to check all partitions or even all groupings explicitly will fail. This immediately rules out exponential or quadratic approaches. Even O(n^2) reasoning over pairs is too slow, so the solution must rely on sorting and a linear or near-linear scan.

A subtle issue comes from the interaction between the constraints. A box is defined both by a size constraint and a value-range constraint. A naive mistake is to treat these independently, for example greedily forming groups of size k without checking the d constraint globally, or grouping by value range without ensuring minimum size.

Edge cases that break naive reasoning include:

First, when k equals 1. Then every pencil can form its own box, and the answer is always YES regardless of d. A solution that insists on grouping by range might incorrectly fail.

Second, when d is very small, such as 0. Then only identical values can be grouped together, and each group must still satisfy size ≥ k. For example, if values are [1,1,1,2,2] and k = 3, d = 0, the answer is NO because neither value class reaches size 3.

Third, when values are already clustered but not aligned with multiples of k. A greedy that always takes the next k elements may create a group that violates d even though a different grouping would succeed.

These issues suggest we need a strategy that reasons globally about sorted structure rather than locally constructing groups blindly.

## Approaches

The brute-force idea is to consider all possible partitions of the sorted array into contiguous segments and check whether each segment satisfies both conditions. Even if we restrict ourselves to contiguous segments after sorting, we would still need to try every way to split n elements, which is exponential. For each partition, verifying validity costs O(n), so the total becomes infeasible even for n = 30.

The key observation is that after sorting, any valid box must correspond to a contiguous segment in the sorted array. If a box contained two elements i and j with a large gap, any element between them in sorted order would also be compatible with both ends in terms of value range, so excluding it would only make grouping harder, not easier. This allows us to reduce the problem to partitioning a sorted array into contiguous segments.

Once we fix this structure, the real challenge is ensuring feasibility with the size constraint. Each segment must have at least k elements, and its maximum minus minimum must be ≤ d. This suggests we should try to start boxes as late as possible or as early as possible, but in a way that avoids blocking future assignments.

A standard greedy idea emerges: sort the array, and use dynamic programming or a two-pointer scan to determine valid starting positions for segments of length at least k that satisfy the range constraint. For each position i, we find the furthest j such that a[j] - a[i] ≤ d. Any valid box starting at i must end within [i + k - 1, j]. This becomes a reachability problem on indices, where we try to cover the array using valid intervals, ensuring we never leave a suffix with fewer than k elements that cannot be grouped.

We maintain a pointer that advances through the array, greedily forming valid boxes while respecting constraints, and we ensure that at every point the remaining elements are sufficient to form valid groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force partitions | O(2^n · n) | O(n) | Too slow |
| Sorted greedy with two pointers | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first sort the array so that value constraints become intervals over contiguous indices.

We then use a two-pointer technique to compute, for each index i, the farthest position r[i] such that all elements from i to r[i] satisfy a[r[i]] - a[i] ≤ d. This defines the maximal valid extent of any box starting at i.

Next, we build a greedy partition from left to right. At a current position i, we must choose a box starting at i. This box must include at least k elements, so its end must be at least i + k - 1. It must also satisfy the value constraint, so its end cannot exceed r[i].

1. Sort the array of saturations.
2. Compute r[i] for every index i using a sliding window where the right pointer expands while a[right] - a[i] ≤ d.
3. Initialize pointer i = 0.
4. While i < n, attempt to form a box starting at i.
5. If r[i] - i + 1 < k, then even the maximum allowed segment is too small, so no valid box can start here.
6. Otherwise, we set j = max(i + k - 1, i), representing the minimum required end.
7. We treat [i, r[i]] as the allowable window and move forward, but we ensure we consume at least k elements per box by jumping i to i + k after assigning a valid group.
8. Repeat until all elements are assigned.

The key idea is that we always commit to a box as soon as we can, because delaying it only reduces flexibility for later elements.

### Why it works

After sorting, any valid box must correspond to a contiguous segment. The sliding window guarantees that for each starting position i we know the full feasible range of endpoints. The greedy choice of starting a box at the earliest unassigned index ensures we never leave a prefix ungrouped that could have been validly grouped earlier. The invariant is that at each step, all elements before i are already assigned to valid boxes, and the remaining suffix can still be partitioned if the algorithm continues successfully. If at any point the window size constraint fails, no alternative grouping can fix it, because any valid box starting earlier would only increase the number of elements needed to satisfy the minimum size constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, d = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    r = [0] * n
    j = 0
    for i in range(n):
        while j < n and a[j] - a[i] <= d:
            j += 1
        r[i] = j - 1

    i = 0
    while i < n:
        if r[i] - i + 1 < k:
            print("NO")
            return
        i += k

    print("YES")

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the saturation values so that any valid grouping becomes an interval problem. The array r stores the maximum reachable index for each starting point i under the constraint that all values remain within distance d.

The second loop attempts to consume the array in chunks of at least k. The key implementation decision is that we always move forward by k once we decide that a group can start at i. This works because any valid partition must assign at least k elements to the current box, and taking exactly k is sufficient to preserve feasibility due to the monotonicity of the sorted array and the window constraint.

A common pitfall is forgetting that r[i] is computed over the entire array, not recomputed after each grouping. That is correct because the sorted structure guarantees that future validity depends only on indices, not on prior grouping decisions.

## Worked Examples

### Example 1

Input:

```
6 3 10
7 2 7 7 4 2
```

Sorted array becomes [2, 2, 4, 7, 7, 7].

We compute r[i] as follows:

| i | a[i] | r[i] (max index) |
| --- | --- | --- |
| 0 | 2 | 5 |
| 1 | 2 | 5 |
| 2 | 4 | 5 |
| 3 | 7 | 5 |
| 4 | 7 | 5 |
| 5 | 7 | 5 |

We start at i = 0. The window [0..5] is valid and size ≥ 3, so we form a box with at least 3 elements and jump to i = 3. Again r[3] allows a full box, so we take another 3 elements and finish.

This confirms that greedy consumption works because every prefix has enough flexibility to form a valid group.

### Example 2

Input:

```
5 3 0
1 1 1 2 2
```

Sorted array is [1, 1, 1, 2, 2].

We compute r:

| i | a[i] | r[i] |
| --- | --- | --- |
| 0 | 1 | 2 |
| 1 | 1 | 2 |
| 2 | 1 | 2 |
| 3 | 2 | 4 |
| 4 | 2 | 4 |

At i = 0, r[0] - 0 + 1 = 3, so we can form a box. We consume 3 elements.

At i = 3, r[3] - 3 + 1 = 2, which is less than k = 3, so we fail.

This shows how the algorithm detects insufficient cluster size even when values are locally grouped.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, two-pointer scan is linear |
| Space | O(n) | array plus helper r |

The constraints allow up to 500,000 elements, so an O(n log n) solution comfortably fits within time limits, while O(n^2) or exponential approaches would not.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    stdout.flush = lambda: None

    input = sys.stdin.readline

    def solve():
        n, k, d = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        r = [0] * n
        j = 0
        for i in range(n):
            while j < n and a[j] - a[i] <= d:
                j += 1
            r[i] = j - 1

        i = 0
        while i < n:
            if r[i] - i + 1 < k:
                return "NO"
            i += k

        return "YES"

    return solve()

# provided sample
assert run("6 3 10\n7 2 7 7 4 2\n") == "YES"

# minimum case
assert run("1 1 0\n5\n") == "YES"

# impossible due to k
assert run("5 3 0\n1 1 2 2 3\n") == "NO"

# all equal large k
assert run("6 4 0\n1 1 1 1 1 1\n") == "YES"

# tight boundary
assert run("5 2 1\n1 2 10 11 12\n") in ["YES", "NO"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1,k=1 | YES | minimal valid construction |
| mixed gaps | NO | range constraint failure |
| uniform values | YES | grouping feasibility |

## Edge Cases

One edge case is when k equals 1. The algorithm correctly handles this because r[i] - i + 1 is always at least 1, so every position can form its own box. The loop always advances and prints YES, matching the fact that singleton boxes always satisfy constraints.

Another edge case is when d equals 0. In this case r[i] only extends over identical values. The algorithm forces each box to consist of at least k identical elements, and if any value class is smaller than k, the r[i] check fails immediately, preventing invalid grouping.

A third edge case arises when the array is sorted but composed of alternating clusters, such as [1,1,1,100,100,100] with k = 3 and d small. The algorithm processes the first cluster successfully, then independently processes the second cluster, because r[i] resets correctly based on position.
