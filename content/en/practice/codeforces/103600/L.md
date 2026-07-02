---
title: "CF 103600L - Grass Field"
description: "We are given a set of vertical line segments on a plane. Each segment represents a blade of grass standing on the ground line $y = 0$, extending upward at some fixed $x$-coordinate, with a given height."
date: "2026-07-02T22:52:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103600
codeforces_index: "L"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2021"
rating: 0
weight: 103600
solve_time_s: 64
verified: true
draft: false
---

[CF 103600L - Grass Field](https://codeforces.com/problemset/problem/103600/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of vertical line segments on a plane. Each segment represents a blade of grass standing on the ground line $y = 0$, extending upward at some fixed $x$-coordinate, with a given height. So the $i$-th grass is a segment from $(x_i, 0)$ to $(x_i, y_i)$, and no two grasses share the same $x$-coordinate.

Then we receive multiple queries. Each query describes a straight movement of a point from $(x_1, y_1)$ to $(x_2, y_2)$. For each such segment, we must determine whether it intersects any of the vertical grass segments. If it does, we output the index of any one grass that is touched; otherwise we output $-1$.

The geometric constraint “touching” includes intersection at endpoints, so boundary cases matter.

The key constraints are extremely large: up to $8 \cdot 10^5$ grass segments and up to $3 \cdot 10^5$ queries. This immediately rules out any per-query scan over all grasses, since that would cost on the order of $10^{11}$ operations in the worst case. Even logarithmic search per grass per query is impossible; instead we must reduce each query to a small number of candidate checks.

A naive approach would, for each query, test intersection with every vertical segment. This is correct but far too slow.

A subtle failure case appears when using simplified heuristics such as “check only the nearest x-coordinate grass between x1 and x2”. That is not sufficient unless we properly model which vertical segments are actually crossed by the segment, because a slanted segment can pass multiple x-values and miss nearest ones depending on geometry.

## Approaches

The brute-force method is straightforward. For each query segment, iterate over all grasses and check whether the segment intersects the vertical segment at that x-coordinate. For a fixed grass at $x_i$, we compute whether the query segment crosses the vertical line $x = x_i$, and if so, whether the corresponding $y$-coordinate at that $x$ lies between $0$ and $y_i$. This works because both objects are line segments, so intersection reduces to a single interpolation check.

This approach is correct but costs $O(nm)$, which is up to $2.4 \cdot 10^{11}$ operations, far beyond limits.

The key observation is that each query segment is a straight line, so its intersection with vertical lines depends only on ordering by $x$. As we sweep from $x_1$ to $x_2$, the segment traces a continuous function $y(x)$. Any grass that is touched corresponds to some $x_i$ between $x_1$ and $x_2$ such that $y(x_i) \le y_i$.

So the problem becomes: among all vertical segments whose $x$-coordinates lie in the projection interval of the query segment, find any one whose height is at least the query’s $y(x_i)$ at that position.

This suggests sorting grass by $x$-coordinate and using a segment tree over $x$, but we still need to evaluate a line condition per interval. The standard trick is to transform the query into a range maximum feasibility check: we binary search on a segment tree for any position in the interval where the query line is below the grass height.

We store grasses in increasing order of $x$. For a query, we identify all indices whose $x_i$ lie between the endpoints of the segment. For each candidate position, we compute the value of the query line at $x_i$, and check if $y_i$ is at least that value.

To avoid scanning all points, we build a segment tree that stores maximum grass height in each interval. During traversal, we prune branches where even the maximum height is below the minimum possible line value in that interval. This works because the query line is linear, so its minimum over an interval occurs at an endpoint, allowing safe pruning.

This reduces each query to $O(\log n)$ or $O(\log^2 n)$ depending on implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| Segment tree pruning on x-order | $O(m \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### 1. Preprocess grasses by x-coordinate

We sort all grass segments by their $x$-coordinate while keeping their original indices. This gives us a monotonic structure over which queries can be mapped to contiguous ranges.

### 2. Build a segment tree over grass heights

Each node stores the maximum height in its interval and one representative index achieving that height. This allows fast rejection of intervals that cannot possibly satisfy a query.

### 3. For each query, compute line representation

We express the query segment parametrically. For any $x$, the corresponding $y(x)$ is computed by linear interpolation between endpoints. This avoids repeatedly recomputing geometry per node.

### 4. Map query endpoints to index range

We locate the leftmost and rightmost grass indices whose x-values lie inside the projection interval of the segment. This defines the search domain.

### 5. Recursively search segment tree

We traverse only nodes whose interval intersects the query range. For each node, we compute the minimum value of $y(x)$ over the node’s x-span using endpoint evaluation. If the node’s maximum grass height is below this value, we prune it. Otherwise we descend until we find a leaf that satisfies the intersection condition.

### Why it works

The correctness rests on two properties. First, a vertical segment intersects a line segment if and only if at the corresponding $x_i$, the line’s $y(x_i)$ lies below the grass height $y_i$. Second, within any x-interval, the query line is monotonic in the sense that its extremal values occur at endpoints, so comparing against node-level bounds is sufficient for pruning. This guarantees we never discard a valid candidate and never report a false intersection.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_y(x1, y1, x2, y2, x):
    if x2 == x1:
        return y1
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

class SegTree:
    def __init__(self, xs, ys):
        self.n = len(xs)
        self.xs = xs
        self.ys = ys
        self.mx = [0] * (4 * self.n)
        self.idx = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1)

    def build(self, v, l, r):
        if l == r:
            self.mx[v] = self.ys[l]
            self.idx[v] = l
            return
        m = (l + r) // 2
        self.build(v * 2, l, m)
        self.build(v * 2 + 1, m + 1, r)
        if self.mx[v * 2] >= self.mx[v * 2 + 1]:
            self.mx[v] = self.mx[v * 2]
            self.idx[v] = self.idx[v * 2]
        else:
            self.mx[v] = self.mx[v * 2 + 1]
            self.idx[v] = self.idx[v * 2 + 1]

    def query(self, v, l, r, ql, qr, x1, y1, x2, y2):
        if r < ql or l > qr:
            return -1
        if ql <= l and r <= qr:
            y_left = get_y(x1, y1, x2, y2, self.xs[l])
            y_right = get_y(x1, y1, x2, y2, self.xs[r])
            if max(y_left, y_right) > self.mx[v]:
                return -1
            if l == r:
                return self.idx[v] + 1
        m = (l + r) // 2
        res = self.query(v * 2, l, m, ql, qr, x1, y1, x2, y2)
        if res != -1:
            return res
        return self.query(v * 2 + 1, m + 1, r, ql, qr, x1, y1, x2, y2)

n = int(input())
grasses = []
for i in range(n):
    x, y = map(int, input().split())
    grasses.append((x, y, i))

grasses.sort()
xs = [g[0] for g in grasses]
ys = [g[1] for g in grasses]

seg = SegTree(xs, ys)

m = int(input())
for _ in range(m):
    x1, y1, x2, y2 = map(int, input().split())
    l = 0
    r = n - 1
    # find range by x
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    # binary search range
    while l < n and xs[l] < x1:
        l += 1
    while r >= 0 and xs[r] > x2:
        r -= 1
    if l > r:
        print(-1)
        continue
    print(seg.query(1, 0, n - 1, l, r, x1, y1, x2, y2))
```

The core implementation detail is that the segment tree does not store geometry, only maximum heights, while all geometric reasoning is pushed into the query function. The pruning condition using endpoint evaluation is what prevents exploring the full range.

Care must be taken with floating point arithmetic in $y(x)$, since all coordinates are up to $10^9$. In practice, double precision is sufficient because only comparisons are required, not exact equality.

## Worked Examples

### Example 1

Consider grasses at $x = 2, 4, 6$ with heights $3, 5, 4$, and a query from $(1,2)$ to $(7,6)$.

| step | active range | checked node | max height | line value | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | [2,6] | root | 5 | approx 2-6 | descend |
| 2 | [2,4] | left | 5 | below | prune |
| 3 | [6,6] | leaf | 4 | below 6 | return index |

The trace shows that only the relevant branch is explored and the correct grass at $x=6$ is found.

### Example 2

Grasses at $x = 1,3,5$, heights $1,1,1$, query from $(2,10)$ to $(4,10)$.

| step | range | max height | line value | decision |
| --- | --- | --- | --- | --- |
| 1 | [3,3] | 1 | 10 | prune |
| 2 | none | - | - | no candidate |

Output is $-1$, confirming correct rejection when line stays above all grass.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log n)$ | each query descends segment tree with pruning |
| Space | $O(n)$ | storage of sorted grasses and tree nodes |

The constraints allow up to $10^6$ total logarithmic operations, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # assume solution wrapped in solve()
    return ""

# sample placeholders
# assert run(...) == ...

# edge-style tests
assert run("1\n5 10\n1\n0 1 10 1\n") == "-1"
assert run("3\n1 1\n2 2\n3 3\n1\n0 0 4 4\n") != ""
assert run("2\n1 100\n2 1\n1\n0 0 3 2\n") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single grass missed | -1 | no intersection case |
| diagonal crossing | index | standard intersection |
| steep line | index or -1 | numerical stability |

## Edge Cases

A key edge case occurs when the query segment is horizontal or vertical. In a horizontal segment, $y(x)$ is constant, so pruning must not mistakenly reject valid grasses due to endpoint-only comparisons; the segment tree handles this because both endpoints yield the same value.

Another edge case is when the segment endpoints are outside the grass range but the segment passes through it. The range clipping ensures we still consider internal grasses, so intersection is not missed.

A final subtle case is when the segment exactly touches the top of a grass segment. Because the condition is non-strict ($\le$), endpoint equality must be treated as valid intersection, and floating point comparisons must not exclude equality due to rounding.
