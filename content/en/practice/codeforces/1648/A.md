---
title: "CF 1648A - Weird Sum"
description: "We are given a 2D grid of size $n times m$ where each cell contains a color represented by an integer. The task is to compute the sum of Manhattan distances between every pair of cells that share the same color."
date: "2026-06-10T03:58:43+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "geometry", "math", "matrices", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1648
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 775 (Div. 1, based on Moscow Open Olympiad in Informatics)"
rating: 1400
weight: 1648
solve_time_s: 72
verified: true
draft: false
---

[CF 1648A - Weird Sum](https://codeforces.com/problemset/problem/1648/A)

**Rating:** 1400  
**Tags:** combinatorics, data structures, geometry, math, matrices, sortings  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a 2D grid of size $n \times m$ where each cell contains a color represented by an integer. The task is to compute the sum of Manhattan distances between every pair of cells that share the same color. The Manhattan distance between two cells $(r_1, c_1)$ and $(r_2, c_2)$ is $|r_1 - r_2| + |c_1 - c_2|$, which counts the number of vertical and horizontal steps needed to move from one cell to another.

The input consists of $n$ rows with $m$ integers each, and the total number of cells does not exceed 100,000. This implies we cannot afford a solution that iterates over all pairs of cells directly, since that could result in roughly $(10^5)^2 / 2 = 5 \cdot 10^9$ operations, far exceeding a 2-second time limit. A linear or near-linear approach is necessary.

Edge cases include grids where all cells have the same color, a grid with only one row or column, or a grid where each cell has a distinct color. A careless brute-force method would attempt to sum distances over all pairs blindly, which would be too slow for the largest inputs.

## Approaches

The naive approach iterates over each color, collects all positions of that color, and sums the Manhattan distances over all pairs. If a color appears $k$ times, this requires $O(k^2)$ operations per color. In the worst case, if all 100,000 cells have the same color, this approach requires $O(10^{10})$ operations, which is impractical.

The key insight is that Manhattan distance is separable into row and column contributions: $|r_1 - r_2| + |c_1 - c_2| = |r_1 - r_2| + |c_1 - c_2|$. Therefore, we can compute the row and column sums independently. If we sort all row indices of a color and compute a running sum, the total distance contributed by the rows can be calculated in linear time relative to the number of occurrences. The same applies to column indices. Specifically, after sorting, for each position $i$, the total distance to all previous positions is $i \cdot \text{row}_i - \text{sum of previous rows}$. Summing this over all positions gives the total row contribution, and analogously for columns.

This reduces the time complexity from $O(k^2)$ per color to $O(k \log k)$ for sorting plus $O(k)$ for the sum computation. Given that the sum of all $k$ over all colors is at most 100,000, this is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((nm)^2) | O(nm) | Too slow |
| Optimal | O(nm log nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Create a dictionary mapping each color to two lists: the row indices and the column indices of all occurrences of that color. This separates the row and column contributions and organizes positions by color.
2. For each color, sort the list of row indices. Sorting is necessary because the formula for the sum of distances works on ordered sequences.
3. Initialize a running sum of distances for rows. Iterate over the sorted row indices. For the current index $i$, add $i \cdot \text{row}_i - \text{sum of previous rows}$ to the total. This efficiently computes the sum of $|r_i - r_j|$ for all previous $j < i$ in linear time.
4. Repeat steps 2-3 for the column indices, summing the contributions to the same total variable.
5. After processing all colors, print the accumulated sum. This is the total sum of Manhattan distances between all pairs of cells with the same color.

Why it works: The separation into rows and columns leverages the linearity of Manhattan distance. Sorting ensures that we can calculate cumulative differences efficiently. The formula $i \cdot x_i - \text{sum of previous}$ is derived from the observation that $\sum_{j=0}^{i-1} |x_i - x_j| = i \cdot x_i - \sum_{j=0}^{i-1} x_j$ for a sorted sequence, guaranteeing that every pair is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def main():
    n, m = map(int, input().split())
    color_positions = defaultdict(lambda: ([], []))  # maps color -> (rows, cols)
    
    for r in range(n):
        row = list(map(int, input().split()))
        for c, color in enumerate(row):
            color_positions[color][0].append(r)
            color_positions[color][1].append(c)
    
    total_sum = 0
    for rows, cols in color_positions.values():
        for indices in (rows, cols):
            indices.sort()
            acc = 0
            running_sum = 0
            for i, val in enumerate(indices):
                acc += i * val - running_sum
                running_sum += val
            total_sum += acc
    
    print(total_sum)

if __name__ == "__main__":
    main()
```

The dictionary collects row and column indices separately for each color, enabling independent sum calculations. Sorting ensures the formula applies correctly. `running_sum` accumulates the sum of previous indices for each dimension, which avoids recalculating sums repeatedly. This method handles all sizes of grids and colors without exceeding memory or time constraints.

## Worked Examples

Sample Input 1:

```
2 3
1 2 3
3 2 1
```

| Color | Rows | Cols | Sorted Rows | Row contribution | Sorted Cols | Col contribution | Total contribution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [0,1] | [0,2] | [0,1] | 1 | [0,2] | 2 | 3 |
| 2 | [0,1] | [1,1] | [0,1] | 1 | [1,1] | 0 | 1 |
| 3 | [0,1] | [2,0] | [0,1] | 1 | [0,2] | 2 | 3 |

Total sum: 3 + 1 + 3 = 7, which matches the expected output.

A second example with one color filling the grid:

```
2 2
5 5
5 5
```

| Color | Rows | Cols | Row contribution | Col contribution |
| --- | --- | --- | --- | --- |
| 5 | [0,0,1,1] | [0,1,0,1] | 4 | 4 |

The Manhattan distances between all six pairs: distances sum to 8, matching our calculation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm log nm) | Sorting row and column indices for each color dominates; sum computation is linear. |
| Space | O(nm) | Storing positions for each color requires O(number of cells). |

With $nm \le 10^5$, sorting dominates but fits comfortably within 2 seconds. Memory usage remains under the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided sample
assert run("2 3\n1 2 3\n3 2 1\n") == "7", "sample 1"

# Minimum size
assert run("1 1\n1\n") == "0", "single cell"

# All cells same
assert run("2 2\n5 5\n5 5\n") == "8", "all same color"

# Row only
assert run("1 4\n1 2 1 2\n") == "4", "single row"

# Column only
assert run("4 1\n1\n2\n1\n2\n") == "4", "single column"

# Maximum distinct
assert run("2 3\n1 2 3\n4 5 6\n") == "0", "all distinct colors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | 0 | Single cell, no pairs |
| 2x2 all same | 8 | Multiple pairs, verifies sum calculation |
| 1x4 mixed | 4 | Horizontal distances, row contributions |
| 4x1 mixed | 4 | Vertical distances, column contributions |
| 2x3 all distinct | 0 | No pairs, ensures sum stays zero |

## Edge Cases

For a grid where all cells have the same color, such as:

```
2 2
5 5
5 5
```

Rows: [0,0,1,1], Cols: [0,1,0,1]. Sorting rows and columns, the algorithm computes row contribution: 1_0-0=0, 2_0-0=0, 3*
