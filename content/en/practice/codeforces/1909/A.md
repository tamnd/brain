---
title: "CF 1909A - Distinct Buttons"
description: "We are asked to move on an infinite grid starting from the origin. We have four possible moves corresponding to the four cardinal directions: up, down, left, and right."
date: "2026-06-08T20:28:13+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1909
codeforces_index: "A"
codeforces_contest_name: "Pinely Round 3 (Div. 1 + Div. 2)"
rating: 800
weight: 1909
solve_time_s: 96
verified: true
draft: false
---

[CF 1909A - Distinct Buttons](https://codeforces.com/problemset/problem/1909/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to move on an infinite grid starting from the origin. We have four possible moves corresponding to the four cardinal directions: up, down, left, and right. Each move is triggered by a separate button on a controller, but the controller is fragile: if we press all four buttons at least once during our journey, it breaks. Therefore, we are limited to using at most three distinct directions to reach all the given points. Each test case provides a set of points with integer coordinates, and we need to determine whether it is possible to visit all of them without pressing all four buttons.

The constraints are moderate. There can be up to 100 points per test case and up to 1000 test cases. Each coordinate is small, between -100 and 100, which allows us to perform simple scanning over coordinates without worrying about inefficiency. The key challenge is not computational performance but geometric reasoning: we need to figure out which directions are necessary to reach all points.

A naive mistake would be to try to visit points in arbitrary order and track exact button presses. For instance, if points span all four quadrants relative to the origin, a careless approach might attempt a path visiting each quadrant sequentially and mistakenly assume it is always possible. For example, with points `(1,1)`, `(-1,-1)`, `(1,-1)`, and `(-1,1)`, any path must use all four directions, so the correct answer is "NO".

## Approaches

The brute-force approach would try all permutations of the points and see whether there exists an order of visiting them that uses at most three directions. This is impractical because the factorial growth of permutations would explode even for modest `n=10`. It is correct in principle but infeasible for our constraints.

The key observation is that we do not need to simulate the path or the order. Every point's quadrant relative to the origin determines which directions are needed. We can classify each point by its x and y coordinates:

- To reach points with x > 0, we must be able to move right.
- To reach points with x < 0, we must be able to move left.
- To reach points with y > 0, we must be able to move up.
- To reach points with y < 0, we must be able to move down.

This yields four potential directions, corresponding to the four buttons. If all four directions are required to reach the points, the controller would break. Otherwise, it is safe.

Therefore, for each test case, we check if there are points with positive x, negative x, positive y, and negative y simultaneously. If all four exist, the answer is "NO". Otherwise, it is "YES". This reduces the problem to simple scanning of coordinates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, initialize four flags: `need_right`, `need_left`, `need_up`, `need_down` to `False`. These represent whether we must press the corresponding button to reach any point.
2. Iterate over all points in the test case. For each point `(x, y)`, update the flags:

- If `x > 0`, set `need_right = True`.
- If `x < 0`, set `need_left = True`.
- If `y > 0`, set `need_up = True`.
- If `y < 0`, set `need_down = True`.
3. After processing all points, check if all four flags are `True`. If so, output "NO" because visiting all points requires all four buttons. Otherwise, output "YES".
4. Repeat for all test cases.

Why it works: the flags capture the minimal set of directions needed to reach all points. If any button is unnecessary, the controller will not break. Since we are only counting which buttons are required, the actual order of visiting points does not matter. The solution correctly answers "YES" if and only if at most three buttons are needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    need_right = need_left = need_up = need_down = False
    for _ in range(n):
        x, y = map(int, input().split())
        if x > 0:
            need_right = True
        if x < 0:
            need_left = True
        if y > 0:
            need_up = True
        if y < 0:
            need_down = True
    if need_right and need_left and need_up and need_down:
        print("NO")
    else:
        print("YES")
```

The code follows the algorithm step by step. The flags are updated independently for each point. We avoid storing points since we only need direction information. Boundary conditions where points lie on axes are handled automatically because `x=0` or `y=0` does not require any horizontal or vertical movement. Using `sys.stdin.readline` ensures fast input for large numbers of test cases.

## Worked Examples

Consider the first sample test case:

| Step | Point `(x, y)` | Flags after update |
| --- | --- | --- |
| 1 | (1, -1) | right=True, left=False, up=False, down=True |
| 2 | (0, 0) | right=True, left=False, up=False, down=True |
| 3 | (1, -1) | right=True, left=False, up=False, down=True |

None of the flags are simultaneously all `True`, so the output is "YES". The trace confirms that only two buttons are needed: right and down.

Consider the third sample:

| Step | Point `(x, y)` | Flags after update |
| --- | --- | --- |
| 1 | (1,1) | right=True, left=False, up=True, down=False |
| 2 | (-1,-1) | right=True, left=True, up=True, down=True |
| 3 | (1,-1) | right=True, left=True, up=True, down=True |
| 4 | (-1,1) | right=True, left=True, up=True, down=True |

All four flags are True, so the output is "NO". The trace demonstrates that points in all four quadrants require all four buttons.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case requires scanning all n points, and t ≤ 1000, n ≤ 100 |
| Space | O(1) | Only four boolean flags are stored per test case |

Given the small maximum values of t and n, the total number of operations is at most 1000 * 100 = 100,000, which easily fits within 1-second time limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        need_right = need_left = need_up = need_down = False
        for _ in range(n):
            x, y = map(int, input().split())
            if x > 0:
                need_right = True
            if x < 0:
                need_left = True
            if y > 0:
                need_up = True
            if y < 0:
                need_down = True
        if need_right and need_left and need_up and need_down:
            print("NO")
        else:
            print("YES")
    return output.getvalue().strip()

# Provided samples
assert run("6\n3\n1 -1\n0 0\n1 -1\n4\n-3 -2\n-3 -1\n-3 0\n-3 1\n4\n1 1\n-1 -1\n1 -1\n-1 1\n6\n-4 14\n-9 -13\n-14 5\n14 15\n-8 -4\n19 9\n6\n82 64\n39 91\n3 46\n87 83\n74 21\n7 25\n1\n100 -100") == "YES\nYES\nNO\nNO\nYES\nYES"

# Custom cases
assert run("1\n1\n0 0") == "YES", "single origin point"
assert run("1\n2\n0 5\n0 -5") == "YES", "vertical line requires up/down only"
assert run("1\n2\n5 0\n-5 0") == "YES", "horizontal line requires left/right only"
assert run("1\n4\n1 1\n1 -1\n-1 1\n-1 -1") == "NO", "points in all four quadrants"
assert run("1\n3\n0 1\n1 0\n0 -1") == "YES", "three directions only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 point at origin | YES | No movement needed |
| Vertical points | YES | Only two directions used |
| Horizontal points | YES | Only two directions used |
| Four quadrants | NO | Requires all four directions |
| Three directions | YES | Exactly three buttons needed, valid |

## Edge Cases

If all points
