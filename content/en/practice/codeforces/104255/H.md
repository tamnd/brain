---
title: "CF 104255H - Birthday"
description: "We are given a convex polygon with $n$ vertices. The only allowed operation is drawing a diagonal between two existing vertices. Each diagonal splits one polygonal region into two smaller regions."
date: "2026-07-01T21:53:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104255
codeforces_index: "H"
codeforces_contest_name: "BSUIR Open X. Reload. Students final"
rating: 0
weight: 104255
solve_time_s: 94
verified: false
draft: false
---

[CF 104255H - Birthday](https://codeforces.com/problemset/problem/104255/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a convex polygon with $n$ vertices. The only allowed operation is drawing a diagonal between two existing vertices. Each diagonal splits one polygonal region into two smaller regions. The goal is to continue adding diagonals until every resulting region is a triangle, and we want to minimize how many diagonals are used.

A useful way to rephrase the task is that we are triangulating a convex polygon. Each cut increases the number of pieces, and we want to reach a full decomposition into triangles with as few cuts as possible.

The input size is small, $n \le 100$, so any quadratic or cubic reasoning over vertices is completely safe. This immediately suggests that the answer is likely a known closed-form or a simple combinatorial property rather than a dynamic programming over states that depends on geometry.

A subtle point is that “cutting along diagonals” implies each cut is a straight line between two vertices, and a single diagonal is the only operation. There is no restriction about crossing diagonals, but in a convex polygon, optimal triangulations never require crossings anyway.

There are no tricky corner cases beyond the smallest valid polygon. For $n = 4$, we have a quadrilateral, and one diagonal produces exactly two triangles. For larger $n$, the structure scales regularly.

## Approaches

A direct but overly literal approach is to simulate the process of cutting the polygon into triangles by repeatedly choosing diagonals. At each step, we could try all valid diagonals, apply one, recursively solve the resulting sub-polygons, and minimize the number of cuts.

This brute-force view quickly becomes a problem of enumerating triangulations. A convex polygon with $n$ vertices has Catalan-number many triangulations, which grows roughly like $O(4^n / n^{3/2})$. Even for $n = 50$, this is already far beyond any computational limit, so exhaustive search is impossible.

The key observation is that we are not asked to optimize over different triangulations, but only to count how many diagonals are needed in any valid triangulation. This removes all combinatorial complexity: every triangulation of a convex $n$-gon uses the same number of diagonals.

To see why, consider what a triangulation produces. A convex $n$-gon is partitioned into triangles, and each triangle has three edges. In a triangulation, every added diagonal contributes exactly one internal edge, and the final structure is a planar graph where all faces are triangles.

There is a standard structural fact: any triangulation of a convex $n$-gon always produces exactly $n - 2$ triangles. Since the original polygon has $n$ vertices, the triangulation always splits it into $n - 2$ triangular faces. Each diagonal increases the number of faces by exactly one. Starting from 1 face (the original polygon), reaching $n - 2$ faces requires exactly $n - 3$ cuts.

This makes the answer independent of geometry or strategy. Any sequence of valid diagonal cuts that fully triangulates the polygon must use exactly $n - 3$ diagonals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force triangulation search | Exponential | O(n) | Too slow |
| Formula $n - 3$ | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$, representing the number of vertices of the convex polygon.
2. Recognize that each diagonal cut splits one region into two, increasing the number of regions by exactly one.
3. Start from one region (the original polygon).
4. A full triangulation produces $n - 2$ triangular regions.
5. Each cut increases region count by one, so the number of cuts is exactly the number of times we need to go from 1 region to $n - 2$ regions.
6. Compute the answer as $n - 3$ and output it.

### Why it works

The invariant is the relationship between faces and cuts in a planar subdivision of a convex polygon. Initially there is one face. Each diagonal insertion splits exactly one existing face into two, increasing the face count by one. Since every valid triangulation must end with exactly $n - 2$ triangular faces, the total number of required splits is fixed as $n - 3$, independent of how diagonals are chosen. No sequence of valid diagonal insertions can change this count.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
print(n - 3)
```

The solution reads the number of vertices and directly applies the derived formula. There is no need to simulate geometry or maintain any structure because the final count depends only on the invariant relationship between vertices, triangles, and diagonals in any triangulation.

The only implementation detail to be careful about is stripping the input line, since competitive programming inputs often include trailing newlines.

## Worked Examples

### Example 1

Input:

```
5
```

A convex pentagon must be split into triangles. The algorithm computes $5 - 3 = 2$.

| Step | n | Computation | Result |
| --- | --- | --- | --- |
| Read input | 5 | - | - |
| Apply formula | 5 | 5 - 3 | 2 |

This confirms that a pentagon requires exactly two diagonals to fully triangulate.

### Example 2

Input:

```
8
```

For an octagon, the same invariant applies.

| Step | n | Computation | Result |
| --- | --- | --- | --- |
| Read input | 8 | - | - |
| Apply formula | 8 | 8 - 3 | 5 |

The output is 5, meaning five diagonals are needed to partition the octagon into six triangles.

This trace shows that even as the polygon grows, the process depends only on vertex count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single arithmetic operation after reading input |
| Space | O(1) | No additional data structures are used |

The input constraint $n \le 100$ is far beyond what this solution requires. The computation is constant time and trivially fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline().strip())
    return str(n - 3)

# provided samples
assert run("5\n") == "2", "sample 1"
assert run("8\n") == "5", "sample 2"

# custom cases
assert run("4\n") == "1", "minimum valid polygon"
assert run("6\n") == "3", "hexagon case"
assert run("100\n") == "97", "maximum n boundary"
assert run("7\n") == "4", "odd n sanity check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 | 1 | smallest polygon (quadrilateral) |
| 6 | 3 | simple convex polygon scaling |
| 100 | 97 | upper bound correctness |
| 7 | 4 | general consistency |

## Edge Cases

For $n = 4$, the algorithm computes $4 - 3 = 1$. A quadrilateral is already almost triangulated, and exactly one diagonal is required, matching the geometric reality.

For larger $n$, such as $n = 5$, the algorithm returns 2. If we explicitly draw diagonals in a pentagon, any valid triangulation produces exactly three triangles and thus exactly two diagonals. The formula correctly matches this structure without depending on which diagonals are chosen.

For the maximum case $n = 100$, the computation remains stable and direct. There is no accumulation of error or state dependence, since the formula is purely arithmetic and derived from invariant face counting.
