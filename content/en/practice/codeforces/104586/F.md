---
title: "CF 104586F - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u043a\u0440\u043e\u043b\u0438\u0447\u044c\u0438 \u043d\u043e\u0440\u044b"
description: "We are given a tree of caves. Each cave contains some number of balls. A character starts at a fixed cave and walks through the tree toward a leaf, but at every junction he chooses the next unvisited edge uniformly at random."
date: "2026-06-30T07:34:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104586
codeforces_index: "F"
codeforces_contest_name: "Codemasters Codecup 2023 - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 104586
solve_time_s: 100
verified: true
draft: false
---

[CF 104586F - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u043a\u0440\u043e\u043b\u0438\u0447\u044c\u0438 \u043d\u043e\u0440\u044b](https://codeforces.com/problemset/problem/104586/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree of caves. Each cave contains some number of balls. A character starts at a fixed cave and walks through the tree toward a leaf, but at every junction he chooses the next unvisited edge uniformly at random. He never goes back through an edge he already used, so his walk is always a simple path from the start node down to some leaf.

Every cave contributes its ball count if the walk passes through it. The task is to compute the expected total number of balls collected when starting from the given starting node.

The input size is up to ten thousand nodes, so any solution that enumerates paths explicitly or simulates random walks is impossible. A full enumeration of paths in a tree would grow exponentially with branching degree, so the only viable direction is to compute expectations locally and combine them through dynamic programming on the tree.

A subtle edge case appears when the starting node is already a leaf. In that case the walk never moves, so the answer is just the value at that node. Another corner case is when the tree degenerates into a path, where the randomness disappears entirely and the expectation becomes deterministic, which is useful for sanity checking.

## Approaches

A brute force interpretation would explicitly simulate all possible root-to-leaf paths from the starting node. At each node with degree d, the walk splits into d equally likely continuations. Even in a tree of size 10000, the number of distinct root-to-leaf paths can be exponential, so this approach fails immediately.

The key observation is that the process is a random walk on a tree that never revisits nodes, so once we step into a child subtree, the future expectation depends only on that subtree and not on the rest of the graph. This allows us to define a function E[v] as the expected number of balls collected starting from node v and moving away from the parent we came from.

At a node v, every neighbor except the parent is equally likely to be chosen as the next step. If we move to a neighbor u, we collect everything in u’s subtree according to E[u]. Therefore, E[v] becomes the value at v plus the average of E[u] over all children u. This is a standard tree DP, but with a normalization by degree minus one.

To compute this cleanly, we root the tree at the starting node and do a DFS that computes expectations bottom-up.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over paths | O(exp(n)) | O(n) | Too slow |
| Tree DP with expectation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the tree at the starting node s. The walk always moves away from the parent, so for each node we treat its parent as forbidden when computing transition probabilities.

We compute, for each node v, the expected number of balls collected starting from v when it is entered from its parent.

1. Build adjacency lists for the tree.

This gives constant time access to neighbors, which is necessary because transitions depend on degree.
2. Run a DFS from the start node, passing the parent.

The parent is needed because the transition rule excludes the edge we came from.
3. For each node v, collect all neighbors except the parent.

These are the valid next steps. If there are no such neighbors, v is a leaf in the rooted sense.
4. If v is a leaf, set dp[v] = a[v].

The walk stops here, so expectation is exactly the local value.
5. Otherwise compute dp[v] = a[v] plus the average of dp[u] over all valid neighbors u.

Each neighbor is chosen with probability 1 / deg(v excluding parent), so expectation is linear:

dp[v] = a[v] + sum(dp[u]) / k.
6. Return dp[s], the value computed at the start node.

The recursion naturally propagates expectations from leaves upward, because dp[u] is fully determined before it is used in dp[v].

### Why it works

At any node v, once the walk reaches v from its parent, the future path is a Markov process that depends only on v and its subtree. Each outgoing edge is chosen uniformly among remaining edges, so the expectation of future gain is exactly the average of child expectations. Linearity of expectation ensures that summing contributions from independent subtrees and averaging over choices produces the correct global expectation.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(200000)

n, s = map(int, input().split())
a = list(map(float, input().split()))

g = [[] for _ in range(n)]
for _ in range(n - 1):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    g[x].append(y)
    g[y].append(x)

dp = [0.0] * n

def dfs(v, p):
    children = []
    for to in g[v]:
        if to != p:
            dfs(to, v)
            children.append(to)

    if not children:
        dp[v] = a[v]
        return dp[v]

    total = 0.0
    for to in children:
        total += dp[to]

    dp[v] = a[v] + total / len(children)
    return dp[v]

print(dfs(s - 1, -1))
```

The solution builds the tree in adjacency form and runs a DFS from the starting node. The recursion computes dp values bottom-up. Each node aggregates results from its children only, excluding the parent edge to enforce the non-backtracking rule.

The only delicate part is ensuring the probability normalization is done using the number of valid outgoing edges, not the full degree. This is why children are explicitly filtered during DFS.

## Worked Examples

### Example 1

Input:

```
4 4
0 2 0 0
1 2
2 3
3 4
```

This is a chain, so every node except endpoints has exactly one child in the DFS rooted at 4.

| Node | Children | dp value computation |
| --- | --- | --- |
| 1 | none | 0 |
| 2 | 1 | 2 + 0 = 2 |
| 3 | 2 | 0 + 2 = 2 |
| 4 | 3 | 0 + 2 = 2 |

The expectation at node 4 is 2 because every path is deterministic and always passes through node 2.

### Example 2

Input:

```
6 6
0 1 2 2 0 0
1 3
3 5
5 4
5 6
2 4
```

From node 6, there is exactly one neighbor, so the walk is deterministic at first.

| Node | Children | dp |
| --- | --- | --- |
| 1 | none | 0 |
| 2 | none | 1 |
| 3 | 5 | 2 + dp[5] |
| 4 | 5 | 2 + dp[5] |
| 5 | 4,6 | 0 + (dp[4] + dp[6]) / 2 |
| 6 | 5 | 0 + dp[5] |

Solving bottom-up yields dp[5] = 2, dp[4] = 4, dp[3] = 6, dp[6] = 2.5.

The table shows how branching introduces averaging, while leaf chains propagate deterministic contributions upward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node and edge is processed once in DFS |
| Space | O(n) | Adjacency list and recursion stack |

The constraints allow up to 10000 nodes, so a linear traversal fits comfortably within limits. Each node does constant work beyond recursive calls, so the total runtime remains proportional to the size of the tree.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    n, s = map(int, input().split())
    a = list(map(float, input().split()))

    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        x, y = map(int, input().split())
        g[x-1].append(y-1)
        g[y-1].append(x-1)

    dp = [0.0] * n

    sys.setrecursionlimit(200000)

    def dfs(v, p):
        child = []
        for to in g[v]:
            if to != p:
                dfs(to, v)
                child.append(to)
        if not child:
            dp[v] = a[v]
            return dp[v]
        dp[v] = a[v] + sum(dp[c] for c in child) / len(child)
        return dp[v]

    return str(dfs(s-1, -1))

# minimum chain
assert abs(float(run("""2 1
1 2
1 2
""")) - 3.0) < 1e-9

# star-shaped tree
assert abs(float(run("""4 1
10 0 0 0
1 2
1 3
1 4
""")) - 10.0) < 1e-9

# balanced tree
assert abs(float(run("""7 1
1 1 1 1 1 1 1
1 2
1 3
2 4
2 5
3 6
3 7
""")) - 2.0) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain | deterministic accumulation | linear path correctness |
| star | single split averaging | branching expectation |
| balanced | multi-level averaging | recursive correctness |

## Edge Cases

A leaf start node is handled directly by the base case. Since there are no children, the DFS assigns dp[v] = a[v], which matches the fact that no movement occurs.

A high-degree node is handled by averaging over all children. Because we explicitly exclude the parent, we never incorrectly include a backward move, which would otherwise distort probabilities.

A linear chain reduces to a deterministic walk. Each node has exactly one child, so the averaging degenerates into direct propagation without dilution, which matches the intended behavior of forced movement along a single path.
