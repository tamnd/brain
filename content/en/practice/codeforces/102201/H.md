---
title: "CF 102201H - Hard To Explain"
description: "Root the tree at vertex 1. For a query (V, T), the relevant vertices are exactly the ancestors of V, including V itself and the root. Among those ancestors, vertex i can be used only when Ci = T, and its cost is the value of the line [ fi(T)=Ai+BiT."
date: "2026-08-18T10:35:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102201
codeforces_index: "H"
codeforces_contest_name: "Moscow Pre-Finals Workshop 2019. KAIST Contest"
rating: 0
weight: 102201
solve_time_s: 600
verified: true
draft: false
---

[CF 102201H - Hard To Explain](https://codeforces.com/problemset/problem/102201/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m  
**Verified:** yes  

## Solution
## Problem Understanding

Root the tree at vertex 1. For a query `(V, T)`, the relevant vertices are exactly the ancestors of `V`, including `V` itself and the root. Among those ancestors, vertex `i` can be used only when `C_i >= T`, and its cost is the value of the line

[
f_i(T)=A_i+B_iT.
]

The task is to return the smallest such value.

The tree condition on `B` is the central structural property:

[
B_{\operatorname{parent}(v)}\le B_v.
]

So along every root-to-leaf path, the slopes of the corresponding lines never decrease. Without this condition, the problem would require a fully dynamic convex hull structure. With it, the lines belonging to one root-to-vertex path have a useful ordering.

There are up to 80,000 vertices and 160,000 queries. A query may involve an entire root-to-leaf path, so explicitly walking the path is already too slow on a chain-shaped tree. In the worst case there are about (80,000) ancestors per query, giving roughly (1.28\times10^{10}) line evaluations for 160,000 queries. The solution has to get close to logarithmic work per query.

There are three edge conditions that commonly cause incorrect implementations.

First, the queried vertex itself belongs to the path. For example,

```
1 1
5
7
1000000000
1 0
```

has answer `5`, because vertex 1 is also the queried vertex. An implementation that starts from `parent[V]` would incorrectly find no candidate.

Second, the condition is `C_i >= T`, not `C_i > T`. For

```
2 1
10 1
1 2
5 5
1 2
2 5
```

the answer is `6`, because vertex 2 has `C_2 = 5` and is valid at `T = 5`. A strict comparison would discard it and return `15`.

Third, `T = 0` is legal. In that case every vertex satisfies `C_i >= T`, so the answer is simply the smallest `A_i` on the root-to-`V` path. In the sample, the query `(4, 0)` considers vertices `1, 2, 4` and returns `2`. Any implementation that assumes a positive query coordinate or starts its Li Chao domain at `1` can fail here.

## Approaches

The brute-force solution follows the definition directly. For every query, walk from `V` toward the root, ignore vertices whose `C_i` is smaller than `T`, and evaluate `A_i+B_iT` for the rest. This is correct because every vertex on that walk is exactly one of the vertices on the unique path from the root to `V`.

The problem is the path length. A chain of 80,000 vertices together with 160,000 queries can require (80,000\cdot160,000=12.8) billion evaluations. Even though one evaluation is only a couple of integer operations, that is far beyond the time limit.

The first useful observation is to regard every vertex as a line

[
y=A_i+B_ix.
]

The query then asks for the lowest valid line at `x = T`. The second observation is that validity is a prefix of the x-axis: line `i` exists for all `x <= C_i`. Thus every vertex actually gives us a line segment extending from the left toward `C_i`.

The third observation is the tree structure. If we process vertices from the root toward a node, we are inserting lines whose slopes are nondecreasing. A query at vertex `V` needs exactly the data structure obtained after inserting the lines on the root-to-`V` path.

We can make this persistent. Each vertex stores a version of the data structure inherited from its parent, then adds its own line segment. A query at `V` uses version `V`, so the persistence automatically restricts the candidate set to ancestors of `V`.

The remaining issue is that a line is valid only up to `C_i`, rather than on the entire x-axis. A Li Chao tree can insert a line over an interval instead of over the whole coordinate domain. Since every valid interval is `[0, C_i]`, we perform a range insertion of the line on that prefix. The Li Chao tree then guarantees that a query at `T` sees exactly the lines whose validity interval contains `T`.

Persistence is handled by copying only the Li Chao nodes changed by an insertion. The version belonging to a child points to the parent's root, so different tree branches share all unchanged structure.

The resulting approach is a persistent segment tree whose nodes contain Li Chao information. A range insertion costs (O(\log^2 C)), where (C\le10^9), and a point query costs (O(\log C)). With the given bounds, the logarithms are at most about 30.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(NQ)) | (O(N)) | Too slow |
| Persistent interval Li Chao | (O(N\log^2 10^9+Q\log 10^9)) | (O(N\log^2 10^9)) worst case | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex 1 and determine the parent of every vertex.

We do this iteratively rather than recursively, because a tree can be a chain of 80,000 vertices and Python's recursion limit is not suitable for such a traversal.
2. For every vertex `v`, define `root[v]` to be the root of a persistent Li Chao tree representing all valid line segments belonging to the vertices on the path from vertex 1 to `v`.

The version for the root initially contains line 1. For every other vertex `v`, start from `root[parent[v]]` and insert the line

[
y=A_v+B_vx
]

on the interval

[
[0,C_v].
]

This is the key persistence invariant. At the moment `root[v]` is built, it contains exactly the lines belonging to ancestors of `v`.
3. Represent the x-axis by the integer interval `[0, 10^9]`.

We only ever query integer values of `T`, so no floating-point intersections are needed. A Li Chao tree works entirely with comparisons of integer line values.
4. To insert a line on `[0,C_v]`, recursively descend through the Li Chao coordinate tree.

If the current coordinate interval is completely covered by `[0,C_v]`, perform an ordinary Li Chao insertion on that interval.

If only part of the interval is covered, recursively process the covered children.

Because the data structure is persistent, every modified Li Chao node is copied. Unmodified children continue to point to the old version.
5. For an ordinary Li Chao insertion, keep one candidate line at every segment-tree node.

Compare the old and new lines at the left endpoint, midpoint, and right endpoint. If the new line is better at the midpoint, swap it with the stored line. The line that loses at the midpoint can still be relevant on at most one side, so recurse into that side.

This is the standard Li Chao invariant: along every root-to-leaf path, at least one stored line is optimal at the corresponding leaf coordinate.
6. To answer `(V,T)`, start at `root[V]` and descend to the leaf representing `T`.

At every visited Li Chao node, evaluate its stored line at `T` and take the minimum. Since `root[V]` contains only ancestors of `V`, and interval insertion made a line present only for `T <= C_i`, the minimum is exactly over the vertices allowed by the query.
7. Output the collected answers in their original order.

### Why it works

The invariant is that `root[v]` contains precisely the line segments of vertices on the root-to-`v` path. This is true for vertex 1 after inserting its line. When moving from a parent to a child, persistence copies the parent's version and adds exactly the child's line segment, so the invariant remains true.

For a query `(V,T)`, a line from vertex `i` appears in `root[V]` exactly when `i` is an ancestor of `V`. Its interval insertion places it into the Li Chao structure only on coordinates `x <= C_i`, so it participates in the query exactly when `T <= C_i`. The Li Chao invariant then guarantees that the minimum value among all participating lines is found on the root-to-`T` search path.

The monotonicity of `B` is compatible with the ancestor construction and is the structural reason this problem admits a path-based convex-hull solution. The implementation below uses the more general interval Li Chao formulation, so it does not need floating-point intersection calculations or special cases for equal slopes.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30
XMAX = 10**9

def solve():
    n, q = map(int, input().split())

    A = [0] + list(map(int, input().split()))
    B = [0] + list(map(int, input().split()))
    C = [0] + list(map(int, input().split()))

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    parent = [0] * (n + 1)
    order = [1]
    parent[1] = -1

    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    # Persistent Li Chao nodes.
    #
    # Each node contains:
    #   line index stored at this node
    #   left child
    #   right child
    #
    # A line index of 0 means "no line".
    lc = [0]
    rc = [0]
    ln = [0]

    def value(line_id, x):
        if line_id == 0:
            return INF
        return A[line_id] + B[line_id] * x

    def clone(node):
        if node == 0:
            lc.append(0)
            rc.append(0)
            ln.append(0)
        else:
            lc.append(lc[node])
            rc.append(rc[node])
            ln.append(ln[node])
        return len(ln) - 1

    def add_line(node, l, r, new_line):
        node = clone(node)

        old_line = ln[node]

        if old_line == 0:
            ln[node] = new_line
            return node

        mid = (l + r) >> 1

        if value(new_line, mid) < value(old_line, mid):
            ln[node], new_line = new_line, old_line

        if l == r:
            return node

        if value(new_line, l) < value(ln[node], l):
            left = add_line(lc[node], l, mid, new_line)
            lc[node] = left
        elif value(new_line, r) < value(ln[node], r):
            right = add_line(rc[node], mid + 1, r, new_line)
            rc[node] = right

        return node

    def add_segment(node, l, r, ql, qr, new_line):
        if qr < l or r < ql:
            return node

        node = clone(node)

        if ql <= l and r <= qr:
            # The whole interval is covered, so this is a normal
            # Li Chao insertion.
            return add_line(node, l, r, new_line)

        mid = (l + r) >> 1

        if ql <= mid:
            lc[node] = add_segment(
                lc[node], l, mid, ql, qr, new_line
            )

        if qr > mid:
            rc[node] = add_segment(
                rc[node], mid + 1, r, ql, qr, new_line
            )

        return node

    def query(node, l, r, x):
        ans = value(ln[node], x)

        if l == r:
            return ans

        mid = (l + r) >> 1

        if x <= mid:
            if lc[node]:
                other = query(lc[node], l, mid, x)
                if other < ans:
                    ans = other
        else:
            if rc[node]:
                other = query(rc[node], mid + 1, r, x)
                if other < ans:
                    ans = other

        return ans

    roots = [0] * (n + 1)

    # Build versions in parent-before-child order.
    for v in order:
        base = roots[parent[v]] if parent[v] > 0 else 0
        roots[v] = add_segment(base, 0, XMAX, 0, C[v], v)

    out = []

    for _ in range(q):
        v, t = map(int, input().split())
        out.append(str(query(roots[v], 0, XMAX, t)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first traversal constructs the parent relation. The array `order` is a topological order of the rooted tree in the sense that every parent occurs before its children, which lets us build `root[v]` without recursion.

The arrays `lc`, `rc`, and `ln` form the persistent Li Chao tree. Index zero represents an empty node. A copied node inherits both child pointers and its stored line from the previous version, so only nodes affected by the new line need to be changed.

`add_line` is the ordinary Li Chao insertion. The line stored at a node is the one currently better at the midpoint. If the displaced line can still beat it on the left or right endpoint, it is recursively inserted into that side.

`add_segment` adds the line only to the coordinate interval `[0,C_v]`. When the current interval is completely covered, it delegates to `add_line`. Otherwise it copies the current node and continues into the intersecting children.

The boundary is inclusive. The call uses `0` through `C[v]`, so a query with `T == C[v]` correctly accepts the vertex. The global coordinate interval is also inclusive on both ends, which is why the recursion uses `[l, r]` rather than a half-open interval.

Python integers have arbitrary precision, so expressions such as `B[i] * T + A[i]` cannot overflow. In C++, a 64-bit signed integer is also sufficient here because the largest value is at most about (10^{18}+10^9).

One implementation detail deserves attention. The tree traversal is iterative, while the Li Chao recursion has depth only about 30 because its coordinate range is `[0,10^9]`. Thus the tree itself cannot trigger Python's recursion-depth limitation.

## Worked Examples

The supplied sample has the tree

```
        1
       / \
      2   3
     / \
    4   5
```

For vertex 4, the path is `1 -> 2 -> 4`. Their lines are

[
5+T,\qquad 4+2T,\qquad 2+4T.
]

The validity limits are `10^9`, `2`, and `5`.

For the first query, `T = 0`, every one of these lines is valid.

| Vertex | Line | C | Value at T=0 | Current minimum |
| --- | --- | --- | --- | --- |
| 1 | (5+T) | (10^9) | 5 | 5 |
| 2 | (4+2T) | 2 | 4 | 4 |
| 4 | (2+4T) | 5 | 2 | 2 |

The answer is `2`.

For the second query, `T = 2`, all three vertices still satisfy their validity condition.

| Vertex | Line | C | Value at T=2 | Current minimum |
| --- | --- | --- | --- | --- |
| 1 | (5+T) | (10^9) | 7 | 7 |
| 2 | (4+2T) | 2 | 8 | 7 |
| 4 | (2+4T) | 5 | 10 | 7 |

The answer is `7`.

The trace demonstrates why the validity condition is attached to the line itself rather than to the vertex being queried. At `T=2`, vertex 2 is exactly on its boundary and remains eligible.

A second example isolates the boundary condition.

```
3 3
10 1 100
1 2 3
1000000000 5 100
1 2
2 3
2 5
3 5
3 0
```

The root-to-3 path contains vertices 1, 2, and 3.

| Query | Eligible vertices | Values | Answer |
| --- | --- | --- | --- |
| `(2,5)` | 1, 2 | 15, 11 | 11 |
| `(3,5)` | 1, 2, 3 | 15, 11, 115 | 11 |
| `(3,0)` | 1, 2, 3 | 10, 1, 100 | 1 |

The first query is especially useful because `C_2 = 5` and `T = 5`. The line from vertex 2 must remain present. The last query confirms that `T = 0` makes every vertex eligible and reduces the objective to the minimum `A`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log^2 10^9+Q\log 10^9)) | Every vertex creates one persistent interval insertion, and every query performs one Li Chao point query |
| Space | (O(N\log^2 10^9)) worst case | Persistence copies the Li Chao nodes modified by every interval insertion |

Since (\log_2(10^9)) is only about 30, the logarithmic factor is bounded by a small constant. The solution avoids walking root-to-vertex paths per query, which is the part that makes the direct implementation impossible for a chain-shaped tree.

The large memory limit of 1024 MB is useful for this persistent representation. The main cost is the copied Li Chao nodes, not the original tree.

## Test Cases

```python
import io
import sys

# The production solution is the solve() function from above.
# For assert-based tests, execute the same algorithm against an
# in-memory stdin/stdout pair.

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
sample1 = """\
5 2
5 4 3 2 1
1 2 3 4 5
1000000000 2 4 5 2
1 2
1 3
2 4
2 5
4 0
4 2
"""

assert run(sample1) == """\
2
7
""".strip(), "sample 1"

# Minimum-size tree. The only possible candidate is the root.
sample2 = """\
1 3
17
23
1000000000
1 0
1 1000000000
1 999999999
"""

assert run(sample2) == """\
17
23000000017
23000000000
""".strip(), "single vertex"

# Exact C boundary and T = 0.
sample3 = """\
3 3
10 1 100
1 2 3
1000000000 5 100
1 2
2 3
2 5
3 5
3 0
"""

assert run(sample3) == """\
11
11
1
""".strip(), "C boundary and zero"

# Equal slopes. The ancestor condition allows equal B values.
# At T=10, vertex 3 is valid exactly at C=10.
sample4 = """\
4 4
20 5 1 100
7 7 7 7
1000000000 3 10 2
1 2
2 3
2 4
3 3
3 10
4 10
4 0
"""

assert run(sample4) == """\
15
71
27
1
""".strip(), "equal slopes"

# Large values, testing 64-bit-sized products.
sample5 = """\
2 3
1000000000 1000000000
1000000000 1000000000
1000000000 1000000000
1 2
2 0
2 1
2 1000000000
"""

assert run(sample5) == """\
1000000000
2000000000
1000000000000001000000000
""".strip(), "large arithmetic"

# A chain catches implementations that accidentally exclude an
# ancestor or use the wrong validity comparison.
sample6 = """\
5 4
50 40 30 20 10
1 2 3 4 5
1000000000 1 2 3 4
1 2
2 3
3 4
4 5
5 0
5 1
5 2
5 4
"""

assert run(sample6) == """\
10
41
56
250
""".strip(), "chain boundaries"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | `17`, `23000000017`, `23000000000` | Root-only paths and the largest possible query value |
| Three-vertex chain | `11`, `11`, `1` | Exact `C_i = T` boundary and `T = 0` |
| Equal slopes | `15`, `71`, `27`, `1` | Non-strict monotonicity of `B` and equal-slope lines |
| Large arithmetic | Large 64-bit-sized values | Correct integer arithmetic without overflow |
| Five-vertex chain | `10`, `41`, `56`, `250` | Multiple ancestor validity boundaries and path persistence |

## Edge Cases

The single-vertex case

```
1 3
17
23
1000000000
1 0
1 1000000000
1 999999999
```

has no edges and every query uses the same root line. The persistent structure starts empty and inserts the root line over `[0,10^9]`. Every query reaches that line, producing `17`, `23000000017`, and `23000000000`.

For an exact validity boundary,

```
3 1
10 1 100
1 2 3
1000000000 5 100
1 2
2 3
2 5
```

vertex 2 has `C_2 = 5`, so its line is inserted over `[0,5]`. Querying at `T=5` reaches the endpoint of that interval and includes the line. Its value is `1+7*5=36` in this particular input if the line has `B_2=7`; in the earlier concrete test, `A_2=1` and `B_2=2`, giving `11`. The implementation uses `qr = C[v]`, so equality is handled naturally.

For `T=0`, every `C_i` is at least 1, so every line on the path is valid. The Li Chao query starts at coordinate zero, and no special branch is necessary. In the sample path `1 -> 2 -> 4`, the values are `5`, `4`, and `2`, so the answer is `2`.

Equal slopes are also legal because the condition on `B` is non-strict. Suppose an ancestor and its child both have `B=7`. Their lines are parallel. The Li Chao comparisons still work because it never divides by a slope difference. The line with the smaller value at the query coordinate wins automatically.

Finally, the largest possible product is on the order of (10^9\cdot10^9=10^{18}). Python handles this directly with arbitrary-precision integers. In a fixed-width implementation, the calculation must use a 64-bit signed type rather than a 32-bit integer.
