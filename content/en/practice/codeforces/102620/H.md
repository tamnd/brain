---
title: "CF 102620H - Icebergs"
description: "The problem describes a collection of icebergs, where each iceberg is given as a simple polygon through the coordinates of its border points. The task is to compute the total area covered by all icebergs and output only the integer part of that area."
date: "2026-07-31T03:31:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102620
codeforces_index: "H"
codeforces_contest_name: "mBIT Standard June 2020"
rating: 0
weight: 102620
solve_time_s: 97
verified: true
draft: false
---

[CF 102620H - Icebergs](https://codeforces.com/problemset/problem/102620/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a collection of icebergs, where each iceberg is given as a simple polygon through the coordinates of its border points. The task is to compute the total area covered by all icebergs and output only the integer part of that area. The polygons do not overlap, so their individual areas can simply be added together. The input contains several independent polygon descriptions, and the output is the sum of their areas rounded down.

The number of polygons can reach 1000, and each polygon has at most 50 vertices. This means the total number of vertices is at most 50000, so an algorithm that processes each vertex a constant number of times is easily fast enough. A method that compares every pair of edges of every polygon would still work for these limits in some situations, but it is unnecessary. The intended approach should be linear in the number of vertices because the geometry has a direct formula.

The main edge cases come from polygon orientation and fractional areas. A polygon can be listed clockwise or counterclockwise, so directly applying the signed area formula without taking care of the sign can produce a negative result. For example:

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

A careless implementation might compute a signed area of `-1` and incorrectly print a negative value.

Another case is when the real area is not an integer. For example:

```
1
3
0 0
1 0
0 1
```

The actual area is `0.5`, so the required output is:

```
0
```

The answer is not rounded to the nearest integer. The fractional part must always be discarded.

A final common mistake is forgetting that the last vertex connects back to the first one. For this input:

```
1
4
0 0
2 0
2 2
0 2
```

the output is:

```
4
```

Ignoring the closing edge leaves an incomplete polygon and gives the wrong area.

## Approaches

The brute force approach would be to divide each polygon into many small pieces or attempt to simulate the interior of the shape on a grid. This is unnecessary because the coordinates are exact and the polygon boundary already contains enough information. A grid based solution would depend on the coordinate range, which can reach one million, making the number of possible cells far too large.

The key observation is that a polygon area can be obtained directly from its boundary using the shoelace formula. Each consecutive pair of vertices contributes a signed value that represents the area of a triangle formed with the origin. When all contributions are summed, overlapping signed regions cancel correctly, leaving exactly the polygon's area.

The brute force method works because it tries to reconstruct the inside of the iceberg, but it ignores the fact that the boundary already describes the shape completely. The observation that the area depends only on ordered edges lets us reduce the problem to a single pass over all vertices.

For a polygon with vertices `(x1, y1), (x2, y2), ... , (xp, yp)`, the signed double area is:

$$S = \sum_{i=1}^{p}(x_i y_{i+1} - x_{i+1} y_i)$$

where the next vertex after the last one is the first vertex. The actual area is `abs(S) / 2`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(area of coordinate range) | O(1) | Too slow |
| Shoelace Formula | O(total number of vertices) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of polygons. For each polygon, store the first vertex because the final edge must connect back to it.
2. Traverse every vertex and add the cross product contribution between the current vertex and the next vertex. The contribution is `x1*y2 - x2*y1`.
3. After processing all edges, take the absolute value of the accumulated value because the input order may describe the polygon in either direction.
4. Add the doubled area to a global sum. Keeping everything doubled avoids floating point errors while processing the geometry.
5. After all polygons are processed, divide the total doubled area by two using integer division. This automatically removes the fractional part as required.

Why it works:

The shoelace formula is based on decomposing the polygon into signed triangles. If vertices are ordered counterclockwise, all triangles contribute positively. If they are ordered clockwise, all contributions are negative. Taking the absolute value restores the real doubled area. Since polygons do not overlap, adding the doubled areas of all polygons gives exactly twice the total covered area. Integer division by two then gives the required floor value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    total2 = 0

    for _ in range(n):
        p = int(input())
        points = []

        for _ in range(p):
            x, y = map(int, input().split())
            points.append((x, y))

        area2 = 0
        for i in range(p):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % p]
            area2 += x1 * y2 - x2 * y1

        total2 += abs(area2)

    print(total2 // 2)

if __name__ == "__main__":
    solve()
```

The input is processed polygon by polygon because only the current boundary is needed. The list of points is stored temporarily so that the last vertex can be connected back to the first vertex.

The expression `(i + 1) % p` handles the closing edge. Without the modulo operation, the final side of every polygon would be missing.

The calculation uses doubled areas instead of floating point values. Coordinates can be as large as one million, so cross products can be large, but Python integers automatically expand to hold the required values. The absolute value is applied per polygon before adding to the final answer because every polygon may have its own orientation.

## Worked Examples

For the first sample:

```
1
4
0 0
1 0
1 1
0 1
```

| Step | Current edge | Contribution | Accumulated doubled area |
| --- | --- | --- | --- |
| 1 | (0,0) to (1,0) | 0 | 0 |
| 2 | (1,0) to (1,1) | 1 | 1 |
| 3 | (1,1) to (0,1) | 1 | 2 |
| 4 | (0,1) to (0,0) | 0 | 2 |

The doubled area is `2`, so the real area is `1`. This demonstrates the normal counterclockwise case.

For the second sample:

```
2
5
98 35
79 90
21 90
2 36
50 0
3
0 0
20 0
0 20
```

The two polygons produce:

| Polygon | Doubled area | Area |
| --- | --- | --- |
| Pentagon | 11801 | 5900.5 |
| Triangle | 400 | 200 |

The total doubled area is `12201`. Dividing by two gives `6100`, which matches the required floor operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V) | Each vertex from every polygon is processed once |
| Space | O(P) | Only the current polygon's vertices are stored |

The maximum total number of vertices is small enough that a linear scan easily fits within the limits. The algorithm performs only simple arithmetic operations and avoids any dependence on coordinate magnitude.

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

assert run("""1
4
0 0
1 0
1 1
0 1
""") == "1\n", "sample 1"

assert run("""2
5
98 35
79 90
21 90
2 36
50 0
3
0 0
20 0
0 20
""") == "6100\n", "sample 2"

assert run("""1
3
0 0
1 0
0 1
""") == "0\n", "half area"

assert run("""1
4
0 0
0 1
1 1
1 0
""") == "1\n", "clockwise polygon"

assert run("""1
4
0 0
1000000 0
1000000 1000000
0 1000000
""") == "1000000000000\n", "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Unit square | 1 | Basic shoelace calculation |
| Pentagon plus triangle | 6100 | Multiple polygons and flooring |
| Right triangle | 0 | Fractional area handling |
| Clockwise square | 1 | Orientation independence |
| Large square | 1000000000000 | Large integer arithmetic |

## Edge Cases

A clockwise polygon is handled by taking the absolute value of the signed area. For:

```
1
4
0 0
0 1
1 1
1 0
```

the accumulated doubled area is `-2`. The algorithm converts it to `2`, then divides by two to get `1`.

A polygon with a fractional area keeps the doubled value until the final operation. For:

```
1
3
0 0
1 0
0 1
```

the doubled area is `1`. The algorithm computes `1 // 2`, producing `0`, which matches the required floor behavior.

The closing edge is included by using the first vertex after the last one. For:

```
1
4
0 0
2 0
2 2
0 2
```

the final contribution from `(0,2)` back to `(0,0)` is included, giving doubled area `8` and final answer `4`.
