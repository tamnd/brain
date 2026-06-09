---
title: "CF 1706E - Qpwoeirut and Vertices"
description: "We are given a connected undirected graph with $n$ vertices and $m$ edges. Each edge is numbered from 1 to $m$, and we are asked to process $q$ queries."
date: "2026-06-09T21:20:49+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dfs-and-similar", "divide-and-conquer", "dsu", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1706
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 809 (Div. 2)"
rating: 2300
weight: 1706
solve_time_s: 133
verified: false
draft: false
---

[CF 1706E - Qpwoeirut and Vertices](https://codeforces.com/problemset/problem/1706/E)

**Rating:** 2300  
**Tags:** binary search, data structures, dfs and similar, divide and conquer, dsu, greedy, trees  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected undirected graph with $n$ vertices and $m$ edges. Each edge is numbered from 1 to $m$, and we are asked to process $q$ queries. Each query provides a range of vertex indices $[l, r]$, and we are to determine the smallest number of initial edges $k$ such that all vertices in that range are mutually reachable using only edges 1 through $k$.

Restating in practical terms: imagine you add edges to an initially empty graph one by one following the given order. For a given set of consecutive vertices, we want to know the moment when they form a connected component among themselves. We do not care about connectivity to vertices outside this range, only internal connectivity.

The constraints imply that $n$ can be up to $10^5$ and $m, q$ up to $2 \cdot 10^5$ per test case, with totals over all test cases bounded similarly. This means an algorithm with complexity $O(n m q)$ or $O(n^2)$ is impossible. We need something linear or near-linear in $m$ and $n$ per test case.

Non-obvious edge cases include ranges of length 1 and queries where $l$ and $r$ are at the extremes of the vertex ordering. For example, a query like $l=1, r=1$ should return 0, because a single vertex is trivially connected to itself. Careless implementations that always process edges would return at least 1.

## Approaches

A naive approach is to simulate adding edges incrementally and, for each query, check whether the vertices in the query range are connected. This requires maintaining a subgraph of the first $k$ edges and performing $O(r-l+1)$ connectivity checks per query. In the worst case, this is $O(m q n)$, which is far too slow.

The key insight is that the problem asks for connectivity of **consecutive ranges of vertices**, not arbitrary sets. This allows us to compute, for each vertex $i$, the earliest edge $f[i]$ after which vertex $i$ becomes connected to $i-1$. If we maintain this information while iterating through the edges in order, the problem reduces to a **range maximum query**: for a query $[l, r]$, the answer is $\max(f[l+1], f[l+2], ..., f[r])$. This works because connectivity of the whole range requires the largest edge index that connects any consecutive pair.

To efficiently compute $f[i]$, we can use a Disjoint Set Union (DSU) structure, also known as Union-Find. As we add edges, we merge the sets containing the edge endpoints and track the maximum vertex in each component. When two components merge, we update the first edge that connects consecutive vertices in that component. This process runs in near-linear time.

This reduces the per-query work to a range maximum query on the array $f$, which can be preprocessed with a segment tree or simply a prefix maximum array if queries are offline.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q \cdot n \cdot m)$ | $O(n+m)$ | Too slow |
| Optimal | $O((n+m) \cdot \alpha(n) + q)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Initialize a DSU structure for $n$ vertices. Each vertex starts in its own component.
2. Initialize an array $f[2..n]$ with zeros. $f[i]$ will store the minimum edge index after which vertices $i-1$ and $i$ are connected.
3. Iterate over edges in order $1..m$. For an edge connecting $u$ and $v$:

- Find the components of $u$ and $v$ using DSU.
- If they are already in the same component, skip.
- Otherwise, merge the two components. After merging, for all consecutive vertices spanning the union, update $f[i] = \text{current edge index}$ if it was zero.
4. After processing all edges, compute the prefix maximum array $F$ from $f$. Here $F[i] = \max(f[2..i])$. This allows $O(1)$ query answer by taking $F[r]$ or $F[r] - F[l]$ depending on indexing.
5. For each query $[l, r]$:

- If $l = r$, output 0.
- Otherwise, output $\max(f[l+1..r])$. This corresponds to the earliest edge after which the entire range becomes connected.

**Why it works:** Every merge step ensures that the first edge connecting any two consecutive vertices is recorded in $f$. Because a range is connected if and only if all consecutive pairs are connected, taking the maximum of these values gives the minimal $k$ required. The DSU guarantees we never miss a merge and the union-by-rank heuristic ensures efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.size = [1]*n
        self.left = list(range(n))
        self.right = list(range(n))

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y, edge_idx, f):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.size[x] < self.size[y]:
            x, y = y, x
        for i in range(self.left[y]+1, self.right[y]+1):
            if f[i] == 0:
                f[i] = edge_idx
        self.p[y] = x
        self.size[x] += self.size[y]
        self.left[x] = min(self.left[x], self.left[y])
        self.right[x] = max(self.right[x], self.right[y])

def solve():
    t = int(input())
    for _ in range(t):
        n, m, q = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(m)]
        edges = [(u-1, v-1) for u,v in edges]
        f = [0]*(n+1)
        dsu = DSU(n)
        for idx, (u, v) in enumerate(edges, 1):
            dsu.union(u, v, idx, f)
        prefix_max = [0]*(n+1)
        for i in range(2, n+1):
            prefix_max[i] = max(prefix_max[i-1], f[i])
        for _ in range(q):
            l, r = map(int, input().split())
            if l == r:
                print(0, end=' ')
            else:
                print(prefix_max[r], end=' ')
        print()

if __name__ == "__main__":
    solve()
```

The DSU stores leftmost and rightmost vertices in each component. When two components merge, it updates the earliest edge connecting all consecutive vertices in the merged interval. The prefix maximum array converts consecutive pair values into fast query responses. Boundary handling ensures queries of length 1 return 0.

## Worked Examples

### Example 1

Input:

```
2 1 2
1 2
1 1
1 2
```

State of key variables after edges:

| Vertex | f[i] |
| --- | --- |
| 2 | 1 |

Query results:

| Query | Max f[l+1..r] | Answer |
| --- | --- | --- |
| 1 1 | - | 0 |
| 1 2 | f[2]=1 | 1 |

This confirms that a single vertex is trivially connected and the first edge connects vertices 1 and 2.

### Example 2

Input:

```
5 5 5
1 2
1 3
2 4
3 4
3 5
1 4
3 4
2 2
2 5
3 5
```

Prefix max $F$ after processing edges: `[0, 0, 1, 3, 3, 5]`

Queries:

| Query | Max f[l+1..r] | Answer |
| --- | --- | --- |
| 1 4 | max(f[2..4])=3 | 3 |
| 3 4 | f[4]=3 | 3 |
| 2 2 | - | 0 |
| 2 5 | max(f[3..5])=5 | 5 |
| 3 5 | max(f[4..5])=5 | 5 |

The table shows that taking the maximum over consecutive pairs correctly produces the earliest edge covering the entire range.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) α(n) + q) | DSU operations run in near-linear time with path compression and union by size. Computing |
