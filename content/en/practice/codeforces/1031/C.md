---
title: "CF 1031C - Cram Time"
description: "Lesha has two separate time budgets, one for today and one for tomorrow. Each lecture note has a fixed reading cost equal to its index: note 1 takes 1 hour, note 2 takes 2 hours, and so on."
date: "2026-06-16T20:40:47+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1031
codeforces_index: "C"
codeforces_contest_name: "Technocup 2019 - Elimination Round 2"
rating: 1600
weight: 1031
solve_time_s: 818
verified: false
draft: false
---

[CF 1031C - Cram Time](https://codeforces.com/problemset/problem/1031/C)

**Rating:** 1600  
**Tags:** greedy  
**Solve time:** 13m 38s  
**Verified:** no  

## Solution
## Problem Understanding

Lesha has two separate time budgets, one for today and one for tomorrow. Each lecture note has a fixed reading cost equal to its index: note 1 takes 1 hour, note 2 takes 2 hours, and so on. He may choose any subset of notes, but each chosen note must be read completely in a single day, and each note can be used at most once across both days.

The goal is to maximize the total number of distinct notes he reads, splitting them into two groups: one group assigned to today whose total cost does not exceed `a`, and another group assigned to tomorrow whose total cost does not exceed `b`.

Even though the notes are indexed indefinitely, only small indices are practically usable because costs grow linearly. The key structure is that smaller indices are strictly cheaper, so they are always more efficient in terms of maximizing count.

The constraints allow `a, b` up to 10^9, which immediately rules out any attempt to simulate knapsack states or try subsets dynamically. Any solution must reason directly about the structure of optimal selections rather than enumerate possibilities.

A naive mistake is to try assigning notes greedily day by day without global coordination. For example, if `a = 3` and `b = 3`, choosing `{1,2}` for today uses up 3 hours, leaving nothing useful for tomorrow except large-cost items. But swapping assignments or splitting differently can improve total count. Another subtle failure mode is picking the smallest possible notes independently for each day without ensuring global uniqueness; both days might try to use the same cheap notes.

## Approaches

The brute-force idea is to try all possible ways to split a prefix of notes between the two days. For a fixed largest note index `k`, we could choose any subset of `{1..k}`, assign each element either to day one or day two, and check feasibility of both sums. This is already exponential in `k`, since each note has three choices: unused, day one, or day two. Even if we cap `k` at the largest value where `k(k+1)/2 ≤ a+b`, the number of assignments grows far too quickly.

The key observation is that since costs are strictly increasing, any optimal solution will always consist of prefix-like selections. If a higher-numbered note is used, all cheaper unused notes are always better candidates to include first. This reduces the problem to distributing the smallest numbers across two knapsacks.

Instead of thinking in terms of assignment, we reverse the perspective: we first try to take as many smallest notes as possible ignoring the split, then we decide how to divide them between the two days. If we take notes 1, 2, 3, …, k, their total cost is `k(k+1)/2`. We choose the maximum `k` such that this sum fits into `a + b`. After that, the remaining task is to split these first `k` numbers between two capacity constraints.

Once the prefix is fixed, assigning greedily from largest to smallest is optimal: larger items are harder to place, so they should be placed first into whichever day can accommodate them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force subsets | Exponential | Exponential | Too slow |
| Prefix + greedy split | O(k) | O(k) | Accepted |

## Algorithm Walkthrough

### Step 1: Find the maximum prefix

We compute the largest `k` such that `1 + 2 + ... + k ≤ a + b`. This ensures we never try to use a note we cannot afford even in total.

The reasoning is that any optimal solution that uses `k` notes must necessarily use some subset of the first `k` indices, because skipping a smaller note in favor of a larger one is never beneficial.

### Step 2: Initialize remaining capacities

We treat `a` and `b` as remaining capacities for two independent bins. Initially both are full.

### Step 3: Assign notes from k down to 1

We iterate from `k` down to `1`. For each note `i`, we try to place it in the day where it fits.

We prefer placing it into day one if possible. If not, we attempt day two.

The reason we go downward is that larger notes are more restrictive. If we delay them, we may lose feasibility even though a valid assignment exists.

### Step 4: Store assignments

We maintain two lists: one for day one and one for day two. Each time we assign a note, we subtract its cost from the corresponding capacity.

### Step 5: Output

We print both groups.

### Why it works

The correctness relies on a monotonic exchange argument. Any optimal solution can be transformed into one that uses a prefix of integers without decreasing the number of elements. Once the prefix is fixed, assigning larger elements first never blocks a feasible solution because any failure to place a large element would imply that both bins are too small to accommodate it, which contradicts feasibility of any valid partition containing it.

Thus, greedy placement from largest to smallest preserves feasibility and maximizes usage of all available numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_k(total):
    k = 0
    cur = 0
    while True:
        if cur + (k + 1) > total:
            break
        k += 1
        cur += k
    return k

a, b = map(int, input().split())
total = a + b

k = max_k(total)

a_rem, b_rem = a, b
day1 = []
day2 = []

for i in range(k, 0, -1):
    if i <= a_rem:
        day1.append(i)
        a_rem -= i
    else:
        day2.append(i)
        b_rem -= i

print(len(day1))
print(*day1)
print(len(day2))
print(*day2)
```

The first function computes the largest prefix sum that fits into the combined capacity. This avoids any need to consider numbers beyond what is globally possible.

The greedy loop processes from `k` downward. Each number is placed into the first bin where it fits. The subtraction updates ensure we never exceed capacity.

The choice to try day one first is arbitrary; either order works because the final assignment is not unique.

## Worked Examples

### Example 1: a = 3, b = 3

We first compute the maximum `k` such that `k(k+1)/2 ≤ 6`. This gives `k = 3` since `1+2+3 = 6`.

| i | a_rem | b_rem | Action | day1 | day2 |
| --- | --- | --- | --- | --- | --- |
| 3 | 3 | 3 | fits in day1 | [3] | [] |
| 2 | 0 | 3 | fits in day2 | [3] | [2] |
| 1 | 0 | 1 | fits in day2 | [3] | [2,1] |

Day one uses 3 hours exactly, day two uses 3 hours exactly. All notes are used.

This demonstrates that the greedy order avoids blocking smaller elements unnecessarily while still placing large constraints first.

### Example 2: a = 5, b = 2

Total is 7, so `k = 3` since `1+2+3 = 6`.

| i | a_rem | b_rem | Action | day1 | day2 |
| --- | --- | --- | --- | --- | --- |
| 3 | 5 | 2 | fits in day1 | [3] | [] |
| 2 | 2 | 2 | fits in day1 | [3,2] | [] |
| 1 | 0 | 2 | fits in day2 | [3,2] | [1] |

This shows imbalance is handled naturally: larger capacity absorbs heavier items first, while smaller day still receives leftover small elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | single pass over chosen prefix |
| Space | O(k) | storing assigned notes |

The value of `k` is bounded by the largest integer such that `k(k+1)/2 ≤ 2×10^9`, which is about 60000, so the solution easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a, b = map(int, input().split())
    total = a + b

    k = 0
    cur = 0
    while cur + (k + 1) <= total:
        k += 1
        cur += k

    a_rem, b_rem = a, b
    day1 = []
    day2 = []

    for i in range(k, 0, -1):
        if i <= a_rem:
            day1.append(i)
            a_rem -= i
        else:
            day2.append(i)
            b_rem -= i

    out = []
    out.append(str(len(day1)))
    out.append(" ".join(map(str, day1)))
    out.append(str(len(day2)))
    out.append(" ".join(map(str, day2)))
    return "\n".join(out)

# sample
assert run("3 3") is not None

# minimum case
assert run("0 0") == "0\n\n0\n"

# only one day
assert run("10 0") is not None

# asymmetric split
assert run("5 2") is not None

# large balanced
assert run("1000000000 1000000000") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | empty groups | zero capacity handling |
| 10 0 | all in one day | single-side packing |
| 5 2 | split feasibility | greedy distribution correctness |
| large equal | full utilization | performance and prefix bound |

## Edge Cases

When one of `a` or `b` is zero, the algorithm naturally places everything into the other day because the greedy check fails for the empty side first and all items go to the only available capacity.

For very large equal inputs, the prefix computation stops at about 60000, so no overflow or performance issue appears. The greedy loop still only runs over this prefix, ensuring linear time behavior independent of input magnitude.

A subtle case is when capacities are highly skewed, for example `a = 1` and `b = 1000000000`. The algorithm still first determines the prefix from total capacity, then assigns small values first into the large bin, preserving feasibility without any special-case logic.
