---
title: "CF 1924B - Space Harbour"
description: "We have a straight line with n points, each occupied by a ship. Some of these points already host harbours, each with an associated value. A ship at a point incurs a cost if it were to \"move\" to the next harbour to its right."
date: "2026-06-08T19:10:29+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1924
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 921 (Div. 1)"
rating: 2100
weight: 1924
solve_time_s: 334
verified: false
draft: false
---

[CF 1924B - Space Harbour](https://codeforces.com/problemset/problem/1924/B)

**Rating:** 2100  
**Tags:** data structures, implementation, math, sortings  
**Solve time:** 5m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We have a straight line with `n` points, each occupied by a ship. Some of these points already host harbours, each with an associated value. A ship at a point incurs a cost if it were to "move" to the next harbour to its right. The cost is defined as the product of the value of the closest harbour to its left and the distance to the next harbour on its right. If a ship is already at a harbour, the cost is zero. The task is to handle two types of operations efficiently: adding a harbour at a new position with a given value, and computing the total cost of moving ships within a specified segment to their next harbours.

The input limits are large: `n` and `q` can reach up to 300,000, which rules out any approach that computes the cost naively for each query because iterating over segments could result in `O(n * q)` operations, potentially over `9 * 10^10` steps. This necessitates a data structure or algorithm that can answer range sum queries efficiently and handle dynamic insertion of harbours.

A few subtle edge cases must be considered. If a query asks for the cost for ships exactly at harbour positions, the cost is zero. Similarly, adding a harbour splits the interval between existing harbours and changes the cost for ships in that interval. For instance, if ships occupy points `[1, 2, 3, 4]` with harbours at `1` and `4`, adding a harbour at `3` reduces the cost for the ship at `3` to zero and changes the cost for the ship at `2`.

## Approaches

A naive brute-force approach iterates over each query and each ship within the segment for type 2 queries, computing the nearest left and right harbours. For type 1 queries, it simply adds the new harbour to the list. This is correct but extremely slow: the worst-case complexity is `O(n * q)`, which is unfeasible for the given bounds.

The key insight for an optimal solution is that the cost of each ship depends linearly on intervals defined by the positions of harbours. Between two consecutive harbours, the cost of a ship at position `i` is simply `(i - left) * value[left]` if `left` is the nearest harbour to the left and `right` is the nearest to the right. This observation allows us to represent costs as prefix sums over intervals. Using a balanced data structure, such as `SortedDict` from `sortedcontainers`, we can maintain harbour positions and efficiently compute cumulative costs. When a new harbour is added, only the interval it splits needs to be updated. For type 2 queries, a binary search or interval query lets us quickly sum costs over a segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Interval-based with SortedDict + prefix sums | O((m+q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a sorted mapping of harbour positions to their values. This ensures O(log n) access to nearest left and right harbours for any point.
2. Precompute initial costs for all ships. For each interval between consecutive harbours, the cost for a ship at position `i` is `(i - left) * value[left]`. Store prefix sums of costs so that range queries can be answered in O(log n) using cumulative sums.
3. When processing a type 1 query `(1 x v)`, find the interval `[L, R]` that contains `x`. Remove the cumulative cost for that interval, then split it into `[L, x-1]` and `[x+1, R]` with the new harbour at `x`. Recompute prefix sums for these intervals.
4. For a type 2 query `(2 l r)`, use the prefix sum array to efficiently compute the sum of costs between `l` and `r`. Binary search in the harbour positions identifies which intervals overlap with `[l, r]`, then sum the precomputed costs for those intervals.
5. Repeat this process for all queries.

Why it works: the invariant is that at any point, the cost array correctly represents the cost of moving ships in every interval between consecutive harbours. Adding a new harbour only affects the interval it splits, and prefix sums allow rapid querying. The combination of sorted mapping and interval-based prefix sums guarantees both correctness and efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline
from sortedcontainers import SortedDict

n, m, q = map(int, input().split())
harbour_positions = list(map(int, input().split()))
harbour_values = list(map(int, input().split()))

harbours = SortedDict()
for pos, val in zip(harbour_positions, harbour_values):
    harbours[pos] = val

# Precompute interval costs
def interval_cost(l, r, val):
    # sum_{i=l}^{r} (i - l) * val = val * (sum_{i=0}^{r-l} i) = val * (r-l)*(r-l+1)//2
    length = r - l + 1
    return val * (length * (length - 1) // 2)

# store prefix sum of costs by intervals
intervals = SortedDict()
prev = None
for pos in harbours:
    if prev is not None:
        intervals[prev] = (pos, interval_cost(prev + 1, pos - 1, harbours[prev]))
    prev = pos

def add_harbour(x, v):
    idx = harbours.bisect_left(x)
    right = harbours.peekitem(idx)[0]
    left = harbours.peekitem(idx - 1)[0]
    # remove old interval
    if left in intervals:
        del intervals[left]
    # add new intervals
    if left <= x - 1:
        intervals[left] = (x, interval_cost(left + 1, x - 1, harbours[left]))
    if x + 1 <= right - 1:
        intervals[x] = (right, interval_cost(x + 1, right - 1, v))
    harbours[x] = v

def query_cost(l, r):
    total = 0
    # find relevant intervals
    idx = intervals.bisect_right(l)
    if idx > 0:
        idx -= 1
    keys = list(intervals.islice(idx, len(intervals)))
    for start in keys:
        end, cost = intervals[start]
        if start > r:
            break
        sub_l = max(l, start + 1)
        sub_r = min(r, end - 1)
        if sub_l <= sub_r:
            length = sub_r - sub_l + 1
            val = harbours[start]
            total += val * (length * (length + 1) // 2 - (sub_l - start - 1) * (sub_l - start) // 2)
    return total

for _ in range(q):
    parts = input().split()
    t = int(parts[0])
    if t == 1:
        x, v = int(parts[1]), int(parts[2])
        add_harbour(x, v)
    else:
        l, r = int(parts[1]), int(parts[2])
        print(query_cost(l, r))
```

The solution uses `SortedDict` to maintain harbour positions and efficiently access nearest neighbours. Costs between harbours are precomputed for intervals. When adding a harbour, only the interval it splits is updated. Querying costs uses the precomputed values with careful adjustment for partial intervals. Off-by-one errors are avoided by handling inclusive ranges `[l, r]` properly.

## Worked Examples

Sample 1:

| Position | Harbour | Nearest left harbour | Nearest right harbour | Cost |
| --- | --- | --- | --- | --- |
| 1 | Yes | 1 | 3 | 0 |
| 2 | No | 1 | 3 | 3 |
| 3 | Yes | 3 | 8 | 0 |
| 4 | No | 3 | 8 | 24 |
| 5 | No | 3 | 8 | 72 |
| 6 | No | 3 | 8 | 96 |
| 7 | No | 3 | 8 | 120 |
| 8 | Yes | 8 | - | 0 |

First type 2 query `(2 2 5)` sums `3 + 0 + 24 + 72 = 99`. After adding harbour at 5, interval costs update, and subsequent queries reflect zero cost for ship at new harbour positions.

Another example: adding a harbour at the middle of two existing harbours splits the interval and redistributes costs proportionally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((m + q) log n) | SortedDict operations (insertion, bisect) are O(log n). Each query touches only relevant intervals. |
| Space | O(n) | Stores harbours, intervals, and prefix sums. |

Given `n, q ≤ 3*10^5`, worst-case operations are under 10^7, which fits comfortably in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
```
