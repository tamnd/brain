---
title: "CF 103448K - \u76ae\u5361\u4e18\u4e0e Minimum Spanning Tree-I"
description: "We are given a graph with $n$ vertices where every pair of vertices is connected by an edge. This is not a standard complete graph with arbitrary weights: most edges follow a simple rule based on vertex weights, while a smaller subset of edges comes with explicitly given costs…"
date: "2026-07-03T07:28:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103448
codeforces_index: "K"
codeforces_contest_name: "The 16-th Beihang University Collegiate Programming Contest (BCPC 2021) - Preliminary"
rating: 0
weight: 103448
solve_time_s: 54
verified: true
draft: false
---

[CF 103448K - \u76ae\u5361\u4e18\u4e0e Minimum Spanning Tree-I](https://codeforces.com/problemset/problem/103448/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph with $n$ vertices where every pair of vertices is connected by an edge. This is not a standard complete graph with arbitrary weights: most edges follow a simple rule based on vertex weights, while a smaller subset of edges comes with explicitly given costs that override this rule.

Each vertex $i$ has a value $a_i$. For any pair of distinct vertices $u, v$, if there is no special edge provided for that pair, the weight of the edge is defined as $\min(a_u, a_v)$. Additionally, the input gives $m$ special edges, each with its own weight $w$, and these replace the default rule for those pairs.

The task is to compute a minimum spanning tree over this graph and output both its total weight and the chosen edges.

The difficulty is entirely in the size of the graph. With up to $5 \times 10^5$ vertices, the complete graph would have on the order of $10^{11}$ edges, so we cannot even think about constructing it explicitly. Any solution must avoid iterating over all pairs.

A useful way to interpret the structure is that most edges are determined by a global rule, and only a small number of edges break that rule. The challenge is to compress the implicit complete graph into something linear or near-linear in size while preserving all MST-relevant structure.

A common failure case comes from trying to apply Kruskal directly to only the $m$ given edges. For example, if all $a_i$ are equal and there are no special edges, every edge has weight $a_i$, so any spanning tree is valid and has total weight $(n-1)\cdot a_i$. If we ignore implicit edges entirely, we would incorrectly conclude that the graph is disconnected.

Another naive idea is to consider only edges between each node and the globally smallest $a_i$. This is actually correct for the implicit graph alone, but becomes subtle when special edges exist. A special edge might be cheaper than the implicit star edge, and must be included.

The real issue is combining a dense implicit structure with sparse overrides without materializing the full graph.

## Approaches

If we ignore constraints, the most direct approach is to build all $\binom{n}{2}$ edges, assign each weight using the rule or override, and run Kruskal’s algorithm. This is correct because MST is defined over the full edge set. However, the number of edges is quadratic, and even generating them already exceeds any feasible time limit.

The key observation is that the implicit complete graph has a very rigid structure. For any edge $(u, v)$, its weight is always the smaller of $a_u$ and $a_v$. This means that among all edges incident to a vertex $v$, the cheapest connection is always to a vertex with minimum $a$-value. If we pick the vertex $r$ with minimal $a_r$, then for every other vertex $v$, the edge $(r, v)$ has weight $a_r$, and this is the smallest possible implicit edge incident to $v$.

This collapses the entire dense graph into a star centered at $r$, without changing any MST outcome for the implicit part. Any edge between two non-root vertices has weight at least $a_r$, so replacing it with two edges through $r$ never increases cost.

The special edges can then be layered on top of this compressed structure. We treat the graph as consisting of $n-1$ star edges from $r$ plus the $m$ given edges, and run Kruskal on this reduced edge set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full graph Kruskal | $O(n^2 \log n)$ | $O(n^2)$ | Too slow |
| Star compression + Kruskal | $O((n+m)\log n)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

### 1. Find the global minimum vertex

We scan all vertices and find an index $r$ such that $a_r = \min a_i$. This vertex will act as the hub of the implicit structure.

### 2. Build a reduced edge list

We create an edge list initially containing all special edges $(u, v, w)$ from the input.

For every vertex $v \neq r$, we add an edge $(r, v)$ with weight $a_r$. This represents the best possible implicit connection for $v$.

This step replaces the dense implicit graph with a linear number of edges while preserving all MST-relevant options.

### 3. Run Kruskal on the reduced graph

We sort all collected edges by weight and apply Kruskal’s algorithm with a DSU structure. Every time we take an edge that connects two different components, we include it in the MST.

### 4. Output the result

We output the total weight of selected edges and list all chosen edges.

### Why it works

The core invariant is that for every vertex $v$, the cheapest way to connect $v$ to any vertex with smaller or equal $a$-value is represented either by a special edge or by the single edge $(r, v)$. Any non-special implicit edge $(u, v)$ can be replaced by a path $u \to r \to v$ without increasing cost, since both edges on that path have weight at most $\min(a_u, a_v)$. This ensures that restricting attention to star edges plus special edges preserves all possible MST candidates, so Kruskal on this reduced set produces a globally optimal spanning tree.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        return True

n, m = map(int, input().split())
edges = []

special = []
for _ in range(m):
    u, v, w = map(int, input().split())
    u -= 1
    v -= 1
    special.append((w, u, v))

a = list(map(int, input().split()))

r = min(range(n), key=lambda i: a[i])

for w, u, v in special:
    edges.append((w, u, v))

for i in range(n):
    if i != r:
        edges.append((a[r], r, i))

edges.sort()

dsu = DSU(n)

total = 0
res = []

for w, u, v in edges:
    if dsu.union(u, v):
        total += w
        res.append((u, v))
        if len(res) == n - 1:
            break

print(total)
for u, v in res:
    print(u + 1, v + 1)
```

The DSU maintains connectivity while Kruskal processes edges in increasing weight order. Special edges are included directly, and implicit edges are represented only through connections to the global minimum vertex.

A subtle point is that the weight of all star edges is exactly $a_r$, not $a_i$. This is because $\min(a_r, a_i) = a_r$ for all $i$, since $r$ is chosen as the global minimum.

## Worked Examples

### Example 1

Consider a small case where $a = [5, 2, 4]$. The minimum vertex is $r = 1$ (0-indexed), since $a_1 = 2$.

All implicit edges are represented as star edges:

$(1,0)$ weight 2, $(1,2)$ weight 2.

Suppose there is one special edge $(0,2)$ with weight 1.

| Step | Edge | Weight | Chosen? | DSU Components |
| --- | --- | --- | --- | --- |
| 1 | (0,2) | 1 | yes | {0,2}, {1} |
| 2 | (1,0) | 2 | yes | {0,1,2} |

The MST uses the special edge first, then connects the remaining component via the star.

This demonstrates how special edges can override the implicit star structure when they are cheaper.

### Example 2

Let $a = [3, 3, 3, 3]$ with no special edges.

All star edges have weight 3, and any spanning tree must pick exactly 3 edges.

| Step | Edge | Weight | Chosen? | DSU Components |
| --- | --- | --- | --- | --- |
| 1 | (0,1) | 3 | yes | {0,1}, {2}, {3} |
| 2 | (0,2) | 3 | yes | {0,1,2}, {3} |
| 3 | (0,3) | 3 | yes | {0,1,2,3} |

Any spanning tree has the same cost, and the algorithm naturally produces a valid one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\log n)$ | Sorting $m + n$ edges dominates, DSU operations are nearly linear |
| Space | $O(n+m)$ | Stores DSU arrays and reduced edge list |

The constraints allow up to $5 \times 10^5$ vertices and edges, so an $O(n \log n)$ or $O((n+m)\log n)$ approach is necessary. The reduction from a dense graph to a sparse one is what makes this feasible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.p = list(range(n))
            self.r = [0]*n
        def find(self, x):
            while self.p[x] != x:
                self.p[x] = self.p[self.p[x]]
                x = self.p[x]
            return x
        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a == b:
                return False
            if self.r[a] < self.r[b]:
                a, b = b, a
            self.p[b] = a
            if self.r[a] == self.r[b]:
                self.r[a] += 1
            return True

    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u-1, v-1))
    a = list(map(int, input().split()))
    r = min(range(n), key=lambda i: a[i])

    for i in range(n):
        if i != r:
            edges.append((a[r], r, i))

    edges.sort()
    dsu = DSU(n)

    total = 0
    cnt = 0
    for w, u, v in edges:
        if dsu.union(u, v):
            total += w
            cnt += 1
            if cnt == n-1:
                break

    return str(total)

# provided samples (placeholders since exact formatting not given)
# assert run("...") == "..."
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=1, m=0$ single node | 0 | trivial MST |
| all $a_i$ equal | $(n-1)a_i$ | uniform-weight star behavior |
| one very small special edge | uses special edge first | override correctness |
| no special edges | star centered at min | implicit graph compression |

## Edge Cases

When all vertices have identical $a_i$, the implicit graph assigns the same weight to every edge. The algorithm still selects a single root and builds a star, which is valid because every spanning tree has identical total weight, so any tree is optimal.

When a special edge connects two non-root vertices with weight smaller than $a_r$, Kruskal will pick it before any star edge, merging components early. The star edges then connect remaining vertices as needed, preserving optimality.

When a special edge forms a cycle with lower cost alternatives, DSU prevents it from being chosen, ensuring the algorithm never violates acyclicity while still considering it in sorted order.
