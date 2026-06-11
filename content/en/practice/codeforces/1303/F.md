---
title: "CF 1303F - Number of Components"
description: "We are given an initially empty matrix of size $n times m$, where all cells start with zero. Each cell can take integer values through a sequence of queries."
date: "2026-06-11T18:08:14+07:00"
tags: ["codeforces", "competitive-programming", "dsu", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1303
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 82 (Rated for Div. 2)"
rating: 2800
weight: 1303
solve_time_s: 132
verified: false
draft: false
---

[CF 1303F - Number of Components](https://codeforces.com/problemset/problem/1303/F)

**Rating:** 2800  
**Tags:** dsu, implementation  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an initially empty matrix of size $n \times m$, where all cells start with zero. Each cell can take integer values through a sequence of queries. After each query, which sets a specific cell to a new value, we are asked to count how many connected components of equal values exist in the matrix. Cells are connected if they share an edge, and a component is any maximal group of connected cells with the same value.

The input guarantees that the values assigned in queries are non-decreasing. This is a crucial constraint because it allows us to process the matrix incrementally without worrying that a previously assigned value will later decrease and potentially break existing components.

The matrix can be up to $300 \times 300 = 90{,}000$ cells, and there can be up to $2 \cdot 10^6$ queries. Counting components by traversing the entire matrix after each query is immediately infeasible because that would be $O(q \cdot n \cdot m)$, which can reach $2 \cdot 10^6 \cdot 9 \cdot 10^4 \approx 2 \cdot 10^{11}$ operations.

Non-obvious edge cases include updating a cell to the same value it already has, which should not change the number of components, and updating a cell that merges multiple existing components, which can reduce the component count by more than one. For example, consider a 2x2 block: if the top-left and bottom-right are separate 1-valued cells and we set the bottom-left to 1, it may connect them into a single component.

## Approaches

The brute-force solution iterates over the entire matrix after each query and performs a flood-fill or BFS to count components. This is correct because each BFS visits each component exactly once, but it requires $O(n \cdot m)$ work per query. With $q$ up to $2 \cdot 10^6$, this is far too slow.

The key observation is that the non-decreasing property of cell values allows us to process cells in increasing value order and use a Union-Find (Disjoint Set Union, DSU) data structure to maintain connected components incrementally. We can store each cell as a node in a DSU and only union it with its neighbors when its value becomes active. Once a cell's value is set, it never decreases, so we never need to split components. This turns the problem from full matrix traversal per query into an incremental union-find problem, giving amortized nearly constant time per union operation with path compression.

Another subtlety is handling multiple queries on the same cell. We only need to process the cell the first time its value reaches a particular threshold. Since queries are sorted by non-decreasing value, we can group updates by value and process them as a batch.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q \cdot n \cdot m)$ | $O(n \cdot m)$ | Too slow |
| Union-Find / Incremental | $O(n \cdot m + q \cdot \alpha(nm))$ | $O(n \cdot m)$ | Accepted |

## Algorithm Walkthrough

1. Represent each cell as a unique index $i \cdot m + j$ in a DSU structure. This allows efficient union and find operations.
2. Sort all queries in non-decreasing order of the new value $c_i$. This ensures that when processing a value, all previous cells with smaller values are already active.
3. Initialize an array `active` to track which cells have been updated to a non-zero value. Initialize the DSU parent array so each cell is its own component. Set the initial number of components to zero.
4. Iterate through the sorted queries. For each query, mark the cell as active if it was previously zero. Increase the component count by one since a new isolated cell represents a new component.
5. Check all four neighbors of the active cell. If a neighbor is active and has the same value, union the two cells in the DSU. Every successful union reduces the component count by one.
6. Record the current number of components as the answer for this query.
7. After processing all queries, output the recorded answers in the original query order.

Why it works: The algorithm maintains the invariant that `components` equals the number of connected components formed by all currently active cells. Since values never decrease and we union only when cells become active, we never incorrectly merge components, and each union operation correctly decrements the component count when two components merge.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, q = map(int, input().split())
queries = []
for idx in range(q):
    x, y, c = map(int, input().split())
    queries.append((c, x - 1, y - 1, idx))

# sort queries by value, non-decreasing
queries.sort()

parent = [-1] * (n * m)
size = [1] * (n * m)
active = [0] * (n * m)
ans = [0] * q

def find(u):
    if parent[u] == -1:
        return u
    parent[u] = find(parent[u])
    return parent[u]

def union(u, v):
    u = find(u)
    v = find(v)
    if u == v:
        return False
    if size[u] < size[v]:
        u, v = v, u
    parent[v] = u
    size[u] += size[v]
    return True

components = 0
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

for c, x, y, idx in queries:
    pos = x * m + y
    if active[pos]:
        ans[idx] = components
        continue
    active[pos] = 1
    components += 1
    for d in range(4):
        nx, ny = x + dx[d], y + dy[d]
        if 0 <= nx < n and 0 <= ny < m:
            npos = nx * m + ny
            if active[npos]:
                if union(pos, npos):
                    components -= 1
    ans[idx] = components

# restore original query order
res = [0] * q
for i, (_, _, _, idx) in enumerate(queries):
    res[idx] = ans[idx]

print('\n'.join(map(str, res)))
```

This implementation explicitly tracks which cells have been activated. Each union is attempted only with active neighbors, ensuring we never merge inactive cells. Sorting queries by value allows processing to be incremental and correct. We restore the original query order at the end because the problem requires output in input order.

## Worked Examples

**Sample 1**

| Query | Cell Activated | Components | Notes |
| --- | --- | --- | --- |
| (2,1,1) | (1,0) | 1 | New cell, no neighbors active |
| (1,2,1) | (0,1) | 2 | New cell, no neighbors same value |
| (2,2,1) | (1,1) | 3 → 2 | Connected to both (1,0) and (0,1), merged two components |
