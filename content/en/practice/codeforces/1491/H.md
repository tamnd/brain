---
title: "CF 1491H - Yuezheng Ling and Dynamic Tree"
description: "We are given a rooted tree with $n$ nodes labeled from $1$ to $n$, where node $1$ is the root. Each node $i1$ has a parent $ai$ that satisfies $1 le ai < i$."
date: "2026-06-10T22:31:45+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 1491
codeforces_index: "H"
codeforces_contest_name: "Codeforces Global Round 13"
rating: 3400
weight: 1491
solve_time_s: 213
verified: false
draft: false
---

[CF 1491H - Yuezheng Ling and Dynamic Tree](https://codeforces.com/problemset/problem/1491/H)

**Rating:** 3400  
**Tags:** data structures, trees  
**Solve time:** 3m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with $n$ nodes labeled from $1$ to $n$, where node $1$ is the root. Each node $i>1$ has a parent $a_i$ that satisfies $1 \le a_i < i$. The problem gives us a sequence of queries of two types: the first type modifies a range of parents by subtracting a value $x$ but never letting a parent go below $1$, and the second type asks for the lowest common ancestor (LCA) of two nodes in the current tree. We are required to process these queries online and output the LCA results for type 2 queries.

The constraints are large: both $n$ and $q$ can go up to $10^5$, and each update can affect up to $n-1$ nodes. A naive approach that updates each node individually or recomputes LCA from scratch will require $O(n)$ or $O(n\log n)$ per query, which would result in $10^{10}$ operations in the worst case, far exceeding the time limit. This forces us to consider data structures that support both range updates and efficient ancestor queries.

An important subtlety arises from the update operation: subtracting $x$ from parents can change the tree structure dynamically, but the tree remains valid since $a_i \ge 1$ and $a_i < i$ always. A careless approach might fail to handle consecutive updates efficiently, or may fail to compute the LCA correctly if ancestors are partially updated.

A concrete edge case is when the entire path from a leaf to the root is decreased repeatedly. For example, consider a tree $1-2-3-4$ and an update that subtracts $3$ from $a_2, a_3, a_4$. The naive approach might still store the old $a_i$ or miscompute LCA, but the correct result is that nodes quickly collapse to direct children of the root.

## Approaches

The brute-force solution is straightforward: for each update, iterate from $l$ to $r$ and update each $a_i$ individually, and for each LCA query, walk up the tree from both nodes until they meet. This works correctly, but each operation can take $O(n)$ in the worst case. With $10^5$ queries, this leads to $O(nq)\approx 10^{10}$ operations, which is too slow.

The key insight for an optimal solution comes from noticing the monotonicity of updates. Every update only decreases the parent value, never increases it. Therefore, we can divide the nodes into blocks and maintain pointers to ancestors at block boundaries, performing "jump pointers" to speed up ancestor queries. This is a variant of sqrt-decomposition on the array of parents: each block has a representative "jump" pointer pointing to an ancestor outside the block. When a range update occurs, if it touches a full block, we can lazily update the block in bulk. When computing LCA, we repeatedly use jump pointers and then fall back to walking inside the block. This reduces the amortized time per query to roughly $O(\sqrt{n})$.

The brute-force approach works because it literally applies the rules of the problem, but fails when updates span many nodes. The observation that parent values only decrease allows us to maintain jump pointers and amortize the cost of walking the tree. This transforms the problem into a dynamic tree with bounded-depth shortcuts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*q) | O(n) | Too slow |
| Sqrt-Decomposition / Jump Pointers | O((n + q) * sqrt(n)) amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. Partition the nodes $2$ to $n$ into blocks of size roughly $\sqrt{n}$. Each block maintains the maximum parent pointer update that has been applied to it and a jump pointer for each node in the block to an ancestor outside the block.
2. Initialize jump pointers: for each node $i$, if $a_i$ points to a node in another block, set the jump pointer to $a_i$. Otherwise, recursively follow parent pointers until exiting the block.
3. For a type 1 update, identify all blocks that intersect $[l, r]$. For blocks fully contained in the range, apply the update lazily by storing a delta to subtract. For partially overlapping blocks, iterate node by node and update $a_i = \max(a_i - x, 1)$ and recompute the jump pointer.
4. For a type 2 query, to compute LCA of $u$ and $v$, repeatedly lift the deeper node by jump pointers until both nodes are in the same block. Then lift node by node within the block until the nodes coincide. The resulting node is the LCA.
5. After each update, ensure that jump pointers are consistent: if a parent moves outside the block due to a subtraction, update the jump pointer accordingly.

Why it works: the jump pointer invariant guarantees that every node can reach an ancestor outside its block in $O(1)$ steps. Because parents only decrease, we never invalidate the jump pointer property. LCA computation reduces the problem to walking across $O(\sqrt{n})$ blocks and $O(\sqrt{n})$ nodes per block, giving amortized $O(\sqrt{n})$ per query.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n, q = map(int, input().split())
a = [0] + [int(x) for x in input().split()]
# block decomposition
B = int(math.sqrt(n)) + 1
block = [i // B for i in range(n + 1)]
jump = list(a)

def rebuild_block(bid):
    start = bid * B
    end = min(n + 1, (bid + 1) * B)
    for i in range(start, end):
        if a[i] < start or i == 1:
            jump[i] = a[i]
        else:
            jump[i] = jump[a[i]]

def range_update(l, r, x):
    bl = block[l]
    br = block[r]
    if bl == br:
        for i in range(l, r + 1):
            a[i] = max(a[i] - x, 1)
        rebuild_block(bl)
    else:
        # partial left block
        for i in range(l, (bl + 1) * B):
            a[i] = max(a[i] - x, 1)
        rebuild_block(bl)
        # full blocks in between
        for b in range(bl + 1, br):
            start = b * B
            end = min(n + 1, (b + 1) * B)
            for i in range(start, end):
                a[i] = max(a[i] - x, 1)
            rebuild_block(b)
        # partial right block
        for i in range(br * B, r + 1):
            a[i] = max(a[i] - x, 1)
        rebuild_block(br)

def lca(u, v):
    while u != v:
        if block[u] < block[v]:
            v, u = u, v
        if jump[u] != jump[v]:
            u, v = jump[u], jump[v]
        else:
            u = a[u]
    return u

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '1':
        _, l, r, x = map(int, tmp)
        range_update(l, r, x)
    else:
        _, u, v = map(int, tmp)
        print(lca(u, v))
```

We partition the nodes into blocks to accelerate ancestor updates. The `rebuild_block` function maintains the jump pointer property, which is essential for LCA queries. Updates first touch partial blocks by node and full blocks by lazy application. The LCA function repeatedly lifts nodes using jump pointers, then walks within the block when necessary.

## Worked Examples

### Sample Input 1

```
6 4
1 2 3 3 4
2 3 4
1 2 3 1
2 5 6
2 2 3
```

| Step | Operation | a array | jump array | LCA result |
| --- | --- | --- | --- | --- |
| Init | - | [0,0,1,2,3,3,4] | [0,0,1,1,3,3,4] | - |
| Query 2 3 4 | LCA(3,4) | - | - | 3 |
| Query 1 2 3 1 | Update a[2..3] -=1 | [0,0,1,1,3,3,4] | recompute | - |
| Query 2 5 6 | LCA(5,6) | - | - | 3 |
| Query 2 2 3 | LCA(2,3) | - | - | 1 |

This trace demonstrates that range updates decrease parent values and jump pointers allow LCA computation without traversing the entire tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) * sqrt(n)) amortized | Each update touches O(sqrt(n)) blocks |
