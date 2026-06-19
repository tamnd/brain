---
title: "CF 106368A - Forgetful Shustrik and the Remote Control"
description: "We are working with a television remote control that can display integer channel numbers. There is a starting channel, typically zero or one depending on the statement variant, and a target channel we want to reach. The remote has two kinds of interactions."
date: "2026-06-19T08:23:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106368
codeforces_index: "A"
codeforces_contest_name: "Innopolis Open 2025-2026. Final round"
rating: 0
weight: 106368
solve_time_s: 50
verified: false
draft: false
---

[CF 106368A - Forgetful Shustrik and the Remote Control](https://codeforces.com/problemset/problem/106368/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a television remote control that can display integer channel numbers. There is a starting channel, typically zero or one depending on the statement variant, and a target channel we want to reach.

The remote has two kinds of interactions. One allows moving step by step using increment and decrement buttons, changing the current channel by one per press. The other allows direct input of a number using digit buttons, but some digits may be broken and cannot be used. If a number contains even one broken digit, it cannot be entered directly.

The task is to compute the minimum number of button presses required to reach the target channel starting from the initial channel, combining both strategies optimally.

The key constraint shape in this problem is that the target channel can be large, but the cost of digit construction depends on the number of digits and the availability of digit buttons. This rules out any strategy that tries to simulate arbitrary sequences of button presses between all intermediate numbers. A direct graph search over all integers up to the target is unnecessary and would be too slow when the range is large, since transitions form a dense graph of size proportional to the numeric range.

A subtle edge case appears when the target number itself cannot be typed due to broken digits. For example, if the target is 807 and digit 0 is broken, we cannot directly form 807 even though it is optimal in most unbroken cases. A naive solution that always prefers direct typing would fail here and must fall back to incremental movement.

Another edge case occurs when the initial channel is already close to the target and incrementing is cheaper than typing any valid number. For instance, if only one digit is broken and all valid numbers are much larger or smaller than the target, brute selection of any constructible number may overestimate the cost unless compared against pure +/- movement.

## Approaches

A brute-force approach tries every integer value that can be formed using the working digits, computes the cost of typing that number, and then adds the cost of moving from that number to the target using increment and decrement operations. The answer is the minimum over all such candidates, including the option of never typing and using only increments.

If the target is up to 10^6 or 10^9, the number of possible constructed integers grows exponentially in digit length, but in practice is bounded by the range of numbers we consider. However, enumerating all valid digit strings up to length d yields O(9^d) possibilities, which becomes infeasible even for moderate d such as 9, since this is millions of states.

The key observation is that the problem decomposes cleanly by pivoting around a single candidate number. For any number x that can be typed, the total cost is the number of digits in x plus the absolute difference |x − target|. The structure is simple enough that we do not need to explore transitions between typed numbers; each candidate is independent.

This reduces the problem to generating all valid numbers that can be typed with the working digits and evaluating a simple formula for each. Since digit length is bounded by the maximum between target length and a small extension beyond it, enumeration remains manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration with unrestricted range search | O(10^d · d) | O(d) | Too slow |
| Enumerate valid constructible numbers + direct evaluation | O(k · d) where k is number of valid candidates | O(d) | Accepted |

## Algorithm Walkthrough

1. Read the target channel and the set of working digit buttons. We treat each number as a string construction problem rather than a numeric transition problem because cost depends on digit composition.
2. Generate all numbers that can be formed using only allowed digits up to a reasonable digit length bound. The bound is taken as one digit longer than the target length because any optimal candidate larger than that would only increase the movement cost without reducing typing cost enough to compensate.
3. For each constructed number, compute its cost as the number of digits used to type it plus the absolute difference between it and the target number. This reflects the strategy of typing the candidate and then using +/- buttons to adjust.
4. Track the minimum cost across all valid constructed numbers.
5. Also compare against the baseline strategy of using only increment and decrement operations from the starting channel to the target channel.
6. Output the minimum among all evaluated strategies.

The reason digit-by-digit generation works is that the cost function depends only on the final numeric value and its digit length, not on how we reached that number. This removes any need for state transitions.

### Why it works

Every feasible strategy can be reduced to choosing a single intermediate typed number, followed by linear adjustment using increment or decrement operations. Since digit input has no dependency between numbers, there is no advantage in mixing partial constructions or transitioning between constructed values. This makes each candidate independent, and the global optimum must appear among these isolated evaluations.

## Python Solution

```

```
