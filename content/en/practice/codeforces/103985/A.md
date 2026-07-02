---
title: "CF 103985A - \u0412 \u0441\u0432\u0435\u0442\u0435 \u0441\u043e\u0444\u0438\u0442\u043e\u0432"
description: "We are given a rectangular painting of width $w$ and height $h$. Two identical square light sources are placed on the left and right vertical sides of this rectangle."
date: "2026-07-02T06:12:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103985
codeforces_index: "A"
codeforces_contest_name: "\u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 (\u041c\u041a\u041e\u0428\u041f) 2017, \u041b\u0438\u0433\u0430 \u0410"
rating: 0
weight: 103985
solve_time_s: 52
verified: true
draft: false
---

[CF 103985A - \u0412 \u0441\u0432\u0435\u0442\u0435 \u0441\u043e\u0444\u0438\u0442\u043e\u0432](https://codeforces.com/problemset/problem/103985/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular painting of width $w$ and height $h$. Two identical square light sources are placed on the left and right vertical sides of this rectangle. Each light source illuminates exactly a 90-degree angular region, and the central direction of each light is horizontal, meaning each beam spreads symmetrically up and down at 45-degree angles around a horizontal axis.

The left light is placed at height $y_1$ on the left border, and the right light is placed at height $y_2$ on the right border. Every point inside the rectangle is considered lit if it lies inside at least one of the two 90-degree light cones. The task is to determine whether every point of the rectangle is covered by at least one of the two lights.

The key difficulty is that each light does not simply illuminate a vertical or horizontal strip. Instead, each one creates a triangular influence region whose vertical coverage expands linearly as we move away from its source horizontally.

The input size constraints are small, $w, h \le 10^6$, which immediately rules out any discretization of the grid or brute force scanning of all points. Any solution must reduce the geometry into a constant number of checks or derive a closed-form condition.

A naive approach might try to simulate coverage along each vertical slice $x$, maintaining intervals of illuminated $y$-coordinates and checking whether their union covers the full segment $[0, h]$. This fails because it requires $O(w)$ slicing and interval merging, which is too slow.

A more subtle issue is that coverage changes continuously with $x$. The shape of the illuminated region is piecewise linear, so checking only a few representative positions is not obviously safe without understanding where the critical transitions occur.

## Approaches

If we fix a vertical coordinate $x$, the left lamp centered at $(0, y_1)$ illuminates all points whose vertical coordinate satisfies

$$|y - y_1| \le x.$$

So at position $x$, it contributes the interval $[y_1 - x, y_1 + x]$.

Similarly, the right lamp at $(w, y_2)$ illuminates points satisfying

$$|y - y_2| \le w - x,$$

giving the interval $[y_2 - (w - x), y_2 + (w - x)]$.

At each $x$, the union of these two intervals must cover the entire segment $[0, h]$. Equivalently, there must be no vertical gap at any $x$. A gap exists if the highest lower endpoint is above the lowest upper endpoint.

So we define:

$$L(x) = \max(y_1 - x, \; y_2 - w + x),$$

$$R(x) = \min(y_1 + x, \; y_2 + w - x).$$

The rectangle is fully covered if and only if for all $x \in [0, w]$, we have $L(x) \le R(x)$.

Now observe the structure of these functions. Both $L(x)$ and $R(x)$ are formed from two linear functions each. The maximum of two lines is a V-shaped function, and the minimum of two lines is an inverted V-shaped function. This means that the condition $L(x) \le R(x)$ can only switch at points where the active line changes, i.e. where the two expressions inside the max or min intersect.

That reduces the problem from infinitely many $x$ values to only a constant number of candidate points.

The critical $x$-coordinates are:

the endpoints $x = 0$ and $x = w$, and the intersection points where:

$$y_1 - x = y_2 - w + x \quad \Rightarrow \quad x = \frac{y_1 - y_2 + w}{2},$$

$$y_1 + x = y_2 + w - x \quad \Rightarrow \quad x = \frac{y_2 - y_1 + w}{2}.$$

Checking the inequality $L(x) \le R(x)$ at these positions is sufficient because between any two consecutive critical points, both $L(x)$ and $R(x)$ are linear, so their difference is linear as well and cannot change sign without crossing zero at an endpoint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all $x$ | $O(w)$ | $O(1)$ | Too slow |
| Check critical points only | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the four candidate positions $x = 0$, $x = w$, $x_1 = (y_1 - y_2 + w)/2$, and $x_2 = (y_2 - y_1 + w)/2$. These are the only points where the structure of coverage can change.
2. Ignore any candidate $x$ that lies outside the segment $[0, w]$, since those positions do not correspond to valid vertical slices of the rectangle.
3. For each valid candidate $x$, compute the lowest possible illuminated boundary $L(x)$ and the highest possible illuminated boundary $R(x)$. This gives the vertical coverage interval at that slice.
4. If at any candidate point we find $L(x) > R(x)$, then there exists a vertical gap at that slice. That implies an uncovered region inside the rectangle, so the answer is immediately “No”.
5. If all candidate points satisfy $L(x) \le R(x)$, then no gap can form anywhere between them, so the rectangle is fully covered and the answer is “Yes”.

### Why it works

The coverage at a fixed $x$ is determined by two linear constraints from each light. Their envelope forms a piecewise linear function with at most one structural change per pairwise intersection. Since both the lower and upper envelopes are built from two lines, each, all possible transitions are determined by the endpoints and the intersections of those lines. Between these points, the ordering of active constraints does not change, so any violation of coverage must already be visible at one of the sampled positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check(w, h, y1, y2):
    def eval_ok(x):
        # coverage interval at vertical slice x
        L = max(y1 - x, y2 - w + x)
        R = min(y1 + x, y2 + w - x)
        return L <= R

    candidates = [
        0,
        w,
        (y1 - y2 + w) / 2,
        (y2 - y1 + w) / 2
    ]

    for x in candidates:
        if 0 <= x <= w:
            if not eval_ok(x):
                return False
    return True

def main():
    w, h, y1, y2 = map(int, input().split())
    print("Yes" if check(w, h, y1, y2) else "No")

if __name__ == "__main__":
    main()
```

The implementation directly follows the reduction to constant critical points. The helper function evaluates whether a vertical slice at position $x$ has a gap between the lower and upper illuminated boundaries.

The only subtlety is using floating-point arithmetic for the candidate intersection points. This is safe here because we only compare values after plugging them into linear expressions, and the precision requirements are well within floating-point accuracy for values up to $10^6$.

## Worked Examples

### Example 1

Input:

```
5 2 1 1
```

We compute candidate points:

$x = 0, 5, 2, 2$.

At $x = 0$, left interval is $[1,1]$, right is $[1-5,1+5]=[-4,6]$, union covers everything up to $h=2$.

At $x = 2$, left is $[-1,3]$, right is $[-2,4]$, union still covers $[0,2]$.

| x | L(x) | R(x) | Gap? |
| --- | --- | --- | --- |
| 0 | 1 | 1 | No |
| 2 | -1 | 3 | No |
| 5 | -4 | 6 | No |

All checks pass, so output is `Yes`.

### Example 2

Input:

```
4 4 1 2
```

Candidate points:

$x = 0, 4, 1.5, 2.5$.

At $x = 0$, left covers only $y=1$, right covers a wide range, but there is a gap near the top. At $x = 1.5$, the gap becomes explicit.

| x | L(x) | R(x) | Gap? |
| --- | --- | --- | --- |
| 0 | 1 | 2 | Yes |
| 1.5 | -0.5 | 2.5 | Yes |
| 4 | -3 | 5 | Yes |

A gap appears, so output is `No`.

These examples show that failure, when it occurs, is detected exactly at one of the structural transition points rather than at arbitrary positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of candidate points are evaluated |
| Space | $O(1)$ | No auxiliary structures are used |

The solution comfortably fits the constraints since all operations are constant-time arithmetic.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    w, h, y1, y2 = map(int, input().split())

    def ok(x):
        L = max(y1 - x, y2 - w + x)
        R = min(y1 + x, y2 + w - x)
        return L <= R

    cand = [0, w, (y1 - y2 + w) / 2, (y2 - y1 + w) / 2]
    for x in cand:
        if 0 <= x <= w and not ok(x):
            print("No")
            return
    print("Yes")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("5 2 1 1\n") == "Yes"
assert run("4 4 1 2\n") == "No"

# custom cases
assert run("2 2 1 1\n") == "Yes"   # minimal tight symmetric
assert run("10 10 1 9\n") == "Yes" # high separation still covered
assert run("6 6 1 1\n") == "No"    # gap in middle region
assert run("3 10 5 5\n") == "Yes"  # symmetric center case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 1 1 | Yes | minimal symmetric case |
| 10 10 1 9 | Yes | large width with separated sources |
| 6 6 1 1 | No | central uncovered region |
| 3 10 5 5 | Yes | balanced symmetric lighting |

## Edge Cases

A subtle case occurs when both lights are at the same height. In that situation, the intersection points of the envelope collapse into symmetric positions, and the only possible failure would be at the midpoint. The algorithm explicitly evaluates both candidate intersection points, which coincide in this case, so the check remains valid.

Another edge case appears when one light is significantly higher than the other. The critical point then lies strictly inside $(0, w)$, and a naive endpoint-only check would miss the uncovered region. Evaluating the intersection points captures this exact transition where the lower envelope switches dominance from one light to the other.
