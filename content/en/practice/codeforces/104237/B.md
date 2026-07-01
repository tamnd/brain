---
title: "CF 104237B - Road Intersections"
description: "We are given a collection of infinite straight lines laid out on a plane. Each line is either vertical, representing an avenue with a fixed x-coordinate, or horizontal, representing a street with a fixed y-coordinate."
date: "2026-07-01T23:19:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104237
codeforces_index: "B"
codeforces_contest_name: "Harker Programming Invitational 2023 Novice"
rating: 0
weight: 104237
solve_time_s: 60
verified: true
draft: false
---

[CF 104237B - Road Intersections](https://codeforces.com/problemset/problem/104237/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of infinite straight lines laid out on a plane. Each line is either vertical, representing an avenue with a fixed x-coordinate, or horizontal, representing a street with a fixed y-coordinate. Every vertical line intersects every horizontal line exactly once, and each such crossing counts as an intersection.

The task is to compute how many such intersection points exist among all given lines.

The input size is at most 1000 lines. This immediately suggests that a quadratic approach is acceptable, since a solution that checks all pairs of lines performs at most about 10^6 operations, which is comfortably within limits in Python.

A few corner cases matter here. If all lines are vertical, then there are no horizontal lines to intersect with, so the answer must be zero. The same holds symmetrically if all lines are horizontal. Another subtle case is when there is exactly one vertical or one horizontal line. In that situation, the answer equals the size of the opposite group, and a mistaken implementation that tries to pair lines of the same type would incorrectly produce extra counts.

A naive but common mistake is to count intersections by comparing every pair of lines and incrementing when coordinates differ, which is logically unrelated to the geometry of the problem. Intersections only occur between perpendicular lines, not between arbitrary pairs.

## Approaches

The brute-force idea is to consider every pair of lines and check whether they intersect. However, most pairs are irrelevant: two vertical lines never intersect each other, and two horizontal lines never intersect each other. The only meaningful interactions are between a vertical line and a horizontal line.

If we separate the input into two groups, vertical lines and horizontal lines, the problem simplifies significantly. Every vertical line at x = a intersects every horizontal line at y = b exactly once. That means each pair contributes exactly one intersection.

So instead of checking all pairs among N lines, we only need to count how many lines are vertical and how many are horizontal. The final answer is their product.

The brute-force approach would still iterate over all pairs of lines and check types, leading to O(N²) checks. The optimized version reduces the problem to counting frequencies in O(N).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow but unnecessary |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We convert the geometric problem into counting two categories of lines.

1. Read the number of lines N and initialize two counters, one for vertical lines and one for horizontal lines. This separation is essential because intersections only happen across categories.
2. For each line, read its type. If it is vertical, increment the vertical counter. If it is horizontal, increment the horizontal counter. The actual coordinate value is irrelevant because any vertical line intersects every horizontal line regardless of position.
3. After processing all lines, compute the number of intersections as vertical_count multiplied by horizontal_count. This follows directly from the fact that each vertical line forms a crossing with every horizontal line.
4. Output the result.

### Why it works

Each vertical line is defined by a fixed x-coordinate and extends infinitely in both directions. Each horizontal line is defined by a fixed y-coordinate. For any chosen pair consisting of one vertical and one horizontal line, their intersection is guaranteed and unique because they define a single point (x, y). Since there are no duplicate lines, every such pair contributes exactly one intersection, and no other types of pairs contribute anything. This establishes a one-to-one correspondence between intersection points and ordered pairs of vertical and horizontal lines.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    v = 0
    h = 0
    
    for _ in range(n):
        t, x = input().split()
        if t == 'v':
            v += 1
        else:
            h += 1
    
    print(v * h)

if __name__ == "__main__":
    solve()
```

The solution maintains two simple counters while scanning the input once. The coordinate values are read but intentionally ignored because they do not affect whether intersections exist; only orientation matters.

The multiplication at the end encodes the Cartesian product between the two sets of lines. A frequent implementation mistake is attempting to store coordinates and check equality or proximity, which is unnecessary and would incorrectly complicate the logic.

## Worked Examples

### Sample 1

Input:

```
5
h 3
h 2
h 1
v 2
v 1
```

We track counts of horizontal and vertical lines.

| Step | Line | Horizontal | Vertical |
| --- | --- | --- | --- |
| 1 | h 3 | 1 | 0 |
| 2 | h 2 | 2 | 0 |
| 3 | h 1 | 3 | 0 |
| 4 | v 2 | 3 | 1 |
| 5 | v 1 | 3 | 2 |

Final result is 3 × 2 = 6.

This matches the intuition that each of the 2 vertical lines intersects each of the 3 horizontal lines.

### Sample 2

Input:

```
3
v 10
v -5
v 7
```

| Step | Line | Horizontal | Vertical |
| --- | --- | --- | --- |
| 1 | v 10 | 0 | 1 |
| 2 | v -5 | 0 | 2 |
| 3 | v 7 | 0 | 3 |

Final result is 0 × 3 = 0.

This confirms the edge case where no horizontal lines exist, so no intersections are possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each line is processed exactly once with constant-time updates |
| Space | O(1) | Only two integer counters are maintained regardless of input size |

The constraints allow up to 1000 lines, and this solution performs a single linear pass with trivial operations per line, making it easily within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""5
h 3
h 2
h 1
v 2
v 1
""") == "6"

# all vertical
assert run("""4
v 1
v 2
v 3
v 4
""") == "0"

# all horizontal
assert run("""3
h 10
h 20
h 30
""") == "0"

# mixed small
assert run("""2
h 5
v 7
""") == "1"

# balanced
assert run("""6
h 1
h 2
v 1
v 2
v 3
h 3
""") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all vertical | 0 | no horizontal lines edge case |
| all horizontal | 0 | symmetric edge case |
| mixed small | 1 | single intersection correctness |
| balanced | 9 | full Cartesian product behavior |

## Edge Cases

When all lines are vertical, the algorithm reads each line and increments only the vertical counter. The horizontal counter remains zero, so the product is zero. For example:

Input:

```
2
v 1
v 2
```

Execution sets v = 2, h = 0, giving 0 intersections, which matches the fact that parallel vertical lines never meet.

When there is exactly one vertical line and multiple horizontal lines, say:

```
3
v 5
h 1
h 2
```

The counters become v = 1 and h = 2. The result is 2, corresponding to the single vertical line intersecting both horizontal lines exactly once each.
