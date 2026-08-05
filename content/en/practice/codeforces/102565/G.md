---
title: "CF 102565G - Puppetteer"
description: "We have a rooted tree. Every vertex owns a unique number between 1 and N, so the numbers form a permutation of the vertices. For every vertex v, we look only at the vertices inside v's subtree and collect their numbers. These numbers create several maximal consecutive ranges."
date: "2026-08-05T14:19:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102565
codeforces_index: "G"
codeforces_contest_name: "AGM 2020, Final Round, Day 2"
rating: 0
weight: 102565
solve_time_s: 117
verified: true
draft: false
---

[CF 102565G - Puppetteer](https://codeforces.com/problemset/problem/102565/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree. Every vertex owns a unique number between 1 and N, so the numbers form a permutation of the vertices. For every vertex v, we look only at the vertices inside v's subtree and collect their numbers. These numbers create several maximal consecutive ranges. The task is to count those ranges for every vertex.

For example, if a subtree contains the values `{2,3,4,8,10,11}`, the compact intervals are `[2,4]`, `[8,8]`, and `[10,11]`, so the answer for this subtree is 3.

The challenge comes from needing this answer for every subtree. With N reaching 250000 and the total size of all tests reaching 500000, rebuilding the set of values for every vertex is impossible. A quadratic approach can perform around N² operations on a chain-shaped tree, which is far beyond what a two second limit allows. We need a solution close to linear or N log N.

The tricky cases are caused by the fact that compact intervals depend on neighboring values, not on the tree structure directly. A single inserted value can merge two existing intervals or create a new one.

Consider a tree with one vertex:

```
1
```

with value `1`. The answer is:

```
1
```

A solution that counts adjacent pairs instead of maximal ranges would fail because a single value is still a compact interval.

Another case:

```
1
|
2
```

with values:

```
[2,3]
```

The subtree of vertex 1 contains `{2,3}`, so the answer is `1`. A careless implementation that checks only whether every value has a successor would miss that `[2,3]` is one complete interval.

A final important case is merging:

```
values = {1,3}
```

There are two intervals, `[1,1]` and `[3,3]`. Adding value `2` changes the answer from 2 to 1 because the new value connects both sides. Any update formula that only counts new isolated values will be incorrect.

## Approaches

The direct approach is to process every subtree independently. For each vertex, we collect all values below it, sort them, and count the breaks between consecutive numbers. This is correct because compact intervals are exactly the maximal groups where consecutive values differ by one.

However, in a chain tree, the root subtree contains N vertices, the next subtree contains N-1 vertices, and so on. Sorting every subtree gives roughly:

```
N + (N-1) + ... + 1 = O(N²)
```

values processed even before sorting costs are considered.

The key observation is that we do not need the whole sorted set. When we insert a value x into a maintained set, only the presence of x-1 and x+1 matters.

If neither neighbor exists, x creates a new interval.

If one neighbor exists, x extends an existing interval.

If both neighbors exist, x joins two intervals into one.

Therefore the number of compact intervals can be maintained dynamically while traversing subtrees.

To answer all subtree queries efficiently, we use the DSU on tree technique, also called small-to-large merging. For each vertex we keep the largest child's data structure and reuse it. The smaller child subtrees are added into this structure temporarily. Since every vertex moves only O(log N) times between structures, the total work is O(N log N).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N² log N) | O(N) | Too slow |
| DSU on Tree | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex 1 and compute the size of every subtree. During this DFS, store the heavy child of each vertex, meaning the child with the largest subtree.
2. Traverse the tree using DSU on tree. First process every light child without keeping its data afterwards. Then process the heavy child while keeping its maintained set.
3. After the heavy child is processed, add all vertices from the light child subtrees and the current vertex into the maintained set. The current value of the interval counter now represents the answer for this subtree.
4. Save the current counter as the answer of the vertex. If this subtree was not marked as kept, remove all its vertices from the maintained structure so that the parent call can continue correctly.

The maintained invariant is that the active set always contains exactly the vertices belonging to the currently processed DSU subtree. The interval counter is updated only through local changes caused by adding or removing one value, so it always equals the number of compact intervals in that set.

When inserting x, the change is:

```
+1 - (x-1 exists) - (x+1 exists)
```

When deleting x, the inverse change is:

```
-1 + (x-1 exists) + (x+1 exists)
```

These formulas cover all cases, including splitting and merging intervals.

## Python Solution

```python
import sys
sys.setrecursionlimit(1 << 20)

input = sys.stdin.readline

def solve():
    n = int(input())
    val = [0] + list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        g[a].append(b)
        g[b].append(a)

    size = [1] * (n + 1)
    heavy = [0] * (n + 1)
    parent = [0] * (n + 1)

    def dfs(v, p):
        parent[v] = p
        best = 0
        for u in g[v]:
            if u == p:
                continue
            dfs(u, v)
            size[v] += size[u]
            if size[u] > best:
                best = size[u]
                heavy[v] = u

    dfs(1, 0)

    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    order = []

    def euler(v, p):
        tin[v] = len(order)
        order.append(v)
        for u in g[v]:
            if u != p:
                euler(u, v)
        tout[v] = len(order)

    euler(1, 0)

    present = [False] * (n + 2)
    ans = [0] * (n + 1)
    current = 0

    def add_vertex(v):
        nonlocal current
        x = val[v]
        current += 1
        if present[x - 1]:
            current -= 1
        if present[x + 1]:
            current -= 1
        present[x] = True

    def remove_vertex(v):
        nonlocal current
        x = val[v]
        present[x] = False
        current -= 1
        if present[x - 1]:
            current += 1
        if present[x + 1]:
            current += 1

    def add_subtree(v):
        for i in range(tin[v], tout[v]):
            add_vertex(order[i])

    def remove_subtree(v):
        for i in range(tin[v], tout[v]):
            remove_vertex(order[i])

    def dfs2(v, p, keep):
        for u in g[v]:
            if u != p and u != heavy[v]:
                dfs2(u, v, False)

        if heavy[v]:
            dfs2(heavy[v], v, True)

        for u in g[v]:
            if u != p and u != heavy[v]:
                add_subtree(u)

        add_vertex(v)
        ans[v] = current

        if not keep:
            remove_subtree(v)

    dfs2(1, 0, True)

    print(*ans[1:])

t = int(input())
for _ in range(t):
    solve()
```

The first DFS computes subtree sizes and identifies the heavy child. The second DFS is the DSU-on-tree traversal. The `present` array stores whether a value is currently inside the active subtree.

The interval counter is updated before changing `present[x]` during insertion because the old neighbors describe the existing intervals. During deletion, the value is removed first and then the neighbors are checked because the value itself must no longer be considered present.

Python integers are arbitrary precision, so no overflow handling is required. The recursion limit is increased because a tree can be a chain with depth N. The Euler order allows adding or removing a whole subtree by iterating through one contiguous segment.
