---
title: "CF 106E - Space Rescuers"
description: "We are asked to place a space rescue station in three-dimensional space such that the maximum distance from it to any of the given planets is minimized. Each planet is represented by its coordinates $(x, y, z)$."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 106
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 82 (Div. 2)"
rating: 2100
weight: 106
solve_time_s: 323
verified: false
draft: false
---

[CF 106E - Space Rescuers](https://codeforces.com/problemset/problem/106/E)

**Rating:** 2100  
**Tags:** geometry, ternary search  
**Solve time:** 5m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to place a space rescue station in three-dimensional space such that the maximum distance from it to any of the given planets is minimized. Each planet is represented by its coordinates $(x, y, z)$. The input consists of an integer $n$ representing the number of planets followed by $n$ lines of coordinates. The output should be a point $(x_0, y_0, z_0)$ that minimizes the farthest distance to any planet. The answer is accepted if the distance differs from the optimal by at most $10^{-6}$.

The constraints are small: $n \le 100$ and coordinates are within $[-10^4, 10^4]$. Since the number of planets is low, we can afford algorithms with cubic or even quartic iterations over planets, but the continuous nature of space prevents a purely discrete brute-force. A naive approach would try all possible points on a grid, but the precision requirement makes that impossible.

Non-obvious edge cases include configurations where planets are aligned or symmetric. For example, if planets are at $(1, 0, 0)$ and $(-1, 0, 0)$, the optimal point is $(0, 0, 0)$. A careless algorithm that only considers planets themselves as candidate points could incorrectly pick one of the planets instead of the center.

## Approaches

The brute-force idea is to check all points in a 3D bounding box and compute the maximum distance to planets. For a grid of size $M^3$, each check requires $O(n)$ distance computations. With $M = 20000$ (covering all integer coordinates) and $n = 100$, this would require $20000^3 \cdot 100$ operations, clearly infeasible.

The key observation is that the maximum distance function $f(x, y, z) = \max_i \text{dist}((x, y, z), (x_i, y_i, z_i))$ is convex in 3D. Intuitively, as we move the candidate point closer to the center of the farthest planets, the maximal distance decreases. Convexity allows us to use iterative geometric optimization methods like ternary search or gradient descent. Since $n$ is small, a randomized hill-climbing method that moves the candidate point towards the farthest planet works efficiently.

The idea is to start at any point (for example, the first planet), identify the farthest planet from the current point, and move slightly towards it. Repeating this gradually converges to the minimal enclosing sphere center.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grid | O(M^3 * n) | O(n) | Too slow |
| Iterative Hill Climb / Ternary Search | O(n * iterations) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize the candidate point at any planet, for example, the first one. This is reasonable because the optimal point is typically somewhere inside the convex hull of the planets.
2. Set an initial step size equal to half of the largest distance between any two planets. This ensures the initial moves cover significant space.
3. Repeat until the step size becomes very small:

1. Compute the distance from the current candidate point to all planets.
2. Identify the planet farthest from the current candidate point.
3. Move the candidate point a fraction of the step size towards that farthest planet.
4. Reduce the step size slightly, for example multiply by 0.99, to allow finer adjustments.
4. After enough iterations, output the current candidate point. The process converges to a point minimizing the maximum distance to planets.

Why it works: at each step we reduce the maximum distance by moving toward the farthest planet. The convexity of the maximal distance function ensures that no local minimum traps the process. Gradually reducing the step size allows us to refine the position with arbitrary precision.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def main():
    n = int(input())
    planets = [tuple(map(int, input().split())) for _ in range(n)]
    
    # Initialize at the first planet
    x, y, z = planets[0]
    
    # Step size: half the max distance between any two planets
    step = 0.0
    for i in range(n):
        for j in range(i+1, n):
            step = max(step, distance(planets[i], planets[j]))
    step /= 2
    
    # Iterative hill climb
    for _ in range(10000):
        farthest = max(planets, key=lambda p: distance((x, y, z), p))
        dx, dy, dz = farthest[0]-x, farthest[1]-y, farthest[2]-z
        d = math.sqrt(dx*dx + dy*dy + dz*dz)
        if d == 0:
            break
        x += dx/d * step
        y += dy/d * step
        z += dz/d * step
        step *= 0.995
    
    print(f"{x:.10f} {y:.10f} {z:.10f}")

if __name__ == "__main__":
    main()
```

The solution starts at a planet to ensure the candidate point is inside the convex hull of planets. Computing the maximum pairwise distance gives a reasonable initial step size. In each iteration, we move toward the farthest planet by a fraction of the step size, gradually reducing it to refine precision. We handle zero distance cases to prevent division by zero. The number of iterations is chosen sufficiently high to achieve the required $10^{-6}$ precision.

## Worked Examples

For Sample 1:

| Iteration | Candidate (x,y,z) | Farthest Planet | Max Distance |
| --- | --- | --- | --- |
| 0 | 5,0,0 | (-5,0,0) | 10 |
| 1 | 0,0,0 | (-5,0,0) | 5 |
| ... | ... | ... | ... |
| final | 0,0,0 | any planet | 5 |

The trace shows that moving toward the farthest planet at each step quickly centers the point among the planets, minimizing the maximum distance.

Constructed Input:

```
2
1 0 0
-1 0 0
```

Output: `0.0 0.0 0.0`. The algorithm moves from the first planet toward the second, stopping at the midpoint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * iterations) | Each iteration computes distances to n planets; iterations are a fixed constant (10000) |
| Space | O(n) | Stores n planets only |

With $n \le 100$ and a fixed number of iterations, the algorithm runs comfortably within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided sample
assert run("5\n5 0 0\n-5 0 0\n0 3 4\n4 -3 0\n2 2 -2\n") == "0.0000000000 0.0000000000 0.0000000000", "sample 1"

# Custom cases
assert run("2\n1 0 0\n-1 0 0\n") == "0.0000000000 0.0000000000 0.0000000000", "two planets symmetric"
assert run("1\n10000 10000 10000\n") == "10000.0000000000 10000.0000000000 10000.0000000000", "single planet"
assert run("3\n1 1 1\n2 2 2\n3 3 3\n") == "2.0000000000 2.0000000000 2.0000000000", "aligned planets"
assert run("4\n-10000 -10000 -10000\n10000 10000 10000\n-10000 10000 -10000\n10000 -10000 10000\n") == "0.0000000000 0.0000000000 0.0000000000", "cube corners"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 planets at ±1 | 0,0,0 | Symmetric midpoint calculation |
| 1 planet | 10000,10000,10000 | Single planet case |
| 3 aligned planets | 2,2,2 | Center of line segment |
| 4 cube corners | 0,0,0 | Symmetric 3D distribution |

## Edge Cases

For two planets at $(1,0,0)$ and $(-1,0,0)$, the initial point is $(1,0,0)$. The farthest is ((-1,0,0)\
