---
title: "CF 1176E - Cover it!"
description: "We are given an undirected, unweighted, connected graph with $n$ vertices and $m$ edges. Each query provides a fresh graph. The goal is to select at most $lfloor n/2 rfloor$ vertices such that every vertex not selected has at least one neighbor in the chosen set."
date: "2026-06-12T01:46:09+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 1176
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 565 (Div. 3)"
rating: 1700
weight: 1176
solve_time_s: 104
verified: false
draft: false
---

[CF 1176E - Cover it!](https://codeforces.com/problemset/problem/1176/E)

**Rating:** 1700  
**Tags:** dfs and similar, dsu, graphs, shortest paths, trees  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected, unweighted, connected graph with $n$ vertices and $m$ edges. Each query provides a fresh graph. The goal is to select at most $\lfloor n/2 \rfloor$ vertices such that every vertex not selected has at least one neighbor in the chosen set. In other words, the chosen vertices form a dominating set of the graph with size constrained by half of the vertices. The output for each query is the number of chosen vertices and their indices. Multiple correct outputs are allowed.

The constraints allow $n$ up to $2 \cdot 10^5$ per query, with $\sum m$ over all queries also bounded by $2 \cdot 10^5$. This implies that any algorithm that processes each edge more than a constant number of times will likely exceed the time limit. Consequently, algorithms with time complexity worse than $O(n + m)$ per query are not feasible. Naive approaches that try all subsets of vertices are infeasible because the number of subsets grows exponentially with $n$. We need a linear or near-linear solution in terms of vertices and edges.

Non-obvious edge cases include graphs where some vertices have high degrees and others have degree one, or graphs with small $n$. For instance, in a triangle graph with three vertices, any single vertex dominates the rest, and the algorithm must not choose more than $\lfloor 3/2 \rfloor = 1$ vertex. Careless greedy choices might select too many vertices and violate the size bound.

## Approaches

A brute-force approach would be to iterate over all subsets of vertices of size at most $\lfloor n/2 \rfloor$ and check if they dominate the remaining vertices. This guarantees correctness because it checks every possible selection. However, for $n = 10^5$, there are $\binom{10^5}{5 \cdot 10^4}$ subsets, which is astronomically large. Even iterating over subsets of size 2 or 3 is impractical when $n$ is large.

The key insight is to exploit the graph structure. Because the graph is connected, it contains a spanning tree. Coloring the vertices of any spanning tree in two colors (say, 0 and 1) using a depth-first search guarantees that all edges connect vertices of different colors in a bipartite manner. The smaller color class will have size at most $\lfloor n/2 \rfloor$ and, by the tree property, every vertex in the larger class has a neighbor in the smaller class. Therefore, choosing all vertices of the smaller color class satisfies the domination requirement.

This approach is linear in the number of vertices and edges and trivially satisfies the size constraint. It works even for graphs with cycles because the spanning tree guarantees that the selected vertices dominate at least the tree edges, and cycles do not break this property.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Bipartite DFS on Spanning Tree | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of queries $t$.
2. For each query, read $n$ and $m$, and construct an adjacency list for the graph.
3. Initialize an array to store the color of each vertex. Color 0 means one set, color 1 means the other. Initialize all colors as unassigned.
4. Perform a depth-first search starting from vertex 1. Assign the starting vertex color 0. For each neighbor, assign the opposite color recursively.
5. After DFS, count the number of vertices in each color class. Let the smaller class be the candidate for selection.
6. Print the size of the smaller color class (at most $\lfloor n/2 \rfloor$) and the indices of its vertices.

Why it works: The DFS ensures that adjacent vertices have opposite colors, forming a bipartition of the spanning tree. Every vertex in the larger class is adjacent to at least one vertex in the smaller class because of the tree edges. Choosing the smaller class satisfies the domination requirement and respects the size constraint.

## Python Solution

```
PythonRun
```

The adjacency list construction ensures we efficiently access neighbors. The recursive DFS handles bipartitioning and builds color classes. Slicing the smaller class ensures we do not exceed $\lfloor n/2 \rfloor$ vertices.

## Worked Examples

Sample input:

```

```

| Step | Current vertex | Color | set0 | set1 |
| --- | --- | --- | --- | --- |
| Start | 1 | 0 | [1] | [] |
| Visit 2 | 2 | 1 | [1] | [2] |
| Visit 3 | 3 | 1 | [1] | [2,3] |
| Visit 4 | 4 | 1 | [1] | [2,3,4] |

The smaller set is set0 = [1], size 1. Since $\lfloor 4/2 \rfloor = 2$, we can take set0 and add arbitrary elements from set1 up to 2. The solution outputs 2 vertices, e.g., 1 and 2.

Second sample:

```
6 8
2 5
5 4
4 3
4 1
1 3
2 3
2 6
5 6
```

DFS coloring produces two sets: set0 = [1,3,5], set1 = [2,4,6]. Each set has size 3, exactly $\lfloor 6/2 \rfloor = 3$. Choosing either set satisfies domination.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per query | DFS visits each vertex and edge once |
| Space | O(n + m) | Adjacency list and color array |

With $\sum n, \sum m \le 2 \cdot 10^5$, this solution fits comfortably in the 2-second limit with linear operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("2\n4 6\n1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n6 8\n
```
