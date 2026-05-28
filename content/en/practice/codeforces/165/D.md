---
title: "CF 165D - Beard Graph"
description: "The graph in this problem is almost a simple path. Every vertex has degree at most 2, except possibly one special vertex that may have larger degree. A tree with this shape looks like several chains glued together at one center. Initially every edge is black."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "trees"]
categories: ["algorithms"]
codeforces_contest: 165
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 112 (Div. 2)"
rating: 2100
weight: 165
solve_time_s: 133
verified: true
draft: false
---

[CF 165D - Beard Graph](https://codeforces.com/problemset/problem/165/D)

**Rating:** 2100  
**Tags:** data structures, dsu, trees  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph in this problem is almost a simple path. Every vertex has degree at most 2, except possibly one special vertex that may have larger degree. A tree with this shape looks like several chains glued together at one center.

Initially every edge is black. Queries can repaint an edge white or black, and can also ask for the shortest path between two vertices using only black edges.

Since the graph is a tree, the shortest path between two vertices is unique. The real question in each type-3 query is whether every edge on that unique path is currently black. If yes, the answer is simply the number of edges on the path. If even one edge is white, the answer is `-1`.

The constraints are large enough that recomputing paths directly is impossible. The graph has up to `10^5` vertices and there are up to `3 * 10^5` queries. A naive DFS or BFS for every distance query would cost `O(n)` per query, which becomes roughly `3 * 10^10` operations in the worst case. That is far beyond the limit.

The unusual structure of the graph is the key. A normal tree would require a heavy tree data structure such as Heavy-Light Decomposition. Here we can do something much simpler because the tree is either a path or several paths connected at one center vertex.

There are a few edge cases that easily break careless implementations.

Consider a pure path:

```
1 - 2 - 3 - 4
```

If edge `(2,3)` becomes white, then vertices `1` and `4` are disconnected even though both are still connected to other vertices. A solution that only tracks connected components lazily may accidentally report distance `3`.

Another subtle case is when one endpoint is the center vertex. For example:

```
    2
    |
1 - 3 - 4
    |
    5
```

If edge `(3,4)` is white, then queries from `3` to `4` must return `-1`, while queries from `3` to `2` still work. The center itself is not special in connectivity logic, only in decomposition.

There is also the case where both vertices lie on the same branch. Example:

```
1 - 2 - 3 - 4
      |
      5
```

The path from `1` to `2` never touches the center branching structure. A solution that always routes through the center would overcount distances or inspect wrong edges.

Finally, queries may ask for distance from a vertex to itself. Even if many edges are white, the answer must still be `0` because the empty path uses no edges.

## Approaches

The brute-force solution is straightforward. For every distance query, run BFS or DFS using only black edges and compute the shortest path. Since the graph is a tree, DFS alone is enough. Edge repainting is trivial because we only update a color array.

This works logically because the graph is small enough conceptually to explore directly. The problem is scale. A single DFS may visit all `10^5` vertices. Repeating this for `3 * 10^5` queries leads to tens of billions of operations.

The graph structure gives a much stronger property. Since there is at most one high-degree vertex, the tree can be decomposed into several independent chains starting from the center. Every vertex belongs to exactly one branch.

Suppose the special center is `c`.

Every path falls into one of two categories.

If both vertices are on the same branch, the path stays entirely inside that branch.

If they are on different branches, the path must go through `c`.

This turns the problem into maintaining black segments on arrays.

For each branch, assign positions increasing away from the center. Then each edge corresponds to exactly one position on exactly one branch.

Now a path is valid if every edge in a contiguous interval is black. This becomes a range-sum query problem.

We maintain a Fenwick tree over all edge positions. White edges contribute `1`, black edges contribute `0`.

Then:

If the number of white edges on the path is zero, the path exists.

Otherwise, it does not.

Distance computation is independent of colors because the underlying tree never changes. We precompute depths once and use them directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the tree and compute degrees of all vertices.
2. Find the center vertex. This is the only vertex whose degree may exceed 2. If no such vertex exists, the tree is just a path, and any vertex can serve as the center.
3. Starting from every neighbor of the center, walk along the chain and assign:

- which branch each vertex belongs to,
- its depth from the center,
- a linear position for each edge.

Every branch becomes a contiguous interval in a Fenwick tree.
4. For every edge, store the Fenwick tree index representing that edge. Initially all edges are black, so the Fenwick tree starts with zeros.
5. For a query that paints an edge white, add `1` at that edge's Fenwick position.
6. For a query that paints an edge black, add `-1` at that edge's Fenwick position.
7. For a distance query between `a` and `b`, first handle the trivial case `a == b`. The answer is `0`.
8. If `a` and `b` belong to the same branch, then the path is a contiguous segment inside that branch.

Query the Fenwick tree on the interval between their depths.

If the sum is zero, return the absolute depth difference.

Otherwise return `-1`.
9. If `a` and `b` belong to different branches, then the path must go through the center.

Query the segment from `a` up to the center and from `b` up to the center.

If both segments contain no white edges, return `depth[a] + depth[b]`.

Otherwise return `-1`.

### Why it works

Each edge belongs to exactly one branch and appears exactly once in the Fenwick tree. Because the graph is a tree, every pair of vertices has a unique simple path.

If two vertices lie on the same branch, their path is exactly the interval between their depths on that chain.

If they lie on different branches, their path is the concatenation of:

- vertex `a` up to the center,
- center down to vertex `b`.

The Fenwick tree stores exactly which edges are white. A path exists if and only if the count of white edges on all required intervals is zero. Since the stored distances are the actual tree depths from the center, the reported length is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, l, r):
        if l > r:
            return 0
        return self.sum(r) - self.sum(l - 1)

def solve():
    n = int(input())

    edges = [None]
    g = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)

    for i in range(1, n):
        u, v = map(int, input().split())
        edges.append((u, v))

        g[u].append((v, i))
        g[v].append((u, i))

        deg[u] += 1
        deg[v] += 1

    center = 1
    for i in range(1, n + 1):
        if deg[i] > 2:
            center = i
            break

    branch = [0] * (n + 1)
    depth = [0] * (n + 1)

    edge_pos = [0] * n

    timer = 0
    branch_id = 0

    for nxt, eid in g[center]:
        branch_id += 1

        prev = center
        cur = nxt
        d = 1

        while True:
            branch[cur] = branch_id
            depth[cur] = d

            timer += 1
            edge_pos[eid] = timer

            next_vertex = -1
            next_edge = -1

            for to, ne in g[cur]:
                if to != prev:
                    next_vertex = to
                    next_edge = ne
                    break

            if next_vertex == -1:
                break

            prev = cur
            cur = next_vertex
            eid = next_edge
            d += 1

    bit = Fenwick(n)

    black = [1] * n

    def path_white_same_branch(a, b):
        da = depth[a]
        db = depth[b]

        if da > db:
            da, db = db, da

        return bit.range_sum(da + 1, db)

    def path_white_to_center(v):
        return bit.range_sum(1, depth[v])

    q = int(input())

    ans = []

    for _ in range(q):
        query = list(map(int, input().split()))

        if query[0] == 1:
            eid = query[1]

            if black[eid] == 0:
                black[eid] = 1
                bit.add(edge_pos[eid], -1)

        elif query[0] == 2:
            eid = query[1]

            if black[eid] == 1:
                black[eid] = 0
                bit.add(edge_pos[eid], 1)

        else:
            a, b = query[1], query[2]

            if a == b:
                ans.append("0")
                continue

            if a == center:
                white = path_white_to_center(b)
                if white == 0:
                    ans.append(str(depth[b]))
                else:
                    ans.append("-1")
                continue

            if b == center:
                white = path_white_to_center(a)
                if white == 0:
                    ans.append(str(depth[a]))
                else:
                    ans.append("-1")
                continue

            if branch[a] == branch[b]:
                white = path_white_same_branch(a, b)

                if white == 0:
                    ans.append(str(abs(depth[a] - depth[b])))
                else:
                    ans.append("-1")
            else:
                white = (
                    path_white_to_center(a)
                    + path_white_to_center(b)
                )

                if white == 0:
                    ans.append(str(depth[a] + depth[b]))
                else:
                    ans.append("-1")

    print("\n".join(ans))

solve()
```

The implementation starts by identifying the special center vertex. If no vertex has degree larger than two, the graph is just a path, and any endpoint choice still works because every node lies on one branch.

The branch construction step is the most important part. Starting from each neighbor of the center, we walk linearly until reaching a leaf. Since all non-center vertices have degree at most two, every branch is just a chain and can be traversed greedily.

Each traversed edge receives a Fenwick index. The key invariant is that edges along a branch receive consecutive indices in increasing depth order. This lets interval queries correspond exactly to path queries.

The Fenwick tree stores white edges, not black edges. A path is usable only when the queried sum is zero. This is slightly cleaner because repainting to white becomes adding `1`.

One subtle point is the query inside the same branch:

```
bit.range_sum(da + 1, db)
```

The edge connecting depth `k-1` to depth `k` is represented at position `k`. So the path between depths `da` and `db` uses edges `da+1 ... db`.

Another easy mistake is handling the center vertex. The center itself has depth `0` and belongs to no branch. Special handling avoids invalid interval queries.

## Worked Examples

### Sample 1

Input:

```
3
1 2
2 3
7
3 1 2
3 1 3
3 2 3
2 2
3 1 2
3 1 3
3 2 3
```

The tree is a simple path:

```
1 - 2 - 3
```

We choose `1` as center.

| Step | Query | White edges | Result |
| --- | --- | --- | --- |
| 1 | `3 1 2` | none | `1` |
| 2 | `3 1 3` | none | `2` |
| 3 | `3 2 3` | none | `1` |
| 4 | `2 2` | edge 2 becomes white |  |
| 5 | `3 1 2` | edge 2 not used | `1` |
| 6 | `3 1 3` | edge 2 blocks path | `-1` |
| 7 | `3 2 3` | edge 2 blocks path | `-1` |

This trace demonstrates that the algorithm checks only edges on the actual unique path. White edges elsewhere do not matter.

### Custom Example

Input:

```
5
1 3
2 3
3 4
3 5
6
3 1 4
2 3
3 1 4
3 2 5
1 3
3 2 5
```

The graph:

```
    2
    |
1 - 3 - 4
    |
    5
```

Edge 3 is `(3,4)`.

| Step | Query | White edges | Result |
| --- | --- | --- | --- |
| 1 | `3 1 4` | none | `2` |
| 2 | `2 3` | `(3,4)` white |  |
| 3 | `3 1 4` | path blocked | `-1` |
| 4 | `3 2 5` | unaffected | `2` |
| 5 | `1 3` | `(3,4)` black again |  |
| 6 | `3 2 5` | connected | `2` |

This example shows why different branches can be processed independently. Whitening one branch does not affect paths entirely inside other branches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Tree preprocessing is linear, each query performs Fenwick updates or range sums |
| Space | O(n) | Adjacency list, branch arrays, and Fenwick tree |

The preprocessing walks through each edge exactly once. Every repaint query performs one Fenwick update, and every distance query performs a constant number of Fenwick prefix sums. With `3 * 10^5` queries, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            while idx <= self.n:
                self.bit[idx] += val
                idx += idx & -idx

        def sum(self, idx):
            res = 0
            while idx > 0:
                res += self.bit[idx]
                idx -= idx & -idx
            return res

        def range_sum(self, l, r):
            if l > r:
                return 0
            return self.sum(r) - self.sum(l - 1)

    n = int(input())

    edges = [None]
    g = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)

    for i in range(1, n):
        u, v = map(int, input().split())
        edges.append((u, v))
        g[u].append((v, i))
        g[v].append((u, i))
        deg[u] += 1
        deg[v] += 1

    center = 1
    for i in range(1, n + 1):
        if deg[i] > 2:
            center = i
            break

    branch = [0] * (n + 1)
    depth = [0] * (n + 1)
    edge_pos = [0] * n

    timer = 0
    branch_id = 0

    for nxt, eid in g[center]:
        branch_id += 1

        prev = center
        cur = nxt
        d = 1

        while True:
            branch[cur] = branch_id
            depth[cur] = d

            timer += 1
            edge_pos[eid] = timer

            nx = -1
            ne = -1

            for to, ee in g[cur]:
                if to != prev:
                    nx = to
                    ne = ee
                    break

            if nx == -1:
                break

            prev = cur
            cur = nx
            eid = ne
            d += 1

    bit = Fenwick(n)
    black = [1] * n

    def path_same(a, b):
        da = depth[a]
        db = depth[b]
        if da > db:
            da, db = db, da
        return bit.range_sum(da + 1, db)

    def to_center(v):
        return bit.range_sum(1, depth[v])

    q = int(input())
    ans = []

    for _ in range(q):
        t, *rest = map(int, input().split())

        if t == 1:
            e = rest[0]
            if black[e] == 0:
                black[e] = 1
                bit.add(edge_pos[e], -1)

        elif t == 2:
            e = rest[0]
            if black[e] == 1:
                black[e] = 0
                bit.add(edge_pos[e], 1)

        else:
            a, b = rest

            if a == b:
                ans.append("0")
            elif a == center:
                ans.append(str(depth[b]) if to_center(b) == 0 else "-1")
            elif b == center:
                ans.append(str(depth[a]) if to_center(a) == 0 else "-1")
            elif branch[a] == branch[b]:
                ans.append(
                    str(abs(depth[a] - depth[b]))
                    if path_same(a, b) == 0
                    else "-1"
                )
            else:
                ans.append(
                    str(depth[a] + depth[b])
                    if to_center(a) + to_center(b) == 0
                    else "-1"
                )

    return "\n".join(ans)

# provided sample
assert run(
"""3
1 2
2 3
7
3 1 2
3 1 3
3 2 3
2 2
3 1 2
3 1 3
3 2 3
"""
) == "\n".join(["1", "2", "1", "1", "-1", "-1"]), "sample"

# minimum graph
assert run(
"""2
1 2
3
3 1 2
2 1
3 1 2
"""
) == "\n".join(["1", "-1"]), "minimum size"

# star-shaped beard
assert run(
"""5
1 3
2 3
3 4
3 5
5
3 1 2
2 1
3 1 2
3 4 5
3 3 3
"""
) == "\n".join(["2", "-1", "2", "0"]), "center handling"

# same branch query
assert run(
"""4
1 2
2 3
3 4
4
2 2
3 1 2
3 1 4
3 3 4
"""
) == "\n".join(["1", "-1", "1"]), "same branch intervals"

# repaint back to black
assert run(
"""3
1 2
2 3
5
2 1
3 1 3
1 1
3 1 3
3 2 2
"""
) == "\n".join(["-1", "2", "0"]), "repainting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum graph with one edge | `1`, `-1` | Correct handling of smallest tree |
| Star-shaped beard | `2`, `-1`, `2`, `0` | Center vertex logic |
| Same branch intervals | `1`, `-1`, `1` | Correct interval mapping |
| Repainting edge back black | `-1`, `2`, `0` | Fenwick updates work both ways |

## Edge Cases

Consider the case where both queried vertices are identical.

```
2
1 2
1
3 1 1
```

The algorithm immediately returns `0` before inspecting any edges. This is correct because the empty path always exists.

Now consider a disconnected path caused by one white edge.

```
4
1 2
2 3
3 4
3
2 2
3 1 4
3 1 2
```

Edge `(2,3)` becomes white.

For query `(1,4)`, the algorithm checks the interval covering depths `1..3`. The Fenwick tree reports one white edge, so the answer is `-1`.

For query `(1,2)`, the checked interval excludes the white edge entirely, so the answer is `1`.

Finally, consider branching through the center.

```
5
1 3
2 3
3 4
3 5
2
2 1
3 2 4
```

Edge `(1,3)` becomes white.

The path from `2` to `4` uses edges `(2,3)` and `(3,4)` only. The algorithm checks exactly those two branch segments. Since neither is white, the answer remains `2`.

This confirms the central invariant: only edges on the unique tree path matter.
