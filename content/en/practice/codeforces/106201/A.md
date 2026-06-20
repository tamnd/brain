---
title: "CF 106201A - \u041d\u0435\u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0439 \u043f\u043e\u0434\u0445\u043e\u0434"
description: "We are given an $n times m$ grid, and we are allowed to choose a single starting cell on the boundary of this grid. From that chosen cell, a process starts that spreads to all four neighboring cells each second, exactly like a breadth-first expansion on a grid."
date: "2026-06-20T22:27:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106201
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2025"
rating: 0
weight: 106201
solve_time_s: 41
verified: true
draft: false
---

[CF 106201A - \u041d\u0435\u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0439 \u043f\u043e\u0434\u0445\u043e\u0434](https://codeforces.com/problemset/problem/106201/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times m$ grid, and we are allowed to choose a single starting cell on the boundary of this grid. From that chosen cell, a process starts that spreads to all four neighboring cells each second, exactly like a breadth-first expansion on a grid. The time required to reach any cell is exactly its Manhattan-style grid distance from the chosen start cell, because movement is only allowed in four directions with unit cost.

The task is to pick a boundary cell such that the maximum distance from it to any cell in the grid is minimized. In other words, we are choosing a source on the border to minimize the farthest cell’s distance under 4-directional movement.

The output is simply the coordinates of any optimal boundary cell.

The constraints allow $n, m \le 10^{18}$, which immediately rules out any simulation or grid traversal. Any solution must be constant time, since even linear time in either dimension is impossible.

A naive approach would be to pick a candidate boundary cell and compute its maximum distance to all cells, which would already require scanning the grid. That is infeasible, and even worse, doing it for all boundary cells would multiply the cost by $O(n + m)$, which is still impossible.

A subtle edge case arises when $n = 1$ or $m = 1$. In such degenerate grids, every cell lies on the boundary, and the distance structure collapses into a simple line. Another edge case is when the grid is symmetric, such as $n = m$, where multiple optimal answers exist and any of them is valid.

## Approaches

The key observation is that the spreading process behaves like a multi-source distance problem where we pick exactly one source on the boundary. The farthest cell from a boundary start is always the cell that is “deepest” inside the grid with respect to that starting edge.

If we fix a starting cell on the top row, the worst-case distance will be dominated by the bottom row. Similarly, starting from the bottom row makes the top row the bottleneck. The same symmetry holds horizontally.

So the optimal strategy is to choose a boundary cell that minimizes the maximum of its vertical and horizontal distances to the farthest edges. Intuitively, we want to start as centrally as possible along the boundary, but constrained to remain on the perimeter.

This reduces the problem to minimizing distance to the farthest side. If we start on the top or bottom row, the limiting distance is the vertical height minus 1. If we start on the left or right column, the limiting distance is the horizontal width minus 1. To minimize the worst case, we compare $n$ and $m$ and choose the side with smaller maximum reach.

If $n \le m$, it is better to choose a cell on the middle column of a row boundary, because vertical depth is smaller or equal. If $m < n$, we choose a cell on the middle row of a column boundary.

More concretely, the optimal point is always centered on the longer dimension’s axis while staying on the boundary of the shorter dimension.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all boundary starts + BFS) | $O(nm(n+m))$ | $O(nm)$ | Too slow |
| Optimal (geometry reasoning) | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reason about which boundary cell minimizes the maximum distance to any cell in the grid.

1. Compare $n$ and $m$. This decides whether vertical or horizontal spread dominates the worst-case distance.
2. If $n \le m$, we prioritize minimizing horizontal extremes. We place the starting cell on the top or bottom boundary, and choose a column as close to the center as possible. The best column is $j = \lceil m/2 \rceil$, because it minimizes the maximum distance to left and right edges.
3. In the case $n \le m$, we can choose either row $i = 1$ or $i = n$, since both are symmetric. We pick $i = 1$ for concreteness.
4. If $m < n$, we instead prioritize minimizing vertical extremes. We place the starting cell on the left or right boundary, and choose a row as close to the center as possible. The best row is $i = \lceil n/2 \rceil$.
5. In this case, we fix $j = 1$, since either left or right boundary is symmetric.
6. Output the chosen coordinates.

### Why it works

The grid distance to the farthest cell depends only on how far the starting point is from the opposite boundaries. Any interior offset away from the center of the long dimension strictly increases the maximum distance to one side without improving the other side enough to compensate. Since the start must lie on the boundary, the optimal tradeoff is achieved by centering along the dimension we are not “anchoring” on. This ensures that the maximum distance to the farthest corner is minimized among all boundary choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

if n <= m:
    i = 1
    j = (m + 1) // 2
else:
    i = (n + 1) // 2
    j = 1

print(i, j)
```

The implementation directly follows the observation that only the relative sizes of $n$ and $m$ matter. When rows are fewer or equal, we fix a boundary row and center the column. When columns are fewer, we fix a boundary column and center the row.

The expression $(m + 1) // 2$ correctly computes the middle column with proper handling for both odd and even widths, ensuring minimal maximum deviation to either side.

## Worked Examples

### Example 1

Input:

```
2 5
```

We compare $n = 2$ and $m = 5$, so $n \le m$. We fix $i = 1$ and choose the middle column $j = 3$.

| Step | n | m | Decision | i | j |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 5 | n ≤ m | 1 | - |
| 2 | 2 | 5 | center column | 1 | 3 |

Output:

```
1 3
```

This choice minimizes horizontal extremes, since column 3 is equally distant from both sides.

### Example 2

Input:

```
4 31
```

Here again $n \le m$, so we stay on a boundary row and center the column.

| Step | n | m | Decision | i | j |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 31 | n ≤ m | 1 | - |
| 2 | 4 | 31 | center column | 1 | 16 |

Output:

```
1 16
```

This places the start at the midpoint of the long dimension, minimizing worst-case horizontal distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations and comparisons |
| Space | $O(1)$ | No additional data structures used |

The solution easily fits within limits since it does not depend on grid size and performs only constant-time arithmetic even for maximal values up to $10^{18}$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())

    if n <= m:
        i = 1
        j = (m + 1) // 2
    else:
        i = (n + 1) // 2
        j = 1

    return f"{i} {j}"

# provided samples
assert run("2 5") == "1 3"
assert run("4 31") == "1 16"

# edge: single row
assert run("1 7") == "1 4"

# edge: single column
assert run("6 1") == "3 1"

# square grid
assert run("5 5") == "1 3"

# large asymmetric
assert run("1000000000000000000 2") == "500000000000000000 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 7 | 1 4 | single row boundary degeneracy |
| 6 1 | 3 1 | single column boundary degeneracy |
| 5 5 | 1 3 | symmetric grid handling |
| 1e18 2 | center row selection correctness | extreme size and integer handling |

## Edge Cases

When $n = 1$, the grid is effectively a line. Every cell is on the boundary, but the farthest cell from any chosen start is always an endpoint. The algorithm selects $i = 1$ and centers the column, which correctly minimizes the maximum distance to both ends of the line.

When $m = 1$, the situation is symmetric. The algorithm chooses $j = 1$ and centers the row, ensuring equal distance to top and bottom endpoints.

When $n = m$, both branches are valid choices. The algorithm consistently chooses the top row and center column, which is optimal since any boundary-centered selection has the same maximal distance.
