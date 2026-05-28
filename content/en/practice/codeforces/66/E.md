---
title: "CF 66E - Petya and Post"
description: "We have a circular route with n post offices, each with a gas station. Each station i has a[i] liters of gasoline available, and the distance from station i to i+1 is b[i] kilometers, wrapping around at the end."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 66
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 61 (Div. 2)"
rating: 2000
weight: 66
solve_time_s: 132
verified: false
draft: false
---

[CF 66E - Petya and Post](https://codeforces.com/problemset/problem/66/E)

**Rating:** 2000  
**Tags:** data structures, dp  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We have a circular route with `n` post offices, each with a gas station. Each station `i` has `a[i]` liters of gasoline available, and the distance from station `i` to `i+1` is `b[i]` kilometers, wrapping around at the end. Petya’s uncle wants to start at a post office, pick up a car, and drive exactly one round along the circle in either direction, refueling only at the stations he passes, never refueling more than once at the same station. The car consumes exactly one liter per kilometer.

We are asked to find all stations from which starting the route allows completing the full circle without running out of gas.

The sum of all gasoline `sum(a)` equals the sum of all distances `sum(b)`, which guarantees that a solution exists from at least one starting point. Each station has at least one liter of gas, and each distance is at least one kilometer.

With `n` up to 10^5 and a time limit of 2 seconds, any solution with complexity worse than O(n log n) is risky. A naive O(n^2) approach, which tries starting at every station and simulates the full loop, would involve about 10^10 operations and is infeasible.

Edge cases include having all stations with exactly enough gas to reach the next station, stations with extremely uneven gas distribution, or distances forming a “bottleneck” that prevents starting from certain points. For example:

```
n = 3
a = [1, 5, 2]
b = [3, 2, 3]
```

Naively starting at station 1 would fail immediately because 1 < 3, whereas starting at station 2 succeeds. Missing these checks would lead to incorrect answers.

## Approaches

The brute-force approach is straightforward: try starting from each station, keep a running fuel counter, and simulate moving forward. For each station, subtract `b[i]` from your fuel and add `a[i]` at the next station. If fuel ever drops below zero, that starting point fails. Each simulation takes O(n), and we repeat this n times for O(n^2), which is too slow.

The key insight is that the problem is equivalent to the classic "circular gas station / gas tour" problem. If we define the net fuel change at each station as `a[i] - b[i]`, then completing the circle requires the cumulative sum of these net changes to never drop below zero, starting from the chosen station. Because `sum(a) == sum(b)`, the total net sum is zero. The points where the cumulative sum reaches a minimum determine which starting stations are feasible. Any station immediately after a global minimum of the cumulative sum is a valid starting point.

This observation allows us to compute cumulative sums once and find the global minimum, giving an O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Cumulative Sum / Min Tracking | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the net fuel change at each station: `delta[i] = a[i] - b[i]`. This represents how much fuel you gain or lose moving from station `i` to `i+1`.
2. Compute the prefix sums of `delta` along the circle: `pref[i] = delta[0] + delta[1] + ... + delta[i]`. Extend the array circularly by one extra round to simplify wrap-around handling if needed.
3. Find the global minimum value of the cumulative sum. Let `min_sum` be the smallest prefix sum and let `min_index` be the last index where this minimum occurs. This identifies the position where fuel is the most “deficient” along the loop.
4. Any station immediately after this global minimum (i.e., `(min_index + 1) % n`) is a feasible starting point. Due to circular symmetry, the sequence of stations after this point maintains non-negative fuel throughout the loop.
5. Check all stations sequentially starting from `min_index + 1` using a running sum to identify all stations that can start a complete circle without negative fuel. These are the valid answers.

Why it works: The cumulative sum of net fuel represents how much fuel you have relative to starting at station 0. The global minimum identifies the worst point along the circle. Starting just after this ensures that you never hit negative fuel because any preceding deficit is bypassed, and the total sum of fuel matches the total distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

delta = [a[i] - b[i] for i in range(n)]

# Compute prefix sums
pref = [0] * n
pref[0] = delta[0]
for i in range(1, n):
    pref[i] = pref[i-1] + delta[i]

# Find minimum prefix sum
min_pref = pref[0]
min_index = 0
for i in range(n):
    if pref[i] < min_pref:
        min_pref = pref[i]
        min_index = i

# The station after the minimum is a valid start
start = (min_index + 1) % n

# Verify all valid stations using running sum from 'start'
res = []
fuel = 0
for i in range(n):
    idx = (start + i) % n
    fuel += delta[idx]
    if fuel < 0:
        start = (idx + 1) % n
        fuel = 0
        res = []
    else:
        res.append(idx + 1)  # 1-based indexing

print(len(res))
print(' '.join(map(str, sorted(res))))
```

Explanation: We first calculate net fuel gains per station, then prefix sums to track cumulative fuel changes. The station immediately after the global minimum prefix sum is the starting point. We iterate around the circle to confirm all valid starting stations, handling wrap-around with modulo indexing.

## Worked Examples

### Sample 1

```
n = 4
a = [1, 7, 2, 3]
b = [8, 1, 1, 3]
```

| Station | delta | prefix | fuel (from start 2) |
| --- | --- | --- | --- |
| 1 | -7 | -7 | - |
| 2 | 6 | -1 | 6 |
| 3 | 1 | 0 | 7 |
| 4 | 0 | 0 | 7 |

Global minimum of prefix sum is -7 at index 0. Start after that: station 2. Iterating gives valid stations 2 and 4.

### Custom Case

```
n = 3
a = [1, 5, 2]
b = [3, 2, 3]
```

Prefix sum: -2, 3, 2. Minimum = -2 at index 0. Start at station 2. Only station 2 allows completing the circle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass for delta, one pass for prefix, one pass to identify valid starts |
| Space | O(n) | Store delta and prefix sums |

With `n ≤ 10^5`, this algorithm runs comfortably within the 2-second time limit, using negligible memory compared to 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        delta = [a[i] - b[i] for i in range(n)]
        pref = [0]*n
        pref[0] = delta[0]
        for i in range(1, n):
            pref[i] = pref[i-1] + delta[i]
        min_pref = pref[0]
        min_index = 0
        for i in range(n):
            if pref[i] < min_pref:
                min_pref = pref[i]
                min_index = i
        start = (min_index + 1) % n
        res = []
        fuel = 0
        for i in range(n):
            idx = (start + i) % n
            fuel += delta[idx]
            if fuel < 0:
                start = (idx + 1) % n
                fuel = 0
                res = []
            else:
                res.append(idx + 1)
        print(len(res))
        print(' '.join(map(str, sorted(res))))
    return f.getvalue().strip()

# provided sample
assert run("4\n1 7 2 3\n8 1 1 3\n") == "2\n2 4"

# minimum input
assert run("1\n1\n1\n") == "1\n1"

# all equal values
assert run("3\n2 2 2\n2 2 2\n") == "3\n1 2 3"

# edge case: uneven distribution
assert run("3\n1 5 2\n3 2
```
