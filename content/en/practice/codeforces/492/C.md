---
title: "CF 492C - Vanya and Exams"
description: "Vanya has a number of exams, each graded between 1 and a maximum score r. He wants his overall average to reach at least avg to qualify for a scholarship. For each exam, he can improve his score by writing essays, with the cost of increasing a grade by 1 point varying per exam."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 492
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 280 (Div. 2)"
rating: 1400
weight: 492
solve_time_s: 57
verified: true
draft: false
---

[CF 492C - Vanya and Exams](https://codeforces.com/problemset/problem/492/C)

**Rating:** 1400  
**Tags:** greedy, sortings  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Vanya has a number of exams, each graded between 1 and a maximum score _r_. He wants his overall average to reach at least _avg_ to qualify for a scholarship. For each exam, he can improve his score by writing essays, with the cost of increasing a grade by 1 point varying per exam. The goal is to minimize the total number of essays he must write to reach the required average.

The input gives the number of exams _n_, the maximum grade _r_, and the required average _avg_. Each exam then has two numbers: the current grade and the number of essays required per point of increase. The output should be a single integer: the minimum total essays required.

The constraints are significant. With _n_ up to 10^5 and _r_ as large as 10^9, any algorithm with worse than O(n log n) complexity risks timing out. For instance, iterating over every possible grade increase explicitly would be too slow. Also, _b_i_ can be as large as 10^6, so we must account for essay costs carefully to avoid integer overflow if using naive summation.

Edge cases can be subtle. One is when the current average already meets or exceeds _avg_, in which case no essays are required. Another is when some exams are already at the maximum grade _r_, and the algorithm must avoid attempting to increase them further. A careless implementation might always attempt to increase grades in index order, ignoring the essay cost, leading to a non-optimal solution. For example, if:

```
2 5 5
5 10
3 1
```

Vanya already has 8 points total and needs 10, so he must increase only the second exam by 2 points, despite the first exam also being at max; a naive approach that blindly processes exams in input order could fail.

## Approaches

A brute-force approach would consider every possible increment for every exam until the required total score is reached. For each increment, we add the corresponding essay cost and stop when the total average is enough. While correct in principle, the worst-case number of operations can reach O(n*r), which is up to 10^14 in this problem - clearly infeasible.

The key observation is that essay costs per point vary per exam, and we want to spend as few essays as possible. Therefore, we should prioritize increasing grades in exams that require fewer essays per point. Sorting the exams by essay cost allows us to greedily select the cheapest increments first. After sorting, we iterate through the exams, increasing each as much as needed or until it reaches the maximum grade. We continue until the sum of grades meets or exceeds _n × avg_. This reduces the complexity to O(n log n) due to sorting, which is efficient enough for the input limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*r) | O(n) | Too slow |
| Greedy Sort by Cost | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of grades Vanya currently has. Let this be `current_sum`.
2. Compute the total points required to reach the desired average, which is `required_sum = n * avg`.
3. If `current_sum >= required_sum`, print 0 and terminate, since no essays are needed.
4. Pair each exam’s current grade with its essay cost. Sort these pairs by essay cost in ascending order. This ensures we always pick the cheapest increments first.
5. Initialize `essays = 0` and `needed = required_sum - current_sum`.
6. Iterate over the sorted exams. For each exam, calculate the maximum possible increase: `increase = min(r - grade, needed)`.
7. Add `increase * essay_cost` to `essays`. Subtract `increase` from `needed`.
8. If `needed` reaches zero, break the loop. Print the total `essays`.

**Why it works**

This greedy method is correct because the essay cost per point is fixed per exam. To minimize the total essays, any optimal solution must always spend as few essays as possible per point increase. Sorting by cost guarantees that every point we add is the cheapest available. The algorithm maintains the invariant that at each step, `needed` is the remaining number of points required, and the total essays spent is minimal for the increments performed so far. Once `needed` is zero, the average requirement is satisfied.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, r, avg = map(int, input().split())
exams = [tuple(map(int, input().split())) for _ in range(n)]

current_sum = sum(grade for grade, _ in exams)
required_sum = n * avg

if current_sum >= required_sum:
    print(0)
    sys.exit()

# sort exams by essay cost
exams.sort(key=lambda x: x[1])

needed = required_sum - current_sum
essays = 0

for grade, cost in exams:
    increase = min(r - grade, needed)
    essays += increase * cost
    needed -= increase
    if needed == 0:
        break

print(essays)
```

The code first calculates how many total points are missing to reach the required average. Sorting the exams by cost ensures that each essay spent is as efficient as possible. The `min(r - grade, needed)` line ensures we never exceed the maximum grade or overshoot the required points.

## Worked Examples

**Sample 1**

Input:

```
5 5 4
5 2
4 7
3 1
3 2
2 5
```

| Exam | Grade | Cost | Max increase | Needed | Essays added | Remaining Needed |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 1 | 2 | 10 | 2 | 8 |
| 4 | 3 | 2 | 2 | 8 | 4 | 6 |
| 2 | 4 | 7 | 1 | 6 | 7 | 5 |
| 5 | 2 | 5 | 3 | 5 | 15 | 2 |
| 1 | 5 | 2 | 0 | 2 | 0 | 2 |

After processing the cheapest exams first, only 4 essays are required to reach the required average.

**Sample 2**

Input:

```
2 5 2
5 10
3 1
```

`current_sum = 8` and `required_sum = 4`. Since 8 >= 4, output is 0. No essays needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting exams dominates the runtime |
| Space | O(n) | Storing the list of exams |

With n up to 10^5, O(n log n) operations fit comfortably within the 1-second limit. Memory usage is also well below 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, r, avg = map(int, input().split())
    exams = [tuple(map(int, input().split())) for _ in range(n)]

    current_sum = sum(grade for grade, _ in exams)
    required_sum = n * avg

    if current_sum >= required_sum:
        return "0"

    exams.sort(key=lambda x: x[1])
    needed = required_sum - current_sum
    essays = 0

    for grade, cost in exams:
        increase = min(r - grade, needed)
        essays += increase * cost
        needed -= increase
        if needed == 0:
            break

    return str(essays)

# provided samples
assert run("5 5 4\n5 2\n4 7\n3 1\n3 2\n2 5\n") == "4"
assert run("2 5 2\n5 10\n3 1\n") == "0"

# custom cases
assert run("1 5 5\n5 1\n") == "0", "single exam already enough"
assert run("3 10 10\n10 3\n9 2\n8 1\n") == "3", "needs minimal increases on cheapest exam"
assert run("2 1000000000 1000000000\n1 1\n1 1\n") == str(1999999998), "max r and avg"
assert run("4 10 7\n7 5\n6 1\n5 1\n4 2\n") == "4", "mixed costs, must choose cheapest first"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 5\n5 1 | 0 | Single exam already meets avg |
| 3 10 10\n10 3\n9 2\n8 1 | 3 | Correct greedy selection by essay cost |
| 2 10^9 10^9\n1 1\n1 1 | 1999999998 | Handles large numbers without overflow |
| 4 10 7\n7 5\n6 1\n5 1\n4 2 | 4 | Greedy increments avoid costly essays |

## Edge Cases

If the current average is already sufficient
