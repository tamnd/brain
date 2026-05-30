---
title: "CF 485B - Valuable Resources"
description: "We are asked to build a square city on a 2D Cartesian map such that it encloses all given mines, represented as points with integer coordinates. The sides of the square must remain parallel to the axes, and our goal is to minimize the area of the square."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 485
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 276 (Div. 2)"
rating: 1300
weight: 485
solve_time_s: 669
verified: false
draft: false
---

[CF 485B - Valuable Resources](https://codeforces.com/problemset/problem/485/B)

**Rating:** 1300  
**Tags:** brute force, greedy  
**Solve time:** 11m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to build a square city on a 2D Cartesian map such that it encloses all given mines, represented as points with integer coordinates. The sides of the square must remain parallel to the axes, and our goal is to minimize the area of the square. The input consists of `n` points, each with coordinates `(x_i, y_i)`, and the output is a single integer representing the minimal area of the square.

The constraints indicate that `n` can be up to 1000 and coordinates can be as large as ±10^9. This implies that any approach with complexity worse than `O(n)` or `O(n log n)` is acceptable, as 1000 points are easily manageable. Brute-force approaches that attempt to iterate over all possible square positions would involve `O(n^2)` or worse, which is still feasible for 1000 points but unnecessary since a more direct geometric approach exists.

An edge case arises when all points lie on a line, for example:

```
2
1 1
1 5
```

Here, a square that covers the vertical line must extend horizontally as well, so the side of the square is dictated by the largest spread in either dimension. A careless approach might take only the maximum difference in x or y individually without considering that the square side must be the larger of the two differences.

Another subtle case is when all points are identical:

```
3
0 0
0 0
0 0
```

Here the square should have a side length of 0 and area 0. Handling zero-area correctly is important.

## Approaches

A naive approach is to try all possible top-left and bottom-right pairs of points as corners of the square, compute the required square side to cover them, and keep the minimal area found. For each pair, we would check all points to see if they fit inside. This would yield roughly `O(n^3)` operations and is inefficient even for `n = 1000`, potentially taking 10^9 operations in the worst case.

The key observation is that the square’s sides must cover the extreme x and y coordinates of the mines. Let `min_x` and `max_x` be the minimum and maximum x-coordinates, and `min_y` and `max_y` the minimum and maximum y-coordinates. Any square covering all points must span at least `max_x - min_x` horizontally and `max_y - min_y` vertically. To satisfy the square shape, we take the larger of these two spans as the side length. This observation reduces the problem to a simple linear scan for min/max values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all corner pairs) | O(n^3) | O(n) | Too slow |
| Min-Max Reduction (optimal) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize four variables to track the extreme coordinates: `min_x`, `max_x`, `min_y`, and `max_y`. Set `min_x` and `min_y` to very large values (infinity) and `max_x` and `max_y` to very small values (-infinity).
2. Iterate through each mine coordinate `(x_i, y_i)`. For each point, update `min_x` if `x_i` is smaller, `max_x` if `x_i` is larger, `min_y` if `y_i` is smaller, and `max_y` if `y_i` is larger. This step finds the bounding rectangle of all mines.
3. Compute the required side length of the square as `side = max(max_x - min_x, max_y - min_y)`. This ensures the square can cover the rectangle defined by the extremes while maintaining equal sides.
4. Compute the area as `area = side * side` and output the result.

Why it works: The bounding rectangle of the points determines the minimal width and height needed to cover all mines. Taking the larger dimension ensures that the city remains square while still covering all points. No smaller square can enclose all mines because at least one side would be too short to cover the extremal points in one dimension.

## Python Solution

```python
import sys
input = sys.stdin.readline

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

side = max(max_x - min_x, max_y - min_y)
area = side * side
print(area)
```

The code above mirrors the algorithm steps directly. The use of `float('inf')` and `float('-inf')` ensures any first point will correctly initialize the extremes. Updating min/max values individually avoids off-by-one mistakes, especially for negative coordinates.

## Worked Examples

**Sample 1:**

```
Input:
2
0 0
2 2
```

| Step | min_x | max_x | min_y | max_y |
| --- | --- | --- | --- | --- |
| Initial | inf | -inf | inf | -inf |
| After (0,0) | 0 | 0 | 0 | 0 |
| After (2,2) | 0 | 2 | 0 | 2 |

Side = max(2-0, 2-0) = 2, Area = 4. Correct.

**Custom Sample 2:**

```
Input:
3
1 3
4 5
2 2
```

| Step | min_x | max_x | min_y | max_y |
| --- | --- | --- | --- | --- |
| Initial | inf | -inf | inf | -inf |
| After (1,3) | 1 | 1 | 3 | 3 |
| After (4,5) | 1 | 4 | 3 | 5 |
| After (2,2) | 1 | 4 | 2 | 5 |

Side = max(4-1, 5-2) = 3, Area = 9. Correct.

These traces confirm that the algorithm correctly computes the minimal square to cover all points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over all points to compute min/max coordinates |
| Space | O(1) | Only four variables to track extremes, independent of n |

Given `n` ≤ 1000, this algorithm executes almost instantly. Memory use is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
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

    side = max(max_x - min_x, max_y - min_y)
    return str(side * side)

# Provided sample
assert run("2\n0 0\n2 2\n") == "4", "sample 1"

# Minimum size input
assert run("2\n0 0\n0 0\n") == "0", "all points identical"

# Vertical line
assert run("2\n1 1\n1 5\n") == "16", "vertical line"

# Horizontal line
assert run("2\n3 7\n8 7\n") == "25", "horizontal line"

# Maximum spread
assert run("4\n-1000000000 -1000000000\n1000000000 1000000000\n0 0\n-500000000 500000000\n") == "4000000000000000000", "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 identical points | 0 | Zero-area case |
| Vertical line | 16 | Side must equal y-difference |
| Horizontal line | 25 | Side must equal x-difference |
| Large coordinates | 4e18 | Handles extreme coordinate values without overflow |

## Edge Cases

For identical points like `2\n0 0\n0 0`, `min_x = max_x = min_y = max_y = 0`, side = 0, area = 0. The algorithm handles this correctly because it uses `max(max_x - min_x, max_y - min_y)` which is 0.

For vertical lines `2\n1 1\n1 5`, `min_x = max_x = 1`, `min_y = 1`, `max_y = 5`, side = max(0, 4) = 4, area = 16. The algorithm correctly chooses the largest dimension as the square side.

For horizontal lines `2\n3 7\n8 7`, `min_x = 3`, `max_x = 8`, `min_y = max_y = 7`, side = max(5, 0) = 5, area = 25. Again, it correctly identifies the square side
