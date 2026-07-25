---
title: "CF 102870I - Irregular Shape of Orz Pandas"
description: "The problem gives the vertices of an irregular polygon in the order they appear around its boundary. Each vertex has integer coordinates. The task is to calculate the exact area enclosed by this polygon and print the result."
date: "2026-07-25T13:18:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102870
codeforces_index: "I"
codeforces_contest_name: "2020-2021 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102870
solve_time_s: 49
verified: true
draft: false
---

[CF 102870I - Irregular Shape of Orz Pandas](https://codeforces.com/problemset/problem/102870/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives the vertices of an irregular polygon in the order they appear around its boundary. Each vertex has integer coordinates. The task is to calculate the exact area enclosed by this polygon and print the result. The input is not describing a grid shape or a collection of cells. It is a geometric boundary, so the order of the points matters because every point is connected to the next one, with the final point connected back to the first.

The number of vertices is small enough that an O(n) solution is the intended direction. Any algorithm that tries every pair of vertices, builds many triangles, or repeatedly performs geometric checks would add unnecessary work. Even though the coordinate values can be large, the polygon vertices are integers, so the area can be represented exactly using integer arithmetic before the final division by two.

A common mistake is to use floating point geometry from the beginning. Large coordinates can make floating point accumulation lose precision, especially when many positive and negative cross products cancel each other. Another mistake is forgetting that the polygon can have a fractional area ending in .5.

Consider a triangle with vertices:

```
3
0 0
1 0
0 1
```

The correct output is:

```
0.5
```

An implementation that stores the area only as an integer would incorrectly output `0`.

Another edge case is a polygon whose points are listed clockwise instead of counterclockwise:

```
4
0 0
0 1
1 1
1 0
```

The signed area becomes negative. The actual geometric area is positive, so the absolute value must be taken before formatting the answer.

A third case is a degenerate polygon:

```
3
0 0
1 1
2 2
```

All points lie on the same line, so the enclosed area is `0`. A correct shoelace implementation naturally handles this because all cross product contributions cancel.

## Approaches

The straightforward approach is to split the polygon into triangles. One can choose the first vertex as a fixed point and compute the area of every triangle formed by it and two neighboring vertices. This is correct because any simple polygon can be partitioned into triangles. However, a careless implementation may repeatedly compute geometric relationships or search for valid diagonals, creating unnecessary complexity.

The key observation is that polygon area does not require explicitly constructing triangles. The shoelace formula directly converts the boundary into a sum of cross products. For every edge from `(x_i, y_i)` to `(x_{i+1}, y_{i+1})`, we add `x_i * y_{i+1} - x_{i+1} * y_i`. The final absolute value of this sum is twice the polygon area.

The formula works because every edge contributes the signed area of a triangle with the origin. When all boundary edges are combined, the outside regions cancel and only the polygon interior remains.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Triangle Construction | O(n²) | O(1) | Too slow and unnecessary |
| Shoelace Formula | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all polygon vertices in their given order. The order must be preserved because the edges of the polygon are defined by consecutive vertices.
2. Iterate through every vertex and pair it with the next vertex in the cycle. For the last vertex, the next vertex is the first one. Add the cross product contribution `x_i * y_next - x_next * y_i` to a running sum.
3. Take the absolute value of the accumulated sum. The sign only tells whether the vertices were listed clockwise or counterclockwise.
4. Format the result by dividing the doubled area by two. If the value is odd, the area has a `.5` fractional part.

Why it works: The shoelace sum is exactly twice the signed area of a polygon. Each directed edge contributes a triangle area relative to the origin. Adding all these signed contributions removes the areas outside the polygon and keeps the interior. Taking the absolute value removes dependence on traversal direction, so the algorithm always returns the true geometric area.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))

    points = []
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        points.append((x, y))

    area2 = 0

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area2 += x1 * y2 - x2 * y1

    area2 = abs(area2)

    if area2 % 2 == 0:
        print(area2 // 2)
    else:
        print(str(area2 // 2) + ".5")

if __name__ == "__main__":
    solve()
```

The input section stores the vertices because the cyclic order is required by the shoelace formula. Keeping the points in a list also makes the wraparound edge from the final vertex back to the first vertex simple and avoids boundary mistakes.

The main loop computes the doubled signed area. Python integers do not overflow, which is useful here because coordinate multiplication can be much larger than the original coordinate range.

The output logic avoids floating point entirely. Since the computed value is twice the area, an even value represents an integer area and an odd value represents an area ending in `.5`.

## Worked Examples

Consider the polygon:

```
4
0 0
2 0
2 2
0 2
```

| Step | Current edge | Contribution | Running area2 |
| --- | --- | --- | --- |
| 1 | (0,0) to (2,0) | 0 | 0 |
| 2 | (2,0) to (2,2) | 4 | 4 |
| 3 | (2,2) to (0,2) | 4 | 8 |
| 4 | (0,2) to (0,0) | 0 | 8 |

The final doubled area is `8`, so the polygon area is `4`. This demonstrates the normal counterclockwise case where every contribution is easy to interpret.

Consider the polygon:

```
3
0 0
1 0
0 1
```

| Step | Current edge | Contribution | Running area2 |
| --- | --- | --- | --- |
| 1 | (0,0) to (1,0) | 0 | 0 |
| 2 | (1,0) to (0,1) | 1 | 1 |
| 3 | (0,1) to (0,0) | 0 | 1 |

The doubled area is `1`, so the answer is `0.5`. This shows why the solution keeps the doubled area and formats the fraction only at the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vertex participates in one cross product calculation |
| Space | O(n) | The vertices are stored to preserve the cyclic order |

The linear runtime easily fits the intended constraints because the algorithm only performs a constant amount of arithmetic per vertex. The memory usage is also small because the only stored data is the polygon boundary.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# helper solution copy
def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    points = [(int(next(it)), int(next(it))) for _ in range(n)]

    area2 = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area2 += x1 * y2 - x2 * y1

    area2 = abs(area2)

    if area2 % 2 == 0:
        print(area2 // 2)
    else:
        print(str(area2 // 2) + ".5")

assert run("""3
0 0
1 0
0 1
""") == "0.5\n", "triangle fraction"

assert run("""4
0 0
2 0
2 2
0 2
""") == "4\n", "square"

assert run("""3
0 0
1 1
2 2
""") == "0\n", "degenerate polygon"

assert run("""4
0 0
0 1
1 1
1 0
""") == "1\n", "clockwise ordering"

assert run("""5
0 0
4 0
5 2
2 4
0 3
""") == "15\n", "irregular polygon"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle with vertices `(0,0),(1,0),(0,1)` | 0.5 | Fractional area handling |
| Square with side length 2 | 4 | Standard polygon calculation |
| Three collinear points | 0 | Degenerate case |
| Clockwise square | 1 | Absolute value handling |
| Irregular five-sided polygon | 15 | General shoelace computation |

## Edge Cases

For the fractional triangle case:

```
3
0 0
1 0
0 1
```

The algorithm computes a doubled area of `1`. Since it is odd, it prints `0.5`. No floating point calculation is needed.

For reversed vertex order:

```
4
0 0
0 1
1 1
1 0
```

The shoelace sum becomes negative because the traversal is clockwise. The absolute value changes the doubled area from `-2` to `2`, producing the correct answer `1`.

For a degenerate polygon:

```
3
0 0
1 1
2 2
```

The cross product contributions cancel each other. The final doubled area is `0`, so the algorithm correctly prints `0`.

For large coordinates, every multiplication is performed using integer arithmetic. Python handles the required precision automatically, so no rounding error can appear from intermediate calculations.

I can also provide a shorter contest-style editorial version if you want one closer to what would appear on a Codeforces tutorial page.
