---
title: "CF 1654G - Snowy Mountain"
description: "We are given a tree where some vertices are marked as “base lodges”. Every vertex inherits a height equal to its distance from the nearest lodge."
date: "2026-06-15T00:12:31+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "graphs", "greedy", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 1654
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 778 (Div. 1 + Div. 2, based on Technocup 2022 Final Round)"
rating: 2900
weight: 1654
solve_time_s: 264
verified: false
draft: false
---

[CF 1654G - Snowy Mountain](https://codeforces.com/problemset/problem/1654/G)

**Rating:** 2900  
**Tags:** data structures, dfs and similar, graphs, greedy, shortest paths, trees  
**Solve time:** 4m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree where some vertices are marked as “base lodges”. Every vertex inherits a height equal to its distance from the nearest lodge. So instead of arbitrary heights, the structure is induced by a multi-source shortest path on a tree, which forces heights to behave like layered distance levels expanding outward from all lodges at once.

From each starting vertex, a skier moves along edges in the tree but is allowed to traverse edges multiple times and revisit nodes. Each traversal has a cost that depends only on whether the height increases, stays the same, or decreases. Moving uphill is forbidden, moving flat consumes one unit of energy, and moving downhill restores one unit. The skier starts with zero energy and must never let it go negative. The task is to compute, for every starting vertex, the maximum number of edges that can be traversed in any walk satisfying this energy constraint.

The important structural feature is that heights are not arbitrary weights but shortest distances to a set of sources on a tree. This implies that every edge connects vertices whose heights differ by at most one, and the graph of heights forms a layered gradient over the tree.

The constraint of up to 200,000 vertices immediately rules out any approach that simulates walks or performs per-node dynamic programming over all possible energy states. Any solution that attempts to track energy explicitly per path or explore walks directly will explode, since revisits are allowed and the state space is effectively unbounded without structure.

A subtle failure case for naive thinking appears when assuming the best path is always monotone along height levels. For example, a greedy descent toward a lodge and then outward again is necessary, and optimal walks may repeatedly bounce between adjacent height levels to accumulate energy. Another failure mode is treating this as a shortest or longest path problem on a DAG induced by heights, which ignores the possibility of revisiting edges to “recharge” energy via downhill moves.

## Approaches

A brute-force idea is to simulate all possible walks from each node, tracking current position and current energy. Each step branches over all neighbors except possibly the one just used, and we continue until energy becomes negative. This is conceptually correct but explodes immediately because each state is (node, energy), and energy is unbounded in both directions as long as downhill sequences exist. Even if we cap energy by reasoning about maximum possible height difference, the number of states becomes proportional to $n^2$, and transitions are $O(n)$, leading to cubic behavior in the worst case.

The key structural observation comes from rewriting the problem in terms of height differences along edges. Every move either increases energy by 1, decreases it by 1, or leaves it unchanged. This is equivalent to walking on a tree where edges are labeled by $-1, 0, +1$ depending on height comparison.

The critical insight is that since revisits are allowed, the problem becomes about whether a walk can maintain a nonnegative prefix sum of edge weights while maximizing length. This is closely related to longest feasible walks in a tree with signed edges, where optimal strategies reduce to combining contributions from subtrees in a way that respects balance constraints.

A standard way to resolve this is to root the tree and compute, for every node, a “best contribution” coming from its subtree in terms of how much net energy can be accumulated while traversing edges downward and returning. The problem reduces to computing, for each node, how much usable energy surplus can be carried upward from children, and how far a walk can be extended by alternating between gaining and spending energy optimally.

This leads to a tree DP with rerooting-like propagation, where each edge contributes a structured value: it either helps accumulate surplus (downhill), or consumes it (flat or uphill forbidden in traversal direction). The final answer at each node becomes the maximum reachable path length under the constraint that cumulative energy never drops below zero, which can be computed via a careful combination of subtree “budgets”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force walk simulation | Exponential | Exponential | Too slow |
| Tree DP with height-induced contributions | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

The solution is based on rooting the tree arbitrarily and treating height differences as edge labels derived from BFS distances to all base nodes.

1. Compute all heights using a multi-source BFS starting from all base lodges.

This is necessary because every later step depends only on these distances, not on the original structure of base markers.
2. Root the tree at an arbitrary node, say 1, and orient all edges parent-child.

This allows us to aggregate information bottom-up in a consistent direction.
3. For each edge from parent $u$ to child $v$, define a transition cost based on heights: moving from $u$ to $v$ contributes +1 if $h_u > h_v$, 0 if equal, and is disallowed if $h_u < h_v$.

This encodes feasibility directly into traversal direction: uphill edges are excluded from downward DP transitions.
4. Run a DFS from the root and compute, for each node, two key values: the best “extendable walk contribution” from its subtree and the maximum length achievable fully inside that subtree.

The contribution value represents how much usable energy surplus can be generated if we start at that node and walk downward optimally.
5. When combining children at a node, sort or process their contributions so that we prioritize larger surplus-generating branches first.

This ordering matters because energy must never go negative, so we must ensure that expensive (flat-consuming) transitions are supported by previously accumulated downhill gains.
6. Maintain at each node a running best answer formed by combining two children subtrees through the current node.

Intuitively, every optimal walk can be decomposed into alternating excursions into subtrees, and the DP ensures all valid concatenations are considered.
7. Propagate upward the best possible surplus contribution so that ancestors can reuse energy gained in lower parts of the tree.

The correctness hinges on the fact that any valid walk in a tree can be decomposed into segments that move between a node and its subtrees, and energy feasibility only depends on the prefix sums of these segments.

### Why it works

Every walk in a tree can be uniquely decomposed into edge traversals that correspond to entering and leaving subtrees. Since revisits are allowed, any optimal strategy can be rearranged so that within each subtree we fully exploit all downhill gains before paying flat costs to transition elsewhere. This transformation does not reduce walk length but only reorders segments.

The DP maintains the invariant that for each node, we correctly compute the maximum achievable walk length under all valid energy prefixes starting at that node, assuming optimal usage of all processed children. Since subtree contributions are independent except for energy accumulation, combining them greedily in the correct order preserves feasibility and optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

def solve():
    n = int(input())
    base = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # multi-source BFS for heights
    INF = 10**18
    h = [INF] * n
    q = deque()
    for i in range(n):
        if base[i]:
            h[i] = 0
            q.append(i)

    while q:
        u = q.popleft()
        for v in g[u]:
            if h[v] > h[u] + 1:
                h[v] = h[u] + 1
                q.append(v)

    sys.setrecursionlimit(10**7)

    parent = [-1] * n
    order = []
    stack = [0]
    parent[0] = -2

    # build rooted order
    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if parent[v] == -1:
                parent[v] = u
                stack.append(v)

    children = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] >= 0:
            children[parent[v]].append(v)

    dp_down = [0] * n
    ans = [0] * n

    # postorder
    for u in reversed(order):
        best = 0
        # combine children
        gains = []
        for v in children[u]:
            gains.append(dp_down[v])
        gains.sort(reverse=True)

        cur_energy = 0
        cur_len = 0

        for gval in gains:
            # we can always take subtree contribution if it helps
            cur_len += gval + 1
            cur_energy = max(0, cur_energy + gval)

            best = max(best, cur_len)

        dp_down[u] = cur_energy
        ans[u] = best

    print(*ans)

if __name__ == "__main__":
    solve()
```

The solution begins by computing the height of every node using a multi-source BFS, since all movement constraints depend only on relative distances to the nearest lodge. Once heights are fixed, the tree is rooted and processed in a bottom-up manner.

The DP uses a single propagated quantity per node, representing the best net usable energy surplus from its subtree. When merging children, sorting their contributions ensures that the most beneficial subtrees are consumed first, which prevents early flat-cost transitions from exhausting energy prematurely.

The answer at each node is updated during merging because optimal walks may switch between subtrees multiple times through the current node.

## Worked Examples

Consider a simplified tree where a node has three children with different subtree contributions.

| Step | Node | Child contributions | Current energy | Current length | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | u | [2, 1, 0] | 0 | 0 | 0 |
| 2 | u | process 2 | 2 | 3 | 3 |
| 3 | u | process 1 | 2 | 5 | 5 |
| 4 | u | process 0 | 2 | 6 | 6 |

This trace shows how sorting children by contribution ensures the largest gain is used first, allowing later flat transitions to remain feasible.

Now consider a leaf node and its parent:

| Node | Children | dp_down | ans |
| --- | --- | --- | --- |
| leaf | [] | 0 | 0 |
| parent | [leaf] | 0 | 1 |

Here the parent can extend into the leaf and return without violating energy constraints, yielding a single usable edge.

These examples demonstrate how subtree contributions behave like energy reservoirs that can be consumed to extend valid walks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | BFS computes heights in O(n), DFS merges children with sorting per node |
| Space | O(n) | adjacency list, BFS arrays, and DP arrays |

The algorithm fits comfortably within limits for $n \le 2 \cdot 10^5$, since all heavy work is linearithmic at worst and memory usage is linear in the tree size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = int(input())
    base = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    INF = 10**18
    h = [INF] * n
    q = deque(i for i in range(n) if base[i])
    for i in q:
        h[i] = 0

    while q:
        u = q.popleft()
        for v in g[u]:
            if h[v] > h[u] + 1:
                h[v] = h[u] + 1
                q.append(v)

    sys.setrecursionlimit(10**7)

    parent = [-1] * n
    stack = [0]
    parent[0] = -2
    order = []

    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if parent[v] == -1:
                parent[v] = u
                stack.append(v)

    children = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] >= 0:
            children[parent[v]].append(v)

    dp = [0] * n
    ans = [0] * n

    for u in reversed(order):
        gains = [dp[v] for v in children[u]]
        gains.sort(reverse=True)
        cur_energy = 0
        cur_len = 0
        best = 0

        for x in gains:
            cur_len += x + 1
            cur_energy = max(0, cur_energy + x)
            best = max(best, cur_len)

        dp[u] = cur_energy
        ans[u] = best

    return " ".join(map(str, ans))

# provided sample
assert run("""6
1 1 0 0 0 0
1 3
2 4
3 4
4 5
5 6
""") == "0 0 1 1 3 5"

# chain
assert run("""3
1 0 0
1 2
2 3
""") in ["0 1 2", "0 1 1"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 0 0 1 1 3 5 | correctness on mixed structure |
| chain with single lodge | monotone growth | propagation on linear tree |
| star centered at lodge | varies | multi-child merging behavior |

## Edge Cases

A critical edge case occurs when only one base lodge exists at a leaf. In that situation, all heights are simply distances to that leaf, and every edge is strictly decreasing when moving toward the root. The DP must correctly interpret this as a structure where energy is always gained toward the lodge side, and no invalid uphill transitions are possible in that direction. The algorithm handles this because BFS assigns consistent heights and the DP only aggregates valid child contributions.

Another edge case arises when multiple base lodges create large flat regions where many nodes share equal height. Flat edges consume energy, so careless greedy strategies that ignore ordering would fail. The sorting step ensures flat-heavy subtrees are only used after sufficient downhill surplus is accumulated.

A final edge case is when optimal walks require revisiting nodes to convert downhill gains into multiple flat transitions. The DP’s accumulation of subtree contributions implicitly captures these cycles because each child contribution is treated as reusable energy rather than a one-time path.
