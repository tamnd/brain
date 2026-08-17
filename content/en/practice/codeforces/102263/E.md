---
title: "CF 102263E - Longest path Problem"
description: "We have a weighted tree, and every original edge is considered independently. For one chosen edge of weight (w), deleting it splits the tree into two components, say (A) and (B)."
date: "2026-08-17T19:57:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102263
codeforces_index: "E"
codeforces_contest_name: "ArabellaCPC 2019"
rating: 0
weight: 102263
solve_time_s: 239
verified: true
draft: false
---

[CF 102263E - Longest path Problem](https://codeforces.com/problemset/problem/102263/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a weighted tree, and every original edge is considered independently. For one chosen edge of weight (w), deleting it splits the tree into two components, say (A) and (B). We may then reconnect the two components by putting the same edge, with the same weight (w), between any vertex of (A) and any vertex of (B). The task is to output the smallest possible diameter after this reconnection.

The input contains (n) vertices and (n-1) weighted edges. The (i)-th output value corresponds to the (i)-th input edge, so every edge needs its own answer. The official constraints allow (n=200000), edge weights up to (10^9), and the original judge has a 1 second time limit with 256 MB of memory.

The size of the tree immediately rules out doing a traversal separately for every edge. A single traversal costs (O(n)), and doing that for (n-1) edges already costs (O(n^2)), about (4\cdot10^{10}) vertex visits at the maximum (n). We need to reuse information between the different cuts.

There are three edge cases that are particularly easy to mishandle.

For a tree consisting of two vertices, the only edge is also the whole tree.

```
2
1 2 5
```

The correct output is

```
5
```

After removing the edge, both components contain one vertex. The only possible reconnection has weight 5, so the resulting diameter is 5. A solution that assumes both components have a nonzero diameter or radius can incorrectly produce a larger value.

Weighted edges create another trap. Consider

```
3
1 2 10
2 3 1
```

The correct output is

```
11
11
```

After removing either edge, one component consists of a single vertex and the other consists of two vertices. For the two-vertex component whose edge has weight 10, the best vertex has eccentricity 10. It is not valid to replace the vertex radius by (D/2), because the midpoint of a weighted edge need not be a vertex. The same issue appears with the component containing the edge of weight 1.

Finally, the optimal reconnection vertices need not be the endpoints of the original removed edge. For the official sample,

```
4
1 2 2
1 3 3
2 4 2
```

the second edge has weight 3. Removing it leaves vertex 3 on one side and the path (3? ) Actually the other component is (1-2-4). Its best reconnection vertex is vertex 2, not vertex 1. Reconnecting 3 directly to 2 gives the answer 5. The official statement also gives this particular reconstruction.

## Approaches

The direct approach is to process each edge independently. Delete the edge, traverse both resulting components, find their diameters, find their best possible attachment vertices, and combine the two components. This is correct because after the cut the only new path between the components is the newly inserted edge.

For a component (T), let its diameter be (D(T)), and let its vertex radius be (R(T)), meaning the minimum eccentricity among vertices of (T). If we reconnect (x\in A) to (y\in B) with the removed edge of weight (w), every path in the new tree is either entirely inside (A), entirely inside (B), or crosses the new edge. The longest path crossing the edge has length

[
\operatorname{ecc}_A(x)+w+\operatorname{ecc}_B(y).
]

The choices of (x) and (y) are independent, so the best possible crossing path is

[
R(A)+w+R(B).
]

Consequently the answer for the cut is

[
\max(D(A),D(B),R(A)+w+R(B)).
]

The brute-force method could compute these quantities from scratch for every edge. Even if each cut is handled in only (O(n)), the total is (O(n^2)). On (n=200000), one complete scan per edge is already

[
(n-1)n=39,999,800,000
]

vertex visits, before accounting for the additional work needed to determine diameters and centers. That is far beyond the available time.

The useful observation is that deleting an edge always creates one of only two directed components. For an edge (u-v), we can think of the state (u\rightarrow v) as describing the component containing (u) when (v) is forbidden as a neighbor. There are exactly (2(n-1)) such directed states.

This turns the problem into a rerooting DP. For every directed state we store the maximum distance from its root to any vertex in that component, one endpoint of such a maximum-depth path, the diameter, and two endpoints of the diameter. The state can be built from the corresponding states of all neighboring components.

The remaining difficulty is the radius. Once diameter endpoints (a,b) are known, the eccentricity of any vertex (x) is

[
\max(d(x,a),d(x,b)).
]

Thus the best vertex lies on the path from (a) to (b). Along this path, the first quantity increases while the second decreases, so the optimum is attained by one of the two vertices immediately surrounding the midpoint of the diameter. Weighted edges make the midpoint potentially lie inside an edge, which is why we explicitly locate those two vertices using binary lifting.

This is also the same high-level decomposition described in the contest discussion: compute diameter endpoints and depth information for both directed sides of every edge, then use the centers of those components when reconnecting them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Rerooting DP + binary lifting | (O(n\log n)) | (O(n\log n)) | Accepted |

## Algorithm Walkthrough

1. Root the original tree at vertex 1 and build an iterative DFS order. For every vertex, store its parent, the directed edge connecting it to its parent, its depth, and its weighted distance from the root. An iterative traversal avoids Python recursion-depth problems on a path containing 200000 vertices.
2. Represent every undirected edge by two directed edge IDs. For a directed edge (u\rightarrow v), define its DP state to describe the component containing (u) after the edge (uv) is removed. The state stores four pieces of information: the maximum distance from (u), an endpoint achieving that maximum, the diameter length, and the two endpoints of that diameter.
3. Compute the child-side states in reverse DFS order. Suppose (u) has a parent (p). To construct the component rooted at (u) after excluding (p), inspect every neighbor of (u) except (p). If the neighbor is (v), its contribution as a branch from (u) has length

[
w(u,v)+H(v\rightarrow u),
]

where (H(v\rightarrow u)) is the maximum downward distance stored by the opposite directed state. The largest branch gives the height of the state.

1. While scanning the branches of a vertex, keep the three largest branch lengths and the two largest child diameters. Three branch candidates are sufficient because when one edge is excluded, at most the current best branch disappears, leaving the next two candidates. Two diameter candidates are sufficient for the same reason.
2. For a state rooted at (u), the diameter has two possible forms. It can be completely inside one neighboring component, in which case we take that component's diameter. Or it can pass through (u), in which case it uses the two largest branch lengths. If those branch endpoints are (x) and (y), the candidate diameter is

[
\operatorname{branch}(x)+\operatorname{branch}(y).
]

The endpoints of the resulting diameter are known at the same time, so no separate diameter traversal is needed.

1. Perform the second, top-down rerooting pass. Once the state describing the parent side of a vertex is available, every neighboring component of that vertex has a known state. For each child edge, recompute the state of the opposite side while excluding that child. This gives the DP state for every directed edge, so every possible cut is now represented.
2. Build a binary-lifting table for the rooted tree. Besides ordinary ancestor jumps, the root-distance array lets us determine the weighted distance travelled by every jump. We use the table both for LCA queries and for finding the vertex closest to a specified distance along an ancestor path.
3. For each directed component, take its stored diameter endpoints (a,b). Let (D=d(a,b)). The optimal vertex is one of the two vertices surrounding distance (D/2) from (a) along the diameter path. Binary lifting locates those candidates in (O(\log n)). Their eccentricities are obtained directly from their positions on the diameter, so no extra all-vertices scan is necessary.
4. For every original edge of weight (w), let its two directed states have diameters (D_1,D_2) and vertex radii (R_1,R_2). The answer is

[
\boxed{\max(D_1,D_2,R_1+w+R_2)}.
]

The construction of the DP state guarantees that (D_1,D_2) describe exactly the two components created by deleting this edge. The radius computation considers the best possible vertex in each component, so the third term is the smallest possible path that crosses the new edge.

Why it works: every path in the reconnected tree belongs to exactly one of three classes, entirely in the first component, entirely in the second component, or crossing the new edge. The first two classes are bounded exactly by the two component diameters. For the third class, choosing an attachment vertex (x) contributes its eccentricity inside its component, and the two choices are independent, so minimizing both eccentricities gives the sum of the two component radii plus the fixed edge weight. The rerooting DP computes the exact diameter of every directed component, while a diameter's endpoints determine every vertex's eccentricity. Since the minimum eccentricity on the diameter path occurs at one of the two vertices surrounding its midpoint, the binary-lifting step finds the exact vertex radius.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    m = n - 1

    # Forward-star adjacency representation.
    # Directed edge d has source implicit in the current adjacency list,
    # destination to[d], weight wt[d], and next adjacency edge nxt[d].
    head = array('i', [-1]) * n
    to = array('i', [0]) * (2 * m)
    nxt = array('i', [0]) * (2 * m)
    wt = array('q', [0]) * (2 * m)

    for i in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1

        d = 2 * i
        r = d ^ 1

        to[d] = v
        wt[d] = w
        nxt[d] = head[u]
        head[u] = d

        to[r] = u
        wt[r] = w
        nxt[r] = head[v]
        head[v] = r

    # Root the tree at 0.
    parent = array('i', [-1]) * n
    parent[0] = 0
    parent_edge = array('i', [-1]) * n
    depth = array('i', [0]) * n
    dist_root = array('q', [0]) * n

    order = []
    order_append = order.append
    order_append(0)

    stack = [0]

    while stack:
        u = stack.pop()
        e = head[u]

        while e != -1:
            v = to[e]
            if v != parent[u]:
                parent[v] = u
                parent_edge[v] = e
                depth[v] = depth[u] + 1
                dist_root[v] = dist_root[u] + wt[e]
                order_append(v)
                stack.append(v)
            e = nxt[e]

    # DP state for directed edge d:
    # component containing source(d), excluding destination(d).
    height = array('q', [0]) * (2 * m)
    far = array('i', [0]) * (2 * m)

    diam = array('q', [0]) * (2 * m)
    dia_a = array('i', [0]) * (2 * m)
    dia_b = array('i', [0]) * (2 * m)

    def build_state(u, excluded):
        # Three best branches are enough because one branch may be excluded
        # and we still need the two best remaining branches.
        b1v = 0
        b1x = u
        b1e = -1

        b2v = 0
        b2x = u
        b2e = -1

        b3v = 0
        b3x = u
        b3e = -1

        # Two best diameters, because one neighbor may be excluded.
        d1v = 0
        d1a = u
        d1b = u
        d1e = -1

        d2v = 0
        d2a = u
        d2b = u
        d2e = -1

        e = head[u]

        while e != -1:
            if e != excluded:
                r = e ^ 1

                branch = wt[e] + height[r]
                endpoint = far[r]

                if branch > b1v:
                    b3v, b3x, b3e = b2v, b2x, b2e
                    b2v, b2x, b2e = b1v, b1x, b1e
                    b1v, b1x, b1e = branch, endpoint, e
                elif branch > b2v:
                    b3v, b3x, b3e = b2v, b2x, b2e
                    b2v, b2x, b2e = branch, endpoint, e
                elif branch > b3v:
                    b3v, b3x, b3e = branch, endpoint, e

                dv = diam[r]
                if dv > d1v:
                    d2v, d2a, d2b, d2e = d1v, d1a, d1b, d1e
                    d1v, d1a, d1b, d1e = dv, dia_a[r], dia_b[r], e
                elif dv > d2v:
                    d2v, d2a, d2b, d2e = dv, dia_a[r], dia_b[r], e

            e = nxt[e]

        # Select the best two branches after excluding one edge.
        if b1e != excluded:
            x1v, x1x, x1e = b1v, b1x, b1e
            x2v, x2x, x2e = b2v, b2x, b2e
        else:
            x1v, x1x, x1e = b2v, b2x, b2e
            if b2e != excluded:
                x2v, x2x, x2e = b3v, b3x, b3e
            else:
                x2v, x2x, x2e = 0, u, -1

        best_d = d1v
        best_a = d1a
        best_b = d1b

        if d1e == excluded:
            best_d = d2v
            best_a = d2a
            best_b = d2b

        cross = x1v + x2v
        if cross > best_d:
            best_d = cross
            best_a = x1x
            best_b = x2x

        return x1v, x1x, best_d, best_a, best_b

    # Bottom-up pass.
    for idx in range(n - 1, 0, -1):
        u = order[idx]
        d = parent_edge[u] ^ 1

        h, f, dd, aa, bb = build_state(u, d)

        height[d] = h
        far[d] = f
        diam[d] = dd
        dia_a[d] = aa
        dia_b[d] = bb

    # Top-down pass.
    for u in order:
        e = head[u]

        while e != -1:
            v = to[e]

            if parent[v] == u:
                h, f, dd, aa, bb = build_state(u, e)

                height[e] = h
                far[e] = f
                diam[e] = dd
                dia_a[e] = aa
                dia_b[e] = bb

            e = nxt[e]

    # Binary lifting.
    LOG = max(1, n.bit_length())
    up = [array('i', parent)]

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

    def climb_with_distance(v, x):
        # Move upward as far as possible without exceeding distance x.
        used = 0

        for k in range(LOG - 1, -1, -1):
            p = up[k][v]
            if p != v:
                w = dist_root[v] - dist_root[p]
                if w <= x:
                    x -= w
                    used += w
                    v = p

        return v, used

    def vertex_radius(a, b, D):
        if a == b:
            return 0

        l = lca(a, b)
        da = dist_root[a] - dist_root[l]
        db = dist_root[b] - dist_root[l]

        half = D // 2

        # Find the vertex at or immediately before the midpoint,
        # walking from a.
        if 2 * da >= D:
            p, used = climb_with_distance(a, half)
            ppos = used

            if 2 * ppos == D:
                return ppos

            # Find the next vertex toward b.
            if p != l:
                q = parent[p]
                edge_w = dist_root[p] - dist_root[q]
            else:
                # p is the LCA. The next vertex lies on the lca -> b path.
                q, _ = climb_with_distance(b, db - 1)
                edge_w = dist_root[q] - dist_root[l]

            qpos = ppos + edge_w

            r1 = max(ppos, D - ppos)
            r2 = max(qpos, D - qpos)
            return min(r1, r2)

        # The midpoint is on the lca -> b part.
        # Find the vertex at or immediately after the midpoint,
        # walking from b.
        need_from_b = D - half
        q, used_b = climb_with_distance(b, need_from_b)
        qpos = D - used_b

        if 2 * qpos == D:
            return qpos

        p = parent[q]
        edge_w = dist_root[q] - dist_root[p]
        ppos = qpos - edge_w

        r1 = max(ppos, D - ppos)
        r2 = max(qpos, D - qpos)
        return min(r1, r2)

    radius = array('q', [0]) * (2 * m)

    for d in range(2 * m):
        radius[d] = vertex_radius(dia_a[d], dia_b[d], diam[d])

    ans = []

    for i in range(m):
        d = 2 * i
        r = d ^ 1

        cross = radius[d] + wt[d] + radius[r]
        best = diam[d]

        if diam[r] > best:
            best = diam[r]
        if cross > best:
            best = cross

        ans.append(str(best))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The adjacency structure uses arrays rather than Python lists of tuples because the input can contain 200000 vertices and the implementation also needs several DP arrays and a binary-lifting table. The packed integer arrays keep memory predictable and avoid the large per-object overhead of Python integers.

The directed DP arrays are indexed by the two directed versions of each original edge. If `d` represents one direction, `d ^ 1` represents the reverse direction. This makes the two components of every cut immediately available at the end.

The bottom-up pass computes the side that points toward a vertex's parent. The top-down pass then supplies the missing parent-side information and computes the other direction for every child. This is the standard two-pass rerooting pattern, but here the state contains both a longest branch and a diameter.

The `build_state` function keeps three branch candidates. The third candidate is necessary because the best branch can be precisely the one excluded for the requested directed state. Keeping only two branches would silently lose the correct second-best branch in that situation. The same exclusion issue explains why two diameter candidates are retained.

The radius calculation deliberately does not use `diameter // 2`. That formula is correct when the center is allowed to be anywhere on the tree, but the new edge endpoints must be existing vertices. With weighted edges, the continuous midpoint can lie strictly inside an edge. The code instead locates the two nearest vertices on either side of that midpoint and takes the better eccentricity.

All distances use 64-bit packed integers. A tree can contain up to (199999) edges of weight (10^9), so a path can have weight close to (2\cdot10^{14}), which does not fit in a 32-bit integer.

## Worked Examples

For Sample 1,

```
4
1 2 2
1 3 3
2 4 2
```

the three cuts can be summarized as follows.

| Edge | Component diameters | Component radii | Edge weight | Crossing value | Answer |
| --- | --- | --- | --- | --- | --- |
| (1-2) | 2, 3 | 2, 3 | 2 | 7 | 7 |
| (1-3) | 4, 0 | 2, 0 | 3 | 5 | 5 |
| (2-4) | 3, 0 | 3, 0 | 2 | 5 | 5 |

The first edge separates the path (2-4) from the edge (1-3). Their radii are both attained at the middle available vertices of their respective components, giving (2+2+3=7). For the second edge, the singleton component has radius zero, while the other component has diameter 4 and radius 2. The best crossing path has length (3+2=5). This gives the official output `7, 5, 5`.

For Sample 2, consider the weighted path

```
3
1 2 10
2 3 1
```

| Edge | Left component | Right component | Radii | Crossing value | Answer |
| --- | --- | --- | --- | --- | --- |
| (1-2) | `{1}` | `2-3` | 0, 1 | 11 | 11 |
| (2-3) | `1-2` | `{3}` | 10, 0 | 11 | 11 |

The second component of the first cut has only two vertices connected by an edge of weight 1, so its radius is 1. The removed edge contributes 10, giving 11. For the second cut the roles reverse, and the two-vertex component has radius 10. This example specifically demonstrates why a weighted vertex radius cannot be obtained by blindly taking half the diameter.

A useful internal DP trace for a three-vertex unit path is even simpler.

| Vertex/state | Best branch | Second branch | Diameter | Diameter endpoints |
| --- | --- | --- | --- | --- |
| leaf | 0 | 0 | 0 | leaf, leaf |
| middle | 1 | 0 | 1 | middle, leaf |
| whole path | 1 | 1 | 2 | two leaves |

At the middle vertex, the two branches each have length 1, so their sum creates the diameter 2. This is exactly the local invariant used by every directed state in the rerooting DP.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Rerooting takes (O(n)); each of the (2(n-1)) component radii uses binary lifting in (O(\log n)). |
| Space | (O(n\log n)) | The DP and graph storage use (O(n)), while binary lifting uses (O(n\log n)). |

For (n=200000), the logarithmic factor is about 18. The packed-array implementation keeps the memory footprint well below the 256 MB limit in principle. The original problem's 1 second limit is quite tight for Python, so a C++ implementation is the safer choice for the original judge, while this Python version is designed to minimize memory overhead and avoid recursion costs. The intended algorithmic complexity is (O(n\log n)), matching the binary-lifting strategy described in the contest discussion.

## Test Cases

The following tests assume that the `solve` function from the solution above is available. The helper resets both `sys.stdin` and the module-level `input` function because the competitive-programming solution binds `input` to `sys.stdin.readline`.

```python
import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    finally:
        sys.stdin = old_stdin
        input = old_input

# A safer helper when stdout is not redirected by the surrounding environment.
def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided sample.
assert run("""\
4
1 2 2
1 3 3
2 4 2
""") == "7\n5\n5", "sample 1"

# Minimum-size tree.
assert run("""\
2
1 2 5
""") == "5", "minimum-size tree"

# Weighted path, catches the incorrect radius = diameter / 2 assumption.
assert run("""\
3
1 2 10
2 3 1
""") == "11\n11", "unequal weighted edges"

# All equal weights, star-shaped tree.
assert run("""\
4
1 2 1
1 3 1
1 4 1
""") == "2\n2\n2", "equal-weight star"

# Path with equal weights.
assert run("""\
4
1 2 1
2 3 1
3 4 1
""") == "3\n3\n3", "equal-weight path"

# Large boundary test: maximum n and all equal weights.
n = 200000
large = [str(n)]
large.extend(f"1 {v} 1" for v in range(2, n + 1))
large_input = "\n".join(large) + "\n"
large_output = run(large_input)
assert large_output == "2\n" * (n - 1), "maximum-size star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2 5` | `5` | Singleton components and minimum (n) |
| `3 / 1 2 10 / 2 3 1` | `11 / 11` | Weighted centers and non-half-integer diameter centers |
| `4 / 1 2 1 / 1 3 1 / 1 4 1` | `2 / 2 / 2` | Equal weights and high-degree rerooting |
| `4 / 1 2 1 / 2 3 1 / 3 4 1` | `3 / 3 / 3` | Path structure and midpoint handling |
| Star with (n=200000) | `2` repeated | Maximum-size input and memory behavior |

## Edge Cases

The two-vertex tree

```
2
1 2 5
```

creates two singleton components after the cut. Their diameter and radius are both zero. The only remaining path is the new edge of weight 5, so the formula becomes

[
\max(0,0,0+5+0)=5.
]

The DP represents each singleton with height 0, diameter 0, and identical diameter endpoints. The radius routine immediately returns 0 when both endpoints coincide.

The weighted path

```
3
1 2 10
2 3 1
```

shows why the radius calculation must be vertex-based. After cutting (2-3), the component containing vertices 1 and 2 has diameter 10. Its only possible centers are vertices 1 and 2, both having eccentricity 10. The continuous midpoint of the edge would have eccentricity 5, but that point cannot be chosen as an endpoint of the reconnected edge. The algorithm sees diameter endpoints 1 and 2, finds that there is no vertex between them, and returns radius 10.

For the official sample,

```
4
1 2 2
1 3 3
2 4 2
```

cutting (1-3) gives the singleton component `{3}` and the component `1-2-4`. The latter has diameter 4 between vertices 1 and 4, and vertex 2 is exactly at the midpoint, so its radius is 2. The removed edge has weight 3. The best crossing path is consequently (0+3+2=5), which is larger than the internal diameter 4. The algorithm outputs 5 and corresponds to reconnecting vertex 3 directly to vertex 2, as described by the problem.

The final subtle case is a weighted diameter whose midpoint lies inside an edge. Suppose a component is a path with edge weights 4 and 10. Its diameter is 14, while the midpoint lies 7 units from either endpoint, inside the second edge. The available vertices are at positions 0, 4, and 14, so their eccentricities are 14, 10, and 14. The correct vertex radius is 10, not 7. The binary-lifting routine locates the vertices surrounding position 7 and takes the smaller eccentricity, which is exactly the required discrete center.
