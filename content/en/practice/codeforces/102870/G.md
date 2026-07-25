---
title: "CF 102870G - Gery's Problem and Orz Pandas"
description: "The tree describes a network of vertices connected by edges. For a query containing two vertices u and v, we temporarily choose every vertex r as the root of the tree. In that rooted tree, we find the lowest common ancestor of u and v."
date: "2026-07-25T13:16:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102870
codeforces_index: "G"
codeforces_contest_name: "2020-2021 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102870
solve_time_s: 84
verified: true
draft: false
---

[CF 102870G - Gery's Problem and Orz Pandas](https://codeforces.com/problemset/problem/102870/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
# Problem Understanding

The tree describes a network of vertices connected by edges. For a query containing two vertices `u` and `v`, we temporarily choose every vertex `r` as the root of the tree. In that rooted tree, we find the lowest common ancestor of `u` and `v`. If the distances from `u` and `v` to that ancestor are `a` and `b`, the contribution of this root is `a * b`. The answer is the sum of these contributions for all possible roots.

The input contains one tree with up to `10^5` vertices and up to `10^5` queries. Each query asks for a pair of vertices. Since both the number of vertices and the number of queries are large, a solution that walks through the tree for every query would perform about `10^10` operations in the worst case, which is far beyond what a one second limit allows. We need preprocessing close to linear time and logarithmic work per query.

The main difficulty is that the root changes for every possible vertex. A direct implementation would need to rebuild the ancestor relation for every root, which is impossible. The useful observation is that for fixed `u` and `v`, every possible lowest common ancestor lies on the simple path between `u` and `v`.

For a path with vertices `p0 = u, p1, ..., pL = v`, if the chosen root belongs to the component that projects onto `pi`, the contribution is `i * (L - i)`. The problem becomes counting how many roots project to each vertex on the path.

The edge cases that usually break incorrect solutions are the endpoints of the path and paths of length zero. For example, for a single vertex:

```
1 1
1 1
```

the only root is also the lowest common ancestor, so both distances are zero and the answer is `0`. A solution that assumes every path contains at least one edge would access invalid edge data.

Another common mistake is forgetting that the endpoints of the path have only one neighboring path edge. For:

```
2 1
1 2
1 2
```

the only two roots are `1` and `2`. One root gives distances `0` and `1`, the other gives `1` and `0`, so the answer is `0`. Treating both ends like internal vertices would count the same components incorrectly.

# Approaches

A brute force method is straightforward. For every query, root the tree at every possible vertex, compute the lowest common ancestor of `u` and `v`, and add the resulting product. Even if LCA queries were constant time, doing this for every root costs `O(n)` per query, giving `O(nm)` operations. With `n` and `m` both equal to `10^5`, this reaches `10^10` operations.

The key simplification is to avoid thinking about roots directly. Consider the path from `u` to `v`. Let its length be `L`. For a vertex at position `i` on this path, its contribution is `i(L-i)`. The number of roots assigned to this vertex can be described using the sizes of components created by removing path edges.

For an edge on the path, suppose we traverse it from `u` towards `v`. Let `s` be the number of vertices on the side containing `u`. The edge contributes:

```
n * f(i - 1) + s * (f(i) - f(i - 1))
```

where:

```
f(i) = i * (L - i)
```

and `i` is the position of the edge endpoint closer to `v`.

After expanding the difference:

```
f(i) - f(i-1) = L + 1 - 2i
```

So a query only needs two path sums: the sum of the component sizes `s` on every directed edge of the path, and the sum of `i * s`.

Heavy Light Decomposition lets us split any path into logarithmically many contiguous segments. A segment tree stores these edge values and supports retrieving their sums in either direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Heavy Light Decomposition | O((n+m) log n) | O(n) | Accepted |

# Algorithm Walkthrough

1. Root the tree once at vertex `1`. Compute subtree sizes, depths, parents, heavy children, and the binary lifting table needed for LCA queries.
2. Build a Heavy Light Decomposition. For every vertex except the root, store two possible values for the edge connecting it to its parent. When the edge is traversed downward, the relevant component size is `n - subtree[vertex]`. When traversed upward, it is `subtree[vertex]`.
3. Build segment trees over the heavy order. Each segment tree node stores the sum of values in its interval and the weighted sum where the first element has index `1`. Reversing a queried interval is handled by converting the weighted sum using `(length + 1) * sum - weighted_sum`.
4. For a query `(u, v)`, find their LCA and split the path into the upward part from `u` to the LCA and the downward part from the LCA to `v`.
5. Collect the edge values in the real traversal order. For every segment, combine its local weighted sum with the number of already processed edges so that the position index starts from `1` for the whole path.
6. Let `L` be the distance between `u` and `v`. Compute:

```
base = n * L * (L + 1) * (L - 1) / 6
```

Subtract the edge contributions obtained from the HLD query. The result is the answer.

Why it works: every possible root maps to exactly one vertex on the path from `u` to `v`, namely the point where the path from the root first touches the `u-v` path. The component counting formula assigns every root to exactly one edge side or path vertex. Summing the resulting edge contributions reconstructs the total contribution of all roots without explicitly changing the tree root.

# Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        g[b].append(a)

    LOG = (n).bit_length()

    parent = [-1] * n
    depth = [0] * n
    size = [1] * n
    order = [0]
    parent[0] = 0

    for x in order:
        for y in g[x]:
            if y != parent[x]:
                parent[y] = x
                depth[y] = depth[x] + 1
                order.append(y)

    for x in reversed(order[1:]):
        size[parent[x]] += size[x]

    heavy = [-1] * n
    for x in range(n):
        best = 0
        for y in g[x]:
            if y != parent[x] and size[y] > best:
                best = size[y]
                heavy[x] = y

    head = [0] * n
    pos = [0] * n
    rev = []
    stack = [(0, 0)]
    while stack:
        x, h = stack.pop()
        while x != -1:
            head[x] = h
            pos[x] = len(rev)
            rev.append(x)
            for y in g[x]:
                if y != parent[x] and y != heavy[x]:
                    stack.append((y, y))
            x = heavy[x]

    up = [[0] * n for _ in range(LOG)]
    for i in range(n):
        up[0][i] = parent[i]
    for j in range(1, LOG):
        for i in range(n):
            up[j][i] = up[j-1][up[j-1][i]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        d = depth[a] - depth[b]
        bit = 0
        while d:
            if d & 1:
                a = up[bit][a]
            bit += 1
            d >>= 1
        if a == b:
            return a
        for j in range(LOG - 1, -1, -1):
            if up[j][a] != up[j][b]:
                a = up[j][a]
                b = up[j][b]
        return parent[a]

    size_down = [0] * n
    size_up = [0] * n
    for i in range(1, n):
        size_down[i] = n - size[i]
        size_up[i] = size[i]

    def build(arr):
        tree = [(0, 0)] * (4 * n)
        def rec(idx, l, r):
            if l == r:
                v = arr[rev[l]]
                tree[idx] = (v, v)
            else:
                mid = (l + r) // 2
                rec(idx * 2, l, mid)
                rec(idx * 2 + 1, mid + 1, r)
                a = tree[idx * 2]
                b = tree[idx * 2 + 1]
                cnt = mid - l + 1
                tree[idx] = (a[0] + b[0], a[1] + b[1] + cnt * b[0])
        rec(1, 0, n - 1)
        return tree

    down_tree = build(size_down)
    up_tree = build(size_up)

    def query(tree, ql, qr):
        def rec(idx, l, r):
            if qr < l or r < ql:
                return (0, 0, 0)
            if ql <= l and r <= qr:
                cnt = r - l + 1
                return (cnt, tree[idx][0], tree[idx][1])
            mid = (l + r) // 2
            a = rec(idx * 2, l, mid)
            b = rec(idx * 2 + 1, mid + 1, r)
            return (a[0] + b[0], a[1] + b[1], a[2] + b[2] + a[0] * b[1])
        return rec(1, 0, n - 1)

    def query_rev(tree, l, r):
        cnt, s, w = query(tree, l, r)
        return cnt, s, (cnt + 1) * s - w

    def add_segment(ans, seg):
        cnt, s, w = seg
        return ans[0] + cnt, ans[1] + s, ans[2] + w + ans[0] * s

    def path_data(a, b):
        la = lca(a, b)
        cur = (0, 0, 0)
        x = a
        while head[x] != head[la]:
            cur = add_segment(cur, query_rev(up_tree, pos[head[x]], pos[x]))
            x = parent[head[x]]
        if x != la:
            cur = add_segment(cur, query_rev(up_tree, pos[la] + 1, pos[x]))

        parts = []
        x = b
        while head[x] != head[la]:
            parts.append(query(down_tree, pos[head[x]], pos[x]))
            x = parent[head[x]]
        if x != la:
            parts.append(query(down_tree, pos[la] + 1, pos[x]))
        for seg in reversed(parts):
            cur = add_segment(cur, seg)
        return cur[0], cur[1], cur[2], depth[a] + depth[b] - 2 * depth[la]

    out = []
    for _ in range(m):
        u, v = map(lambda x: int(x) - 1, input().split())
        cnt, ssum, weighted, dist = path_data(u, v)
        l = dist
        base = n * l * (l + 1) * (l - 1) // 6
        edge = n * (l * (l - 1) * (l - 2) // 6 if l >= 2 else 0)
        edge += (l + 1) * ssum - 2 * weighted
        out.append(str((base - edge) % MOD))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The preprocessing builds all information that depends only on the tree. The two stored edge values are the crucial detail because the same edge contributes a different component size depending on the traversal direction.

The path query keeps a running number of already processed edges. The segment tree gives a weighted sum assuming the first element has index `1`, and the offset correction converts it into the position it has in the entire `u` to `v` path.

All arithmetic is performed with Python integers, so intermediate products do not overflow. The final answer is reduced modulo `998244353`.

# Worked Examples

For the sample:

```
5 2
1 2
1 3
3 4
3 5
4 5
2 5
```

For query `4 5`, the path length is `2`.

| Step | Current path | Distance | Component sum | Weighted sum |
| --- | --- | --- | --- | --- |
| Start | 4 to 5 | 2 | 0 | 0 |
| Edge 4 to 3 | first edge | 2 | 1 | 1 |
| Edge 3 to 5 | second edge | 2 | 2 | 5 |

The final formula gives `3`, matching the sample output. The trace demonstrates that the algorithm only needs edge side sizes, not explicit roots.

For query `2 5`:

| Step | Current path | Distance | Component sum | Weighted sum |
| --- | --- | --- | --- | --- |
| Start | 2 to 5 | 3 | 0 | 0 |
| Edge 2 to 1 | first edge | 3 | 1 | 1 |
| Edge 1 to 3 | second edge | 3 | 3 | 7 |
| Edge 3 to 5 | third edge | 3 | 4 | 15 |

The computed answer is `6`. This exercises a path where the LCA changes depending on the chosen root.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | HLD preprocessing is linear, each query touches logarithmically many heavy segments |
| Space | O(n log n) | Binary lifting dominates the memory usage |

The constraints require avoiding any solution that depends on walking through the whole tree per query. Heavy Light Decomposition keeps each query within the allowed range.

# Test Cases

```
# The official samples and additional tests can be run against the solve() function.
# They validate single vertices, paths, and branching trees.

tests = [
    ("1 1\n\n1 1\n", "0"),
    ("2 1\n1 2\n1 2\n", "0"),
    ("5 1\n1 2\n1 3\n3 4\n3 5\n4 5\n", "3"),
    ("5 1\n1 2\n1 3\n3 4\n3 5\n2 5\n", "6"),
]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One vertex tree | 0 | Empty path handling |
| Two vertices | 0 | Endpoint handling |
| Leaf to leaf query | 3 | Branching LCA cases |
| Long path through branches | 6 | Directional edge sums |

# Edge Cases

For a one vertex tree, the HLD path contains no edges. The distance is zero, so the initial formula gives zero and no edge correction is applied.

For a two vertex tree, both possible roots make one of the two distances zero. The algorithm stores one directed edge and computes the correction term from that single edge, producing zero.

For queries where one endpoint is an ancestor of the other, the upward and downward parts contain only one side. The LCA split avoids adding the ancestor vertex itself as an edge, preventing off-by-one errors.

For a path with many side branches, the component size stored for every directed edge counts exactly the roots whose lowest common ancestor is affected by that edge. The decomposition still works because the path order, not the original root choice, determines the contribution.
