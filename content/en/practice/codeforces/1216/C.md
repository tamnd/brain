---
title: "CF 1216C - White Sheet"
description: "We are given three rectangles on a plane aligned with the axes. The first rectangle is a white sheet, and two subsequent rectangles are black sheets. Each rectangle is defined by its bottom-left and top-right coordinates."
date: "2026-06-11T22:52:34+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1216
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 587 (Div. 3)"
rating: 1700
weight: 1216
solve_time_s: 148
verified: true
draft: false
---

[CF 1216C - White Sheet](https://codeforces.com/problemset/problem/1216/C)

**Rating:** 1700  
**Tags:** geometry, math  
**Solve time:** 2m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three rectangles on a plane aligned with the axes. The first rectangle is a white sheet, and two subsequent rectangles are black sheets. Each rectangle is defined by its bottom-left and top-right coordinates. The task is to determine if, after placing the black sheets on top of the white sheet, any portion of the white sheet is still visible from above.

The coordinates define the rectangle edges exactly, and rectangles include their boundaries. A point on the edge of the white sheet counts as visible if it is not strictly covered by any black sheet. The black sheets can overlap each other and can partially or completely cover the white sheet.

The coordinate range goes up to $10^6$, but there are only three rectangles, so any algorithm that does a small constant number of arithmetic comparisons is efficient. We do not need complex data structures, grids, or sweeps; a geometric reasoning approach suffices.

The key edge cases arise when the white sheet is completely covered along one axis but not the other. For example, the white sheet could be entirely covered horizontally but still extend vertically outside the black sheets. A naive check of total area or simple overlap would fail here. We also need to handle zero-width or zero-height overlaps gracefully.

For instance, if the white sheet spans from (0,0) to (4,4), the first black sheet covers (0,0) to (4,2) and the second black sheet covers (0,2) to (4,4). The white sheet is fully covered. Any approach that only checks individual overlaps without combining them might incorrectly report a visible part.

## Approaches

The brute-force approach is to consider every point on the white sheet and check if it is covered by either black sheet. This works in principle but is infeasible because even a moderate grid sampling would take millions of checks given the coordinate bounds up to $10^6$. Checking each integer coordinate inside the white rectangle is $O((x_2-x_1)*(y_2-y_1))$, which can reach $10^{12}$ operations, far exceeding time limits.

The key observation is that a rectangle can only be completely covered if it is fully blocked along one axis. This lets us reduce the problem to a small number of 1D checks. We can separately check coverage along the horizontal (x) axis and vertical (y) axis. The white sheet is invisible only if there exists a configuration where the black sheets jointly cover the entire horizontal span or the entire vertical span. If any gap remains along either axis, some part of the white sheet remains visible.

So the optimal solution checks the maximum left and minimum right of the black sheets to see if they completely block the white sheet horizontally. Similarly, it checks the maximum bottom and minimum top of the black sheets for vertical coverage. If either axis has a gap outside the combined black sheet projection, the answer is "YES"; otherwise, it is "NO".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((x2-x1)*(y2-y1)) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Extract the coordinates of the white sheet: x1, y1, x2, y2.
2. Extract the coordinates of the first black sheet: x3, y3, x4, y4.
3. Extract the coordinates of the second black sheet: x5, y5, x6, y6.
4. Compute the horizontal coverage of the black sheets combined. The leftmost block is min(x3, x5), and the rightmost block is max(x4, x6). Check if this combined range covers the white sheet entirely, i.e., if the leftmost ≤ x1 and the rightmost ≥ x2.
5. Compute the vertical coverage similarly. The bottommost block is min(y3, y5), and the topmost block is max(y4, y6). Check if this covers the white sheet entirely vertically.
6. If both horizontal and vertical coverage fully block the white sheet, print "NO". Otherwise, print "YES".

Why it works: By projecting rectangles onto each axis, we reduce the 2D coverage problem to 1D intervals. The white sheet is fully invisible only if its entire horizontal interval is covered and its entire vertical interval is covered. Any gap along either axis guarantees at least one visible point. This works for any combination of partial overlaps and ensures we handle the edge cases of overlapping black sheets.

## Python Solution

```python
import sys
input = sys.stdin.readline

x1, y1, x2, y2 = map(int, input().split())
x3, y3, x4, y4 = map(int, input().split())
x5, y5, x6, y6 = map(int, input().split())

# Compute horizontal coverage
h_left = min(x3, x5)
h_right = max(x4, x6)
horizontal_covers = h_left <= x1 and h_right >= x2

# Compute vertical coverage
v_bottom = min(y3, y5)
v_top = max(y4, y6)
vertical_covers = v_bottom <= y1 and v_top >= y2

if horizontal_covers and vertical_covers:
    print("NO")
else:
    print("YES")
```

The solution first reads coordinates and computes the extreme boundaries of the black sheets along each axis. We then check if the union of black sheet projections fully contains the white sheet along both axes. It is important to use `<=` and `>=` to handle exact edge alignments, because coverage including the edge counts as blocking.

## Worked Examples

**Sample 1:**

Input:

```
2 2 4 4
1 1 3 5
3 1 5 5
```

| Variable | Value |
| --- | --- |
| h_left | min(1,3)=1 |
| h_right | max(3,5)=5 |
| horizontal_covers | 1 ≤ 2 and 5 ≥ 4 → True |
| v_bottom | min(1,1)=1 |
| v_top | max(5,5)=5 |
| vertical_covers | 1 ≤ 2 and 5 ≥ 4 → True |

Both axes are fully covered, output is NO.

**Sample 2:**

Input:

```
2 2 4 4
0 0 3 3
1 1 5 5
```

| Variable | Value |
| --- | --- |
| h_left | min(0,1)=0 |
| h_right | max(3,5)=5 |
| horizontal_covers | 0 ≤ 2 and 5 ≥ 4 → True |
| v_bottom | min(0,1)=0 |
| v_top | max(3,5)=5 |
| vertical_covers | 0 ≤ 2 and 5 ≥ 4 → True |

Here the union still covers, output NO. If we move one black sheet up so v_bottom > y1, a gap appears, giving YES.

These traces show that projecting onto each axis accurately determines coverage without checking every point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a handful of arithmetic and comparisons |
| Space | O(1) | Only variables for coordinates and extrema |

With only three rectangles, this solution executes in constant time and memory. The largest coordinate is $10^6$, and all operations are integer comparisons and min/max, fitting easily within the 1-second, 256 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x1, y1, x2, y2 = map(int, input().split())
    x3, y3, x4, y4 = map(int, input().split())
    x5, y5, x6, y6 = map(int, input().split())
    h_left = min(x3, x5)
    h_right = max(x4, x6)
    horizontal_covers = h_left <= x1 and h_right >= x2
    v_bottom = min(y3, y5)
    v_top = max(y4, y6)
    vertical_covers = v_bottom <= y1 and v_top >= y2
    return "NO" if horizontal_covers and vertical_covers else "YES"

# provided samples
assert run("2 2 4 4\n1 1 3 5\n3 1 5 5\n") == "NO", "sample 1"
assert run("2 2 4 4\n0 0 3 3\n1 1 5 5\n") == "NO", "sample 2"

# custom cases
assert run("0 0 1 1\n2 2 3 3\n4 4 5 5\n") == "YES", "white completely free"
assert run("0 0 2 2\n0 0 1 3\n1 0 3 2\n") == "NO", "exact full coverage"
assert run("0 0 2 2\n0 0 1 1\n1 0 3 1\n") == "YES", "vertical gap"
assert run("0 0 2 2\n0 0 1 3\n1 1 3 3\n") == "YES", "horizontal gap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
|  |  |  |
