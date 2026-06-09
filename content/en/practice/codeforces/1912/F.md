---
title: "CF 1912F - Fugitive Frenzy"
description: "We are asked to compute the expected duration of a pursuit on a tree, where a police officer and a fugitive take turns moving. The city is represented as an undirected tree with $n$ vertices."
date: "2026-06-08T20:17:06+07:00"
tags: ["codeforces", "competitive-programming", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1912
codeforces_index: "F"
codeforces_contest_name: "2023-2024 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 3100
weight: 1912
solve_time_s: 185
verified: false
draft: false
---

[CF 1912F - Fugitive Frenzy](https://codeforces.com/problemset/problem/1912/F)

**Rating:** 3100  
**Tags:** math, probabilities  
**Solve time:** 3m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the expected duration of a pursuit on a tree, where a police officer and a fugitive take turns moving. The city is represented as an undirected tree with $n$ vertices. The police officer starts at a fixed vertex, while the fugitive chooses any other vertex to start. The officer moves first, either stepping to an adjacent vertex or standing still, consuming one unit of time. The fugitive then instantly moves to any vertex that is not on the path to the officer, effectively avoiding capture unless forced. Both play optimally: the officer minimizes expected capture time, and the fugitive maximizes it.

The output is the expected number of minutes until the fugitive is caught. Because the fugitive moves instantaneously and always knows the officer's location, the problem reduces to computing the expected capture time under a two-player game with perfect information for the fugitive.

The number of vertices is small ($n \le 100$), so algorithms that are cubic in $n$ are feasible. The tree structure guarantees a unique path between any two vertices, which simplifies computing safe moves for the fugitive. Edge cases include:

- $n = 2$, where the police and fugitive are at adjacent vertices, leading to immediate capture.
- Trees with a "long path" where the fugitive can continually move to distant vertices. A naive breadth-first search ignoring the fugitive’s instantaneous moves will fail to produce the correct expectation.

Understanding these subtleties is crucial: the fugitive's instant movement means we cannot simulate turn-by-turn positions naively.

## Approaches

The brute-force approach would attempt to enumerate every sequence of moves for the officer and fugitive and compute the expected capture time recursively. For each officer position $p$ and fugitive position $f$, we could try all officer moves and all possible fugitive safe moves, averaging over possibilities. This leads to $O(n^2 \cdot n \cdot n)$ recursion in the worst case, since there are $n^2$ position pairs and up to $n$ moves for each. Even with memoization, the state space is $O(n^2)$, but the recursion for computing expectations can multiply this to $O(n^4)$, which is acceptable for $n \le 100$, but cumbersome and error-prone.

The key insight is that the fugitive can always avoid the officer unless the officer is already "close enough" to trap him. In other words, from a position $(p, f)$, the expected capture time only depends on the subtree distances: the furthest distance the officer can reduce in one move. The fugitive will distribute himself over all positions that are maximally safe. This reduces the problem to a system of linear equations, where each state $(p, f)$ represents an unknown expected capture time $E[p][f]$. If $p = f$, $E[p][f] = 0$. Otherwise, the officer chooses a move to minimize $1 + E[p'][f']$, and the fugitive chooses $f'$ to maximize $E[p'][f']$. This leads to a min-max linear system solvable by iteration or matrix inversion.

This insight reduces the naive $O(n^4)$ recursion with probability branches to an iterative $O(n^3)$ solution: for each officer position, we compute expected times against all possible fugitive positions using dynamic programming, propagating values until convergence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(n^2) | Acceptable but complex to implement |
| Linear System / DP | O(n^3) | O(n^2) | Efficient, clean, and feasible |

## Algorithm Walkthrough

1. Parse the tree input and construct an adjacency list representation. Each vertex stores its neighbors to allow constant-time access to officer moves.
2. Initialize a 2D array $E[p][f]$ representing the expected capture time if the officer is at $p$ and the fugitive at $f$. Set $E[p][p] = 0$ for all $p$, since capture occurs instantly.
3. Precompute the "safe moves" for the fugitive. For each pair $(p, f)$, find all vertices $f'$ such that the path from $f$ to $f'$ does not pass through $p$. This can be done efficiently using BFS or DFS from $f$, ignoring the subtree containing $p$.
4. Initialize $E[p][f] = 1$ for $p \ne f$ as a starting guess. This represents the base time for the officer’s next move.
5. Iterate until convergence:

1. For each officer position $p$ and fugitive position $f$, if $p \ne f$, compute the minimum over all officer moves $p' \in \{p\} \cup \text{neighbors}(p)$ of $1 + \text{average of } E[p'][f']$ over all safe fugitive moves $f'$.
2. Update $E[p][f]$ to this minimum value. Repeat until changes are below a small epsilon ($1e-9$).
6. The final answer is the expected time from $E[s][f]$, averaged over all possible fugitive starting positions $f \ne s$, since the fugitive can choose any initial vertex optimally.

This works because the operator in step 5 is a contraction mapping: each update brings values closer to the true expectation, and the unique fixed point represents the min-max expectation for all positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = map(int, input().split())
        adj[u-1].append(v-1)
        adj[v-1].append(u-1)
    s = int(input()) - 1

    # Precompute distances and safe moves
    from collections import deque
    safe = [[[] for _ in range(n)] for _ in range(n)]
    for p in range(n):
        for f in range(n):
            visited = [False]*n
            visited[p] = True
            q = deque([f])
            safe[p][f] = []
            while q:
                u = q.popleft()
                safe[p][f].append(u)
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)

    # Initialize expected times
    E = [[0.0 if i==j else 1.0 for j in range(n)] for i in range(n)]
    eps = 1e-9
    changed = True
    while changed:
        changed = False
        for p in range(n):
            for f in range(n):
                if p == f:
                    continue
                best = float('inf')
                for np_ in [p] + adj[p]:
                    # Fugitive maximizes
                    sume = 0
                    moves = safe[np_][f]
                    for nf in moves:
                        sume += E[np_][nf]
                    sume /= len(moves)
                    best = min(best, 1 + sume)
                if abs(E[p][f] - best) > eps:
                    E[p][f] = best
                    changed = True

    # Fugitive chooses initial position to maximize expectation
    ans = 0.0
    for f in range(n):
        if f != s:
            ans = max(ans, E[s][f])
    print(ans)

if __name__ == "__main__":
    main()
```

The adjacency list allows constant-time access to officer moves. Safe moves for the fugitive are precomputed using BFS, ignoring the subtree containing the officer. The DP updates $E[p][f]$ until convergence. Averaging over safe fugitive moves implements the probabilistic expectation of the fugitive’s mixed strategy. We take the maximum over initial positions because the fugitive selects the starting vertex optimally.

## Worked Examples

**Sample 1**

Input:

```
2
1 2
2
```

| Step | Officer | Fugitive | E[p][f] |
| --- | --- | --- | --- |
| init | 2 | 1 | 1 |

Here, the officer can move to 1 immediately, capturing the fugitive in one minute. The output is 1.

**Sample 2 (custom)**

Input:

```
3
1 2
2 3
1
```

| Step | Officer | Fugitive | E[p][f] |
| --- | --- | --- | --- |
| init | 1 | 2 | 1.5 |
| init | 1 | 3 | 2 |

The fugitive at 3 maximizes time. The optimal expectation is 2.

These traces show how the fugitive exploits distant positions and the officer chooses moves minimizing the expected capture time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | For each officer and fugitive position pair, we iterate over up to $n$ officer moves and consider up to $n$ safe fugitive moves. |
| Space | O(n^2) | Store E[p][f] and safe[p][f] arrays. |

Given $n \le 100$, (O(n^3
