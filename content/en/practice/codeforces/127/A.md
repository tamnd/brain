---
title: "CF 127A - Wasted Time"
description: "Scrooge signs papers by moving a pen along a polyline. The signature starts at the first point, then draws straight segments between consecutive points until the last point is reached."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 127
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 93 (Div. 2 Only)"
rating: 900
weight: 127
solve_time_s: 99
verified: true
draft: false
---

[CF 127A - Wasted Time](https://codeforces.com/problemset/problem/127/A)

**Rating:** 900  
**Tags:** geometry  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

Scrooge signs papers by moving a pen along a polyline. The signature starts at the first point, then draws straight segments between consecutive points until the last point is reached. His pen speed is fixed at 50 millimeters per second, and he repeats the exact same signature `k` times.

The task is to compute the total amount of time spent signing all papers.

The input gives the points of the polyline in order. Each pair of consecutive points forms one segment of the signature. The total distance traveled by the pen is the sum of the Euclidean lengths of all those segments. Once we know the total distance for one signature, we multiply it by `k` and divide by the writing speed.

The constraints are tiny. There are at most 100 points, so at most 99 segments. Even expensive computations would fit easily within the limit. A straightforward linear scan over the segments is enough. Geometry problems sometimes require careful optimization or precision tricks, but here the numbers are small and the formula is direct.

The main implementation risk is precision handling. Distances between points are usually non-integers because of square roots. Using integer arithmetic would silently truncate values and produce wrong answers.

Consider this input:

```
2 1
0 0
1 1
```

The segment length is `sqrt(2) ≈ 1.41421356`. The correct time is:

```
1.41421356 / 50 ≈ 0.028284271
```

If a solution accidentally uses integer division or converts the distance to an integer before dividing, it would print `0`, which is incorrect.

Another easy mistake is forgetting to multiply by `k`.

For example:

```
2 5
0 0
10 0
```

One signature has length `10`, so one signature takes `10 / 50 = 0.2` seconds. Since there are 5 papers, the correct answer is:

```
1.0
```

A careless implementation that computes only one signature would output `0.2`.

A third subtle case is negative coordinates. Distance depends on coordinate differences, not on absolute positions.

Example:

```
2 1
-3 -4
0 0
```

The distance is still `5`, because:

```
sqrt((0 - (-3))^2 + (0 - (-4))^2) = sqrt(9 + 16) = 5
```

Using absolute coordinate values directly instead of differences would break such cases.

## Approaches

The brute-force idea is already fast enough here. We can process every segment independently, compute its Euclidean length using the distance formula, and sum all lengths together.

For two consecutive points `(x1, y1)` and `(x2, y2)`, the segment length is:

$d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$Drag the points to update the distance between two points.-10-8-6-4-2246810-10-5510A(6.0, 6.0)B(-6.0, -6.0)d = 16.97Delta x = 12Delta y = 12

After summing all segment lengths, we multiply by `k` because the same signature is repeated `k` times. Finally, we divide by the writing speed `50`.

The brute-force method works because the signature path is explicitly given as consecutive segments. There is no hidden structure to reconstruct and no need to optimize repeated computations. Every segment contributes independently to the total distance.

Sometimes geometry problems tempt people into overthinking intersections or overlapping paths. None of that matters here. Even if the polyline crosses itself or retraces earlier segments, Scrooge still physically moves the pen along the entire path, so every segment must be counted exactly as drawn.

The optimal approach is identical to the brute-force approach because the constraints are so small that a single linear pass is already optimal. We simply traverse the polyline once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`.
2. Read all `n` points of the polyline in order.
3. Initialize a variable `total_distance = 0.0`.
4. Iterate through consecutive pairs of points.

For every `i` from `0` to `n - 2`, take points:

```
(x[i], y[i]) and (x[i+1], y[i+1])
```
5. Compute the Euclidean distance between the two points.

The distance formula measures the exact length of the straight segment connecting them.
6. Add this segment length to `total_distance`.

After processing all pairs, `total_distance` equals the full pen movement for one signature.
7. Multiply `total_distance` by `k`.

The signature is identical every time, so the total traveled distance scales linearly with the number of papers.
8. Divide the result by `50`.

The pen speed is 50 millimeters per second, so:

```
time = distance / speed
```
9. Print the answer as a floating-point number.

### Why it works

Every signature consists of exactly the segments between consecutive points. The algorithm processes each of those segments once and computes its exact geometric length using the Euclidean distance formula.

The invariant during the loop is that after processing the first `i` segments, `total_distance` equals the total pen movement along those segments. Since each segment contributes independently and no segment is skipped or double-counted, the final sum is exactly the length of one complete signature.

Multiplying by `k` gives the total distance for all signatures, and dividing by the constant speed converts distance into time. Because the computation directly matches the physical process described in the problem, the algorithm is correct.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

# solution

def solve():
    n, k = map(int, input().split())

    points = [tuple(map(int, input().split())) for _ in range(n)]

    total_distance = 0.0

    for i in range(n - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        dx = x2 - x1
        dy = y2 - y1

        total_distance += math.hypot(dx, dy)

    total_time = (total_distance * k) / 50.0

    print(f"{total_time:.9f}")

solve()
```

The solution follows the algorithm directly. First, it reads all points into a list so consecutive points can be accessed easily.

Inside the loop, `dx` and `dy` store coordinate differences between neighboring points. The function `math.hypot(dx, dy)` computes:

```
sqrt(dx^2 + dy^2)
```

This is safer and cleaner than manually writing the square root formula.

The accumulator `total_distance` is a floating-point value because segment lengths are generally not integers.

The multiplication by `k` happens after the entire signature length is computed. This avoids repeating the same calculations unnecessarily.

The final print uses 9 digits after the decimal point, which comfortably satisfies the required precision.

## Worked Examples

### Example 1

Input:

```
2 1
0 0
10 0
```

Trace:

| Step | Current Segment | Segment Length | total_distance |
| --- | --- | --- | --- |
| Initial | none | 0 | 0 |
| 1 | (0,0) → (10,0) | 10 | 10 |

Final computation:

| Value | Result |
| --- | --- |
| total_distance | 10 |
| k | 1 |
| total_time | 10 / 50 = 0.2 |

Output:

```
0.200000000
```

This example confirms the simplest possible case, a single horizontal segment.

### Example 2

Input:

```
3 2
0 0
3 4
6 8
```

Trace:

| Step | Current Segment | Segment Length | total_distance |
| --- | --- | --- | --- |
| Initial | none | 0 | 0 |
| 1 | (0,0) → (3,4) | 5 | 5 |
| 2 | (3,4) → (6,8) | 5 | 10 |

Final computation:

| Value | Result |
| --- | --- |
| total_distance | 10 |
| k | 2 |
| total_time | 20 / 50 = 0.4 |

Output:

```
0.400000000
```

This trace demonstrates that the algorithm correctly accumulates multiple segments before scaling by `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each segment is processed exactly once |
| Space | O(1) | Only a few variables are used besides input storage |

With at most 100 points, the algorithm performs fewer than 100 distance computations. This is trivial for the time limit, and memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())

    points = [tuple(map(int, input().split())) for _ in range(n)]

    total_distance = 0.0

    for i in range(n - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        total_distance += math.hypot(x2 - x1, y2 - y1)

    total_time = (total_distance * k) / 50.0

    return f"{total_time:.9f}"

# provided sample
assert run(
"""2 1
0 0
10 0
"""
) == "0.200000000", "sample 1"

# minimum-size input
assert run(
"""2 1
0 0
0 1
"""
) == "0.020000000", "minimum case"

# diagonal distance
assert run(
"""2 1
0 0
3 4
"""
) == "0.100000000", "3-4-5 triangle"

# multiple segments and repeated signatures
assert run(
"""3 2
0 0
3 4
6 8
"""
) == "0.400000000", "multiple segments"

# negative coordinates
assert run(
"""2 1
-3 -4
0 0
"""
) == "0.100000000", "negative coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 0 0 / 0 1` | `0.020000000` | Minimum valid input |
| `2 1 / 0 0 / 3 4` | `0.100000000` | Correct Euclidean distance |
| `3 2 / 0 0 / 3 4 / 6 8` | `0.400000000` | Multiple segments and multiplication by `k` |
| `2 1 / -3 -4 / 0 0` | `0.100000000` | Correct handling of negative coordinates |

## Edge Cases

Consider the case where the segment length is irrational.

Input:

```
2 1
0 0
1 1
```

The algorithm computes:

```
dx = 1
dy = 1
distance = sqrt(2)
```

Then:

```
time = sqrt(2) / 50
```

Because the implementation uses floating-point arithmetic and `math.hypot`, no precision is lost through integer truncation.

Now consider repeated signatures.

Input:

```
2 5
0 0
10 0
```

The loop computes a single signature distance of `10`. After the loop:

```
total_distance = 10
```

Then:

```
total_time = (10 * 5) / 50 = 1
```

The multiplication happens after the full path length is computed, so every signature is counted correctly.

Finally, consider negative coordinates.

Input:

```
2 1
-3 -4
0 0
```

The algorithm computes:

```
dx = 3
dy = 4
distance = 5
```

Only coordinate differences matter, so the position of the polyline in the plane does not affect correctness. The final answer is:

```
5 / 50 = 0.1
```
