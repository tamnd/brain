---
title: "CF 105859J - Hill Climb Racing"
description: "We are given a one-dimensional terrain described by heights at evenly spaced points. The car moves from the leftmost point to the rightmost point, stepping from index 0 to index 1, then 1 to 2, and so on until index l. Each step corresponds to moving one meter horizontally."
date: "2026-06-25T14:42:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105859
codeforces_index: "J"
codeforces_contest_name: "Mines HSPC 2025 Open Division"
rating: 0
weight: 105859
solve_time_s: 37
verified: true
draft: false
---

[CF 105859J - Hill Climb Racing](https://codeforces.com/problemset/problem/105859/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional terrain described by heights at evenly spaced points. The car moves from the leftmost point to the rightmost point, stepping from index 0 to index 1, then 1 to 2, and so on until index l. Each step corresponds to moving one meter horizontally.

The key restriction is on how steeply the terrain rises between consecutive points. If the height increases too sharply from position i to i+1, the car may not have enough acceleration to climb that segment. Formally, the car can only handle upward changes in height up to a fixed limit a per step. If the next point is lower, descending is always allowed regardless of magnitude.

The task is to determine whether every consecutive pair of points can be traversed under this rule. If even one upward step exceeds the allowed increase, the whole route becomes impossible.

The input size goes up to 10^6 positions, which forces the solution to be strictly linear in the number of height samples. Any solution that attempts recomputing paths, using nested comparisons, or simulating physical movement beyond simple adjacent checks would time out. The only feasible approach is a single pass over the array computing local differences.

A subtle edge case arises when heights oscillate. For example, a sequence like 0 5 1 5 0 with a small a may look manageable globally, but only one upward jump determines failure. Another case is when all rises are small individually but accumulated intuition might mislead: there is no accumulation, only per-step constraints.

Another corner case is strictly decreasing terrain such as 10 1 0 0 0. Even with a very small acceleration, this is always valid because downward movement imposes no restriction.

## Approaches

A brute-force mindset would simulate the car’s traversal and, for each step, check whether it can climb from the current point to the next. In its most literal form, this still requires only scanning adjacent pairs once, but one might incorrectly assume that more complex reasoning is needed, such as tracking energy, maintaining a slope profile, or considering longer segments. Those interpretations quickly become unnecessary because the rule is purely local: only h[i+1] - h[i] matters when positive.

The naive incorrect direction would be to try computing maximum slope over larger windows or attempt to smooth the terrain, which would lead to O(l^2) or worse behavior if implemented literally.

The correct observation is that feasibility is determined independently at each step. The car only fails when it encounters a single transition where the upward jump exceeds a. This reduces the entire problem to finding whether the maximum positive difference between consecutive elements is at most a.

We therefore compute all adjacent differences and track the maximum upward slope. If any one exceeds a, the answer is immediate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Check all adjacent pairs | O(l) | O(1) | Accepted |
| Any global or window-based method | O(l^2) or O(l log l) | O(l) | Too slow / unnecessary |

## Algorithm Walkthrough

1. Read l and a, then read the array h of length l+1 representing heights along the track.
2. Initialize a variable max_up as 0 to store the largest upward jump seen so far.
3. Iterate i from 0 to l-1, examining each consecutive pair h[i] and h[i+1].
4. Compute the difference h[i+1] - h[i]. If this value is positive, compare it with max_up and update max_up if it is larger.
5. After processing all pairs, compare max_up with a. If max_up is greater than a, output "BUG REPORT".
6. Otherwise, output "POSSIBLE".

The reason this works is that every valid traversal depends only on whether each local ascent is feasible. Downward moves impose no constraint and can be ignored entirely. The algorithm reduces the terrain to its worst upward step, and feasibility depends solely on that single extremal value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    l, a = map(int, input().split())
    h = list(map(int, input().split()))

    max_up = 0

    for i in range(l):
        diff = h[i + 1] - h[i]
        if diff > 0:
            if diff > max_up:
                max_up = diff

    if max_up > a:
        print("BUG REPORT")
    else:
        print("POSSIBLE")

if __name__ == "__main__":
    solve()
```

The implementation is a direct translation of the observation that only upward differences matter. The loop runs exactly l times, comparing adjacent elements once. The variable max_up captures the single critical statistic that determines success.

A common mistake here is to take absolute differences. That would incorrectly penalize downhill movement, which the problem explicitly allows without restriction. Another mistake is using prefix maxima or attempting to “simulate” vehicle motion beyond adjacent comparisons, which introduces unnecessary complexity without affecting correctness.

## Worked Examples

### Example 1

Input:

```
4 3
1 2 5 1 1
```

| i | h[i] | h[i+1] | diff | max_up |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 1 | 1 |
| 1 | 2 | 5 | 3 | 3 |
| 2 | 5 | 1 | -4 | 3 |
| 3 | 1 | 1 | 0 | 3 |

The largest upward jump is 3, which matches a. The path is exactly at the limit, so it is valid and the output is POSSIBLE.

### Example 2

Input:

```
4 3
0 3 1 5 0
```

| i | h[i] | h[i+1] | diff | max_up |
| --- | --- | --- | --- | --- |
| 0 | 0 | 3 | 3 | 3 |
| 1 | 3 | 1 | -2 | 3 |
| 2 | 1 | 5 | 4 | 4 |
| 3 | 5 | 0 | -5 | 4 |

Here the maximum upward step is 4, which exceeds a = 3. The car gets stuck at the transition from 1 to 5, so the correct output is BUG REPORT.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(l) | Each adjacent pair is checked once in a single pass over the array |
| Space | O(1) | Only a single variable tracks the maximum upward slope |

The constraints allow up to 10^6 height values, so a linear scan is necessary. Any algorithm requiring sorting or nested traversal would be too slow, but this solution performs only a constant amount of work per element.

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

# provided samples
assert run("4 3\n1 2 5 1 1\n") == "POSSIBLE"
assert run("4 3\n0 3 1 5 0\n") == "BUG REPORT"
assert run("3 1000000\n0 999999 1 1000000\n") == "POSSIBLE"

# minimum size (single step)
assert run("1 5\n0 10\n") == "BUG REPORT"

# all equal heights
assert run("3 1\n5 5 5 5\n") == "POSSIBLE"

# strictly decreasing
assert run("4 1\n10 7 3 1 0\n") == "POSSIBLE"

# tight boundary case
assert run("2 2\n1 3 1\n") == "POSSIBLE"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single rise exceeds limit | BUG REPORT | minimal failing case |
| flat terrain | POSSIBLE | no upward constraint triggered |
| decreasing sequence | POSSIBLE | downhill is unrestricted |
| exact boundary equality | POSSIBLE | equality is allowed |

## Edge Cases

A single-step terrain like `0 10` immediately exposes whether the implementation correctly focuses only on adjacent differences. The algorithm computes one upward jump of 10 and compares it to a.

A flat terrain such as `5 5 5 5` produces only zero differences. The max_up remains zero, so any non-negative acceleration passes.

A strictly descending sequence like `10 7 3 1 0` tests that negative differences are ignored entirely. Even if the terrain is steep downward, no constraint is violated.

A boundary equality case like `1 3 1` with a = 2 confirms that the condition is inclusive. The algorithm records max_up = 2 and correctly accepts the path without rejecting equality.
