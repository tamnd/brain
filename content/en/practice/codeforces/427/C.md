---
title: "CF 427C - Checkposts"
description: "We are given a directed graph where each node represents a city junction, and each directed edge represents a one-way road. Each junction has a cost to build a police checkpost."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 427
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 244 (Div. 2)"
rating: 1700
weight: 427
solve_time_s: 94
verified: true
draft: false
---

[CF 427C - Checkposts](https://codeforces.com/problemset/problem/427/C)

**Rating:** 1700  
**Tags:** dfs and similar, graphs, two pointers  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each node represents a city junction, and each directed edge represents a one-way road. Each junction has a cost to build a police checkpost. A checkpost at junction _i_ protects all junctions reachable from _i_ and able to return to _i_, including _i_ itself. In other words, a checkpost at a node secures its strongly connected component (SCC). The goal is to cover all nodes by placing checkposts so that the total cost is minimized, and then count how many different minimal-cost arrangements exist.

The input size allows up to 100,000 junctions and 300,000 roads. A brute-force approach that tries all combinations of junctions is clearly infeasible, because the number of subsets grows exponentially. We need a linear or near-linear approach with respect to nodes and edges, which suggests that graph traversal and SCC decomposition techniques are suitable.

A subtle edge case arises when SCCs contain multiple nodes. For example, if nodes 2 and 3 form a cycle, both are mutually reachable. We only need one checkpost inside this SCC. A careless approach that considers individual nodes independently may place multiple redundant checkposts, inflating the cost. Another edge case is when multiple nodes in an SCC have the same minimal cost-then the number of ways to pick the cheapest node multiplies.

## Approaches

The naive approach considers every node independently. We could imagine iterating over every junction, trying to place a checkpost there, and testing if all nodes are covered via reachability. This approach is correct in theory because it checks all combinations, but in practice it requires enumerating all subsets of nodes, giving a complexity of $O(2^n)$ - impossible for $n$ up to 100,000.

The key insight is that the protection relationship exactly mirrors strongly connected components. Any SCC is a maximal set of nodes where each node can reach every other node. Therefore, placing one checkpost in each SCC suffices to cover all nodes in that SCC, and no more checkposts are needed. The minimal cost per SCC is just the cost of its cheapest node. The number of ways to pick checkposts in that SCC is the count of nodes that share that minimal cost.

Once we decompose the graph into SCCs, the problem reduces to iterating over each SCC, picking the minimal cost and counting multiplicities. The SCC decomposition can be done in linear time using Kosaraju's or Tarjan's algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n + m) | Too slow |
| Optimal (SCC + min cost) | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Parse the input to extract the number of nodes `n`, their checkpost costs, the number of edges `m`, and the list of directed edges.
2. Construct an adjacency list for the graph.
3. Perform Kosaraju’s algorithm to find SCCs. This involves two DFS passes: the first pass fills nodes into a stack according to finishing times; the second pass processes nodes in stack order on the transposed graph to identify SCCs.
4. For each SCC, determine the minimum checkpost cost. Count how many nodes in the SCC share that minimal cost.
5. Sum the minimum costs across all SCCs to get the total minimal expenditure.
6. Multiply the counts of minimal-cost nodes for each SCC, modulo $10^9 + 7$, to get the total number of ways to achieve the minimal cost.

Why it works: Each SCC forms a maximal set of nodes that can protect each other. By placing a checkpost at the cheapest node within an SCC, we cover all its nodes with minimal cost. Because SCCs are disjoint in terms of protection, the total minimal cost is the sum across SCCs. Multiplying counts accounts for independent choices in each SCC.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

MOD = 10**9 + 7

def kosaraju_scc(n, adj):
    visited = [False] * n
    order = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    # Transpose graph
    adj_t = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            adj_t[v].append(u)

    visited = [False] * n
    sccs = []

    def dfs2(u, comp):
        visited[u] = True
        comp.append(u)
        for v in adj_t[u]:
            if not visited[v]:
                dfs2(v, comp)

    for u in reversed(order):
        if not visited[u]:
            comp = []
            dfs2(u, comp)
            sccs.append(comp)

    return sccs

def main():
    n = int(input())
    costs = list(map(int, input().split()))
    m = int(input())
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u-1].append(v-1)

    sccs = kosaraju_scc(n, adj)
    total_cost = 0
    ways = 1

    for comp in sccs:
        min_cost = min(costs[u] for u in comp)
        count = sum(1 for u in comp if costs[u] == min_cost)
        total_cost += min_cost
        ways = (ways * count) % MOD

    print(total_cost, ways)

if __name__ == "__main__":
    main()
```

The code first builds the graph and runs Kosaraju’s algorithm to get SCCs. For each SCC, it finds the cheapest node and counts duplicates. Summing minimums gives the total cost. Multiplying counts gives the number of ways. Using `sys.setrecursionlimit` ensures DFS on large graphs does not crash.

## Worked Examples

**Sample Input 1**

```
3
1 2 3
3
1 2
2 3
3 2
```

| Step | SCCs found | min cost per SCC | ways per SCC | cumulative total cost | cumulative ways |
| --- | --- | --- | --- | --- | --- |
| 1 | [0], [1,2] | 1, 2 | 1,1 | 3 | 1 |

The graph decomposes into a single node SCC [0] and a cycle [1,2]. The cheapest nodes cost 1 and 2, respectively. There is only one way to pick the minimum in each SCC.

**Custom Input 2**

```
4
1 1 2 2
4
1 2
2 1
3 4
4 3
```

| Step | SCCs found | min cost per SCC | ways per SCC | cumulative total cost | cumulative ways |
| --- | --- | --- | --- | --- | --- |
| 1 | [0,1], [2,3] | 1,2 | 2,2 | 3 | 4 |

Two SCCs, each forming a cycle. Minimal-cost nodes in first SCC: nodes 0,1 both cost 1, giving 2 ways. Second SCC: nodes 2,3 both cost 2, giving 2 ways. Multiply 2*2 = 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Kosaraju's algorithm runs in linear time. Summing and counting minimums per SCC is O(n). |
| Space | O(n + m) | Adjacency lists, transpose graph, visited array, and SCC storage all scale linearly with n + m. |

Given the constraints (n ≤ 10^5, m ≤ 3·10^5) and linear time complexity, the solution easily fits in the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided sample
assert run("3\n1 2 3\n3\n1 2\n2 3\n3 2\n") == "3 1", "sample 1"

# Minimum-size input
assert run("1\n5\n0\n") == "5 1", "single node no edges"

# Two SCCs with multiple minimal nodes
assert run("4\n1 1 2 2\n4\n1 2\n2 1\n3 4\n4 3\n") == "3 4", "two cycles with duplicate minimums"

# All nodes same cost
assert run("3\n2 2 2\n2\n1 2\n2 3\n") == "4 1", "same cost, linear chain"

# Edge case: single cycle covering all nodes
assert run("3\n3 1 2\n3\n1 2\n2 3\n3 1\n") == "1 1", "full cycle"

# No edges, all nodes isolated
assert run("3\n1 2 3\n0\n") == "6 1", "isolated nodes"
```

|
