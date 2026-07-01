---
title: "CF 104180I - A Rainy Delivery"
description: "We are given a directed graph where each vertex represents a friend’s house and each directed edge represents a one-way road between two houses."
date: "2026-07-02T00:45:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104180
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 02-10-23 Div. 2 (Beginner)"
rating: 0
weight: 104180
solve_time_s: 57
verified: true
draft: false
---

[CF 104180I - A Rainy Delivery](https://codeforces.com/problemset/problem/104180/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each vertex represents a friend’s house and each directed edge represents a one-way road between two houses. We may start at any vertex we like, and once we start, we can follow directed edges arbitrarily, revisiting vertices and edges multiple times. Our goal is to maximize the number of distinct vertices we can visit in a single traversal.

In graph terms, we are looking for a starting node and a reachable set under directed movement, where revisits are allowed but do not increase the count. The answer is the size of the largest set of vertices that can be reached from some starting vertex following directed edges.

The constraints are tight enough to shape the approach. With $N \le 1000$ and $M \le 2N$, the graph is sparse, so algorithms with $O(N^2)$ or $O(NM)$ are acceptable, but anything cubic over all pairs or exponential exploration is not viable. A full pairwise reachability computation over all nodes using naive BFS or DFS from each node is already near the limit but still plausible. However, we need to be careful about repeated recomputation if we do not reuse structure.

A key subtlety is that revisiting nodes is allowed, so the structure is not a simple path problem. Instead, cycles become beneficial because they allow revisiting without constraint, meaning strongly connected components behave like single "free travel zones".

Edge cases that matter:

A simple chain already demonstrates that reachability is directional and asymmetric. For example:

Input:

```
3 2
1 2
2 3
```

From node 1, we can reach 1, 2, 3, so answer is 3. A naive approach starting from node 3 would only see itself, so failing to try all starts misses the global maximum.

A cycle is another critical case:

```
3 3
1 2
2 3
3 1
```

From any node, all nodes are reachable, and revisiting is allowed, so the whole component is fully usable.

A final subtle case is when components feed into each other asymmetrically. A node might reach a large chain but cannot be reached back, so the best starting point is not obvious without exploring all nodes or compressing structure.

## Approaches

The brute-force idea is straightforward: for every starting node, run a DFS or BFS following directed edges and count how many distinct nodes can be reached. The final answer is the maximum over all starts.

This is correct because every valid route begins at some node, and BFS/DFS enumerates exactly the set of nodes reachable from that start. However, this repeats work heavily. Each traversal costs $O(N + M)$, and doing it for all $N$ nodes yields $O(N(N+M))$, which in the worst case is about $10^6$ operations per run, still borderline but acceptable in Python only with careful implementation. However, this ignores the deeper structure: many nodes share the same reachability patterns inside strongly connected regions.

The key observation is that strongly connected components (SCCs) collapse cycles into single units. Inside an SCC, every node can reach every other, so starting anywhere in the SCC yields the same reachable "macro behavior". After collapsing SCCs, we get a directed acyclic graph (DAG). On this DAG, the problem becomes: from which component can we reach the largest number of components?

Since $M \le 2N$, the graph is sparse, and SCC decomposition with Kosaraju or Tarjan runs in linear time. After compression, we compute a DP over the DAG in topological order, where each component’s value is its size plus the sum of best reachable components downstream.

This reduces repeated exploration into a single traversal per edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS from every node | O(N(N+M)) | O(N+M) | Too slow |
| SCC + DAG DP | O(N+M) | O(N+M) | Accepted |

## Algorithm Walkthrough

1. Build the directed graph from the input edges. This structure will be used both for forward traversal and SCC processing.
2. Run a DFS-based algorithm to compute strongly connected components. We first perform a DFS to obtain finishing order, then reverse the graph and process nodes in reverse finishing order to assign component IDs. The purpose is to group nodes that are mutually reachable into single units.
3. For each SCC, compute its size. This represents how many original nodes are “freely interchangeable” in that component.
4. Build a condensed graph where each SCC is a node. For every original edge $u \to v$, if $comp[u] \ne comp[v]$, add a directed edge from $comp[u]$ to $comp[v]$. This produces a DAG because SCC contraction removes cycles.
5. Compute the best reachable size from each SCC using dynamic programming on the DAG. We process components in reverse topological order derived from SCC finishing order. For each component, its value is its own size plus the maximum over all outgoing neighbors.
6. The answer is the maximum DP value across all SCCs, since we are allowed to start from any node.

The reason this ordering works is that once SCCs are formed, dependencies only go forward in the DAG, so when computing a component’s best reachability, all downstream results are already known.

### Why it works

After compression, every valid walk corresponds to a path in the SCC DAG. Because the DAG has no cycles, any path cannot revisit components, so reachability becomes additive along directed edges. Each SCC contributes its full size exactly once because within a component all nodes are mutually reachable. Therefore, maximizing reachable nodes reduces to finding the maximum path sum in a DAG where node weights are SCC sizes.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        rg[b].append(a)

    visited = [False] * n
    order = []

    def dfs1(u):
        visited[u] = True
        for v in g[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    comp = [-1] * n
    cid = 0

    def dfs2(u):
        comp[u] = cid
        for v in rg[u]:
            if comp[v] == -1:
                dfs2(v)

    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u)
            cid += 1

    comp_size = [0] * cid
    for i in range(n):
        comp_size[comp[i]] += 1

    dag = [[] for _ in range(cid)]
    for u in range(n):
        for v in g[u]:
            cu, cv = comp[u], comp[v]
            if cu != cv:
                dag[cu].append(cv)

    dp = [-1] * cid

    def dfs_dp(u):
        if dp[u] != -1:
            return dp[u]
        best = 0
        for v in dag[u]:
            best = max(best, dfs_dp(v))
        dp[u] = comp_size[u] + best
        return dp[u]

    ans = 0
    for i in range(cid):
        ans = max(ans, dfs_dp(i))

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by constructing both the forward and reversed adjacency lists, since Kosaraju’s algorithm requires traversals in both directions. The first DFS computes a finishing order, and the second DFS on the reversed graph assigns component identifiers.

After SCC labeling, we accumulate sizes of components by counting how many original nodes belong to each component. This is essential because each SCC contributes that many distinct friends.

The DAG construction step is careful to only add edges between different components. Without this filter, self-loops would introduce redundant transitions and potentially complicate DP.

The final DP computes the longest weighted path in the condensed DAG. Memoization ensures each component is solved once.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
2 3
```

SCC decomposition yields three components: {1}, {2}, {3}. The DAG is 1 → 2 → 3.

| Step | Node | DP result |
| --- | --- | --- |
| dfs_dp(3) | 3 | 1 |
| dfs_dp(2) | 2 | 2 (2 + 1) |
| dfs_dp(1) | 1 | 3 (1 + 2) |

The final answer is 3, which matches the ability to traverse the entire chain starting from node 1.

This confirms that the DP correctly accumulates reachable nodes along a linear DAG.

### Example 2

Input:

```
3 1
1 2
```

SCCs are {1}, {2}, {3}. The DAG has a single edge 1 → 2.

| Step | Node | DP result |
| --- | --- | --- |
| dfs_dp(3) | 3 | 1 |
| dfs_dp(2) | 2 | 1 |
| dfs_dp(1) | 1 | 2 |

Answer is 2.

This shows that unreachable nodes do not get counted, and starting from node 1 is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Two DFS passes for SCC plus one pass for DP over condensed graph |
| Space | O(N + M) | Adjacency lists, component arrays, and recursion stacks |

The constraints $N \le 1000$, $M \le 2N$ are easily satisfied since the solution is linear. Even Python recursion overhead remains safe due to small graph size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import ModuleType

    # assuming solution is defined above in same file
    # we re-run solve() indirectly by re-executing script logic is not needed here
    # so we redefine a minimal wrapper

    # For testing purposes, we assume solve() is accessible
    solve()
    return ""

# provided samples
assert run("3 2\n1 2\n2 3\n") == "3", "sample 1"
assert run("3 1\n1 2\n") == "2", "sample 2"

# custom cases
assert run("1 0\n") == "1", "single node"
assert run("2 2\n1 2\n2 1\n") == "2", "cycle"
assert run("4 3\n1 2\n2 3\n4 3\n") == "3", "merge into chain"
assert run("5 0\n") == "1", "isolated nodes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 | minimum graph |
| 2-cycle | 2 | SCC merging correctness |
| chain + merge | 3 | DAG propagation |
| no edges | 1 | isolated nodes behavior |

## Edge Cases

A single-node graph like `1 0` produces one SCC of size 1. The DP immediately returns 1 because there are no outgoing edges, so the best reachable set is just itself.

A fully bidirectional cycle such as `1 2, 2 1` collapses into one SCC of size 2. The condensed graph has a single node, so DP returns 2, correctly reflecting that revisiting inside the cycle allows access to all nodes.

A graph with disconnected chains ensures that starting point matters. For `1→2→3` and `4→5`, SCCs remain singletons, and DP from node 4 yields 2 while DP from node 1 yields 3. The final maximum correctly chooses 3, showing that global maximization over components is essential.
