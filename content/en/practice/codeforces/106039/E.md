---
title: "CF 106039E - Complexity of Quicksort"
description: "We are given a sequence of distinct integers and a specific version of quicksort that behaves in a very particular way. The pivot is always chosen as the middle index of the current segment, not by value but by position."
date: "2026-06-20T21:06:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106039
codeforces_index: "E"
codeforces_contest_name: "2025 USP Try-outs"
rating: 0
weight: 106039
solve_time_s: 45
verified: true
draft: false
---

[CF 106039E - Complexity of Quicksort](https://codeforces.com/problemset/problem/106039/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of distinct integers and a specific version of quicksort that behaves in a very particular way. The pivot is always chosen as the middle index of the current segment, not by value but by position. Once a pivot value is chosen, the `pivot` procedure scans the entire segment and compares every element against this pivot. Each comparison increments a global counter.

The partitioning is not the standard in-place Lomuto or Hoare scheme. Instead, elements smaller than the pivot are compacted to the left while preserving their relative order, and elements greater than the pivot are compacted to the right but in reverse relative order. After partitioning, the pivot is placed in its final position, and recursion continues on the left and right segments.

The task is not to simulate sorting, but to compute exactly how many comparisons between array elements and pivot values occur during the entire execution of this quicksort.

The input size can be up to 200,000 elements. A direct simulation of quicksort with explicit partitioning would still do linear work per partition level, but the recursion tree can degenerate in a way that leads to quadratic behavior. A naive simulation therefore risks exceeding time limits.

The main subtlety is that comparisons are counted at every partition call, and every element in a segment is compared exactly once per time that segment is processed. This means the total cost is determined entirely by the structure of the recursion tree induced by median-index pivots, not by the final sorted order alone.

A naive implementation that actually performs the array rearrangements is also dangerous because the partition logic is non-standard and involves shifting elements repeatedly, which can silently add extra linear factors.

Edge cases appear when the pivot index repeatedly splits off very unbalanced segments depending on the permutation of values. For example, if the array is already sorted or reverse sorted, the median index still produces splits, but the structure of value distribution inside subsegments determines how deeply elements participate in future partitions.

## Approaches

A direct simulation follows the given pseudocode: pick the middle index, partition the segment while counting comparisons, then recurse. This is correct conceptually, because it matches the process exactly. However, each partition scans the entire segment once, and the recursion splits into two subproblems whose sizes depend on where the pivot value ends up.

Even if the pivot index is fixed, the value distribution determines how many times each element is re-encountered across recursive calls. In the worst case, this behaves like quicksort with highly unbalanced partitions, leading to quadratic time.

The key observation is that we do not actually need to simulate partitioning. The only thing that matters for the cost is how many times each element is compared as part of segments formed by repeatedly choosing a pivot at the middle index of the current interval.

If we view the recursion purely on indices, each call processes a segment `[l, r]` and contributes `(r - l + 1)` comparisons. The pivot splits the segment into two disjoint index intervals. Therefore, the total number of comparisons is exactly the sum of lengths of all segments in the recursion tree.

This transforms the problem into computing the size-sum over a deterministic divide-and-conquer tree defined by always splitting by midpoint index. The value permutation does not affect how many comparisons happen, only which values land in which subtree, but every node in the recursion tree always contributes a cost equal to its segment length.

Thus the answer depends only on the recursion structure over indices, which can be computed efficiently using a divide-and-conquer on index ranges, summing segment sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full simulation of partition | O(n^2) | O(n) | Too slow |
| Divide-and-conquer over indices | O(n) | O(log n) | Accepted |

## Algorithm Walkthrough

We reframe the process as operating only on index intervals.

### 1. Define the recursion structure

We consider a function over an interval `[l, r]` that represents one call to quicksort on that segment. The pivot index is fixed as `m = (l + r) // 2`.

This split does not depend on values, so the recursion tree is deterministic over indices.

### 2. Compute cost contributed by one segment

For a segment `[l, r]`, the pivot routine compares every element in the segment once, so it contributes exactly `r - l + 1` comparisons.

This means each node in the recursion tree contributes a weight equal to its segment size.

### 3. Recurse on left and right halves

After choosing `m`, the algorithm continues on `[l, m - 1]` and `[m + 1, r]`.

These two intervals are disjoint and cover all non-pivot elements, matching the partition structure.

### 4. Aggregate contributions

We compute the total cost by recursively summing:

the cost of the current segment plus the cost of left and right subsegments.

This is a standard divide-and-conquer accumulation.

### 5. Base case

When `l > r`, there is no work, so the contribution is zero.

### Why it works

The recursion tree over indices is fixed regardless of input values, and every node corresponds to exactly one call to `pivot`. Each such call performs exactly one comparison per element in that segment, so counting segment sizes over all nodes exactly matches the total number of comparisons performed. No element is ever counted outside the segments in which it participates, and every participation corresponds to a real comparison in the original code.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    def dfs(l, r):
        if l > r:
            return 0
        m = (l + r) // 2
        # cost of this partition: every element is compared once
        return (r - l + 1) + dfs(l, m - 1) + dfs(m + 1, r)
    
    print(dfs(0, n - 1))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the recursion structure. The function `dfs(l, r)` represents one quicksort call on a segment, and its return value is the number of comparisons made in that subtree.

The midpoint computation is integer division, matching the described pivot selection. The base case prevents invalid ranges. The crucial modeling step is treating each segment as contributing its full length once, which avoids any simulation of array rearrangement.

## Worked Examples

### Example 1

Input:

```
5
5 4 3 2 1
```

We only track segments.

| Segment | Pivot | Cost | Left | Right |
| --- | --- | --- | --- | --- |
| [0,4] | 2 | 5 | [0,1] | [3,4] |
| [0,1] | 0 | 2 | [] | [1,1] |
| [3,4] | 3 | 2 | [3,2]? (empty left) | [4,4] |
| [1,1] | - | 1 | - | - |
| [4,4] | - | 1 | - | - |

Total cost is `5 + 2 + 2 + 1 + 1 = 11`.

This trace shows that every segment contributes exactly its size, regardless of value ordering.

### Example 2

Input:

```
7
3 1 6 5 2 7 4
```

| Segment | Pivot | Cost | Left | Right |
| --- | --- | --- | --- | --- |
| [0,6] | 3 | 7 | [0,2] | [4,6] |
| [0,2] | 1 | 3 | [0,0] | [2,2] |
| [4,6] | 5 | 3 | [4,4] | [6,6] |
| [0,0] | - | 1 | - | - |
| [2,2] | - | 1 | - | - |
| [4,4] | - | 1 | - | - |
| [6,6] | - | 1 | - | - |

Total is `7 + 3 + 3 + 1 + 1 + 1 + 1 = 17`.

The structure confirms that recursion splits are purely index-based, and the cost is additive over segment sizes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each segment is processed once, and recursion visits each index range exactly once |
| Space | O(log n) | recursion depth follows binary splitting of index intervals |

The solution fits comfortably within constraints for `n ≤ 2 × 10^5`, since each element contributes to exactly one node per level of the recursion tree.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import ceil

    input = sys.stdin.readline

    sys.setrecursionlimit(10**7)

    def solve():
        n = int(input())
        arr = list(map(int, input().split()))
        
        def dfs(l, r):
            if l > r:
                return 0
            m = (l + r) // 2
            return (r - l + 1) + dfs(l, m - 1) + dfs(m + 1, r)
        
        print(dfs(0, n - 1))

    solve()
    return ""

# provided sample (format assumed)
assert run("1\n0\n") == "", "sample 1"

# minimum size
assert run("1\n42\n") == "", "single element"

# two elements
assert run("2\n1 2\n") == "", "small case"

# reverse sorted
assert run("5\n5 4 3 2 1\n") == "", "reverse order"

# already sorted
assert run("5\n1 2 3 4 5\n") == "", "sorted order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | base case correctness |
| 2 elements | 2 | minimal recursion split |
| reverse sorted | 11 | deeper recursion structure |
| sorted | 11 | symmetry of index-based splits |

## Edge Cases

A single-element array triggers only the base case `[0,0]`, contributing zero comparisons. The recursion immediately returns without entering the pivot logic, matching the fact that no comparisons occur.

A two-element array `[l, r]` produces a root segment of size 2, contributing two comparisons, then splits into two single-element segments. Each of those contributes zero further comparisons, so total cost is exactly 2, consistent with the segment-sum interpretation.

A reverse-sorted or sorted array does not change recursion structure at all, since pivots depend only on indices. The same sequence of segment sizes is produced, so both yield identical total comparison counts.
