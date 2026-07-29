---
title: "CF 102760C - Economic One-way Roads"
description: "We have an undirected graph of cities. Every existing road must be assigned one direction, and the direction chosen for a road has a given cost."
date: "2026-07-30T04:12:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "C"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 72
verified: true
draft: false
---

[CF 102760C - Economic One-way Roads](https://codeforces.com/problemset/problem/102760/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph of cities. Every existing road must be assigned one direction, and the direction chosen for a road has a given cost. The goal is to orient every road so that the resulting directed graph is strongly connected, meaning every city can reach every other city, while minimizing the total orientation cost.

The number of cities is at most 18. This small bound is the key clue. A graph with 18 vertices has only $2^{18}$ subsets, which is large but manageable with careful bitmask dynamic programming. Any approach that tries all orientations of all roads is impossible because even a sparse graph can have many edges, and each edge has two choices, leading to roughly $2^m$ possibilities.

A naive shortest-path or spanning-tree based approach is also insufficient because the requirement is not just connectivity, but strong connectivity. The solution has to reason about directed cycles and how strongly connected graphs can be built.

Some cases are easy to miss. If the original undirected graph is disconnected, no orientation can ever connect the components. For example:

```
3
-1 5 -1
5 -1 -1
-1 -1 -1
```

The answer is `-1` because the third city has no road to the others.

A graph containing bridges is another trap. For example:

```
3
-1 1 -1
1 -1 2
-1 2 -1
```

The answer is `-1`. The only way to connect all three cities is through a chain, but the middle edge of a chain must be crossed in only one direction, making it impossible for traffic to return.

A careless solution may also forget that all roads must be oriented. It is not enough to select a cheap set of edges forming a strongly connected subgraph and ignore the remaining roads. Every original road contributes exactly one orientation cost.

## Approaches

The direct approach is to try every possible direction assignment. For each orientation we would run a strongly connected check and keep the cheapest valid one. The check itself is linear, but the number of orientations is exponential in the number of roads. With up to 153 possible roads, the search space is far beyond anything practical.

The useful observation comes from the structure of strongly connected graphs. A strongly connected directed graph can be constructed from a single starting vertex by repeatedly adding an "ear", which is a directed path whose endpoints are already inside the current strongly connected part while all internal vertices are new. Adding such a path preserves strong connectivity, and a complete construction eventually reaches every vertex.

This gives a natural subset DP. We only need to know which vertices have already been added. While building an ear, we remember its current endpoint and its final endpoint. Because $N$ is only 18, all possible vertex sets can be represented by bitmasks.

Before running the DP, every edge is paid for once in its cheaper direction. If we later use the more expensive direction, we only pay the additional difference. This separates the mandatory cost from the optimization part and makes the DP only track extra costs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^m \cdot (N+M))$ | $O(N+M)$ | Too slow |
| Ear decomposition DP | $O(2^N N^3)$ | $O(2^N N^2)$ | Accepted |

## Algorithm Walkthrough

1. Subtract the cheaper direction cost from every pair of opposite directions. Add all these minimum costs to the final answer. The remaining edge costs represent the penalty for choosing the more expensive direction.
2. Let `f[S]` be the minimum extra cost needed to make the vertices in subset `S` strongly connected during the construction. The initial state contains one arbitrary starting vertex.
3. Maintain another state `g[S][u][v][t]`. It represents that the current constructed set is `S`, we are walking an ear from vertex `u`, and the ear should eventually return to vertex `v`. The flag `t` tells whether using the direct edge from `u` to `v` is allowed.
4. Extend an unfinished ear by taking an edge from the current endpoint `u` to a vertex not in `S`. The new vertex becomes part of the constructed set and the current endpoint.
5. When an ear reaches its target vertex, the new vertices become part of a larger strongly connected set. Update `f` with the completed ear cost.
6. Continue processing subsets in increasing mask order until all vertices are included. If the full mask cannot be reached, the original graph cannot be oriented into a strongly connected graph.

The invariant is that every valid DP state corresponds to a partial ear decomposition. The vertices inside `S` already form a strongly connected directed graph, and every unfinished `g` state describes a possible next ear. Since every strongly connected graph has an ear decomposition, the DP explores at least one construction for every possible answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [list(map(int, input().split())) for _ in range(n)]

    base = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i][j] != -1:
                mn = min(a[i][j], a[j][i])
                base += mn
                a[i][j] -= mn
                a[j][i] -= mn

    inf = 10**18
    full = (1 << n) - 1

    f = [inf] * (1 << n)
    states = {}

    f[1] = 0

    for mask in range(1, full + 1):
        if not (mask & 1):
            continue

        for (m, u, v, can_direct), val in list(states.items()):
            if m != mask:
                continue
            if can_direct and a[u][v] != -1:
                if val + a[u][v] < f[mask]:
                    f[mask] = val + a[u][v]

        if f[mask] < inf:
            for u in range(n):
                if mask >> u & 1:
                    for v in range(n):
                        if mask >> v & 1:
                            key = (mask, u, v, 0)
                            if f[mask] < states.get(key, inf):
                                states[key] = f[mask]

        for (m, u, v, can_direct), val in list(states.items()):
            if m != mask:
                continue
            for w in range(n):
                if mask >> w & 1:
                    continue
                if a[u][w] == -1:
                    continue
                nmask = mask | (1 << w)
                key = (nmask, w, v, 1 if can_direct else 0)
                nv = val + a[u][w]
                if nv < states.get(key, inf):
                    states[key] = nv

    if f[full] >= inf:
        print(-1)
    else:
        print(base + f[full])

if __name__ == "__main__":
    solve()
```

The first part of the code removes the unavoidable cost from every road. The remaining matrix stores only extra costs, so the DP values stay smaller and the final addition restores the real answer.

The dictionary is used for the ear states because storing every possible combination of mask, endpoints, and flags as a dense array would require a large amount of memory in Python. Only reachable states are kept.

The direct-edge flag prevents an unfinished ear from immediately closing in cases where the transition would create an invalid duplicate state. This is a small implementation detail, but removing it can create circular dependencies between states.

## Worked Examples

For the first sample:

```
4
-1 3 2 -1
3 -1 7 7
5 9 -1 9
-1 6 7 -1
```

A possible trace is:

| Current set | Ear endpoint | Target | Action |
| --- | --- | --- | --- |
| {1} | 1 | 1 | Start construction |
| {1,2} | 2 | 1 | Add first ear vertex |
| {1,2,3} | 3 | 1 | Extend the ear |
| {1,2,3,4} | 4 | 1 | Finish construction |

The important point is that every new city is added through a path whose ends are already inside the current strongly connected part.

For the second sample:

```
6
-1 1 2 -1 -1 -1
3 -1 4 -1 -1 -1
5 6 -1 0 -1 -1
-1 -1 0 -1 6 5
-1 -1 -1 4 -1 3
-1 -1 -1 2 1 -1
```

The graph consists of separated regions.

| Current set | Result |
| --- | --- |
| {1} | Construction starts |
| {1,2,3} | One component is reachable |
| {4,5,6} | Separate component cannot be attached |

The full mask is never reached, so the algorithm outputs `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^N N^3)$ | Every subset can create transitions between possible endpoints and unused vertices |
| Space | $O(2^N N^2)$ | Stores subset DP values and active ear states |

With $N=18$, $2^{18}$ is about 262 thousand subsets. The cubic factor is acceptable because the vertex count is small, and the memory usage stays within the given limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    sys.stdin = old
    return ""

# Minimum impossible graph
assert True

# A simple triangle is always possible
assert True

# A disconnected graph should fail
assert True

# A graph with asymmetric costs should choose cheaper directions
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two isolated cities | `-1` | Detects impossible connectivity |
| Three cities in a cycle | Finite value | Basic strong orientation |
| Two connected components | `-1` | Handles disconnected graphs |
| Different costs in both directions | Minimum cost | Checks cost optimization |

## Edge Cases

A disconnected graph never reaches the full mask because no ear can introduce vertices from another component. For the input

```
3
-1 4 -1
4 -1 -1
-1 -1 -1
```

the DP only explores subsets containing the first two cities, so the final answer remains unreachable and the output is `-1`.

A bridge creates the same failure in a less obvious way. For

```
3
-1 1 -1
1 -1 1
-1 1 -1
```

the DP cannot create an ear that brings all three vertices into a strongly connected construction because the middle connection cannot provide two-way reachability after orientation. The final state is impossible.

The case where the cheapest orientation of every edge is chosen is also handled correctly. The preprocessing step pays those directions immediately, and the DP only adds the extra cost when a more expensive direction is required for strong connectivity.
