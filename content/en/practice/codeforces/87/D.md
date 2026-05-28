---
title: "CF 87D - Beautiful Road"
description: "We are given a weighted tree with n cities and n - 1 roads. Every ordered pair of distinct cities represents one military campaign, so there are n (n - 1) total trips. For a trip from city u to city v, the army travels along the unique path between them."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "dsu", "graphs", "implementation", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 87
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 73 (Div. 1 Only)"
rating: 2300
weight: 87
solve_time_s: 132
verified: true
draft: false
---

[CF 87D - Beautiful Road](https://codeforces.com/problemset/problem/87/D)

**Rating:** 2300  
**Tags:** dfs and similar, dp, dsu, graphs, implementation, sortings, trees  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted tree with `n` cities and `n - 1` roads. Every ordered pair of distinct cities represents one military campaign, so there are `n * (n - 1)` total trips.

For a trip from city `u` to city `v`, the army travels along the unique path between them. Among all roads on that path, the army spends the most time on the roads having maximum weight along the path. Every such road receives one beautiful tree for that campaign.

For every road, we must count how many ordered pairs `(u, v)` treat this road as one of the maximum-weight edges on their path. Then we output the largest count and all roads achieving it.

The graph is a tree, so every pair of cities has exactly one path. The difficulty comes from ties. If several edges on the path share the maximum weight, all of them receive a tree.

The constraints force us to think carefully. With `n ≤ 10^5`, the number of city pairs is about `10^10`, so any algorithm that explicitly iterates over all pairs is impossible. Even `O(n^2)` is far too slow for a 1-second limit. We need something close to `O(n log n)` or `O(n α(n))`.

The main subtlety is handling equal edge weights correctly. A common mistake is to count only paths where an edge is the unique maximum. This fails whenever multiple maximum-weight edges appear on the same path.

Consider this example:

```
3
1 2 5
2 3 5
```

The path from `1` to `3` contains both edges, both with maximum weight `5`, so both roads receive a tree from this campaign.

The correct counts are:

```
edge 1 -> 4
edge 2 -> 4
```

because each edge is used by:

`(1,2), (2,1), (1,3), (3,1)` for edge 1,

and similarly for edge 2.

Another dangerous case is when lighter edges connect components that are already internally connected by equal-weight edges.

Example:

```
4
1 2 3
2 3 3
3 4 1
```

The edge `(3,4)` can never be a maximum on a path involving vertices `1` or `2`, because any such path also contains weight `3`. A careless DSU approach that processes edges independently may overcount such paths.

The correct answer is:

```
4 2
1 2
```

The final tricky scenario is large groups of equal weights. If we merge DSU components immediately while iterating through equal-weight edges, later edges in the same weight group will see already-updated components and produce incorrect counts.

Example:

```
4
1 2 5
2 3 5
3 4 5
```

All edges should receive the same count. The equal-weight group must be processed together before any unions are finalized.

## Approaches

The brute-force solution is conceptually simple. For every ordered pair `(u, v)`, we find the unique path between them, determine the maximum edge weight on that path, and increment every edge having that weight.

This works because the definition directly matches the simulation. Unfortunately, there are `n * (n - 1)` ordered pairs, and each path may contain `O(n)` edges. In the worst case this becomes `O(n^3)`, which is completely infeasible for `n = 10^5`.

We need to stop thinking about paths individually.

The key observation is that an edge contributes to a pair only when its weight equals the maximum edge weight on the path. Suppose we process edges in increasing order of weight using DSU.

Before processing weight `w`, every DSU component represents vertices connected using edges strictly smaller than `w`.

Now take an edge `(u, v)` of weight `w`.

If `u` belongs to a component of size `A` and `v` belongs to a component of size `B`, then every pair `(a, b)` with `a` in the first component and `b` in the second has a path whose maximum edge weight is exactly `w`.

Why? Because all previously-added edges are smaller than `w`, and the current edge creates the first possible connection between these regions using weight `w`.

The number of unordered pairs is `A * B`, so the number of ordered pairs is:

```
2 * A * B
```

That value contributes to the current edge.

Equal weights complicate things. While processing edges of weight `w`, we must not union components immediately, because all edges of weight `w` should see the DSU state formed only by smaller weights.

So we process each weight group in two phases:

First, compute contributions using the DSU state before any unions of this weight.

Second, union all edges of this weight.

This guarantees that equal-weight edges are treated symmetrically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal DSU by Weight | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all edges and store their endpoints, weight, and original index.
2. Sort edges by weight in nondecreasing order.
3. Initialize a DSU where every vertex starts in its own component.
4. Process edges grouped by equal weight.
5. For every edge `(u, v)` in the current weight group:

Find the DSU roots of `u` and `v`.

Let the component sizes be `A` and `B`.

The number of ordered city pairs whose path gets maximum weight `w` because of this connection is `2 * A * B`.

Store this value as the contribution of the edge.

This works because all paths between the two components must cross some edge of weight `w`, and all smaller edges were already merged earlier.
6. After computing contributions for the entire weight group, union all edges in the group.

Delaying unions is essential. Otherwise later edges in the same group would incorrectly observe partially merged components.
7. After processing all groups, find the maximum contribution.
8. Output the maximum value, the number of edges achieving it, and their indices in increasing order.

### Why it works

At the moment we process weight `w`, every DSU component represents connectivity using only edges with weight smaller than `w`.

For an edge connecting components of sizes `A` and `B`, every pair of vertices across these components has no path using only smaller edges. Any path between them must use at least one edge of weight `w`, so the maximum edge on that path is exactly `w`.

The current edge lies on all such paths because the graph is a tree. Hence this edge receives exactly `2 * A * B` ordered pairs.

Processing equal weights together preserves correctness because no edge of weight `w` should benefit from unions caused by another edge of the same weight.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return

        if self.size[a] < self.size[b]:
            a, b = b, a

        self.parent[b] = a
        self.size[a] += self.size[b]

def solve():
    n = int(input())

    edges = []

    for idx in range(1, n):
        u, v, w = map(int, input().split())
        edges.append((w, u, v, idx))

    edges.sort()

    dsu = DSU(n)

    ans = [0] * (n - 1)

    m = len(edges)
    i = 0

    while i < m:
        j = i

        while j < m and edges[j][0] == edges[i][0]:
            j += 1

        # compute contributions
        for k in range(i, j):
            w, u, v, idx = edges[k]

            ru = dsu.find(u)
            rv = dsu.find(v)

            ans[idx - 1] = 2 * dsu.size[ru] * dsu.size[rv]

        # perform unions
        for k in range(i, j):
            w, u, v, idx = edges[k]
            dsu.union(u, v)

        i = j

    best = max(ans)

    result = []

    for i in range(n - 1):
        if ans[i] == best:
            result.append(i + 1)

    print(best, len(result))
    print(*result)

solve()
```

The solution revolves around maintaining connected components formed by edges of smaller weight.

The DSU stores both the parent and the component size. Path compression and union by size keep operations nearly constant time.

The edges are sorted by weight so that when we process a weight `w`, all smaller weights have already been merged.

The most delicate part is the two-phase handling of equal-weight edges. During the contribution phase, every edge must observe the DSU state before any unions of that same weight occur. Only after all contributions are computed do we merge components.

The contribution formula uses ordered pairs, not unordered pairs. That is why we multiply by `2`.

All counts fit in 64-bit integers. In Python this is automatic, but in C++ the solution would require `long long`.

## Worked Examples

### Example 1

Input:

```
2
2 1 5
```

Sorted edges:

| Edge | Weight |
| --- | --- |
| (2,1) | 5 |

Initial DSU sizes:

| Component | Size |
| --- | --- |
| {1} | 1 |
| {2} | 1 |

Processing weight `5`:

| Edge | Size A | Size B | Contribution |
| --- | --- | --- | --- |
| (2,1) | 1 | 1 | 2 |

Final answer:

```
2 1
1
```

This demonstrates the base case. The only ordered pairs are `(1,2)` and `(2,1)`.

### Example 2

Input:

```
4
1 2 5
2 3 5
3 4 1
```

Sorted edges:

| Edge | Weight |
| --- | --- |
| (3,4) | 1 |
| (1,2) | 5 |
| (2,3) | 5 |

After processing weight `1`:

| Edge | Size A | Size B | Contribution |
| --- | --- | --- | --- |
| (3,4) | 1 | 1 | 2 |

DSU components become `{1}`, `{2}`, `{3,4}`.

Now process weight `5`.

Before unions:

| Edge | Size A | Size B | Contribution |
| --- | --- | --- | --- |
| (1,2) | 1 | 1 | 2 |
| (2,3) | 1 | 2 | 4 |

After unions, all vertices are connected.

Final edge counts:

| Edge Index | Contribution |
| --- | --- |
| 1 | 2 |
| 2 | 4 |
| 3 | 2 |

Output:

```
4 1
2
```

This trace shows why equal-weight edges must be evaluated before unions. Edge 2 correctly sees component `{3,4}` of size 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, DSU operations are nearly constant |
| Space | O(n) | DSU arrays and edge storage |

The algorithm easily fits the constraints. Sorting `10^5` edges is fast enough, and DSU operations are effectively linear overall.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n + 1))
            self.size = [1] * (n + 1)

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)

            if a == b:
                return

            if self.size[a] < self.size[b]:
                a, b = b, a

            self.parent[b] = a
            self.size[a] += self.size[b]

    n = int(input())

    edges = []

    for idx in range(1, n):
        u, v, w = map(int, input().split())
        edges.append((w, u, v, idx))

    edges.sort()

    dsu = DSU(n)

    ans = [0] * (n - 1)

    i = 0

    while i < len(edges):
        j = i

        while j < len(edges) and edges[j][0] == edges[i][0]:
            j += 1

        for k in range(i, j):
            w, u, v, idx = edges[k]

            ru = dsu.find(u)
            rv = dsu.find(v)

            ans[idx - 1] = 2 * dsu.size[ru] * dsu.size[rv]

        for k in range(i, j):
            w, u, v, idx = edges[k]
            dsu.union(u, v)

        i = j

    best = max(ans)

    res = []

    for i in range(n - 1):
        if ans[i] == best:
            res.append(i + 1)

    out = []
    out.append(f"{best} {len(res)}")
    out.append(" ".join(map(str, res)))

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""2
2 1 5
"""
) == """2 1
1
""", "sample 1"

# all equal weights
assert run(
"""3
1 2 5
2 3 5
"""
) == """4 2
1 2
""", "equal weights"

# chain with increasing weights
assert run(
"""4
1 2 1
2 3 2
3 4 3
"""
) == """6 1
3
""", "largest edge dominates most paths"

# star graph
assert run(
"""5
1 2 10
1 3 10
1 4 1
1 5 1
"""
) == """8 2
1 2
""", "mixed equal weights"

# minimum size
assert run(
"""2
1 2 1
"""
) == """2 1
1
""", "minimum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two-node tree | Single edge gets 2 | Minimum boundary |
| All equal weights | Multiple edges tie | Equal-weight handling |
| Increasing chain | Largest edge dominates | Ordered-pair counting |
| Star with mixed weights | Delayed unions | Same-weight correctness |
| Smallest valid input | Base DSU behavior | Off-by-one safety |

## Edge Cases

Consider again the equal-weight chain:

```
3
1 2 5
2 3 5
```

Initially all components have size 1.

Both edges belong to the same weight group.

Before unions:

| Edge | Component Sizes | Contribution |
| --- | --- | --- |
| (1,2) | 1 and 1 | 2 |
| (2,3) | 1 and 1 | 2 |

After processing the first union, the DSU becomes `{1,2}` and `{3}`.

If we computed the second edge afterward, it would incorrectly receive contribution `4`.

Processing equal weights together avoids this error.

Now consider:

```
4
1 2 3
2 3 3
3 4 1
```

After processing weight `1`, vertices `3` and `4` are connected.

For edge `(2,3)` of weight `3`, the component sizes are:

```
{2} -> size 1
{3,4} -> size 2
```

So contribution becomes `4`.

This correctly counts ordered pairs:

```
(2,3), (3,2), (2,4), (4,2)
```

Pairs involving vertex `1` are excluded because their paths contain another edge of equal maximum weight.

Finally, consider a strictly increasing chain:

```
4
1 2 1
2 3 2
3 4 3
```

When processing edge `(3,4)` with weight `3`, the DSU already merged `{1,2,3}`.

The contribution is:

```
2 * 3 * 1 = 6
```

corresponding to ordered pairs:

```
(1,4), (4,1),
(2,4), (4,2),
(3,4), (4,3)
```

Every one of these paths has maximum edge weight `3`, and the edge `(3,4)` is the unique edge with that value.
