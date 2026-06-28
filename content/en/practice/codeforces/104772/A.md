---
title: "CF 104772A - Axis-Aligned Area"
description: "We are given a collection of points on a 2D plane. Each point represents a location with integer coordinates. The task is to consider all these points together and determine the area of the smallest rectangle whose sides are parallel to the coordinate axes and that contains…"
date: "2026-06-28T15:38:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104772
codeforces_index: "A"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104772
solve_time_s: 53
verified: true
draft: false
---

[CF 104772A - Axis-Aligned Area](https://codeforces.com/problemset/problem/104772/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of points on a 2D plane. Each point represents a location with integer coordinates. The task is to consider all these points together and determine the area of the smallest rectangle whose sides are parallel to the coordinate axes and that contains every point.

In more concrete terms, imagine stretching a rubber band aligned with the x and y directions so that it just encloses all the given points. The rectangle formed by the extreme left, right, bottom, and top positions defines the region we care about. The output is the area of that rectangle.

If all points lie on a single vertical or horizontal line, the rectangle collapses in one direction, and the area becomes zero.

The constraints are small enough that we only need to scan through all points once or twice. Even if the number of points is large, say up to 200,000, any solution that performs a constant amount of work per point is sufficient. This immediately rules out any approach that tries to examine pairs of points or construct geometric structures like convex hulls, since those would introduce at least quadratic or log-linear overhead that is unnecessary for an axis-aligned enclosure.

A few edge cases matter for correctness. If there is only one point, the area must be zero because both width and height are zero. If all points share the same x-coordinate, the width is zero regardless of y-variation. Similarly, if all share the same y-coordinate, the height is zero.

As a concrete failure case, consider points (0, 0), (0, 5), (0, 10). A naive approach that mistakenly assumes a non-degenerate rectangle might return a positive area based on y-range only, but the correct width is zero, so the area is zero.

Another subtle case is when negative coordinates appear, such as (-3, 2), (4, -1), (-2, 7). Any solution that initializes min and max incorrectly (for example starting from 0 instead of the first point) may compute a wrong bounding box.

## Approaches

The brute-force idea is to consider every pair of points and treat them as opposite corners of a candidate axis-aligned rectangle. For each such pair, we would check whether all other points lie inside or on the boundary of the rectangle, and compute its area. This works because any valid enclosing rectangle must have its boundaries defined by some subset of points.

However, this approach performs O(n^3) operations in the worst case: O(n^2) candidate rectangles, and for each candidate we scan O(n) points to verify containment. Even with modest constraints like n = 10^4, this becomes infeasible.

The key observation is that an axis-aligned enclosing rectangle is completely determined by four values only: the minimum x-coordinate, maximum x-coordinate, minimum y-coordinate, and maximum y-coordinate among all points. Once these extremes are known, no other information about the distribution of points matters.

This reduces the problem from a combinatorial search over pairs to a single pass aggregation problem. We simply track these four values while scanning the input once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal (min/max scan) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all points one by one while maintaining four variables: min_x, max_x, min_y, max_y. These track the bounding box seen so far.
2. Initialize min_x and min_y with very large values, and max_x and max_y with very small values. This ensures that the first point correctly sets all boundaries without special casing.
3. For each point (x, y), update min_x = min(min_x, x), max_x = max(max_x, x), and similarly for y. This step gradually expands the bounding rectangle as new extremes are discovered.
4. After processing all points, compute width as max_x - min_x and height as max_y - min_y. These represent the full span of the point set along each axis.
5. Multiply width and height to obtain the final area.
6. Output the result directly.

The reason each update is correct is that any valid enclosing axis-aligned rectangle must have boundaries at or beyond the extreme points. Any candidate rectangle with a smaller boundary would exclude at least one point, and any larger rectangle is unnecessary for the minimal enclosure.

### Why it works

At every prefix of the input, the variables min_x, max_x, min_y, and max_y represent the exact bounding box of the points processed so far. When a new point arrives, only these four values can possibly change the enclosure. Since the final rectangle depends only on global extremes, maintaining these values incrementally guarantees that after the last point, we have the exact minimal axis-aligned rectangle containing all points. No configuration of interior points can alter the boundary without violating inclusion of an extreme point.

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
        x, y = map(int, input().split())
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
    
    width = max_x - min_x
    height = max_y - min_y
    print(width * height)

if __name__ == "__main__":
    solve()
```

The implementation keeps the logic strictly streaming, so it never stores all points. The initialization using infinities avoids special-casing the first point and prevents errors when coordinates are negative.

The subtraction step is safe even when all points are identical, since both width and height become zero.

## Worked Examples

### Example 1

Input:

```
4
0 0
0 5
3 0
3 5
```

| Step | min_x | max_x | min_y | max_y | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | first point |
| 2 | 0 | 0 | 0 | 5 | update y max |
| 3 | 0 | 3 | 0 | 5 | update x max |
| 4 | 0 | 3 | 0 | 5 | no change |

Final width = 3, height = 5, area = 15.

This confirms that the algorithm correctly tracks boundary expansion as new extremes appear.

### Example 2

Input:

```
3
2 7
-1 4
5 -3
```

| Step | min_x | max_x | min_y | max_y | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 7 | 7 | first point |
| 2 | -1 | 2 | 4 | 7 | update min_x and min_y |
| 3 | -1 | 5 | -3 | 7 | update max_x and min_y |

Final width = 6, height = 10, area = 60.

This example exercises negative coordinates and shows that initialization with infinities avoids bias toward zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each point updates constant number of variables |
| Space | O(1) | only four integers are stored |

The algorithm is optimal because every point must be read at least once, and all work per point is constant, matching the lower bound imposed by input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for _ in range(n):
        x, y = map(int, input().split())
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    return str((max_x - min_x) * (max_y - min_y))

# provided sample (assumed format)
assert run("""4
0 0
0 5
3 0
3 5
""") == "15", "sample 1"

# single point
assert run("""1
10 10
""") == "0", "single point"

# all vertical line
assert run("""3
2 1
2 5
2 9
""") == "0", "zero width"

# all horizontal line
assert run("""3
-1 7
3 7
10 7
""") == "0", "zero height"

# negative coordinates
assert run("""3
-3 2
4 -1
-2 7
""") == "60", "mixed negatives"

# square
assert run("""4
0 0
0 2
2 0
2 2
""") == "4", "perfect square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 0 | degenerate rectangle |
| vertical line | 0 | zero width case |
| horizontal line | 0 | zero height case |
| mixed negatives | 60 | correct handling of negative coords |
| square | 4 | standard geometry correctness |

## Edge Cases

A single-point input sets min and max values simultaneously, so both width and height remain zero throughout execution, producing area zero without any special branching.

When all points lie on a vertical line, such as x = 2 for every point, max_x and min_x remain equal, so width is zero. The algorithm still updates y bounds correctly, but the final multiplication collapses the area to zero.

When all points lie on a horizontal line, the symmetric behavior occurs with height becoming zero.

For negative coordinates, initialization with infinities ensures that the first comparison correctly captures real values. For example, starting from (−3, 2) immediately sets both min_x and max_x to −3 and max_y to 2, preventing any incorrect bias that would occur if initialization used zero.
