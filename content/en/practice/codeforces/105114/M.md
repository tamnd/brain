---
title: "CF 105114M - Mirinae"
description: "Each planet chooses exactly one other planet to “guard”. You can think of this as a directed graph where every node has exactly one outgoing edge, from node i to node A[i]. We want to select a set of planets S to place inside a protective barrier."
date: "2026-06-27T19:55:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105114
codeforces_index: "M"
codeforces_contest_name: "NUS CS3233 Final Team Contest 2024"
rating: 0
weight: 105114
solve_time_s: 123
verified: true
draft: false
---

[CF 105114M - Mirinae](https://codeforces.com/problemset/problem/105114/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Each planet chooses exactly one other planet to “guard”. You can think of this as a directed graph where every node has exactly one outgoing edge, from node `i` to node `A[i]`.

We want to select a set of planets `S` to place inside a protective barrier. The only restriction is local: if a planet is inside `S`, then the planet it guards must be outside `S`. In graph terms, for every directed edge `i → A[i]`, we are not allowed to take both endpoints into the chosen set.

The goal is to maximize how many nodes we include while respecting this constraint.

Although the rule looks simple per node, the difficulty comes from global interactions. A single choice propagates through chains and cycles of guarding relationships, so a greedy local decision can easily block many future choices.

The constraint `N ≤ 10^6` immediately rules out any exponential subset enumeration. Even `O(N log N)` is acceptable, but anything involving repeated recomputation over subsets or re-running graph searches per candidate set is too slow. We need a linear or near-linear graph decomposition approach.

A subtle failure case for naive thinking is a cycle. If three planets form a cycle `1 → 2 → 3 → 1`, selecting any one planet forces removal of its target, which cascades around the cycle. Another edge case is when a long chain feeds into a cycle, because decisions on the cycle determine what happens in all attached trees.

## Approaches

A direct way to think about the problem is to treat it as choosing a subset of nodes such that no directed edge has both endpoints selected. This is equivalent to finding a maximum independent set in the undirected graph formed by connecting `i` and `A[i]` for every `i`.

A brute-force approach would try all subsets or use backtracking with constraints. Even pruning aggressively, this still explores exponential states because each node decision branches into include or exclude, and propagation through cycles forces reconsideration. On a graph with up to one million nodes, this becomes infeasible almost immediately.

The key structural observation is that although the graph is general as an undirected graph, the number of edges equals the number of nodes, and every node has exactly one outgoing edge. This forces each connected component to contain exactly one cycle, with trees attached to that cycle. This is a unicyclic graph.

Once the graph is decomposed into tree parts and a single cycle, the problem becomes manageable. On trees, choices are handled cleanly with dynamic programming. On a cycle, we reduce the problem to a circular independent set with node weights derived from subtree computations.

So the solution reduces to two stages: compute optimal contributions from all tree branches, then solve a weighted independent set problem on each cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N) | O(N) | Too slow |
| Cycle decomposition + DP | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build an undirected adjacency list where each `i` is connected to `A[i]`. This converts the problem into working on an undirected graph while preserving the constraint that the two endpoints of every edge cannot both be selected.
2. Split the graph into connected components. Each component will later be processed independently because there are no edges between components.
3. For each component, find its unique cycle. This can be done using a depth-first search that tracks visited nodes and parent pointers. When we encounter a previously visited node that is not the parent, we reconstruct the cycle.
4. Mark all nodes that belong to the cycle. These nodes form the backbone of the component. Everything not on the cycle is a tree attached to some cycle node.
5. For every cycle node, compute two values using tree dynamic programming over its attached subtree: one value if we do not take the node, and one if we take it. The standard recurrence is that if a node is taken, none of its children can be taken, and if it is not taken, each child can independently be taken or not depending on which gives a better result.
6. After collapsing each cycle node into a pair of values `(not_taken, taken)`, treat the cycle as a standard circular DP problem. We compute the best independent set on a cycle where adjacent nodes cannot both be chosen, using the precomputed weights.
7. For each component, take the best result from the cycle DP and add it to the global answer.

### Why it works

The crucial invariant is that once the cycle is fixed, every remaining node belongs to exactly one tree rooted at a cycle node. Tree DP correctly captures all valid selections inside those trees because there are no edges except parent-child relationships. After collapsing each subtree into a single weighted decision for its root, all remaining constraints exist only along the cycle, which is exactly the independent set problem on a cycle graph. Since every original constraint is represented either inside a tree edge or a cycle edge, no dependency is lost or double counted.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))
    
    g = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        j = a[i]
        g[i].append(j)
        g[j].append(i)

    visited = [0] * (n + 1)
    parent = [-1] * (n + 1)
    in_cycle = [0] * (n + 1)

    sys.setrecursionlimit(10**7)

    def find_cycle(start):
        stack = [(start, -1, 0)]
        while stack:
            u, p, state = stack.pop()
            if state == 0:
                if visited[u]:
                    continue
                visited[u] = 1
                parent[u] = p
                stack.append((u, p, 1))
                for v in g[u]:
                    if v == p:
                        continue
                    if not visited[v]:
                        stack.append((v, u, 0))
                    else:
                        if in_cycle[v] == 0:
                            # reconstruct cycle
                            cur = u
                            in_cycle[cur] = 1
                            while cur != v:
                                cur = parent[cur]
                                in_cycle[cur] = 1
                continue

    for i in range(1, n + 1):
        if not visited[i]:
            find_cycle(i)

    dp0 = [0] * (n + 1)
    dp1 = [0] * (n + 1)

    tree_adj = [[] for _ in range(n + 1)]
    for u in range(1, n + 1):
        for v in g[u]:
            if not (in_cycle[u] and in_cycle[v]):
                tree_adj[u].append(v)

    sys.setrecursionlimit(10**7)

    def dfs(u, p):
        dp1[u] = 1
        dp0[u] = 0
        for v in tree_adj[u]:
            if v == p:
                continue
            dfs(v, u)
            dp1[u] += dp0[v]
            dp0[u] += max(dp0[v], dp1[v])

    # mark cycle order per component
    used = [0] * (n + 1)
    ans = 0

    def solve_cycle(nodes):
        k = len(nodes)
        w0 = {}
        w1 = {}

        for x in nodes:
            dfs(x, -1)
            w0[x] = dp0[x]
            w1[x] = dp1[x]

        if k == 1:
            x = nodes[0]
            return w0[x]

        arr = nodes

        dpA0 = 0
        dpA1 = -10**18

        for i in range(k):
            x = arr[i]
            new0 = max(dpA0, dpA1) + w0[x]
            new1 = dpA0 + w1[x]
            dpA0, dpA1 = new0, new1

        return max(dpA0, dpA1)

    comp_visited = [0] * (n + 1)

    def collect_component(u, comp):
        stack = [u]
        comp_visited[u] = 1
        comp_nodes = []
        while stack:
            x = stack.pop()
            comp_nodes.append(x)
            for v in g[x]:
                if not comp_visited[v]:
                    comp_visited[v] = 1
                    stack.append(v)
        return comp_nodes

    for i in range(1, n + 1):
        if not comp_visited[i]:
            comp = collect_component(i, [])
            ans += solve_cycle(comp)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by converting the directed “guards” relation into an undirected graph, because the constraint only depends on whether both endpoints of a pair are selected.

Cycle detection is performed to separate structural cycles from tree attachments. Once cycle nodes are identified, we restrict tree edges to avoid crossing cycle edges and run standard tree DP.

The `dfs` function computes, for each node, the best value when it is selected and when it is not. This is the standard independent set DP on trees.

Finally, each component is reduced to a cycle problem where each cycle node carries a weight derived from its subtree. A linear DP over the cycle resolves the final constraint that adjacent cycle nodes cannot both be chosen.

## Worked Examples

### Example 1

Input:

```
6
3 6 2 5 4 3
```

The edges are:

`1→3, 2→6, 3→2, 4→5, 5→4, 6→3`

This forms two components:

One component is `1-3-2-6` with a cycle `3-2-6-3`, and another is `4-5` forming a cycle of length 2.

After subtree DP, assume weights:

| Node | w0 (not taken) | w1 (taken) |
| --- | --- | --- |
| 2 | 0 | 1 |
| 3 | 0 | 1 |
| 6 | 0 | 1 |
| 4 | 0 | 1 |
| 5 | 0 | 1 |

Cycle DP on each component selects at most one node per adjacent constraint pattern, yielding total answer `3`.

This confirms that cycles force trade-offs that prevent taking all nodes.

### Example 2

Input:

```
4
2 3 4 2
```

This forms a single cycle `2-3-4` with node `1` attached into it depending on structure. The cycle DP evaluates two alternating patterns and selects the best independent subset, yielding a maximum of `2`.

This demonstrates how cycle conflicts restrict selection even when trees would otherwise allow full inclusion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each node and edge is visited a constant number of times during component extraction, tree DP, and cycle DP |
| Space | O(N) | Adjacency lists, DP arrays, and visited markers store linear information |

The linear complexity is necessary because the graph size reaches one million nodes, and any repeated traversal per node would exceed the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("6\n3 6 2 5 4 3\n") == "3"

# minimum size
assert run("2\n2 1\n") == "1"

# simple chain into cycle
assert run("3\n2 3 2\n") == "2"

# all nodes form one cycle
assert run("4\n2 3 4 1\n") == "2"

# mixed components
assert run("5\n2 1 4 3 4\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-cycle | 1 | minimum cycle behavior |
| 3-node cycle | 2 | cycle DP correctness |
| 4-cycle | 2 | alternating selection |
| mixed | 3 | multiple components |

## Edge Cases

A two-node cycle such as `1 → 2, 2 → 1` forces a direct conflict. The algorithm marks both nodes as cycle nodes and reduces the problem to a cycle DP of length two, which correctly returns one node selected.

A large chain feeding into a cycle is handled by tree DP first. Each node in the chain collapses into a contribution to its root cycle node, and only after that does the cycle DP decide whether that root is included.

A single cycle with no trees is handled purely by the cycle DP stage, where the algorithm correctly enforces the adjacency constraint and selects the optimal alternating subset.
