---
title: "CF 120D - Three Sons"
description: "We have a rectangular cornfield represented as a grid of size n × m, where each cell contains a certain number of tons of corn. The father wants to divide this field among three sons in such a way that each son receives exactly a predetermined amount of corn: A, B, or C tons."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 120
codeforces_index: "D"
codeforces_contest_name: "School Regional Team Contest, Saratov, 2011"
rating: 1400
weight: 120
solve_time_s: 95
verified: true
draft: false
---

[CF 120D - Three Sons](https://codeforces.com/problemset/problem/120/D)

**Rating:** 1400  
**Tags:** brute force  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular cornfield represented as a grid of size _n_ × _m_, where each cell contains a certain number of tons of corn. The father wants to divide this field among three sons in such a way that each son receives exactly a predetermined amount of corn: _A_, _B_, or _C_ tons. The division must be performed using two parallel lines, either horizontal or vertical, which fall strictly between the rows or columns. Each resulting section must include at least one square.

The input consists of the dimensions of the field, the corn quantities in each cell, and the target sums for the three sons. The output is the number of ways to place the two parallel lines so that the three resulting parts contain the exact amounts _A_, _B_, and _C_, in any order.

Given that _n_ and _m_ are both at most 50, a brute-force approach that examines every possible pair of lines is feasible if we compute the sum efficiently. Since the sum in any rectangle can be calculated in constant time with prefix sums, we can afford to check all possible partitions without exceeding the time limit. A subtle edge case occurs when one of the desired amounts is zero, especially if the field contains zeros. Another edge case is when all cells have equal values and the desired amounts are identical, which can lead to multiple valid partitions that might be missed by naive implementations that assume unique sums.

## Approaches

A naive brute-force approach iterates over all pairs of horizontal or vertical lines. For horizontal lines, we try placing the first line between row 1 and _n-1_, and the second line between the first line +1 and _n-1_. For vertical lines, we do the same along columns. For each candidate pair of lines, we calculate the sum of corn in the three resulting sections and check if they match the multiset {_A_, _B_, _C_}. This method works because the field is small, but if we calculate the sum of each section by iterating over the cells, the time complexity becomes O(n²·m + m²·n), which is inefficient for the worst-case 50×50 grid.

The key optimization is using prefix sums. By precomputing a 2D prefix sum array of size n×m, we can compute the sum of any rectangular section in constant time. For horizontal partitions, the sum of rows r1..r2 is simply the prefix sum difference, and similarly for vertical partitions with column sums. This reduces the complexity to O(n² + m²), which is acceptable since n² + m² ≤ 50² + 50² = 5000. After computing sums efficiently, we only need to check all permutations of {_A_, _B_, _C_} against the three section sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force without prefix sum | O(n²·m + m²·n) | O(1) | Too slow |
| Optimized with prefix sums | O(n² + m²) | O(n·m) | Accepted |

## Algorithm Walkthrough

1. Read the dimensions _n_, _m_ and the field grid. Read the target corn amounts _A_, _B_, _C_.
2. Compute a 2D prefix sum array `ps` where `ps[i][j]` represents the sum of the rectangle from the top-left corner to cell (i,j). The formula is `ps[i][j] = field[i][j] + ps[i-1][j] + ps[i][j-1] - ps[i-1][j-1]`.
3. Initialize a counter to zero to track valid partitions.
4. Check horizontal partitions. For each pair of lines `r1` and `r2` (1 ≤ r1 < r2 < n), compute the sum of corn in the three horizontal strips using the prefix sums: top rows 0..r1-1, middle rows r1..r2-1, bottom rows r2..n-1. If the multiset of these sums matches {_A_, _B_, _C_}, increment the counter.
5. Check vertical partitions analogously. For each pair of columns `c1` and `c2` (1 ≤ c1 < c2 < m), compute the sum of corn in the three vertical strips using the prefix sums: left columns 0..c1-1, middle columns c1..c2-1, right columns c2..m-1. If the multiset of these sums matches {_A_, _B_, _C_}, increment the counter.
6. Print the counter.

Why it works: The prefix sum array guarantees that every rectangular region sum can be computed in O(1). By iterating over all valid pairs of lines and checking sums against all permutations of {_A_, _B_, _C_}, we ensure that all possible valid divisions are counted exactly once. Each partition is guaranteed to contain at least one row or column because of the loop bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
field = [list(map(int, input().split())) for _ in range(n)]
A, B, C = map(int, input().split())

# compute prefix sums
ps = [[0]*m for _ in range(n)]
for i in range(n):
    for j in range(m):
        ps[i][j] = field[i][j]
        if i > 0:
            ps[i][j] += ps[i-1][j]
        if j > 0:
            ps[i][j] += ps[i][j-1]
        if i > 0 and j > 0:
            ps[i][j] -= ps[i-1][j-1]

def rect_sum(r1, c1, r2, c2):
    res = ps[r2][c2]
    if r1 > 0:
        res -= ps[r1-1][c2]
    if c1 > 0:
        res -= ps[r2][c1-1]
    if r1 > 0 and c1 > 0:
        res += ps[r1-1][c1-1]
    return res

targets = sorted([A, B, C])
count = 0

# horizontal partitions
for r1 in range(1, n):
    for r2 in range(r1+1, n):
        s1 = rect_sum(0, 0, r1-1, m-1)
        s2 = rect_sum(r1, 0, r2-1, m-1)
        s3 = rect_sum(r2, 0, n-1, m-1)
        if sorted([s1, s2, s3]) == targets:
            count += 1

# vertical partitions
for c1 in range(1, m):
    for c2 in range(c1+1, m):
        s1 = rect_sum(0, 0, n-1, c1-1)
        s2 = rect_sum(0, c1, n-1, c2-1)
        s3 = rect_sum(0, c2, n-1, m-1)
        if sorted([s1, s2, s3]) == targets:
            count += 1

print(count)
```

The prefix sum computation ensures constant-time rectangle queries. We carefully handle boundaries to avoid off-by-one errors. Sorting the sums before comparison handles the fact that the order of _A_, _B_, _C_ does not matter.

## Worked Examples

**Sample 1**

Input:

```
3 3
1 1 1
1 1 1
1 1 1
3 3 3
```

| r1 | r2 | s1 | s2 | s3 | matches? |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 3 | 3 | yes |

| c1 | c2 | s1 | s2 | s3 | matches? |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 3 | 3 | yes |

Count = 2, which matches the expected output.

**Custom Input**

```
3 3
1 2 3
4 5 6
7 8 9
6 15 24
```

Horizontal partitions yield sums `[1+2+3+4+5+6]=21` etc., only `r1=1,r2=2` produces `[6, 15, 24]` after sorting. Vertical partitions also produce no new matches. Output = 1.

These traces confirm the algorithm correctly considers all line placements and uses prefix sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² + m²) | Two nested loops for line positions along rows and columns; rectangle sum queries are O(1) |
| Space | O(n·m) | 2D prefix sum array of size n×m |

Given n,m ≤ 50, worst-case 2500 operations per direction, total ~5000 sum checks, well within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    field = [list(map(int, input().split())) for _ in range(n)]
    A, B, C = map(int, input
```
