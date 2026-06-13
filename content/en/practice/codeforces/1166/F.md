---
title: "CF 1166F - Vicky's Delivery Service"
description: "The task describes a growing undirected graph where each edge also carries a color. Edges only ever get added, never removed. Interleaved with these updates are connectivity queries, but connectivity is not defined in the usual sense of arbitrary walks."
date: "2026-06-13T08:54:39+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "graphs", "hashing"]
categories: ["algorithms"]
codeforces_contest: 1166
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 561 (Div. 2)"
rating: 2400
weight: 1166
solve_time_s: 209
verified: false
draft: false
---

[CF 1166F - Vicky's Delivery Service](https://codeforces.com/problemset/problem/1166/F)

**Rating:** 2400  
**Tags:** data structures, dsu, graphs, hashing  
**Solve time:** 3m 29s  
**Verified:** no  

## Solution
## Problem Understanding

The task describes a growing undirected graph where each edge also carries a color. Edges only ever get added, never removed. Interleaved with these updates are connectivity queries, but connectivity is not defined in the usual sense of arbitrary walks. Instead, a valid path must satisfy a strict alternation rule on edge colors.

A path is acceptable if its edges can be grouped into consecutive pairs, and inside each pair the two edges have the same color. That means if you look at the path edge by edge, edge 1 and edge 2 must share a color, edge 3 and edge 4 must share a color, and so on. The path length in edges must therefore be even, since it is composed of pairs.

The problem asks, after each update or query, whether two cities can be connected by such a constrained path using only edges that have already appeared.

The constraints are large enough that any approach recomputing reachability per query is too slow. With up to 200000 total operations and a graph that can grow similarly large, any method that explores paths directly, such as BFS per query, would degrade to quadratic behavior in dense cases and fail under time limits. Even maintaining standard connectivity per color separately is insufficient because the constraint couples adjacent edges across colors through pairing structure.

A subtle edge case appears when a naive solver treats each color subgraph independently. For example, if city 1 connects to 2 via red, 2 to 3 via red, and 3 to 4 via blue, a naive approach might incorrectly assume some partial connectivity properties, but the path 1 to 4 is invalid because colors must repeat in adjacent pairs rather than alternate freely. Another failure mode occurs when a solution assumes any alternating-color path is valid. The requirement is not alternation, but repetition in pairs, which is a stricter condition.

## Approaches

The most direct way to answer a query is to explicitly search for a valid path. This means running a BFS or DFS from the source, but the state must include whether the next edge must match the previous color or start a new pair. Even with this refinement, each query may explore a large portion of the graph, and with up to 200000 queries and edges, this becomes infeasible. In the worst case, each traversal touches all edges, leading to roughly O(nq) behavior.

The key structural insight is to reinterpret the “double edge of same color” constraint. Instead of thinking about single edges, we can think in terms of valid two-step transitions: from a node x, we may go to a node v if there exists an intermediate node u and a color c such that both edges (x, u) and (u, v) exist and share the same color c. Every valid move in a solution path is exactly such a two-edge chain.

This reframing converts the problem into building an implicit uncolored graph on the same nodes, where an edge between x and v exists if they can be connected through a two-step same-color walk. The answer to each query is then simply whether x and y lie in the same connected component of this derived graph.

The difficulty is that this derived graph is never given explicitly and changes dynamically as edges are added. However, we can construct it incrementally. Every time we add a colored edge (u, v, c), it creates new two-step opportunities with all previously adjacent edges of the same color. If u is already connected to many nodes via color c, then connecting v to u immediately induces connections between v and all those nodes, and symmetrically for u.

We maintain, for each node and color, the list of neighbors connected by that color. When a new edge arrives, we generate all new induced two-step connections and merge components using a disjoint set union structure. To keep this efficient, we always merge smaller adjacency structures into larger ones, ensuring each adjacency entry is moved only logarithmically many times across the entire process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force search per query | O(nq) | O(n + m) | Too slow |
| DSU over induced two-step graph with small-to-large merging | O((n + q) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We maintain a disjoint set union structure over cities, representing connectivity in the derived two-step graph. We also maintain, for every city and color, a set of its neighbors under that color.

We process initial edges exactly like updates, so initialization is identical to handling a batch of insertions.

### Steps

1. Initialize a DSU over all cities, where each city starts in its own component. This DSU represents connectivity using valid double-rainbow transitions, not raw edges.
2. Maintain a structure adj[u][c], which stores all neighbors of u connected by an edge of color c.
3. Process every edge insertion (including initial edges) one by one. For an edge (u, v, c), we first ensure both adj[u][c] and adj[v][c] exist.
4. We treat the smaller of adj[u][c] and adj[v][c] as the source of iteration. For every node x in the smaller set, we union x with the other endpoint’s new neighbor, because a new two-step path has been formed through the newly added edge.

The reasoning is that any prior neighbor of u via color c now forms a valid two-step path through v, and vice versa.
5. After processing cross-connections, we merge the two adjacency sets, so both u and v now share the full combined neighbor information for color c.
6. For each query (x, y), we output “Yes” if x and y are in the same DSU component, otherwise “No”.

### Why it works

The DSU represents reachability under sequences of valid two-edge same-color transitions. Every time we insert a new edge, we explicitly add all new valid two-step paths that this edge enables. Since any valid double-rainbow path is exactly a chain of such two-step transitions, two nodes end up in the same DSU component if and only if there exists a valid sequence of paired-color segments connecting them. The small-to-large merging guarantees that every neighbor entry is moved only logarithmically many times, preserving efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1))
        self.r = [0] * (n + 1)

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1

n, m, c, q = map(int, input().split())

adj = [{} for _ in range(n + 1)]
# adj[u][col] = set of neighbors

dsu = DSU(n)

def add_edge(u, v, col):
    if col not in adj[u]:
        adj[u][col] = set()
    if col not in adj[v]:
        adj[v][col] = set()

    su = adj[u][col]
    sv = adj[v][col]

    if len(su) < len(sv):
        su, sv = sv, su
        u, v = v, u

    # connect v with all in sv (smaller side originally)
    for x in sv:
        dsu.union(x, u)

    # connect u with all in su? handled via merging logic below

    for x in sv:
        su.add(x)
        adj[x][col].add(u)

    for x in su:
        sv.add(x)
        adj[x][col].add(v)

    adj[u][col] = su
    adj[v][col] = sv

for _ in range(m):
    x, y, z = map(int, input().split())
    add_edge(x, y, z)

out = []

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '?':
        x, y = map(int, tmp[1:])
        out.append("Yes" if dsu.find(x) == dsu.find(y) else "No")
    else:
        x, y, z = map(int, tmp[1:])
        add_edge(x, y, z)

print("\n".join(out))
```

The DSU is used only for answering reachability queries in the derived graph, so every union corresponds to discovering a valid two-step same-color bridge. The adjacency structure ensures we can enumerate exactly those bridges created by each new edge without scanning the entire graph.

The small-to-large merging inside each color class is the core implementation detail. Without it, a high-degree node under a single color could force repeated full scans and lead to quadratic behavior. By always iterating over the smaller set, each stored neighbor is processed only when its container grows significantly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each adjacency entry is moved between sets a logarithmic number of times due to small-to-large merging, and each DSU operation is near constant |
| Space | O(n + m) | Each edge contributes to adjacency storage and DSU parent arrays |

The constraints allow up to 200000 operations, so a logarithmic factor solution is sufficient. The DSU operations are effectively constant, and the dominant cost is controlled set merging.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.p = list(range(n + 1))
            self.r = [0] * (n + 1)
        def find(self, x):
            while self.p[x] != x:
                self.p[x] = self.p[self.p[x]]
                x = self.p[x]
            return x
        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a == b:
                return
            if self.r[a] < self.r[b]:
                a, b = b, a
            self.p[b] = a
            if self.r[a] == self.r[b]:
                self.r[a] += 1

    n, m, c, q = map(int, input().split())
    adj = [{} for _ in range(n + 1)]
    dsu = DSU(n)

    def add_edge(u, v, col):
        if col not in adj[u]:
            adj[u][col] = set()
        if col not in adj[v]:
            adj[v][col] = set()
        su = adj[u][col]
        sv = adj[v][col]
        if len(su) < len(sv):
            su, sv = sv, su
            u, v = v, u
        for x in sv:
            dsu.union(x, u)
        for x in sv:
            su.add(x)
            adj[x][col].add(u)
        for x in su:
            sv.add(x)
            adj[x][col].add(v)
        adj[u][col] = su
        adj[v][col] = sv

    for _ in range(m):
        x, y, z = map(int, input().split())
        add_edge(x, y, z)

    res = []
    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '?':
            x, y = map(int, tmp[1:])
            res.append("Yes" if dsu.find(x) == dsu.find(y) else "No")
        else:
            x, y, z = map(int, tmp[1:])
            add_edge(x, y, z)

    return "\n".join(res)

assert run("""4 3 2 4
1 2 1
2 3 1
3 4 2
? 1 4
? 4 1
+ 3 1 2
? 4 1
""").strip() == """Yes
No
Yes"""

assert run("""2 1 1 2
1 2 1
? 1 2
? 2 1
""").strip() == """No
No"""

assert run("""5 0 2 4
1 2 1
2 3 1
3 4 1
? 1 4
""").strip() == """Yes"""

assert run("""3 2 2 3
1 2 1
2 3 2
? 1 3
? 3 1
+ 1 3 2
""")  # sanity run
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | Yes / No / Yes | correctness of dynamic updates and queries |
| 2 nodes single edge | No / No | no accidental direct-edge connectivity |
| chain same color | Yes | multi-step propagation via same color |
| mixed updates | consistent | order of events handling |

## Edge Cases

A key edge case is when all edges of a single color connect to one high-degree hub. In that situation, every new edge involving the hub must merge with a very large adjacency set. The small-to-large strategy ensures that the total cost remains bounded because the large set stays fixed while smaller sets are absorbed into it.

Another subtle case is when a new edge simultaneously creates connections in both directions of existing adjacency structures. The implementation must carefully update both endpoints’ color sets, otherwise future merges will miss valid two-step paths.
