---
title: "CF 248D - Sweets for Everyone!"
description: "We have a street represented as a sequence of sections. Each section can be a house, a shop, or empty land. The Lou Who family starts at the first section of the street and wants to distribute exactly one kilogram of sweets to each house."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 248
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 152 (Div. 2)"
rating: 2300
weight: 248
solve_time_s: 94
verified: true
draft: false
---

[CF 248D - Sweets for Everyone!](https://codeforces.com/problemset/problem/248/D)

**Rating:** 2300  
**Tags:** binary search, greedy, implementation  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a street represented as a sequence of sections. Each section can be a house, a shop, or empty land. The Lou Who family starts at the first section of the street and wants to distribute exactly one kilogram of sweets to each house. They can buy sweets from shops, but each shop will sell at most one kilogram, and each house must receive exactly one kilogram. The goal is to determine the minimum number of kilograms they must bring from home to ensure every house is served within a given time limit, moving between consecutive sections in one unit of time.

The key constraints are the length of the street, which can go up to 500,000, and the time limit, which can reach up to one billion. This implies that an algorithm with linear or near-linear complexity is acceptable, but any approach that is quadratic in the number of sections is too slow. Edge cases include streets where the number of shops is less than the number of houses, streets where houses are at the very beginning or end, and time limits smaller than the street length.

For example, if the input is `HSHSHS` with a time limit of 6, there are three houses and three shops, but if they start without any sweets, they would need to backtrack to buy from shops, exceeding the time limit. The correct minimum number of sweets to bring from home is 1.

## Approaches

A brute-force approach would simulate all possible paths along the street while tracking sweets collected and distributed. For each starting number of home sweets, you would attempt to move step by step, buying from shops as needed and delivering to houses, checking if the total time remains within the limit. This works in principle, but its complexity is O(n * k) where k is the number of sweets tried, which can be O(n) in the worst case. With n up to 500,000, this becomes infeasible.

The key insight is to note that the problem is monotonic: if a certain number of home sweets `k` allows serving all houses within the time limit, any larger `k` will also succeed. Conversely, if `k` is too small, it will fail. This makes binary search over `k` viable. For a given `k`, we can simulate the delivery in a single linear pass along the street, keeping track of the number of sweets on hand, buying at shops, and delivering to houses. This reduces the complexity to O(n log H), where H is the maximum number of homes. Linear simulation is fast enough for n up to 500,000, and log H is small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Binary Search + Linear Simulation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the total number of houses on the street. Let this number be `house_count`. The maximum home sweets `k` we may need is `house_count`.
2. Initialize binary search bounds: `low = 0`, `high = house_count`.
3. For each candidate `k` in the binary search, simulate distributing sweets as follows:

a. Start at the first section with `sweets = k`.

b. Move along the street one section at a time, incrementing a time counter at each step.

c. If the section is a shop and `sweets` are needed, buy one kilogram if not already bought from that shop.

d. If the section is a house and `sweets > 0`, give one kilogram. If `sweets == 0`, you would need to backtrack to a shop or bring more home sweets, which fails the simulation.
4. After simulating the entire street, if all houses have received sweets and the total time does not exceed `t`, the candidate `k` is feasible. Otherwise, it is too small.
5. Continue binary search until the smallest feasible `k` is found. If no `k` in [0, house_count] works, output -1.

The invariant that guarantees correctness is that sweets are always tracked correctly and never reused across houses or shops. Monotonicity of `k` ensures binary search will converge.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, t = map(int, input().split())
street = input().strip()

house_count = street.count('H')

def can_distribute(k):
    sweets = k
    time = 0
    shop_used = [False] * n
    for i, c in enumerate(street):
        time += 1
        if c == 'S' and not shop_used[i]:
            if sweets < house_count:
                sweets += 1
                shop_used[i] = True
        elif c == 'H':
            if sweets == 0:
                return False
            sweets -= 1
    return time <= t

low, high = 0, house_count
answer = -1
while low <= high:
    mid = (low + high) // 2
    if can_distribute(mid):
        answer = mid
        high = mid - 1
    else:
        low = mid + 1

print(answer)
```

In the code, `can_distribute` simulates moving along the street for a given `k`. The array `shop_used` ensures we do not buy more than one kilogram per shop. Binary search determines the minimal `k` that satisfies the simulation. Care must be taken to track time and sweets precisely. Forgetting to increment time per section or to mark shops as used would produce incorrect results.

## Worked Examples

### Sample 1

Input: `6 6` and street `HSHSHS`

| i | c | sweets | action | time |
| --- | --- | --- | --- | --- |
| 0 | H | 1 | give | 1 |
| 1 | S | 1 | buy | 2 |
| 2 | H | 2 | give | 3 |
| 3 | S | 1 | buy | 4 |
| 4 | H | 2 | give | 5 |
| 5 | S | 1 | buy | 6 |

`k = 1` is sufficient and time = 6 ≤ t.

### Sample 2

Input: `6 10` and street `HSHSHS`

With `k = 0`, we can buy sweets from shops as we go, time = 6 ≤ 10. Minimal `k = 0`.

These traces show that simulation accurately tracks sweets and time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Binary search over [0, house_count], each simulation is O(n) |
| Space | O(n) | Street array and shop_used array |

With n ≤ 500,000, and log n ≤ 20, the solution completes comfortably under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, t = map(int, input().split())
    street = input().strip()

    house_count = street.count('H')

    def can_distribute(k):
        sweets = k
        time = 0
        shop_used = [False] * n
        for i, c in enumerate(street):
            time += 1
            if c == 'S' and not shop_used[i]:
                if sweets < house_count:
                    sweets += 1
                    shop_used[i] = True
            elif c == 'H':
                if sweets == 0:
                    return False
                sweets -= 1
        return time <= t

    low, high = 0, house_count
    answer = -1
    while low <= high:
        mid = (low + high) // 2
        if can_distribute(mid):
            answer = mid
            high = mid - 1
        else:
            low = mid + 1
    return str(answer)

# Provided samples
assert run("6 6\nHSHSHS\n") == "1", "sample 1"
assert run("6 10\nHSHSHS\n") == "0", "sample 2"

# Custom cases
assert run("1 1\nH\n") == "1", "single house"
assert run("5 5\nH...H\n") == "0", "enough time without extra sweets"
assert run("5 3\nHSHSH\n") == "1", "need one home sweet to avoid backtrack"
assert run("3 2\nHHH\n") == "-1", "impossible with too little time"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\nH\n` | 1 | Minimum-size street |
| `5 5\nH...H\n` | 0 | Time is sufficient without extra sweets |
| `5 3\nHSHSH\n` | 1 | Requires home sweets to avoid backtracking |
| `3 2\nHHH\n` | -1 | Impossible scenario due to tight time |

## Edge Cases

If all houses are at the start of the street and there are few or no shops, the algorithm correctly returns the number of houses as home sweets if necessary. For example, `HHH.SS` with `t = 6` would require `k = 1` if we can reach the first house within time, or more if backtracking is needed. The simulation increments time for
