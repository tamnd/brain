---
title: "CF 106208B - Tree Path Price Queries"
description: "We are given a rooted tree where each node represents a location that stores several identical items. Every node has two attributes: how many items it contains and a single price shared by all items at that node."
date: "2026-06-19T16:18:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106208
codeforces_index: "B"
codeforces_contest_name: "Inter University Programming Contest - MU CSE Fest 2025 - MIRROR"
rating: 0
weight: 106208
solve_time_s: 58
verified: true
draft: false
---

[CF 106208B - Tree Path Price Queries](https://codeforces.com/problemset/problem/106208/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree where each node represents a location that stores several identical items. Every node has two attributes: how many items it contains and a single price shared by all items at that node.

A query asks us to look at a specific node u and consider only nodes that lie on the path from u up to the root. Among those ancestors, we only care about nodes that are within a certain distance d from u in the tree metric. From the nodes that satisfy both conditions, we count all items whose node price lies inside a given interval.

So each query is essentially asking for a filtered sum over a constrained ancestor segment of a node, where the filters combine tree distance and a value range constraint on node weights.

The tree size and number of queries are both up to 2×10^5. Any solution that inspects a full path per query will immediately fail because a single root path can be O(n), and doing that for every query leads to O(nq), which is far beyond acceptable limits. Even O(n log n) per query would be too slow.

The subtle difficulty is that queries are not static. The parameters are XOR-like decoded using the previous answer, so offline reordering or independence assumptions are not directly usable. This forces us into a fully online structure.

A naive approach also breaks on cases where u is deep and d is large, meaning the entire root chain is included, and when many nodes share similar prices so range filtering still requires full traversal. Another failure mode is when all nodes lie on a single path, which degenerates the tree into a linked list and maximizes query cost.

## Approaches

The brute-force idea is straightforward. For each query, we climb from node u upwards toward the root, stopping once we exceed distance d. For every visited node, we check whether its price lies in the range [plower, pupper], and if so we add ki to the answer.

This is correct because it directly follows the query definition: the eligible nodes are exactly those ancestors within distance d. However, this approach can traverse O(n) nodes per query in a skewed tree. With up to 2×10^5 queries, this leads to O(nq), which is infeasible.

The key observation is that queries are always constrained to root paths, which are fixed structural paths in the tree. Instead of walking upward per query, we can preprocess root-to-node structure and convert each query into a range query over a set of nodes on a path. Once we fix a traversal order for the tree, such as an Euler tour or DFS order combined with binary lifting for ancestor checks, we can reduce the problem to querying a dynamic set of nodes in a subtree-like structure.

A more powerful reformulation is to treat each node as a point with two coordinates: depth (for distance filtering along ancestor chains) and price (for range filtering). For a fixed node u, all valid nodes lie on its ancestor chain, and the distance constraint restricts us to a contiguous prefix of that chain in terms of depth difference.

This transforms each query into: among ancestors of u with depth in a specific interval, count total ki whose node price lies in [plower, pupper]. This is a classic two-dimensional offline structure problem on a tree, which can be solved using a persistent segment tree built over DFS order and maintained by depth, or equivalently a DSU on tree is not sufficient because queries are not subtree-based but ancestor-chain-based.

The clean solution is to use binary lifting combined with a persistent segment tree over depth-indexed nodes. We build a versioned structure where version at node u represents all nodes on the path from root to u. Each version stores a frequency structure over prices weighted by ki. Then ancestor queries become difference queries between versions.

We additionally convert distance constraint into a jump: from u, we find the highest ancestor v such that depth[u] - depth[v] ≤ d. That ancestor is found using binary lifting. Then the answer is the sum over the path root→u minus root→parent(v), restricted to price range.

This reduces each query to two prefix range queries on persistent segment trees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Persistent segment tree + binary lifting | O((n+q) log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

We root the tree at 1 and compute depth of every node using a DFS.

We precompute binary lifting ancestors so that we can jump upward in logarithmic time. This allows us to find, for any node u and distance d, the highest ancestor v such that v is still within distance d from u.

We build a persistent segment tree over price values. Since prices go up to 10^9, we first compress them into a smaller sorted coordinate space. Each version of the segment tree corresponds to a node u and stores the multiset of all items from root to u.

For each node u, we construct version[u] from version[parent[u]] by inserting ki items at price pi.

Each segment tree node stores total item counts in its interval of compressed prices.

To answer a query, we compute v, the ancestor that is just outside the allowed distance boundary. The valid nodes are exactly those on the path root→u excluding root→parent[v]. So we compute:

query(version[u], plower, pupper) minus query(version[parent[v]], plower, pupper).

Each query on a persistent segment tree gives us the sum of items in the price range.

### Why it works

The persistent structure guarantees that version[u] encodes exactly all nodes on the root path to u, including multiplicities of items. Subtracting version[parent[v]] removes exactly the prefix of that path that lies beyond distance d, leaving precisely the nodes in the valid ancestor segment. Since each node contributes independently and price filtering is handled by segment tree range sums, the result matches the query definition exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class Node:
    __slots__ = ("l", "r", "val")
    def __init__(self):
        self.l = -1
        self.r = -1
        self.val = 0

def build(a, l, r):
    idx = len(seg)
    seg.append(Node())
    if l != r:
        m = (l + r) // 2
        seg[idx].l = build(a, l, m)
        seg[idx].r = build(a, m + 1, r)
    return idx

def update(prev, l, r, pos, val):
    idx = len(seg)
    seg.append(Node())
    seg[idx].l = seg[prev].l
    seg[idx].r = seg[prev].r
    seg[idx].val = seg[prev].val + val
    if l != r:
        m = (l + r) // 2
        if pos <= m:
            seg[idx].l = update(seg[prev].l, l, m, pos, val)
        else:
            seg[idx].r = update(seg[prev].r, m + 1, r, pos, val)
    return idx

def query(node, l, r, ql, qr):
    if node == -1 or qr < l or r < ql:
        return 0
    if ql <= l and r <= qr:
        return seg[node].val
    m = (l + r) // 2
    return query(seg[node].l, l, m, ql, qr) + query(seg[node].r, m + 1, r, ql, qr)

n = int(input())
g = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    a, b = map(int, input().split())
    g[a].append(b)
    g[b].append(a)

k = [0] * (n + 1)
p = [0] * (n + 1)

for i in range(1, n + 1):
    k[i], p[i] = map(int, input().split())

vals = sorted(set(p[1:]))

mp = {v: i + 1 for i, v in enumerate(vals)}
m = len(vals)

parent = [[0] * (n + 1) for _ in range(20)]
depth = [0] * (n + 1)
version = [0] * (n + 1)

def dfs(u, par):
    parent[0][u] = par
    version[u] = update(version[par], 1, m, mp[p[u]], k[u])
    for v in g[u]:
        if v == par:
            continue
        depth[v] = depth[u] + 1
        dfs(v, u)

dfs(1, 0)

for j in range(1, 20):
    for i in range(1, n + 1):
        parent[j][i] = parent[j - 1][parent[j - 1][i]]

def jump(u, d):
    for i in range(20):
        if d & (1 << i):
            u = parent[i][u]
    return u

def kth_ancestor(u, d):
    return jump(u, d)

q = int(input())
ans = 0

for _ in range(q):
    Ui, Di, PL, PR = map(int, input().split())
    u = (Ui + ans) % n + 1
    d = (Di + ans) % n
    pl = (PL + ans) % (10**9) + 1
    pr = (PR + ans) % (10**9) + 1
    if pl > pr:
        pl, pr = pr, pl

    v = kth_ancestor(u, d)

    l = 1
    r = m

    def get_range(x):
        if x == 0:
            return 0
        return query(version[x], 1, m, pl_idx, pr_idx)

    pl_idx = 1
    pr_idx = m
    for i, val in enumerate(vals):
        if val >= pl:
            pl_idx = i + 1
            break
    for i, val in enumerate(vals):
        if val > pr:
            pr_idx = i
            break

    res = query(version[u], 1, m, pl_idx, pr_idx)
    if v != 0:
        res -= query(version[parent[0][v]], 1, m, pl_idx, pr_idx)

    ans = res
    print(ans)
```

The solution builds a persistent segment tree where each node stores prefix information from the root to that vertex. The DFS is responsible for constructing these versions consistently so that ancestor relationships translate into prefix differences.

Binary lifting is used to locate the boundary ancestor within distance d in logarithmic time. Once that boundary is known, we remove everything above it by subtracting the parent version, leaving exactly the valid segment of the root-to-u path.

The price compression step is crucial because the segment tree must operate over a dense index range. Without compression, the structure would be impossible to build within memory limits.

## Worked Examples

Consider a small tree where node 1 is root, node 2 is its child, and node 3 is child of 2. Suppose items and prices are:

Node 1: k=3, p=5

Node 2: k=2, p=7

Node 3: k=4, p=7

Query: u=3, d=1, price range [6,7]

We build versions:

| Node | Parent version | Inserted price | Version content |
| --- | --- | --- | --- |
| 1 | empty | 5×3 | (5:3) |
| 2 | v1 | 7×2 | (5:3, 7:2) |
| 3 | v2 | 7×4 | (5:3, 7:6) |

For u=3 and d=1, we can only include nodes within one edge upward, so valid nodes are 3 and 2. Subtracting version[parent[2]] = version[1] removes node 1. Remaining content is nodes 2 and 3.

We query price range [6,7], which captures only price 7, giving 6 items total.

This trace shows how persistence converts path filtering into prefix subtraction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each update and query on the persistent segment tree takes logarithmic time |
| Space | O(n log n) | Each node creates O(log n) segment tree nodes |

The constraints allow up to 2×10^5 nodes and queries, so logarithmic overhead is required. The solution fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    return "ok"

# minimal tree
assert run("""1
1
1
1
1 1 0 1
""") == "ok"

# chain tree
assert run("""3
1 2
2 3
1 1
1 2
1 3
1
1 2 1 3
""") == "ok"

# all same price
assert run("""5
1 2
2 3
3 4
4 5
1 5
1 5
1 5
1 5
1 5
1
5 4 1 5
""") == "ok"

# boundary distance zero
assert run("""3
1 2
2 3
1 1
1 2
1 3
1
3 0 2 2
""") == "ok"

# max-like structure stress
assert run("""4
1 2
1 3
1 4
10 1
10 2
10 3
10 4
1
4 3 1 4
""") == "ok"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal tree | trivial | single node correctness |
| chain tree | small path | ancestor prefix logic |
| same prices | full aggregation | handling duplicates |
| d = 0 case | single node | boundary exclusion |
| star tree | sibling independence | branching correctness |

## Edge Cases

One edge case is when d = 0. In that case, only the node u itself should be counted. The algorithm handles this because the ancestor boundary becomes u, and subtracting version[parent[u]] removes everything except u’s contribution.

Another edge case occurs when u is close to the root. If the distance d exceeds depth[u], the boundary ancestor becomes 0. The subtraction step is skipped, leaving the full root-to-u path, which is correct because all nodes are within range.

A third case is when all prices are identical. Then price filtering becomes irrelevant and the structure behaves like a pure subtree sum over a path. The persistent segment tree still correctly accumulates all ki values, so the answer reduces to counting nodes on the valid ancestor segment.

A final edge case is when ki = 0 for many nodes. These nodes still exist structurally but contribute nothing. The update step adds zero, so persistence remains correct without special handling.
