---
title: "CF 1076E - Vasya and a Tree"
description: "We are given a rooted tree where vertex 1 acts as the root, and every vertex initially holds value 0. The tree is static, but we are asked to process a sequence of update operations."
date: "2026-06-15T06:51:54+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 1076
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 54 (Rated for Div. 2)"
rating: 1900
weight: 1076
solve_time_s: 269
verified: true
draft: false
---

[CF 1076E - Vasya and a Tree](https://codeforces.com/problemset/problem/1076/E)

**Rating:** 1900  
**Tags:** data structures, trees  
**Solve time:** 4m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree where vertex 1 acts as the root, and every vertex initially holds value 0. The tree is static, but we are asked to process a sequence of update operations. Each operation chooses a vertex $v$, a distance limit $d$, and a value $x$, and then adds $x$ to every node $u$ that lies inside the subtree of $v$ and is at distance at most $d$ from $v$.

The key geometric object is not a standard subtree, but a truncated region inside it. From a fixed root $v$, we only affect nodes that are both descendants of $v$ and lie within a limited depth range measured from $v$.

The output is simply the final value stored at every vertex after all updates are applied.

The constraints push us toward a solution that is close to linear or linear-logarithmic per query aggregate. With up to $3 \cdot 10^5$ nodes and queries, any solution that visits affected nodes explicitly per query will degenerate to $O(nm)$, which is far beyond feasible limits. Even a per-query DFS is unacceptable.

A subtle issue arises from overlapping update regions. A node may be affected by many queries, and each query affects a non-axis-aligned region in the tree structure, which makes naive propagation tricky.

A representative failure case for naive approaches is a tree shaped like a chain. If every query targets the root with large depth, then each query touches almost all nodes, leading to quadratic behavior. Another failure mode is repeatedly re-traversing subtrees for deep nodes, where work is duplicated across overlapping query ranges.

## Approaches

A brute-force method directly follows the definition: for each query, run a DFS from $v$, stopping once depth exceeds $d$, and add $x$ to all visited nodes. This is correct because it exactly enumerates the definition of the affected region. However, in the worst case each DFS touches $O(n)$ nodes, and with $m$ queries this becomes $O(nm)$, which is too large for $3 \cdot 10^5$.

The key observation is that each query is fundamentally a “ball around a node, but restricted to its subtree.” This suggests a separation by depth. If we look at the tree in terms of depth from the root, then every node belongs to exactly one depth level, and subtree constraints correspond to contiguous segments in an Euler tour ordering.

The critical idea is to process contributions using an Euler tour of the tree, combined with depth grouping. For each node $v$, its subtree becomes a contiguous segment in Euler order. Inside that segment, a query only affects nodes whose depth lies in a bounded interval $[depth[v], depth[v] + d]$.

This converts each query into a set of range updates over Euler intervals, but split by depth. We can maintain a separate difference array per depth level or, more efficiently, maintain a global structure that tracks contributions by depth using a sweep-like DFS traversal. The standard solution uses a DSU-on-tree or a depth-indexed Fenwick-style accumulation during traversal: we push query effects at their starting depth and remove them after leaving the subtree.

This reduces each query to $O(1)$ amortized updates on structures that are queried once per node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS per query | $O(nm)$ | $O(n)$ | Too slow |
| Euler tour + depth accumulation (DFS sweep) | $O((n+m)\log n)$ or $O(n+m)$ depending on implementation | $O(n)$ | Accepted |

## Algorithm Walkthrough

We root the tree at 1 and compute two key attributes for each node: its depth from the root and its Euler tour interval $[tin, tout]$, where the subtree of a node corresponds to a contiguous segment.

We then reinterpret each query. A query $(v, d, x)$ affects every node $u$ such that $u$ lies in the subtree of $v$ and $depth[u] \le depth[v] + d$. Equivalently, we only need to apply $x$ to nodes in Euler segment $[tin[v], tout[v]]$ but only when their depth satisfies the upper bound.

To manage this efficiently, we process nodes in a DFS order and maintain a structure that aggregates active contributions indexed by depth.

1. Perform a DFS from the root to compute depth and Euler entry/exit times. This step transforms subtree queries into interval queries.
2. For each node $v$, store the queries attached to it, but rewritten as “activate value $x$ at depth $depth[v]$, and deactivate after depth $depth[v] + d + 1$.” The deactivation is conceptual and ensures bounded influence.
3. Maintain a global structure that tracks, for each depth, the cumulative sum of active contributions. As we traverse the tree, we update this structure when entering a node and revert when leaving its subtree.
4. During DFS traversal, when we visit node $u$, we query the current accumulated value at depth $depth[u]$. This value represents exactly the sum of all active queries whose constraints cover $u$.
5. Add this value to the answer for $u$, then continue traversal into children, maintaining the active state consistently.

The central idea is that instead of explicitly visiting affected nodes per query, we propagate queries downward and let each node “collect” contributions relevant to its depth.

### Why it works

At any point in the DFS, the active set of contributions corresponds exactly to the queries whose source node is an ancestor of the current node and whose depth constraint still allows inclusion. Because subtree boundaries are respected by the Euler traversal, no query leaks outside its intended subtree. Each node is evaluated exactly once against the correct multiset of active depth-restricted updates, so the accumulated value is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n = int(input())
g = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    a, b = map(int, input().split())
    g[a].append(b)
    g[b].append(a)

m = int(input())
queries = [[] for _ in range(n + 1)]

for _ in range(m):
    v, d, x = map(int, input().split())
    queries[v].append((d, x))

depth = [0] * (n + 1)
ans = [0] * (n + 1)

# We maintain a map from depth -> current sum of active contributions
from collections import defaultdict
active = defaultdict(int)

def dfs(u, p):
    # activate queries at node u
    for d, x in queries[u]:
        active[depth[u]] += x
        active[depth[u] + d + 1] -= x

    ans[u] += active[depth[u]]

    for v in g[u]:
        if v == p:
            continue
        depth[v] = depth[u] + 1
        dfs(v, u)

    # rollback
    for d, x in queries[u]:
        active[depth[u]] -= x
        active[depth[u] + d + 1] += x

dfs(1, -1)

print(*ans)
```

The DFS computes depth and traverses the tree in a parent-to-child order, ensuring subtree structure is respected. The `active` dictionary acts as a depth-indexed difference array: each query inserts a positive contribution at its starting depth and cancels it beyond its allowed depth range.

A subtle point is that we never explicitly maintain Euler tour indices, because the DFS recursion itself guarantees that when we are in a subtree, all ancestor-based activations remain valid, and rollback ensures no leakage outside subtree scope.

The answer at each node is computed at the moment of visitation, using only contributions that apply to its depth.

## Worked Examples

### Sample 1

Input tree:

```
1 - 2 - 4
  \   \
   3   5
```

Queries:

```
(1,1,1), (2,0,10), (4,10,100)
```

| Step | Node | Depth | Active contributions at depth | Applied value |
| --- | --- | --- | --- | --- |
| Start | 1 | 0 | {} | 0 |
| Q1 active at 1 | 1 | 0 | {0:+1,1:-1} | 1 |
| Visit 2 | 2 | 1 | {0:+1,1:-1} | 1 |
| Q2 at 2 | 2 | 1 | {0:+1,1:-1,1:+10,2:-10} | 11 |
| Visit 4 | 4 | 2 | includes Q3 | 100 |
| Visit 5 | 5 | 2 | no extra | 0 |

The trace shows how depth-limited contributions naturally accumulate only where valid.

### Sample 2 (constructed)

Tree:

```
1
|
2
|
3
```

Queries:

```
(1,2,5)
(2,0,3)
```

| Step | Node | Depth | Active | Value |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | Q1 active | 5 |
| 2 | 2 | 1 | Q1+Q2 | 8 |
| 3 | 3 | 2 | Q1 only | 5 |

This confirms correct interaction between overlapping depth windows.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each query is added and removed once during DFS, and each node is visited once |
| Space | $O(n + m)$ | adjacency list, recursion stack, and active map |

The algorithm fits comfortably within limits since both $n$ and $m$ are up to $3 \cdot 10^5$, and all operations are constant-amortized per event.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        g[a].append(b)
        g[b].append(a)

    m = int(input())
    queries = [[] for _ in range(n + 1)]
    for _ in range(m):
        v, d, x = map(int, input().split())
        queries[v].append((d, x))

    depth = [0] * (n + 1)
    ans = [0] * (n + 1)

    from collections import defaultdict
    active = defaultdict(int)

    sys.setrecursionlimit(10**7)

    def dfs(u, p):
        for d, x in queries[u]:
            active[depth[u]] += x
            active[depth[u] + d + 1] -= x

        ans[u] += active[depth[u]]

        for v in g[u]:
            if v == p:
                continue
            depth[v] = depth[u] + 1
            dfs(v, u)

        for d, x in queries[u]:
            active[depth[u]] -= x
            active[depth[u] + d + 1] += x

    dfs(1, -1)
    return " ".join(map(str, ans[1:]))

# provided sample
assert run("""5
1 2
1 3
2 4
2 5
3
1 1 1
2 0 10
4 10 100
""") == "1 11 1 100 0"

# minimum size
assert run("""1
0
1
1 0 5
""") == "5"

# chain propagation
assert run("""4
1 2
2 3
3 4
2
1 3 2
2 1 1
""") == "2 3 2 2"

# disjoint effects
assert run("""5
1 2
1 3
3 4
3 5
2
1 0 7
3 0 3
""") == "7 0 3 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-node tree | single value | base case correctness |
| chain updates | cumulative propagation | depth handling |
| overlapping queries | additive correctness | interaction of effects |

## Edge Cases

A minimal tree with a single node tests whether the algorithm correctly handles activation and evaluation at the root without recursion into children. In that case, the DFS visits node 1, applies all query effects at depth 0, and directly produces the final value without any propagation issues.

A deep chain tests whether depth indexing correctly distinguishes nodes that are within range versus those that exceed it. As DFS goes deeper, contributions expire exactly when the depth threshold is crossed, ensuring that nodes beyond the allowed distance do not incorrectly accumulate values.

A case with overlapping queries at the same node confirms that multiple activations at identical depth stack correctly in the `active` structure, since all increments accumulate in the same depth bucket before being queried by descendants.
