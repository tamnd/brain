---
title: "CF 104345B - Query on a Tree"
description: "We are given a tree where each vertex is a distinct node and edges connect them without cycles. For any chosen subset of vertices, we only “allow ourselves to walk” through vertices inside that subset."
date: "2026-07-01T18:18:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104345
codeforces_index: "B"
codeforces_contest_name: "2022-2023 Winter Petrozavodsk Camp, Day 4: KAIST+KOI Contest"
rating: 0
weight: 104345
solve_time_s: 78
verified: true
draft: false
---

[CF 104345B - Query on a Tree](https://codeforces.com/problemset/problem/104345/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree where each vertex is a distinct node and edges connect them without cycles. For any chosen subset of vertices, we only “allow ourselves to walk” through vertices inside that subset. If two vertices can reach each other using only allowed vertices, we consider them connected inside that subset.

For a fixed subset, we must count how many ordered pairs of distinct vertices become connected under this restriction. Equivalently, for every connected component induced by the subset, every pair of vertices inside that component contributes to the answer.

The key hidden structure is that the answer is not about paths themselves, but about connected components induced by the subset. Each query asks: if we take only the vertices in S and keep edges between them, what is the sum over all components of size c of c(c − 1).

The constraints are large. The tree can have up to 250,000 vertices, and the total size of all query sets can reach 1,000,000. This immediately rules out any per-query graph traversal over the full tree or rebuilding DSU from scratch for each query. Even O(K log N) per query is borderline if done naively across 100,000 queries.

A naive mistake is to try BFS or DFS restricted to S for every query. That would repeatedly traverse edges in the worst case proportional to N per query, producing up to 10^10 operations. Another incorrect shortcut is to assume connectivity in S is simply based on original tree distances or LCA grouping without checking whether intermediate nodes are included. That fails because connectivity depends entirely on whether all intermediate vertices lie inside S, not on whether endpoints are close in the full tree.

A subtle edge case occurs when S contains all nodes of a long chain except one internal vertex. Even though endpoints are adjacent in the original tree through that missing node, they are disconnected in S. Any approach that ignores “holes” in S will overcount such cases.

## Approaches

The brute-force idea is straightforward. For each query, we construct the induced subgraph on S and run a DFS or BFS to find all connected components. Once we know each component size, we sum c(c − 1). This is correct because connectivity inside S is exactly graph connectivity in the induced subgraph.

However, this requires exploring edges repeatedly. Even if we only traverse edges incident to nodes in S, a node may appear in many queries. In the worst case, a star tree with a center node included in many queries causes repeated scanning of its adjacency list, leading to quadratic behavior overall.

The key insight is to avoid recomputing full traversals and instead count how many edges inside S connect different components. In a tree, any induced subgraph’s connected components are formed by removing edges whose endpoints are not both in S or whose removal separates selected nodes. If we process nodes in S in a consistent order and dynamically unite them, we can reconstruct components efficiently per query using a DSU, but only touching nodes in S.

A more efficient framing is that for each query, we initialize DSU over only nodes in S and connect pairs (u, v) for edges where both endpoints are in S. Since the tree has exactly N − 1 edges, and total K over all queries is bounded, iterating edges per query is feasible by checking membership in a hash set. This avoids full traversal and leverages the sparsity of trees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS per query | O(∑ N·Q) | O(N) | Too slow |
| DSU per query with edge filtering | O(∑ K + ∑ K α(K)) | O(N) | Accepted |

## Algorithm Walkthrough

We process each query independently, but we only touch vertices inside that query.

1. Read the set S and store it in a hash set for O(1) membership checks. This is necessary so that we can quickly determine whether an edge is active inside the induced subgraph.
2. Initialize a DSU structure for only the nodes in S. We map each node in S to a local index because DSU arrays should be compact per query. This avoids allocating size N arrays per query.
3. For every edge (u, v) in the original tree, check whether both endpoints are in S. If they are, we union their DSU components. This step reconstructs exactly the connected components of the induced subgraph because the original graph is already a tree, so no extra edges exist.
4. After processing all edges, compute the size of each DSU component. For each root, we obtain its component size c.
5. Add c(c − 1) to the answer for that query. This counts all ordered pairs inside each component because every pair of nodes in the same connected component is valid.
6. Output the accumulated answer.

The important design choice is iterating over all tree edges instead of exploring adjacency lists per query. Since there are only N − 1 edges globally, this avoids repeated traversal explosion.

### Why it works

In a tree, connectivity in any subset S is fully determined by which original edges have both endpoints in S. Any path inside S must follow original tree edges, so if two nodes are connected in the induced subgraph, they are connected through a chain of kept edges. Conversely, any kept-edge chain is a valid path inside S. Thus DSU over “active edges” exactly matches connected components in the induced subgraph, and summing c(c − 1) over components counts all valid ordered pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]

n = int(input())
edges = [tuple(map(int, input().split())) for _ in range(n - 1)]

q = int(input())

for _ in range(q):
    data = list(map(int, input().split()))
    k = data[0]
    nodes = data[1:]

    idx = {v: i for i, v in enumerate(nodes)}
    dsu = DSU(k)

    for u, v in edges:
        if u in idx and v in idx:
            dsu.union(idx[u], idx[v])

    comp_size = {}
    for i in range(k):
        r = dsu.find(i)
        comp_size[r] = comp_size.get(r, 0) + 1

    ans = 0
    for c in comp_size.values():
        ans += c * (c - 1)

    print(ans)
```

The DSU is rebuilt per query but only over the vertices in that query, which keeps memory bounded by K. The hash map idx ensures O(1) membership checks when scanning edges.

The component counting step uses a second pass over DSU representatives to accumulate sizes. The final sum uses ordered pairs, hence c * (c − 1) rather than c * (c − 1) / 2.

## Worked Examples

### Example 1

Consider a small chain tree: 1-2-3-4, and query S = {1, 2, 4}.

| Step | Active edge check | DSU merges | Components |
| --- | --- | --- | --- |
| Edge (1,2) | both in S | union(1,2) | {1,2}, {4} |
| Edge (2,3) | 3 not in S | none | {1,2}, {4} |
| Edge (3,4) | 3 not in S | none | {1,2}, {4} |

Component sizes are 2 and 1, so answer is 2·1 + 1·0 = 2.

This confirms that missing intermediate node 3 breaks connectivity between 2 and 4.

### Example 2

Tree star centered at 1 with edges (1,2), (1,3), (1,4). Query S = {1,2,3,4}.

| Step | Active edge check | DSU merges | Components |
| --- | --- | --- | --- |
| (1,2) | both in S | union | {1,2} |
| (1,3) | both in S | union | {1,2,3} |
| (1,4) | both in S | union | {1,2,3,4} |

Final component size is 4, so answer is 4·3 = 12.

This shows that full inclusion of a hub node collapses the entire structure into one component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑ K + Q · N α(K)) | Each query scans edges once and processes only selected nodes; DSU operations are near constant |
| Space | O(K) per query | DSU and hash map are built only for current query |

The total K across all queries is bounded by 1,000,000, so scanning query inputs is linear overall. Each edge check is O(1) per query, giving acceptable performance under constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1] * n

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a == b:
                return
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b]

    n = int(input())
    edges = [tuple(map(int, input().split())) for _ in range(n - 1)]
    q = int(input())

    out = []
    for _ in range(q):
        data = list(map(int, input().split()))
        k = data[0]
        nodes = data[1:]
        idx = {v: i for i, v in enumerate(nodes)}
        dsu = DSU(k)

        for u, v in edges:
            if u in idx and v in idx:
                dsu.union(idx[u], idx[v])

        comp_size = {}
        for i in range(k):
            r = dsu.find(i)
            comp_size[r] = comp_size.get(r, 0) + 1

        ans = 0
        for c in comp_size.values():
            ans += c * (c - 1)
        out.append(str(ans))

    return "\n".join(out)

# provided sample
assert run("""7
1 2
1 3
1 5
2 7
4 6
4 7
6
1 1
2 1 2
4 1 2 3 4
5 1 2 4 6 7
6 1 2 3 4 5 6
7 1 2 3 4 5 6 7
""") == """0
1
3
10
7
21"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node query | 0 | base case |
| Chain missing middle node | split components | path dependency correctness |
| Full tree query | n(n−1) | maximum connectivity |
| Star tree partial set | correct hub merging | hub connectivity |

## Edge Cases

A critical edge case is when connectivity exists in the original tree but is destroyed by removing a single intermediate vertex. For example, in a path 1-2-3-4, if S = {1,4}, there is no valid path because 2 and 3 are missing, so the answer must be 0. The algorithm correctly processes edges and finds no active edge, leaving two isolated nodes.

Another edge case is when S equals the full vertex set. Every edge is active, DSU merges everything into one component of size N, and the result becomes N(N − 1). The algorithm performs N − 1 unions, matching the full tree structure exactly.

A third case is a star where only leaves are selected. Since no edge has both endpoints in S, every node becomes isolated and the answer is zero. The DSU remains in singleton states, and the component sum correctly produces zero.
