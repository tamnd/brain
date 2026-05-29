---
title: "CF 246D - Colorful Graph"
description: "We are given an undirected graph where each vertex has a color, represented by an integer. The goal is to determine which color has the most diverse set of neighboring colors."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 246
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 151 (Div. 2)"
rating: 1600
weight: 246
solve_time_s: 90
verified: true
draft: false
---

[CF 246D - Colorful Graph](https://codeforces.com/problemset/problem/246/D)

**Rating:** 1600  
**Tags:** brute force, dfs and similar, graphs  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph where each vertex has a color, represented by an integer. The goal is to determine which color has the most diverse set of neighboring colors. Formally, for each color $k$, we look at all vertices of that color and collect the colors of all adjacent vertices that are different from $k$. The color whose set of neighboring colors has the largest size is the answer. If multiple colors tie, we pick the smallest color number.

The graph can have up to $10^5$ vertices and edges, so an algorithm with complexity higher than $O(n + m)$ or $O((n + m)\log n)$ will likely time out. We also need to manage colors that can be as high as $10^5$, so creating arrays directly indexed by color could be memory-intensive if done naively.

A few non-obvious edge cases are critical. First, a graph where all vertices have the same color. For example, with 3 vertices all colored 1 and edges 1-2, 2-3, 1-3, there are no distinct neighboring colors, so the output must still be 1, the only color. Second, if multiple colors have the same maximum diversity, we must select the smallest one, not the first we encounter. Lastly, disconnected vertices or components with isolated colors do not contribute neighbors, but the color still counts for consideration if present.

## Approaches

The brute-force method is to consider each color $k$ independently. For every vertex of color $k$, scan its adjacency list and add all differing neighbor colors into a set. Once we process all vertices of $k$, we know the cardinality of $Q(k)$. Repeating this for all colors guarantees correctness, but it is too slow because iterating over all vertices for each color can lead to $O(n \cdot m)$ operations in dense graphs.

The key insight to optimize is that we do not need to process every vertex for every color. Each edge only connects two vertices, and it contributes to the diversity counts of at most two colors: the colors of its endpoints if they are different. Therefore, we can iterate over all edges once, and for each edge connecting vertices $u$ and $v$ with different colors, we add $c[v]$ to the set of neighboring colors of $c[u]$ and $c[u]$ to the set of neighboring colors of $c[v]$. This reduces the problem from scanning all adjacency lists repeatedly to a single pass over edges. The rest is bookkeeping to maintain these sets and find the color with the largest set size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(n) per color | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph vertices, colors, and edges. Maintain a mapping from vertex index to color.
2. Initialize an empty dictionary to store for each color the set of neighboring colors.
3. For each edge $u, v$, check if the colors of $u$ and $v$ differ. If so, insert the color of $v$ into the neighbor set of $c[u]$, and the color of $u$ into the neighbor set of $c[v]$. This ensures each color's set counts only distinct neighbor colors.
4. After processing all edges, iterate through all colors present in the graph. Keep track of the color with the maximum size of neighbor set. If multiple colors have the same maximum size, select the smallest one.
5. Output the selected color.

Why it works: every edge that connects two different colors contributes exactly once to the neighbor diversity count of each color. The invariant is that the set of neighbor colors for each color is precisely the union of all colors of vertices adjacent to any vertex of that color. By using sets, we automatically avoid duplicates. Therefore, the maximum cardinality is correctly computed.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

n, m = map(int, input().split())
colors = list(map(int, input().split()))
edges = [tuple(map(int, input().split())) for _ in range(m)]

# Map color to its set of neighboring colors
neighbor_colors = defaultdict(set)

for u, v in edges:
    u -= 1
    v -= 1
    cu, cv = colors[u], colors[v]
    if cu != cv:
        neighbor_colors[cu].add(cv)
        neighbor_colors[cv].add(cu)

# Ensure every color present in graph has an entry (even isolated)
unique_colors = set(colors)
for color in unique_colors:
    neighbor_colors[color]  # touch entry to ensure existence

# Find color with maximum neighbor diversity, tie-breaking by smallest color
max_diversity = -1
best_color = None
for color in neighbor_colors:
    diversity = len(neighbor_colors[color])
    if diversity > max_diversity or (diversity == max_diversity and color < best_color):
        max_diversity = diversity
        best_color = color

print(best_color)
```

The code first builds the neighbor sets, then ensures all present colors have a corresponding entry to handle isolated colors. Finally, it searches for the maximum diversity while respecting the tie-breaking rule. Care is taken to decrement indices for 1-based input.

## Worked Examples

**Sample 1:**

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

| Vertex | Color | Neighboring colors (after processing all edges) |
| --- | --- | --- |
| 1 | 1 | {2, 3} |
| 2 | 1 | {2, 3} |
| 3 | 2 | {1, 3} |
| 4 | 3 | {1, 2, 5, 8} |
| 5 | 5 | {3} |
| 6 | 8 | {3} |

The set sizes per color:

| Color | Neighbor Diversity |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 4 |
| 5 | 1 |
| 8 | 1 |

Maximum diversity is 4 for color 3, which is printed.

**Custom Example 2: All vertices same color**

Input:

```
3 2
1 1 1
1 2
2 3
```

Each vertex has color 1 and all edges connect vertices of the same color. Neighbor sets are empty. Maximum diversity is 0, the only color present is 1. Output:

```
1
```

This confirms isolated or non-diverse colors are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One pass to read input, one pass through edges to fill neighbor sets, one pass over colors to select maximum. |
| Space | O(n + m) | Neighbor sets per color and storage for edges. |

Given the constraints, with $n, m \le 10^5$, this runs efficiently within the 2-second limit.

## Test Cases

```python
import sys, io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    colors = list(map(int, input().split()))
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    neighbor_colors = defaultdict(set)
    for u, v in edges:
        u -= 1
        v -= 1
        cu, cv = colors[u], colors[v]
        if cu != cv:
            neighbor_colors[cu].add(cv)
            neighbor_colors[cv].add(cu)
    for color in set(colors):
        neighbor_colors[color]
    max_div = -1
    best = None
    for color in neighbor_colors:
        div = len(neighbor_colors[color])
        if div > max_div or (div == max_div and color < best):
            max_div = div
            best = color
    return str(best)

# provided sample
assert run("6 6\n1 1 2 3 5 8\n1 2\n3 2\n1 4\n4 3\n4 5\n4 6\n") == "3", "sample 1"

# custom cases
assert run("3 2\n1 1 1\n1 2\n2 3\n") == "1", "all same color"
assert run("4 2\n1 2 3 4\n1 2\n3 4\n") == "1", "tie between 1 and 3, pick smaller"
assert run("5 0\n10 20 30 40 50\n") == "10", "no edges, smallest color"
assert run("5 4\n1 2 3 2 1\n1 2\n2 3\n3 4\n4 5\n") == "2", "diversity across middle color"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2, all 1 | 1 | handles all same-color vertices |
| 4 2, colors 1-4 | 1 | tie-breaking selects smallest |
