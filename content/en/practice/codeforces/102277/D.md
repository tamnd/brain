---
title: "CF 102277D - Circle Meets Square"
description: "We have a circle and an axis-aligned square in the Cartesian plane. The circle is described by its center (x, y) and radius r. The square is described by its bottom-left corner (tx, ty) and side length s, so its opposite corner is (tx + s, ty + s)."
date: "2026-08-16T19:33:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "D"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 65
verified: true
draft: false
---

[CF 102277D - Circle Meets Square](https://codeforces.com/problemset/problem/102277/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circle and an axis-aligned square in the Cartesian plane. The circle is described by its center `(x, y)` and radius `r`. The square is described by its bottom-left corner `(tx, ty)` and side length `s`, so its opposite corner is `(tx + s, ty + s)`. The task is to classify their geometric relationship. We print `0` when they are disjoint, `1` when their common part consists of exactly one point, and `2` when they overlap with positive area. The official limits are only `1000` in magnitude for the coordinates and dimensions, with a 1 second time limit and 256 MB of memory.

The numerical bounds are small, but they do not suggest a useful simulation. The objects contain infinitely many points, and even iterating over every integer coordinate in the bounding box would not be a valid geometric algorithm because a tangency point can have non-integer coordinates. The clean solution should use a constant number of arithmetic operations and avoid floating-point geometry entirely.

There are several boundary cases where an implementation that only checks whether some corner lies inside the other object can fail. For example,

```
0 0 5
5 0 6
```

has output `1`. The square starts at `(5, 0)`, which is exactly five units from the circle center, so the two objects touch at `(5, 0)`. A strict `< r` test would incorrectly report `0`, because the touching point is on the circle rather than inside it.

A second case is a circle completely inside the square:

```
0 0 1
-5 -5 10
```

The correct output is `0`. The circle does not intersect the square's boundary at all, even though the two geometric regions have containment. A method that assumes "one object is inside the other, so they overlap" would confuse containment with boundary intersection. The required classification is about whether the circle and square have a common region or a single common point, so for the disk and square regions this case actually has positive-area intersection and must be classified as `2`. This illustrates why the exact meaning of the objects matters: the circle represents its filled interior as part of the region being compared.

A more useful edge case is the reverse containment:

```
0 0 10
-1 -1 2
```

The correct output is `2`. The entire square lies inside the circle, so their intersection has positive area. Checking only whether a circle extreme point lies inside the square would miss this completely.

The cleanest way to avoid all of these special cases is to reduce the problem to one quantity: the minimum distance from the circle's center to any point of the square.

## Approaches

A direct geometric brute force can enumerate the square's four corners and the four cardinal points of the circle, then classify whether any of those candidate points lies strictly inside or exactly on the other shape. This is a constant-size search, and with the appropriate convexity argument it can solve the problem. It performs four corner-to-circle checks and four circle-extreme-point-to-square checks, so its worst case is eight distance or containment checks, plus the corresponding arithmetic. The approach is accepted asymptotically because this problem has only one test case, but it is easy to make it incomplete by forgetting containment configurations or boundary cases.

The better observation is that we do not need to search for an intersection point at all. For a fixed circle center, find the point of the square that is closest to that center. If the center is horizontally outside the square, the closest point must use the corresponding vertical side. If the center is horizontally inside the square, its closest point has the same `x` coordinate. The same reasoning applies independently to the `y` coordinate.

This gives the closest square point by clamping each coordinate independently. If the center has coordinate `x`, and the square spans `[tx, tx+s]`, the closest valid square `x` coordinate is

```
min(max(x, tx), tx+s)
```

and similarly for `y`.

Once the closest point is known, the geometry becomes a simple distance comparison. Let `d` be the distance from the circle center to that point. If `d < r`, the circle reaches into the square with positive area. If `d = r`, the circle is tangent to the square at exactly one point. If `d > r`, the circle and square are disjoint, unless the square is completely inside the circle. The latter case is already covered by `d < r`, because the circle center is then either inside the square or close enough to the square boundary that the circle contains part of the square.

The important simplification is that the comparison can be done with squared distances. Since both `d` and `r` are nonnegative, comparing `d²` with `r²` gives exactly the same result and avoids square roots and floating-point precision issues.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Corner and extreme-point checks | O(1) | O(1) | Accepted, but more case-heavy |
| Closest point by clamping | O(1) | O(1) | Accepted, preferred |

## Algorithm Walkthrough

1. Read the circle center `(x, y)`, radius `r`, and the square's bottom-left corner `(tx, ty)` and side length `s`.
2. Compute the square's right and top boundaries as `right = tx + s` and `top = ty + s`. The square is exactly the Cartesian product `[tx, right] × [ty, top]`.
3. Clamp the circle center's `x` coordinate to the square's horizontal interval. Compute `px = min(max(x, tx), right)`. If `x` is already inside the interval, `px` equals `x`. If `x` is to the left, `px` becomes `tx`, and if `x` is to the right, `px` becomes `right`.
4. Perform the same operation for `y`, obtaining `py = min(max(y, ty), top)`. The point `(px, py)` is the closest point in the square to the circle center.
5. Compute the squared distance from `(x, y)` to `(px, py)` as `dist2 = (x - px)^2 + (y - py)^2`. Compare it with `r^2`.
6. Print `2` if `dist2 < r^2`, because the circle extends into the square and the intersection has positive area. Print `1` if `dist2 == r^2`, because the nearest square point lies exactly on the circle. Otherwise print `0`, because every point of the square is farther from the circle center than the radius.

The invariant behind the algorithm is that `(px, py)` is always a closest point of the square to the circle center. Every point of the square is at least as far away from the center as this point. Consequently, if even this closest point lies outside the circle, the entire square is outside it. If it lies strictly inside the circle, a small neighborhood around that point also lies inside the circle, giving positive-area intersection. If it lies exactly on the circle, the square and circle meet at the closest point and cannot penetrate one another, giving a single-point contact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, y, r = map(int, input().split())
    tx, ty, s = map(int, input().split())

    right = tx + s
    top = ty + s

    px = min(max(x, tx), right)
    py = min(max(y, ty), top)

    dx = x - px
    dy = y - py

    dist2 = dx * dx + dy * dy
    r2 = r * r

    if dist2 < r2:
        print(2)
    elif dist2 == r2:
        print(1)
    else:
        print(0)

if __name__ == "__main__":
    solve()
```

The first two input lines describe the two geometric objects exactly as in the algorithm. We immediately compute the square's right and top boundaries, so subsequent expressions can treat the square as two closed coordinate intervals.

The two `min(max(...))` expressions implement coordinate clamping. Python's integer arithmetic is particularly convenient here because every input is integral and the largest squared difference is easily within Python's arbitrary-precision integer range.

The subtraction is deliberately performed after clamping. This gives the horizontal and vertical components of the shortest vector from the circle center to the square. Squaring and adding gives the squared minimum distance.

The strict and non-strict comparisons are both necessary. `<` means the closest square point is inside the circle, while `==` represents exact tangency. Replacing the equality case with `<=` would incorrectly classify every tangent configuration as an overlap.

No square root is taken, so there is no floating-point error around tangent cases such as a distance of exactly `5` compared with radius `5`.

## Worked Examples

### Sample 1

The first provided sample is:

```
0 0 5
2 3 1
```

The square spans `x = [2, 3]` and `y = [3, 4]`. The circle center `(0, 0)` lies below and to the left, so the closest square point is its bottom-left corner `(2, 3)`.

| `x` | `y` | `px` | `py` | `dist2` | `r2` | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 3 | 13 | 25 | 2 |

Since `13 < 25`, the closest point of the square is inside the circle. The intersection consequently contains an area rather than only a boundary point. The expected output is `2`.

### Sample 2

The second provided sample is:

```
0 0 5
5 0 6
```

The square spans `x = [5, 11]` and `y = [0, 6]`. The circle center is directly to the left of the square, so its closest point is `(5, 0)`.

| `x` | `y` | `px` | `py` | `dist2` | `r2` | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 0 | 25 | 25 | 1 |

The squared distances are equal, so the closest point lies exactly on the circle. The two shapes touch at one point, and the expected output is `1`.

### Sample 3

The third provided sample is:

```
0 5 4
-1 -1 1
```

The square spans `x = [-1, 0]` and `y = [-1, 0]`. The closest point to the circle center `(0, 5)` is `(0, 0)`.

| `x` | `y` | `px` | `py` | `dist2` | `r2` | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 0 | 25 | 16 | 0 |

Here `25 > 16`, so even the closest point of the square is outside the circle. The square and circle are disjoint, giving output `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of coordinate operations and arithmetic comparisons are performed. |
| Space | O(1) | Only a fixed number of integer variables are stored. |

The problem's coordinates and dimensions are bounded by `1000`, but the algorithm does not depend on those bounds at all. Its running time remains constant even if the coordinate limits are increased dramatically. It easily fits the 1 second and 256 MB limits specified for the problem.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    x, y, r = map(int, input().split())
    tx, ty, s = map(int, input().split())

    right = tx + s
    top = ty + s

    px = min(max(x, tx), right)
    py = min(max(y, ty), top)

    dx = x - px
    dy = y - py

    dist2 = dx * dx + dy * dy
    r2 = r * r

    if dist2 < r2:
        print(2)
    elif dist2 == r2:
        print(1)
    else:
        print(0)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("0 0 5\n2 3 1\n") == "2\n", "sample 1"
assert run("0 0 5\n5 0 6\n") == "1\n", "sample 2"
assert run("0 5 4\n-1 -1 1\n") == "0\n", "sample 3"

# Minimum-size objects, clearly separated
assert run("0 0 1\n2 2 1\n") == "0\n", "minimum sizes, disjoint"

# All values in the first and second descriptions are small and equal where possible.
# The circle center is inside the square.
assert run("0 0 1\n0 0 1\n") == "2\n", "center inside square"

# Exact corner tangency
assert run("0 0 5\n5 5 1\n") == "0\n", "corner is farther than radius"

# Exact side tangency, catches < versus <=
assert run("0 0 5\n5 0 1\n") == "1\n", "side tangency"

# Square completely inside the circle
assert run("0 0 10\n-1 -1 2\n") == "2\n", "square inside circle"

# Large coordinates and dimensions
assert run("1000 1000 1000\n-999 -999 1000\n") == "0\n", "large disjoint configuration"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 1 / 2 2 1` | `0` | Minimum-size objects and clear separation |
| `0 0 1 / 0 0 1` | `2` | Circle center inside the square |
| `0 0 5 / 5 5 1` | `0` | Diagonal distance and corner handling |
| `0 0 5 / 5 0 1` | `1` | Exact side tangency and equality handling |
| `0 0 10 / -1 -1 2` | `2` | Entire square contained inside the circle |
| `1000 1000 1000 / -999 -999 1000` | `0` | Large boundary values |

## Edge Cases

The first subtle case is exact tangency. With

```
0 0 5
5 0 1
```

the square's closest point to the center is `(5, 0)`. The squared distance is `25`, exactly equal to `r² = 25`, so the algorithm prints `1`. A strict-inside test without a separate equality case would incorrectly print `0`.

The second case is when the circle center lies inside the square. For

```
0 0 1
-5 -5 10
```

clamping leaves the center unchanged, so `(px, py) = (0, 0)`. The minimum squared distance is `0`, which is less than `1`. The algorithm prints `2`, correctly recognizing that the circle and square have a positive-area intersection.

The third case is when the square lies completely inside the circle:

```
0 0 10
-1 -1 2
```

Again, the circle center lies inside the square, so the closest square point to the center is the center itself and the minimum squared distance is `0`. Since `0 < 100`, the result is `2`. This case is useful because checking only circle boundary points against the square would miss the intersection entirely.

The fourth case is diagonal separation:

```
0 0 5
5 5 1
```

The closest point is `(5, 5)`, giving squared distance `25 + 25 = 50`. Since `50 > 25`, the result is `0`. Comparing squared distances also handles the diagonal without introducing a square root.

The fifth case is the large-coordinate boundary configuration:

```
1000 1000 1000
-999 -999 1000
```

The square ends at `(1, 1)`, which is the closest point to `(1000, 1000)`. The squared distance is `999² + 999²`, which is greater than `1000²`, so the algorithm prints `0`. This confirms that the coordinate boundaries do not require any special handling.
