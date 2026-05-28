---
title: "CF 208E - Blood Cousins"
description: "We are given a rooted forest representing family relationships, where each node corresponds to a person, and each edge points from a child to their parent. A person may have no parent, in which case they are a root of one of the trees in the forest."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 208
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 130 (Div. 2)"
rating: 2100
weight: 208
solve_time_s: 66
verified: true
draft: false
---

[CF 208E - Blood Cousins](https://codeforces.com/problemset/problem/208/E)

**Rating:** 2100  
**Tags:** binary search, data structures, dfs and similar, trees  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted forest representing family relationships, where each node corresponds to a person, and each edge points from a child to their parent. A person may have no parent, in which case they are a root of one of the trees in the forest. For each query, we are asked: given a person `v` and an integer `p`, how many other people share the same `p`-th ancestor as `v`? In other words, how many "p-th cousins" does `v` have?

The input consists of `n` people with their parent information and `m` queries. Both `n` and `m` can be as large as 100,000, meaning any solution with complexity worse than `O(n log n + m log n)` is unlikely to fit in the 2-second time limit. Brute-force approaches that walk up the tree for every query or compare all pairs of nodes are infeasible.

Edge cases include nodes without a `p`-th ancestor. For example, if a node is at depth 2 and we ask for its 3rd ancestor, the answer must be zero because the ancestor does not exist. Another subtle case is nodes in separate trees: they will never share a common ancestor with nodes in other trees, so queries about them must account for forest structure, not just a single tree.

## Approaches

A brute-force approach would traverse up the tree for each query to find the `p`-th ancestor of `v` and then check all other nodes to count which have the same ancestor. This is correct logically but takes `O(n * m)` in the worst case, which is about 10 billion operations and far too slow.

The key observation to optimize is that for each node, the `p`-th ancestor can be computed efficiently using depth information and precomputation. We can precompute the ancestors using either binary lifting or a simple depth-indexed DFS order because the tree is static. Once we know the `p`-th ancestor of each node, the problem reduces to counting nodes at a specific depth within a subtree rooted at that ancestor. This allows us to process queries in `O(log n)` time using techniques like DFS ordering and binary search.

The optimal approach builds the tree, computes the depth and DFS in/out times of each node, and maintains depth-indexed lists of nodes. Then for each query `(v, p)`, we determine `v`'s `p`-th ancestor `u`, and count nodes at the same depth as `v` within `u`'s subtree, excluding `v` itself. Using binary search over sorted DFS-in times gives an `O(log n)` query per node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Optimal | O(n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse input to build the parent array and construct the forest using adjacency lists. Each node points to its children. Identify roots where the parent is zero. This setup is necessary to traverse trees efficiently.
2. Perform a DFS on each root to compute three things for every node: its depth, its DFS-in time, and its DFS-out time. Depth tells us how many generations below the root a node is. DFS-in/out times allow us to represent each subtree as a contiguous interval in the traversal order.
3. For each depth level, maintain a sorted list of DFS-in times of nodes at that depth. This allows us to quickly query how many nodes exist at a particular depth inside a subtree using binary search.
4. Precompute a `2^k`-ancestor table for each node (binary lifting) to quickly find any `p`-th ancestor in `O(log n)`. This table allows us to move up the tree in powers of two efficiently.
5. For each query `(v, p)`, determine the `p`-th ancestor `u` of `v` using the binary lifting table. If `v` does not have a `p`-th ancestor, the answer is zero. Otherwise, retrieve the list of DFS-in times for nodes at `v`'s depth and count how many of these times fall within `u`'s DFS-in/out interval. Subtract one to exclude `v` itself.
6. Collect the answers and output them in the order of queries.

This works because DFS-in/out times ensure that every node in a subtree of `u` has a DFS-in time between `u`'s in and out. Depth-indexed lists guarantee we only consider nodes at the same generation. Binary lifting ensures we can compute ancestors in logarithmic time per query.

## Python Solution

```python
import sys
input = sys.stdin.readline
import bisect

n = int(input())
parents = list(map(int, input().split()))
children = [[] for _ in range(n)]
roots = []

for i, p in enumerate(parents):
    if p == 0:
        roots.append(i)
    else:
        children[p-1].append(i)

LOG = 17  # since 2^17 > 1e5
up = [[-1]*LOG for _ in range(n)]
depth = [0]*n
tin = [0]*n
tout = [0]*n
timer = 0
nodes_by_depth = dict()

def dfs(u, d):
    global timer
    depth[u] = d
    tin[u] = timer
    if d not in nodes_by_depth:
        nodes_by_depth[d] = []
    nodes_by_depth[d].append(timer)
    timer += 1
    for v in children[u]:
        up[v][0] = u
        for k in range(1, LOG):
            if up[v][k-1] != -1:
                up[v][k] = up[up[v][k-1]][k-1]
        dfs(v, d+1)
    tout[u] = timer - 1

for r in roots:
    dfs(r, 0)

def get_kth_ancestor(v, k):
    for i in range(LOG):
        if k & (1 << i):
            v = up[v][i]
            if v == -1:
                break
    return v

m = int(input())
queries = [tuple(map(int, input().split())) for _ in range(m)]
res = []

for v, p in queries:
    v -= 1
    u = get_kth_ancestor(v, p)
    if u == -1:
        res.append(0)
        continue
    d = depth[v]
    arr = nodes_by_depth[d]
    left = bisect.bisect_left(arr, tin[u])
    right = bisect.bisect_right(arr, tout[u])
    res.append(right - left - 1)

print(' '.join(map(str, res)))
```

The first section parses input and builds the adjacency list. DFS assigns depth and DFS-in/out times and fills the dictionary mapping depths to sorted lists of in-times. Binary lifting precomputes ancestors. Queries leverage these precomputations, counting nodes in a depth-sorted array via binary search to stay within logarithmic complexity. Subtracting one removes the node itself from the count.

## Worked Examples

### Sample 1

Input:

```
6
0 1 1 0 4 4
7
1 1
1 2
2 1
2 2
4 1
5 1
6 1
```

| Query | v | p | p-th ancestor u | Nodes at depth of v in u's subtree | Count |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | -1 | - | 0 |
| 2 | 1 | 2 | -1 | - | 0 |
| 3 | 2 | 1 | 1 | [2,3] | 1 |
| 4 | 2 | 2 | -1 | - | 0 |
| 5 | 4 | 1 | -1 | - | 0 |
| 6 | 5 | 1 | 4 | [5,6] | 1 |
| 7 | 6 | 1 | 4 | [5,6] | 1 |

This confirms the DFS and depth tracking allows counting cousins correctly and handles roots and missing ancestors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log n) | DFS takes O(n), binary lifting table fills in O(n log n), each query uses binary search in O(log n) |
| Space | O(n log n) | Store tree, DFS times, binary lifting table, and depth-indexed lists |

With `n` and `m` up to 10^5, operations are under 10^7, well within 2 seconds. Memory usage fits 256 MB limit.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open(__file__).read(), globals())
    return sys.stdout.getvalue().strip()

# provided sample
assert run("6\n0 1 1 0 4 4\n7\n1 1\n1 2\n2 1\n2 2\n4 1\n5 1\n6 1\n") == "0 0 1 0 0 1 1", "sample 1"

# single node
assert run("1\n0\n1\n1 1\n") == "0",
```
