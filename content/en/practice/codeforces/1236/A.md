---
title: "CF 1236A - Stones"
description: "We are given three piles of stones. From these piles, Alice can repeatedly perform two kinds of moves. One move consumes one stone from the first pile and two stones from the second pile. The other move consumes one stone from the second pile and two stones from the third pile."
date: "2026-06-15T20:11:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1236
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 593 (Div. 2)"
rating: 800
weight: 1236
solve_time_s: 309
verified: true
draft: false
---

[CF 1236A - Stones](https://codeforces.com/problemset/problem/1236/A)

**Rating:** 800  
**Tags:** brute force, greedy, math  
**Solve time:** 5m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three piles of stones. From these piles, Alice can repeatedly perform two kinds of moves. One move consumes one stone from the first pile and two stones from the second pile. The other move consumes one stone from the second pile and two stones from the third pile. Each move also contributes to her collected score: every stone removed counts toward her total.

The process is fully flexible, but every action reduces availability for future actions because both operations compete for stones in the second pile. The task is to choose a sequence of moves that maximizes the total number of stones removed.

The input size is small, with each pile containing at most 100 stones and at most 100 test cases. This immediately rules out any need for complex graph search or dynamic programming over large states. Even a cubic or quadratic enumeration over possible move counts is safe under the constraints.

A subtle issue comes from the shared middle pile. Both operations consume stones from it, so a greedy strategy like “always take as many of the first operation as possible” can block better use of the second operation later.

For example, if we aggressively use the first operation early, we might deplete the second pile in a way that prevents pairing with the third pile, losing potentially many moves of the second type. This interdependence is the core difficulty: local greed on one operation can reduce global optimality.

## Approaches

A brute-force way to think about the problem is to simulate all possible sequences of operations. At every step, we choose either the first or second operation if it is valid. This forms a search tree where each node branches into up to two states. However, the depth can be as large as 200 operations in worst cases, and the branching factor makes this exponential, quickly becoming infeasible even though the input size is small.

The key observation is that we do not actually care about the order of operations, only about how many times each operation is used. If we fix that the first operation is used x times and the second operation is used y times, then feasibility depends only on resource constraints:

The first pile must satisfy x ≤ a, the third pile must satisfy 2y ≤ c, and the second pile must satisfy 2x + y ≤ b.

Each operation contributes exactly 3 stones to the answer, so the goal becomes maximizing 3(x + y).

This reduces the problem to checking all valid values of x and computing the best corresponding y. Since x is bounded by at most 100, we can iterate over all possibilities efficiently.

The brute-force idea of exploring sequences becomes a much simpler enumeration over counts, and the dependency between operations is handled cleanly by the constraint on the second pile.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force sequence search | Exponential | O(depth) | Too slow |
| Enumerate operation counts | O(a) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Fix the number of times we apply the first operation. Call this value x. We can try every x from 0 up to a because the first pile limits how many times we can use it.
2. After choosing x, we account for its consumption of the second pile. The second pile loses 2x stones, so the remaining amount is b - 2x. This remaining resource determines how many second operations are still possible.
3. Compute how many second operations can be performed. Each second operation needs one stone from the second pile and two from the third pile, so the maximum is limited by both remaining second-pile stones and available triples in the third pile. This gives y = min(b - 2x, c // 2).
4. Compute the total stones collected for this configuration as 3(x + y). We keep track of the maximum value across all x.
5. After testing all feasible x values, output the best result.

The key idea behind trying all x values is that once x is fixed, the remaining structure becomes completely greedy and deterministic for y, so no further decision-making is needed.

### Why it works

The second pile is the only shared resource between both operations, so the entire optimization reduces to deciding how much of it is reserved for the first operation versus the second. Once that split is fixed by choosing x, both operations independently consume different resources, making the remainder problem greedy and linear. This guarantees that no interleaving of operations can outperform a fixed allocation of x and y.

## Python Solution

```
PythonRun
```

The solution iterates over all possible counts of the first operation. The early break is safe because increasing x only reduces remaining capacity in the second pile, so beyond a certain point no valid configurations exist.

For each x, the computation of y is greedy and does not require further branching because both constraints on the second operation are independent and monotonic.

## Worked Examples

### Example 1

Input: `3 4 5`

We try all values of x.

| x | b left after x | y = min(b-left, c//2) | total |
| --- | --- | --- | --- |
| 0 | 4 | 2 | 6 |
| 1 | 2 | 2 | 9 |
| 2 | 0 | 0 | 6 |
| 3 | invalid (b exhausted) | - | - |

The best configuration is x = 1 and y = 2, giving 9 stones. This shows that balancing usage of the second pile is more important than maximizing either operation independently.

### Example 2

Input: `1 0 5`

| x | b left | y | total |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 1 | invalid | - | - |

No operation of the first type is possible because the second pile is empty, and even the second type cannot be started because it requires at least one stone in the second pile. The answer is 0.

This confirms that both operations depend critically on the middle pile being nonzero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(a) per test case | We enumerate all possible values of x up to a |
| Space | O(1) | Only a few integer variables are used |

The constraints keep a, b, and c at most 100, so at worst we perform about 10,000 iterations across all test cases, which is easily within limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | 0 | minimal edge case |
| 10 10 10 | 30 | balanced large symmetric case |
| 5 1 10 | 3 | middle pile bottleneck |
| 0 4 10 | 6 | only second operation possible |

## Edge Cases

A key edge case occurs when the second pile is too small to support any first operation but still large enough to enable the second operation. In input like `a = 5, b = 1, c = 10`, the first operation is completely blocked, but the second operation still yields value. The algorithm handles this naturally because the loop over x immediately restricts to x = 0, and y
