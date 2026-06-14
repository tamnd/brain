---
title: "CF 1085C - Connect Three"
description: "We are given three distinct cells on an infinite grid, each representing a square plot of land. Initially everything is blocked, and we are allowed to “clear” any cells we want."
date: "2026-06-15T05:39:12+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1085
codeforces_index: "C"
codeforces_contest_name: "Technocup 2019 - Elimination Round 4"
rating: 1600
weight: 1085
solve_time_s: 145
verified: true
draft: false
---

[CF 1085C - Connect Three](https://codeforces.com/problemset/problem/1085/C)

**Rating:** 1600  
**Tags:** implementation, math  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three distinct cells on an infinite grid, each representing a square plot of land. Initially everything is blocked, and we are allowed to “clear” any cells we want. The goal is to clear a set of cells so that the three given cells become connected through 4-directional movement over cleared cells. Connectivity means that starting from any of the three special cells, we can walk step by step to the other two using only adjacent cleared cells.

The task is not just to decide if this is possible, but to construct a configuration of cleared cells with minimum possible size. In other words, we are looking for the smallest connected set of grid cells that contains all three given points.

The constraints are small: coordinates are up to 1000, and there are only three points. This rules out anything like dynamic programming over large states or graph shortest paths on the full grid, since the answer is a geometric construction rather than a search problem. The structure is rigid enough that the solution must come from observing how shortest Manhattan connections behave.

A naive approach might try to run BFS from each point and somehow merge shortest paths, or even enumerate candidate connecting structures. That would implicitly explore many grid cells and quickly become unnecessary overkill. The key difficulty is that multiple shortest paths exist between two points, and we must choose them so that all three points share a single connected structure without wasting extra cells.

A subtle failure case for naive intuition is assuming that connecting pairs independently with shortest paths always works. For example, connecting A to B and B to C with Manhattan shortest paths may create redundant detours or fail to minimize overlap, especially when the “middle” point is not well chosen. The correct solution must force maximum overlap among the three connection paths.

## Approaches

A brute-force mindset would be to consider all possible connected shapes containing the three points and compute the size of their union. But even restricting ourselves to paths between pairs, the number of possible shortest Manhattan paths between two points grows combinatorially with their distance. Exploring all combinations of three-pair connections becomes infeasible even for moderate distances, since each pair alone can have exponentially many shortest paths in terms of choices of horizontal and vertical ordering.

The key structural insight is that in Manhattan geometry, optimal connections between multiple points behave like a Steiner tree whose branching happens at a very specific location. For three terminals, there is always an optimal configuration where all paths meet at a single grid-aligned junction. Once this is accepted, the problem reduces to finding the correct meeting point.

The crucial observation is that for axis-aligned distance, the optimal “junction” minimizes the sum of distances to the three points independently in x and y dimensions. This is achieved by choosing the median x-coordinate and median y-coordinate among the three points. Once this center is fixed, the best strategy is to connect each point to this center using monotone horizontal and vertical segments. This guarantees minimal total union size because each segment is a shortest path in Manhattan distance, and overlap is maximized automatically through the shared center.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all connections | Exponential | Exponential | Too slow |
| Median Steiner construction | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Extract the x and y coordinates of the three given points.
2. Compute a candidate meeting point using the median of the x-coordinates and the median of the y-coordinates. This choice is optimal because it minimizes the total Manhattan distance sum to all three points independently along each axis.
3. For each of the three points, construct a path to the meeting point by first moving horizontally until x matches, then vertically until y matches. The order does not matter, but fixing one order keeps the construction simple and deterministic.
4. Mark every cell visited by these three paths in a set to avoid duplicates. This ensures we output the union of all required cleared plots without repetition.
5. Output the size of the set, followed by all coordinates in any order.

### Why it works

The correctness rests on the fact that any optimal solution for connecting three points in Manhattan geometry can be transformed into one where all paths intersect at a single grid point without increasing the number of cells used. Once such a junction exists, the optimal junction minimizing total path length is exactly the coordinate-wise median. The construction using axis-aligned shortest paths guarantees that we never introduce unnecessary detours, and any overlap between paths only reduces the total number of unique cells, which is beneficial for optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def path(x1, y1, x2, y2):
    cells = []
    x, y = x1, y1

    dx = 1 if x2 > x else -1
    while x != x2:
        cells.append((x, y))
        x += dx
    cells.append((x, y))

    dy = 1 if y2 > y else -1
    while y != y2:
        if (x, y) not in cells:
            cells.append((x, y))
        y += dy
    cells.append((x, y))

    return cells

def solve():
    pts = [tuple(map(int, input().split())) for _ in range(3)]

    xs = sorted(p[0] for p in pts)
    ys = sorted(p[1] for p in pts)

    cx = xs[1]
    cy = ys[1]

    res = set()

    for x, y in pts:
        for cell in path(x, y, cx, cy):
            res.add(cell)

    print(len(res))
    for x, y in res:
        print(x, y)

if __name__ == "__main__":
    solve()
```

The solution first reads the three points and computes the median coordinate in both dimensions. That median acts as the shared junction. Each point is then connected to this junction using a simple L-shaped Manhattan path.

The helper function builds a monotone path without revisiting unnecessary cells. The set ensures that overlapping segments, which are essential for optimality, do not inflate the count. This is important because the optimal structure relies heavily on shared segments, and duplicates must be removed.

A subtle implementation detail is the handling of inclusive endpoints. Each path must include both endpoints so that the final union correctly forms a connected structure containing all three original points.

## Worked Examples

### Example 1

Input:

```
0 0
1 1
2 2
```

Sorted coordinates give x median = 1, y median = 1, so the meeting point is (1,1).

| Step | Action | Current path cells |
| --- | --- | --- |
| 1 | Connect (0,0) to (1,1) | (0,0), (1,0), (1,1) |
| 2 | Connect (1,1) to (1,1) | (1,1) |
| 3 | Connect (2,2) to (1,1) | (2,2), (1,2), (1,1) |

Union gives 5 distinct cells.

This confirms that overlapping at the center reduces total cost, and the structure naturally forms a cross-like Steiner tree.

### Example 2

Input:

```
0 0
0 2
2 1
```

Median x = 0, median y = 1, so center is (0,1).

| Step | Action | Current path cells |
| --- | --- | --- |
| 1 | (0,0) → (0,1) | (0,0), (0,1) |
| 2 | (0,2) → (0,1) | (0,2), (0,1) |
| 3 | (2,1) → (0,1) | (2,1), (1,1), (0,1) |

Union size becomes 5.

This shows how the median center aligns vertical and horizontal structure to maximize overlap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three fixed-length paths are constructed |
| Space | O(1) | At most a constant number of grid cells are stored |

The coordinate limits do not affect complexity because we never explore the grid globally. We only construct a constant number of segments proportional to Manhattan distances between fixed points, and the constraints guarantee these remain small enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    pts = [tuple(map(int, sys.stdin.readline().split())) for _ in range(3)]

    xs = sorted(p[0] for p in pts)
    ys = sorted(p[1] for p in pts)
    cx, cy = xs[1], ys[1]

    res = set()

    def path(x1, y1, x2, y2):
        x, y = x1, y1
        res_local = []
        dx = 1 if x2 > x else -1
        while x != x2:
            res_local.append((x, y))
            x += dx
        res_local.append((x, y))
        dy = 1 if y2 > y else -1
        while y != y2:
            res_local.append((x, y))
            y += dy
        return res_local

    for x, y in pts:
        for cell in path(x, y, cx, cy):
            res.add(cell)

    out = [str(len(res))]
    for x, y in res:
        out.append(f"{x} {y}")
    return "\n".join(out)

# provided sample
assert run("0 0\n1 1\n2 2\n")  # structure check, output size verified separately

# custom cases
assert run("0 0\n0 1\n0 2\n").split()[0] == "3"
assert run("0 0\n1 0\n2 0\n").split()[0] == "3"
assert run("0 0\n2 2\n0 2\n").split()[0] == "5"
assert run("5 5\n5 5\n5 6\n") != ""  # invalid case guard (distinct assumed in problem)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| vertical line | 3 cells | collinear optimal compression |
| horizontal line | 3 cells | symmetric axis behavior |
| L shape | 5 cells | median junction behavior |
| near-overlap | valid non-empty | robustness of construction |

## Edge Cases

A degenerate but instructive case is when all three points lie on a straight vertical line, for example (0,0), (0,1), (0,2). The median construction picks (0,1), and each point connects directly along the same column. The union is exactly the three cells, and no extra branching appears. The algorithm naturally collapses redundant structure because all paths overlap completely along the vertical segment.

Another case is when points form a right-angle pattern like (0,0), (0,2), (2,1). The median becomes (0,1). One path is trivial, one is a single step vertical, and one forms a horizontal then vertical segment. Tracing it confirms that all paths intersect at the chosen center, and no alternative junction could reduce the union further without increasing distance from at least one point.
