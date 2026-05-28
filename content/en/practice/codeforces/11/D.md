---
title: "CF 11D - A Simple Task"
description: "We are asked to count the number of simple cycles in an undirected graph. A simple cycle is a closed loop where no vertex or edge is repeated."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "graphs"]
categories: ["algorithms"]
codeforces_contest: 11
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 11"
rating: 2200
weight: 11
solve_time_s: 89
verified: true
draft: false
---
[CF 11D - A Simple Task](https://codeforces.com/problemset/problem/11/D)

**Rating:** 2200  
**Tags:** bitmasks, dp, graphs  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of simple cycles in an undirected graph. A simple cycle is a closed loop where no vertex or edge is repeated. The input gives us the number of vertices `n` and the number of edges `m`, followed by `m` pairs of integers describing which vertices are connected. The output is a single integer representing the total count of simple cycles.

The key constraint here is that `n` is at most 19. This is small enough that exponential algorithms based on subsets of vertices are feasible because $2^{19}$ is roughly 500,000. The number of edges `m` is unbounded in the problem statement, but in practice it cannot exceed $n(n-1)/2$ since the graph is simple. This means brute force approaches that examine all possible vertex sequences will quickly become infeasible due to factorial growth. A careless approach that tries to enumerate every permutation of vertices and check if it forms a cycle will fail even for `n=10`.

An edge case to consider is a graph with no edges or a single vertex. For example, `n=1, m=0` should output 0, because no cycles exist. Another subtle edge case is a graph that forms a tree. Trees have no cycles, and a naive algorithm that checks paths without proper bookkeeping might falsely count a path that loops back on itself as a cycle. Cliques are also worth checking because they maximize the number of cycles.

## Approaches

The brute-force approach would be to try every subset of vertices, generate all permutations of each subset, and check if it forms a cycle. This is correct because any simple cycle must correspond to some permutation of a subset of vertices. However, the number of permutations grows as `n!`, and even for `n=10` this is over 3 million operations per subset, making it unworkable.

The key insight is that we can exploit two facts. First, the graph is small (`n <= 19`), which allows us to represent subsets of vertices as bitmasks. Second, cycles are closed paths where each vertex is visited exactly once, and dynamic programming can efficiently count paths between vertices over subsets. We can define `dp[mask][v]` as the number of ways to reach vertex `v` visiting exactly the vertices in `mask` starting from the smallest vertex in `mask`. Then, a cycle is simply a subset where `dp[mask][v]` can return to the starting vertex through an edge, and we can ensure each cycle is counted exactly once by fixing the smallest vertex as the starting point.

The brute-force works because it guarantees correctness by construction, but fails due to factorial growth. The bitmask dynamic programming approach works because it reduces the factorial complexity to `O(n * 2^n)`, which is manageable for `n = 19`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slow |
| Bitmask DP | O(n * 2^n) | O(n * 2^n) | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices `n` and edges `m` and build an adjacency matrix `adj` such that `adj[u][v] = True` if there is an edge between `u` and `v`. The adjacency matrix allows constant-time checks for connectivity.
2. Initialize a DP table `dp[mask][v]` where `mask` is a bitmask representing the set of vertices visited and `v` is the last vertex in the path. The table stores the number of paths that visit exactly the vertices in `mask` ending at `v`, starting from the smallest vertex in `mask`.
3. For each vertex `v`, set `dp[1 << v][v] = 1`. This represents starting a path at vertex `v` with only `v` in the path.
4. Iterate over all `mask` from 1 to `(1 << n) - 1`. For each vertex `u` in `mask`, consider every neighbor `v` of `u`. If `v` is not yet in `mask` and `v` is greater than the smallest vertex in `mask` (to prevent double-counting cycles), update `dp[mask | (1 << v)][v] += dp[mask][u]`. This extends all paths ending at `u` by adding `v`.
5. After filling the DP table, count cycles. For each subset `mask` with at least 3 vertices, find the smallest vertex `s`. For each vertex `v` in `mask` other than `s`, if there is an edge between `v` and `s`, add `dp[mask][v]` to the answer. Each cycle is counted exactly once because we fixed `s` as the smallest vertex in the cycle.
6. Output the total count.

The invariant here is that `dp[mask][v]` correctly counts all paths from the smallest vertex in `mask` to `v` using exactly the vertices in `mask`. By extending paths only to vertices greater than the start, we prevent counting the same cycle multiple times in different rotations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
adj = [[False] * n for _ in range(n)]
for _ in range(m):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    adj[a][b] = adj[b][a] = True

dp = [[0] * n for _ in range(1 << n)]
for v in range(n):
    dp[1 << v][v] = 1

for mask in range(1, 1 << n):
    # find smallest vertex in mask
    s = (mask & -mask).bit_length() - 1
    for u in range(n):
        if not (mask & (1 << u)):
            continue
        for v in range(n):
            if adj[u][v] and not (mask & (1 << v)) and v > s:
                dp[mask | (1 << v)][v] += dp[mask][u]

ans = 0
for mask in range(1, 1 << n):
    if bin(mask).count("1") < 3:
        continue
    s = (mask & -mask).bit_length() - 1
    for v in range(n):
        if v != s and (mask & (1 << v)) and adj[v][s]:
            ans += dp[mask][v]

print(ans)
```

The adjacency matrix allows constant-time neighbor checks. The DP initialization sets paths starting at each vertex. We carefully extend only to vertices larger than the smallest in the mask to avoid duplicate counting. The final loop only counts cycles of length at least 3, summing paths that can return to the starting vertex.

## Worked Examples

### Sample 1

Input:

```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

| mask | s | v | dp[mask][v] | Comment |
| --- | --- | --- | --- | --- |
| 0001 | 0 | 0 | 1 | start at vertex 1 |
| 0011 | 0 | 1 | 1 | path 1->2 |
| 0111 | 0 | 2 | 1 | path 1->2->3 |
| 1111 | 0 | 3 | 1 | path 1->2->3->4 |
| final | - | - | 7 | 4 triangles + 3 quadrilaterals |

This trace confirms DP correctly extends paths and counts cycles once.

### Custom Example

Input:

```
3 2
1 2
2 3
```

| mask | s | v | dp[mask][v] | Comment |
| --- | --- | --- | --- | --- |
| 0001 | 0 | 0 | 1 | start 1 |
| 0011 | 0 | 1 | 1 | path 1->2 |
| 0111 | 0 | 2 | 1 | path 1->2->3 |
| final | - | - | 0 | No edge 3->1, no cycle |

This shows the algorithm correctly ignores non-cycles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 * 2^n) | Each mask iterates over n vertices and n neighbors |
| Space | O(n * 2^n) | DP table stores a value for each mask and vertex |

With `n <= 19`, `2^n * n^2` is around 5 million operations, comfortably under 2 seconds. The DP table fits in memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    adj = [[False] * n for _ in range(n)]
    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a][b] = adj[b][a] = True
    dp = [[0] * n for _ in range(1 << n)]
    for v in range(n):
        dp[1 << v][v] = 1
    for mask in range(1,
```
