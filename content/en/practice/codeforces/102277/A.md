---
title: "CF 102277A - Window on the Wall"
description: "The problem asks for the largest rectangular window that can be cut into a rectangular wall. The wall has width w and height h, and the window must stay at least d units away from every edge of the wall. The required gap applies independently to all four sides."
date: "2026-08-17T03:26:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "A"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 419
verified: true
draft: false
---

[CF 102277A - Window on the Wall](https://codeforces.com/problemset/problem/102277/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks for the largest rectangular window that can be cut into a rectangular wall. The wall has width `w` and height `h`, and the window must stay at least `d` units away from every edge of the wall. The required gap applies independently to all four sides. We need to output the maximum possible window area, or `0` when the required gap leaves no room for a window. The original contest specifies `w, h < 1000` and `d < 100`, with a one-second time limit and 256 MB of memory.

The geometry immediately reduces the available width by `d` on the left and `d` on the right, so the largest possible window width is `w - 2d`. The same reasoning gives a maximum height of `h - 2d`. If either value is non-positive, no window with positive area can fit. Otherwise, the largest rectangle uses both available dimensions.

The small bounds mean even an `O(w h)` enumeration would only examine roughly one million pairs in the worst case, since `w` and `h` are below `1000`. That is not remotely comparable to the `10^5`-scale constraints where quadratic algorithms are automatically ruled out. However, this problem contains enough geometric structure that enumeration is unnecessary: the answer can be computed with a constant number of arithmetic operations.

There are two boundary cases that commonly cause incorrect implementations. First, the gap can consume an entire dimension. For example, with input `30 20 12`, the available width is `30 - 24 = 6`, while the available height is `20 - 24 = -4`, so the correct output is `0`. A careless implementation that multiplies the two values without checking them produces `-24`, which cannot represent a window area.

Second, the gap can be larger than half of both dimensions. For `40 25 50`, the available dimensions are `-60` and `-75`, so the answer is again `0`. Checking only whether `w - 2d` is positive is insufficient because the height must also be large enough. The official samples include both of these impossible cases.

The other boundary is the exact-fit case. If `w = 2d` or `h = 2d`, the corresponding window dimension is zero. A rectangle of zero area is not a usable window, so the answer must still be `0`. For example, `10 20 5` leaves width `0`, giving output `0`.

## Approaches

A direct brute-force approach could enumerate every integer width from `1` through `w - 1` and every integer height from `1` through `h - 1`. For each pair, we would check whether the rectangle can fit while leaving the required gap on every side, and keep the largest valid area. The method is correct because every candidate pair of dimensions is considered, so the best valid pair must eventually be found.

With `w, h < 1000`, that enumeration performs at most about `(w - 1)(h - 1)`, which is below one million dimension pairs. So unlike many Codeforces problems, the brute force is not actually catastrophic under these constraints. It is nevertheless solving a much more general problem than necessary, and its `O(w h)` work is avoidable.

The key observation is that enlarging a valid window can never make its area smaller. Once the required border has been reserved, the window can occupy every remaining unit of width and every remaining unit of height. There is no interaction between the horizontal and vertical constraints, so the optimal width and optimal height can be determined independently.

The wall gives `w` units horizontally. The left border consumes `d`, and the right border consumes another `d`, leaving `w - 2d`. Vertically, the top and bottom borders similarly leave `h - 2d`. If both quantities are positive, their product is the largest possible area. If either is non-positive, no positive-area window exists.

The brute-force works because it eventually tests the maximum dimensions, but fails to exploit the fact that every smaller valid dimension is dominated by a larger one. The observation that both dimensions can simply be pushed to their maximum values reduces the entire problem to constant-time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(w h) | O(1) | Accepted under the given bounds, but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the wall width `w`, wall height `h`, and required border gap `d`.
2. Compute the maximum possible window width as `w - 2d`. The subtraction is by `2d` because the window must leave `d` units on both the left and right sides.
3. Compute the maximum possible window height as `h - 2d`. The same argument applies to the top and bottom sides.
4. Check whether either available dimension is less than or equal to zero. If so, output `0`, because a non-positive width or height cannot form a positive-area rectangular window.
5. Otherwise, multiply the available width and height and output the product. Choosing the maximum available value in either direction cannot hurt the area, so these two dimensions together give the largest possible window.

### Why it works

Consider any valid window. Because it must leave at least `d` units between its perimeter and each wall edge, its width can never exceed `w - 2d`, and its height can never exceed `h - 2d`. When both quantities are positive, a window with exactly those dimensions fits by placing the required gap on each side, so no valid window can have a larger width or height. Since area is the product of width and height, `(w - 2d)(h - 2d)` is the maximum possible area. When either dimension is non-positive, no positive-area rectangle can satisfy the border requirement, so returning zero is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

w, h, d = map(int, input().split())

window_w = w - 2 * d
window_h = h - 2 * d

if window_w <= 0 or window_h <= 0:
    print(0)
else:
    print(window_w * window_h)
```

The first line reads the three integers from the only input line. There are no test cases to loop over, so the program performs the computation exactly once.

The next two assignments translate the geometry directly into arithmetic. `2 * d` is used rather than `d` because the required border appears on both opposite sides of each dimension.

The condition uses `<= 0`, not `< 0`. When the remaining dimension is exactly zero, the resulting rectangle has zero area and is not a valid positive-area window.

Python integers do not overflow, and the given bounds make the resulting area very small anyway. The solution also uses only a constant amount of memory.

## Worked Examples

For Sample 1, the input is `40 25 5`. The required gap removes `5` units from each side.

| Step | `w` | `h` | `d` | `window_w` | `window_h` | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Read input | 40 | 25 | 5 |  |  |  |
| Compute dimensions | 40 | 25 | 5 | 30 | 15 |  |
| Check feasibility | 40 | 25 | 5 | 30 | 15 | valid |
| Compute area | 40 | 25 | 5 | 30 | 15 | 450 |

Both remaining dimensions are positive, so the entire `30 × 15` interior can be used. The output is `450`, matching the sample.

For Sample 2, consider `30 20 12`.

| Step | `w` | `h` | `d` | `window_w` | `window_h` | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Read input | 30 | 20 | 12 |  |  |  |
| Compute dimensions | 30 | 20 | 12 | 6 | -4 |  |
| Check feasibility | 30 | 20 | 12 | 6 | -4 | invalid |
| Output | 30 | 20 | 12 | 6 | -4 | 0 |

The horizontal dimension still has room, but the vertical dimension does not. A single invalid dimension is enough to make the whole window impossible, so the algorithm returns `0`.

These traces demonstrate why feasibility must be checked before multiplying the dimensions. The multiplication itself has no geometric meaning when one of the dimensions is non-positive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only two subtractions, one comparison, and at most one multiplication are performed |
| Space | O(1) | Only a constant number of integer variables are stored |

The official bounds are below `1000` for the wall dimensions and below `100` for the gap, so the constant-time solution is far below the requirements of the one-second and 256 MB limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    w, h, d = map(int, input().split())

    window_w = w - 2 * d
    window_h = h - 2 * d

    if window_w <= 0 or window_h <= 0:
        print(0)
    else:
        print(window_w * window_h)

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

# Provided samples
assert run("40 25 5\n") == "450\n", "sample 1"
assert run("30 20 12\n") == "0\n", "sample 2"
assert run("40 25 50\n") == "0\n", "sample 3"
assert run("999 888 7\n") == "860890\n", "sample 4"

# Minimum-size dimensions
assert run("1 1 1\n") == "0\n", "no room for a window"

# Exact-fit boundary
assert run("10 20 5\n") == "0\n", "zero remaining width"

# All dimensions comfortably fit
assert run("100 100 10\n") == "6400\n", "all-equal wall dimensions"

# Maximum-size input values
assert run("999 999 99\n") == "641601\n", "maximum bounds"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `0` | Minimum dimensions and impossible installation |
| `10 20 5` | `0` | Exact zero-width boundary |
| `100 100 10` | `6400` | Symmetric dimensions and ordinary valid case |
| `999 999 99` | `641601` | Maximum input bounds and arithmetic |

## Edge Cases

For `30 20 12`, the algorithm computes `window_w = 6` and `window_h = -4`. Since `window_h <= 0`, it immediately outputs `0`. This prevents a negative product from being mistaken for an area.

For `40 25 50`, the available dimensions are `-60` and `-75`. The same feasibility check returns `0`. This catches implementations that assume the input always leaves enough room simply because `w` and `h` themselves are positive.

For the exact-fit case `10 20 5`, the available width is `10 - 2(5) = 0`. The algorithm treats zero as impossible and outputs `0`, rather than accepting a degenerate rectangle.

For a normal valid case such as `40 25 5`, the available dimensions are `30` and `15`. Both are positive, so the algorithm multiplies them and obtains `450`. The calculation uses every part of the wall that is allowed to belong to the window, which proves that no smaller candidate can be optimal.
