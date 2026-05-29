---
title: "CF 246D - Colorful Graph"
description: "We are asked to analyze an undirected graph where each vertex has a color. For every color that appears in the graph, we want to compute how many distinct colors appear among its neighboring vertices."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 246
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 151 (Div. 2)"
rating: 1600
weight: 246
solve_time_s: 57
verified: true
draft: false
---

[CF 246D - Colorful Graph](https://codeforces.com/problemset/problem/246/D)

**Rating:** 1600  
**Tags:** brute force, dfs and similar, graphs  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to analyze an undirected graph where each vertex has a color. For every color that appears in the graph, we want to compute how many _distinct colors_ appear among its neighboring vertices. Formally, if you pick all vertices of a particular color, look at all edges that connect these vertices to other vertices of a different color, and count the number of unique colors you see, that is the "neighbor color diversity" for that color. Our task is to find the color with the largest neighbor diversity. If multiple colors tie, we select the smallest one numerically.

The input provides the number of vertices $n$, the number of edges $m$, the color of each vertex as a list of integers, and then the list of edges. The output is a single integer: the color with the maximum diversity among neighbors.

The constraints are significant: $n$ and $m$ can each be up to $10^5$. This rules out algorithms with $O(n \cdot m)$ or $O(n^2)$ complexity. An approach that examines each vertex’s neighbors multiple times naively could easily require $10^{10}$ operations, which is not feasible in a 2-second time limit. We must aim for something closer to $O(n + m)$ or $O(m \log n)$ in practice.

Subtle edge cases include graphs where all vertices have the same color, or a color is isolated with no differently-colored neighbors. For example, a graph of three vertices all colored 1, with edges between them, should produce 1 as the output with a neighbor diversity of 0. A careless implementation that assumes every color has neighbors of different colors could fail here. Another edge case is when multiple colors tie for maximum diversity, requiring the smallest numerical color to be chosen.

## Approaches

The brute-force approach is straightforward. For each color $k$, collect all vertices of color $k$. Then, for each such vertex, iterate over its neighbors and record the colors that are not $k$. Finally, count the distinct colors for each $k$ and track the maximum. This works because it directly implements the definition of neighbor diversity, but it is too slow for large graphs. In the worst case, with 100,000 vertices each connected to 100,000 edges, this can result in $O(n \cdot m)$ operations, which is $10^{10}$.

The key insight to optimize is that we do not need to iterate over all vertices by color explicitly. Instead, we can process edges directly: for each edge connecting vertices $u$ and $v$, we only care if the colors differ. If they do, we can record that color $c[u]$ sees color $c[v]$ as a neighbor and vice versa. Using a dictionary of sets keyed by color allows us to accumulate neighbor colors efficiently in $O(m)$ time since each edge is processed once. This reduces the problem from a vertex-focused approach to an edge-focused approach, which is linear in the number of edges and vertices combined.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read input values: number of vertices $n$, number of edges $m$, the list of vertex colors, and the list of edges. Store vertex colors in a list indexed from 1 to $n$.
2. Initialize a dictionary where each key is a color and each value is a set of neighboring colors. This will allow us to track neighbor diversity without duplicates.
3. For each edge connecting vertices $u$ and $v$, compare their colors. If the colors differ, add $c[v]$ to the neighbor set of $c[u]$ and $c[u]$ to the neighbor set of $c[v]$. This ensures that each color only counts distinct neighbors, and we do not double-count within the same edge.
4. Initialize variables to track the best color and the maximum diversity observed so far. Iterate over all colors that appear in the dictionary. If a color’s neighbor set has a larger size than the current maximum, update the best color. If the size is equal, take the numerically smaller color.
5. Print the best color at the end.

The reason this works is that each edge contributes exactly to the sets of neighbor colors for the two colors it connects, ensuring we account for all distinct neighboring colors. Using sets guarantees that duplicates are eliminated automatically. By iterating over the keys of this dictionary, we only consider colors present in the graph, and comparing set sizes ensures we select the color with maximum neighbor diversity.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
colors = list(map(int, input().split()))

from collections import defaultdict

neighbor_colors = defaultdict(set)

for _ in range(m):
    u, v = map(int, input().split())
    cu, cv = colors[u - 1], colors[v - 1]
    if cu != cv:
        neighbor_colors[cu].add(cv)
        neighbor_colors[cv].add(cu)

best_color = colors[0]
max_diversity = -1

for color in set(colors):
    diversity = len(neighbor_colors[color])
    if diversity > max_diversity or (diversity == max_diversity and color < best_color):
        max_diversity = diversity
        best_color = color

print(best_color)
```

The solution begins by reading input efficiently with `sys.stdin.readline`. Colors are stored in a zero-indexed list, so we adjust edge indices accordingly. We use `defaultdict(set)` to accumulate neighboring colors, ensuring duplicates are ignored automatically. When iterating to find the best color, we only consider colors that appear in the graph, and we maintain both the diversity count and the numerical tie-breaking logic.

## Worked Examples

### Sample 1

Input:

```
6 6
1 1 2 3 5 8
1 2
3 2
1 4
4 3
4 5
4 6
```

| Step | neighbor_colors | max_diversity | best_color |
| --- | --- | --- | --- |
| After edge 1-2 | {1: {1}, 1: {1}} | -1 | 1 |
| After edge 3-2 | {1: {2}, 2: {1}} | -1 | 1 |
| After edge 1-4 | {1: {2,3}, 2:{1}, 3:{1}} | -1 | 1 |
| After edge 4-3 | unchanged | -1 | 1 |
| After edge 4-5 | {1:{2,3}, 2:{1},3:{1,5},5:{3}} | -1 | 1 |
| After edge 4-6 | {1:{2,3}, 2:{1},3:{1,5,8},5:{3},8:{3}} | -1 | 1 |
| Final iteration | compute diversities | 3 | 3 |

The table shows how edges update neighbor sets, and at the end, color 3 has neighbors {1, 5, 8}, which is the maximum diversity of 3.

### Custom Small Example

Input:

```
3 2
1 2 1
1 2
2 3
```

| Step | neighbor_colors | max_diversity | best_color |
| --- | --- | --- | --- |
| After edges | {1:{2},2:{1},1:{2}} | -1 | 1 |
| Final | 1: 1, 2:1 | 1 | 1 |

Here, both colors have diversity 1, so the smaller color 1 is chosen.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each edge is processed once, each color is processed once. |
| Space | O(n + m) | Each color stores sets of neighboring colors, in worst case all edges connect distinct colors. |

The algorithm is comfortably within constraints: $10^5 + 10^5$ operations are well under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    colors = list(map(int, input().split()))
    from collections import defaultdict
    neighbor_colors = defaultdict(set)
    for _ in range(m):
        u, v = map(int, input().split())
        cu, cv = colors[u - 1], colors[v - 1]
        if cu != cv:
            neighbor_colors[cu].add(cv)
            neighbor_colors[cv].add(cu)
    best_color = colors[0]
    max_diversity = -1
    for color in set(colors):
        diversity = len(neighbor_colors[color])
        if diversity > max_diversity or (diversity == max_diversity and color < best_color):
            max_diversity = diversity
            best_color = color
    return str(best_color)

# Provided sample
assert run("6 6\n1 1 2 3 5 8\n1 2\n3 2\n1 4\n4 3\n4 5\n4 6\n") == "3"

# Custom cases
```
