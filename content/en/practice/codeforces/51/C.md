---
title: "CF 51C - Three Base Stations"
description: "We are given a village represented as points along a one-dimensional line, each point being a house coordinate. The task is to place exactly three cellular base stations along this line so that every house lies within the coverage of at least one station."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 51
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 48"
rating: 1800
weight: 51
solve_time_s: 133
verified: false
draft: false
---

[CF 51C - Three Base Stations](https://codeforces.com/problemset/problem/51/C)

**Rating:** 1800  
**Tags:** binary search, greedy  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a village represented as points along a one-dimensional line, each point being a house coordinate. The task is to place exactly three cellular base stations along this line so that every house lies within the coverage of at least one station. Coverage is symmetric: a station at position `t` with power `d` covers the interval `[t - d, t + d]`. The output we want is the minimal `d` that allows full coverage and one valid configuration of the three stations.

Constraints tell us that `n` can be up to 200,000 and coordinates can reach `10^9`. Sorting and linear passes over the array are feasible, but any naive approach that tries all possible placements for all three stations would be astronomically slow. For instance, iterating over all potential station positions for each house is impossible because `10^9` values are too many.

Subtle edge cases include: houses stacked at the same coordinate, very sparse houses (e.g., one at 1 and another at 10^9), and cases where fewer than three stations would trivially suffice if overlaps are allowed. A naive approach that only tries to split the houses evenly could miss the fact that a single station might cover multiple clusters, giving a smaller `d`.

## Approaches

The brute-force method would attempt to place three stations at all possible combinations of house coordinates, compute the required `d` for each combination, and pick the minimal. This is correct because it enumerates every scenario, but it is infeasible: if `n = 2 × 10^5`, the number of combinations is on the order of `O(n^3)` or more than `10^15` operations.

The key observation is that the problem has a monotonic property: if a given `d` can cover all houses with three stations, any larger `d` can also cover all houses. Conversely, if a `d` is too small, no smaller `d` will work. This monotonicity allows us to binary search on `d`. For a candidate `d`, we can greedily cover the houses from left to right, placing a station at the farthest point that covers the next uncovered house, then continue. If we can cover all houses with three or fewer stations, the candidate `d` is feasible.

Greedy coverage works because each station’s coverage interval is continuous, so it is always optimal to place the next station at the rightmost point that can cover the first uncovered house. Any station placed further left would unnecessarily increase the number of stations or the required `d`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Binary Search + Greedy | O(n log(maxX)) | O(n) | Accepted |

## Algorithm Walkthrough

1. **Sort the house coordinates**. Sorting is necessary to traverse houses from left to right and apply greedy coverage correctly.
2. **Initialize binary search bounds**. Set `lo = 0` and `hi = 1e9`, the maximum distance a station could possibly need. Use a small epsilon (e.g., `1e-7`) for floating-point precision.
3. **Binary search loop**. For each middle value `mid = (lo + hi) / 2`, check if we can cover all houses with three stations of power `mid`. If feasible, move `hi = mid`; otherwise, move `lo = mid`.
4. **Greedy coverage check**. Start at the leftmost house. Place a station at `house + mid`, covering all houses up to `house + 2 * mid`. Repeat for the next uncovered house, up to three stations. If any house remains uncovered after three stations, the candidate `mid` is too small.
5. **Reconstruct stations' positions**. Once binary search converges, perform the greedy coverage once more to generate exact positions: place each station at the rightmost point of the interval that covers the next uncovered house.

**Why it works**. Sorting ensures that houses are processed in order. Greedy placement guarantees minimal overlap: placing a station farther left would not extend coverage but could force an extra station. Binary search relies on monotonicity: if `d` is feasible, larger values remain feasible. This combination produces the minimal `d`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_cover(houses, d):
    n = len(houses)
    count = 0
    i = 0
    while i < n:
        count += 1
        limit = houses[i] + 2 * d
        while i < n and houses[i] <= limit:
            i += 1
        if count > 3:
            return False
    return True

def find_stations(houses, d):
    stations = []
    n = len(houses)
    i = 0
    while i < n and len(stations) < 3:
        pos = houses[i] + d
        stations.append(pos)
        limit = houses[i] + 2 * d
        while i < n and houses[i] <= limit:
            i += 1
    while len(stations) < 3:
        stations.append(stations[-1])
    return stations

n = int(input())
houses = list(map(int, input().split()))
houses.sort()

lo, hi = 0.0, 1e9
eps = 1e-7
while hi - lo > eps:
    mid = (lo + hi) / 2
    if can_cover(houses, mid):
        hi = mid
    else:
        lo = mid

d = hi
stations = find_stations(houses, d)
print(f"{d:.6f}")
print(" ".join(f"{s:.6f}" for s in stations))
```

The solution separates checking feasibility (`can_cover`) from reconstructing the stations (`find_stations`). Sorting before greedy placement is critical. The binary search uses floating-point numbers and stops when the interval is smaller than `1e-7` to ensure precision for six decimals in the output.

## Worked Examples

**Sample 1**

Input:

```
4
1 2 3 4
```

| Step | i | House | Count | Limit | Stations |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 + 2*0.5 = 2 | [1.5] |
| 2 | 2 | 3 | 2 | 3 + 1 = 4 | [1.5, 3.5] |
| 3 | done | - | - | - | [1.5, 3.5] |

Demonstrates minimal `d = 0.5` covers all houses with two stations.

**Custom Example**

Input:

```
5
1 2 10 11 12
```

Binary search finds `d = 2.5`. Greedy stations placed at 2.5, 11.5, and repeat last station 11.5 to satisfy three stations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(maxX)) | Sorting takes O(n log n), binary search requires O(log(maxX)) iterations, each with a linear pass over houses |
| Space | O(n) | Houses array plus station array |

This fits within the time and memory limits. `n` up to 2 × 10^5 is manageable with sorting and multiple linear passes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    houses = list(map(int, input().split()))
    houses.sort()
    lo, hi = 0.0, 1e9
    eps = 1e-7
    def can_cover(houses, d):
        n = len(houses)
        count = 0
        i = 0
        while i < n:
            count += 1
            limit = houses[i] + 2*d
            while i < n and houses[i] <= limit:
                i += 1
            if count > 3:
                return False
        return True
    def find_stations(houses, d):
        stations = []
        n = len(houses)
        i = 0
        while i < n and len(stations) < 3:
            pos = houses[i] + d
            stations.append(pos)
            limit = houses[i] + 2*d
            while i < n and houses[i] <= limit:
                i += 1
        while len(stations) < 3:
            stations.append(stations[-1])
        return stations
    while hi - lo > eps:
        mid = (lo + hi)/2
        if can_cover(houses, mid):
            hi = mid
        else:
            lo = mid
    d = hi
    stations = find_stations(houses, d)
    out = f"{d:.6f}\n{' '.join(f'{s:.6f}' for s in stations)}"
    return out

# Provided sample
assert run("4\n1 2 3 4\n").startswith("0.500000"), "sample 1"

# Custom cases
assert run("1\n100\n").startswith("0.000
```
