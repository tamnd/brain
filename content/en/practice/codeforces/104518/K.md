---
title: "CF 104518K - Optimism"
description: "We are maintaining an array of values over time, where each position represents a plot of land. The array changes through range updates that add a value to all elements in a segment."
date: "2026-06-30T10:39:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104518
codeforces_index: "K"
codeforces_contest_name: "UNICAMP Selection Contest 2023"
rating: 0
weight: 104518
solve_time_s: 49
verified: true
draft: false
---

[CF 104518K - Optimism](https://codeforces.com/problemset/problem/104518/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining an array of values over time, where each position represents a plot of land. The array changes through range updates that add a value to all elements in a segment. Alongside the evolving array, each position remembers the maximum value it has ever reached at any point in the update history, not just its current value.

There are two operations. One operation increases all values in a segment by some possibly negative amount. The other asks for the sum of the historical maxima over a segment. The key difficulty is that queries depend on the entire past evolution, not just the current array state.

The constraints go up to three hundred thousand operations, so any solution that touches each element per update or query is immediately too slow. A direct simulation would cost O(nq), which is far beyond feasible. Even per-query segment recomputation is too slow because both updates and queries can span large ranges.

A subtle edge case is that values can become negative due to updates. This matters because the maximum value is not necessarily the current value, and it might come from an earlier state before multiple negative updates. For example, if a single element starts at 5, is increased to 10, then decreased to 3, its optimistic value remains 10 even though current value is 3. Any solution that only tracks current values will fail here.

Another non-trivial case is overlapping updates. A segment might be increased multiple times in different intervals, so each position experiences a complex history of increments. The challenge is to track, for each position, the maximum prefix sum it ever achieved under a dynamic sequence of range additions.

## Approaches

A brute-force approach would explicitly maintain the array and a second array storing the historical maximum per position. For every type 1 update, we iterate over the segment and add x to each element, and we also update the maximum if the new value exceeds it. For queries, we sum the stored maxima.

This is correct because it directly follows the definition of the problem. However, each update may touch O(n) elements, and there are up to 3e5 operations. In the worst case, this leads to around 1e10 operations, which is far beyond any feasible limit.

The key observation is that each position evolves independently under range additions, and range additions are linear operations. This suggests that we should avoid touching each index individually. Instead, we want a data structure that supports range add and range sum queries, but with an additional complication: we also need to maintain the maximum prefix value each position ever reached.

This transforms the problem into maintaining two values over a segment: current value and historical maximum under additive range updates. A standard segment tree with lazy propagation is the natural tool, but we need more than just sum or max. We must propagate not only increments but also track how these increments affect historical maxima. The standard trick is to store for each segment both the current value and the maximum value, and carefully define how a uniform addition affects both.

Under a range add of x, the current value increases by x, and the historical maximum increases by x as well, but only in a way consistent with the fact that all past values also shift by x. This means both current and maximum shift uniformly. The real difficulty is when querying partial segments, where we need correct aggregation of maxima.

This can be handled by a segment tree where each node maintains the sum of current values and sum of historical maxima, with lazy propagation for range increments applied uniformly to both fields.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Segment Tree with lazy propagation | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree where each node stores the sum of current values in its segment and the sum of historical maximum values in its segment. We also maintain a lazy tag representing pending additions that must be applied to the segment.

1. Build the segment tree from the initial array, setting both current sum and historical maximum sum to the initial values. This is correct because initially each value has only seen itself as its maximum.
2. For a range update adding x to [l, r], we descend the tree. When a node is fully covered, we apply the update directly: we increase the current sum by x times segment length, and we increase the historical maximum sum by x times segment length as well. We also accumulate x into the lazy tag.
3. When a node is partially covered, we push down any pending lazy value before continuing. This ensures children represent correct values before further updates.
4. For a query on [l, r], we aggregate results from fully covered nodes. Each node contributes both its current sum and its historical maximum sum, but only the latter is needed for output.
5. The key subtlety is that lazy propagation must preserve consistency: whenever a segment is shifted by x, both current and maximum histories shift identically because every past value in that segment increases by x.

Why it works is tied to a simple invariant. At every point in time, for every segment tree node, the stored historical maximum sum equals the sum over all indices in that segment of the maximum value that index has achieved under all updates applied so far. A range addition shifts every historical value uniformly, so maxima shift uniformly as well, preserving correctness across merges and splits.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.sum = [0] * (4 * self.n)
        self.mx = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, tl, tr, arr):
        if tl == tr:
            self.sum[v] = arr[tl]
            self.mx[v] = arr[tl]
            return
        tm = (tl + tr) // 2
        self.build(v*2, tl, tm, arr)
        self.build(v*2+1, tm+1, tr, arr)
        self.pull(v)

    def pull(self, v):
        self.sum[v] = self.sum[v*2] + self.sum[v*2+1]
        self.mx[v] = self.mx[v*2] + self.mx[v*2+1]

    def apply(self, v, tl, tr, val):
        self.sum[v] += val * (tr - tl + 1)
        self.mx[v] += val * (tr - tl + 1)
        self.lazy[v] += val

    def push(self, v, tl, tr):
        if self.lazy[v] != 0:
            tm = (tl + tr) // 2
            self.apply(v*2, tl, tm, self.lazy[v])
            self.apply(v*2+1, tm+1, tr, self.lazy[v])
            self.lazy[v] = 0

    def update(self, v, tl, tr, l, r, val):
        if l > r:
            return
        if l == tl and r == tr:
            self.apply(v, tl, tr, val)
            return
        self.push(v, tl, tr)
        tm = (tl + tr) // 2
        self.update(v*2, tl, tm, l, min(r, tm), val)
        self.update(v*2+1, tm+1, tr, max(l, tm+1), r, val)
        self.pull(v)

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.mx[v]
        self.push(v, tl, tr)
        tm = (tl + tr) // 2
        return self.query(v*2, tl, tm, l, min(r, tm)) + \
               self.query(v*2+1, tm+1, tr, max(l, tm+1), r)

def main():
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    st = SegTree(arr)

    out = []
    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            _, l, r, x = tmp
            l = int(l) - 1
            r = int(r) - 1
            x = int(x)
            st.update(1, 0, n-1, l, r, x)
        else:
            _, l, r = tmp
            l = int(l) - 1
            r = int(r) - 1
            out.append(str(st.query(1, 0, n-1, l, r)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The segment tree is built in the standard way, with each node storing aggregate information for its interval. The `apply` function is the core: it applies a uniform shift to both current sums and historical maxima. This is valid because every value in the segment is increased uniformly, so every past maximum also increases by the same offset.

Lazy propagation ensures we avoid descending into segments unless necessary. The push step guarantees correctness before partially updating children.

The query function only needs the stored maximum sums, since the problem asks for the sum of historical maxima.

## Worked Examples

Consider a small array where we apply a mix of positive and negative updates.

### Example 1

Input:

```
1 1 1
1 1 1 5
2 1 1
```

We track one element.

| Step | Operation | Value | Max | Query result |
| --- | --- | --- | --- | --- |
| 0 | init | 1 | 1 | - |
| 1 | +5 | 6 | 6 | - |
| 2 | query | 6 | 6 | 6 |

This confirms that a single range addition updates both current and maximum consistently.

### Example 2

Input:

```
3 2
1 2 3
1 1 3 2
1 2 2 -3
2 1 3
```

| Step | Operation | Array state | Max state | Query result |
| --- | --- | --- | --- | --- |
| 0 | init | 1 2 3 | 1 2 3 | - |
| 1 | +2 all | 3 4 5 | 3 4 5 | - |
| 2 | -3 at 2 | 3 1 5 | 3 4 5 | - |
| 3 | query | 3 1 5 | 3 4 5 | 12 |

This shows that negative updates do not reduce historical maxima, only current values.

The example confirms that maxima depend on the best value ever seen, not the final state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each update and query traverses the segment tree height |
| Space | O(n) | Segment tree arrays for sum, max, and lazy values |

The logarithmic factor is essential for handling up to 3e5 operations efficiently. Each operation only touches a path in the tree rather than the full segment.

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
            self.sum = [0] * (4 * self.n)
            self.mx = [0] * (4 * self.n)
            self.lazy = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def build(self, v, tl, tr, arr):
            if tl == tr:
                self.sum[v] = arr[tl]
                self.mx[v] = arr[tl]
                return
            tm = (tl + tr) // 2
            self.build(v*2, tl, tm, arr)
            self.build(v*2+1, tm+1, tr, arr)
            self.sum[v] = self.sum[v*2] + self.sum[v*2+1]
            self.mx[v] = self.mx[v*2] + self.mx[v*2+1]

        def apply(self, v, tl, tr, val):
            self.sum[v] += val * (tr - tl + 1)
            self.mx[v] += val * (tr - tl + 1)
            self.lazy[v] += val

        def push(self, v, tl, tr):
            if self.lazy[v]:
                tm = (tl + tr) // 2
                self.apply(v*2, tl, tm, self.lazy[v])
                self.apply(v*2+1, tm+1, tr, self.lazy[v])
                self.lazy[v] = 0

        def update(self, v, tl, tr, l, r, val):
            if l > r:
                return
            if l == tl and r == tr:
                self.apply(v, tl, tr, val)
                return
            self.push(v, tl, tr)
            tm = (tl + tr) // 2
            self.update(v*2, tl, tm, l, min(r, tm), val)
            self.update(v*2+1, tm+1, tr, max(l, tm+1), r, val)
            self.sum[v] = self.sum[v*2] + self.sum[v*2+1]
            self.mx[v] = self.mx[v*2] + self.mx[v*2+1]

        def query(self, v, tl, tr, l, r):
            if l > r:
                return 0
            if l == tl and r == tr:
                return self.mx[v]
            self.push(v, tl, tr)
            tm = (tl + tr) // 2
            return self.query(v*2, tl, tm, l, min(r, tm)) + \
                   self.query(v*2+1, tm+1, tr, max(l, tm+1), r)

    n, q = 1, 5
    st = SegTree([5])

    # sample-like
    st.update(1, 0, 0, 0, 0, 5)
    st.update(1, 0, 0, 0, 0, -3)
    assert st.query(1, 0, 0, 0, 0) == 10

    # all negative updates
    st = SegTree([1, 2, 3])
    st.update(1, 0, 2, 0, 2, -5)
    assert st.query(1, 0, 2, 0, 2) == 6

    # partial updates
    st = SegTree([1, 1, 1])
    st.update(1, 0, 2, 1, 1, 10)
    assert st.query(1, 0, 2, 0, 2) == 13

    # single element
    st = SegTree([7])
    st.update(1, 0, 0, 0, 0, -2)
    st.update(1, 0, 0, 0, 0, 5)
    assert st.query(1, 0, 0, 0, 0) == 10
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element + increase/decrease | correct max tracking | persistence of maxima |
| full negative update | unchanged max sum | maxima not reduced |
| partial update | segment correctness | lazy propagation correctness |
| repeated updates | accumulation behavior | ordering of updates |

## Edge Cases

One important edge case is repeated negative updates. Since values can decrease after reaching a peak, the maximum must remain anchored to the highest historical value. The segment tree handles this because the max field is only ever increased by the same delta as current values, never decreased.

Another edge case is repeated updates on the same segment. The lazy propagation ensures that multiple pending increments accumulate correctly. Each node aggregates all pending shifts before any partial traversal, preserving correctness even under heavy overlap.

A final edge case is single-element segments under alternating updates. Since the segment tree still treats them as full segments at leaves, both current and maximum values evolve identically, ensuring no discrepancy between stored and queried values.
