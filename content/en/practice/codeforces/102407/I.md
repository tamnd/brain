---
title: "CF 102407I - \u0412\u044b\u0440\u0432\u0430\u0442\u044c\u0441\u044f \u0438\u0437 \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u044f"
description: "We have an (n times n) grid, with the Joker at cell ((a,b)). We need to count cells inside the grid whose Manhattan distance from the Joker is exactly (d). For a cell ((x,y)), the condition is [ ] Without the grid boundaries, these cells form a diamond around ((a,b))."
date: "2026-08-11T16:19:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102407
codeforces_index: "I"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102407
solve_time_s: 88
verified: true
draft: false
---

[CF 102407I - \u0412\u044b\u0440\u0432\u0430\u0442\u044c\u0441\u044f \u0438\u0437 \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/102407/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n \times n) grid, with the Joker at cell ((a,b)). We need to count cells inside the grid whose Manhattan distance from the Joker is exactly (d).

For a cell ((x,y)), the condition is

[
|x-a|+|y-b|=d.
]

Without the grid boundaries, these cells form a diamond around ((a,b)). The diamond has four diagonal sides, and on an unrestricted infinite grid it contains exactly (4d) cells. The difficulty is that some parts of this diamond can lie outside the (n \times n) room.

The input contains (n,a,b,d), where (n) is as large as (10^{18}). The answer itself can also be of order (10^{18}), so the implementation needs integer arithmetic that comfortably handles values larger than 32-bit integers. Python integers are suitable for this directly.

The size of (n) rules out iterating over the grid. Even scanning all (n^2) cells would require up to (10^{36}) checks in the largest case. An approach proportional to (d) is also impossible because (d) can independently reach (10^{18}). We need a constant amount of work, independent of both (n) and (d).

There are several boundary cases where a simple formula such as (4d) fails. For example, with input `5 1 1 2`, the unrestricted diamond has eight cells, but only three fit inside the room: ((1,3)), ((2,2)), and ((3,1)). The correct answer is `3`, so blindly returning (4d) would count cells outside the room.

Another subtle case is the diamond corner. For `3 2 2 1`, all four cells at distance one are inside the room, so the answer is `4`. If we count the four diagonal sides independently, every side contains two endpoints and the total is eight. Each of the four diamond vertices belongs to two neighboring sides, so simply adding the four side lengths double-counts every vertex and produces `8` instead of `4`.

A third case occurs when the entire diamond is outside the room. For `3 2 2 10`, no cell can have Manhattan distance ten from the center because the maximum possible distance inside the grid is four. The correct answer is `0`. Any solution that assumes at least one point of the theoretical diamond survives would fail here.

## Approaches

The direct approach is to inspect every cell ((x,y)) of the room and test whether (|x-a|+|y-b|=d). It is correct because it examines every possible cell exactly once and applies the definition of Manhattan distance directly. Its worst-case running time is (O(n^2)), which becomes (10^{36}) cell checks when (n=10^{18}). The memory usage can remain (O(1)), but the running time makes the approach unusable.

We can do better by looking at the geometry of the equation instead of the individual cells. The equation

[
|x-a|+|y-b|=d
]

describes four diagonal line segments. Their endpoints are

[
(a-d,b),\quad (a,b+d),\quad (a+d,b),\quad (a,b-d).
]

For example, the segment from ((a-d,b)) to ((a,b+d)) can be parameterized as

[
(x,y)=(a-d+k,b+k),\qquad 0\le k\le d.
]

Every integer (k) gives exactly one grid cell on that side of the diamond. The other three sides have the same structure, with the signs of the coordinate changes adjusted accordingly.

The brute-force approach works because it considers all cells independently, but it fails because there are far too many cells. The observation that the desired set consists of only four monotone diagonal segments lets us replace an enormous two-dimensional search with four one-dimensional intervals.

For one such segment, we do not need to iterate over (k=0,1,\ldots,d). We only need to determine which values of (k) keep both coordinates inside ([1,n]). Since each coordinate changes by exactly (+1) or (-1) as (k) increases, each coordinate restriction is simply an interval of allowed (k)-values. Intersecting those intervals gives the exact number of valid cells on the segment in constant time.

There is one final detail. Adjacent diamond segments share their endpoint, so summing the four clipped segments counts every diamond vertex twice whenever that vertex itself lies inside the room. We subtract one for every such vertex. A vertex outside the room cannot create a duplicate inside the room because the two segments meet only at that vertex.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(1)) | Too slow |
| Optimal | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Represent each of the four sides of the Manhattan-distance diamond as a parameterized segment. The four starting points are ((a-d,b)), ((a,b+d)), ((a+d,b)), and ((a,b-d)), and each segment moves for exactly (d) unit steps in one of the four diagonal directions. This covers every cell at Manhattan distance exactly (d) before applying the room boundaries.
2. For one segment, introduce an integer parameter (k) with (0\le k\le d). Its coordinates have the form

[
x=x_0+s_xk,\qquad y=y_0+s_yk,
]

where (s_x,s_y) are each either (1) or (-1). Every valid integer (k) corresponds to one cell on that side.
3. Convert the condition (1\le x\le n) into an interval for (k). If (s_x=1), then

[
1-x_0\le k\le n-x_0.
]

If (s_x=-1), then

[
x_0-n\le k\le x_0-1.
]

Do the same for the (y)-coordinate. Intersect both coordinate intervals with the original interval ([0,d]).
4. If the resulting lower bound is (L) and upper bound is (R), the segment contributes (R-L+1) cells when (L\le R), and contributes zero otherwise. This handles a completely outside segment and a partially clipped segment with exactly the same calculation.
5. Sum the contributions of all four segments. The four segments cover the entire Manhattan-distance diamond, but each diamond vertex belongs to two segments.
6. Check the four vertices ((a-d,b)), ((a,b+d)), ((a+d,b)), and ((a,b-d)). For every vertex whose two coordinates are inside ([1,n]), subtract one from the sum. This removes precisely the duplicate occurrence created by the two adjacent segments.

### Why it works

Every cell at Manhattan distance (d) lies on exactly one of the four diagonal sides of the diamond, except for the four diamond vertices, which lie on two neighboring sides. The parameterization of each side generates every integer cell on that side exactly once. The interval intersection keeps exactly those generated cells whose coordinates belong to the room. Consequently, summing the four clipped segments counts every valid cell once and every valid diamond vertex twice. Subtracting one for each vertex inside the room removes exactly those duplicate counts, leaving every required cell counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def segment_count(x0, y0, sx, sy, d, n):
    lo = 0
    hi = d

    if sx == 1:
        lo = max(lo, 1 - x0)
        hi = min(hi, n - x0)
    else:
        lo = max(lo, x0 - n)
        hi = min(hi, x0 - 1)

    if sy == 1:
        lo = max(lo, 1 - y0)
        hi = min(hi, n - y0)
    else:
        lo = max(lo, y0 - n)
        hi = min(hi, y0 - 1)

    if lo > hi:
        return 0
    return hi - lo + 1

def solve():
    n, a, b, d = map(int, input().split())

    segments = [
        (a - d, b, 1, 1),
        (a, b + d, 1, -1),
        (a + d, b, -1, -1),
        (a, b - d, -1, 1),
    ]

    answer = 0

    for x0, y0, sx, sy in segments:
        answer += segment_count(x0, y0, sx, sy, d, n)

    vertices = [
        (a - d, b),
        (a, b + d),
        (a + d, b),
        (a, b - d),
    ]

    for x, y in vertices:
        if 1 <= x <= n and 1 <= y <= n:
            answer -= 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The `segment_count` function is the core of the solution. It starts with the natural parameter range (0\le k\le d), which represents the complete diamond side. Each coordinate then narrows this range according to the grid boundaries.

For a positive direction, such as (x=x_0+k), the lower boundary (x\ge1) gives (k\ge1-x_0), while the upper boundary (x\le n) gives (k\le n-x_0). For a negative direction, (x=x_0-k), the inequalities reverse and give (k\ge x_0-n) and (k\le x_0-1). Handling these inequalities directly avoids any special cases based on whether the Joker is near a particular side of the room.

The four segment descriptions use consecutive diamond vertices. Their direction pairs are ((1,1)), ((1,-1)), ((-1,-1)), and ((-1,1)), so each side is traversed exactly once.

The vertex subtraction happens after all four segment counts have been computed. A vertex is duplicated only when that vertex itself is inside the room. Checking its coordinates explicitly is safer than trying to infer this from neighboring segment lengths.

There is no overflow issue in Python because its integers have arbitrary precision. In languages with fixed-width integer types, 64-bit signed integers are sufficient for the input coordinates and for the answer, since the answer cannot exceed the number of cells in the room, (10^{36}), actually the number on a distance ring is at most (4d), which is at most (4\cdot10^{18}), so an unsigned 64-bit type or a sufficiently wide signed type is needed depending on the language.

## Worked Examples

### Sample 1

For `5 3 3 2`, the Joker is at the center of the room and the entire distance-two diamond fits inside the grid.

| Segment | Start | Direction | Valid (k) | Contribution |
| --- | --- | --- | --- | --- |
| 1 | ((1,3)) | ((1,1)) | (0..2) | 3 |
| 2 | ((3,5)) | ((1,-1)) | (0..2) | 3 |
| 3 | ((5,3)) | ((-1,-1)) | (0..2) | 3 |
| 4 | ((3,1)) | ((-1,1)) | (0..2) | 3 |
|  |  |  | Segment sum | 12 |

All four diamond vertices are inside the room, so each was counted twice. We subtract four:

[
12-4=8.
]

The output is `8`.

This example demonstrates why the vertex correction is necessary even when the diamond is completely contained in the room.

### Sample 2

For `5 2 3 4`, the theoretical diamond is much larger than the room. Only small pieces of two opposite sides reach the grid.

| Segment | Start | Direction | Valid (k) | Contribution |
| --- | --- | --- | --- | --- |
| 1 | ((-2,3)) | ((1,1)) | (3..4) | 2 |
| 2 | ((2,7)) | ((1,-1)) | none | 0 |
| 3 | ((6,3)) | ((-1,-1)) | (1..2) | 2 |
| 4 | ((2,-1)) | ((-1,1)) | none | 0 |
|  |  |  | Segment sum | 4 |

None of the four diamond vertices is inside the room, so there is no duplicate to subtract. The answer is `4`.

This trace demonstrates why clipping each side independently handles a diamond that is mostly outside the room without requiring any special geometric case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | Four segments and four vertices are processed, with a constant number of arithmetic operations each. |
| Space | (O(1)) | Only a constant number of coordinates and interval bounds are stored. |

The constraints allow (n) and (d) to reach (10^{18}), so neither the grid size nor the radius can be used as an iteration bound. The algorithm performs the same constant amount of work for every input, making it easily fast enough for the two-second limit and using negligible memory.

## Test Cases

```python
import sys
import io

def segment_count(x0, y0, sx, sy, d, n):
    lo = 0
    hi = d

    if sx == 1:
        lo = max(lo, 1 - x0)
        hi = min(hi, n - x0)
    else:
        lo = max(lo, x0 - n)
        hi = min(hi, x0 - 1)

    if sy == 1:
        lo = max(lo, 1 - y0)
        hi = min(hi, n - y0)
    else:
        lo = max(lo, y0 - n)
        hi = min(hi, y0 - 1)

    return max(0, hi - lo + 1)

def solution(inp: str) -> str:
    n, a, b, d = map(int, inp.split())

    segments = [
        (a - d, b, 1, 1),
        (a, b + d, 1, -1),
        (a + d, b, -1, -1),
        (a, b - d, -1, 1),
    ]

    answer = sum(
        segment_count(x0, y0, sx, sy, d, n)
        for x0, y0, sx, sy in segments
    )

    vertices = [
        (a - d, b),
        (a, b + d),
        (a + d, b),
        (a, b - d),
    ]

    for x, y in vertices:
        if 1 <= x <= n and 1 <= y <= n:
            answer -= 1

    return str(answer)

def run(inp: str) -> str:
    return solution(inp).strip()

# Provided samples
assert run("5 3 3 2") == "8", "sample 1"
assert run("5 2 3 4") == "4", "sample 2"
assert run(
    "1000000000000000000 123456789987654321 "
    "987654321123456789 543211234567899876"
) == "679013703432097408", "sample 3"

# Minimum-size input
assert run("1 1 1 1") == "0", "no cell can be at positive distance"

# Entire ring fits, checking duplicate diamond vertices
assert run("5 3 3 1") == "4", "four immediate neighbors"

# Diamond starts at a corner and is heavily clipped
assert run("5 1 1 2") == "3", "corner clipping"

# All n, a, b, d equal
assert run("5 5 5 5") == "0", "all-equal boundary values"

# Maximum-size coordinates and radius
assert run("1000000000000000000 1 1 1000000000000000000") == \
       "999999999999999999", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `0` | Minimum grid and empty distance ring |
| `5 3 3 1` | `4` | All four vertices are inside and must be de-duplicated |
| `5 1 1 2` | `3` | Corner clipping and boundary inequalities |
| `5 5 5 5` | `0` | A large radius can produce no cells at all |
| `10^18 1 1 10^18` | `999999999999999999` | Maximum coordinate and radius values |

## Edge Cases

For `5 1 1 2`, the four theoretical vertices are ((-1,1)), ((1,3)), ((3,1)), and ((1,-1)). Only the middle two vertices are inside, while the diagonal sides between them produce the third valid point ((2,2)). The segment clipping gives exactly three total cells, and the two inside vertices are each counted twice before the duplicate correction. The final answer is `3`.

For `3 2 2 1`, the four vertices are ((1,2)), ((2,3)), ((3,2)), and ((2,1)). Each segment contains two points, giving a raw total of eight. Every one of the four vertices is inside the room, so four duplicate occurrences are removed. The result is `4`.

For `3 2 2 10`, every theoretical vertex lies outside the room, and every segment's allowed (k)-interval becomes empty after intersecting the coordinate restrictions. All four segment contributions are zero, and there are no vertices to subtract. The result is `0`.

For `5 3 3 2`, every side has three valid parameter values, so the raw segment total is twelve. The four diamond vertices are inside the room and are exactly the four duplicated cells. Subtracting them leaves `8`, matching the sample and confirming the invariant that only adjacent-side endpoints are duplicated.

If you want, I can also turn this into a more typical **Codeforces-style concise editorial**, keeping the same proof and solution but reducing the exposition substantially.
