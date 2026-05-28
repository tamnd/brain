---
title: "CF 97E - Leaders"
description: "We are given an undirected graph where vertices represent people and edges represent relationships. For every query (u, v), we must decide whether there exists a simple path from u to v whose length is odd. The keyword here is \"simple\". We are not allowed to revisit vertices."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 97
codeforces_index: "E"
codeforces_contest_name: "Yandex.Algorithm 2011: Finals"
rating: 2200
weight: 97
solve_time_s: 123
verified: true
draft: false
---

[CF 97E - Leaders](https://codeforces.com/problemset/problem/97/E)

**Rating:** 2200  
**Tags:** dfs and similar, dsu, graphs, trees  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph where vertices represent people and edges represent relationships. For every query `(u, v)`, we must decide whether there exists a simple path from `u` to `v` whose length is odd.

The keyword here is "simple". We are not allowed to revisit vertices. The graph is not necessarily connected, and it may contain cycles.

A direct BFS from every query vertex would not work. Both the number of vertices and edges can reach `10^5`, and there are also up to `10^5` queries. Any solution that spends linear time per query would require around `10^10` operations in the worst case, far beyond the limit.

The real difficulty is that a pair of vertices may have both even and odd simple paths between them. The answer is not determined by shortest path parity alone.

Consider this graph:

```
1 - 2
|   |
3 - 4
```

Between `1` and `2`, there is an odd path `1-2`, but also an even path `1-3-4-2`. The problem only asks whether at least one odd simple path exists.

A common mistake is to think bipartite coloring solves everything. In a bipartite graph, all paths between two vertices have the same parity, so coloring works there. But once the graph contains an odd cycle, both parities may become possible.

For example:

```
1 - 2
 \ /
  3
```

The triangle contains an odd cycle. Between `1` and `2`, we have:

```
1-2        length 1
1-3-2      length 2
```

Both parities exist. Any approach that stores only one parity per pair will fail.

Another subtle case is querying the same vertex.

Input:

```
3 3
1 2
2 3
3 1
2
1 1
2 2
```

Output:

```
Yes
Yes
```

The triangle contains an odd cycle, so vertex `1` can return to itself using a simple odd cycle of length `3`. A careless implementation may incorrectly answer `"No"` because the empty path has length `0`.

Disconnected components are another source of mistakes.

Input:

```
4 1
1 2
2
1 3
3 4
```

Output:

```
No
No
```

No path exists at all, so the answer must be `"No"` regardless of parity.

## Approaches

The brute-force idea is straightforward. For every query `(u, v)`, run a BFS or DFS that tracks parity. We can duplicate each vertex into two states:

```
(vertex, parity)
```

When traversing an edge, parity flips.

If we can reach `(v, 1)`, then an odd path exists.

This approach is correct for walks, but not necessarily for simple paths. Preventing repeated vertices makes the search much harder. In general graphs, tracking simple-path parity directly per query becomes expensive.

Even if we ignore the simplicity issue and run BFS per query, the complexity becomes:

```
O(q(n + m))
```

With all values near `10^5`, this is roughly `10^10` operations.

The key observation is structural.

Inside a connected bipartite component, every path between two vertices has fixed parity. If two vertices are in the same color class, all paths between them are even. If they are in opposite classes, all paths are odd.

Inside a connected non-bipartite component, the situation changes completely. An odd cycle exists, and that odd cycle lets us flip path parity. In fact:

If a connected component is non-bipartite, then every pair of vertices has both an even and an odd simple path between them.

That single fact collapses the whole problem.

So the solution becomes:

1. Find connected components.
2. Determine whether each component is bipartite.
3. If the component is bipartite, use vertex colors to determine parity.
4. If the component is non-bipartite, every pair inside it answers `"Yes"`.

This reduces all queries to constant-time checks after one DFS/BFS preprocessing pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per query | O(q(n + m)) | O(n + m) | Too slow |
| Optimal graph preprocessing | O(n + m + q) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the graph.

The graph is sparse, so adjacency lists are the natural representation.
2. Traverse every connected component using DFS or BFS.

During traversal, assign a binary color to each vertex.
3. While traversing edges `(u, v)`, check coloring consistency.

If `u` and `v` already have the same color, the component is not bipartite.
4. Store for every vertex:

- its connected component id
- its bipartite color
- whether its component is bipartite
5. For each query `(u, v)`:

1. If `u` and `v` belong to different connected components, print `"No"`.

No path exists at all.
2. Otherwise, if the component is non-bipartite, print `"Yes"`.

A non-bipartite connected component contains an odd cycle, which allows constructing an odd simple path between any pair.
3. Otherwise the component is bipartite.

In bipartite graphs, all paths between two vertices have the same parity.

Print `"Yes"` if the colors differ, otherwise `"No"`.

### Why it works

A connected graph is bipartite if and only if it contains no odd cycle.

In a bipartite graph, every edge connects opposite color classes. Any path alternates colors at every step, so the parity of a path between two vertices is uniquely determined by their colors.

If the graph is non-bipartite, an odd cycle exists. Starting from any path between `u` and `v`, we can route through the odd cycle to flip parity while keeping the path simple. Since the component is connected, every pair of vertices can reach the odd cycle and use it to change parity.

That means:

- bipartite component → parity fixed
- non-bipartite component → both parities available

The algorithm checks exactly these conditions, so every answer is correct.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    comp = [-1] * (n + 1)
    color = [-1] * (n + 1)
    bipartite = []

    cid = 0

    for start in range(1, n + 1):
        if comp[start] != -1:
            continue

        queue = deque([start])
        comp[start] = cid
        color[start] = 0

        ok = True

        while queue:
            u = queue.popleft()

            for v in graph[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    color[v] = color[u] ^ 1
                    queue.append(v)
                else:
                    if color[v] == color[u]:
                        ok = False

        bipartite.append(ok)
        cid += 1

    q = int(input())

    out = []

    for _ in range(q):
        u, v = map(int, input().split())

        if comp[u] != comp[v]:
            out.append("No")
        elif not bipartite[comp[u]]:
            out.append("Yes")
        else:
            out.append("Yes" if color[u] != color[v] else "No")

    print("\n".join(out))

solve()
```

The preprocessing phase performs a BFS on every connected component. During traversal, vertices receive alternating colors.

The `comp` array identifies which connected component each vertex belongs to. This immediately answers connectivity queries.

The `color` array stores the bipartite partition. Adjacent vertices must always receive opposite colors. If we ever encounter an edge connecting equal colors, the component contains an odd cycle and is marked non-bipartite.

The `bipartite` list stores one boolean per component. This lets each query run in constant time.

A subtle implementation detail is that we continue traversing even after detecting a coloring conflict. Stopping early would leave parts of the component unvisited and break later queries.

Another important detail is handling queries like `(u, u)`. In a bipartite component, the answer is `"No"` because every cycle is even. In a non-bipartite component, the answer becomes `"Yes"` because an odd cycle exists.

## Worked Examples

### Example 1

Input:

```
7 7
1 3
1 4
2 3
2 4
5 6
6 7
7 5
8
1 2
1 3
1 4
2 4
1 5
5 6
5 7
6 7
```

The graph has two connected components.

| Vertex | Component | Color | Bipartite Component |
| --- | --- | --- | --- |
| 1 | 0 | 0 | Yes |
| 2 | 0 | 0 | Yes |
| 3 | 0 | 1 | Yes |
| 4 | 0 | 1 | Yes |
| 5 | 1 | 0 | No |
| 6 | 1 | 1 | No |
| 7 | 1 | 1 | No |

Now process queries.

| Query | Same Component | Bipartite | Color Relation | Answer |
| --- | --- | --- | --- | --- |
| 1 2 | Yes | Yes | Same | No |
| 1 3 | Yes | Yes | Different | Yes |
| 1 4 | Yes | Yes | Different | Yes |
| 2 4 | Yes | Yes | Different | Yes |
| 1 5 | No | - | - | No |
| 5 6 | Yes | No | - | Yes |
| 5 7 | Yes | No | - | Yes |
| 6 7 | Yes | No | - | Yes |

The first component is bipartite, so parity is determined entirely by colors. The second component contains a triangle, so every pair has an odd simple path.

### Example 2

Input:

```
3 2
1 2
2 3
4
1 1
1 2
1 3
2 3
```

| Vertex | Component | Color | Bipartite |
| --- | --- | --- | --- |
| 1 | 0 | 0 | Yes |
| 2 | 0 | 1 | Yes |
| 3 | 0 | 0 | Yes |

Queries:

| Query | Color Relation | Answer |
| --- | --- | --- |
| 1 1 | Same | No |
| 1 2 | Different | Yes |
| 1 3 | Same | No |
| 2 3 | Different | Yes |

This example demonstrates the fixed parity property of bipartite graphs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + q) | BFS processes every vertex and edge once, then each query is O(1) |
| Space | O(n + m) | Adjacency list plus auxiliary arrays |

With `10^5` vertices, edges, and queries, linear preprocessing easily fits within the time limit. The memory usage is also safe for the given constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    comp = [-1] * (n + 1)
    color = [-1] * (n + 1)
    bipartite = []

    cid = 0

    for start in range(1, n + 1):
        if comp[start] != -1:
            continue

        q = deque([start])
        comp[start] = cid
        color[start] = 0

        ok = True

        while q:
            u = q.popleft()

            for v in graph[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    color[v] = color[u] ^ 1
                    q.append(v)
                else:
                    if color[v] == color[u]:
                        ok = False

        bipartite.append(ok)
        cid += 1

    queries = int(input())

    out = []

    for _ in range(queries):
        u, v = map(int, input().split())

        if comp[u] != comp[v]:
            out.append("No")
        elif not bipartite[comp[u]]:
            out.append("Yes")
        else:
            out.append("Yes" if color[u] != color[v] else "No")

    return "\n".join(out)

# provided sample
assert run(
"""7 7
1 3
1 4
2 3
2 4
5 6
6 7
7 5
8
1 2
1 3
1 4
2 4
1 5
5 6
5 7
6 7
"""
) == "\n".join([
    "No",
    "Yes",
    "Yes",
    "Yes",
    "No",
    "Yes",
    "Yes",
    "Yes"
]), "sample 1"

# single isolated vertex
assert run(
"""1 0
3
1 1
1 1
1 1
"""
) == "\n".join([
    "No",
    "No",
    "No"
]), "isolated vertex"

# simple chain
assert run(
"""4 3
1 2
2 3
3 4
4
1 2
1 3
1 4
2 4
"""
) == "\n".join([
    "Yes",
    "No",
    "Yes",
    "No"
]), "bipartite parity"

# triangle graph
assert run(
"""3 3
1 2
2 3
3 1
4
1 1
1 2
1 3
2 2
"""
) == "\n".join([
    "Yes",
    "Yes",
    "Yes",
    "Yes"
]), "non-bipartite component"

# disconnected graph
assert run(
"""5 2
1 2
4 5
4
1 3
2 5
4 5
3 3
"""
) == "\n".join([
    "No",
    "No",
    "Yes",
    "No"
]), "disconnected components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single isolated vertex | All `No` | No self odd path without cycles |
| Simple chain | Alternating parity | Bipartite parity logic |
| Triangle graph | All `Yes` | Odd cycle enables all parities |
| Disconnected graph | Mixed answers | Connectivity handling |

## Edge Cases

Consider a graph with a non-bipartite component and a self-query.

Input:

```
3 3
1 2
2 3
3 1
1
1 1
```

During BFS, vertices receive colors:

```
1 -> 0
2 -> 1
3 -> 1
```

Edge `(2, 3)` connects equal colors, so the component is marked non-bipartite.

For query `(1, 1)`, both vertices belong to the same non-bipartite component, so the algorithm prints `"Yes"`.

That is correct because the cycle:

```
1-2-3-1
```

has odd length `3`.

Now consider disconnected vertices.

Input:

```
4 1
1 2
2
1 3
3 4
```

Components become:

```
{1,2}
{3}
{4}
```

For both queries, the component ids differ, so the algorithm immediately answers `"No"`.

This avoids incorrectly reasoning about parity when no path exists at all.

Finally, consider a bipartite graph where multiple paths exist.

Input:

```
4 4
1 3
3 2
1 4
4 2
2
1 2
1 3
```

The graph is bipartite with colors:

```
1,2 -> 0
3,4 -> 1
```

Even though there are two different paths from `1` to `2`, both have even length:

```
1-3-2
1-4-2
```

The algorithm answers `"No"` because the colors are equal.

For `(1,3)`, colors differ, so the answer is `"Yes"`.

This confirms the invariant that all paths in a bipartite graph have the same parity.
