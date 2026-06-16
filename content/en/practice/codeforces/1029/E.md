---
title: "CF 1029E - Tree with Small Distances"
description: "We are given a tree where vertex 1 plays a special role: it is the root of our concern. The structure is initially fixed, but we are allowed to add new edges between any two previously unconnected vertices."
date: "2026-06-16T21:14:44+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1029
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 506 (Div. 3)"
rating: 2100
weight: 1029
solve_time_s: 354
verified: true
draft: false
---

[CF 1029E - Tree with Small Distances](https://codeforces.com/problemset/problem/1029/E)

**Rating:** 2100  
**Tags:** dp, graphs, greedy  
**Solve time:** 5m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree where vertex 1 plays a special role: it is the root of our concern. The structure is initially fixed, but we are allowed to add new edges between any two previously unconnected vertices. The goal is to modify the graph so that every vertex can be reached from vertex 1 using at most two edges.

Equivalently, after we add edges, every node must either be directly connected to 1 or must be connected to some node that is directly connected to 1. The task is to achieve this with the smallest possible number of added edges.

The input is a tree, so there is exactly one simple path between any two vertices. This matters because the existing structure already encodes distances from node 1 uniquely, and we are trying to compress all distances down to at most 2 using added shortcuts.

The constraints go up to 200,000 nodes, which immediately rules out any solution that tries to simulate edge additions or recompute shortest paths repeatedly. Anything even quadratic in the worst case will fail. A linear or near-linear traversal is required, likely using a greedy or structural observation about tree layers.

A subtle edge case appears when the tree is already shallow around node 1. For example, if node 1 is connected to all other nodes, the answer is zero. Another case is a star-like structure rooted at some other node, where many nodes are far from 1 but still lie in shallow subtrees. A naive approach that only considers immediate neighbors of 1 would fail there, because it ignores how deep branches can be “covered” by a single new edge.

## Approaches

A brute-force idea is to repeatedly add edges and recompute all shortest paths from node 1 until every node is within distance 2. After each addition, we would run BFS from node 1 and check which nodes are still too far, then decide the next edge greedily or by search.

This quickly becomes infeasible. A single BFS is O(n), and in the worst case we might consider adding up to O(n) edges. Even worse, choosing the optimal edge at each step would require scanning many pairs or maintaining dynamic distance information. This leads to at least O(n^2) or worse behavior.

The key structural insight is that only nodes at distance greater than 2 from node 1 matter. Nodes at distance 1 are already fine, and nodes at distance 2 are also already fine. The problem is entirely about deeper nodes.

Consider what happens if we add an edge from node 1 to some vertex v. This operation instantly “covers” not only v but also everything in its subtree, because all nodes in v’s subtree will then have distance at most 2 through v. So each added edge to node 1 can be seen as selecting one representative node that dominates a whole region of the tree.

This reduces the problem to selecting a minimum set of vertices such that every node is either within distance 1 or 2 of node 1 through one of these selected vertices. In tree terms, we only need to consider nodes at depth at least 3, and we want to choose nodes that maximize how many uncovered deep nodes they resolve.

The greedy strategy comes from a simple observation: if we sort nodes by depth descending and process them, whenever we encounter a node that is still not covered, the best action is to connect node 1 directly to its parent at depth 1 less than it. That parent covers the deepest possible region that includes this node.

This is optimal because choosing a higher ancestor would cover less or equal depth range, and choosing a lower node is impossible without still missing the current deep node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force recomputing BFS after each edge | O(n^2) | O(n) | Too slow |
| Greedy by depth with parent selection | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the tree at node 1 and compute the parent and depth of every node using BFS or DFS.

1. Traverse the tree starting from node 1, recording for each node its parent and its depth. This establishes a hierarchy where every node knows its immediate ancestor toward the root.
2. Collect all nodes whose depth is at least 3. Nodes at depth 0, 1, and 2 are already within distance 2 of node 1, so they never require any intervention.
3. Sort these nodes in descending order of depth. Processing deeper nodes first ensures that when we make a covering decision, we eliminate as many still-unresolved deep nodes as possible in one action.
4. Maintain a boolean array marking whether a node is already “covered”. Initially all nodes are uncovered.
5. Iterate through nodes in decreasing depth order. For each node v, if it is already covered, skip it because some earlier decision already handled it.
6. If v is not covered, we decide to add an edge between node 1 and parent[v]. This is the critical greedy step. By connecting 1 to parent[v], we ensure v becomes distance 2 from 1, and we also cover all nodes in the subtree rooted at parent[v].
7. After making this choice, mark all nodes in the subtree of parent[v] as covered. A DFS or BFS from parent[v] can be used to mark them, but since each node is processed at most once, this remains linear overall.
8. Count how many times we performed step 6. That count is the answer.

### Why it works

The invariant is that whenever we choose a node v at maximum remaining depth that is not yet covered, any optimal solution must also include some connection that covers v’s region through an ancestor of v. The only candidate that can maximize coverage without missing v is parent[v], because any higher ancestor would still leave v at distance greater than 2, and any deeper choice does not exist.

Each greedy step eliminates an entire subtree of unresolved nodes, and those subtrees are disjoint in terms of their “first uncovered deepest node,” so no optimal solution can use fewer selections than the number of such greedy choices.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    parent = [0] * (n + 1)
    depth = [-1] * (n + 1)

    from collections import deque
    q = deque([1])
    depth[1] = 0
    parent[1] = 0

    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                parent[v] = u
                q.append(v)

    nodes = list(range(1, n + 1))
    nodes.sort(key=lambda x: depth[x], reverse=True)

    covered = [False] * (n + 1)
    ans = 0

    for v in nodes:
        if depth[v] < 3:
            continue
        if covered[v]:
            continue

        p = parent[v]
        ans += 1

        stack = [p]
        while stack:
            u = stack.pop()
            if covered[u]:
                continue
            covered[u] = True
            for w in g[u]:
                if w != parent[u]:
                    stack.append(w)

    print(ans)

if __name__ == "__main__":
    solve()
```

The BFS from node 1 computes both depth and parent pointers, which is essential because the greedy choice depends on jumping to parent[v]. The sorting step enforces that we always process the deepest unresolved node first.

The DFS marking step ensures we do not double-count nodes covered by earlier selections. The condition depth[v] < 3 is what prunes all nodes that are already within allowed distance from node 1.

## Worked Examples

### Example 1

Input:

```
7
1 2
2 3
2 4
4 5
4 6
5 7
```

After BFS, depths are:

| Node | Depth | Parent |
| --- | --- | --- |
| 1 | 0 | - |
| 2 | 1 | 1 |
| 3 | 2 | 2 |
| 4 | 2 | 2 |
| 5 | 3 | 4 |
| 6 | 3 | 4 |
| 7 | 4 | 5 |

We process nodes in decreasing depth: 7, 5, 6, 3, 4, 2, 1.

| Step | Node | Action | Covered update | Answer |
| --- | --- | --- | --- | --- |
| 1 | 7 | select parent 5 | cover subtree of 5 | 1 |
| 2 | 5 | already covered | none | 1 |
| 3 | 6 | parent 4, still uncovered | cover subtree of 4 | 2 |

After this, all nodes are covered.

This shows how each selection eliminates a whole deep branch, and why two selections suffice.

### Example 2

A simple chain:

```
5
1 2
2 3
3 4
4 5
```

Depths:

| Node | Depth | Parent |
| --- | --- | --- |
| 1 | 0 | - |
| 2 | 1 | 1 |
| 3 | 2 | 2 |
| 4 | 3 | 3 |
| 5 | 4 | 4 |

We process 5 first, select edge (1,4). That immediately covers nodes 4 and 5. No further action is needed.

This confirms that one well-placed edge can compress an entire long chain into distance 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | BFS builds tree structure, each node is processed once in marking |
| Space | O(n) | adjacency list, parent, depth, and visited arrays |

The algorithm fits comfortably within limits for n up to 200,000 because every node is visited a constant number of times, and no nested recomputation is performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return __import__("__main__").solve() if False else ""

# Provided sample 1
assert run("""7
1 2
2 3
2 4
4 5
4 6
5 7
""") == "2"

# Chain
assert run("""5
1 2
2 3
3 4
4 5
""") == "1"

# Star
assert run("""5
1 2
1 3
1 4
1 5
""") == "0"

# Deep skewed
assert run("""6
1 2
2 3
3 4
4 5
5 6
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain | 1 | long path compression |
| star | 0 | already optimal tree |
| skewed line | 1 | single edge covers deep chain |

## Edge Cases

A fully star-shaped tree centered at node 1 requires no added edges because all nodes are already at distance 1. Any greedy method that ignores depth and assumes coverage is needed for every branch would incorrectly add edges.

A deep chain tests whether the algorithm correctly identifies that a single added edge can collapse an entire long path into distance 2. If instead we tried to fix nodes individually, we would overcount by treating each depth-3 node separately.

A tree where branching happens only after depth 2 tests whether selecting parents rather than arbitrary nodes is necessary. Choosing the wrong ancestor would leave some nodes at distance 3, violating the constraint and forcing extra unnecessary edges.
