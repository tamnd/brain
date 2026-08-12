---
title: "CF 102331D - Determinant"
description: "We have a connected undirected graph and need the determinant of its adjacency matrix modulo (998244353). The graph has up to (25,000) vertices and (500,000) edges, but the unusual condition involving (k+1) vertices is the real structural constraint."
date: "2026-08-13T03:33:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "D"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 188
verified: true
draft: false
---

[CF 102331D - Determinant](https://codeforces.com/problemset/problem/102331/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph and need the determinant of its adjacency matrix modulo (998244353). The graph has up to (25,000) vertices and (500,000) edges, but the unusual condition involving (k+1) vertices is the real structural constraint. The official statement gives (k\le 25), and the contest tutorial identifies the equivalent structure as having edge-biconnected components of size at most (k).

The determinant of an adjacency matrix can be viewed combinatorially through the Leibniz formula. Every nonzero term corresponds to a permutation of the vertices in which every vertex is sent to an adjacent vertex. Decomposing that permutation into cycles gives a decomposition of all vertices into directed cycles, and the sign of a cycle of length (l) is ((-1)^{l-1}).

The key graph observation is about bridges. If an edge is a bridge, no cycle can contain that edge. Consequently, a bridge can occur in a permutation cycle only as a 2-cycle consisting of its two endpoints. After removing all bridges, every remaining connected component has no bridge internally, so these components form the natural small pieces of the graph.

Why are those pieces small? Suppose the graph obtained after deleting all bridges had a component containing at least (k+1) vertices. Choose any (k+1) vertices from it. No bridge separates any two of these vertices, because they are still connected after every bridge has been removed. That contradicts the condition in the statement. Conversely, if every such component has at most (k) vertices, any (k+1) chosen vertices must lie in at least two different components, and a bridge on the component-tree path separates a suitable pair. Thus the given condition is exactly the statement that every edge-biconnected component contains at most (k\le25) vertices.

This changes the scale of the problem completely. A general (25,000\times25,000) determinant is far too large. Gaussian elimination would require roughly

[
\frac{n^3}{3}\approx\frac{25000^3}{3}\approx5.2\cdot10^{12}
]

field operations in the dense worst case. Even storing such a matrix would require hundreds of millions of entries. The useful work must instead happen inside components of size at most 25, with a tree DP connecting them.

There are several edge cases that easily break a careless implementation. For a single vertex,

```
1 0 1
```

the adjacency matrix is ([0]), so the answer is (0). Treating an empty graph as having determinant (1) without considering that the actual component contains one uncovered vertex gives the wrong result.

For two vertices joined by one bridge,

```
2 1 1
1 2
```

the adjacency matrix is

[
\begin{pmatrix}0&1\1&0\end{pmatrix},
]

whose determinant is (-1), so the required modular answer is (998244352). A DP that counts the bridge 2-cycle but forgets its odd permutation sign produces (1) instead.

For a path on three vertices,

```
3 2 1
1 2
2 3
```

the determinant is (0). The middle vertex cannot be covered by a cycle decomposition. A tree DP that only tracks whether every edge is used can incorrectly count the two edges as a valid structure, even though determinant terms are cycle covers, not arbitrary edge subsets.

A bridge-free component also has to be handled without assuming that every component contributes a nonzero determinant. For example,

```
3 3 3
1 2
2 3
3 1
```

has one component containing all three vertices. Its adjacency matrix has determinant (2), and there are no bridge transitions at all. The component DP must reduce to an ordinary small determinant in this case.

## Approaches

The direct approach follows the definition of determinant. We could construct the entire adjacency matrix and run Gaussian elimination modulo (998244353). This is correct because elementary row operations preserve the determinant when their effects are tracked. Unfortunately, a (25,000\times25,000) dense elimination needs about (5.2\cdot10^{12}) elimination updates in the worst case, which is nowhere near the available five seconds.

The determinant expansion itself is even worse. The Leibniz formula has (n!) permutation terms, so it is useful only as a way to understand what the determinant counts, not as an algorithm.

The brute-force view does reveal the structure we need. A determinant term is a cycle decomposition of the vertices. A bridge cannot belong to a cycle of length at least three, because such a cycle would give another path between the bridge endpoints. Hence every bridge used by a determinant term is a 2-cycle.

Remove all bridges and contract every remaining connected component into one node. The result is a tree. Each component has at most (k) vertices, so we can process this tree from the leaves toward an arbitrary root. This is exactly the tree DP approach described in the contest tutorial.

Consider a component (B) and one of its vertices (v). Several child components can be attached to (v) by bridges. In a valid cycle decomposition, at most one of those child bridges can be used, because using a bridge means that (v) participates in the 2-cycle with the child endpoint.

For every child component (C), define two DP values. The value (dp[C][0]) means that the bridge from (C) to its parent is not used. The value (dp[C][1]) means that the bridge is used, so the boundary vertex of (C) is removed from the internal cycle cover of (C). The sign of the parent-child 2-cycle is deliberately handled by the parent transition, so (dp[C][1]) itself is just the determinant contribution after deleting that boundary vertex. This convention is what makes the local matrix especially clean.

For a vertex (v), let

[
s_v=\prod_C dp[C][0],
]

where (C) ranges over all child components attached to (v). If no child bridge is used, (v) stays inside the current component and receives weight (s_v).

If exactly one child bridge is used, the contribution is

[
t_v=\sum_C dp[C][1]\prod_{D\ne C}dp[D][0].
]

We compute this without division, because some (dp[C][0]) can be zero. Starting with `prod = 1` and `t = 0`, each child updates

[
t\leftarrow t\cdot dp[C][0]+prod\cdot dp[C][1],
]

followed by

[
prod\leftarrow prod\cdot dp[C][0].
]

Now let (A) be the ordinary adjacency matrix of the current edge-biconnected component. We replace it by a small weighted matrix (B) of the same size:

[
B_{vv}=-t_v,
]

and for an internal edge (v\mathord{-}u),

[
B_{vu}=s_v.
]

The two directions can have different weights, which is fine because only the determinant is being used. Expanding the determinant of (B), choosing a diagonal entry (-t_v) means that (v) uses one child bridge. Choosing the remaining rows through internal edges leaves a determinant of the adjacency matrix on the vertices that were not removed. The minus sign is exactly the sign of the bridge 2-cycle.

Thus (dp[B][0]=\det B).

If (p) is the vertex of (B) incident to the parent bridge, then (dp[B][1]) must remove (p) from the internal component. All children attached directly to (p) must use type 0, contributing (s_p). Hence

[
dp[B][1]=s_p\det B_{\setminus p},
]

where (B_{\setminus p}) is obtained by deleting row and column (p).

Each determinant is now at most (25\times25). Since the sum of component sizes is (n), the total cost is (O(nk^2)), matching the intended complexity stated in the contest tutorial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force determinant | (O(n^3)) with Gaussian elimination, or (O(n!)) from Leibniz expansion | (O(n^2)) for a dense matrix | Too slow |
| Optimal bridge-component DP | (O(m+n k^2)) | (O(m+n)) | Accepted |

## Algorithm Walkthrough

1. Find every bridge of the original graph using a low-link DFS. An edge (u-v) is a bridge exactly when the DFS subtree of (v) has no back edge reaching (u) or an ancestor of (u), equivalently `low[v] > tin[u]`. The implementation uses an iterative DFS so that a path of (25,000) vertices does not depend on Python recursion depth.
2. Remove all bridges conceptually and find the connected components that remain. These are the edge-biconnected components. The given condition guarantees that every component has at most (k) vertices.
3. Build the component tree. Each original bridge connects two different components, and because bridges cannot form a cycle, contracting every component produces a tree.
4. Root the component tree arbitrarily. For every non-root component, remember the endpoint of its parent bridge that lies inside the component. This vertex is the boundary vertex that has to disappear when the component uses its parent bridge.
5. Process components in reverse tree order. For every vertex (v) of the current component, combine all already-computed child components attached to (v). Compute (s_v) as the product of all child type-0 values.
6. Compute (t_v) as the sum of configurations in which exactly one child uses its bridge. The recurrence `t = t * dp0 + prod * dp1` adds either the new child to the unique chosen child or leaves the previous choice unchanged. It avoids division by a potentially zero (dp0).
7. Build the local matrix (B). Put (-t_v) on its diagonal. For every internal edge from (v) to (u), put (s_v) at position ((v,u)). The row weight (s_v) represents the contribution of all child subtrees when (v) remains in the component.
8. Compute (\det B) by modular Gaussian elimination. This value is (dp[B][0]), because every determinant term chooses either the diagonal option for a vertex that leaves through a child bridge or an internal edge for a vertex that remains in the component.
9. For every non-root component, delete its parent-boundary vertex from (B), compute the resulting determinant, and multiply it by (s_p). This gives (dp[B][1]). The parent component will supply the minus sign when it uses the bridge as a 2-cycle.
10. After the root component has been processed, its type-0 value is the determinant of the entire original adjacency matrix, so output it modulo (998244353).

Why it works: every determinant term is a vertex cycle decomposition. Inside one edge-biconnected component, all cycles are internal unless a vertex participates in a bridge 2-cycle. A bridge can only be used in such a 2-cycle, and a vertex can belong to at most one cycle, so each vertex can either remain inside its component or connect to exactly one child component. The values (s_v) and (t_v) enumerate exactly these two possibilities. The local determinant enumerates all compatible internal cycle covers, while the recursive DP values already account for every descendant component. Since the component graph is a tree, every determinant cycle decomposition has exactly one recursive decomposition and is counted once with its correct sign.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 998244353

def determinant(a):
    n = len(a)
    if n == 0:
        return 1

    ans = 1

    for col in range(n):
        pivot = col
        while pivot < n and a[pivot][col] == 0:
            pivot += 1

        if pivot == n:
            return 0

        if pivot != col:
            a[pivot], a[col] = a[col], a[pivot]
            ans = -ans

        p = a[col][col] % MOD
        ans = ans * p % MOD
        inv = pow(p, MOD - 2, MOD)

        row = a[col]

        for r in range(col + 1, n):
            x = a[r][col]
            if x == 0:
                continue

            factor = x * inv % MOD
            rr = a[r]
            rr[col] = 0

            for c in range(col + 1, n):
                rr[c] = (rr[c] - factor * row[c]) % MOD

    return ans % MOD

def solve():
    n, m, k = map(int, input().split())

    head = array('i', [-1]) * n
    to = array('i')
    nxt = array('i')
    eu = array('i')
    ev = array('i')

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        eid = len(eu)
        eu.append(u)
        ev.append(v)

        to.append(v)
        nxt.append(head[u])
        head[u] = len(to) - 1

        to.append(u)
        nxt.append(head[v])
        head[v] = len(to) - 1

    # Find bridges with iterative low-link DFS.
    tin = array('i', [0]) * n
    low = array('i', [0]) * n
    parent = array('i', [-1]) * n
    parent_edge = array('i', [-1]) * n
    it = array('i', head)
    bridge = array('b', [0]) * m

    timer = 0
    stack = [0]
    timer += 1
    tin[0] = low[0] = timer

    while stack:
        v = stack[-1]
        e = it[v]

        if e == -1:
            stack.pop()

            p = parent[v]
            if p != -1:
                pe = parent_edge[v]
                if low[v] > tin[p]:
                    bridge[pe >> 1] = 1
                if low[v] < low[p]:
                    low[p] = low[v]
            continue

        it[v] = nxt[e]

        if e == parent_edge[v]:
            continue

        u = to[e]

        if tin[u] == 0:
            parent[u] = v
            parent_edge[u] = e ^ 1
            timer += 1
            tin[u] = low[u] = timer
            stack.append(u)
        else:
            if tin[u] < low[v]:
                low[v] = tin[u]

    # Build edge-biconnected components by ignoring bridges.
    comp = array('i', [-1]) * n
    blocks = []
    pos = array('i', [0]) * n

    cid = 0
    for start in range(n):
        if comp[start] != -1:
            continue

        vertices = []
        stack = [start]
        comp[start] = cid

        while stack:
            v = stack.pop()
            pos[v] = len(vertices)
            vertices.append(v)

            e = head[v]
            while e != -1:
                if not bridge[e >> 1]:
                    u = to[e]
                    if comp[u] == -1:
                        comp[u] = cid
                        stack.append(u)
                e = nxt[e]

        blocks.append(vertices)
        cid += 1

    bc = cid

    # Component tree.
    tree = [[] for _ in range(bc)]

    for e in range(m):
        if not bridge[e]:
            continue

        u = eu[e]
        v = ev[e]
        cu = comp[u]
        cv = comp[v]

        tree[cu].append((cv, u, v))
        tree[cv].append((cu, v, u))

    # Root the component tree.
    parent_block = array('i', [-2]) * bc
    parent_block[0] = -1

    parent_vertex = array('i', [-1]) * bc
    order = [0]

    for c in order:
        for d, vc, vd in tree[c]:
            if parent_block[d] != -2:
                continue

            parent_block[d] = c
            parent_vertex[d] = vd
            order.append(d)

    # For every local vertex, store its child components.
    children_at = []
    for vertices in blocks:
        children_at.append([[] for _ in vertices])

    for c in range(1, bc):
        p = parent_block[c]

        # Find the edge p-c and its endpoint inside p.
        for d, vp, vc in tree[p]:
            if d == c:
                children_at[p][pos[vp]].append(c)
                break

    dp0 = array('i', [0]) * bc
    dp1 = array('i', [0]) * bc

    # Process bottom-up.
    for c in reversed(order):
        vertices = blocks[c]
        s = len(vertices)

        sv = [1] * s
        tv = [0] * s

        for i in range(s):
            prod = 1
            chosen = 0

            for child in children_at[c][i]:
                a = dp0[child]
                b = dp1[child]

                chosen = (chosen * a + prod * b) % MOD
                prod = prod * a % MOD

            sv[i] = prod
            tv[i] = chosen

        # B[i][i] = -t_i
        # B[i][j] = s_i for an internal edge i-j.
        mat = [[0] * s for _ in range(s)]

        for i in range(s):
            mat[i][i] = (-tv[i]) % MOD

        for i, v in enumerate(vertices):
            e = head[v]
            while e != -1:
                if comp[to[e]] == c:
                    j = pos[to[e]]
                    mat[i][j] = sv[i]
                e = nxt[e]

        dp0[c] = determinant([row[:] for row in mat])

        if c != 0:
            boundary = pos[parent_vertex[c]]
            reduced = []

            for i in range(s):
                if i == boundary:
                    continue

                row = []
                for j in range(s):
                    if j == boundary:
                        continue
                    row.append(mat[i][j])
                reduced.append(row)

            minor = determinant(reduced)
            dp1[c] = sv[boundary] * minor % MOD

    print(dp0[0] % MOD)

if __name__ == "__main__":
    solve()
```

The first part of the implementation stores the graph in forward-star arrays. The `array` module keeps the adjacency representation compact, which matters because the statement permits up to (500,000) input edges even though the structural promise makes such dense inputs impossible under the stated (k\le25). The representation is still robust against the raw input limit.

The bridge DFS keeps `tin[v]` and `low[v]`. For an undirected edge, the reverse of the DFS-tree edge is skipped explicitly. When a child finishes, `low[child] > tin[parent]` identifies a bridge.

After the bridges are known, another traversal assigns every vertex to its bridge-connected component. The `pos` array maps an original vertex to its local index inside its component, so the small determinant matrices can be built without dictionaries.

The component tree is rooted iteratively. For each component, `children_at[i]` contains exactly the child components whose bridge endpoint lies at local vertex `i`. This is the information needed for the (s_v,t_v) transition.

The recurrence

```
chosen = (chosen * a + prod * b) % MOD
prod = prod * a % MOD
```

is deliberately written without modular division. A tempting implementation would compute (t_v=s_v\sum dp_1/dp_0), but (dp_0) can be zero. The prefix-product recurrence remains valid in every case.

The local matrix is only (s\times s), not (2s\times2s). The auxiliary-vertex construction from the original editorial can be algebraically eliminated. Row (v) is multiplied by (s_v), while choosing a child connection gives the diagonal value (-t_v). This produces the compact matrix (B) described above and cuts the constant factor substantially. The original tutorial describes the equivalent fictitious-vertex construction and gives (O(k^3)) work per component.

Gaussian elimination searches for a nonzero pivot because a zero pivot does not necessarily mean the determinant is zero until every row below that column has been checked. Row swaps flip the determinant sign, while adding a multiple of one row to another does not change it. Every arithmetic operation is reduced modulo (998244353), so Python integers never become large enough to cause overflow issues.

The empty matrix occurs when a component has one boundary vertex and that vertex is deleted. Its determinant is (1), which is the standard empty-product convention and is required for a leaf component consisting of a single vertex.

## Worked Examples

### Sample 1

The graph is the path

```
1 - 2 - 3 - 4
```

with (k=1). Every edge is a bridge, so every edge-biconnected component contains one vertex.

Root the component tree at vertex 1.

| Component | Vertex | Child (dp_0) | Child (dp_1) | (s_v) | (t_v) | (dp_0) | (dp_1) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 4 | none | none | 1 | 0 | 0 | 1 |
| 3 | 3 | 0 | 1 | 0 | 1 | 1 | 0 |
| 2 | 2 | 1 | 0 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 | 0 | 1 | 1 | not needed |

For the leaf vertex 4, its local matrix is simply ([0]), giving (dp_0=0). Deleting its boundary vertex leaves the empty matrix, so (dp_1=1). The parent therefore sees the bridge 2-cycle with its negative sign through the diagonal entry (-t_v).

At the root, the resulting local matrix is ([0]) with an effective child connection, and the final determinant is (1), matching the sample output. The example demonstrates why the sign of a bridge 2-cycle must be introduced exactly once.

### Sample 2

The six vertices form two small cyclic regions connected through bridges. After removing the bridges, the component tree has components of size at most three, satisfying (k=3).

For each component, the children are processed first. At every boundary vertex, the DP combines the possibility that no child bridge is used with the possibility that exactly one child bridge is used.

| Stage | Current component | Local size | (dp_0) | (dp_1) |
| --- | --- | --- | --- | --- |
| 1 | leaf component | small | computed from its local matrix | computed after deleting boundary |
| 2 | middle component | small | combines child (s_v,t_v) values | deletes its parent boundary |
| 3 | root component | small | final determinant | not needed |

The resulting root value is

[
998244352\equiv -1\pmod{998244353},
]

which is the second sample output. The trace exercises the case where a component has both internal edges and bridge transitions, so the local determinant must combine cycle covers inside the component with child 2-cycles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m+n k^2)) | Bridge detection and component construction are linear. A component of size (s\le k) needs (O(s^3)) determinant work, and (\sum s=n), giving (O(nk^2)). |
| Space | (O(m+n)) | The graph, bridge information, component tree, and DP arrays are linear in the input size. |

The largest component has only 25 vertices, so the expensive linear algebra is performed on tiny matrices. The sum of component sizes is (n), which is why the cubic local computation becomes (O(nk^2)) globally. The contest tutorial gives the same (O(nk^2)) bound for the intended tree DP.

The iterative DFS avoids recursion-stack problems, and the compact adjacency arrays keep memory usage controlled even when reading the nominal (500,000)-edge input limit.

## Test Cases

```python
# Assume the solution code above is saved as solution.py.
# This harness redirects stdin/stdout and calls solve() directly.

import io
import sys
from contextlib import redirect_stdout

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    try:
        with redirect_stdout(out):
            solve()
        return out.getvalue().strip()
    finally:
        sys.stdin = old_stdin

# Provided samples.
assert run("""\
4 3 1
1 2
2 3
3 4
""") == "1", "sample 1"

assert run("""\
6 6 3
2 3
5 6
2 5
1 2
3 4
6 2
""") == "998244352", "sample 2"

assert run("""\
10 15 10
1 8
1 7
6 7
2 8
6 9
1 2
4 9
4 10
4 6
5 6
3 8
9 10
8 10
3 5
2 7
""") == "35", "sample 3"

# Minimum-size graph.
assert run("""\
1 0 1
""") == "0", "single isolated vertex"

# One bridge. The adjacency matrix has determinant -1.
assert run("""\
2 1 1
1 2
""") == "998244352", "single edge"

# Three-vertex path. Its determinant is zero.
assert run("""\
3 2 1
1 2
2 3
""") == "0", "odd path"

# One bridge-free component. Its adjacency matrix is the triangle matrix,
# whose determinant is 2.
assert run("""\
3 3 3
1 2
2 3
3 1
""") == "2", "triangle"

# Maximum n with a path. For P_n, det(P_n) is 1 when n is divisible by 4.
n = 25000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
large_path = f"{n} {n - 1} 1\n{edges}\n"
assert run(large_path) == "1", "maximum-n path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 1` | `0` | Empty adjacency matrix entry and minimum-size boundary case |
| `2 1 1` | `998244352` | Sign of a bridge 2-cycle |
| `3 2 1` | `0` | A cycle cover does not exist for an odd path |
| Triangle with (k=3) | `2` | A bridge-free component and ordinary local determinant |
| Path with (25,000) vertices | `1` | Maximum (n), iterative DFS, and linear-sized component tree |

## Edge Cases

For a single vertex,

```
1 0 1
```

there are no edges and no bridges. The only component contains vertex 1, so its local matrix is ([0]). Gaussian elimination finds no pivot and returns (0). The root DP is therefore (0), exactly matching the adjacency determinant.

For a single bridge,

```
2 1 1
1 2
```

both vertices are singleton components. The leaf has (dp_0=0) and (dp_1=1), because deleting its boundary leaves the empty matrix. At the parent, the child contributes (t=1), so the local matrix is ([-1]). Its determinant is (-1), represented modulo (998244353) as (998244352). The bridge's 2-cycle sign is consequently accounted for exactly once.

For the three-vertex path,

```
3 2 1
1 2
2 3
```

the leaf at vertex 3 gives (dp_0=0,dp_1=1). At vertex 2, the child connection gives (t_2=1), so the local matrix becomes ([-1]), giving (dp_0=-1) and (dp_1=0). The zero (dp_1) means that vertex 2 cannot simultaneously be removed through its parent bridge while its child side is already fixed. At the root, the resulting determinant is (0), as required.

For the triangle,

```
3 3 3
1 2
2 3
3 1
```

there are no bridges, so the component tree contains one node. Every (s_v) is (1) and every (t_v) is (0). The local matrix is exactly the triangle adjacency matrix,

[
\begin{pmatrix}
0&1&1\
1&0&1\
1&1&0
\end{pmatrix},
]

whose determinant is (2). The DP therefore degenerates naturally to the ordinary determinant computation for a small bridge-free component.

The large path test uses (25,000) singleton components. Its component tree is itself a path, so the bridge DFS reaches the maximum possible depth. Because the implementation uses an explicit stack rather than recursive Python calls, it handles the case without recursion-limit or C-stack problems. The determinant recurrence for a path is (D_n=-D_{n-2}), with (D_0=1) and (D_2=-1). Since (25,000\equiv0\pmod4), the answer is (1). This test exercises the linear part of the algorithm rather than the small-matrix part.
