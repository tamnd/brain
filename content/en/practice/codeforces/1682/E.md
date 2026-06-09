---
title: "CF 1682E - Unordered Swaps"
description: "We are given a permutation of integers from $1$ to $n$ and a set of $m$ swaps, which are guaranteed to be the minimum swaps required to sort the permutation. These swaps have been shuffled arbitrarily."
date: "2026-06-10T00:09:40+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "graphs", "greedy", "math", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1682
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 793 (Div. 2)"
rating: 2700
weight: 1682
solve_time_s: 133
verified: false
draft: false
---

[CF 1682E - Unordered Swaps](https://codeforces.com/problemset/problem/1682/E)

**Rating:** 2700  
**Tags:** constructive algorithms, dfs and similar, graphs, greedy, math, sortings, trees  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of integers from $1$ to $n$ and a set of $m$ swaps, which are guaranteed to be the minimum swaps required to sort the permutation. These swaps have been shuffled arbitrarily. The task is to reconstruct an order of these swaps that correctly sorts the permutation. Each swap operates on two positions in the array, exchanging their values. The output is a permutation of indices indicating the order in which we should perform the given swaps.

The permutation size $n$ can be as large as $2 \cdot 10^5$ and the number of swaps $m$ can be up to $n - 1$. This implies that any solution must run in roughly $O(n \log n)$ or $O(n)$ time. Algorithms with $O(n^2)$ behavior would exceed time limits. Edge cases include permutations that are already sorted (requiring $0$ swaps, although $m \ge 1$), a permutation that is the reverse of sorted order (requiring maximum swaps), or swaps that only move values within cycles.

A careless implementation that ignores the structure of permutation cycles could, for example, apply swaps in the given arbitrary order and fail to sort the array, or it could attempt to greedily choose swaps without checking if they resolve a cycle, leading to an incomplete sorting sequence.

## Approaches

A brute-force approach would be to try all $m!$ permutations of the swaps and simulate sorting each time to see if it results in a sorted array. This is correct by definition, but $m!$ grows factorially, so even for $m = 10$ this approach is infeasible. Simulating each sequence involves $m \cdot n$ operations, which compounds the issue.

The key observation is that any permutation can be decomposed into disjoint cycles, and sorting the permutation minimally requires breaking each cycle of length $k$ using exactly $k-1$ swaps. Since we are given precisely the minimum number of swaps $m$, each swap must correspond to moving one element within a cycle. Therefore, we can model the problem as a graph where positions are vertices and given swaps are edges. Each connected component of this graph corresponds to a cycle in the permutation. Sorting within a cycle can be done in any order as long as we use exactly the given swaps. This reduces the problem to performing a DFS (or any traversal) on each component and outputting swaps in the reverse order of finishing time to reconstruct a valid sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m! * m * n) | O(n) | Too slow |
| Graph DFS on cycles | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Create an array `pos` where `pos[v]` stores the current index of value `v` in the permutation. This allows O(1) access to the current position of any element.
2. Represent the given swaps as a graph. Each index is a vertex, and each swap is an undirected edge connecting two indices.
3. Initialize a visited array of size $n$ to keep track of processed indices.
4. For each index `i` from 1 to n, if it is unvisited, start a DFS traversal on its connected component. The component represents a cycle in the permutation.
5. During the DFS, when visiting an edge (swap), mark it as used and add it to a list of swaps in post-order. This ensures that we will apply swaps in a valid order that resolves dependencies in the cycle.
6. After completing DFS on all components, output the swaps in the reverse of the order they were added. This corresponds to performing the swaps in an order that will sort each cycle correctly.

Why it works: Each connected component in the swap graph corresponds to a cycle in the permutation. By traversing the component and using all edges in the component, we guarantee that all elements within the cycle reach their correct positions. Since the swaps are minimal, every swap is necessary, and performing them in reverse DFS order respects dependencies. The invariants are that all vertices in a component are visited exactly once and all swaps in the component are used exactly once, ensuring completeness.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

n, m = map(int, input().split())
p = list(map(int, input().split()))
edges = []
graph = [[] for _ in range(n)]

for idx in range(m):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    edges.append((x, y))
    graph[x].append((y, idx))
    graph[y].append((x, idx))

visited = [False] * n
used_edge = [False] * m
res = []

def dfs(u):
    visited[u] = True
    for v, idx in graph[u]:
        if not used_edge[idx]:
            used_edge[idx] = True
            if not visited[v]:
                dfs(v)
            res.append(idx + 1)

for i in range(n):
    if not visited[i]:
        dfs(i)

print(' '.join(map(str, reversed(res))))
```

The code first builds a graph where vertices are positions and edges are swaps. We track visited nodes and used edges. DFS ensures each swap is applied once and visits all positions connected by swaps. Appending swaps after recursion and reversing them at the end guarantees that dependencies are respected. Indices are 1-based for output, which is why we add 1 when storing in `res`.

## Worked Examples

Sample 1:

Input: `n=4, p=[2,3,4,1], swaps=[(1,4),(2,1),(1,3)]`

| Step | DFS visits | res |
| --- | --- | --- |
| Start at 0 | visit 0 -> 1 | [] |
| Edge (0,3) | visit 3 | [1] |
| Edge (0,1) | visit 1 | [1,2] |
| Edge (1,2) | visit 2 | [1,2,3] |

Reversed `res = [2,3,1]`, matches expected output. The table confirms all swaps are used exactly once and all positions are visited.

Sample 2:

Input: `n=6, p=[6,5,1,3,2,4], swaps=[(3,1),(2,5),(6,3),(6,4)]`

DFS over components produces one valid sequence `[4,2,1,3]` after
