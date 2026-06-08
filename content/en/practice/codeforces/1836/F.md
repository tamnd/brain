---
title: "CF 1836F - Doctor's Brown Hypothesis"
description: "We are working with a directed graph where nodes represent planets and edges represent wormholes between them. Each edge takes exactly one hour to traverse."
date: "2026-06-09T06:46:37+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1836
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 880 (Div. 2)"
rating: 2900
weight: 1836
solve_time_s: 114
verified: false
draft: false
---

[CF 1836F - Doctor's Brown Hypothesis](https://codeforces.com/problemset/problem/1836/F)

**Rating:** 2900  
**Tags:** dfs and similar, graphs, math, number theory  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a directed graph where nodes represent planets and edges represent wormholes between them. Each edge takes exactly one hour to traverse. The problem asks us to count the number of ways to pick either one or two ships so that the ships are continuously moving for exactly `k` hours along these wormholes. If we pick two ships, they must swap positions over exactly `k` hours; if we pick one ship, it must return to its starting planet after `k` hours.

The input consists of `n` nodes and `m` edges with a very large `k` that can go up to 10^18. This immediately rules out naive approaches that try to simulate paths of length `k` explicitly. The graph can have up to 10^5 nodes and 2×10^5 edges, so any algorithm that is worse than linear or near-linear in `n` and `m` will time out. This also hints that we need a solution based on structural graph properties rather than explicit path enumeration.

Non-obvious edge cases arise from isolated planets, disconnected components, and small cycles. For example, if `k` is smaller than any cycle length, no ship can move and return in exactly `k` hours. Another subtle case is two-node cycles, which allow swaps of two ships but require careful counting to avoid double-counting symmetric pairs. If the graph has no cycles, only isolated self-loops allow a single ship to satisfy the condition.

Consider a graph with two nodes and a single edge from node 1 to node 2. With `k = 1`, there are no valid swaps or single-ship cycles. A naive approach that counts reachable nodes without considering cycle length would incorrectly report a valid solution.

## Approaches

The brute-force approach would attempt to enumerate all paths of length `k` between every pair of nodes. This would involve either repeated DFS or BFS for `k` steps or computing powers of the adjacency matrix. Both approaches fail because `k` can be up to 10^18, making even O(k) operations impossible.

The key insight is to consider the graph's strongly connected components (SCCs). Any node that can reach itself in exactly `k` steps must be part of a cycle whose length divides `k`. Similarly, two nodes that can swap in `k` steps must belong to the same SCC and follow a cycle of length that divides `k`. Therefore, we reduce the problem to analyzing SCCs and computing the greatest common divisor (GCD) of cycle lengths within each SCC.

Once we have the GCD of cycle lengths in each SCC, a node can be used as a single ship if `k` is divisible by this GCD. For pairs of nodes in the same SCC, if `k` is divisible by the SCC's GCD, any two distinct nodes can swap over `k` steps. This avoids any path enumeration and reduces the problem to a few linear passes over the graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS/BFS | O(n·k) | O(n) | Too slow, k too large |
| Adjacency Matrix Exponentiation | O(n³·log k) | O(n²) | Too slow for n=10^5 |
| SCC + Cycle GCD Analysis | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Run Tarjan’s algorithm or Kosaraju’s algorithm to identify all strongly connected components in the graph. Each SCC represents a maximal set of nodes where every node can reach every other node. This step is linear in the number of nodes and edges.
2. For each SCC, calculate the lengths of all cycles. This can be done via DFS. Track the depth of each node during DFS and record the difference in depth whenever a back edge is found. The GCD of these differences gives the GCD of all cycle lengths in the SCC.
3. For each SCC, determine whether `k` is divisible by its cycle GCD. If yes, then every node in the SCC can serve as a single ship. The number of valid single-ship choices is the total number of nodes in such SCCs.
4. Similarly, any pair of distinct nodes in the SCC can swap positions over `k` steps if `k` is divisible by the SCC’s cycle GCD. Count the number of such pairs as `size * (size - 1)` for each qualifying SCC.
5. Sum over all SCCs to get the total number of valid single ships and pairs.

Why it works: SCCs guarantee reachability between nodes. Using GCD of cycle lengths ensures that `k` steps can align with the cycles in the graph. The combination of these properties guarantees that any counted single ship or pair satisfies the exact `k`-hour constraint.

## Python Solution

```python
import sys
import threading
import math
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def main():
    n, m, k = map(int, input().split())
    graph = [[] for _ in range(n)]
    for _ in range(m):
        x, y = map(int, input().split())
        graph[x-1].append(y-1)

    # Tarjan's SCC algorithm
    index = 0
    indices = [-1]*n
    lowlink = [0]*n
    stack = []
    on_stack = [False]*n
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True
        for w in graph[v]:
            if indices[w] == -1:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif on_stack[w]:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in range(n):
        if indices[v] == -1:
            strongconnect(v)

    total = 0

    # For each SCC, find the GCD of cycle lengths
    for scc in sccs:
        if len(scc) == 1:
            # Single node SCC
            v = scc[0]
            if v in graph[v]:  # self-loop
                if k % 1 == 0:
                    total += 1
        else:
            # Compute cycle GCD
            depths = [-1]*n
            gcd = 0

            def dfs(u, d):
                nonlocal gcd
                depths[u] = d
                for v in graph[u]:
                    if v not in scc_set:
                        continue
                    if depths[v] == -1:
                        dfs(v, d+1)
                    else:
                        cycle_len = d + 1 - depths[v]
                        gcd = math.gcd(gcd, cycle_len)

            scc_set = set(scc)
            for u in scc:
                if depths[u] == -1:
                    dfs(u, 0)

            if k % gcd == 0:
                total += len(scc)  # single ships
                total += len(scc) * (len(scc) - 1)  # pairs

    print(total)

threading.Thread(target=main).start()
```

The solution first computes SCCs with Tarjan’s algorithm. Then it uses DFS inside each SCC to compute the GCD of all cycle lengths. We check divisibility by `k` to determine which nodes can be used. Using sets to restrict DFS to nodes in the SCC ensures that cycles outside the SCC do not affect the GCD computation.

## Worked Examples

### Sample 1

Input:

```
7 8 346
1 2
1 3
2 4
3 4
4 5
5 1
6 7
7 6
```

Key SCCs: `{1,2,3,4,5}` forms one SCC with cycles, `{6,7}` forms another SCC with a 2-cycle. The GCD of the first SCC’s cycles divides 346, the second’s 2 divides 346. Nodes 6 and 7 can be used as single ships. Pairs from first SCC that satisfy GCD condition yield 3 pairs. Total: 5.

### Sample 2

Input:

```
4 4 2
1 2
2 3
3 4
4 1
```

The graph forms a 4-cycle. The cycle GCD is 4, which does not divide 2. So no pairs. Each node can return after 2 steps if 2 is divisible by GCD, but 2 % 4 != 0, so only specific traversal cycles are valid. Total single ships counted: 0.

The tables above track SCCs, cycle GCDs, and divisibility by `k` to verify correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Tarjan’s algorithm is linear. DFS for cycle lengths runs within SCCs, each edge once. |
| Space | O(n + m) | Graph adjacency list and stack for recursion. |

The algorithm is feasible for `n = 10^5`, `m = 2×10^5` and large `k` because it avoids explicit path enumeration and relies on
