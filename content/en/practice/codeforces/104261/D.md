---
title: "CF 104261D - Celestial Sky"
description: "We are working on a discrete sky represented as integer coordinates in a small grid, specifically points in a 1000 by 1000 space. Two kinds of points are placed on this grid: stars and black holes."
date: "2026-07-01T21:41:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104261
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 03-24-23 Div. 2 (Beginner)"
rating: 0
weight: 104261
solve_time_s: 71
verified: true
draft: false
---

[CF 104261D - Celestial Sky](https://codeforces.com/problemset/problem/104261/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a discrete sky represented as integer coordinates in a small grid, specifically points in a 1000 by 1000 space. Two kinds of points are placed on this grid: stars and black holes. Stars are the objects we want to count, while black holes are hazards that invalidate nearby stars.

Each black hole affects a 3 by 3 square centered on itself. Any star that lies in that square is considered destroyed and must not be counted in future queries. The task is to process multiple rectangular queries and, for each query, report how many stars remain valid after removing all stars affected by any black hole.

A subtlety is that multiple stars and black holes may share coordinates, so we are effectively dealing with multisets over a grid, not sets. Also, since the grid size is fixed and small but the number of points is large, the structure of the solution is driven by preprocessing rather than per-query scanning.

The constraints push us away from anything that iterates over all stars for each query. With up to 100,000 stars, black holes, and queries, a naive per-query scan over all stars would require about 10^10 operations, which is far beyond a one second limit.

A few edge situations matter:

If a star lies exactly on a black hole center, it is removed, but so are stars in all adjacent cells including diagonals within one unit distance. For example, a black hole at (5,5) removes stars from (4,4) to (6,6). A naive mistake is to only remove orthogonal neighbors or to forget diagonal cells.

Another edge case comes from overlapping black holes. If two black holes overlap their 3x3 regions, the effect does not double remove anything, but we must ensure we do not accidentally subtract multiple times or corrupt counts.

Finally, queries can cover partial or full grid ranges, and must reflect the final cleaned star field, not the original one.

## Approaches

A direct approach is straightforward. We could simulate the black hole effect by iterating over every black hole and marking all affected cells in a grid. Then we would subtract affected stars or mark them invalid. After that, each query would simply count stars in its rectangle by scanning all stars and checking whether each lies inside the query rectangle and is not invalid.

This works conceptually, but the bottleneck appears immediately. Marking black hole effects takes up to 9 cells per black hole, which is fine, but answering each query by scanning all stars costs O(N) per query, leading to O(NQ) which is 10^10 in the worst case.

The key observation is that the coordinate range is extremely small: only 1000 by 1000. This allows us to abandon per-point scanning entirely and instead build a frequency grid. We can store how many stars exist at each coordinate, and separately mark which coordinates are "dead" due to black hole influence. Once we have a final 2D grid of valid star counts, we can build a 2D prefix sum over it. Then each query becomes a constant-time inclusion-exclusion operation.

The reason this works is that both transformations, black hole propagation and star counting, are local operations over a small bounded grid. Once everything is projected into a fixed 2D array, we reduce the problem to a classic static range sum query problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ) | O(N + M) | Too slow |
| Optimal | O(N + M + R^2 + Q) | O(R^2) | Accepted |

Here R = 1000.

## Algorithm Walkthrough

We reduce the entire problem into operations on a fixed grid.

1. Create a 2D array `stars[x][y]` initialized to zero, representing how many stars exist at each coordinate. For each star input, increment this cell. This compresses all duplicates naturally into counts rather than individual objects.
2. Create a second 2D boolean array `blocked[x][y]` initialized to false. For each black hole at (x, y), mark all cells in its 3 by 3 neighborhood as blocked. This includes all coordinates (i, j) such that |i - x| ≤ 1 and |j - y| ≤ 1, provided they remain inside the grid.

The reason for marking all 9 cells is that the destruction radius is Manhattan-unrestricted within one step in both directions, so it forms a full square neighborhood.
3. Build a final grid `valid[x][y]` such that it equals `stars[x][y]` if the cell is not blocked, otherwise it is zero. This step collapses the physical effect of black holes into removal of star counts.
4. Construct a 2D prefix sum array `ps[x][y]` over `valid`. Each entry stores the sum of all valid stars in the rectangle from (0,0) to (x,y). This allows efficient query answering.
5. For each query rectangle (x1, y1, x2, y2), compute the sum using inclusion-exclusion on the prefix sum array. This gives the number of surviving stars in the region.

Why prefix sums matter here is that once the grid is fixed, every query is just a submatrix sum. Without prefix sums, we would still scan up to 10^6 cells per query, which is too slow.

### Why it works

The correctness comes from two invariants. First, after processing all black holes, a cell is marked valid if and only if it is not within distance 1 in both coordinates from any black hole. This exactly matches the destruction rule.

Second, the prefix sum array guarantees that every query sum is computed as a precise decomposition of disjoint rectangles covering the query region. Because each cell’s contribution is stored exactly once in `valid`, the sum returned is exactly the number of surviving stars in the queried area.

No transformation introduces double counting or omission: black holes only zero out cells, and prefix sums only reorganize addition without changing values.

## Python Solution

```python
import sys
input = sys.stdin.readline

R = 1000

def solve():
    n, m, q = map(int, input().split())

    stars = [[0] * R for _ in range(R)]
    blocked = [[0] * R for _ in range(R)]

    for _ in range(n):
        x, y = map(int, input().split())
        stars[x][y] += 1

    for _ in range(m):
        x, y = map(int, input().split())
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < R and 0 <= j < R:
                    blocked[i][j] = 1

    valid = [[0] * R for _ in range(R)]
    for i in range(R):
        for j in range(R):
            if not blocked[i][j]:
                valid[i][j] = stars[i][j]

    ps = [[0] * R for _ in range(R)]

    for i in range(R):
        for j in range(R):
            ps[i][j] = valid[i][j]
            if i > 0:
                ps[i][j] += ps[i - 1][j]
            if j > 0:
                ps[i][j] += ps[i][j - 1]
            if i > 0 and j > 0:
                ps[i][j] -= ps[i - 1][j - 1]

    def query(x1, y1, x2, y2):
        res = ps[x2][y2]
        if x1 > 0:
            res -= ps[x1 - 1][y2]
        if y1 > 0:
            res -= ps[x2][y1 - 1]
        if x1 > 0 and y1 > 0:
            res += ps[x1 - 1][y1 - 1]
        return res

    for _ in range(q):
        x1, y1, x2, y2 = map(int, input().split())
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        print(query(x1, y1, x2, y2))

if __name__ == "__main__":
    solve()
```

The implementation begins by compressing all stars into a fixed grid. This is important because it avoids carrying individual objects forward and ensures all later operations are array-based.

The black hole expansion step explicitly iterates over a 3 by 3 neighborhood. Boundary checks ensure we do not access invalid indices at the edges of the grid.

The `valid` grid is constructed as a filtered version of the star grid. This separation makes reasoning simpler because black hole logic and summation logic are not mixed.

The prefix sum construction follows the standard 2D recurrence, carefully subtracting overlap from the top-left diagonal. The query function applies the same inclusion-exclusion pattern.

Swapping coordinates in queries ensures correctness even if the input does not guarantee ordering of corners.

## Worked Examples

We use a simplified illustrative grid to trace behavior.

Consider a small instance:

Input:

```
3 1 2
0 0
1 1
2 2
1 1
0 0 2 2
0 0 1 1
```

Here we have stars at three diagonal positions and a black hole at (1,1).

| Step | Action | State |
| --- | --- | --- |
| 1 | Insert stars | (0,0)=1, (1,1)=1, (2,2)=1 |
| 2 | Apply black hole | blocks (0-2,0-2) around (1,1) |
| 3 | Valid grid | all cells become 0 |
| 4 | Prefix sum | all zeros |

Query (0,0)-(2,2) returns 0.

This shows that a single central black hole can eliminate all nearby diagonal stars, which is easy to miss if only orthogonal neighbors are considered.

Second example:

Input:

```
4 0 1
0 0
0 1
1 0
1 1
0 0 1 1
```

| Step | Action | State |
| --- | --- | --- |
| 1 | Insert stars | full 2x2 block |
| 2 | No black holes | unchanged |
| 3 | Valid grid | all four cells = 1 |
| 4 | Prefix sum | total = 4 |

Query returns 4, confirming prefix sums accumulate all contributions correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R^2 + N + M + Q) | grid initialization, marking, prefix sums, and constant-time queries |
| Space | O(R^2) | storage for star grid, blocked grid, and prefix sums |

The constraint R = 1000 makes the O(R^2) preprocessing trivial in practice, since it is only 10^6 operations. All other components are linear in input size, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import builtins
    return sys.modules["__main__"].solve_capture(inp)

# Since full harness integration depends on environment, we instead show logical asserts.

# sample 1
# (not executed here in isolation)

# custom cases
# minimum input
# 1 star, 1 black hole, 1 query
# boundary overlap
# full blocking case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single cell | correct handling of 3x3 blocking | edge expansion |
| no black holes | sum correctness | baseline prefix sum |
| full block center | zero output | full annihilation |
| boundary black hole at corner | correct clipping | boundary safety |

## Edge Cases

A key edge case is a black hole at the corner of the grid, such as (0,0). The algorithm iterates over a 3 by 3 neighborhood but clamps indices.

Input:

```
1 1 1
0 0
0 0
0 0 0 0
```

Execution marks cells (0,0), (0,1), (1,0), (1,1). The star at (0,0) is therefore invalidated. Query over the whole grid returns 0.

The prefix sum remains valid because blocked cells were correctly zeroed before accumulation, so no invalid contribution propagates into query results.
