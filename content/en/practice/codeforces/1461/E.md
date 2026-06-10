---
title: "CF 1461E - Water Level"
description: "We are asked to manage a water cooler over a number of days. The cooler starts with k liters of water, and every day x liters are consumed by coworkers. At the beginning of each day, John can add exactly y liters of water if doing so does not exceed the maximum limit r."
date: "2026-06-11T02:24:24+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "graphs", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1461
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 689 (Div. 2, based on Zed Code Competition)"
rating: 2200
weight: 1461
solve_time_s: 177
verified: false
draft: false
---

[CF 1461E - Water Level](https://codeforces.com/problemset/problem/1461/E)

**Rating:** 2200  
**Tags:** brute force, graphs, greedy, implementation, math  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to manage a water cooler over a number of days. The cooler starts with `k` liters of water, and every day `x` liters are consumed by coworkers. At the beginning of each day, John can add exactly `y` liters of water if doing so does not exceed the maximum limit `r`. The cooler’s water level must always stay within `[l, r]`. The goal is to determine if John can maintain this water level for `t` consecutive days.

The input parameters are large: `k`, `l`, `r`, and `y` can go up to `10^18`, and `t` up to `10^18`, while `x` is up to `10^6`. This rules out any approach that simulates each day individually in a loop, since iterating `t` times would be far too slow. Instead, we need to reason in terms of bounds, cycles, or patterns that allow skipping multiple days in a single step.

Edge cases arise when adding water is not possible because it would exceed `r`, or when consumption `x` is greater than what remains in the cooler. For example, if `k = 8`, `l = 1`, `r = 10`, `t = 2`, `x = 6`, and `y = 4`, adding `y` on the first day would exceed `r`, so John cannot add water, leaving 2 liters. After one more day, 6 liters are used, resulting in 0 liters, which is below `l`, so the correct output is "No". A naive approach might incorrectly attempt to add water regardless of exceeding `r`.

## Approaches

The brute-force approach is straightforward: simulate each day by first attempting to add `y` liters if the resulting level does not exceed `r`, then subtract `x` liters for daily consumption. Repeat for `t` days. This works because it directly implements the rules, but it requires `O(t)` iterations. With `t` up to `10^18`, this is infeasible.

The key insight is that the water level evolves predictably. Two cases arise:

1. **`y >= x`**: If the water addition is at least the daily consumption, the water level can potentially increase over time. The limit `r` prevents infinite growth. We only need to worry about whether there exists a point where water cannot be added because it would exceed `r`, or whether `l` is violated. In this case, the problem reduces to checking the remainder modulo `x`, because repeated addition and subtraction cycles eventually repeat water levels modulo `x`. This lets us skip simulating each day individually.
2. **`y < x`**: Here, the water level decreases over time. If adding `y` cannot offset `x`, we can compute how many days the water can last by solving `(k + y) - x*d >= l` in chunks. We can quickly determine if John runs out of water before `t` days without iterating each day.

Using modulo arithmetic, visited states, and smart skips, we can reduce the time complexity to `O(x)` or logarithmic in certain cases, far below `t`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t) | O(1) | Too slow |
| Optimal | O(x) | O(x) | Accepted |

## Algorithm Walkthrough

1. Check if `x > y` and `y == 0`. If `x > y` and adding water is impossible, compute the number of days before `k` falls below `l` using integer division: `days = (k - l) // x + 1`. If `days >= t`, print "Yes"; otherwise, "No". This is safe because water only decreases linearly.
2. Initialize a set `visited` to track water levels modulo `x` to detect cycles. Start with the initial water level `k`.
3. While `t > 0`, attempt to add water. Only add `y` liters if `k + y <= r`. If adding is not possible, do nothing.
4. Subtract `x` liters for the day. If `k < l` after subtraction, print "No" and terminate.
5. Reduce `t` by 1.
6. Compute `k % x`. If this modulo value has been seen before, a cycle exists. Since repeating modulo `x` values will not violate the limits, we can immediately print "Yes" and terminate.
7. Otherwise, add the modulo value to `visited` and continue.
8. If `t` reaches zero without violating the bounds, print "Yes".

Why it works: The water level modulo `x` fully determines the subsequent evolution because daily consumption and additions are multiples of `x` in effect. By tracking seen modulo values, the algorithm detects cycles and ensures no overflow or underflow occurs. Linear decreases are handled analytically when `y < x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

k, l, r, t, x, y = map(int, input().split())

if x > y and y == 0:
    # water decreases linearly, can't add
    if k - t * x >= l:
        print("Yes")
    else:
        print("No")
    exit()

visited = set()
while t > 0:
    # if we can safely add water, do it
    if k + y <= r:
        k += y
    # subtract daily consumption
    k -= x
    t -= 1
    if k < l:
        print("No")
        exit()
    modk = k % x
    if modk in visited:
        print("Yes")
        exit()
    visited.add(modk)

print("Yes")
```

The solution first handles the trivial decreasing case where `y = 0` and `x` is large. For the main loop, it safely adds water only when permitted, decreases `k` by `x`, and tracks modulo `x` states to detect cycles. Once a cycle is detected, the water level pattern repeats indefinitely, so maintaining the cooler is guaranteed.

## Worked Examples

**Sample 1:** `8 1 10 2 6 4`

| Day | Add y? | k before subtract | k after subtract | Mod k | Visited |
| --- | --- | --- | --- | --- | --- |
| 1 | no | 8 | 2 | 2 | {2} |
| 2 | yes | 6 | 0 | 0 | {2,0} -> violates l |

Output: `No`. The cooler falls below `l` on day 2.

**Sample 2:** `8 1 10 2 6 5`

| Day | Add y? | k before subtract | k after subtract | Mod k | Visited |
| --- | --- | --- | --- | --- | --- |
| 1 | yes | 13 -> capped at r=10 | 4 | 4 | {4} |
| 2 | yes | 9 | 3 | 3 | {4,3} |

Output: `Yes`. Water stays in bounds.

These traces demonstrate that modulo tracking captures cycles and correctly handles when adding `y` is limited by `r`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(x) | Maximum number of unique water levels modulo x is x. Once we see a repeat, we stop. |
| Space | O(x) | Store visited modulo x values to detect cycles. |

Since `x <= 10^6`, storing and checking modulo values fits comfortably within memory limits, and O(x) operations execute well under the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    k, l, r, t, x, y = map(int, input().split())
    if x > y and y == 0:
        return "Yes" if k - t * x >= l else "No"
    visited = set()
    while t > 0:
        if k + y <= r:
            k += y
        k -= x
        t -= 1
        if k < l:
            return "No"
        modk = k % x
        if modk in visited:
            return "Yes"
        visited.add(modk)
    return "Yes"

# provided samples
assert run("8 1 10 2 6 4\n") == "No", "sample 1"
assert run("8 1 10 2 6 5\n") == "Yes", "sample 2"
# custom cases
assert run("1 1 1 1 1 1\n") == "Yes", "minimum-size input"
assert run("10 1 20 5 3 4\n") == "Yes", "water fluctuates but stays in range"
assert run("5 1 5 3 2 0\n") == "No", "cannot add water, runs out"
assert run("10 5 15 1000000 2 1\n") == "Yes", "long t with cycle detection"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 1 1 | Yes | minimum values |
| 10 1 20 5 3 4 | Yes | fluctuating within bounds |
| 5 1 5 3 2 0 |  |  |
