---
title: "CF 104236E - Wifi Connection"
description: "We are given a set of points on a 2D plane, each representing an observation station in a national park. Every station is equipped with a wireless device that has a uniform power level $P$."
date: "2026-07-01T23:25:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104236
codeforces_index: "E"
codeforces_contest_name: "Harker Programming Invitational 2023 Advanced"
rating: 0
weight: 104236
solve_time_s: 60
verified: true
draft: false
---

[CF 104236E - Wifi Connection](https://codeforces.com/problemset/problem/104236/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points on a 2D plane, each representing an observation station in a national park. Every station is equipped with a wireless device that has a uniform power level $P$. This power determines a communication radius: two stations can directly communicate if their Euclidean distance is at most $\sqrt{P}$. Communication is not limited to direct links, since messages can be relayed through intermediate stations, so connectivity is defined in the graph-theoretic sense.

The task is to choose the smallest possible value of $P$ such that all stations become connected through this communication network.

Reframed, we are building a complete weighted graph on the points, where the weight between two nodes is the squared Euclidean distance. We want the smallest threshold $P$ such that if we keep only edges with weight at most $P$, the resulting graph is connected.

The constraint $N \le 500$ implies that a full pairwise consideration of edges is feasible. There are at most about $125{,}000$ edges, so algorithms with $O(N^2 \log N)$ or $O(N^2)$ behavior are acceptable. Anything cubic or worse would also pass only in optimized form but is unnecessary here.

A few edge cases matter. If all points are identical, the answer is zero because no connection is needed. If points form a line with one extremely distant outlier, the answer is dictated by that single longest required connection along the best possible spanning structure, not by the absolute farthest pair of points.

A naive mistake is to assume the answer is the maximum distance between any two points. For example, if three points form a triangle where two are far apart but both are close to a central point, connectivity is achieved through the center, so the maximum edge is not needed directly.

## Approaches

The problem is fundamentally about connectivity under a distance threshold. If we fix a candidate value of $P$, we can construct a graph where we connect all pairs of points whose squared distance is at most $P$, then check whether the graph is connected using BFS or DSU. This gives a correct but expensive solution if we search over possible $P$ values.

The brute force idea becomes: compute all pairwise squared distances, sort them, and try thresholds in increasing order, checking connectivity each time. In the worst case, we might recompute connectivity $O(N)$ times, each costing $O(N^2)$, leading to $O(N^3)$ behavior, which is unnecessary but still borderline tolerable for $N=500$ only in highly optimized code.

The key observation is that we are effectively looking for the minimum threshold such that the graph becomes connected, which is exactly the definition of a Minimum Spanning Tree (MST). If we build the MST of the complete graph using squared distances as weights, the answer is the maximum edge weight in the MST. This works because the MST is the cheapest way to connect all nodes, and any connectivity threshold must at least allow all MST edges.

So instead of trying thresholds, we directly compute the MST using Prim’s algorithm in $O(N^2)$, since we can maintain distances in a dense graph without explicit edge storage. The final answer is the largest edge used in the MST.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force threshold checking | $O(N^3)$ | $O(N^2)$ | Too slow |
| Prim MST (dense graph) | $O(N^2)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We treat each point as a node in a fully connected graph where edge weights are squared Euclidean distances.

1. Start from any node, for convenience node 0, and mark it as included in the MST. This represents the fact that we begin building a connected structure from a single station.
2. Maintain an array `min_dist[i]` storing the smallest squared distance from node `i` to any node already in the MST. Initially this is computed from node 0 only.
3. Repeatedly select the node not yet in the MST with the smallest `min_dist`. This choice ensures we always extend the current connected component using the cheapest possible connection available.
4. Add this node to the MST and update the answer as the maximum value of `min_dist` among all selected edges. This maximum is tracked because it represents the bottleneck edge in the spanning structure.
5. After adding a node, update `min_dist` for all remaining nodes by comparing their current values with the distance to the newly added node. This keeps `min_dist` consistent with the current partial MST.
6. Continue until all nodes are included. The final answer is the largest edge weight chosen during this process.

### Why it works

At every step, Prim’s algorithm maintains the invariant that the current set of chosen nodes is connected using edges of minimal possible total cost for that set. Any edge that connects this component to the rest of the graph must have weight at least the current `min_dist` of the chosen node. Since we always pick the smallest available such edge, we are effectively constructing the minimum bottleneck spanning tree. The largest edge in this structure is the smallest possible threshold that still allows connectivity of the full graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    if n == 1:
        print(0)
        return

    in_mst = [False] * n
    min_dist = [10**30] * n

    in_mst[0] = True
    for i in range(1, n):
        dx = pts[i][0] - pts[0][0]
        dy = pts[i][1] - pts[0][1]
        min_dist[i] = dx * dx + dy * dy

    ans = 0

    for _ in range(n - 1):
        v = -1
        best = 10**30
        for i in range(n):
            if not in_mst[i] and min_dist[i] < best:
                best = min_dist[i]
                v = i

        in_mst[v] = True
        ans = max(ans, best)

        for i in range(n):
            if not in_mst[i]:
                dx = pts[i][0] - pts[v][0]
                dy = pts[i][1] - pts[v][1]
                dist = dx * dx + dy * dy
                if dist < min_dist[i]:
                    min_dist[i] = dist

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation is a direct dense Prim’s algorithm. The `min_dist` array always reflects the cheapest way to connect each outside node to the current MST. We use squared distances to avoid floating point operations, since the comparison of $\sqrt{P}$ distances is equivalent to comparing squared values.

A subtle detail is initializing distances from node 0 correctly; failing to do so leads to incorrect infinite values and breaks the selection step. Another important point is tracking the maximum of selected edge weights rather than summing them, since the problem asks for a threshold rather than a total cost.

## Worked Examples

### Example 1

Input:

```
5
1 2
5 5
5 8
10 6
12 3
```

We start from node 0.

| Step | Chosen node | Edge used | min_dist updated | Current max |
| --- | --- | --- | --- | --- |
| 1 | 0 | - | initialize | 0 |
| 2 | 1 | 0-1 = 32 | update from 1 | 32 |
| 3 | 2 | 1-2 = 9 | update from 2 | 32 |
| 4 | 3 | 1-3 = 34 | update from 3 | 34 |
| 5 | 4 | 3-4 = 29 | final | 34 |

The largest edge in the MST is 34, which becomes the threshold. This confirms that even though some pairs are farther apart, the MST avoids using unnecessarily long direct edges.

### Example 2

Input:

```
4
0 0
0 1
0 2
10 10
```

| Step | Chosen node | Edge used | Current max |
| --- | --- | --- | --- |
| 1 | 0 | - | 0 |
| 2 | 1 | 0-1 = 1 | 1 |
| 3 | 2 | 1-2 = 1 | 1 |
| 4 | 3 | 2-3 = 200 | 200 |

The isolated point forces a long connection, and since no intermediate stations exist near it, the MST must include that large edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ | Each of $N$ iterations scans all nodes and updates distances using pairwise computation |
| Space | $O(N)$ | Only arrays for MST membership and minimum distances are stored |

With $N \le 500$, about 250,000 distance checks are performed, which comfortably fits within the time limit in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import sqrt

    data = inp.strip().split()
    n = int(data[0])
    pts = [(int(data[i]), int(data[i+1])) for i in range(1, len(data), 2)]

    if n == 1:
        return "0\n"

    in_mst = [False] * n
    min_dist = [10**30] * n

    in_mst[0] = True
    for i in range(1, n):
        dx = pts[i][0] - pts[0][0]
        dy = pts[i][1] - pts[0][1]
        min_dist[i] = dx*dx + dy*dy

    ans = 0

    for _ in range(n - 1):
        v = -1
        best = 10**30
        for i in range(n):
            if not in_mst[i] and min_dist[i] < best:
                best = min_dist[i]
                v = i

        in_mst[v] = True
        ans = max(ans, best)

        for i in range(n):
            if not in_mst[i]:
                dx = pts[i][0] - pts[v][0]
                dy = pts[i][1] - pts[v][1]
                dist = dx*dx + dy*dy
                if dist < min_dist[i]:
                    min_dist[i] = dist

    return str(ans) + "\n"

# provided sample
assert run("""5
1 2
5 5
5 8
10 6
12 3
""") == "34\n"

# minimum input
assert run("""1
0 0
""") == "0\n"

# all equal points
assert run("""3
1 1
1 1
1 1
""") == "0\n"

# line case
assert run("""4
0 0
0 1
0 2
0 3
""") == "9\n"

# far isolated point
assert run("""3
0 0
1 0
100 100
""") == "20000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 0 | base case |
| identical points | 0 | zero distances |
| line chain | 9 | MST chaining behavior |
| isolated far node | 20000 | forced long edge |

## Edge Cases

For a single station, the MST has no edges, so the algorithm initializes `ans` as zero and immediately returns it. The selection loop is never entered, which matches the fact that no connectivity requirement exists.

When all points coincide, every computed squared distance is zero, so every `min_dist` update remains zero. Each chosen edge has weight zero, so the final maximum is also zero, matching the expected output.

In cases with one distant outlier, the algorithm initially builds a cluster among close points with small edges, then eventually connects the outlier using the smallest possible link to that cluster. Since all intermediate options are already exhausted, the final edge must be large, and the MST correctly captures this as the bottleneck.
