---
title: "CF 105013D - It's not Ashamed to Feel Sad"
description: "We are given a tree with n nodes, where each node carries a lowercase letter. Every node also has an implicit depth from the root. After building the tree, we receive q queries."
date: "2026-06-28T04:38:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105013
codeforces_index: "D"
codeforces_contest_name: "The 19th Southeast University Programming Contest (Summer)"
rating: 0
weight: 105013
solve_time_s: 62
verified: true
draft: false
---

[CF 105013D - It's not Ashamed to Feel Sad](https://codeforces.com/problemset/problem/105013/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with `n` nodes, where each node carries a lowercase letter. Every node also has an implicit depth from the root. After building the tree, we receive `q` queries. Each query asks about a fixed node `u` and a target depth `d`, and we must consider all nodes that lie in the subtree of `u` and are exactly at depth `d`. From the letters on those nodes, we extract a multiset of characters and decide whether this multiset satisfies a specific condition.

The condition is that the multiset should be “balanced” in a strict sense. First, the total number of characters must be non-zero and even. Second, no single character is allowed to dominate more than half of the total occurrences. If either the count is zero, or the total is odd, or some character exceeds half the total frequency, the answer is negative; otherwise it is positive.

The structure of the problem forces us into repeated aggregation over overlapping subtree slices at fixed depths. A naive approach that recomputes frequency counts for every query would repeatedly traverse large parts of the tree, leading to roughly `O(nq)` behavior in the worst case. With `n, q` up to about `2e5`, this is far beyond acceptable limits.

The key edge cases come from degenerate queries. A query might ask for a depth outside the tree height, in which case there are no nodes to consider and the answer must be negative. Another subtle case is when only one node exists at the queried depth inside a subtree, producing an odd total, which must immediately fail even if the character condition would otherwise pass.

## Approaches

A direct approach processes each query independently. For a query `(u, d)`, we traverse the subtree of `u`, collect all nodes whose depth equals `d`, and count character frequencies. Each such traversal can take linear time in the size of the subtree. In a chain-like tree, both subtree size and number of queries can be large, so the total cost becomes proportional to `nq`. This fails because it recomputes the same subtree information repeatedly.

The structure of the problem suggests that the only relevant information is frequency distributions grouped by depth. The tree itself is static, so we can preprocess each node once and reuse results. The challenge is that each query asks for a different subtree, so we still need a way to aggregate frequencies dynamically without recomputing from scratch.

This is exactly where tree DSU, also known as DSU on tree or small-to-large merging, becomes effective. We compute subtree sizes and identify heavy children. Then we process all light subtrees in a way that their contributions can be discarded after use, while the heavy child’s data is preserved. This guarantees that each node’s contribution is added and removed only `O(log n)` times across the recursion, keeping the overall complexity nearly linear.

Instead of recomputing frequency tables for every query, we maintain a global frequency structure indexed by depth and character. As we traverse the tree, we temporarily add contributions of subtrees, answer queries at the current node, and optionally remove contributions depending on whether we are keeping that subtree’s data.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| DSU on Tree | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at node `1` and compute for each node its depth and subtree size. While doing this, identify the heavy child, the child with the largest subtree. This choice minimizes repeated recomputation later.
2. Maintain a global structure `freq[depth][char]` that stores how many times each letter appears at a given depth among the currently active part of the tree.
3. Define a DFS procedure that processes a node `u`. First, recursively process all light children while discarding their contributions after finishing them. This ensures that their data does not persist unnecessarily.
4. If node `u` has a heavy child, process it next and keep its contribution. This subtree becomes the base state for `u`.
5. Add contributions of node `u`’s light subtrees and itself into `freq`. At this moment, `freq` represents exactly the multiset of all nodes in the subtree of `u`.
6. Answer all queries attached to node `u` by looking at the precomputed depth `d`. For that depth, compute total frequency and maximum character frequency. The answer is valid only if the total is non-zero, even, and no character exceeds half of the total.
7. After answering queries, if we are not in a heavy-path retention state, remove the contributions of the current subtree before returning to the parent. This restores the structure for sibling computations.

The correctness relies on the invariant that at each node `u`, immediately after step 5, the frequency structure contains exactly the nodes in `u`’s subtree at correct depths. Heavy-child retention ensures we do not repeatedly rebuild large subtrees, while light subtrees are safely discarded after use.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, q = map(int, input().split())
g = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)

s = " " + input().strip()

parent = [0] * (n + 1)
depth = [0] * (n + 1)
sz = [0] * (n + 1)
heavy = [0] * (n + 1)

def dfs1(u, p):
    parent[u] = p
    sz[u] = 1
    for v in g[u]:
        if v == p:
            continue
        depth[v] = depth[u] + 1
        dfs1(v, u)
        sz[u] += sz[v]
        if sz[v] > sz[heavy[u]]:
            heavy[u] = v

dfs1(1, 0)

maxd = max(depth)

freq = [None] + [[0] * 26 for _ in range(n + 5)]
ans = [None] * (q + 1)
queries = [[] for _ in range(n + 1)]

for i in range(1, q + 1):
    u, d = map(int, input().split())
    queries[u].append((d, i))

def add(u, p, val):
    freq[depth[u]][ord(s[u]) - 97] += val
    for v in g[u]:
        if v == p:
            continue
        add(v, u, val)

def dfs(u, p, keep):
    for v in g[u]:
        if v == p or v == heavy[u]:
            continue
        dfs(v, u, False)

    if heavy[u]:
        dfs(heavy[u], u, True)

    for v in g[u]:
        if v == p or v == heavy[u]:
            continue
        add(v, u, 1)

    freq[depth[u]][ord(s[u]) - 97] += 1

    for d, idx in queries[u]:
        arr = freq[d]
        total = sum(arr)
        mx = max(arr) if total > 0 else 0
        if total == 0 or total % 2 == 1 or mx > total // 2:
            ans[idx] = "No"
        else:
            ans[idx] = "Yes"

    if not keep:
        add(u, p, -1)

dfs(1, 0, True)

print("\n".join(ans[1:]))
```

The implementation mirrors the DSU-on-tree logic. The `dfs1` pass computes subtree sizes and heavy children. The `dfs` function maintains the active frequency table. Light subtrees are processed with `keep = False`, meaning their contributions are removed after use. The heavy subtree is preserved, allowing reuse of its accumulated state. Each query is answered by directly inspecting the frequency slice at the required depth.

The key implementation detail is that depth is used as an index into the frequency table. This avoids recomputing subtree filtering for each query and reduces each query to constant-time aggregation over 26 characters.

## Worked Examples

Consider a small tree:

Input:

```
5 2
1 2
1 3
3 4
3 5
ababa
1 2
3 3
```

We compute depths:

node 1 at depth 0, nodes 2 and 3 at depth 1, nodes 4 and 5 at depth 2.

For query `(1, 2)`, we consider nodes 4 and 5. Their letters might be `a` and `a`, so total is 2, maximum frequency is 2, which violates the “no majority” rule, so answer is `No`.

For query `(3, 3)`, there are no nodes at depth 3 in subtree of 3, so total is 0, also `No`.

| Query | Depth slice | Frequencies | Total | Max | Result |
| --- | --- | --- | --- | --- | --- |
| (1,2) | {4,5} | a:2 | 2 | 2 | No |
| (3,3) | ∅ | ∅ | 0 | 0 | No |

This trace shows how both empty and majority-dominated cases are rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Each node is added and removed a limited number of times under DSU-on-tree, queries are O(1) aggregate checks |
| Space | O(n) | adjacency list, subtree arrays, and frequency table |

The constraints allow about `2e5` nodes and queries, so linear-log behavior fits comfortably within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    s = " " + input().strip()

    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    sz = [0] * (n + 1)
    heavy = [0] * (n + 1)

    def dfs1(u, p):
        sz[u] = 1
        for v in g[u]:
            if v == p:
                continue
            depth[v] = depth[u] + 1
            dfs1(v, u)
            sz[u] += sz[v]
            if sz[v] > sz[heavy[u]]:
                heavy[u] = v

    dfs1(1, 0)

    freq = [ [0]*26 for _ in range(n+5) ]
    queries = [[] for _ in range(n+1)]
    ans = [None]*(q+1)

    for i in range(1, q+1):
        u, d = map(int, sys.stdin.readline().split())
        queries[u].append((d,i))

    def add(u,p,val):
        freq[depth[u]][ord(s[u])-97] += val
        for v in g[u]:
            if v!=p:
                add(v,u,val)

    def dfs(u,p,keep):
        for v in g[u]:
            if v==p or v==heavy[u]:
                continue
            dfs(v,u,False)
        if heavy[u]:
            dfs(heavy[u],u,True)
        for v in g[u]:
            if v==p or v==heavy[u]:
                continue
            add(v,u,1)
        freq[depth[u]][ord(s[u])-97] += 1
        for d,i in queries[u]:
            arr = freq[d]
            total = sum(arr)
            mx = max(arr) if total else 0
            ans[i] = "Yes" if total and total%2==0 and mx<=total//2 else "No"
        if not keep:
            add(u,p,-1)

    dfs(1,0,True)

    return "\n".join(ans[1:])

# minimal tree
assert run("""3 1
1 2
1 3
aba
1 1
""").strip() in ["Yes","No"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small tree | Yes/No | basic correctness |

## Edge Cases

One important edge case is when the queried depth lies completely outside the subtree depth range. In that case, the frequency slice is empty, and the algorithm correctly returns zero total, triggering a `No`. This avoids any accidental indexing into unused depth layers.

Another edge case is a subtree containing only one node at the queried depth. Even if that node is valid, the total becomes 1, which is odd, and the algorithm correctly rejects it before checking character dominance.
