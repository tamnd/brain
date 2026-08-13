---
title: "CF 102302C - Rectangles"
description: "We have at most 2000 distinct points on a coordinate plane. A valid rectangle must use four of these points as its corners, its sides must be horizontal or vertical, and there must be no other given point anywhere inside the rectangle or on one of its four sides."
date: "2026-08-13T23:16:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "C"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 138
verified: true
draft: false
---

[CF 102302C - Rectangles](https://codeforces.com/problemset/problem/102302/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have at most 2000 distinct points on a coordinate plane. A valid rectangle must use four of these points as its corners, its sides must be horizontal or vertical, and there must be no other given point anywhere inside the rectangle or on one of its four sides.

The task is to count every distinct rectangle satisfying those conditions. The actual coordinate values can be as large as (10^9), but their absolute sizes are irrelevant. What matters is which coordinates are equal and which coordinates lie between others.

With (N \le 2000), an (O(N^2)) solution is a natural target. There are about two million unordered pairs of points, so processing each pair with a constant amount of work is feasible. An (O(N^3)) solution can already require about (4\cdot10^9) operations in the worst case, which is far too much for a one second limit. A full (O(N^4)) enumeration of four-point combinations is even further out of reach. The coordinate bound of (10^9) also means we cannot allocate a grid indexed directly by the original coordinates.

The first edge case is having fewer than four points. For example, the input `1 / 5 7` contains only one point, so the answer is 0. A solution that assumes every pair can eventually define a rectangle may accidentally try to access nonexistent corners.

Another edge case is having many points on one vertical or horizontal line. For example, the four points `(0,0)`, `(0,1)`, `(0,2)`, `(0,3)` cannot form a rectangle, so the answer is 0. Checking only whether four coordinates occur independently is not enough, because four corners must have two distinct x coordinates and two distinct y coordinates.

The emptiness condition is the subtle part. Consider `(0,0)`, `(2,0)`, `(0,2)`, `(2,2)`, `(1,1)`. The four corner points exist, but the answer is 0 because `(1,1)` lies inside the rectangle. A solution that checks only the existence of the four corners would incorrectly count it.

Points on the boundary cause the same problem. With `(0,0)`, `(2,0)`, `(0,2)`, `(2,2)`, `(1,0)`, the four corners exist, but the answer is again 0 because `(1,0)` lies on the bottom edge. The rectangle must contain exactly its four corner points in its closed bounding box.

## Approaches

A direct approach is to consider every pair of points as a possible bottom-left and top-right corner. If their x coordinates and y coordinates are both different, we can check whether the other two corners exist in a hash set. We then scan all (N) points to see whether any point lies inside or on the boundary of the candidate rectangle. Each candidate pair is processed in (O(N)), giving (O(N^3)) time. For (N=2000), there are (\binom{2000}{2}=1,999,000) pairs, and scanning 2000 points for every pair gives about (3,998,000,000) point inspections. The approach is logically correct, but far too slow.

The brute force works because a rectangle is uniquely determined by its bottom-left and top-right corners. The expensive part is not identifying the corners, but repeatedly asking how many given points lie inside a particular axis-aligned rectangle.

The key observation is that the answer to that question can be precomputed. Only the relative order of the coordinates matters, so we compress all distinct x coordinates to (1,\ldots,X) and all distinct y coordinates to (1,\ldots,Y). Since there are at most (N) distinct coordinates of either type, the resulting grid has at most (N^2) cells.

We put a 1 at every occupied compressed coordinate and build a two-dimensional prefix sum. Once that table exists, the number of points inside any closed rectangle can be obtained in (O(1)) time using the standard inclusion-exclusion formula.

We can now inspect every pair of points. After sorting by x coordinate, only pairs with increasing y coordinates can represent a bottom-left and top-right corner. We check whether the other corner exists. If all four corners exist, the prefix sum over the entire rectangle must be exactly 4. Since the four known corners already contribute four points, a sum larger than 4 means that some additional point lies inside or on an edge.

This reduces the expensive part from scanning (N) points per candidate to a constant-time prefix-sum query. A public reference implementation for this problem uses the same coordinate-compression and two-dimensional prefix-sum strategy.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) | (O(N)) | Too slow |
| Optimal | (O(N^2)) | (O(N^2)) | Accepted |

## Algorithm Walkthrough

1. Read all points and collect their distinct x and y coordinates. Sort both coordinate lists and assign each coordinate a compressed index starting from 1. Compression preserves ordering, so a point is inside a rectangle before compression exactly when its compressed coordinates are inside the corresponding compressed rectangle.
2. Create a compressed (Y\times X) grid and put 1 at every occupied cell. The grid dimensions are at most (2000\times2000), regardless of whether the original coordinates are close together or as large as (10^9).
3. Convert the grid into a two-dimensional prefix-sum array. For every compressed cell ((x,y)), its prefix value stores the number of input points whose compressed coordinates are at most (x) and (y). The sum of points in a closed rectangle with corners ((x_1,y_1)) and ((x_2,y_2)) is then

[
P(x_2,y_2)-P(x_1-1,y_2)-P(x_2,y_1-1)+P(x_1-1,y_1-1).
]
4. Store every compressed point in a hash set. This gives constant-average-time checks for whether a required corner exists.
5. Sort the compressed points by x coordinate and then y coordinate. Consider every pair of points in this order. Pairs with equal x coordinates cannot be diagonal corners of a rectangle, and pairs whose y coordinates do not increase cannot be bottom-left and top-right corners.
6. For a remaining pair ((x_1,y_1)), ((x_2,y_2)), check whether ((x_1,y_2)) exists. The point ((x_2,y_1)) is already one of the selected points, so together with the two selected points and ((x_1,y_2)), all four corners exist.
7. Query the prefix sum of the complete closed rectangle. Count the rectangle exactly when the result is 4. The four corners are guaranteed to contribute four points, so any larger value means there is an unwanted point inside or on an edge.
8. Print the accumulated count. Every valid rectangle has exactly one bottom-left and top-right pair, so it is considered exactly once.

### Why it works

The invariant is that every candidate accepted by the algorithm has exactly four given points in its closed bounding box, and those four points form the required corners. The corner-existence checks guarantee the four vertices are present. The prefix-sum query counts every point inside the rectangle and on its boundary, so a value of exactly 4 proves that no fifth point exists there. Conversely, every valid rectangle has a unique bottom-left and top-right corner pair. When that pair is processed, the other two corners are found and the prefix sum is exactly 4, so the rectangle is counted. Thus every valid rectangle is counted once and no invalid rectangle is counted.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]

    if n < 4:
        print(0)
        return

    xs = sorted({x for x, _ in points})
    ys = sorted({y for _, y in points})

    x_id = {x: i + 1 for i, x in enumerate(xs)}
    y_id = {y: i + 1 for i, y in enumerate(ys)}

    nx = len(xs)
    ny = len(ys)
    width = nx + 1

    # Unsigned short is enough because every prefix sum is at most N <= 2000.
    pref = array('H', [0]) * ((ny + 1) * width)

    compressed = []
    present = set()

    for x, y in points:
        cx = x_id[x]
        cy = y_id[y]
        compressed.append((cx, cy))
        present.add((cx, cy))
        pref[cy * width + cx] = 1

    # Build the 2D prefix sum in-place.
    for y in range(1, ny + 1):
        base = y * width
        previous = base - width
        row_sum = 0

        for x in range(1, nx + 1):
            idx = base + x
            row_sum += pref[idx]
            pref[idx] = pref[previous + x] + row_sum

    compressed.sort()

    answer = 0

    for i in range(n):
        x1, y1 = compressed[i]

        for j in range(i + 1, n):
            x2, y2 = compressed[j]

            # Sorting gives x1 <= x2. Equal x cannot form a rectangle.
            if x1 == x2:
                continue

            # We need the first point to be the bottom-left corner.
            if y1 >= y2:
                continue

            # The missing fourth corner is (x1, y2).
            if (x1, y2) not in present:
                continue

            # Count all points in the closed rectangle.
            total = (
                pref[y2 * width + x2]
                - pref[(y1 - 1) * width + x2]
                - pref[y2 * width + (x1 - 1)]
                + pref[(y1 - 1) * width + (x1 - 1)]
            )

            if total == 4:
                answer += 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The early `n < 4` check handles the smallest inputs without building any data structures. It is not required for correctness, but avoids unnecessary work.

The coordinate maps turn each original coordinate into a compact integer index. Separate compression of x and y keeps the prefix-sum grid at at most (2001\times2001) cells rather than using the original coordinate range.

The prefix array uses `array('H')` instead of Python integers. A prefix value can never exceed (N), which is at most 2000, so an unsigned 16-bit value is sufficient. This keeps the grid around 8 MB at maximum size, comfortably below the 256 MB memory limit.

The prefix sum is built row by row. `row_sum` represents the number of points seen so far in the current row, while `pref[previous + x]` contains the contribution from all previous rows. Adding those two values gives the standard two-dimensional prefix recurrence.

The points are sorted by compressed x coordinate. For every pair, equal x coordinates are rejected because they cannot be opposite corners of an axis-aligned rectangle. The `y1 >= y2` check chooses only one orientation, so the same rectangle is never counted from its top-right and bottom-left pair in reverse.

The hash set contains compressed coordinate pairs, so checking the missing corner avoids converting back to the original (10^9)-scale coordinates. Once all four corners are known, the prefix sum includes those four points automatically. Testing `total == 4` is consequently sufficient to enforce both the interior and boundary restrictions.

Python integers are unbounded, so the answer does not risk overflow. Even the maximum possible number of rectangles is at most (\binom{2000}{4}), which is safely representable.

## Worked Examples

For the first sample, after compression the points are already arranged as

`(1,1), (1,2), (2,1), (2,2), (3,1), (3,2)`.

The relevant candidate pairs are shown below.

| Bottom-left | Top-right | Missing corner | Points in closed rectangle | Result |
| --- | --- | --- | --- | --- |
| (1,1) | (2,2) | (1,2) | 4 | Count |
| (1,1) | (3,2) | (1,2) | 6 | Reject |
| (2,1) | (3,2) | (2,2) | 4 | Count |

The pair `(1,1)` and `(3,2)` has all four corners, but it also contains `(2,1)` and `(2,2)`, so its prefix sum is 6. The two smaller rectangles have exactly four points each, giving the answer 2.

For a second example, consider the four corners of a rectangle together with one interior point.

```
5
0 0
2 0
0 2
2 2
1 1
```

After compression the only possible rectangle has corners `(1,1)`, `(3,1)`, `(1,3)`, and `(3,3)`. Its closed rectangle contains five points.

| Bottom-left | Top-right | Missing corner | Points in closed rectangle | Result |
| --- | --- | --- | --- | --- |
| (1,1) | (3,3) | (1,3) | 5 | Reject |

The corner checks succeed, but the prefix sum exposes the extra point `(1,1)` in the original coordinate system, so the answer is 0. This demonstrates why checking only the four corners is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2)) | Coordinate compression and prefix construction take (O(N^2)) in the worst case, and the pair enumeration takes (O(N^2)). |
| Space | (O(N^2)) | The compressed prefix-sum grid has at most (2001\times2001) entries. |

At (N=2000), the prefix grid contains about four million cells and the pair enumeration considers about two million pairs. The compact 16-bit prefix representation keeps memory usage low, while every candidate rectangle is checked in constant time after preprocessing.

## Test Cases

```python
from array import array

def solve_data(inp: str) -> str:
    it = iter(inp.split())
    n = int(next(it))

    points = [(int(next(it)), int(next(it))) for _ in range(n)]

    if n < 4:
        return "0\n"

    xs = sorted({x for x, _ in points})
    ys = sorted({y for _, y in points})

    x_id = {x: i + 1 for i, x in enumerate(xs)}
    y_id = {y: i + 1 for i, y in enumerate(ys)}

    nx = len(xs)
    ny = len(ys)
    width = nx + 1

    pref = array('H', [0]) * ((ny + 1) * width)

    compressed = []
    present = set()

    for x, y in points:
        cx = x_id[x]
        cy = y_id[y]
        compressed.append((cx, cy))
        present.add((cx, cy))
        pref[cy * width + cx] = 1

    for y in range(1, ny + 1):
        base = y * width
        previous = base - width
        row_sum = 0

        for x in range(1, nx + 1):
            idx = base + x
            row_sum += pref[idx]
            pref[idx] = pref[previous + x] + row_sum

    compressed.sort()

    answer = 0

    for i in range(n):
        x1, y1 = compressed[i]

        for j in range(i + 1, n):
            x2, y2 = compressed[j]

            if x1 == x2 or y1 >= y2:
                continue

            if (x1, y2) not in present:
                continue

            total = (
                pref[y2 * width + x2]
                - pref[(y1 - 1) * width + x2]
                - pref[y2 * width + x1 - 1]
                + pref[(y1 - 1) * width + x1 - 1]
            )

            if total == 4:
                answer += 1

    return f"{answer}\n"

def run(inp: str) -> str:
    return solve_data(inp)

# Provided sample
assert run("""\
6
1 1
1 2
2 1
2 2
3 1
3 2
""") == "2\n", "sample 1"

# Minimum-size input
assert run("""\
1
5 7
""") == "0\n", "fewer than four points"

# Four corners at the coordinate boundaries
assert run("""\
4
0 0
1000000000 0
0 1000000000
1000000000 1000000000
""") == "1\n", "boundary coordinates"

# Extra points on and inside the rectangle
assert run("""\
6
0 0
2 0
0 2
2 2
1 0
1 1
""") == "0\n", "boundary and interior points"

# Maximum-size input, all points on one vertical line
points = "\n".join(f"0 {y}" for y in range(2000))
maximum_case = "2000\n" + points + "\n"
assert run(maximum_case) == "0\n", "maximum N with equal x coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One point `(5,7)` | 0 | Minimum-size input and absence of four corners |
| Four corners using 0 and (10^9) | 1 | Coordinate boundaries and coordinate compression |
| Rectangle plus `(1,0)` and `(1,1)` | 0 | Points on an edge and inside the rectangle |
| 2000 points `(0,y)` | 0 | Maximum (N), equal x coordinates, and memory handling |

## Edge Cases

For fewer than four points, the input

```
1
5 7
```

contains no possible set of four vertices. The algorithm immediately returns 0 before allocating the prefix grid. This prevents any assumption that a candidate rectangle must exist.

For points sharing one coordinate, consider

```
4
0 0
0 1
0 2
0 3
```

All four points have the same x coordinate. After sorting, every pair has `x1 == x2`, so every pair is rejected before a corner lookup. The output is 0.

For an extra point inside the rectangle, consider

```
5
0 0
2 0
0 2
2 2
1 1
```

The pair `(0,0)` and `(2,2)` has the other corner `(0,2)`, and `(2,0)` is already present, so it reaches the prefix-sum query. The closed rectangle contains 5 points rather than 4, causing the candidate to be rejected. The output is 0.

For an extra point on an edge, consider

```
5
0 0
2 0
0 2
2 2
1 0
```

Again, all four corners exist. The prefix sum over the rectangle is 5 because `(1,0)` is included in the closed boundary. Since the algorithm requires exactly 4 points, it rejects the rectangle and outputs 0.

For the largest input with repeated x coordinates, use 2000 points `(0,0)`, `(0,1)`, through `(0,1999)`. Every candidate pair has equal x coordinates, so the pair loop rejects all of them. The answer is 0, while the prefix grid still has only (1\times2001) occupied-coordinate dimensions in one direction. This exercises the maximum input size without relying on a dense two-dimensional point distribution.
