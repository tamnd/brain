---
title: "CF 237A - Free Cash"
description: "We are asked to determine how many cash registers Valera needs in his fast-food cafe so that every visitor can be served immediately, assuming each visitor arrives at a specific time during a single day and each service takes less than a minute."
date: "2026-06-04T16:42:18+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 237
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 147 (Div. 2)"
rating: 1000
weight: 237
solve_time_s: 207
verified: true
draft: false
---

[CF 237A - Free Cash](https://codeforces.com/problemset/problem/237/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 3m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine how many cash registers Valera needs in his fast-food cafe so that every visitor can be served immediately, assuming each visitor arrives at a specific time during a single day and each service takes less than a minute. Each input line after the first gives the hour and minute a customer arrives. The output is a single integer: the maximum number of people that arrive at exactly the same time, because that is the number of cashes required to avoid any customer leaving.

The constraints let `n` go up to 100,000, and the time is provided in chronological order. This implies that any solution iterating over all customers once or using a map from times to counts is acceptable. A naive solution comparing every pair of customers for overlapping times would require roughly `n^2` operations, which is infeasible at the upper limit of `n`.

The main edge cases to be careful of are multiple customers arriving at the exact same time, customers arriving at sequential times without overlap, and the smallest possible input of a single customer. For example, if three customers arrive at 8:00 and two more at 9:00, the correct output is 3, even though only five customers exist in total. A careless implementation might sum arrivals rather than take the maximum concurrent arrivals.

## Approaches

The brute-force method is to compare every customer against every other customer and count how many share the same timestamp. This would be correct because the problem reduces to counting simultaneous arrivals, but it would perform roughly `n^2` comparisons in the worst case, which is far too slow for `n = 10^5`.

The optimal approach leverages the fact that the input is already in chronological order. We can iterate once, keeping track of the number of consecutive customers that share the same hour and minute. Whenever we encounter a new time, we reset the counter. The largest value the counter reaches during this iteration is the minimum number of cashes required. This method is both simple and linear in time, `O(n)`, because we process each customer exactly once and only perform constant-time operations for each.

The key insight is that because the times are sorted, all customers arriving at the same time are contiguous. This means we do not need a hash map or any complex data structure; a simple counter suffices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `current_count` to 1, representing the first customer, and `max_count` to 1, which will store the maximum simultaneous arrivals.
2. Store the arrival time of the first customer in `last_time` as a tuple `(hour, minute)`.
3. Iterate over the remaining `n-1` customers:

a. For each customer, read the arrival time as a tuple `(hour, minute)`.

b. If this time matches `last_time`, increment `current_count` because another customer has arrived at the same minute.

c. If it does not match, set `current_count` to 1 since we have a new time.

d. Update `last_time` to the current time.

e. Update `max_count` if `current_count` exceeds it.
4. After iterating all customers, `max_count` is the minimum number of cashes required. Print it.

The invariant here is that `current_count` always reflects the number of customers arriving at the current time, and `max_count` records the largest such value seen so far. Because times are sorted, no customer with the same timestamp will appear later in the input without being counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
h, m = map(int, input().split())
last_time = (h, m)
current_count = 1
max_count = 1

for _ in range(n - 1):
    h, m = map(int, input().split())
    current_time = (h, m)
    if current_time == last_time:
        current_count += 1
    else:
        current_count = 1
        last_time = current_time
    if current_count > max_count:
        max_count = current_count

print(max_count)
```

The solution reads the first customer outside the loop to initialize `last_time` and `current_count`. For each subsequent customer, it compares times and updates the counters. This ensures no off-by-one errors in counting the first occurrence and avoids unnecessary checks. Using tuples `(hour, minute)` keeps the comparison simple and clear.

## Worked Examples

**Sample Input 1**

```
4
8 0
8 10
8 10
8 45
```

| Step | last_time | current_time | current_count | max_count |
| --- | --- | --- | --- | --- |
| init | (8,0) | (8,0) | 1 | 1 |
| 1 | (8,0) | (8,10) | 1 | 1 |
| 2 | (8,10) | (8,10) | 2 | 2 |
| 3 | (8,10) | (8,45) | 1 | 2 |

The table shows that the maximum simultaneous arrivals are 2, so we need 2 cashes.

**Sample Input 2**

```
3
9 0
9 15
9 30
```

| Step | last_time | current_time | current_count | max_count |
| --- | --- | --- | --- | --- |
| init | (9,0) | (9,0) | 1 | 1 |
| 1 | (9,0) | (9,15) | 1 | 1 |
| 2 | (9,15) | (9,30) | 1 | 1 |

Each customer arrives at a different minute, so one cash is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate over each customer exactly once and perform constant-time operations per customer. |
| Space | O(1) | We only store a few counters and tuples; no additional arrays or maps are needed. |

Given `n ≤ 100,000` and linear iteration, the solution executes well within the 2-second time limit, with negligible memory usage compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    h, m = map(int, input().split())
    last_time = (h, m)
    current_count = 1
    max_count = 1
    for _ in range(n - 1):
        h, m = map(int, input().split())
        current_time = (h, m)
        if current_time == last_time:
            current_count += 1
        else:
            current_count = 1
            last_time = current_time
        if current_count > max_count:
            max_count = current_count
    return str(max_count)

# provided samples
assert run("4\n8 0\n8 10\n8 10\n8 45\n") == "2", "sample 1"
assert run("3\n9 0\n9 15\n9 30\n") == "1", "sample 2"

# custom cases
assert run("1\n0 0\n") == "1", "single customer"
assert run("5\n10 0\n10 0\n10 0\n10 0\n10 0\n") == "5", "all same time"
assert run("6\n1 1\n1 2\n1 2\n1 2\n1 3\n1 4\n") == "3", "three at same minute"
assert run("4\n23 59\n23 59\n0 0\n0 0\n") == "2", "boundary wrap-around"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 customer | 1 | Minimum input size |
| all same time | 5 | Maximum simultaneous arrivals |
| mixed duplicates | 3 | Multiple groups with duplicates |
| boundary wrap | 2 | Times at end and start of day, ensure no cross-day counting |

## Edge Cases

For a single customer, input `1\n12 30\n`, `current_count` and `max_count` are initialized to 1 and the loop does not run, producing 1, which is correct. For all customers arriving at the same time, the counter increments correctly through the loop, yielding the correct maximum. When arrivals are at the end of the day and the next at midnight, the comparison `(hour, minute)` ensures no false aggregation across days. This concrete handling prevents any off-by-one or cross-boundary errors.
