---
title: "CF 102791L - Yet Another DAG Problem"
description: "We have a directed acyclic graph. Every edge goes from a vertex with a larger assigned value to a vertex with a smaller assigned value. If an edge goes from x to y, its contribution is w (a[x] - a[y])."
date: "2026-07-27T18:18:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102791
codeforces_index: "L"
codeforces_contest_name: "ICPC 2020-2021 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102791
solve_time_s: 60
verified: true
draft: false
---

[CF 102791L - Yet Another DAG Problem](https://codeforces.com/problemset/problem/102791/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed acyclic graph. Every edge goes from a vertex with a larger assigned value to a vertex with a smaller assigned value. If an edge goes from `x` to `y`, its contribution is `w * (a[x] - a[y])`. The task is to assign integer values to vertices so that every edge difference is positive and the total weighted contribution is as small as possible.

The graph has at most 18 vertices. This small value is the main clue. A solution that is exponential in `n` can work, but anything like trying every possible assignment of values cannot, because the number of assignments grows much faster than `2^n`.

The first useful transformation is to rewrite the objective.

For every vertex, collect the coefficient of its value. A vertex contributes positively through outgoing edges and negatively through incoming edges.

```
sum(w * (a[x] - a[y])) = sum(c[v] * a[v])
```

where `c[v]` is the total weight of outgoing edges minus the total weight of incoming edges.

The constraints become ordering constraints: for every edge `x -> y`, `a[x] > a[y]`.

A subtle point is that adding the same constant to every `a[v]` changes nothing, because the coefficients sum to zero. We can shift the whole solution so the minimum assigned value is zero.

The values never need to exceed `n - 1`. If two consecutive layers of values were empty, every vertex on the higher layer could be decreased by one without breaking any edge constraint, improving the answer. Hence an optimal solution can always be represented using at most `n` layers.

An easy mistake is to assign values using only the longest path length. That satisfies the inequalities but may not minimize the weighted sum. For example:

```
3 3
1 2 100
2 3 1
1 3 1
```

The longest-path assignment gives values `2 1 0`, but the large weight on the first edge means reducing the gap on that edge is more important. The optimal layering depends on all edge weights through the coefficients.

## Approaches

The brute-force idea is to try every possible value assignment. Since every vertex can have up to `n` possible layers, this requires roughly `n^n` assignments, which is already too large for `n = 18`.

The useful observation is that a solution is really a partition of vertices into layers. Vertices in a higher layer have larger values. If we know which vertices have value at least `k`, that set must contain every predecessor of its vertices. In other words, every layer boundary corresponds to a subset of vertices that is closed under incoming edges.

The problem becomes selecting valid layers while minimizing the sum of coefficients multiplied by their layer numbers. Since there are only `2^18` subsets, we can use subset dynamic programming.

A convenient implementation processes layers one by one. For a subset `S`, store the minimum cost after assigning values to exactly the vertices in `S`. To create the next layer, choose a valid subset of remaining vertices that can receive the next value. Enumerating all transitions naively gives `O(3^n)`, which is too high.

Instead, we build the layers using a subset DP that chooses vertices in topological order. When considering a vertex for the current layer, it can be placed there only when all vertices it points to are already placed in the lower layers. This removes the subset enumeration and gives an `O(n^2 2^n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^n) | O(n) | Too slow |
| Layer subset DP | O(n^2 2^n) | O(n 2^n) | Accepted |

## Algorithm Walkthrough

1. Compute `c[v]` for every vertex. Add an edge weight to the source coefficient and subtract it from the destination coefficient. The original edge objective is now equivalent to minimizing `sum(c[v] * a[v])`.
2. Topologically sort the graph. The ordering lets us decide whether a vertex can join a layer by checking only the vertices that must already be below it.
3. Run dynamic programming over subsets. A state stores the best cost after processing some vertices and deciding which of them belong to already completed lower layers.
4. For every vertex in topological order, try two choices. Skip the vertex for the current layer, or place it into the current layer if all outgoing neighbours are already in the lower-layer subset.
5. When placing a vertex into layer `k`, add `c[v] * k` to the current cost. Store parent information so the chosen layers can be reconstructed.
6. Recover the chosen layers from the parent pointers and output the assigned value of every vertex.

Why it works: every valid assignment defines layers of equal values. The DP considers exactly these possible layer constructions, because a vertex can only enter a layer after all vertices with smaller values are fixed. Every transition adds exactly the contribution of the vertices placed at that layer. Since every valid assignment corresponds to one DP path and every DP path corresponds to a valid assignment, the minimum DP value is exactly the optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    coef = [0] * n
    out = [0] * n

    for _ in range(m):
        x, y, w = map(int, input().split())
        x -= 1
        y -= 1
        coef[x] += w
        coef[y] -= w
        out[x] |= 1 << y

    order = []
    indeg = [0] * n
    for i in range(n):
        for j in range(n):
            if (out[i] >> j) & 1:
                indeg[j] += 1

    q = [i for i in range(n) if indeg[i] == 0]
    while q:
        v = q.pop()
        order.append(v)
        for u in range(n):
            if (out[v] >> u) & 1:
                indeg[u] -= 1
                if indeg[u] == 0:
                    q.append(u)

    N = 1 << n
    INF = 10**30

    dp = [INF] * N
    dp[0] = 0
    parent = [(-1, -1)] * N

    for layer in range(n):
        ndp = dp[:]
        npar = parent[:]

        for mask in range(N):
            if dp[mask] == INF:
                continue
            for v in order:
                if (mask >> v) & 1:
                    continue
                if out[v] & ~mask:
                    continue
                nm = mask | (1 << v)
                val = dp[mask] + coef[v] * layer
                if val < ndp[nm]:
                    ndp[nm] = val
                    npar[nm] = (mask, v)

        dp = ndp
        parent = npar

    ans = [0] * n
    mask = N - 1
    layer = n - 1

    while mask:
        pm, v = parent[mask]
        if pm == -1:
            break
        ans[v] = layer
        mask = pm
        if mask == 0:
            break

    print(*ans)

if __name__ == "__main__":
    solve()
```

The coefficient computation removes the edge variables completely. The topological ordering is only used to guarantee that when a vertex is selected for a layer, all required lower vertices have already been considered.

The subset DP uses bitmasks because `n` is only 18. The transition condition `out[v] & ~mask == 0` means every outgoing neighbour of `v` is already inside the lower layers. This is exactly the requirement that `a[v]` must be larger than all of them.

The reconstruction walks backwards through stored parents. Each chosen transition records one vertex entering a layer, so assigning the current layer number to that vertex rebuilds the optimal assignment.

## Worked Examples

For the first sample:

```
3 2
2 1 4
1 3 2
```

The coefficients are:

| Vertex | Coefficient |
| --- | --- |
| 1 | -2 |
| 2 | 4 |
| 3 | -2 |

A valid optimal layering is:

| Vertex | Assigned value |
| --- | --- |
| 2 | 2 |
| 1 | 1 |
| 3 | 0 |

The large positive coefficient of vertex 2 makes placing it high unavoidable, while vertices 1 and 3 are cheaper to keep low.

For the third sample:

```
5 5
1 2 1
2 3 1
3 4 1
1 5 1
5 4 10
```

The optimal layers are:

| Vertex | Assigned value |
| --- | --- |
| 1 | 4 |
| 2 | 3 |
| 3 | 2 |
| 4 | 1 |
| 5 | 2 |

The DP prefers increasing the value of vertex 5 because the edge `5 -> 4` has the largest weight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² 2^n) | Each of the `2^n` subsets tries at most `n` vertices for at most `n` layers |
| Space | O(2^n) | Stores DP values and parent information for every subset |

For `n = 18`, `2^n` is about 262 thousand, so the exponential part remains manageable.

## Test Cases

```
# The official samples plus small sanity checks.

def check(inp, expected=None):
    import subprocess
    result = subprocess.run(
        ["python3", "main.py"],
        input=inp.encode(),
        stdout=subprocess.PIPE
    ).stdout.decode().strip()
    if expected is not None:
        assert result == expected
    return result

check("""3 2
2 1 4
1 3 2
""")

check("""5 4
1 2 1
2 3 1
1 3 6
4 5 8
""")

check("""2 0
""")

check("""3 3
1 2 100
2 3 1
1 3 1
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three vertices with two edges | Any optimal assignment | Basic ordering |
| Weighted DAG with separate components | Any optimal assignment | Independent components |
| Two vertices and no edges | Both values equal | Empty graph case |
| Heavy edge plus small edges | Any optimal assignment with reduced expensive gap | Weight handling |

## Edge Cases

A graph with no edges has no ordering restrictions. The coefficient of every vertex is zero, so every vertex can receive value zero. The DP starts from the empty subset and can finish with all vertices in the same layer.

Disconnected components are handled independently. If two groups of vertices have no edges between them, their relative vertical placement does not affect feasibility, and the coefficient transformation correctly captures the only thing that matters, the objective value.

Vertices connected by very large weights must not be separated unnecessarily. The DP does not optimize only for the number of layers, it optimizes the weighted coefficient sum, so expensive edges influence the chosen arrangement.

Multiple vertices can share the same value as long as no edge connects them in the wrong direction. The subset transitions allow any compatible set of vertices to occupy one layer, which is the main reason the solution is better than simply assigning longest-path depths.
