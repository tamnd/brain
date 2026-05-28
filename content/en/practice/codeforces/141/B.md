---
title: "CF 141B - Hopscotch"
description: "We are asked to determine whether a stone thrown onto a hopscotch court lands strictly inside a square, and if so, to identify which square. The court is constructed from squares of side length a, arranged in rows with a repeating 1-1-2-1-2 pattern."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 141
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 101 (Div. 2)"
rating: 1400
weight: 141
solve_time_s: 86
verified: true
draft: false
---

[CF 141B - Hopscotch](https://codeforces.com/problemset/problem/141/B)

**Rating:** 1400  
**Tags:** geometry, math  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a stone thrown onto a hopscotch court lands strictly inside a square, and if so, to identify which square. The court is constructed from squares of side length `a`, arranged in rows with a repeating 1-1-2-1-2 pattern. Each square is numbered sequentially starting from the bottom row, left to right. Coordinates `(x, y)` specify where the stone lands in the plane, with `(0, 0)` at the bottom-left corner of the first square. If the stone lands on a border or outside the court, the output should be `-1`.

The constraints indicate that `a` is small, up to 100, while `x` and `y` can be very large, up to `10^6` in magnitude. This rules out any approach that iterates over all potential squares individually, since the number of squares vertically could exceed `10^4` in the worst case.

The non-obvious edge cases involve stones landing exactly on the borders of squares or between rows. For example, with `a = 1`, a stone at `(0, 0)` is on the corner of the first square and should return `-1`. Similarly, a stone that lands exactly in the horizontal gap between two squares in a row of two should also return `-1`. Any naive solution that simply divides `x` and `y` by `a` without checking strict containment will fail on these border cases.

## Approaches

A brute-force solution would involve generating the coordinates of every square, storing their bounding boxes, and checking whether `(x, y)` lies strictly inside each box. This works because it directly models the problem, but it is too slow for large coordinates since the number of squares grows linearly with `y` and the alternating row widths. With `y` up to `10^6` and `a` possibly 1, we would need to examine up to `10^6` rows, each with up to 2 squares, giving millions of checks in the worst case.

The key observation for an optimal solution is that the hopscotch court is periodic. The bottom row is a single square, the next row is a single square, then a double-square row, and then this 1-2 pattern repeats. The vertical layout allows us to directly compute which row the stone is in by integer division of `y` by `a`, while the horizontal layout is simple to handle once the row type is determined. We also need to handle the strict inside condition by checking that the stone is not on the boundary of a square. This reduces the problem to arithmetic computations based on `x`, `y`, and `a`, avoiding the need to generate all squares explicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(y/a) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. First, check if `x` is negative. If it is, the stone is outside the court, so output `-1`.
2. Compute the row index by integer division of `y` by `a` to find which row contains the stone vertically. Call this `row`.
3. Compute the remainder `y % a` to determine the position inside the row. If the remainder is 0 or exactly `a`, the stone is on the horizontal boundary, so output `-1`.
4. Determine the type of the row: the first two rows are single squares, then the pattern repeats with a double-square row followed by a single-square row. Use the row index to identify whether the row has 1 or 2 squares.
5. For single-square rows, check whether `x` is strictly between 0 and `a`. If not, output `-1`.
6. For double-square rows, check whether `x` is strictly between 0 and `2*a`. If `x` lies between 0 and `a`, the stone is in the first square; if between `a` and `2*a`, the stone is in the second square. If `x` is outside this range, output `-1`.
7. Compute the absolute square number by summing the number of squares in all previous rows and adding the local square index within the current row.

Why it works: The algorithm directly maps `y` to a row and `x` to a column, respecting the alternating 1-2 pattern. By checking strict inequalities, we guarantee that stones on boundaries are rejected. The periodic row pattern allows calculation without generating the full court.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, x, y = map(int, input().split())

if x < 0:
    print(-1)
    sys.exit()

row = y // a
row_pos = y % a

if row_pos == 0:
    print(-1)
    sys.exit()

# first two rows: 1 square each
if row == 0:
    if 0 < x < a:
        print(1)
    else:
        print(-1)
    sys.exit()
elif row == 1:
    if 0 < x < a:
        print(2)
    else:
        print(-1)
    sys.exit()

# pattern repeats starting from row 2
# rows: 2 -> 2+ pattern 1-2-1-2...
pattern_row = row - 2
# compute how many full cycles of 2 rows we have
cycle = pattern_row // 2
# determine type of row in cycle
row_in_cycle = pattern_row % 2  # 0 -> 1-square, 1 -> 2-squares

# base number of squares before this cycle
base_square = 2 + cycle * 3

if row_in_cycle == 0:  # single square row
    if 0 < x < a:
        print(base_square + 1)
    else:
        print(-1)
else:  # double square row
    if 0 < x < a:
        print(base_square + 1)
    elif a < x < 2*a:
        print(base_square + 2)
    else:
        print(-1)
```

The code first handles the trivial cases of negative `x` and the first two rows. For subsequent rows, it determines the row's type by using modular arithmetic and integer division, then maps `x` to the correct square. Boundary checks are strict to exclude stones on edges.

## Worked Examples

**Sample 1**: `a=1, x=0, y=0`

| Variable | Value |
| --- | --- |
| x | 0 |
| y | 0 |
| row | 0 |
| row_pos | 0 |

The check `row_pos == 0` triggers, and the output is `-1`. The stone is on the corner of the first square.

**Sample 2**: `a=2, x=1, y=5`

| Variable | Value |
| --- | --- |
| row | 2 |
| row_pos | 1 |
| pattern_row | 0 |
| row_in_cycle | 0 |
| base_square | 2 |

The stone is in a single-square row, `0 < x < a` is true (`1 < 2`), so the square number is `base_square + 1 = 3`.

These traces show how the algorithm maps coordinates to row, identifies the square type, and computes the correct square number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All operations are arithmetic and conditional checks, independent of `x` or `y`. |
| Space | O(1) | Only a few integer variables are used. |

The solution handles large `x` and `y` efficiently and fits well within the constraints of 2 seconds and 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    old_out = sys.stdout
    sys.stdout = io.StringIO()
    exec(open("solution.py").read())
    res = sys.stdout.getvalue().strip()
    sys.stdout = old_out
    return res

# provided sample
assert run("1 0 0") == "-1", "sample 1"

# custom cases
assert run("2 1 5") == "3", "stone inside 3rd square"
assert run("2 2 5") == "-1", "stone on vertical border of double row"
assert run("1 -1 1") == "-1", "stone outside left"
assert run("3 1 1") == "1", "stone inside first square"
assert run("1 1 2") == "-1", "stone exactly on boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 5 | 3 | Correct mapping in a single-square row beyond first two rows |
| 2 2 5 | -1 | Stone on boundary in double-square row |
| 1 -1 1 | -1 | Negative x coordinate |
| 3 1 1 | 1 | Stone inside the first square |
| 1 1 2 | -1 | Stone on horizontal boundary |

## Edge Cases

For the input `1 0 0`, the stone is on the corner. The algorithm computes `row = 0`, `row_pos = 0`, triggering the horizontal boundary check and correctly outputs `-1`.

For `2
