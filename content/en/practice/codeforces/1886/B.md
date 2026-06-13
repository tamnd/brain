---
title: "CF 1886B - Fear of the Dark"
description: "Monocarp starts at the origin $(0,0)$ and wants to reach his home at point $P$. The only illuminated regions come from two lanterns located at points $A$ and $B$. Both lanterns must use the same power $w$, which means each lantern illuminates a disk of radius $w$."
date: "2026-06-08T22:15:18+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1886
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 156 (Rated for Div. 2)"
rating: 1200
weight: 1886
solve_time_s: 131
verified: true
draft: false
---

[CF 1886B - Fear of the Dark](https://codeforces.com/problemset/problem/1886/B)

**Rating:** 1200  
**Tags:** binary search, geometry, math  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

Monocarp starts at the origin $(0,0)$ and wants to reach his home at point $P$. The only illuminated regions come from two lanterns located at points $A$ and $B$. Both lanterns must use the same power $w$, which means each lantern illuminates a disk of radius $w$.

We need the smallest value of $w$ such that there exists a continuous path from the origin to the house that never leaves the illuminated area.

The illuminated area is simply the union of two circles of equal radius $w$. A valid path exists if both endpoints, the origin and the house, belong to the same connected illuminated component.

The coordinates are at most $1000$ in magnitude, and there are up to $10^4$ test cases. Any solution doing substantial work per test case would be wasteful. Since there are only four relevant points, $O$, $P$, $A$, and $B$, we should expect a constant-time geometric solution.

Several situations are easy to overlook.

Suppose both the origin and the house are covered by the same lantern. For example:

```
P=(2,0)
A=(1,0)
B=(100,100)
```

The answer is simply the larger of $AO$ and $AP$. A solution that always tries to use both lanterns would overestimate the result.

Another tricky case occurs when the origin is covered by one lantern and the house by the other. Then the two illuminated circles must intersect or touch so that Monocarp can transfer from one illuminated region to the other. For example:

```
P=(10,0)
A=(0,0)
B=(10,0)
```

The minimum radius is $5$, not $0$. Each endpoint is already at a lantern center, but the circles must connect.

Touching counts as connected because circle boundaries are illuminated. If the distance between lantern centers is exactly $2w$, the circles meet at one point and a path still exists.

## Approaches

A natural first idea is binary search on the answer.

For a fixed radius $w$, we can check whether a valid illuminated path exists. The origin belongs to circle $A$ if $AO \le w$, and similarly for all other point-circle relationships. The two circles are connected whenever $AB \le 2w$. This creates a tiny graph consisting of the origin, the house, and the two circles. We can determine whether the origin and house lie in the same connected illuminated component.

The check takes constant time, and binary search over real numbers requires roughly sixty iterations to achieve far more precision than necessary. This already passes comfortably.

The key observation is that there are only two lanterns. Any valid path must fall into one of a very small number of configurations.

Either one lantern alone covers both endpoints, or the origin is covered by one lantern and the house by the other. There are no other possibilities.

If a single lantern covers both endpoints, the required radius is simply the maximum of its distances to the two endpoints.

If different lanterns are responsible for the two endpoints, then three conditions must hold simultaneously:

1. The first lantern covers its endpoint.
2. The second lantern covers its endpoint.
3. The two circles intersect.

The required radius is the maximum among those three requirements.

Since there are only two possible assignments of lanterns to endpoints, we can compute all candidates directly and take the minimum. This removes the need for binary search entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Binary Search + Feasibility Check | O(log precision) | O(1) | Accepted |
| Direct Geometric Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute all relevant distances:

- $AO, AP, BO, BP,$ and $AB$.
2. Consider the case where lantern $A$ alone covers both the origin and the house.

The required radius is:

$$\max(AO, AP)$$
3. Consider the case where lantern $B$ alone covers both the origin and the house.

The required radius is:

$$\max(BO, BP)$$
4. Consider the case where the origin is covered by lantern $A$ and the house by lantern $B$.

The origin requires $AO \le w$, the house requires $BP \le w$, and the circles must intersect, which requires:

$$AB \le 2w$$

Hence:

$$w=\max\left(AO,\ BP,\ \frac{AB}{2}\right)$$
5. Consider the symmetric assignment where the origin is covered by lantern $B$ and the house by lantern $A$.

The required radius is:

$$w=\max\left(BO,\ AP,\ \frac{AB}{2}\right)$$
6. The answer is the minimum among the four candidate radii.

### Why it works

The illuminated region is the union of exactly two disks. Any path from the origin to the house must start in a disk containing the origin and end in a disk containing the house.

If both endpoints lie in the same disk, that disk alone provides a connected illuminated route. This yields the first two candidates.

Otherwise, the origin and house must lie in different disks. Since only two disks exist, Monocarp must move from one disk to the other. That is possible exactly when the disks intersect or touch. The radius must simultaneously satisfy the coverage requirements for the two endpoints and the intersection requirement. This yields the remaining two candidates.

Every possible valid configuration belongs to one of these four cases, and each candidate is the smallest radius that makes its case feasible. Taking the minimum over all cases gives the global optimum.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def dist(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

t = int(input())

for _ in range(t):
    px, py = map(int, input().split())
    ax, ay = map(int, input().split())
    bx, by = map(int, input().split())

    ao = dist(ax, ay, 0, 0)
    ap = dist(ax, ay, px, py)

    bo = dist(bx, by, 0, 0)
    bp = dist(bx, by, px, py)

    ab = dist(ax, ay, bx, by)

    ans = min(
        max(ao, ap),
        max(bo, bp),
        max(ao, bp, ab / 2.0),
        max(bo, ap, ab / 2.0),
    )

    print(f"{ans:.10f}")
```

The first part computes the five distances that completely describe the geometry relevant to the problem.

The next four expressions correspond exactly to the four possible connectivity patterns discussed in the proof.

The subtle point is the appearance of `ab / 2.0`. Two circles of equal radius $w$ intersect when $AB \le 2w$, which is equivalent to $w \ge AB/2$. Forgetting this factor of two is the most common mistake.

Using `math.hypot` avoids manually squaring and taking square roots, while remaining numerically stable.

Printing ten decimal places easily satisfies the required $10^{-6}$ precision.

## Worked Examples

### Sample 1, Test Case 1

```
P = (3,3)
A = (1,0)
B = (-1,6)
```

| Quantity | Value |
| --- | --- |
| AO | 1.000000 |
| AP | 3.605551 |
| BO | 6.082763 |
| BP | 5.000000 |
| AB | 6.324555 |
| max(AO, AP) | 3.605551 |
| max(BO, BP) | 6.082763 |
| max(AO, BP, AB/2) | 5.000000 |
| max(BO, AP, AB/2) | 6.082763 |

Answer:

$$\min(3.605551, 6.082763, 5.000000, 6.082763) = 3.605551$$

The optimal solution uses lantern $A$ alone. It already covers both endpoints.

### Sample 1, Test Case 2

```
P = (3,3)
A = (-1,-1)
B = (4,3)
```

| Quantity | Value |
| --- | --- |
| AO | 1.414214 |
| AP | 5.656854 |
| BO | 5.000000 |
| BP | 1.000000 |
| AB | 6.403124 |
| max(AO, AP) | 5.656854 |
| max(BO, BP) | 5.000000 |
| max(AO, BP, AB/2) | 3.201562 |
| max(BO, AP, AB/2) | 5.656854 |

Answer:

$$\min(5.656854, 5.000000, 3.201562, 5.656854) = 3.201562$$

Here the origin is covered by lantern $A$, the house by lantern $B$, and the circles meet exactly when the radius reaches $AB/2$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of distance calculations and comparisons |
| Space | O(1) | No auxiliary data structures are used |

Each test case performs a constant amount of geometric computation. Even with $10^4$ test cases, the running time is negligible and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys
import math

def solve():
    input = sys.stdin.readline

    def dist(x1, y1, x2, y2):
        return math.hypot(x1 - x2, y1 - y2)

    t = int(input())
    out = []

    for _ in range(t):
        px, py = map(int, input().split())
        ax, ay = map(int, input().split())
        bx, by = map(int, input().split())

        ao = dist(ax, ay, 0, 0)
        ap = dist(ax, ay, px, py)
        bo = dist(bx, by, 0, 0)
        bp = dist(bx, by, px, py)
        ab = dist(ax, ay, bx, by)

        ans = min(
            max(ao, ap),
            max(bo, bp),
            max(ao, bp, ab / 2.0),
            max(bo, ap, ab / 2.0),
        )

        out.append(f"{ans:.10f}")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# provided sample
out = run(
"""2
3 3
1 0
-1 6
3 3
-1 -1
4 3
"""
).strip().splitlines()

assert abs(float(out[0]) - 3.6055512755) < 1e-6
assert abs(float(out[1]) - 3.2015621187) < 1e-6

# single lantern A covers everything
out = float(run(
"""1
2 0
1 0
100 100
"""
).strip())
assert abs(out - 1.0) < 1e-6

# symmetric transfer through touching circles
out = float(run(
"""1
10 0
0 0
10 0
"""
).strip())
assert abs(out - 5.0) < 1e-6

# choose lantern B alone
out = float(run(
"""1
1 1
100 100
0 1
"""
).strip())
assert abs(out - 1.0 < 1e-6)

# negative coordinates
out = float(run(
"""1
-3 -4
-1 0
-4 -3
"""
).strip())
assert out > 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| House near lantern A, lantern B far away | 1.0 | Single-lantern solution |
| Lanterns at endpoints of a segment | 5.0 | Circle-intersection requirement |
| Lantern B covers both endpoints | 1.0 | Symmetry between A and B |
| Negative coordinates | Positive finite answer | Distance computations in all quadrants |

## Edge Cases

### One lantern alone is sufficient

Input:

```
1
2 0
1 0
100 100
```

Distances are:

```
AO = 1
AP = 1
```

Lantern $A$ covers both endpoints with radius $1$. The algorithm computes `max(AO, AP)=1` and returns it. Any approach forcing both lanterns to participate would produce a larger answer.

### Different lanterns cover the two endpoints

Input:

```
1
10 0
0 0
10 0
```

The origin lies at lantern $A$'s center and the house lies at lantern $B$'s center. Coverage alone suggests radius $0$, but the illuminated regions would be disconnected.

The algorithm also checks $AB/2 = 5$, producing:

```
max(AO, BP, AB/2) = 5
```

which is the true minimum radius.

### Circles only touch

Input:

```
1
4 0
0 0
4 0
```

The optimal radius is $2$.

The circles meet at exactly one point because:

$$AB = 4 = 2 \times 2$$

Touching is enough since boundaries are illuminated. The formula naturally handles this because it uses the non-strict condition $AB \le 2w$.

### Symmetric assignments

Input:

```
1
3 3
4 3
-1 -1
```

This is the second sample with lantern labels swapped.

The algorithm evaluates both mixed assignments:

$$\max(AO, BP, AB/2)$$

and

$$\max(BO, AP, AB/2)$$

so it remains correct regardless of which lantern covers the origin and which covers the house.
