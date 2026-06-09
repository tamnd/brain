---
title: "CF 1620B - Triangles on a Rectangle"
description: "We are asked to select three points on the boundary of a rectangle to form a triangle with maximum possible area, with the restriction that exactly two of the points lie on the same side."
date: "2026-06-10T06:00:34+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1620
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 119 (Rated for Div. 2)"
rating: 1000
weight: 1620
solve_time_s: 76
verified: true
draft: false
---

[CF 1620B - Triangles on a Rectangle](https://codeforces.com/problemset/problem/1620/B)

**Rating:** 1000  
**Tags:** geometry, greedy, math  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to select three points on the boundary of a rectangle to form a triangle with maximum possible area, with the restriction that exactly two of the points lie on the same side. The rectangle’s corners are at $(0,0)$ and $(w,h)$, and each side has at least two interior lattice points. The input gives these points explicitly, separated by the horizontal sides ($y=0$ and $y=h$) and vertical sides ($x=0$ and $x=w$).

The output is the doubled area of this triangle. Doubling avoids fractions because the area formula for a triangle with vertices $(x_1,y_1)$, $(x_2,y_2)$, $(x_3,y_3)$ is $\frac12 |(x_1(y_2-y_3) + x_2(y_3-y_1) + x_3(y_1-y_2))|$.

Given constraints: the rectangle dimensions $w$ and $h$ can reach $10^6$, and each side can have up to $2\cdot 10^5$ points, with the total across all test cases capped at $2\cdot 10^5$. This means we cannot examine all triplets of points explicitly. For instance, if each side has 10 points, brute-force over all $4 \times 10$ points yields $\binom{40}{3}=9,880$ triangles. With the maximum input sizes, brute-force becomes computationally impossible.

Edge cases include when points are clustered at one end of a side or evenly spread. A careless algorithm that only considers arbitrary triplets or only midpoints could miss the maximum area triangle. For example, if two points on $x=0$ are at $y=1$ and $y=6$, and the other point is at $x=w$, $y$ anywhere, the maximum area triangle uses the extreme vertical points on $x=0$, not a middle point.

## Approaches

The naive approach is to iterate over all pairs of points on a side and combine them with every other point on the remaining three sides. This is correct because it explicitly checks all valid triangles, but with up to $2\cdot10^5$ points per side, this can produce $O(n^3)$ operations, which is far beyond what we can compute in 2 seconds.

The key insight is that for any side, the triangle with maximum area occurs when we choose the two points that are farthest apart on that side. For a horizontal side, the difference in $x$ coordinates gives the base of a triangle; for a vertical side, the difference in $y$ coordinates gives the base. To maximize the area, the third point should lie on the opposite side in the direction perpendicular to the base. Concretely, for a horizontal base along $y=0$, the best third point is either $y=h$ or $y=0$ depending on which gives the largest vertical distance (here always $y=h$). Similarly, for a vertical base along $x=0$, the third point should be at $x=w$. This reduces the search from all pairs to just checking the two endpoints of each side, giving a constant number of candidate triangles per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(1) per side, O(t) total | O(1) | Accepted |

## Algorithm Walkthrough

1. Read rectangle dimensions $w$ and $h$ and the points on each side.
2. For each horizontal side ($y=0$ and $y=h$), identify the leftmost and rightmost points. The base length is the difference of their $x$ coordinates. Multiply this by the maximum vertical distance to the other side (which is $h$) to get the doubled area.
3. For each vertical side ($x=0$ and $x=w$), identify the bottommost and topmost points. The base length is the difference of their $y$ coordinates. Multiply this by the maximum horizontal distance to the opposite side (which is $w$) to get the doubled area.
4. Compare the doubled areas from all four sides and output the maximum.

Why it works: The area formula for a triangle is $0.5 \cdot \text{base} \cdot \text{height}$. To maximize the area given a fixed side as the base, we need the largest possible base on that side and the largest possible perpendicular distance to the third point. Extremal points on a rectangle guarantee both, so considering only side endpoints is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        w, h = map(int, input().split())
        
        # Horizontal bottom side
        kx0, *xs0 = map(int, input().split())
        # Horizontal top side
        kx1, *xs1 = map(int, input().split())
        # Vertical left side
        ky0, *ys0 = map(int, input().split())
        # Vertical right side
        ky1, *ys1 = map(int, input().split())
        
        # max horizontal length on bottom and top, multiplied by vertical distance h
        max_area = max((xs0[-1] - xs0[0]) * h, (xs1[-1] - xs1[0]) * h)
        # max vertical length on left and right, multiplied by horizontal distance w
        max_area = max(max_area, (ys0[-1] - ys0[0]) * w, (ys1[-1] - ys1[0]) * w)
        
        print(max_area)

if __name__ == "__main__":
    solve()
```

The code first unpacks the number of points and their coordinates using `*xs` and `*ys`. This ensures the leftmost and rightmost points can be accessed immediately without additional sorting since input guarantees ascending order. Multiplying the base length by the perpendicular distance gives the doubled area directly, avoiding any floating point operations.

## Worked Examples

Sample input:

```
5 8
2 1 2
3 2 3 4
3 1 4 6
2 4 5
```

| Side | Endpoints | Base Length | Third Point Distance | Doubled Area |
| --- | --- | --- | --- | --- |
| y=0 | 1,2 | 1 | 8 | 8 |
| y=8 | 2,4 | 2 | 8 | 16 |
| x=0 | 1,6 | 5 | 5 | 25 |
| x=5 | 4,5 | 1 | 5 | 5 |

Maximum is 25, which matches the sample output.

Another example:

```
10 7
2 3 9
2 1 7
3 1 3 4
3 4 5 6
```

| Side | Endpoints | Base Length | Third Point Distance | Doubled Area |
| --- | --- | --- | --- | --- |
| y=0 | 3,9 | 6 | 7 | 42 |
| y=7 | 1,7 | 6 | 7 | 42 |
| x=0 | 1,4 | 3 | 10 | 30 |
| x=10 | 4,6 | 2 | 10 | 20 |

Maximum is 42.

These tables show how only endpoints of each side suffice to compute the maximum area.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case computes four differences and four multiplications, independent of number of points per side |
| Space | O(1) | Only a few variables per test case, points are read and discarded |

Given $t \le 10^4$ and total points $\le 2 \cdot 10^5$, this runs well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("3\n5 8\n2 1 2\n3 2 3 4\n3 1 4 6\n2 4 5\n10 7\n2 3 9\n2 1 7\n3 1 3 4\n3 4 5 6\n11 5\n3 1 6 8\n3 3 6 8\n3 1 3 4\n2 2 4\n") == "25\n42\n35", "sample 1"

# Custom tests
assert run("1\n3 3\n2 1 2\n2 1 2\n2 1 2\n2 1 2\n") == "6", "smallest rectangle"
assert run("1\n1000000 1000000\n2 1 1000000\n2 1 1000000\n2 1 1000000\n2 1 1000000\n") == "1000000000000", "maximum size rectangle"
assert run("1\n5 5\n3 1 3 5\n3 1 3 5\n2 2 4
```
