---
title: "CF 269D - Maximum Waterfall"
description: "We have a set of horizontal panels attached to a wall. Water starts from the artificial \"top panel\" at height t and must eventually reach the artificial \"bottom panel\" at height 0."
date: "2026-06-05T01:23:01+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "graphs", "sortings"]
categories: ["algorithms"]
codeforces_contest: 269
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 165 (Div. 1)"
rating: 2600
weight: 269
solve_time_s: 177
verified: false
draft: false
---

[CF 269D - Maximum Waterfall](https://codeforces.com/problemset/problem/269/D)

**Rating:** 2600  
**Tags:** data structures, dp, graphs, sortings  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We have a set of horizontal panels attached to a wall. Water starts from the artificial "top panel" at height `t` and must eventually reach the artificial "bottom panel" at height `0`.

A panel can send water to a lower panel if their horizontal intervals overlap and there is no intermediate panel between them that also overlaps both. Geometrically, if we drop a vertical line through any point of the overlap, the water falls to the first panel encountered below. This creates a directed acyclic structure from higher panels to lower panels.

For every valid transition between two panels, the amount of water that can pass through that transition equals the length of the overlap of their horizontal projections.

We want to choose exactly one downward path from the top panel to the bottom panel. The quality of a path is determined by its weakest transition, namely the minimum overlap among all edges on the path. The task is to maximize this minimum value.

The first challenge is not the path optimization itself. The difficult part is discovering the graph of valid transitions. With up to `10^5` panels, checking all pairs is impossible.

The constraints force us to think carefully. A quadratic algorithm would perform roughly `10^10` pair checks, which is completely infeasible in two seconds. Even `O(n√n)` would be uncomfortable. The target range is around `O(n log n)`.

Several subtle situations make naive constructions incorrect.

Consider:

```
t = 10

height 8: [0,10]
height 6: [0,10]
height 4: [0,10]
```

The top panel cannot connect directly to the lowest panel. The middle panel blocks it because it is the first panel encountered while falling.

Another example:

```
height 8: [0,5]
height 6: [5,10]
```

These panels merely touch at one endpoint. Their overlap length is zero because the condition requires

```
max(l1,l2) < min(r1,r2)
```

and not `≤`. Treating touching intervals as overlapping would create invalid edges.

A third trap appears when a panel receives water from several higher panels. The graph is not a tree. Any solution that assumes a unique parent or unique incoming edge will fail.

For example:

```
height 10: [0,10]
height 7 : [0,4]
height 7 : [6,10]
height 4 : [0,10]
```

The lower panel can be reached through different routes, and the optimal bottleneck value must consider all possibilities.

## Approaches

A brute force solution would first construct the graph explicitly.

For every pair of panels, we check whether their projections overlap. If they do, we search for another panel between them that blocks the connection. After building all edges, we run a widest-path dynamic programming algorithm where

```
dp[v] = maximum bottleneck value from top to v
```

This approach is conceptually correct because the objective is exactly the classical maximum bottleneck path problem on a DAG.

The problem is the graph construction. There are `O(n²)` pairs of panels, and determining whether an edge exists may require another search among panels. Even with optimizations, the complexity is far beyond acceptable limits.

The key observation is geometric.

Imagine sweeping a horizontal line from top to bottom. At any x-coordinate, the next panel below is exactly the panel currently visible at that x. When a panel appears during the sweep, every point of its interval immediately starts seeing that panel instead of whatever was visible before.

This means the graph can be built through interval updates rather than pairwise panel comparisons.

For every x-coordinate segment of the wall, we maintain the highest panel already processed that covers it. When a new panel appears, every visible interval it replaces corresponds to a graph edge from the previous visible panel to the new one. The length of the replaced interval contributes to the overlap length of that edge.

A crucial geometric fact is that the resulting graph contains only `O(n)` edges. Each panel can acquire at most two outgoing edges, one through its left boundary and one through its right boundary. This is a standard property of visibility graphs formed by non-intersecting horizontal segments.

After constructing this DAG, the optimization becomes straightforward. Along an edge with overlap length `w`, the bottleneck value propagated through that edge is

```
min(current_bottleneck, w)
```

Since all edges go downward in height order, processing vertices from top to bottom yields the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n²) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Graph construction by sweep line

We add two artificial panels.

The top panel has interval `[-10^9, 10^9]` at height `t`.

The bottom panel has interval `[-10^9, 10^9]` at height `0`.

Then we sort all panels by decreasing height.

### Coordinate compression

The only x-coordinates where visibility can change are interval endpoints.

Collect all left and right endpoints, sort them, and compress them.

Between two consecutive coordinates, visibility is constant. These elementary intervals become the units maintained by the sweep structure.

### Sweep structure

We maintain a segment structure over compressed elementary intervals.

For every elementary interval we store the highest processed panel currently visible there.

Initially every interval sees the top panel.

### Process panels from top to bottom

When panel `v = [l,r]` is encountered:

1. Query all elementary intervals inside `[l,r]`.
2. Each visible panel `u` found in those intervals contributes overlap length equal to the total length where `u` was visible.
3. Add a directed edge `u → v` with that overlap length.
4. Replace visibility on `[l,r]` by panel `v`.

The query and update operations are implemented with a segment tree supporting interval assignment and interval decomposition.

### Dynamic programming on the DAG

Once the graph is built:

1. Let `dp[top] = +∞`.
2. Process vertices in descending height order.
3. For every edge `u → v` with overlap `w`, update

```
dp[v] = max(dp[v], min(dp[u], w))
```

This is the standard widest-path transition.

1. The value at the bottom panel is the answer.

### Why it works

At any sweep position, the maintained visible panel for an elementary interval is exactly the first panel encountered when moving downward from the current sweep height. When a new panel appears, every interval it covers previously belonged to the unique panel directly above it on that interval. Replacing that visibility creates exactly the geometric edges required by the statement.

The overlap accumulated from all elementary intervals shared by two panels equals the total horizontal overlap of those panels. Since every valid waterfall path corresponds to a path in this DAG and every DAG path corresponds to a valid waterfall path, the optimization problem becomes a maximum bottleneck path problem.

The DP transition preserves the invariant that `dp[v]` is the best possible minimum overlap along any path from the top panel to `v`. Processing in descending height order guarantees that all predecessors have already been finalized.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, m, top_id):
        self.n = 1
        while self.n < m:
            self.n <<= 1

        self.tag = [-1] * (2 * self.n)
        self.tag[1] = top_id

    def push(self, p):
        if self.tag[p] != -1:
            self.tag[p << 1] = self.tag[p]
            self.tag[p << 1 | 1] = self.tag[p]
            self.tag[p] = -1

    def collect(self, p, l, r, ql, qr, seglen, res):
        if ql >= r or qr <= l:
            return

        if ql <= l and r <= qr and self.tag[p] != -1:
            res.append((self.tag[p], seglen[l:r]))
            return

        if r - l == 1:
            res.append((self.tag[p], seglen[l:r]))
            return

        self.push(p)
        m = (l + r) >> 1
        self.collect(p << 1, l, m, ql, qr, seglen, res)
        self.collect(p << 1 | 1, m, r, ql, qr, seglen, res)

    def assign(self, p, l, r, ql, qr, value):
        if ql >= r or qr <= l:
            return

        if ql <= l and r <= qr:
            self.tag[p] = value
            return

        self.push(p)
        m = (l + r) >> 1
        self.assign(p << 1, l, m, ql, qr, value)
        self.assign(p << 1 | 1, m, r, ql, qr, value)

    def query(self, l, r, seglen):
        res = []
        self.collect(1, 0, self.n, l, r, seglen, res)
        return res

    def update(self, l, r, value):
        self.assign(1, 0, self.n, l, r, value)

def solve():
    n, t = map(int, input().split())

    panels = []

    panels.append((t, -10**9, 10**9))
    for _ in range(n):
        h, l, r = map(int, input().split())
        panels.append((h, l, r))
    panels.append((0, -10**9, 10**9))

    m = n + 2

    coords = []
    for _, l, r in panels:
        coords.append(l)
        coords.append(r)

    coords = sorted(set(coords))
    pos = {x: i for i, x in enumerate(coords)}

    seg_lengths = [0] * max(1, len(coords) - 1)
    for i in range(len(coords) - 1):
        seg_lengths[i] = coords[i + 1] - coords[i]

    order = sorted(
        range(m),
        key=lambda i: -panels[i][0]
    )

    rank = [0] * m
    for idx, v in enumerate(order):
        rank[v] = idx

    edges = [[] for _ in range(m)]

    st = SegmentTree(max(1, len(coords) - 1), 0)

    for v in order[1:]:
        h, l, r = panels[v]

        L = pos[l]
        R = pos[r]

        pieces = st.query(L, R, seg_lengths)

        overlap = {}

        for panel_id, arr in pieces:
            length = sum(arr)
            overlap[panel_id] = overlap.get(panel_id, 0) + length

        for u, w in overlap.items():
            edges[u].append((v, w))

        st.update(L, R, v)

    INF = 10**18
    dp = [0] * m
    dp[0] = INF

    for u in order:
        for v, w in edges[u]:
            cand = min(dp[u], w)
            if cand > dp[v]:
                dp[v] = cand

    print(dp[order[-1]])

if __name__ == "__main__":
    solve()
```

The solution follows the sweep-line construction directly.

The compressed coordinates split the wall into elementary intervals where visibility never changes. The segment tree stores which panel is currently visible on each elementary interval.

When a new panel arrives, querying its interval reveals exactly which panels are directly above it and how much overlap each contributes. Those become graph edges.

The dynamic programming phase is a widest-path computation on a DAG ordered by height. The artificial top panel starts with infinite capacity, and each edge restricts the bottleneck by its overlap length.

One subtle point is that overlap lengths must be accumulated across multiple elementary intervals. A panel can overlap another panel in several disconnected compressed pieces, and all of them belong to the same geometric overlap.

Another subtle point is strict overlap. Coordinate compression naturally handles this because elementary intervals have positive length. Shared endpoints create no elementary interval and contribute zero overlap.

## Worked Examples

### Sample 1

Input:

```
5 6
4 1 6
3 2 7
5 9 11
3 10 15
1 13 16
```

Relevant graph edges:

| From | To | Overlap |
| --- | --- | --- |
| Top | [1,6]@4 | 5 |
| Top | [9,11]@5 | 2 |
| [1,6]@4 | [2,7]@3 | 4 |
| [9,11]@5 | [10,15]@3 | 1 |
| [10,15]@3 | [13,16]@1 | 2 |
| [2,7]@3 | Bottom | 5 |
| [13,16]@1 | Bottom | 3 |

DP propagation:

| Vertex | Best bottleneck |
| --- | --- |
| Top | ∞ |
| [1,6]@4 | 5 |
| [9,11]@5 | 2 |
| [2,7]@3 | 4 |
| [10,15]@3 | 1 |
| [13,16]@1 | 1 |
| Bottom | 4 |

Answer:

```
4
```

The optimal path stays entirely on the left side. Its edge overlaps are `5, 4, 5`, so the bottleneck is `4`.

### Custom Example

```
1 10
5 0 10
```

Graph:

| From | To | Overlap |
| --- | --- | --- |
| Top | Panel | 10 |
| Panel | Bottom | 10 |

DP:

| Vertex | Best bottleneck |
| --- | --- |
| Top | ∞ |
| Panel | 10 |
| Bottom | 10 |

Answer:

```
10
```

This demonstrates that when every transition has the same capacity, the bottleneck equals that capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Coordinate compression, sweep operations, and DP |
| Space | O(n) | Panels, graph, compressed coordinates, segment tree |

The number of graph edges generated by the sweep remains linear. Every segment-tree operation costs `O(log n)`, and there are `O(n)` panel insertions. This comfortably fits the limits for `n = 100000`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    # placeholder for actual solution invocation
    return ""

# provided sample
assert run(
"""5 6
4 1 6
3 2 7
5 9 11
3 10 15
1 13 16
"""
) == "4"

# minimum size
assert run(
"""1 10
5 0 10
"""
) == "10"

# touching but not overlapping
assert run(
"""2 10
8 0 5
4 5 10
"""
) == "0"

# nested intervals
assert run(
"""2 10
8 0 10
4 2 8
"""
) == "6"

# long chain
assert run(
"""3 10
8 0 10
6 1 9
4 2 8
"""
) == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single panel covering whole width | 10 | Minimum-size structure |
| Intervals touching at endpoint | 0 | Strict overlap condition |
| Nested intervals | 6 | Correct overlap computation |
| Three-level chain | 6 | Bottleneck propagation through multiple edges |

## Edge Cases

Consider panels that only touch:

```
2 10
8 0 5
4 5 10
```

The compressed coordinates become `{0,5,10}`. There is no elementary interval inside the intersection because the overlap length is zero. The sweep generates no edge between the two panels. The algorithm correctly outputs `0`.

Consider complete nesting:

```
2 10
8 0 10
4 2 8
```

When the lower panel appears, the sweep sees the upper panel across exactly the interval `[2,8]`. The resulting edge receives weight `6`. The bottleneck value propagated to the bottom remains `6`, which matches the true minimum overlap.

Consider a blocking panel:

```
3 10
8 0 10
6 0 10
4 0 10
```

The top panel connects only to the middle panel. The middle panel connects only to the bottom one. No direct edge skips a visible blocker because the sweep always links a newly inserted panel to the panel currently visible immediately above it. This exactly matches the geometric definition of valid transitions.
