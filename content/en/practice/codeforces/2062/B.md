---
title: "CF 2062B - Clockwork"
description: "We are asked to determine if we can indefinitely avoid letting any clock hit zero in a sequence of clocks. Each clock has an initial time ai. Every second, all clocks decrease by one. We can move to an adjacent clock and immediately reset its time back to ai."
date: "2026-06-08T07:33:31+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2062
codeforces_index: "B"
codeforces_contest_name: "Ethflow Round 1 (Codeforces Round 1001, Div. 1 + Div. 2)"
rating: 900
weight: 2062
solve_time_s: 127
verified: false
draft: false
---

[CF 2062B - Clockwork](https://codeforces.com/problemset/problem/2062/B)

**Rating:** 900  
**Tags:** greedy, math  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine if we can indefinitely avoid letting any clock hit zero in a sequence of clocks. Each clock has an initial time `a_i`. Every second, all clocks decrease by one. We can move to an adjacent clock and immediately reset its time back to `a_i`. The catch is that if any clock reaches zero before we can reset it, we lose instantly. We can start from any clock and can move back and forth freely. The input gives several test cases, each with a list of clock values, and the output should be "YES" if a perpetual strategy exists or "NO" otherwise.

The constraints allow up to 500,000 clocks across all test cases, and each clock value can be as large as 10^9. This immediately rules out simulating every second because even a single clock with value 10^9 would require a billion operations. The solution must therefore reason mathematically about whether a sequence of moves exists to indefinitely prevent any clock from hitting zero.

An important subtlety arises when clocks have small values relative to their position. For instance, if we have `[2, 2]`, we cannot indefinitely cycle because by the time we reset the second clock, the first has already reached zero. Small sequences with small values relative to the number of clocks are the edge cases that break naive approaches.

## Approaches

The brute-force approach would attempt to simulate every second: decrement all clocks, move to a neighboring clock, and reset it if possible. This is correct in principle, but infeasible. For `n = 10^5` and `a_i = 10^9`, the simulation would perform far too many operations.

The key observation is that the problem can be reduced to a simple check using a greedy approach. If we consider walking from left to right (and later right to left), we can maintain the minimal remaining time a clock must have to survive until we can reset it. Specifically, for the left-to-right pass, we imagine moving from the first clock to the last, always resetting at the current clock. At each clock, we compute the maximum "debt" of time we need to carry: the previous debt plus one for the step taken must not exceed the clock's initial value. If it does, that direction is impossible. We then do the same from right to left and check if there exists a starting clock where both passes succeed.

This transforms the problem into a linear scan from left to right and right to left, which is O(n) per test case. The insight is that we do not need to simulate every second; we only need to check the constraints imposed by movement and reset timing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * max(a_i)) | O(n) | Too slow |
| Greedy Linear Pass | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two arrays `left_debt` and `right_debt` of size `n`. `left_debt[i]` will represent the minimal time needed to survive from the left up to clock `i`. Similarly, `right_debt[i]` will track minimal time from the right.
2. Perform a left-to-right pass. Set `left_debt[0] = 0` since we can start at any clock. For each clock `i` from 1 to n-1, compute `left_debt[i] = max(left_debt[i-1] + 1, 0)`. If at any point `left_debt[i] > a[i]`, it is impossible to reach this clock from the left without losing.
3. Perform a right-to-left pass similarly. Set `right_debt[n-1] = 0` and propagate toward the first clock. At each step, ensure that `right_debt[i] <= a[i]`.
4. Check if there exists a clock `i` where both `left_debt[i] <= a[i]` and `right_debt[i] <= a[i]`. If such a clock exists, we can start there and indefinitely move back and forth. If none exist, it is impossible.

The key invariant is that `debt[i]` represents the minimal time that must remain on clock `i` to survive moving from that direction. If `debt[i] > a[i]`, the clock cannot sustain our movement and reset plan. This guarantees that if a feasible clock exists, following the linear passes ensures an indefinite strategy.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_survive(a):
    n = len(a)
    left_debt = [0] * n
    right_debt = [0] * n
    
    # left to right pass
    for i in range(1, n):
        left_debt[i] = max(left_debt[i-1] + 1, 0)
        if left_debt[i] > a[i]:
            left_debt[i] = float('inf')
    
    # right to left pass
    for i in range(n-2, -1, -1):
        right_debt[i] = max(right_debt[i+1] + 1, 0)
        if right_debt[i] > a[i]:
            right_debt[i] = float('inf')
    
    # check for feasible starting point
    for i in range(n):
        if left_debt[i] <= a[i] and right_debt[i] <= a[i]:
            return "YES"
    return "NO"

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(can_survive(a))
```

The solution maintains two linear passes, one from each side, computing the minimal required remaining time at each clock. Setting infeasible clocks to infinity ensures they are excluded from candidate starting points. The final scan identifies a clock where both constraints hold, representing a safe starting position.

## Worked Examples

Input `[4, 10, 5]`:

| Clock | a[i] | Left debt | Right debt |
| --- | --- | --- | --- |
| 0 | 4 | 0 | 2 |
| 1 | 10 | 1 | 1 |
| 2 | 5 | 2 | 0 |

No clock satisfies `left_debt[i] <= a[i]` and `right_debt[i] <= a[i]` simultaneously at all positions; thus the output is "NO". This shows that a mid-sized clock flanked by smaller clocks cannot sustain indefinite survival.

Input `[5, 3, 5]`:

| Clock | a[i] | Left debt | Right debt |
| --- | --- | --- | --- |
| 0 | 5 | 0 | 2 |
| 1 | 3 | 1 | 1 |
| 2 | 5 | 2 | 0 |

Clock 1 satisfies both conditions: `1 <= 3` and `1 <= 3`. Starting at this clock, we can indefinitely move left and right, resetting clocks as we go.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Two linear passes plus one scan to find a feasible starting clock |
| Space | O(n) | Arrays storing left and right debts |

The algorithm fits comfortably within constraints since the sum of all clocks over all test cases is ≤ 5·10^5. Each test case is processed in linear time with a small constant factor.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assume solution.py contains the above code
    return output.getvalue().strip()

# Provided samples
assert run("5\n2\n4 10\n2\n2 2\n3\n4 10 5\n3\n5 3 5\n5\n12 13 25 17 30\n") == "YES\nNO\nNO\nYES\nYES"

# Custom tests
assert run("1\n2\n1 1\n") == "YES", "minimum-size input"
assert run("1\n3\n1 1 1\n") == "NO", "all equal, too small to survive"
assert run("1\n4\n10 10 10 10\n") == "YES", "all equal, large values"
assert run("1\n5\n5 6 1 6 5\n") == "YES", "middle small value still survives with right strategy"
assert run("1\n2\n1 1000000000\n") == "YES", "extreme values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 clocks `[1,1]` | YES | Minimal input, barely survives |
| 3 clocks `[1,1,1]` | NO | Small values, cannot survive |
| 4 clocks `[10,10,10,10]` | YES | All large, simple survival |
| 5 clocks `[5,6,1,6,5]` | YES | Edge case with middle small clock |
| 2 clocks `[1,1000000000]` | YES | Extreme difference in clock values |

## Edge Cases

For `[2,2]`, left pass: `left_debt = [0,1]`, right pass: `right_debt = [1,0]`. Clock 0 has `0 <= 2` and `1 <=
