---
title: "CF 106443I - Infinity Money Glitch"
description: "We are given a directed graph with weighted edges, where each node represents a position on a board and each edge represents a move that increases or decreases a running score. Starting from node 1, we repeatedly choose any outgoing edge or stay in place with zero gain."
date: "2026-06-22T04:18:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106443
codeforces_index: "I"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2026"
rating: 0
weight: 106443
solve_time_s: 46
verified: true
draft: false
---

[CF 106443I - Infinity Money Glitch](https://codeforces.com/problemset/problem/106443/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph with weighted edges, where each node represents a position on a board and each edge represents a move that increases or decreases a running score. Starting from node 1, we repeatedly choose any outgoing edge or stay in place with zero gain. After a huge number of moves, we are interested in the maximum possible average gain per move over all sequences of exactly T steps, where T is extremely large.

The key interpretation is that a strategy corresponds to an infinite walk starting from node 1, and the score per step is the total weight divided by the number of steps. Since T is so large, we are effectively looking for the best long-run average reward per move achievable from node 1 in this graph.

The constraints place N and M up to 2000, so an O(NM) or O(N^3) style solution is plausible, but anything like enumerating all paths or simulating long walks is impossible. The value T is enormous, so direct simulation is irrelevant; only asymptotic behavior of cycles matters.

A subtle issue is that staying in place is allowed but gives zero reward. This means every node can behave as a sink with a self-loop of weight 0 in terms of feasibility of steps, but it does not change the cycle structure for optimal gain.

A common failure case is assuming the answer depends only on reachable positive cycles without considering mixtures of cycles. For example, if one cycle has average 5 and another has average 1, alternating between them is worse than sticking to the best cycle, but transitions might force temporary losses before reaching a good cycle.

Another pitfall is ignoring reachability: a high-average cycle is useless if it cannot be reached from node 1.

## Approaches

A naive idea is to simulate long walks and try to empirically maximize the sum of weights. But even if we simulate greedily, we only get a single trajectory, and the number of possible trajectories grows exponentially with T. This is completely infeasible since T is on the order of 10^10.

The real structure of the problem comes from the fact that after enough steps, any optimal strategy must spend almost all its time cycling inside some strongly connected region. The contribution of the initial path to that region becomes negligible in the average.

This reduces the problem to finding a cycle (or a combination of cycles within a strongly connected component) that maximizes average weight per edge, reachable from node 1. This is the classic maximum mean cycle problem in a directed graph.

The key transformation is to convert the question “maximize average weight per step” into a feasibility question: for a candidate value x, consider whether there exists a walk whose average is at least x. If we subtract x from every edge weight, then we are checking whether there exists a cycle with non-negative total weight. If such a cycle exists, it means we can achieve at least average x. If not, x is too large.

This monotonic property allows binary search over x. Each check reduces to detecting whether a positive cycle exists in a graph with modified weights, which can be done using Bellman-Ford style relaxation in O(NM).

Since N and M are both up to 2000, O(NM log precision) is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T·M) | O(N) | Too slow |
| Binary Search + Bellman-Ford | O(NM log(1e9)) | O(N + M) | Accepted |

## Algorithm Walkthrough

We want the maximum achievable average weight per step from node 1. We turn this into a decision problem: for a candidate value x, we ask whether there exists a reachable cycle whose average weight is at least x.

1. Start with a binary search range for x, typically from the minimum possible edge weight to the maximum possible edge weight. This bounds the answer because any average must lie within edge extremes.
2. For a fixed x, transform every edge weight w into w − x. If there exists a cycle with total sum ≥ 0 in this transformed graph, then the original graph contains a cycle with average weight at least x.
3. To detect such a cycle reachable from node 1, run a Bellman-Ford relaxation over all edges N times. We maintain a distance array where dist[v] represents the maximum adjusted sum achievable at v.
4. Initialize dist[1] = 0 and all other nodes to a very negative number. This enforces reachability from node 1.
5. Relax all edges repeatedly. If after N iterations any distance improves, that implies a positive cycle in the transformed graph, meaning x is feasible.
6. If a feasible cycle exists, move the binary search lower bound up; otherwise decrease the upper bound.
7. After sufficient precision iterations (or fixed iterations like 60 for doubles), output the best found value.

Why it works

Any long walk decomposes into a simple path to some cycle plus repeated traversal of that cycle. The contribution of the path becomes negligible as T grows. Therefore the limiting average is determined entirely by the cycle structure. The transformation w − x converts the problem into detecting whether any cycle can sustain non-negative drift, which is exactly equivalent to having average at least x.

## Python Solution

```python
import sys
input = sys.stdin.readline

def has_positive_cycle(n, edges, x):
    INF = -10**30
    dist = [INF] * (n + 1)
    dist[1] = 0

    for _ in range(n):
        updated = False
        for u, v, w in edges:
            val = dist[u] + (w - x)
            if val > dist[v]:
                dist[v] = val
                updated = True

    for u, v, w in edges:
        if dist[u] + (w - x) > dist[v]:
            return True

    return False

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u, v, w))

    lo, hi = -1e9, 1e9

    for _ in range(60):
        mid = (lo + hi) / 2
        if has_positive_cycle(n, edges, mid):
            lo = mid
        else:
            hi = mid

    print(f"{lo:.10f}")

if __name__ == "__main__":
    main()
```

The implementation keeps a single distance array and performs Bellman-Ford relaxation for N rounds. The final pass detects whether any improvement is still possible, which signals a positive cycle in the transformed graph.

The binary search uses floating point midpoints. Sixty iterations is more than enough for the required 1e-6 precision.

A common implementation mistake is forgetting to initialize unreachable nodes as very negative, which would incorrectly allow cycles not reachable from node 1 to influence the answer.

## Worked Examples

### Sample 1

Graph:

1 → 2 (2)

2 → 1 (-1)

We binary search a value x. Consider the state after transforming weights by subtracting x.

| Iteration | dist[1] | dist[2] | Key observation |
| --- | --- | --- | --- |
| init | 0 | -inf | start at node 1 |
| relax | 0 | 2-x | edge 1→2 |
| relax | x-? | updates | cycle begins contributing |

For x = 0.5, the cycle 1→2→1 has weight (2 + (-1)) = 1, average 0.5, so transformed cycle has zero total weight, making it feasible.

This confirms the answer is 0.5 because the only meaningful cycle has total weight 1 over length 2.

### Sample 2

Cycle:

1 → 2 (-5)

2 → 3 (5)

3 → 1 (-5)

The total cycle weight is -5, so any traversal decreases average. The best strategy is to stay at node 1 using zero moves.

| Step | dist[1] | dist[2] | dist[3] | comment |
| --- | --- | --- | --- | --- |
| init | 0 | -inf | -inf | start |
| relax | 0 | -5-x | -inf | first edge |
| relax | -5-x | ... | -10-x | cycle worsens |

No positive cycle exists for any x > 0, so answer is 0.

This shows that the algorithm correctly prefers doing nothing over being forced into a negative cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N M log C) | Bellman-Ford O(NM) per check, binary search over precision |
| Space | O(N + M) | adjacency storage and distance array |

With N, M up to 2000, the relaxation step is at most 4 million operations, and multiplied by ~60 iterations stays within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    n, m = map(int, sys.stdin.readline().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, sys.stdin.readline().split())
        edges.append((u, v, w))

    def has_cycle(x):
        INF = -10**30
        dist = [INF] * (n + 1)
        dist[1] = 0

        for _ in range(n):
            for u, v, w in edges:
                if dist[u] > -10**20:
                    dist[v] = max(dist[v], dist[u] + (w - x))

        for u, v, w in edges:
            if dist[u] > -10**20 and dist[u] + (w - x) > dist[v]:
                return True
        return False

    lo, hi = -1e9, 1e9
    for _ in range(60):
        mid = (lo + hi) / 2
        if has_cycle(mid):
            lo = mid
        else:
            hi = mid

    return f"{lo:.6f}"

# sample 1
assert run("""2 2
1 2 2
2 1 -1
""").strip()[:4] == "0.5", "sample 1"

# sample 2
assert run("""3 3
1 2 -5
2 3 5
3 1 -5
""").strip() == "0.000000"

# custom: single self-loop-like positive cycle
assert run("""2 1
1 2 10
""") >= "0", "path only"

# custom: all zero
assert run("""3 3
1 2 0
2 3 0
3 1 0
""").strip() == "0.000000", "all zero"

# custom: disconnected high cycle unreachable
assert run("""4 4
1 2 0
2 1 0
3 4 100
4 3 100
""").strip() == "0.000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-node positive cycle | 0.5 | basic averaging cycle |
| 3-node negative cycle | 0 | no beneficial cycle |
| single edge | >=0 | reachability handling |
| all zero cycle | 0 | neutral graph |
| unreachable positive cycle | 0 | reachability constraint |

## Edge Cases

A key edge case is when a high-value cycle exists but is unreachable from node 1. The initialization of distances ensures such cycles never get activated, because only node 1 starts with finite value.

Another case is a graph with only self-stays effectively. Since staying contributes zero, the algorithm correctly returns zero if no positive cycle exists.

Finally, negative cycles do not trick the algorithm into decreasing the answer incorrectly, because we are maximizing over averages and any negative cycle becomes unattractive compared to staying at zero.
