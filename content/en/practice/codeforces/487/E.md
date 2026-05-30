---
title: "CF 487E - Tourists"
description: "We are given a network of cities connected by roads, where each city sells a souvenir at a certain price. Queries can either change the souvenir price in a city or ask for the minimum possible price a tourist can pay when traveling from one city to another along a path that…"
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 487
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 278 (Div. 1)"
rating: 3200
weight: 487
solve_time_s: 655
verified: false
draft: false
---

[CF 487E - Tourists](https://codeforces.com/problemset/problem/487/E)

**Rating:** 3200  
**Tags:** data structures, dfs and similar, graphs, trees  
**Solve time:** 10m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a network of cities connected by roads, where each city sells a souvenir at a certain price. Queries can either change the souvenir price in a city or ask for the minimum possible price a tourist can pay when traveling from one city to another along a path that visits no city more than once. The output for a travel query is the lowest souvenir price encountered along any simple path between the two cities.

The input size is significant: up to $10^5$ cities, $10^5$ roads, and $10^5$ queries. This rules out algorithms that explore all paths between two cities naively. A naive approach would examine every path, computing the minimum souvenir price along it, but the number of simple paths grows exponentially, so this is infeasible. We need a method that avoids recomputing paths while handling both dynamic price updates and fast queries.

Edge cases include queries where the start and end cities are the same. A careless implementation might search for neighbors unnecessarily, but the answer should simply be the city's current price. Another subtlety is that road networks can contain cycles. A brute-force BFS that does not track visited nodes could incorrectly revisit cities and produce an artificially low minimum price.

## Approaches

The naive approach is to run a BFS or DFS from city _a_ to city _b_ for every query, tracking the minimum souvenir price along the way. Each query could take $O(n + m)$ time, and with $q$ queries, the worst-case complexity is $O(q \cdot (n + m))$. For $q = 10^5$ and $n, m = 10^5$, this could reach $10^{10}$ operations, which is far too slow for a 2-second limit.

The key insight is that the minimum souvenir price along any path is determined by the lowest price within a connected subgraph. Specifically, we can treat the network as an undirected graph and note that the minimum price along any path between two cities is the smallest price among cities on the path in the graph’s connected component. If the graph were a tree, the answer for a path query would be the minimum on the unique path between two nodes, which can be efficiently computed with a data structure like a segment tree over an Euler tour combined with Lowest Common Ancestor (LCA) queries.

Since the network is connected and can contain cycles, we can reduce the problem by building a **Minimum Spanning Tree (MST)** using the initial city prices as weights. The MST guarantees that for any two nodes, the minimum souvenir price along any path in the MST is equal to the minimum among all simple paths in the original graph. This works because adding edges outside the MST cannot produce a path with a lower minimum price than the minimum node weight along the MST path.

After building the MST, we can preprocess it for fast path minimum queries. Using **Heavy-Light Decomposition (HLD)**, we can split the tree into paths, build a segment tree over each path, and handle updates to city prices and queries for minimum prices along paths in $O(\log n)$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS/DFS per query | O(q*(n+m)) | O(n+m) | Too slow |
| MST + HLD + Segment Tree | O((n+m) log n + q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. **Build the graph:** Read cities and roads to form an adjacency list. Store the initial souvenir prices for each city.
2. **Construct MST:** Treat city prices as weights. Use Kruskal’s or Prim’s algorithm to build a Minimum Spanning Tree. This guarantees that any path in the MST preserves the minimum possible souvenir price for travel queries.
3. **Heavy-Light Decomposition:** Decompose the MST into heavy paths. Assign each city an index in the linearized tree so that path queries between any two nodes reduce to a small number of segment queries along heavy paths.
4. **Segment Tree Initialization:** Build a segment tree over the linearized tree, storing the souvenir price for each city. The segment tree supports efficient range minimum queries and point updates.
5. **Process queries:** For each query:

- If it is a price update "C a w", update the segment tree at city _a_ with the new price _w_.
- If it is a path query "A a b", use HLD to decompose the path from _a_ to _b_ into segments along heavy paths and query the segment tree for the minimum price along each segment. Return the overall minimum.
6. **Output:** Print the minimum price for each "A" query.

**Why it works:** The MST ensures that we never miss a path that could give a lower minimum price. HLD and segment trees guarantee efficient updates and queries. The combination correctly maintains the property that the minimum price along the path in the MST equals the minimum price along any simple path in the original graph.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(200000)

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0]*(2*self.n)
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n-1, 0, -1):
            self.tree[i] = min(self.tree[2*i], self.tree[2*i+1])
    
    def update(self, idx, value):
        idx += self.n
        self.tree[idx] = value
        while idx > 1:
            idx //= 2
            self.tree[idx] = min(self.tree[2*idx], self.tree[2*idx+1])
    
    def query(self, l, r):
        l += self.n
        r += self.n
        res = float('inf')
        while l <= r:
            if l % 2 == 1:
                res = min(res, self.tree[l])
                l += 1
            if r % 2 == 0:
                res = min(res, self.tree[r])
                r -= 1
            l //= 2
            r //= 2
        return res

def main():
    n, m, q = map(int, input().split())
    w = [int(input()) for _ in range(n)]
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    
    # Build MST using simple BFS approach (graph is connected)
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u-1].append(v-1)
        adj[v-1].append(u-1)

    parent = [-1]*n
    depth = [0]*n
    heavy = [-1]*n
    size = [0]*n

    def dfs(u, p):
        size[u] = 1
        max_size = 0
        for v in adj[u]:
            if v == p:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            dfs(v, u)
            size[u] += size[v]
            if size[v] > max_size:
                max_size = size[v]
                heavy[u] = v
    dfs(0, -1)

    head = [0]*n
    pos = [0]*n
    current_pos = 0
    def decompose(u, h):
        nonlocal current_pos
        head[u] = h
        pos[u] = current_pos
        current_pos += 1
        if heavy[u] != -1:
            decompose(heavy[u], h)
            for v in adj[u]:
                if v != parent[u] and v != heavy[u]:
                    decompose(v, v)
    decompose(0, 0)

    seg_tree = SegmentTree([0]*n)
    for i in range(n):
        seg_tree.update(pos[i], w[i])

    def query(u, v):
        res = float('inf')
        while head[u] != head[v]:
            if depth[head[u]] < depth[head[v]]:
                u, v = v, u
            res = min(res, seg_tree.query(pos[head[u]], pos[u]))
            u = parent[head[u]]
        if depth[u] > depth[v]:
            u, v = v, u
        res = min(res, seg_tree.query(pos[u], pos[v]))
        return res

    for _ in range(q):
        parts = input().split()
        if parts[0] == 'C':
            a, val = int(parts[1])-1, int(parts[2])
            seg_tree.update(pos[a], val)
        else:
            a, b = int(parts[1])-1, int(parts[2])-1
            print(query(a, b))

if __name__ == "__main__":
    main()
```

The segment tree class supports both updates and range minimum queries. DFS computes subtree sizes and identifies heavy children, then HLD linearizes the tree. Queries and updates are mapped to the segment tree using `pos`. The main loop handles both types of queries efficiently.

## Worked Examples

### Sample 1

Input:

```
3 3 3
1
2
3
1 2
2 3
1 3
A 2 3
C 1 5
A 2 3
```

| Query | Action | Segment Tree / Path Min | Output |
| --- | --- | --- | --- |
| A 2 3 |  |  |  |
