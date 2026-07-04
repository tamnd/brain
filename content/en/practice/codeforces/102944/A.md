---
title: "CF 102944A - Ann Arbor"
description: "We are given a simple daily log of customer arrivals to a bubble tea shop. Each day has a number of customers, and every time the total number of customers reaches a multiple of a fixed value k, that customer receives a free drink."
date: "2026-07-04T07:35:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102944
codeforces_index: "A"
codeforces_contest_name: "UMPT 2020-2021 Team Tryout Contest"
rating: 0
weight: 102944
solve_time_s: 41
verified: true
draft: false
---

[CF 102944A - Ann Arbor](https://codeforces.com/problemset/problem/102944/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a simple daily log of customer arrivals to a bubble tea shop. Each day has a number of customers, and every time the total number of customers reaches a multiple of a fixed value `k`, that customer receives a free drink. The counting is continuous across customers within a single day, but resets each day when we only care about whether at least one multiple of `k` is hit during that day.

The task is not to simulate rewards globally, but to inspect each day independently and determine whether that day contains at least one customer whose position in the arrival order is divisible by `k`. If every day has at least one such customer, we output `"awesome"`. Otherwise, we output the first day index where no such customer exists.

The input size is small: both `k` and `D` are at most 1000, and each day has at most 2000 customers. This immediately rules out any need for advanced data structures or optimizations beyond linear scanning. Even a straightforward per-day computation is comfortably within limits since the total work is at most about 2 million checks.

A subtle edge case appears when a day has fewer than `k` customers. In that case, there is no multiple of `k` in that range, so the answer for that day is automatically “no free drink”. For example, if `k = 10` and `a_i = 5`, that day contributes nothing. A careless implementation that only checks whether `a_i % k == 0` would be incorrect, since having exactly 10, 20, 30 customers matters, not just divisibility of the total count.

Another corner case is when `k = 1`. Every customer qualifies, so every day with at least one customer must succeed, and even days with zero customers still produce zero free drinks, meaning failure if any such day exists.

## Approaches

A direct approach is to simulate each day. For a given day `i` with `a_i` customers, we iterate through customer positions from 1 to `a_i` and check whether any position is divisible by `k`. If we find at least one such position, the day is valid; otherwise, it is invalid.

This works because the problem reduces to checking existence of an integer `x` in `[1, a_i]` such that `x % k == 0`. However, this brute-force view is slightly wasteful: it scans all customers even though we only care about whether a multiple of `k` exists in the range.

The key observation is that multiples of `k` appear at positions `k, 2k, 3k, ...`. So a day contains a free drink if and only if `a_i >= k`. Once `a_i` is at least `k`, the `k`-th customer in that day exists and guarantees at least one free drink. If `a_i < k`, there is no multiple of `k` at all.

This reduces each day to a single comparison, turning the entire problem into a simple scan over the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(D * max a_i) | O(1) | Accepted |
| Direct Observation | O(D) | O(1) | Accepted |

## Algorithm Walkthrough

We process each day one by one while tracking whether every day satisfies the condition.

1. Read `k` and `D`, then read the array of daily customer counts. This gives all information needed to evaluate each day independently.
2. For each day `i`, check whether `a_i >= k`. This condition captures whether at least one multiple of `k` exists among customer positions that day. The reason is that the first qualifying customer is always the `k`-th arrival.
3. If `a_i < k`, we immediately know this day has no free drink and we can stop processing further days. We output `i` as the first failing day.
4. If we finish all days without encountering a failure, we output `"awesome"`.

### Why it works

Within a single day, free drinks occur exactly at positions that are multiples of `k`. The smallest such position is `k`, so the existence of any qualifying customer depends only on whether the day has at least `k` customers. This creates a monotone property: once `a_i` crosses `k`, success is guaranteed for that day, and below `k`, success is impossible. Because each day is independent, scanning in order correctly identifies the first failure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k, D = map(int, input().split())
    a = list(map(int, input().split()))

    for i in range(D):
        if a[i] < k:
            print(i + 1)
            return

    print("awesome")

if __name__ == "__main__":
    solve()
```

The solution reads the parameters and iterates through each day's customer count once. The core decision is the comparison `a[i] < k`, which directly encodes whether any multiple of `k` exists in that day's sequence. The early return ensures we stop at the first violating day.

A common mistake is to try simulating customer indices or checking divisibility conditions on `a[i]` itself. The correct interpretation is about positions inside the day, not properties of the total count.

## Worked Examples

### Example 1

Input:

```
10 5
14 33 5 58 74
```

| Day | a_i | a_i < k | Result so far |
| --- | --- | --- | --- |
| 1 | 14 | No | valid |
| 2 | 33 | No | valid |
| 3 | 5 | Yes | fail at day 3 |

Day 3 has only 5 customers, so no position reaches 10. This is the first failure, so output is `3`.

### Example 2

Input:

```
10 5
22 71 79 94 50
```

| Day | a_i | a_i < k | Result so far |
| --- | --- | --- | --- |
| 1 | 22 | No | valid |
| 2 | 71 | No | valid |
| 3 | 79 | No | valid |
| 4 | 94 | No | valid |
| 5 | 50 | No | valid |

Every day has at least 10 customers, so each day includes positions 10, 20, etc. No failures occur, so output is `"awesome"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(D) | Each day is checked once with a constant-time comparison |
| Space | O(1) | Only the input array and a few variables are stored |

The constraints allow up to 1000 days, so a single linear scan is trivial in terms of runtime. Even a less optimized O(D * a_i) solution would pass comfortably, but the direct comparison makes the solution immediate.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("10 5\n14 33 5 58 74\n") == "3"
assert run("10 5\n22 71 79 94 50\n") == "awesome"

# k = 1, always valid unless zero customers exist
assert run("1 3\n5 0 2\n") == "2"

# minimum edge: first day fails immediately
assert run("10 3\n1 20 30\n") == "1"

# all days valid
assert run("5 4\n5 5 5 5\n") == "awesome"

# boundary: exactly k customers
assert run("7 3\n7 6 7\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=1 mix with zero | 2 | zero-customer day fails |
| immediate failure | 1 | early exit correctness |
| all equal valid | awesome | full pass case |
| exact k boundary | 2 | strict `< k` logic |

## Edge Cases

When `k = 1`, every customer is a multiple of `k`, so any day with at least one customer passes. The algorithm handles this correctly because `a_i < 1` is only true when `a_i = 0`, so only empty days fail.

When a day has exactly `k - 1` customers, there is no multiple of `k` in the range. For example, `k = 10` and `a_i = 9` leads to failure. The check `a_i < k` correctly captures this boundary without needing explicit iteration.

When a day has exactly `k` customers, the `k`-th customer exists and guarantees success. For example, `k = 10`, `a_i = 10` succeeds immediately because position 10 is a multiple of 10.
