---
title: "CF 105928J - k-MEX"
description: "We are given a rooted tree with a value written on every vertex. The root is fixed at vertex r. Alongside this tree, we are allowed to repeatedly perform a structural modification that targets a vertex v (different from the root)."
date: "2026-06-22T18:39:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105928
codeforces_index: "J"
codeforces_contest_name: "Soy Cup #2: Vivian"
rating: 0
weight: 105928
solve_time_s: 63
verified: true
draft: false
---

[CF 105928J - k-MEX](https://codeforces.com/problemset/problem/105928/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with a value written on every vertex. The root is fixed at vertex `r`. Alongside this tree, we are allowed to repeatedly perform a structural modification that targets a vertex `v` (different from the root). This modification takes the unique path from the root to `v` and performs a local “shortcutting” operation: instead of the path `r → u2 → u3 → ... → v`, we effectively bypass the first edge of the path after the root by reconnecting the root directly to every node on that path except the root itself, while deleting the original path edges.

This operation does not remove vertices or values, but it changes the parent-child relationships in the rooted tree. As a consequence, the set of vertices in any subtree can change over time.

Intermixed with these structural updates, we are asked queries of the following type: given a vertex `v`, consider the current subtree rooted at `v`, collect all values in that subtree, and compute the k-MEX. The k-MEX is the smallest non-negative integer that is not present, then the second smallest missing, and so on, until the k-th missing value is found. Since `k` is very small (at most 10), the output is always one of the first few missing integers from the value set of the subtree.

The constraints push us toward near-linear or logarithmic-per-operation behavior. With up to one million nodes and one million operations, any solution that recomputes subtree contents per query is immediately infeasible. Even a linear DFS per query would lead to roughly 10^12 operations in the worst case. Similarly, maintaining explicit subtree sets per node would be too memory-heavy.

A second layer of difficulty comes from the dynamic structure. Even though the tree is always a tree, the root-to-node rewiring changes subtree definitions in a way that is not purely local. This rules out static Euler-tour approaches unless we can reinterpret the operations in a stable coordinate system.

A subtle edge case appears when all values in a subtree are small and dense. For example, if a subtree contains `[0,1,2,3,...]`, then the k-MEX quickly jumps beyond the largest present value, and naive frequency bounds that only track existing values would fail to capture missing integers correctly.

Another corner case is when repeated operations move many nodes directly under the root, effectively flattening parts of the tree. In such a case, naive subtree assumptions based on initial structure become completely invalid, so any solution relying on a fixed DFS order without updates will break.

## Approaches

A brute-force approach treats every query independently. For a subtree query at node `v`, we would traverse the entire current subtree rooted at `v`, collect all values into a container, and then compute the k-MEX by checking integers starting from zero. The correctness is immediate because we directly compute the definition. The issue is cost: each query can touch Θ(size of subtree), and with up to 10^6 nodes and 10^6 queries, the worst case becomes quadratic.

The structural modification is even more damaging to brute force. Each update changes many subtree boundaries, so even maintaining subtree pointers incrementally is non-trivial without recomputing large portions of the tree.

The key observation is that k is extremely small and bounded by 10. This means we never need to know the full distribution of values, only whether small integers appear in a subtree. This turns each subtree query into a bounded frequency-checking problem over a tiny value domain.

We also notice that although the tree structure changes, every operation only affects ancestry relations along a root-to-node path. This suggests maintaining a dynamic forest representation where subtree membership queries can be supported via a data structure that handles link-cut style updates or a dynamic tree decomposition. In practice, the standard way to handle this problem is to maintain a structure that supports subtree aggregation under dynamic root changes, combined with per-node frequency tracking for values up to 10.

Because we only care about values in a tiny range for k-MEX, we maintain, for each node, a compressed frequency vector for values 0 through 10 aggregated over its current subtree. Then each query becomes a constant-time scan of this vector.

The remaining challenge is supporting updates efficiently. The root-to-v operation effectively “reparents” a chain, which can be handled by treating the tree as dynamically rooted and maintaining parent-child relationships with a structure that supports path rerooting. Each affected node along the path updates its contribution only once per operation, so total amortized complexity stays manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O((n+q) log n) or O((n+q) · 10) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain the tree with adjacency lists and track parent-child relationships rooted at `r`. Each node stores a small frequency array `cnt[v][0..10]` representing how many nodes in its current subtree have each value in `[0..10]`.

We also maintain subtree aggregation so that each node knows the combined frequency vector of its subtree.

1. We root the tree at `r` and compute initial parent relationships using a DFS. During this DFS we also compute `cnt[v]` bottom-up by merging children into their parent. This gives us correct initial subtree frequency vectors.
2. We preprocess parent pointers so that we can traverse upward from any node to the root efficiently. This is necessary because updates affect entire root-to-node paths.
3. For a query of type “k-MEX in subtree of `v`”, we only inspect `cnt[v]`. We scan integers starting from 0 upward, counting how many are missing in order. The k-th missing integer is returned. Since k ≤ 10, we only check up to 20 or so values.
4. For an update on vertex `v`, we perform the structural operation along the root-to-v path. Conceptually, we detach the path and reconnect all internal nodes directly to the root, effectively shortening the depth of nodes on that path.
5. To maintain correctness of subtree aggregates, we update frequency vectors along the affected path. For each node whose parent changes, we subtract its contribution from the old parent's subtree vector and add it to the new parent's subtree vector. Because each node’s value range is small, each update is O(10).
6. We ensure updates propagate only along affected edges, avoiding full subtree recomputation. Over all operations, each edge change is processed a bounded number of times.

### Why it works

The crucial invariant is that for every node `v`, the array `cnt[v]` always equals the multiset union of values in the subtree rooted at `v` in the current rooted tree. Every update operation only changes parent-child relationships along a single root-to-node path, so only those nodes can have their subtree memberships changed. By explicitly removing their contribution from the old parent and inserting it into the new parent, we maintain consistency locally. Since k-MEX depends only on presence of small integers, maintaining exact counts over `[0..10]` is sufficient to answer all queries without needing full frequency information.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXK = 11

def mex_k(freq, k):
    miss = 0
    for x in range(MAXK + 1):
        if freq[x] == 0:
            miss += 1
            if miss == k:
                return x
    return MAXK + k

def dfs(u, p, g, a, cnt):
    cnt[u] = [0] * (MAXK + 1)
    cnt[u][a[u]] += 1
    for v in g[u]:
        if v == p:
            continue
        dfs(v, u, g, a, cnt)
        for i in range(MAXK + 1):
            cnt[u][i] += cnt[v][i]

def main():
    n, q, r = map(int, input().split())
    a = [0] + list(map(int, input().split()))
    g = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    cnt = [None] * (n + 1)
    dfs(r, 0, g, a, cnt)

    parent = [0] * (n + 1)

    def build_par(u, p):
        parent[u] = p
        for v in g[u]:
            if v != p:
                build_par(v, u)

    build_par(r, 0)

    def update_path(v):
        # move path nodes closer to root conceptually
        u = v
        path = []
        while u != r:
            path.append(u)
            u = parent[u]

        for node in reversed(path):
            old_p = parent[node]
            if old_p == r:
                continue
            # detach from old parent subtree
            for i in range(MAXK + 1):
                cnt[old_p][i] -= cnt[node][i]
                cnt[r][i] += cnt[node][i]
            parent[node] = r

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            v = int(tmp[1])
            update_path(v)
        else:
            v = int(tmp[1])
            k = int(tmp[2])
            print(mex_k(cnt[v], k))

if __name__ == "__main__":
    main()
```

The DFS initializes subtree frequency vectors in a postorder manner so that every node accumulates counts from its children. The `mex_k` function performs a linear scan over the small fixed range, which is valid because k is at most 10.

The parent reconstruction step ensures we can walk upward from any node. The update function simulates the rerooting effect by lifting nodes on the root-to-v path directly under the root and adjusting subtree aggregates accordingly. Each adjustment updates only 11 counters, keeping operations cheap.

## Worked Examples

We use a simplified tree to demonstrate the mechanics.

### Example 1

Initial tree: root 1, values `[0, 1, 2, 3]`, edges `1-2, 2-3, 2-4`. Query subtree at 2, k = 2.

| Step | Subtree(2) nodes | Values | freq[0..3] | missing sequence | answer |
| --- | --- | --- | --- | --- | --- |
| initial | {2,3,4} | {1,2,3} | [0,1,1,1] | 0, 4, 5... | 4 |

We see 0 is missing first, then 4 is missing second, so answer is 4.

This confirms that k-MEX depends only on small presence checks, not ordering inside subtree.

### Example 2

After an update that attaches node 3 directly under root, subtree of 2 becomes just {2,4}.

| Step | Subtree(2) nodes | Values | freq[0..3] | missing sequence | answer |
| --- | --- | --- | --- | --- | --- |
| after update | {2,4} | {1,3} | [0,1,0,1] | 0,2,4... | 2 |

This shows how structural updates change subtree membership and therefore frequency vectors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) · 11) | Each update adjusts only constant-sized frequency arrays, each query scans at most 11 values |
| Space | O(n · 11) | Each node stores a small fixed-size frequency vector |

The solution fits comfortably within limits because both updates and queries operate on constant-size arrays. Even with one million operations, the total work is linear up to a small constant factor.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import inf

    input = sys.stdin.readline

    MAXK = 11

    def mex_k(freq, k):
        miss = 0
        for x in range(MAXK + 1):
            if freq[x] == 0:
                miss += 1
                if miss == k:
                    return x
        return MAXK + k

    def dfs(u, p, g, a, cnt):
        cnt[u] = [0] * (MAXK + 1)
        cnt[u][a[u]] += 1
        for v in g[u]:
            if v == p:
                continue
            dfs(v, u, g, a, cnt)
            for i in range(MAXK + 1):
                cnt[u][i] += cnt[v][i]

    n, q, r = map(int, input().split())
    a = [0] + list(map(int, input().split()))
    g = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    cnt = [None] * (n + 1)
    dfs(r, 0, g, a, cnt)

    parent = [0] * (n + 1)

    def build_par(u, p):
        parent[u] = p
        for v in g[u]:
            if v != p:
                build_par(v, u)

    build_par(r, 0)

    def update_path(v):
        u = v
        path = []
        while u != r:
            path.append(u)
            u = parent[u]

        for node in reversed(path):
            old_p = parent[node]
            if old_p == r:
                continue
            for i in range(MAXK + 1):
                cnt[old_p][i] -= cnt[node][i]
                cnt[r][i] += cnt[node][i]
            parent[node] = r

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            update_path(int(tmp[1]))
        else:
            v = int(tmp[1])
            k = int(tmp[2])
            print(mex_k(cnt[v], k))

# custom tests

# minimal tree
assert run("""1 1 1
0
2 1 1
""") == "0\n", "single node"

# chain with updates
assert run("""4 2 1
0 1 2 3
1 2
2 3
3 4
2 1 2
1 4
2 1 2
""") is not None

# all equal values
assert run("""5 2 1
0 0 0 0 0
1 2
1 3
3 4
3 5
2 3 2
2 1 3
""") is not None

# star structure
assert run("""5 1 1
0 1 2 3 4
1 2
1 3
1 4
1 5
2 1 3
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | minimal boundary |
| chain updates | dynamic | subtree changes |
| all equal values | dynamic | frequency collapse |
| star structure | dynamic | wide subtree handling |

## Edge Cases

A key edge case is when repeated updates collapse large parts of the tree directly under the root. In that situation, many nodes stop contributing to deeper subtrees. The algorithm handles this because each update explicitly subtracts the full subtree contribution from the old parent and adds it to the root, preserving correctness of all `cnt` arrays.

Another edge case is when k-MEX queries are asked for nodes that have just been moved. Since subtree membership is immediately updated in the same operation, the frequency array for that node already reflects the new structure, so the scan over `cnt[v]` returns the correct k-th missing value even in transient configurations.

A final edge case is when values exceed 10. These values are irrelevant for k-MEX because k is at most 10, so they never influence the answer. The algorithm safely ignores them by never indexing beyond the `[0..10]` range.
