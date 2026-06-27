---
title: "CF 105013K - Going to Find Your Love"
description: "The task can be understood as a shortest path problem on a directed weighted graph, but with an extra layer of state tracking. Each node in the graph can be visited multiple times depending on how many special “bad” nodes have been passed so far."
date: "2026-06-28T02:14:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105013
codeforces_index: "K"
codeforces_contest_name: "The 19th Southeast University Programming Contest (Summer)"
rating: 0
weight: 105013
solve_time_s: 48
verified: true
draft: false
---

[CF 105013K - Going to Find Your Love](https://codeforces.com/problemset/problem/105013/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The task can be understood as a shortest path problem on a directed weighted graph, but with an extra layer of state tracking. Each node in the graph can be visited multiple times depending on how many special “bad” nodes have been passed so far. When we traverse a normal node, our state does not change. When we traverse a bad node, we consume one unit of a limited resource, and this affects how many future bad nodes we are still allowed to pass through.

Formally, we are not just interested in the cheapest cost to reach each node, but in the cheapest cost to reach each pair consisting of a node and a count of how many bad nodes have already been used. The output requires, for every node, the minimum cost among all valid states.

The input describes a weighted directed graph with up to one hundred thousand nodes and edges, plus a small constraint k that bounds how many bad nodes we are allowed to pass through. A subset of nodes are marked as bad, and each time we enter one, we consume one unit of this allowance.

The output is a list of shortest reachable costs for each node, or -1 if no valid path exists under the constraint.

The constraints immediately rule out any approach that recomputes shortest paths independently per node or per state. A naive shortest path per state would explode to something like O(nk log n) or worse depending on implementation details, so we must treat the problem as a single unified shortest path over an expanded state space.

A subtle edge case appears when k = 0. In this case, any path that touches a bad node becomes invalid, so only paths through safe nodes matter. Another corner case is when the destination itself is bad; we still must allow entering it if we have remaining quota exactly at the moment of entry.

## Approaches

A direct approach is to treat each query “what is the cost to reach node v after using i bad nodes” as a separate distance state and run a multi-state shortest path. This leads naturally to defining a dynamic programming table where dist[u][i] is the minimum cost to reach node u after having used i bad nodes.

From a graph perspective, this is equivalent to constructing a layered graph with k+1 copies of each node. Each original edge u → v of weight w becomes transitions between layers depending on whether v is bad. If v is not bad, the layer index stays the same. If v is bad, the layer index increases by one. The goal is then a shortest path from (1, 0) in this expanded graph.

This formulation is correct but still needs an efficient way to compute shortest paths. The brute-force method would repeatedly relax edges across all states without prioritization, which degenerates into something similar to SPFA over a graph of size n·k with up to m·k transitions. In the worst case, this can become too slow due to repeated reprocessing of states.

The key observation is that this expanded graph has non-negative edge weights, so we can safely apply Dijkstra’s algorithm on the state graph. Each state is a node in a larger graph, and each transition is a weighted edge. Once seen this way, the problem becomes a standard single-source shortest path problem.

The SPFA version in the statement and the Dijkstra version differ only in implementation choice: SPFA tries to relax dynamically, while Dijkstra enforces order using a priority queue, preventing repeated unnecessary relaxations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over states (uncontrolled relaxation) | O(n · k · m) worst case | O(n · k) | Too slow |
| SPFA on state graph | O(n · k · m) worst case | O(n · k) | Risky / borderline |
| Dijkstra on state graph | O((n · k + m · k) log(n · k)) | O(n · k + m · k) | Accepted |

## Algorithm Walkthrough

We convert the original graph into a state-expanded graph where each node u has k+1 versions representing how many bad nodes have been used so far upon reaching u.

We then run Dijkstra from the initial state.

1. Construct a mapping from each pair (node u, used_bad i) to a unique index in the state graph. This allows us to treat each state as a normal node in a shortest path algorithm.
2. For every original edge u → v with weight w, we add transitions between states. If v is a bad node, then from state (u, i) we can go to (v, i+1) as long as i+1 ≤ k. If v is not bad, we go to (v, i). This encodes the constraint directly into graph structure.
3. Initialize all distances in the state graph to infinity, except the starting state (1, 0), which is set to zero.
4. Push the starting state into a priority queue. This ensures that we always expand the currently cheapest reachable state first.
5. Repeatedly extract the state with minimum distance. If it has already been processed, skip it. Otherwise, relax all outgoing transitions to neighboring states, updating their distances if a shorter path is found.
6. After the algorithm finishes, for each original node u, take the minimum distance over all states (u, i) for i from 0 to k. This gives the best possible cost to reach u under any valid usage of bad nodes.

Why it works is tied to a simple invariant: whenever we pop a state (u, i) from the priority queue, we have already found the minimum possible cost to reach that exact configuration. Because all transitions have non-negative weights, any future improvement would require a strictly cheaper path to the same state, which contradicts the ordering property enforced by the priority queue. This guarantees that once a state is finalized, it never needs to be revisited.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m, p, k = map(int, input().split())
    bad = [False] * (n + 1)

    for _ in range(p):
        x = int(input())
        bad[x] = True

    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        g[u].append((v, w))

    INF = 10**18
    dist = [[INF] * (k + 1) for _ in range(n + 1)]
    dist[1][0] = 0

    pq = [(0, 1, 0)]

    while pq:
        d, u, used = heapq.heappop(pq)
        if d != dist[u][used]:
            continue

        for v, w in g[u]:
            if bad[v]:
                if used < k and dist[v][used + 1] > d + w:
                    dist[v][used + 1] = d + w
                    heapq.heappush(pq, (dist[v][used + 1], v, used + 1))
            else:
                if dist[v][used] > d + w:
                    dist[v][used] = d + w
                    heapq.heappush(pq, (dist[v][used], v, used))

    for i in range(1, n + 1):
        ans = min(dist[i])
        print(-1 if ans == INF else ans, end=" ")

if __name__ == "__main__":
    solve()
```

The solution directly implements Dijkstra on a layered state space. The distance table stores the best known cost for each (node, used_bad) pair. The priority queue always expands the most promising state, and stale entries are ignored by comparing against the current best distance.

The key implementation detail is the separation between transitions depending on whether the next node is bad. That condition determines whether the second dimension of the state increases. Another important detail is taking the minimum over all layers at the end, since reaching a node with fewer or more used bad nodes can both be optimal depending on the path structure.

## Worked Examples

Consider a small graph with three nodes where node 2 is bad, and we are allowed k = 1 bad node. Edges are 1 → 2 (cost 5), 2 → 3 (cost 2), and 1 → 3 (cost 10).

We track states as (node, used_bad).

Initial state is (1, 0) with distance 0.

| Step | State popped | Distance | Update action |
| --- | --- | --- | --- |
| 1 | (1,0) | 0 | Relax 1→2 gives (2,1)=5, relax 1→3 gives (3,0)=10 |
| 2 | (2,1) | 5 | Relax 2→3 gives (3,1)=7 |
| 3 | (3,0) | 10 | No improvements |
| 4 | (3,1) | 7 | No improvements |

Final answer for node 3 is min(10, 7) = 7.

This shows how using the bad-node allowance can enable a longer but cheaper route.

Now consider k = 0 on the same graph. Any path entering node 2 is invalid.

| Step | State popped | Distance | Update action |
| --- | --- | --- | --- |
| 1 | (1,0) | 0 | Only 1→3 is allowed, so (3,0)=10 |
| 2 | (3,0) | 10 | Done |

Now node 3 is only reachable via the direct edge, confirming how the constraint blocks intermediate nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n · k + m · k) log(n · k)) | Each state is processed once with Dijkstra, and each edge creates up to k transitions |
| Space | O(n · k + m · k) | Distance table plus adjacency over expanded state graph |

The value of k is small in typical constraints, making the state expansion feasible. The logarithmic factor from the priority queue keeps the solution comfortably within limits even for n up to 100000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like small graph
assert run("""3 3 1 1
2
1 2 5
2 3 2
1 3 10
""") == "0 5 7", "basic case"

# k = 0 blocks bad node
assert run("""3 3 1 0
2
1 2 5
2 3 2
1 3 10
""") == "0 -1 10", "no bad allowed"

# single node
assert run("""1 0 0 0
""") == "0", "single node"

# all nodes bad but k large enough
assert run("""2 1 2 1
2
1
1 2 5
""") == "0 5", "all bad allowed once"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small graph | 0 5 7 | layered relaxation correctness |
| k = 0 case | 0 -1 10 | constraint enforcement |
| single node | 0 | trivial base case |
| all bad | 0 5 | bad consumption logic |

## Edge Cases

A key edge case is when k = 0. In that case, any transition into a bad node must be completely blocked. The algorithm naturally handles this because the condition `used < k` prevents creation of invalid states. For example, if node 2 is bad and k = 0, from (1,0) we never push (2,1), so all paths through node 2 disappear.

Another edge case is when the destination node is bad. The algorithm still allows reaching it as long as the state transition happens within bounds. If reaching node v consumes the last available quota exactly, the state (v, k) is still valid and participates in the final minimum computation.

A third case appears when multiple different paths reach the same node with different used_bad values. The algorithm correctly keeps all of them, and the final min over all states ensures that we do not mistakenly discard a better path that uses a different number of bad nodes.
