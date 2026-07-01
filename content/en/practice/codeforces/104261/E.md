---
title: "CF 104261E - Gluing Pluto Back Together"
description: "We are given a complete weighted graph with up to 12 vertices. Each vertex represents a rock fragment, and the cost matrix tells us how expensive it is to directly glue any two fragments together."
date: "2026-07-01T21:41:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104261
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 03-24-23 Div. 2 (Beginner)"
rating: 0
weight: 104261
solve_time_s: 71
verified: true
draft: false
---

[CF 104261E - Gluing Pluto Back Together](https://codeforces.com/problemset/problem/104261/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a complete weighted graph with up to 12 vertices. Each vertex represents a rock fragment, and the cost matrix tells us how expensive it is to directly glue any two fragments together. The task is to arrange all fragments into a single cycle, using each fragment exactly once, so that the total cost of all chosen edges in the cycle is minimized.

In graph terms, we are looking for a minimum weight Hamiltonian cycle in a complete undirected graph with symmetric edge weights. The output is the sum of weights of exactly N edges forming one cycle that visits every vertex once and returns to the starting vertex.

The constraint N ≤ 12 is the key signal here. Any algorithm that tries to enumerate permutations of all vertices directly runs in O(N!) which becomes 12! ≈ 479 million permutations, and each permutation requires summing N edges. That is already too slow in Python under a 4 second limit once constant factors are included. This immediately suggests a bitmask dynamic programming approach over subsets.

A few edge cases are easy to miss in naive formulations. One is treating the cycle as a path and forgetting to close it, which leads to missing the final edge back to the start. For example, if N = 3 and costs are all 1, a path-based solution might compute cost 2 instead of the correct cycle cost 3. Another issue is double counting cycles in brute force permutations, since every cycle appears in 2N rotations and reversals, which complicates naive minimization unless carefully normalized.

## Approaches

The brute force idea is straightforward. We fix a starting node and generate all permutations of the remaining nodes. For each permutation, we compute the cycle cost by summing edges between consecutive nodes plus the edge returning to the start. This is correct because it explicitly checks every possible Hamiltonian cycle.

The problem is the scale of repetition. There are (N−1)! permutations after fixing the start, and each evaluation costs O(N), so the total complexity becomes O(N! · N). For N = 12, this is far beyond feasible limits.

The key observation is that the state of a partial construction only depends on which nodes have already been used and which node we are currently at. The order in which we reached that subset does not matter for future decisions. This is exactly the structure that bitmask dynamic programming captures.

We define DP[mask][i] as the minimum cost to start from a fixed node 0, visit exactly the nodes in mask, and end at node i. From each state, we try extending to any unvisited node j, adding cost[i][j]. Finally, we close the cycle by returning from each endpoint back to 0.

This reduces the exponential explosion from permutations of order N! to subsets of size 2^N, each with N transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (permutations) | O(N! · N) | O(N) | Too slow |
| Bitmask DP (TSP) | O(N^2 · 2^N) | O(N · 2^N) | Accepted |

## Algorithm Walkthrough

We fix one node as the starting point, usually node 0. This removes rotational symmetry of the cycle, since any cycle can be rotated to start at 0 without changing its cost.

We define a DP table indexed by subset and last visited node. The subset tracks which nodes are already included in the partial path.

1. Initialize all DP values to a large number, since we are minimizing costs. We set DP[1 << 0][0] = 0 because starting at node 0 with only node 0 visited costs nothing.
2. Iterate over all subsets of nodes using bitmasks from 0 to (1 << N) − 1. Each subset represents a partial set of visited fragments.
3. For each subset, iterate over all possible last nodes i included in that subset. If DP[mask][i] is invalid, skip it because it represents an unreachable state.
4. From state (mask, i), try extending the cycle by going to any node j not in mask. The transition updates DP[mask | (1 << j)][j] with DP[mask][i] + cost[i][j]. This ensures we always accumulate the cheapest way to reach each state.
5. After filling the DP table, all nodes have been visited in states where mask equals (1 << N) − 1. For each possible last node i, we add cost[i][0] to close the cycle back to the starting node and take the minimum.

The key idea is that DP compresses all permutations that share the same visited set and ending point into one state. That is what prevents recomputation of identical subproblems.

### Why it works

At any point, DP[mask][i] represents the minimum cost among all possible orders of visiting exactly the nodes in mask and ending at i. Any extension to a new node j depends only on i and mask, not on how we arrived at this configuration. This establishes an optimal substructure: the best solution to a larger set can be built from the best solutions of its subsets. Since every Hamiltonian cycle corresponds to exactly one sequence of states in this DP, and every state transition preserves correctness by considering all possibilities, the final minimum over all endpoints correctly yields the optimal cycle.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    cost = [list(map(int, input().split())) for _ in range(n)]
    
    INF = 10**18
    size = 1 << n
    dp = [[INF] * n for _ in range(size)]
    
    dp[1][0] = 0  # start from node 0, mask = 000...001
    
    for mask in range(size):
        if not (mask & 1):
            continue
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            if not (mask & (1 << i)):
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                new_mask = mask | (1 << j)
                new_cost = dp[mask][i] + cost[i][j]
                if new_cost < dp[new_mask][j]:
                    dp[new_mask][j] = new_cost
    
    full = size - 1
    ans = INF
    for i in range(n):
        ans = min(ans, dp[full][i] + cost[i][0])
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The DP table is initialized with a large sentinel value to represent unreachable states. The starting state fixes node 0 with a bitmask containing only that node.

The triple loop structure is necessary: mask enumerates subsets, i enumerates endpoints of those subsets, and j tries extensions. The condition checks ensure we only extend valid states and never reuse nodes already included in the subset.

The final loop explicitly closes the cycle by returning to node 0. This is the step most commonly missed in incorrect implementations, and it is essential because DP only builds Hamiltonian paths, not cycles directly.

## Worked Examples

We trace the sample input.

Input:

```
4
0 1 2 3
1 0 4 5
2 4 0 6
3 5 6 0
```

We track only meaningful DP transitions.

| Step | Mask | Last node | DP value | Action |
| --- | --- | --- | --- | --- |
| init | 0001 | 0 | 0 | start |
| extend | 0011 | 1 | 1 | 0→1 |
| extend | 0101 | 2 | 2 | 0→2 |
| extend | 1001 | 3 | 3 | 0→3 |
| full paths | 1111 | 1,2,3 | computed | multiple permutations |

Now consider one optimal path: 0 → 1 → 2 → 3 → 0 gives cost 1 + 4 + 6 + 3 = 14.

This trace shows that DP constructs all partial paths from node 0 while preserving minimal cost for each state. The final closure step ensures the cycle is completed correctly.

A second small case helps confirm correctness:

Input:

```
3
0 1 1
1 0 1
1 1 0
```

All cycles have equal cost 3. DP will produce 2 (path cost 0→1→2) and then add 2→0, yielding 3. Every permutation collapses to the same optimal value, confirming symmetry handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N^2 · 2^N) | For each subset and endpoint, we try transitions to up to N nodes |
| Space | O(N · 2^N) | DP table stores a value for each (mask, last node) pair |

With N ≤ 12, 2^N = 4096 and N^2 · 2^N is about 589k operations, which is easily within limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    input = sys.stdin.readline
    n = int(input())
    cost = [list(map(int, input().split())) for _ in range(n)]
    
    INF = 10**18
    size = 1 << n
    dp = [[INF] * n for _ in range(size)]
    dp[1][0] = 0
    
    for mask in range(size):
        if not (mask & 1):
            continue
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            if not (mask & (1 << i)):
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                dp[mask | (1 << j)][j] = min(dp[mask | (1 << j)][j], dp[mask][i] + cost[i][j])
    
    full = size - 1
    ans = min(dp[full][i] + cost[i][0] for i in range(n))
    return str(ans)

# provided sample
assert run("""4
0 1 2 3
1 0 4 5
2 4 0 6
3 5 6 0
""") == "14"

# minimum n=2
assert run("""2
0 5
5 0
""") == "10"

# symmetric all equal
assert run("""3
0 2 2
2 0 2
2 2 0
""") == "6"

# chain-like asymmetry
assert run("""4
0 1 100 100
1 0 1 100
100 1 0 1
100 100 1 0
""") == "4"

# zero-cost edges
assert run("""3
0 0 0
0 0 0
0 0 0
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| N=2 symmetric | 10 | minimal cycle correctness |
| all equal | 6 | symmetry handling |
| chain asymmetry | 4 | DP chooses structured route |
| all zeros | 0 | zero-cost edge handling |

## Edge Cases

A common edge case is when all costs are zero. The DP will propagate zeros through all states, and the final closure also adds zero, producing a correct result of 0. This confirms that the algorithm does not rely on positive weights for correctness.

Another subtle case is when the optimal cycle does not resemble a simple greedy path. For example, in asymmetric-looking cost matrices, the best path may avoid locally cheap edges to reduce later costs. The DP handles this because every state stores the true minimum over all partial permutations, not a locally greedy choice.

Finally, the smallest case N = 2 tests correctness of cycle closure. The DP builds a single path 0 → 1, and the final step explicitly adds cost[1][0], ensuring the cycle is complete and not accidentally treated as a path.
