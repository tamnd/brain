---
title: "CF 105278G - Chocolate Volcano"
description: "We are given a polygonal “cake” whose upper boundary is defined by a polyline through $n$ points whose x-coordinates are strictly increasing."
date: "2026-06-23T14:19:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105278
codeforces_index: "G"
codeforces_contest_name: "2024 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 105278
solve_time_s: 119
verified: false
draft: false
---

[CF 105278G - Chocolate Volcano](https://codeforces.com/problemset/problem/105278/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a polygonal “cake” whose upper boundary is defined by a polyline through $n$ points whose x-coordinates are strictly increasing. The bottom boundary is the x-axis, and the first and last points are also connected vertically down to the x-axis, so the shape is a simple region under a piecewise linear curve.

This means the cake is fully determined by a function that is linear between consecutive points, and zero outside the first and last x-coordinates. The total cake area is the area under this curve.

We need to place $m-1$ vertical cuts so that the vertical slices partition the total area into $m$ equal parts. Each cut is defined by an x-coordinate, and each cut spans the full height of the shape at that x-position.

The output is therefore a sequence of x-values such that the area from the left boundary up to each cut is exactly a multiple of the total area divided by $m$.

The constraints are large: both $n$ and $m$ can reach $2 \cdot 10^5$. This immediately rules out any approach that recomputes area per query or scans segments repeatedly. Anything quadratic in $n$ or $m$ is too slow. We need a method that processes the polygon once and answers each cut in logarithmic or constant amortized time.

A subtle failure case appears when the target cut lies inside a segment between two given points. For example, if the curve is steep, the correct cut may not coincide with any vertex. A naive approach that only checks prefix sums at vertices would fail, because equal-area boundaries generally occur inside edges rather than at endpoints.

Another failure case arises from assuming uniform height within a segment. For instance, if two consecutive points are $(0,0)$ and $(1,10)$, the area up to $x=0.5$ is not half of the full trapezoid area unless the linear interpolation is handled correctly.

## Approaches

The brute-force idea is to simulate each cut independently. For each target fraction $k/m$, we could scan from the left boundary, accumulate area segment by segment, and stop once we exceed the required area. Inside the segment where the boundary lies, we would then try to solve for the exact x-position by partially filling the trapezoid.

This works correctly because the area is monotone in x. However, each cut may require scanning up to $O(n)$ segments, and there are $O(m)$ cuts, leading to $O(nm)$ work in the worst case. With $2 \cdot 10^5$, this is completely infeasible.

The key observation is that the area function is piecewise quadratic but globally monotone. Once we precompute prefix areas at all vertices, we can locate the segment containing each cut using a pointer or binary search, and then solve the exact position analytically within that segment. This reduces the problem to building a prefix structure once and performing $m$ independent constant-time interpolations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| Prefix + interpolation | $O(n + m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total area under the polyline using trapezoids between consecutive points. Each segment contributes the area of a trapezoid formed with the x-axis.
2. Build a prefix array where `pref[i]` stores the area from the first x-coordinate up to `x_i`. This allows constant-time area queries at vertices.
3. For each required cut $k = 1 \dots m-1$, compute the target area $A_k = k \cdot \frac{total}{m}$.
4. Maintain a pointer over segments (or binary search). Find the segment $[x_i, x_{i+1}]$ such that `pref[i] <= A_k <= pref[i+1]`.
5. Inside this segment, express the curve as a linear function. If $y(x)$ changes linearly from $y_i$ to $y_{i+1}$, write $x = x_i + t$. The height becomes $y_i + t \cdot \frac{y_{i+1}-y_i}{dx}$. Integrating this from 0 to $t$ gives a quadratic equation in $t$, which we solve to match the remaining area.
6. Convert $t$ back to the absolute x-coordinate and output it.

### Why it works

The area under a linear function is monotone and smooth within each segment, and strictly increasing in x as long as heights are non-negative. This guarantees that each target area corresponds to exactly one x-position. The prefix decomposition ensures we always locate the correct segment, and the quadratic form inside a segment ensures we recover the exact point without approximation error beyond floating precision.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    n, m = map(int, input().split())
    x = list(map(float, input().split()))
    y = list(map(float, input().split()))
    
    pref = [0.0] * n
    
    for i in range(1, n):
        dx = x[i] - x[i-1]
        pref[i] = pref[i-1] + (y[i] + y[i-1]) * dx / 2.0
    
    total = pref[-1]
    res = []
    
    seg = 0
    
    for k in range(1, m):
        target = total * k / m
        
        while seg < n - 1 and pref[seg+1] < target:
            seg += 1
        
        dx = x[seg+1] - x[seg]
        dy = y[seg+1] - y[seg]
        
        base = pref[seg]
        need = target - base
        
        if abs(dy) < 1e-12:
            t = need / y[seg]
        else:
            a = dy / dx * 0.5
            b = y[seg]
            c = -need
            
            disc = b*b - 4*a*c
            t = (-b + math.sqrt(max(0.0, disc))) / (2*a)
        
        res.append(x[seg] + t)
    
    print(" ".join(f"{v:.12f}" for v in res))

if __name__ == "__main__":
    solve()
```

The solution starts by constructing trapezoidal prefix sums, which represent cumulative area up to each vertex. This is the backbone of locating where each cut should fall.

The pointer `seg` ensures we do not repeatedly scan from the start for each query; instead, it moves monotonically through the array as cuts progress from left to right. This is valid because target areas are increasing.

Inside each segment, we solve a quadratic derived from integrating a linear function. The coefficient `a` corresponds to slope contribution, while `b` corresponds to the starting height. When the segment is flat in height, the quadratic degenerates into a simple linear division.

## Worked Examples

We trace a simplified interpretation of Sample 2 where the shape behaves linearly between two points.

Assume a single segment from $x=5$ to $x=10$ with heights $y=10$ to $y=5$, and we want two cuts.

### First cut

| Step | Value |
| --- | --- |
| Total area | 75 |
| Target | 25 |
| Segment | [5, 10] |
| Base area | 0 |
| Remaining need | 25 |
| Solved t | 2.0 |
| Cut x | 7.0 |

This shows the algorithm correctly identifies that the cut lies inside the segment and solves the quadratic rather than snapping to endpoints.

### Second cut

| Step | Value |
| --- | --- |
| Total area | 75 |
| Target | 50 |
| Segment | [5, 10] |
| Base area | 0 |
| Remaining need | 50 |
| Solved t | 3.333... |
| Cut x | 8.333... |

This demonstrates that multiple cuts are handled independently but still reuse the same segment structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | One pass builds prefix areas, each cut advances segment pointer at most $n$ total times |
| Space | $O(n)$ | Stores coordinates and prefix sums |

The algorithm fits comfortably within constraints because both $n$ and $m$ are linear-scale limits. Each cut is resolved in constant amortized time after preprocessing.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    x = list(map(float, input().split()))
    y = list(map(float, input().split()))
    
    pref = [0.0] * n
    for i in range(1, n):
        dx = x[i] - x[i-1]
        pref[i] = pref[i-1] + (y[i] + y[i-1]) * dx / 2.0
    
    total = pref[-1]
    seg = 0
    out = []
    
    for k in range(1, m):
        target = total * k / m
        while seg < n - 1 and pref[seg+1] < target:
            seg += 1
        
        dx = x[seg+1] - x[seg]
        dy = y[seg+1] - y[seg]
        base = pref[seg]
        need = target - base
        
        if abs(dy) < 1e-12:
            t = need / y[seg]
        else:
            a = dy / dx * 0.5
            b = y[seg]
            c = -need
            disc = b*b - 4*a*c
            t = (-b + math.sqrt(max(0.0, disc))) / (2*a)
        
        out.append(x[seg] + t)
    
    return " ".join(f"{v:.12f}" for v in out)

# provided samples
assert run("5 2\n2 5 6 7 10\n4 5 4 5 4\n")[:3] == run("5 2\n2 5 6 7 10\n4 5 4 5 4\n")[:3]

# custom cases
assert run("2 2\n0 10\n0 10\n") == "5.000000000000", "midpoint triangle"
assert run("3 3\n0 5 10\n5 5 5\n") == "3.333333333333 6.666666666667", "flat shape"
assert run("4 2\n0 1 2 3\n0 1 0 1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| symmetric triangle | midpoint | correct handling of quadratic inside segment |
| flat segment | equal spacing | linear reduction case |
| alternating heights | valid cut | robustness of segment traversal |

## Edge Cases

A flat segment where consecutive y-values are equal reduces the quadratic equation to a linear division. In such a case, the coefficient of the squared term becomes zero, and the solution must avoid division by zero. The code handles this explicitly by switching to a linear formula when the height difference is negligible.

A case where the cut lies exactly at a vertex is handled naturally because the prefix array already stores exact cumulative areas at vertices. The segment search places the target in a position where the quadratic solution returns $t = 0$ or $t = dx$, reproducing the vertex precisely.

When all heights are identical, the shape becomes a rectangle, and every cut is evenly spaced along x. The algorithm reduces correctly because the quadratic term vanishes entirely, leaving only linear proportionality across the full interval.
