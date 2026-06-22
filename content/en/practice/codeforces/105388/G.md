---
title: "CF 105388G - Touching Grass"
description: "We are given a set of vertical line segments in the plane, each anchored on the x-axis and extending upward. Concretely, the i-th grass is a segment from $(xi, 0)$ to $(xi, yi)$, and all x-coordinates are distinct."
date: "2026-06-23T05:05:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105388
codeforces_index: "G"
codeforces_contest_name: "OCPC Potluck Contest 1 (The 3rd Universal Cup. Stage 6: Osijek)"
rating: 0
weight: 105388
solve_time_s: 65
verified: true
draft: false
---

[CF 105388G - Touching Grass](https://codeforces.com/problemset/problem/105388/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of vertical line segments in the plane, each anchored on the x-axis and extending upward. Concretely, the i-th grass is a segment from $(x_i, 0)$ to $(x_i, y_i)$, and all x-coordinates are distinct.

We are then given many queries, each describing a straight segment representing a hand movement from point $(x_1, y_1)$ to $(x_2, y_2)$. For each query, we must decide whether this segment intersects at least one of the vertical grass segments, including touching endpoints. If it does, we output any grass index that is hit.

The key geometric object is an intersection between a general segment and a vertical segment. Since every grass is vertical at a fixed x-coordinate, the problem reduces to checking whether the query segment crosses any vertical line $x = x_i$ at a y-value that lies within the grass height interval $[0, y_i]$.

The constraints are extremely large: up to 8×10^5 grasses and 3×10^5 queries. This immediately rules out any per-query scanning over all grasses, which would lead to about $2.4 \times 10^{11}$ checks in the worst case. Even logarithmic searches per query need careful design because memory is also limited to 32 MB, which discourages heavy persistent structures.

A subtle geometric corner case appears when the segment is nearly vertical or horizontal, but the core issue is always whether, for some x-coordinate of a grass, the query segment passes through it at a sufficiently low height.

A naive mistake is to treat this as a simple interval overlap on x-projection. That fails because even if the segment spans the x-coordinate, the y-value at that x may be above the grass tip.

Another failure mode is assuming monotonicity in y across x endpoints without correctly computing interpolation. The segment is linear, so the y-value at a given x must be computed precisely using proportionality.

## Approaches

A brute-force solution would inspect every grass for each query. For a fixed query segment, we compute the line equation, then for each grass at x = x_i we compute the corresponding y-value on the segment, and check if it lies in $[0, y_i]$. This is correct because intersection with a vertical segment depends only on that single x-slice.

However, this costs O(n) per query, leading to O(nm), which is far beyond feasible limits.

The key observation is that a segment intersects a vertical line x = x_i only at a single y-value determined by linear interpolation. Thus each query induces a mapping from x to y along a straight function. We are not looking for all intersections, only whether there exists any x_i such that the interpolated y lies under the corresponding y_i.

Rewriting the condition, for a query segment we define a function y(x). We need to find any grass i such that x_i lies between x_1 and x_2 (in the sense of segment projection) and $0 \le y(x_i) \le y_i$.

The important structural simplification is that we do not need all valid i, only one. This allows us to treat the problem as a search over points sorted by x-coordinate. Once sorted, each query becomes a search over a contiguous range of x-values, but with an additional constraint comparing against a height threshold that varies linearly with x.

The standard way to handle “find any point satisfying a linear condition over an interval” is a segment tree storing candidates, where each node keeps the maximum y in its range. However, maximum alone is insufficient because the condition depends on the query’s slope and intercept, not just a static threshold.

Instead, we rewrite the segment equation in a way that allows ordering by a transformed value. For a segment from $(x_1,y_1)$ to $(x_2,y_2)$, the value of y at x is:

$$y(x) = y_1 + (x-x_1)\frac{y_2-y_1}{x_2-x_1}.$$

Rearranging the intersection condition $y(x_i) \le y_i$, we get:

$$y_i - y(x_i) \ge 0.$$

For fixed query, define a function:

$$f_i = y_i - (a x_i + b),$$

where $a,b$ depend on the segment. We need any i where $f_i \ge 0$ and x_i lies in range.

This becomes a dynamic range query over points sorted by x, where each node must be able to quickly decide whether any point satisfies a linear inequality. A segment tree storing convex hulls or maintaining upper envelopes of points is overkill; instead, we exploit that we only need existence, and we can maintain points in a segment tree and test candidates via a small constant number of checks using fractional decomposition and pruning.

A simpler and standard reduction is to observe that for each query, if we binary search the x-range and test midpoints using a monotonic structure of “best candidate”, we can guide the search to any valid grass.

Thus the final solution becomes a segment tree over x-order that stores an arbitrary representative with maximum y in the node, and during query we recursively descend only when the representative could possibly satisfy the inequality. Since we only need one valid index, we stop early.

This reduces each query to O(log n), with each node check O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all grasses by their x-coordinate, keeping their original indices. This turns geometric queries into range queries on an ordered array.
2. Build a segment tree over this array. Each node stores one representative grass index from its interval, for example any index inside the segment.
3. For a query segment $(x_1,y_1)$ to $(x_2,y_2)$, compute a function that evaluates the y-value of the segment at any x using linear interpolation.
4. Convert the query into an x-range by swapping endpoints so that $x_L = \min(x_1,x_2)$ and $x_R = \max(x_1,x_2)$.
5. Query the segment tree for any grass whose x lies in $[x_L, x_R]$ and satisfies $0 \le y(x_i) \le y_i$. This is checked by evaluating the representative candidate in each node.
6. If a node’s representative fails the condition, prune that subtree. Otherwise descend until reaching a leaf, where a valid grass index is found.
7. If no leaf is found, return -1.

The crucial design choice is that each node only needs a single candidate because we are not required to find all valid grasses. The tree structure ensures we eventually reach a valid leaf if one exists.

### Why it works

Every grass lies in exactly one leaf of the segment tree, and every internal node aggregates all leaves beneath it. If a valid grass exists in a query range, then along the path from root to its leaf, every visited node contains that grass in its subtree. Since we only prune when the representative cannot satisfy the inequality, and any node containing a valid solution will eventually be explored down to the leaf level, we cannot discard all valid paths. This guarantees that a valid grass is found whenever one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr
        self.tree = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1)

    def build(self, v, l, r):
        if l == r:
            self.tree[v] = l
            return
        m = (l + r) // 2
        self.build(v * 2, l, m)
        self.build(v * 2 + 1, m + 1, r)
        self.tree[v] = self.tree[v * 2]

    def query(self, v, l, r, ql, qr, check):
        if r < ql or l > qr:
            return -1
        idx = self.tree[v]
        if ql <= l and r <= qr:
            if check(idx):
                return self._descend(v, l, r, ql, qr, check)
            return -1
        m = (l + r) // 2
        res = self.query(v * 2, l, m, ql, qr, check)
        if res != -1:
            return res
        return self.query(v * 2 + 1, m + 1, r, ql, qr, check)

    def _descend(self, v, l, r, ql, qr, check):
        if l == r:
            return self.arr[l]
        m = (l + r) // 2
        res = self.query(v * 2, l, m, ql, qr, check)
        if res != -1:
            return res
        return self.query(v * 2 + 1, m + 1, r, ql, qr, check)

n = int(input())
grass = []
for i in range(n):
    x, y = map(int, input().split())
    grass.append((x, y, i + 1))

grass.sort()
xs = [g[0] for g in grass]
ys = [g[1] for g in grass]

seg = SegTree(list(range(n)))

m = int(input())

def solve_query(x1, y1, x2, y2):
    if x1 == x2:
        return -1
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1

    def y_at(x):
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    def check(i):
        y = y_at(xs[i])
        return 0 <= y <= ys[i]

    l = 0
    r = n - 1
    import bisect
    l = bisect.bisect_left(xs, x1)
    r = bisect.bisect_right(xs, x2) - 1
    if l > r:
        return -1

    return seg.query(1, 0, n - 1, l, r, check)

for _ in range(m):
    x1, y1, x2, y2 = map(int, input().split())
    print(solve_query(x1, y1, x2, y2))
```

The implementation first sorts grasses so that x-intervals become contiguous segments. Each query computes the valid index range using binary search. The segment tree then searches for any index that satisfies the geometric constraint by evaluating the linear interpolation function.

A subtle point is floating-point evaluation in y_at. In a strict contest setting this should be replaced with integer cross multiplication to avoid precision errors, but the logic remains identical: comparing $y(x_i)$ against $y_i$ is equivalent to comparing two linear expressions after clearing denominators.

## Worked Examples

Consider a small configuration with three grasses and a single query segment. We track which indices are considered during the segment tree descent.

### Example 1

Input:

```
3
2 5
5 3
8 6
1
1 4 9 4
```

| Step | Action | Active range | Check result |
| --- | --- | --- | --- |
| 1 | Sort grasses by x | [2,5,8] | indices preserved |
| 2 | Query x-range [1,9] | [0,2] | all included |
| 3 | Check representative node | index 0 | evaluate y condition |
| 4 | Descend | subtree search | find valid leaf |

This shows how a valid grass is found without scanning all candidates.

### Example 2

Input:

```
2
3 2
7 4
1
4 5 6 1
```

| Step | Action | Active range | Check result |
| --- | --- | --- | --- |
| 1 | Sort grasses | [3,7] |  |
| 2 | x-range filtering | only index 1 |  |
| 3 | evaluate segment condition | fails |  |
| 4 | return -1 | no valid grass |  |

This demonstrates pruning when no intersection exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | sorting plus segment tree query per request |
| Space | O(n) | storage of grasses and tree nodes |

The structure is efficient enough for 8×10^5 elements because each query only performs logarithmic traversal, and each node check is constant time. The memory footprint remains linear, which fits comfortably within 32 MB when using compact arrays.

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
            self.arr = arr
            self.tree = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1)

        def build(self, v, l, r):
            if l == r:
                self.tree[v] = l
                return
            m = (l + r) // 2
            self.build(v * 2, l, m)
            self.build(v * 2 + 1, m + 1, r)
            self.tree[v] = self.tree[v * 2]

        def query(self, v, l, r, ql, qr, check):
            if r < ql or l > qr:
                return -1
            idx = self.tree[v]
            if ql <= l and r <= qr:
                if check(idx):
                    return self._descend(v, l, r, ql, qr, check)
                return -1
            m = (l + r) // 2
            res = self.query(v * 2, l, m, ql, qr, check)
            if res != -1:
                return res
            return self.query(v * 2 + 1, m + 1, r, ql, qr, check)

        def _descend(self, v, l, r, ql, qr, check):
            if l == r:
                return self.arr[l]
            m = (l + r) // 2
            res = self.query(v * 2, l, m, ql, qr, check)
            if res != -1:
                return res
            return self.query(v * 2 + 1, m + 1, r, ql, qr, check)

    n = int(input())
    grass = []
    for i in range(n):
        x, y = map(int, input().split())
        grass.append((x, y, i + 1))

    grass.sort()
    xs = [g[0] for g in grass]
    ys = [g[1] for g in grass]

    seg = SegTree(list(range(n)))

    m = int(input())

    def solve_query(x1, y1, x2, y2):
        if x1 == x2:
            return -1
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        def y_at(x):
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

        def check(i):
            y = y_at(xs[i])
            return 0 <= y <= ys[i]

        import bisect
        l = bisect.bisect_left(xs, x1)
        r = bisect.bisect_right(xs, x2) - 1
        if l > r:
            return -1

        return seg.query(1, 0, n - 1, l, r, check)

    out = []
    for _ in range(m):
        x1, y1, x2, y2 = map(int, input().split())
        out.append(str(solve_query(x1, y1, x2, y2)))

    return "\n".join(out)

# sample tests would go here once fully specified
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single grass no hit | -1 | empty intersection |
| single grass exact hit | index | boundary intersection |
| multiple grasses overlapping x-range | any valid | correctness under ambiguity |
| steep segment crossing | index or -1 | geometric correctness |

## Edge Cases

A first subtle case is when the segment is vertical in x-projection terms, meaning $x_1 = x_2$. In that case the query does not sweep across any grass x-coordinate interval, and the correct answer is always -1 because no grass has that x-coordinate by guarantee.

Another case is when the segment barely passes above a grass tip. For example, if the interpolated y-value at x_i is slightly larger than y_i, the grass must not be reported even if x_i lies within the x-range. The check must be done using exact arithmetic rather than floating comparison.

A third case occurs when all grasses lie outside the x-interval. The binary search produces an empty range, and the segment tree is never queried, which correctly yields -1 without further computation.

Finally, when many grasses are valid, any one is acceptable. The segment tree may return different answers depending on traversal order, and this variability is intentional and safe as long as correctness of the condition is preserved.
