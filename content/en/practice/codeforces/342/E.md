---
title: "CF 342E - Xenia and Tree"
description: "We are working with a tree where every node represents a point in a connected acyclic graph. Initially only node 1 is colored red, while every other node starts blue. Over time, we perform two kinds of operations."
date: "2026-06-06T17:38:06+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "trees"]
categories: ["algorithms"]
codeforces_contest: 342
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 199 (Div. 2)"
rating: 2400
weight: 342
solve_time_s: 82
verified: true
draft: false
---

[CF 342E - Xenia and Tree](https://codeforces.com/problemset/problem/342/E)

**Rating:** 2400  
**Tags:** data structures, divide and conquer, trees  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a tree where every node represents a point in a connected acyclic graph. Initially only node 1 is colored red, while every other node starts blue. Over time, we perform two kinds of operations. One operation turns a chosen blue node red permanently, increasing the set of red nodes. The other operation asks, for a given node, how close it is to the nearest red node in terms of tree distance.

Each query is online, so we must answer type 2 queries immediately as the red set evolves. The key difficulty is that red nodes accumulate over time, and distances are measured on a tree, so recomputing shortest paths from scratch for each query would be far too slow.

The constraints push us toward a solution that is close to linear or logarithmic per query. With up to 100,000 nodes and 100,000 queries, anything that recomputes a BFS or DFS per query immediately degenerates into roughly 10¹⁰ operations in the worst case, which is not viable. Even recomputing distances from all red nodes per query is clearly impossible.

A subtle edge case appears when many consecutive type 2 queries are issued before any new red node is added. In that case, a naive approach might repeatedly recompute distances from scratch even though the answer does not change. Another corner is when red nodes become dense in a small region of the tree, which breaks any solution that assumes a single source or tries to maintain only one “best” red node.

## Approaches

A direct solution would maintain a set of red nodes and, for each query asking for a distance, run a multi-source BFS starting from all red nodes. This is correct because BFS on a tree gives exact distances. However, each such query would cost O(n), and with O(n) queries this becomes O(n²), which is too slow.

The key observation is that the tree structure allows us to separate updates from queries using a centroid decomposition. Instead of trying to answer “distance to any red node” directly, we reframe the problem by maintaining, for every node, information about its path through the centroid decomposition tree.

Each node belongs to O(log n) centroid components. For each centroid in this decomposition, we maintain the minimum distance from that centroid to any red node in its component subtree. When a node becomes red, we update all its ancestor centroids. When we query a node, we combine these stored values across its centroid path and recover the minimum distance to any red node.

This works because every path between two nodes passes through a well-defined set of centroid ancestors, and distances decompose cleanly along those ancestors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS per query | O(nm) | O(n) | Too slow |
| Centroid Decomposition | O(n log n + m log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

We build a centroid decomposition of the tree and maintain, for every centroid, a value representing the minimum distance from that centroid to any currently red node.

1. First, we root the centroid decomposition. At each stage, we compute subtree sizes and select a centroid that splits the current component into balanced parts. This ensures recursion depth is logarithmic.
2. For every node in the original tree, we precompute its distance to each centroid on its centroid path. This is done during decomposition using BFS or DFS from each centroid.
3. We initialize all centroid values to infinity, then set node 1 as red. For node 1, we update all centroids on its path by taking the minimum distance from those centroids to node 1.
4. For a type 1 query, when a node becomes red, we walk up its centroid path. For each centroid ancestor, we update its stored minimum value using the precomputed distance from that centroid to the node.
5. For a type 2 query, we again traverse the centroid path of the queried node. For each centroid ancestor, we combine the stored centroid value with the distance from that centroid to the query node. The minimum over all such combinations is the answer.

The crucial idea is that every path from a query node to any red node must pass through at least one centroid ancestor where both distances are accounted for correctly.

### Why it works

At any moment, each centroid stores the closest red node in its component in terms of distance measured through that centroid. For any query node v and any red node r, there exists a centroid c on the decomposition paths of both v and r such that the path distance dist(v, r) equals dist(v, c) + dist(c, r). Since we store the minimum possible dist(c, r) over all red nodes, checking all centroids on v’s path guarantees that we capture the true minimum distance to any red node.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, q = map(int, input().split())
g = [[] for _ in range(n)]

for _ in range(n - 1):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    g[a].append(b)
    g[b].append(a)

parent_centroid = [-1] * n
sub_size = [0] * n
blocked = [False] * n

centroid_tree = [[] for _ in range(n)]
dist_to_centroid = [[] for _ in range(n)]
centroids_on_path = [[] for _ in range(n)]

INF = 10**18
best = [INF] * n

def dfs_size(v, p):
    sub_size[v] = 1
    for to in g[v]:
        if to != p and not blocked[to]:
            dfs_size(to, v)
            sub_size[v] += sub_size[to]

def dfs_centroid(v, p, total):
    for to in g[v]:
        if to != p and not blocked[to]:
            if sub_size[to] > total // 2:
                return dfs_centroid(to, v, total)
    return v

def add_dist(v, p, c, d):
    dist_to_centroid[v].append(d)
    centroids_on_path[v].append(c)
    for to in g[v]:
        if to != p and not blocked[to]:
            add_dist(to, v, c, d + 1)

def build(c_parent, entry):
    dfs_size(entry, -1)
    c = dfs_centroid(entry, -1, sub_size[entry])
    blocked[c] = True

    parent_centroid[c] = c_parent

    add_dist(c, -1, c, 0)

    for to in g[c]:
        if not blocked[to]:
            build(c, to)

def update(v):
    for i in range(len(centroids_on_path[v])):
        c = centroids_on_path[v][i]
        d = dist_to_centroid[v][i]
        best[c] = min(best[c], d)

def query(v):
    ans = INF
    for i in range(len(centroids_on_path[v])):
        c = centroids_on_path[v][i]
        d = dist_to_centroid[v][i]
        ans = min(ans, best[c] + d)
    return ans

build(-1, 0)

update(0)

for _ in range(q):
    t, v = map(int, input().split())
    v -= 1
    if t == 1:
        update(v)
    else:
        print(query(v))
```

The decomposition is built once using recursive centroid splitting. During construction, each node stores a list of centroids on its path along with distances to them. This allows both updates and queries to operate without traversing the original tree.

The `best` array is the core structure: `best[c]` always represents the minimum distance from centroid `c` to any red node. Updating a node only requires walking its centroid path, which is logarithmic in depth.

A subtle detail is that centroid decomposition must mark nodes as blocked once chosen, otherwise recursion would revisit already decomposed components and break the size guarantees.

## Worked Examples

### Example 1

Input:

```
5 4
1 2
2 3
2 4
4 5
2 1
2 5
1 2
2 5
```

We start with node 1 red.

| Step | Query | Red nodes | Query node | Answer |
| --- | --- | --- | --- | --- |
| 1 | query 1 | {1} | 1 | 0 |
| 2 | query 5 | {1} | 5 | 3 |
| 3 | paint 2 | {1,2} | - | - |
| 4 | query 5 | {1,2} | 5 | 2 |

The second query improves after node 2 becomes red because the path 5 → 4 → 2 is shorter than 5 → 4 → 2 → 1.

This confirms that multiple red sources are handled correctly, not just the initial root.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each node participates in O(log n) centroid levels, and each update/query walks that path |
| Space | O(n log n) | Each node stores centroid path information across decomposition levels |

The logarithmic factor comes from repeated halving of components during centroid decomposition. With 10⁵ nodes and queries, this comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    # Paste solution here as functionally encapsulated version if needed
    # For illustration, assume solve() exists
    return solve()

# sample 1
assert run("""5 4
1 2
2 3
2 4
4 5
2 1
2 5
1 2
2 5
""").strip() == """0
3
2"""

# single node chain
assert run("""3 3
1 2
2 3
2 3
1 2
2 3
""").strip() == """2
1"""

# all nodes already red via updates
assert run("""4 3
1 2
2 3
3 4
2 4
1 3
2 4
""").strip() == """3
1"""

# star shaped tree
assert run("""5 5
1 2
1 3
1 4
1 5
2 5
1 5
2 5
2 2
""").strip() == """1
0
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain updates | mixed distances | propagation along paths |
| star tree | center dominance | centroid correctness |
| incremental activation | evolving set | online updates |

## Edge Cases

A tricky situation is when updates cluster deep in one subtree. In a naive centroid approach, forgetting to propagate updates to all centroid ancestors leads to incorrect distances for nodes outside that subtree. The centroid path structure prevents this because every node shares at least one centroid with every path crossing its region.

Another edge case is when the query node itself becomes red. In that case, the centroid update ensures its own centroid entries become zero-distance sources, so querying it correctly returns zero without special casing.

For a path graph, centroid decomposition degenerates into a balanced split sequence, but each node still maintains O(log n) centroid entries, ensuring queries remain efficient even in worst-case linear structures.
