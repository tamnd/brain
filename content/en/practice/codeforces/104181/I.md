---
title: "CF 104181I - A Rainy Delivery"
description: "We are given a directed graph where each node represents a friend’s house and each directed edge represents a one-way road. You are allowed to choose any starting house, then repeatedly travel along directed roads, possibly revisiting houses and roads multiple times."
date: "2026-07-02T00:39:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104181
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 02-10-23 Div. 1 (Advanced)"
rating: 0
weight: 104181
solve_time_s: 66
verified: true
draft: false
---

[CF 104181I - A Rainy Delivery](https://codeforces.com/problemset/problem/104181/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each node represents a friend’s house and each directed edge represents a one-way road. You are allowed to choose any starting house, then repeatedly travel along directed roads, possibly revisiting houses and roads multiple times.

The goal is to maximize how many distinct houses you can visit along such a walk. Since revisits are allowed but only unique houses count, the problem reduces to finding a starting node and a directed walk that covers as many distinct reachable nodes as possible.

A key observation is that once you enter a directed cycle, you can stay within that cycle and traverse it indefinitely, which means all nodes in that cycle become mutually reachable. From any node, all nodes reachable through directed paths are effectively part of the same reachable closure, but cycles compress this structure.

The constraints are small in terms of nodes, up to 1000, and edges are sparse with at most 2N edges. This strongly suggests that an O(N^2) or O(NM) approach is acceptable, while anything like enumerating all paths or subsets of nodes is not.

A naive interpretation would be to try every starting node and perform a DFS/BFS counting reachable nodes. That already gives a correct answer in many cases, but it misses an important subtlety: because cycles allow revisiting, and because reachability is transitive through strongly connected components, the real structure is a DAG of SCCs. The answer depends on longest reachability in that condensation graph, not just local BFS counts if SCC structure is not considered carefully.

A common mistake is to treat the graph as if simple reachability from each node is independent, but in cyclic graphs, naive reachability double counts or fails to exploit that entire SCCs behave as single units.

Edge cases include:

A single directed cycle such as 1 → 2 → 3 → 1. Any start should give answer 3, not 1 or 2.

A chain such as 1 → 2 → 3. Starting at 1 yields 3, but starting at 3 yields only 1. The answer is 3.

A graph with branching and merging paths, where multiple SCC paths converge, can make naive greedy traversal undercount or overcount if SCC compression is ignored.

## Approaches

The brute-force idea is straightforward: for each node, run a BFS or DFS and count how many nodes are reachable. The answer is the maximum over all starting nodes. This is correct because every valid walk stays within the reachable set of its start, and revisiting does not increase the set beyond reachability.

However, this approach assumes that reachability is independent of path reuse structure. In dense graphs or graphs with many overlapping paths, this still works but becomes inefficient if we try to repeatedly recompute reachability in naive ways with extra state. The worst case is O(N(N + M)), which is about 10^6 operations here, still borderline but acceptable.

The deeper issue is understanding that SCCs form the real atomic units. Inside a strongly connected component, all nodes are mutually reachable, so any node inside can reach the entire component. Once SCCs are built, the graph becomes a DAG. The task reduces to finding the maximum number of nodes reachable from any SCC in this DAG, which becomes a longest path over DAG nodes weighted by component sizes.

This observation reduces redundant exploration and gives a clean dynamic programming structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS/BFS from each node | O(N(N+M)) | O(N+M) | Too slow in worst case |
| SCC condensation + DP on DAG | O(N+M) | O(N+M) | Accepted |

## Algorithm Walkthrough

## 1. Compute strongly connected components

We first decompose the graph into SCCs using Kosaraju or Tarjan. The reason is that inside an SCC, every node is mutually reachable, so they behave as a single unit in terms of collecting friends.

## 2. Build the condensed graph

We compress each SCC into a single node. For every edge u → v in the original graph, if u and v belong to different SCCs, we add a directed edge between their components. This produces a DAG because SCC condensation removes cycles.

## 3. Assign weights to components

Each SCC node gets a weight equal to the number of original nodes inside it. This reflects how many friends we automatically collect if we enter that component.

## 4. Compute reachability DP on DAG

We compute the maximum sum of weights reachable from each component. Since the graph is a DAG, we can process nodes in topological order or use memoized DFS. For each component, its value is its own weight plus the best among all outgoing neighbors.

## 5. Take the best starting point

We try every component as a starting point and take the maximum DP value.

### Why it works

The key invariant is that SCC compression preserves reachability in a one-to-one way: any path in the original graph corresponds to a path in the SCC DAG, and any walk inside an SCC does not increase the set of reachable components beyond that SCC. Therefore, maximizing visited distinct nodes is equivalent to choosing a starting SCC and maximizing total weight over reachable nodes in a DAG. Since DAG paths do not form cycles, DP correctly accumulates optimal reachable sums without double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    gr = [[] for _ in range(n)]
    
    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        gr[b].append(a)

    # Kosaraju: first pass order
    vis = [False] * n
    order = []

    def dfs1(u):
        vis[u] = True
        for v in g[u]:
            if not vis[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not vis[i]:
            dfs1(i)

    # second pass assign components
    comp = [-1] * n
    comps = []

    def dfs2(u, cid):
        comp[u] = cid
        comps[cid].append(u)
        for v in gr[u]:
            if comp[v] == -1:
                dfs2(v, cid)

    for u in reversed(order):
        if comp[u] == -1:
            comps.append([])
            dfs2(u, len(comps) - 1)

    k = len(comps)

    # build condensed graph
    dag = [set() for _ in range(k)]
    weight = [0] * k

    for cid in range(k):
        weight[cid] = len(comps[cid])
        for u in comps[cid]:
            for v in g[u]:
                if comp[v] != cid:
                    dag[cid].add(comp[v])

    dag = [list(s) for s in dag]

    # DP on DAG
    dp = [-1] * k
    vis_dp = [False] * k

    def dfs(u):
        if vis_dp[u]:
            return dp[u]
        vis_dp[u] = True
        best = 0
        for v in dag[u]:
            best = max(best, dfs(v))
        dp[u] = weight[u] + best
        return dp[u]

    ans = 0
    for i in range(k):
        ans = max(ans, dfs(i))

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by building both the original graph and its reverse, which is required for Kosaraju’s algorithm. The first DFS computes a finishing order, ensuring that nodes are processed in a way that respects exit structure of the graph.

The second DFS assigns component IDs on the reversed graph, grouping mutually reachable nodes. Each component is stored explicitly so we can compute its size and outgoing edges.

The condensation step uses a set per component to avoid duplicate edges, which matters because multiple original edges can collapse into the same SCC transition. The DP step then computes the best reachable sum from each SCC using memoized DFS.

A subtle detail is recursion depth; Python requires increasing recursion limit due to depth up to 1000 nodes, and possibly deeper DFS chains.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
2 3
```

Here all nodes form a simple chain with no cycles.

| Step | SCC assignment | Condensed graph | DP value |
| --- | --- | --- | --- |
| 1 | {1}, {2}, {3} | 1→2→3 | computed bottom-up |
| 2 | each node size 1 | same chain | dp[3]=1 |
| 3 |  |  | dp[2]=2 |
| 4 |  |  | dp[1]=3 |

This shows that reachability accumulates linearly along the chain.

### Example 2

Input:

```
3 1
1 2
```

| Step | SCC assignment | Condensed graph | DP value |
| --- | --- | --- | --- |
| 1 | {1}, {2}, {3} | 1→2 | dp[2]=1 |
| 2 |  |  | dp[1]=2 |
| 3 |  |  | node 3 isolated = 1 |

The best starting point is node 1 giving 2.

These examples confirm that DP correctly aggregates reachable components.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Kosaraju runs in linear time, SCC DAG construction and DP are also linear |
| Space | O(N + M) | adjacency lists, component storage, and DP arrays |

The constraints allow up to about 2000 edges, so linear graph processing is easily fast enough within 5 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, sys.stdin.readline().split())
    g = [[] for _ in range(n)]
    gr = [[] for _ in range(n)]
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        a -= 1
        b -= 1
        g[a].append(b)
        gr[b].append(a)

    sys.setrecursionlimit(10**7)

    vis = [False] * n
    order = []

    def dfs1(u):
        vis[u] = True
        for v in g[u]:
            if not vis[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not vis[i]:
            dfs1(i)

    comp = [-1] * n
    comps = []

    def dfs2(u, cid):
        comp[u] = cid
        comps[cid].append(u)
        for v in gr[u]:
            if comp[v] == -1:
                dfs2(v, cid)

    for u in reversed(order):
        if comp[u] == -1:
            comps.append([])
            dfs2(u, len(comps) - 1)

    k = len(comps)
    dag = [set() for _ in range(k)]
    weight = [len(c) for c in comps]

    for cid in range(k):
        for u in comps[cid]:
            for v in g[u]:
                if comp[v] != cid:
                    dag[cid].add(comp[v])

    dag = [list(s) for s in dag]

    from functools import lru_cache

    @lru_cache(None)
    def dfs(u):
        best = 0
        for v in dag[u]:
            best = max(best, dfs(v))
        return weight[u] + best

    ans = 0
    for i in range(k):
        ans = max(ans, dfs(i))
    return str(ans) + "\n"

# provided samples
assert run("3 2\n1 2\n2 3\n") == "3\n", "sample 1"
assert run("3 1\n1 2\n") == "2\n", "sample 2"
assert run("5 5\n3 5\n3 2\n2 3\n4 5\n5 1\n") == "4\n", "sample 3"

# custom cases
assert run("1 0\n") == "1\n", "single node"
assert run("3 3\n1 2\n2 3\n3 1\n") == "3\n", "single cycle"
assert run("4 3\n1 2\n2 3\n3 4\n") == "4\n", "chain"
assert run("4 2\n1 2\n3 4\n") == "2\n", "disconnected components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | minimal graph handling |
| single cycle | 3 | SCC collapsing correctness |
| chain | 4 | linear reachability accumulation |
| disconnected components | 2 | independent subgraphs handled correctly |

## Edge Cases

A single strongly connected cycle such as `1 → 2 → 3 → 1` is handled by grouping all nodes into one SCC. During condensation, this becomes a single node of weight 3 with no outgoing edges, and DP immediately returns 3 regardless of starting point.

A purely linear graph like `1 → 2 → 3 → 4` produces four SCCs of size 1 each. The DAG becomes a chain, and DP correctly accumulates from the end backward, ensuring the maximum starting node is the head of the chain, yielding 4.

A disconnected graph such as `1 → 2` and `3 → 4` results in two independent DAG components. Since DP is evaluated over all SCC roots, the maximum correctly picks the larger reachable segment, which is 2 in this case.
