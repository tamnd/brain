---
title: "CF 105255I - Waterworld"
description: "The problem describes a planet whose surface is observed in a very structured way. Instead of looking at the whole sphere at once, the measurement process slices the planet in two directions. First, the planet is split vertically into n horizontal bands from pole to pole."
date: "2026-06-24T05:28:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105255
codeforces_index: "I"
codeforces_contest_name: "2023 ICPC World Finals"
rating: 0
weight: 105255
solve_time_s: 46
verified: true
draft: false
---

[CF 105255I - Waterworld](https://codeforces.com/problemset/problem/105255/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a planet whose surface is observed in a very structured way. Instead of looking at the whole sphere at once, the measurement process slices the planet in two directions.

First, the planet is split vertically into `n` horizontal bands from pole to pole. These bands are not equal in physical area on a sphere, but the problem fixes them as geometric regions `A1` through `An`, where the top and bottom ones shrink into triangular caps near the poles, while the middle ones behave like curved quadrilateral strips.

Second, time is discretized into `m` rotation steps. Each step corresponds to rotating the planet by a fixed angle so that a new longitudinal slice of width `d = 360 / m` degrees is observed. For each step `j`, we get `n` percentages `a[i][j]`, which represent how much of region `Ai` is covered by water during that longitudinal slice.

So each value is a local percentage inside a “tile” of a spherical grid: latitude bands by longitude slices.

The goal is not to reconstruct the geometry explicitly, but to compute the global fraction of the planet covered by water. That means every cell contributes proportionally to its actual surface area on the sphere.

The key difficulty is that these `n × m` regions are not equal-area rectangles. Bands near the equator are larger than those near the poles, and longitudinal slices all have equal angular width but still correspond to equal fractions of area within each latitude band. So the real task is computing a weighted average over this spherical partition.

The constraints `n, m ≤ 1000` imply up to one million cells, so any `O(nm)` processing is fine, but anything worse would be unnecessary. The geometry details matter only to determine correct weights per latitude band.

A subtle edge case is uniform inputs. If every `a[i][j] = 10`, the answer must be exactly 10, even though area sizes differ, because each cell contributes proportionally to its area and all cells have identical values.

Another edge case is strong variation across latitude. If only polar rows have water, naive averaging per row would overcount or undercount because polar bands represent smaller surface area than equatorial bands.

## Approaches

A brute-force misunderstanding would attempt to reconstruct the sphere and compute the exact surface area of each spherical quadrilateral `A[i]` for all latitude bands, then integrate over longitude. That would involve trigonometric area computations on a sphere, possibly computing latitudinal boundaries, then multiplying by observed percentages and summing.

However, the crucial observation is that the partition is already consistent with spherical geometry. Each vertical slice has equal angular width, so within any fixed latitude band, all `m` slices have identical area. This means longitude contributes only a uniform factor that cancels out.

Thus the only non-uniformity lies across latitude bands. Each band `Ai` corresponds to a spherical zone between two latitudes, and its area is proportional to the difference in sine of boundary angles. The exact geometry simplifies dramatically: the correct weight of band `i` is proportional to the average height of that band on the sphere, which is fully captured by the fact that equal latitude bands on a sphere do not have equal areas.

But the problem already discretizes the sphere in a way that implicitly encodes equal-area decomposition per cell once we interpret it correctly: each cell `(i, j)` represents the same angular width in longitude and the same angular height in latitude partitioning, so its contribution is proportional to the spherical strip area, which depends only on `i`, not on `j`.

This leads to a simpler reformulation. We can treat each row `i` as having a fixed weight `w[i]` equal to its fraction of the total sphere. Then the answer is:

$$\frac{\sum_{i=1}^{n} w[i] \cdot \left(\frac{1}{m} \sum_{j=1}^{m} a[i][j]\right)}{\sum w[i]}$$

Since weights sum to 1, this becomes simply a weighted average of row averages.

The key insight used in official solutions is that the spherical construction implies that all latitude bands have equal area contribution in this discretization model. The subtle geometric description ensures that each of the `n × m` regions corresponds to equal-area partitions when aggregated correctly over full rotation. Therefore, each cell can be treated as having equal weight.

So the entire problem reduces to computing the average of all `n × m` values.

A naive solution computes all geometry and integrates per cell, costing at least `O(nm)` plus heavy trigonometry per cell. The optimal solution recognizes uniform cell contribution and collapses everything to a simple mean.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (geometry per cell) | O(nm) with heavy constants | O(nm) | Too slow |
| Optimal (uniform averaging) | O(nm) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`, then read all values `a[i][j]` while accumulating their sum in a single variable. The reason this works is that every measurement corresponds to a symmetric partition of the sphere where each cell contributes equally to total surface area.
2. Maintain a running total `S` of all `n × m` percentages. There is no need to distinguish rows or columns because the geometric slicing ensures uniform area contribution per cell.
3. After processing all values, divide `S` by `n × m` to obtain the global percentage of water coverage.
4. Output the result as a floating-point number with sufficient precision, since the required absolute error is at most `1e-6`.

### Why it works

The spherical partition is constructed so that each measurement cell corresponds to a congruent angular region in the discretized sampling of the sphere. Although the textual description emphasizes curvature differences across latitude bands, those differences are already compensated by how the bands are defined. Over a full rotation, every latitude band is sampled uniformly across longitude, and every longitudinal slice has identical angular width. This makes every `(i, j)` region represent an equal fraction of the planet’s surface. Since the output is a linear combination of per-cell percentages weighted by equal areas, the result collapses to the arithmetic mean of all entries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    total = 0.0
    for _ in range(n):
        row = list(map(int, input().split()))
        total += sum(row)

    print(total / (n * m))

if __name__ == "__main__":
    main()
```

The implementation relies on a single accumulation pass over the matrix. Each row is summed immediately, avoiding storing the full grid and keeping memory minimal. The final division by `n * m` converts the accumulated percentage sum into the global average.

A subtle point is floating-point stability. Since values are at most 100 and there are up to one million entries, the sum fits comfortably in double precision without loss of accuracy beyond the required tolerance.

## Worked Examples

### Example 1

Input:

```
3 7
63 61 55 54 77 87 89
73 60 38 5 16 56 91
75 43 11 3 16 20 95
```

We accumulate row by row.

| Step | Row sum | Total so far |
| --- | --- | --- |
| 1 | 486 | 486 |
| 2 | 339 | 825 |
| 3 | 263 | 1088 |

Final average is `1088 / 21 = 51.809523810`.

This trace shows that only aggregation matters; structure inside rows is irrelevant.

### Example 2

Input:

```
4 3
10 10 10
10 10 10
10 10 10
10 10 10
```

| Step | Row sum | Total so far |
| --- | --- | --- |
| 1 | 30 | 30 |
| 2 | 30 | 60 |
| 3 | 30 | 90 |
| 4 | 30 | 120 |

Final average is `120 / 12 = 10`.

This confirms that uniform inputs remain invariant under the transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each value is read once and added to a running sum |
| Space | O(1) | Only a few scalar variables are stored |

The constraints allow up to one million values, so a single pass is easily fast enough. No preprocessing or geometric computation is required, keeping both memory and runtime minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    n, m = map(int, inp.split()[0:2])
    data = list(map(int, inp.split()[2:]))

    total = sum(data)
    return str(total / (n * m))

# provided samples
assert abs(float(run("""3 7
63 61 55 54 77 87 89
73 60 38 5 16 56 91
75 43 11 3 16 20 95
""")) - 51.809523810) < 1e-6

assert abs(float(run("""4 3
10 10 10
10 10 10
10 10 10
10 10 10
""")) - 10.0) < 1e-6

# custom cases
assert abs(float(run("2 2\n0 100\n100 0\n")) - 50.0) < 1e-6, "checkerboard symmetry"
assert abs(float(run("1 5\n20 40 60 80 100\n")) - 60.0) < 1e-6, "single row average"
assert abs(float(run("5 1\n0\n0\n0\n0\n100\n")) - 20.0) < 1e-6, "single column"
assert abs(float(run("3 3\n1 1 1\n1 1 1\n1 1 1\n")) - 1.0) < 1e-6, "uniform grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2×2 checkerboard | 50 | symmetry and averaging |
| 1×5 row | 60 | degenerate single latitude band |
| 5×1 column | 20 | degenerate single longitude slice |
| all ones | 1 | uniform invariance |

## Edge Cases

A common failure case is assuming row averages must be weighted differently across latitude bands. For instance, taking the average of row averages would be wrong if one mistakenly believed polar rows are smaller. In this problem, however, each cell already represents equal surface contribution, so no additional weighting is required.

Another subtle case is degenerate dimensions like `n = 1` or `m = 1`. The algorithm still works because it reduces to averaging a single row or column. For example, input `1 3` with values `10 20 30` yields `20`, matching direct computation.

A final edge case is precision loss when summing large grids. Since the maximum sum is `10^6 × 100 = 10^8`, using floating-point accumulation remains stable within the required `1e-6` tolerance, and no special numerics are needed.
