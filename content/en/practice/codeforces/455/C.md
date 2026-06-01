---
title: "CF 455C - Civilization"
description: "The graph consists of cities connected by roads. The condition that between any two connected cities there is exactly one simple path means every connected component is a tree. Since the graph may be disconnected, the whole graph is a forest."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "dsu", "ternary-search", "trees"]
categories: ["algorithms"]
codeforces_contest: 455
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 260 (Div. 1)"
rating: 2100
weight: 455
solve_time_s: 121
verified: true
draft: false
---

[CF 455C - Civilization](https://codeforces.com/problemset/problem/455/C)

**Rating:** 2100  
**Tags:** dfs and similar, dp, dsu, ternary search, trees  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph consists of cities connected by roads. The condition that between any two connected cities there is exactly one simple path means every connected component is a tree. Since the graph may be disconnected, the whole graph is a forest.

Two types of operations must be processed online.

The first operation asks for the diameter of the connected component containing a given city. Here, the diameter is the length of the longest path inside that tree.

The second operation merges two connected components by adding exactly one new edge between some city in the first component and some city in the second component. We are free to choose the endpoints of this new edge, but we must choose them so that the diameter of the resulting tree is as small as possible.

The graph initially contains up to $3 \cdot 10^5$ vertices and up to $3 \cdot 10^5$ queries. Any solution that recomputes diameters from scratch after every merge is immediately too slow. Even a single DFS over an entire component costs $O(n)$, and doing that for many queries would lead to tens of billions of operations in the worst case.

The key challenge is that components change over time. We need a way to maintain the diameter of each connected component efficiently as components are merged.

Several edge cases are easy to mishandle.

Consider two isolated vertices:

```
2 0 2
2 1 2
1 1
```

After merging, the resulting tree has one edge, so the diameter is 1. A solution that assumes diameters never increase from 0 would be wrong.

Consider merging components that already belong to the same tree:

```
3 2 2
1 2
2 3
2 1 3
1 1
```

The merge operation should do nothing. The answer remains 2. Accidentally applying the diameter update formula anyway would corrupt the stored value.

Another subtle case is when the optimal new edge is not attached to an endpoint of the diameter.

Suppose we merge two paths of length 4. Connecting diameter endpoints produces diameter 9, which is terrible. The optimal choice is connecting the centers of both trees, producing diameter 5. Any approach that only looks at diameter endpoints will fail.

## Approaches

A brute force solution would explicitly maintain every connected component. Whenever a query asks for a diameter, we could run two DFS traversals to compute it. Whenever two components merge, we add the edge and continue.

The standard tree diameter trick works because running DFS from an arbitrary node finds one diameter endpoint, and running DFS again from that endpoint finds the diameter length. The problem is cost. A single diameter computation requires traversing the whole component. With up to $3 \cdot 10^5$ queries, the worst case becomes roughly $O(nq)$, far beyond the limit.

The observation that changes everything is that a merge operation does not ask us to construct the actual optimal edge. It only asks us to maintain the diameter after connecting the two trees in the best possible way.

Suppose two trees have diameters $d_1$ and $d_2$.

For a tree with diameter $d$, its radius is:

$$r = \left\lceil \frac{d}{2} \right\rceil$$

The radius is the minimum possible maximum distance from a chosen center to all vertices.

When merging two trees optimally, we connect their centers. Any other choice can only make the longest path larger.

The resulting diameter becomes:

$$\max\left(d_1,\ d_2,\ r_1 + r_2 + 1\right)$$

The first two terms cover paths entirely inside one original tree. The third term covers paths that cross the new edge.

This means we only need one piece of information per connected component: its diameter.

Since connected components are merged dynamically, Disjoint Set Union is a perfect fit. Each DSU root stores the diameter of its component. A merge operation combines two DSU sets and updates the stored diameter using the formula above.

The remaining task is computing the initial diameter of every tree. Since the graph is a forest, we can process each connected component once using the standard two-DFS diameter computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O((n + q) α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the forest from the input edges.
2. Use DFS to identify every connected component.
3. For each component, compute its diameter using two traversals.

First find the farthest vertex from an arbitrary starting point. Then start from that farthest vertex and find the maximum distance again. That distance is the tree diameter.
4. Initialize a DSU structure.

Each connected component becomes one DSU set, and the root stores the diameter of that component.
5. For a query of type 1, find the DSU representative of the requested city and output the stored diameter.
6. For a query of type 2, find the DSU representatives of both cities.
7. If both representatives are identical, do nothing.

The cities already belong to the same component.
8. Otherwise compute:

$$r_1=\left\lceil\frac{d_1}{2}\right\rceil,\quad r_2=\left\lceil\frac{d_2}{2}\right\rceil$$
9. Compute the new diameter:

$$d=\max(d_1,d_2,r_1+r_2+1)$$
10. Union the two DSU sets and store this new diameter in the resulting root.

### Why it works

Each DSU set always represents exactly one connected component of the current forest.

Initially, diameters are computed correctly by the standard tree-diameter algorithm. For merge operations, connecting the centers minimizes the maximum distance that can pass through the new edge. The longest path in the merged tree must either stay entirely inside the first tree, stay entirely inside the second tree, or cross the new edge. Those three possibilities correspond exactly to:

$$d_1,\quad d_2,\quad r_1+r_2+1$$

Taking their maximum gives the true diameter of the optimally merged tree. Since every union stores this value, the invariant that each DSU root stores the correct diameter remains true after every operation.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())

    g = [[] for _ in range(n)]

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union_initial(a, b):
        ra = find(a)
        rb = find(b)

        if ra == rb:
            return

        if size[ra] < size[rb]:
            ra, rb = rb, ra

        parent[rb] = ra
        size[ra] += size[rb]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1

        g[a].append(b)
        g[b].append(a)

        union_initial(a, b)

    diameter = [0] * n

    visited = [False] * n

    def bfs(start):
        dist = [-1] * n
        dist[start] = 0

        dq = deque([start])
        farthest = start

        while dq:
            v = dq.popleft()

            if dist[v] > dist[farthest]:
                farthest = v

            for to in g[v]:
                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    dq.append(to)

        return farthest, dist[farthest]

    for v in range(n):
        if visited[v]:
            continue

        stack = [v]
        component = []
        visited[v] = True

        while stack:
            cur = stack.pop()
            component.append(cur)

            for to in g[cur]:
                if not visited[to]:
                    visited[to] = True
                    stack.append(to)

        start = component[0]
        endpoint, _ = bfs(start)
        _, diam = bfs(endpoint)

        root = find(start)
        diameter[root] = diam

    def merge(a, b):
        ra = find(a)
        rb = find(b)

        if ra == rb:
            return

        d1 = diameter[ra]
        d2 = diameter[rb]

        new_d = max(
            d1,
            d2,
            (d1 + 1) // 2 + (d2 + 1) // 2 + 1
        )

        if size[ra] < size[rb]:
            ra, rb = rb, ra

        parent[rb] = ra
        size[ra] += size[rb]
        diameter[ra] = new_d

    ans = []

    for _ in range(q):
        query = list(map(int, input().split()))

        if query[0] == 1:
            x = query[1] - 1
            ans.append(str(diameter[find(x)]))
        else:
            x = query[1] - 1
            y = query[2] - 1
            merge(x, y)

    sys.stdout.write("\n".join(ans))

solve()
```

The graph is built once at the beginning because the actual endpoints chosen during merge operations never matter. Only the resulting diameter matters.

The first DSU construction groups vertices according to the initial forest. After that, every connected component's diameter is computed exactly once using the classic double-BFS technique.

The diameter array is indexed by DSU roots. Whenever two components merge, the new diameter is computed directly from the old diameters using the radius formula. No traversal of the graph is needed.

A common mistake is using `d // 2` instead of `(d + 1) // 2`. The radius of a diameter-5 tree is 3, not 2. The ceiling division is essential.

Another easy mistake is updating the diameter before checking whether the two vertices already belong to the same DSU set. The merge formula is only valid for distinct components.

## Worked Examples

### Example 1

Input:

```
6 0 6
2 1 2
2 3 4
2 5 6
2 3 2
2 5 3
1 1
```

Initial state:

| Component | Diameter |
| --- | --- |
| {1} | 0 |
| {2} | 0 |
| {3} | 0 |
| {4} | 0 |
| {5} | 0 |
| {6} | 0 |

Processing queries:

| Query | Components Merged | New Diameter |
| --- | --- | --- |
| 2 1 2 | {1} + {2} | 1 |
| 2 3 4 | {3} + {4} | 1 |
| 2 5 6 | {5} + {6} | 1 |
| 2 3 2 | diameter 1 + diameter 1 | 3 |
| 2 5 3 | diameter 1 + diameter 3 | 4 |
| 1 1 | answer | 4 |

Output:

```
4
```

This example shows repeated merging of small trees. The diameter update formula alone is sufficient, no graph traversal is needed after initialization.

### Example 2

Input:

```
5 4 3
1 2
2 3
3 4
4 5
1 1
2 2 5
1 3
```

Initial component:

| Component | Diameter |
| --- | --- |
| {1,2,3,4,5} | 4 |

Processing:

| Query | Result |
| --- | --- |
| 1 1 | 4 |
| 2 2 5 | same component |
| 1 3 | 4 |

Output:

```
4
4
```

This demonstrates that merge requests inside the same component must be ignored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) α(n)) | Initial graph processing is linear, DSU operations are amortized inverse Ackermann |
| Space | O(n) | Graph, DSU arrays, and auxiliary storage |

The forest contains at most $3 \cdot 10^5$ vertices and edges. Linear preprocessing plus near-constant-time DSU operations easily fits within the limits.

## Test Cases

```python
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m, q = map(int, input().split())

    g = [[] for _ in range(n)]

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def unite(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        g[b].append(a)
        unite(a, b)

    diameter = [0] * n
    vis = [False] * n

    def bfs(s):
        dist = [-1] * n
        dist[s] = 0
        dq = deque([s])
        far = s

        while dq:
            v = dq.popleft()
            if dist[v] > dist[far]:
                far = v

            for to in g[v]:
                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    dq.append(to)

        return far, dist[far]

    for i in range(n):
        if vis[i]:
            continue

        stack = [i]
        vis[i] = True
        comp = []

        while stack:
            v = stack.pop()
            comp.append(v)

            for to in g[v]:
                if not vis[to]:
                    vis[to] = True
                    stack.append(to)

        a, _ = bfs(comp[0])
        _, d = bfs(a)

        diameter[find(comp[0])] = d

    def merge(a, b):
        ra = find(a)
        rb = find(b)

        if ra == rb:
            return

        nd = max(
            diameter[ra],
            diameter[rb],
            (diameter[ra] + 1) // 2 + (diameter[rb] + 1) // 2 + 1
        )

        if size[ra] < size[rb]:
            ra, rb = rb, ra

        parent[rb] = ra
        size[ra] += size[rb]
        diameter[ra] = nd

    out = []

    for _ in range(q):
        qry = list(map(int, input().split()))

        if qry[0] == 1:
            out.append(str(diameter[find(qry[1] - 1)]))
        else:
            merge(qry[1] - 1, qry[2] - 1)

    return "\n".join(out)

# provided sample
assert run(
"""6 0 6
2 1 2
2 3 4
2 5 6
2 3 2
2 5 3
1 1
"""
) == "4"

# single isolated node
assert run(
"""1 0 1
1 1
"""
) == "0"

# merge two isolated vertices
assert run(
"""2 0 2
2 1 2
1 1
"""
) == "1"

# same component merge should do nothing
assert run(
"""3 2 2
1 2
2 3
2 1 3
1 2
"""
) == "2"

# chain of length four
assert run(
"""5 4 1
1 2
2 3
3 4
4 5
1 3
"""
) == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single isolated vertex | 0 | Minimum graph size |
| Two isolated vertices merged | 1 | Diameter growth from 0 |
| Merge inside same component | 2 | Correct DSU handling |
| Path of length 4 | 4 | Initial diameter computation |
| Sample case | 4 | Full workflow |

## Edge Cases

Consider two isolated vertices:

```
2 0 2
2 1 2
1 1
```

Both components start with diameter 0. The merge formula gives:

$$\max(0,0,0+0+1)=1$$

The query correctly returns:

```
1
```

Consider a merge inside the same component:

```
3 2 2
1 2
2 3
2 1 3
1 2
```

The DSU representatives are equal, so the merge operation exits immediately. The stored diameter remains 2, and the answer is:

```
2
```

Consider two paths of length 4 being merged. Each tree has diameter 4 and radius 2.

The formula gives:

$$\max(4,4,2+2+1)=5$$

Connecting centers achieves diameter 5. Connecting endpoints would create diameter 9. The algorithm always stores the optimal value because it relies on the radius-based formula rather than any particular edge choice.

Finally, isolated vertices are handled naturally. Their diameter is 0, their radius is also 0, and all formulas remain valid without special cases.
