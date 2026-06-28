---
title: "CF 104916D - \u041a\u0430\u043c\u044b\u0448\u043e\u0432\u044b\u0439 \u043a\u043e\u0442"
description: "We are given a sequence of events ordered by time. At each time moment, the cat catches some number of mice. Multiple catches may happen at the same time moment, so the raw input can contain repeated timestamps with associated counts."
date: "2026-06-28T08:11:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104916
codeforces_index: "D"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u0421\u0430\u043c\u0430\u0440\u0435 2022-2023 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104916
solve_time_s: 26
verified: false
draft: false
---

[CF 104916D - \u041a\u0430\u043c\u044b\u0448\u043e\u0432\u044b\u0439 \u043a\u043e\u0442](https://codeforces.com/problemset/problem/104916/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of events ordered by time. At each time moment, the cat catches some number of mice. Multiple catches may happen at the same time moment, so the raw input can contain repeated timestamps with associated counts.

The task is to choose a continuous time interval, measured in terms of these events, such that the total number of mice caught inside the interval is at least a given threshold $k$. Among all such valid intervals, we want the minimum possible difference between the rightmost and leftmost timestamps in the interval.

Before reasoning about the main task, the input structure has an important simplification step. If several entries share the same timestamp, they can be merged into a single entry whose value is the sum of all mice caught at that time. After this compression, timestamps become strictly increasing, and each position represents a distinct moment in time with an associated weight.

The constraints imply that the sequence length can be large, so any quadratic scan over all pairs of endpoints would be too slow. A naive $O(n^2)$ solution would attempt every left endpoint and scan rightward until the sum condition is satisfied, which is not acceptable for large $n$.

The main subtle edge cases come from two behaviors.

The first is handling duplicate timestamps correctly. If we do not merge equal timestamps, a sliding window might treat identical times as separate positions, which artificially increases interval length or breaks correctness when computing time differences. For example, if input contains time 5 repeated twice, one with 3 mice and one with 4 mice, failing to merge would allow intervals that include only one of them, but any correct interpretation of the problem treats both as occurring at the same instant.

The second edge case is when the optimal interval does not end at the earliest point where the sum reaches $k$. A greedy “stop immediately when sum ≥ k” approach can miss better answers. Consider a case where adding a small additional segment barely increases time span but allows later shrinking of the left boundary to produce a smaller overall range. The correct solution must maintain a valid window and continue adjusting both ends rather than committing early.

## Approaches

A brute-force approach fixes a left index and then expands a right index until the sum of mice in the interval reaches at least $k$. For each left position, we recompute the sum from scratch or incrementally scan rightward. In the worst case, every left pointer scan touches almost the full array, leading to $O(n^2)$ time complexity. This is too slow when $n$ is large.

The structure of the problem suggests a monotonic behavior: as we move the right endpoint to the right, the sum of mice never decreases; as we move the left endpoint to the right, the sum never increases. This monotonicity allows a two-pointer technique, where both pointers move forward across the array at most once.

Instead of restarting computation for every left position, we maintain a running sum for a window $[l, r]$. We expand $r$ until the sum becomes large enough. Then we try to shrink $l$ while preserving validity, recording the best interval each time a valid window is obtained. If shrinking breaks validity, we expand $r$ again. Each element enters and leaves the window at most once, so the total work becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Two Pointers | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### 1. Preprocess the sequence

Combin
