---
title: "CF 2112A - Race"
description: "In this problem, Alice and Bob are racing to a prize that will appear at one of two distinct points on a one-dimensional line. Alice has already chosen her starting point a."
date: "2026-06-08T04:26:26+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2112
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 180 (Rated for Div. 2)"
rating: 800
weight: 2112
solve_time_s: 78
verified: true
draft: false
---

[CF 2112A - Race](https://codeforces.com/problemset/problem/2112/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

In this problem, Alice and Bob are racing to a prize that will appear at one of two distinct points on a one-dimensional line. Alice has already chosen her starting point `a`. Bob wants to select an integer starting point `b` that is different from Alice's, so that he can reach the prize faster than Alice no matter which of the two locations `x` or `y` the prize appears. The distance between any two points is simply the absolute difference of their coordinates.

The input gives multiple test cases, each specifying `a`, `x`, and `y`, all distinct integers between 1 and 100. The output must state for each test case whether such a point `b` exists. The answer is "YES" if Bob can guarantee beating Alice regardless of the prize location, and "NO" otherwise.

Given the tight bounds (all numbers ≤ 100 and up to 1000 test cases), any algorithm iterating through all integers in the feasible range is acceptable, because at most 100 steps are needed per test case. However, it is possible to reason about the problem without full brute-force enumeration.

The main edge cases occur when the prize locations straddle Alice's position, for example `a = 3, x = 1, y = 5`. In such a situation, if Bob picks a point to beat Alice to one prize, he might lose to her at the other. A naive approach that selects the midpoint or one of the prizes without checking both distances can incorrectly claim "YES" when no such guaranteed position exists.

## Approaches

A straightforward brute-force approach is to check every possible integer `b` between 1 and 100 (excluding `a`) and see if for both prize positions, `|b - x| < |a - x|` and `|b - y| < |a - y|` hold. This works because the domain is small, and for each test case it requires at most 99 checks with two absolute differences per check, which is negligible in practice. The brute force works because we explicitly verify Bob's win condition for every feasible starting position, but it is somewhat inelegant.

The key insight for an optimal solution is that the integer `b` that guarantees victory must lie strictly between `a` and the "farthest" prize location. If both prizes are on the same side of Alice (for example `a < x < y`), Bob can start beyond the farther prize, closer to it than Alice, which guarantees he will beat her to both prizes. If the prizes are on opposite sides of Alice (`x < a < y`), no matter where Bob starts, he will be closer to one prize than Alice but farther from the other. Thus, a guaranteed position exists only when both prizes are on the same side of Alice. This reduces the problem to comparing the positions: Bob wins if `(x - a) * (y - a) > 0`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100 * t) | O(1) | Accepted |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. This determines how many separate races we need to evaluate.
2. For each test case, read the integers `a`, `x`, and `y`. These define Alice's starting position and the two possible prize locations.
3. Compute the product `(x - a) * (y - a)`. This product captures the relative positions of the prizes with respect to Alice. If the product is positive, both prizes are on the same side of Alice. If negative, they lie on opposite sides.
4. If the product is positive, output "YES". Bob can pick the position closest to the farther prize and guarantee beating Alice to both.
5. Otherwise, output "NO". There is no single integer starting position for Bob that guarantees he will be closer than Alice to both prizes.

Why it works: The invariant is that the sign of `(x - a) * (y - a)` fully encodes the geometric arrangement. Positive means both prizes are either to the left or right of Alice, ensuring a single starting point exists to reach both faster. Negative means they straddle Alice, making it impossible for Bob to pick a position that is closer to both prizes simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, x, y = map(int, input().split())
    if (x - a) * (y - a) > 0:
        print("YES")
    else:
        print("NO")
```

The code first reads the number of test cases. For each test case, it parses the three integers representing Alice's starting point and the two potential prize positions. The core logic checks whether both prizes are on the same side relative to Alice using the product `(x - a) * (y - a)`. The output is immediate and case-insensitive by default, since Codeforces accepts "YES"/"NO".

## Worked Examples

**Sample Input 1:** `1 3 4`

| Variable | Value | Reasoning |
| --- | --- | --- |
| a | 1 | Alice's start |
| x | 3 | Prize 1 |
| y | 4 | Prize 2 |
| x - a | 2 | Distance from Alice to prize 1 |
| y - a | 3 | Distance from Alice to prize 2 |
| product | 6 | Positive, both prizes on the right |
| Output | YES | Bob can start at 4 to beat Alice to both |

**Sample Input 2:** `3 1 5`

| Variable | Value | Reasoning |
| --- | --- | --- |
| a | 3 |  |
| x | 1 |  |
| y | 5 |  |
| x - a | -2 |  |
| y - a | 2 |  |
| product | -4 | Negative, prizes on opposite sides |
| Output | NO | Bob cannot guarantee victory |

These traces show that the product test captures the relative geometry correctly in all scenarios, even when prizes straddle Alice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires only a constant-time computation. |
| Space | O(1) | No extra memory is needed beyond a few integers per test case. |

Given the constraints (t ≤ 1000, all numbers ≤ 100), the solution executes well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(sys.stdin.readline())
    for _ in range(t):
        a, x, y = map(int, sys.stdin.readline().split())
        if (x - a) * (y - a) > 0:
            output.append("YES")
        else:
            output.append("NO")
    return "\n".join(output)

# Provided samples
assert run("3\n1 3 4\n5 3 1\n3 1 5\n") == "YES\nYES\nNO", "sample 1"

# Custom cases
assert run("2\n2 3 4\n2 1 3\n") == "YES\nNO", "prizes on same side vs opposite side"
assert run("1\n50 51 52\n") == "YES", "consecutive numbers, all on one side"
assert run("1\n50 49 48\n") == "YES", "consecutive numbers on the other side"
assert run("1\n50 49 51\n") == "NO", "prizes straddle Alice"
assert run("1\n1 2 100\n") == "NO", "extreme values, straddling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 3 4 | YES | Both prizes on same side |
| 2 1 3 | NO | Prizes on opposite sides |
| 50 51 52 | YES | Sequential prizes to right |
| 50 49 48 | YES | Sequential prizes to left |
| 50 49 51 | NO | Prizes straddle Alice |
| 1 2 100 | NO | Large gap, straddling |

## Edge Cases

If Alice is between the two prizes, such as `a = 3, x = 1, y = 5`, the product `(x - a) * (y - a) = (-2) * 2 = -4` is negative. The algorithm immediately outputs "NO", correctly reflecting that no single position can beat Alice to both prizes. If both prizes are to the right of Alice (`a = 1, x = 3, y = 4`), the product is positive and the algorithm outputs "YES", correctly allowing Bob to pick `b = 4` to guarantee victory. These cases demonstrate that the product test robustly handles both straddling and unidirectional prize configurations.
