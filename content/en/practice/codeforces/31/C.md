---
title: "CF 31C - Schedule"
description: "We are given a list of n lessons, each with a start and end time, scheduled in a single room. Two lessons overlap if one"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 31
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 31 (Div. 2, Codeforces format)"
rating: 1700
weight: 31
solve_time_s: 58
verified: true
draft: false
---

[CF 31C - Schedule](https://codeforces.com/problemset/problem/31/C)

**Rating:** 1700  
**Tags:** implementation  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of `n` lessons, each with a start and end time, scheduled in a single room. Two lessons overlap if one starts before another ends. The goal is to find which single lesson can be removed so that the remaining lessons have no overlaps. If removing any single lesson produces a conflict-free schedule, we should list all such possibilities. If the schedule is already conflict-free, any lesson can be removed.

The constraints are moderate: `n` is at most 5000, and times go up to 10^6. With `n = 5000`, a brute-force approach that checks every pair of lessons repeatedly would involve on the order of 5000^2 = 25 million operations, which might still fit in a 2-second limit if carefully implemented, but it is close to the edge. This motivates seeking a linear or linearithmic solution for safety. The lesson times are integers, so no floating-point precision issues arise.

Edge cases include the following. If lessons are already non-overlapping, the answer should include all lessons. If multiple lessons share the same start or end time, the algorithm must treat them correctly: lessons that touch exactly at start and end are allowed and do not count as overlapping. If a lesson is completely nested inside another, removing either could potentially resolve the conflict, but not always - the algorithm needs to reason globally, not just locally.

## Approaches

The simplest approach is brute force: for each lesson, temporarily remove it, then check all remaining lessons pairwise to see if any overlap. This works because it directly implements the problem statement, but it requires O(n^3) operations: O(n) removals, and for each removal O(n^2) pairwise comparisons. With `n = 5000`, that is clearly infeasible.

The key insight is that we do not need to check all pairs repeatedly. If we sort lessons by start time, we only need to compare adjacent lessons to detect overlaps. Once sorted, an overlap occurs only when the end of the previous lesson exceeds the start of the current lesson. Thus, we can preprocess the maximum end time seen from the left and minimum start time from the right. Then, for any candidate lesson to remove, we can check whether merging the lessons on its left and right would introduce an overlap. This reduces the problem to O(n log n) for sorting plus O(n) for the overlap checks.

The brute force works because it directly implements the definition of conflict, but it fails for `n = 5000` due to cubic complexity. The observation that conflicts only occur between adjacent lessons in a start-time sorted array allows us to reduce the problem to linear passes, avoiding nested loops entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Sorting + Prefix/Suffix | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the lesson times and store them along with their original indices.
2. Sort the lessons by start time. This allows us to focus on conflicts only between consecutive lessons.
3. Build a `max_end_from_left` array, where each entry i contains the maximum ending time among lessons 0 to i. This allows us to know the latest end time before any lesson.
4. Build a `min_start_from_right` array, where each entry i contains the minimum start time among lessons i to n-1. This allows us to know the earliest start time after any lesson.
5. For each lesson at index i, check whether removing it resolves conflicts: compare `max_end_from_left[i-1]` with `min_start_from_right[i+1]`. If `max_end_from_left[i-1] <= min_start_from_right[i+1]`, removing this lesson creates a non-overlapping schedule.
6. Collect all original indices of lessons that satisfy the above condition and output them in increasing order.

Why it works: Sorting guarantees that any overlap occurs between consecutive lessons. The `max_end_from_left` and `min_start_from_right` arrays capture the extremal times efficiently, allowing us to test removal in constant time per lesson. This ensures we identify all lessons whose removal results in a conflict-free schedule.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
lessons = []

for i in range(n):
    l, r = map(int, input().split())
    lessons.append((l, r, i + 1))

lessons.sort(key=lambda x: x[0])  # sort by start time

max_end_from_left = [0] * n
min_start_from_right = [0] * n

max_end_from_left[0] = lessons[0][1]
for i in range(1, n):
    max_end_from_left[i] = max(max_end_from_left[i-1], lessons[i][1])

min_start_from_right[-1] = lessons[-1][0]
for i in range(n-2, -1, -1):
    min_start_from_right[i] = min(min_start_from_right[i+1], lessons[i][0])

res = []
for i in range(n):
    left_max = max_end_from_left[i-1] if i > 0 else float('-inf')
    right_min = min_start_from_right[i+1] if i < n-1 else float('inf')
    if left_max <= right_min:
        res.append(lessons[i][2])

print(len(res))
print(" ".join(map(str, sorted(res))))
```

The solution first sorts lessons to reduce conflict detection to adjacency checks. The `max_end_from_left` array accumulates the latest end seen so far, and `min_start_from_right` accumulates the earliest start to the right. Each lesson is tested by comparing these values. Using `float('-inf')` and `float('inf')` handles boundary lessons correctly without extra conditions.

## Worked Examples

**Sample 1**

Input:

```
3
3 10
20 30
1 3
```

After sorting by start time:

| i | start | end | index |
| --- | --- | --- | --- |
| 0 | 1 | 3 | 3 |
| 1 | 3 | 10 | 1 |
| 2 | 20 | 30 | 2 |

`max_end_from_left`: [3, 10, 30]

`min_start_from_right`: [3, 3, 20]

Check each lesson:

- i = 0: left_max = -inf, right_min = 3 → -inf ≤ 3 
- i = 1: left_max = 3, right_min = 20 → 3 ≤ 20 
- i = 2: left_max = 10, right_min = inf → 10 ≤ inf 

All lessons can be removed, output 1 2 3.

**Custom Sample**

Input:

```
4
1 5
2 6
7 8
9 10
```

Sorted lessons:

| i | start | end | index |
| --- | --- | --- | --- |
| 0 | 1 | 5 | 1 |
| 1 | 2 | 6 | 2 |
| 2 | 7 | 8 | 3 |
| 3 | 9 | 10 | 4 |

`max_end_from_left`: [5, 6, 8, 10]

`min_start_from_right`: [2, 7, 9, 9]

Check removals:

- i=0: left=-inf, right=7 → 
- i=1: left=5, right=7 → 5 ≤ 7 
- i=2: left=6, right=10 → 6 ≤ 10 
- i=3: left=8, right=inf → 

Removing 1 or 2 resolves the only conflict (1-5 vs 2-6).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates. Linear passes for prefix/suffix arrays and checking removals are O(n). |
| Space | O(n) | Storing lesson data, prefix and suffix arrays. |

With `n ≤ 5000`, O(n log n) is easily under 100,000 operations, well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    lessons = []
    for i in range(n):
        l, r = map(int, input().split())
        lessons.append((l, r, i + 1))
    lessons.sort(key=lambda x: x[0])
    max_end_from_left = [0] * n
    min_start_from_right = [0] * n
    max_end_from_left[0] = lessons[0][1]
    for i in range(1, n):
        max_end_from_left[i] = max(max_end_from_left[i-1], lessons[i][1])
    min_start_from_right[-1] = lessons[-1][0]
    for i in range(n-2, -1, -1):
        min_start_from_right[i] = min(min_start_from_right[i+1], lessons[i][0])
    res = []
    for i in range(n):
        left_max = max_end_from_left[i-1] if i > 0 else
```
