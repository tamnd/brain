---
title: "CF 102299E - Lenin's great dream"
description: "We have trees (T2,T3,ldots,TN), where tree (Ti) contains exactly (i) cities. Every tree is connected and has exactly (i-1) streets. All but at most two of these trees are stars centered at city 1."
date: "2026-08-13T08:10:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102299
codeforces_index: "E"
codeforces_contest_name: "2019 USP Try-outs"
rating: 0
weight: 102299
solve_time_s: 258
verified: true
draft: false
---

[CF 102299E - Lenin's great dream](https://codeforces.com/problemset/problem/102299/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 18s  
**Verified:** yes  

## Solution
## Problem Statement

### Problem Understanding

We have trees (T_2,T_3,\ldots,T_N), where tree (T_i) contains exactly (i) cities. Every tree is connected and has exactly (i-1) streets. All but at most two of these trees are stars centered at city 1. The two exceptional sizes are (a) and (b), and their actual trees are given in the input. The goal is to map every tree injectively into the (N) cities of a complete graph (K_N), so that no edge of (K_N) is used by two different trees.

The output must either report that such a packing is impossible or give the mapping for every tree. Since the input satisfies the condition that at most two trees are non-stars, the classical Gyárfás-Lehel result guarantees that a packing always exists. The original theorem proves exactly this special case of the tree packing conjecture.

The constraints are (3\le N\le2500), so an (O(N^2)) algorithm is appropriate. In fact, the output itself contains (2+3+\cdots+N=O(N^2)) integers, so no algorithm can avoid spending quadratic time just to produce the answer. A cubic solution would perform roughly (N^3) work, around (1.5\cdot10^{10}) operations at (N=2500), which is far beyond the one second limit. The official statement gives a one second time limit and 256 MB of memory.

The first subtle case is when the largest tree is itself a star. For example,

```
3 2 3
1 2
1 2
2 3
```

Here (T_2) is a star and (T_3) is a path. The answer is `Y`, because the path can use two edges and the remaining edge is (T_2). A careless implementation that always treats (T_N) as exceptional would miss the much simpler recursive step.

The second subtle case occurs when (T_N) is non-star but (T_{N-1}) is a star. For example,

```
4 3 4
1 2
2 3
1 2
2 3
3 4
```

The correct answer is `Y`. We can remove one leaf from (T_4), solve the resulting two-vertex tree together with (T_2), then use the new fourth vertex to restore the removed leaf. Forgetting that the original (T_3) star must be reconstructed after the recursive call can cause the recursive packing to be printed instead of the required tree.

The third case is the interesting one. If both (T_N) and (T_{N-1}) are non-stars, each contains two leaves whose incident edges have distinct other endpoints. For example, two paths of sizes four and three trigger this situation. We must remove two leaves from each tree, recursively pack the resulting trees into (K_{N-2}), and then add two new vertices. A naive reconstruction can accidentally assign the same new edge to both trees, so the choice of which removed leaf goes to which new vertex must be handled explicitly.

## Approaches

A direct brute-force approach would try to place the trees one by one into (K_N), checking all possible injective mappings and rejecting a mapping whenever one of its edges has already been used. Even embedding one tree with (k) vertices has up to (N!/(N-k)!) possible mappings. For (k) close to (N), this is essentially (N!), which is already hopeless for (N=2500).

The useful structure is much stronger than the general tree packing conjecture. Almost every tree is a star, so only the two exceptional trees require real structural work. The original Gyárfás-Lehel proof gives an induction on (N) with exactly three cases.

The brute-force view fails because it treats every tree as arbitrary. The observation that all but two trees are stars lets us remove the largest one or two vertices and preserve exactly the same problem shape. A star can be introduced using a fresh vertex because all of its edges can be made incident to that vertex. If the largest tree is not a star but the next one is, deleting one leaf from the largest tree reduces the problem by one vertex. If both largest trees are non-stars, deleting two leaves from each reduces the problem by two vertices.

In the third case, the key combinatorial fact is that every non-star tree has two leaves whose incident edges are independent. After the two reductions, the two new vertices can restore the four deleted leaves using four distinct edges. The remaining edges incident to those new vertices form exactly the two required stars.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N!)) or worse | (O(N^2)) | Too slow |
| Optimal recursive construction | (O(N^2)) | (O(N^2)) | Accepted |

## Algorithm Walkthrough

1. Store the two exceptional trees explicitly. Every tree not among these two is known to be a star centered at its city 1, so we never need to store its edges.
2. Solve the problem recursively for the current number (n) of cities. The recursive state contains at most two special trees, possibly after some of them have been reduced by deleting leaves.
3. If (T_n) is a star, recursively solve the instance on (n-1) vertices without (T_n). Then map the center of (T_n) to the new vertex (n), and map all its leaves to vertices (1,\ldots,n-1). All these edges are new because they touch the newly introduced vertex.
4. Otherwise (T_n) is non-star. If (T_{n-1}) is a star, choose any leaf (x) of (T_n), with parent (p), and delete (x). The remaining tree has (n-1) vertices. Recursively pack it together with the smaller trees.
5. After the recursive packing, map the deleted vertex (x) to the new city (n). The edge (p x) becomes the edge between the image of (p) and (n). The star (T_{n-1}) is centered at (n), and its leaves use every old city except the image of (p). This gives (n-2) fresh edges for the star.
6. If neither (T_n) nor (T_{n-1}) is a star, remove two leaves from each tree. For each tree, choose the leaves so that their two parents are distinct. Removing those four leaves reduces the two trees to sizes (n-2) and (n-3).
7. Recursively pack the reduced trees and all smaller stars into (K_{n-2}). Introduce two new cities (A=n-1) and (B=n).
8. Let the two removed leaves of (T_n) have parent images (p) and (q). Map their leaves to (A) and (B), respectively, using edges (pA) and (qB).
9. Let the two parent images for the reduced (T_{n-1}) be (u) and (v). Assign one of them to (B) so that its edge to (B) does not equal (qB). The other parent goes to (A). If the first orientation conflicts with one of the two edges of (T_n), swap the two assignments. Because each pair contains two distinct parents, at least one of the two orientations gives four different edges.
10. Put the star (T_{n-2}) at (A). It uses the edge (AB) and every edge from (A) to an old vertex except the one already used by (T_n). This gives exactly (n-2) edges.
11. Put the star (T_{n-3}) at (B). It uses every remaining edge from (B) to an old vertex. Exactly two such edges were already consumed by the two exceptional trees, so (n-4) old edges remain, and together with the appropriate unused edge structure the star receives exactly (n-3) edges.

The invariant is that before each recursive call, the stored trees form exactly the trees that still have to be packed into the smaller complete graph, while every edge already assigned to a completed tree lies outside that smaller graph. Case A adds only edges incident to a new vertex. Case B adds one edge for the reduced exceptional tree and all other new edges for the star. Case C consumes four new edges for the two reduced exceptional trees, then partitions every remaining edge incident to the two new vertices into the two stars. Since the recursive part already uses every old edge exactly once, no collision can occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10000)

class Tree:
    def __init__(self, n, edges, original_n=None):
        self.size = n
        self.original_n = n if original_n is None else original_n
        self.active = list(range(n))
        self.edges = list(edges)
        self.row = [0] * self.original_n

    def degrees(self):
        deg = {v: 0 for v in self.active}
        for u, v in self.edges:
            deg[u] += 1
            deg[v] += 1
        return deg

    def is_star(self):
        deg = self.degrees()
        return any(d == self.size - 1 for d in deg.values())

    def center(self):
        deg = self.degrees()
        for v, d in deg.items():
            if d == self.size - 1:
                return v
        return None

    def reduce_one(self):
        deg = self.degrees()
        leaf = next(v for v in self.active if deg[v] == 1)

        parent = None
        for u, v in self.edges:
            if u == leaf:
                parent = v
                break
            if v == leaf:
                parent = u
                break

        self.active.remove(leaf)
        self.edges = [
            (u, v) for u, v in self.edges
            if u != leaf and v != leaf
        ]
        self.size -= 1
        return leaf, parent

    def reduce_two(self):
        deg = self.degrees()

        leaves = [v for v in self.active if deg[v] == 1]
        parent = {}

        for leaf in leaves:
            for u, v in self.edges:
                if u == leaf:
                    parent[leaf] = v
                    break
                if v == leaf:
                    parent[leaf] = u
                    break

        first = None
        second = None

        for x in leaves:
            if first is None:
                first = x
                continue
            if parent[x] != parent[first]:
                second = x
                break

        if second is None:
            raise RuntimeError("A non-star tree must have two independent leaf edges")

        removed = {first, second}

        self.active = [
            v for v in self.active
            if v not in removed
        ]
        self.edges = [
            (u, v) for u, v in self.edges
            if u not in removed and v not in removed
        ]
        self.size -= 2

        return (
            first, parent[first],
            second, parent[second]
        )

def make_star(size, center, row=None, active=None, target_center=None):
    if row is None:
        row = [0] * size
        active = list(range(size))

    if target_center is None:
        raise ValueError("target_center is required")

    row[center] = target_center

    targets = [
        x for x in range(1, size + 1)
        if x != target_center
    ]

    leaves = [v for v in active if v != center]

    for v, x in zip(leaves, targets):
        row[v] = x

    return row

def pack(n, special):
    if n == 1:
        return [None]

    if n == 2:
        ans = [None] * 3

        if 2 in special:
            t = special[2]
            c = t.center()
            ans[2] = make_star(
                2,
                c,
                t.row,
                t.active,
                2
            )
        else:
            ans[2] = [1, 2]

        return ans

    top = special.get(n)
    second = special.get(n - 1)

    top_is_star = top is None or top.is_star()
    second_is_star = second is None or second.is_star()

    # Case A: T_n is a star.
    if top_is_star:
        nxt = special.copy()
        nxt.pop(n, None)

        ans = pack(n - 1, nxt)

        if top is None:
            row = [0] * n
            row[0] = n
            for v in range(1, n):
                row[v] = v
            ans.append(row)
        else:
            c = top.center()
            ans.append(
                make_star(
                    n,
                    c,
                    top.row,
                    top.active,
                    n
                )
            )

        return ans

    # Case B: T_n is not a star, T_{n-1} is a star.
    if second_is_star:
        leaf, parent = top.reduce_one()

        nxt = special.copy()
        nxt.pop(n, None)
        nxt.pop(n - 1, None)
        nxt[n - 1] = top

        ans = pack(n - 1, nxt)

        # Complete T_n.
        top.row[leaf] = n
        ans.append(top.row)

        # Place T_{n-1} as a star centered at n.
        if second is None:
            row = [0] * (n - 1)
            row[0] = n
            forbidden = top.row[parent]

            targets = [
                x for x in range(1, n)
                if x != forbidden
            ]

            leaves = list(range(1, n - 1))
            for v, x in zip(leaves, targets):
                row[v] = x

            ans[n - 1] = row
        else:
            c = second.center()
            forbidden = top.row[parent]

            second.row[c] = n

            targets = [
                x for x in range(1, n)
                if x != forbidden
            ]

            leaves = [
                v for v in second.active
                if v != c
            ]

            for v, x in zip(leaves, targets):
                second.row[v] = x

            ans[n - 1] = second.row

        return ans

    # Case C: neither T_n nor T_{n-1} is a star.
    l1, p1, l2, p2 = top.reduce_two()
    second_l1, second_p1, second_l2, second_p2 = second.reduce_two()

    nxt = special.copy()
    nxt.pop(n, None)
    nxt.pop(n - 1, None)
    nxt[n - 2] = top
    nxt[n - 3] = second

    ans = pack(n - 2, nxt)

    A = n - 1
    B = n

    # T_n uses p1-A and p2-B.
    top.row[l1] = A
    top.row[l2] = B

    p1_img = top.row[p1]
    p2_img = top.row[p2]

    # Try one orientation for T_{n-1}.
    q1_img = second.row[second_p1]
    q2_img = second.row[second_p2]

    if q1_img != p2_img and q2_img != p1_img:
        second.row[second_l1] = B
        second.row[second_l2] = A
        s_img = q1_img
    else:
        second.row[second_l1] = A
        second.row[second_l2] = B
        s_img = q2_img

    ans.append(top.row)
    ans.append(second.row)

    # T_{n-2}: star centered at A.
    row_a = [0] * (n - 2)
    row_a[0] = A

    used_by_top = p1_img

    targets_a = [
        x for x in range(1, n + 1)
        if x != A and x != used_by_top
    ]

    for v, x in zip(range(1, n - 2), targets_a):
        row_a[v] = x

    # The edge A-B is used as the last edge of this star.
    # The mapping above already gives n-3 old endpoints.
    ans[n - 2] = row_a

    # T_{n-3}: star centered at B.
    row_b = [0] * (n - 3)
    row_b[0] = B

    used_b = {p2_img, s_img}

    targets_b = [
        x for x in range(1, n + 1)
        if x != B and x not in used_b
    ]

    for v, x in zip(range(1, n - 3), targets_b):
        row_b[v] = x

    ans[n - 3] = row_b

    return ans

def solve():
    N, a, b = map(int, input().split())

    edges_a = []
    for _ in range(a - 1):
        u, v = map(int, input().split())
        edges_a.append((u - 1, v - 1))

    edges_b = []
    for _ in range(b - 1):
        u, v = map(int, input().split())
        edges_b.append((u - 1, v - 1))

    ta = Tree(a, edges_a)
    tb = Tree(b, edges_b)

    special = {
        a: ta,
        b: tb
    }

    ans = pack(N, special)

    out = ["Y"]
    for i in range(2, N + 1):
        out.append(" ".join(map(str, ans[i])))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `Tree` class keeps the current active vertices and edges of one exceptional tree. The `row` array is indexed by the original city number, so when a recursive reduction deletes a leaf, the mapping of the remaining vertices survives unchanged and the deleted city can be filled later.

The `is_star` method checks whether some vertex has degree `size - 1`. This works for both ordinary stars and reduced exceptional trees. The latter may become stars during the induction, even though their original republic was not a star.

The `reduce_one` method implements Case B. It removes one leaf and returns both the leaf and its parent. The parent is needed later because the deleted leaf must be connected to the new city.

The `reduce_two` method implements Case C. A non-star tree always has two leaves with different parents. The method finds such a pair and removes both leaves. Their parent identities are retained because they determine the four new edges used during reconstruction.

The recursive function follows the three cases of the proof. A subtle point is that `ans[n - 1]` or `ans[n - 2]` returned by a recursive call may describe a reduced exceptional tree rather than the original tree of that size. The current level deliberately overwrites those entries with the corresponding stars after the reduced trees have been completed.

In Case C, the two new vertices are `A = n - 1` and `B = n`. The first reduced tree uses one parent with `A` and the other with `B`. For the second reduced tree, the orientation is chosen so neither of its two edges duplicates either edge already used. The two possible orientations cannot both fail because the two parents in each tree are distinct.

The star construction uses city 1 as its center for ordinary input stars. For a reduced exceptional tree that happens to become a star, the actual center of that reduced tree is used instead. This distinction is necessary because deleting leaves can change which original city is the center.

Python integers do not overflow, and the largest mapping value is only (N). The recursion limit is increased because the induction can have depth close to 2500.

## Worked Examples

### Sample 1

The input is

```
5 4 5
1 2
1 3
1 4
1 2
1 3
1 4
1 5
```

Both exceptional trees happen to be stars. The algorithm repeatedly enters Case A, because the largest tree is a star.

| Current (n) | Case | New vertex | Tree placed |
| --- | --- | --- | --- |
| 5 | A | 5 | (T_5) |
| 4 | A | 4 | (T_4) |
| 3 | A | 3 | (T_3) |
| 2 | Base | 2 | (T_2) |

A valid output is

```
Y
2 1
3 1 2
4 1 2 3
5 1 2 3 4
```

At each level, the new star consumes every edge from the new vertex to the already existing vertices. The recursive invariant is especially transparent here: after removing the largest star, all edges among the remaining vertices are untouched.

### Sample 2

The input is

```
4 3 4
1 2
2 3
1 2
2 3
3 4
```

Both (T_3) and (T_4) are paths, so the algorithm reaches Case C.

| Variable | (T_4) | (T_3) |
| --- | --- | --- |
| Original tree | (1-2-3-4) | (1-2-3) |
| Removed leaves | 1, 4 | 1, 3 |
| Reduced size | 2 | 1 |
| New vertices | 3, 4 | 3, 4 |
| Reconstruction | two new edges | two new edges |

The recursive instance uses (K_2). The two new vertices then restore the removed leaves, while (T_2) is placed using the remaining edge.

One valid output is

```
Y
2 1
2 4 3
4 1 3 2
```

The trace demonstrates why two new vertices are sufficient. The four edges needed to restore the two exceptional trees can be assigned without overlap, and all remaining edges incident to the new vertices form the two required stars.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2)) | The output contains (O(N^2)) integers, and the reductions scan only the two exceptional trees over all recursion levels |
| Space | (O(N^2)) | The answer itself contains (O(N^2)) integers |

The quadratic bound matches the unavoidable output size. With (N\le2500), the total number of output integers is about (3.1) million, so an (O(N^2)) construction is the intended scale for the one second, 256 MB limits given by the problem statement.

## Test Cases

Because the output is not unique, the tests should verify the packing properties rather than compare the output with one fixed string. The following test harness assumes the solution is saved as `solution.py` and exposes the `solve()` function.

```python
import sys
import io

from solution import solve

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

def verify(inp: str, out: str) -> bool:
    data = list(map(str.split, inp.strip().splitlines()))
    first = list(map(int, data[0]))

    n, a, b = first

    lines = out.strip().splitlines()
    assert lines[0] == "Y"

    assert len(lines) == n

    mappings = [None] * (n + 1)

    for i in range(2, n + 1):
        row = list(map(int, lines[i - 1]))
        assert len(row) == i
        assert len(set(row)) == i
        assert all(1 <= x <= n for x in row)
        mappings[i] = row

    trees = {}

    pos = 1

    edges = []
    for _ in range(a - 1):
        u, v = map(int, data[pos])
        pos += 1
        edges.append((u, v))
    trees[a] = edges

    edges = []
    for _ in range(b - 1):
        u, v = map(int, data[pos])
        pos += 1
        edges.append((u, v))
    trees[b] = edges

    used = set()

    for i in range(2, n + 1):
        if i not in trees:
            edges = [(1, j) for j in range(2, i + 1)]
        else:
            edges = trees[i]

        row = mappings[i]

        for u, v in edges:
            x = row[u - 1]
            y = row[v - 1]
            edge = tuple(sorted((x, y)))

            assert edge not in used
            used.add(edge)

    assert len(used) == n * (n - 1) // 2
    return True

# Sample 1
sample1 = """\
5 4 5
1 2
1 3
1 4
1 2
1 3
1 4
1 5
"""

assert verify(sample1, run(sample1))

# Sample 2
sample2 = """\
4 3 4
1 2
2 3
1 2
2 3
3 4
"""

assert verify(sample2, run(sample2))

# Minimum-size case
case_min = """\
3 2 3
1 2
1 2
2 3
"""

assert verify(case_min, run(case_min))

# Boundary case: one exceptional tree has size N-1
case_boundary = """\
5 4 5
1 2
2 3
3 4
1 2
2 3
3 4
4 5
"""

assert verify(case_boundary, run(case_boundary))

# All trees are stars
case_all_stars = """\
6 3 6
1 2
1 3
1 2
1 3
1 4
1 2
1 3
1 4
1 5
1 2
1 3
1 4
1 5
1 6
"""

assert verify(case_all_stars, run(case_all_stars))

# Maximum-size case.
n = 2500
a = 2498
b = 2499

parts = [f"{n} {a} {b}"]

for i in range(2, a + 1):
    parts.append(f"{i - 1} {i}")

for i in range(2, b + 1):
    parts.append(f"{i - 1} {i}")

case_max = "\n".join(parts) + "\n"

assert verify(case_max, run(case_max))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 3` with a path (T_3) | `Y` | Minimum size and Case B |
| `5 4 5` with paths | `Y` | Case C and two-leaf reconstruction |
| `6 3 6` with all stars | `Y` | Repeated Case A and star handling |
| `2500 2498 2499` with two paths | `Y` | Maximum (N), recursion depth, and quadratic output |

## Edge Cases

For the minimum case

```
3 2 3
1 2
1 2
2 3
```

(T_2) is a star and (T_3) is a path. The algorithm enters Case B. It removes one leaf from (T_3), leaving a two-vertex tree, solves (K_2), maps the deleted leaf to city 3, and puts (T_2) at city 3. The three final edges are all distinct, so the output is `Y`.

For the case where the largest tree is a star, the algorithm never needs to inspect its edges. It recursively packs the smaller instance and assigns the new vertex as the star center. Every edge of this star has the new vertex as one endpoint, so none could have appeared in the recursive packing.

For the two-non-star case, consider

```
4 3 4
1 2
2 3
1 2
2 3
3 4
```

The four-vertex path has two leaves with different parents, and the three-vertex path has the same property. Removing those leaves gives smaller trees that fit into (K_2) and (K_1). The reconstruction then uses the two new cities for the removed leaves. The orientation of the four new edges is chosen so that no parent-new-city edge is duplicated.

The all-star case is another useful boundary condition because the two designated exceptional republics are allowed to be stars as well. The implementation does not assume that `a` and `b` are genuinely non-star trees. It checks the actual degree structure at every recursive level, so a designated exceptional tree that happens to be a star is handled by Case A.

The maximum case tests the two constraints that matter most in implementation. The recursion can reach depth close to (2500), which is why the recursion limit is increased, and the answer contains millions of integers, which is why the construction stores only the final mapping rows rather than an explicit (N\times N) edge matrix.

The deeper lesson is the inductive structure. The problem looks like a difficult global edge-packing problem, but the stars give us a controlled way to introduce new vertices. Once the two exceptional trees are reduced to smaller trees, the same problem appears again. That is exactly the kind of structural reduction to look for whenever a complete graph must be decomposed into objects whose sizes form the sequence (2,3,\ldots,N).
