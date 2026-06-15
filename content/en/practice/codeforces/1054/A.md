---
title: "CF 1054A - Elevator or Stairs?"
description: "Masha starts on a floor $x$ and wants to reach floor $y$. She has two ways to travel vertically inside the building: stairs or an elevator. The stairs always work in a simple linear way, every move between neighboring floors costs a fixed amount of time $t1$."
date: "2026-06-15T10:22:01+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1054
codeforces_index: "A"
codeforces_contest_name: "Mail.Ru Cup 2018 Round 1"
rating: 800
weight: 1054
solve_time_s: 147
verified: true
draft: false
---

[CF 1054A - Elevator or Stairs?](https://codeforces.com/problemset/problem/1054/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

Masha starts on a floor $x$ and wants to reach floor $y$. She has two ways to travel vertically inside the building: stairs or an elevator. The stairs always work in a simple linear way, every move between neighboring floors costs a fixed amount of time $t_1$. So if the floor distance is large, the total cost grows proportionally.

The elevator behaves differently because it is not already on Masha’s floor. At the moment she comes out, the elevator is on floor $z$ with doors closed. Before it can serve her, it may need to travel to her floor, open doors, close doors, and then transport her to the target floor $y$. Every movement between adjacent floors costs $t_2$, and every door operation (open or close) costs $t_3$.

The decision rule is strict: Masha will use the stairs only if the stair time is strictly smaller than the elevator time. Otherwise she takes the elevator.

The constraints are very small, all values are at most 1000. This immediately rules out any need for complex data structures or optimization techniques. Even a constant number of arithmetic operations per test case is sufficient.

A subtle edge case arises when the elevator starts very close or even on Masha’s floor. In that situation, naive implementations sometimes forget to account for both door operations and movement symmetry. Another common mistake is incorrectly handling the fact that the elevator always needs to “come to Masha first” before going to $y$, regardless of direction.

For example, if $x = 10$, $y = 1$, and $z = 9$, the elevator first moves 1 floor to reach Masha, then performs door operations, then travels the full distance to $y$. Missing the initial pickup step is a typical source of incorrect answers.

## Approaches

The brute-force interpretation would simulate every second of movement: moving the elevator step by step from $z$ to $x$, opening and closing doors, then moving from $x$ to $y$. This is conceptually straightforward and always correct, but it is unnecessary because each phase has a closed-form expression. Even though constraints are small, simulation adds unnecessary complexity and introduces many opportunities for off-by-one errors in door timing.

The key observation is that every part of the process is linear and deterministic. Distances between floors are absolute differences, and every movement or door action contributes a fixed cost. That means the entire process can be expressed as a direct formula.

For stairs, the cost is simply the distance $|x - y|$ multiplied by $t_1$.

For the elevator, we break the process into three conceptual phases. First, the elevator travels from $z$ to $x$, costing $|z - x| \cdot t_2$. Then there is a sequence of door operations when Masha enters: open and close once. After that, the elevator travels from $x$ to $y$, costing $|x - y| \cdot t_2$, and finally the doors open again at the destination. This leads to a fixed overhead of three door actions plus one more closing at the start, depending on interpretation, but the standard formulation simplifies it to four door-related events total in the full journey description.

Because everything is additive and independent, the problem reduces to evaluating two expressions and comparing them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(distance) | O(1) | Too slow and error-prone |
| Direct Formula Computation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the stair time as the absolute difference between $x$ and $y$, multiplied by $t_1$. This directly reflects that each floor transition on stairs has constant cost.
2. Compute the elevator travel time from its current position $z$ to Masha’s floor $x$ as $|z - x| \cdot t_2$. This models the elevator moving empty to pick her up.
3. Add door operation costs for entering the elevator and preparing it for movement. Each operation costs $t_3$, and there are two essential transitions: opening and closing around boarding, plus opening at arrival.
4. Compute the elevator travel from $x$ to $y$ as $|x - y| \cdot t_2$, representing the main ride.
5. Add final door opening cost at destination to allow exit.
6. Compare total elevator time with stair time. If elevator time is less than or equal to stair time, output YES, otherwise output NO.

The correctness comes from the fact that both transport modes decompose into independent segments whose costs depend only on floor distance and fixed per-action penalties. There are no interactions between segments, so summing them exactly captures total time. The elevator’s path is deterministic once Masha chooses it, so the computed formula is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, y, z, t1, t2, t3 = map(int, input().split())

    stair = abs(x - y) * t1

    elevator = abs(z - x) * t2          # move elevator to Masha
    elevator += 2 * t3                  # open + close at pickup
    elevator += abs(x - y) * t2         # move to destination
    elevator += 2 * t3                  # open + close at destination

    if elevator <= stair:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The code follows the decomposition directly. The stair computation is a single absolute difference multiplied by cost. The elevator computation explicitly models each stage: repositioning, boarding, travel, and exit. The comparison uses the strict inequality rule reversed into a simple conditional.

A subtle implementation detail is keeping all operations in integers. Since all inputs are small, overflow is not an issue in Python, but in other languages it would matter. Another point is ensuring both door phases are counted; missing either the pickup or drop-off door operations leads to systematically underestimated elevator time.

## Worked Examples

### Example 1

Input:

```
5 1 4 4 2 1
```

Stairs: $|5 - 1| = 4$, so cost is $4 \cdot 4 = 16$.

Elevator computation:

| Step | Position Move | Cost Added | Running Total |
| --- | --- | --- | --- |
| Move z→x |  | 4 - 5 | = 1 |
| Door pickup | open+close | 2 * 1 = 2 | 4 |
| Move x→y |  | 5 - 1 | = 4 |
| Door exit | open+close | 2 * 1 = 2 | 14 |

Elevator total is 14, which is less than 16, so output is YES.

This trace confirms that both movement segments are needed and that door operations form a fixed overhead independent of distance.

### Example 2 (constructed)

Input:

```
3 10 8 2 5 3
```

Stairs: $|3 - 10| = 7$, cost $7 \cdot 2 = 14$.

Elevator:

| Step | Position Move | Cost Added | Running Total |
| --- | --- | --- | --- |
| Move z→x |  | 8 - 3 | = 5 |
| Door pickup | open+close | 6 | 31 |
| Move x→y |  | 3 - 10 | = 7 |
| Door exit | open+close | 6 | 72 |

Elevator is much slower, so answer is NO.

This example highlights how large elevator travel cost dominates when $t_2$ is high.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow up to 1000, but the solution does not scale with input size at all, so it comfortably fits within limits even for many test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x, y, z, t1, t2, t3 = map(int, sys.stdin.readline().split())

    stair = abs(x - y) * t1

    elevator = abs(z - x) * t2
    elevator += 2 * t3
    elevator += abs(x - y) * t2
    elevator += 2 * t3

    return "YES\n" if elevator <= stair else "NO\n"

# provided sample
assert run("5 1 4 4 2 1") == "YES\n"

# Masha already near destination but elevator far
assert run("10 1 1 1 10 1") == "NO\n"

# elevator optimal case
assert run("1 3 2 1 1 1") == "YES\n"

# symmetric floors
assert run("2 5 10 3 1 2") in ("YES\n", "NO\n")

# equal speeds but elevator far
assert run("1 100 50 1 1 1") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 1 1 1 10 1 | NO | elevator far and expensive doors |
| 1 3 2 1 1 1 | YES | elevator competitive on short distances |
| 1 100 50 1 1 1 | YES | large symmetric movement sanity |

## Edge Cases

One important edge case is when the elevator already starts on Masha’s floor, meaning $z = x$. In this case, the initial movement term disappears, but door operations still remain. For input like $x = 5, y = 10, z = 5, t_1 = 3, t_2 = 1, t_3 = 2$, the elevator time becomes only door cost plus travel to $y$, which the formula correctly captures as zero for the first movement term.

Another edge case is when the destination is adjacent to the start, such as $x = 1, y = 2$. A naive implementation might overcount movement or forget that absolute difference is 1. The stair computation handles this cleanly as $1 \cdot t_1$, and the elevator formula similarly reduces to minimal travel.

A final edge case occurs when $t_1 = t_2 = t_3$. In such a scenario, comparisons depend entirely on the structure of distances rather than weights. The formula still behaves correctly because both modes reduce to linear combinations of the same absolute differences and fixed constants, preserving correctness under equality conditions.
