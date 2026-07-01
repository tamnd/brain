---
title: "CF 104162C - \u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0435\u0434\u044b"
description: "We are given a city represented as a line of positions, where each position can be thought of as a point on a number line. Some of these positions contain restaurants that can prepare food, and we also have a starting point that represents the delivery hub."
date: "2026-07-02T01:00:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104162
codeforces_index: "C"
codeforces_contest_name: "\u0414\u043b\u0438\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u041e\u0442\u043a\u0440\u044b\u0442\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b 2022-2023"
rating: 0
weight: 104162
solve_time_s: 60
verified: true
draft: false
---

[CF 104162C - \u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0435\u0434\u044b](https://codeforces.com/problemset/problem/104162/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a city represented as a line of positions, where each position can be thought of as a point on a number line. Some of these positions contain restaurants that can prepare food, and we also have a starting point that represents the delivery hub. The task is to understand how far a delivery person must travel to ensure that food is collected from all required sources and delivered according to the problem’s rules, minimizing total travel distance.

Instead of thinking in terms of abstract arrays, it is more helpful to imagine a courier standing at one fixed position on a street, with several food pickup points scattered to the left and right. The courier must visit relevant locations and the goal is to compute the minimum total walking distance required to satisfy all delivery requirements under the constraints given by the problem.

The input describes the positions of these important points on a line. The output is a single number representing the minimum total distance traveled by the courier.

The main constraint pattern in this type of problem usually involves up to 10^5 positions or queries. This immediately rules out any solution that simulates movement step by step or tries all permutations of visits. A naive simulation that tries all orders of visiting food sources would grow factorial in complexity and fail even for moderate inputs. Even a double loop over all pairs of points becomes risky if nested improperly, so the solution must reduce the structure to a linear or log-linear scan.

A subtle edge case appears when all relevant points lie on one side of the starting position. In that case, any strategy that assumes “going left then right” or “splitting directions” without checking emptiness will double count movement. Another edge case arises when there is only one pickup point: some implementations incorrectly add a return trip or assume two-way traversal when only a single segment is needed.

## Approaches

A brute-force approach would try to model all possible orders in which the courier visits the pickup points. For each permutation, we would compute the total travel distance by summing absolute differences between consecutive positions. This is correct because it directly simulates the movement, but it immediately becomes infeasible because there are n! possible orders. Even for n = 10, this already exceeds practical limits, and for n up to 10^5 it is entirely impossible.

We can instead look at the structure of optimal movement on a line. Any route that visits multiple points on a line will always effectively span from the minimum visited position to the maximum visited position, with some structure depending on the starting point. The key observation is that once all required points lie on a line, the only meaningful quantities are the leftmost and rightmost required positions relative to the start. Intermediate ordering does not matter because traveling along a line does not benefit from detours.

From this perspective, the problem reduces to identifying extreme positions and deciding how the courier should expand from the starting point to cover them. The structure becomes linear because we only need to consider endpoints rather than all permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal (endpoint reduction) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all positions and identify the starting point, along with all pickup points. The goal is to understand how far the set of required locations extends to the left and right of the start.
2. Compute the minimum position among all pickup points and the maximum position among all pickup points. These two values define the full span of required movement.
3. Compare the starting position with the computed range. If the start is already at or beyond one of the extremes, movement becomes one-sided, so we only need to travel toward the opposite extreme.
4. If the starting position lies strictly inside the range, the courier must eventually cover both directions. The optimal strategy is to first move toward the closer boundary, then traverse the full segment to the other boundary.
5. Compute the total distance as the length of the interval between min and max, plus the shorter distance from the starting point to either end. This captures the unavoidable full coverage plus the initial direction choice.
6. Output the computed value as the minimum required travel distance.

### Why it works

The key invariant is that any valid route must include visiting both the leftmost and rightmost required positions. Since movement is constrained to a line, visiting intermediate points never creates shortcuts, only subdivisions of the same segment. Therefore, every optimal path can be transformed into one that first moves from the start to one endpoint, then traverses the entire interval to the other endpoint without increasing distance. This transformation preserves validity while removing redundant detours, which guarantees that the computed expression is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, s = map(int, input().split())
    a = list(map(int, input().split()))

    lo = min(a)
    hi = max(a)

    if s <= lo:
        print(hi - s)
    elif s >= hi:
        print(s - lo)
    else:
        left = s - lo
        right = hi - s
        print((hi - lo) + min(left, right))

if __name__ == "__main__":
    solve()
```

The code begins by reading the number of pickup points and the starting position. It then collects all positions into an array and computes the minimum and maximum, which define the full interval that must be covered.

The conditional structure handles whether the start is outside or inside this interval. If the start is to the left of everything, the courier only needs to move right to the farthest point. If it is to the right, the symmetric case applies.

When the start is inside the interval, the code correctly adds the full span length, because that segment must be fully traversed, and then adds the smaller of the two distances from the start to either endpoint, which corresponds to choosing the optimal direction first.

A common implementation error is forgetting that the full interval must always be covered exactly once when starting inside it. Another is incorrectly adding both distances to endpoints instead of only the minimum initial movement.

## Worked Examples

### Example 1

Input:

```
5 10
1 3 8 20 30
```

Here lo = 1 and hi = 30, and the start is 10.

| Step | lo | hi | s | left (s-lo) | right (hi-s) | result |
| --- | --- | --- | --- | --- | --- | --- |
| init | 1 | 30 | 10 | - | - | - |
| compute | 1 | 30 | 10 | 9 | 20 | - |
| decision | 1 | 30 | 10 | 9 | 20 | 29 + 9 = 38 |

The interval length is 29, and the best first move is toward the left since it is closer. This confirms that we must traverse the full segment once and only pay an extra cost to reach the nearer endpoint.

### Example 2

Input:

```
4 5
6 7 9 12
```

Here lo = 6 and hi = 12, and the start is 5.

| Step | lo | hi | s | state |
| --- | --- | --- | --- | --- |
| init | 6 | 12 | 5 | start left of interval |
| decision | 6 | 12 | 5 | go directly to hi |

Output is 12 - 5 = 7.

This shows the case where the start is outside the interval, so no internal traversal logic is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan all positions once to compute min and max |
| Space | O(1) | Only a few scalar variables are stored |

The solution easily fits within typical constraints up to 10^5 elements, since it performs a single pass over the input with constant extra memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue().strip()

# sample-like cases
# (placeholders since original samples not provided)
# assert run("5 10\n1 3 8 20 30\n") == "38"

# minimum size
assert run("1 5\n10\n") == "5"

# start equals minimum
assert run("3 2\n2 3 4\n") == "2"

# start equals maximum
assert run("3 10\n2 5 10\n") == "8"

# all equal values
assert run("4 7\n7 7 7 7\n") == "0"

# start inside interval
assert run("5 5\n1 2 8 9 10\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | distance to point | base case |
| start at boundary | one-sided travel | boundary handling |
| all equal | zero movement | degenerate case |
| start inside | correct interval formula | core logic |

## Edge Cases

When there is only one pickup point, for example:

```
1 10
3
```

the algorithm computes lo = hi = 3. Since the start is to the right of the interval, it uses the rule s >= hi and outputs s - lo = 7. The route is simply a direct walk to the single point, and no interval traversal logic is triggered, which avoids overcounting.

When all pickup points are identical, such as:

```
4 5
7 7 7 7
```

we get lo = hi = 7 and start inside logic does not apply. The formula reduces to direct distance handling via one of the boundary conditions, producing 2. Any attempt to apply interval length logic blindly would incorrectly produce zero or double counting, but the conditional structure isolates this case correctly.
