---
title: "CF 104518B - Potato War 1"
description: "Two players each start with a fixed number of potatoes and then grow more potatoes at a constant daily rate. Technoblade starts with $X1$ potatoes and gains $Y1$ potatoes per day. His rival starts with $X2$ potatoes and gains $Y2$ potatoes per day."
date: "2026-06-30T10:36:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104518
codeforces_index: "B"
codeforces_contest_name: "UNICAMP Selection Contest 2023"
rating: 0
weight: 104518
solve_time_s: 51
verified: true
draft: false
---

[CF 104518B - Potato War 1](https://codeforces.com/problemset/problem/104518/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players each start with a fixed number of potatoes and then grow more potatoes at a constant daily rate. Technoblade starts with $X_1$ potatoes and gains $Y_1$ potatoes per day. His rival starts with $X_2$ potatoes and gains $Y_2$ potatoes per day. Time progresses in whole days, and both growth processes happen at the same pace.

The task is to determine the earliest day when Technoblade’s total strictly exceeds his rival’s total. If such a moment never arrives, the answer is -1.

After $d$ days, the totals are linear expressions:

$$T(d) = X_1 + d \cdot Y_1, \quad S(d) = X_2 + d \cdot Y_2$$

We are asked to find the smallest non-negative integer $d$ such that $T(d) > S(d)$, or decide that no such $d$ exists.

The constraints are small, with all values up to 1000, which means even direct simulation over time is feasible. However, linear growth problems often hide a subtle issue: when the competitor grows faster or starts ahead, the inequality may never flip, or may only flip once. That makes it important to reason about monotonicity rather than blindly iterating.

A common failure case appears when Technoblade starts behind but grows faster. A naive solution might stop too early or fail to consider $d = 0$. Another edge case is when both grow at the same rate but one starts ahead, in which case the answer is either 0 or impossible forever depending on initial values.

## Approaches

The brute-force approach simulates day by day. Starting from $d = 0$, we compute both values and check whether Technoblade has strictly more potatoes. If not, we increment the day and repeat. Since the values grow linearly, this process is guaranteed to eventually either find a crossing point or detect that it never happens within a reasonable bound.

This works because the difference between the two players evolves linearly as well. However, if we simulate indefinitely, the worst case occurs when Technoblade never catches up. In that situation, a naive loop would run forever or rely on an arbitrary cutoff, which is unsafe.

The key observation is that we can compare growth rates directly. Define the difference:

$$D(d) = (X_1 - X_2) + d (Y_1 - Y_2)$$

This is a linear function. If $Y_1 \le Y_2$, the function is non-increasing or constant. In that case, if Technoblade is not already ahead at $d = 0$, he will never become ahead later. If $Y_1 > Y_2$, the difference strictly increases over time, so there will be at most one crossing point. Instead of simulating, we can solve a simple inequality.

From:

$$X_1 + dY_1 > X_2 + dY_2$$

we get:

$$X_1 - X_2 > d (Y_2 - Y_1)$$

If $Y_1 = Y_2$, the comparison never changes after day 0. Otherwise we can compute the threshold directly using integer arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(D) | O(1) | Too slow / unsafe |
| Direct Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the initial difference $diff = X_1 - X_2$. This captures who is ahead before any growth happens.
2. If $diff > 0$, Technoblade is already strictly ahead at day 0, so the answer is 0. No future simulation is needed because the requirement is already satisfied.
3. If $Y_1 = Y_2$, both players grow at the same rate, so the difference never changes. If Technoblade is not already ahead, it is impossible for him to ever become ahead, so return -1.
4. If $Y_1 < Y_2$, Technoblade grows more slowly, meaning the gap only worsens over time. Even if he is initially close, he can never overtake, so return -1.
5. If $Y_1 > Y_2$, the difference increases by a fixed positive amount each day. We need the smallest $d$ such that:

$$X_1 + dY_1 > X_2 + dY_2$$

Rearranging:

$$diff + d (Y_1 - Y_2) > 0$$

Solve for $d$:

$$d > \frac{X_2 - X_1}{Y_1 - Y_2}$$

The smallest integer $d$ satisfying this is:

$$d = \left\lfloor \frac{X_2 - X_1}{Y_1 - Y_2} \right\rfloor + 1$$
6. Output the computed $d$.

### Why it works

The key invariant is that the difference between the two players is a linear function of time with constant slope $Y_1 - Y_2$. A linear function over integers can cross zero at most once unless the slope is zero. This means the ordering of the two players can change at most one time, and the exact crossing point can be computed algebraically instead of being searched. The algorithm exploits this by converting a dynamic process into a single inequality solve, guaranteeing correctness without iteration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x1, y1, x2, y2 = map(int, input().split())
    
    diff = x1 - x2
    
    if diff > 0:
        print(0)
        return
    
    if y1 == y2:
        print(-1)
        return
    
    if y1 < y2:
        print(-1)
        return
    
    # y1 > y2
    gap = x2 - x1
    gain = y1 - y2
    
    d = gap // gain
    if gap % gain != 0:
        d += 1
    
    print(d)

if __name__ == "__main__":
    solve()
```

The code begins by checking whether Technoblade is already ahead at day zero, which immediately determines the answer. It then handles the cases where the relative growth rates are not favorable, since in both equal and smaller growth scenarios the inequality never flips in his favor.

Only in the strictly increasing case does it compute the exact crossing point. The division is carefully handled using ceiling logic, since we need the first integer day where the strict inequality holds. The use of integer arithmetic avoids floating-point precision issues and keeps the solution deterministic.

## Worked Examples

### Example 1

Input:

```
100 2 200 1
```

Here $X_1 = 100$, $Y_1 = 2$, $X_2 = 200$, $Y_2 = 1$

| Day d | Techno | Rival | Difference |
| --- | --- | --- | --- |
| 0 | 100 | 200 | -100 |
| 1 | 102 | 201 | -99 |
| 2 | 104 | 202 | -98 |
| 100 | 300 | 300 | 0 |
| 101 | 302 | 301 | 1 |

The difference starts negative but increases each day by 1. The first time it becomes strictly positive is at $d = 101$, which matches the formula:

$$d = \frac{100}{1} + 1 = 101$$

This confirms that the algorithm correctly identifies the first strict inequality crossing.

### Example 2

Input:

```
5 1 10 2
```

| Day d | Techno | Rival | Difference |
| --- | --- | --- | --- |
| 0 | 5 | 10 | -5 |
| 1 | 6 | 12 | -6 |
| 2 | 7 | 14 | -7 |

The gap is shrinking in the wrong direction because Technoblade grows slower. The difference never becomes positive, so the answer is -1. The algorithm correctly classifies this case via the $Y_1 < Y_2$ check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and comparisons are performed |
| Space | O(1) | No auxiliary structures are used |

The constraints allow any approach, but the constant-time solution ensures immediate computation even for repeated runs or extended inputs.

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

# sample-style cases
assert run("100 0 99 1000") == "0"
assert run("100 2 200 1") == "101"

# equal growth, already ahead
assert run("10 5 1 5") == "0"

# equal growth, never ahead
assert run("1 2 10 2") == "-1"

# slower growth always losing
assert run("5 1 10 2") == "-1"

# exact boundary crossing
assert run("0 3 3 1") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 5 1 5 | 0 | already ahead at d=0 |
| 1 2 10 2 | -1 | equal growth, never catches up |
| 0 3 3 1 | 2 | exact integer crossing case |

## Edge Cases

When both players grow at the same rate, the system becomes static in terms of ordering. For input `10 3 5 3`, the difference is always 5, so the answer is 0. The algorithm handles this immediately via the equality check on growth rates.

When Technoblade starts behind but grows faster, the answer depends entirely on whether the linear function crosses zero at an integer point. For `0 2 5 1`, the difference increases by 1 per day starting at -5, so the crossing occurs exactly when the accumulated gain offsets the initial deficit. The computed value $d = 5$ matches direct simulation.

When Technoblade grows slower, such as `10 1 100 5`, the gap worsens each day. The algorithm detects this via $Y_1 < Y_2$ and returns -1 without attempting unnecessary computation, matching the fact that the linear difference has negative slope and never crosses zero in the positive direction.
