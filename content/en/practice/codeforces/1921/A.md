---
title: "CF 1921A - Square"
description: "We are given the four vertices of a square on a 2D coordinate plane. The points are presented in arbitrary order, so we do not know which point is the bottom-left corner, top-right corner, and so on. The square has two special properties."
date: "2026-06-08T19:21:57+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1921
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 920 (Div. 3)"
rating: 800
weight: 1921
solve_time_s: 117
verified: true
draft: false
---

[CF 1921A - Square](https://codeforces.com/problemset/problem/1921/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the four vertices of a square on a 2D coordinate plane. The points are presented in arbitrary order, so we do not know which point is the bottom-left corner, top-right corner, and so on.

The square has two special properties. Its sides are parallel to the coordinate axes, and its area is strictly positive. Because the sides are axis-aligned, the square's vertices must use exactly two distinct x-coordinates and exactly two distinct y-coordinates. The side length is simply the distance between the two x-values, which is equal to the distance between the two y-values.

For each test case, we must compute the area of the square.

The constraints are tiny. There are at most 100 test cases, and each test case contains only four points. Any algorithm that performs a few dozen operations per test case will run instantly. Efficiency is not the challenge here. The challenge is recognizing the geometric structure hidden by the random ordering of the vertices.

A common mistake is assuming the points arrive in a useful order. Consider:

```
1 2
4 5
1 5
4 2
```

The first two points are diagonally opposite corners, not adjacent corners. Computing the distance between consecutive input points would produce the wrong side length.

Another subtle case is when coordinates are negative:

```
-1 1
1 -1
1 1
-1 -1
```

The side length is not obtained from the largest coordinate value. We must compute the difference between the maximum and minimum x-values, giving `1 - (-1) = 2`.

A careless implementation might also try to use Euclidean distances between arbitrary pairs of points. For example:

```
17 11
17 39
45 11
45 39
```

The diagonal length is much larger than the side length. Squaring the diagonal would not give the area. The correct side length is `45 - 17 = 28`, so the area is `28² = 784`.

## Approaches

A brute-force solution would examine all pairs of points and determine which pairs form edges of the square. Since there are only four points, there are six pairs. We could find the smallest non-zero horizontal or vertical distance and use it as the side length. This works because the input is guaranteed to describe a valid axis-aligned square.

Even though this approach is already fast enough, it is more complicated than necessary. We are solving a geometry problem whose structure is much simpler than a general square-detection problem.

The key observation is that an axis-aligned square has exactly two distinct x-coordinates and two distinct y-coordinates. The side length is simply:

```
max(x) - min(x)
```

Since the figure is guaranteed to be a square, the same value is also equal to:

```
max(y) - min(y)
```

Once we know the side length, the area is its square.

This turns the problem into extracting the minimum and maximum x-values from the four points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

The asymptotic complexity is the same because the input size per test case is fixed, but the optimal approach is much cleaner and directly uses the geometry of axis-aligned squares.

## Algorithm Walkthrough

1. Read the four points of the current test case.
2. Store all x-coordinates in a list.
3. Compute the minimum and maximum x-values.
4. Calculate the side length as `max_x - min_x`.

Since the square is axis-aligned, every vertex lies on one of exactly two vertical lines. Their separation is the side length.
5. Compute the area as `side_length * side_length`.
6. Output the area.

### Why it works

For an axis-aligned square, the left side and right side lie on two distinct x-values. Every vertex belongs to one of those two vertical lines. The horizontal distance between them is exactly the side length of the square.

Because the input is guaranteed to form a valid square, `max(x) - min(x)` is always positive and equals the square's side length. Squaring that value gives the area. No other geometric calculations are needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    xs = []

    for _ in range(4):
        x, y = map(int, input().split())
        xs.append(x)

    side = max(xs) - min(xs)
    print(side * side)
```

The solution reads four points for each test case and keeps only their x-coordinates. Since the square is guaranteed to be axis-aligned, the side length is determined by the horizontal distance between the leftmost and rightmost vertices.

Using `max(xs) - min(xs)` avoids any dependence on the input order. Whether the vertices are listed clockwise, counterclockwise, or completely shuffled, the extreme x-values remain the same.

All arithmetic fits comfortably inside standard integer types. The coordinate range is at most 1000 in magnitude, so the largest possible side length is 2000 and the largest possible area is 4,000,000.

## Worked Examples

### Example 1

Input points:

```
(1,2)
(4,5)
(1,5)
(4,2)
```

| Step | xs | min_x | max_x | side | area |
| --- | --- | --- | --- | --- | --- |
| After reading points | [1, 4, 1, 4] | 1 | 4 | 3 | 9 |

Output:

```
9
```

This example shows why point ordering does not matter. The points are not given around the perimeter of the square, yet the extreme x-values immediately reveal the side length.

### Example 2

Input points:

```
(-1,1)
(1,-1)
(1,1)
(-1,-1)
```

| Step | xs | min_x | max_x | side | area |
| --- | --- | --- | --- | --- | --- |
| After reading points | [-1, 1, 1, -1] | -1 | 1 | 2 | 4 |

Output:

```
4
```

This example demonstrates that negative coordinates require no special handling. The difference between the maximum and minimum x-values still produces the correct side length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Four points are processed per test case |
| Space | O(1) | Only a few integers are stored |

The number of points is fixed, so each test case requires a constant amount of work and memory. With at most 100 test cases, the solution runs comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        xs = []
        for _ in range(4):
            x, y = map(int, input().split())
            xs.append(x)

        side = max(xs) - min(xs)
        ans.append(str(side * side))

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""3
1 2
4 5
1 5
4 2
-1 1
1 -1
1 1
-1 -1
45 11
45 39
17 11
17 39
"""
) == "9\n4\n784"

# side length 1
assert run(
"""1
0 0
1 0
0 1
1 1
"""
) == "1"

# negative coordinates
assert run(
"""1
-3 -3
-1 -3
-3 -1
-1 -1
"""
) == "4"

# large coordinate range
assert run(
"""1
-1000 -1000
1000 -1000
-1000 1000
1000 1000
"""
) == "4000000"

# shuffled order
assert run(
"""1
5 2
2 2
5 5
2 5
"""
) == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Unit square with side 1 | 1 | Smallest positive area |
| Negative-coordinate square | 4 | Correct handling of negative values |
| Coordinates at limits | 4000000 | Boundary values and largest area |
| Random vertex order | 9 | Independence from input ordering |

## Edge Cases

Consider the square:

```
1
0 0
1 0
0 1
1 1
```

The x-values are `[0, 1, 0, 1]`. The algorithm computes `max_x = 1`, `min_x = 0`, giving a side length of `1`. The area is `1`. This is the smallest possible valid square because the area must be positive.

Consider a square entirely in negative coordinates:

```
1
-3 -3
-1 -3
-3 -1
-1 -1
```

The x-values are `[-3, -1, -3, -1]`. The side length becomes `-1 - (-3) = 2`, and the area is `4`. The subtraction automatically handles negative values correctly.

Consider a shuffled input order:

```
1
4 5
1 2
4 2
1 5
```

The points are not listed around the boundary. The algorithm ignores ordering and uses only the extreme x-values. It finds `max_x = 4` and `min_x = 1`, producing side length `3` and area `9`.

Consider the largest coordinate spread allowed:

```
1
-1000 -1000
1000 -1000
-1000 1000
1000 1000
```

The side length is `1000 - (-1000) = 2000`, and the area is `4,000,000`. The computation remains a simple integer subtraction and multiplication, well within limits.
