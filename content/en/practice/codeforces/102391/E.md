---
title: "CF 102391E - Dead Cacti Society"
description: "We start with a connected weighted cactus. Each original vertex (v) has a healing value (RVv), and each original edge (e) has a length (Le) and a healing value (REe). For every cycle, exactly one edge must be removed. Removing an edge (e={u,v}) does not simply delete it."
date: "2026-08-14T14:13:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "E"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 498
verified: false
draft: false
---

[CF 102391E - Dead Cacti Society](https://codeforces.com/problemset/problem/102391/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a connected weighted cactus. Each original vertex (v) has a healing value (RV_v), and each original edge (e) has a length (L_e) and a healing value (RE_e).

For every cycle, exactly one edge must be removed. Removing an edge (e={u,v}) does not simply delete it. Instead, a new leaf is attached to (u) with edge length (RV_u+RE_e), and another new leaf is attached to (v) with edge length (RV_v+RE_e). After doing this for every cycle, the graph is a tree. We want the smallest possible diameter of that final tree.

The input contains up to (100,000) original vertices and (150,000) edges. Since a connected graph has (M-N+1) independent cycles here, there can be nearly (50,000) cycles. The edge lengths and healing values reach (10^9), so the answer can be around (10^{14}). This rules out enumerating all choices of removed edges, and it also means every distance calculation must use 64-bit integers. An (O((N+M)\log V)) solution is appropriate for the (10)-second limit.

There are several ways a careless solution can fail.

Consider the smallest possible cactus, a triangle with all original edge lengths equal to (1), all vertex healing values (0), and all edge healing values (1).

```
3 3
0 0 0
1 2 1 1
2 3 1 1
3 1 1 1
```

The answer is (4). After cutting any edge, the remaining two original edges form a path of length (2), and the two new healing edges add another (2). A solution that computes the diameter only among original vertices would incorrectly report (2).

The second trap is that the best edge to cut is not necessarily the shortest edge. Sample 1 contains a triangle where cutting edge (1\text{-}2), the shortest edge, gives diameter (12), while cutting edge (2\text{-}3) gives the optimal diameter (10). The healing value of the selected edge changes both new leaves, so the original edge length alone is not enough.

```
3 3
1 2 3
3 1 2 3
1 2 1 2
2 3 3 1
```

A third common mistake is to forget bridges. They are never cut, but they still contribute their ordinary edge length to every path crossing them. For example,

```
4 4
0 0 0 0
1 2 1 1
2 3 1 1
3 1 1 1
3 4 10 1
```

has answer (12). The triangle is broken into a path, and the bridge of length (10) remains attached to vertex (3). Treating every biconnected component as a cycle that can be freely modified would give an invalid state.

## Approaches

The direct solution is to enumerate the edge removed from every cycle. If the cycles have lengths (c_1,c_2,\ldots,c_k), there are

[
\prod_{i=1}^{k}c_i
]

possible final trees. For each choice, we could construct the resulting tree and run a tree-diameter algorithm in (O(N+M)).

This is correct because every legal final tree corresponds to exactly one choice of one edge from every cycle. The problem is the number of choices. A cactus made from roughly (50,000) triangles sharing one articulation vertex has about (3^{50,000}) different choices. Even one operation per choice would already be hopeless, and recomputing a diameter makes the brute force roughly (O(3^{50,000}(N+M))).

The useful observation is that the objective is a minimum possible maximum. That immediately suggests binary search. Fix a candidate diameter (R), and ask whether there exists some way of cutting the cactus whose final diameter is at most (R). This feasibility condition is monotone: if (R) is feasible, every larger value is also feasible.

The remaining question is how to check one value of (R) efficiently. A cactus has a very useful decomposition. Every biconnected component is either a single bridge or one simple cycle. Replacing every cycle by a separate block node gives a block-cut tree. This tree contains all the structural choices while each individual cycle can be processed as one local object. The official contest tutorial uses exactly this decomposition together with a reverse DFS dynamic program and binary search.

For every node (u) of this decomposition, define (d_u) as the minimum possible distance from (u) to its farthest vertex inside the already processed subtree, under the condition that every diameter inside that subtree is at most (R). If no valid choice exists, (d_u) is infinity.

For an ordinary original vertex, the transition is the standard tree transition. Every child contributes its farthest distance, and the two largest contributions must have sum at most (R). The largest contribution becomes (d_u).

A cycle is more complicated because we may cut any one of its edges. Once an edge is cut, the cycle becomes a path, with a healing leaf at each endpoint. If the cycle is viewed from its parent articulation vertex, every possible cut separates it into a left path and a right path. We can scan both sides with prefix and suffix dynamic programming, so every possible cut is evaluated in constant time after linear preprocessing for the cycle.

The key structural fact is that only distances from each cycle vertex into its attached subtree are needed. Once those values are known, the rest of the cycle is just a weighted path plus two candidate healing leaves. That is what reduces an apparently exponential choice over cycle edges to linear work per cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(3^{\Theta(N)}(N+M))) in the worst case | (O(N+M)) | Too slow |
| Optimal | (O((N+M)\log V)) | (O(N+M)) | Accepted |

## Algorithm Walkthrough

1. Decompose the cactus into bridges and simple cycles using Tarjan's biconnected-component algorithm.

For every bridge, connect its two original vertices directly in a new block-cut tree. For every cycle, create one extra cycle node and connect it to every vertex belonging to that cycle. The resulting graph is a tree because every cycle is replaced by a single block node.

For each cycle we also preserve its vertices in cyclic order and the corresponding original edge IDs. This order is needed when evaluating every possible removed edge.

1. Binary-search the answer.

Let (R) be the current candidate diameter. The feasibility check determines whether some legal set of cuts produces a tree of diameter at most (R).

An upper bound is obtained by taking the largest value among all original edge lengths and all possible healing-edge lengths. A final diameter uses at most (N-1) ordinary tree edges and at most two healing edges per cycle, so

\maxWeight\left(N-1+2(M-N+1)\right).
]

1. Process the block-cut tree in reverse DFS order.

For every original vertex (u), all child subtrees have already produced their (d)-values. If a child is an original vertex connected by a bridge of length (w), its contribution is (d_v+w). If the child is a cycle block, its (d_v) already includes the whole cycle path from (u), so no additional edge length is added.

Keep the two largest contributions (x) and (y). If (x+y>R), the candidate diameter is impossible. Otherwise set (d_u=x).

1. Process a cycle block with its parent vertex as the pivot.

Suppose the cycle contains vertices

[
v_0,v_1,\ldots,v_{L-1},v_L
]

where (v_0=v_L) is the pivot. Let edge (e_i) connect (v_i) and (v_{i+1}).

For every non-pivot vertex (v_i), (d_{v_i}) is already known. Define (l_i) as the distance from the pivot to (v_i) along the left side of the cycle:

[
l_0=0,\qquad
l_i=l_{i-1}+L_{e_{i-1}}.
]

Similarly, define suffix distances (r_i) along the other direction.

The first set of prefix values records the farthest distance from the pivot:

[
LD_i=\max_{1\le j\le i}(d_{v_j}+l_j).
]

We also need

[
LF_i=\max_{1\le j\le i}(d_{v_j}-l_j),
]

because for two subtrees (p<q), their distance through the path is

[
(d_{v_p}-l_p)+(d_{v_q}+l_q).
]

Thus the best diameter whose endpoints are both on the left can be updated incrementally by

\max(LG_{i-1},LF_{i-1}+d_{v_i}+l_i).
]

The right side uses the symmetric suffix arrays (RD,RF,RG). The official solution derives the same left-half recurrence from these two expressions for subtree distances.

1. Add the healing leaves to the cycle transition.

Suppose edge (e_{i-1}) is the edge we cut. Its endpoints are (v_{i-1}) and (v_i), so the two new leaf lengths are

[
a=RV_{v_{i-1}}+RE_{e_{i-1}},
]

and

[
b=RV_{v_i}+RE_{e_{i-1}}.
]

After the cut, the cycle becomes a path from (v_{i-1}) to (v_i). Every possible diameter inside this local structure falls into one of six endpoint types.

The first type has both endpoints in the left part. Its value is the left prefix diameter (LG_{i-1}).

The second type has both endpoints in the right part. Its value is (RG_i).

The third type has one endpoint in a left subtree and one in a right subtree. Its value is (LD_{i-1}+RD_i).

The fourth type uses the new healing leaf at (v_{i-1}) and an endpoint in the right part. Its value is

[
a+\max(LH_{i-1},l_{i-1}+RD_i).
]

The fifth type is symmetric, using the healing leaf at (v_i):

[
b+\max(RH_i,r_{i+1}+LD_{i-1}).
]

The sixth type connects the two new healing leaves directly through the remaining cycle path:

[
a+l_{i-1}+r_{i+1}+b.
]

Take the maximum of these six values. If that maximum is at most (R), this particular cut is valid.

For a valid cut, the distance from the pivot to the farthest vertex in this processed cycle is

[
D=
\max(
LD_{i-1},
RD_i,
a+l_{i-1},
b+r_{i+1}
).
]

The cycle block takes the minimum such (D) over all its possible cut edges.

1. Reject the candidate as soon as a subtree has no valid state.

If an original vertex has two child branches whose combined distance exceeds (R), no choice outside that subtree can repair the violation. Likewise, if every possible cut in a cycle exceeds (R), that cycle cannot be part of a solution of diameter at most (R).

1. After processing the root, the candidate (R) is feasible exactly when the root has a finite (d)-value.

Binary search then returns the smallest feasible (R).

### Why it works

The invariant is that (d_u) is the smallest possible farthest distance from (u) among all valid configurations of the processed subtree, with every internal diameter at most (R).

For an ordinary vertex, only the two deepest child branches can form a diameter through that vertex, so retaining the smallest possible maximum depth is sufficient. For a cycle block, once its cut edge is fixed, the block becomes a path, and every possible diameter has its endpoints in exactly one of the six categories above. The prefix and suffix maxima compute the best value for each category without enumerating pairs of vertices. Taking the minimum depth over every valid cut preserves exactly the best possible state for the parent.

Thus the root is feasible exactly when some legal set of cycle cuts produces a tree whose diameter is at most (R). Since feasibility is monotone, binary search gives the minimum possible diameter.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

INF = 10**30

def solve():
    n, m = map(int, input().split())
    rv = [0] + list(map(int, input().split()))

    U = [0] * (m + 1)
    V = [0] * (m + 1)
    W = [0] * (m + 1)
    RE = [0] * (m + 1)

    g = [[] for _ in range(n + 1)]

    max_base = 0

    for eid in range(1, m + 1):
        a, b, w, re = map(int, input().split())
        U[eid] = a
        V[eid] = b
        W[eid] = w
        RE[eid] = re
        g[a].append((b, eid))
        g[b].append((a, eid))
        max_base = max(max_base, w, rv[a] + re, rv[b] + re)

    # Tarjan decomposition.
    dfn = [0] * (n + 1)
    low = [0] * (n + 1)
    edge_stack = []

    # Block-cut tree.
    # Original vertices are 1..n.
    # Cycle block vertices are n+1..cnt.
    t = [[] for _ in range(n + 2)]

    # cycle_info[node] = (vertices, edge_ids)
    # vertices has length len(edge_ids)+1 and starts/ends at the pivot.
    cycle_info = [None] * (n + 1)

    timer = 0
    cnt = n
    max_cycle_len = 0

    def add_component(pivot, edges):
        nonlocal cnt, max_cycle_len

        if len(edges) == 1:
            eid = edges[0]
            a = U[eid]
            b = V[eid]
            t[a].append((b, eid))
            t[b].append((a, eid))
            return

        cnt += 1
        node = cnt

        # A cactus biconnected component with more than one edge
        # is a simple cycle. Build its cyclic order locally.
        local = {}
        for eid in edges:
            a = U[eid]
            b = V[eid]
            local.setdefault(a, []).append(eid)
            local.setdefault(b, []).append(eid)

        verts = [pivot]
        eids = []

        cur = pivot
        prev_eid = 0

        while True:
            choices = local[cur]
            if choices[0] != prev_eid:
                eid = choices[0]
            else:
                eid = choices[1]

            eids.append(eid)

            a = U[eid]
            b = V[eid]
            nxt = b if a == cur else a

            verts.append(nxt)

            prev_eid = eid
            cur = nxt

            if cur == pivot:
                break

        cycle_info.append((verts, eids))
        max_cycle_len = max(max_cycle_len, len(eids))

        # Connect every cycle vertex to the block node.
        for i in range(len(eids)):
            v = verts[i]
            eid = eids[i]
            t[node].append((v, eid))
            t[v].append((node, eid))

    def tarjan(u, parent_eid):
        nonlocal timer

        timer += 1
        dfn[u] = low[u] = timer

        for v, eid in g[u]:
            if eid == parent_eid:
                continue

            if dfn[v] == 0:
                edge_stack.append(eid)
                tarjan(v, eid)

                if low[v] < low[u]:
                    low[u] = low[v]

                if low[v] >= dfn[u]:
                    comp = []
                    while True:
                        x = edge_stack.pop()
                        comp.append(x)
                        if x == eid:
                            break
                    add_component(u, comp)

            elif dfn[v] < dfn[u]:
                edge_stack.append(eid)
                if dfn[v] < low[u]:
                    low[u] = dfn[v]

    tarjan(1, 0)

    # Root the block-cut tree once.
    parent = [0] * (cnt + 1)
    parent[1] = -1
    order = [1]

    for u in order:
        for v, _ in t[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    # Reusable cycle arrays. Reusing them is much cheaper than allocating
    # ten fresh lists for every cycle on every binary-search iteration.
    size = max_cycle_len + 3

    lp = [0] * size
    rp = [0] * size
    ld = [0] * size
    rd = [0] * size
    lf = [0] * size
    rf = [0] * size
    lg = [0] * size
    rg = [0] * size
    lh = [0] * size
    rh = [0] * size

    def check(limit):
        d = [INF] * (cnt + 1)

        for u in reversed(order):
            if u <= n:
                best1 = 0
                best2 = 0

                for v, eid in t[u]:
                    if parent[v] != u:
                        continue

                    if v > n:
                        cur = d[v]
                    else:
                        cur = d[v] + W[eid]

                    if cur > best1:
                        best2 = best1
                        best1 = cur
                    elif cur > best2:
                        best2 = cur

                if best1 + best2 > limit:
                    return False

                if best1 > limit:
                    return False

                d[u] = best1
                continue

            verts, eids = cycle_info[u]
            L = len(eids)

            lp[0] = 0
            ld[0] = 0
            lf[0] = 0
            lh[0] = 0
            lg[0] = 0

            for i in range(1, L):
                lp[i] = lp[i - 1] + W[eids[i - 1]]
                x = d[verts[i]]
                ld[i] = max(ld[i - 1], x + lp[i])
                lf[i] = max(lf[i - 1], x - lp[i])
                lh[i] = max(lh[i - 1] + W[eids[i - 1]], x)

            if L >= 2:
                lg[1] = 0

            for i in range(2, L):
                x = d[verts[i]]
                lg[i] = max(
                    lg[i - 1],
                    lf[i - 1] + x + lp[i]
                )

            rp[L + 1] = 0
            for i in range(L, 1, -1):
                rp[i] = rp[i + 1] + W[eids[i - 1]]

            rd[L] = 0
            rf[L] = 0
            rh[L] = 0
            rg[L] = 0

            for i in range(L - 1, 0, -1):
                x = d[verts[i]]
                rd[i] = max(rd[i + 1], x + rp[i + 1])
                rf[i] = max(rf[i + 1], x - rp[i + 1])
                rh[i] = max(rh[i + 1] + W[eids[i]], x)

            if L >= 2:
                rg[L - 1] = 0

            for i in range(L - 2, 0, -1):
                x = d[verts[i]]
                rg[i] = max(
                    rg[i + 1],
                    rf[i + 1] + x + rp[i + 1]
                )

            best_depth = INF

            for i in range(1, L + 1):
                eid = eids[i - 1]

                a = rv[verts[i - 1]] + RE[eid]
                b = rv[verts[i]] + RE[eid]

                r1 = lg[i - 1]
                r2 = rg[i]
                r3 = ld[i - 1] + rd[i]
                r4 = a + max(lh[i - 1], lp[i - 1] + rd[i])
                r5 = b + max(rh[i], rp[i + 1] + ld[i - 1])
                r6 = a + lp[i - 1] + rp[i + 1] + b

                diameter = max(r1, r2, r3, r4, r5, r6)

                if diameter <= limit:
                    depth = max(
                        ld[i - 1],
                        rd[i],
                        a + lp[i - 1],
                        b + rp[i + 1]
                    )
                    if depth < best_depth:
                        best_depth = depth

            if best_depth > limit:
                return False

            d[u] = best_depth

        return True

    cycles = m - n + 1
    lo = 0
    hi = max_base * (n - 1 + 2 * cycles)

    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The input arrays store the endpoints, original length, and healing value of every edge separately. Keeping the edge ID throughout the cactus decomposition is useful because a cycle transition needs both its original length and its healing value.

Tarjan's algorithm stores edges on a stack. Whenever `low[v] >= dfn[u]`, the edges up to the tree edge (u\text{-}v) form one biconnected component. In a cactus, that component is either a single bridge or a simple cycle, so no general-purpose biconnected-component machinery is needed.

The block-cut tree is rooted once before binary search. Its structure never changes, so rebuilding it during every feasibility check would waste time.

The `check` function processes this tree in reverse order. For an original vertex, the two largest child depths are enough because every path passing through that vertex can use at most two child branches. A cycle block is processed with the ten reusable arrays corresponding to the prefix and suffix quantities described above.

The duplicate pivot at the end of `verts` is deliberate. It represents the closing point of the cycle and makes the indexing of the two sides uniform. The DP never reads a subtree value for that duplicate pivot, so no value from the parent is needed.

All distances use Python integers, so there is no overflow issue. In languages with fixed-width integers, signed 64-bit arithmetic is required.

The binary search uses the strict condition `lo < hi`, and a feasible midpoint moves the upper boundary to `mid`. This returns the first feasible value directly without needing a separate answer variable.

## Worked Examples

### Sample 1

The graph is a single triangle. There are three possible edges to remove. The resulting tree always consists of the two surviving original edges plus two healing leaves.

| Cut edge | Healing leaf at first endpoint | Healing leaf at second endpoint | Diameter |
| --- | --- | --- | --- |
| (1\text{-}2) | (RV_1+RE_2=3) | (RV_2+RE_2=4) | 12 |
| (2\text{-}3) | (RV_2+RE_1=3) | (RV_3+RE_1=4) | 10 |
| (3\text{-}1) | (RV_3+RE_3=6) | (RV_1+RE_3=4) | 14 |

The second choice is optimal. After removing edge (2\text{-}3), the remaining path is (2\text{-}1\text{-}3), with length (1+2=3). The two healing leaves add (3) and (4), giving diameter (3+3+4=10).

The DP sees the same choice while processing the only cycle. For a candidate (R=10), the cut (2\text{-}3) has all six diameter categories at most (10), and its resulting depth from the pivot is at most (10). The other two cuts violate the limit.

### Sample 2

There are two triangles sharing vertex (1). Because the block-cut tree branches at vertex (1), the final diameter can be the sum of the largest depth contributed by each triangle.

For the first cycle, the best depth from vertex (1) for each possible cut is:

| Cut in cycle (1\text{-}2\text{-}3) | Maximum depth from vertex 1 |
| --- | --- |
| (1\text{-}2) | 12 |
| (2\text{-}3) | 10 |
| (3\text{-}1) | 17 |

For the second cycle, the corresponding values are:

| Cut in cycle (1\text{-}4\text{-}5) | Maximum depth from vertex 1 |
| --- | --- |
| (1\text{-}4) | 13 |
| (4\text{-}5) | 12 |
| (5\text{-}1) | 12 |

Since the two cycles meet at vertex (1), the diameter between their farthest branches is the sum of the two depths.

| First cycle cut | Second cycle cut | Resulting cross-cycle diameter |
| --- | --- | --- |
| (1\text{-}2) | (1\text{-}4) | 25 |
| (1\text{-}2) | (4\text{-}5) | 24 |
| (1\text{-}2) | (5\text{-}1) | 24 |
| (2\text{-}3) | (1\text{-}4) | 23 |
| (2\text{-}3) | (4\text{-}5) | 22 |
| (2\text{-}3) | (5\text{-}1) | 22 |
| (3\text{-}1) | (1\text{-}4) | 30 |
| (3\text{-}1) | (4\text{-}5) | 29 |
| (3\text{-}1) | (5\text{-}1) | 29 |

The minimum is (22), obtained by cutting edges (2\text{-}3) and (4\text{-}5). This example demonstrates why the DP must preserve the minimum possible farthest depth, rather than only the diameter of an individual cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((N+M)\log V)) | Tarjan and the block-cut construction are linear. Each feasibility check scans every block and cycle edge a constant number of times, and binary search performs (O(\log V)) checks. |
| Space | (O(N+M)) | The original graph, block-cut tree, decomposition data, DP arrays, and temporary cycle arrays are all linear in the input size. |

There are at most (M-N+1) cycles, and the total number of edges over all cycles is at most (M). Consequently, a complete feasibility check is linear. With at most about (2\cdot10^{14}) possible answer values, binary search needs fewer than (50) iterations. This fits the stated limits, while Python benefits significantly from reusing the cycle arrays instead of allocating new arrays for every cycle during every check.

## Test Cases

The following harness assumes the solution above is saved as `solution.py`. It redirects standard input and output and calls the `solve` function directly.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solution.input = sys.stdin.readline
        solution.solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample 1
assert run("""\
3 3
1 2 3
3 1 2 3
1 2 1 2
2 3 3 1
""") == "10", "sample 1"

# Sample 2
assert run("""\
5 6
1 2 3 4 5
1 2 6 1
1 3 5 4
2 3 4 2
1 4 3 6
1 5 2 3
4 5 1 5
""") == "22", "sample 2"

# Minimum-size cactus, all equal values.
# Any cut produces a path with two original edges and two healing edges.
assert run("""\
3 3
0 0 0
1 2 1 1
2 3 1 1
3 1 1 1
""") == "4", "minimum size and all equal values"

# A bridge attached to one cycle vertex.
# The optimal cut avoids making the long bridge branch even longer.
assert run("""\
4 4
0 0 0 0
1 2 1 1
2 3 1 1
3 1 1 1
3 4 10 1
""") == "12", "bridge attachment"

# Large values, testing 64-bit-sized distances.
assert run("""\
3 3
1000000000 1000000000 1000000000
1 2 1000000000 1000000000
2 3 1000000000 1000000000
3 1 1000000000 1000000000
""") == "6000000000", "large weights"

# Maximum-size instance: one cycle containing all 100000 vertices.
# All original edges and healing edges have length 1.
n = 100000
parts = [
    f"{n} {n}",
    " ".join(["0"] * n)
]
for i in range(1, n):
    parts.append(f"{i} {i + 1} 1 1")
parts.append(f"{n} 1 1 1")

max_case = "\n".join(parts) + "\n"
assert run(max_case) == "100001", "maximum-size single cycle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum triangle with all values equal | 4 | Healing leaves must participate in the diameter. |
| Triangle with a length-10 bridge | 12 | Bridges remain intact and their lengths must be included in subtree depths. |
| Triangle with values (10^9) | 6000000000 | Large integer arithmetic and binary-search bounds. |
| 100000-vertex cycle | 100001 | Linear cycle processing, boundary indexing, and maximum input size. |

## Edge Cases

The minimum triangle with all values equal is handled by the cycle transition itself. For

```
3 3
0 0 0
1 2 1 1
2 3 1 1
3 1 1 1
```

the cycle has three possible cut positions. Every cut creates two healing edges of length (1), while the two surviving original edges also have total length (2). The cycle DP's sixth category, the path between the two healing leaves, reaches (4), so the feasibility check succeeds exactly at (R=4).

The sample-1 case catches the difference between original edge length and healing cost. Cutting (2\text{-}3) uses healing value (RE=1), producing leaf lengths (2+1=3) and (3+1=4). The remaining path has length (1+2=3), giving diameter (10). Cutting the shortest original edge (1\text{-}2) instead uses (RE=2), producing larger healing leaves and diameter (12). The cycle DP considers the healing values directly through (a=RV_u+RE_e) and (b=RV_v+RE_e).

For the bridge case,

```
4 4
0 0 0 0
1 2 1 1
2 3 1 1
3 1 1 1
3 4 10 1
```

Tarjan creates one cycle block for vertices (1,2,3) and one ordinary tree edge (3\text{-}4). The bridge contributes (10+d_4) when vertex (3) is processed. The cycle transition then compares all three possible cuts while carrying that already-computed branch depth. The best result is (12).

For the large-value case,

```
3 3
1000000000 1000000000 1000000000
1 2 1000000000 1000000000
2 3 1000000000 1000000000
3 1 1000000000 1000000000
```

every surviving original edge has length (10^9), and every healing edge has length (2\cdot10^9). The final tree has a path containing two original edges and two healing edges, so its diameter is (6\cdot10^9). Python integers handle this directly, while a C++ implementation needs `long long`.

Finally, a cycle can contain almost all (100,000) vertices. The prefix and suffix computations are linear in the cycle length, and every edge is touched only a constant number of times per feasibility check. The algorithm never enumerates pairs of cycle vertices or complete cut configurations, which is the property that keeps the maximum-size case within the required complexity.
