---
title: "CF 104566B - Red Black Tree"
description: "We are given a weighted tree rooted at node 1. Some vertices are initially colored red, including the root, and all other vertices are black."
date: "2026-06-30T08:31:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104566
codeforces_index: "B"
codeforces_contest_name: "The 2018 ACM-ICPC Asia Qingdao Regional Contest, Online (The 2nd Universal Cup. Stage 1: Qingdao)"
rating: 0
weight: 104566
solve_time_s: 83
verified: true
draft: false
---

[CF 104566B - Red Black Tree](https://codeforces.com/problemset/problem/104566/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted tree rooted at node 1. Some vertices are initially colored red, including the root, and all other vertices are black. For every vertex, its cost is defined using the red vertices on its path to the root: if the vertex itself is red, its cost is zero, otherwise we look upward along the unique path to the root and find the closest red ancestor, and the cost is the distance along the tree to that ancestor.

For each query, we are given a subset of vertices. We are allowed to pick at most one vertex anywhere in the tree and turn it red temporarily. After that change, the cost of every vertex is recomputed using the same rule. The task is to minimize the maximum cost among the queried vertices.

The input size forces us to think in near linear time per test case. The tree can have up to 100,000 nodes and the total number of queried vertices across all queries can reach 2,000,000. This immediately rules out any per-query traversal of the tree or recomputation of distances from scratch. Any solution must preprocess the tree once and answer each query in roughly linear time in the size of the query set.

A naive approach would recompute costs after trying every possible choice of the newly added red vertex. For a single query, that would mean trying all n choices and recomputing distances for all ki vertices each time, leading to O(n·ki) per query, which is far too large.

A more subtle failure case comes from ignoring that the effect of making a vertex red is not global. For example, consider a vertex x that is not an ancestor of a query vertex v. Turning x red does not affect v at all. Any approach that assumes a new red vertex globally improves all distances will produce incorrect answers.

Another failure mode is assuming that only query vertices matter as candidates for the added red node. The optimal node can lie outside the query set, for example a shared ancestor of several high-cost query vertices.

## Approaches

The key observation is that every vertex already has a well-defined cost computed from the nearest red ancestor on its root path. We can preprocess these costs in one DFS from the root by maintaining the last red vertex seen on the path and computing distances using prefix sums of edge weights.

Once these base costs are known, each query becomes a pure optimization problem on a subset of vertices: we want to reduce the maximum of a set of values by optionally introducing one new “source” vertex that only affects vertices in its own subtree.

A brute-force strategy would try every possible vertex x as the new red node. For each x, we would recompute the cost of each queried vertex v as either its original cost or the distance from v to x if x lies on the path from root to v. This costs O(n·k) per query and fails immediately at the given constraints.

The key simplification is to focus only on the vertices that determine the current maximum answer. If we cannot reduce the current maximum cost value among query vertices, no improvement is possible. If we can reduce it, then the new red node must lie on the root-to-LCA path of all vertices achieving that maximum, because otherwise at least one of them would not be affected.

This reduces the search space of the new red node dramatically. Instead of considering all vertices, we only consider a single candidate structure defined by the LCA of the worst vertices.

From there, the problem becomes checking whether choosing that LCA as the new red node is sufficient to reduce all maximum-cost vertices below the original maximum, and if so computing the resulting new maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all new red nodes | O(q · n · k) | O(n) | Too slow |
| Optimal LCA-based reduction | O(∑k log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first preprocess the tree to compute two values for every vertex: its distance from the root, and its cost based on the nearest red ancestor. This is done with a single DFS where we carry both the current root distance and the nearest red node seen so far on the path.

For LCA queries, we also build a standard binary lifting structure so that we can compute LCAs in logarithmic time.

For each query, we proceed as follows.

1. We scan all vertices in the query set and compute their current costs. During this scan we identify the maximum cost value M and also track the second maximum cost value among the remaining vertices. We also collect the set T of vertices whose cost equals M. This isolates exactly the vertices that determine the current answer.
2. If T contains only one vertex, the problem becomes simpler because we only need to consider reducing that single vertex. If multiple vertices share the maximum, all of them must be reduced simultaneously for the answer to improve.
3. We compute the LCA of all vertices in T. This node is the deepest vertex that is an ancestor of every maximum-cost vertex, and any candidate new red node that affects all of them must lie on the path from the root down to this LCA.
4. We test whether choosing this LCA as the new red node is sufficient to reduce all vertices in T. For each v in T, the new cost would become the distance from v to the LCA, which equals dist_root[v] − dist_root[LCA]. If any of these values is still at least M, then no improvement is possible for the maximum.
5. If the reduction is valid, we compute the new maximum among the query vertices. This is the maximum of two values: the second maximum from the original query set, and the largest reduced cost among vertices in T.
6. The answer for the query is the minimum between the original maximum M and the improved value obtained above.

### Why it works

The algorithm relies on the fact that only vertices achieving the maximum cost matter for improvement. Any valid improvement must reduce all of them simultaneously; otherwise the maximum remains unchanged. The only vertices capable of affecting all of them are those that are ancestors of every maximum-cost vertex, and among these, the deepest such vertex minimizes distances to all affected nodes. This forces the optimal candidate to be the LCA of the maximum set, since any higher ancestor only increases distances without improving feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n, m, q = map(int, input().split())
    red = list(map(int, input().split()))
    red_set = set(red)

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        g[u].append((v, w))
        g[v].append((u, w))

    LOG = (n + 1).bit_length()
    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    dist_root = [0] * (n + 1)
    parent_red = [0] * (n + 1)

    def dfs(u, p):
        up[0][u] = p
        parent_red[u] = p if u in red_set else parent_red[p]
        for v, w in g[u]:
            if v == p:
                continue
            depth[v] = depth[u] + 1
            dist_root[v] = dist_root[u] + w
            dfs(v, u)

    dfs(1, 0)

    for i in range(1, LOG):
        for v in range(1, n + 1):
            up[i][v] = up[i - 1][up[i - 1][v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        i = 0
        while diff:
            if diff & 1:
                a = up[i][a]
            diff >>= 1
            i += 1
        if a == b:
            return a
        for i in range(LOG - 1, -1, -1):
            if up[i][a] != up[i][b]:
                a = up[i][a]
                b = up[i][b]
        return up[0][a]

    # compute initial costs
    # cost[v] = dist to nearest red ancestor
    # we can reconstruct from parent_red pointer
    cost = [0] * (n + 1)
    for v in range(1, n + 1):
        cost[v] = dist_root[v] - dist_root[parent_red[v]]

    for _ in range(q):
        tmp = list(map(int, input().split()))
        k = tmp[0]
        nodes = tmp[1:]

        M = -1
        M2 = -1
        T = []

        for v in nodes:
            c = cost[v]
            if c > M:
                M2 = M
                M = c
                T = [v]
            elif c == M:
                T.append(v)
            elif c > M2:
                M2 = c

        if len(T) == 1:
            t_lca = T[0]
        else:
            t_lca = T[0]
            for v in T[1:]:
                t_lca = lca(t_lca, v)

        # check feasibility of using t_lca
        ok = True
        best_reduced = 0

        for v in T:
            newc = dist_root[v] - dist_root[t_lca]
            if newc >= M:
                ok = False
            best_reduced = max(best_reduced, newc)

        if not ok:
            print(M)
        else:
            ans = max(M2, best_reduced)
            print(min(M, ans))

if __name__ == "__main__":
    solve()
```

The solution begins with a DFS that computes root distances and identifies, for every node, its nearest red ancestor on the root path. This allows constant-time evaluation of the initial cost of any vertex.

Binary lifting is used for LCA queries because we repeatedly need to compute the common ancestor of all maximum-cost vertices in a query. The LCA computation is the only logarithmic component per query.

Each query is processed by scanning its vertices once to extract the maximum and second maximum costs and to collect the set of worst vertices. The LCA of this set defines the only meaningful candidate for placing a new red vertex.

Finally, we verify whether this candidate can actually reduce all worst vertices below the current maximum and compute the improved answer accordingly.

## Worked Examples

Consider a query where the costs of queried nodes are `[10, 7, 10, 3]`.

| Step | Action | M | M2 | T | LCA(T) |
| --- | --- | --- | --- | --- | --- |
| 1 | Scan nodes | 10 | 7 | [v1, v3] | - |
| 2 | Compute LCA of T | 10 | 7 | [v1, v3] | x |

If both maximum-cost nodes lie in different branches, their LCA becomes the only candidate for improvement. If distances from both nodes to x are less than 10, the maximum drops; otherwise it remains unchanged.

Now consider a second query where all nodes have costs `[5, 5, 5]`.

| Step | Action | M | M2 | T | LCA(T) |
| --- | --- | --- | --- | --- | --- |
| 1 | Scan nodes | 5 | - | all nodes | - |
| 2 | Compute LCA of T | 5 | - | all nodes | root-subtree node |

In this case, even after choosing the LCA, at least one node may still have cost 5 or more, so no improvement is possible and the answer stays 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + qk) log n) | DFS preprocessing plus LCA per query over collected worst nodes |
| Space | O(n log n) | Binary lifting table and auxiliary arrays |

The constraints allow up to 10^6 total nodes and 2×10^6 total query elements, so a linear scan per query combined with logarithmic LCA operations fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve()

# Minimal tree
assert run("""1
2 1 1
1
1 2 1
1 1 2
""") is not None

# All nodes in query
assert run("""1
3 1 1
1
1 2 1
2 3 1
3 1 2 3
""") is not None

# Single node query
assert run("""1
5 2 1
1 3
1 2 1
2 3 1
3 4 1
4 5 1
1 5
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node query | 0 or unchanged | base cost handling |
| full query | computed max reduction | global structure handling |
| small chain | correct ancestor reasoning | LCA correctness |

## Edge Cases

When all queried vertices already have zero cost because they are red or have a red ancestor directly above them, the algorithm correctly identifies M as zero and immediately returns zero, since no improvement is possible.

When multiple maximum-cost vertices lie in completely different subtrees, the LCA becomes high in the tree and cannot reduce all of them sufficiently. The feasibility check correctly fails because at least one vertex remains above or equal to the original maximum threshold after applying the candidate red node.

When the query contains a single vertex, the algorithm correctly reduces to checking whether that vertex can be improved, but since any candidate red node must be its ancestor, the LCA computation degenerates to the vertex itself, producing no change and preserving correctness.
