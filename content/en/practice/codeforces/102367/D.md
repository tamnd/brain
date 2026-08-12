---
title: "CF 102367D - Deliveries"
description: "The warehouses and roads form a tree, so between any two warehouses there is exactly one route. A truck has battery capacity T, and it may recharge whenever Sam stops."
date: "2026-08-12T23:36:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102367
codeforces_index: "D"
codeforces_contest_name: "Fall 2019 ICPC-style Waterloo Local Contest"
rating: 0
weight: 102367
solve_time_s: 546
verified: true
draft: false
---

[CF 102367D - Deliveries](https://codeforces.com/problemset/problem/102367/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The warehouses and roads form a tree, so between any two warehouses there is exactly one route. A truck has battery capacity `T`, and it may recharge whenever Sam stops. Every warehouse on the route is a mandatory stop, while stops in the middle of a road are optional charging stops.

Consider one road of length `D`. Starting with a full battery, the truck can cover at most `T` kilometres before another charging stop is necessary. Thus traversing this road requires `ceil(D / T)` travel segments. The first segment starts at the previous warehouse, and every additional segment requires one intermediate stop. Since every warehouse is already counted as a stop, the contribution of this road can be folded neatly into the formula

`1 + ceil(D / T)`

for the whole path, where the extra `1` accounts for the first warehouse of the route.

For a path containing edges with lengths `D1, D2, ..., Dk`, the answer is consequently

`1 + sum(ceil(Di / T))`.

The tree itself has up to `100000` vertices and the same order of magnitude of queries. Edge lengths and battery capacities are both at most `20000`. A query cannot afford to walk through its entire tree path, because a single path can contain `99999` edges and doing that for `100000` queries gives almost `10^10` edge visits. Even ordinary `O(log N)` tree queries are not enough by themselves because the edge cost depends on the query's `T`.

The small bound of `20000` on edge lengths is the second half of the structure. The function `ceil(D / T)` depends only on the edge length `D`, so for a fixed `T` it becomes a static edge weight. The solution combines this observation with a persistent segment tree over edge lengths.

There are several boundary cases that are easy to mishandle. If an edge length is exactly divisible by `T`, it needs exactly `D/T` travel segments, not `D/T + 1`. For example,

```
2 1
1 2 10
1 2 5
```

has answer `3`, because the two warehouse stops plus one charging stop are required. A formula using `floor(D/T)` for the number of charging intervals would be off by one.

If an edge has length at most `T`, it requires no intermediate charging stop. For example,

```
2 1
1 2 5
1 2 10
```

has answer `2`. The truck reaches warehouse 2 without stopping in the middle, so counting one charging stop merely because the edge exists would be incorrect.

A route can contain many mandatory warehouse stops even when the battery never needs recharging. For example,

```
3 1
1 2 1
2 3 1
1 3 10
```

has answer `3`, because Sam must stop at warehouses 1, 2, and 3. Counting only charging stops would incorrectly produce zero or one.

Finally, a very long road is not impossible. Sam is allowed to stop at an arbitrary point on a road, recharge, and continue. For example,

```
2 1
1 2 20
1 2 5
```

has answer `5`: four travel segments require three intermediate charging stops, plus the two warehouse stops. An implementation that rejects edges longer than `T` would solve a different problem.

## Approaches

The direct solution is to find the unique path between `S` and `F`, inspect every edge on that path, and add `ceil(D/T)`, finally adding one for the first warehouse. This is correct because every edge can be considered independently. The truck can recharge at the end of an edge before entering the next one, so the optimal number of charging stops on one edge does not interact with the other edges.

The problem is the path length. A tree can be a chain of `100000` vertices, so one query can inspect `99999` edges. With `100000` such queries, the worst case is roughly `10^10` edge operations, far beyond what the time limit allows.

The first useful observation is that for a fixed battery capacity `T`, every edge receives the static weight `ceil(D/T)`. Once those weights are fixed, a normal root-prefix sum plus LCA answers a path sum in constant time after the LCA has been found.

The difficulty is that `T` changes from query to query. There are only `20000` possible values of `T`, but building a complete root-prefix array for every possible `T` would require about `2 * 10^9` stored values, which is too much.

The second observation is that the edge length itself is also bounded by `20000`. For large `T`, the function `ceil(D/T)` changes only a small number of times as `D` ranges from `1` to `20000`. For example, if `T = 200`, the possible values are only `1, 2, ..., 100`. We can represent the path's edge lengths as a frequency distribution and sum these constant ranges rather than examining every edge.

A persistent segment tree gives exactly the required path frequency distribution. Root the original tree at vertex 1 and associate every non-root vertex with the length of the edge joining it to its parent. For every vertex `v`, build a persistent segment-tree version containing the edge lengths on the path from the root to `v`. The multiset of edge lengths on the path from `u` to `v` is then obtained from the versions of `u`, `v`, and their LCA:

`root[u] + root[v] - 2 * root[lca(u,v)]`.

Inside the persistent segment tree, a whole value interval can be processed at once whenever `ceil(D/T)` is constant throughout that interval. For large `T`, only a small number of such intervals exist.

For small `T`, the opposite strategy is better. We precompute the root-prefix sums for every small `T` that occurs in the queries. A threshold of `200` gives at most `200 * 100000 = 20 million` prefix values, which fit comfortably when stored as 32-bit integers. Queries with small `T` then need only an LCA and three array accesses.

This is a standard square-root style tradeoff. Small capacities are cheap to precompute, while large capacities have few distinct quotient ranges and are cheap to evaluate from the persistent structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(NQ)` | `O(N)` | Too slow |
| Optimal | `O(NB + Q(D/B)log D + Nlog N)` | `O(NB + Nlog D + Nlog N)` | Accepted |

Here `D <= 20000` is the maximum edge length and `B` is the small-capacity threshold used by the implementation, `200` in the code.

## Algorithm Walkthrough

1. Root the warehouse tree at vertex `1`. For every vertex, store its parent, depth, and the length of its parent edge. The parent edge is associated with the child, so a root-to-vertex path contains every edge exactly once.
2. Build binary lifting tables for the parents. This lets us find `lca(S,F)` in `O(log N)`, which identifies the common part of the two root paths.
3. Read all queries before doing the capacity-dependent preprocessing. Count which small values of `T` actually occur. There is no reason to build a prefix array for a capacity that no query uses.
4. For every used `T <= B`, construct a root-prefix array. For a vertex `v` with parent `p`, set

`pref[v] = pref[p] + ceil(edge[v] / T)`.

A query with this capacity is then answered by

`pref[S] + pref[F] - 2 * pref[LCA] + 1`.
5. Build a persistent segment-tree version for every vertex. Version `v` is obtained from version `parent[v]` by inserting exactly one value, the length of the edge from `parent[v]` to `v`. Persistence means that older versions remain unchanged.
6. For a query whose `T` is larger than `B`, first find its LCA and its number of path edges. If `T` is at least the maximum edge length in the entire tree, every edge has contribution `1`, so the answer is simply the number of path edges plus `1`.
7. Otherwise, evaluate the sum of `ceil(D/T)` over the path using the three persistent versions. At a segment-tree node representing `[lo, hi]`, compute the value of `ceil(D/T)` at both endpoints. If they are equal, every edge length in this entire segment has the same contribution, so multiply that contribution by the number of path edges represented by the node and stop descending.
8. If the contribution differs inside the segment, descend into its two children. The counts from the two endpoint versions are added and the LCA version is subtracted twice, giving exactly the frequency of edge lengths from that child segment on the requested path.
9. Add `1` after the path edge contribution has been computed. This is the initial warehouse stop. Every other warehouse stop is already represented implicitly by the `ceil(D/T)` contribution of the preceding edge.

### Why it works

For every road of length `D`, exactly `ceil(D/T)` battery-sized travel segments are necessary. Between consecutive segments there must be a charging stop, while the warehouses at the ends of the route and between roads are mandatory stops. Across a path with `k` edges, the total is exactly `1 + sum ceil(D/T)`.

For small `T`, the root-prefix array stores precisely this edge contribution on every root path, so the standard tree path subtraction gives the exact sum.

For large `T`, the persistent segment-tree versions represent exactly the multiset of edge lengths on each root path. Adding the versions of the two endpoints and subtracting the LCA version twice gives exactly the multiset of edges on the requested path. Every segment on which `ceil(D/T)` is constant can be replaced by its frequency multiplied by that constant. Descending only where the value changes therefore computes the same sum without inspecting individual path edges.

The invariant throughout both cases is that every edge on the requested tree path contributes exactly `ceil(D/T)` once, and no edge outside that path contributes anything. The final `+1` accounts for the first warehouse, completing the required stop count.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MAX_D = 20000
B = 200

def solve():
    n, q = map(int, input().split())

    head = array('i', [-1]) * n
    to = array('i')
    nxt = array('i')
    ew = array('i')

    def add_edge(u, v, w):
        idx = len(to)
        to.append(v)
        ew.append(w)
        nxt.append(head[u])
        head[u] = idx

    max_edge = 0

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        add_edge(u, v, w)
        add_edge(v, u, w)
        if w > max_edge:
            max_edge = w

    queries = []
    used_small = set()

    for _ in range(q):
        s, f, t = map(int, input().split())
        s -= 1
        f -= 1
        queries.append((s, f, t))
        if t <= B and t < max_edge:
            used_small.add(t)

    parent = array('i', [-1]) * n
    depth = array('i', [0]) * n
    parent_edge = array('i', [0]) * n
    order = array('i')
    order.append(0)
    parent[0] = 0

    idx = 0
    while idx < len(order):
        u = order[idx]
        idx += 1

        e = head[u]
        while e != -1:
            v = to[e]
            if v != parent[u]:
                parent[v] = u
                depth[v] = depth[u] + 1
                parent_edge[v] = ew[e]
                order.append(v)
            e = nxt[e]

    LOG = max(1, n.bit_length())
    up = [parent]

    for _ in range(1, LOG):
        prev = up[-1]
        cur = array('i', [0]) * n
        for v in range(n):
            cur[v] = prev[prev[v]]
        up.append(cur)

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        if a == b:
            return a

        for k in range(LOG - 1, -1, -1):
            ua = up[k][a]
            ub = up[k][b]
            if ua != ub:
                a = ua
                b = ub

        return parent[a]

    prefixes = {}

    for t in used_small:
        pref = array('i', [0]) * n
        for pos in range(1, n):
            v = order[pos]
            p = parent[v]
            pref[v] = pref[p] + (parent_edge[v] + t - 1) // t
        prefixes[t] = pref

    left = array('i', [0])
    right = array('i', [0])
    cnt = array('i', [0])
    roots = array('i', [0]) * n

    if max_edge > 0:
        for pos in range(1, n):
            v = order[pos]
            old_root = roots[parent[v]]
            value = parent_edge[v]

            new_root = len(cnt)
            left.append(left[old_root])
            right.append(right[old_root])
            cnt.append(cnt[old_root] + 1)

            cur_new = new_root
            cur_old = old_root
            lo = 1
            hi = max_edge

            while lo < hi:
                mid = (lo + hi) >> 1

                if value <= mid:
                    old_child = left[cur_old]
                    new_child = len(cnt)

                    left.append(left[old_child])
                    right.append(right[old_child])
                    cnt.append(cnt[old_child] + 1)

                    left[cur_new] = new_child
                    cur_new = new_child
                    cur_old = old_child
                    hi = mid
                else:
                    old_child = right[cur_old]
                    new_child = len(cnt)

                    left.append(left[old_child])
                    right.append(right[old_child])
                    cnt.append(cnt[old_child] + 1)

                    right[cur_new] = new_child
                    cur_new = new_child
                    cur_old = old_child
                    lo = mid + 1

            roots[v] = new_root

    sys.setrecursionlimit(1_000_000)

    def persistent_sum(ra, rb, rc, t):
        def dfs(a, b, c, lo, hi):
            total = cnt[a] + cnt[b] - 2 * cnt[c]
            if total == 0:
                return 0

            qlo = (lo + t - 1) // t
            qhi = (hi + t - 1) // t

            if qlo == qhi:
                return total * qlo

            mid = (lo + hi) >> 1
            ans = dfs(left[a], left[b], left[c], lo, mid)
            ans += dfs(right[a], right[b], right[c], mid + 1, hi)
            return ans

        return dfs(ra, rb, rc, 1, max_edge)

    out = []

    for s, f, t in queries:
        w = lca(s, f)
        edge_count = depth[s] + depth[f] - 2 * depth[w]

        if t >= max_edge:
            out.append(str(edge_count + 1))
            continue

        pref = prefixes.get(t)
        if pref is not None:
            value = pref[s] + pref[f] - 2 * pref[w] + 1
            out.append(str(value))
            continue

        value = persistent_sum(roots[s], roots[f], roots[w], t)
        out.append(str(value + 1))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The adjacency structure uses compact integer arrays rather than a list of Python tuples. This matters because the persistent segment tree and the small-capacity prefix arrays are the dominant memory consumers, and the memory limit is only 256 MB.

The initial tree traversal produces `parent`, `depth`, `parent_edge`, and an order in which every parent occurs before its children. That order makes both the persistent versions and the capacity-specific prefix sums easy to construct without recursion through the original tree.

The binary lifting table is used only for LCA queries. The LCA is the correct subtraction point because the root-to-`S` and root-to-`F` paths contain the common root-to-LCA part twice.

For small capacities, `ceil(D/T)` is calculated as `(D + T - 1) // T`. The prefix values fit in signed 32-bit integers because the largest possible path contains fewer than `100000` edges and each contribution is at most `20000`.

The persistent segment tree stores counts rather than sums of edge lengths. Counts are sufficient because the query needs a frequency-weighted sum of `ceil(D/T)`. At a segment where the quotient is constant, only the number of edges matters.

The persistent update is written iteratively because it creates about `O(N log 20000)` nodes. Avoiding a Python function call for every level makes preprocessing substantially cheaper.

The query routine uses the relation `count_path = count_S + count_F - 2 * count_LCA`. A node with zero path count is discarded immediately. If the quotient is equal at both ends of its value range, the entire range has one contribution and recursion can stop there.

The condition `t >= max_edge` is handled before either preprocessing method. Every road can then be traversed without an intermediate charging stop, so the answer is simply the number of edges plus one warehouse stop.

## Worked Examples

### Sample 1

Consider the first query, from warehouse `3` to warehouse `7`, with capacity `T = 2`. Its path is

`3 -> 2 -> 4 -> 7`

with edge lengths `2, 3, 6`.

| Edge | Length | `ceil(D/T)` | Running edge sum |
| --- | --- | --- | --- |
| `3 -> 2` | 2 | 1 | 1 |
| `2 -> 4` | 3 | 2 | 3 |
| `4 -> 7` | 6 | 3 | 6 |
| Initial warehouse |  |  | `6 + 1 = 7` |

The output is `7`.

For the second query, from `2` to `6` with `T = 1`, the path consists of edges of lengths `3` and `5`.

| Edge | Length | `ceil(D/T)` | Running edge sum |
| --- | --- | --- | --- |
| `2 -> 4` | 3 | 3 | 3 |
| `4 -> 6` | 5 | 5 | 8 |
| Initial warehouse |  |  | `8 + 1 = 9` |

The output is `9`.

The remaining queries produce the same calculation.

| Query | Path edge lengths | `T` | Sum of `ceil(D/T)` | Answer |
| --- | --- | --- | --- | --- |
| `3 -> 7` | `2, 3, 6` | 2 | 6 | 7 |
| `2 -> 6` | `3, 5` | 1 | 8 | 9 |
| `5 -> 7` | `4, 6` | 3 | 4 | 5 |
| `1 -> 4` | `1, 3` | 1 | 4 | 5 |
| `3 -> 7` | `2, 3, 6` | 1 | 11 | 12 |

This sample exercises both exact divisibility and roads that require several charging stops.

### Sample 2

The path is a chain with edge lengths `5, 10, 20`.

For `T = 20`, every edge needs one travel segment.

| Edge | Length | `ceil(D/T)` | Running edge sum |
| --- | --- | --- | --- |
| `1 -> 2` | 5 | 1 | 1 |
| `2 -> 3` | 10 | 1 | 2 |
| `3 -> 4` | 20 | 1 | 3 |
| Initial warehouse |  |  | `3 + 1 = 4` |

For `T = 10`, the last edge needs two segments.

| Edge | Length | `ceil(D/T)` | Running edge sum |
| --- | --- | --- | --- |
| `1 -> 2` | 5 | 1 | 1 |
| `2 -> 3` | 10 | 1 | 2 |
| `3 -> 4` | 20 | 2 | 4 |
| Initial warehouse |  |  | `4 + 1 = 5` |

For `T = 5`, the three contributions are `1, 2, 4`, giving `8`.

| `T` | Edge contribution sum | Final answer |
| --- | --- | --- |
| 20 | 3 | 4 |
| 10 | 4 | 5 |
| 5 | 7 | 8 |

This sample demonstrates the exact boundary at `D = T` and `D = 2T`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(NB + NlogD + NlogN + Q(D/B)logD)` | Small capacities use `O(N)` preprocessing each, while large capacities visit only the quotient-change ranges |
| Space | `O(NB + NlogD + NlogN)` | Small-capacity prefixes, persistent segment-tree versions, and binary lifting tables dominate memory |

With `B = 200` and `D <= 20000`, the small-capacity preprocessing stores at most about 20 million 32-bit integers. The persistent segment tree needs roughly `N log D` nodes, and the LCA table needs `N log N` integers. All of these structures are stored with compact integer arrays rather than Python objects.

The key bound for large capacities is that `ceil(D/T)` can take only `O(D/T)` distinct values. Since `T > B`, this is at most about `D/B`, which is at most `100` for the chosen threshold. The persistent tree processes these ranges without scanning the original path.

## Test Cases

The following tests assume the `solve()` function from the solution above is available.

```python
import sys
import io

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input
    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline
        from contextlib import redirect_stdout
        out = io.StringIO()
        with redirect_stdout(out):
            solve()
        return out.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        input = old_input

sample1 = """\
7 5
1 2 1
2 3 2
2 4 3
4 5 4
4 6 5
4 7 6
3 7 2
2 6 1
5 7 3
1 4 1
3 7 1
"""

sample2 = """\
4 3
1 2 5
2 3 10
3 4 20
1 4 20
1 4 10
1 4 5
"""

assert run(sample1) == "7\n9\n5\n5\n12", "sample 1"
assert run(sample2) == "4\n5\n8", "sample 2"

minimum_case = """\
2 1
1 2 1
1 2 1
"""
assert run(minimum_case) == "2", "minimum-size case"

exact_boundary = """\
3 4
1 2 10
2 3 20
1 3 10
1 3 20
1 3 5
1 3 10
"""
assert run(exact_boundary) == "4\n3\n6\n4", "exact divisibility boundaries"

equal_edges = """\
5 4
1 2 10
2 3 10
3 4 10
4 5 10
1 5 10
1 5 5
1 5 20
2 4 10
"""
assert run(equal_edges) == "5\n9\n5\n3", "all equal edge lengths"

large_chain = "100000 100000\n"
large_chain += "".join(f"{i} {i + 1} 1\n" for i in range(1, 100000))
large_chain += "".join(f"1 100000 {t}\n" for t in range(1, 100001))

large_output = run(large_chain).splitlines()
assert len(large_output) == 100000, "maximum-size case"
assert large_output[0] == "100000", "maximum-size T=1"
assert large_output[-1] == "100000", "maximum-size large T"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1`, one edge of length `1`, `T = 1` | `2` | Minimum tree and no charging stop |
| Three-vertex path with lengths `10, 20` | `4`, `3`, `6`, `4` | Exact multiples of the battery capacity |
| Four equal edges of length `10` | `5`, `9`, `5`, `3` | Repeated equal edge values and several capacities |
| Chain with `100000` vertices and `100000` queries | `100000` for every query | Maximum-size tree, large query count, and capacity extremes |

## Edge Cases

The first edge case is an edge whose length is exactly equal to the battery capacity. Consider

```
2 1
1 2 10
1 2 10
```

The path has one edge and `ceil(10/10) = 1`, so the answer is `1 + 1 = 2`. The algorithm enters the `t >= max_edge` case and returns the path's one edge plus one. There is no intermediate charging stop.

The second edge case is an edge that is slightly longer than the capacity. Consider

```
2 1
1 2 11
1 2 10
```

The edge needs `ceil(11/10) = 2` travel segments. One charging stop is required in the middle, so the answer is `3`. The persistent or prefix calculation records the edge contribution as `2`, and the final `+1` gives `3`.

The third edge case is a route containing several mandatory warehouses but no charging. Consider

```
3 1
1 2 5
2 3 5
1 3 10
```

Both edges have `ceil(5/10) = 1`. Their contribution is `2`, and the initial `+1` gives `3`. The middle warehouse is counted because it is the endpoint of the first edge and the starting point of the second edge.

The fourth edge case is a road much longer than the battery. Consider

```
2 1
1 2 20
1 2 5
```

The single edge contributes `ceil(20/5) = 4`, so the answer is `5`. The algorithm never declares the road unreachable. It only counts the three intermediate charging stops implied by the four travel segments.

The fifth edge case is a query whose capacity exceeds every road in the tree. If the largest road has length `20` and `T = 21`, every road contributes exactly one. The persistent tree is unnecessary, and the direct result `number_of_edges_on_path + 1` is exact. This shortcut also avoids wasting time on a query whose answer is independent of the actual edge lengths.
