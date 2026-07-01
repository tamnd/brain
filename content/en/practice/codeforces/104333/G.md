---
title: "CF 104333G - Minimum Enclosing Axis-Parallel Square"
description: "We are given several independent sets of points on a 2D plane. For each set, we must enclose all points inside an axis-aligned square, meaning the square’s sides are parallel to the coordinate axes."
date: "2026-07-01T18:56:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104333
codeforces_index: "G"
codeforces_contest_name: "Replay of BU - PSTU Programming club collaborative contest"
rating: 0
weight: 104333
solve_time_s: 78
verified: false
draft: false
---

[CF 104333G - Minimum Enclosing Axis-Parallel Square](https://codeforces.com/problemset/problem/104333/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent sets of points on a 2D plane. For each set, we must enclose all points inside an axis-aligned square, meaning the square’s sides are parallel to the coordinate axes. Among all such squares that fully contain every point, we want the one with minimum possible area.

For a fixed test case, the geometric meaning is simple: we are allowed to place a square anywhere, but its side length must be large enough to cover the entire spread of points in both x and y directions. Once we know the side length, the area is just its square.

The constraints push us toward a per-test constant or logarithmic solution. The total number of points across all test cases is at most 200,000, so any solution that processes each point a constant number of times is acceptable. Anything quadratic per test case would immediately fail, since even moderate splits of input would exceed time limits.

A subtle issue arises from coordinate ranges. Coordinates can be as large as ±10^9, so any approach relying on enumerating candidate square positions or brute-force geometry over the plane is infeasible.

The main edge cases come from degenerate point sets. If all points are identical, the enclosing square should have side length 0, producing area 0. If there is only one point, the same logic applies. Another case is when points are aligned in a line horizontally or vertically, where only one dimension determines the answer. A naive mistake is to compute area as `(max_x - min_x) * (max_y - min_y)` without enforcing the square constraint, which underestimates the required square side when one dimension is larger.

For example, points `(0,0)` and `(10,1)` give width 10 and height 1. A rectangle area would be 10, but a square must have side 10, giving area 100.

## Approaches

The brute-force idea is to consider every possible square placement. One could imagine choosing a bottom-left corner and a side length, then checking whether all points fit inside. For each candidate, we scan all points, leading to O(n) verification. If we discretize candidate positions using point coordinates, we still have O(n^2) or worse possibilities for centers or corners, since any point might define a boundary. This quickly becomes impossible beyond n around a few thousand.

The key observation is that an axis-aligned square enclosing all points is completely determined by the extremal coordinates. The smallest rectangle that contains all points has width `max_x - min_x` and height `max_y - min_y`. Any square must have side length at least the larger of these two values, because shrinking either dimension would exclude at least one extreme point.

Once we accept that the side length is fixed by these extremes, the optimal square is simply the minimal square whose side is `max(max_x - min_x, max_y - min_y)`. We do not need to consider position choices beyond ensuring the square can be placed anywhere; shifting the square does not change the required side length.

Thus, each test case reduces to a linear scan computing min and max for x and y.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) or worse | O(1) | Too slow |
| Optimal | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read all points and track four values: minimum x, maximum x, minimum y, maximum y. These four values capture the entire geometric spread of the set without storing intermediate structure.
2. Compute horizontal span as `dx = max_x - min_x`. This represents the smallest possible width of any axis-aligned rectangle containing all points.
3. Compute vertical span as `dy = max_y - min_y`. This represents the smallest possible height of any such rectangle.
4. Determine the required square side length as `side = max(dx, dy)`. This step enforces the square constraint by ensuring both dimensions fit within a single equal-length side.
5. Compute area as `side * side` and output it for the test case.

The key reason step 4 is correct is that any square must simultaneously cover both horizontal and vertical spreads. If the side were smaller than either dx or dy, at least one pair of extreme points would lie outside the square in that dimension.

### Why it works

The set of points defines a minimum bounding rectangle aligned with axes. Any axis-aligned square that contains all points must fully contain this rectangle. Therefore, its side length cannot be smaller than the larger side of the rectangle. Conversely, a square of side `max(dx, dy)` can always be positioned to cover the bounding rectangle, since we are not constrained to a fixed origin. This makes the computed side both necessary and sufficient, which guarantees optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        min_x = 10**18
        max_x = -10**18
        min_y = 10**18
        max_y = -10**18

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

        dx = max_x - min_x
        dy = max_y - min_y
        side = max(dx, dy)
        out.append(str(side * side))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly maintains running extrema for x and y while reading input, avoiding storing the point list. This is important because the total number of points across all test cases can reach 200,000.

The only subtlety is initialization of min and max values. Using large sentinel values ensures correctness for negative coordinates as well. The final square side computation uses integer arithmetic only, which is safe since differences are within 64-bit range.

## Worked Examples

### Example 1

Input:

```
1
2
0 0
10 1
```

We track extrema as follows:

| Step | min_x | max_x | min_y | max_y | dx | dy | side |
| --- | --- | --- | --- | --- | --- | --- | --- |
| After (0,0) | 0 | 0 | 0 | 0 | - | - | - |
| After (10,1) | 0 | 10 | 0 | 1 | 10 | 1 | 10 |

The final side is 10, so the area is 100. This confirms that even though the vertical spread is small, the square must expand to match the horizontal span.

### Example 2

Input:

```
1
3
-2 0
0 2
2 0
```

| Step | min_x | max_x | min_y | max_y | dx | dy | side |
| --- | --- | --- | --- | --- | --- | --- | --- |
| After (-2,0) | -2 | -2 | 0 | 0 | - | - | - |
| After (0,2) | -2 | 0 | 0 | 2 | 2 | 2 | 2 |
| After (2,0) | -2 | 2 | 0 | 2 | 4 | 2 | 4 |

Final side is 4, so area is 16. This case shows a symmetric spread where horizontal range dominates after processing all points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each point is processed once to update extrema |
| Space | O(1) | Only four variables are maintained regardless of input size |

The total time over all test cases is O(2·10^5), which fits comfortably within limits. Memory usage is constant aside from input buffering.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        min_x = 10**18
        max_x = -10**18
        min_y = 10**18
        max_y = -10**18

        for _ in range(n):
            x, y = map(int, input().split())
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        side = max(max_x - min_x, max_y - min_y)
        out.append(str(side * side))

    return "\n".join(out)

# provided sample
assert run("""2
2
0 0
1 0
2
0 0
0 4
""") == "1\n16"

# single point
assert run("""1
1
5 5
""") == "0"

# all points same line horizontal
assert run("""1
3
0 0
5 0
10 0
""") == "100"

# all points same line vertical
assert run("""1
3
2 1
2 5
2 9
""") == "64"

# mixed negative coordinates
assert run("""1
2
-3 -3
1 2
""") == "25"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 0 | zero-area degenerate square |
| horizontal line | 100 | width dominates height |
| vertical line | 64 | height dominates width |
| mixed negatives | 25 | correct handling of negative bounds |

## Edge Cases

For a single point like `(5, 5)`, the algorithm sets all extrema equal, producing `dx = dy = 0` and therefore area `0`. This matches the fact that a square of side zero still contains the point.

For points aligned horizontally such as `(0,0), (5,0), (10,0)`, the vertical span is zero while horizontal span is 10. The algorithm computes `side = 10`, producing area 100. Any attempt to use rectangle area would incorrectly output 0 for height contribution or 0 for area if mishandled.

For vertically aligned points like `(2,1), (2,5), (2,9)`, the horizontal span is zero and vertical span is 8. The algorithm returns side 8 and area 64, correctly expanding horizontally even though no horizontal spread exists.

For mixed negative coordinates like `(-3,-3)` and `(1,2)`, extrema handling ensures correct differences regardless of sign. The computed spans are `dx = 4`, `dy = 5`, giving side 5 and area 25. This confirms that initialization and min/max updates correctly handle full integer range.
