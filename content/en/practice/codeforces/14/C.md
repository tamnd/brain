---
title: "CF 14C - Four Segments"
description: "We are given exactly four line segments on the 2D plane. Every segment is axis-aligned, or may even degenerate into a single point."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "geometry", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 14
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 14 (Div. 2)"
rating: 1700
weight: 14
solve_time_s: 108
verified: true
draft: false
---
[CF 14C - Four Segments](https://codeforces.com/problemset/problem/14/C)

**Rating:** 1700  
**Tags:** brute force, constructive algorithms, geometry, implementation, math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given exactly four line segments on the 2D plane. Every segment is axis-aligned, or may even degenerate into a single point. The task is to decide whether these four segments together form the border of one rectangle with positive area, where all rectangle sides are parallel to the coordinate axes.

A valid rectangle in this problem has very strict structure. There must be exactly two horizontal sides and exactly two vertical sides. The horizontal sides must share the same left and right endpoints, and the vertical sides must connect those endpoints. The rectangle must also have non-zero width and non-zero height.

The coordinate bounds are very large, up to $10^9$, but there are only four segments. That changes the nature of the problem completely. We do not need sophisticated geometry or optimization. Even checking every possible arrangement of the four segments is trivial because $4! = 24$. The real challenge is correctness, not performance.

Several edge cases make naive implementations fail.

One common mistake is checking only the existence of two distinct x-coordinates and two distinct y-coordinates. Consider this input:

```
0 0 2 0
0 1 2 1
0 0 0 0
2 0 2 1
```

The third segment is just a point, so the left side of the rectangle is missing. The correct answer is `NO`. A careless solution might incorrectly accept it because all four corner coordinates appear somewhere.

Another dangerous case is overlapping or duplicated segments:

```
0 0 2 0
0 0 2 0
0 0 0 1
2 0 2 1
```

There are four segments, but only one horizontal side actually exists. The correct answer is `NO`.

A third subtle case is zero-area rectangles:

```
0 0 0 0
0 1 0 1
0 0 0 1
0 0 0 1
```

All points lie on one vertical line. Width is zero, so no rectangle exists. The correct answer is `NO`.

Another source of bugs is reversed endpoint order. These two segments represent the same geometric line:

```
0 0 3 0
3 0 0 0
```

Any correct solution must normalize segment direction before comparing them.

## Approaches

A brute-force approach would try every permutation of the four segments and ask whether they can play the roles of top, bottom, left, and right sides of a rectangle.

This works because there are only four segments. For each permutation, we can verify:

1. The first two segments are horizontal.
2. The last two segments are vertical.
3. The horizontal segments share the same x-range.
4. The vertical segments share the same y-range.
5. The endpoints connect perfectly into a rectangle.
6. Width and height are both positive.

Since there are only 24 permutations, this approach is already fast enough.

The interesting observation is that we do not actually need permutations if we classify segments by orientation. A rectangle aligned to the axes has a rigid structure:

- exactly two horizontal segments,
- exactly two vertical segments,
- matching coordinate ranges.

Once we separate the segments into horizontal and vertical groups, the verification becomes deterministic.

The brute-force solution succeeds because the input size is tiny. The structural observation about rectangles lets us simplify the logic into direct comparisons instead of trying all arrangements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4!) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four segments.
2. Normalize every segment so that its endpoints are ordered consistently.

For horizontal segments, store the smaller x-coordinate first. For vertical segments, store the smaller y-coordinate first. This avoids bugs caused by reversed input order.
3. Classify each segment.

If $y_1 = y_2$, the segment is horizontal.

If $x_1 = x_2$, the segment is vertical.

Otherwise, the segment is diagonal and can never belong to the required rectangle, so return `NO`.
4. Verify that there are exactly two horizontal segments and exactly two vertical segments.

Any valid axis-aligned rectangle has precisely this structure.
5. Let the horizontal segments be:

$$(x_1, y_a) \to (x_2, y_a)$$

and

$$(x_1', y_b) \to (x_2', y_b)$$

Check that:

$$x_1 = x_1'$$

and

$$x_2 = x_2'$$

This guarantees both horizontal sides span the same width.
6. Let the vertical segments be:

$$(x_c, y_1) \to (x_c, y_2)$$

and

$$(x_d, y_1') \to (x_d, y_2')$$

Check that:

$$y_1 = y_1'$$

and

$$y_2 = y_2'$$

This guarantees both vertical sides span the same height.
7. Verify that the rectangle corners match correctly.

The left and right x-coordinates from the horizontal sides must equal the x-coordinates of the vertical sides.

The bottom and top y-coordinates from the vertical sides must equal the y-coordinates of the horizontal sides.
8. Check that width and height are positive.

Width is:

$$x_2 - x_1$$

Height is:

$$y_2 - y_1$$

Both must be strictly greater than zero.
9. If all checks pass, print `YES`. Otherwise print `NO`.

### Why it works

A rectangle parallel to the axes is completely determined by two distinct x-values and two distinct y-values. The four sides must exactly connect those coordinates.

The algorithm verifies every geometric property required for such a rectangle:

- correct orientations,
- matching side lengths,
- shared endpoints,
- positive area.

If any condition fails, at least one rectangle side is missing, duplicated, disconnected, or degenerate. If all conditions hold, the four segments uniquely form the rectangle border.

## Python Solution

```python
import sys
input = sys.stdin.readline

def normalize(x1, y1, x2, y2):
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
    else:
        if x1 > x2:
            x1, x2 = x2, x1
    return (x1, y1, x2, y2)

def solve():
    horizontal = []
    vertical = []

    for _ in range(4):
        x1, y1, x2, y2 = map(int, input().split())

        x1, y1, x2, y2 = normalize(x1, y1, x2, y2)

        if y1 == y2:
            horizontal.append((x1, y1, x2, y2))
        elif x1 == x2:
            vertical.append((x1, y1, x2, y2))
        else:
            print("NO")
            return

    if len(horizontal) != 2 or len(vertical) != 2:
        print("NO")
        return

    h1 = horizontal[0]
    h2 = horizontal[1]

    v1 = vertical[0]
    v2 = vertical[1]

    # Horizontal sides must share x-range
    if h1[0] != h2[0] or h1[2] != h2[2]:
        print("NO")
        return

    # Vertical sides must share y-range
    if v1[1] != v2[1] or v1[3] != v2[3]:
        print("NO")
        return

    left_x = h1[0]
    right_x = h1[2]

    bottom_y = v1[1]
    top_y = v1[3]

    # Positive area
    if left_x == right_x or bottom_y == top_y:
        print("NO")
        return

    xs = sorted([v1[0], v2[0]])
    ys = sorted([h1[1], h2[1]])

    if xs != [left_x, right_x]:
        print("NO")
        return

    if ys != [bottom_y, top_y]:
        print("NO")
        return

    print("YES")

solve()
```

The first helper function normalizes segment direction. This is critical because the input does not guarantee endpoint ordering. Without normalization, two identical segments written in opposite directions would fail equality checks.

The main function separates segments by orientation. Any segment that is neither horizontal nor vertical immediately invalidates the configuration.

After classification, the code checks the rectangle structure directly. The two horizontal segments must span the same interval on the x-axis, and the two vertical segments must span the same interval on the y-axis.

The positive-area check prevents degenerate rectangles where width or height is zero.

The final coordinate comparisons guarantee that all four sides connect consistently. This catches cases with disconnected or misplaced segments even when lengths appear correct.

Since coordinates fit safely inside Python integers, overflow is never an issue.

## Worked Examples

### Example 1

Input:

```
1 1 6 1
1 0 6 0
6 0 6 1
1 1 1 0
```

| Step | Horizontal Segments | Vertical Segments | Result |
| --- | --- | --- | --- |
| After classification | (1,1)-(6,1), (1,0)-(6,0) | (6,0)-(6,1), (1,0)-(1,1) | valid |
| X-range check | both use x = 1 to 6 | - | pass |
| Y-range check | - | both use y = 0 to 1 | pass |
| Area check | width = 5 | height = 1 | pass |
| Final match | x values = {1,6}, y values = {0,1} | consistent | YES |

This example demonstrates the ideal rectangle structure. Every side connects perfectly, and both dimensions are positive.

### Example 2

Input:

```
0 0 2 0
0 1 2 1
0 0 0 0
2 0 2 1
```

| Step | Horizontal Segments | Vertical Segments | Result |
| --- | --- | --- | --- |
| After classification | (0,0)-(2,0), (0,1)-(2,1), (0,0)-(0,0) | (2,0)-(2,1) | invalid |
| Count check | 3 horizontal | 1 vertical | fail |
| Final answer | - | - | NO |

The degenerate point segment is classified as horizontal because both y-values are equal. The algorithm correctly rejects the input because a rectangle requires exactly two horizontal and two vertical sides.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only four segments are processed |
| Space | O(1) | A few fixed-size lists and variables are used |

The solution easily fits within the limits. Even exhaustive checking would be trivial here because the input size never grows.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def normalize(x1, y1, x2, y2):
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
        else:
            if x1 > x2:
                x1, x2 = x2, x1
        return (x1, y1, x2, y2)

    horizontal = []
    vertical = []

    for _ in range(4):
        x1, y1, x2, y2 = map(int, input().split())

        x1, y1, x2, y2 = normalize(x1, y1, x2, y2)

        if y1 == y2:
            horizontal.append((x1, y1, x2, y2))
        elif x1 == x2:
            vertical.append((x1, y1, x2, y2))
        else:
            return "NO"

    if len(horizontal) != 2 or len(vertical) != 2:
        return "NO"

    h1, h2 = horizontal
    v1, v2 = vertical

    if h1[0] != h2[0] or h1[2] != h2[2]:
        return "NO"

    if v1[1] != v2[1] or v1[3] != v2[3]:
        return "NO"

    left_x = h1[0]
    right_x = h1[2]

    bottom_y = v1[1]
    top_y = v1[3]

    if left_x == right_x or bottom_y == top_y:
        return "NO"

    xs = sorted([v1[0], v2[0]])
    ys = sorted([h1[1], h2[1]])

    if xs != [left_x, right_x]:
        return "NO"

    if ys != [bottom_y, top_y]:
        return "NO"

    return "YES"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""1 1 6 1
1 0 6 0
6 0 6 1
1 1 1 0
"""
) == "YES", "sample 1"

# zero area rectangle
assert run(
"""0 0 0 0
0 1 0 1
0 0 0 1
0 0 0 1
"""
) == "NO", "zero width"

# duplicated segment
assert run(
"""0 0 2 0
0 0 2 0
0 0 0 1
2 0 2 1
"""
) == "NO", "duplicate horizontal side"

# reversed endpoints
assert run(
"""3 0 0 0
0 2 3 2
0 0 0 2
3 2 3 0
"""
) == "YES", "normalization check"

# diagonal segment
assert run(
"""0 0 1 1
0 1 1 1
0 0 0 1
1 0 1 1
"""
) == "NO", "diagonal edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Degenerate vertical line | NO | Positive area requirement |
| Duplicate horizontal segment | NO | Missing rectangle side |
| Reversed endpoints | YES | Correct normalization |
| One diagonal segment | NO | Orientation validation |

## Edge Cases

### Degenerate segments treated as valid sides

Input:

```
0 0 2 0
0 1 2 1
0 0 0 0
2 0 2 1
```

The third segment is a single point. During classification, it becomes a horizontal segment because its y-values match. The algorithm ends up with three horizontal segments and one vertical segment, so it immediately rejects the configuration with `NO`.

This prevents point segments from pretending to be rectangle sides.

### Zero-area rectangle

Input:

```
0 0 0 0
0 1 0 1
0 0 0 1
0 0 0 1
```

After normalization:

- both vertical segments lie on $x = 0$,
- horizontal segments are actually points.

The computed width is:

$$0 - 0 = 0$$

The positive-area check fails, so the answer is `NO`.

### Reversed endpoint order

Input:

```
3 0 0 0
0 2 3 2
0 0 0 2
3 2 3 0
```

Normalization converts the segments into consistent ordering:

- `(0,0)-(3,0)`
- `(0,2)-(3,2)`
- `(0,0)-(0,2)`
- `(3,0)-(3,2)`

All rectangle checks pass, so the algorithm correctly outputs `YES`.

Without normalization, direct coordinate comparisons would fail even though the geometry is correct.

### Duplicate sides

Input:

```
0 0 2 0
0 0 2 0
0 0 0 1
2 0 2 1
```

Both horizontal segments occupy the exact same position. Their y-values are identical, so there is no top side and bottom side distinction.

Later, the algorithm compares the y-values collected from horizontal segments against the y-range from vertical segments:

- horizontal y-values: `[0, 0]`
- vertical y-range: `[0, 1]`

The mismatch produces `NO`.

This catches overlapping segments that do not actually enclose an area.
