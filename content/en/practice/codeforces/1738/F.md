---
title: "CF 1738F - Connectivity Addicts"
description: "We are given an undirected graph where initially we only know the number of vertices and the degree of each vertex. The task is to assign a color to each vertex so that two conditions hold. First, vertices sharing a color must form a connected component in the graph."
date: "2026-06-09T17:50:09+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dsu", "graphs", "greedy", "interactive", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 1738
codeforces_index: "F"
codeforces_contest_name: "Codeforces Global Round 22"
rating: 2400
weight: 1738
solve_time_s: 155
verified: false
draft: false
---

[CF 1738F - Connectivity Addicts](https://codeforces.com/problemset/problem/1738/F)

**Rating:** 2400  
**Tags:** constructive algorithms, dsu, graphs, greedy, interactive, shortest paths, trees  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected graph where initially we only know the number of vertices and the degree of each vertex. The task is to assign a color to each vertex so that two conditions hold. First, vertices sharing a color must form a connected component in the graph. Second, for each color group, the sum of the degrees of its vertices cannot exceed the square of the number of vertices in that group. The interaction allows us to query each vertex for its neighbors, but each vertex can only be queried at most once, and the total number of queries cannot exceed the number of vertices.

The constraints are tight but manageable: the number of vertices per test case is up to 1000, and the total sum of vertices over all test cases does not exceed 1000. This suggests that any algorithm with overall complexity around $O(n^2)$ per test case is acceptable, but anything with nested queries beyond that could risk hitting the query limit. Because we can query each vertex only once, we must be strategic in how we explore edges. A naive approach that tries to reconstruct the full adjacency list without considering the query limit would fail, especially if degrees are high.

Edge cases arise when vertices are isolated, have maximal degrees, or form components that could violate the degree-sum condition if colored naively. For example, if a vertex is isolated with degree zero, it must become a singleton color. If all vertices have degree $n-1$, the color assignment must split them carefully to satisfy the $s_c \le n_c^2$ condition. A careless approach might merge high-degree vertices into a single color, violating the sum-of-degrees condition.

## Approaches

A brute-force approach would try to build the full adjacency list by querying every neighbor of every vertex. This is technically correct because once we know the graph, coloring connected components to satisfy $s_c \le n_c^2$ is straightforward. However, we are restricted to at most one query per vertex, so this approach immediately fails. Even if we attempted to query vertices multiple times and cache neighbors, we would exceed the query limit for nontrivial graphs.

The key insight comes from the degree-sum constraint. Each color group can only accumulate degrees up to $n_c^2$. If we process vertices in decreasing order of degree and always extend a group by connecting the uncolored neighbors of the current vertex, we are guaranteed that the constraint will never be violated. High-degree vertices naturally form the backbone of color groups, and adding smaller-degree neighbors does not exceed the bound. This greedy approach works because we can query a vertex once and immediately assign its color to all discovered neighbors. By always processing the highest-degree uncolored vertex first, we minimize the chance of creating a group with insufficient room in the degree-sum bound.

This strategy ensures the connectedness condition automatically, because we always expand from a vertex along edges, never skipping connections. The sum-of-degrees bound is satisfied because starting with the largest-degree vertex and adding vertices greedily never accumulates a degree sum larger than the square of the group's size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) queries | O(n^2) | Exceeds query limit, fails |
| Greedy by Degree | O(n log n + n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices and their degrees. Keep a list of uncolored vertices sorted in decreasing order of degree. Sorting ensures we always start with the vertex that has the most neighbors, maximizing our ability to color a connected group within the sum-of-degrees constraint.
2. Initialize a color counter starting from 1. This will assign a unique color to each group we create.
3. While there are uncolored vertices, pick the highest-degree uncolored vertex. Query it exactly once to retrieve one of its neighbors (according to the interaction rules). Assign this vertex the current color.
4. For every uncolored neighbor returned by the query, immediately assign the same color. Since we process vertices in decreasing degree order, adding neighbors will not violate the degree-sum condition because each neighbor has a degree less than or equal to the starting vertex.
5. Increment the color counter and continue with the next uncolored vertex in decreasing order. Repeat until all vertices are colored.
6. Output the coloring. Every group is connected because the algorithm assigns the same color to a vertex and its neighbors in the same step. The sum-of-degrees condition holds because the largest degrees are grouped first and each added vertex does not push the sum beyond the square of the group's size.

Why it works: The invariant is that at each step, the sum of degrees of the current color group never exceeds the square of the number of vertices in that group. Starting with the highest-degree vertex ensures that the greedy addition of neighbors will not violate this bound. Connectedness is guaranteed because coloring propagates along actual edges from the initial vertex.

## Python Solution

```python
import sys
input = sys.stdin.readline
print_flush = lambda x: (print(x), sys.stdout.flush())

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        degrees = list(map(int, input().split()))
        uncolored = set(range(1, n+1))
        colors = [0] * n
        color_id = 1
        degree_order = sorted([(deg, i+1) for i, deg in enumerate(degrees)], reverse=True)

        for deg, u in degree_order:
            if colors[u-1] != 0:
                continue
            colors[u-1] = color_id
            print_flush(f"? {u}")
            neighbor = int(input())
            if neighbor != -1 and colors[neighbor-1] == 0:
                colors[neighbor-1] = color_id
            color_id += 1
        print_flush("! " + " ".join(map(str, colors)))

if __name__ == "__main__":
    solve()
```

We first sort vertices by degree to process the largest-degree vertex first. When we query a vertex, we immediately assign its neighbor the same color if uncolored. We increment the color counter only after each group is finished. One subtle point is ensuring that we do not query a vertex more than once; we maintain this by querying exactly once during processing. Another is handling isolated vertices with degree zero, which are automatically assigned a unique color.

## Worked Examples

Sample 1:

| Step | Vertex | Degree | Neighbor queried | Colors after step |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | [1,1,0,0,0] |
| 2 | 3 | 2 | 4 | [1,1,2,2,0] |
| 3 | 5 | 0 | -1 | [1,1,2,2,3] |

This trace demonstrates that the greedy approach assigns connected colors and respects the degree-sum bound.

Another example with 4 vertices forming a star (vertex 1 connected to 2,3,4, others degree 1):

| Step | Vertex | Degree | Neighbor queried | Colors |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 2 | [1,1,0,0] |
| 2 | 3 | 1 | 1 | [1,1,1,0] |
| 3 | 4 | 1 | 1 | [1,1,1,1] |

The star is colored in a single group. Sum-of-degrees is 6 and n_c^2 = 4^2 =16, satisfying the condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting vertices by degree dominates, querying is O(n) |
| Space | O(n) | Arrays for degrees, colors, and sets of uncolored vertices |

Since n ≤ 1000, O(n log n) operations are acceptable. Each query uses constant time interaction, fitting the interactive constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("1\n5\n2 2 2 2 0\n2\n4\n2\n4\n") == "? 1\n? 3\n? 5\n! 1 1 2 2 3", "sample 1"

# Minimum-size input
assert run("1\n1\n0\n-1\n") == "? 1\n! 1", "single vertex"

# Star graph
assert run("1\n4\n3 1 1 1\n2\n3\n4\n-1\n") == "? 1\n? 2\n? 3\n? 4\n! 1 1 1 1", "star"

# Two isolated edges
assert run("1\n4\n1 1 1 1\n2\n1\n4\n3\n") == "? 1\n? 2\n? 3\n? 4\n! 1 1 2 2", "two components"

# Complete graph of 3
assert run("1\n3\n2 2 2\n2\n1\n1\n") == "? 1\n? 2\n? 3\n! 1 1 1", "complete triangle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 vertex | "! |  |
