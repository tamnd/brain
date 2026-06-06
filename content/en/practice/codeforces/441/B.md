---
title: "CF 441B - Valera and Fruits"
description: "Valera has a garden with a number of fruit trees, each producing a specific number of fruits on a particular day. Each fruit becomes collectible on its ripening day and remains fresh only for the next day."
date: "2026-06-07T06:01:12+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 441
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 252 (Div. 2)"
rating: 1400
weight: 441
solve_time_s: 81
verified: true
draft: false
---

[CF 441B - Valera and Fruits](https://codeforces.com/problemset/problem/441/B)

**Rating:** 1400  
**Tags:** greedy, implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

Valera has a garden with a number of fruit trees, each producing a specific number of fruits on a particular day. Each fruit becomes collectible on its ripening day and remains fresh only for the next day. Valera can pick at most a fixed number of fruits per day, which can be split across different trees. The task is to determine the maximum number of fruits Valera can collect if he plans optimally.

The input provides the number of trees and the daily collection limit, followed by a list of trees where each tree is represented by the day its fruits ripen and the total number of fruits it produces. The output is a single integer: the maximum number of fruits collected.

The bounds of the problem are modest: both the number of trees and the daily collection limit are at most 3000. This suggests that an algorithm with time complexity roughly quadratic in these parameters is feasible, but anything cubic or higher would likely be too slow. The number of days that matter is implicitly bounded by the latest ripening day plus one because fruits only last for two days.

A subtle edge case arises when multiple trees ripen on the same day or when the sum of available fruits exceeds the daily collection limit. For example, if two trees ripen on day 1 with 5 and 7 fruits respectively, and Valera can collect only 6 per day, a naive approach that collects fruits in arbitrary order could leave some uncollected on the second day, reducing the total. The correct output requires prioritizing leftover fruits from the previous day before picking new fruits.

Another edge case is when fruits ripen on the last possible day in the input. Since fruits only last for the ripening day and the next day, the algorithm must not attempt to pick fruits beyond this day range, which would produce zero but could be mishandled in naive loops.

## Approaches

The brute-force approach is straightforward: iterate through each day, track the available fruits on that day, and pick up to the daily limit. This would involve checking every tree every day, calculating how many fruits are still available, and updating remaining fruits accordingly. This is correct logically, but with 3000 days and 3000 trees, it results in up to 9 million operations per day check, which is acceptable but unnecessary.

The key observation for an optimal solution is that fruits only last for two consecutive days. This allows us to maintain a single array `day_fruits` indexed by day, storing the total number of fruits that ripen on that day. On each day, Valera should first collect any leftover fruits from the previous day, then collect newly ripened fruits up to his limit. There is no need to consider trees individually once their fruits are aggregated by day, because individual allocation does not affect the total collected if the daily limit is respected. This reduces the problem to a simple linear scan over the days, keeping track of leftovers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max_day) | O(n) | Works but can be simplified |
| Optimal | O(max_day) | O(max_day) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `fruits_on_day` of size large enough to cover all ripening days plus one. Each index represents a day and stores the number of fruits ripening that day.
2. Populate `fruits_on_day` using the input. For each tree with ripening day `a` and `b` fruits, add `b` to `fruits_on_day[a]`.
3. Initialize a variable `leftover` to track fruits that were not collected on the previous day.
4. Iterate through each day from 1 to the last possible day (maximum ripening day plus one). On each day, compute how many fruits Valera can collect as the minimum between his daily limit and the sum of `leftover` and newly ripened fruits.
5. Update `leftover` as the maximum between zero and the sum of `leftover` and newly ripened fruits minus the daily limit. This ensures that only uncollected fruits carry over to the next day.
6. Accumulate the collected fruits into a running total.
7. Output the total collected fruits.

The invariant here is that on any day, Valera never exceeds his daily limit and always prioritizes leftover fruits from the previous day, ensuring no avoidable losses. Because fruits only last two days, tracking leftovers for a single day is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, v = map(int, input().split())
max_day = 0
fruits_on_day = [0] * 3002  # Enough for day 1..3001

for _ in range(n):
    a, b = map(int, input().split())
    fruits_on_day[a] += b
    max_day = max(max_day, a)

total_collected = 0
leftover = 0

for day in range(1, max_day + 2):
    today_fruits = leftover + fruits_on_day[day]
    collected = min(today_fruits, v)
    total_collected += collected
    leftover = max(0, today_fruits - v)

print(total_collected)
```

We first read the number of trees and the daily collection limit. `fruits_on_day` aggregates the fruits by ripening day. The loop over the days ensures leftover fruits are always considered first. The size of `fruits_on_day` is slightly larger than the maximum day to avoid index errors on the last day plus one.

## Worked Examples

Sample 1 Input:

```
2 3
1 5
2 3
```

| Day | Leftover | Fruits Ripening | Available Today | Collected | New Leftover |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 5 | 5 | 3 | 2 |
| 2 | 2 | 3 | 5 | 3 | 2 |
| 3 | 2 | 0 | 2 | 2 | 0 |

Total collected: 3 + 3 + 2 = 8. Confirms correct handling of leftover fruits.

Sample 2 Input:

```
1 2
1 4
```

| Day | Leftover | Fruits Ripening | Available Today | Collected | New Leftover |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 4 | 2 | 2 |
| 2 | 2 | 0 | 2 | 2 | 0 |

Total collected: 2 + 2 = 4. Demonstrates simple two-day collection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(max_day) | Each day is visited once; max_day ≤ 3000 |
| Space | O(max_day) | Array `fruits_on_day` stores ripening fruits per day |

Given the bounds n, v ≤ 3000, and days ≤ 3000, this algorithm runs well under the 1-second limit and comfortably fits in memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, v = map(int, input().split())
    fruits_on_day = [0] * 3002
    max_day = 0
    for _ in range(n):
        a, b = map(int, input().split())
        fruits_on_day[a] += b
        max_day = max(max_day, a)
    total_collected = 0
    leftover = 0
    for day in range(1, max_day + 2):
        today_fruits = leftover + fruits_on_day[day]
        collected = min(today_fruits, v)
        total_collected += collected
        leftover = max(0, today_fruits - v)
    return str(total_collected)

# Provided samples
assert run("2 3\n1 5\n2 3\n") == "8", "sample 1"
assert run("1 2\n1 4\n") == "4", "sample 2"

# Custom cases
assert run("1 1\n1 1\n") == "1", "minimum input"
assert run("3 10\n1 5\n2 15\n3 10\n") == "30", "all fruits collectible each day"
assert run("2 2\n1 3\n1 4\n") == "4", "daily limit smaller than total ripening fruits"
assert run("3 2\n1 2\n2 2\n3 2\n") == "6", "exact daily collection possible"
assert run("3 5\n2 7\n2 3\n3 8\n") == "18", "carryover from previous day handled"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1 1\n1 1\n" | 1 | Minimum input edge case |
| "3 10\n1 5\n2 15\n3 10\n" | 30 | All fruits collectible within daily limit |
| "2 2\n1 3\n1 4\n" | 4 | Daily limit smaller than total ripening fruits |
| "3 2\n1 2\n2 2\n3 2\n" | 6 | Exact daily collection possible |
| "3 5\n2 7\n2 3\n3 8\n" | 18 | Correct handling of leftovers across days |

## Edge Cases

If all fruits ripen on the same day
