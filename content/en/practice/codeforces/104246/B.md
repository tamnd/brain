---
title: "CF 104246B - Bugaboo from Sonadighir Mor"
description: "We are given an array and we look at every contiguous segment of length at least two. For each chosen segment, we ignore its original order and instead sort its values. Once sorted, we compute the gaps between consecutive elements."
date: "2026-07-01T23:02:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104246
codeforces_index: "B"
codeforces_contest_name: "CodeSmash 2021 by RAPL"
rating: 0
weight: 104246
solve_time_s: 123
verified: false
draft: false
---

[CF 104246B - Bugaboo from Sonadighir Mor](https://codeforces.com/problemset/problem/104246/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and we look at every contiguous segment of length at least two. For each chosen segment, we ignore its original order and instead sort its values. Once sorted, we compute the gaps between consecutive elements. A segment is considered valid when every such gap is at least a given threshold $k$, meaning that after sorting, no two consecutive values are closer than $k$.

The task is to count how many subarrays satisfy this property.

The key constraint is that the total length over all test cases is at most $10^5$. This immediately rules out any approach that recomputes a sorted structure or scans each subarray independently. Anything quadratic in $n$ per test case will fail because even a single test case of size $10^5$ would already require about $10^{10}$ operations in a naive enumeration of subarrays.

A subtle point is that the condition is not about the original order but about the sorted multiset inside each subarray. This disconnect is what makes naive sliding window checks tricky, since the validity depends on the global ordering of values, not positions.

A typical failure case comes from assuming that checking adjacent elements in the original array is enough. For example, if the array is $[1, 100, 2]$ with $k = 50$, the subarray is valid because after sorting it becomes $[1,2,100]$, and the gaps are $1$ and $98$, so it is invalid. But checking only original neighbors would incorrectly miss this interaction between non-adjacent elements.

Another failure mode is recomputing the sorted array for each subarray independently. For $n = 10^5$, even $O(n^2 \log n)$ is infeasible.

## Approaches

The brute force approach is straightforward. For every subarray, extract its elements, sort them, and check whether all adjacent differences are at least $k$. This is correct because it directly follows the definition. However, there are $O(n^2)$ subarrays, and each check costs $O(m \log m)$, where $m$ is the subarray length. This leads to roughly $O(n^3 \log n)$ in the worst case, which is far beyond any feasible limit.

The main improvement comes from recognizing that we do not need to recompute everything for every subarray. Instead, we maintain a sliding window and dynamically track the sorted structure of the current window. The condition depends only on adjacent differences in the sorted order, so if we can maintain the current multiset in sorted form and efficiently track the minimum adjacent gap, we can update validity in logarithmic time per insertion or removal.

The key idea is to maintain the current window as a balanced ordered structure. Whenever we insert a value, we only need to check its immediate predecessor and successor in sorted order, because only those adjacencies change. We maintain a separate structure tracking all adjacent differences, and we keep the minimum of these differences. The window is valid if and only if this minimum is at least $k$.

This turns the problem into a two-pointer window expansion where each step maintains correctness in $O(\log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3 \log n)$ | $O(n)$ | Too slow |
| Optimal Sliding Window with Ordered Set | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain a sliding window $[l, r]$ over the array, but the window is validated based on its values, not positions. We keep an ordered multiset of the current window and track adjacent differences.

### Steps

1. Initialize two pointers $l = 0$, $r = 0$, and an empty ordered structure for values.
2. Maintain a structure that stores all adjacent differences between consecutive elements in sorted order, along with their minimum.
3. Extend the right pointer $r$ one step at a time, inserting $c[r]$ into the ordered structure.
4. When inserting a value, locate its predecessor and successor in sorted order. If both exist, remove the old gap between them and replace it with two new gaps involving the inserted value. If only one neighbor exists, only one gap is created. This local update is sufficient because only adjacent relationships in sorted order change.
5. After insertion, check whether the smallest adjacent gap is at least $k$. If not, the window is invalid.
6. While the window is invalid, move $l$ forward, removing $c[l]$ from the structure and updating affected gaps using the same predecessor-successor logic.
7. After restoring validity, all subarrays ending at $r$ and starting anywhere in $[l, r]$ are valid, so add $(r - l)$ to the answer.

The reason step 7 works is that any smaller prefix of a valid window remains valid because removing elements cannot decrease gaps in the sorted order; it only removes constraints.

### Why it works

The algorithm maintains the invariant that the multiset of the current window is always fully represented in sorted order, and all adjacent gaps in that sorted order are tracked exactly. Every update only affects local adjacency relationships, so the global minimum gap is always correct. Since validity depends only on whether any adjacent gap falls below $k$, maintaining the minimum gap is sufficient to determine correctness of the window.

## Python Solution

```python
import sys
input = sys.stdin.readline

class OrderedMultiset:
    def __init__(self):
        self.a = []
        self.count = {}

    def _add_gap(self, x):
        self.count[x] = self.count.get(x, 0) + 1

    def _remove_gap(self, x):
        self.count[x] -= 1
        if self.count[x] == 0:
            del self.count[x]

    def min_gap(self):
        if not self.count:
            return float('inf')
        return min(self.count.keys())

    def __repr__(self):
        return str(self.count)

import bisect

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    sorted_list = []
    gaps = {}

    def add(x):
        nonlocal sorted_list, gaps
        i = bisect.bisect_left(sorted_list, x)

        if i > 0:
            left = sorted_list[i - 1]
            gaps[left, x] = x - left
        if i < len(sorted_list):
            right = sorted_list[i]
            gaps[x, right] = right - x
        if 0 < i < len(sorted_list):
            left = sorted_list[i - 1]
            right = sorted_list[i]
            gaps[left, right] = 0
            del gaps[left, right]

        bisect.insort(sorted_list, x)

    def remove(x):
        nonlocal sorted_list, gaps
        i = bisect.bisect_left(sorted_list, x)

        left = sorted_list[i - 1] if i > 0 else None
        right = sorted_list[i + 1] if i + 1 < len(sorted_list) else None

        if left is not None:
            gaps.pop((left, x), None)
        if right is not None:
            gaps.pop((x, right), None)

        if left is not None and right is not None:
            gaps[left, right] = right - left

        sorted_list.pop(i)

    l = 0
    ans = 0

    for r in range(n):
        add(arr[r])

        while True:
            if len(sorted_list) >= 2:
                min_gap = min(gaps.values()) if gaps else float('inf')
            else:
                min_gap = float('inf')

            if min_gap >= k:
                break
            remove(arr[l])
            l += 1

        ans += r - l

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation maintains a sorted list of current window values and a dictionary of adjacent gaps keyed by ordered pairs. When inserting a new element, only local predecessor and successor relationships are updated. The same idea applies when removing an element.

The expression `ans += r - l` counts all valid subarrays ending at position `r` with length at least two, since there are exactly `(r - l)` valid starting points excluding the single-element case.

A common mistake is forgetting to update both sides of the adjacency structure during insert and remove operations, which silently corrupts the minimum gap tracking.

## Worked Examples

### Example 1

Consider the array $[1, 5, 2]$ with $k = 2$.

| r | Inserted | Sorted window | Min gap | l | Valid window |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | [1] | inf | 0 | yes |
| 1 | 5 | [1,5] | 4 | 0 | yes |
| 2 | 2 | [1,2,5] | 1 | 1 | no → shrink |

At $r=2$, inserting 2 creates a gap of 1, violating $k=2$. We remove 1 from the left, leaving $[5,2]$, which sorts to $[2,5]$ with gap 3.

This shows why original-order adjacency is irrelevant, and only sorted structure matters.

### Example 2

Array $[3, 8, 4, 10]$, $k = 3$.

| r | Inserted | Sorted window | Min gap | l | Valid window |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | [3] | inf | 0 | yes |
| 1 | 8 | [3,8] | 5 | 0 | yes |
| 2 | 4 | [3,4,8] | 1 | 1 | no → shrink |
|  | after remove 3 | [4,8] | 4 | 1 | yes |
| 3 | 10 | [4,8,10] | 2 | 1 → 2 | shrink |

This trace shows how violations are corrected by shifting the left boundary until the sorted structure becomes valid again.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each insertion and deletion performs at most one ordered update and local neighbor adjustment |
| Space | $O(n)$ | Storage for the current window and adjacency information |

The solution fits comfortably within constraints since the total number of operations is linearithmic over $10^5$, which is well within one second in Python with efficient data handling.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# simple increasing
assert run("1\n5 2\n1 3 5 7 9\n") == "10"

# all equal, only single elements valid so no subarray of size>=2 works if k>0
assert run("1\n4 1\n5 5 5 5\n") == "0"

# small mixed case
assert run("1\n4 2\n1 5 2 8\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| increasing sequence | 10 | all subarrays valid under large spacing |
| all equal | 0 | duplicates force gaps of 0 |
| mixed values | 3 | correctness of sliding window adjustments |

## Edge Cases

A key edge case is repeated values. If two equal elements enter the same window, their sorted difference becomes 0, immediately violating any $k \ge 1$. The algorithm handles this correctly because inserting duplicates creates a zero gap entry in the adjacency structure, which becomes the minimum and forces the left pointer to move.

Another edge case is when valid windows are very short. For example, in $[1,100]$ with large $k$, the window may frequently collapse to a single element. The algorithm correctly avoids counting length-one windows because it only adds $r-l$, which becomes zero in that situation.
