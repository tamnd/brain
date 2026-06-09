---
title: "CF 1713A - Traveling Salesman Problem"
description: "We are working on a grid where movement is allowed in the four cardinal directions, and every move costs one step."
date: "2026-06-09T20:12:12+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1713
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 812 (Div. 2)"
rating: 800
weight: 1713
solve_time_s: 104
verified: true
draft: false
---

[CF 1713A - Traveling Salesman Problem](https://codeforces.com/problemset/problem/1713/A)

**Rating:** 800  
**Tags:** geometry, greedy, implementation  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a grid where movement is allowed in the four cardinal directions, and every move costs one step. Several points are placed on this grid, but with a restriction: every point lies strictly on one of the axes, meaning either its x-coordinate is zero or its y-coordinate is zero. Our task is to start at the origin, visit all these points in any order, and return back to the origin while minimizing total movement cost.

A useful way to reframe the task is that each point lies on a horizontal or vertical line passing through the origin. Points on the x-axis sit on the line y = 0, and points on the y-axis sit on x = 0. Since movement is Manhattan distance, traveling between points is additive along axis-aligned segments.

The input size per test is small, but the number of test cases can be large. Each test contains up to 100 points, so a quadratic or cubic solution per test is already safe, but we should aim for a linear or near-linear observation-based solution. The total number of points across tests is not bounded, which means an O(n²) per test solution is still fine, but anything worse per test case structure would be unnecessary.

A naive interpretation might suggest trying all permutations of visiting points to compute the shortest closed walk. That would immediately explode combinatorially since there are n! possible orders. Even computing pairwise shortest paths and doing a traveling salesman dynamic programming solution is overkill for n ≤ 100.

Edge cases worth thinking about come from degenerate distributions of points:

If all points are at (0, 0), no movement is required.

If all points lie only on one axis side, for example only positive y-axis, a naive strategy might still try to weave between unnecessary directions, but the optimal path simply goes to the farthest point and comes back, collecting everything on the way.

## Approaches

The brute-force idea is to treat each box as a node and consider every possible order of visiting them, summing Manhattan distances between consecutive points and returning to the origin. This is a classic traveling salesman formulation. The correctness is straightforward because it checks all possible tours.

The failure is purely computational. With n points, the number of permutations is n!, and even for n = 10 this becomes already infeasible, while here n can be 100. Even dynamic programming over subsets would require O(n² · 2ⁿ), which is far beyond limits.

The key observation is that the geometry is heavily restricted. Every point lies on one of two lines crossing at the origin. This means the movement can be decomposed independently along the x-axis and y-axis directions. On each axis, all points lie on a single line, so visiting them optimally reduces to walking from 0 to the furthest point and back while sweeping through intermediate points.

For the x-axis, only the maximum positive x and minimum negative x matter. Any route that visits both extremes must traverse the full span between them, and intermediate points are automatically covered if we move monotonically outward. The same logic applies to the y-axis.

Thus, the optimal strategy is simply to compute how far we must go in each direction: the farthest right, left, up, and down points, and sum twice those distances because each axis requires a round trip.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (TSP over points) | O(n!) | O(n) | Too slow |
| Optimal (extreme coordinates) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Separate the points into contributions on the x-axis and y-axis. Points with y = 0 contribute to horizontal movement, and points with x = 0 contribute to vertical movement. This separation works because movement on one axis does not affect the other.
2. Track the maximum positive x-coordinate among all points on the x-axis.
3. Track the minimum negative x-coordinate among all points on the x-axis.
4. Track the maximum positive y-coordinate among all points on the y-axis.
5. Track the minimum negative y-coordinate among all points on the y-axis.
6. Compute the required horizontal distance as max_x + abs(min_x). This represents the total span needed to reach both extremes from the origin.
7. Compute the required vertical distance as max_y + abs(min_y) for the same reason.
8. Return twice the sum of these two spans, since each excursion from the origin to cover extremes must return back.

The key idea behind these steps is that visiting all points on a line does not require revisiting intermediate structure; only extremes define the necessary travel envelope.

### Why it works

All points on the x-axis lie on a single straight line y = 0, so any route that visits both the leftmost and rightmost points must traverse the entire interval between them. Intermediate points lie inside this interval and are automatically visited during that traversal if we move monotonically. The same applies to the y-axis independently. Since movements on x and y axes are orthogonal and additive under Manhattan distance, the total optimal path is the sum of independent optimal traversals for each axis, each requiring a round trip from the origin.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0
    
    for _ in range(n):
        x, y = map(int, input().split())
        if y == 0:
            max_x = max(max_x, x)
            min_x = min(min_x, x)
        else:
            max_y = max(max_y, y)
            min_y = min(min_y, y)
    
    ans = 2 * (max_x - min_x + max_y - min_y)
    print(ans)
```

The implementation keeps four running values that capture the geometric envelope of all points. The initialization at zero works because the origin is always a valid baseline, and any axis-only point will adjust either the positive or negative extreme accordingly.

The final formula multiplies by two because we must return to the origin after collecting all points, making each axis traversal a round trip.

## Worked Examples

### Sample 1

Input:

```
n = 4
(0, -2), (1, 0), (-1, 0), (0, 2)
```

We track extremes:

| Step | max_x | min_x | max_y | min_y |
| --- | --- | --- | --- | --- |
| (0,-2) | 0 | 0 | 0 | -2 |
| (1,0) | 1 | 0 | 0 | -2 |
| (-1,0) | 1 | -1 | 0 | -2 |
| (0,2) | 1 | -1 | 2 | -2 |

Horizontal span = 1 - (-1) = 2

Vertical span = 2 - (-2) = 4

Total = 2 × (2 + 4) = 12

This trace shows how extremes fully determine the cost, regardless of ordering.

### Sample 2

Input:

```
n = 3
(0,2), (-3,0), (0,-1)
```

| Step | max_x | min_x | max_y | min_y |
| --- | --- | --- | --- | --- |
| (0,2) | 0 | 0 | 2 | 0 |
| (-3,0) | 0 | -3 | 2 | 0 |
| (0,-1) | 0 | -3 | 2 | -1 |

Horizontal span = 0 - (-3) = 3

Vertical span = 2 - (-1) = 3

Total = 2 × (3 + 3) = 12

This confirms that even mixed distributions collapse into independent axis spans.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each point is processed once to update extremes |
| Space | O(1) | Only four integers are maintained |

The solution fits easily within constraints since even the largest possible total number of points only requires linear scanning.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        max_x = 0
        min_x = 0
        max_y = 0
        min_y = 0
        for _ in range(n):
            x, y = map(int, input().split())
            if y == 0:
                max_x = max(max_x, x)
                min_x = min(min_x, x)
            else:
                max_y = max(max_y, y)
                min_y = min(min_y, y)
        out.append(str(2 * (max_x - min_x + max_y - min_y)))
    return "\n".join(out)

# provided samples
assert run("""3
4
0 -2
1 0
-1 0
0 2
3
0 2
-3 0
0 -1
1
0 0
""") == """12
12
0"""

# single point off-origin
assert run("""1
1
0 5
""") == "10"

# only x-axis points
assert run("""1
2
-2 0
3 0
""") == "10"

# only y-axis points
assert run("""1
2
0 -4
0 6
""") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single y-axis point | 10 | basic round trip behavior |
| only x-axis spread | 10 | handling of negative and positive extremes |
| only y-axis spread | 20 | symmetry on vertical axis |

## Edge Cases

When there is only one point at a non-origin location, the algorithm sets one axis span to zero and the other to the distance from the origin to that point. For example, input `(0, 5)` yields max_y = 5 and min_y = 0, producing a vertical span of 5 and final answer 10. The traversal corresponds to going up to (0,5) and returning.

When all points lie strictly on the x-axis, say `(-2,0)` and `(3,0)`, the y-span remains zero while the x-span becomes 5. The algorithm produces 10, corresponding to going from origin to -2, crossing through origin to 3, and returning.

When points include the origin itself, it does not affect any extrema. A point at (0,0) contributes no movement requirement and is naturally ignored by the span logic, since all extrema remain unchanged.
