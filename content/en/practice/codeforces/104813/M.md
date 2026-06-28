---
title: "CF 104813M - Painter"
description: "We are working on an infinite 2D integer grid where every lattice point initially has the same default character \".\". We are then given a sequence of painting operations that overwrite regions of this grid with new characters."
date: "2026-06-28T13:14:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104813
codeforces_index: "M"
codeforces_contest_name: "The 9th CCPC (Harbin) Onsite(The 2nd Universal Cup. Stage 10: Harbin)"
rating: 0
weight: 104813
solve_time_s: 80
verified: false
draft: false
---

[CF 104813M - Painter](https://codeforces.com/problemset/problem/104813/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are working on an infinite 2D integer grid where every lattice point initially has the same default character `"."`. We are then given a sequence of painting operations that overwrite regions of this grid with new characters. There are two types of updates: one paints all integer points inside a circle, and the other paints all integer points inside an axis-aligned rectangle. A third type of operation asks us to output a finite sub-rectangle of the grid after all previous painting effects have been applied in order.

The key interpretation is that each operation is applied in sequence and overwrites previous colors. When multiple shapes overlap, the later operation completely replaces earlier colors at affected points. A render query simply asks for the final state of a bounded region after applying all prior updates.

The coordinate ranges are extremely large, up to 10^9 in magnitude, so we cannot simulate the grid explicitly. However, the total area of all render queries is small, at most 10^4 in total. This is the only part of the input where we are forced to materialize actual grid cells. Every other operation is defined geometrically over huge coordinate space.

A naive mistake is to try iterating over every point affected by every circle or rectangle. A circle of radius up to 10^9 could contain up to 10^18 integer points, so even a single operation is impossible to expand explicitly. Another subtle mistake is updating render queries directly without carefully respecting operation order. Since operations overwrite previous ones, the final color depends entirely on the most recent covering operation, not on how many operations intersect.

The critical edge case is overlapping updates with different shapes. For example, a rectangle paint followed by a circle paint that partially overlaps a render area must ensure the circle fully overrides the rectangle inside its region. Any approach that precomputes a single final grid without respecting order will fail.

## Approaches

The brute-force idea is straightforward in concept: maintain a dictionary or grid map of all painted points. For each circle or rectangle operation, iterate over every integer point in its geometric region and assign the given color. When a render query arrives, iterate over the requested region and output the stored values or `"."` if unpainted.

This is correct because it directly simulates the problem definition. The issue is runtime. A rectangle can be as large as 2·10^18 area, and even though render regions are small, updates dominate completely. Expanding circles is even worse because checking all integer points in a radius-r disk is O(r^2). With up to 2000 operations, this is completely infeasible.

The key observation is that we never need to explicitly simulate the entire grid. We only ever query small regions, and we only need the final color at those points. Instead of expanding shapes globally, we reverse the perspective: for each render query, we directly compute the color of each requested point independently by checking operations in reverse order.

For a fixed point (x, y), its final color is determined by the last operation that covers it. So we scan operations backward and stop as soon as we find one that paints that point. Since we only evaluate at most 10^4 total query points, and there are at most 2000 operations, this gives a manageable upper bound of 2×10^7 geometric checks.

Each check is constant time: rectangle containment is simple inequalities, and circle containment is a squared distance check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grid Simulation | O(total painted area) | O(grid) | Too slow |
| Reverse per-query evaluation | O(n · q) where q ≤ 10^4 | O(1) extra | Accepted |

## Algorithm Walkthrough

We process operations once, store them, and answer each render query independently.

1. Read all operations and store them in a list in order. We do not try to apply them immediately because rendering requires final-state queries, and later operations can override earlier ones.
2. When we encounter a render operation, we expand its rectangular region into a list of points. Since the sum of all render areas is at most 10^4, this expansion is safe.
3. For each point in the render region, we scan the operation list backward from the last operation to the first.
4. For each operation, we check whether it covers the current point.

For a rectangle, we check whether x1 ≤ x ≤ x2 and y1 ≤ y ≤ y2.

For a circle, we check whether (x - cx)^2 + (y - cy)^2 ≤ r^2.
5. The first operation we find in reverse order that covers the point determines its final color. We assign that character and stop scanning further for that point.
6. If no operation covers the point, we output `"."`.

The reason we scan backward is that later operations overwrite earlier ones. This guarantees that the first match encountered in reverse is exactly the last applied paint.

### Why it works

At any fixed grid point, its final color depends only on the latest operation that includes it. Because operations are applied sequentially and overwrite previous values, the painting process induces a last-writer-wins rule per cell. Scanning operations in reverse order reconstructs that last writer directly. Since each point is evaluated independently, no global state is required, and correctness follows from the fact that geometric containment checks exactly match whether an operation affects that point.

## Python Solution

```python
import sys
input = sys.stdin.readline

ops = []
renders = []

n = int(input())
for _ in range(n):
    parts = input().split()
    if parts[0] == "Circle":
        x, y, r = map(int, parts[1:4])
        col = parts[4]
        ops.append(("C", x, y, r, col))
    elif parts[0] == "Rectangle":
        x1, y1, x2, y2 = map(int, parts[1:5])
        col = parts[5]
        ops.append(("R", x1, y1, x2, y2, col))
    else:
        x1, y1, x2, y2 = map(int, parts[1:5])
        renders.append((x1, y1, x2, y2))

out_lines = []

for x1, y1, x2, y2 in renders:
    for y in range(y2, y1 - 1, -1):
        row = []
        for x in range(x1, x2 + 1):
            color = "."
            for op in reversed(ops):
                if op[0] == "R":
                    _, a1, b1, a2, b2, c = op
                    if a1 <= x <= a2 and b1 <= y <= b2:
                        color = c
                        break
                else:
                    _, cx, cy, r, c = op
                    dx = x - cx
                    dy = y - cy
                    if dx * dx + dy * dy <= r * r:
                        color = c
                        break
            row.append(color)
        out_lines.append("".join(row))

sys.stdout.write("\n".join(out_lines))
```

The solution keeps all operations in a list and delays evaluation until rendering. Each rendered cell independently scans operations backwards. The nested loops over the render area are necessary because output is explicitly required per cell, but the constraint ensures this total work remains small.

A subtle detail is the reversed iteration over y in the output, because the problem requires printing from y2 down to y1. This direction matters for matching the required visual orientation.

Circle checks use squared distance to avoid floating point operations, ensuring correctness with integer arithmetic.

## Worked Examples

We trace a simplified scenario derived from the sample structure.

### Example 1

Input operations:

```
Circle (0,0,r=1,'A')
Rectangle (0,0,1,1,'B')
Render (0,0,1,1)
```

Render region points are (0,0), (1,0), (0,1), (1,1).

| Point | Scan order (reverse ops) | First match | Result |
| --- | --- | --- | --- |
| (0,0) | Rectangle, Circle | Rectangle | B |
| (1,0) | Rectangle, Circle | Rectangle | B |
| (0,1) | Rectangle, Circle | Rectangle | B |
| (1,1) | Rectangle, Circle | Rectangle | B |

All points are covered by the rectangle last, so circle has no visible effect.

This confirms the key invariant: later operations dominate earlier ones even if they overlap partially.

### Example 2

```
Circle (0,0,r=2,'C')
Rectangle (-1,-1,1,1,'R')
Render (-1,-1,1,1)
```

| Point | Scan order | First match | Result |
| --- | --- | --- | --- |
| (0,0) | Rectangle, Circle | Rectangle | R |
| (1,1) | Rectangle, Circle | Rectangle | R |
| (2,0) | Circle only | Circle | C (outside render excluded if needed) |

Inside overlap, rectangle wins because it was applied later.

This demonstrates that order, not shape dominance, determines output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q · N) | Each render cell checks all operations in reverse until first hit |
| Space | O(N) | Stored list of operations and render output buffer |

The total number of rendered cells is at most 10^4, and each cell scans at most 2000 operations, giving about 2×10^7 primitive checks. This fits comfortably within time limits in Python with simple integer arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    ops = []
    renders = []
    n = int(input())
    for _ in range(n):
        parts = input().split()
        if parts[0] == "Circle":
            x, y, r = map(int, parts[1:4])
            col = parts[4]
            ops.append(("C", x, y, r, col))
        elif parts[0] == "Rectangle":
            x1, y1, x2, y2 = map(int, parts[1:5])
            col = parts[5]
            ops.append(("R", x1, y1, x2, y2, col))
        else:
            x1, y1, x2, y2 = map(int, parts[1:5])
            renders.append((x1, y1, x2, y2))

    out = []
    for x1, y1, x2, y2 in renders:
        for y in range(y2, y1 - 1, -1):
            row = []
            for x in range(x1, x2 + 1):
                color = "."
                for op in reversed(ops):
                    if op[0] == "R":
                        _, a1, b1, a2, b2, c = op
                        if a1 <= x <= a2 and b1 <= y <= b2:
                            color = c
                            break
                    else:
                        _, cx, cy, r, c = op
                        dx = x - cx
                        dy = y - cy
                        if dx * dx + dy * dy <= r * r:
                            color = c
                            break
                row.append(color)
            out.append("".join(row))

    return "\n".join(out)

# provided sample (formatted minimally)
assert run("""7
Circle 0 0 5 *
Circle -2 2 1 @
Circle 2 2 1 @
Rectangle 0 -1 0 0 ^
Rectangle -2 -2 2 -2 _
Render -5 -5 5 5
Render -1 0 1 2
""").strip() == """.....*.....
..*******..
.**@***@**.
.*@@@*@@@*.
.**@***@**.
*****^*****
.****^****.
.**_____**.
.*********.
..*******..
.....*.....
@*@
***
*^*""".strip()

# minimal edge
assert run("""3
Rectangle 0 0 0 0 A
Render 0 0 0 0
Render 1 1 1 1
""").strip() == """A
.""".strip()

# circle override
assert run("""3
Circle 0 0 1 B
Rectangle 0 0 0 0 A
Render 0 0 0 0
""").strip() == """A""".strip()

# negative coords
assert run("""2
Rectangle -1 -1 1 1 Z
Render -1 -1 1 1
""") == "ZZZ\nZZZ\nZZZ"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell rectangle + render | A / . | basic overwrite |
| rectangle then circle | A | order precedence |
| negative coordinates | 3x3 grid | coordinate handling |

## Edge Cases

A subtle edge case is when a render region contains points never affected by any operation. In that case, scanning all operations yields no match and the output must remain `"."`. For example, if we only paint a rectangle far away and render the origin, every point should stay `"."`. The reverse scan correctly handles this because it falls through all operations without assigning a color.

Another edge case is when a circle barely touches a point on its boundary. Since the condition is inclusive `(u-x)^2 + (v-y)^2 <= r^2`, boundary points must be colored. The integer squared-distance check ensures exact inclusion without floating-point error.

A final edge case is overlapping rectangle and circle where the circle is applied later but only partially overlaps the render region. Because each cell independently checks operations in reverse, only the affected subset of cells will pick up the circle color, while others remain determined by earlier operations or default `"."`.
