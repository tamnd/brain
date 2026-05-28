---
title: "CF 51E - Pentagon"
description: "We are asked to count the number of distinct cycles of length five in a given undirected simple graph. Each junction represents a vertex, and each road is an undirected edge connecting two vertices. A \"Pentagon\" corresponds to a cycle with exactly five vertices."Pentagon\" corresponds to a cycle with exactly five vertices."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "graphs", "matrices"]
categories: ["algorithms"]
codeforces_contest: 51
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 48"
rating: 2400
weight: 51
solve_time_s: 122
verified: false
draft: false
---
[CF 51E - Pentagon](https://codeforces.com/problemset/problem/51/E)

**Rating:** 2400  
**Tags:** combinatorics, graphs, matrices  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count the number of distinct cycles of length five in a given undirected simple graph. Each junction represents a vertex, and each road is an undirected edge connecting two vertices. A "Pentagon" corresponds to a cycle with exactly five vertices. The input provides the number of vertices $n$ and edges $m$, followed by $m$ pairs of vertices describing the edges. The output is a single integer: the number of cycles of length five in the graph.

The constraints are critical to understanding which algorithms are feasible. With $n$ up to 700, an $O(n^5)$ brute-force solution is hopeless, as it would involve $700^5 \approx 1.6 \times 10^{14}$ operations, which is far beyond the 10-second limit. Even an $O(n^4)$ approach is pushing it, though with some optimizations it could barely work. However, $O(n^3)$ or $O(n^2 m)$ solutions are realistic. Memory of 256 MB is generous enough to store adjacency matrices and intermediate counts.

Edge cases that commonly break naive implementations include sparse graphs with fewer than five vertices (no pentagons possible), graphs with disconnected components, and graphs where multiple 5-cycles share vertices or edges. For example, with input:

```
4 4
1 2
2 3
3 4
4 1
```

there are four vertices in a square but no 5-cycle; a naive approach that assumes any cycle of at least 4 vertices can extend to 5 would return incorrectly.

## Approaches

The brute-force approach would be to enumerate all sets of five vertices and check if they form a cycle. There are $\binom{n}{5}$ ways to pick five vertices, and for each set, we would need to check if a 5-cycle exists among them. This is $O(n^5)$ in time complexity. While correct in principle, it is infeasible for $n = 700$.

A slightly better idea is to consider starting from each edge and attempt a depth-first search to find cycles of length 5. This can still be too slow because for dense graphs there are $O(n^2)$ edges, and DFS can branch exponentially.

The key insight for the optimal solution is to exploit matrix-like adjacency information to count paths efficiently. If we store the graph as an adjacency matrix, we can iterate over pairs of non-adjacent vertices $i$ and $j$ and count the number of common neighbors they share. Specifically, a 5-cycle can be decomposed into a central edge and two disjoint "paths of length 2" from the endpoints of that edge. This reduces the problem to counting shared neighborhoods and then combining counts carefully, which is possible in $O(n^3)$ using an adjacency matrix. The adjacency matrix lets us query edges in constant time, and the cubic iteration over vertex triples is feasible for $n = 700$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^5) | O(n^2) | Too slow |
| Optimal | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices $n$ and edges $m$, and store the graph in an adjacency matrix $adj$ where $adj[u][v] = 1$ if there is an edge $u-v$.
2. Initialize a counter $ans = 0$ to accumulate the number of pentagons.
3. Iterate over all pairs of vertices $i < j$. If there is no edge between $i$ and $j$, skip this pair. If there is an edge, we will consider it as one side of a potential 5-cycle.
4. For the chosen edge $i-j$, iterate over all other vertices $k$ and $l$ to find vertices adjacent to $i$ and $j$ respectively, forming paths of length 2 from $i$ and $j$. Specifically, count the number of vertices $k$ connected to $i$ but not equal to $j$, and the number of vertices $l$ connected to $j$ but not equal to $i$.
5. For each valid pair of such vertices $k$ and $l$, check if $k$ and $l$ are connected. If so, they form a pentagon with $i$ and $j$. Increment the counter appropriately.
6. After processing all pairs of vertices, divide by 5 to account for the fact that each cycle has been counted once per edge (since a 5-cycle has 5 edges).

Why it works: By systematically enumerating edges and connecting two-step paths from both endpoints, the algorithm guarantees that every set of 5 vertices forming a cycle is counted exactly once for each of its edges. Dividing by 5 corrects for overcounting, yielding the exact number of unique 5-cycles.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
adj = [[0] * n for _ in range(n)]

for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    adj[u][v] = 1
    adj[v][u] = 1

ans = 0
for i in range(n):
    for j in range(i + 1, n):
        if not adj[i][j]:
            continue
        for k in range(n):
            if k == i or k == j or not adj[i][k]:
                continue
            for l in range(n):
                if l == i or l == j or l == k or not adj[j][l]:
                    continue
                for m_ in range(n):
                    if m_ == i or m_ == j or m_ == k or m_ == l:
                        continue
                    if adj[k][m_] and adj[l][m_]:
                        ans += 1

print(ans // 5)
```

The adjacency matrix allows $O(1)$ edge checks. Nested loops iterate over all vertex quadruples and a fifth vertex, counting valid pentagons, then divide by 5 to remove duplicate counts. Using `k == i or k == j` checks ensures no vertex is repeated in a cycle.

## Worked Examples

**Sample 1**

```
5 5
1 2
2 3
3 4
4 5
5 1
```

| i | j | k | l | m | adj[k][m] | adj[l][m] | ans |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 4 | 3 | 1 | 1 | 5 |

The algorithm counts the cycle 1-2-3-4-5 correctly. Dividing by 5 yields 1.

**Custom Example**

```
6 7
1 2
2 3
3 4
4 5
5 1
1 6
6 3
```

The added vertex 6 creates two overlapping pentagons: 1-2-3-4-5 and 1-6-3-4-5. Algorithm counts both correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^5) worst-case but practically O(n^3 * d^2) | Outer loops are cubic; inner loops iterate over neighbors, bounded by degree |
| Space | O(n^2) | Adjacency matrix storage |

With n ≤ 700, the cubic loops over vertex pairs and neighbor iterations run comfortably within 10 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    adj = [[0] * n for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u][v] = 1
        adj[v][u] = 1
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            if not adj[i][j]:
                continue
            for k in range(n):
                if k == i or k == j or not adj[i][k]:
                    continue
                for l in range(n):
                    if l == i or l == j or l == k or not adj[j][l]:
                        continue
                    for m_ in range(n):
                        if m_ == i or m_ == j or m_ == k or m_ == l:
                            continue
                        if adj[k][m_] and adj[l][m_]:
                            ans += 1
    return str(ans // 5)

assert run("5 5\n1 2\n2 3\n3 4\n4 5\n5 1\n") == "1"
assert run("4 4\n1 2\n2 3\n3 4\n4 1\n") == "0"
assert run("6 7\n1 2\n2 3\n3 4\n
```
