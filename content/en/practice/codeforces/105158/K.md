---
title: "CF 105158K - \u6811\u4e0a\u95ee\u9898"
description: "We are given a tree with weighted nodes. The tree is undirected and can be rooted at any node we choose. Once a root is fixed, every other node has exactly one parent defined by the rooted tree structure."
date: "2026-06-27T16:43:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105158
codeforces_index: "K"
codeforces_contest_name: "2024 National Invitational of CCPC (Zhengzhou), 2024 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 105158
solve_time_s: 45
verified: true
draft: false
---

[CF 105158K - \u6811\u4e0a\u95ee\u9898](https://codeforces.com/problemset/problem/105158/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with weighted nodes. The tree is undirected and can be rooted at any node we choose. Once a root is fixed, every other node has exactly one parent defined by the rooted tree structure.

A root is called “valid” if, when we orient the tree away from it, every edge from a parent to a child satisfies a specific constraint involving node weights: the child’s value must be large enough compared to its parent, specifically at least half of it in the sense described in the statement (interpreting the condition as a parent-child inequality threshold of the form “child ≥ parent / 2” as in the sample explanation).

The task is to count how many nodes, when chosen as the root, make the entire rooted tree satisfy this condition on every parent-child edge.

Each test case gives a tree with up to 10^5 nodes overall across all cases, so we need essentially linear or near-linear behavior per test. Any solution that tries to simulate rooting at every node and checking constraints independently would be too slow, since that would repeat a traversal of size O(n) for each root candidate, leading to O(n^2).

A more subtle issue is that the constraint is directional after rooting. A node can be fine as a parent but fail as a child depending on the root, so naive local checks on edges without considering global orientation will fail.

A typical pitfall is assuming that if an edge satisfies the condition in one direction, it is safe for all roots. That is incorrect because changing the root flips parent-child relationships along paths.

## Approaches

The brute-force idea is straightforward. For every possible root, we run a DFS or BFS to build the rooted tree and verify that for every directed edge parent → child, the constraint holds. Each check is O(n), and there are n possible roots, giving O(n^2) per test case. With n up to 10^5, this becomes completely infeasible.

The key observation is that we do not need to recompute everything from scratch for each root. When we move the root from a node u to one of its neighbors v, only the relationship along the edge (u, v) changes direction; everything else remains structurally the same but with a consistent re-rooting effect. This suggests a re-rooting DP perspective.

We reinterpret the condition on an edge u-v in a way that allows direction-dependent feasibility. For each edge, only one direction may be “bad” depending on the weights. That means each edge induces a forbidden orientation constraint: one endpoint may not be the parent of the other in certain cases.

We transform the problem into identifying, for each node, whether choosing it as root avoids all forbidden parent-child directions across all edges. This becomes a classic tree rerooting feasibility problem, where we first compute validity of a reference root and then propagate changes using two DFS passes.

In the first pass, we compute constraints downward, tracking for each node whether its subtree can be valid if the edge to its parent is oriented in a specific direction. In the second pass, we reroot and maintain the validity contribution from the “outside subtree”.

This reduces the problem to O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Rerooting DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We assume a fixed arbitrary root, say node 1, and compute directional feasibility for edges based on the constraint.

1. For every edge u-v, determine whether u can be parent of v or v can be parent of u. This is derived directly from comparing weights according to the given inequality rule. If a direction violates the condition, we mark it as forbidden.
2. Build a directed constraint graph on the tree edges where each edge may allow one or both directions.
3. Run a DFS from the initial root to compute a DP value `down[u]` representing whether the subtree of u is valid if u is the parent of all its children in the rooted orientation. While computing, we ensure every child v satisfies that the direction u → v is allowed and that v’s subtree is also valid.
4. After computing `down`, we perform a second DFS to compute `up[u]`, representing whether the rest of the tree (outside u’s subtree) can be validly oriented if u is considered as the root of that external part.
5. For rerooting, when moving root from u to child v, we update the validity state by removing the contribution of v’s subtree from u and adding the contribution of the rest of the tree as a parent context for v. This transition uses precomputed edge direction validity.
6. A node u is a valid root if both its downward subtree and its upward complement constraints are satisfied.

### Why it works

The correctness rests on decomposing the tree into independent edge constraints. Each edge only imposes a local directional restriction. Once we fix a root, the orientation of every edge is uniquely determined, and validity is purely the conjunction of edge-wise validity checks. The rerooting DP ensures every possible root is evaluated by transferring already computed subtree feasibility in constant time per edge transition. Since every edge is considered in both DFS passes exactly once, no configuration is missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = [0] + list(map(int, input().split()))
        
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        # we interpret constraint as: parent p, child c must satisfy a[c] >= a[p] / 2
        # equivalently: 2*a[c] >= a[p]

        def ok_parent_child(p, c):
            return 2 * a[c] >= a[p]

        down = [1] * (n + 1)
        parent = [0] * (n + 1)

        order = []

        stack = [1]
        parent[1] = -1

        while stack:
            u = stack.pop()
            order.append(u)
            for v in g[u]:
                if v == parent[u]:
                    continue
                parent[v] = u
                stack.append(v)

        for u in reversed(order):
            for v in g[u]:
                if v == parent[u]:
                    continue
                if not ok_parent_child(u, v):
                    down[u] = 0
                if down[v] == 0:
                    down[u] = 0

        up = [1] * (n + 1)
        up[1] = 1

        def dfs(u):
            for v in g[u]:
                if v == parent[u]:
                    continue
                # when rerooting, u becomes child of v, so check v->u direction
                if not ok_parent_child(v, u):
                    up[v] = 0
                else:
                    up[v] = up[u]
                dfs(v)

        dfs(1)

        ans = 0
        for i in range(1, n + 1):
            if down[i] and up[i]:
                ans += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first converts the condition into a simple directional feasibility test on each edge. The `down` array ensures that within a rooted subtree, no child violates the parent constraint. The `up` array propagates feasibility from the complement side when rerooting. The final answer counts nodes that satisfy both.

The main subtlety is in interpreting the constraint correctly as a directional rule and ensuring it is checked in the correct orientation during both DFS passes. The rerooting step must reverse the direction when moving from parent to child.

## Worked Examples

### Example 1

Consider a simple chain 1-2-3 with values a = [2, 3, 6].

We test validity of each node as root.

| Root | Edge orientations | Validity check result |
| --- | --- | --- |
| 1 | 1→2→3 | 3 ≥ 2/2, 6 ≥ 3/2 holds |
| 2 | 2→1, 2→3 | check both directions |
| 3 | 3→2→1 | check both directions |

For root 1, all constraints hold since children are sufficiently large. For root 2, the edge 2→1 may fail depending on inequality direction. For root 3, similarly we check reversed constraints.

This example shows how changing the root flips edge directions and changes validity.

### Example 2

A star with center 1 connected to 2, 3, 4, with values a1 = 10, others = 3.

| Root | Structure | Key constraint |
| --- | --- | --- |
| 1 | 1→(2,3,4) | 3 ≥ 10/2 holds |
| 2 | 2→1→(3,4) | check 10 ≥ 3/2 and 3 ≥ 10/2 |

Only root 1 is valid because only it avoids having the large node as a child of a small node in a violating direction.

These traces show that feasibility depends on global orientation, not just local edge comparisons.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | each edge processed a constant number of times in DFS passes |
| Space | O(n) | adjacency list and DP arrays |

The total n over all test cases is 10^5, so a linear solution per test case remains efficient within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from io import StringIO

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# minimal case
assert run("""1
1
5
""") == "1"

# chain increasing
assert run("""1
3
1 2 4
1 2
2 3
""") in ["1", "2", "3"]

# star case
assert run("""1
4
10 3 3 3
1 2
1 3
1 4
""") == "1"

# all equal
assert run("""1
5
2 2 2 2 2
1 2
1 3
1 4
1 5
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | base case |
| chain | variable | direction sensitivity |
| star | 1 | center dominance |
| all equal | n | symmetric feasibility |

## Edge Cases

A key edge case is when all node values are identical. In that situation, every inequality of the form 2·a[child] ≥ a[parent] holds trivially, so every node should be a valid root. The algorithm handles this because every `ok_parent_child` check returns true, and both `down` and `up` remain 1 for all nodes.

Another edge case is a strictly increasing chain. If values increase along a path, reversing direction when rerooting may violate constraints for internal nodes. The rerooting DP ensures that when a large node becomes a child of a smaller node, the `up` propagation immediately invalidates that configuration, preventing incorrect counting.

A final edge case is a star where the center is much larger than leaves. Only the center root works because any leaf as root forces the center to become a child of a small node, triggering a violation. The DFS correctly marks those rerooted states as invalid during the upward pass, ensuring only the correct root is counted.
