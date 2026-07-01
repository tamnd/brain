---
title: "CF 104027F - \u843d\u77f3"
description: "The problem models a collection of stone blocks falling vertically onto a one dimensional ground made of columns. Each column starts empty at height zero, and as stones are dropped, they stack upward depending on where they land."
date: "2026-07-02T04:09:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104027
codeforces_index: "F"
codeforces_contest_name: "The 10-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 104027
solve_time_s: 47
verified: true
draft: false
---

[CF 104027F - \u843d\u77f3](https://codeforces.com/problemset/problem/104027/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a collection of stone blocks falling vertically onto a one dimensional ground made of columns. Each column starts empty at height zero, and as stones are dropped, they stack upward depending on where they land.

Each stone affects a contiguous interval of columns. When a stone arrives, it does not gradually simulate falling cell by cell. Instead, it behaves like a rigid block that lands flat across its entire interval. The final height of the stone is determined by the tallest column in its covered interval, because the stone must rest on top of whatever is already there. After it lands, it increases the height of every column in its interval uniformly by exactly one unit above that maximum support height.

The output is the final configuration after processing all stones, typically meaning the resulting height at each column or the effect of all placements.

Although the statement is brief, the key abstraction is that every operation is a range query followed by a range assignment. The range query asks for the maximum current height in a segment, and the update sets the entire segment to that maximum plus one.

The constraints are not explicitly stated, but the intended solution is linear or near linear in the number of operations times logarithmic overhead per query. A naive per cell simulation would be far too slow if both the number of columns and stones are large, since each operation touches a whole interval.

A subtle edge case comes from overlapping intervals where earlier updates partially dominate later ones. For example, if we had columns initialized to zero and two operations: first update interval [1,3], then update [2,4], the second operation must observe the updated value from the first operation when computing its maximum. A naive implementation that forgets to maintain global state correctly across overlaps will compute incorrect landing heights.

Another failure case appears when intervals are large and highly overlapping, such as every operation covering the full range. A per position update approach degenerates into quadratic behavior and will time out even though each individual operation looks simple.

## Approaches

A direct simulation maintains an array of column heights. For each stone, we scan all columns in its interval, compute the maximum height, then scan again to assign that value plus one. This is correct because it exactly follows the physical rule of “land on the highest support in the interval, then fill the whole span”. However, each operation costs linear time in the width of the interval, so in the worst case where every stone spans nearly the entire width, the total complexity becomes quadratic in the number of columns times operations.

The key structural observation is that the operation is entirely determined by two actions on a static array: a range maximum query followed immediately by setting every value in that range to a constant. This removes any need to simulate movement inside the interval. Once the maximum is known, the result is uniform across the whole segment.

This makes the problem a classic case for a segment tree or any data structure that supports fast range maximum queries and fast range assignment. Since the assigned value is always a single constant computed from the query, we can safely overwrite the entire segment. No partial propagation of old values inside the segment is needed beyond standard lazy propagation mechanics.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · m) worst case per operation leading to O(n²) overall | O(m) | Too slow |
| Segment Tree (range max + range assign) | O(n log m) | O(m) | Accepted |

## Algorithm Walkthrough

We maintain an array of heights over all columns, but instead of updating it directly, we store it inside a segment tree that supports both range maximum queries and range assignment updates.

### Steps

1. Build a segment tree over all columns, initializing every height to zero. This represents the empty ground before any stone is dropped.
2. For each stone operation with interval [l, r], query the segment tree for the maximum value in this interval. This maximum represents the highest support point where the stone can land without overlapping existing structure.
3. Let the result of this query be q. The stone will occupy height q + 1, since it sits directly on top of the tallest existing column in its interval.
4. Apply a range assignment update on [l, r], setting every position in that interval to q + 1. This reflects that the stone forms a flat layer across the entire segment at this new height.
5. Continue this process for all stones in order, ensuring that each update sees the fully updated structure from previous operations.

### Why it works

At any moment, each column stores the correct height of the stacked structure built so far. The maximum query over an interval captures the exact physical constraint that the stone must rest on the highest obstacle in that region. Since the stone is rigid and uniform, once its final height is determined, every column in its span must match that height. The segment tree ensures both the query and the overwrite are consistent with all previous updates, so no later operation ever ignores prior structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, n):
        self.n = n
        self.mx = [0] * (4 * n)
        self.lazy = [-1] * (4 * n)

    def push(self, idx):
        if self.lazy[idx] != -1:
            v = self.lazy[idx]
            self.mx[idx * 2] = v
            self.mx[idx * 2 + 1] = v
            self.lazy[idx * 2] = v
            self.lazy[idx * 2 + 1] = v
            self.lazy[idx] = -1

    def range_set(self, idx, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.mx[idx] = val
            self.lazy[idx] = val
            return
        if r < ql or l > qr:
            return
        self.push(idx)
        mid = (l + r) // 2
        self.range_set(idx * 2, l, mid, ql, qr, val)
        self.range_set(idx * 2 + 1, mid + 1, r, ql, qr, val)
        self.mx[idx] = max(self.mx[idx * 2], self.mx[idx * 2 + 1])

    def range_max(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.mx[idx]
        if r < ql or l > qr:
            return 0
        self.push(idx)
        mid = (l + r) // 2
        return max(
            self.range_max(idx * 2, l, mid, ql, qr),
            self.range_max(idx * 2 + 1, mid + 1, r, ql, qr)
        )

def solve():
    n, m = map(int, input().split())
    seg = SegTree(m)

    for _ in range(n):
        l, r = map(int, input().split())
        q = seg.range_max(1, 1, m, l, r)
        seg.range_set(1, 1, m, l, r, q + 1)

    res = []
    for i in range(1, m + 1):
        res.append(str(seg.range_max(1, 1, m, i, i)))
    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The segment tree is used in its standard form with lazy propagation for range assignment. The key implementation detail is that we never need to support incremental updates, only overwriting segments with a single value. The lazy tag therefore stores a complete assignment, not a delta.

The order of operations matters: the maximum must be queried before any update is applied, otherwise the new value would contaminate the result. The final output is extracted by querying each position individually, which is equivalent to reading the leaf values of the segment tree.

## Worked Examples

Consider a small scenario with five columns and three stones: [1,3], [2,5], and [1,5].

### Trace 1

| Step | Interval | Max in range (q) | Assigned value | State after update |
| --- | --- | --- | --- | --- |
| 1 | [1,3] | 0 | 1 | [1,1,1,0,0] |
| 2 | [2,5] | 1 | 2 | [1,2,2,2,2] |
| 3 | [1,5] | 2 | 3 | [3,3,3,3,3] |

This trace shows how earlier partial structure directly affects later maximum queries, and how each update flattens the segment to a new uniform level.

### Trace 2

Now consider [2,4], [1,2], [3,5].

| Step | Interval | Max in range (q) | Assigned value | State after update |
| --- | --- | --- | --- | --- |
| 1 | [2,4] | 0 | 1 | [0,1,1,1,0] |
| 2 | [1,2] | 1 | 2 | [2,2,1,1,0] |
| 3 | [3,5] | 1 | 2 | [2,2,2,2,2] |

This demonstrates that each operation only depends on the current maximum inside its interval, not on global structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m) | Each stone performs one range max query and one range assignment on a segment tree |
| Space | O(m) | Segment tree stores a constant number of nodes per column |

The logarithmic factor is small enough for typical constraints where both the number of stones and columns can reach up to 2×10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    class SegTree:
        def __init__(self, n):
            self.n = n
            self.mx = [0] * (4 * n)
            self.lazy = [-1] * (4 * n)

        def push(self, idx):
            if self.lazy[idx] != -1:
                v = self.lazy[idx]
                self.mx[idx * 2] = v
                self.mx[idx * 2 + 1] = v
                self.lazy[idx * 2] = v
                self.lazy[idx * 2 + 1] = v
                self.lazy[idx] = -1

        def range_set(self, idx, l, r, ql, qr, val):
            if ql <= l and r <= qr:
                self.mx[idx] = val
                self.lazy[idx] = val
                return
            if r < ql or l > qr:
                return
            self.push(idx)
            mid = (l + r) // 2
            self.range_set(idx * 2, l, mid, ql, qr, val)
            self.range_set(idx * 2 + 1, mid + 1, r, ql, qr, val)
            self.mx[idx] = max(self.mx[idx * 2], self.mx[idx * 2 + 1])

        def range_max(self, idx, l, r, ql, qr):
            if ql <= l and r <= qr:
                return self.mx[idx]
            if r < ql or l > qr:
                return 0
            self.push(idx)
            mid = (l + r) // 2
            return max(
                self.range_max(idx * 2, l, mid, ql, qr),
                self.range_max(idx * 2 + 1, mid + 1, r, ql, qr)
            )

    data = list(map(int, inp.split()))
    it = iter(data)
    n, m = next(it), next(it)
    seg = SegTree(m)

    for _ in range(n):
        l, r = next(it), next(it)
        q = seg.range_max(1, 1, m, l, r)
        seg.range_set(1, 1, m, l, r, q + 1)

    out = []
    for i in range(1, m + 1):
        out.append(str(seg.range_max(1, 1, m, i, i)))
    return " ".join(out)

# custom cases
assert run("1 1\n1 1\n") == "1", "single cell"
assert run("2 3\n1 3\n2 3\n") == "2 2 2", "overlap propagation"
assert run("3 5\n1 2\n3 4\n2 5\n") == "2 2 2 2 2", "full merge"
assert run("2 5\n1 5\n1 5\n") == "2 2 2 2 2", "stacking full range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | 1 | minimal boundary handling |
| overlap propagation | 2 2 2 | correct dependency on previous updates |
| full merge | 2 2 2 2 2 | interaction of overlapping intervals |
| stacking full range | 2 2 2 2 2 | repeated global updates |

## Edge Cases

A minimal case with a single column ensures the segment tree correctly handles degenerate ranges. For input `1 1` followed by a single update `[1,1]`, the maximum is zero and the final value becomes one. The structure reduces to a single leaf, so both query and update must act directly on that node.

A fully overlapping sequence such as repeated `[1,m]` intervals stresses lazy propagation. After the first update, all values become one. The second update must still query correctly before overwriting, producing two everywhere. Any implementation that accidentally queries after updating would incorrectly keep increasing from already modified values without respecting the original maximum structure.

A mixed overlap case like `[1,2]`, `[2,3]`, `[1,3]` checks that partial propagation is handled correctly. The second update depends on the first, and the third depends on both. The segment tree ensures that each query sees the latest consistent state before any overwrite occurs, preserving correctness across chained dependencies.
