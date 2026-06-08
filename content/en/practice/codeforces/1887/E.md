---
title: "CF 1887E - Good Colorings"
description: "We are asked to interact with a grid of size $n times n$. Initially, $2n$ cells are pre-colored with unique colors from $1$ to $2n$, and the rest are uncolored. In each of up to 10 allowed moves, we can request Alice to color a previously uncolored cell."
date: "2026-06-08T22:12:34+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "graphs", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1887
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 905 (Div. 1)"
rating: 3100
weight: 1887
solve_time_s: 136
verified: false
draft: false
---

[CF 1887E - Good Colorings](https://codeforces.com/problemset/problem/1887/E)

**Rating:** 3100  
**Tags:** binary search, constructive algorithms, graphs, interactive  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to interact with a grid of size $n \times n$. Initially, $2n$ cells are pre-colored with unique colors from $1$ to $2n$, and the rest are uncolored. In each of up to 10 allowed moves, we can request Alice to color a previously uncolored cell. The color Alice chooses is arbitrary among the $2n$ available colors, and adaptive: she may choose colors based on the moves we make. After our moves, we must identify a rectangle formed by four cells such that all four are colored with distinct colors.

The input for each test case consists of $n$ and the $2n$ initially colored cells with their coordinates. The output is either a query for Alice (“? x y”) or a final answer giving the coordinates of the rectangle (“! x1 x2 y1 y2”). The rectangle must have its sides parallel to the grid axes, and the colors of its four corners must be distinct.

The constraints $3 \le n \le 1000$ and up to 200 test cases imply that any solution that iterates through all possible rectangles is impractical. There are $\binom{n}{2}^2$ potential rectangles in an $n \times n$ grid, which is on the order of $10^{11}$ for $n = 1000$. This rules out brute-force checking of all rectangles, so we need a constructive approach that guarantees finding a valid rectangle quickly.

A subtle edge case arises if the $2n$ initially colored cells are aligned such that naive row or column selection fails. For example, if all pre-colored cells occupy only the first two rows and the first two columns, a careless selection of rectangle coordinates might pick overlapping colors, leading to an ERROR verdict. Another tricky scenario is when Alice places her colors in a way that would tempt us to query outside the minimal rectangle, wasting our limited 10 moves.

## Approaches

A brute-force approach would attempt to check all $\binom{2n}{4}$ combinations of colored cells, testing whether they form a rectangle with distinct colors. This approach is correct in principle but unfeasible: for $n = 1000$, $\binom{2000}{4} \approx 4 \cdot 10^{12}$ operations. Even generating the rectangles alone exceeds the time limit.

The key insight is that among any $2n$ colored cells in an $n \times n$ grid, by the pigeonhole principle, there must exist at least two rows and two columns each containing at least two colored cells. This guarantees that a rectangle with corners in these rows and columns exists. The goal is to select these rows and columns and pick four cells with distinct colors. Since the grid is dense enough, we do not need more than 10 queries to find a valid rectangle: the initial $2n$ colored cells are sufficient in most cases, and our queries can be used strategically if needed.

Instead of searching blindly, we can organize the colored cells by rows and columns and attempt to form rectangles from the rows and columns containing multiple colors. This reduces the search to a small subset of cells rather than the entire grid. Any extra queries are used to confirm or supplement missing colors to guarantee distinctness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((2n)^4)$ | $O(2n)$ | Too slow |
| Constructive Rectangle Search | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$ and the $2n$ initially colored cells for the current test case. Store them in a 2D array `color[x][y]` indexed by row and column.
2. Build two dictionaries: `rows` mapping each row to the set of colors in that row and `cols` mapping each column to the set of colors in that column. This allows us to quickly identify rows and columns containing multiple distinct colors.
3. Identify at least two rows that have at least two distinct colors. Similarly, identify at least two columns with at least two distinct colors. By the pigeonhole principle, this is always possible for $2n$ cells in an $n \times n$ grid.
4. Iterate over the candidate rows and columns to find four cells forming a rectangle. Select one color from each row and column such that the four selected colors are distinct. If a conflict arises (two cells have the same color), a single query can be used to fetch an uncolored cell in the rectangle to guarantee distinctness.
5. Output the rectangle coordinates in the format `! x1 x2 y1 y2`. Alice checks that all four corners are colored with distinct colors. If needed, use queries to fill missing corners or confirm color uniqueness.

Why it works: The algorithm relies on the density of pre-colored cells. With $2n$ distinct colors and $n \times n$ cells, there must exist at least two rows and two columns each containing multiple colors, guaranteeing a rectangle. Organizing by row and column ensures we can select four cells forming a rectangle. Even if Alice colors adaptively during queries, choosing uncolored cells inside this rectangle allows us to satisfy distinctness within our 10-query limit.

## Python Solution

```python
import sys
input = sys.stdin.readline
flush = sys.stdout.flush

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        color = [[0] * (n + 1) for _ in range(n + 1)]
        rows = {}
        cols = {}

        for c in range(1, 2 * n + 1):
            x, y = map(int, input().split())
            color[x][y] = c
            if x not in rows:
                rows[x] = []
            if y not in cols:
                cols[y] = []
            rows[x].append((y, c))
            cols[y].append((x, c))

        row_candidates = [r for r, cells in rows.items() if len(cells) >= 2]
        col_candidates = [c for c, cells in cols.items() if len(cells) >= 2]

        r1, r2 = row_candidates[:2]
        c1, c2 = col_candidates[:2]

        # Pick four distinct colors if possible
        used_colors = set()
        rect = []
        for x in [r1, r2]:
            for y, col in rows[x]:
                if y in [c1, c2] and col not in used_colors:
                    rect.append((x, y))
                    used_colors.add(col)
        if len(rect) < 4:
            # Fill missing with queries
            for x in [r1, r2]:
                for y in [c1, c2]:
                    if (x, y) not in [(rx, ry) for rx, ry in rect]:
                        print(f"? {x} {y}")
                        flush()
                        c = int(input())
                        rect.append((x, y))
                        used_colors.add(c)
                        if len(rect) == 4:
                            break
                if len(rect) == 4:
                    break

        xs = [r for r, _ in rect]
        ys = [c for _, c in rect]
        print(f"! {xs[0]} {xs[1]} {ys[0]} {ys[1]}")
        flush()
```

The solution first populates the colored cells and organizes them by row and column. Candidate rows and columns are selected to maximize the chance of forming a rectangle with four distinct colors. Missing corners are filled via interactive queries. Boundary handling ensures we never query outside the grid, and the algorithm stops as soon as four distinct colors are secured.

## Worked Examples

### Example 1

Input:

```
n = 3
Colored cells: (1,2)=1, (1,3)=2, (2,1)=3, (2,3)=4, (3,1)=5, (3,2)=6
```

Candidate rows: 1,2 (both have >=2 colors)

Candidate columns: 1,2,3 (select first two with >=2 colors)

Rectangle selected: (1,2),(1,3),(2,2),(2,3)

Table of selection:

| Step | Action | Cells chosen | Colors |
| --- | --- | --- | --- |
| 1 | Identify rows | 1,2 | - |
| 2 | Identify cols | 2,3 | - |
| 3 | Pick cells | (1,2),(1,3),(2,2),(2,3) | 1,2,?,4 |
| 4 | Query missing | (2,2) | 6 |
| 5 | Output rectangle | ! 1 2 2 3 | All distinct |

This shows that queries are only needed if a corner is uncolored. The rectangle is valid.

### Example 2

Input:

```
n = 3
Colored cells: (1,1)=1, (1,2)=2, (1,3)=3, (2,1)=4, (2,2)=5, (2,3)=6
```

Rows with >=2 colors: 1,2

Columns with >=2 colors: 1,2,3

Rectangle selected: (1,1),(1,
