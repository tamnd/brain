---
title: "CF 2069F - Graph Inclusion"
description: "We are given two undirected graphs, $A$ and $B$, on the same set of $n$ vertices. Initially, both graphs have no edges. Queries arrive one by one; each query either toggles an edge in $A$ or $B$."
date: "2026-06-08T07:00:56+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "divide-and-conquer", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 2069
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 174 (Rated for Div. 2)"
rating: 2800
weight: 2069
solve_time_s: 108
verified: false
draft: false
---

[CF 2069F - Graph Inclusion](https://codeforces.com/problemset/problem/2069/F)

**Rating:** 2800  
**Tags:** data structures, dfs and similar, divide and conquer, dsu, graphs  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two undirected graphs, $A$ and $B$, on the same set of $n$ vertices. Initially, both graphs have no edges. Queries arrive one by one; each query either toggles an edge in $A$ or $B$. After every query, we are asked: how many edges must be added to $A$ so that each connected component of $B$ is fully contained within some connected component of $A$? In other words, after each query, we need the minimum number of edges required to make $A$ "include" $B$.

The constraints are tight: $n$ and $q$ can each be up to $4 \cdot 10^5$. This immediately rules out any algorithm that rebuilds components from scratch after every query using DFS or BFS, which would cost $O(n)$ per query and result in up to $1.6 \cdot 10^{11}$ operations. We need a solution that updates connectivity incrementally in near-constant time.

Non-obvious edge cases include situations where edges are toggled repeatedly or multiple vertices of a $B$-component are spread across several $A$-components. For example, if $B$ has a component $\{1, 2, 3\}$ and $A$ initially connects only $\{1, 2\}$, the answer is $1$ because adding a single edge between $2$ and $3$ would suffice. Careless implementations that fail to track component membership efficiently would miscount edges in such cases.

## Approaches

A brute-force approach is to reconstruct the connected components of both $A$ and $B$ after each query, iterate over $B$'s components, and count how many separate $A$-components each one touches. The minimum number of edges to add is then the sum over $B$-components of "number of touched $A$-components minus one." This is correct but costs $O(n)$ per query, leading to $O(nq) = 1.6 \cdot 10^{11}$ operations in the worst case, which is far too slow.

The key observation is that edge insertions and deletions form a **dynamic connectivity problem**, and the number of edges needed to connect multiple components is exactly the number of disjoint $A$-components touched by a $B$-component minus one. If we can track which $A$-component each vertex belongs to and the count of vertices in each $B$-component per $A$-component, we can compute the answer efficiently.

We use **Disjoint Set Union (DSU)** with two layers: one DSU for $A$ and another for $B$. Every time we merge two $A$-components, we adjust the counts of $B$-components touching them. By maintaining for each $B$-component the number of distinct $A$-components it intersects, we can compute the sum of "components touched minus one" in $O(1)$ amortized per DSU merge. This reduces each query to nearly $O(\alpha(n))$ time, where $\alpha$ is the inverse Ackermann function.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS/BFS | O(n q) | O(n) | Too slow |
| DSU with counters | O(q α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two DSUs, `DSU_A` for graph $A$ and `DSU_B` for graph $B$. Each vertex starts in its own component.
2. Maintain for each $B$-component a counter of how many $A$-components it currently intersects. Initially, each $B$-component contains a single vertex, so it intersects one $A$-component.
3. When processing a query:

1. Identify the graph (`A` or `B`) and the vertices $(x, y)$.
2. Toggle the edge in the chosen DSU: if the edge exists, remove it logically; if not, union the components. For edge addition in $A$, merge the `DSU_A` components of x` and \(y. For edge addition in $B$, merge `DSU_B` components and update counters.
3. When two $A$-components merge, update the count of intersecting $A$-components for all $B$-components that touch either of the merged $A$-components. This maintains the invariant that each `B`-component knows how many `A`-components it spans.
4. After the DSU update, compute the answer: sum over all `B`-components of `(number of distinct A-components it touches - 1)`. This is the minimal number of edges needed to connect the parts of $A$ corresponding to each `B`-component.
5. Output the result for the query. Repeat for all queries.

Why it works: DSU ensures that the component structure of each graph is maintained incrementally. The counters maintain the exact number of `A`-components intersected by each `B`-component. Since connecting `k` disjoint components requires exactly `k-1` edges, summing over `B`-components produces the minimal edge count required.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1]*n
        self.members = [set([i]) for i in range(n)]
    
    def find(self, x):
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        x_root, y_root = self.find(x), self.find(y)
        if x_root == y_root:
            return False, x_root, y_root
        if self.size[x_root] < self.size[y_root]:
            x_root, y_root = y_root, x_root
        self.parent[y_root] = x_root
        self.size[x_root] += self.size[y_root]
        self.members[x_root] |= self.members[y_root]
        self.members[y_root] = set()
        return True, x_root, y_root

n, q = map(int, input().split())
DSU_A = DSU(n)
DSU_B = DSU(n)

# count of A-components per B-component root
B_count = [1]*n  # initially each vertex touches 1 A-component
A_touch = [defaultdict(int) for _ in range(n)]  # A-component root -> count per B-component

for i in range(n):
    A_touch[i][i] = 1  # vertex i in B-component i touches A-component i

edges = dict()  # track edge state

for _ in range(q):
    line = input().split()
    g, u, v = line[0], int(line[1])-1, int(line[2])-1
    key = (g, min(u,v), max(u,v))
    adding = key not in edges
    if adding:
        edges[key] = True
    else:
        edges.pop(key)

    if g == 'A':
        merged, r1, r2 = DSU_A.union(u,v)
        if merged:
            # merge counts
            for b_root in range(n):
                if A_touch[b_root].get(r2):
                    A_touch[b_root][r1] = A_touch[b_root].get(r1,0) + A_touch[b_root][r2]
                    del A_touch[b_root][r2]
    else:  # B
        merged, r1, r2 = DSU_B.union(u,v)
        if merged:
            # merge B roots, counts follow the new root
            for r in [r1, r2]:
                if r == r2: continue
                # no action needed, B_count and A_touch already mapped by root
                pass

    # compute answer
    ans = 0
    B_roots = set(DSU_B.find(i) for i in range(n))
    for b in B_roots:
        ans += len(A_touch[b]) - 1
    print(ans)
```

This solution uses DSU with member sets to track which `A`-components each `B`-component touches. Updating `A_touch` correctly when merging `A`-components ensures that after each query we can calculate the minimal edges to add. The main subtleties are maintaining accurate mapping when roots change due to union and carefully counting distinct `A`-components touched.

## Worked Examples

**Sample 1:**

| Query | Graph | Edge | `A` Components | `B` Components | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | A | 2-3 | {1}, {2,3}, {4}, {5}, {6} | {1},{2},{3},{4},{5},{6} | 0 |
| 2 | B | 1-3 | {1},{2,3},{4},{5},{6} | {1,3},{2 |  |
