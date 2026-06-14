---
title: "CF 1547A - Shortest Path with Obstacle"
description: "We are working on an infinite grid where movement is allowed in four directions: up, down, left, and right, each costing one step. We are given three special cells: a start cell, a target cell, and a forbidden cell that cannot be stepped on."
date: "2026-06-14T19:49:34+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1547
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 731 (Div. 3)"
rating: 800
weight: 1547
solve_time_s: 460
verified: true
draft: false
---

[CF 1547A - Shortest Path with Obstacle](https://codeforces.com/problemset/problem/1547/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 7m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on an infinite grid where movement is allowed in four directions: up, down, left, and right, each costing one step. We are given three special cells: a start cell, a target cell, and a forbidden cell that cannot be stepped on. The task is to compute the shortest number of moves required to go from the start to the target without ever landing on the forbidden cell.

If the forbidden cell were not present, the answer would simply be the Manhattan distance between the start and the target, since in a grid with free movement the shortest path is always the sum of horizontal and vertical separations.

The constraint of up to 10^4 test cases forces us to avoid any graph search per query. A BFS over the grid would be far too slow because even though coordinates are bounded by 1000, the grid is conceptually unbounded and BFS complexity depends on explored area, not input size. We need an O(1) formula per test case.

A key edge case arises when the forbidden cell lies exactly on the straight Manhattan path between A and B. For example, if A is (1,1), B is (1,5), and F is (1,3), the direct vertical path is blocked. A naive Manhattan distance computation would return 4, but the true answer is 6 because we must detour around F. Another subtle case is when F is not on any shortest path corridor between A and B; then the answer remains unchanged.

## Approaches

Without the obstacle, the problem is trivial. The shortest path between two grid points is simply the Manhattan distance, computed as the absolute difference in x-coordinates plus the absolute difference in y-coordinates. This works because every optimal path must make exactly that many horizontal and vertical moves, and any permutation of those moves is valid.

Introducing a single forbidden cell changes things only in a very restricted way. The only time the answer differs from the Manhattan distance is when every shortest path from A to B is forced to pass through F. This happens exactly when A, B, and F lie on the same row or column segment and F is between them. In that situation, any shortest path would step on F, so we must detour by going around it, which adds exactly two extra steps.

If F is not on the geometric segment formed by A and B in Manhattan sense, we can still achieve the Manhattan distance by slightly adjusting the order of moves so that we never land on F. This is possible because there is always at least one alternative shortest route that avoids a single off-path point.

So the solution reduces to computing the Manhattan distance and then checking whether F blocks the direct alignment of A and B on a straight segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute-force BFS on grid | O(N) per query (effectively unbounded) | O(N) | Too slow |
| Manhattan + blocking check | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the Manhattan distance between A and B as the base answer. This represents the shortest possible path ignoring the obstacle.
2. Check whether A and B are aligned either horizontally or vertically. If they are not aligned in this way, no single point can force all shortest paths through F, so the base answer remains valid.
3. If A and B share the same x-coordinate, then any shortest path moves only vertically. In this case, check whether F also lies on this same vertical line and its y-coordinate lies strictly between those of A and B.
4. If A and B share the same y-coordinate, perform the symmetric check for horizontal alignment.
5. If F lies exactly on the segment between A and B in either case, increase the answer by 2 to account for the detour around the blocked cell.

The detour cost of exactly 2 comes from the fact that the smallest way to avoid a blocked intermediate cell on a straight line is to step aside one unit, pass around it, and return to the original line.

### Why it works

A shortest path in the grid is fully determined by choosing an order of horizontal and vertical moves. A single blocked cell can only invalidate all shortest paths if it lies on every monotone path that preserves optimal length. That only happens when the path is constrained to a single row or column segment. Outside this configuration, we can always reorder moves so that the forbidden cell is bypassed without increasing total path length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    xA, yA = map(int, input().split())
    xB, yB = map(int, input().split())
    xF, yF = map(int, input().split())

    ans = abs(xA - xB) + abs(yA - yB)

    if xA == xB == xF:
        if min(yA, yB) < yF < max(yA, yB):
            ans += 2

    if yA == yB == yF:
        if min(xA, xB) < xF < max(xA, xB):
            ans += 2

    return ans

t = int(input())
out = []
for _ in range(t):
    input()
    out.append(str(solve()))

print("\n".join(out))
```

The implementation computes the Manhattan distance directly and then applies a constant-time correction if the forbidden cell lies strictly between A and B on a shared axis. The blank line between test cases is consumed explicitly because the input format includes it.

A common implementation mistake is to forget the strict inequality check. If F equals A or B, it should not trigger any detour logic because the problem guarantees distinct cells, but even if that assumption is relaxed, endpoints do not block shortest paths in the same way.

## Worked Examples

Consider the case where A = (1,1), B = (3,3), and F = (2,2). The Manhattan distance is 4. The cells are not aligned horizontally or vertically, so no correction applies.

| Step | x condition | y condition | correction | answer |
| --- | --- | --- | --- | --- |
| init | - | - | 0 | 4 |

This shows that diagonal movement cases are unaffected by a single obstacle not lying on a forced corridor.

Now consider A = (2,5), B = (2,1), F = (2,3). The Manhattan distance is 4. Since all points share x = 2 and F lies between y = 5 and y = 1, every direct vertical shortest path passes through F.

| Step | alignment | F between | correction | answer |
| --- | --- | --- | --- | --- |
| init | vertical | yes | +2 | 6 |

This confirms the detour rule, where the path must move one step sideways and return, increasing length by exactly 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed in constant time using arithmetic and comparisons |
| Space | O(1) | Only a fixed number of variables are stored |

The constraints allow up to 10^4 queries, so an O(1) solution per query is necessary. The approach satisfies this easily.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve_case():
        xA, yA = map(int, input().split())
        xB, yB = map(int, input().split())
        xF, yF = map(int, input().split())

        ans = abs(xA - xB) + abs(yA - yB)

        if xA == xB == xF and min(yA, yB) < yF < max(yA, yB):
            ans += 2
        if yA == yB == yF and min(xA, xB) < xF < max(xA, xB):
            ans += 2

        return ans

    t_line = input().strip()
    if not t_line:
        t_line = input().strip()
    t = int(t_line)

    res = []
    for _ in range(t):
        input()  # empty line
        res.append(str(solve_case()))
    return "\n".join(res)

# provided samples (abbreviated formatting assumed consistent)
sample_in = """7

1 1
3 3
2 2

2 5
2 1
2 3

1000 42
1000 1
1000 1000

1 10
3 10
2 10

3 8
7 8
3 7

2 1
4 1
1 1

1 344
1 10
1 1
"""

assert run(sample_in).split() == ["4","6","41","4","4","2","334"]

# custom cases
assert run("""1

1 1
1 5
1 3
""") == "6"

assert run("""1

1 1
5 5
10 10
""") == "8"

assert run("""1

2 2
2 2
1 1
""") == "0"

assert run("""1

3 1
1 1
2 1
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| vertical block | 6 | obstacle on straight vertical segment |
| diagonal no effect | 8 | obstacle irrelevant off path |
| same point | 0 | degenerate zero distance |
| horizontal block | 4 | symmetric horizontal obstruction |

## Edge Cases

One important case is when A and B are aligned but F lies outside the segment. For example A = (1,1), B = (1,5), F = (1,10). The algorithm checks strict inequality, so no correction is applied and the answer remains 4. This is correct because we can route the path upward without ever touching F.

Another case is when alignment holds in x or y but F coincides with one endpoint. The problem guarantees distinct points, but even if not, endpoints do not force detours since the path starts or ends there.

A final case is when A and B are not aligned, even if F shares coordinates with one of them. The Manhattan path can always be rearranged to avoid F while preserving length, so no correction is needed.
