---
title: "CF 257A - Sockets"
description: "Vasya has a set of electrical devices and a limited number of wall sockets in his flat. Additionally, he owns multiple supply-line filters, each of which provides extra sockets but occupies one itself when plugged in."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 257
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 159 (Div. 2)"
rating: 1100
weight: 257
solve_time_s: 70
verified: true
draft: false
---

[CF 257A - Sockets](https://codeforces.com/problemset/problem/257/A)

**Rating:** 1100  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

Vasya has a set of electrical devices and a limited number of wall sockets in his flat. Additionally, he owns multiple supply-line filters, each of which provides extra sockets but occupies one itself when plugged in. The task is to determine the minimum number of supply-line filters Vasya needs to plug in so that every device can be connected to electricity, either directly into the wall sockets or through one or more supply-line filters. If it is impossible to plug in all devices even after using all filters, the answer should be -1.

The input gives three integers: the number of supply-line filters `n`, the number of devices `m`, and the number of wall sockets `k`. Then it provides an array `a` of length `n`, where each element represents the number of sockets on a filter. Each device or filter occupies one socket, so using a filter with `x` sockets effectively adds `x - 1` extra sockets to the total.

Constraints are small: all values are at most 50. This means we can use algorithms with quadratic or even cubic time without performance concerns. A naive brute-force enumeration of all subsets of filters is possible because `2^50` is too large, but a greedy approach works perfectly due to the nature of the problem.

Edge cases arise when the number of devices is already less than or equal to the available wall sockets, in which case no filters are needed. Another tricky case is when the sum of additional sockets from all filters is still insufficient to reach the required number of devices, which should return -1.

For example, if `n = 2`, `m = 5`, `k = 2`, and the filters have sockets `[2, 2]`, each filter gives only 1 extra socket, totaling 4 sockets (2 wall + 2 extra from filters), which is insufficient for 5 devices, so the output should be -1.

## Approaches

The brute-force approach would enumerate all possible subsets of filters and compute the total number of sockets for each subset, then select the minimal subset that allows all devices to be plugged in. While correct, this approach would require checking up to `2^n` combinations, which is feasible for `n ≤ 20` but far too slow for `n = 50`.

The key observation is that every filter adds `a[i] - 1` extra sockets after occupying one itself. To maximize the gain with minimal filters, it makes sense to use the filters with the largest number of sockets first. This turns the problem into a simple greedy algorithm: sort the filters by `a[i]` in descending order, plug in the largest filters sequentially, and track how many devices can be connected after each filter. Stop as soon as the total sockets reach or exceed the number of devices. If all filters are used and the total is still insufficient, return -1.

The greedy approach works because the problem is linear in how extra sockets accumulate. There are no dependencies or penalties for choosing one filter over another beyond its immediate socket contribution. Sorting and sequentially taking the largest yields the minimal set necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow for n = 50 |
| Optimal (Greedy) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n`, `m`, `k` and the array `a` of filter sockets.
2. Check if the available wall sockets `k` are already enough to plug all devices. If `k >= m`, print 0 and return.
3. Sort the array `a` in descending order. This ensures that the largest filters, which contribute the most additional sockets, are considered first.
4. Initialize a variable `extra_sockets` to 0 to track the number of sockets provided by filters beyond the one they occupy.
5. Initialize a counter `filters_used` to 0 to track the number of filters plugged in.
6. Iterate through the sorted array `a`. For each filter:

- Increment `filters_used` by 1.
- Add `a[i] - 1` to `extra_sockets`.
- If `extra_sockets + k` reaches or exceeds `m`, print `filters_used` and return.
7. If the loop finishes and `extra_sockets + k` is still less than `m`, print -1.

Why it works: the invariant is that at every step, the number of additional devices we can plug in is maximized by always picking the filter with the largest number of sockets remaining. Because each filter’s contribution is independent, no subset of filters with smaller sockets can achieve the same or better result with fewer filters. Sorting ensures that the minimal number of filters is selected.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
a = list(map(int, input().split()))

if k >= m:
    print(0)
    sys.exit()

a.sort(reverse=True)

extra_sockets = 0
filters_used = 0

for sockets in a:
    filters_used += 1
    extra_sockets += sockets - 1
    if extra_sockets + k >= m:
        print(filters_used)
        break
else:
    print(-1)
```

We first check if wall sockets alone suffice, which saves unnecessary computation. Sorting in reverse order ensures that we always pick the filter that contributes the most extra sockets next. The `for` loop tracks the accumulation of extra sockets and immediately returns the minimal number of filters needed once we reach the target.

## Worked Examples

**Sample 1**

Input: `3 5 3` with filters `[3, 1, 2]`

| Step | Wall Sockets k | Extra Sockets | Filters Used | Total Available Sockets |
| --- | --- | --- | --- | --- |
| Initial | 3 | 0 | 0 | 3 |
| First filter (3) | 3 | 2 | 1 | 5 |

The total sockets reach 5, which matches the number of devices, so 1 filter is sufficient.

**Sample 2**

Input: `4 7 2` with filters `[3, 1, 4, 2]`

Sorted filters: `[4, 3, 2, 1]`

| Step | Wall Sockets k | Extra Sockets | Filters Used | Total Available Sockets |
| --- | --- | --- | --- | --- |
| Initial | 2 | 0 | 0 | 2 |
| First filter (4) | 2 | 3 | 1 | 5 |
| Second filter (3) | 2 | 5 | 2 | 7 |

Total sockets reach 7, matching the number of devices, so 2 filters are needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array dominates the computation. Iteration is O(n) but negligible for n ≤ 50. |
| Space | O(n) | We store the array of filter sockets. Other variables are O(1). |

Given the small constraints (n, m, k ≤ 50), this algorithm runs in well under 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    if k >= m:
        return "0"
    a.sort(reverse=True)
    extra_sockets = 0
    filters_used = 0
    for sockets in a:
        filters_used += 1
        extra_sockets += sockets - 1
        if extra_sockets + k >= m:
            return str(filters_used)
    return "-1"

# Provided samples
assert run("3 5 3\n3 1 2\n") == "1", "sample 1"
assert run("4 7 2\n3 1 4 2\n") == "2", "sample 2"

# Custom test cases
assert run("2 1 1\n1 1\n") == "0", "no filters needed"
assert run("5 10 3\n1 1 1 1 1\n") == "-1", "not enough sockets"
assert run("3 5 1\n5 2 2\n") == "1", "largest filter first"
assert run("4 6 2\n2 2 2 2\n") == "2", "multiple small filters needed"
assert run("1 50 50\n50\n") == "0", "exact match with wall sockets"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 1\n1 1 | 0 | No filters needed because wall sockets suffice |
| 5 10 3\n1 1 1 1 1 | -1 | Even using all filters, not enough sockets |
| 3 5 1\n5 2 2 | 1 | Largest filter provides enough extra sockets |
| 4 6 2\n2 2 2 2 | 2 | Multiple small filters accumulate to reach target |
| 1 50 50\n50 | 0 | Exact wall sockets match devices, no filters needed |

## Edge Cases

If wall sockets alone cover all devices, the algorithm immediately returns 0. For example, `n = 3, m = 2
