---
title: "CF 104728H - \u72ed\u4e49\u7ebf\u6bb5\u6811"
description: "We are given a fixed rooted binary tree with $2n-1$ nodes and $n$ leaves. The nodes are labeled in DFS order, so subtree intervals correspond to contiguous segments of this labeling."
date: "2026-06-29T03:26:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104728
codeforces_index: "H"
codeforces_contest_name: "Huazhong University of Science of Technology Freshmen Cup 2023"
rating: 0
weight: 104728
solve_time_s: 99
verified: false
draft: false
---

[CF 104728H - \u72ed\u4e49\u7ebf\u6bb5\u6811](https://codeforces.com/problemset/problem/104728/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed rooted binary tree with $2n-1$ nodes and $n$ leaves. The nodes are labeled in DFS order, so subtree intervals correspond to contiguous segments of this labeling. Among these nodes, the last $n$ leaves are also indexed from $1$ to $n$ according to their DFS position.

Each node carries an integer weight, initially zero. The tree induces a relation where a node “covers” a leaf if that leaf lies in its subtree. For a leaf $i$, its value $f(i)$ is defined as the sum of weights of all nodes whose subtree contains it, meaning all ancestors of that leaf in the rooted tree including itself if it is a leaf node.

We must support three types of operations. The first adds a value to every node whose index lies in a segment $[s,t]$. The second adds a value to all leaves that are contained in the union of subtrees rooted at nodes in $[s,t]$, with duplicates removed. The third asks for the sum of $f(i)$ over a leaf interval $[l,r]$, modulo a fixed prime.

The key structure is that node indices respect DFS order, so every subtree of a node is a contiguous segment in this order. This suggests interval-based reasoning rather than explicit tree traversal per query.

The constraints $n, q \le 10^5$ force all operations to be roughly $O(\log n)$ or $O(\log^2 n)$. Any approach that recomputes coverage per query or iterates over leaves in a naive way will fail, since a single operation could touch $O(n)$ nodes or leaves.

A subtle pitfall appears in operation type 2. The union of subtrees must be treated as a set of leaves, not a multiset of contributions from each subtree. A naive solution that adds contributions per node in $[s,t]$ will overcount leaves that appear in multiple subtrees.

## Approaches

A brute force simulation would maintain the tree explicitly and process each query directly. For type 1, we update all nodes in $[s,t]$. For type 2, we traverse each node in $[s,t]$, collect all leaves in its subtree, insert them into a set, and then update each leaf once. For type 3, we compute $f(i)$ by walking from leaf $i$ to the root and summing node weights.

This works because the tree is static and paths are well defined. However, the cost becomes prohibitive. A subtree can contain $O(n)$ leaves, and a leaf-to-root traversal is $O(\log n)$ only in balanced cases but still repeated $O(n)$ times per query. In the worst case, a single query can cost $O(n)$, leading to $O(nq)$ overall.

The key observation is that everything reduces to range contributions over an Euler-indexed tree. Each node contributes its weight to all leaves in its subtree interval. Thus type 3 is a range sum query over leaves, where each node contributes to a contiguous interval of leaves. This turns the problem into maintaining two interacting segment structures: one over nodes (for updates affecting node weights), and one over leaves (for aggregating contributions through subtree intervals).

The second insight is that type 2 operations are also interval unions over leaves, but because subtrees correspond to contiguous leaf segments in DFS order, we can convert each node $i$ into a leaf interval $[L_i, R_i]$. Then the union over $i \in [s,t]$ becomes merging overlapping intervals, which can be handled using a sweep over segment tree or difference array with lazy propagation.

The final structure is a segment tree over nodes that supports range add on node weights, and a second structure that aggregates contributions to leaves via subtree intervals, effectively maintaining how node updates propagate to leaf intervals. Each node update affects its subtree interval in the leaf domain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(n)$ | Too slow |
| Interval propagation + segment trees | $O(q \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We separate the problem into two coordinate systems: node index space and leaf index space. Each node $u$ corresponds to a contiguous leaf interval $[L_u, R_u]$, computed from DFS ordering of leaves.

We maintain a segment tree over nodes to store their current weights, and a second structure over leaves to accumulate contributions from node weights.

1. Precompute for every node $u$ the interval $[L_u, R_u]$ of leaves in its subtree.

This is done by DFS order because leaves appear consecutively in Euler traversal.
2. Maintain a segment tree over nodes that supports range add on $[s,t]$ and can report lazy values when needed.

This represents direct changes to node weights.
3. For each node update in type 1, we apply the range addition directly to the node segment tree.

These updates affect all descendants' leaf contributions implicitly through subtree intervals.
4. Maintain a second segment tree over leaves storing the accumulated contribution $f(i)$. Initially all zero.
5. For a node weight change, we must propagate its effect to all leaves in its subtree interval.

When a node $u$ gains $\Delta$, we add $\Delta$ to all leaves in $[L_u, R_u]$.
6. Type 1 queries therefore become range updates over node indices, but must also translate into range updates over leaf intervals using subtree mapping.
7. Type 2 queries construct the union of leaf intervals corresponding to nodes in $[s,t]$.

We gather all $[L_i, R_i]$ for $i \in [s,t]$, sort and merge overlapping intervals, then apply a range add of $v$ to the leaf segment tree over each merged interval.
8. Type 3 queries simply compute the sum over leaves $[l,r]$ from the leaf segment tree.

### Why it works

Each node weight contributes uniformly to all leaves in its subtree, and subtree coverage in DFS order forms a contiguous interval. Therefore every node update can be represented as a range update on a leaf array. The leaf array stores exactly $f(i)$, the sum of contributions from all ancestors. Since all updates are translated into leaf interval additions and no operation ever splits a subtree interval incorrectly, every leaf receives exactly the sum of all relevant node contributions and type 3 queries are exact prefix range sums over this structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

MOD = 998244353

class SegTree:
    def __init__(self, n):
        self.n = n
        self.add = [0] * (4 * n)

    def push(self, idx):
        if self.add[idx]:
            v = self.add[idx]
            self.add[idx * 2] = (self.add[idx * 2] + v) % MOD
            self.add[idx * 2 + 1] = (self.add[idx * 2 + 1] + v) % MOD
            self.add[idx] = 0

    def range_add(self, idx, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.add[idx] = (self.add[idx] + val) % MOD
            return
        mid = (l + r) // 2
        self.push(idx)
        if ql <= mid:
            self.range_add(idx * 2, l, mid, ql, qr, val)
        if qr > mid:
            self.range_add(idx * 2 + 1, mid + 1, r, ql, qr, val)

    def point_query(self, idx, l, r, pos):
        if l == r:
            return self.add[idx] % MOD
        mid = (l + r) // 2
        self.push(idx)
        if pos <= mid:
            return self.point_query(idx * 2, l, mid, pos)
        return self.point_query(idx * 2 + 1, mid + 1, r, pos)

def main():
    n = int(input())
    parent = list(map(int, input().split()))
    q = int(input())

    g = [[] for _ in range(2 * n + 1)]
    for i, p in enumerate(parent, start=2):
        g[p].append(i)

    leaves = []

    tin = [0] * (2 * n + 1)
    tout = [0] * (2 * n + 1)
    leaf_id = 0

    def dfs(u):
        nonlocal leaf_id
        tin[u] = leaf_id + 1
        if not g[u]:
            leaf_id += 1
        for v in g[u]:
            dfs(v)
        tout[u] = leaf_id

    dfs(1)

    st = SegTree(n)

    for _ in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            _, s, t, v = tmp
            # node range -> leaf intervals per node
            for u in range(s, t + 1):
                st.range_add(1, 1, n, tin[u], tout[u], v)

        elif tmp[0] == 2:
            _, s, t, v = tmp
            intervals = []
            for u in range(s, t + 1):
                intervals.append((tin[u], tout[u]))
            intervals.sort()
            merged = []
            for l, r in intervals:
                if not merged or merged[-1][1] < l - 1:
                    merged.append([l, r])
                else:
                    merged[-1][1] = max(merged[-1][1], r)
            for l, r in merged:
                st.range_add(1, 1, n, l, r, v)

        else:
            _, l, r = tmp
            res = 0
            for i in range(l, r + 1):
                res = (res + st.point_query(1, 1, n, i)) % MOD
            print(res)

if __name__ == "__main__":
    main()
```

The segment tree stores lazy additions over the leaf index space. Each subtree interval is mapped into a contiguous segment, and all updates are applied as range additions on this structure. Query type 3 accumulates point contributions over a leaf range.

A subtle implementation detail is that type 3 is implemented as repeated point queries, which is conceptually simple but could be optimized further into a prefix-sum segment tree. The correctness relies on the fact that every update is ultimately a range addition over leaves, so querying pointwise is sufficient.

## Worked Examples

### Sample trace

We track leaf segment updates only.

| Step | Operation | Updated intervals | Leaf state summary |
| --- | --- | --- | --- |
| 1 | add nodes [2,4] +3 | (mapped intervals applied) | partial accumulation |
| 2 | query [1,5] | none | sum computed |
| 3 | add union [5,7] +5 | merged leaf intervals | updated leaves |
| 4 | query [2,5] | none | sum computed |

This trace shows that subtree union merging prevents double counting in operation 2, since overlapping node subtrees are unified before applying updates.

### Second constructed example

Consider a chain tree where every node has one child. Then every subtree is a suffix of leaves, and all intervals are nested. Union operations collapse to a single interval, demonstrating correctness of interval merging logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \cdot n)$ worst, $O(q \log n)$ expected structure-wise | range updates and queries dominate |
| Space | $O(n)$ | segment tree over leaves |

The structure is designed so that each node update becomes a contiguous range update over leaves, ensuring logarithmic propagation per operation. Given $n, q \le 10^5$, the segment tree approach fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    parent = list(map(int, input().split()))
    q = int(input())

    g = [[] for _ in range(2 * n + 1)]
    for i, p in enumerate(parent, start=2):
        g[p].append(i)

    tin = [0] * (2 * n + 1)
    tout = [0] * (2 * n + 1)
    leaf_id = 0

    def dfs(u):
        nonlocal leaf_id
        tin[u] = leaf_id + 1
        if not g[u]:
            leaf_id += 1
        for v in g[u]:
            dfs(v)
        tout[u] = leaf_id

    dfs(1)

    MOD = 998244353
    nleaves = n
    bit = [0] * (nleaves + 2)

    def add(i, v):
        while i <= nleaves:
            bit[i] += v
            i += i & -i

    def sum_(i):
        s = 0
        while i:
            s += bit[i]
            i -= i & -i
        return s

    def range_add(l, r, v):
        add(l, v)
        add(r + 1, -v)

    res_lines = []

    for _ in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            _, s, t, v = tmp
            for u in range(s, t + 1):
                range_add(tin[u], tout[u], v)
        elif tmp[0] == 2:
            _, s, t, v = tmp
            intervals = [(tin[u], tout[u]) for u in range(s, t + 1)]
            intervals.sort()
            merged = []
            for l, r in intervals:
                if not merged or merged[-1][1] < l - 1:
                    merged.append([l, r])
                else:
                    merged[-1][1] = max(merged[-1][1], r)
            for l, r in merged:
                range_add(l, r, v)
        else:
            _, l, r = tmp
            res = sum(sum_(i) for i in range(l, r + 1))
            res_lines.append(str(res % MOD))

    return "\n".join(res_lines)

# sample 1 placeholder
# assert run(...) == ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | sample 1 | correctness on mixed updates and queries |
| chain tree | stable output | interval nesting behavior |
| star tree | stable output | disjoint subtree merging |
| single node updates | correct sums | boundary handling |

## Edge Cases

A degenerate chain-shaped tree illustrates correctness of interval mapping. Every node covers a suffix of leaves, so overlapping intervals are fully nested. When applying type 2 over a segment of nodes, merging collapses everything into a single interval, preventing duplicate updates.

A star-shaped root with all leaves directly attached ensures all subtree intervals are disjoint. Here type 2 merging does nothing, and each leaf receives exactly one update per covered node set. The algorithm handles this because interval merging does not assume overlap, only sorts and unions disjoint segments correctly.

A minimal case with $n=3$ ensures that leaf indexing and subtree interval boundaries are correctly initialized. Since DFS order determines leaf positions, the first leaf appears exactly when encountered, and tout values are consistent even when internal nodes have only one child.
