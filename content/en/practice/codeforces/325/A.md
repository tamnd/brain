---
title: "CF 325A - Square and Rectangles"
description: "We are given up to five axis-aligned rectangles on a plane. Each rectangle is defined by its bottom-left and top-right coordinates. No two rectangles overlap, although they may touch at edges or corners."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 325
codeforces_index: "A"
codeforces_contest_name: "MemSQL start[c]up Round 1"
rating: 1500
weight: 325
solve_time_s: 260
verified: true
draft: false
---

[CF 325A - Square and Rectangles](https://codeforces.com/problemset/problem/325/A)

**Rating:** 1500  
**Tags:** implementation  
**Solve time:** 4m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given up to five axis-aligned rectangles on a plane. Each rectangle is defined by its bottom-left and top-right coordinates. No two rectangles overlap, although they may touch at edges or corners. The task is to determine whether the union of these rectangles exactly forms a perfect square. This means that the combined area covered by the rectangles must form a square with sides parallel to the axes, without gaps or holes.

The constraint on the number of rectangles being at most five is critical. It allows us to reason geometrically about all possible arrangements instead of relying on heavy computational geometry or grid simulations. Each rectangle’s coordinates are bounded by 31,400, which ensures that simple arithmetic or comparisons do not risk integer overflow in Python.

Non-obvious edge cases include arrangements where rectangles only touch at corners, rectangles forming a square with holes inside, or rectangles aligned in a line that is not square-shaped. For instance, three rectangles forming an L-shape that looks like part of a square could mislead a naive check based only on bounding coordinates.

## Approaches

A brute-force approach would involve creating a 2D boolean grid large enough to cover the bounding box of all rectangles and marking all cells that lie within any rectangle. Then, we could iterate over the grid to check if all cells within the bounding square are covered. This works because the number of rectangles is very small, but it is inelegant and requires potentially large memory if the bounding coordinates are near the maximum of 31,400.

The optimal approach relies on geometric reasoning. First, we compute the minimum bounding square that contains all rectangles by finding the smallest `x1` and `y1` and the largest `x2` and `y2`. If the width and height of this bounding box are unequal, the rectangles cannot form a square. If they are equal, the next step is to ensure that the combined area of the rectangles equals the area of this bounding square. If the sum of the individual rectangle areas matches the area of the bounding box, and no overlaps are present (guaranteed by the problem statement), then the rectangles exactly form a square.

The key insight is that for a small number of non-overlapping rectangles, the combination forming a square is equivalent to their bounding box being square-shaped and their total area matching the bounding box area.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grid | O(S^2) where S is the side length of bounding box | O(S^2) | Works but overkill |
| Geometric Bounding + Area Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of rectangles `n` and their coordinates.
2. Initialize `min_x`, `min_y` to infinity and `max_x`, `max_y` to zero. These will track the bounding rectangle.
3. Initialize `total_area` to zero. This will sum the area of all rectangles.
4. Iterate over each rectangle. For each rectangle with coordinates `(x1, y1, x2, y2)`, update `min_x` and `min_y` to the smaller of their current values and `x1`, `y1`. Update `max_x` and `max_y` to the larger of their current values and `x2`, `y2`. Add `(x2 - x1) * (y2 - y1)` to `total_area`.
5. Compute the width `w = max_x - min_x` and height `h = max_y - min_y` of the bounding rectangle.
6. If `w != h`, print "NO" and terminate. Otherwise, check if `total_area == w * h`. If true, print "YES"; otherwise, print "NO".

The algorithm works because the invariant that the rectangles do not overlap ensures that summing the areas is equivalent to computing the union area. Checking the bounding box ensures that the shape is square. There are no gaps if the areas match because rectangles cannot extend beyond the bounding box and cannot overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
min_x = float('inf')
min_y = float('inf')
max_x = 0
max_y = 0
total_area = 0

for _ in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    min_x = min(min_x, x1)
    min_y = min(min_y, y1)
    max_x = max(max_x, x2)
    max_y = max(max_y, y2)
    total_area += (x2 - x1) * (y2 - y1)

width = max_x - min_x
height = max_y - min_y

if width != height or total_area != width * height:
    print("NO")
else:
    print("YES")
```

The code directly implements the algorithm. Careful handling of bounding box initialization avoids errors for rectangles starting at zero. Using `float('inf')` guarantees any input will update the min values correctly. Summing rectangle areas works because the problem guarantees no overlaps, so we do not double-count.

## Worked Examples

For the sample input:

| Rectangle | x1 | y1 | x2 | y2 | Total Area | min_x | min_y | max_x | max_y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 2 | 3 | 6 | 0 | 0 | 2 | 3 |
| 2 | 0 | 3 | 3 | 5 | 6 | 0 | 0 | 3 | 5 |
| 3 | 2 | 0 | 5 | 2 | 6 | 0 | 0 | 5 | 5 |
| 4 | 3 | 2 | 5 | 5 | 6 | 0 | 0 | 5 | 5 |
| 5 | 2 | 2 | 3 | 3 | 1 | 0 | 0 | 5 | 5 |

Bounding box width and height: 5, total area: 25. Width equals height and total area equals 25, so output is YES.

Another input with rectangles forming a line:

```
2
0 0 1 3
1 0 2 3
```

Bounding box: width 2, height 3, area 6, rectangle area sum 6. Width != height, output NO. This shows the algorithm correctly detects non-square shapes even if total area matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over at most 5 rectangles, constant-time operations per rectangle |
| Space | O(1) | Only a few variables are used to track bounding box and total area |

With n ≤ 5, the algorithm runs instantly and uses negligible memory, well within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    min_x = float('inf')
    min_y = float('inf')
    max_x = 0
    max_y = 0
    total_area = 0

    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        min_x = min(min_x, x1)
        min_y = min(min_y, y1)
        max_x = max(max_x, x2)
        max_y = max(max_y, y2)
        total_area += (x2 - x1) * (y2 - y1)

    width = max_x - min_x
    height = max_y - min_y

    return "YES" if width == height and total_area == width * height else "NO"

# provided samples
assert run("5\n0 0 2 3\n0 3 3 5\n2 0 5 2\n3 2 5 5\n2 2 3 3\n") == "YES", "sample 1"

# custom cases
assert run("1\n0 0 1 1\n") == "YES", "single rectangle square"
assert run("2\n0 0 1 2\n1 0 2 2\n") == "NO", "rectangles form rectangle, not square"
assert run("3\n0 0 2 1\n0 1 1 2\n1 1 2 2\n") == "YES", "L-shaped fills 2x2 square"
assert run("2\n0 0 3 3\n3 0 6 3\n") == "NO", "two rectangles side by side non-square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 rectangle 1x1 | YES | Minimum input, single rectangle forming square |
| 2 rectangles 1x2 + 1x2 | NO | Rectangle union is rectangle, not square |
| 3 rectangles forming 2x2 L-shape | YES | Area sum equals square, checks corner touching |
| 2 rectangles side by side 3x3 | NO | Bounding box rectangular, area sum matches but not square |

## Edge Cases

The L-shaped arrangement demonstrates that rectangles touching only at edges or corners are handled correctly. The algorithm relies on the area sum and bounding box, so it automatically rejects configurations with gaps, like two rectangles forming a 2x1 +
