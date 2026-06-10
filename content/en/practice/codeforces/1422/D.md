---
title: "CF 1422D - Returning Home"
description: "We are moving on an enormous grid. The starting cell is $(sx,sy)$ and the destination is $(fx,fy)$. Walking works normally: moving one cell horizontally or vertically costs one minute, so the cost of walking between two positions is Manhattan distance."
date: "2026-06-11T06:22:12+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "shortest-paths", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1422
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 675 (Div. 2)"
rating: 2300
weight: 1422
solve_time_s: 205
verified: true
draft: false
---

[CF 1422D - Returning Home](https://codeforces.com/problemset/problem/1422/D)

**Rating:** 2300  
**Tags:** graphs, shortest paths, sortings  
**Solve time:** 3m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are moving on an enormous grid. The starting cell is $(s_x,s_y)$ and the destination is $(f_x,f_y)$. Walking works normally: moving one cell horizontally or vertically costs one minute, so the cost of walking between two positions is Manhattan distance.

There are also special locations. A special location $(x_i,y_i)$ can be reached instantly from any position that shares its $x$-coordinate or its $y$-coordinate. Equivalently, if we are standing at $(a,b)$, we can move to $(x_i,y_i)$ at cost

$$\min(|a-x_i|,\;|b-y_i|).$$

If the $x$-coordinates already match, the first term is zero and the teleport is free. The same happens when the $y$-coordinates match.

The task is to find the minimum time required to reach home.

The city size $n$ can be as large as $10^9$, which immediately tells us that the grid itself cannot be represented. The number of special locations is at most $10^5$, so any solution that works directly on the set of special locations is feasible. A graph with $10^5$ vertices is manageable, but a graph with all pairwise edges would contain about $10^{10}$ edges, which is completely impossible.

The most dangerous part of the problem is understanding how teleports interact.

Consider:

```
start = (1,1)
finish = (100,100)

special:
(1,50)
(50,50)
```

The first special point is reachable for free because the $x$-coordinate already matches. After arriving at $(1,50)$, the second special point can be reached with cost $\min(49,0)=0$ because the $y$-coordinates match. A solution that only considers ordinary Manhattan distances between special points misses this chain of free moves.

Another subtle case is when using no special point is optimal.

```
start = (1,1)
finish = (3,3)
```

with no special locations.

The answer is simply $4$. Any graph construction must include the possibility of walking directly to the destination.

A third trap is assuming every pair of special points needs an edge.

```
(1,100)
(2,100)
(1000000000,100)
```

The useful transitions come from neighboring points after sorting by coordinates. Connecting every pair would be correct but far too slow. The key observation is that only nearest neighbors in sorted order matter.

## Approaches

A natural first idea is to build a graph whose vertices are the special locations together with the start and finish positions.

Suppose we create an edge between every pair of special locations. The cost of moving from special point $i$ to special point $j$ is

$$\min(|x_i-x_j|,\;|y_i-y_j|).$$

We can also connect the start to every special point with cost

$$\min(|s_x-x_i|,\;|s_y-y_i|).$$

Finally, every vertex can walk directly to the destination with Manhattan distance.

This graph models the problem correctly, and Dijkstra's algorithm would find the answer.

The problem is size. With $m=10^5$, a complete graph contains roughly

$$\frac{m(m-1)}2 \approx 5 \cdot 10^9$$

edges. Storing or processing that graph is impossible.

The breakthrough comes from examining the edge weight

$$\min(|x_i-x_j|,\;|y_i-y_j|).$$

Suppose two points are connected because their $x$-coordinates are close. When points are sorted by $x$, the cheapest useful connection through the $x$-dimension always appears between neighboring points in that ordering.

This is the same observation used in several geometric shortest-path problems. If point $A$ and point $C$ are separated by another point $B$ in sorted $x$-order, then

$$|x_A-x_C|$$

cannot be smaller than both neighboring gaps. Any path that wants to exploit small $x$-difference can do so through adjacent points.

The same reasoning holds for the $y$-coordinate.

So instead of connecting every pair, we sort the special points by $x$ and connect neighboring pairs. Then we sort by $y$ and connect neighboring pairs again. The resulting graph has only $O(m)$ edges.

After this reduction, Dijkstra's algorithm runs comfortably within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force complete graph | $O(m^2 \log m)$ | $O(m^2)$ | Too slow |
| Neighbor graph + Dijkstra | $O(m \log m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

### Graph interpretation

Each special location becomes a graph vertex.

We do not create a vertex for the start position. Instead, the start provides the initial distance for every special location.

We also do not create a vertex for the destination. Reaching home is treated as a final walking step from any visited location.

### Steps

1. Read all special locations and assign each one an index.
2. Sort the special locations by $x$-coordinate.
3. For every adjacent pair in this ordering, add an undirected edge whose weight equals the difference in $x$-coordinates.

The shortest transition based on the $x$-dimension can always be represented through neighboring points in sorted order.
4. Sort the special locations by $y$-coordinate.
5. For every adjacent pair in this ordering, add an undirected edge whose weight equals the difference in $y$-coordinates.

This captures all useful transitions based on the $y$-dimension.
6. Initialize Dijkstra.

For every special point $i$,

$$dist[i] =
\min(|s_x-x_i|,\;|s_y-y_i|).$$

This is exactly the cost of reaching that special location from the start.
7. Initialize the answer with the cost of walking directly from start to finish:

$$|s_x-f_x|+|s_y-f_y|.$$
8. Run Dijkstra on the graph of special locations.
9. Whenever a vertex $i$ is extracted from the priority queue, update the answer using

$$dist[i] + |x_i-f_x| + |y_i-f_y|.$$

This represents using teleports up to point $i$, then walking directly home.
10. Relax all graph edges in the usual Dijkstra manner.
11. After Dijkstra finishes, output the smallest answer found.

### Why it works

The crucial property is that every useful transition between special locations can be decomposed into moves between neighboring points in sorted $x$-order or sorted $y$-order.

Suppose an optimal path uses an edge whose cost is determined by the $x$-difference. Moving through consecutive points in sorted $x$-order reproduces that cost without increasing it, because the sum of consecutive coordinate gaps equals the total gap. The same argument holds for the $y$-dimension.

As a result, every optimal route in the complete graph has an equivalent route in the sparse graph built from neighboring pairs only. Dijkstra then computes the shortest distances to all special locations, and combining each of them with the final Manhattan walk to home examines every possible optimal strategy.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    sx, sy, fx, fy = map(int, input().split())

    pts = []
    for i in range(m):
        x, y = map(int, input().split())
        pts.append((x, y, i))

    g = [[] for _ in range(m)]

    by_x = sorted(pts)
    for i in range(m - 1):
        x1, y1, id1 = by_x[i]
        x2, y2, id2 = by_x[i + 1]
        w = x2 - x1
        g[id1].append((id2, w))
        g[id2].append((id1, w))

    by_y = sorted(pts, key=lambda p: p[1])
    for i in range(m - 1):
        x1, y1, id1 = by_y[i]
        x2, y2, id2 = by_y[i + 1]
        w = y2 - y1
        g[id1].append((id2, w))
        g[id2].append((id1, w))

    INF = 10**30
    dist = [INF] * m
    pq = []

    for x, y, idx in pts:
        d = min(abs(sx - x), abs(sy - y))
        dist[idx] = d
        heapq.heappush(pq, (d, idx))

    ans = abs(sx - fx) + abs(sy - fy)

    while pq:
        curd, v = heapq.heappop(pq)
        if curd != dist[v]:
            continue

        x, y, _ = pts[v]

        ans = min(
            ans,
            curd + abs(x - fx) + abs(y - fy)
        )

        for to, w in g[v]:
            nd = curd + w
            if nd < dist[to]:
                dist[to] = nd
                heapq.heappush(pq, (nd, to))

    print(ans)

solve()
```

The graph contains only special locations. The start position appears through the initial Dijkstra distances, which exactly match the cost of reaching each special point from the start.

The two sorting passes create the sparse graph. A common mistake is using

$$\min(|x_i-x_j|, |y_i-y_j|)$$

as the edge weight between neighboring points. The accepted solution uses only the coordinate difference corresponding to the sorting order. This is the key compression argument from the official solution.

Another subtle point is the final answer update. Reaching a special point does not force further teleport usage. At any moment we may stop and walk directly home, so every extracted vertex contributes a candidate answer.

All values fit easily inside 64-bit integers, but Python integers remove any overflow concerns.

## Worked Examples

### Sample 1

Input:

```
5 3
1 1 5 5
1 2
4 1
3 3
```

Special points:

| Index | Point |
| --- | --- |
| 0 | (1,2) |
| 1 | (4,1) |
| 2 | (3,3) |

Initial distances:

| Vertex | Cost from start |
| --- | --- |
| (1,2) | 0 |
| (4,1) | 0 |
| (3,3) | 2 |

Dijkstra progression:

| Popped vertex | Distance | Best answer so far |
| --- | --- | --- |
| (1,2) | 0 | 7 |
| (4,1) | 0 | 5 |
| (3,3) | 2 | 4+2=6 |

The minimum found is 5.

This trace shows why direct walking is not always optimal. The teleports allow us to reach $(4,1)$ for free and save part of the route.

### Example 2

Input:

```
10 2
1 1 10 10
1 7
7 7
```

Initial distances:

| Vertex | Cost |
| --- | --- |
| (1,7) | 0 |
| (7,7) | 6 |

Dijkstra:

| Popped vertex | Distance | Candidate answer |
| --- | --- | --- |
| (1,7) | 0 | 12 |
| (7,7) | 6 | 12 |

Direct walking costs $18$, so the answer becomes $12$.

This example demonstrates how reaching a teleport point for free can significantly shorten the journey.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m)$ | Two sorts and Dijkstra on $O(m)$ edges |
| Space | $O(m)$ | Graph, distances, and priority queue |

With $m \le 10^5$, sorting dominates the runtime. $m \log m$ is roughly a few million operations, well within a 2-second limit in Python. The graph contains only linear many edges, so memory usage remains comfortably below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    sx, sy, fx, fy = map(int, input().split()

)
    pts = []
    for i in range(m):
        x, y = map(int, input().split())
        pts.append((x, y, i))

    g = [[] for _ in range(m)]

    by_x = sorted(pts)
    for i in range(m - 1):
        x1, y1, a = by_x[i]
        x2, y2, b = by_x[i + 1]
        w = x2 - x1
        g[a].append((b, w))
        g[b].append((a, w))

    by_y = sorted(pts, key=lambda p: p[1])
    for i in range(m - 1):
        x1, y1, a = by_y[i]
        x2, y2, b = by_y[i + 1]
        w = y2 - y1
        g[a].append((b, w))
        g[b].append((a, w))

    INF = 10**30
    dist = [INF] * m
    pq = []

    for x, y, idx in pts:
        d = min(abs(sx - x), abs(sy - y))
        dist[idx] = d
        heapq.heappush(pq, (d, idx))

    ans = abs(sx - fx) + abs(sy - fy)

    while pq:
        d, v = heapq.heappop(pq)
        if d != dist[v]:
            continue

        x, y, _ = pts[v]
        ans = min(ans, d + abs(x - fx) + abs(y - fy))

        for to, w in g[v]:
            nd = d + w
            if nd < dist[to]:
                dist[to] = nd
                heapq.heappush(pq, (nd, to))

    return str(ans) + "\n"

# sample
assert run(
"""5 3
1 1 5 5
1 2
4 1
3 3
"""
) == "5\n"

# no special locations
assert run(
"""10 0
1 1 10 10
"""
) == "18\n"

# start equals finish
assert run(
"""100 0
5 5 5 5
"""
) == "0\n"

# teleport immediately reachable
assert run(
"""10 1
1 1 10 10
1 10
"""
) == "9\n"

# large coordinate boundary
assert run(
"""1000000000 1
1 1 1000000000 1000000000
1 1000000000
"""
) == "999999999\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| No special locations | 18 | Direct Manhattan path |
| Start equals finish | 0 | Zero-distance answer |
| Immediate teleport access | 9 | Free access through matching coordinate |
| Large coordinates | 999999999 | Correct handling of $10^9$-scale values |

## Edge Cases

### No special locations

Input:

```
10 0
1 1 10 10
```

The graph is empty. Dijkstra never processes any vertex. The initial answer is the Manhattan distance

$$18.$$

That value is printed directly.

### Destination already reached

Input:

```
100 0
5 5 5 5
```

The direct-walk answer starts at zero. No route can improve on that, so the algorithm outputs zero.

### Free chain through matching coordinates

Input:

```
100 2
1 1 100 100
1 50
50 50
```

The first special point has initial distance zero because its $x$-coordinate matches the start.

The second point is connected through a zero-cost $y$-transition.

Dijkstra propagates this free movement correctly and discovers the optimal route. This confirms that chains of teleports are naturally handled by the graph construction.

### Extremely large grid

Input:

```
1000000000 1
1 1 1000000000 1000000000
1 1000000000
```

The grid itself is never represented. Only coordinates are stored. All computations use differences between coordinates, so the algorithm remains $O(m \log m)$ regardless of the size of $n$.
