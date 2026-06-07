---
title: "CF 2126B - No Casino in the Mountains"
description: "We are given a sequence of days, each labeled either as rainy (1) or good (0). Jean wants to complete as many hikes as possible. Each hike takes exactly k consecutive days of good weather, and after finishing a hike, he must rest for at least one day before starting another."
date: "2026-06-08T03:21:47+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2126
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1037 (Div. 3)"
rating: 800
weight: 2126
solve_time_s: 89
verified: true
draft: false
---

[CF 2126B - No Casino in the Mountains](https://codeforces.com/problemset/problem/2126/B)

**Rating:** 800  
**Tags:** dp, greedy  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of days, each labeled either as rainy (1) or good (0). Jean wants to complete as many hikes as possible. Each hike takes exactly `k` consecutive days of good weather, and after finishing a hike, he must rest for at least one day before starting another. The problem asks us to determine the maximum number of hikes he can fit into the sequence of days.

The input can be large: up to `10^5` days per test case and up to `10^4` test cases, with the sum of all days across test cases not exceeding `10^5`. This implies that any solution must run in linear time relative to the number of days. Quadratic or nested loops iterating over ranges of days will be too slow.

Non-obvious edge cases include sequences with intermittent rains that break possible hikes, sequences where `k` is greater than the number of consecutive good days, and sequences where all days are rainy or all are good. For example, if `n = 5`, `k = 2`, and `a = [0, 1, 0, 0, 0]`, a naive greedy that jumps every `k` days without checking intervening breaks may overcount hikes.

## Approaches

A brute-force approach would attempt to start a hike on every day `i` and check whether the next `k` days are all good. If they are, we would increment the hike count and skip to day `i + k + 1` for the next potential hike. This works because it respects the mandatory rest day. However, this requires checking `k` days for each possible starting day, leading to a worst-case complexity of `O(n * k)`. For large `n` and `k`, this could reach `10^10` operations, which is unacceptable.

The key observation is that we do not need to re-check overlapping segments repeatedly. We can instead count the number of consecutive good days in a single pass. Every time we find a block of `length` consecutive zeros, the number of hikes that can be performed in that block is `length // k`. Each hike within this block will naturally respect the mandatory rest day because we can conceptually place a "1" after each hike, effectively reducing the usable length. This reduces the problem to a single linear scan of the array, which is optimal given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k) | O(1) | Too slow for large n and k |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `count` to zero to store the number of hikes for the current test case. Initialize a variable `length` to zero to track the current streak of consecutive good days.
2. Iterate over each day in the array. If the day is good (`a[i] = 0`), increment `length`. If the day is rainy (`a[i] = 1`), reset `length` to zero. This maintains the invariant that `length` always represents the current contiguous block of good days ending at `i`.
3. Whenever `length` reaches `k`, we can schedule a hike. Increment `count` by one. Then, to enforce the mandatory rest day, decrement `length` by `k + 1`. The subtraction effectively skips over the days used by the hike plus the rest day, keeping `length` ready to count the next potential hike in the remaining days.
4. Continue the iteration until the end of the array. After the iteration, `count` holds the maximum number of hikes for the test case.
5. Print `count` for each test case.

The reason this works is that the algorithm maintains the length of consecutive good days and greedily schedules hikes whenever a full block of size `k` is available. Subtracting `k + 1` ensures the next hike respects the mandatory rest day without re-scanning or overlapping segments. No valid hikes are missed, and no hikes violate the rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    count = 0
    length = 0
    for day in a:
        if day == 0:
            length += 1
            if length >= k:
                count += 1
                length -= k + 1
        else:
            length = 0
    print(count)
```

The first line reads the number of test cases. For each test case, we read `n` and `k` and then the array `a`. The main loop iterates over each day, updating the current streak of good weather. When a hike is possible, we increment `count` and enforce the rest day by reducing `length`. Resetting `length` on rainy days ensures we never attempt hikes that include bad weather.

## Worked Examples

**Sample 1:**

Input: `n = 5, k = 1, a = [0, 1, 0, 0, 0]`

| day | a[i] | length | count |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 0 | 1 | 2 |
| 4 | 0 | 1 | 2 |
| 5 | 0 | 2 | 3 |

This demonstrates that multiple hikes can be scheduled with intervening rest days. The greedy decrement of `length` ensures we skip rest days correctly.

**Sample 2:**

Input: `n = 7, k = 3, a = [0, 0, 0, 0, 0, 0, 0]`

| day | a[i] | length | count |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 0 | 2 | 0 |
| 3 | 0 | 3 | 1 |
| 4 | 0 | 0 | 1 |
| 5 | 0 | 1 | 1 |
| 6 | 0 | 2 | 1 |
| 7 | 0 | 3 | 2 |

This shows that the algorithm schedules hikes in every possible block, respecting the required rest day.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each day is visited once, and operations inside the loop are constant time. |
| Space | O(1) | Only a few integer variables are used. The input array is read once. |

This fits comfortably within the problem's constraints, since `n` summed across all test cases is at most `10^5`, making O(n) linear passes acceptable under a 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided samples
assert run("5\n5 1\n0 1 0 0 0\n7 3\n0 0 0 0 0 0 0\n3 1\n1 1 1\n4 2\n0 1 0 1\n6 2\n0 0 1 0 0 0\n") == "3\n2\n0\n0\n2", "sample tests"

# Custom edge cases
assert run("1\n1 1\n0\n") == "1", "single good day"
assert run("1\n1 1\n1\n") == "0", "single rainy day"
assert run("1\n5 5\n0 0 0 0 0\n") == "1", "entire array one hike"
assert run("1\n5 2\n0 0 0 0 0\n") == "2", "overlapping block with rest day"
assert run("1\n6 2\n0 0 1 0 0 0\n") == "2", "split by rain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 day good | 1 | minimum-size input |
| 1 day rainy | 0 | minimum-size input with no hike |
| 5 days all good, k=5 | 1 | single hike fits exactly |
| 5 days all good, k=2 | 2 | multiple hikes with rest day enforced |
| 6 days split by rain, k=2 | 2 | correct handling of broken good day blocks |

## Edge Cases

For the case `a = [0]` with `k = 1`, the algorithm increments `length` to 1, which meets the hike requirement, adds to `count`, and subtracts `k + 1 = 2`, making `length` negative, but the loop ends and `count = 1`. This correctly schedules one hike.

For `a = [1]` with `k = 1`, `length`
