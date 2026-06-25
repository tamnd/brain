---
title: "CF 106386H - Ultimate Figure Skating"
description: "We are given a directed graph with weighted nodes. Each node represents a skating element, and each element has a score. A directed edge from $x$ to $y$ means you are allowed to perform element $y$ immediately after element $x$."
date: "2026-06-25T10:15:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106386
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 2-25-26 (Advanced)"
rating: 0
weight: 106386
solve_time_s: 43
verified: true
draft: false
---

[CF 106386H - Ultimate Figure Skating](https://codeforces.com/problemset/problem/106386/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph with weighted nodes. Each node represents a skating element, and each element has a score. A directed edge from $x$ to $y$ means you are allowed to perform element $y$ immediately after element $x$. A performance is a walk over this graph where each step follows a directed edge, and the walk can start at any node.

The key twist is that repeating the same element does not add any score after its first appearance. So if we visit a node multiple times, only the first visit contributes its value; all subsequent visits contribute zero.

The task is to choose a valid walk that maximizes the sum of distinct node values encountered along the walk.

The graph can be large, with up to $10^5$ nodes and $2 \cdot 10^5$ edges. Any solution that tries to enumerate paths or perform exponential exploration over walks will immediately fail. Even $O(n^2)$ approaches are too large in the worst case because the graph can be dense enough that traversal patterns repeat heavily.

A subtle difficulty is that cycles are allowed, and in fact they are the only way to “revisit” nodes. However, revisiting a node is only useful if it helps reach new nodes that have not been collected yet. Once all reachable valuable nodes in a region are collected, continuing to loop gives no benefit.

An easy mistake is to assume this is a longest path problem or a DAG DP problem. That fails because cycles are allowed and useful. Another common mistake is to compress strongly connected components but then treat the resulting graph incorrectly, especially if one forgets that within an SCC, all nodes are mutually reachable and can be collected in any order without revisits costing anything.

For example, if we have a cycle $1 \to 2 \to 3 \to 1$, the correct behavior is that starting anywhere in this cycle allows collecting all three values. A naive path DP might count only one direction of traversal and miss that the whole component is effectively free to traverse.

## Approaches

The brute-force idea is to simulate all possible walks starting from every node, maintaining a visited set of nodes whose values have already been collected. At each step, we move along any outgoing edge and add the node’s value if it has not been seen before. This is correct because it directly matches the definition of the process.

The failure point is the state space. The visited set alone has size $2^n$, and for each state there are up to $n$ possible next moves. Even restricting to reachable states, the number of distinct paths in a graph with cycles is unbounded, since walks can loop arbitrarily many times before deciding to progress. This makes direct simulation impossible.

The key observation is that cycles inside the graph do not matter internally. Once you enter a strongly connected component, you can traverse within it freely and collect every node in that component without worrying about ordering. The only meaningful structure is how these components connect to each other.

This reduces the problem to a directed acyclic graph of strongly connected components. Inside each component, we can sum all node values, since once we enter it, we can collect everything in it. Between components, we are restricted by the condensation DAG, so we are effectively choosing a path in this DAG that maximizes the sum of component weights.

This transforms the problem into a longest path problem on a DAG, where node weights are the sums of SCC values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over walks | Exponential | Exponential | Too slow |
| SCC compression + DP on DAG | $O(n + m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

1. Compute strongly connected components of the graph. Each node is assigned a component id. This step groups nodes that are mutually reachable, which matters because inside such a group, ordering constraints no longer restrict total collection.
2. For each component, compute its total value by summing all node weights inside it. This is valid because once the walk enters the component, it can traverse internally and eventually visit all nodes.
3. Build the condensed graph where each SCC becomes a single node. For every original edge $u \to v$, if the components differ, add a directed edge between their component representatives.
4. Since SCC condensation always produces a directed acyclic graph, compute a topological order of the components.
5. Run dynamic programming over the DAG. Let $dp[c]$ be the maximum total value achievable ending at component $c$. Initialize all $dp[c]$ with the component’s own sum, since we may start anywhere.
6. Traverse components in topological order. For each edge $c \to d$, update $dp[d]$ as $dp[d] = \max(dp[d], dp[c] + value[d])$. This transition represents moving from one region of mutually reachable nodes into another and collecting all nodes in the destination component upon arrival.
7. The answer is the maximum value among all dp states.

The correctness relies on the fact that once a component is entered, all its nodes can be collected without penalty, and leaving it cannot provide any additional value except through outgoing edges. Since SCC contraction removes all internal ordering constraints, every valid walk corresponds exactly to a path in the DAG.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n, m = map(int, input().split())
    val = list(map(int, input().split()))
    
    g = [[] for _ in range(n)]
    gr = [[] for _ in range(n)]
    
    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        g[x].append(y)
        gr[y].append(x)

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

    # second pass: assign components
    comp = [-1] * n
    comps = []

    def dfs2(u, idx):
        comp[u] = idx
        comps[idx].append(u)
        for v in gr[u]:
            if comp[v] == -1:
                dfs2(v, idx)

    for u in reversed(order):
        if comp[u] == -1:
            comps.append([])
            dfs2(u, len(comps) - 1)

    k = len(comps)

    comp_sum = [0] * k
    for c in range(k):
        s = 0
        for u in comps[c]:
            s += val[u]
        comp_sum[c] = s

    dag = [set() for _ in range(k)]
    indeg = [0] * k

    for u in range(n):
        for v in g[u]:
            cu, cv = comp[u], comp[v]
            if cu != cv and cv not in dag[cu]:
                dag[cu].add(cv)
                indeg[cv] += 1

    topo = []
    stack = [i for i in range(k) if indeg[i] == 0]
    while stack:
        u = stack.pop()
        topo.append(u)
        for v in dag[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)

    dp = comp_sum[:]

    for u in topo:
        for v in dag[u]:
            if dp[v] < dp[u] + comp_sum[v]:
                dp[v] = dp[u] + comp_sum[v]

    print(max(dp))

if __name__ == "__main__":
    solve()
```

The first half of the code performs Kosaraju’s algorithm to identify strongly connected components. The forward DFS produces a finishing order, while the reverse graph DFS assigns components. This is necessary because reachability symmetry inside SCCs is what allows collapsing cycles safely.

The second half builds the condensation graph. A set is used per component to avoid duplicate edges, since multiple original edges can connect the same pair of components. Without deduplication, indegree and DP transitions would still work but would waste time and risk redundant updates.

The DP stage is a longest-path computation over a DAG, initialized with component sums because each component is self-sufficient as a starting point. The transition adds the full destination component value because entering it allows full collection.

## Worked Examples

Consider a small graph with a cycle and a tail:

Input:

```
5 5
1 10 100 1 50
1 2
2 3
3 1
3 4
4 5
```

SCC decomposition yields one component $\{1,2,3\}$ with sum 111, and singletons 4 and 5.

| Step | Component | dp before | Transition | dp after |
| --- | --- | --- | --- | --- |
| init | {1,2,3} | 111 | start | 111 |
| process | 4 | 0 | 111 + 1 | 112 |
| process | 5 | 0 | 112 + 50 | 162 |

This shows that once the cycle is entered, all its nodes are collected immediately, and only outward structure matters.

Now consider a branching graph:

Input:

```
4 3
5 1 10 2
1 2
1 3
3 4
```

Each node is its own SCC.

| Step | Node | dp before | Transition | dp after |
| --- | --- | --- | --- | --- |
| start | 1 | 5 | init | 5 |
| 1 → 2 | 2 | 1 | 5 + 1 | 6 |
| 1 → 3 | 3 | 10 | 5 + 10 | 15 |
| 3 → 4 | 4 | 2 | 15 + 2 | 17 |

The best path is 1 → 3 → 4, confirming that the DP is selecting the best route in the DAG rather than just the highest immediate node.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Kosaraju runs in linear time, SCC condensation and DP also process each edge once |
| Space | $O(n + m)$ | adjacency lists, reverse graph, SCC storage, and DP arrays |

The constraints allow up to $3 \cdot 10^5$ total graph size, so linear-time SCC decomposition and DAG DP fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    return sys.stdout.getvalue()

# NOTE: In actual use, run() should call solve() and capture output.
# Here we only illustrate structure.

# sample-style and custom tests would be placed when integrated
```

A proper harness would redirect stdout and call the solver directly; the structure above is a placeholder consistent with typical CF testing setups.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cycle graph | sum of all nodes | SCC collapsing correctness |
| DAG chain | sum along best path | DP correctness on DAG |
| multiple branches | max path selection | correct global optimum |

## Edge Cases

A fully cyclic graph is the most important corner case. If all nodes are mutually reachable, the algorithm compresses everything into one SCC and returns the sum of all values. Any path-based DP that does not compress SCCs would incorrectly treat revisits as invalid or double count improperly.

Another edge case is a graph with multiple disconnected components. Each component becomes its own SCC, and since DP initializes each component independently, the algorithm correctly allows starting anywhere without needing artificial source nodes.

A final subtle case is when the best path enters a cycle late and then exits through a different node. SCC contraction ensures that entering the cycle immediately grants all values, so there is no benefit in simulating partial traversal; the DP correctly avoids undercounting by treating the whole component atomically.
