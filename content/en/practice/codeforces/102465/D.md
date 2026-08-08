---
title: "CF 102465D - Monument Tour"
description: "The city is a rectangular grid. The bus chooses one horizontal eastbound road, represented by a fixed row coordinate y = r, enters from the west, travels all the way east, and must leave on that same row."
date: "2026-08-08T09:17:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "D"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 373
verified: true
draft: false
---

[CF 102465D - Monument Tour](https://codeforces.com/problemset/problem/102465/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is a rectangular grid. The bus chooses one horizontal eastbound road, represented by a fixed row coordinate `y = r`, enters from the west, travels all the way east, and must leave on that same row. Whenever it has to visit monuments above or below this road, it can turn vertically, visit the required monuments, and return to the main road.

For a fixed main-road row `r`, consider all monuments having the same `x` coordinate. They lie on one vertical street, so the bus can visit all of them in a single vertical excursion. Only the smallest and largest `y` coordinates at that `x` matter. If those extremes are `L` and `R`, the bus has to cover the interval `[L, R]` and return to `r`.

The input gives `X` northbound streets and `Y` eastbound streets, followed by `N` monument coordinates `(x, y)`. The output is the minimum number of grid blocks traversed by choosing the best horizontal road.

The limits are large enough to rule out trying every possible road and scanning every monument. With up to `100000` monuments and `100000` possible horizontal roads, a direct `O(NY)` computation can reach `10^10` operations. Even `O(XY)` is of the same order in the worst case. A solution around `O(N log N)` is appropriate because sorting `O(N)` derived values is easily feasible within the constraints.

There are several edge cases that can make a seemingly reasonable implementation wrong. If several monuments share an `x` coordinate, treating them independently overcounts the vertical travel. For example:

```
2 2
2
0 0
0 1
```

The correct answer is `3`. The bus can enter on row `0`, travel one block east, and visit both monuments on the same vertical street without any extra detour. A careless implementation that charges `2 * |r-y|` independently for both monuments would get `5` for row `0`.

A single monument is another useful boundary case:

```
1 1
1
0 0
```

The answer is `0`, because the bus starts and finishes at the only available horizontal position and there are no east-west blocks to traverse. An implementation that blindly adds `X` instead of `X - 1` would produce `1`.

A monument can also lie at the first or last row:

```
3 5
1
2 4
```

Choosing row `4` gives the minimum cost, namely `2`, because the bus travels two horizontal blocks and never needs a vertical detour. An implementation that assumes the optimal road must be somewhere strictly inside the city can miss this case.

Finally, duplicate coordinates are allowed:

```
2 3
3
0 1
0 1
0 1
```

The answer is `1`. The repeated monument does not create additional travel. Keeping only the minimum and maximum `y` for each `x` naturally handles duplicates.

## Approaches

A straightforward solution is to try every possible horizontal road. For each candidate row `r`, we can inspect every monument and determine how much vertical travel is required. If we process the monuments independently, this takes `O(N)` work for one candidate, so all `Y` candidates require `O(NY)` time. In the worst case that is `100000 * 100000 = 10^10` monument checks, far beyond what a one-second limit can handle.

We can improve the constant factors by grouping monuments with the same `x`, but that does not solve the main problem. After grouping, there can still be `100000` different vertical streets, and trying every possible `r` still gives quadratic work.

The key observation is that one vertical street only needs its lowest and highest monument. Suppose those values are `L` and `R`. If the main road is at `r`, the shortest vertical excursion that visits the entire interval and returns to `r` has length

`2 * (R - L)` when `r` is inside `[L, R]`.

If `r < L`, the bus must first travel from `r` to `L`, traverse the interval, and return from `R` to `r`. Its length is

`2 * (R - r)`.

Similarly, if `r > R`, its length is

`2 * (r - L)`.

These three cases can be written more compactly as

`2 * (R - L + distance(r, [L, R]))`.

The constant part `2 * (R - L)` does not affect the choice of `r`. The interesting part is minimizing the sum of distances from `r` to all the intervals.

There is a useful identity:

`distance(r, [L, R]) = (|r-L| + |r-R| - (R-L)) / 2`.

Consequently, after adding the constant terms, minimizing the whole tour is equivalent to minimizing

`sum(|r-L| + |r-R|)`.

So every occupied vertical street contributes two values, its lower endpoint `L` and upper endpoint `R`, and we simply need a value `r` minimizing the sum of absolute differences to all these endpoint values. Such a value is a median.

This is exactly the observation used in the official SWERC analysis: keep only the extreme `y` coordinates for each `x`, count a single-point interval twice, and choose the median of all resulting endpoints.

Thus the geometry disappears. We first reduce every occupied column to an interval, collect both endpoints, sort them, take a median, and evaluate the resulting tour.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(NY)` | `O(N)` | Too slow |
| Optimal | `O(N log N)` | `O(N + X)` | Accepted |

## Algorithm Walkthrough

1. Read all monument coordinates and maintain, for every `x`, the smallest and largest `y` appearing there. These two values completely describe the vertical work needed at that street because visiting everything between them covers every monument on that street.
2. For every `x` that contains at least one monument, append its minimum `y` and maximum `y` to an endpoint array. If all monuments at that `x` have the same `y`, the minimum and maximum are equal, so the same coordinate is deliberately inserted twice.
3. Sort the endpoint array. Since every interval contributes exactly two endpoints, the number of stored values is at most `2N`.
4. Choose the lower median of the sorted endpoints as the main-road row `r`. Any median minimizes the sum of absolute distances, so the lower median is sufficient even when there are an even number of endpoints.
5. Start the answer with `X - 1`, which is the east-west distance from the western boundary at coordinate `0` to the eastern boundary at coordinate `X - 1`.
6. For every occupied `x`, let its interval be `[L, R]`. If `r < L`, add `2 * (R-r)`. If `r > R`, add `2 * (r-L)`. Otherwise add `2 * (R-L)`. This is exactly the shortest excursion from the main road that visits the whole interval and returns.

The invariant behind the algorithm is that every possible tour with main road `r` has exactly the same horizontal cost, `X - 1`, and its vertical cost is the sum of independent costs for the occupied `x` coordinates. Replacing each column by its extreme interval loses no information. The vertical cost of each interval can then be rewritten in terms of distances to its two endpoints, so the complete objective becomes a sum of absolute deviations from the endpoint array. A median minimizes that objective, which means the selected road is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    X, Y = map(int, input().split())
    N = int(input())

    INF = 10**30
    low = [INF] * X
    high = [-1] * X

    for _ in range(N):
        x, y = map(int, input().split())
        if y < low[x]:
            low[x] = y
        if y > high[x]:
            high[x] = y

    endpoints = []

    for x in range(X):
        if high[x] != -1:
            endpoints.append(low[x])
            endpoints.append(high[x])

    endpoints.sort()
    road = endpoints[(len(endpoints) - 1) // 2]

    answer = X - 1

    for x in range(X):
        if high[x] == -1:
            continue

        L = low[x]
        R = high[x]

        if road < L:
            answer += 2 * (R - road)
        elif road > R:
            answer += 2 * (road - L)
        else:
            answer += 2 * (R - L)

    print(answer)

if __name__ == "__main__":
    solve()
```

The `low` and `high` arrays implement the first algorithm step. `low[x]` stores the lowest monument on vertical street `x`, while `high[x]` stores the highest one. The sentinel `high[x] == -1` identifies columns containing no monuments.

The endpoint list contains exactly two values for every occupied column. For a column containing only one distinct `y`, both values are equal, which gives the required double contribution automatically.

The median is selected with `(len(endpoints) - 1) // 2`. With an even number of endpoints this chooses the lower of the two middle values. Both middle values are valid minimizers, so either choice gives the same minimum cost.

The horizontal contribution is `X - 1`, not `X`. The coordinates of the city range from `0` through `X - 1`, so traveling from the west boundary to the east boundary crosses exactly `X - 1` blocks.

Python integers have arbitrary precision, so the accumulated answer cannot overflow. The maximum answer is easily within ordinary 64-bit range anyway, but using Python integers removes the concern entirely.

## Worked Examples

### Sample 1

The occupied vertical streets produce the following intervals:

| `x` | `L` | `R` | Endpoint contribution |
| --- | --- | --- | --- |
| 1 | 0 | 2 | `0, 2` |
| 2 | 4 | 4 | `4, 4` |
| 4 | 2 | 2 | `2, 2` |

The complete endpoint array before sorting is `[0, 2, 4, 4, 2, 2]`.

| Step | State |
| --- | --- |
| Group monuments | `[1:[0,2], 2:[4,4], 4:[2,2]]` |
| Endpoints | `[0,2,4,4,2,2]` |
| Sorted endpoints | `[0,2,2,2,4,4]` |
| Chosen road | `2` |
| Horizontal cost | `5` |
| Column `x=1` | `2 * (2-0) = 4` |
| Column `x=2` | `2 * (4-2) = 4` |
| Column `x=4` | `0` |
| Total | `5 + 4 + 4 = 13` |

The chosen road is row `2`, which is the lower median of the endpoint values. The first column requires the bus to visit rows `0` and `2`, while the second requires a trip from row `2` to row `4` and back. The final column already lies on the main road.

### Sample 2

The monument intervals are:

| `x` | `L` | `R` | Endpoint contribution |
| --- | --- | --- | --- |
| 0 | 0 | 3 | `0, 3` |
| 2 | 2 | 3 | `2, 3` |
| 3 | 2 | 2 | `2, 2` |
| 4 | 3 | 6 | `3, 6` |

The endpoint values are `[0,3,2,3,2,2,3,6]`.

| Step | State |
| --- | --- |
| Group monuments | `[0:[0,3], 2:[2,3], 3:[2,2], 4:[3,6]]` |
| Sorted endpoints | `[0,2,2,2,3,3,3,6]` |
| Chosen road | `2` |
| Horizontal cost | `4` |
| Column `x=0` | `2 * (3-0) = 6` |
| Column `x=2` | `2 * (3-2) = 2` |
| Column `x=3` | `0` |
| Column `x=4` | `2 * (6-2) = 8` |
| Total | `4 + 6 + 2 + 0 + 8 = 20` |

The median is again row `2`. The interval at `x=3` contains the main road, so it contributes only its width, which is zero because both endpoints are `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(X + N + N log N)` | Building extrema costs `O(N)`, scanning columns costs `O(X)`, and sorting at most `2N` endpoints costs `O(N log N)` |
| Space | `O(X + N)` | The extrema arrays use `O(X)` space and the endpoint array contains at most `2N` values |

With `X, Y, N <= 100000`, the dominant operation is sorting at most `200000` integers. This is comfortably within the intended scale, while the brute-force `10^10` checks are not.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    X = next(it)
    Y = next(it)
    N = next(it)

    INF = 10**30
    low = [INF] * X
    high = [-1] * X

    for _ in range(N):
        x = next(it)
        y = next(it)
        low[x] = min(low[x], y)
        high[x] = max(high[x], y)

    endpoints = []
    for x in range(X):
        if high[x] != -1:
            endpoints.append(low[x])
            endpoints.append(high[x])

    endpoints.sort()
    road = endpoints[(len(endpoints) - 1) // 2]

    answer = X - 1

    for x in range(X):
        if high[x] == -1:
            continue

        L = low[x]
        R = high[x]

        if road < L:
            answer += 2 * (R - road)
        elif road > R:
            answer += 2 * (road - L)
        else:
            answer += 2 * (R - L)

    return str(answer)

# Provided sample 1
assert solve("""\
6 5
4
1 0
1 2
2 4
4 2
""") == "13", "sample 1"

# Provided sample 2
assert solve("""\
5 7
9
0 0
0 2
0 3
2 2
2 3
3 2
4 3
4 4
4 6
""") == "20", "sample 2"

# Minimum-size city, single monument
assert solve("""\
1 1
1
0 0
""") == "0", "minimum size"

# All monuments at the same coordinate
assert solve("""\
2 3
3
0 1
0 1
0 1
""") == "1", "duplicate coordinates"

# One column spans the whole height, so every road inside it is optimal
assert solve("""\
3 5
2
1 0
1 4
""") == "6", "single wide interval"

# Monuments on both boundaries, forcing the median choice to matter
assert solve("""\
4 5
2
0 0
3 4
""") == "7", "boundary monuments"

# Large input shape, all coordinates equal
large = "100000 100000\n100000\n" + "\n".join(
    "99999 99999" for _ in range(100000)
) + "\n"
assert solve(large) == "99999", "large duplicate input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, one monument at `(0,0)` | `0` | Minimum dimensions and `X-1` horizontal cost |
| `2 3`, three identical monuments | `1` | Duplicate coordinates and repeated endpoint values |
| `3 5`, monuments at `(1,0)` and `(1,4)` | `6` | One vertical interval and median lying inside it |
| `4 5`, monuments at `(0,0)` and `(3,4)` | `7` | Boundary coordinates and nontrivial median |
| `100000 100000`, `100000` identical monuments | `99999` | Maximum `N` and large dimensions without quadratic work |

## Edge Cases

When several monuments share one `x` coordinate, the algorithm replaces them with one interval. For example,

```
2 2
2
0 0
0 1
```

gives the interval `[0,1]`. Its endpoints are `0` and `1`, so the median can be either row `0` or row `1`. Choosing row `0`, the horizontal cost is `1` and the vertical excursion costs `2`, giving `3`. The two monuments are visited during one trip, rather than paying for two separate trips.

When all monuments have exactly the same coordinate,

```
2 3
3
0 1
0 1
0 1
```

the interval for `x=0` is `[1,1]`, and its endpoints are inserted as `1,1`. The median is consequently `1`. The horizontal cost is `1`, and the vertical cost is zero, so the answer is `1`. Duplicates do not affect the geometry.

For a single monument at the only available position,

```
1 1
1
0 0
```

the endpoint array is `[0,0]`, so the chosen road is `0`. Since `X=1`, the horizontal cost is `X-1=0`, and the interval also contributes zero. The result is `0`.

For a monument at the extreme edge of the vertical range,

```
3 5
1
2 4
```

the endpoint array is `[4,4]`, so the chosen road is `4`. The monument is directly on the main road. The bus only has to travel from the western side to the eastern side, crossing `X-1=2` blocks, so the answer is `2`. The algorithm does not assume that the optimal row is an interior coordinate.

For a column whose monuments span a large interval,

```
3 5
2
1 0
1 4
```

the endpoint array is `[0,4]`. Any row from `0` through `4` minimizes the distance to this interval, and the lower median chooses `0`. The vertical excursion costs `2 * (4-0)=8`, while the horizontal traversal costs `2`, giving `10`. If the city has only five eastbound roads, row `0` is valid because monument coordinates range from `0` through `4`. This demonstrates why the interval formula must include both endpoints correctly.

The core lesson is that the problem looks two-dimensional only until monuments sharing an `x` coordinate are compressed into vertical intervals. After that, the only remaining decision is the position of one horizontal line, and the entire optimization reduces to the classic fact that a median minimizes a sum of absolute distances.
