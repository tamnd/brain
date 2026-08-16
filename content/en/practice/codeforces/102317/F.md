---
title: "CF 102317F - Dot the i's and Cross the T's"
description: "The task is geometric. Each test case gives a set of distinct points in the plane, and we have to count how many different groups of four points can be arranged as a capital T."
date: "2026-08-17T03:46:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102317
codeforces_index: "F"
codeforces_contest_name: "UCF Locals 2016"
rating: 0
weight: 102317
solve_time_s: 80
verified: true
draft: false
---

[CF 102317F - Dot the i's and Cross the T's](https://codeforces.com/problemset/problem/102317/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is geometric. Each test case gives a set of distinct points in the plane, and we have to count how many different groups of four points can be arranged as a capital `T`.

For four points `A`, `M`, `B`, and `C`, the horizontal part of the `T` is the segment `AB`, with `M` exactly at its midpoint. The remaining point `C` is the endpoint of the stem. The stem must have the same length as `AB`, and it must be perpendicular to `AB` at `M`. Equivalently, if `A` and `B` are known, then `M` is forced and there are only two possible locations for `C`.

The input contains at most 100 test cases. Each set contains between 4 and 50 distinct points, and every coordinate lies between `-1000` and `1000`. The official time limit is 1 second and the memory limit is 256 MB.

The small bound of 50 points is large enough to rule out a straightforward four-point enumeration when there can be 100 test cases. Enumerating every ordered choice of four distinct points takes

`50 * 49 * 48 * 47 = 5,527,200`

choices for one maximum-sized test case, or up to 552,720,000 choices across 100 such cases. A solution closer to cubic time is comfortable, while a quadratic solution is even better.

Floating-point comparison is the main numerical issue. The statement defines two values as equal when their difference is at most `10^-6`. Comparing coordinates with `==` can consequently reject a valid point because arithmetic such as `(x1 + x2) / 2` may not be represented exactly.

For example, the four points

```
(0, 0)
(2, 0)
(1, 0)
(1, 2)
```

form a `T`, so the answer is `1`. An implementation that calculates the midpoint and compares floating-point coordinates with exact equality is relying on a property the problem does not guarantee.

A second edge case is that the same `T` can be described with `A` and `B` exchanged. For

```
(0, 0)
(2, 0)
(1, 0)
(1, 2)
```

the pairs `(A,B)` and `(B,A)` describe the same crossbar. Counting ordered pairs would produce `2` instead of the correct answer `1`.

A third edge case occurs when a candidate crossbar has only one of the two possible stem endpoints present. For

```
(0, 0)
(2, 0)
(1, 0)
(1, 2)
(5, 5)
```

there is still exactly one `T`. We must check both perpendicular directions, but count only the points that actually exist.

The official UCF statement gives the same geometric definition and the `10^-6` equality tolerance.

## Approaches

The direct approach is to choose four distinct points and test every possible assignment of those points to `A`, `M`, `B`, and `C`. The test follows directly from the definition: verify that `M` is the midpoint of `AB`, that `CM` has the same length as `AB`, and that the two segments meeting at `M` are perpendicular.

That approach is correct because every valid `T` consists of four points, so examining every possible assignment eventually examines its correct roles. The problem is the number of choices. With 50 points, even enumerating ordered quadruples requires 5,527,200 choices per test case, and 100 maximum-sized cases can reach 552,720,000 choices before the geometric checks are performed.

The structure of the geometry gives us a much better way to organize the search. Instead of choosing four points, choose the two endpoints `A` and `B` of the crossbar. Once these two points are fixed, there is no freedom left in the other two positions.

The midpoint is

`M = ((Ax + Bx) / 2, (Ay + By) / 2)`.

Let the vector from `A` to `B` be `(dx, dy)`. A perpendicular vector of the same length is either `(-dy, dx)` or `(dy, -dx)`. Consequently, the only possible stem endpoints are

`C1 = M + (-dy, dx)`

and

`C2 = M + (dy, -dx)`.

So every unordered pair of points generates at most two candidate fourth points. We only need to check whether those candidate coordinates occur in the input.

With at most 50 points, even the simple implementation that scans all points to locate each candidate takes only `O(p^3)` time. There are `O(p^2)` choices of `A,B`, two candidate locations, and an `O(p)` scan for each candidate. This is easily small enough for the given bounds.

The brute-force method works because every possible role assignment is examined, but fails because it explores combinations whose geometry could have been determined immediately. The observation that the crossbar endpoints uniquely determine the midpoint and both possible stems removes an entire dimension of the search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(p^4) | O(1) | Too slow in the worst case |
| Optimal | O(p^3) | O(p) | Accepted |

## Algorithm Walkthrough

1. Read the `p` points of the current test case and store their coordinates.
2. Enumerate every unordered pair of points `A` and `B`. Using only pairs with `i < j` is essential because exchanging the endpoints of the crossbar does not create a different `T`.
3. Compute the midpoint `M` of `A` and `B`. The midpoint is forced by the first condition of the definition, so no other input point needs to be selected for `M` independently.
4. Compute `dx = Bx - Ax` and `dy = By - Ay`. The vector `(dx, dy)` describes the crossbar.
5. Construct the two possible stem endpoints. A vector perpendicular to `(dx, dy)` with exactly the same length is `(-dy, dx)`, and its opposite is `(dy, -dx)`. Adding either vector to `M` gives one possible position for `C`.
6. For each candidate `C`, scan the input points and check whether both its coordinates are within `10^-6` of the candidate coordinates. If a point matches, increment the answer.
7. Process every pair and both perpendicular directions, then print the resulting count in the required `Set #k: answer` format followed by a blank line.

The numerical comparison is applied independently to the two coordinates. A point is considered present when both coordinate differences are at most `10^-6`, matching the equality rule from the statement.

### Why it works

For every valid `T`, its two crossbar endpoints are some unordered pair `A,B` in the input. When the algorithm reaches that pair, its midpoint calculation produces exactly the required point `M`. The vector `AB` determines exactly two perpendicular vectors having the same length as `AB`, so the two generated candidates are precisely the two geometrically possible positions for `C`.

Thus the valid `C` of the `T` must be found by the scan. Conversely, whenever a generated candidate matches an input point, the midpoint condition, equal-length condition, and perpendicularity condition all hold by construction, so those four points form a valid `T`.

Using `i < j` means each crossbar is considered once. For a fixed crossbar, each possible stem endpoint is considered once, so no valid group is counted more than once.

## Python Solution

```python
import sys
input = sys.stdin.readline

EPS = 1e-6

def same_point(x1, y1, x2, y2):
    return abs(x1 - x2) <= EPS and abs(y1 - y2) <= EPS

def solve_case(points):
    n = len(points)
    ans = 0

    for i in range(n):
        ax, ay = points[i]

        for j in range(i + 1, n):
            bx, by = points[j]

            dx = bx - ax
            dy = by - ay

            mx = (ax + bx) / 2.0
            my = (ay + by) / 2.0

            # Two perpendicular vectors having the same length as AB.
            candidates = (
                (mx - dy, my + dx),
                (mx + dy, my - dx),
            )

            for cx, cy in candidates:
                for px, py in points:
                    if same_point(cx, cy, px, py):
                        ans += 1
                        break

    return ans

def main():
    t = int(input())

    out = []

    for case_no in range(1, t + 1):
        p = int(input())
        points = [tuple(map(float, input().split())) for _ in range(p)]

        ans = solve_case(points)

        out.append(f"Set #{case_no}: {ans}")
        out.append("")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The `solve_case` function implements the pair-based search from the walkthrough. The outer two loops choose `A` and `B` with `i < j`, so the crossbar is never duplicated.

The midpoint uses division by `2.0` because the coordinates are real numbers. The two candidate points are then obtained directly from the perpendicular transformation. If `(dx, dy)` is the crossbar vector, `(-dy, dx)` rotates it by 90 degrees without changing its length.

The inner scan deliberately uses an epsilon comparison instead of a dictionary keyed by raw floating-point coordinates. A dictionary based on exact floating-point values would make the result dependent on representation details. With only 50 points, scanning is simpler and fast enough.

The `break` after finding a matching point is also necessary. The input points are guaranteed to be distinct, so one candidate can correspond to at most one input point. Without the `break`, a future duplicate coordinate would incorrectly increase the count, even though duplicates are excluded by the statement.

Python integers do not overflow, and the answer is at most `2 * C(50, 2) = 2450`, so no special integer handling is required.

The required blank line after each answer is produced by appending an empty string after every case. The official statement specifies this output format.

## Worked Examples

The Codeforces problem page links to the original UCF problem set, whose indexed statement gives the complete geometric definition and input/output specification. The accessible problem text does not expose the sample cases in its indexed extract, so the following are two concrete traces constructed directly from the definition rather than being presented as official samples.

### Sample 1

Consider:

```
1
4
0 0
2 0
1 0
1 2
```

The expected output is:

```
Set #1: 1
```

For the pair `(0,0)` and `(2,0)`, the crossbar vector is `(2,0)`. Its midpoint is `(1,0)`, and the two candidate stem endpoints are `(1,2)` and `(1,-2)`. Only `(1,2)` exists.

| A | B | M | Candidate C | Found | Answer |
| --- | --- | --- | --- | --- | --- |
| `(0,0)` | `(2,0)` | `(1,0)` | `(1,2)` | yes | 1 |
| `(0,0)` | `(2,0)` | `(1,0)` | `(1,-2)` | no | 1 |
| `(0,0)` | `(1,0)` | `(0.5,0)` | `(0.5,1)` | no | 1 |
| `(0,0)` | `(1,2)` | `(0.5,1)` | `(-1.5,1.5)` | no | 1 |
| `(2,0)` | `(1,0)` | `(1.5,0)` | `(1.5,-1)` | no | 1 |
| remaining pairs |  |  |  | no | 1 |

The important part of the trace is that the valid `T` is found from its crossbar pair alone. The other pairs do not need any special treatment and simply generate candidates that are absent.

### Sample 2

Consider:

```
1
5
0 0
2 0
1 0
1 2
1 -2
```

The expected output is:

```
Set #1: 2
```

The same crossbar now has both possible stem endpoints.

| A | B | M | Candidate C | Found | Answer |
| --- | --- | --- | --- | --- | --- |
| `(0,0)` | `(2,0)` | `(1,0)` | `(1,2)` | yes | 1 |
| `(0,0)` | `(2,0)` | `(1,0)` | `(1,-2)` | yes | 2 |
| `(0,0)` | `(1,0)` | `(0.5,0)` | `(0.5,1)` | no | 2 |
| `(0,0)` | `(1,2)` | `(0.5,1)` | `(-1.5,1.5)` | no | 2 |
| `(2,0)` | `(1,0)` | `(1.5,0)` | `(1.5,1)` | no | 2 |
| remaining pairs |  |  |  | no | 2 |

This example exercises the two-direction part of the construction. A solution that checks only one perpendicular direction would incorrectly return `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(p^3) | O(p²) unordered crossbar pairs, two candidates per pair, and O(p) point scans |
| Space | O(p) | The input point set is stored in memory |

With `p <= 50`, the worst case is only about `50² * 50 = 125,000` point comparisons per test case up to constant factors, or roughly 12.5 million comparisons over 100 maximum-sized cases. That is comfortably smaller than the hundreds of millions of four-point assignments considered by brute force. The official bounds are small enough that the straightforward floating-point scan is preferable to introducing a more complicated spatial lookup structure.

## Test Cases

The following test harness uses the same `solve_case` logic as the submission. The custom cases cover the minimum number of points, both possible stem directions, floating-point coordinates, and a larger set containing several unrelated points.

```python
import sys
import io

EPS = 1e-6

def same_point(x1, y1, x2, y2):
    return abs(x1 - x2) <= EPS and abs(y1 - y2) <= EPS

def solve_case(points):
    n = len(points)
    ans = 0

    for i in range(n):
        ax, ay = points[i]

        for j in range(i + 1, n):
            bx, by = points[j]

            dx = bx - ax
            dy = by - ay

            mx = (ax + bx) / 2.0
            my = (ay + by) / 2.0

            candidates = (
                (mx - dy, my + dx),
                (mx + dy, my - dx),
            )

            for cx, cy in candidates:
                for px, py in points:
                    if same_point(cx, cy, px, py):
                        ans += 1
                        break

    return ans

def solution(data):
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)

    t = int(input())
    out = []

    for case_no in range(1, t + 1):
        p = int(input())
        points = [tuple(map(float, input().split())) for _ in range(p)]
        out.append(f"Set #{case_no}: {solve_case(points)}")
        out.append("")

    sys.stdin = old_stdin
    return "\n".join(out)

def run(inp: str) -> str:
    return solution(inp)

# Constructed sample 1
assert run("""1
4
0 0
2 0
1 0
1 2
""") == "Set #1: 1\n", "one T"

# Constructed sample 2
assert run("""1
5
0 0
2 0
1 0
1 2
1 -2
""") == "Set #1: 2\n", "both stem directions"

# Minimum-size case with no T
assert run("""1
4
0 0
1 0
0 1
1 1
""") == "Set #1: 0\n", "minimum size, no valid T"

# All points form two T's around the same crossbar
assert run("""1
6
-1 0
1 0
0 0
0 2
0 -2
3 3
""") == "Set #1: 2\n", "unrelated point must not matter"

# Floating-point coordinates
assert run("""1
4
0.1 0.1
2.1 0.1
1.1 0.1
1.1 2.1
""") == "Set #1: 1\n", "floating-point midpoint"

# Several unrelated points and a diagonal crossbar
assert run("""1
7
0 0
2 2
1 1
-1 3
3 -1
10 10
-5 -4
""") == "Set #1: 2\n", "diagonal crossbar with both stems"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Four points forming one axis-aligned `T` | `Set #1: 1` | Basic construction |
| Five points with both perpendicular stems | `Set #1: 2` | Both candidate directions |
| Four corners of a unit square | `Set #1: 0` | Minimum-size case without a valid `T` |
| Valid `T` plus unrelated point | `Set #1: 2` | Irrelevant points do not affect the count |
| Decimal coordinates | `Set #1: 1` | Floating-point midpoint handling |
| Diagonal crossbar with unrelated points | `Set #1: 2` | Rotation logic for non-axis-aligned geometry |

The last case is especially useful because a solution written only for horizontal or vertical segments would fail it. The perpendicular-vector formula works identically for every orientation.

## Edge Cases

The first edge case is duplicate counting from exchanging `A` and `B`. For

```
1
4
0 0
2 0
1 0
1 2
```

the pair `(0,0),(2,0)` produces `(1,2)` as a valid stem endpoint. When the loops later consider `(2,0),(0,0)`, they do not process it because the algorithm requires `i < j`. The answer remains `1`, rather than becoming `2`.

The second edge case is floating-point equality. For

```
1
4
0.1 0.1
2.1 0.1
1.1 0.1
1.1 2.1
```

the midpoint of the first two points is `(1.1, 0.1)`. The candidate stem is `(1.1, 2.1)`, which is present. The comparison uses an absolute tolerance of `10^-6` on both coordinates, so small representation errors do not change the result. The output is `Set #1: 1`.

The third edge case is that a crossbar can have two valid stems. For

```
1
5
0 0
2 0
1 0
1 2
1 -2
```

the midpoint is `(1,0)`, while the two perpendicular vectors are `(0,2)` and `(0,-2)`. Both generated points are present, so the algorithm increments the answer twice and outputs `Set #1: 2`.

The fourth edge case is a diagonal crossbar. Consider

```
1
7
0 0
2 2
1 1
-1 3
3 -1
10 10
-5 -4
```

The crossbar vector is `(2,2)`, its midpoint is `(1,1)`, and the two equal-length perpendicular vectors are `(-2,2)` and `(2,-2)`. The corresponding stem endpoints are `(-1,3)` and `(3,-1)`, both present in the input. The answer is `2`. The calculation uses vector rotation rather than assumptions about horizontal or vertical coordinates, so the same reasoning handles arbitrary orientations.
