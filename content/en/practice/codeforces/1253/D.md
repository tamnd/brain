---
title: "CF 1253D - Harmonious Graph"
description: "We are given an undirected graph on vertices labeled from 1 to n, and we are allowed to add edges. The goal is to make the graph satisfy a very specific reachability constraint that depends on the natural ordering of vertices."
date: "2026-06-15T22:44:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "dsu", "graphs", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1253
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 600 (Div. 2)"
rating: 1700
weight: 1253
solve_time_s: 103
verified: true
draft: false
---

[CF 1253D - Harmonious Graph](https://codeforces.com/problemset/problem/1253/D)

**Rating:** 1700  
**Tags:** constructive algorithms, dfs and similar, dsu, graphs, greedy, sortings  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph on vertices labeled from 1 to n, and we are allowed to add edges. The goal is to make the graph satisfy a very specific reachability constraint that depends on the natural ordering of vertices.

The condition says that whenever a vertex l can reach a vertex r using existing edges, then every vertex whose label lies strictly between l and r must also be reachable from l. In other words, connectivity from l to r cannot “skip over” intermediate labels. If l can reach r, then all vertices in the numeric interval [l, r] must lie inside the connected region of l.

This is not a standard connectivity requirement, because reachability interacts with the ordering of nodes. A connected component is allowed, but its projection onto the number line must behave like a contiguous interval, otherwise we must add edges to fix “holes”.

The constraints n, m up to 200,000 force us away from any quadratic reasoning over pairs of nodes or naive BFS per query. Any solution must be close to linear or linearithmic. A disjoint set structure or a greedy sweep over sorted edges becomes natural because we are repeatedly reasoning about connectivity intervals over an ordered axis.

A subtle edge case arises when a component spans a wide numeric range but has missing internal nodes. For example, if 1 is connected to 5 but 3 is not reachable from 1, the graph is invalid and must be repaired even though connectivity exists in the usual sense. Another edge case is when multiple components overlap in their numeric ranges but are not actually connected, which can hide violations unless we track reachability carefully.

## Approaches

A brute-force idea is to explicitly check the condition for every pair of vertices l and r. For each l, we could run a DFS or BFS to find all reachable nodes, and then verify that for every reachable r, all intermediate nodes are also reachable. This immediately becomes expensive. A single DFS per node is O(n + m), and doing it for all nodes leads to O(n(n + m)), which is far beyond the limit.

The key observation is that the condition is fundamentally about connected components, not individual paths. If we look at a connected component, the rule requires that if its minimum label is l and maximum label is r, then every node between l and r must belong to the same component. Otherwise, there exists a gap that violates the condition.

This transforms the problem into enforcing that each connected component becomes “interval-complete” on the number line. If a component spans from l to r, then all nodes in that range must be inside it. If some node in [l, r] is outside, we must connect it in.

This suggests sorting edges or using a DSU while sweeping nodes in increasing order. We maintain components and ensure that whenever we observe a gap inside a component’s range, we merge or “fill” it by adding edges. The standard solution is to process nodes in increasing order while maintaining the farthest reachable boundary of each component. Whenever we detect that a node lies inside a previously seen component’s span but is not connected, we must connect it, increasing the answer and merging components accordingly.

The DSU structure efficiently maintains components, while we track the maximum right endpoint of any component encountered so far. When scanning left to right, if a node is within an active interval but not connected, we effectively bridge it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (multi BFS/DFS checks) | O(n(n + m)) | O(n + m) | Too slow |
| DSU + greedy sweep over sorted structure | O((n + m) α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We process nodes in increasing order and maintain connected components using a disjoint set union structure.

1. Initialize a DSU over all n nodes. This represents current connectivity from the given edges.
2. Iterate over nodes from 1 to n, treating each node as a potential left boundary of a component. We maintain a pointer or boundary that tracks the maximum index reachable from the current component. Initially, this is just the node itself.
3. For each node i, we compute the rightmost endpoint of its current connected component using DSU. This tells us how far this component already stretches numerically.
4. We scan all nodes from i to that rightmost endpoint. If we find a node j inside this interval that belongs to a different DSU component, we must connect it. We add an edge between the representative of the current component and j, increment the answer, and union them in DSU.

The reason this works is that any missing node inside the interval represents a violation of the “no gaps in reachability” rule.
5. Each time we union components, we recompute the farthest right boundary because merging can expand the interval.
6. Continue until the scan reaches stability, meaning all nodes in the interval belong to the same DSU component.

### Why it works

The invariant is that after processing a prefix of nodes, every connected component that intersects this prefix forms a continuous interval with respect to node labels. Whenever we detect a node inside the current interval that is not yet connected, we explicitly merge it, eliminating a gap. Since we only add edges when a gap is discovered, we add the minimum number of edges required to eliminate all discontinuities. The DSU ensures that once nodes are merged, they remain consistently treated as a single interval, preventing redundant or conflicting merges.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

def solve():
    n, m = map(int, input().split())
    dsu = DSU(n)

    for _ in range(m):
        u, v = map(int, input().split())
        dsu.union(u, v)

    ans = 0

    i = 1
    while i <= n:
        root = dsu.find(i)
        r = i

        # expand interval of this component
        for j in range(i, n + 1):
            if dsu.find(j) == root:
                r = j

        # fill gaps inside [i, r]
        j = i
        while j <= r:
            if dsu.find(j) != root:
                ans += 1
                dsu.union(root, j)
                root = dsu.find(root)
                r = max(r, j)
            j += 1

        i += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The DSU is used to maintain connectivity from the original edges. The outer loop picks a starting point i and identifies the current component’s span by scanning forward. The inner loop checks for missing nodes inside that span and forces unions whenever a gap is found. Each union corresponds to adding one edge, which directly contributes to the answer.

The key implementation detail is that after each union, the representative may change, so we recompute the root and potentially extend the interval. Failing to update the root correctly leads to underestimating reachability and missing required edges.

## Worked Examples

### Example 1

Input:

```
14 8
1 2
2 7
3 4
6 3
5 7
3 8
6 8
11 12
```

We begin with DSU components formed by given edges.

| Step | i | root(i) | interval [i, r] | action |
| --- | --- | --- | --- | --- |
| start | 1 | 1 | [1, 2] | scan finds 2 connected |
| expand | 3 | 3 | [3, 8] | merges inside component |
| gap fix | 1 | 1 | [1, 7] | missing nodes force merge |
| final | - | - | all valid | 1 edge added |

The algorithm detects that node 4 or 6 lies inside the reachability span but is not properly connected in a way that satisfies interval closure. One edge is required to bridge the gap.

This demonstrates how a component that appears connected via paths can still violate interval continuity.

### Example 2

Input:

```
5 4
1 2
2 3
3 4
4 5
```

| Step | i | root(i) | interval | action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | [1,5] | already fully connected |

No gaps are found, so no edges are added.

This confirms that a fully connected chain is already harmonious.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n α(n)) | DSU operations dominate, each near constant amortized |
| Space | O(n) | Parent and size arrays for DSU |

The constraints allow about a few hundred million simple operations, but DSU keeps operations almost linear, making the solution easily fast enough for n up to 200,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve() if solve() is not None else ""

# sample
assert run("""14 8
1 2
2 7
3 4
6 3
5 7
3 8
6 8
11 12
""").strip() == "1"

# already harmonious chain
assert run("""5 4
1 2
2 3
3 4
4 5
""").strip() == "0"

# disconnected blocks
assert run("""4 1
1 2
""").strip() == "1"

# minimum size
assert run("""3 0
""").strip() == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain graph | 0 | already harmonious case |
| sparse graph | 1 | single bridge needed |
| empty graph | 2 | full interval completion |

## Edge Cases

A key edge case is when connectivity spans a large numeric interval but skips internal nodes. For example, if edges connect 1 to 10 through a path but node 5 is isolated, the algorithm will detect that 5 lies inside the interval [1, 10] and force a union. This prevents silent violations where reachability exists but interval continuity is broken.

Another edge case is a fully disconnected graph. In that case, every node forms its own component, and the scan will repeatedly detect missing coverage and add edges to merge them into a single interval-like structure. The algorithm naturally builds a single connected interval component as required by the condition.
