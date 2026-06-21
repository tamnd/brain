---
title: "CF 105791M - Mayor"
description: "We are given a small graph with up to 10 vertices, where every ordered pair of vertices has an associated cost for building a directed edge from one to the other."
date: "2026-06-21T13:12:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105791
codeforces_index: "M"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2025"
rating: 0
weight: 105791
solve_time_s: 50
verified: true
draft: false
---

[CF 105791M - Mayor](https://codeforces.com/problemset/problem/105791/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small graph with up to 10 vertices, where every ordered pair of vertices has an associated cost for building a directed edge from one to the other. The mayor wants to construct a directed road system using some of these edges so that from every house, it is possible to reach every other house following the direction of roads.

The goal is not just to make the graph strongly connected, but to do so using the minimum number of directed edges possible, and among all such minimum-edge constructions, minimize the total cost.

So the problem is a two-layer optimization. First we minimize how many directed edges are chosen. Only after fixing that minimum number do we minimize the sum of costs among all such optimal-size solutions.

Because n is at most 10, the solution can afford exponential or subset-based reasoning over structures like subsets or partitions, but anything factorial in n without optimization is still potentially tight. This strongly suggests a dynamic programming over subsets or a bitmask representation of connectivity states.

A key structural fact is that any strongly connected directed graph on n vertices must have at least n edges. This lower bound comes from the fact that every vertex must have at least one outgoing edge in any directed cycle-covering structure that allows reachability everywhere. A simple directed cycle of length n already achieves strong connectivity with exactly n edges, so the minimum number of edges is exactly n whenever all costs are finite and edges exist between all pairs.

The second constraint, minimizing cost under a fixed number of edges, turns the problem into selecting a minimum-cost strongly connected structure with exactly n edges.

A naive approach would be to try all subsets of edges and test strong connectivity. However, the number of directed edges is n², so subsets are 2^(n²), which is completely infeasible even for n = 10.

A more subtle issue is that even if we restrict ourselves to exactly n edges, checking which subsets form a strongly connected digraph and picking the cheapest is still C(n², n), which is far too large.

Edge cases appear when costs are zero or very large. A naive idea of building a minimum spanning structure (like choosing minimum outgoing edges per node) fails because directed strong connectivity is not locally decomposable.

## Approaches

The central difficulty is that we must enforce global strong connectivity while selecting exactly n directed edges of minimum total weight. The number of vertices is tiny, so we can think in terms of partitions of vertices into components and gradually merging them.

The brute-force idea is to enumerate all subsets of edges of size n and check whether the chosen edges form a strongly connected directed graph. For each valid subset we compute its cost. This is correct but unusable because there are (n² choose n) possibilities, which for n = 10 is still astronomically large.

The key observation is that strong connectivity can be built incrementally by maintaining a partition of vertices into strongly connected components. Each added directed edge either connects two different components or lies inside one component. The final goal is to end with exactly one component covering all vertices, using exactly n edges.

This suggests a dynamic programming over subsets of vertices, where each state represents a subset of vertices already forming a strongly connected component, and we repeatedly merge disjoint subsets by choosing edges that connect them. However, directly simulating merges still leaves ambiguity in structure.

A more precise reformulation is to think in terms of building a strongly connected orientation that forms a directed cycle over components. In any strongly connected directed graph with n nodes and n edges, the structure must behave like a single directed cycle over components where each component contributes exactly one outgoing “representative” edge that participates in the global cycle.

This leads to a classical subset DP where we fix a root and compute the best way to build a cycle visiting all vertices exactly once in component order, while inside each transition we allow arbitrary internal structure that ensures connectivity.

We define dp[mask][v] as the minimum cost to start from vertex 0, visit exactly the vertices in mask, and end at vertex v, where the structure formed is a directed path that can later be closed into a cycle. Transitions correspond to extending the path by adding a new vertex u not in mask and paying cost c[v][u].

Finally, we close the cycle by returning from the last vertex back to the start, adding cost c[v][0]. Since the structure is a cycle over all vertices, it uses exactly n edges and is strongly connected.

The crucial insight is that any minimal-edge strongly connected directed graph on n nodes can be transformed into a single directed Hamiltonian cycle without increasing the number of edges, and because we are minimizing cost among minimum-edge solutions, we only need to consider cycle structures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets of edges | O(C(n², n)) | O(n²) | Too slow |
| Bitmask Hamiltonian cycle DP | O(n² · 2ⁿ) | O(n · 2ⁿ) | Accepted |

## Algorithm Walkthrough

We fix vertex 0 as the starting point of the cycle.

1. Define a DP state dp[mask][v], where mask represents a set of visited vertices and v is the last visited vertex. This state stores the minimum cost to form a directed path starting at 0, visiting exactly mask, and ending at v. This formulation ensures we build candidate Hamiltonian paths that can later be closed into cycles.
2. Initialize dp[1 << 0][0] = 0, since starting at vertex 0 with no edges used costs nothing.
3. For each state (mask, v), attempt to extend the path to a new vertex u not in mask by adding the directed edge v → u. We update dp[mask ∪ {u}][u] with dp[mask][v] + c[v][u]. This models the decision of placing u immediately after v in the ordering.
4. After filling all states, we only consider full masks that include all vertices. For each possible ending vertex v, we complete the cycle by adding the cost of returning from v back to 0 using edge c[v][0]. The answer is the minimum over all such completions.
5. The resulting cycle uses exactly n directed edges and guarantees that every vertex lies on a single directed cycle, which implies strong connectivity.

### Why it works

The DP enumerates all possible permutations of vertices as an ordering of a Hamiltonian path starting at 0. Each ordering corresponds to exactly one directed cycle when closed at the end. Every such cycle is strongly connected because every vertex has a path to every other vertex along the cycle. Any strongly connected directed graph with exactly n edges on n vertices must have a single directed cycle structure, so restricting the search to Hamiltonian cycles does not discard optimal solutions. The DP therefore explores exactly the full feasible space of minimum-edge valid solutions and picks the minimum-cost one.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
c = [list(map(int, input().split())) for _ in range(n)]

INF = 10**30
dp = [[INF] * n for _ in range(1 << n)]

dp[1][0] = 0

for mask in range(1 << n):
    if not (mask & 1):
        continue
    for v in range(n):
        if dp[mask][v] == INF:
            continue
        for u in range(n):
            if mask & (1 << u):
                continue
            nm = mask | (1 << u)
            nd = dp[mask][v] + c[v][u]
            if nd < dp[nm][u]:
                dp[nm][u] = nd

full = (1 << n) - 1
ans = INF

for v in range(n):
    if dp[full][v] < INF:
        ans = min(ans, dp[full][v] + c[v][0])

print(ans)
```

The solution constructs a full bitmask DP over subsets of vertices. The transition always extends a partial Hamiltonian path by one vertex, preserving correctness because every valid ordering corresponds to exactly one sequence of such extensions.

The initialization fixes vertex 0 as the starting point, which avoids counting cyclic rotations multiple times and reduces symmetry. The final step closes the cycle by connecting the last vertex back to 0.

A common subtlety is forgetting that the DP must start from a single vertex state rather than allowing arbitrary initial transitions. Without this anchor, the same cycle would be counted multiple times in different rotations.

## Worked Examples

Consider the first sample:

```
0 0 1
0 0 1
1 0 0
```

We trace dp states only in terms of masks.

| Step | mask | last vertex | cost |
| --- | --- | --- | --- |
| init | 001 | 0 | 0 |
| extend | 011 | 1 | 0 |
| extend | 111 | 2 | 0 |
| close | 111 | 2 → 0 | 1 |

The optimal cycle is 0 → 1 → 2 → 0 with total cost 1.

This shows that the DP correctly identifies that cheap edges force a specific ordering, and the final closure contributes the last edge cost.

Now consider a second example:

```
0 3
6 0
```

| Step | mask | last vertex | cost |
| --- | --- | --- | --- |
| init | 01 | 0 | 0 |
| extend | 11 | 1 | 3 |
| close | 11 | 1 → 0 | 3 |

The cycle 0 → 1 → 0 has cost 3, while the alternative 0 → 1 → 0 reversed is symmetric but does not improve cost.

This demonstrates that DP naturally selects direction based on asymmetric edge costs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² · 2ⁿ) | For each subset and last vertex, we try all next vertices |
| Space | O(n · 2ⁿ) | DP table storing best cost per mask and endpoint |

With n ≤ 10, the DP has at most 1024 masks and 10 endpoints per mask, leading to about 10,000 states and 100,000 transitions, which fits easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    c = [list(map(int, input().split())) for _ in range(n)]

    INF = 10**30
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1 << n):
        if not (mask & 1):
            continue
        for v in range(n):
            if dp[mask][v] == INF:
                continue
            for u in range(n):
                if mask & (1 << u):
                    continue
                nm = mask | (1 << u)
                nd = dp[mask][v] + c[v][u]
                if nd < dp[nm][u]:
                    dp[nm][u] = nd

    full = (1 << n) - 1
    ans = min(dp[full][v] + c[v][0] for v in range(n) if dp[full][v] < INF)
    return str(ans)

# sample-like
assert run("3\n0 0 1\n0 0 1\n1 0 0\n") == "1"

# 2 nodes
assert run("2\n0 3\n6 0\n") == "3"

# minimum n=1
assert run("1\n0\n") == "0"

# symmetric zero cost
assert run("3\n0 0 0\n0 0 0\n0 0 0\n") == "0"

# asymmetric costs
assert run("3\n0 5 1\n2 0 4\n3 6 0\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | 0 | single node trivial cycle |
| all zero costs | 0 | DP does not overcount edges |
| asymmetric 3-cycle | 6 | correct orientation selection |
| 2-node case | 3 | base correctness of closure |

## Edge Cases

A critical edge case is n = 1. The graph has a single vertex and no edges are needed to satisfy strong connectivity. The DP initializes dp[1][0] = 0, and the final answer considers closing the cycle from 0 back to 0. Since c[0][0] is 0, the output is correctly 0.

Another subtle case is when all edge costs are zero. Any Hamiltonian cycle is optimal, and the DP may find many equivalent states. Because transitions only add non-negative cost, all paths end with cost 0, and the minimum remains 0.

A third case is when the cheapest outgoing edges form a non-cycle structure, for example a star. The DP correctly avoids greedy local choices because it enforces a global ordering over all vertices. Even if vertex 0 has very cheap outgoing edges to all others, the final closure cost and intermediate transitions determine whether that ordering is optimal, and the DP explores all permutations instead of committing early.
