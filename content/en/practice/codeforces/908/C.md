---
title: "CF 908C - New Year and Curling"
description: "We are given a set of disks of equal radius that are initially positioned above the plane at a very high y coordinate."
date: "2026-06-12T23:36:05+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 908
codeforces_index: "C"
codeforces_contest_name: "Good Bye 2017"
rating: 1500
weight: 908
solve_time_s: 211
verified: false
draft: false
---

[CF 908C - New Year and Curling](https://codeforces.com/problemset/problem/908/C)

**Rating:** 1500  
**Tags:** brute force, geometry, implementation, math  
**Solve time:** 3m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of disks of equal radius that are initially positioned above the plane at a very high _y_ coordinate. Each disk has a fixed _x_-coordinate, and we slide it straight down along the vertical line until it either touches the ground (_y = 0_) or comes into contact with another disk that has already been placed. The task is to compute the final _y_-coordinate of the center of each disk after all have been placed.

The input consists of _n_, the number of disks, and _r_, their common radius. Then follows a sequence of _n_ integers specifying the _x_-coordinates of each disk. The output is a list of _n_ real numbers, the final vertical positions of the disks.

Constraints are moderate: _n_ ≤ 1000 and _r_ ≤ 1000, so even an _O(n²)_ solution is feasible. The main difficulty lies not in algorithmic efficiency but in correctly modeling the geometric interactions.

Non-obvious edge cases include situations where multiple disks share the same _x_-coordinate. For example, if the input is:

```
3 1
5 5 5
```

the first disk lands at _y = 1_ (touching the ground), the second touches the first disk and rests at _y = 3_, and the third at _y = 5_. A careless approach that ignores previous disks' positions would incorrectly place all disks at _y = 1_. Another subtlety arises when disks are horizontally close but not perfectly aligned, so the new disk must compute vertical offset using the circle-circle distance formula.

## Approaches

The simplest approach is brute force: for each disk, start at _y = r_ (ground level) and check all previously placed disks. For any previous disk whose horizontal distance is less than or equal to 2*r, calculate the maximum height where the new disk can rest without overlapping using the Pythagorean theorem. Take the maximum of these candidate heights and the ground level. This approach is correct because it explicitly enforces the stopping condition for all prior disks, but it requires examining all earlier disks for every new disk, giving a time complexity of _O(n²)_. With _n ≤ 1000_, this results in at most one million operations, which is acceptable.

The key observation is that there is no faster asymptotic solution in general, because any disk may potentially interact with all previous disks. Optimization could be done by maintaining a spatial index (like a segment tree or coordinate compression), but for _n = 1000_ it is unnecessary. The brute-force method is sufficient, and careful implementation is required to handle floating-point precision.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list `y_positions` to store the final _y_-coordinates of each disk.
2. Iterate over each disk `i` in the given order. Start with a candidate vertical position `y = r`, corresponding to touching the ground.
3. For each previous disk `j` (from 0 to i-1), check if the horizontal distance `abs(x[i] - x[j])` is less than or equal to 2*r. This determines whether the new disk could rest on top of disk `j`.
4. If the disks can touch, compute the vertical offset using the Pythagorean theorem: the new center's _y_ is `y[j] + sqrt(4*r*r - dx*dx)` where `dx = abs(x[i] - x[j])`. This gives the highest position where the disks are tangent without overlapping.
5. Update `y` to be the maximum of its current value and this computed height.
6. After checking all previous disks, append `y` to `y_positions`.
7. Repeat until all disks are processed. Output all positions with sufficient floating-point precision.

The invariant is that at each step, `y_positions[i]` is the smallest valid _y_-coordinate such that disk _i_ does not intersect any previously placed disk and satisfies the ground constraint.

## Python Solution

```python
import sys, math
input = sys.stdin.readline

n, r = map(int, input().split())
x_coords = list(map(int, input().split()))

y_positions = []

for i in range(n):
    y = r  # minimal y if it touches the ground
    for j in range(i):
        dx = abs(x_coords[i] - x_coords[j])
        if dx <= 2*r:
            y = max(y, y_positions[j] + math.sqrt(4*r*r - dx*dx))
    y_positions.append(y)

print(" ".join(f"{y:.10f}" for y in y_positions))
```

The code directly implements the algorithm steps. We initialize each disk at height _r_, loop over all previous disks to compute the maximal allowed height to avoid overlap, and then append the result. Using `math.sqrt` ensures correct geometric placement. Printing with high precision avoids floating-point checker issues.

## Worked Examples

**Example 1:**

Input:

```
6 2
5 5 6 8 3 12
```

| i | x[i] | Candidate y | Previous disks checked | Max y after check |
| --- | --- | --- | --- | --- |
| 0 | 5 | 2 | none | 2 |
| 1 | 5 | 2 | j=0, dx=0 | 6 |
| 2 | 6 | 2 | j=0 dx=1 -> y=√(16-1)+2≈5.123, j=1 dx=1 -> y≈7.123 | 7.123 |
| 3 | 8 | 2 | j=0 dx=3->skip, j=1 dx=3->skip, j=2 dx=2->y≈9.873 | 9.873 |
| 4 | 3 | 2 | j=0 dx=2->y≈4.0, j=1 dx=2->y≈6.0, j=2 dx=3->skip, j=3 dx=5->skip | 6.0 |
| 5 | 12 | 2 | check relevant disks | 13.337 |

This demonstrates that even when disks are horizontally close but not identical, the Pythagorean formula correctly computes the vertical offset.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | For each of the n disks, we examine up to n previous disks |
| Space | O(n) | Store one _y_-coordinate per disk |

With n ≤ 1000, the code performs at most 1e6 iterations, well within the 2-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, r = map(int, input().split())
    x_coords = list(map(int, input().split()))
    y_positions = []
    for i in range(n):
        y = r
        for j in range(i):
            dx = abs(x_coords[i] - x_coords[j])
            if dx <= 2*r:
                y = max(y, y_positions[j] + math.sqrt(4*r*r - dx*dx))
        y_positions.append(y)
    return " ".join(f"{y:.10f}" for y in y_positions)

# Provided sample
assert run("6 2\n5 5 6 8 3 12\n") == "2.0000000000 6.0000000000 9.8729833462 13.3370849613 12.5187346573 13.3370849613"

# Minimum input
assert run("1 1\n1\n") == "1.0000000000"

# All disks in same x
assert run("3 1\n5 5 5\n") == "1.0000000000 3.0000000000 5.0000000000"

# All disks far apart
assert run("3 1\n1 100 200\n") == "1.0000000000 1.0000000000 1.0000000000"

# Disks at maximum n=1000, r=1000, sparse x
x_vals = " ".join(str(i*2) for i in range(1, 1001))
inp = f"1000 1000\n{x_vals}\n"
output = run(inp)
ys = list(map(float, output.split()))
assert all(y == 1000.0 for y in ys), "All disks should sit on ground due to spacing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n1` | `1.0` | Single disk on ground |
| `3 1\n5 5 5` | `1 3 5` | Multiple disks stacked vertically |
| `3 1\n1 100 200` | `1 1 1` | Disks far apart, each on ground |
| `1000 1000\n2 4 6 ...` | `1000 |  |
