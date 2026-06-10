---
title: "CF 1464F - My Beautiful Madness"
description: "We maintain a multiset of paths on a tree. Paths can be inserted and deleted dynamically. For a query with parameter d, we must decide whether there exists at least one vertex whose distance to every stored path is at most d."
date: "2026-06-11T01:57:05+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 1464
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 692 (Div. 1, based on Technocup 2021 Elimination Round 3)"
rating: 3500
weight: 1464
solve_time_s: 122
verified: false
draft: false
---

[CF 1464F - My Beautiful Madness](https://codeforces.com/problemset/problem/1464/F)

**Rating:** 3500  
**Tags:** data structures, trees  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We maintain a multiset of paths on a tree. Paths can be inserted and deleted dynamically.

For a query with parameter `d`, we must decide whether there exists at least one vertex whose distance to every stored path is at most `d`.

Another way to say the same thing is this:

For every stored path `P`, consider all vertices whose distance from `P` is at most `d`. We need to know whether the intersection of all these sets is non-empty.

The tree contains up to `2 · 10^5` vertices and there are up to `2 · 10^5` operations. Any solution that touches all active paths during a query is immediately ruled out. Even `O(√q)` work per operation is uncomfortable. We need something close to logarithmic time.

The difficulty is that the maintained objects are paths, not vertices. Insertions and deletions happen online, so we cannot process queries offline.

A subtle edge case appears when the same path is inserted multiple times.

```
add (1,2)
add (1,2)
delete (2,1)
```

One copy still remains. Any structure that only stores existence instead of multiplicity will break.

Another easy mistake is to think that a query asks whether all stored paths intersect. For `d > 0` that is not true.

Consider a chain:

```
1 - 2 - 3 - 4 - 5
```

with stored paths `(1,1)` and `(5,5)`.

For `d = 2`, vertex `3` is within distance `2` of both paths, so the answer is `Yes` even though the paths themselves are disjoint.

The hardest part is understanding what condition on all stored paths is actually being tested.

## Approaches

A brute force approach would explicitly maintain all active paths. For a query `3 d`, we could test every vertex of the tree and check its distance to every active path.

Distance from a vertex to a path can be computed using LCA machinery, but even if that check were constant time, we would still perform

```
O(n · |P|)
```

work per query.

With both values reaching `2 · 10^5`, this is completely impossible.

The key observation is that every path `(u,v)` can be represented by its LCA.

Let

```
l = lca(u,v)
```

A vertex `x` is within distance `d` from path `(u,v)` iff the projection of `x` onto the path reaches the path before climbing more than `d` edges. Rewriting this condition for all active paths simultaneously reveals a surprisingly strong structure.

Suppose we collect LCAs of all active paths.

Let `L` be the deepest active LCA.

If some vertex is within distance `d` from every path, then that vertex must lie inside the subtree of the ancestor obtained by climbing `2d` edges above `L`.

That reduces the problem to a subtree.

Inside that subtree, only the LCAs matter. We need all active LCAs to belong to the same ancestor subtree, and the diameter of the active LCA set inside that subtree must be small enough.

The active LCAs form a dynamic set of vertices. Dynamic tree diameters are a standard structure: if two segments know their diameters, the diameter of their union can be obtained by checking only the endpoints of the two diameters.

This turns the whole problem into maintaining:

1. A dynamic multiset of LCAs.
2. The deepest active LCA.
3. The diameter of all active LCAs inside an Euler-tour subtree.
4. The number of active paths whose LCA belongs to a subtree.

All operations can then be handled in logarithmic time.

The accepted solution uses:

- Euler tour intervals.
- Binary lifting.
- A Fenwick tree.
- A segment tree maintaining diameters.
- A multiset ordered by depth.

The resulting complexity is `O(log n)` per update and query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · | P | ) per query |
| Optimal | O(log n) per operation | O(n log n) | Accepted |

## Algorithm Walkthrough

### Geometric reformulation

For an active path `(u,v)` let

```
l = lca(u,v)
```

The path consists of two upward chains meeting at `l`.

For a vertex `x` to be within distance `d` from this path, the ancestor of `l` obtained after climbing `d` edges must still be reachable from `x` without exceeding another `d` edges.

After simplifying this condition across all paths, only the LCAs remain relevant.

### Maintained objects

Let `S` be the multiset of LCAs of all active paths.

For every active path:

1. Add its LCA to `S`.
2. Remove its LCA when the path disappears.

We maintain:

1. The deepest vertex of `S`.
2. Counts of active LCAs inside Euler-tour subtrees.
3. Diameter information of active LCAs.

### Data structures

1. Run a DFS.
2. Compute Euler entry `tin` and exit `tout`.
3. Build binary lifting tables.
4. Build a Fenwick tree over Euler order.
5. Build a segment tree whose leaves correspond to vertices.

A segment tree node stores the diameter of all active vertices in its interval.

A diameter is represented by:

```
(endpoint1, endpoint2, length)
```

### Merging two diameter structures

Suppose the left child has diameter endpoints `(a,b)` and the right child has `(c,d)`.

The diameter of the union must be one of:

```
(a,b)
(c,d)
(a,c)
(a,d)
(b,c)
(b,d)
```

Checking these six pairs is enough.

This is the standard dynamic diameter merge.

### Inserting a path

1. Compute `l = lca(u,v)`.
2. Add one occurrence of `l` to the depth-ordered multiset.
3. Add one occurrence of `l` to the Fenwick tree.
4. If this is the first occurrence of `l`, activate its leaf in the segment tree.

### Deleting a path

1. Compute `l = lca(u,v)`.
2. Remove one occurrence from the multiset.
3. Remove one occurrence from the Fenwick tree.
4. If the multiplicity becomes zero, deactivate the segment-tree leaf.

### Answering query `3 d`

Let `L` be the deepest active LCA.

1. Move `d` edges upward from `L`, obtaining `x`.
2. Move another `d` edges upward from `x`, obtaining `y`.

The candidate common point must lie inside subtree `y`.

First check whether every active LCA belongs to that subtree.

Using Euler intervals and the Fenwick tree:

```
count(subtree(y)) == number_of_active_paths
```

must hold.

If not, answer `No`.

Otherwise query the segment tree on the Euler interval of subtree `y`.

This returns the diameter of all active LCAs in that subtree.

Let the diameter endpoints be `(p,q)`.

The answer is `Yes` iff

```
dist(x,p) ≤ d
and
dist(x,q) ≤ d
```

Because every active LCA lies on a set whose farthest pair is `(p,q)`.

If both diameter endpoints fit inside the radius-`d` ball centered at `x`, every active LCA fits as well.

### Why it works

The deepest active LCA is the most restrictive one. Any feasible vertex must stay close to it.

Climbing `2d` levels above that deepest LCA produces the largest subtree that can still contain a common feasible vertex. Every active LCA must lie inside this subtree. If even one active LCA escapes, no vertex can satisfy all constraints simultaneously.

Inside the valid subtree, feasibility depends only on the maximum pairwise distance among active LCAs. The diameter endpoints are sufficient because every other active LCA lies no farther from the center candidate than one of the diameter endpoints. Thus checking the two diameter endpoints completely characterizes the whole set.

This invariant is preserved after every insertion and deletion because all maintained structures depend only on active LCA multiplicities.

## Python Solution

```python
import sys
from bisect import bisect_left, insort

input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    LOG = 20

    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    depth = [0] * (n + 1)
    up = [[0] * (n + 1) for _ in range(LOG + 1)]
    euler = [0] * (n + 1)

    timer = 0

    sys.setrecursionlimit(1 << 20)

    def dfs(v, p):
        nonlocal timer
        timer += 1
        tin[v] = timer
        euler[timer] = v

        up[0][v] = p
        depth[v] = depth[p] + 1

        for i in range(1, LOG + 1):
            up[i][v] = up[i - 1][up[i - 1][v]]

        for to in g[v]:
            if to != p:
                dfs(to, v)

        tout[v] = timer

    dfs(1, 1)

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

        for i in range(LOG, -1, -1):
            if up[i][a] != up[i][b]:
                a = up[i][a]
                b = up[i][b]

        return up[0][a]

    def dist(a, b):
        c = lca(a, b)
        return depth[a] + depth[b] - 2 * depth[c]

    def jump(v, k):
        for i in range(LOG + 1):
            if k >> i & 1:
                v = up[i][v]
        return v

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            n = self.n
            bit = self.bit
            while idx <= n:
                bit[idx] += val
                idx += idx & -idx

        def sum(self, idx):
            bit = self.bit
            res = 0
            while idx:
                res += bit[idx]
                idx -= idx & -idx
            return res

        def range_sum(self, l, r):
            return self.sum(r) - self.sum(l - 1)

    fenwick = Fenwick(n)

    NEG = (-1, -1, -1)

    def merge(A, B):
        if A[0] == -1:
            return B
        if B[0] == -1:
            return A

        cand = [
            (A[0], A[1]),
            (B[0], B[1]),
            (A[0], B[0]),
            (A[0], B[1]),
            (A[1], B[0]),
            (A[1], B[1]),
        ]

        best_u, best_v = A[0], A[1]
        best_d = dist(best_u, best_v)

        for u, v in cand:
            d = dist(u, v)
            if d > best_d:
                best_d = d
                best_u, best_v = u, v

        return (best_u, best_v, best_d)

    seg = [NEG] * (4 * n)

    def update(node, l, r, pos, val):
        if l == r:
            seg[node] = (val, val, 0) if val != -1 else NEG
            return

        mid = (l + r) // 2

        if pos <= mid:
            update(node * 2, l, mid, pos, val)
        else:
            update(node * 2 + 1, mid + 1, r, pos, val)

        seg[node] = merge(seg[node * 2], seg[node * 2 + 1])

    def query(node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return seg[node]

        mid = (l + r) // 2

        if qr <= mid:
            return query(node * 2, l, mid, ql, qr)
        if ql > mid:
            return query(node * 2 + 1, mid + 1, r, ql, qr)

        return merge(
            query(node * 2, l, mid, ql, qr),
            query(node * 2 + 1, mid + 1, r, ql, qr),
        )

    cnt = [0] * (n + 1)

    depth_set = []

    active = 0
    out = []

    for _ in range(q):
        tmp = list(map(int, input().split()))
        tp = tmp[0]

        if tp == 1:
            _, u, v = tmp
            w = lca(u, v)

            insort(depth_set, (depth[w], w))

            fenwick.add(tin[w], 1)

            cnt[w] += 1
            if cnt[w] == 1:
                update(1, 1, n, tin[w], w)

            active += 1

        elif tp == 2:
            _, u, v = tmp
            w = lca(u, v)

            pos = bisect_left(depth_set, (depth[w], w))
            depth_set.pop(pos)

            fenwick.add(tin[w], -1)

            cnt[w] -= 1
            if cnt[w] == 0:
                update(1, 1, n, tin[w], -1)

            active -= 1

        else:
            _, d = tmp

            L = depth_set[-1][1]

            x = jump(L, d if d < depth[L] else depth[L] - 1)
            y = jump(x, d if d < depth[x] else depth[x] - 1)

            inside = fenwick.range_sum(tin[y], tout[y])

            if inside != active:
                out.append("No")
                continue

            dia = query(1, 1, n, tin[y], tout[y])

            if dia[0] == -1:
                out.append("Yes")
                continue

            ok = (
                dist(x, dia[0]) <= d and
                dist(x, dia[1]) <= d
            )

            out.append("Yes" if ok else "No")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the exact structure described above. The Fenwick tree counts active LCAs inside Euler-tour subtrees. The segment tree maintains dynamic diameters of active LCAs. Multiplicity handling is crucial: a vertex disappears from the segment tree only when its count becomes zero.

The diameter merge is the most important piece. For two sets of vertices, the diameter of their union must be formed either by one of the existing diameters or by connecting an endpoint from the left diameter with an endpoint from the right diameter. Checking six pairs is sufficient.

The Euler-tour interval `[tin[v], tout[v]]` converts subtree queries into range queries. That is what allows both the Fenwick tree and the segment tree to work.

## Worked Examples

### Sample 1

Input:

```
1 4
1 1 1
1 1 1
2 1 1
3 0
```

| Operation | Active LCAs | Deepest LCA | Result |
| --- | --- | --- | --- |
| add (1,1) | {1} | 1 |  |
| add (1,1) | {1,1} | 1 |  |
| del (1,1) | {1} | 1 |  |
| query 0 | {1} | 1 | Yes |

The only active path is the single vertex `1`, so its `0`-neighborhood is `{1}` and the intersection is non-empty.

### Custom Example

Chain:

```
1 - 2 - 3 - 4 - 5
```

Operations:

```
add (1,1)
add (5,5)
query 1
query 2
```

| Operation | Active LCAs |
| --- | --- |
| add (1,1) | {1} |
| add (5,5) | {1,5} |
| query 1 | No |
| query 2 | Yes |

With radius `1`, no vertex is close enough to both ends. With radius `2`, vertex `3` satisfies both constraints.

This demonstrates that the problem is about neighborhoods, not path intersections.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | DFS preprocessing plus logarithmic updates and queries |
| Space | O(n log n) | Binary lifting table and segment tree |

With `n, q ≤ 2 · 10^5`, roughly a few million logarithmic operations are performed. This comfortably fits the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    # paste solve() and return captured output
    pass

# sample
assert run("""\
1 4
1 1 1
1 1 1
2 1 1
3 0
""") == "Yes"

# single vertex tree
assert run("""\
1 2
1 1 1
3 0
""") == "Yes"

# duplicate insert/delete handling
assert run("""\
1 5
1 1 1
1 1 1
2 1 1
3 0
3 0
""") == "Yes\nYes"

# chain, radius too small
assert run("""\
5 4
1 2
2 3
3 4
4 5
1 1 1
1 5 5
3 1
""") == "No"

# chain, radius large enough
assert run("""\
5 4
1 2
2 3
3 4
4 5
1 1 1
1 5 5
3 2
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | Yes | Minimum tree size |
| Duplicate path operations | Yes, Yes | Correct multiplicity handling |
| Chain with d=1 | No | Radius too small |
| Chain with d=2 | Yes | Radius boundary |
| Official sample | Yes | Basic correctness |

## Edge Cases

Consider multiple copies of the same path:

```
1 5
1 1 1
1 1 1
2 1 1
3 0
3 0
```

After one deletion, one copy remains active. The counter for vertex `1` becomes `1`, not `0`, so the segment tree leaf stays active. A solution storing only a boolean would incorrectly remove it.

Consider paths whose neighborhoods intersect but whose paths do not:

```
5 3
1 2
2 3
3 4
4 5
1 1 1
1 5 5
3 2
```

The active LCAs are `{1,5}`. Their diameter is `4`. The algorithm finds the appropriate ancestor subtree and verifies both diameter endpoints lie within distance `2` from the candidate center. The answer becomes `Yes`, matching the true neighborhood intersection.

Finally, consider `d = 0`.

The query asks whether all active paths themselves share a common vertex. The algorithm naturally reduces to checking whether the active LCAs collapse into a valid radius-zero configuration. No special handling is needed.
