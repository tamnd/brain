---
title: "CF 125E - MST Company"
description: "We are given a weighted undirected graph whose capital is vertex 1. We must choose a set of roads that connects all cities. Since the chosen graph must be connected and have minimum total weight, the solution will always be a spanning tree whenever a solution exists."
date: "2026-06-02T16:20:28+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "graphs"]
categories: ["algorithms"]
codeforces_contest: 125
codeforces_index: "E"
codeforces_contest_name: "Codeforces Testing Round 2"
rating: 2400
weight: 125
solve_time_s: 147
verified: true
draft: false
---

[CF 125E - MST Company](https://codeforces.com/problemset/problem/125/E)

**Rating:** 2400  
**Tags:** binary search, graphs  
**Solve time:** 2m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted undirected graph whose capital is vertex 1.

We must choose a set of roads that connects all cities. Since the chosen graph must be connected and have minimum total weight, the solution will always be a spanning tree whenever a solution exists.

The extra restriction is that exactly `k` edges of the spanning tree must be incident to the capital.

So the task is:

Find a minimum-weight spanning tree whose degree at vertex `1` is exactly `k`, and output its edge indices.

The graph contains up to 5000 vertices and 100000 edges. A classical minimum spanning tree can be found with Kruskal in `O(m log m)`, which is perfectly fine. The difficult part is enforcing the degree constraint on a single special vertex.

The constraint size immediately rules out anything that enumerates subsets of capital edges. Even checking all possibilities for the degree of vertex 1 would be hopeless because the number of incident edges can be as large as `10^5`.

The key observation is that the restriction affects only one special class of edges, namely those touching vertex 1. That structure is exactly what allows a Lagrangian relaxation, often called WQS binary search in competitive programming.

There are several non-obvious edge cases.

Suppose the graph is disconnected even when all edges are available:

```
3 1 1
1 2 5
```

Vertex 3 is isolated. No spanning tree exists, so the answer is `-1`.

Another important case is when there are too few capital edges.

```
4 2 2
1 2 1
2 3 1
```

Only one edge touches vertex 1, so obtaining degree 2 at the capital is impossible.

A subtler case appears when many spanning trees have the same modified cost during the binary search. If ties are handled incorrectly, the monotonicity of the number of selected capital edges breaks and the reconstruction fails. The implementation must explicitly prefer capital edges among equal modified weights.

## Approaches

The brute-force viewpoint is useful because it exposes what we are really optimizing.

Imagine enumerating all spanning trees. For every tree, count how many edges are incident to vertex 1. Among those with exactly `k` such edges, keep the one with minimum total weight.

This is obviously correct because it directly matches the definition of the answer. Unfortunately a graph with 5000 vertices can have an astronomical number of spanning trees. Even generating them is impossible.

The next natural idea is to run Kruskal while somehow keeping track of how many capital edges are used. That immediately runs into a problem: Kruskal optimizes only total weight and knows nothing about the degree constraint.

The crucial observation is that every capital edge belongs to the same category. Instead of forcing exactly `k` of them, we can temporarily change their weights.

Let `C` be a parameter.

For every edge touching vertex 1, replace its weight by

`w + C`.

All other edges keep their original weight.

Now run a standard MST algorithm on these modified weights.

If `C` is very large, capital edges become expensive and the MST uses few of them.

If `C` is very negative, capital edges become attractive and the MST uses many of them.

This creates a monotone function:

`cnt(C) = number of capital edges in the MST`.

As `C` increases, `cnt(C)` never increases.

That monotonicity allows binary search.

After finding the largest value of `C` for which the MST still contains at least `k` capital edges, we reconstruct a spanning tree with exactly `k` capital edges by running Kruskal once more under the same modified weights and refusing to take more than `k` capital edges.

The reason this works is the standard Lagrangian-relaxation property. At the binary-search boundary, every optimal modified MST corresponds to an optimal original solution with degree constraint `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over spanning trees | Exponential | Exponential | Too slow |
| Binary search + Kruskal | O(log W · m log m) | O(m) | Accepted |

Here `W` is the weight range.

## Algorithm Walkthrough

1. Normalize every edge so that if one endpoint is the capital, it is stored as `(1, x)`.
2. Define a function `count_capital(C)`.

Add `C` to the weight of every capital edge, sort all edges by modified weight, and run Kruskal.

When two edges have the same modified weight, place capital edges first. This maximizes the number of selected capital edges among all optimal modified MSTs.

Return the number of capital edges used.
3. Binary search on `C`.

We need the largest value of `C` such that `count_capital(C) >= k`.

Increasing `C` makes capital edges less attractive, so the predicate is monotone.
4. Let the resulting parameter be `best`.
5. Run Kruskal again using weights modified by `best`.
6. While building the tree, never allow the number of chosen capital edges to exceed `k`.

A non-capital edge is processed normally.

A capital edge is accepted only if:

- it connects two different components, and
- fewer than `k` capital edges have already been chosen.
7. If we fail to obtain exactly `n - 1` edges or fail to reach exactly `k` capital edges, no valid spanning tree exists.
8. Otherwise output the chosen edge indices.

### Why it works

For a fixed parameter `C`, Kruskal finds a minimum spanning tree in the graph whose weights are modified by adding `C` to every capital edge.

Let a tree contain `d` capital edges. Its modified cost is

`original_cost + C * d`.

Binary search finds the largest parameter for which an optimal modified MST still uses at least `k` capital edges.

At this boundary, all trees with degree larger than `k` and all trees with degree smaller than `k` are balanced around the same supporting line of the Lagrangian relaxation. The optimal constrained solution lies among the optimal modified MSTs. By rebuilding the MST and limiting ourselves to exactly `k` capital edges whenever equal-cost choices exist, we obtain one of those optimal constrained trees.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1))

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        self.p[a] = b
        return True

def solve():
    n, m, k = map(int, input().split())

    edges = []

    for idx in range(1, m + 1):
        u, v, w = map(int, input().split())

        if u > v:
            u, v = v, u

        edges.append([u, v, w, idx])

    def count_capital(add):
        arr = []

        for u, v, w, idx in edges:
            if u == 1:
                arr.append((w + add, 0, u, v))
            else:
                arr.append((w, 1, u, v))

        arr.sort()

        dsu = DSU(n)
        cnt = 0
        taken = 0

        for _, typ, u, v in arr:
            if dsu.union(u, v):
                taken += 1
                if typ == 0:
                    cnt += 1
                if taken == n - 1:
                    break

        return cnt

    L = -100000
    R = 100000
    best = None

    while L <= R:
        mid = (L + R) // 2

        if count_capital(mid) >= k:
            best = mid
            L = mid + 1
        else:
            R = mid - 1

    if best is None:
        print(-1)
        return

    arr = []

    for u, v, w, idx in edges:
        if u == 1:
            arr.append((w + best, 0, u, v, idx))
        else:
            arr.append((w, 1, u, v, idx))

    arr.sort()

    dsu = DSU(n)

    answer = []
    capital_used = 0

    for _, typ, u, v, idx in arr:
        if typ == 0 and capital_used == k:
            continue

        if dsu.union(u, v):
            answer.append(idx)

            if typ == 0:
                capital_used += 1

    if len(answer) != n - 1 or capital_used != k:
        print(-1)
        return

    print(n - 1)
    print(*answer)

solve()
```

The first important detail is the sorting order. Capital edges receive type `0` and non-capital edges receive type `1`. Since Python sorts tuples lexicographically, equal modified weights automatically prefer capital edges. Without this tie-breaker the monotonicity used by the binary search can fail.

The binary search looks for the largest parameter whose MST still contains at least `k` capital edges. That exact direction matters. Reversing it changes the reconstruction argument and breaks correctness.

During reconstruction we run Kruskal again under the same modified weights. The only extra rule is that once `k` capital edges have already been chosen, every further capital edge is skipped. This is the step that converts the optimal relaxed solution into an optimal solution satisfying the exact degree requirement.

The DSU implementation uses path compression. Union by rank is unnecessary for these constraints.

## Worked Examples

### Example 1

Input:

```
4 5 2
1 2 1
2 3 1
3 4 1
1 3 3
1 4 2
```

Suppose the binary search has already found the correct parameter.

| Edge considered | Chosen? | Capital edges used | DSU components |
| --- | --- | --- | --- |
| 1-2 | Yes | 1 | merge |
| 2-3 | Yes | 1 | merge |
| 3-4 | Yes | 1 | tree complete |

The unconstrained MST uses only one capital edge.

After applying the optimal parameter and rebuilding:

| Edge considered | Chosen? | Capital edges used |
| --- | --- | --- |
| 1-2 | Yes | 1 |
| 1-4 | Yes | 2 |
| 2-3 | Yes | 2 |

The resulting tree has exactly two capital edges and minimum total weight.

This trace demonstrates why changing the weight of capital edges can force Kruskal toward the required degree.

### Example 2

Input:

```
3 1 1
1 2 5
```

| Step | Result |
| --- | --- |
| Kruskal finishes | only one edge selected |
| Required tree size | 2 edges |
| Connected? | No |

Since a spanning tree cannot be formed, the algorithm outputs `-1`.

This example exercises the connectivity failure path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log W · m log m) | Each binary-search step runs one Kruskal |
| Space | O(m) | Stores all edges and sorting buffers |

The weight range is at most `10^5`, so about 18 binary-search iterations are sufficient. With `m = 100000`, the total work remains comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    # placeholder for local testing
    pass

# sample 1
# verify manually against accepted solution

# minimum graph
inp = """\
1 0 0
"""
# expected: empty spanning tree

# disconnected graph
inp = """\
3 1 1
1 2 5
"""
# expected: -1

# impossible degree
inp = """\
4 2 2
1 2 1
2 3 1
"""
# expected: -1

# boundary degree
inp = """\
3 3 2
1 2 1
1 3 1
2 3 100
"""
# expected tree uses both capital edges
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | Empty tree | Minimum-size instance |
| Disconnected graph | -1 | Connectivity detection |
| Too few capital edges | -1 | Degree infeasibility |
| Degree equals 2 | Valid tree | Exact-degree reconstruction |

## Edge Cases

Consider the disconnected graph:

```
3 1 1
1 2 5
```

Kruskal can select at most one edge. A spanning tree on three vertices requires two edges. During reconstruction the algorithm finishes with fewer than `n - 1` edges and prints `-1`.

Consider insufficient capital edges:

```
4 2 2
1 2 1
2 3 1
```

No matter how negative the binary-search parameter becomes, the graph physically contains only one capital edge. The reconstruction phase cannot reach `capital_used = 2`, so the final validity check rejects the instance.

Consider equal modified weights. Suppose several capital and non-capital edges have identical modified costs. The algorithm always places capital edges first in the ordering. This guarantees that `count_capital(C)` represents the maximum possible number of capital edges among optimal modified MSTs, which is exactly the monotone quantity required by the binary search. Without this tie-breaking rule, different executions of Kruskal could produce different counts for the same parameter, breaking the search.
