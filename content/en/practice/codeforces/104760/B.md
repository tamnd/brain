---
title: "CF 104760B - \u0412\u044b\u0438\u0433\u0440\u044b\u0448"
description: "We are given a small undirected flight network where airports are nodes and flights are edges. A traveler starts at airport 1 and is allowed to take exactly K flights. Each flight moves along an undirected edge to a neighboring airport."
date: "2026-06-28T22:00:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "B"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 60
verified: true
draft: false
---

[CF 104760B - \u0412\u044b\u0438\u0433\u0440\u044b\u0448](https://codeforces.com/problemset/problem/104760/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small undirected flight network where airports are nodes and flights are edges. A traveler starts at airport 1 and is allowed to take exactly K flights. Each flight moves along an undirected edge to a neighboring airport. The traveler may revisit airports and reuse edges any number of times. The only requirement is that after exactly K moves, the traveler must end up back at airport 1. We need to count how many different sequences of visited airports of length K+1 (including the start) satisfy this condition.

The structure is fundamentally about counting walks of fixed length in an undirected graph, with a fixed start and end vertex.

The constraints are very small in graph size but moderate in walk length. With N up to 100 and K up to 60, any approach that explores all paths explicitly would explode, since the branching factor can be large and the number of length-K walks grows exponentially. Even a rough upper bound like N * deg^K makes brute force impossible except for extremely small K.

The key edge case that breaks naive thinking is when there are cycles and multiple ways to return to 1. For example, in a triangle graph with K = 2, returning to 1 requires going out and immediately coming back, but different intermediate nodes may exist, creating multiple valid paths that are easy to undercount if one mistakenly assumes “distance” or shortest paths matter rather than walks.

Another subtle edge case is parity. If the graph structure makes it impossible to return to 1 in exactly K steps (for example a tree and odd K constraints from bipartite structure), the answer must correctly become zero even though many paths exist for K-1 or K+1.

## Approaches

A direct approach is to recursively simulate all possible sequences of K moves starting from node 1. At each step, we branch to all neighbors. After K steps, we check whether we are back at node 1. This is conceptually correct because it enumerates every valid walk exactly once. However, the number of recursive states grows like the number of length-K walks in a graph, which in dense cases is roughly (N-1)^K. With K up to 60, this is far beyond feasible computation.

The structure of the problem suggests a dynamic programming formulation over steps. Instead of enumerating full paths, we track how many ways we can be at each node after t steps. This works because the next position depends only on the current position, not the full history. This is a classic “walk counting on a graph” DP.

We define dp[t][v] as the number of ways to be at vertex v after exactly t flights starting from node 1. The transition is that every way to reach a node u at time t contributes to all neighbors v at time t+1. This compresses the exponential branching into N states per step, making the process linear in K transitions over edges.

The problem reduces to iterating this transition K times and reading dp[K][1].

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS enumeration | O(N^K) | O(K) recursion | Too slow |
| DP over steps and nodes | O(K * M) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph so that neighbor queries are fast. This is necessary because each DP transition needs to iterate over edges efficiently rather than scanning all pairs of nodes.
2. Initialize a DP array where dp[v] represents the number of ways to be at node v after the current number of steps. Set dp[1] = 1 because we start at airport 1 with one valid empty path.
3. Repeat the following process exactly K times, each time representing one flight taken.
4. Create a fresh array ndp filled with zeros. This separation is important because updates must not interfere with the current step’s values.
5. For every node u, distribute dp[u] to all neighbors v by adding dp[u] to ndp[v]. Each addition represents extending all walks that end at u into walks that end at v in one more step.
6. After processing all edges, replace dp with ndp. Now dp represents the number of ways to be at each node after the next step.
7. After completing K iterations, output dp[1], which counts all walks of length K that start and end at node 1.

### Why it works

At every step t, dp[v] exactly counts all walks of length t from node 1 to v. The transition preserves this property because every walk of length t+1 ending at v must come from some neighbor u after t steps, and all such contributions are counted exactly once through the adjacency expansion. No walk is missed because every possible next edge is explored, and no walk is double-counted because each previous state contributes independently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M, K = map(int, input().split())
    adj = [[] for _ in range(N + 1)]

    for _ in range(M):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    dp = [0] * (N + 1)
    dp[1] = 1

    for _ in range(K):
        ndp = [0] * (N + 1)
        for u in range(1, N + 1):
            if dp[u] == 0:
                continue
            for v in adj[u]:
                ndp[v] += dp[u]
        dp = ndp

    print(dp[1])

if __name__ == "__main__":
    solve()
```

The implementation mirrors the DP definition directly. The adjacency list stores the undirected graph so each edge is traversed twice, once from each endpoint, which is consistent with bidirectional flight rules.

The dp array is reset each iteration to ensure we only use states from the previous step. Skipping zero entries avoids unnecessary inner loop work but is not strictly required for correctness. The final answer is taken from dp[1] after exactly K transitions.

## Worked Examples

### Sample 1

Input:

```
4 4 4
1 2
1 3
2 4
3 4
```

We track dp after each step.

| Step | dp[1] | dp[2] | dp[3] | dp[4] |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 |
| 2 | 2 | 0 | 0 | 2 |
| 3 | 0 | 4 | 4 | 0 |
| 4 | 8 | 0 | 0 | 0 |

After 4 steps, dp[1] = 8.

This trace shows how mass alternates between partitions of the graph: from node 1 into its neighbors, then back through intermediate structure. Every valid 4-step closed walk contributes exactly once to the final count.

### Sample 2

Input:

```
4 4 3
1 2
1 3
2 4
3 4
```

| Step | dp[1] | dp[2] | dp[3] | dp[4] |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 |
| 2 | 2 | 0 | 0 | 2 |
| 3 | 0 | 4 | 4 | 0 |

We end after 3 steps with dp[1] = 0.

This confirms that returning to the start depends on parity in this graph structure. After an odd number of steps, all probability mass sits on the opposite partition of the bipartite graph, making return to node 1 impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K · M) | Each of K steps processes every edge once in the adjacency-based transition |
| Space | O(N + M) | Adjacency list plus two DP arrays of size N |

With N ≤ 100 and K ≤ 60, the total operations are on the order of a few thousand edge relaxations per step, which is easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""4 4 4
1 2
1 3
2 4
3 4
""") == "8"

assert run("""4 4 3
1 2
1 3
2 4
3 4
""") == "0"

# custom cases

# minimum case: only two nodes, must bounce back and forth
assert run("""2 1 2
1 2
""") == "1"

# odd step in a 2-node graph must be zero
assert run("""2 1 3
1 2
""") == "0"

# complete triangle, K=2: 1->2->1 and 1->3->1
assert run("""3 3 2
1 2
2 3
1 3
""") == "2"

# disconnected graph: no return possible
assert run("""4 2 2
1 2
3 4
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes, K=2 | 1 | simplest back-and-forth cycle |
| 2 nodes, K=3 | 0 | parity constraint |
| triangle K=2 | 2 | multiple return paths |
| disconnected | 0 | unreachable states |

## Edge Cases

One important case is when the graph is bipartite and K is odd. In such a situation, any walk starting at node 1 must end on the opposite side of the bipartition after an odd number of steps, so returning to node 1 is impossible. The DP naturally captures this because after each step, values alternate between partitions and dp[1] becomes zero whenever parity mismatches the structure.

Another case is when node 1 has degree 1 and the graph is a simple line. For K = 2, the walk must go out and return, yielding exactly one way. For K = 3, it becomes impossible again. The DP correctly reflects this oscillation because all mass repeatedly flows along the single path and cannot branch.

A third case is fully connected small graphs where many revisits are possible. The algorithm handles these without modification because it does not assume uniqueness of paths, only counts accumulations over transitions, ensuring every distinct sequence is counted separately.
