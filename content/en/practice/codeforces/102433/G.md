---
title: "CF 102433G - Glow, Little Pixel, Glow"
description: "Each pulse travels along exactly one wire, either horizontally or vertically. A horizontal pulse on wire a starts at the left edge at time t, while a vertical pulse on wire a starts at the bottom edge at the same kind of reference time."
date: "2026-08-12T07:32:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102433
codeforces_index: "G"
codeforces_contest_name: "2019-2020 ACM-ICPC Pacific Northwest Regional Contest (Div. 1)"
rating: 0
weight: 102433
solve_time_s: 86
verified: true
draft: false
---

[CF 102433G - Glow, Little Pixel, Glow](https://codeforces.com/problemset/problem/102433/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

Each pulse travels along exactly one wire, either horizontally or vertically. A horizontal pulse on wire `a` starts at the left edge at time `t`, while a vertical pulse on wire `a` starts at the bottom edge at the same kind of reference time. Both move at speed one, and each pulse has duration `m`.

Consider one horizontal pulse and one vertical pulse. They intersect at exactly one pixel, determined by their two wire numbers. The only question is whether the two pulses are simultaneously present at that pixel.

For a horizontal pulse on wire `a`, its leading edge reaches the pixel on vertical wire `b` at time `t + b`. Its trailing edge reaches the same pixel at time `t + b + m`. For a vertical pulse on wire `b`, the corresponding interval is `[t_v + a, t_v + a + m_v)`. The half-open interpretation is useful because the statement explicitly says that touching at one instant does not activate the pixel.

There is a much cleaner way to express those intervals. For a horizontal pulse, subtract its horizontal wire number from its starting time and define

`start = t - a`.

For a vertical pulse, do the same with its vertical wire number. After this transformation, the two pulses collide exactly when their transformed time intervals overlap with positive length. A pulse `(t, m, a)` becomes the interval

`[t - a, t - a + m)`.

Thus the two-dimensional motion of the pulses has become a one-dimensional interval-overlap problem. The official contest analysis describes the same geometric idea as projecting both pulse paths onto the diagonal `x = y`, where both pulse trains move at the same speed.

Only horizontal and vertical pulses can activate a pixel together. Two horizontal pulses never meet at a pixel because they travel on different rows, and two vertical pulses have the analogous property. So the answer is simply the number of overlapping pairs consisting of one horizontal interval and one vertical interval.

The number of pulses is at most `200000`. A direct comparison between every horizontal and every vertical pulse can require about `100000 * 100000 = 10^10` comparisons, which is far beyond what a two-second contest program can perform. The wire number is at most `100000`, but constructing a grid of that size would not solve the real issue, because the important dimension is the number of pulse pairs, not the number of wires. The starting times and lengths are also large enough that any solution depending on simulating time unit by time unit would be inappropriate.

Several boundary cases are easy to mishandle.

Consider two pulses that only touch:

```
2
h 1 1 1
v 2 1 1
```

The horizontal interval is `[0, 1)` and the vertical interval is `[1, 2)`. The answer is `0`. A careless implementation using `start <= other_end` or treating closed intervals would count this collision even though the pulses are never simultaneously present.

Consider equal starting positions:

```
2
h 1 3 1
v 1 3 1
```

Both transformed intervals are `[0, 3)`, so the answer is `1`. Equal starts are allowed to overlap immediately.

A pulse can also completely contain another one:

```
2
h 1 10 1
v 3 2 1
```

The intervals are `[0, 10)` and `[2, 4)`, so the answer is `1`. Checking only whether one interval starts inside the other would miss some valid collisions.

Finally, pulses travelling in the same direction must not be counted:

```
2
h 1 10 1
h 5 10 2
```

There is no vertical pulse, so the answer is `0`, even though their transformed intervals overlap.

## Approaches

The brute-force solution follows directly from the physical interpretation. Store all horizontal pulses and all vertical pulses, then inspect every horizontal-vertical pair. For a pair, calculate the two arrival intervals at their intersection and test whether they overlap with positive length. This is correct because every activated pixel corresponds to exactly one horizontal pulse and one vertical pulse, and every such pair has exactly one intersection pixel.

The problem is the number of pairs. If there are `100000` horizontal pulses and `100000` vertical pulses, the algorithm performs `10^10` pair checks. Even a very small constant per comparison is not enough for a two-second limit.

The useful observation is that the exact wire coordinates disappear after the right transformation. A horizontal pulse with starting time `t`, length `m`, and row `a` reaches the diagonal projection with an interval beginning at `t - a`. A vertical pulse with starting time `t`, length `m`, and column `a` gets exactly the same representation. So every pulse becomes one ordinary interval on a line.

Now the task is: given horizontal intervals and vertical intervals, count how many pairs overlap with positive length.

For one horizontal interval `[L, R)`, a vertical interval `[S, E)` overlaps it exactly when

`S < R` and `E > L`.

We can count the first condition by sorting all vertical starts and using binary search. We can count the second condition by sorting all vertical ends and using another binary search. The number satisfying both conditions is

`number of vertical starts < R - number of vertical ends <= L`.

This avoids any two-dimensional data structure. Each horizontal interval is processed with two binary searches after the vertical endpoints have been sorted. The official editorial instead describes an equivalent sweep over four kinds of interval events, maintaining how many horizontal and vertical intervals are active.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read every pulse and transform it into a one-dimensional interval. If the pulse has starting time `t`, wire number `a`, and length `m`, compute `L = t - a` and `R = L + m`. Store `[L, R)` in either the horizontal or vertical collection according to its direction. The subtraction by `a` accounts for the extra travel time needed to reach the intersection pixel.
2. Separate the endpoints of all vertical intervals. Store every vertical start in one array and every vertical end in another array. Sort both arrays. We only need the vertical intervals for queries because every valid collision has exactly one horizontal and one vertical pulse.
3. For each horizontal interval `[L, R)`, find how many vertical intervals start before `R`. With a sorted start array, `bisect_left(starts, R)` gives exactly this count. The strict inequality is deliberate, because an interval starting exactly at `R` only touches the horizontal interval at its endpoint.
4. Find how many vertical intervals end at or before `L`. With a sorted end array, `bisect_right(ends, L)` gives this count. Such intervals cannot overlap `[L, R)`, because their current has already disappeared by time `L`.
5. Subtract the second count from the first. Every remaining vertical interval satisfies both `S < R` and `E > L`, so it overlaps the horizontal interval for a positive amount of time. Add this number to the answer.
6. Print the accumulated answer. Python integers are unbounded, which is useful because as many as `100000 * 100000 = 10^10` pixels can be activated.

### Why it works

For every horizontal and vertical pulse pair, the transformed intervals preserve exactly whether their currents coexist at the corresponding pixel. Two transformed intervals `[L, R)` and `[S, E)` overlap precisely when `S < R` and `E > L`. For each horizontal interval, the first binary search counts all vertical intervals satisfying `S < R`, while the second removes exactly those with `E <= L`. Every remaining vertical interval overlaps the horizontal interval, and every overlapping vertical interval remains in the count. Since every horizontal-vertical pair corresponds to one pixel, the accumulated count is exactly the number of activated pixels.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

def solve(reader=None):
    if reader is None:
        reader = sys.stdin.readline

    n = int(reader())

    horizontal = []
    vertical_starts = []
    vertical_ends = []

    for _ in range(n):
        direction, t, m, a = reader().split()
        t = int(t)
        m = int(m)
        a = int(a)

        left = t - a
        right = left + m

        if direction == 'h':
            horizontal.append((left, right))
        else:
            vertical_starts.append(left)
            vertical_ends.append(right)

    vertical_starts.sort()
    vertical_ends.sort()

    answer = 0

    for left, right in horizontal:
        starts_before_right = bisect_left(vertical_starts, right)
        ends_at_or_before_left = bisect_right(vertical_ends, left)
        answer += starts_before_right - ends_at_or_before_left

    return answer

if __name__ == "__main__":
    print(solve())
```

The input loop performs the geometric transformation immediately, so the original wire number is not needed afterward. For a pulse `(t, m, a)`, `left = t - a` and `right = left + m` describe the interval on the projected line.

Only vertical endpoints need to be sorted. For each horizontal interval, `bisect_left(vertical_starts, right)` counts starts strictly before the right endpoint. Using `bisect_left` rather than `bisect_right` is what excludes intervals that only touch at `right`.

For the other boundary, `bisect_right(vertical_ends, left)` counts ends less than or equal to the left endpoint. Using `bisect_right` is what removes intervals that finish exactly at `left`, matching the statement's rule that endpoint contact does not activate a pixel.

The answer can reach `10^10`, so a 32-bit integer would be insufficient in languages where integers have fixed width. Python's integer type handles it directly.

## Worked Examples

### Sample 1

The four pulses become the following projected intervals.

| Direction | `t` | `m` | `a` | Interval |
| --- | --- | --- | --- | --- |
| h | 1 | 4 | 1 | `[0, 4)` |
| v | 2 | 4 | 2 | `[0, 4)` |
| h | 10 | 2 | 2 | `[8, 10)` |
| v | 11 | 2 | 3 | `[8, 10)` |

The vertical starts are `[0, 8]`, and the vertical ends are `[4, 10]`.

| Horizontal interval | Starts `< right` | Ends `<= left` | New collisions | Answer |
| --- | --- | --- | --- | --- |
| `[0, 4)` | 1 | 0 | 1 | 1 |
| `[8, 10)` | 2 | 1 | 1 | 2 |

The first horizontal pulse overlaps the first vertical pulse. The second horizontal pulse overlaps the second vertical pulse. The result is `2`.

### Sample 2

The transformed intervals are

| Direction | `t` | `m` | `a` | Interval |
| --- | --- | --- | --- | --- |
| h | 1 | 10 | 1 | `[0, 10)` |
| h | 5 | 10 | 2 | `[3, 13)` |
| v | 1 | 10 | 1 | `[0, 10)` |
| v | 5 | 10 | 3 | `[2, 12)` |

The vertical starts are `[0, 2]`, and the vertical ends are `[10, 12]`.

| Horizontal interval | Starts `< right` | Ends `<= left` | New collisions | Answer |
| --- | --- | --- | --- | --- |
| `[0, 10)` | 2 | 0 | 2 | 2 |
| `[3, 13)` | 2 | 0 | 2 | 4 |

Every horizontal interval overlaps both vertical intervals, so all four horizontal-vertical pairs activate pixels. The result is `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the vertical endpoints costs O(n log n), followed by two binary searches for every horizontal pulse |
| Space | O(n) | The horizontal intervals and two vertical endpoint arrays each contain at most n elements |

With `n <= 200000`, O(n log n) requires only a few million sorting and binary-search operations, which is appropriate for the two-second limit. The memory usage is linear in the number of pulses.

## Test Cases

The following test harness uses the same `solve` function as the submitted solution, while passing an in-memory reader so each case can be tested independently.

```
import io

def run(inp: str) -> str:
    return str(solve(io.StringIO(inp)))

# Provided sample 1
assert run("""\
4
h 1 4 1
v 2 4 2
h 10 2 2
v 11 2 3
""") == "2", "sample 1"

# Provided sample 2
assert run("""\
4
h 1 10 1
h 5 10 2
v 1 10 1
v 5 10 3
""") == "4", "sample 2"

# Provided sample 3
assert run("""\
7
v 1 3 1
v 1 15 2
h 4 5 1
h 5 5 2
h 6 5 3
h 7 5 4
h 8 5 5
""") == "5", "sample 3"

# Minimum-size input: one pulse cannot activate any pixel.
assert run("""\
1
h 1 1 1
""") == "0", "single pulse"

# Exact endpoint touching: [0, 1) and [1, 2) do not overlap.
assert run("""\
2
h 1 1 1
v 2 1 1
""") == "0", "endpoint touching"

# Same transformed interval, so the two pulses overlap completely.
assert run("""\
2
h 1 3 1
v 1 3 1
""") == "1", "identical intervals"

# A vertical interval is completely contained inside a horizontal interval.
assert run("""\
2
h 1 10 1
v 3 2 1
""") == "1", "contained interval"

# Same direction pulses never activate a pixel together.
assert run("""\
2
h 1 10 1
h 5 10 2
""") == "0", "same direction"

# Maximum-size case: 100000 horizontal and 100000 vertical pulses.
# All transformed intervals are [100000, 300000), so every pair collides.
lines = ["200000"]
for a in range(1, 100001):
    lines.append(f"h {100000 + a} 200000 {a}")
for a in range(1, 100001):
    lines.append(f"v {100000 + a} 200000 {a}")

assert run("\n".join(lines) + "\n") == "10000000000", "maximum-size all-overlapping case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` horizontal pulse | `0` | Minimum-size input |
| Two intervals `[0,1)` and `[1,2)` | `0` | Exact endpoint boundary |
| Two identical intervals | `1` | Equal starts and complete overlap |
| `[0,10)` and `[2,4)` | `1` | Containment |
| Two horizontal pulses | `0` | Only opposite directions can collide |
| `200000` equal projected intervals | `10000000000` | Maximum input size and 64-bit-sized answer |

## Edge Cases

The endpoint-touching case is handled by the strict binary-search boundaries. For

```
2
h 1 1 1
v 2 1 1
```

the horizontal pulse becomes `[0, 1)` and the vertical pulse becomes `[1, 2)`. `bisect_left(starts, 1)` does not count the vertical start at `1`, so the answer is `0`. This directly encodes the rule that simultaneous presence must last for a positive amount of time.

For equal starting positions,

```
2
h 1 3 1
v 1 3 1
```

both intervals are `[0, 3)`. The vertical start `0` is strictly before the horizontal right endpoint `3`, and the vertical end `3` is strictly after the horizontal left endpoint `0`. The pair is counted, giving `1`.

For containment,

```
2
h 1 10 1
v 3 2 1
```

the intervals are `[0, 10)` and `[2, 4)`. The vertical start satisfies `2 < 10`, and its end satisfies `4 > 0`, so it contributes one collision. The method does not assume that either interval must contain an endpoint of the other.

For same-direction pulses,

```
2
h 1 10 1
h 5 10 2
```

the horizontal interval collection contains both pulses, while the vertical endpoint arrays are empty. Every horizontal query contributes zero, so the answer is `0`. This prevents overlapping projected intervals of the same direction from being mistaken for physical pixel activations.

For the maximum-size case, there are `100000` horizontal and `100000` vertical pulses, each transformed into `[100000, 300000)`. Every horizontal interval overlaps every vertical interval, producing `10^10` activated pixels. The algorithm never enumerates those pairs individually. It counts them through two binary searches per horizontal interval, which is precisely why the O(n log n) approach remains practical.
