---
title: "CF 102439K - Innovations"
description: "We have a weighted tree of cities. Because the graph is a tree, between every pair of cities there is exactly one path, so that path is automatically the shortest path."
date: "2026-08-12T08:17:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "K"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 155
verified: true
draft: false
---

[CF 102439K - Innovations](https://codeforces.com/problemset/problem/102439/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a weighted tree of cities. Because the graph is a tree, between every pair of cities there is exactly one path, so that path is automatically the shortest path. Each query chooses two cities and replaces every edge on their path by an edge whose weight becomes the floor of its square root. The same edge may be changed many times. After the initial state and after every query, we need the sum of distances over all unordered pairs of cities, modulo (10^9+7). The official statement gives the same operation and the sample output (140,92,72,48).

The first useful observation is that we never need to maintain individual pairwise distances. Root the tree arbitrarily. Consider an edge whose child-side subtree contains (s) vertices. Removing this edge separates the tree into parts of sizes (s) and (n-s). Exactly (s(n-s)) unordered pairs have their path crossing this edge. If its current weight is (w), its contribution to the sum of all pairwise distances is

[
w \cdot s(n-s).
]

So the whole answer is simply

[
\sum_{\text{edges }e} w_e \cdot s_e(n-s_e).
]

The coefficient (s_e(n-s_e)) never changes, because the tree structure never changes. Only the edge weights change.

This turns the problem into a dynamic array problem. We need to apply (w \leftarrow \lfloor\sqrt w\rfloor) to every edge on a tree path while maintaining the weighted sum of all edge values.

The bounds make a direct simulation impossible. There can be (2\cdot10^5) queries, and a path can contain (2\cdot10^5-1) edges, so explicitly visiting every path edge can require roughly (4\cdot10^{10}) edge updates. Recomputing all pairwise distances after each query would be even worse, at (O(mn^2)). We need to exploit the fact that square roots reduce the weights very quickly.

There are only a few genuinely dangerous edge cases.

### A single city

The smallest possible input is

```
1 1
1 1
```

There are no roads, so every pairwise-distance sum is zero. The correct output is

```
0
0
```

A careless implementation that assumes every query contains at least one edge may try to access a nonexistent edge or produce an invalid range.

### An edge whose weight is already 1

Consider

```
2 1
1 2 1
1 2
```

The initial sum is (1), and applying the operation gives (\lfloor\sqrt1\rfloor=1), so the answer stays (1):

```
1
1
```

A common mistake is to assume every queried edge changes. The segment tree must be able to stop immediately when all weights in a range are already 1.

### Repeated updates on the same path

Consider

```
3 3
1 2 16
2 3 9
1 3
1 3
1 3
```

Each edge contributes (2w), because each edge separates one vertex from two vertices. The outputs are

```
50
14
6
4
```

The edge weights evolve as (16\to4\to2\to1) and (9\to3\to1\to1). An implementation that applies the square root only once per edge over the entire input would be wrong.

### The root has no edge to its parent

When a rooted tree is flattened, each non-root vertex represents the edge connecting it to its parent. The root represents no edge. For a path query, the root position must not accidentally be treated as a real road. This is especially easy to get wrong when the final heavy-light interval contains the lowest common ancestor.

## Approaches

The most direct solution starts from the edge contribution formula. Root the tree, compute every subtree size, and assign each edge its fixed coefficient (s(n-s)). Then for each query, walk from (u) to (v), change every edge on that path, and adjust the global answer by the corresponding difference in contribution.

This approach is correct because every edge knows exactly how many city pairs use it. If an edge changes from (w) to (w'), the total answer changes by

[
(w'-w)s(n-s).
]

The problem is the number of edges visited. In a path-shaped tree, a query between the two endpoints contains (n-1) edges. With (m=2\cdot10^5), this gives up to roughly (4\cdot10^{10}) edge visits. Even though each individual square root is cheap, that many operations cannot fit into the 1.5 second limit.

The key observation is that an edge cannot change very many times. With (w\le10^6), the sequence is bounded by

[
10^6\to1000\to31\to5\to2\to1.
]

Thus every edge changes at most five times during the entire input. Once an edge reaches 1, all later updates involving it do nothing.

This makes a segment tree particularly suitable. We first use heavy-light decomposition to turn every tree path into (O(\log n)) contiguous intervals of an array. The segment tree then stores the current edge weights on this flattened array.

A simple segment tree could store the maximum weight in every node. If the maximum is 1, an entire queried segment can be skipped. Otherwise we descend until finding the affected edges. That already gives an amortized solution because there are only (O(n)) actual weight changes.

We can make the segment tree stronger by storing both the minimum and maximum weight. The square-root function is monotonic. If a segment has minimum (a) and maximum (b), and

[
\lfloor\sqrt a\rfloor=\lfloor\sqrt b\rfloor,
]

then every value between (a) and (b) has exactly the same new value. We can update the whole segment lazily by assigning that one value. This removes many unnecessary descents.

The segment tree also stores the sum of coefficients in each node and the current weighted sum of that node. When an entire node becomes the same weight (x), its contribution is immediately

[
x\cdot\sum c_i.
]

Thus the root of the segment tree always contains the required answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm)) after preprocessing | (O(n)) | Too slow |
| HLD + segment tree | (O(m\log^2 n+n\log n\log\log W)) amortized | (O(n)) | Accepted |

Here (W\le10^6), so (\log\log W) is effectively a small constant. The actual number of successful changes per edge is at most five.

## Algorithm Walkthrough

1. Root the tree at city 1 and compute `parent`, `depth`, and `subtree_size` for every city. For every non-root vertex (v), the edge from (v) to its parent has coefficient

[
c_v=\text{subtree_size}[v]\cdot(n-\text{subtree_size}[v]).
]

This coefficient counts exactly how many unordered city pairs use that edge.
2. Compute the heavy child of every vertex, meaning the child with the largest subtree. Heavy-light decomposition groups every heavy chain into one contiguous interval of an array. The edge to the parent of vertex (v) is stored at the array position of (v).

The root gets weight zero because it does not correspond to an edge.
3. Build a segment tree over the flattened array. Each segment tree node stores its minimum edge weight, maximum edge weight, the sum of its fixed coefficients, the current weighted contribution, and an optional lazy assignment value.
4. When a queried interval is fully covered, first check its maximum weight. If it is at most 1, the interval needs no work.

Otherwise compute the floor square roots of the minimum and maximum. If they are equal, monotonicity of the square-root function means every value in the interval becomes that same number. The whole segment can be assigned lazily without visiting its leaves.
5. If the minimum and maximum produce different square roots, the segment contains at least two different resulting values, so it cannot be represented by one lazy assignment. Push any pending assignment to the children and recurse into the two halves.
6. Decompose every tree query path using heavy-light decomposition. While the two endpoints belong to different heavy chains, update the entire chain segment belonging to the deeper chain. Once both vertices are on the same chain, update the interval strictly below their lowest common ancestor.

The final interval uses `pos[lca] + 1`, not `pos[lca]`, because a vertex position represents the edge leading into that vertex. The LCA itself has no edge on the path below it.
7. After processing the query, the root of the segment tree contains the sum of (w_e c_e) over every edge. Print this value modulo (10^9+7).

### Why it works

For every edge, the number of city pairs whose path uses that edge is permanently (s(n-s)), so the required global sum is exactly the sum of edge weights multiplied by their fixed coefficients. The segment tree maintains precisely these weighted edge contributions.

During a query, every edge on the requested tree path is transformed once by (w\mapsto\lfloor\sqrt w\rfloor). Heavy-light decomposition covers exactly those edges and no others. The segment tree applies the same transformation to every covered edge. When a whole segment has the same resulting square-root value, the lazy assignment is valid because the square-root function is monotonic. Otherwise the recursion eventually reaches smaller segments where the transformation can be represented correctly.

Thus after every query, every edge has exactly its required current weight, and the segment tree root is exactly the required sum of all pairwise shortest paths.

## Python Solution

```python
import sys
from math import isqrt
from array import array

input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n, m = map(int, input().split())

    # Forward-star adjacency representation.
    head = array('i', [-1]) * n
    to = array('i', [0]) * (2 * max(0, n - 1))
    nxt = array('i', [0]) * (2 * max(0, n - 1))
    ew = array('i', [0]) * (2 * max(0, n - 1))

    ptr = 0
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1

        to[ptr] = v
        ew[ptr] = w
        nxt[ptr] = head[u]
        head[u] = ptr
        ptr += 1

        to[ptr] = u
        ew[ptr] = w
        nxt[ptr] = head[v]
        head[v] = ptr
        ptr += 1

    # Root the tree and compute parent, depth, edge-to-parent weight.
    parent = array('i', [-1]) * n
    depth = array('i', [0]) * n
    weight_to_parent = array('i', [0]) * n
    order = array('i', [0]) * n

    parent[0] = 0
    stack = [0]
    order_len = 0

    while stack:
        v = stack.pop()
        order[order_len] = v
        order_len += 1

        e = head[v]
        while e != -1:
            u = to[e]
            if u != parent[v]:
                parent[u] = v
                depth[u] = depth[v] + 1
                weight_to_parent[u] = ew[e]
                stack.append(u)
            e = nxt[e]

    # Subtree sizes and heavy children.
    size = array('i', [1]) * n
    heavy = array('i', [-1]) * n

    for idx in range(n - 1, 0, -1):
        v = order[idx]
        p = parent[v]
        size[p] += size[v]

        h = heavy[p]
        if h == -1 or size[v] > size[h]:
            heavy[p] = v

    # Heavy-light decomposition.
    chain_head = array('i', [0]) * n
    pos = array('i', [0]) * n

    cur = 0
    chain_stack = [0]

    while chain_stack:
        h = chain_stack.pop()
        v = h

        while v != -1:
            chain_head[v] = h
            pos[v] = cur
            cur += 1

            e = head[v]
            hv = heavy[v]
            while e != -1:
                u = to[e]
                if parent[u] == v and u != hv:
                    chain_stack.append(u)
                e = nxt[e]

            v = hv

    # Flattened edge weights and fixed edge coefficients.
    weights = array('i', [0]) * n
    coeff = array('q', [0]) * n

    for v in range(1, n):
        p = pos[v]
        weights[p] = weight_to_parent[v]
        coeff[p] = size[v] * (n - size[v])

    # Segment tree arrays.
    #
    # mn[x], mx[x]      minimum/maximum weight in the node
    # sumc[x]           sum of fixed edge coefficients
    # sumw[x]           current weighted contribution
    # lazy[x]           >= 0 means all values in this node are assigned to it
    #
    # The root position has coefficient 0 and weight 0.
    S = 4 * n + 5

    mn = array('i', [0]) * S
    mx = array('i', [0]) * S
    lazy = array('i', [-1]) * S
    sumc = array('q', [0]) * S
    sumw = array('q', [0]) * S

    def apply(node, value):
        mn[node] = value
        mx[node] = value
        sumw[node] = value * sumc[node]
        lazy[node] = value

    def build(node, left, right):
        if left == right:
            w = weights[left]
            c = coeff[left]
            mn[node] = w
            mx[node] = w
            sumc[node] = c
            sumw[node] = w * c
            return

        mid = (left + right) >> 1
        lc = node << 1
        rc = lc | 1

        build(lc, left, mid)
        build(rc, mid + 1, right)

        mn[node] = min(mn[lc], mn[rc])
        mx[node] = max(mx[lc], mx[rc])
        sumc[node] = sumc[lc] + sumc[rc]
        sumw[node] = sumw[lc] + sumw[rc]

    def push(node):
        value = lazy[node]
        if value != -1:
            lc = node << 1
            rc = lc | 1
            apply(lc, value)
            apply(rc, value)
            lazy[node] = -1

    def pull(node):
        lc = node << 1
        rc = lc | 1
        mn[node] = min(mn[lc], mn[rc])
        mx[node] = max(mx[lc], mx[rc])
        sumw[node] = sumw[lc] + sumw[rc]

    def range_sqrt(node, left, right, ql, qr):
        if right < ql or qr < left or mx[node] <= 1:
            return

        if ql <= left and right <= qr:
            a = isqrt(mn[node])
            b = isqrt(mx[node])

            if a == b:
                apply(node, a)
                return

        if left == right:
            apply(node, isqrt(mx[node]))
            return

        push(node)

        mid = (left + right) >> 1
        lc = node << 1
        rc = lc | 1

        if ql <= mid:
            range_sqrt(lc, left, mid, ql, qr)
        if qr > mid:
            range_sqrt(rc, mid + 1, right, ql, qr)

        pull(node)

    build(1, 0, n - 1)

    def update_path(u, v):
        while chain_head[u] != chain_head[v]:
            hu = chain_head[u]
            hv = chain_head[v]

            if depth[hu] < depth[hv]:
                u, v = v, u
                hu, hv = hv, hu

            range_sqrt(1, 0, n - 1, pos[hu], pos[u])
            u = parent[hu]

        if u == v:
            return

        if depth[u] < depth[v]:
            u, v = v, u

        # u is deeper. The LCA itself is not an edge on the path.
        range_sqrt(1, 0, n - 1, pos[v] + 1, pos[u])

    out = [str(sumw[1] % MOD)]

    for _ in range(m):
        u, v = map(int, input().split())
        update_path(u - 1, v - 1)
        out.append(str(sumw[1] % MOD))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The first preprocessing phase uses an iterative traversal because Python's default recursion depth is not suitable for a tree that can be a chain of (2\cdot10^5) vertices. The `order` array records a root-to-leaf traversal order, and processing it backwards gives subtree sizes without recursion.

The heavy child is chosen after subtree sizes are known. The decomposition then walks each heavy chain directly and pushes light children onto a stack. This produces contiguous positions for every heavy chain, which is exactly what the segment tree needs.

The coefficient array is indexed by the position of the child vertex. If vertex (v) is not the root, that position represents the edge from `parent[v]` to (v). Its coefficient is `size[v] * (n - size[v])`.

The segment tree does not store a modulo-reduced sum internally. The largest possible total is below roughly (n^2\cdot10^6), which is comfortably within Python integers and also within signed 64-bit arithmetic. Avoiding a modulo operation during every merge and assignment makes the implementation faster. Only the value printed to the user is reduced modulo (10^9+7).

The `lazy` value represents an assignment, not an increment. A value of `-1` means there is no pending assignment. Since edge weights are always nonnegative, `-1` is an unambiguous marker.

The minimum and maximum optimization is the subtle part of the segment tree. Suppose a node contains weights between 16 and 25. Both endpoints have square roots 4 and 5, so the result is not uniform. The node must be split. If instead the node contains values between 16 and 24, the square roots range from 4 to 4, so every value becomes 4 and the entire node can be assigned at once.

The final HLD interval starts at `pos[v] + 1` when both endpoints are on the same chain. This is the most common off-by-one point in this problem. Vertex positions represent incoming edges, so the LCA's position represents the edge from its parent into the LCA, which is not part of the queried path.

## Worked Examples

The official sample is

```
5 3
1 2 4
2 3 4
1 4 9
1 5 16
1 5
1 3
1 4
```

After rooting at city 1, the edge coefficients are 6 for edge (1-2), 4 for edge (2-3), 4 for edge (1-4), and 4 for edge (1-5).

| State | Edge (1-2) | Edge (2-3) | Edge (1-4) | Edge (1-5) | Total |
| --- | --- | --- | --- | --- | --- |
| Initial | (4\cdot6=24) | (4\cdot4=16) | (9\cdot4=36) | (16\cdot4=64) | 140 |
| Query (1,5) | 24 | 16 | 36 | (4\cdot4=16) | 92 |
| Query (1,3) | (2\cdot6=12) | (2\cdot4=8) | 36 | 16 | 72 |
| Query (1,4) | 12 | 8 | (3\cdot4=12) | 16 | 48 |

The first query only changes edge (1-5), because it is the only edge on the path from 1 to 5. The second query changes the two edges from 1 to 3. The last query changes edge (1-4). The output is consequently

```
140
92
72
48
```

The second example stresses repeated transformations.

```
3 3
1 2 16
2 3 9
1 3
1 3
1 3
```

Both edges have coefficient 2.

| Query | Weight (1-2) | Weight (2-3) | Total |
| --- | --- | --- | --- |
| Initial | 16 | 9 | 50 |
| (1,3) | 4 | 3 | 14 |
| (1,3) | 2 | 1 | 6 |
| (1,3) | 1 | 1 | 4 |

The trace demonstrates why an edge cannot simply be marked as "already processed" after its first innovation. It remains eligible until its weight reaches 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m\log^2 n+n\log n\log\log W)) amortized | HLD creates (O(\log n)) segment intervals per query, while every edge changes only (O(\log\log W)), at most five, times |
| Space | (O(n)) | The tree, HLD arrays, and segment tree all use linear memory |

For (n,m\le2\cdot10^5), the important fact is that the expensive part of a path update cannot happen indefinitely. Every road weight falls through only a handful of square-root levels before reaching 1. The segment tree additionally collapses uniform ranges into lazy assignments. The implementation uses iterative tree preprocessing and compact integer arrays to keep Python memory usage reasonable under the 256 MB limit.

## Test Cases

The following test harness assumes the `solve()` function from the solution above is present. It redirects standard input and output so each complete input can be checked independently.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Official sample
sample = """\
5 3
1 2 4
2 3 4
1 4 9
1 5 16
1 5
1 3
1 4
"""
assert run(sample) == "140\n92\n72\n48", "official sample"

# Minimum-size tree, no edges at all.
case_min = """\
1 1
1 1
"""
assert run(case_min) == "0\n0", "single city"

# Weight 1 must never change.
case_one = """\
2 1
1 2 1
1 2
"""
assert run(case_one) == "1\n1", "weight already one"

# All equal values and repeated full-path updates.
case_equal = """\
4 2
1 2 4
2 3 4
3 4 4
1 4
1 4
"""
assert run(case_equal) == "40\n20\n10", "all equal weights"

# Boundary sequence 16 -> 4 -> 2 -> 1 and 9 -> 3 -> 1.
case_repeated = """\
3 3
1 2 16
2 3 9
1 3
1 3
1 3
"""
assert run(case_repeated) == "50\n14\n6\n4", "repeated square roots"

# Maximum-size structural test.
# A path of 200000 vertices with every edge equal to 1.
# Every query is the whole path, so the answer never changes.
n = 200000
m = 200000

initial = n * (n - 1) * (n + 1) // 6
expected_line = str(initial % 1_000_000_007) + "\n"
expected = expected_line * (m + 1)

parts = [f"{n} {m}"]
for i in range(1, n):
    parts.append(f"{i} {i + 1} 1")
for _ in range(m):
    parts.append(f"1 {n}")

max_case = "\n".join(parts) + "\n"

assert run(max_case) == expected, "maximum-size all-one path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, query `1 1` | `0, 0` | No edges and an empty path |
| Two cities with edge weight 1 | `1, 1` | Already-minimal weight |
| Four-city path with all weights 4 | `40, 20, 10` | Equal values and repeated full-path updates |
| Three-city path with weights 16 and 9 | `50, 14, 6, 4` | Multiple square-root levels and repeated queries |
| 200000-city path with all weights 1 | Same value on all 200001 lines | Maximum (n,m), long paths, and skipping unchanged ranges |

## Edge Cases

### A single city

For

```
1 1
1 1
```

the segment tree contains only the artificial root position. Its coefficient is zero, so its weighted contribution is zero. The path update sees that both endpoints are the same vertex and returns without touching the segment tree. The output is

```
0
0
```

The implementation handles this because all HLD intervals are empty when `u == v`, and the segment tree still has a valid single-element root.

### Weight already equal to 1

For

```
2 1
1 2 1
1 2
```

the only edge has coefficient (1). Its initial contribution is (1). During the query, the segment tree sees `mx == 1` and returns immediately. No assignment and no contribution change occur. The output is

```
1
1
```

This early termination is also what keeps repeated queries cheap after all roads on a path have reached 1.

### Repeated transformations

For

```
3 3
1 2 16
2 3 9
1 3
1 3
1 3
```

the first query changes (16\to4) and (9\to3). The second changes (4\to2) and (3\to1). The third changes (2\to1), while the other edge is already 1. The totals are (50,14,6,4).

The segment tree's minimum and maximum values make the third query efficient. Once a range contains only weights 1, its maximum is 1 and the recursion stops before visiting any leaves.

### The lowest common ancestor

Consider

```
3 1
1 2 4
2 3 4
1 3
```

The path contains both edges, so the initial answer is

[
4\cdot2+4\cdot2=16.
]

After the query both weights become 2, giving

[
2\cdot2+2\cdot2=8.
]

The output is

```
16
8
```

When the endpoints are on the same heavy chain, the update must cover positions from `pos[1] + 1` through `pos[3]`. The position of the LCA itself represents the incoming edge to the LCA and must be excluded. This is exactly why the final HLD interval uses `pos[v] + 1`.

### A path with no effective changes

Suppose a large tree contains many edges of weight 1, and a query path consists entirely of those edges. The answer before and after the query is identical. The segment tree recognizes this using the maximum value. The query still performs the HLD decomposition, but every segment immediately returns without descending. This prevents the worst-case behavior from depending on the physical length of an unchanged path.
