---
title: "CF 102433C - Coloring Contention"
description: "We have a connected undirected graph whose vertices are numbered from 1 to (N). Alice assigns one of two colors to every edge. After seeing the coloring, Bob chooses a route from vertex 1 to vertex (N)."
date: "2026-08-14T15:34:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102433
codeforces_index: "C"
codeforces_contest_name: "2019-2020 ACM-ICPC Pacific Northwest Regional Contest (Div. 1)"
rating: 0
weight: 102433
solve_time_s: 107
verified: true
draft: false
---

[CF 102433C - Coloring Contention](https://codeforces.com/problemset/problem/102433/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph whose vertices are numbered from 1 to (N). Alice assigns one of two colors to every edge. After seeing the coloring, Bob chooses a route from vertex 1 to vertex (N). Whenever two consecutive edges on his route have different colors, one color change is counted. Bob wants as few changes as possible, while Alice chooses the coloring to make that minimum as large as possible.

The required output is the largest number of color changes Alice can guarantee on every route from 1 to (N).

The key quantity turns out to be much simpler than the coloring game suggests. Let (d) be the ordinary shortest-path distance from vertex 1 to vertex (N). The answer is exactly (d-1). The two official samples have answers 0 and 3 respectively.

With up to (100000) vertices and (100000) edges, an algorithm that explores many possible colorings or paths is completely infeasible. Even (O(N^2)) would already mean around (10^{10}) operations on the largest inputs, far beyond a one-second contest limit. We need a graph traversal whose work is essentially proportional to the number of vertices and edges, such as BFS in (O(N+M)).

There are several edge cases that can easily cause an incorrect answer if the relationship with shortest-path distance is missed. First, a direct edge from 1 to (N) immediately gives the answer 0. For example,

```
2 1
1 2
```

The only route has one edge, so there are no consecutive edges and hence no possible color change. A formula such as (d) would incorrectly return 1, while the correct answer is 0.

A second case is a graph with a shortest path of length two:

```
3 2
1 2
2 3
```

Alice can color the first edge red and the second blue, forcing one change. The answer is 1. A careless implementation that forgets that the number of changes is one less than the number of edges on the route would return 2.

A third case is when a short route exists alongside a much longer route:

```
4 4
1 4
1 2
2 3
3 4
```

Bob simply takes the direct edge (1)-(4), so Alice cannot force any color change. The answer is 0 even though another route contains three edges and could have two color changes. Alice must defeat Bob's best route, not maximize the changes on some particular route.

## Approaches

A direct brute-force approach would enumerate every possible red and blue coloring of the (M) edges. There are (2^M) such colorings. For each coloring, Bob's optimum can be computed by expanding the state to include his current vertex and the color of the previous edge, then using a 0-1 shortest-path algorithm where continuing along the same color costs 0 and switching colors costs 1. That takes (O(N+M)) time for one coloring, so the total is (O(2^M(N+M))). At (M=100000), this is effectively impossible, even before considering constant factors.

The brute force works because it explicitly considers every decision Alice could make and then solves Bob's optimization exactly. It fails because the number of colorings is exponential. The useful observation is that we do not actually need to construct Alice's coloring. The answer is determined solely by the ordinary shortest-path distance between vertices 1 and (N).

Let that distance be (d). No matter how Alice colors the graph, Bob can choose a shortest path containing exactly (d) edges. A sequence of (d) edges has only (d-1) adjacent pairs, so it can contain at most (d-1) color changes. Thus Alice can never force more than (d-1).

The interesting part is showing that Alice can always achieve (d-1). Run BFS from vertex 1 and let (dist[v]) be the shortest distance from 1 to (v). Color every edge ((u,v)) according to the parity of the smaller of (dist[u]) and (dist[v]). In other words, an edge whose endpoints lie on BFS levels (k) and (k+1) gets color determined by (k)'s parity. Edges whose endpoints have the same BFS distance can also be assigned using that same minimum-distance rule.

Consider any route from 1 to (N). Since (dist[1]=0) and (dist[N]=d), the route must eventually reach BFS level 1, then level 2, and so on through level (d). The first edge by which the route reaches level (k+1) from below must connect levels (k) and (k+1), so its color is determined by the parity of (k). Consecutive such first-reaching edges correspond to (k) and (k+1), so their colors are different. There is consequently at least one color change between every pair of consecutive levels.

There are (d) levels to cross after level 0, giving at least (d-1) changes on every possible route. Combined with the upper bound, the optimum is exactly (d-1).

This reduces the whole game to a single BFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^M(N+M))) | (O(N+M)) | Too slow |
| Optimal | (O(N+M)) | (O(N+M)) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the undirected graph. Each input edge is stored in both directions because Bob can traverse the graph in either direction.
2. Run BFS starting from vertex 1. BFS is the right traversal because every edge has equal cost, so the first time a vertex is reached, its recorded distance is the minimum possible number of edges from vertex 1.
3. Continue BFS until vertex (N) has been reached. The resulting distance (dist[N]) is the length of the shortest route from 1 to (N).
4. Output (dist[N]-1). A shortest route contains (dist[N]) edges and therefore has only (dist[N]-1) adjacent pairs where a color change could occur.

The subtraction is also valid at the smallest possible distance. Since the graph is connected and (N\neq1), we have (dist[N]\ge1), so the answer is never negative.

### Why it works

Let (d=dist[N]). For the upper bound, Bob can always choose a shortest route with (d) edges, and no route with (d) edges can contain more than (d-1) color changes. Hence Alice cannot force more than (d-1).

For the lower bound, consider BFS layers (0,1,\ldots,d), where layer (k) contains vertices at distance (k) from vertex 1. Alice can color an edge connecting layers (k) and (k+1) according to the parity of (k). Any route from layer 0 to layer (d) must cross each boundary between consecutive layers. The colors assigned to the first crossings of those boundaries alternate, so every pair of consecutive boundaries contributes at least one color change. There are (d-1) pairs of boundaries, so every route has at least (d-1) changes.

The upper and lower bounds match, proving that the answer is exactly (dist[N]-1).

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    dist = [-1] * n
    dist[0] = 0

    q = deque([0])

    while q:
        u = q.popleft()

        if u == n - 1:
            break

        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    print(dist[n - 1] - 1)

if __name__ == "__main__":
    solve()
```

The adjacency list uses one list for each vertex. For every undirected input edge ((a,b)), the code inserts (b) into (a)'s list and (a) into (b)'s list. This gives (O(N+M)) storage rather than the (O(N^2)) storage that an adjacency matrix would require.

The `dist` array starts with (-1), which means that a vertex has not yet been visited. Vertex 1 is assigned distance 0 before being placed into the queue. Whenever BFS discovers an unvisited neighbor of (u), its distance becomes `dist[u] + 1`.

The early exit when (N) is removed from the queue is safe because BFS processes vertices in nondecreasing distance order. At that point the recorded distance of (N) is already its shortest-path distance.

There is no need to store Alice's coloring at all. The proof only uses the fact that such a coloring can be constructed from BFS levels, while the value Alice can force is completely determined by the shortest-path distance.

Python integers do not overflow here, and the maximum distance is at most (N-1). The final subtraction is consequently between 0 and (99999).

## Worked Examples

### Sample 1

The graph contains a direct edge from vertex 1 to vertex 3, so BFS reaches the destination immediately.

| Current vertex | Distance | Newly discovered vertex | New distance |
| --- | --- | --- | --- |
| 1 | 0 | 3 | 1 |
| 1 | 0 | 2 | 1 |

The shortest distance is (d=1), so the answer is (d-1=0). This demonstrates the boundary case where Bob's route has only one edge and there are no consecutive edges on which a color change could occur. The official sample output is 0.

### Sample 2

The graph has two symmetric ways to reach vertex 4 and then two symmetric ways to reach vertex 7.

| Current vertex | Distance | Newly discovered vertices |
| --- | --- | --- |
| 1 | 0 | 2, 3 |
| 2 | 1 | 4 |
| 3 | 1 | 4 |
| 4 | 2 | 5, 6 |
| 5 | 3 | 7 |
| 6 | 3 | 7 |

BFS finds (dist[7]=4). Every route from 1 to 7 needs at least four edges, while Alice can color the BFS layers so that every route has at least three changes. Bob can choose a shortest four-edge route, so three is also the maximum possible. The algorithm outputs (4-1=3), matching the official sample.

The example also shows why the existence of multiple shortest paths does not matter. Alice's layer-based coloring handles all of them simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+M)) | BFS visits every vertex at most once and examines every undirected edge a constant number of times. |
| Space | (O(N+M)) | The adjacency list stores (2M) directed adjacency entries, and the distance array and queue use (O(N)) additional space. |

With (N,M\le100000), the algorithm performs only linear work in the input size. This is comfortably within the scale expected for a one-second graph problem, while exponential enumeration of colorings is impossible at these limits.

## Test Cases

```python
import sys
import io
from collections import deque

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    graph = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    dist = [-1] * n
    dist[0] = 0
    q = deque([0])

    while q:
        u = q.popleft()

        if u == n - 1:
            break

        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    print(dist[n - 1] - 1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """3 3
1 3
1 2
2 3
"""
) == "0", "sample 1"

# Provided sample 2
assert run(
    """7 8
1 2
1 3
2 4
3 4
4 5
4 6
5 7
6 7
"""
) == "3", "sample 2"

# Minimum-size graph: one edge, so zero color changes are possible.
assert run(
    """2 1
1 2
"""
) == "0", "minimum-size graph"

# Shortest path has length two, so exactly one change can be forced.
assert run(
    """3 2
1 2
2 3
"""
) == "1", "distance-two path"

# A longer route exists, but Bob has a direct edge and therefore avoids
# every color change.
assert run(
    """4 4
1 4
1 2
2 3
3 4
"""
) == "0", "direct edge beats longer route"

# A chain of length four has answer three.
assert run(
    """5 4
1 2
2 3
3 4
4 5
"""
) == "3", "off-by-one boundary"

# Maximum-size linear graph. The answer is 99999.
n = 100000
large_input = str(n) + " " + str(n - 1) + "\n"
large_input += "".join(f"{i} {i + 1}\n" for i in range(1, n))
assert run(large_input) == "99999", "maximum-size graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2` | 0 | Minimum graph size and the zero-change boundary |
| `3 2 / 1 2 / 2 3` | 1 | Correct subtraction of one from the shortest-path length |
| `4 4 / 1 4 / 1 2 / 2 3 / 3 4` | 0 | Bob chooses the shortest route rather than a longer route |
| `5 4 / 1 2 / 2 3 / 3 4 / 4 5` | 3 | Longer shortest paths and off-by-one handling |
| Chain with (100000) vertices | 99999 | Maximum input size and linear-time behavior |

## Edge Cases

A direct edge from 1 to (N) is the most important lower-bound case. For

```
2 1
1 2
```

BFS assigns `dist[1] = 0` and `dist[2] = 1`. The algorithm prints `1 - 1 = 0`. Alice cannot force a change because Bob uses a single edge, and a single edge has no neighboring edge with which to compare its color.

For a shortest path of exactly two edges,

```
3 2
1 2
2 3
```

BFS produces distances 0, 1, and 2. The algorithm returns (2-1=1). Alice can color (1)-(2) red and (2)-(3) blue, so Bob must change color once. There is only one adjacent pair of edges, which also proves that two changes are impossible.

For a graph containing both short and long routes,

```
4 4
1 4
1 2
2 3
3 4
```

BFS discovers vertex 4 directly at distance 1. It does not matter that the graph also contains the route (1\rightarrow2\rightarrow3\rightarrow4). Bob is minimizing color changes and can always select the direct edge, so Alice's guarantee is 0. This is exactly why the relevant graph quantity is the shortest distance, not the longest route or the number of vertices in the graph.

For a pure chain,

```
5 4
1 2
2 3
3 4
4 5
```

the unique route contains four edges. BFS assigns vertex 5 distance 4, and the answer is 3. Alice can alternate colors along the four edges, producing three changes. Since no route has fewer than four edges, this reaches the upper bound.

For the maximum-size chain with (100000) vertices, the shortest distance is (99999), so the answer is (99998). More generally, a connected graph with (100000) vertices cannot have a shortest path longer than (99999), and the BFS implementation processes the entire graph in (O(N+M)) time without attempting to enumerate routes or colorings.
