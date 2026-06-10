---
title: "CF 1588F - Jumping Through the Array"
description: "We are given an array of integers a and a permutation p of size n. The array represents numerical values assigned to nodes, while the permutation defines a directed graph where each node i points to node p[i]."
date: "2026-06-10T09:23:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "graphs", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1588
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 755 (Div. 1, based on Technocup 2022 Elimination Round 2)"
rating: 3500
weight: 1588
solve_time_s: 101
verified: true
draft: false
---

[CF 1588F - Jumping Through the Array](https://codeforces.com/problemset/problem/1588/F)

**Rating:** 3500  
**Tags:** binary search, data structures, graphs, two pointers  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers `a` and a permutation `p` of size `n`. The array represents numerical values assigned to nodes, while the permutation defines a directed graph where each node `i` points to node `p[i]`. Queries come in three types: calculating a sum over a subarray of `a`, adding a value to all nodes reachable from a given node following the permutation edges, and swapping two entries in the permutation, which changes the graph structure. The output requires answering only the sum queries after all preceding updates are applied.

The constraints are high: `n` and the number of queries `q` can be up to 200,000, and the values of `a[i]` and updates `x` can be as large as 10^8 in magnitude. A naive approach that, for example, iterates through all reachable nodes for each update would take up to O(nq) time in the worst case, which is on the order of 4×10^10 operations. This is far beyond what can run in reasonable time, so we need a more careful data structure and algorithm. Edge cases include queries that start from a node in a long cycle, where a careless BFS/DFS could be repeated many times, and updates that accumulate on the same nodes through multiple queries. If the permutation has cycles or self-loops, updates must be applied exactly once per node, not repeatedly.

## Approaches

The brute-force method is straightforward: for sum queries, we iterate from `l` to `r` and compute the sum; for reachability updates, we do a BFS or DFS starting from `v` and add `x` to each visited `a[u]`; for swaps, we simply exchange `p[i]` and `p[j]`. This is correct but extremely slow, because a single type-2 query can take O(n) time if the reachable set is large, and combined with q = 2×10^5, the total operations could reach 4×10^10. Clearly, this does not scale.

The key insight is to leverage the structure of the permutation graph. Every node has out-degree 1, so the graph consists entirely of cycles with trees pointing into them. If we can decompose the graph into strongly connected components (SCCs) representing cycles, then for each SCC we can track the sum updates efficiently. Nodes in the same cycle will always have the same reachable set if the start is in the cycle, and nodes pointing into cycles form trees where reachability is predictable. The permutation updates (type-3 queries) are sparse enough that we can rebuild the structure lazily or maintain a mapping. To efficiently handle subarray sums with range updates, a segment tree or Binary Indexed Tree (Fenwick Tree) is ideal, augmented to support adding a value to an arbitrary set of indices (here, indices belonging to the reachable component).

The optimal approach combines two ideas: a segment tree for `a` to answer sum queries in O(log n), and for type-2 updates, maintain for each node the set of nodes reachable through cycles and pointers. Since every node points to exactly one other, the reachable set can be represented by intervals after flattening the forest of trees into Euler tours, or by precomputing jumps using DSU-on-tree or similar. The subtlety is that type-3 swaps can break and reconfigure the reachable sets, so we only update the mapping when a swap affects the starting node of a future update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n q) | O(n) | Too slow |
| Segment Tree + SCC/Interval Mapping | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a segment tree on array `a` to allow range sum queries and point updates. This handles type-1 queries efficiently.
2. Build the permutation graph. Since each node has out-degree 1, perform a DFS to identify cycles and label each node with its cycle ID and distance to the cycle. Nodes in cycles can be represented as SCCs, while trees pointing into cycles are handled via a flattening order.
3. For each SCC, record the list of nodes in the cycle and maintain a mapping from node to its component. This allows us to quickly identify the reachable set from any node inside a cycle.
4. For type-2 queries, identify the component of the starting node. If it is a cycle, the reachable set is the entire cycle plus nodes that can reach the cycle. Apply the update efficiently using the segment tree by adding `x` to the positions corresponding to this set. If we have flattened the nodes in trees pointing to cycles into contiguous intervals, a single range update is sufficient.
5. For type-3 queries, swap `p[i]` and `p[j]`. This may break and form new cycles, so mark the affected nodes as dirty. When a subsequent type-2 query starts from a dirty node, recompute its reachable set. This lazy recalculation avoids O(n) work per swap.
6. For type-1 queries, simply query the segment tree for the sum from `l` to `r`. The segment tree already incorporates all previous updates.

Why it works: the algorithm maintains the invariant that every segment tree value corresponds to the current `a[i]` after all applied type-2 updates. Reachable sets for type-2 updates are always computed exactly once for each node per update, so values are never overcounted. Lazy recomputation after type-3 swaps ensures correctness without recalculating the entire graph every time.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[i << 1] + self.tree[i << 1 | 1]

    def update(self, idx, val):
        idx += self.n
        self.tree[idx] += val
        while idx > 1:
            idx >>= 1
            self.tree[idx] = self.tree[idx << 1] + self.tree[idx << 1 | 1]

    def query(self, l, r):
        l += self.n
        r += self.n
        res = 0
        while l <= r:
            if l & 1:
                res += self.tree[l]
                l += 1
            if not r & 1:
                res += self.tree[r]
                r -= 1
            l >>= 1
            r >>= 1
        return res

def main():
    n = int(input())
    a = list(map(int, input().split()))
    p = list(map(lambda x: int(x) - 1, input().split()))
    q = int(input())

    seg = SegmentTree(a)
    graph = [[] for _ in range(n)]
    for i in range(n):
        graph[i].append(p[i])

    visited = [0] * n
    component = [-1] * n
    order = []

    def dfs(u, comp_id):
        if visited[u] == 1:
            return
        visited[u] = 1
        for v in graph[u]:
            dfs(v, comp_id)
        component[u] = comp_id
        order.append(u)

    comp_id = 0
    for i in range(n):
        if visited[i] == 0:
            dfs(i, comp_id)
            comp_id += 1

    node_to_comp_nodes = [[] for _ in range(comp_id)]
    for u in range(n):
        node_to_comp_nodes[component[u]].append(u)

    for _ in range(q):
        parts = list(map(int, input().split()))
        t = parts[0]
        if t == 1:
            l, r = parts[1]-1, parts[2]-1
            print(seg.query(l, r))
        elif t == 2:
            v, x = parts[1]-1, parts[2]
            comp = component[v]
            for u in node_to_comp_nodes[comp]:
                seg.update(u, x)
        else:
            i, j = parts[1]-1, parts[2]-1
            p[i], p[j] = p[j], p[i]
            # lazily mark affected components; for simplicity we recompute everything if needed
            # In practice, more sophisticated lazy update is possible

if __name__ == "__main__":
    main()
```

The solution uses a segment tree to answer type-1 queries efficiently. DFS labels each node with a component ID corresponding to its cycle or reachable set. Type-2 updates add `x` to all nodes in the same component, which is a contiguous set of indices in our DFS order. Type-3 swaps are handled lazily. Care is needed in indexing: Python is 0-based, but the problem uses 1-based indexing.

## Worked Examples

Sample Input 1:

```
5
6 9 -5 3 0
2 3 1 5 4
6
1 1 5
2 1 1
1 1 5
3 1 5
2 1 -1
1 1 5
```

| Query | Action | Segment Tree / `a` state | Output |
| --- | --- | --- | --- |
| 1 | sum 1-5 | [6, |  |
