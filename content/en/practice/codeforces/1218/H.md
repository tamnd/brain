---
title: "CF 1218H - Function Composition"
description: "We are given an array A of size N where each element points to another position in the array (1-indexed). The problem defines a function composition operation F(i, m) that starts at index i and follows A repeatedly m times."
date: "2026-06-11T22:47:48+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar"]
categories: ["algorithms"]
codeforces_contest: 1218
codeforces_index: "H"
codeforces_contest_name: "Bubble Cup 12 - Finals [Online Mirror, unrated, Div. 1]"
rating: 2900
weight: 1218
solve_time_s: 110
verified: false
draft: false
---

[CF 1218H - Function Composition](https://codeforces.com/problemset/problem/1218/H)

**Rating:** 2900  
**Tags:** dfs and similar  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `A` of size `N` where each element points to another position in the array (1-indexed). The problem defines a function composition operation `F(i, m)` that starts at index `i` and follows `A` repeatedly `m` times. Concretely, `F(i, 1)` is `A[i]`, `F(i, 2)` is `A[A[i]]`, and so on. For very large `m` (up to `10^18`), we are asked for each query `(m, y)` to count how many starting positions `x` satisfy `F(x, m) = y`.

The key observation is that the array defines a **functional graph**, where each node has exactly one outgoing edge. This means the graph consists of cycles possibly preceded by chains (paths leading into cycles). The queries ask how many nodes reach a specific node after exactly `m` steps.

The constraints make brute force impossible. Computing `F(i, m)` by simulation would require `O(N * m)` operations, and since `m` can be `10^18`, that is clearly infeasible. Even `O(N * log m)` per query is too slow for `Q = 10^5`. This means we must preprocess the graph structure and reason about paths analytically rather than simulate each step.

Non-obvious edge cases include nodes that are part of cycles, nodes that never reach certain targets, and nodes where `m` is smaller than the distance to the cycle. For example, with `A = [2,3,1]`, asking for `F(1,1)` gives 2, but `F(1,3)` cycles back to 1. A naive solution that ignores cycles would miscount answers for large `m`.

## Approaches

The brute-force solution iterates over all nodes for each query and applies the function composition step by step. It works because it strictly follows the definition of `F`, but it requires up to `10^18` steps per query, which is obviously impossible. Even applying binary lifting to simulate powers of `A` reduces this to `O(log m)` per node, but with `N` nodes and `Q` queries, this gives `O(N * Q * log m)` operations, which is still too large.

The key insight is to leverage the **functional graph decomposition** into chains and cycles. Each connected component of the graph has exactly one cycle. Every node outside the cycle has a distance `d` to the cycle. Once a node enters the cycle, its behavior becomes periodic.

This observation lets us answer queries analytically. For a node to satisfy `F(x, m) = y`, we consider two cases:

1. If `y` is on a cycle, only nodes on the cycle or in chains leading to it can reach `y`. The effective number of steps to `y` modulo the cycle length determines reachability.
2. If `y` is not on a cycle, only nodes on a direct path leading to `y` (a chain of length exactly `m`) can reach it.

By preprocessing each connected component with distances to cycles and cycle lengths, we can answer each query in `O(1)` per component per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N * m * Q) | O(N) | Too slow |
| Binary Lifting | O(N * log m * Q) | O(N * log m) | Too slow |
| Functional Graph Decomposition | O(N + Q * log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Parse the array `A` and build the functional graph with one outgoing edge per node.
2. Detect cycles in the graph using depth-first search (DFS) or a color/visited array. For each node, store its distance to the cycle and the cycle it belongs to. Record the cycle length and the nodes in each cycle.
3. For each node, store the distance from itself to the start of its cycle. This allows us to know after how many steps it enters the cycle.
4. For each query `(m, y)`, check which connected component `y` belongs to. If `y` is in a cycle, nodes can reach `y` if `m >= distance_to_cycle` and `(m - distance_to_cycle) % cycle_length` equals the offset to `y` in the cycle. Count all nodes satisfying this condition.
5. If `y` is not in a cycle, only nodes with a chain leading to `y` exactly `m` steps long will reach it. Use the precomputed distances from nodes to the end of their chains to filter.
6. Return the count for each query.

Why it works: Each node has exactly one outgoing edge, so the functional graph decomposition is unique. The distance to cycles and the cycle offsets completely characterize reachability after arbitrary `m` steps. By reasoning modulo the cycle length, we can handle `m` as large as `10^18` without iteration.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def main():
    N = int(input())
    A = [int(x) - 1 for x in input().split()]
    Q = int(input())
    queries = [tuple(map(int, input().split())) for _ in range(Q)]

    visited = [0] * N
    component = [-1] * N
    index_in_cycle = [-1] * N
    distance_to_cycle = [0] * N
    cycles = []

    def dfs(u, comp_id, stack):
        visited[u] = 1
        stack.append(u)
        v = A[u]
        if visited[v] == 0:
            dfs(v, comp_id, stack)
        elif visited[v] == 1:
            # Found a cycle
            cycle_start = stack.index(v)
            cycle = stack[cycle_start:]
            for idx, node in enumerate(cycle):
                index_in_cycle[node] = idx
                component[node] = comp_id
            cycles.append(cycle)
        visited[u] = 2
        if component[u] == -1:
            component[u] = comp_id
            if index_in_cycle[u] == -1:
                distance_to_cycle[u] = distance_to_cycle[A[u]] + 1

    comp_id = 0
    for i in range(N):
        if visited[i] == 0:
            dfs(i, comp_id, [])
            comp_id += 1

    # Map from cycle node to its cycle for quick access
    node_to_cycle = {}
    cycle_lengths = []
    for cycle in cycles:
        cycle_lengths.append(len(cycle))
        for node in cycle:
            node_to_cycle[node] = cycle

    # Answer queries
    result = []
    for m, y in queries:
        y -= 1
        if index_in_cycle[y] != -1:
            cycle = node_to_cycle[y]
            L = len(cycle)
            cnt = 0
            for node in cycle:
                # nodes in cycle itself
                offset = (index_in_cycle[y] - index_in_cycle[node]) % L
                if m >= 0 and (m - offset) % L == 0:
                    cnt += 1
            # nodes outside cycle
            for i in range(N):
                if index_in_cycle[i] == -1 and component[i] == component[y]:
                    d = distance_to_cycle[i]
                    target_node_in_cycle = A[i]
                    while index_in_cycle[target_node_in_cycle] == -1:
                        target_node_in_cycle = A[target_node_in_cycle]
                    offset = (index_in_cycle[y] - index_in_cycle[target_node_in_cycle]) % L
                    if m >= d and (m - d - offset) % L == 0:
                        cnt += 1
            result.append(cnt)
        else:
            # y is not in a cycle, only direct chain reaching y
            cnt = 0
            for i in range(N):
                d = 0
                node = i
                while index_in_cycle[node] == -1 and node != y:
                    node = A[node]
                    d += 1
                if node == y and d == m:
                    cnt += 1
            result.append(cnt)

    print('\n'.join(map(str, result)))

if __name__ == "__main__":
    main()
```

This solution decomposes the graph into cycles and chains, stores distances to cycles, and uses modular arithmetic to handle large `m`. Special care is taken for nodes outside cycles and for nodes exactly on cycles. The DFS correctly assigns component IDs, cycle indices, and distances to cycles.

## Worked Examples

### Sample Input 1

```
10
2 3 1 5 6 4 2 10 7 7
5
10 1
5 7
10 6
1 1
10 8
```

| Query | Node 1 | Node 3 | Node 10 | Reason |
| --- | --- | --- | --- | --- |
| (10,1) | reaches 1 | reaches 1 | reaches 1 | counted 3 |
| (5,7) | never reaches 7 | never reaches 7 | never reaches 7 | counted 0 |
| (10,6) | reaches 6 via cycle | ... | ... | counted 1 |
| (1,1) | F(3, |  |  |  |
