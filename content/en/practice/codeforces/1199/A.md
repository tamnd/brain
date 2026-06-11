---
title: "CF 1199A - City Day"
description: "We are given a sequence of daily rainfall amounts over the summer, and we need to find the earliest day that is “not-so-rainy."
date: "2026-06-11T23:55:57+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1199
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 576 (Div. 2)"
rating: 1000
weight: 1199
solve_time_s: 85
verified: true
draft: false
---

[CF 1199A - City Day](https://codeforces.com/problemset/problem/1199/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of daily rainfall amounts over the summer, and we need to find the earliest day that is “not-so-rainy.” A day is considered not-so-rainy if, compared to the previous `x` days and the next `y` days (within the summer period), it has strictly less rain than all of them. The input consists of `n` days, with `x` days of look-back and `y` days of look-ahead, followed by `n` distinct integers representing rainfall. The output is the index of the first day that satisfies this condition.

Because `n` can be up to 100,000 and citizens only watch up to 7 days before or after, any solution that compares each day to all other days in a large window would be inefficient. A naive brute-force would check up to `x + y` neighboring days for each day, resulting in at most 100,000 * 14 = 1,400,000 operations in the worst case. This is small enough for a modern CPU, so even a straightforward solution could work. The main subtlety comes from handling boundaries properly: for the first `x` days, we cannot check `x` days before; for the last `y` days, we cannot check `y` days after. Also, because all rain amounts are distinct, strict inequalities are safe and we do not need to handle ties.

A careless approach might forget to limit the range within `1` to `n`. For example, if `x = 2` and we are considering day `1`, we cannot look at days `-1` or `0`. If implemented naively, accessing negative indices could produce incorrect results or runtime errors. Another subtlety is that we must return the earliest day, so if multiple days satisfy the condition, we must pick the one with the smallest index.

## Approaches

The brute-force approach is straightforward: iterate over each day, check the rainfall for the `x` previous days and `y` next days, and determine if the current day is strictly smaller than all neighbors in this window. It is correct because it directly implements the definition of “not-so-rainy,” but it can be inefficient if `x` and `y` were large. Here, `x` and `y` are bounded by 7, so even a direct comparison is acceptable.

The key insight for a slightly cleaner approach is that, because `x` and `y` are very small, we do not need any advanced data structures like segment trees or deques. We can simply iterate from day `1` to day `n` and for each day check its small left and right windows. As soon as we find a day where all neighbors are greater, we can immediately return it. This leverages the fact that the “earliest day” criterion allows a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check neighbors) | O(n * (x + y)) | O(n) | Accepted |
| Optimized (same logic, early exit) | O(n * (x + y)) | O(n) | Accepted |

In practice, both are acceptable given the small `x` and `y`.

## Algorithm Walkthrough

1. Read `n`, `x`, and `y`, and then read the array `a` of rainfall amounts.
2. Iterate through each day index `d` from `1` to `n`.
3. For each day `d`, check all previous days from `max(1, d - x)` up to `d - 1`. If any of these have rain less than or equal to `a[d]`, then day `d` cannot be not-so-rainy, so skip to the next day.
4. Check all next days from `d + 1` up to `min(n, d + y)`. If any of these have rain less than or equal to `a[d]`, then day `d` is disqualified.
5. If both checks pass, print `d` and terminate, because it is the earliest not-so-rainy day.

Why it works: The algorithm explicitly compares the current day to exactly the days citizens are interested in, respecting boundaries. Because all values are distinct, strict comparison guarantees that the condition is correctly evaluated. Linear iteration ensures the first valid day is returned.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, x, y = map(int, input().split())
a = list(map(int, input().split()))

for i in range(n):
    is_valid = True
    for j in range(max(0, i - x), i):
        if a[j] <= a[i]:
            is_valid = False
            break
    if not is_valid:
        continue
    for j in range(i + 1, min(n, i + y + 1)):
        if a[j] <= a[i]:
            is_valid = False
            break
    if is_valid:
        print(i + 1)
        break
```

The code iterates from the first to the last day. For each day, it checks its left and right windows using `max` and `min` to ensure we do not go out of bounds. The first day that passes both checks is printed. The `+1` accounts for 1-based indexing in the problem statement.

## Worked Examples

### Sample 1

Input: `10 2 2`, rainfall: `10 9 6 7 8 3 2 1 4 5`

| Day (i) | Left window | Right window | a[i] | Check result |
| --- | --- | --- | --- | --- |
| 1 | - | 9,6 | 10 | 10 > 9? Yes, 10 > 6? Yes |
| 2 | 10 | 6,7 | 9 | 9 < 10? Yes, 9 < 6? No |
| 3 | 10,9 | 7,8 | 6 | 6 < 10 & 6 < 9? Yes, 6 < 7 & 6 < 8? Yes |

The algorithm stops at day 3 and prints `3`.

### Sample 2

Input: `10 2 2`, rainfall: `10 9 6 7 8 3 2 1 4 5` but checking day 8

Trace shows that day 8 has left neighbors `3,2` and right neighbors `4,5`. `1 < 3,2? Yes`, `1 < 4,5? Yes`, confirming it is a valid not-so-rainy day. Day 8 would be found only after earlier days fail.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * (x + y)) | Each of the n days checks up to x + y neighbors, x, y <= 7, so constant factor |
| Space | O(n) | Storing the rainfall array |

Given `n` up to 10^5 and x+y <= 14, total operations ~1.4 million, which runs comfortably under 1s. Memory usage is linear in `n`, well under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution code
    n, x, y = map(int, input().split())
    a = list(map(int, input().split()))
    for i in range(n):
        is_valid = True
        for j in range(max(0, i - x), i):
            if a[j] <= a[i]:
                is_valid = False
                break
        if not is_valid:
            continue
        for j in range(i + 1, min(n, i + y + 1)):
            if a[j] <= a[i]:
                is_valid = False
                break
        if is_valid:
            print(i + 1)
            break
    return output.getvalue().strip()

# Provided samples
assert run("10 2 2\n10 9 6 7 8 3 2 1 4 5\n") == "3", "sample 1"
# Minimum size input
assert run("1 0 0\n100\n") == "1", "minimum size"
# Maximum x and y
assert run("5 7 7\n5 4 3 2 1\n") == "5", "x+y > n-1 boundary"
# Edge at start
assert run("5 1 1\n1 2 3 4 5\n") == "1", "first day is earliest"
# Edge at end
assert run("5 1 1\n5 4 3 2 1\n") == "5", "last day is earliest"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0\n100` | 1 | Minimum-size input |
| `5 7 7\n5 4 3 2 1` | 5 | Look windows exceed available days |
| `5 1 1\n1 2 3 4 5` | 1 | Earliest day is first day |
| `5 1 1\n5 4 3 2 1` | 5 | Earliest day is last day |

## Edge Cases
