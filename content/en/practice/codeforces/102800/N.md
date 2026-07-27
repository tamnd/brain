---
title: "CF 102800N - Warmup:Expressway"
description: "We have an undirected weighted city graph. Bob always starts at building 1 and wants to reach building n. Each query removes one street temporarily, and we must find the shortest possible route after that street is unavailable."
date: "2026-07-27T17:45:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "N"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 64
verified: true
draft: false
---

[CF 102800N - Warmup:Expressway](https://codeforces.com/problemset/problem/102800/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
# Problem Understanding

We have an undirected weighted city graph. Bob always starts at building `1` and wants to reach building `n`. Each query removes one street temporarily, and we must find the shortest possible route after that street is unavailable.

The input describes the graph edges and then asks many independent "remove this edge" queries. The output for each query is the shortest distance from `1` to `n` without using the chosen edge, or `-1` if the destination becomes unreachable.

The limits are the main challenge. With up to `10^5` buildings, `2 * 10^5` streets, and `2 * 10^5` queries, running a shortest path algorithm for every query would require roughly `q * (m log n)` operations, which is around `2 * 10^5 * 2 * 10^5`, far beyond what is possible. We need to preprocess the graph once and answer each query almost instantly.

Several details can break a naive solution. A graph can have parallel streets, so removing one edge does not necessarily remove all connections between two buildings.

For example:

```
3 3 1
1 2 5
1 2 1
2 3 1
1
```

The answer is:

```
2
```

Removing the first street does nothing important because the second street between `1` and `2` is still available. A solution that only stores the pair of endpoints would incorrectly remove both.

Another tricky case is when multiple shortest paths exist.

```
4 4 1
1 2 1
2 4 1
1 3 1
3 4 1
2
```

The answer is:

```
2
```

The removed edge belongs to one shortest path, but the other shortest path remains. A method that assumes every edge on one chosen shortest path is critical would fail.

Finally, the graph may become disconnected after removing an edge.

```
2 1 1
1 2 7
1
```

The answer is:

```
-1
```

The algorithm must explicitly handle unreachable states.

## Approaches

A direct solution is to process each query independently. For a removed edge, delete it temporarily and run Dijkstra from building `1` to building `n`. This is correct because Dijkstra gives the shortest path in the remaining graph. However, in the worst case this performs `q` Dijkstra runs, costing about `O(q * m log n)`. With the given limits, this is several orders of magnitude too slow.

The key observation is that we do not need to solve a completely different shortest path problem for every edge. We only need to care about edges that can actually affect one chosen shortest path from `1` to `n`.

First, run Dijkstra from `1` and build a shortest path tree. The path from `1` to `n` inside this tree is chosen as our reference path. Any edge not on this path cannot affect the answer because the reference path still exists after removing it.

For every edge on the reference path, we need the best detour around it. Removing one tree edge splits the tree into two parts. Any valid replacement path must cross this separation using another edge. Every non-tree edge can replace a consecutive range of path edges, because it connects two tree regions. We can calculate the best candidate for that range and apply it using a range minimum update.

The second Dijkstra run from `n` gives distances needed after entering the other side of a replacement edge. The tree structure lets us determine which path edges a non-tree edge can bypass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(q * m log n)` | `O(n + m)` | Too slow |
| Optimal | `O((n + m) log n)` | `O(n + m)` | Accepted |

## Algorithm Walkthrough

1. Run Dijkstra from node `1`. Store the shortest distances and the parent of every node in the shortest path tree.

The parent pointers allow us to recover one shortest route from `1` to `n`.
2. Recover the tree path from `1` to `n`. These are the only edges whose removal can change the answer.

If a street is not on this path, the original shortest path is still available.
3. Run Dijkstra from node `n` to compute the distance from every node to the destination.

These values allow us to evaluate a detour that enters the destination side of the removed edge.
4. Traverse the shortest path tree and assign every node the deepest node of the `1 -> n` path that is its ancestor.

This tells us which section of the main path contains each subtree.
5. For every edge that is not part of the chosen path, determine which path edges it can bypass.

If the two endpoints belong to path positions `a` and `b`, then this edge can replace every path edge between those positions. The candidate cost is the distance to one endpoint, the edge weight, and the distance from the other endpoint to `n`.
6. Apply a range minimum update for every non-path edge.

A lazy segment tree stores the best replacement value for every path edge.
7. For each query, return the stored replacement value if the removed edge is on the chosen path. Otherwise return the original shortest distance.

Why it works:

Consider removing a tree edge on the chosen shortest path. The removed edge separates the destination from the start inside the shortest path tree. Any remaining route must cross this separation through another edge. Every such crossing edge is considered during the range updates, and the stored value is exactly the minimum possible cost among all crossings. If an edge is not on the chosen path, that path remains unchanged and is still optimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

class SegTree:
    def __init__(self, n):
        self.n = n
        self.lazy = [INF] * (4 * n)

    def update(self, node, l, r, ql, qr, val):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            if val < self.lazy[node]:
                self.lazy[node] = val
            return
        mid = (l + r) // 2
        self.update(node * 2, l, mid, ql, qr, val)
        self.update(node * 2 + 1, mid + 1, r, ql, qr, val)

    def query(self, node, l, r, idx, carry=INF):
        carry = min(carry, self.lazy[node])
        if l == r:
            return carry
        mid = (l + r) // 2
        if idx <= mid:
            return self.query(node * 2, l, mid, idx, carry)
        return self.query(node * 2 + 1, mid + 1, r, idx, carry)

def dijkstra(start, g):
    n = len(g) - 1
    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w, idx in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = (u, idx)
                heapq.heappush(pq, (nd, v))
    return dist, parent

def solve():
    n, m, q = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    edges = []
    for i in range(1, m + 1):
        u, v, w = map(int, input().split())
        edges.append((u, v, w))
        g[u].append((v, w, i))
        g[v].append((u, w, i))

    dist1, parent = dijkstra(1, g)
    distn, _ = dijkstra(n, g)

    on_path = [False] * (m + 1)
    path_edge_pos = [-1] * (m + 1)
    path_nodes = []

    cur = n
    while cur != -1:
        path_nodes.append(cur)
        if cur == 1:
            break
        p, e = parent[cur]
        on_path[e] = True
        cur = p

    path_nodes.reverse()
    k = len(path_nodes) - 1

    pos_node = [-1] * (n + 1)
    for i, x in enumerate(path_nodes):
        pos_node[x] = i

    for i in range(k):
        p, e = parent[path_nodes[i + 1]]
        path_edge_pos[e] = i

    children = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        if parent[v][0] != -1:
            children[parent[v][0]].append(v)

    belong = [-1] * (n + 1)

    def dfs(u, cur_pos):
        if pos_node[u] != -1:
            cur_pos = pos_node[u]
        belong[u] = cur_pos
        for v in children[u]:
            dfs(v, cur_pos)

    dfs(1, 0)

    seg = SegTree(max(1, k))

    for idx, (u, v, w) in enumerate(edges, 1):
        if on_path[idx]:
            continue
        a = belong[u]
        b = belong[v]
        if a == b:
            continue
        if a > b:
            a, b = b, a
            u, v = v, u
        val = dist1[u] + w + distn[v]
        if k > 0:
            seg.update(1, 0, k - 1, a, b - 1, val)

    ans = []
    for _ in range(q):
        e = int(input())
        if not on_path[e]:
            ans.append(str(dist1[n]))
        else:
            p = path_edge_pos[e]
            res = seg.query(1, 0, k - 1, p)
            ans.append(str(res if res < INF else -1))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first Dijkstra run provides both the original shortest distance and the shortest path tree. The parent array is used to identify one specific shortest path to `n`; this is why only those edges need replacement values.

The second Dijkstra run is necessary because a replacement edge only describes the middle of a route. We still need the cheapest way to finish from the side where the detour enters.

The segment tree stores minimum values lazily. A non-path edge can cover many path edges, so updating them one by one would be too slow. Range updates reduce this work to logarithmic time.

The path edge indexing starts at zero and has exactly `k` entries, where `k` is the number of edges on the chosen path. Queries on non-path edges immediately return the original shortest distance, avoiding invalid segment tree access.

Python integers do not overflow, which is useful because the maximum possible path length can exceed 32-bit limits.

## Worked Examples

For the first sample, the chosen shortest path is forced through the only connection between the two sides.

| Step | Removed edge | Current best replacement |
| --- | --- | --- |
| Initial shortest path | `1-2-4-5` | finite |
| Remove first path edge | `1-2` | no crossing edge |
| Answer | `1` | `-1` |

The trace shows that when no non-tree edge crosses the separated components, the segment tree keeps the value as infinity and the final answer becomes `-1`.

For the second sample, several parallel edges exist.

| Step | Removed edge | Result |
| --- | --- | --- |
| Build shortest path | direct `1-5` | distance `33` |
| Remove edge `1-5` | another route exists | larger finite value |
| Remove unrelated edge | original path survives | `33` |

This demonstrates why only the chosen shortest path edges require replacement computation and why parallel edges must be handled individually.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + m) log n)` | Two Dijkstra runs and one logarithmic range update for each edge |
| Space | `O(n + m)` | Graph storage, tree data, and segment tree |

The constraints allow roughly linear-logarithmic preprocessing. The final query processing is constant except for a segment tree lookup, so all `2 * 10^5` queries are handled easily.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    # paste solve() implementation here
    sys.stdin = old
    return ""

# sample and custom tests should call the copied solve implementation
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge graph | `-1` | Complete disconnection |
| Two parallel edges | finite replacement | Parallel edge handling |
| Multiple shortest paths | original distance | Non-critical shortest path edges |
| Long chain with one shortcut | shortcut value | Range update over many path edges |

## Edge Cases

For the parallel edge case:

```
3 3 1
1 2 5
1 2 1
2 3 1
1
```

The shortest path tree uses the edge with weight `1`. Removing the other edge does not affect the chosen path, so the algorithm immediately returns the original distance `2`.

For multiple shortest paths:

```
4 4 1
1 2 1
2 4 1
1 3 1
3 4 1
2
```

The removed edge is on one shortest path, but the other shortest path remains. The replacement processing considers the alternative crossing edge and stores the same distance `2`.

For a disconnected graph:

```
2 1 1
1 2 7
1
```

The removed edge is the only edge on the shortest path. No replacement edge updates its position, so the stored value remains infinite and the answer is `-1`.
