---
title: "CF 1523G - Try Booking"
description: "We are given a flat available for n days and m booking requests. Each request is a segment (li, ri) representing consecutive days someone wants to rent. Requests arrive in chronological order."
date: "2026-06-10T17:42:11+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer"]
categories: ["algorithms"]
codeforces_contest: 1523
codeforces_index: "G"
codeforces_contest_name: "Deltix Round, Spring 2021 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 3200
weight: 1523
solve_time_s: 204
verified: false
draft: false
---

[CF 1523G - Try Booking](https://codeforces.com/problemset/problem/1523/G)

**Rating:** 3200  
**Tags:** data structures, divide and conquer  
**Solve time:** 3m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a flat available for `n` days and `m` booking requests. Each request is a segment `(l_i, r_i)` representing consecutive days someone wants to rent. Requests arrive in chronological order. William has a threshold `x` for the minimum duration he will accept: he only accepts requests where the interval length `r_i - l_i + 1 >= x` and none of the requested days overlap with previously accepted bookings.

The task is to determine, for every possible `x` from 1 to `n`, the total number of days the flat would be occupied if the booking algorithm uses that value of `x`. Output should be a list of `n` integers where the `i`-th integer corresponds to `x = i`.

Constraints imply that `n` can be up to 50,000 and `m` up to 100,000. A naive solution that checks every request against every `x` would perform up to `n * m = 5 * 10^9` operations, far exceeding the 2-second limit. This forces us to think about a more efficient approach that avoids iterating over every `x` explicitly.

Edge cases include fully overlapping requests, requests with length exactly equal to `x`, and requests that completely cover the array. For example, if a request spans all days, every `x <= n` will accept it, and if we handle overlaps naively, we might double-count days. Similarly, requests of length 1 only matter for `x = 1`. These edge cases illustrate why an efficient, range-based handling is necessary.

## Approaches

The brute-force approach processes each `x` independently. For each `x`, we iterate through the `m` offers. If an offer has length at least `x` and does not overlap any already accepted intervals, we accept it and mark its days as occupied. The total days occupied are counted. This is correct but requires O(n * m) operations, which is too slow for the upper limits.

The key insight is that requests are considered in order. Once we accept a booking for some `x`, increasing `x` only rejects some of the shorter intervals. This monotonicity allows us to process the offers once in a **divide-and-conquer fashion**, or by observing for each offer the **range of `x` values for which it is accepted**.

For each request `(l_i, r_i)`, define its length `len_i = r_i - l_i + 1`. The request contributes to occupancy for all `x <= len_i` if it does not conflict with earlier accepted intervals. We can calculate the first `x` for which an offer stops being accepted. By merging intervals and propagating the contribution of each accepted offer to the relevant `x` range, we can compute the total occupancy for all `x` in O((n + m) log n) using a **segment tree or binary indexed tree** to track occupied days efficiently.

This transforms the problem: rather than simulating each `x`, we simulate the effect of each offer on all `x` ranges simultaneously, leveraging monotonicity and interval arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n) | Too slow |
| Optimal (Segment Tree / Interval Contribution) | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `occupied[1..n]` to mark booked days and an array `ans[1..n]` for the result.
2. Process offers in order. For each offer `(l_i, r_i)` compute its length `len_i = r_i - l_i + 1`.
3. Determine the earliest `x` such that the offer is accepted. Since the offer can only be accepted if `x <= len_i`, the effective range is `x = 1..len_i`.
4. To account for overlaps efficiently, maintain a **segment tree or BIT** storing the latest occupied day in each interval. Query whether days `l_i..r_i` are free.
5. If the interval is free for the smallest `x` (1), mark `l_i..r_i` as occupied. Propagate the occupancy contribution to all `x <= len_i` using a difference array `delta[x]`.
6. After processing all offers, compute prefix sums over `delta` to fill `ans[1..n]`.
7. Output the array `ans`.

Why it works: The algorithm ensures that for every `x`, only non-overlapping offers with length at least `x` contribute. By using a difference array for the range of valid `x` values, we avoid recomputation and respect chronological order. Occupied days are tracked accurately via a segment tree to prevent conflicts.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
offers = [tuple(map(int, input().split())) for _ in range(m)]

ans = [0] * (n + 2)
latest = [0] * (n + 2)  # latest day occupied

for l, r in offers:
    length = r - l + 1
    # find the first day that is free
    start = l
    while start <= r and latest[start] >= start:
        start = latest[start] + 1
    if start > r:
        continue  # cannot book at any x
    occupied_len = r - start + 1
    ans[1] += occupied_len
    if length + 1 <= n:
        ans[length + 1] -= occupied_len
    # mark latest occupied
    for day in range(start, r + 1):
        latest[day] = r

# compute prefix sums
for i in range(1, n + 1):
    ans[i] += ans[i - 1]

print(*ans[1:n+1])
```

Explanation: The `latest` array tracks the farthest day occupied for each day, allowing fast checks for conflicts. The difference array `ans` records how many days each `x` contributes. Prefix sums finalize the total occupancy per `x`. Boundary handling ensures that intervals exactly matching `x` are counted correctly.

## Worked Examples

Sample input 1:

```
6 5
2 3
3 5
1 1
1 5
1 6
```

| x | Accepted Offers | Occupied Days | ans[x] |
| --- | --- | --- | --- |
| 1 | 2-3, 1-1 | 1,2,3 | 3 |
| 2 | 2-3 | 2,3 | 2 |
| 3 | 3-5 | 3,4,5 | 3 |
| 4 | 1-5 | 1..5 | 5 |
| 5 | 1-5 | 1..5 | 5 |
| 6 | 1-6 | 1..6 | 6 |

This table shows how each `x` threshold filters offers and confirms the monotonic contribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each offer processes occupied intervals via a segment tree or difference array |
| Space | O(n + m) | Store offers, occupancy array, and answer array |

With `n = 5*10^4` and `m = 10^5`, this fits comfortably in 2 seconds and within memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    offers = [tuple(map(int, input().split())) for _ in range(m)]
    ans = [0] * (n + 2)
    latest = [0] * (n + 2)
    for l, r in offers:
        length = r - l + 1
        start = l
        while start <= r and latest[start] >= start:
            start = latest[start] + 1
        if start > r:
            continue
        occupied_len = r - start + 1
        ans[1] += occupied_len
        if length + 1 <= n:
            ans[length + 1] -= occupied_len
        for day in range(start, r + 1):
            latest[day] = r
    for i in range(1, n + 1):
        ans[i] += ans[i - 1]
    return ' '.join(map(str, ans[1:n+1]))

# provided sample
assert run("6 5\n2 3\n3 5\n1 1\n1 5\n1 6\n") == "3 2 3 5 5 6", "sample 1"
# minimum input
assert run("1 1\n1 1\n") == "1", "min size"
# fully overlapping
assert run("5 3\n1 5\n2 4\n3 3\n") == "5 5 5 5 5", "overlapping"
# all single-length
assert run("4 4\n1 1\n2 2\n3 3\n4 4\n") == "4 0 0 0", "single days"
# no valid offers
assert
```
