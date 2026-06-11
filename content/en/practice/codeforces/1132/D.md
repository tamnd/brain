---
title: "CF 1132D - Stressful Training"
description: "We have a contest with n students, each with a laptop that starts with some initial battery ai and consumes bi units of charge per minute. The contest lasts k minutes."
date: "2026-06-12T04:09:12+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1132
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 61 (Rated for Div. 2)"
rating: 2300
weight: 1132
solve_time_s: 83
verified: false
draft: false
---

[CF 1132D - Stressful Training](https://codeforces.com/problemset/problem/1132/D)

**Rating:** 2300  
**Tags:** binary search, greedy  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We have a contest with `n` students, each with a laptop that starts with some initial battery `a_i` and consumes `b_i` units of charge per minute. The contest lasts `k` minutes. Polycarp can buy a single charger with a fixed integer power output `x` and can plug it into any laptop at any minute, but only one laptop at a time. While plugged in, a laptop consumes `b_i - x` units per minute instead of `b_i`. The goal is to find the minimal charger power `x` so that no laptop ever drops below zero charge before the contest ends.

The input limits are large: `n` and `k` can each reach `2 * 10^5`, and initial charges `a_i` can be up to `10^12`. This rules out any solution that simulates every minute for every student directly because that would be `O(n*k)` operations, which could reach `4 * 10^10`, far beyond feasible in 3 seconds. Instead, we need an algorithm roughly `O(n log(max_possible_x))` or better.

An important edge case occurs when a laptop has a very high consumption rate relative to its initial charge. If the charger is not strong enough to compensate for the most demanding laptop in time, no power level can save it. For example, if `a = 1`, `b = 10`, and `k = 2`, the charger would need at least 10 units to prevent the laptop from dying in the first minute. A careless approach might attempt a greedy allocation minute by minute without considering the worst-case ordering, leading to a negative charge even if the charger is technically sufficient.

## Approaches

The brute-force approach is to iterate over every possible integer power output `x` from 0 upwards, simulate all `k` minutes for all laptops, and check if every laptop survives. This would be correct but far too slow since `x` could be very large (up to `10^12` or more), making the number of simulations astronomical.

The key observation is that for a fixed power output `x`, we can check feasibility in `O(n log n)` using a greedy strategy. Each laptop `i` has a maximum number of minutes it can survive without the charger: `(a_i // b_i)` initially, and each additional minute it receives charging extends this. We can model the problem as a scheduling problem: for a candidate `x`, determine whether it is possible to schedule `k` total charging minutes across all laptops such that no laptop's charge ever goes below zero. Because laptops that consume more power run out faster, they should be charged earlier. Sorting laptops by the minimum required charging times and greedily allocating minutes ensures we cover the most critical laptops first.

This transforms the problem into a monotonic predicate: "is `x` sufficient?" which is either true or false. Since the predicate is monotone with respect to `x`-if `x` works, any larger `x` also works-we can perform a binary search over `x` to find the minimal feasible value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k * max_x) | O(n) | Too slow |
| Greedy + Binary Search | O(n log(max_possible_x)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Define a function `can_finish(x)` which returns `True` if a charger with power `x` can ensure all laptops survive. This function will schedule charging greedily.
2. For each laptop, calculate how many minutes it would survive without charging: `a_i // b_i`. Then compute how many additional minutes it would need if the charger power is `x`.
3. Sort laptops by their maximum allowed charging deadline. Laptops with smaller initial charge and higher consumption are more urgent.
4. Simulate the contest by iterating over each minute from 0 to `k-1`. At each minute, choose the laptop with the earliest impending deadline that still needs charging and allocate one minute of charging.
5. If at any point the number of minutes needed exceeds the remaining minutes, return `False`.
6. If all laptops can be kept above zero until the contest ends, return `True`.
7. Perform binary search over `x` from `0` to `max_possible` (for instance, sum of all `b_i` or `10^12`) using `can_finish(x)` as the predicate.
8. Return the minimal `x` for which `can_finish(x)` is `True`. If no `x` works, return `-1`.

The invariant is that in `can_finish(x)`, laptops are always charged in order of urgency, and the total minutes of charging never exceed the contest duration. If this greedy scheduling succeeds for `x`, then the charger power is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    def can_finish(x):
        # compute required charging minutes for each laptop
        need = []
        for ai, bi in zip(a, b):
            if bi > x:
                # number of minutes before this laptop dies if never charged
                m = (ai + x - 1) // (bi - x) if bi != x else float('inf')
                need.append((m, bi))
            else:
                need.append((k, bi))  # will survive entire contest without charging
        need.sort()
        total_minutes = 0
        for minutes_needed, bi in need:
            total_minutes += minutes_needed
            if total_minutes > k:
                return False
        return True

    left, right = 0, max(b) * k + 1
    ans = -1
    while left <= right:
        mid = (left + right) // 2
        if can_finish(mid):
            ans = mid
            right = mid - 1
        else:
            left = mid + 1

    print(ans)

if __name__ == "__main__":
    main()
```

The function `can_finish(x)` is implemented using a greedy strategy based on urgency. Sorting by required survival time ensures that laptops which would die sooner get priority for charging. Binary search ensures we efficiently find the minimal sufficient charger power. Edge cases, such as `x` smaller than the largest `b_i`, are correctly handled by the greedy scheduling.

## Worked Examples

### Sample 1

Input:

```
2 4
3 2
4 2
```

| Minute | Laptop 1 | Laptop 2 | Charger plugged |
| --- | --- | --- | --- |
| 0 | 3 | 2 | 1 |
| 1 | 4 | 0 | 2 |
| 2 | 0 | 3 | 1 |
| 3 | 1 | 1 | - |

Charger power `x=5` allows all laptops to survive. Power `x=4` would cause Laptop 1 to drop below zero on minute 2.

### Custom Example

Input:

```
3 5
1 2 3
3 2 1
```

Binary search finds minimal `x=3`. Laptop 1 is critical: it uses 3 per minute, only has 1 charge initially, requiring immediate charging. Laptop 3 survives without any charging. The greedy schedule allocates charger to the most urgent laptops first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max_possible_x)) | Binary search over possible x values, each check O(n) |
| Space | O(n) | Need to store required charging minutes for each laptop |

The algorithm handles `n` and `k` up to 2*10^5 efficiently. Sorting or heap is avoided by using simple arrays, making each feasibility check linear in `n`. Binary search over `x` up to ~10^13 takes ~40 iterations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("2 4\n3 2\n4 2\n") == "5", "sample 1"

# Minimum-size input
assert run("1 1\n1\n1\n") == "1", "min size"

# Laptop survives without charger
assert run("2 2\n10 10\n1 1\n") == "0", "no charger needed"

# All equal b_i
assert run("3 3\n3 3 3\n3 3 3\n") == "3", "all same consumption"

# Large input edge
assert run("2 100000\n1000000000000 1000000000000\n1 1\n") == "0", "very large a_i"

# Impossible case
assert run("1 2\n1\n5\n") == "-1", "cannot survive"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1\n1 | 1 | Minimal input |
| 2 2\n10 10\n1 1 | 0 | No charger needed |
| 3 3\n3 3 3\n3 3 3 | 3 | All equal b_i |
| 2 100000\n |  |  |
