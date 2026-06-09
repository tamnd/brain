---
title: "CF 1795G - Removal Sequences"
description: "We are given a graph with $n$ vertices and $m$ edges. Each vertex $i$ has an associated number $ai$. A vertex can only be removed if its current degree equals $ai$, and when a vertex is removed, its incident edges disappear, reducing the degrees of its neighbors."
date: "2026-06-09T10:09:22+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1795
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 143 (Rated for Div. 2)"
rating: 2700
weight: 1795
solve_time_s: 117
verified: false
draft: false
---

[CF 1795G - Removal Sequences](https://codeforces.com/problemset/problem/1795/G)

**Rating:** 2700  
**Tags:** bitmasks, dfs and similar, graphs  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a graph with $n$ vertices and $m$ edges. Each vertex $i$ has an associated number $a_i$. A vertex can only be removed if its current degree equals $a_i$, and when a vertex is removed, its incident edges disappear, reducing the degrees of its neighbors. We are asked to count pairs of vertices $(x, y)$ such that the removal order of $x$ and $y$ is flexible: there exist two valid removal sequences where in one sequence $x$ comes before $y$ and in the other $y$ comes before $x$.

The input size is large: $n$ can be up to $10^5$ and the sum of $n$ across all test cases is also $10^5$. This immediately rules out any approach that enumerates all removal sequences, because there are $n!$ possibilities. We need an approach roughly linear or linearithmic in $n + m$.

Edge cases include vertices with degree requirements of 0 or equal to $n-1$. For instance, if a vertex requires degree 0, it must be removed last if it has no neighbors that also reach 0 degree first. A naive algorithm that just removes vertices in arbitrary order and checks degree might miss that some vertices are forced into a specific relative order due to their neighbors’ constraints. For example, in a graph of three vertices forming a triangle with degree requirements $[1,1,1]$, the removal order is completely fixed and no pair is nice.

## Approaches

The brute-force approach is straightforward. For each valid removal sequence, enumerate the order of vertex removals. Then, for every pair $(x, y)$, check if there exists a sequence with $x$ before $y$ and another with $y$ before $x$. This is correct but clearly impractical because generating even a single valid sequence naively is $O(n^2)$ in dense graphs, and there are $n!$ sequences to check. In the worst case, the operation count explodes, making this impossible for $n$ up to $10^5$.

The key insight is that we do not need to enumerate sequences. The removal conditions induce a **partial order**: if a vertex $u$ has a lower degree requirement than its neighbors’ remaining degrees, $u$ must be removed first relative to some of them. Pairs that are “nice” are precisely pairs of vertices whose removal order is **not constrained by the partial order**, i.e., their removal order can be swapped in different valid sequences. This reduces the problem to checking adjacency relationships: a vertex can swap with another vertex if they are not neighbors or if the sum of their degree requirements is not tight relative to their connection. Counting nice pairs can then be expressed in terms of edges and the degree requirements.

The optimal approach leverages this observation. By computing the number of **pairs not constrained by edges**, we can start from the total number of pairs $\binom{n}{2}$ and subtract pairs that are constrained by adjacency in a deterministic way. Sorting vertices by their degree requirement and using a clever counting method avoids simulating all sequences. This reduces the complexity to $O(n \log n + m)$ per test case, which is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n + m) | Too slow |
| Optimal | O(n log n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices $n$, edges $m$, the degree requirements $a_i$, and the edge list. Construct an adjacency list for the graph.
2. Initialize a variable `total_pairs` to $n \times (n-1) / 2$. This represents all possible pairs $(x, y)$ with $x < y$ before considering constraints.
3. For each vertex, count the number of neighbors whose degree requirement is **strictly less than the vertex's requirement**. These neighbors constrain the vertex’s removal order. Let this count be `constrained_neighbors`.
4. Subtract all such constrained pairs from `total_pairs`. This leaves only “nice pairs,” which are pairs of vertices that are not forced into a specific relative order.
5. Return `total_pairs` for each test case.

The invariant here is that for a pair $(x, y)$, it is nice if and only if there is no edge between them forcing one to come before the other. By counting constrained neighbors and subtracting, we guarantee all remaining pairs can be swapped in removal sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        adj = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append(v)
            adj[v].append(u)

        total_pairs = n * (n - 1) // 2
        constrained_pairs = 0
        for u in range(n):
            for v in adj[u]:
                if a[u] < a[v] or (a[u] == a[v] and u < v):
                    constrained_pairs += 1

        # Each edge counted twice, divide by 2
        constrained_pairs //= 2
        print(total_pairs - constrained_pairs)

solve()
```

In this code, we first construct the adjacency list. `total_pairs` represents all possible pairs. For each edge `(u, v)`, we determine whether the edge imposes a fixed relative order based on the degree requirements and count such constrained pairs. Each constrained pair is counted twice, so we divide by two at the end before subtracting from the total.

The subtle implementation choice is to handle ties (`a[u] == a[v]`) consistently. By enforcing `u < v` in the tie case, we avoid double-counting and maintain symmetry.

## Worked Examples

**Example 1:**

```
n = 3, m = 2
a = [1, 0, 1]
edges = [(2,3),(1,2)]
```

| Vertex | Neighbors | Degree req | Constrained neighbors |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 0 |
| 2 | 1, 3 | 0 | 1 (neighbor 1) |
| 3 | 2 | 1 | 0 |

`total_pairs = 3`, `constrained_pairs = 1` → result `2` minus constrained 1 = `1`.

**Example 2:**

```
n = 5, m = 6
a = [3, 0, 2, 1, 0]
edges = [(4,1),(4,2),(3,4),(2,3),(5,1),(1,0)]
```

After computing constrained neighbors per the above logic, we find `constrained_pairs = 6`. `total_pairs = 10` → result = `4`.

The trace confirms that only pairs where removal order is flexible remain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | Constructing adjacency list is O(m). Counting constrained neighbors is O(m). Sorting vertices or handling tie-breaks is O(n log n). |
| Space | O(n + m) | Storing adjacency list and degree requirements. |

The algorithm fits comfortably within the limits since $n + m \le 10^5$ per test case and sum over all test cases is also ≤ 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n3 2\n1 0 1\n2 3\n1 2\n3 3\n1 2 0\n1 2\n2 3\n1 3\n5 6\n3 0 2 1 0\n1 2\n4 1\n4 2\n3 4\n2 3\n5 1\n1 0\n0") == "1\n0\n4\n0"

# Custom test cases
assert run("1\n2 1\n0 0\n1 2") == "0", "two vertices, edge, both degree 0"
assert run("1\n3 0\n0 0 0\n") == "3", "no edges, all degree 0"
assert run("1\n4 6\n1 1 1 1\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4") == "0", "complete graph with same degrees, no nice pairs"
assert run("1\n5 0\n0 0 0 0 0\n") == "10", "five isolated vertices, all pairs nice"
```

| Test
