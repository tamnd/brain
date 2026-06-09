---
title: "CF 1781A - Parallel Projection"
description: "We are working inside a rectangular room shaped like a box. A point on the floor marks where the laptop sits, and a point directly above on the ceiling marks where the projector hangs."
date: "2026-06-09T11:15:48+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1781
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2022 - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 (Engine)"
rating: 800
weight: 1781
solve_time_s: 120
verified: false
draft: false
---

[CF 1781A - Parallel Projection](https://codeforces.com/problemset/problem/1781/A)

**Rating:** 800  
**Tags:** geometry, math  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We are working inside a rectangular room shaped like a box. A point on the floor marks where the laptop sits, and a point directly above on the ceiling marks where the projector hangs. A cable must connect these two points, but it is constrained to move only along the surface of the room, meaning it can travel on the floor, walls, and ceiling, and it must always follow directions parallel to the edges of the box.

The task is to compute the shortest possible cable length between the laptop and the projector under these restrictions. The cable cannot cut through the interior of the box, so any path must be composed of axis-aligned segments lying on faces of the cuboid.

The key constraint is geometric rather than combinatorial. We are effectively finding the shortest Manhattan-style path on the surface of a 3D box between two points that lie on opposite faces.

The input sizes are small per test case, up to 10^4 cases, so each case must be solved in constant time. This rules out any graph search or simulation over the surface. The solution must come from recognizing that only a small fixed number of candidate surface unfoldings matter.

A subtle edge case appears when the horizontal projections of the two points align in one coordinate. In such cases, multiple candidate paths collapse into the same geometry, and naive formulas that assume distinct coordinates may overcount or miss the optimal route.

## Approaches

A brute-force view treats the cuboid surface as a graph: every point on edges and faces is a node, and movement along faces is allowed with Manhattan cost. One could discretize the surface into a grid and run a shortest path algorithm. This is correct in principle, but the number of states grows with the resolution of discretization, and even a coarse discretization is unnecessary because the endpoints are continuous coordinates. This makes brute force unusable.

The key observation is that an optimal path between two points on a box surface always corresponds to unfolding two adjacent faces into a plane. Once unfolded, the path becomes a straight-line Manhattan distance between two planar points. There are only a constant number of meaningful unfoldings, and each corresponds to choosing a pair of adjacent faces through which the cable travels.

For a floor point (a, b, 0) and a ceiling point (f, g, h), the optimal path always consists of moving from the floor up a vertical wall and then across to the ceiling. The shortest route depends only on whether we go via the left, right, front, or back walls, which translates into a few absolute difference expressions.

This reduces the problem to evaluating a small set of candidate Manhattan distances and taking the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Surface graph search | O(∞ discretization) | O(large) | Too slow |
| Unfolding + case analysis | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We start by observing that any valid path must move from the floor to a wall, then possibly across that wall, and finally onto the ceiling. Since movement is restricted to axis-aligned edges on faces, every path corresponds to choosing a direction in which we “exit” the floor rectangle.

1. Compute horizontal separations in the floor plane, meaning |a - f| and |b - g|. These represent how far apart the projection of the two points is along the two floor axes.
2. Consider the four possible ways to move between floor and ceiling by using walls aligned with the rectangle edges. Each choice corresponds to routing the path around one side of the box.
3. For each candidate route, convert the 3D path into a 2D Manhattan distance expression. Every route contributes a sum of one horizontal difference, one vertical difference, and the height h.
4. Evaluate all candidate expressions and take the minimum.

The reason we only need a constant number of expressions is that any shortest surface path must correspond to one unfolding of two adjacent faces, and there are only four such unfoldings connecting floor to ceiling through a single wall boundary.

### Why it works

Any valid surface path from floor to ceiling must cross exactly one vertical transition from z = 0 to z = h through a wall. Once that transition point is fixed on an edge of the box, the rest of the path on each face is a straight Manhattan segment. Minimizing over all possible wall edges reduces to comparing a constant set of configurations, and no interior detour can improve a Manhattan path on a flat face.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        w, d, h = map(int, input().split())
        a, b, f, g = map(int, input().split())

        dx = abs(a - f)
        dy = abs(b - g)

        # four candidate surface routes
        ans = min(
            dx + b + g + h,
            dx + (d - b) + (d - g) + h,
            dy + a + f + h,
            dy + (w - a) + (w - f) + h
        )

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation precomputes the horizontal differences and evaluates four geometric configurations. Each expression corresponds to choosing one of the four vertical sides of the room as the transition surface between floor and ceiling. The added terms like b + g or (d - b) + (d - g) represent walking from the points to the chosen wall edge before going vertically through height h.

A common mistake is forgetting that the transition can occur on any of the four walls, not just the nearest one in projection. Another is assuming a direct Manhattan distance plus height, which fails when both points are closer to a different wall than the naive projection suggests.

## Worked Examples

We trace two cases from the sample set.

### Example 1

Input: w=55, d=20, h=29, a=23, b=10, f=18, g=3

| Expression | Value |
| --- | --- |
| dx + b + g + h | 5 + 10 + 3 + 29 = 47 |
| dx + (d-b) + (d-g) + h | 5 + 10 + 17 + 29 = 61 |
| dy + a + f + h | 7 + 23 + 18 + 29 = 77 |
| dy + (w-a) + (w-f) + h | 7 + 32 + 37 + 29 = 105 |

Minimum is 47.

This confirms that routing through the nearest horizontal projection onto one side wall dominates all alternatives.

### Example 2

Input: w=20, d=10, h=5, a=1, b=5, f=2, g=5

| Expression | Value |
| --- | --- |
| dx + b + g + h | 1 + 5 + 5 + 5 = 16 |
| dx + (d-b) + (d-g) + h | 1 + 5 + 5 + 5 = 16 |
| dy + a + f + h | 0 + 1 + 2 + 5 = 8 |
| dy + (w-a) + (w-f) + h | 0 + 19 + 18 + 5 = 42 |

Minimum is 8.

This shows the degenerate case where b equals g, making vertical alignment irrelevant and allowing a direct wall transition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case evaluates a constant number of arithmetic expressions |
| Space | O(1) | Only a few variables are stored per test case |

The constraints allow up to 10^4 test cases, so an O(1) per case solution is necessary. The constant-time geometric evaluation fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            w, d, h = map(int, input().split())
            a, b, f, g = map(int, input().split())

            dx = abs(a - f)
            dy = abs(b - g)

            out.append(str(min(
                dx + b + g + h,
                dx + (d - b) + (d - g) + h,
                dy + a + f + h,
                dy + (w - a) + (w - f) + h
            )))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""5
55 20 29
23 10 18 3
20 10 5
1 5 2 5
15 15 4
7 13 10 10
2 1000 2
1 1 1 999
10 4 10
7 1 2 1
""") == """47
8
14
1002
17"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| same x,y alignment | small value | degenerate vertical alignment |
| symmetric positions | equal candidates | symmetry of walls |
| extreme corner routing | large values | correctness of boundary paths |

## Edge Cases

When both points share the same projection on one axis, some candidate routes collapse and multiple expressions become equal. The algorithm handles this naturally because absolute differences become zero and the minimum still selects a valid wall path.

When a point is already close to a boundary, expressions involving that wall reduce significantly, and the minimum correctly picks that side. The formula structure ensures that no invalid shortcut through the interior is ever considered, since every candidate explicitly enforces surface traversal through a wall plus vertical transition.
