---
title: "CF 144B - Meeting"
description: "We are asked to determine how many generals need warm blankets at a rectangular table placed on an infinite Cartesian plane. The table corners are given by two points with integer coordinates, and each integer point along the perimeter of the rectangle hosts a general."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 144
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 103 (Div. 2)"
rating: 1300
weight: 144
solve_time_s: 75
verified: true
draft: false
---

[CF 144B - Meeting](https://codeforces.com/problemset/problem/144/B)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine how many generals need warm blankets at a rectangular table placed on an infinite Cartesian plane. The table corners are given by two points with integer coordinates, and each integer point along the perimeter of the rectangle hosts a general. There are a number of radiators, each with a position and a heating radius. A general is comfortable if the Euclidean distance to at least one radiator is less than or equal to that radiator's radius. The output is the number of generals outside all radiator ranges.

The constraints are modest: the rectangle perimeter has at most a few thousand points because the coordinates are bounded by ±1000, and the number of radiators is up to 1000. This means that a brute-force check of each general against every radiator is feasible: $O(\text{generals} \times n)$ operations remain well below $10^7$, which comfortably fits a 2-second time limit.

Non-obvious edge cases include rectangles that are aligned with negative coordinates, rectangles with width or height equal to 1 (producing only a line of generals), and radiators located exactly at the general's position. For instance, if the rectangle is defined by (0,0) and (0,3) and there is a radiator at (0,1) with radius 0, only that point is heated; all others require blankets. A careless implementation might iterate incorrectly over the rectangle coordinates or check the heating condition with strict inequality, failing these cases.

## Approaches

The brute-force approach works by enumerating every perimeter point of the rectangle and checking the Euclidean distance to every radiator. For each general, we compute the distance to each radiator and compare it with the radiator's radius. If no radiator covers the general, we increment the blanket counter. This method is correct because it directly implements the problem description, but it requires $O(\text{perimeter} \times n)$ operations. With the maximal perimeter around 8000 points and 1000 radiators, this leads to roughly $8 \cdot 10^6$ distance checks, which is acceptable but might be slightly tight for the largest inputs.

No major optimization is necessary because the problem size is small, but one minor improvement is to precompute the squared radius and compare it with squared distances. This avoids expensive square root calculations, and since we only need to compare distances, the relative comparison remains correct. Other optimizations like spatial partitioning are overkill here.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(P × n), P = perimeter points | O(n) | Accepted |
| Optimal (distance squared) | O(P × n) | O(n) | Accepted |

The optimal approach is the same brute-force with squared distance comparison, which avoids floating-point operations and is slightly faster in practice.

## Algorithm Walkthrough

1. Parse the rectangle corners $(x_a, y_a)$ and $(x_b, y_b)$ and determine the minimum and maximum x and y coordinates to correctly iterate over the rectangle edges regardless of the input order.
2. Collect all radiator positions and their radii. For each radiator, precompute the squared radius $r_i^2$ to avoid square roots in distance checks.
3. Enumerate every integer point along the rectangle perimeter. Iterate over x coordinates for the top and bottom edges and over y coordinates for the left and right edges. Avoid double-counting the corners by carefully handling the edges.
4. For each perimeter point (general), initialize a flag `warm` as False. Iterate through all radiators, computing the squared Euclidean distance to the general. If any radiator satisfies $dx^2 + dy^2 \le r_i^2$, set `warm = True` and break.
5. After checking all radiators, if `warm` remains False, increment the blanket counter.
6. Output the total blanket count.

The correctness of the algorithm follows from checking each perimeter point against all radiators and using squared distances to ensure that no general is misclassified as warm or cold. Each perimeter point is processed exactly once, and the distance comparison is exact in integer arithmetic.

## Python Solution

```python
import sys
input = sys.stdin.readline

xa, ya, xb, yb = map(int, input().split())
n = int(input())
radiators = []
for _ in range(n):
    x, y, r = map(int, input().split())
    radiators.append((x, y, r*r))  # store squared radius

# normalize rectangle coordinates
x_min, x_max = min(xa, xb), max(xa, xb)
y_min, y_max = min(ya, yb), max(ya, yb)

blankets = 0

# generate perimeter points
for x in range(x_min, x_max+1):
    for y in [y_min, y_max]:
        warm = False
        for rx, ry, r2 in radiators:
            dx = x - rx
            dy = y - ry
            if dx*dx + dy*dy <= r2:
                warm = True
                break
        if not warm:
            blankets += 1

for y in range(y_min+1, y_max):  # avoid double-counting corners
    for x in [x_min, x_max]:
        warm = False
        for rx, ry, r2 in radiators:
            dx = x - rx
            dy = y - ry
            if dx*dx + dy*dy <= r2:
                warm = True
                break
        if not warm:
            blankets += 1

print(blankets)
```

The first loop handles the horizontal edges, while the second loop handles the vertical edges excluding the corners already counted. Storing squared radii avoids floating-point precision errors and improves performance. Each distance check uses integer arithmetic only.

## Worked Examples

**Sample 1**

Input rectangle: (2,5) to (4,2)

Radiators: (3,1,2), (5,3,1), (1,3,2)

| General | Distance squared to radiators | Warm? |
| --- | --- | --- |
| (2,2) | 2->10->2 | True |
| (2,3) | 5->5->0 | True |
| (2,4) | 10->5->2 | True |
| (2,5) | 18->5->8 | False |
| (3,2) | 1->4->4 | True |
| (3,5) | 10->4->8 | False |
| (4,2) | 2->1->8 | True |
| (4,3) | 5->1->2 | True |
| (4,4) | 10->1->5 | False |
| (4,5) | 18->1->10 | False |

Blankets required = 4, matching the expected output.

**Sample 2**

Input rectangle: (5,2) to (6,3)

Radiators: (5,2,1), (5,3,1), (6,2,1), (6,3,1)

All perimeter points coincide with radiator coverage, so blankets required = 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(P × n) | Each perimeter point is checked against all n radiators. P ≤ 4000 in the worst case. |
| Space | O(n) | Storing radiator coordinates and squared radii. |

The solution easily fits within the 2-second limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    xa, ya, xb, yb = map(int, input().split())
    n = int(input())
    radiators = []
    for _ in range(n):
        x, y, r = map(int, input().split())
        radiators.append((x, y, r*r))
    x_min, x_max = min(xa, xb), max(xa, xb)
    y_min, y_max = min(ya, yb), max(ya, yb)
    blankets = 0
    for x in range(x_min, x_max+1):
        for y in [y_min, y_max]:
            warm = False
            for rx, ry, r2 in radiators:
                dx = x - rx
                dy = y - ry
                if dx*dx + dy*dy <= r2:
                    warm = True
                    break
            if not warm:
                blankets += 1
    for y in range(y_min+1, y_max):
        for x in [x_min, x_max]:
            warm = False
            for rx, ry, r2 in radiators:
                dx = x - rx
                dy = y - ry
                if dx*dx + dy*dy <= r2:
                    warm = True
                    break
            if not warm:
                blankets += 1
    return str(blankets)

# provided samples
assert run("2 5 4 2\n3\n3 1 2\n5 3 1\n1 3 2\n") == "4", "sample 1"
assert run("5 2 6 3\n4\n5 2 1\n5 3 1\n6 2 1\n6 3 1\n") == "0", "sample 2"

# custom cases
assert run("0 0 0 0\n1
```
