---
title: "CF 102501F - Icebergs"
description: "Edit We are given several icebergs, where each iceberg is described by the ordered list of points on its border. The points form a simple polygon, meaning the border never crosses itself."
date: "2026-08-06T18:51:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102501
codeforces_index: "F"
codeforces_contest_name: "2019-2020 ICPC Southwestern European Regional Programming Contest (SWERC 2019-20)"
rating: 0
weight: 102501
solve_time_s: 65
verified: true
draft: false
---

[CF 102501F - Icebergs](https://codeforces.com/problemset/problem/102501/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
Edit

# Problem Understanding

We are given several icebergs, where each iceberg is described by the ordered list of points on its border. The points form a simple polygon, meaning the border never crosses itself. The task is to find the combined surface area of all polygons and print the integer part of that area, which means rounding down.

The input size is designed around the fact that the total amount of geometry data is small. There can be up to 1000 polygons, and each polygon has at most 50 vertices, so the total number of vertices is at most 50000. This rules out algorithms that repeatedly compare every pair of vertices or scan a large coordinate grid. A grid based solution is impossible because coordinates can be as large as 10^6, creating an area of 10^12 cells for a single direction. The intended solution needs to process each vertex a constant number of times.

The main edge cases come from the way polygon areas are represented. A polygon may be listed clockwise or counterclockwise, and both descriptions represent the same physical iceberg. A careless implementation that assumes one orientation can produce a negative answer.

For example:

```
1
4
0 0
0 1
1 1
1 0
```

The correct output is:

```
1
```

The points are given clockwise, so the signed area from the shoelace formula is negative. Taking the value without applying an absolute value would incorrectly produce a negative result.

Another edge case is a polygon whose area is not an integer.

```
1
3
0 0
1 0
0 1
```

The correct output is:

```
0
```

The triangle has area 0.5, and the required operation is to discard the fractional part. Rounding to the nearest integer would give a different answer, so the implementation must keep the exact doubled area.

## Approaches

The straightforward approach is to try to measure the inside of each polygon directly. One possible method is to create a grid of all coordinates inside the bounding rectangle and test every cell. This works because the coordinates define a flat plane, but it immediately fails for this problem. A polygon spanning from 0 to 10^6 in both dimensions would require checking around 10^12 cells, which is far beyond the allowed time.

A better geometric observation is that a polygon area does not depend on the individual shape of its interior. The border points contain enough information. By connecting every vertex to a fixed origin, the polygon can be divided into triangles. The signed area contribution of each consecutive pair of vertices is computed using the cross product:

[
x_i y_{i+1} - y_i x_{i+1}
]

The sum of these contributions is twice the signed area of the polygon. The sign only tells us the direction in which the vertices are ordered, so taking the absolute value gives the actual doubled area.

The brute force approach works because it directly models the region covered by ice, but it ignores the much smaller amount of information stored in the boundary. The observation that polygon area can be recovered from boundary points reduces the problem from depending on coordinate size to depending only on the number of vertices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(area of bounding boxes) | O(area of bounding boxes) | Too slow |
| Shoelace Formula | O(total number of vertices) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read every polygon and store its vertices in order. The order matters because the shoelace formula uses pairs of neighboring points around the boundary.
2. For every edge from vertex `i` to vertex `i + 1`, add the cross product contribution `x_i * y_{i+1} - y_i * x_{i+1}` to the polygon's doubled signed area.
3. Take the absolute value of the accumulated value for the polygon. This removes the effect of whether the vertices were given clockwise or counterclockwise.
4. Add the doubled area of every polygon into a global total. The icebergs do not overlap, so their areas can simply be summed.
5. Divide the final doubled area by two using integer division. This gives the required value with the fractional part removed.

Why it works:

The shoelace formula is derived by summing the signed areas of triangles formed by consecutive polygon edges and the origin. Every triangle inside the polygon contributes exactly once, while outside regions created by the origin cancel through opposite signs. Because the polygon is simple, the result is exactly the signed area of the polygon. Taking the absolute value gives the real area, and summing the doubled areas preserves exactness until the final truncation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    total_twice = 0

    for _ in range(n):
        p = int(input())
        points = []
        for _ in range(p):
            x, y = map(int, input().split())
            points.append((x, y))

        twice = 0
        for i in range(p):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % p]
            twice += x1 * y2 - y1 * x2

        total_twice += abs(twice)

    print(total_twice // 2)

if __name__ == "__main__":
    solve()
```

The input is processed polygon by polygon because each iceberg is independent. The list of vertices is stored temporarily because the last vertex must connect back to the first vertex when computing the final edge.

The loop over edges uses `(i + 1) % p` to handle the closing side of the polygon. Without the modulo operation, the edge from the last point back to the first point would be missed, which is a common source of incorrect answers.

The calculation is performed with doubled areas instead of floating point numbers. Since all coordinates are integers, every shoelace contribution is also an integer. Keeping this value exact avoids precision errors and makes the final floor operation just an integer division.

Python integers automatically grow beyond fixed machine sizes, which is useful here because the total cross product can be around 10^16.

## Worked Examples

For a unit square:

```
1
4
0 0
1 0
1 1
0 1
```

The calculation is:

| Edge | Cross product contribution | Running doubled area |
| --- | --- | --- |
| (0,0) to (1,0) | 0 | 0 |
| (1,0) to (1,1) | 1 | 1 |
| (1,1) to (0,1) | 1 | 2 |
| (0,1) to (0,0) | 0 | 2 |

The doubled area is 2, so the real area is 1. The example confirms that the algorithm handles a basic polygon and the final division correctly.

For a right triangle:

```
1
3
0 0
20 0
0 20
```

The calculation is:

| Edge | Cross product contribution | Running doubled area |
| --- | --- | --- |
| (0,0) to (20,0) | 0 | 0 |
| (20,0) to (0,20) | 400 | 400 |
| (0,20) to (0,0) | 0 | 400 |

The doubled area is 400, giving an area of 200. The example shows how the method handles non rectangular shapes without needing to inspect the inside of the polygon.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V) | Every vertex is used in one cross product, where V is the total number of vertices across all icebergs. |
| Space | O(P) | Only the current polygon's vertices are stored. |

The maximum number of vertices is 50000, so the linear solution performs only a small number of arithmetic operations and easily fits within the limits.

## Test Cases

```python
import sys
import io

def solve_data(data):
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)
    solve()
    sys.stdin = old_stdin

def run(inp: str) -> str:
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve_data(inp)
    result = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return result

assert run("""1
4
0 0
1 0
1 1
0 1
""") == "1\n", "sample style square"

assert run("""2
3
0 0
20 0
0 20
4
0 0
2 0
2 2
0 2
""") == "202\n", "multiple polygons"

assert run("""1
3
0 0
1 0
0 1
""") == "0\n", "fractional area"

assert run("""1
4
0 0
0 1000000
1000000 1000000
1000000 0
""") == "1000000000000\n", "large coordinates"

assert run("""1
3
0 0
0 5
5 0
""") == "12\n", "clockwise orientation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Unit square | 1 | Basic shoelace computation |
| Two polygons | 202 | Independent area accumulation |
| Half unit triangle | 0 | Correct truncation of fractional areas |
| Large square | 1000000000000 | Large coordinate handling |
| Clockwise triangle | 12 | Orientation independence |

## Edge Cases

A clockwise polygon produces the same physical iceberg as a counterclockwise polygon, but the shoelace sum changes sign. For the input:

```
1
4
0 0
0 1
1 1
1 0
```

the accumulated doubled area is `-2`. The algorithm converts it to `2` before adding it to the answer, producing the correct output `1`.

A polygon with fractional area must not be rounded. For:

```
1
3
0 0
1 0
0 1
```

the doubled area is `1`, so integer division gives `1 // 2 = 0`. The algorithm follows the required floor behavior exactly.

The final edge of the polygon is another subtle case. For:

```
1
3
0 0
2 0
0 2
```

the last edge is from `(0,2)` back to `(0,0)`. The modulo operation includes this edge, producing doubled area `4` and output `2`. Omitting this edge would produce the wrong result even though all listed points were processed.
