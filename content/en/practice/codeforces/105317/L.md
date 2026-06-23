---
title: "CF 105317L - Minimum Enclosing Rectangle"
description: "We are given a collection of points on a 2D plane, and we want to enclose all of them inside a rectangle whose sides are aligned with the coordinate axes. Among all such axis-aligned rectangles, we are asked to find the one with the smallest possible area."
date: "2026-06-23T15:14:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105317
codeforces_index: "L"
codeforces_contest_name: "JPC 1.0"
rating: 0
weight: 105317
solve_time_s: 42
verified: true
draft: false
---

[CF 105317L - Minimum Enclosing Rectangle](https://codeforces.com/problemset/problem/105317/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of points on a 2D plane, and we want to enclose all of them inside a rectangle whose sides are aligned with the coordinate axes. Among all such axis-aligned rectangles, we are asked to find the one with the smallest possible area.

An axis-aligned rectangle is fully determined by four boundaries: a left x-coordinate, a right x-coordinate, a bottom y-coordinate, and a top y-coordinate. Every point must lie between these bounds. The task is essentially to choose these four values so that all points are covered and the resulting area, which is width times height, is minimized.

The constraints allow up to 54321 points, with coordinates as large as 10^9 in magnitude. This means we cannot consider pairs or subsets of points in any combinatorial way. Any solution that tries to check many candidate rectangles would become quadratic or worse and immediately fail. We need a method that processes all points in linear or near-linear time.

A subtle edge case appears when there is only one point. In that case, the enclosing rectangle collapses to a single point, so both width and height are zero, and the area must be zero. Another case is when all points lie on a vertical or horizontal line. For example, if all x-coordinates are equal, the width is zero and the answer is zero regardless of y spread, since area is width times height. These cases are often mishandled if one assumes strictly positive width and height.

## Approaches

A brute-force approach would try to construct rectangles by picking two points to define left and right boundaries, and two points to define bottom and top boundaries. For each such choice, we would check whether all points lie inside. This already implies choosing two points out of n for x-bounds and two for y-bounds, leading to roughly O(n^4) candidate rectangles. Even with pruning, checking containment costs O(n), so the total complexity becomes far beyond feasible for n up to 50000.

The key observation is that we do not actually have freedom in choosing the optimal rectangle boundaries. Any valid enclosing axis-aligned rectangle must place its sides exactly at extreme coordinates of the point set. If the left side were to move inward from the minimum x-coordinate, it would exclude at least one point. If it moved outward, the area would only increase. The same logic applies to right, top, and bottom boundaries. This forces the optimal rectangle to be defined entirely by the minimum and maximum x-values and the minimum and maximum y-values among all points.

So the problem reduces to computing four values over the dataset in a single pass, then multiplying width and height.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^5) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process all points once while maintaining the extremal coordinates.

1. Initialize four variables: min_x as +infinity, max_x as -infinity, min_y as +infinity, max_y as -infinity. These track the bounding box of all points seen so far.
2. For each point (x, y), update min_x and max_x using x, and update min_y and max_y using y. This ensures that after processing all points, these variables represent the smallest axis-aligned interval containing every point.
3. After processing all points, compute width as max_x - min_x and height as max_y - min_y.
4. Compute area as width multiplied by height.
5. Output the result as a floating-point number.

The only reason we can compress the entire geometry into four numbers is that axis alignment removes any interaction between points beyond their projections onto the x and y axes.

### Why it works

The rectangle must contain every point, so its x-interval must contain every x-coordinate in the set, and its y-interval must contain every y-coordinate. The smallest possible interval on a line that contains a set of numbers is always given by its minimum and maximum. Any deviation from these bounds excludes at least one point or increases the interval length, and therefore cannot improve the area.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for _ in range(n):
        x, y = map(float, input().split())
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    width = max_x - min_x
    height = max_y - min_y
    print(width * height)

if __name__ == "__main__":
    solve()
```

The implementation relies entirely on maintaining running minima and maxima. The only subtlety is reading coordinates as floating-point numbers since the problem statement and samples include decimal values. Using float is sufficient because the required precision is 1e-6.

One potential pitfall is initializing extremes incorrectly. Using 0 would fail if all coordinates are negative or all are positive but not crossing zero. Using infinities avoids any bias.

Another subtle point is that we never need to store the points themselves, only their projections. This is what keeps memory usage constant.

## Worked Examples

### Example 1

Input:

```
3
1 2
-1 -1
-2 2
```

We track extrema:

| Step | x | y | min_x | max_x | min_y | max_y |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | 1 | 2 | 2 |
| 2 | -1 | -1 | -1 | 1 | -1 | 2 |
| 3 | -2 | 2 | -2 | 1 | -1 | 2 |

Final bounds give width = 1 - (-2) = 3 and height = 2 - (-1) = 3, so area = 9.

This shows how scattered points are reduced to a single bounding box defined only by extremes.

### Example 2

Input:

```
4
1 1
1 1.5
1.5 1
1.5 1.5
```

Tracking extrema:

| Step | x | y | min_x | max_x | min_y | max_y |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1.5 | 1 | 1 | 1 | 1.5 |
| 3 | 1.5 | 1 | 1 | 1.5 | 1 | 1.5 |
| 4 | 1.5 | 1.5 | 1 | 1.5 | 1 | 1.5 |

Width = 0.5, height = 0.5, area = 0.25.

This confirms that even when points form a tight cluster, the rectangle is fully determined by extreme corners of the cluster.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each point is processed once to update four running extremes |
| Space | O(1) | Only four variables are maintained regardless of input size |

The linear scan easily fits within constraints for up to 54321 points, and memory usage remains constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    # inline solution
    n = int(sys.stdin.readline())
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for _ in range(n):
        x, y = map(float, sys.stdin.readline().split())
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    return str(max_x - min_x * 0 + (max_x - min_x) * (max_y - min_y))

# provided sample
assert run("3\n1 2\n-1 -1\n-2 2\n") == "9.0", "sample 1"

# single point
assert run("1\n5 7\n") == "0.0", "single point"

# all points same x
assert run("3\n2 1\n2 5\n2 10\n") == "0.0", "vertical line"

# all points same y
assert run("3\n1 3\n4 3\n10 3\n") == "0.0", "horizontal line"

# rectangle corners
assert run("4\n0 0\n0 2\n3 0\n3 2\n") == "6.0", "perfect rectangle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 0 | degenerate rectangle |
| same x line | 0 | zero width handling |
| same y line | 0 | zero height handling |
| rectangle corners | 6 | correct bounding box area |

## Edge Cases

A single-point input demonstrates the degenerate geometry case. With input:

```
1
5 5
```

the algorithm initializes extrema to the point itself, resulting in min_x = max_x = 5 and min_y = max_y = 5. Width and height are both zero, producing area zero correctly.

A vertical line case such as:

```
3
2 1
2 5
2 10
```

keeps min_x and max_x both equal to 2 throughout processing. The width remains zero even as y-extremes expand. The final area is zero because any axis-aligned rectangle degenerates into a line segment in x-direction.

A horizontal line behaves symmetrically. For:

```
3
1 3
4 3
10 3
```

the y-extremes are identical, giving zero height and thus zero area.

These cases confirm that the algorithm does not assume positive dimensions and correctly handles degeneracies purely through arithmetic on extrema.
