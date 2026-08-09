---
title: "CF 102471K - All Pair Maximum Flow"
description: "The graph is drawn inside a convex polygon whose vertices are numbered cyclically. Every polygon side is present, and additional diagonals may be added, but the diagonals never cross except at common endpoints. Each edge has a nonnegative capacity."
date: "2026-08-09T18:51:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "K"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 530
verified: true
draft: false
---

[CF 102471K - All Pair Maximum Flow](https://codeforces.com/problemset/problem/102471/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph is drawn inside a convex polygon whose vertices are numbered cyclically. Every polygon side is present, and additional diagonals may be added, but the diagonals never cross except at common endpoints. Each edge has a nonnegative capacity.

For every pair of vertices (s,t), we need the value of the maximum (s)-(t) flow, which is the same as the minimum capacity of an (s)-(t) cut. The required output is the sum of these values over all unordered vertex pairs, reduced modulo (998244353). The original problem has (n\le 200000) and (m\le 400000), with every polygon side present.

The constraints immediately rule out doing anything independently for every pair. There are

[
\frac{n(n-1)}2
]

pairs, which is almost (2\cdot 10^{10}) when (n=200000). Even an operation taking only (O(m)) time per pair would already require roughly (8\cdot10^{15}) edge examinations. A real maximum-flow algorithm is substantially more expensive than simply scanning the edges, so the solution has to exploit the planar structure globally.

There are several edge cases that are easy to mishandle. The smallest graph is a triangle. With three edges of capacity one,

```
3 3
1 2 1
2 3 1
3 1 1
```

the answer is `6`, not `3`. Every pair has two units of flow because the direct edge and the two-edge alternative path can both carry flow.

Zero capacities are also legal. For

```
3 3
1 2 0
2 3 1
3 1 2
```

the answer is `4`. The zero-capacity edge does not make every pair disconnected. For example, the maximum flow between vertices (1) and (3) is still (2), because the cut consisting of the two edges incident to vertex (1) has capacity (2).

Large capacities require 64-bit arithmetic before taking the final modulus. For

```
3 3
1 2 1000000000
2 3 1000000000
3 1 1000000000
```

every pair has flow (2000000000), so the unmodded answer is (6000000000). The required output is `10533882`.

Finally, the edge ((1,n)) needs special treatment when constructing the planar structure. It crosses the cyclic boundary of the vertex numbering, so treating all edges merely as intervals ([u,v]) without separating this edge leads to an incorrect nesting structure.

## Approaches

The brute-force approach is conceptually simple. For every pair (s,t), run a maximum-flow algorithm and add its result to the answer. By the max-flow min-cut theorem this is correct, but there are (n(n-1)/2) calls. At (n=200000), that is exactly (19999900000) maximum-flow computations. Even if every computation magically took only (O(m)), the total would be about (8\cdot10^{15}) basic edge examinations. A genuine max-flow computation makes the situation much worse.

The useful observation comes from the planar embedding. Consider an edge (e) that currently lies on the boundary of the unbounded region, and suppose it has minimum capacity among all such boundary edges. Let (C) be the smallest cycle containing (e). We can remove (e), add its capacity to every other edge of (C), and preserve every pairwise minimum cut. This is the central reduction used for the problem.

Why does this work? In a planar graph, a cut between two vertices can be represented by a path in the planar dual after the unbounded face is split at the two terminals. A cycle (C) enclosing a bounded region cannot be crossed by such a dual path exactly once. If an optimal cut interacts with (C), it can be represented using (e) and one other edge of (C). Since (e) is the cheapest currently exposed boundary edge, replacing the exposed crossing by (e) does not increase the cut value.

Suppose the current capacity of (e) is (w). Removing (e) changes a cut that uses (e) by (-w). Adding (w) to every other edge of (C) compensates exactly whenever the cut uses another edge of (C). Cuts that avoid (C) are unchanged. Conversely, any cut in the modified graph can be extended with (e) when necessary to obtain a cut of no larger value in the original graph. Thus every pairwise minimum cut remains unchanged.

We can repeat this operation until only (n-1) edges remain. The graph is then a tree, and maximum flow between two vertices is simply the minimum edge capacity on their unique path. The original all-pairs problem has been reduced to a tree bottleneck problem.

The remaining challenge is finding the appropriate cycles efficiently. A direct simulation would require maintaining the changing outer boundary of the planar graph. A cleaner representation uses a tree derived from the noncrossing diagonals. The diagonals are sorted by decreasing left endpoint and increasing right endpoint. An ordered structure representing the current boundary tells us which previous edge belongs to the new face created by each diagonal. This produces a tree with (m+1) nodes, where each original graph edge corresponds to one tree edge.

The implementation below uses a Fenwick tree instead of an ordered map. Active boundary pieces are stored by their polygon positions. For a diagonal ((l,r)), all active positions in ([l,r)) become children of that diagonal, and the diagonal is then inserted at position (l). Since every active position is removed only when it becomes a child, the total number of such removals is linear. Each Fenwick operation costs (O(\log n)).

Once this auxiliary tree exists, process its leaves from smallest available capacity upward. When a face becomes exposed, its selected edge is deleted and its capacity is propagated to the other incident edges. A priority queue maintains the next candidate edge. Every auxiliary-tree edge enters the queue at most once, so the total processing cost is (O(m\log m)). This is the same reduction described by the standard solution approach for this problem.

Finally, the surviving (n-1) original edges form a tree. Sort them by transformed capacity in decreasing order. Initially every original vertex is a separate DSU component. When an edge of weight (w) joins components of sizes (a) and (b), exactly (ab) vertex pairs become connected for the first time at threshold (w), so (w\cdot a\cdot b) is added to the answer. This is the descending version of the usual Kruskal bottleneck counting argument.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | At least (O(n^2m)) edge examinations, much more with actual max-flow | (O(n+m)) | Too slow |
| Optimal | (O(m\log m+n\log n)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Read all edges and separate polygon sides from diagonals. Every side ((i,i+1)) is represented by its position (i), while the special side ((1,n)) is represented by position (n). Every other edge is a diagonal ((l,r)) with (l<r).
2. Sort all diagonals by decreasing (l), breaking ties by increasing (r). This ordering follows the nesting structure of noncrossing diagonals. A later diagonal can only interact with the currently exposed boundary pieces that lie inside its interval.
3. Maintain one active edge for each currently exposed polygon position. A Fenwick tree stores which positions are active, while `edge_at[pos]` tells us which original edge occupies that position. For a diagonal ((l,r)), repeatedly find the first active position in ([l,r)). Assign that edge's auxiliary-tree parent to the diagonal and remove the position from the active set.
4. After all active positions in ([l,r)) have been removed, insert the diagonal itself at position (l). This represents the newly created face by a single representative boundary position. Because the graph is noncrossing, the resulting parent relationships form a tree.
5. After all diagonals have been processed, connect every still-active boundary edge to a single root node (m+1). Each original edge (i) now corresponds to the auxiliary-tree edge between node (i) and node `fa[i]`.
6. Initially, every leaf of the auxiliary tree represents a face with exactly one boundary edge leading to its parent. Put all such edges into a min-heap and mark the corresponding leaf as exposed. The heap key is the capacity currently associated with that boundary edge.
7. Remove the smallest heap entry. If the other endpoint of that auxiliary edge has already become exposed, the edge has become part of an already processed boundary, so add the current value to its transformed weight.
8. Otherwise, expose the other endpoint. The edge used to expose it is deleted from the transformed graph, so mark its transformed weight with a very negative sentinel. The capacity used to expose the face is then added to every other incident auxiliary-tree edge. If the neighboring face has not been exposed yet, push that edge into the heap with its newly increased capacity.
9. Continue until the heap is empty. Every original edge marked with a nonnegative transformed weight is one of the (n-1) edges of the final tree. Every deleted edge has the negative sentinel.
10. Sort the surviving edges by transformed weight in decreasing order. Initialize a DSU with one component for every original graph vertex. For each tree edge ((u,v)) with weight (w), find the two current components containing its endpoints. If their sizes are (a) and (b), add (wab) to the answer and merge the components.
11. Reduce the accumulated answer modulo (998244353) and print it.

The invariant behind the whole algorithm is that every transformation preserves the minimum cut between every pair of original vertices. The cycle operation preserves each cut value, so after all deletions the final tree has exactly the same pairwise maximum-flow values as the original graph. On a tree, the value for a pair is the minimum edge on its unique path. Descending DSU processing groups precisely the pairs whose path minimum is the current edge weight, so every pair contributes exactly once. This proves that the final sum is the required sum of all maximum flows.

## Python Solution

```python
import sys
import heapq
from array import array

input = sys.stdin.readline

MOD = 998244353
NEG = -(10 ** 18)

def solve():
    n, m = map(int, input().split())

    # Original endpoints and capacities.
    eu = array('i', [0]) * (m + 1)
    ev = array('i', [0]) * (m + 1)
    cap = array('q', [0]) * (m + 1)

    # fa[i] is the parent of auxiliary-tree node i.
    fa = array('i', [0]) * (m + 2)

    # Active boundary position -> original edge id.
    edge_at = array('i', [0]) * (n + 1)

    diagonals = []

    for eid in range(1, m + 1):
        u, v, w = map(int, input().split())
        if u > v:
            u, v = v, u

        eu[eid] = u
        ev[eid] = v
        cap[eid] = w

        if v == u + 1:
            edge_at[u] = eid
        elif u == 1 and v == n:
            edge_at[n] = eid
        else:
            diagonals.append((u, v, eid))

    # Fenwick tree containing 1 exactly at active positions.
    bit = array('i', [0]) * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    def bit_add(i, delta):
        while i <= n:
            bit[i] += delta
            i += i & -i

    def bit_sum(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    def bit_kth(k):
        """Return the position of the k-th active point, 1-indexed."""
        pos = 0
        step = 1 << (n.bit_length() - 1)
        while step:
            nxt = pos + step
            if nxt <= n and bit[nxt] < k:
                k -= bit[nxt]
                pos = nxt
            step >>= 1
        return pos + 1

    # The nesting order of noncrossing diagonals.
    diagonals.sort(key=lambda x: (-x[0], x[1]))

    for l, r, eid in diagonals:
        before = bit_sum(l - 1)
        right = bit_sum(r - 1)

        # Every active position in [l, r) becomes a child of eid.
        while before < right:
            pos = bit_kth(before + 1)
            old_edge = edge_at[pos]

            fa[old_edge] = eid
            edge_at[pos] = 0
            bit_add(pos, -1)

            right -= 1

        # The new diagonal becomes the representative of this face.
        edge_at[l] = eid
        bit_add(l, 1)

    root = m + 1

    # Remaining active boundary pieces belong to the outer root.
    for pos in range(1, n + 1):
        eid = edge_at[pos]
        if eid:
            fa[eid] = root

    # The auxiliary tree is represented by parent -> children links.
    head = array('i', [-1]) * (m + 2)
    nxt = array('i', [-1]) * (m + 1)

    for eid in range(1, m + 1):
        p = fa[eid]
        nxt[eid] = head[p]
        head[p] = eid

    # nw[i] is the final transformed weight of original edge i.
    nw = array('q', [0]) * (m + 1)
    vis = bytearray(m + 2)

    heap = []

    # Every non-root leaf is initially an exposed face.
    for i in range(1, m + 1):
        if head[i] == -1:
            heapq.heappush(heap, (cap[i], i, fa[i]))
            vis[i] = 1

    while heap:
        cur, u, v = heapq.heappop(heap)

        if vis[v]:
            # Both sides are already exposed. The edge contributes
            # its current value to its transformed weight.
            nw[u] += cur
            continue

        # Expose face v through auxiliary edge u-v.
        vis[v] = 1
        nw[u] = NEG

        # The parent side of v is another incident edge.
        p = fa[v]
        if p != 0:
            if vis[p]:
                nw[v] += cur
            else:
                heapq.heappush(heap, (cur + cap[v], v, p))

        # Process all child sides of v except the edge we arrived through.
        c = head[v]
        while c != -1:
            if c != u:
                if vis[c]:
                    nw[c] += cur
                else:
                    heapq.heappush(heap, (cur + cap[c], v, c))
            c = nxt[c]

    # The non-deleted edges form the final tree.
    tree_edges = []
    for eid in range(1, m + 1):
        if nw[eid] >= 0:
            tree_edges.append((nw[eid], eu[eid], ev[eid]))

    tree_edges.sort(reverse=True)

    # Descending Kruskal on the final tree.
    parent = array('i', range(n + 1))
    size = array('i', [1]) * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    ans = 0

    for w, u, v in tree_edges:
        ru = find(u)
        rv = find(v)

        if ru == rv:
            continue

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        ans = (
            ans
            + (w % MOD) * (size[ru] % MOD) % MOD
            * (size[rv] % MOD)
        ) % MOD

        parent[rv] = ru
        size[ru] += size[rv]

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The first part stores every original edge in compact integer arrays. Python lists of hundreds of thousands of Python integers can consume substantial memory, so `array` and `bytearray` are used for the large numerical structures.

The diagonal construction uses the Fenwick tree as an ordered set. `bit_sum(r-1)-bit_sum(l-1)` tells us how many active boundary representatives lie in ([l,r)). `bit_kth` locates the first one, after which that position is removed. Every removal happens only once, so although each individual operation costs (O(\log n)), the total number of removals is linear.

The auxiliary tree uses `head` and `nxt` rather than lists of Python tuples. Node (i) has parent `fa[i]`, and `head[v]` gives the first child of (v). This representation is enough because the tree is rooted at the artificial outer-face node.

The heap stores `(current_capacity, child, parent)`. The candidate is inserted only when one side of the auxiliary edge becomes exposed while the other side has not. Consequently every auxiliary edge creates at most one heap entry. When an entry is processed, `vis[v]` tells us whether the other face has already been exposed.

The negative sentinel is deliberately much smaller than any possible transformed capacity. Every original capacity is at most (10^9), and there are at most (4\cdot10^5) additions, so every valid transformed capacity is below (4\cdot10^{14}). `-10**18` is therefore safely separated from all valid values.

The final DSU processes edges in decreasing order. Because the surviving graph is a tree, the endpoints of every surviving edge are in different DSU components when that edge is processed. The product of their component sizes counts exactly the pairs whose path first becomes connected at this edge's threshold.

Python integers do not overflow, but the arrays storing capacities use signed 64-bit integers. The largest possible transformed capacity is comfortably inside that range. The answer is reduced modulo (998244353) after every DSU contribution.

## Worked Examples

### Sample 1

The sample has six polygon vertices and two diagonals. The diagonal intervals are ((1,4)) and ((1,5)), so the auxiliary-tree construction gives the following parent relationships:

[
1,2,3\rightarrow7,\qquad
7,4\rightarrow8,\qquad
8,5,6\rightarrow9.
]

Here nodes (1) through (6) represent the polygon edges, nodes (7) and (8) represent the two diagonals, and node (9) is the artificial outer root.

The important processing states are:

| Step | Heap edge value | Exposed node | Important transformed weights |
| --- | --- | --- | --- |
| 1 | 1 | 7 | (w_2=1,\ w_3=1,\ w_1=-\infty) |
| 2 | 10 | 7 already exposed | (w_2=11) |
| 3 | 100 | 7 already exposed | (w_3=101) |
| 4 | 1000 | 8 | (w_4=-\infty,\ w_7=1000) |
| 5 | 10000 | 9 | (w_5=-\infty,\ w_6=10000,\ w_8=10000) |
| 6 | 100000 | 9 already exposed | (w_6=110000) |
| 7 | 1000001 | 8 already exposed | (w_7=1001001) |
| 8 | 10001000 | 9 already exposed | (w_8=10011000) |

The surviving edges are therefore:

| Edge | Endpoints | Transformed capacity |
| --- | --- | --- |
| 2 | (2,3) | 11 |
| 3 | (3,4) | 101 |
| 6 | (6,1) | 110000 |
| 7 | (1,4) | 1001001 |
| 8 | (1,5) | 10011000 |

The descending DSU calculation is:

| Weight | Component sizes | Pair contribution |
| --- | --- | --- |
| 10011000 | (1\cdot1) | 10011000 |
| 1001001 | (2\cdot1) | 2002002 |
| 110000 | (3\cdot1) | 330000 |
| 101 | (4\cdot1) | 404 |
| 11 | (5\cdot1) | 55 |

The sum is

[
10011000+2002002+330000+404+55
=12343461.
]

This demonstrates the complete reduction: the complicated planar graph becomes a five-edge tree whose bottleneck values encode every original pairwise maximum flow. The official sample has the same output.

### Custom Triangle

Consider

```
3 3
1 2 1
2 3 1
3 1 1
```

There are no diagonals, so the auxiliary tree is simply a root connected to all three polygon edges.

| Step | Heap value | Exposed node | Transformed weights |
| --- | --- | --- | --- |
| 1 | 1 | root | (w_1=-\infty,\ w_2=1,\ w_3=1) |
| 2 | 1 | root already exposed | (w_2=2) |
| 3 | 1 | root already exposed | (w_3=2) |

The surviving tree contains two edges of capacity (2). The DSU contributions are (2\cdot1\cdot1=2) and (2\cdot2\cdot1=4), giving `6`.

This example confirms that a cycle can provide more flow than any single edge. The reduction preserves that extra connectivity by increasing the surviving tree capacities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m\log m+n\log n)) | Diagonal sorting, Fenwick operations, heap processing, and final edge sorting |
| Space | (O(n+m)) | Original edges, auxiliary tree, Fenwick tree, heap, and DSU |

The input has (m\le400000), so (m) is only a constant factor larger than (n). The algorithm therefore behaves as (O(m\log m)), which is suitable for the intended limits. The large structures in the Python implementation use compact arrays where practical, keeping memory proportional to the graph size.

## Test Cases

The following tests assume the `solve()` function from the Python Solution section is available.

```python
import sys
import io

# helper: run solution on input string, return output string
def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("""\
6 8
1 2 1
2 3 10
3 4 100
4 5 1000
5 6 10000
6 1 100000
1 4 1000000
1 5 10000000
""") == "12343461", "sample"

# Minimum-size graph, all equal capacities.
# Every pair has flow 2, and there are 3 pairs.
assert run("""\
3 3
1 2 1
2 3 1
3 1 1
""") == "6", "minimum triangle"

# Zero capacity boundary edge.
assert run("""\
3 3
1 2 0
2 3 1
3 1 2
""") == "4", "zero capacity"

# A diagonal crossing the cyclic boundary of the numbering structure.
# The graph is a 4-cycle plus diagonal (1,3), all capacities 1.
assert run("""\
4 5
1 2 1
2 3 1
3 4 1
4 1 1
1 3 1
""") == "13", "diagonal and boundary handling"

# Maximum-size graph with all capacities equal to 1.
# It is just a cycle, so every pair has flow 2.
# The answer is n * (n - 1) modulo 998244353.
n = 200000
lines = [f"{n} {n}"]
for i in range(1, n):
    lines.append(f"{i} {i + 1} 1")
lines.append(f"{n} 1 1")

maximum_case = "\n".join(lines) + "\n"
assert run(maximum_case) == "70025880", "maximum-size cycle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle with three unit edges | `6` | Minimum size and cycle flow |
| Triangle with capacities (0,1,2) | `4` | Zero capacities |
| Four-cycle plus diagonal (1,3) | `13` | Diagonal nesting and cyclic boundary edge |
| (n=m=200000) unit-capacity cycle | `70025880` | Maximum size, equal values, and performance |

## Edge Cases

The minimum-size triangle

```
3 3
1 2 1
2 3 1
3 1 1
```

starts with three auxiliary leaves attached to the root. The first leaf is deleted and the other two receive its capacity, making their transformed capacities equal to (2). The resulting tree has two edges of weight (2), so its three vertex pairs contribute (2+2+2=6). The algorithm never assumes that the original graph is already a tree.

The zero-capacity case

```
3 3
1 2 0
2 3 1
3 1 2
```

selects the zero-capacity edge first. Its capacity is added to the other edges, so nothing changes numerically. The remaining tree has capacities (1) and (2). Its pairwise bottleneck values are (1,1,2), giving `4`. This shows why zero must remain a valid heap value and why the deletion sentinel must be negative rather than using zero to mean "deleted".

The diagonal case

```
4 5
1 2 1
2 3 1
3 4 1
4 1 1
1 3 1
```

contains the cyclic boundary edge ((1,4)) together with the diagonal ((1,3)). The diagonal construction treats ((1,4)) as the boundary position (4), rather than as an ordinary interval from (1) to (4). The resulting transformed tree preserves all six pairwise flows, whose sum is `13`. Mishandling this single wraparound edge changes the auxiliary tree and can silently produce a different answer.

The maximum-capacity triangle

```
3 3
1 2 1000000000
2 3 1000000000
3 1 1000000000
```

produces a transformed tree with two edges of capacity (2000000000). The unmodded sum is (6000000000), and the required result is `10533882`. The implementation keeps capacities in signed 64-bit arrays and performs the final aggregation modulo (998244353), so neither the original capacities nor the intermediate transformed values overflow.
