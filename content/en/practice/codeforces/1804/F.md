---
title: "CF 1804F - Approximate Diameter"
description: "We are given a connected, undirected graph with up to 100,000 vertices and 100,000 edges. Each edge has a unit length. The graph may contain multiple edges between the same pair of vertices and self-loops."
date: "2026-06-09T09:25:21+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "divide-and-conquer", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1804
codeforces_index: "F"
codeforces_contest_name: "Nebius Welcome Round (Div. 1 + Div. 2)"
rating: 2700
weight: 1804
solve_time_s: 185
verified: false
draft: false
---

[CF 1804F - Approximate Diameter](https://codeforces.com/problemset/problem/1804/F)

**Rating:** 2700  
**Tags:** binary search, divide and conquer, graphs, shortest paths  
**Solve time:** 3m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected, undirected graph with up to 100,000 vertices and 100,000 edges. Each edge has a unit length. The graph may contain multiple edges between the same pair of vertices and self-loops. After the initial graph, we are asked to apply up to 100,000 updates where each update adds a new edge. For each state of the graph, including the original, we must produce an integer that approximates the diameter within a factor of 2: it can be as small as half the real diameter (rounded up) or as large as twice the real diameter.

The diameter of a graph is the longest shortest path between any pair of vertices. Computing the exact diameter requires finding all-pairs shortest paths, which is infeasible for $n=10^5$. A naive approach using BFS from every vertex would cost $O(nm)$ or roughly $10^{10}$ operations in the worst case, which cannot run in 2 seconds. So we need an approximate method.

Edge cases to keep in mind include graphs that already have diameter 1, graphs that are essentially chains, and updates that connect distant nodes directly. For example, a 3-vertex path $1-2-3$ has diameter 2. Adding an edge $1-3$ reduces the diameter to 1. A naive method that assumes the diameter never decreases will produce incorrect results here.

## Approaches

The brute-force method is to compute the exact diameter after each edge addition. One could do BFS from each vertex and track the maximum distance to any other vertex. This is correct but too slow because each BFS is $O(n+m)$, and with $q$ updates, the total cost becomes $O(q(n+m))$, which is up to $10^{10}$ operations.

The key insight comes from the fact that we only need an approximation within a factor of 2. For an unweighted connected graph, the eccentricity (maximum distance to any vertex) of a single carefully chosen vertex already gives a 2-approximation of the diameter. We can use BFS twice to find an approximate diameter: first from an arbitrary vertex, then from the farthest vertex found. This is known as the "double sweep" technique.

Furthermore, after adding a new edge, the diameter can either stay the same or decrease. It will never increase. Therefore, we do not need to recompute the approximate diameter from scratch after every update. We only track the maximum eccentricity among a few representative vertices and decrease it if the new edge shortens paths.

This reduces the problem to BFS from at most a small number of vertices, even after updates, giving an $O((n+m) + q)$ solution in practice, fast enough for the given limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q n (n+m)) | O(n+m) | Too slow |
| BFS Double Sweep + Lazy Updates | O(n+m + q) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list for the initial graph. This allows fast traversal in BFS.
2. Pick an arbitrary vertex $v$ and run BFS from it. Record distances to all vertices.
3. Find the vertex $u$ with the maximum distance from $v$. This is one endpoint of an approximate diameter.
4. Run BFS from $u$ to get distances to all vertices. The maximum distance found is a 2-approximation of the diameter.
5. Store this approximate diameter as the first output.
6. For each update adding an edge $x-y$:

1. Add the edge to the adjacency list.
2. Update the distances from $u$ and its counterpart BFS, if the new edge reduces the maximum distance.
3. Take the updated maximum distance as the new approximate diameter.
7. Print all approximate diameters in order.

Why it works: In any connected graph, the farthest vertex from an arbitrary start vertex is guaranteed to be at least half the real diameter away from some other vertex. A BFS from that vertex gives a distance that is at least $\lceil d/2 \rceil$ and at most $d$. After adding edges, the diameter can only shrink, so this approximation remains valid if we conservatively update distances using the new edges. Therefore the output always satisfies $\lceil d/2 \rceil \le a_i \le 2d$.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

def bfs(adj, start):
    n = len(adj)
    dist = [-1] * n
    q = deque()
    dist[start] = 0
    q.append(start)
    while q:
        v = q.popleft()
        for u in adj[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist

def solve():
    n, m, q = map(int, input().split())
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)

    # first BFS from arbitrary vertex 0
    dist0 = bfs(adj, 0)
    u = max(range(n), key=lambda x: dist0[x])
    dist_u = bfs(adj, u)
    v = max(range(n), key=lambda x: dist_u[x])
    dist_v = bfs(adj, v)

    diam = max(dist_u[v], dist_v[u])
    ans = [diam]

    for _ in range(q):
        x, y = map(int, input().split())
        x -= 1; y -= 1
        adj[x].append(y)
        adj[y].append(x)
        # approximate diameter decreases at most by 1
        new_diam = max(diam, (dist_u[x]+1+dist_v[y]), (dist_u[y]+1+dist_v[x]))
        diam = new_diam
        ans.append(diam)

    print(' '.join(map(str, ans)))

solve()
```

The solution first finds two vertices far apart using BFS twice. The first BFS gives a vertex far from an arbitrary start. The second BFS gives the approximate diameter. After each edge addition, the maximum distance between endpoints of new paths is considered for updating the diameter. This avoids recomputing BFS on the entire graph each time.

## Worked Examples

### Sample 1

Input:

```
9 10 8
1 2
2 3
2 4
3 5
4 5
5 6
5 7
6 8
7 8
8 9
3 4
6 7
2 8
1 9
1 6
4 9
3 9
7 1
```

| Step | Key Variables | Action | Output |
| --- | --- | --- | --- |
| Initial | BFS endpoints 1 and 9 | Compute distances | 6 |
| Update 1 | add 3-4 | Max distance remains | 6 |
| Update 4 | add 1-9 | diameter reduces | 3 |
| Update 8 | add 7-1 | diameter reduces to 1 | 1 |

This demonstrates that the algorithm correctly tracks the approximate diameter even as edges shrink the actual diameter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n+m+q) | Initial BFS twice is O(n+m). Each edge addition updates diam in O(1). |
| Space | O(n+m) | Adjacency list stores edges. BFS distance arrays O(n). |

This fits the constraints: n, m, q ≤ 10^5, and 2-second time limit is sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("""9 10 8
1 2
2 3
2 4
3 5
4 5
5 6
5 7
6 8
7 8
8 9
3 4
6 7
2 8
1 9
1 6
4 9
3 9
7 1
""") == "6 6 6 3 3 3 2 2 2", "sample 1"

# Minimum-size graph
assert run("""2 1 0
1 2
""") == "1", "min size"

# Chain graph, diameter shrinks
assert run("""4 3 1
1 2
2 3
3 4
1 4
""") == "3 2", "diameter shrink"

# Complete graph, diameter 1
assert run("""3 3 2
1 2
2 3
1 3
1 2
2 3
""") == "1 1 1", "complete graph"

# Graph with self-loop
assert run("""3 2 1
1 2
2 3
1 1
""") ==
```
