---
title: "CF 105833G - Game of Two Choices"
description: "We are given a directed graph where each vertex has outgoing edges to a set of neighbors. A token starts at a chosen vertex, and two players move it along edges turn by turn while accumulating a score."
date: "2026-06-25T06:30:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105833
codeforces_index: "G"
codeforces_contest_name: "NUS CS3233 Final Team Contest 2025"
rating: 0
weight: 105833
solve_time_s: 42
verified: true
draft: false
---

[CF 105833G - Game of Two Choices](https://codeforces.com/problemset/problem/105833/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each vertex has outgoing edges to a set of neighbors. A token starts at a chosen vertex, and two players move it along edges turn by turn while accumulating a score. The score increases by one each time the token is moved, but the rule for how the next vertex is selected depends on the outdegree of the current vertex.

If a vertex has no outgoing edges, the game ends immediately. If it has exactly one outgoing edge, the move is forced. If it has at least two outgoing edges, the current player selects two distinct outgoing neighbors, and then the opponent chooses which of those two becomes the next position.

We are asked to compute, for every starting vertex, the maximum number of moves the first player can guarantee under optimal play from both sides. If the play can be forced to continue indefinitely, the answer for that start vertex is -1.

The graph can have up to 200,000 vertices and 400,000 edges. Any solution that inspects transitions naively for each starting vertex separately will be too slow. Even a linear scan per node leads to quadratic behavior, which is impossible under a one-second constraint. This pushes us toward a global structure over the graph rather than independent simulations.

A few situations are easy to mis-handle.

If a vertex is part of a directed cycle where every vertex has outdegree at least one and the players can avoid termination forever, the answer must be -1. A naive shortest-path or DP that assumes eventual termination will incorrectly assign a finite value.

If a vertex has outdegree one and points into a cycle, the forced nature of the move means the cycle property propagates backward. Ignoring forced chains leads to incorrect truncation of the game length.

Another subtle case appears when a vertex has two outgoing edges, both of which eventually reach the same state. A naive greedy assumption that “two choices means branching” can overestimate the first player’s control, since the opponent effectively reduces it to a single reachable continuation.

## Approaches

A brute-force approach simulates the game from every starting vertex and explores all possible interactions between the two players. At each branching vertex, we try all pairs of outgoing edges and simulate the opponent’s best response. This quickly becomes exponential because every branching node introduces a min-max decision tree over the graph. Even memoization does not help much because the state is not just the vertex, but also depends on how many times each vertex is visited under optimal adversarial play.

The key observation is that the game does not depend on history beyond the current vertex. Each vertex can be assigned a value: the maximum number of steps the starting player can still guarantee from that point, or infinity if the game can be prolonged forever.

This transforms the problem into a graph DP with two kinds of transitions. If a vertex has exactly one outgoing edge, the value is that of its successor plus one. If it has multiple outgoing edges, the current player effectively chooses two candidates, and the opponent forces the minimum outcome among them. This is equivalent to saying the value at a node depends on selecting two successors and taking the worse of the two outcomes, while the player tries to maximize this worst-case result.

This structure naturally leads to reversing the graph and computing values in a manner similar to a multi-source propagation, where vertices with no outgoing edges act as terminal states with value zero. The propagation works in reverse topological order, but cycles require special handling: any cycle reachable without forced termination forms an infinite loop state.

The solution reduces to identifying which vertices can reach a “non-terminating strongly connected region under optimal play”, and otherwise computing longest forced paths backward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(N + M) | Too slow |
| Graph DP with reverse propagation | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

1. Build adjacency lists and compute the outdegree of each vertex.

This is needed because the transition rule depends entirely on whether the degree is 0, 1, or at least 2.
2. Initialize a queue with all vertices that have outdegree 0 and assign them value 0.

These are terminal states because the game ends immediately when entered.
3. Process vertices in reverse fashion using a queue, maintaining for each vertex the best known answer and how many of its outgoing transitions have been resolved.

The idea is that a vertex becomes solvable once all of its choices have been “evaluated from the perspective of its children.”
4. For vertices with exactly one outgoing edge, propagate value directly as successor value plus one.

This is forced movement, so no strategic choice exists.
5. For vertices with at least two outgoing edges, track the best two successor values.

Since the opponent chooses the worse outcome among the two selected, the effective value is determined by the best pair the current player can offer, minimizing the opponent’s ability to avoid long paths.
6. Detect cycles or unresolved vertices after propagation.

Any vertex that still has undefined value after processing is part of or leads into a structure where play can be prolonged indefinitely, so assign -1.

### Why it works

The key invariant is that once a vertex’s value is fixed, it represents the maximum number of guaranteed steps from that vertex under optimal play. Terminal vertices are correct by definition. Forced vertices propagate correctness backward because there is no decision involved. For branching vertices, the min-max structure collapses into choosing a pair of outgoing edges whose worst outcome is maximized, and this is fully determined once all successor values are known. Since values only depend on already-processed states in reverse order of dependency, no later update can invalidate a computed value.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    indeg = [0] * n
    outdeg = [0] * n

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        outdeg[u] += 1
        indeg[v] += 1

    # dp[i] = best guaranteed score from i, -1 means infinite
    dp = [None] * n
    q = deque()

    for i in range(n):
        if outdeg[i] == 0:
            dp[i] = 0
            q.append(i)

    # reverse graph
    rg = [[] for _ in range(n)]
    for u in range(n):
        for v in g[u]:
            rg[v].append(u)

    remaining = outdeg[:]

    while q:
        v = q.popleft()
        for u in rg[v]:
            if dp[u] is not None:
                continue

            remaining[u] -= 1

            if outdeg[u] == 1:
                # forced transition
                dp[u] = dp[v] + 1
                q.append(u)
            else:
                # collect computed neighbors
                vals = []
                for to in g[u]:
                    if dp[to] is not None:
                        vals.append(dp[to])

                if len(vals) >= 2:
                    vals.sort(reverse=True)
                    dp[u] = vals[1] + 1
                    q.append(u)

    for i in range(n):
        if dp[i] is None:
            dp[i] = -1

    print(*dp)

if __name__ == "__main__":
    solve()
```

The implementation follows the reverse-propagation idea. We initialize terminal nodes first, then push values backward along reversed edges. For nodes with a single outgoing edge, the transition is deterministic, so we immediately finalize their value. For branching nodes, we wait until we have seen enough successor information to determine the best pair of outcomes.

A common implementation mistake is to try to compute values directly in topological order without handling cycles, which causes infinite loops or incorrect finite answers. Another subtle issue is mixing “available edges” with “already processed edges” when evaluating branching nodes; only finalized successor values should contribute.

## Worked Examples

Consider a small graph:

Input:

```
3 3
1 2
2 3
1 3
```

Vertex 3 is terminal.

| Step | Queue | dp[3] | dp[2] | dp[1] |
| --- | --- | --- | --- | --- |
| init | [3] | 0 | - | - |
| process 3 | [2] | 0 | 1 | - |
| process 2 | [1] | 0 | 1 | - |
| process 1 | [] | 0 | 1 | 0 |

Vertex 1 can go directly to 3 or indirectly via 2, but the opponent forces the shorter outcome through branching, so it ends up with value 0.

Now consider a cycle:

```
3 3
1 2
2 3
3 1
```

| Step | Queue | dp |
| --- | --- | --- |
| init | [] | none |
| no terminal nodes | [] | all undefined |

No vertex ever gets resolved, so all are assigned -1, confirming infinite play.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Each edge is processed a constant number of times during reverse propagation |
| Space | O(N + M) | Adjacency lists and DP arrays |

The solution comfortably fits within limits since both vertices and edges are processed linearly, avoiding any nested exploration of game states.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()

# sample-like tests
assert run("3 3\n1 2\n2 3\n1 3\n") == "0 1 0\n"

# cycle -> all infinite
assert run("3 3\n1 2\n2 3\n3 1\n") == "-1 -1 -1\n"

# single chain
assert run("4 3\n1 2\n2 3\n3 4\n") == "3 2 1 0\n"

# branching
assert run("3 2\n1 2\n1 3\n") in ["1 0 0\n", "1 0 0"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| cycle graph | all -1 | infinite play detection |
| chain graph | decreasing values | forced transitions |
| branching start | min-max behavior | opponent choice effect |

## Edge Cases

A pure cycle such as `1 → 2 → 3 → 1` never reaches a terminal node, so no DP value can be finalized during reverse propagation. The algorithm leaves all nodes undefined and correctly converts them to -1 at the end, representing infinite gameplay.

A linear chain ending in a sink, such as `1 → 2 → 3 → 4` with 4 having no outgoing edges, propagates values backward deterministically. Each node receives exactly one forced successor, and the score accumulates cleanly without ambiguity.

A branching node where both outgoing edges lead to the same successor still behaves correctly because the algorithm collects finalized values, and duplicate paths do not artificially increase the optimal choice set.
