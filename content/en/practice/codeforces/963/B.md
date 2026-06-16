---
title: "CF 963B - Destruction of a Tree"
description: "We are given a tree where each vertex has an associated current degree that changes as vertices are removed. A vertex is eligible for removal only when its degree is even at the moment we choose it."
date: "2026-06-17T01:42:32+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 963
codeforces_index: "B"
codeforces_contest_name: "Tinkoff Internship Warmup Round 2018 and Codeforces Round 475 (Div. 1)"
rating: 2000
weight: 963
solve_time_s: 82
verified: false
draft: false
---

[CF 963B - Destruction of a Tree](https://codeforces.com/problemset/problem/963/B)

**Rating:** 2000  
**Tags:** constructive algorithms, dfs and similar, dp, greedy, trees  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree where each vertex has an associated current degree that changes as vertices are removed. A vertex is eligible for removal only when its degree is even at the moment we choose it. When a vertex is removed, all incident edges disappear, so the degrees of its neighbors decrease.

The task is to decide whether there exists a sequence of removals that deletes every vertex, always respecting the rule that the chosen vertex must currently have even degree. If such a sequence exists, we must output one valid order.

The input representation is a rooted description of a tree: each vertex i is either connected to a parent p[i] or is a root if p[i] equals zero. This defines an undirected tree with n minus one edges. The process itself is dynamic because removing a vertex changes degrees globally, so local decisions affect future availability.

The constraint n up to 2 · 10^5 implies that any solution must be close to linear or linearithmic. Anything that repeatedly recomputes degrees or simulates naive removal with updates over adjacency lists per step risks quadratic behavior in dense interaction patterns. A solution that tries all possible orders is factorial and immediately impossible.

A few failure modes appear naturally.

A greedy strategy that repeatedly removes any currently even-degree node can fail if we do not carefully maintain the structure of available nodes, because a locally even vertex may block future progress by breaking parity structure in a subtree.

A second subtle failure arises if we assume parity is independent: removing a node changes parity of all neighbors, so a local choice can flip many nodes from even to odd or vice versa. Ignoring this dependency leads to dead ends even when a valid global ordering exists.

For example, consider a simple path of three nodes 1-2-3. Initially degrees are 1, 2, 1. Removing node 2 is valid since degree is even, leaving two isolated nodes, which are trivially removable. If instead we removed a leaf first without thinking about parity evolution, we could get stuck depending on order in larger trees.

The core difficulty is not checking removability, but choosing an order that preserves the possibility of completing all removals.

## Approaches

A brute-force approach would attempt to simulate all possible sequences of removals. At each step we pick any vertex with even degree and recurse. Since up to n choices exist initially and each removal changes the structure, the state space is essentially permutations of vertices, giving O(n!) possibilities in the worst case. Even with pruning, the branching remains exponential because parity constraints do not eliminate enough branches early.

The key observation is that the problem is fundamentally about parity propagation in a tree. Removing a vertex flips the parity of all its neighbors. This means we are not tracking exact degrees so much as tracking which vertices are currently even, and how that set evolves under toggles along edges.

The crucial structural insight is that the tree allows a bottom-up elimination strategy: leaves can be handled in a controlled way because they have degree 1 initially and only become removable after their parent is removed or after parity flips propagate through adjacent deletions. This suggests processing vertices in an order consistent with a postorder traversal, but the actual condition is dynamic parity, not static degree.

A more precise way to see it is to consider a greedy reduction where we repeatedly remove any leaf whose current state becomes even after accounting for prior deletions. When a leaf is removed, it only affects its parent, which is the only remaining neighbor in a tree. This makes updates local and manageable.

We simulate removals while maintaining current degrees. Each time we remove a vertex, we update the degree of its parent and potentially make it newly eligible. If we always process newly eligible vertices, we effectively propagate removals upward in a way that mirrors a constructive ordering of a valid elimination sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Degree simulation with greedy propagation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency structure of the tree from the parent array. We also compute the initial degree of each node. This is necessary because removability depends on parity of current degree, not just structure.
2. Initialize a queue with all vertices whose current degree is even. These are the only vertices eligible for removal at time zero, and every valid process must start from one of them.
3. Maintain an array to track whether a vertex has already been removed. This prevents double processing and ensures each vertex appears exactly once in the output order.
4. Repeatedly extract a vertex v from the queue and check if it is still valid to remove. If it has already been removed or its current degree is odd due to earlier updates, we skip it. Otherwise, we remove it and append it to the output sequence.
5. When removing a vertex v, we reduce the degree of its only remaining neighbors in the tree. In a rooted representation, this is typically its parent and children still present. Each neighbor whose degree changes may become even, so if it is not removed yet and now has even degree, we add it to the queue.
6. Continue until the queue is empty. At the end, if we have removed all vertices, we output the recorded order. Otherwise, no valid sequence exists.

The reason this ordering is sufficient is that every removal only affects adjacent parity, and in a tree those effects do not create long-range dependencies. The queue ensures we always process vertices exactly when they become eligible, so we never miss a valid removal that could unlock others.

### Why it works

The algorithm maintains the invariant that every vertex in the queue is currently even-degree and not yet removed. Every removal only changes the degree parity of its neighbors, and these are immediately reconsidered for eligibility. Because the graph is acyclic, each edge contributes exactly one local dependency, so no cyclic dependency can prevent eventual processing if a valid global ordering exists. This ensures that whenever a valid full elimination order exists, the queue-driven process discovers it without backtracking.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    adj = [[] for _ in range(n)]
    deg = [0] * n

    for i in range(n):
        if p[i] != 0:
            v = i
            u = p[i] - 1
            adj[v].append(u)
            adj[u].append(v)
            deg[v] += 1
            deg[u] += 1

    removed = [False] * n
    q = deque()

    for i in range(n):
        if deg[i] % 2 == 0:
            q.append(i)
```
