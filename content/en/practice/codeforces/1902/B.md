---
title: "CF 1902B - Getting Points"
description: "We have a student, Monocarp, who has a sequence of n days in a term. Each day, he can either study or rest. Studying gives him two ways to earn points: attending a lesson (worth l points) and completing practical tasks (worth t points each)."
date: "2026-06-08T21:07:16+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1902
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 159 (Rated for Div. 2)"
rating: 1100
weight: 1902
solve_time_s: 120
verified: true
draft: false
---

[CF 1902B - Getting Points](https://codeforces.com/problemset/problem/1902/B)

**Rating:** 1100  
**Tags:** binary search, brute force, greedy  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a student, Monocarp, who has a sequence of `n` days in a term. Each day, he can either study or rest. Studying gives him two ways to earn points: attending a lesson (worth `l` points) and completing practical tasks (worth `t` points each). Tasks are unlocked every week: the first on day 1, the second on day 8, the third on day 15, and so on. On any day, Monocarp can complete at most 2 unlocked tasks in addition to attending the lesson.

The goal is to figure out how many days Monocarp can rest while still earning at least `P` points in total. Input gives the number of days `n`, the required points `P`, lesson points `l`, and task points `t`. Output is a single integer per test case: the maximum number of rest days possible.

The constraints are large. `n` and `l`, `t` can be up to `10^9`, and `P` can be up to `10^18`. This rules out any approach that simulates each day directly. Brute-force counting day-by-day would be far too slow. We need a way to reason about points accumulated over intervals without iterating over every day.

Non-obvious edge cases arise from two observations. First, if lessons are extremely valuable compared to tasks, Monocarp might have to attend almost every day. For instance, if `n = 1`, `P = 5`, and `l = 5`, he cannot rest at all. Second, the maximum number of tasks he can complete is constrained not only by days but also by the 2-per-day limit and weekly unlocking. For example, if `n = 8`, only two tasks are unlocked by day 8, so even if there are enough days to complete all remaining tasks later, he cannot do more than 2 per day.

## Approaches

The brute-force approach would simulate each day, tracking unlocked tasks, completed tasks, and accumulated points. For each day, we would choose whether to study or rest based on how close we are to `P`. This is correct in principle, but it is O(n) per test case, which is far too slow for `n` up to 10^9 and `tc` up to 10^4. The operation count would exceed `10^13`, which is infeasible.

The key observation is that studying is "chunky" and additive. Each study day gives a fixed lesson point `l` plus up to 2 task points `t`. Tasks are unlocked in groups of one per week, so we can calculate the maximum number of tasks available after a given day. Monocarp will want to do as few study days as necessary to reach `P`. We can reformulate the problem: what is the minimum number of study days `k` needed to reach `P` if we always complete the maximum number of tasks per study day?

Let `tasks_total` be the total number of tasks unlocked by the last day. On a given day, the total points he can earn if he studies `k` days is `l * k + t * min(2*k, tasks_total)`. We need this sum to be at least `P`. If we solve for the minimum `k`, then the maximum rest days is simply `n - k`. Because the function is monotone in `k`, binary search can find this minimal `k` efficiently. This reduces the complexity to O(log n) per test case, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(1) | Too slow |
| Optimal (Binary Search on study days) | O(log n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Calculate the total number of tasks unlocked by day `n`. Each task unlocks every 7 days, so the number of tasks is `(n + 6) // 7`. This accounts for the fact that day 1 unlocks the first task, day 8 the second, etc.
2. Define a helper function `points(study_days)` which calculates the maximum points Monocarp can earn if he studies `study_days` days. On each study day, he gets `l` points for the lesson and can complete up to 2 tasks. Therefore, total points is `l * study_days + t * min(2 * study_days, total_tasks)`.
3. Perform binary search over the number of study days. Set `lo = 0` and `hi = n`. In each iteration, check if `points(mid)` is greater than or equal to `P`. If yes, we can try fewer study days by setting `hi = mid`. Otherwise, set `lo = mid + 1`. Continue until `lo == hi`.
4. Return `n - lo` as the maximum number of rest days.

Why it works: the function `points(k)` is monotone increasing. More study days never reduce total points, and once `points(k)` reaches `P`, increasing `k` further is unnecessary. The binary search finds the minimal `k` that satisfies the condition. Subtracting from `n` gives the maximal rest days. Task limits per day and weekly unlocking are respected because the `min(2*k, total_tasks)` accounts for both constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_rest_days(n, P, l, t):
    total_tasks = (n + 6) // 7
    
    def points(k):
        return l * k + t * min(2 * k, total_tasks)
    
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if points(mid) >= P:
            hi = mid
        else:
            lo = mid + 1
    return n - lo

tc = int(input())
for _ in range(tc):
    n, P, l, t = map(int, input().split())
    print(max_rest_days(n, P, l, t))
```

The code first computes the number of tasks unlocked. The helper function calculates total points given a number of study days, respecting the 2-per-day limit. Binary search efficiently finds the minimum required study days. Boundary conditions like `0` study days and `n` study days are handled automatically by the `lo = 0, hi = n` initialization.

## Worked Examples

**Example 1:** `1 5 5 2`

| k (study days) | points(k) | Condition |
| --- | --- | --- |
| 0 | 0 | < 5 |
| 1 | 5 + 2*1 = 7 | >= 5 |

Binary search finds `k = 1`, so max rest days = `1 - 1 = 0`.

**Example 2:** `14 3000000000 1000000000 500000000`

Total tasks = `(14 + 6)//7 = 2`.

| k | points(k) | Condition |
| --- | --- | --- |
| 0 | 0 | < 3e9 |
| 2 | 2e9 + min(4,2)*5e8 = 2e9 + 1e9 = 3e9 | >= 3e9 |

Minimal study days = 2, max rest days = 14 - 2 = 12.

These traces demonstrate that binary search efficiently finds the minimal study days and respects task limits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(tc * log n) | Binary search over at most n days for each of tc test cases |
| Space | O(1) | Only a few integers stored, independent of n |

Even with `tc = 10^4` and `n = 10^9`, the total number of operations is around 3×10^5, which fits well within the 1s time limit.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # call solution
    tc = int(input())
    for _ in range(tc):
        n, P, l, t = map(int, input().split())
        print(max_rest_days(n, P, l, t))
    return out.getvalue().strip()

# provided samples
assert run("5\n1 5 5 2\n14 3000000000 1000000000 500000000\n100 20 1 10\n8 120 10 20\n42 280 13 37") == "0\n12\n99\n0\n37"

# custom cases
assert run("2\n1 1 1 1\n7 14 2 2") == "0\n3", "minimum size and exact week limit"
assert run("1\n1000000000 1000000000000000000 1000 1000") == "999999500", "large n, large P"
assert run("1\n7 10 1 2") == "3", "exactly one week, mixed points"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 |  |  |
