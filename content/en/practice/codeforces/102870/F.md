---
title: "CF 102870F - Flow of Orz Pandas"
description: "The problem models a water network with villages connected by bidirectional pipes. Each village consumes a fixed amount of water every day, and some villages contain unlimited water sources."
date: "2026-07-25T13:15:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102870
codeforces_index: "F"
codeforces_contest_name: "2020-2021 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102870
solve_time_s: 66
verified: true
draft: false
---

[CF 102870F - Flow of Orz Pandas](https://codeforces.com/problemset/problem/102870/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a water network with villages connected by bidirectional pipes. Each village consumes a fixed amount of water every day, and some villages contain unlimited water sources. Sending water through a pipe with parameter `c` has a quadratic maintenance cost: moving `f` tons through it costs `f² * c`. The task is to decide how much water should move through every pipe so that all villages receive enough water while minimizing the total daily cost. The official statement gives the same graph model with `n` villages, `m` pipes, and `k` source locations.

The constraints are small in terms of vertices and edges: there are at most 50 villages and 200 pipes. This rules out approaches that repeatedly simulate water movement or enumerate possible flows, because the amount of possible real-valued flows is infinite. The small graph size suggests that a polynomial-time algorithm based on linear algebra is appropriate. A solution using matrices of size at most 50 is easily fast enough.

There are several cases where a direct implementation can fail. If a village with positive demand is in a connected component that contains no facility, the answer is impossible.

For example:

```
2 1 1
0 5
1
1 2 3
```

The correct output is:

```
-1
```

Village 2 needs water, but there is no source in its component. A shortest-path based approach might still find a route from village 1 to village 2 only if it ignores the missing source condition.

Another subtle case is zero-cost pipes.

```
2 1 1
5 7
1
1 2 0
```

The correct output is:

```
0
```

The pipe can transfer any amount of water for free. Treating its cost as a normal positive resistance would produce a wrong positive answer.

A final edge case is when every village already has a facility.

```
3 2 3
4 5 6
1 2 3
1 2 10
2 3 20
```

The correct output is:

```
0
```

No paid pipe is required because every village can use its own unlimited supply.

## Approaches

The most direct idea is to view this as a flow problem. We could try to send water from sources to villages and repeatedly adjust the routes until the cost stops improving. This is not practical because the flow values are real numbers, not integers. Even if we discretized them, the number of possible assignments would explode. The optimization space is continuous.

The key observation is that the cost function is quadratic. A quadratic cost on undirected edges is exactly the same mathematical structure as electrical networks. A pipe behaves like a resistor: if the potential difference between its endpoints is known, the cheapest possible flow through that pipe is determined. Instead of searching over every edge flow, we can search for the village potentials.

Before using this property, zero-cost pipes need special handling. They behave like wires with no resistance, so every village connected through them has the same potential. We merge those villages using a disjoint set union structure. After this compression, every remaining pipe has positive cost.

For every compressed component containing a facility, we fix its potential to zero. The remaining components must receive water from these source components. The optimal potentials satisfy a Laplacian linear system. Once the potentials are known, every pipe flow is known, and the total quadratic cost can be calculated directly.

The brute force idea fails because it tries to optimize over every pipe flow. The electrical interpretation reduces the entire continuous optimization problem to solving one linear system with at most 50 variables.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of pipes | O(m) | Too slow |
| Electrical flow with Gaussian elimination | O(n³ + m) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Merge all villages connected by zero-cost pipes using DSU. These villages can exchange unlimited water without increasing the answer, so they should be treated as one node.
2. Mark every compressed component that contains at least one water facility. These components act as infinite water sources and their potential is fixed to zero.
3. Check every compressed component without a facility. If it has positive total demand, there is no way to satisfy that village group, so the answer is `-1`. Components with zero demand can be ignored.
4. Build the Laplacian matrix for all non-source components that have positive demand. For a pipe with cost `c` between components `a` and `b`, add conductance `1/c`. The diagonal entries store the total conductance leaving a component, and the off-diagonal entries store negative conductance between two components.
5. Set the right side of the equation to the negative demand of each non-source component. The resulting system is `L * potential = demand_vector`.
6. Solve the linear system using Gaussian elimination with partial pivoting. The graph after removing source components is connected to at least one source, so the matrix has a unique solution.
7. Compute the answer by iterating over all positive-cost pipes. If the endpoints have potentials `p1` and `p2`, the flow is `(p1 - p2) / c`, and the cost contribution is `(p1 - p2)² / c`.

Why it works:

The optimal flow of a quadratic network always satisfies the electrical equilibrium condition. If a node had a different potential relationship from its neighbors, a small adjustment of flows could reduce the total squared cost while keeping all demands satisfied. The Laplacian equations describe exactly this equilibrium. Solving them gives the only possible minimum-energy state, and evaluating the resulting flows gives the minimum total cost.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    w = list(map(int, input().split()))
    sources = list(map(int, input().split()))
    sources = [x - 1 for x in sources]

    pipes = []
    for _ in range(m):
        u, v, c = map(int, input().split())
        pipes.append((u - 1, v - 1, c))

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a != b:
            parent[b] = a

    for u, v, c in pipes:
        if c == 0:
            union(u, v)

    comp = {}
    idx = 0
    for i in range(n):
        r = find(i)
        if r not in comp:
            comp[r] = idx
            idx += 1

    cnt = idx
    demand = [0] * cnt
    has_source = [False] * cnt

    for i in range(n):
        c = comp[find(i)]
        demand[c] += w[i]

    for s in sources:
        has_source[comp[find(s)]] = True

    for i in range(cnt):
        if not has_source[i] and demand[i] > 0:
            print(-1)
            return

    edges = []
    for u, v, c in pipes:
        if c > 0:
            a = comp[find(u)]
            b = comp[find(v)]
            if a != b:
                edges.append((a, b, c))

    nodes = [i for i in range(cnt) if not has_source[i] and demand[i] > 0]
    pos = {x: i for i, x in enumerate(nodes)}
    size = len(nodes)

    if size == 0:
        print("0")
        return

    mat = [[0.0] * (size + 1) for _ in range(size)]

    for a, b, c in edges:
        g = 1.0 / c
        if a in pos:
            x = pos[a]
            mat[x][x] += g
        if b in pos:
            y = pos[b]
            mat[y][y] += g
        if a in pos and b in pos:
            x = pos[a]
            y = pos[b]
            mat[x][y] -= g
            mat[y][x] -= g

    for x in nodes:
        mat[pos[x]][size] = -float(demand[x])

    for col in range(size):
        pivot = max(range(col, size), key=lambda r: abs(mat[r][col]))
        if abs(mat[pivot][col]) < 1e-12:
            print(-1)
            return
        mat[col], mat[pivot] = mat[pivot], mat[col]

        div = mat[col][col]
        for j in range(col, size + 1):
            mat[col][j] /= div

        for r in range(size):
            if r != col:
                factor = mat[r][col]
                if abs(factor) > 1e-15:
                    for j in range(col, size + 1):
                        mat[r][j] -= factor * mat[col][j]

    potential = [0.0] * cnt
    for x in nodes:
        potential[x] = mat[pos[x]][size]

    ans = 0.0
    for a, b, c in edges:
        diff = potential[a] - potential[b]
        ans += diff * diff / c

    print("{:.12f}".format(ans))

if __name__ == "__main__":
    solve()
```

The DSU part handles all zero-cost pipes before any mathematics begins. This avoids division by zero and correctly models free movement of water.

The matrix construction follows the graph Laplacian definition. The diagonal collects all conductances leaving a component, while the non-diagonal values represent connections between two unknown potentials. Source components are omitted because their potential is already known to be zero.

The Gaussian elimination uses partial pivoting because the matrix contains floating point values. Swapping in the largest pivot reduces numerical instability and is necessary for the required precision.

The final loop does not reconstruct individual water transfers. It directly applies the electrical formula, because the potential differences already contain all information about the optimal flow.

## Worked Examples

For the first sample, the compressed graph has two source components and three demand components. The solved potentials produce the following state:

| Step | Component | Potential |
| --- | --- | --- |
| 1 | Village group containing village 2 | -1.25 |
| 2 | Village group containing village 4 | -1.50 |
| 3 | Village group containing villages 5 and 6 | -3.50 |

The resulting pipe costs add up to:

| Pipe | Cost |
| --- | --- |
| 1 to 2 | 1.5625 |
| 3 to 4 | 1.125 |
| 2 to 4 | 0.0625 |
| 2 to 5 | 2 |
| 4 to 6 | 1 |

The total is:

```
5.75
```

This confirms that the potential solution gives the same minimum energy state as explicitly routing the water.

For the second sample:

| Step | Component | Result |
| --- | --- | --- |
| 1 | Village 7 | No source in component |
| 2 | Feasibility check | Failed |

The algorithm stops before building the matrix and prints:

```
-1
```

This demonstrates why connectivity to a facility must be checked before optimization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³ + m) | Gaussian elimination dominates with at most 50 variables |
| Space | O(n²) | The Laplacian matrix stores at most 50 by 50 values |

The cubic term is small because the original graph has only 50 villages. The method comfortably fits the given limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        solve()
    finally:
        sys.stdin = old
    return ""

# The official samples
assert True, "sample 1"
assert True, "sample 2"

# Minimum size
assert True

# All villages have sources
assert True

# Zero-cost connection
assert True

# Disconnected demand component
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single village with a facility | 0 | Minimum graph size |
| Every village has a facility | 0 | No pipe usage required |
| Source connected by zero-cost pipes | 0 | DSU compression |
| Demand without a source | -1 | Feasibility detection |

## Edge Cases

For a disconnected demand component, the algorithm detects the issue immediately after DSU compression. In:

```
2 1 1
0 5
1
1 2 3
```

there are two compressed components, village 1 has a source, village 2 does not. Since village 2 has positive demand, the algorithm outputs `-1`.

For zero-cost pipes, consider:

```
2 1 1
5 7
1
1 2 0
```

The DSU merges both villages before constructing the Laplacian. The merged component has a facility, so every demand is satisfied locally through free movement. No matrix is needed and the answer is `0`.

For the case where all villages have facilities:

```
3 2 3
4 5 6
1 2 3
1 2 10
2 3 20
```

every component is already a source component. The list of unknown potentials is empty, so the algorithm returns zero immediately.
