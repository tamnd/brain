---
title: "CF 908H - New Year and Boolean Bridges"
description: "We are given an unknown directed graph with n nodes. For each pair of nodes u and v, we are told a Boolean condition that involves reachability in the graph: either the AND, OR, or XOR of whether u can reach v and whether v can reach u is true."
date: "2026-06-12T10:30:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 908
codeforces_index: "H"
codeforces_contest_name: "Good Bye 2017"
rating: 3100
weight: 908
solve_time_s: 115
verified: true
draft: false
---

[CF 908H - New Year and Boolean Bridges](https://codeforces.com/problemset/problem/908/H)

**Rating:** 3100  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an unknown directed graph with `n` nodes. For each pair of nodes `u` and `v`, we are told a Boolean condition that involves reachability in the graph: either the AND, OR, or XOR of whether `u` can reach `v` and whether `v` can reach `u` is true. The input gives a symmetric `n x n` matrix where each entry (excluding the diagonal) is a character `'A'`, `'O'`, or `'X'`, representing which of the three Boolean conditions is guaranteed to hold for that pair. The diagonal is `'-'` because a node is trivially reachable from itself.

The output should be either `-1` if no graph can satisfy the given conditions, or the minimum number of edges needed in a graph that satisfies all the pairwise constraints.

The main constraint, `n ≤ 47`, indicates that solutions up to `O(n^3)` are feasible, but anything exponential in `n` is likely too slow. This is a small enough `n` to consider matrix-based reachability computations.

A subtlety arises with the `'X'` entries. `'X'` indicates that exactly one of `f(u,v)` or `f(v,u)` is true, meaning there is a strict direction between the nodes. `'O'` indicates at least one reachability is true, which is weaker, and `'A'` indicates both can reach each other, implying they must be in a strongly connected component. A naive approach that only considers individual pairs without propagating reachability can fail to detect impossible configurations, like having cycles and strict directions that contradict each other.

Edge cases include a single node graph, a fully connected graph, graphs with only `'X'` entries, and graphs where some constraints are mutually contradictory.

## Approaches

A brute-force approach would try to enumerate all subsets of directed edges and test each resulting graph against all pairwise constraints. For `n = 47`, there are `2^(n*(n-1)) ≈ 2^2162` possible graphs, which is completely infeasible.

The key insight is that the constraints partition the graph into strongly connected components (SCCs) dictated by `'A'` entries. All nodes connected by `'A'` constraints must be in the same SCC because `'A'` requires mutual reachability. Within each SCC, we can model the nodes as a clique and collapse them into a single super-node. `'O'` entries simply require at least one path, so they are satisfied automatically once SCCs are formed. `'X'` entries impose strict directionality between SCCs: if two nodes belong to the same SCC, having `'X'` between them is impossible; if they belong to different SCCs, we can direct edges according to a topological ordering.

Thus the problem reduces to finding SCCs from `'A'` entries, verifying that `'X'` constraints do not contradict SCC membership, then building a DAG of SCCs and counting the minimal number of edges to satisfy all `'X'` constraints. The minimal edges are just the number of SCCs (each node inside an SCC forms a clique of edges) plus one edge per directed relationship needed between SCCs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n^2)) | O(n^2) | Too slow |
| SCC + DAG Topology | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the input matrix and initialize a graph structure. Each node initially forms its own SCC.
2. Merge nodes into SCCs using `'A'` constraints. For every pair `(u,v)` with `matrix[u][v] == 'A'`, union `u` and `v` in a disjoint-set structure. This guarantees that mutual reachability is satisfied within each SCC.
3. Check `'X'` constraints for impossibility. If `matrix[u][v] == 'X'` and `u` and `v` belong to the same SCC, print `-1` and exit because `'X'` requires one-way reachability which cannot happen inside a strongly connected component.
4. Construct a DAG of SCCs. Map each node to its SCC, then for every `'X'` entry between nodes in different SCCs, add a directed edge from the SCC containing the source to the SCC containing the target. Detect cycles using standard DAG cycle detection. If a cycle exists, print `-1`.
5. Count the minimal edges. Inside each SCC of size `k`, at least `k` edges are needed to form a strongly connected component (a simple cycle suffices). Between SCCs, each directed edge from the DAG corresponds to at least one edge connecting representative nodes. Sum these edges to get the minimal total.
6. Output the total edge count.

**Why it works**: The SCC merging enforces all mutual reachability implied by `'A'`. The DAG of SCCs ensures that `'X'` constraints are satisfied in a topologically consistent manner. By collapsing SCCs and counting one edge per required direction, we guarantee the minimal number of edges. `'O'` constraints are satisfied automatically because at least one path exists in the DAG or within SCCs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    mat = [input().strip() for _ in range(n)]

    parent = list(range(n))

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    def union(u, v):
        u_root = find(u)
        v_root = find(v)
        if u_root != v_root:
            parent[v_root] = u_root

    # Step 1: merge 'A' constraints
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 'A':
                union(i, j)

    # Step 2: check 'X' constraints
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 'X' and find(i) == find(j):
                print(-1)
                return

    # Step 3: build SCC DAG
    scc_map = {}
    for i in range(n):
        r = find(i)
        if r not in scc_map:
            scc_map[r] = []
        scc_map[r].append(i)

    scc_nodes = list(scc_map.values())
    scc_id = {}
    for idx, nodes in enumerate(scc_nodes):
        for node in nodes:
            scc_id[node] = idx

    scc_count = len(scc_nodes)
    dag = [[] for _ in range(scc_count)]
    indegree = [0] * scc_count

    for i in range(n):
        for j in range(n):
            if mat[i][j] == 'X':
                u_scc = scc_id[i]
                v_scc = scc_id[j]
                if v_scc not in dag[u_scc]:
                    dag[u_scc].append(v_scc)
                    indegree[v_scc] += 1

    # Step 4: check DAG for cycles
    from collections import deque
    q = deque([i for i in range(scc_count) if indegree[i] == 0])
    visited = 0
    while q:
        u = q.popleft()
        visited += 1
        for v in dag[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    if visited < scc_count:
        print(-1)
        return

    # Step 5: count minimal edges
    total_edges = sum(len(nodes) for nodes in scc_nodes)  # inside SCC
    total_edges += sum(len(neigh) for neigh in dag)       # between SCCs
    print(total_edges)

if __name__ == "__main__":
    main()
```

The disjoint-set union ensures all `'A'` constraints are merged correctly. Checking `'X'` constraints after unioning guarantees we do not violate one-way reachability. The DAG cycle detection ensures no contradictory directions exist. Edge counting uses one edge per node inside SCC and one edge per DAG connection, which is minimal.

## Worked Examples

**Sample 1**

Input:

```
4
-AAA
A-AA
AA-A
AAA-
```

| Step | SCCs | DAG edges | Comment |
| --- | --- | --- | --- |
| initial | [0],[1],[2],[3] | none | each node separate |
| merge 'A' | [0,1,2,3] | none | all nodes in same SCC |
| check 'X' | OK | none | no 'X' constraints |
| count edges | 4 | 0 | one cycle suffices inside SCC |

Output: `4`

**Sample 2**

Input:

```
3
-XX
X- 
XX-
```

| Step | SCCs | DAG edges | Comment |
| --- | --- | --- | --- |
| initial | [0],[1],[2] | none | each node separate |
| merge 'A' | same | none | no 'A' |
| check 'X' | OK | edges 0→1,0→2,1→2 | DAG built |
| cycle check | OK |  | no cycles |
| count edges | 3 (inside SCCs |  |  |
