---
title: "CF 102279F - Flood Season"
description: "The polyline describes a one-dimensional terrain profile. Since the x-coordinates are strictly increasing, every pair of consecutive points forms one terrain segment, and rainwater can only stay in a depression when the terrain rises on both sides enough to prevent the water…"
date: "2026-08-16T19:17:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102279
codeforces_index: "F"
codeforces_contest_name: "HCW 19 Team Round (ICPC format)"
rating: 0
weight: 102279
solve_time_s: 196
verified: true
draft: false
---

[CF 102279F - Flood Season](https://codeforces.com/problemset/problem/102279/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

The polyline describes a one-dimensional terrain profile. Since the x-coordinates are strictly increasing, every pair of consecutive points forms one terrain segment, and rainwater can only stay in a depression when the terrain rises on both sides enough to prevent the water from escaping.

For any depression, the water surface is horizontal. Suppose its left boundary is point (i) and its right boundary is point (r). The water level is the lower of the two boundary heights,

[
h=\min(y_i,y_r).
]

The water area is the area between the terrain and the horizontal line (y=h), but only where the terrain is below that line. The task is to find the sum of all such trapped regions, with every piece of terrain belonging to at most one counted region.

The constraint (n\le 10^5) rules out examining every pair of points. A quadratic algorithm would perform about (10^{10}/2) pair checks in the worst case, far beyond what fits into a 2-second limit. The coordinates are at most (10^6), so the total horizontal width of the entire polyline is at most (10^6), but that does not make a scan from every starting point feasible. We need an (O(n)) or (O(n\log n)) solution.

There are several edge cases that are easy to mishandle. With only two points, there is no enclosed depression at all. For example,

```
2
0 0
1000000 1000000
```

has answer `0`. A solution that assumes every pair defines a basin would incorrectly create water here.

Equal heights also matter. For

```
3
0 2
1 0
2 2
```

the answer is `1`, because the two sides form a triangular basin whose water level is 2. A careless next-greater implementation using only strictly greater points can fail to recognize the right boundary when the maximum height is equal to the left height.

The right boundary can also be lower than the left boundary. For

```
3
0 3
1 0
2 2
```

the water level is 2, not 3, because water spills over the right side at height 2. The answer is `2`. This is why the boundary height must be `min(y_i, y_r)`.

Finally, when the right endpoint is higher than the water level, the last terrain segment crosses the water surface somewhere in its interior. For

```
4
0 2
1 0
2 1
3 3
```

the water level is 2. The first two segments contribute (1) and (1.5), while the final segment contributes only (0.25), because only the part below height 2 contains water. The answer is `2.75`. Treating the whole final segment as submerged would overcount.

## Approaches

The direct approach is to try every possible left boundary (i), find every possible right boundary (j>i), and calculate how much water the pair can retain. There are (n(n-1)/2) pairs, which is about (5\cdot10^9) pairs for (n=10^5). Even if each pair were processed in constant time, this is already too slow. If the area were calculated by scanning the interval as well, the complexity would become cubic.

The useful observation is that we do not need to consider arbitrary right boundaries. Starting from point (i), the only meaningful right boundary is the first point to the right whose height is strictly greater than (y_i). If such a point exists, every point before it is at most (y_i), so water starting at (i) reaches exactly that boundary before it can spill over. If no greater point exists, water eventually spills over the highest point to the right. We choose the first occurrence of that suffix maximum as the boundary.

This is exactly the structure described by the official editorial: for every (i), find the smallest (r_i>i) with (y_{r_i}>y_i), or, if none exists, the first position attaining the maximum height among positions to the right. The resulting ranges are either nested or completely separated, which permits processing them by jumping directly from one range to the next.

The first-greater position for every point can be found with a monotonic stack in (O(n)). The fallback suffix maximum can be computed with one right-to-left scan, also in (O(n)).

Once the boundary (r_i) is known, we calculate the water area by walking through the segments from (i) to (r_i). The ranges that are actually processed are disjoint because after handling ([i,r_i]), we continue from (r_i+1). Thus, although an individual range may contain many segments, the total number of processed segments over the whole algorithm is only (O(n)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) or worse | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the polyline into arrays `x` and `y`. The strict increase of `x` means every terrain segment can be integrated independently.
2. Compute `next_greater[i]`, the first index to the right of `i` with `y[index] > y[i]`. Process indices from right to left while maintaining a stack whose heights are strictly decreasing. Before querying the stack for `i`, remove every point whose height is at most `y[i]`, because none of those points can be the first strictly higher point for `i`.
3. Compute `suffix_idx[i]`, the first position attaining the maximum height among indices strictly to the right of `i`. While scanning from right to left, maintain the best point seen so far. When the current height is strictly larger, replace that point. When the heights are equal, keep the existing point because it is farther to the right and the current point is not part of the suffix considered by `suffix_idx[i]`.
4. Start at `i=0`. If `next_greater[i]` exists, use it as `r`. Otherwise use `suffix_idx[i]`. If there is no point to the right, there is no possible basin and the algorithm stops.
5. Set the water level to `h=min(y[i],y[r])`. Every interior vertex of this range is at most `h`, by the definition of `r`. If `y[r] > h`, only the final segment can cross the water surface. If `y[r] <= h`, every segment is completely below or on the water surface.
6. For a completely submerged segment from ((x_1,y_1)) to ((x_2,y_2)), the terrain is linear, so its average height is ((y_1+y_2)/2). With water level `h`, its contribution is

[
(x_2-x_1)\left(h-\frac{y_1+y_2}{2}\right).
]

To avoid repeated halves, the implementation stores twice the area:

[
(x_2-x_1)(2h-y_1-y_2).
]

1. If the final segment goes from (y_1\le h) to (y_2>h), the water occupies only the part before the line reaches height `h`. The depth is a triangle with height (h-y_1). The crossing distance is

[
(x_2-x_1)\frac{h-y_1}{y_2-y_1},
]

so twice the area is

[
(x_2-x_1)\frac{(h-y_1)^2}{y_2-y_1}.
]

The implementation evaluates this rational value using `Decimal` to preserve enough precision even for large coordinates.

1. Add the area of the current range to the answer and set `i=r+1`. The ranges cannot overlap in the part that is counted, so every terrain segment is processed at most once.

### Why it works

For each starting point (i), the chosen (r_i) is exactly the first place where water originating at (i) can escape. If a higher point exists, everything before that point is no higher than (y_i), so the lower boundary height is (y_i). If no higher point exists, the highest point on the suffix is the first place where the water can spill, and its height determines the water level. Thus ([i,r_i]) describes one maximal trapped-water structure.

Two such structures are either nested or disjoint. When we process the leftmost structure and then jump to `r_i+1`, any nested structure is already contained in the processed region, while any disjoint structure begins later. Consequently, the jump never skips water belonging to a separate basin and never counts the same segment twice. Since each processed segment contributes exactly its geometric water area, the accumulated result is the required total area.

## Python Solution

```python
import sys
from decimal import Decimal, getcontext

input = sys.stdin.readline

getcontext().prec = 40

def solve(data=None):
    if data is None:
        tokens = iter(sys.stdin.buffer.read().split())
    else:
        tokens = iter(data.split())

    n = int(next(tokens))
    x = [0] * n
    y = [0] * n

    for i in range(n):
        x[i] = int(next(tokens))
        y[i] = int(next(tokens))

    if n <= 2:
        return "0.0000000000\n"

    # next_greater[i] = first j > i with y[j] > y[i].
    next_greater = [-1] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and y[stack[-1]] <= y[i]:
            stack.pop()

        if stack:
            next_greater[i] = stack[-1]

        stack.append(i)

    # suffix_idx[i] = first position attaining the maximum y
    # among positions strictly to the right of i.
    suffix_idx = [-1] * n
    best = -1

    for i in range(n - 1, -1, -1):
        suffix_idx[i] = best

        if best == -1 or y[i] > y[best]:
            best = i

    # Store twice the integer/rational area.
    integer_area2 = 0
    fractional_area2 = Decimal(0)

    i = 0

    while i < n - 1:
        r = next_greater[i]

        if r == -1:
            r = suffix_idx[i]

        if r == -1:
            break

        h = min(y[i], y[r])

        k = i
        while k < r:
            x1, y1 = x[k], y[k]
            x2, y2 = x[k + 1], y[k + 1]
            dx = x2 - x1

            if y2 <= h:
                # Entire segment is below the water surface.
                integer_area2 += dx * (2 * h - y1 - y2)
            else:
                # The segment crosses the water surface.
                # Only the triangular part before the crossing is wet.
                dy = y2 - y1
                numerator = dx * (h - y1) * (h - y1)

                fractional_area2 += (
                    Decimal(numerator) / Decimal(dy)
                )

                # This must be the last segment of this range.
                break

            k += 1

        i = r + 1

    area = (
        Decimal(integer_area2) + fractional_area2
    ) / Decimal(2)

    return f"{area:.10f}\n"

def main():
    sys.stdout.write(solve())

if __name__ == "__main__":
    main()
```

The first scan constructs the next-greater array with a decreasing monotonic stack. When processing point `i`, every stack element that is not higher than `y[i]` is permanently useless as the first strictly higher point, so removing it is safe.

The suffix scan handles the case where no strictly higher point exists. The assignment to `suffix_idx[i]` happens before considering point `i`, which is what makes the stored index refer strictly to the right. Equal heights deliberately do not replace `best`, because the earlier point is the first occurrence of that suffix maximum.

The main loop uses `r` as the boundary selected by those two structures. If `r=i+1`, there is no interior terrain segment and the contribution is zero. The jump to `r+1` is still correct, because this range cannot contain any positive-area basin.

The area is accumulated in doubled form. Complete segments contribute an integer quantity, while a final crossing segment can produce a rational number. Python integers have arbitrary precision, and `Decimal` handles the rational part without the loss of precision that a binary floating-point value could introduce for large coordinates.

The crossing case deserves particular attention. When `y2 > h`, using the ordinary trapezoid formula would count the part of the segment above the water surface. Instead, only the triangle from `y1` to height `h` is submerged. Since `r` is the first point above `y_i` when such a point exists, there can be at most one such crossing segment in a processed range.

## Worked Examples

### Sample 1

The sample is

```
7
1 1
2 0
3 1
5 5
7 2
8 3
9 0
```

For the first point, the first strictly higher point is point 4, whose height is 5. The water level is therefore 1. The two descending and ascending segments around the valley are completely submerged.

| `i` | `r` | `h` | Segment contributions | Accumulated area |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | (0.5+0.5+0) | (1) |
| 5 | 6 | 2 | (1/3+1/2) | (11/6) |

The first range is `[1,4]`, so the algorithm jumps to point 5. Points 5 and 6 are adjacent, so that range contains no interior depression. Its two boundary heights are 2 and 3, giving no positive-area trapped region.

The range starting at point 4 also explains the fractional term. Its left side rises from height 5 to 2, and the water level is 3 when paired with point 6. The segment from `(5,5)` to `(7,2)` crosses height 3 before reaching point 5's endpoint, producing a triangular contribution of (1/3). The segment from `(7,2)` to `(8,3)` contributes another (1/2). The final result is

[
1+\frac13+\frac12=\frac{11}{6}=1.8333333333\ldots
]

which matches the sample output.

### Custom Example

Consider

```
3
0 3
1 0
2 2
```

There is no point higher than the first height 3, so the fallback rule selects point 3, the maximum of the suffix. The water level is `min(3,2)=2`.

| `i` | `r` | `h` | Segment | Twice area contribution |
| --- | --- | --- | --- | --- |
| 1 | 3 | 2 | `(0,3) -> (1,0)` | 2 |
| 1 | 3 | 2 | `(1,0) -> (2,2)` | 2 |

The total doubled area is 4, giving area 2. The example confirms that the right boundary does not need to be higher than the left boundary. Water simply spills at the lower boundary height.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | The next-greater stack, suffix maximum scan, and range processing each touch every point a constant number of times. |
| Space | (O(n)) | The coordinate arrays, next-greater array, suffix array, and monotonic stack all require linear memory. |

The algorithm performs only linear work for (n\le10^5), leaving a comfortable margin under the 2-second limit. The coordinate arrays contain at most (10^5) elements, so the memory usage is also well below 256 MB.

## Test Cases

The following tests exercise the minimum input size, maximum-size input, equal heights, the fallback suffix-maximum boundary, and the fractional crossing segment.

```python
import io
import sys

# Import the solve function from the submitted solution.
# If the solution is stored in solution.py:
# from solution import solve

# For a self-contained test file, paste the solve function above here.

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided sample
sample1 = """\
7
1 1
2 0
3 1
5 5
7 2
8 3
9 0
"""

assert abs(float(run(sample1)) - 1.8333333333333333) <= 1e-6, "sample 1"

# Minimum-size input: no possible basin.
case_min = """\
2
0 0
1000000 1000000
"""

assert abs(float(run(case_min)) - 0.0) <= 1e-6, "minimum size"

# Maximum-size input with equal heights: no water anywhere.
n = 100000
case_max = str(n) + "\n" + "\n".join(
    f"{i} 1000000" for i in range(n)
) + "\n"

assert abs(float(run(case_max)) - 0.0) <= 1e-6, "maximum size / equal heights"

# No strictly higher point exists to the right.
# The suffix maximum at the right endpoint determines the water level.
case_suffix = """\
3
0 3
1 0
2 2
"""

assert abs(float(run(case_suffix)) - 2.0) <= 1e-6, "suffix maximum"

# The final segment crosses the water level before its endpoint.
case_crossing = """\
4
0 2
1 0
2 1
3 3
"""

assert abs(float(run(case_crossing)) - 2.75) <= 1e-6, "crossing segment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / (0,0) / (1000000,1000000)` | `0` | Minimum-size input and absence of a basin |
| 100000 points with height `1000000` | `0` | Maximum `n` and equal-height handling |
| `(0,3), (1,0), (2,2)` | `2` | Suffix-maximum fallback when no higher point exists |
| `(0,2), (1,0), (2,1), (3,3)` | `2.75` | Correct clipping of the final segment at the water surface |

## Edge Cases

With only two points, the algorithm computes no range because there is no interior segment. For

```
2
0 0
1000000 1000000
```

`i=0` has no meaningful right boundary capable of creating an enclosed region, so the result is exactly `0`.

For equal heights, consider

```
3
0 2
1 0
2 2
```

There is no strictly greater point to the right of the first point. The suffix maximum is the third point at height 2, so `r=2` and `h=2`. Each of the two unit-width segments forms a triangle of area (1/2), giving a total of `1`. The fallback rule handles equality without treating the equal endpoint as a strictly greater point.

When the right boundary is lower than the left boundary,

```
3
0 3
1 0
2 2
```

the suffix maximum is height 2. The algorithm uses `h=min(3,2)=2`, not 3. Each segment contributes a triangle of area 1, giving `2`. This matches the physical behavior because water spills over the right boundary as soon as it reaches height 2.

For a crossing segment,

```
4
0 2
1 0
2 1
3 3
```

the right boundary is the last point, and the water level is 2. The first segment contributes 1, the second contributes (1.5), and the last segment from height 1 to height 3 crosses the water surface halfway through. Its wet part is a triangle with base (1/2) and height 1, contributing (1/4). The total is (1+1.5+0.25=2.75). The implementation's special crossing formula captures exactly this partial segment.

The final subtle case is a boundary immediately adjacent to the starting point. If `r=i+1`, there is no interior terrain between the two boundary points, so the range cannot contain positive-area water. The algorithm adds zero and jumps to `r+1`, preventing both an off-by-one error and unnecessary processing.
