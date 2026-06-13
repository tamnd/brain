---
title: "CF 1198E - Rectangle Painting 2"
description: "We are given an extremely large $n times n$ grid, but instead of listing individual black cells, the input describes black regions as up to 50 axis-aligned rectangles. Every cell outside these rectangles is white initially, and inside them is black."
date: "2026-06-13T14:47:37+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graph-matchings", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1198
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 576 (Div. 1)"
rating: 2500
weight: 1198
solve_time_s: 254
verified: false
draft: false
---

[CF 1198E - Rectangle Painting 2](https://codeforces.com/problemset/problem/1198/E)

**Rating:** 2500  
**Tags:** flows, graph matchings, graphs  
**Solve time:** 4m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an extremely large $n \times n$ grid, but instead of listing individual black cells, the input describes black regions as up to 50 axis-aligned rectangles. Every cell outside these rectangles is white initially, and inside them is black.

The task is to repaint the grid so that every cell becomes white. The only allowed operation is selecting any axis-aligned rectangle and painting it white. The cost of an operation depends only on the rectangle dimensions: for a rectangle of height $h$ and width $w$, the cost is $\min(h, w)$. Multiple operations are allowed, and rectangles may overlap.

The goal is to cover all initially black cells using a set of such painting operations with minimum total cost. White cells never matter because repainting them again is harmless, so the problem is entirely about covering the union of the given black rectangles efficiently.

The key difficulty comes from the scale. The grid size $n$ can be as large as $10^9$, so we cannot work on individual cells. All structure must come from the at most 50 input rectangles.

A naive interpretation would try to simulate painting decisions over the whole grid or consider all possible rectangles. That is impossible because the number of possible rectangles is $O(n^4)$, and even restricting endpoints to black rectangle boundaries would still be far too large without further structure.

A subtle failure case for naive greedy thinking is when rectangles overlap in a way that makes local decisions misleading. For example, two intersecting black rectangles:

```
n = 10
(1,1)-(6,6)
(4,4)-(10,10)
```

A greedy approach might paint each rectangle separately with cost 5 and 6, giving 11. But an optimal solution may split the union region into structured subrectangles and reuse cheaper cuts, potentially reducing cost significantly by exploiting shared boundaries. This shows that decisions must be global over geometry, not per input rectangle.

Another subtle case is when a large rectangle is almost empty except for a thin strip of black cells. Painting the whole bounding box is expensive due to min(h,w), but splitting around empty regions can drastically reduce cost. This again suggests we need a decomposition over structure rather than direct covering.

## Approaches

A brute-force idea is to consider every possible rectangle in the grid and decide whether to paint it or not, ensuring all black cells are covered. This is conceptually correct: we are choosing a set of rectangles whose union covers all black cells. However, even if we restrict rectangle boundaries to the input coordinates, there are still $O(k^4)$ candidate rectangles, where $k$ is the number of unique x and y boundaries, up to about 100. That gives around $10^8$ rectangles, and for each we would need to reason about overlaps and coverage, which quickly becomes infeasible.

The key structural insight is that only the boundaries of the given rectangles matter. Any optimal solution can be assumed to align all rectangle edges with the x and y coordinates appearing in the input. This reduces the infinite grid into a compressed grid of at most $2m$ distinct x-coordinates and $2m$ distinct y-coordinates.

Once the grid is compressed, we consider every subrectangle in this reduced coordinate system. For each subrectangle, we compute whether it contains any black cell using a 2D prefix sum. If it contains no black cells, its cost is zero because it needs no coverage. Otherwise, we have three meaningful options: we can paint the whole subrectangle at cost $\min(h,w)$, or split it horizontally into two smaller subrectangles, or split it vertically. Each split reduces the problem into independent subproblems.

This naturally leads to a interval dynamic programming formulation over 2D segments, where each state represents a compressed rectangle and transitions correspond to horizontal or vertical cuts. The cost structure ensures optimal substructure because painting decisions on disjoint regions do not interact.

The critical reason this works is that the cost function depends only on rectangle shape, not position or content, and splits preserve independence between subproblems.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all rectangles | $O(k^4)$ or worse | $O(k^2)$ | Too slow |
| Coordinate compression + DP | $O(k^4)$ with small $k \le 100$ | $O(k^4)$ | Accepted |

## Algorithm Walkthrough

1. Extract all x-coordinates and y-coordinates from rectangle corners and sort them, removing duplicates. This defines compressed coordinate axes. The reason this works is that any meaningful cut or boundary in an optimal solution must align with an input rectangle edge, since no cost structure encourages arbitrary positions.
2. Build a compressed grid where each cell corresponds to a region between consecutive x and y coordinates. Mark which compressed cells are black using a 2D difference array or direct marking from input rectangles.
3. Build a 2D prefix sum over the compressed grid so that we can check in constant time whether any subrectangle contains at least one black cell.
4. Define a DP state $dp[x1][x2][y1][y2]$ as the minimum cost to paint all black cells inside the subrectangle defined by compressed coordinates. This captures the idea that we solve independently for every geometric subproblem.
5. If the subrectangle contains no black cells, set $dp = 0$. This is a base case because no operation is needed.
6. Otherwise compute the cost of painting the entire subrectangle at once, which is $\min(\text{width}, \text{height})$. This represents the strategy of covering everything in one operation.
7. Try all horizontal splits between $y1$ and $y2$, splitting the rectangle into two smaller rectangles and combining their DP values. This captures the possibility of separating independent horizontal bands of black cells.
8. Try all vertical splits between $x1$ and $x2$, similarly combining results from left and right subrectangles. This captures vertical decomposition.
9. Take the minimum over painting the whole rectangle and all possible splits. This ensures we consider both global coverage and recursive decomposition.

### Why it works

The correctness comes from the fact that any valid painting strategy induces a partition of the plane into regions covered by individual operations. If an operation crosses a potential split line, that line can be chosen from the finite set of coordinates without loss of generality, because rectangle boundaries in the input define all meaningful interaction points.

This means every optimal solution can be transformed into one where cuts only happen along compressed grid lines, and each subrectangle is solved independently. The DP enumerates exactly these decompositions, so it must reach the optimal cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    rects = []
    xs = set()
    ys = set()

    for _ in range(m):
        x1, y1, x2, y2 = map(int, input().split())
        rects.append((x1, y1, x2, y2))
        xs.add(x1); xs.add(x2)
        ys.add(y1); ys.add(y2)

    xs = sorted(xs)
    ys = sorted(ys)

    xid = {x:i for i, x in enumerate(xs)}
    yid = {y:i
```
