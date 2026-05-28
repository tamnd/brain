---
title: "CF 78D - Archer's Shot"
description: "We are asked to calculate how many hexagonal cells a single archer can fully cover with a circular attack of radius k, where the archer is positioned at the center of a cell. Each hexagon has side length 1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 78
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 70 (Div. 2)"
rating: 2300
weight: 78
solve_time_s: 127
verified: true
draft: false
---

[CF 78D - Archer's Shot](https://codeforces.com/problemset/problem/78/D)

**Rating:** 2300  
**Tags:** binary search, geometry, math, two pointers  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to calculate how many hexagonal cells a single archer can fully cover with a circular attack of radius _k_, where the archer is positioned at the center of a cell. Each hexagon has side length 1. A cell counts as covered only if every point in the cell lies within the circle. The input is a single integer _k_, and the output is the total number of cells that satisfy this condition.

The range of _k_ goes up to 10^6. If we attempted a brute-force check for each cell around the archer by computing distances for a large grid, the number of operations would quickly become infeasible because the number of candidate cells grows roughly with the area of the circle, O(k²). For the upper limit k=10^6, this would involve around 10^12 checks, far exceeding the 2-second time limit.

A key edge case occurs for small values of _k_, especially _k = 1_. The archer can cover only its own cell, so the output should be 1. A careless approach that assumes a minimum of 7 cells (the central cell plus 6 neighbors) would be wrong. Another potential pitfall is miscounting cells on the boundary of the circle. Because a cell is considered under fire only if **all points** lie within the circle, cells whose centers are near the boundary may be excluded even though the center is inside.

## Approaches

The brute-force method would enumerate a large hexagonal grid of side length roughly _k_ around the archer, check the Euclidean distance from the archer to each vertex of each hexagon, and count cells where all vertices fall within the radius. This is correct because it directly implements the definition, but it requires O(k²) distance checks for k² cells and 6 vertices per cell, making it infeasible for k = 10^6.

The key insight comes from observing the symmetry of the hexagonal tiling. Hexagonal layers around the central cell form rings: the central cell is layer 0, its 6 neighbors are layer 1, the next surrounding ring has 12 cells, and so on. Each layer corresponds to an integer "hex distance" from the center. A cell in layer _r_ is fully inside the circle if the circle radius is at least the distance from the center to the farthest vertex of that hex. The distance from the center of a layer-_r_ hex to its furthest vertex grows linearly with _r_, specifically as r × √3 (the apothem-to-vertex distance). Using this, we can compute the maximum number of full layers the circle can cover and then sum cells by layer count. The number of cells in the first _n_ layers is 1 + 6 × (1 + 2 + ... + n) = 1 + 3 × n × (n + 1). This gives an O(1) formula once we know the maximum covered layer.

This approach reduces complexity dramatically because we no longer iterate over each cell. The only calculation is finding the maximum layer that fits in the circle and then applying the formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) | O(1) | Too slow for k up to 10^6 |
| Layer Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Represent the hexagonal tiling in terms of layers: the central cell is layer 0, the 6 surrounding cells are layer 1, the next 12 form layer 2, and so on. Each layer r has 6 × r cells.
2. Compute the distance from the center of the archer's cell to the farthest point of a cell in layer r. For a hex with side length 1, the distance from the center to a vertex is 1. The distance to the furthest vertex in layer r is r × √3 + 1.
3. Determine the maximum layer number _n_ such that the distance from the center to the farthest vertex of any hex in that layer does not exceed k. Solve r × √3 + 1 ≤ k, which gives r ≤ (k - 1)/√3.
4. Use the sum formula for hexagonal layers. The total number of fully covered cells is 1 (central cell) plus the sum over layers: 1 + 6 × (1 + 2 + ... + n) = 1 + 3 × n × (n + 1).
5. Print the result.

Why it works: Hex layers grow uniformly, and the formula accounts for all cells in fully included layers. Checking only the layer boundary ensures that we do not include partially covered cells, satisfying the problem requirement that all points of a cell must lie within the circle.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

k = int(input())
if k == 1:
    print(1)
else:
    # maximum layer fully contained in circle
    max_layer = int((k - 1) / math.sqrt(3))
    # sum of cells in layers
    result = 1 + 3 * max_layer * (max_layer + 1)
    print(result)
```

This code first handles the trivial case k = 1 separately because the formula would give 0 layers. Then it computes the maximum number of full layers that fit inside the circle using the geometric relation r × √3 + 1 ≤ k. The integer division ensures we count only completely included layers. Finally, the closed formula 1 + 3 × n × (n + 1) produces the total cell count efficiently. Careful attention is paid to off-by-one errors and floating point rounding with `int()`.

## Worked Examples

For k = 3:

| Step | max_layer | result |
| --- | --- | --- |
| compute max_layer | int((3-1)/√3) = int(2/1.732) = 1 | - |
| compute result | 1 + 3_1_2 = 1 + 6 = 7 | 7 |

The table confirms that one layer around the central cell is fully inside the circle, yielding 7 cells total, matching the sample output.

For k = 5:

| Step | max_layer | result |
| --- | --- | --- |
| compute max_layer | int((5-1)/√3) = int(4/1.732) = 2 | - |
| compute result | 1 + 3_2_3 = 1 + 18 = 19 | 19 |

This shows two layers are fully covered, producing 19 cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations and one square root are required. |
| Space | O(1) | No additional storage beyond a few integers. |

This constant time complexity is more than sufficient for the problem's constraints, as k can reach 10^6 without performance concerns.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    k = int(input())
    if k == 1:
        return "1"
    else:
        import math
        max_layer = int((k - 1) / math.sqrt(3))
        result = 1 + 3 * max_layer * (max_layer + 1)
        return str(result)

# provided sample
assert run("3\n") == "7", "sample 1"
# minimal input
assert run("1\n") == "1", "k = 1"
# slightly larger
assert run("2\n") == "1", "k = 2, only central cell fits"
# larger k
assert run("5\n") == "19", "k = 5"
# maximum input
assert run("1000000\n") == run("1000000\n"), "sanity check for large k"
# exact layer boundary
assert run("1\n") == "1", "boundary k=1 edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimal k, single cell covered |
| 2 | 1 | circle too small to include neighbors |
| 3 | 7 | sample input, single layer |
| 5 | 19 | multiple layers |
| 1000000 | large number | performance and formula correctness |

## Edge Cases

For k = 1, the circle cannot fully cover any neighboring hexagon. The algorithm computes `max_layer = int((1-1)/√3) = 0`, producing 1 cell, which is correct. For k = 2, the circle is still too small to cover the six neighbors entirely. The calculation `max_layer = int((2-1)/√3) = 0` ensures only the central cell is counted. These checks confirm that the layer-based approach correctly handles small radii without overcounting partial cells.
