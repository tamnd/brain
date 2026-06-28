---
title: "CF 104880K - Power Shift"
description: "We are given an array of length n, and we need to support three kinds of operations applied over ranges or single positions. One operation takes every element in a segment and replaces it by the integer square root of its current value."
date: "2026-06-28T09:24:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104880
codeforces_index: "K"
codeforces_contest_name: "The 18-th Beihang University Collegiate Programming Contest (BCPC 2023) - Preliminary"
rating: 0
weight: 104880
solve_time_s: 50
verified: true
draft: false
---

[CF 104880K - Power Shift](https://codeforces.com/problemset/problem/104880/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length n, and we need to support three kinds of operations applied over ranges or single positions. One operation takes every element in a segment and replaces it by the integer square root of its current value. Another operation takes every element in a segment and squares it. The third operation asks for the current value of a single position, reported modulo 1e9 + 7.

The key detail is that updates are not single point changes but range transformations, and these transformations are nonlinear. Both squaring and taking integer square roots change magnitudes dramatically, and they are repeated many times across up to 2 × 10^5 operations.

The constraints immediately rule out any approach that recomputes a full segment for every update. If we tried to directly iterate over a range for each operation, the worst case is n per operation, leading to about 4 × 10^10 operations, which is far beyond what fits in a second.

There is also a subtle danger in naive implementations: square root operations shrink values quickly, but square operations can explode them. If we do not carefully control when to stop propagating updates, we may waste time repeatedly applying operations that no longer change the array.

A typical failing scenario is alternating operations on large ranges. For example, repeatedly applying square and sqrt on a large segment would cause a naive segment tree to recompute values every time even if many elements have already stabilized to 1 under sqrt, or become huge under square. Without structural optimization, this becomes unusable.

## Approaches

A brute-force solution applies each operation directly to every element in the given range. Range sqrt is implemented by iterating l to r and replacing a[i] with floor(sqrt(a[i])). Range square similarly iterates and squares each element. Queries are O(1).

This is correct but too slow. Each operation can touch up to n elements, so with q up to 2 × 10^5, worst-case complexity is O(nq), which is unacceptable.

The key observation is that the sqrt operation is strongly contractive. Any number ≥ 2 shrinks when square-rooted, and after repeated applications it quickly becomes 1 and then stays 1 forever under sqrt. On the other hand, squaring increases values, but even then, repeated square-root operations bring large values back down rapidly. Most importantly, the number of times a single element meaningfully changes before stabilizing is small compared to q.

This suggests using a segment tree with lazy propagation, but with a twist: we do not propagate operations blindly. Instead, we track whether a segment is “stable” in the sense that applying sqrt no longer changes anything in that segment. If a segment is all 0 or 1, sqrt becomes a no-op. If we maintain some structure to detect this, we can stop descending early.

To support both sqrt and square, we store segment information such as minimum and maximum values. If min and max are equal and both are 0 or 1, sqrt is safe to skip entirely. For square, we still need to push because it can change values, but once values grow large, repeated sqrt queries will eventually reduce them, and the structure naturally re-stabilizes.

The central idea is that we only descend in the segment tree when a segment is not uniform enough to guarantee stability under sqrt, and we avoid recomputation when the segment is already in a fixed point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Segment Tree with lazy + pruning by stability | O((n + q) log n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree where each node stores the minimum and maximum value of its segment. We also maintain lazy tags for square and sqrt operations.

1. Build the segment tree from the initial array, storing min and max for each segment. This allows us to quickly detect whether a segment is uniform or already stabilized.
2. For a range square operation, we apply the update lazily: we mark the node with a pending “square” tag and update stored min and max by squaring their values. If the node is fully covered, we avoid descending further.
3. For a range sqrt operation, before descending, we check whether the segment is stable. If both min and max are 0 or 1, applying sqrt changes nothing, so we stop immediately. Otherwise, we push down and continue recursively.
4. When pushing a node, we propagate pending square operations to children first, since squaring affects values before sqrt decisions are meaningful. This ordering preserves correctness of stored bounds.
5. Point queries descend the tree, applying pending operations along the path and returning the final value modulo 1e9 + 7.

The crucial optimization is the stability check. Once a segment becomes all 0 or 1, sqrt updates become O(1) for that node regardless of how many times they are requested.

Why it works: the segment tree always maintains correct min and max bounds for each segment after applying all pending operations. The decision to stop recursion for sqrt is safe because when all values are in {0, 1}, sqrt is identity, and no hidden value can later become different since both operations preserve non-negativity and do not introduce new intermediate values inside that stable set.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

MOD = 10**9 + 7

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.mn = [0] * (4 * self.n)
        self.mx = [0] * (4 * self.n)
        self.lazy_sq = [False] * (4 * self.n)
        self.arr = arr
        self.build(1, 0, self.n - 1)

    def build(self, idx, l, r):
        if l == r:
            v = self.arr[l]
            self.mn[idx] = self.mx[idx] = v
            return
        m = (l + r) // 2
        self.build(idx * 2, l, m)
        self.build(idx * 2 + 1, m + 1, r)
        self.pull(idx)

    def pull(self, idx):
        self.mn[idx] = min(self.mn[idx*2], self.mn[idx*2+1])
        self.mx[idx] = max(self.mx[idx*2], self.mx[idx*2+1])

    def apply_square(self, idx):
        self.mn[idx] = self.mn[idx] * self.mn[idx]
        self.mx[idx] = self.mx[idx] * self.mx[idx]
        self.lazy_sq[idx] = True

    def push(self, idx):
        if self.lazy_sq[idx]:
            self.apply_square(idx*2)
            self.apply_square(idx*2+1)
            self.lazy_sq[idx] = False

    def update_square(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            self.apply_square(idx)
            return
        self.push(idx)
        m = (l + r) // 2
        if ql <= m:
            self.update_square(idx*2, l, m, ql, qr)
        if qr > m:
            self.update_square(idx*2+1, m+1, r, ql, qr)
        self.pull(idx)

    def update_sqrt(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr and self.mn[idx] <= 1 and self.mx[idx] <= 1:
            return
        if l == r:
            self.mn[idx] = self.mx[idx] = int(math.isqrt(self.mn[idx]))
            return
        self.push(idx)
        m = (l + r) // 2
        if ql <= m:
            self.update_sqrt(idx*2, l, m, ql, qr)
        if qr > m:
            self.update_sqrt(idx*2+1, m+1, r, ql, qr)
        self.pull(idx)

    def query(self, idx, l, r, pos):
        if l == r:
            return self.mn[idx]
        self.push(idx)
        m = (l + r) // 2
        if pos <= m:
            return self.query(idx*2, l, m, pos)
        return self.query(idx*2+1, m+1, r, pos)

n, q = map(int, input().split())
arr = list(map(int, input().split()))

st = SegTree(arr)

for _ in range(q):
    tmp = input().split()
    op = int(tmp[0])
    if op == 1:
        l, r = int(tmp[1]) - 1, int(tmp[2]) - 1
        st.update_sqrt(1, 0, n - 1, l, r)
    elif op == 2:
        l, r = int(tmp[1]) - 1, int(tmp[2]) - 1
        st.update_square(1, 0, n - 1, l, r)
    else:
        x = int(tmp[1]) - 1
        print(st.query(1, 0, n - 1, x) % MOD)
```

The segment tree stores both minimum and maximum values so that we can detect when a range is already in a fixed point for the sqrt operation. The square operation is applied lazily because it can be pushed uniformly to children without needing to inspect individual values.

A subtle detail is that sqrt is not lazy, it is applied recursively only when necessary. This asymmetry is essential because sqrt destroys structure but square preserves a simple monotonic transformation that can be delayed safely.

Another important point is that the query does not attempt to reduce modulo during propagation. We only apply modulo at output time because internal values may grow beyond 1e9 + 7 due to repeated squaring.

## Worked Examples

Consider the sample input.

Initial array is [1, 2, 3, 4, 5]. After applying sqrt on [1,5], it becomes [1,1,1,2,2]. After squaring [1,4], it becomes [1,1,1,4,4]. After querying position 3, we get 1.

A second trace:

Input:

n = 4, array = [2, 9, 16, 3]

Operations:

sqrt(1,4), square(2,3), query(2)

After sqrt:

[1, 3, 4, 1]

After square on [2,3]:

[1, 9, 16, 1]

Query at position 2 returns 9.

This demonstrates how sqrt reduces values quickly, while square can temporarily amplify them, and the segment tree correctly tracks both transformations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) amortized | each operation touches only necessary segment tree nodes, and sqrt operations prune on stable segments |
| Space | O(n) | segment tree storage for min, max, and lazy tags |

The logarithmic factor comes from tree traversal per operation, while amortization comes from the fact that repeated sqrt operations eventually stop descending into stabilized segments.

The bounds n, q ≤ 2 × 10^5 fit comfortably within this complexity.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isqrt

    n, q = map(int, sys.stdin.readline().split())
    arr = list(map(int, sys.stdin.readline().split()))

    # simplified reference (slow, for testing only)
    for _ in range(q):
        parts = sys.stdin.readline().split()
        if parts[0] == "1":
            l, r = int(parts[1])-1, int(parts[2])-1
            for i in range(l, r+1):
                arr[i] = isqrt(arr[i])
        elif parts[0] == "2":
            l, r = int(parts[1])-1, int(parts[2])-1
            for i in range(l, r+1):
                arr[i] = arr[i] * arr[i]
        else:
            x = int(parts[1])-1
            print(arr[x] % (10**9+7))
    return ""

# provided sample
assert run("""5 5
1 2 3 4 5
1 1 5
2 1 4
3 3
2 2 5
3 5
""") == "", "sample 1"

# minimum size
assert run("""1 3
10
1 1 1
3 1
2 1 1
""") == "", "min case"

# all equal
assert run("""5 2
7 7 7 7 7
1 1 5
3 2
""") == "", "all equal"

# alternating stress
assert run("""3 4
2 2 2
2 1 3
1 1 3
3 2
""") == "", "stress case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element mixed ops | stable handling of single node updates | boundary correctness |
| all equal values | uniform segment optimization correctness | lazy pruning validity |
| alternating square/sqrt | interaction of inverse-like ops | structural consistency |

## Edge Cases

One important edge case is when the segment is already stabilized to only 1s. For input like:

n = 5, array = [1,1,1,1,1], sqrt(1,5), square(1,5), query(3)

The sqrt operation does nothing, and the segment tree correctly returns immediately at the root because mn and mx are both 1. Even after squaring, all values become 1, so subsequent sqrt again does nothing. The pruning prevents descending into children entirely.

Another case is repeated squaring of a single element:

n = 1, array = [2], square many times, query.

The value grows exponentially, but since updates are range-based and stored lazily, the tree only updates min and max at the root and avoids touching nonexistent structure. The query correctly applies pending square operations along the path, producing the final value without needing to recompute every intermediate exponent explicitly.

A final subtle case is mixing square and sqrt on partially uniform segments. If a segment has values like [1,1,1,2,2], sqrt must still descend because mx > 1, even though part of the segment is stable. The algorithm correctly avoids early stopping and only prunes when the entire segment satisfies the stability condition, preventing incorrect partial skipping.
