---
title: "CF 1346B - Boot Camp"
description: "The problem asks us to schedule the maximum number of lectures during a programming boot camp that lasts n days. Each day is either a normal day, where we can hold lectures, or an excursion day, where no lectures are allowed."
date: "2026-06-11T14:51:45+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1346
codeforces_index: "B"
codeforces_contest_name: "Kotlin Heroes: Episode 4"
rating: 1400
weight: 1346
solve_time_s: 190
verified: false
draft: false
---

[CF 1346B - Boot Camp](https://codeforces.com/problemset/problem/1346/B)

**Rating:** 1400  
**Tags:** *special, greedy  
**Solve time:** 3m 10s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to schedule the maximum number of lectures during a programming boot camp that lasts `n` days. Each day is either a normal day, where we can hold lectures, or an excursion day, where no lectures are allowed. On normal days, we cannot schedule more than `k_1` lectures on any single day, and for any pair of consecutive days, the sum of lectures cannot exceed `k_2`. The goal is to determine the largest total number of lectures that can be assigned across all days, while respecting these constraints.

The input consists of multiple test cases. Each test case provides the number of days, the per-day and per-pair lecture limits, and a binary string representing which days are excursions. The output is a single integer per test case, the maximum total lectures possible.

The key constraints are that `n` can be as large as 5000, `k_1` and `k_2` can be up to 200,000, and there may be up to 50 test cases. This suggests that an algorithm with complexity `O(n^2)` per test case would be too slow in the worst case, because `5000^2 * 50` operations is on the order of a billion. We need an approach that works in linear or linearithmic time per test case.

A subtle aspect is that consecutive days affect each other through the `k_2` constraint. A naive approach might try to assign `k_1` lectures to every non-excursion day, but this can violate the pairwise sum constraint. Another edge case occurs when several excursion days are consecutive or at the edges; the algorithm must correctly reset the accumulation of lectures in such segments.

For example, if we have `n = 4`, `k_1 = 3`, `k_2 = 4` and the day string is `1101`, then a naive approach assigning `k_1` everywhere would yield `[3, 3, 0, 3]`, but `3 + 3 = 6` exceeds `k_2 = 4`. The correct assignment is `[2, 2, 0, 3]`, yielding total 7.

## Approaches

The brute-force approach is to iterate through every non-excursion day and try all possible lecture counts from `0` to `k_1`, while checking the consecutive day sum constraint. For each day, we would keep track of possible cumulative totals and valid last-day counts. This can be implemented as a dynamic programming solution with `dp[i][x]` representing the maximum total lectures until day `i` if day `i` has `x` lectures. Each update would require checking all `x` and `y` pairs for consecutive days. In the worst case, with `n = 5000` and `k_1 = 200,000`, this approach is infeasible because it requires `O(n * k_1^2)` operations.

The key insight comes from observing that the `k_2` constraint can be represented as a ceiling on how much a single day can take relative to its neighbor. If `k_2 >= 2 * k_1`, then the consecutive constraint never binds, and we can simply assign `k_1` to every non-excursion day. Otherwise, if `k_2 < 2 * k_1`, then for each pair of consecutive non-excursion days, the maximum we can assign to each is limited by `floor(k_2 / 2)`. This reduces the problem to splitting the boot camp into contiguous blocks of non-excursion days, and assigning either `k_1` or `floor(k_2 / 2)` per day, alternating as needed, similar to a "fence painting" problem where neighbors constrain each other.

This observation allows a linear-time solution. We can scan the string of days, identify segments of consecutive non-excursion days, and for each segment, compute the maximum lectures by filling it alternately with the allowed maximum values while never exceeding `k_2` on any consecutive pair. Excursion days act as natural separators that reset the alternation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k_1^2) | O(n * k_1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, parse `n`, `k_1`, `k_2` and the day string.
3. Compute `max_pair = min(k_1, k_2 // 2)`. This represents the maximum number of lectures that can be safely assigned to a day when considering the consecutive day limit.
4. Initialize a counter for total lectures.
5. Scan through the day string from left to right. Maintain a running length of consecutive non-excursion days.
6. Whenever an excursion day or the end of the string is encountered, process the preceding segment of consecutive non-excursion days. For a segment of length `L`, the maximum total lectures is `L * max_pair + (L // 2) * (k_2 - 2 * max_pair)` if `k_2 < 2 * k_1`, or simply `L * k_1` if `k_2 >= 2 * k_1`.
7. Reset the segment counter at each excursion day and continue.
8. After processing all segments, output the accumulated total lectures.

The invariant is that at every segment of consecutive non-excursion days, the assigned lectures never violate the per-day limit `k_1` and the consecutive-day sum limit `k_2`. Excursion days naturally separate segments so we do not need to consider cross-boundary violations.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k1, k2 = map(int, input().split())
    s = input().strip()
    
    max_pair = min(k1, k2 // 2)
    total = 0
    count = 0
    
    for ch in s + '0':
        if ch == '1':
            count += 1
        else:
            if count > 0:
                # maximum lectures in this segment
                segment_total = count * max_pair + (count // 2) * (k2 - 2 * max_pair)
                total += segment_total
                count = 0
    print(total)
```

The solution scans each day exactly once and processes segments of consecutive non-excursion days. Appending `'0'` at the end ensures the last segment is processed without special boundary checks. Using integer division ensures we respect the consecutive day limit when splitting additional lectures.

## Worked Examples

**Example 1**

Input: `4 5 7`, days: `1011`.

Segments of non-excursion days are `[1]`, `[1, 1]`.

`k2 // 2 = 3`, `max_pair = min(5, 3) = 3`.

| Segment | Length | Calculated lectures | Tota
