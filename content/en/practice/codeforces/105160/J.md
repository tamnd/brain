---
title: "CF 105160J - \u4e0a\u5b66"
description: "We are given a tree with nodes labeled from 1 to n, plus an extra node 0. Node 0 is connected to node 1, so effectively node 0 acts like a root attached above the original tree. Every other edge connects the n student locations into a tree. Each student lives at a unique node i."
date: "2026-06-27T11:02:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105160
codeforces_index: "J"
codeforces_contest_name: "2024 University of Shanghai for Science and Technology(USST) Freshman Challenge Contest"
rating: 0
weight: 105160
solve_time_s: 69
verified: true
draft: false
---

[CF 105160J - \u4e0a\u5b66](https://codeforces.com/problemset/problem/105160/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with nodes labeled from 1 to n, plus an extra node 0. Node 0 is connected to node 1, so effectively node 0 acts like a root attached above the original tree. Every other edge connects the n student locations into a tree.

Each student lives at a unique node i. A bus route is a trail that never repeats an edge and always finishes at node 0. A student can only board a bus at their own node, and once they board, they ride along that bus until it reaches node 0.

Because the graph is a tree, any edge-simple route ending at node 0 behaves like a downward-to-upward path toward the root: it cannot branch and cannot revisit edges, so it effectively corresponds to choosing a start node and walking along the unique simple path toward node 0.

A key consequence is that a single bus can serve multiple students if and only if all those students lie on a single rootward path, meaning their nodes are arranged on one ancestor chain in the rooted tree (rooted at node 0).

We are asked to count how many ways to choose 3 students such that they are not all served by a single bus. In other words, we count all triples of nodes except those where the three nodes lie on a single root-to-leaf path.

The constraint n up to 2 × 10^5 implies that any solution must be near linear or O(n log n). Anything quadratic over pairs or triples of nodes will be far too slow. Even O(n^{4/3}) style solutions are unnecessary here because the structure is a tree and suggests a simple combinational count after preprocessing.

A subtle edge case arises from misunderstanding what “same bus” means. It is not about connectivity in the original tree, but about lying on one ancestor chain. For example, in a star centered at node 1, nodes 2, 3, 4 are not on a single path, so any triple involving them is valid. In contrast, in a chain 4-3-2-1-0, any three nodes along that chain are invalid because one bus from 4 to 0 passes through all of them.

## Approaches

A direct approach would enumerate all triples of nodes and check whether they lie on a single root-to-0 path. Checking this condition requires verifying whether one node is the deepest among them and whether the other two are ancestors of it. This can be done using parent pointers or LCA queries in O(1) or O(log n), but enumerating all triples costs O(n^3), which is impossible for n = 2 × 10^5.

The key observation is to flip the perspective. Instead of checking triples, we count the bad ones. A triple is bad exactly when all three nodes lie on a single ancestor chain in the rooted tree.

Now fix a node v as the deepest node in such a triple. The other two nodes must be chosen among the ancestors of v (excluding v itself or including it carefully depending on formulation). Once we define depth properly, each bad triple has a unique deepest node, which avoids double counting.

This reduces the problem to a purely combinational sum over nodes after computing depths with a single DFS or BFS from node 0.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over triples | O(n^3) | O(1) | Too slow |
| Depth counting on tree | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the tree at node 0 and compute the depth of every node, where depth[v] is the number of student nodes on the path from v up to node 0, including v itself.

1. Build adjacency list of the tree, including node 0 connected to node 1.
2. Run a BFS or DFS from node 0 to compute parent relationships and depths. We set depth[0] = 0, and for any child u of v, depth[u] = depth[v] + 1. This ensures depth[v] counts how many student nodes lie on the path from v to the root side excluding node 0.
3. Precompute the total number of triples of students as C(n, 3). This represents all possible selections.
4. Compute the number of bad triples. For each node v, treat v as the deepest node in the triple. Then the other two nodes must be chosen among the ancestors of v that are also student nodes, of which there are depth[v] - 1.

So the contribution of v is C(depth[v] - 1, 2), provided depth[v] ≥ 3.
5. Sum this value over all nodes v.
6. The answer is total triples minus bad triples.

The reason this decomposition works is that every valid “same bus” triple corresponds to exactly one deepest node in the tree order. Once that node is fixed, the remaining two nodes are uniquely constrained to lie above it.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
adj = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

# include node 0 connected to 1
adj.append([])  # index n+1 unused (just safety, not needed)
adj[0] = [1]
adj[1].append(0)

parent = [-1] * (n + 1)
depth = [0] * (n + 1)

stack = [0]
parent[0] = 0

while stack:
    v = stack.pop()
    for u in adj[v]:
        if u == parent[v]:
            continue
        parent[u] = v
        depth[u] = depth[v] + 1
        stack.append(u)

def C2(x):
    return x * (x - 1) // 2

total = n * (n - 1) * (n - 2) // 6
bad = 0

for v in range(1, n + 1):
    if depth[v] >= 3:
        bad += C2(depth[v] - 1)

print(total - bad)
```

The code first constructs the tree and explicitly adds the connection between node 0 and node 1. A DFS computes parent and depth arrays rooted at node 0.

The function C2(x) computes binomial coefficients for pairs efficiently. For each node v, we interpret depth[v] - 1 as the number of valid ancestors among student nodes above v. Choosing any two of them together with v forms a bad triple.

Finally, we subtract these from the total number of triples.

A common pitfall is misdefining depth: if depth starts from node 1 instead of node 0, the combinational formula breaks. Another issue is forgetting that node 0 is not a student and must not be included in combinations.

## Worked Examples

### Example 1

Consider a simple chain: 3-2-1-0.

Depths are:

node 1: 1, node 2: 2, node 3: 3.

| v | depth[v] | bad contribution C(depth[v]-1,2) |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 3 | 1 |

Total triples are C(3,3) = 1.

Bad triples = 1 (the triple {1,2,3}).

Answer = 0.

This confirms that in a chain all triples are invalid because they lie on one path.

### Example 2

Consider a star: node 1 connected to 0, and nodes 2, 3, 4 connected to 1.

Depths:

node 1 = 1, nodes 2,3,4 = 2.

| v | depth[v] | contribution |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 0 |
| 4 | 2 | 0 |

Total triples = C(4,3) = 4.

Bad triples = 0.

Answer = 4.

This shows that in a branching structure, no three nodes lie on a single ancestor chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One DFS for depths and one linear pass over nodes |
| Space | O(n) | Adjacency list and auxiliary arrays |

The algorithm fits easily within constraints since both memory and runtime scale linearly with the number of nodes, and n can be as large as 2 × 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import comb

    n = int(_sys.stdin.readline())
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, _sys.stdin.readline().split())
        adj[u].append(v)
        adj[v].append(u)

    adj.append([])
    adj[0] = [1]
    adj[1].append(0)

    parent = [-1] * (n + 1)
    depth = [0] * (n + 1)

    stack = [0]
    parent[0] = 0

    while stack:
        v = stack.pop()
        for u in adj[v]:
            if u == parent[v]:
```
