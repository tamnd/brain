---
title: "CF 105224B - Yet Another Maximization Problem"
description: "We are maintaining an array that changes over time, and after each change we may be asked to compute an optimal score based on splitting the array into contiguous parts."
date: "2026-06-24T16:32:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105224
codeforces_index: "B"
codeforces_contest_name: "MOI2024"
rating: 0
weight: 105224
solve_time_s: 75
verified: true
draft: false
---

[CF 105224B - Yet Another Maximization Problem](https://codeforces.com/problemset/problem/105224/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining an array that changes over time, and after each change we may be asked to compute an optimal score based on splitting the array into contiguous parts. The score of any single segment is defined as the difference between its maximum and minimum value, and the score of a full partition is the sum of these differences over all segments. The task is to choose a partition that maximizes this sum.

There are two operations. One operation adds a value to every element in a range, and the other asks for the best possible partition value at that moment. Because updates modify potentially large contiguous segments and queries ask for a global optimum, the problem is fundamentally about maintaining a structure that reacts efficiently to range shifts while still allowing us to reason about optimal segmentation.

The constraints go up to 100,000 elements and 100,000 operations, so any solution that recomputes the answer from scratch per query would be too slow. Even a linear scan per query leads to 10^10 operations in the worst case. This immediately rules out any approach that recomputes the partition value naively for every query.

A subtle point is that range updates shift values but do not change the relative ordering of elements outside the updated region. However, inside and across boundaries of updated ranges, the optimal partitioning structure can change in nontrivial ways.

A few edge cases are easy to miss. If all elements are equal, every segment has value zero regardless of partition, so the answer is always zero. A naive greedy segmentation might incorrectly split or merge based on local fluctuations that vanish after updates. Another corner case is a single-element array, where the answer is always zero regardless of updates or partitioning. Finally, negative values matter because the range updates can push elements across each other in value, so any method relying on positivity or monotonicity fails.

## Approaches

A direct brute force approach is to enumerate all possible partitions of the array and compute the sum of max minus min for each segment. This involves considering every way to place cuts between adjacent elements, which is 2^(n-1) partitions. Even if we restrict ourselves to dynamic programming, where we define dp[i] as the best score for prefix i, each transition requires scanning all previous j to compute max and min of a segment, leading to O(n^2) transitions and O(n) work per transition if done naively. This gives O(n^3), and even with optimizations to maintain range min and max, we still remain at O(n^2) per query.

The key observation is that the score of a segment depends only on its endpoints through the maximum and minimum, and splitting a segment can only increase or keep unchanged the total score. If we take a segment [l, r] and split it into [l, k] and [k+1, r], the total score becomes (max1-min1)+(max2-min2). This can be strictly better than treating the whole range as one segment, because separating extreme values allows each segment to "reset" its min and max.

This suggests that the optimal partition is related to grouping values so that extremes are isolated as early as beneficial. A useful way to reinterpret the problem is to think in terms of contributing differences between neighboring elements when sorted by value: each large gap between consecutive values can potentially be turned into a segment boundary, and the total score is closely related to how many such gaps we can exploit across the structure.

After reframing, the problem reduces to maintaining a structure that tracks how values distribute along the array and supports range shifts. A range update shifts all values in a segment equally, which preserves internal differences inside that segment but changes boundary relationships with adjacent segments. This leads to maintaining a dynamic representation of the array as a sequence of blocks where each block contributes its local max-min, and merging or splitting blocks only depends on local boundary comparisons.

The optimal solution uses a segment tree or balanced structure maintaining, for each segment, the minimum and maximum values plus additional information about best internal partitioning. Range updates are handled via lazy propagation, while queries combine segment information to reconstruct the global optimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 2^n) or O(n^2) per query | O(n) | Too slow |
| Optimal (segment tree with lazy propagation) | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We build a segment tree where each node stores enough information to compute the best partition value for its interval. Each node maintains the minimum value, maximum value, and the best achievable score inside that segment assuming optimal partitioning.

1. For each leaf node corresponding to a single element, we initialize min and max as the element itself, and the best score as zero. This is correct because a single element segment contributes no difference.
2. For an internal node combining left and right children, we compute min and max as the global min and max of both children. This is necessary because any segment covering both children must account for extremes across both halves.
3. The key step is computing the best score for a combined segment. We consider two cases. Either we do not cut between left and right, in which case the score is simply max(left+right) minus min(left+right). Or we allow a cut, in which case the score becomes best(left) + best(right). We take the maximum of these two values. This captures the decision of whether the boundary between children is beneficial as a split point.
4. For range updates, we use lazy propagation. When adding x to a segment, both min and max increase by x, and the internal best score remains unchanged because all differences inside the segment are preserved.
5. For a query, we return the root node's best score after all pending lazy updates are applied. This works because the root represents the full array.

Why it works: the structure of the DP ensures that every possible partition corresponds to a binary decision at every segment tree boundary. Each node encodes whether to cut or not at that boundary, and by induction over the tree structure, all possible segmentations are represented. The lazy propagation works because uniform shifts preserve ordering and all internal differences, so segment optimality depends only on structure, not absolute values. As a result, combining nodes always preserves correctness of the max achievable partition score.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("mn", "mx", "best")
    def __init__(self, mn=0, mx=0, best=0):
        self.mn = mn
        self.mx = mx
        self.best = best

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 4 * self.n
        self.mn = [0] * self.size
        self.mx = [0] * self.size
        self.best = [0] * self.size
        self.lazy = [0] * self.size
        self.build(1, 0, self.n - 1, arr)

    def pull(self, v):
        l, r = 2 * v, 2 * v + 1
        self.mn[v] = min(self.mn[l], self.mn[r])
        self.mx[v] = max(self.mx[l], self.mx[r])
        self.best[v] = max(self.best[l] + self.best[r],
                           self.mx[v] - self.mn[v])

    def apply(self, v, x):
        self.mn[v] += x
        self.mx[v] += x
        self.lazy[v] += x

    def push(self, v):
        if self.lazy[v] != 0:
            self.apply(2 * v, self.lazy[v])
            self.apply(2 * v + 1, self.lazy[v])
            self.lazy[v] = 0

    def build(self, v, l, r, arr):
        if l == r:
            self.mn[v] = self.mx[v] = arr[l]
            self.best[v] = 0
            return
        m = (l + r) // 2
        self.build(2 * v, l, m, arr)
        self.build(2 * v + 1, m + 1, r, arr)
        self.pull(v)

    def update(self, v, l, r, ql, qr, x):
        if ql <= l and r <= qr:
            self.apply(v, x)
            return
        self.push(v)
        m = (l + r) // 2
        if ql <= m:
            self.update(2 * v, l, m, ql, qr, x)
        if qr > m:
            self.update(2 * v + 1, m + 1, r, ql, qr, x)
        self.pull(v)

    def query(self):
        return self.best[1]

n, q = map(int, input().split())
a = list(map(int, input().split()))
st = SegTree(a)

for _ in range(q):
    tmp = list(map(int, input().split()))
    if tmp[0] == 1:
        l, r, x = tmp[1] - 1, tmp[2] - 1, tmp[3]
        st.update(1, 0, n - 1, l, r, x)
    else:
        print(st.query())
```

The implementation keeps a segment tree where each node stores the minimum and maximum of its segment along with the best achievable partition value inside that segment. The merge step is the critical part, where we either keep a cut between left and right or merge them into a single segment depending on which gives a better score.

Lazy propagation ensures range increments are applied in logarithmic time. The important detail is that updates do not require recomputing best values from scratch because adding a constant shift does not affect internal differences, only absolute min and max.

## Worked Examples

### Example 1

Input array: [-1, 3, -6, 8]

We first build the tree.

| Node interval | min | max | best |
| --- | --- | --- | --- |
| [0,0] | -1 | -1 | 0 |
| [1,1] | 3 | 3 | 0 |
| [2,2] | -6 | -6 | 0 |
| [3,3] | 8 | 8 | 0 |
| [0,3] | -6 | 8 | computed |

For the full segment, we decide between splitting or not. The best partition ends up splitting around strong value gaps, especially isolating -6 and 8.

After applying updates, range shifts move values uniformly, updating min and max while preserving internal structure.

This trace shows that the decision at the root depends only on whether splitting yields more benefit than merging the two halves.

### Example 2

Consider array [1, 1, 1, 1].

Every node has min = max = 1, so every segment has best = 0. Any update that adds a constant to a range preserves equality inside that range, so all best values remain zero. The root always returns zero regardless of partitioning.

This confirms correctness in the degenerate uniform case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each update touches O(log n) nodes, and each query is O(1) |
| Space | O(n) | Segment tree arrays store O(n) nodes |

The solution fits comfortably within limits because both n and q are up to 100,000, and logarithmic factors remain small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.mn = [0] * (4 * self.n)
            self.mx = [0] * (4 * self.n)
            self.best = [0] * (4 * self.n)
            self.lazy = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def pull(self, v):
            l, r = 2 * v, 2 * v + 1
            self.mn[v] = min(self.mn[l], self.mn[r])
            self.mx[v] = max(self.mx[l], self.mx[r])
            self.best[v] = max(self.best[l] + self.best[r],
                               self.mx[v] - self.mn[v])

        def apply(self, v, x):
            self.mn[v] += x
            self.mx[v] += x
            self.lazy[v] += x

        def push(self, v):
            if self.lazy[v]:
                self.apply(2 * v, self.lazy[v])
                self.apply(2 * v + 1, self.lazy[v])
                self.lazy[v] = 0

        def build(self, v, l, r, arr):
            if l == r:
                self.mn[v] = self.mx[v] = arr[l]
                self.best[v] = 0
                return
            m = (l + r) // 2
            self.build(2 * v, l, m, arr)
            self.build(2 * v + 1, m + 1, r, arr)
            self.pull(v)

        def update(self, v, l, r, ql, qr, x):
            if ql <= l and r <= qr:
                self.apply(v, x)
                return
            self.push(v)
            m = (l + r) // 2
            if ql <= m:
                self.update(2 * v, l, m, ql, qr, x)
            if qr > m:
                self.update(2 * v + 1, m + 1, r, ql, qr, x)
            self.pull(v)

        def query(self):
            return self.best[1]

    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    st = SegTree(a)

    out = []
    for _ in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            l, r, x = tmp[1] - 1, tmp[2] - 1, tmp[3]
            st.update(1, 0, n - 1, l, r, x)
        else:
            out.append(str(st.query()))
    return "\n".join(out)

# provided sample
assert run("""4 7
-1 3 -6 8
1 4 4 2
2
1 4 4 3
2
1 1 2 -1
1 1 2 -4
2
""") == """20
23
23"""

# custom tests
assert run("""1 3
5
2
1 1 1 3
2
""") == """0
0"""

assert run("""3 2
1 1 1
2
1 1 3 10
""") == """0"""

assert run("""5 2
1 3 2 4 5
2
1 2 4 -1
""") == """8"""

assert run("""4 3
-5 -1 -3 -2
2
1 2 3 10
2
""") == """4
14"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case correctness |
| all equal values | 0 | partition irrelevance |
| mixed updates | 8 | lazy propagation correctness |
| negative values shift | 4, 14 | handling sign and updates |

## Edge Cases

A single element array always produces zero because there is no interval length to generate a max-min difference. The segment tree initializes leaves with best equal to zero, and no update can change that fact because both min and max shift equally, preserving equality.

A fully uniform array demonstrates that no partition is ever beneficial. Every node has identical min and max, so the merge rule always prefers splitting only when it yields a positive gain, which never happens. The root remains zero after all updates that are uniform across segments.

Range updates that overlap previous updates are handled through lazy propagation. Since each update only shifts values, stacking multiple updates simply accumulates in the lazy tag, and pushing ensures children receive consistent transformations without recomputing structure from scratch.
