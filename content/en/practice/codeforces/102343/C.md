---
title: "CF 102343C - Fitting on the Bed"
description: "The bed is an axis-aligned rectangle whose lower-left corner is (0, 0) and whose upper-right corner is (W, L). Anya is modeled as a line segment of length H."
date: "2026-08-17T18:06:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "C"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 816
verified: true
draft: false
---

[CF 102343C - Fitting on the Bed](https://codeforces.com/problemset/problem/102343/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The bed is an axis-aligned rectangle whose lower-left corner is `(0, 0)` and whose upper-right corner is `(W, L)`. Anya is modeled as a line segment of length `H`. Her head is one endpoint of that segment, located at `(x, y)`, and the angle `a` describes the direction from her head toward her feet. An angle of `0` points to the right, while `90` points upward, so the usual mathematical convention applies.

The task is to determine whether the entire segment lies inside the bed. Touching the boundary is allowed, so an endpoint with coordinate exactly `0`, `W`, `0`, or `L` is still valid.

The input contains only six integers, with `L` and `W` at most `500`, `H` at most `200`, and the head coordinates constrained to the bed. These bounds are tiny, but the real simplification is structural rather than computational. There is no large graph, array, or search space to process. A constant number of arithmetic operations is enough.

The main edge cases come from the fact that the head is guaranteed to be inside the bed, but the other endpoint is not. For example,

```
100 100 20
90 50 0
```

gives the second endpoint `(110, 50)`, so the answer is `NO`. A careless implementation that checks only the head position would incorrectly accept it.

A boundary endpoint is valid. For example,

```
100 100 20
80 50 0
```

puts the second endpoint at `(100, 50)`, exactly on the right edge. The correct output is `YES`. Using strict inequalities such as `0 < x < W` would incorrectly reject it.

The direction can point downward or to the left, so simply adding `H * cos(a)` and `H * sin(a)` without considering their signs is another common mistake. For example,

```
100 100 20
50 50 270
```

ends at `(50, 30)`, which is inside the bed. The correct output is `YES`.

The segment may also fit diagonally even when one horizontal or vertical projection looks large. For example,

```
100 100 50
50 75 225
```

ends at approximately `(14.64, 39.64)`, so both endpoints are inside and the answer is `YES`.

## Approaches

A direct geometric approach might try to examine many points along Anya's body and check whether each point lies inside the rectangle. If we discretize the body into one-centimeter pieces, there are at most `H + 1 <= 201` points, so this version would actually run comfortably within the limits. Its weakness is conceptual rather than practical: a continuous line segment contains infinitely many points, and checking a finite sample does not by itself prove that the unsampled portions are inside.

The useful observation is that the bed is a convex set. A line segment whose two endpoints are inside a convex set is completely inside that set. A rectangle is convex, so we do not need to inspect the interior of Anya's body at all. The head is already given, so only the endpoint at her feet needs to be computed and checked.

The brute-force idea works because it tries to verify the whole segment point by point, but it is unnecessary and does not naturally give an exact continuous proof. The convexity observation reduces the entire problem to computing one endpoint and performing four coordinate comparisons.

The endpoint is obtained from the standard polar-coordinate displacement:

`dx = H * cos(a)`

`dy = H * sin(a)`

so the feet are at

`(x + dx, y + dy)`.

Because the trigonometric functions use radians, the input angle must first be converted with `a * pi / 180`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Discretize the segment | O(H) | O(1) | Accepted for these bounds, but conceptually unnecessary |
| Check the second endpoint | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the bed dimensions `L` and `W`, Anya's height `H`, and the head position `(x, y)` together with the angle `a`. The head itself is already known to be on the bed, so it does not need a separate geometric search.
2. Convert the angle from degrees to radians. Python's `math.sin` and `math.cos` expect radians, so using the degree value directly would produce a completely different direction.
3. Compute the displacement of Anya's feet from her head using `H * cos(a)` horizontally and `H * sin(a)` vertically. Negative values are valid because Anya may face left or downward.
4. Add the displacement to the head coordinates to obtain the second endpoint `(fx, fy)`.
5. Check whether `fx` lies between `0` and `W` and whether `fy` lies between `0` and `L`, using inclusive comparisons. A small floating-point tolerance is used because values such as `cos(90°)` are represented approximately rather than as exact zeroes.
6. Print `YES` if both coordinates are within their respective ranges. Otherwise print `NO`.

The key property is that throughout the algorithm we only need to maintain the fact that both endpoints of Anya's segment are inside the rectangle. The head is inside by the input specification, and after the final coordinate check the feet are also inside. Since the rectangle is convex, every point between those two endpoints is inside it as well. Thus the entire segment fits exactly when the computed second endpoint fits.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    L, W, H = map(int, input().split())
    x, y, angle = map(int, input().split())

    rad = math.radians(angle)

    foot_x = x + H * math.cos(rad)
    foot_y = y + H * math.sin(rad)

    eps = 1e-9

    if -eps <= foot_x <= W + eps and -eps <= foot_y <= L + eps:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The first input line gives the rectangle dimensions and the segment length. The second line gives the head coordinates and direction.

`math.radians(angle)` performs the required degree-to-radian conversion. The endpoint calculation follows directly from the geometric displacement of a vector with length `H`.

The comparisons are inclusive because touching a bed boundary still counts as fitting. The tolerance handles floating-point noise near exact boundary cases. For example, mathematically `cos(90°) = 0`, but the computed value can be a tiny number such as `6.12e-17`.

There is no integer-overflow concern in Python, and the floating-point values are small because every coordinate and length is at most a few hundred. The order of operations also matters: the angle must be converted before calling `sin` and `cos`.

## Worked Examples

Since the archived Codeforces problem page does not expose the original sample values, the following traces use representative inputs that exercise the same geometry.

### Example 1

Input:

```
100 100 20
90 50 0
```

The body points directly right, so the horizontal coordinate increases by `20`.

| Step | L | W | H | x | y | angle | foot_x | foot_y | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Read input | 100 | 100 | 20 | 90 | 50 | 0° |  |  |  |
| Convert angle | 100 | 100 | 20 | 90 | 50 | 0 rad |  |  |  |
| Compute endpoint | 100 | 100 | 20 | 90 | 50 | 0 rad | 110 | 50 |  |
| Check bounds | 100 | 100 | 20 | 90 | 50 | 0 rad | 110 | 50 | `NO` |

The head is inside the bed, but the feet are at `x = 110`, beyond the right edge. Since one endpoint is outside, the segment cannot fit.

### Example 2

Input:

```
100 100 50
50 75 225
```

The angle `225°` points down and left.

| Step | L | W | H | x | y | angle | foot_x | foot_y | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Read input | 100 | 100 | 50 | 50 | 75 | 225° |  |  |  |
| Convert angle | 100 | 100 | 50 | 50 | 75 | `3.927...` |  |  |  |
| Compute endpoint | 100 | 100 | 50 | 50 | 75 | `3.927...` | `14.64...` | `39.64...` |  |
| Check bounds | 100 | 100 | 50 | 50 | 75 | `3.927...` | `14.64...` | `39.64...` | `YES` |

Both endpoints lie inside the rectangle. Convexity then gives the entire segment for free, so there is no reason to test intermediate points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one angle conversion, two trigonometric evaluations, and a constant number of comparisons are required |
| Space | O(1) | Only a constant number of scalar variables are stored |

The constraints are already small, but the constant-time solution is independent of `L`, `W`, and `H`. It comfortably fits the one-second time limit and uses negligible memory.

## Test Cases

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    L, W, H = map(int, input().split())
    x, y, angle = map(int, input().split())

    rad = math.radians(angle)

    foot_x = x + H * math.cos(rad)
    foot_y = y + H * math.sin(rad)

    eps = 1e-9

    if -eps <= foot_x <= W + eps and -eps <= foot_y <= L + eps:
        print("YES")
    else:
        print("NO")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Custom cases

assert run("1 1 0\n0 0 0\n") == "YES\n", "zero-length segment"

assert run("100 100 20\n90 50 0\n") == "NO\n", \
    "feet pass through the right boundary"

assert run("100 100 20\n80 50 0\n") == "YES\n", \
    "feet land exactly on the right boundary"

assert run("100 100 20\n50 50 270\n") == "YES\n", \
    "downward direction"

assert run("100 100 50\n50 75 225\n") == "YES\n", \
    "diagonal segment"

assert run("500 500 200\n0 0 180\n") == "NO\n", \
    "maximum-size boundary case with feet outside"

assert run("500 500 200\n250 250 45\n") == "YES\n", \
    "maximum dimensions with a diagonal segment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0` with head `(0,0)` | `YES` | Minimum dimensions and zero-length segment |
| `100 100 20`, head `(90,50)`, angle `0` | `NO` | Endpoint crosses the right boundary |
| `100 100 20`, head `(80,50)`, angle `0` | `YES` | Exact boundary contact is allowed |
| `100 100 20`, head `(50,50)`, angle `270` | `YES` | Negative vertical displacement |
| `100 100 50`, head `(50,75)`, angle `225` | `YES` | Diagonal placement |
| `500 500 200`, head `(0,0)`, angle `180` | `NO` | Maximum dimensions and leftward overflow |
| `500 500 200`, head `(250,250)`, angle `45` | `YES` | Large valid diagonal placement |

## Edge Cases

A head that is inside the bed does not imply that Anya fits. For

```
100 100 20
90 50 0
```

the displacement is `(20, 0)`, so the feet are at `(110, 50)`. The x-coordinate violates `0 <= x <= 100`, and the algorithm prints `NO`.

Exact boundary contact must be accepted. For

```
100 100 20
80 50 0
```

the feet are at `(100, 50)`. The condition `foot_x <= W` is satisfied exactly, so the answer is `YES`. The small epsilon also protects this comparison against harmless floating-point representation error.

Angles in the lower half of the circle produce negative vertical displacement. For

```
100 100 20
50 50 270
```

the endpoint is mathematically `(50, 30)`. Both coordinates are within the rectangle, so the algorithm prints `YES`. Treating the angle as if it always produced positive movement would fail here.

A diagonal direction can change both coordinates simultaneously. For

```
100 100 50
50 75 225
```

the endpoint is approximately `(14.64, 39.64)`. Both coordinates remain inside the bed, and convexity guarantees that every point between the head and feet also remains inside. The answer is `YES`.

Finally, a segment of length zero is already completely determined by its head. With

```
1 1 0
0 0 0
```

both endpoints are `(0, 0)`, which lies on the lower-left corner of the bed. Boundary points are valid, so the correct output is `YES`.
