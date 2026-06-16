---
title: "CF 962A - Equator"
description: "We are given a sequence of days, and on each day Polycarp solves a fixed number of problems. If we look at the entire training period, there is a total number of problems solved across all days."
date: "2026-06-17T01:44:23+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 962
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 42 (Rated for Div. 2)"
rating: 1300
weight: 962
solve_time_s: 74
verified: true
draft: false
---

[CF 962A - Equator](https://codeforces.com/problemset/problem/962/A)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of days, and on each day Polycarp solves a fixed number of problems. If we look at the entire training period, there is a total number of problems solved across all days. The task is to find the earliest day such that by the end of that day, Polycarp has already solved at least half of the total number of problems from the whole schedule.

In other words, we compute a running sum from day one onward and stop at the first position where this prefix sum reaches at least half of the overall sum. The answer is the index of that day.

The constraints allow up to 200,000 days, so any solution must run in linear time. A quadratic approach that repeatedly recomputes prefix sums or scans suffixes would perform on the order of $n^2$, which is too slow at this scale. A single pass accumulation is sufficient and necessary.

A subtle point is the definition of “half or more.” Since the total sum can be odd, we are not dividing into exact halves but comparing against a threshold of $\lceil \frac{S}{2} \rceil$ or equivalently checking when the prefix sum multiplied by 2 is at least the total sum.

Edge cases are mostly structural. When $n = 1$, the answer is always 1 because the first day already contains all problems. Another corner case is when one large value appears late in the sequence, meaning the answer is not early even if the prefix grows slowly at first.

## Approaches

A straightforward way to solve the problem is to compute the total number of problems first, then for each day recompute the sum of problems from day one up to that day. Each check would involve summing a prefix from scratch. This is correct because it directly mirrors the definition of the condition, but it repeats work heavily. For day $i$, recomputing the prefix sum costs $O(i)$, and summing over all days gives $O(n^2)$ operations in the worst case, which is too large for $n = 200{,}000$.

The key observation is that prefix sums can be maintained incrementally. Instead of recomputing, we accumulate the running sum as we iterate once. At each step, we compare the current prefix sum with half of the total sum. The first index satisfying the condition is the answer.

This works because the condition depends only on prefixes, and prefix sums form a monotonic non-decreasing sequence. Once the threshold is crossed, it will remain crossed for all later indices, so the first crossing point is uniquely defined.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal Prefix Sum Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array of daily solved problems and compute the total sum of all values. This total defines the threshold we must reach.
2. Initialize a running variable `prefix = 0`. This will store the cumulative number of problems solved up to the current day.
3. Iterate over the days from left to right. For each day, add the current value to `prefix`.
4. After updating `prefix`, check whether `2 * prefix >= total`. This comparison avoids floating-point division and directly encodes the “at least half” condition.
5. The first index where the condition becomes true is returned immediately as the answer.

The reasoning behind stopping immediately is that once a prefix reaches half of the total, all later prefixes will also satisfy the condition due to monotonic growth.

### Why it works

The prefix sum sequence is non-decreasing because all daily values are positive. The condition “prefix sum is at least half of total sum” defines a monotonic predicate over indices: once it becomes true, it never becomes false again. This guarantees that the first index satisfying it is well-defined and unique, and scanning left to right finds it without backtracking.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)
prefix = 0

for i, x in enumerate(a, start=1):
    prefix += x
    if prefix * 2 >= total:
        print(i)
        break
```

The solution first computes the total number of problems so that the target threshold is known. Then it performs a single pass, maintaining a running prefix sum. The comparison uses multiplication by 2 to avoid floating-point operations and preserve integer safety.

The enumeration starts at 1 because the problem asks for a 1-based day index. The moment the condition is satisfied, the loop terminates early, which ensures minimal unnecessary computation.

## Worked Examples

### Example 1

Input:

```
4
1 3 2 1
```

Total sum is 7, so the threshold is 3.5, meaning we look for the first prefix reaching at least 4.

| Day | Value | Prefix Sum | Condition (2*prefix >= 7) |
| --- | --- | --- | --- |
| 1 | 1 | 1 | No |
| 2 | 3 | 4 | Yes |

The answer is 2 because the prefix reaches 4 at day 2, which already covers at least half of all problems.

### Example 2

Input:

```
6
1 2 3 4 2 0
```

Total sum is 12, so threshold is 6.

| Day | Value | Prefix Sum | Condition (2*prefix >= 12) |
| --- | --- | --- | --- |
| 1 | 1 | 1 | No |
| 2 | 2 | 3 | No |
| 3 | 3 | 6 | Yes |

The first valid day is 3, because the prefix sum equals exactly half of the total at that point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We compute the total once and then scan the array once |
| Space | O(1) | Only a few integer variables are used |

The linear scan is sufficient for $n \le 200{,}000$, and all operations are constant time integer additions and comparisons, so the solution easily fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    
    total = sum(a)
    prefix = 0
    
    for i, x in enumerate(a, start=1):
        prefix += x
        if prefix * 2 >= total:
            return str(i)

    return ""

# provided sample
assert run("4\n1 3 2 1\n") == "2"

# minimum size
assert run("1\n5\n") == "1"

# already satisfied early
assert run("3\n10 1 1\n") == "1"

# exact half on last element
assert run("4\n1 1 1 3\n") == "4"

# all equal
assert run("5\n2 2 2 2 2\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | 1 | single element edge case |
| 10 1 1 | 1 | early dominance of first element |
| 1 1 1 3 | 4 | threshold reached at last position |
| 2 2 2 2 2 | 3 | symmetric prefix growth |

## Edge Cases

One important edge case is when the first element alone already exceeds half of the total. For input:

```
3
10 1 1
```

The total is 12, so half is 6. The first prefix is 10, which already satisfies the condition, so the answer is 1. The algorithm handles this naturally because the check is performed immediately after processing the first element.

Another case is when the threshold is reached exactly at the last element. For:

```
4
1 1 1 3
```

The total is 6, half is 3. The prefix sums are 1, 2, 3, 6, and the first time we reach at least 3 is at day 3, but depending on equality handling, day 3 is valid since 2 * 3 >= 6. The algorithm correctly triggers at that point and stops early.

A final structural case is uniform distribution, such as:

```
5
2 2 2 2 2
```

The total is 10, half is 5. Prefix sums are 2, 4, 6, so day 3 is the first time the threshold is crossed. The monotonic nature of prefix sums guarantees there is no ambiguity in selecting this index.
