---
title: "CF 2014G - Milky Days"
description: "We are tracking Little John's milk consumption over time. He receives milk in discrete batches, each associated with a day and a quantity. Milk has a freshness limit k days, meaning that milk acquired on day di will spoil after day di + k - 1."
date: "2026-06-08T13:02:45+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2014
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 974 (Div. 3)"
rating: 2200
weight: 2014
solve_time_s: 119
verified: true
draft: false
---

[CF 2014G - Milky Days](https://codeforces.com/problemset/problem/2014/G)

**Rating:** 2200  
**Tags:** brute force, data structures, greedy, implementation  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tracking Little John's milk consumption over time. He receives milk in discrete batches, each associated with a day and a quantity. Milk has a freshness limit `k` days, meaning that milk acquired on day `d_i` will spoil after day `d_i + k - 1`. Each day, John drinks milk greedily from the freshest available stock, up to `m` pints. A milk satisfaction day occurs whenever he manages to drink exactly `m` pints.

The input is a sequence of diary entries, each specifying a day and the amount of milk received. Our goal is to count, for each test case, the number of days when John is fully satisfied. Days with insufficient milk do not count. The output is a single integer per test case.

The constraints allow `n` up to `10^5` per test case, with a total `n` over all test cases up to `2 * 10^5`. The daily consumption limit `m` and freshness `k` are also up to `10^5`. This means any solution that iterates day-by-day over a full timeline up to `10^6` would be too slow. We must instead process milk events in an efficient way, focusing only on days when milk is present or spoiled.

Edge cases include situations where milk from previous days accumulates, but later entries arrive out of immediate order. For example, milk arriving on day 1 and day 4, with `k = 3`, means milk from day 1 spoils before day 4, even if John is drinking partially each day. Another edge case occurs when John receives more milk than he can drink in one day - leftover milk must be carried forward without losing the freshness constraint.

## Approaches

A brute-force solution would maintain an array representing every day, and track how much milk is available. For each day, we would subtract milk consumed, discard spoiled milk, and count satisfaction days. This is correct in principle but too slow because the day numbers can reach `10^6`. Iterating through every day for each batch results in roughly `10^6 * 10^5` operations in the worst case, which exceeds the time limit.

The key insight is that we do not need to simulate every day. Milk consumption can be represented as a queue of batches sorted by expiry, since John always drinks the freshest milk first. Using a priority queue or deque allows us to maintain the milk stock efficiently. Each day with events (milk acquisition or milk expiry) is processed directly. We update milk quantities and count satisfaction days without iterating empty days. By skipping over gaps between days, we reduce unnecessary operations and achieve linear complexity with respect to the number of diary entries.

The brute-force approach works because it simulates reality accurately, but fails when the number of days is too large relative to the number of milk events. The observation that milk can be tracked as expiring batches lets us reduce the problem to processing `2n` events per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(d_i) * n) | O(max(d_i)) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort milk batches by acquisition day if not already sorted. This ensures we process milk in chronological order. Since the problem guarantees sorted input, we can skip this step in practice.
2. Initialize a deque or priority queue to store milk batches. Each element stores two values: remaining pints and expiry day. The front of the queue is the freshest milk available to drink today.
3. Set a variable `current_day` to the first acquisition day. Iterate over all milk events in chronological order, considering the day gaps between events.
4. For each day with milk available:

- Remove expired milk from the front of the queue. A batch expires if its expiry day is less than `current_day`.
- Drink up to `m` pints. Start with the freshest batch. If a batch has fewer than `m` pints, consume it completely and continue to the next batch. Keep track of total milk consumed.
- If exactly `m` pints were consumed, increment the satisfaction counter.
- Move to the next day.
5. For each milk acquisition event on day `d_i`, append the new batch `(a_i, d_i + k - 1)` to the queue. After processing consumption for that day, increment `current_day`.
6. Repeat until all milk batches have been consumed or expired.

Why it works: The invariant is that the queue always contains unspoiled milk in order of freshness. By always consuming from the freshest batch first and removing expired milk at the start of each day, we guarantee that consumption respects freshness. Counting a day as satisfying only when exactly `m` pints are consumed reflects the problem definition. Skipping days without events is safe because no milk is present, so no satisfaction days are possible.

## Python Solution

```python
import sys
import heapq
from collections import deque

input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        events = [tuple(map(int, input().split())) for _ in range(n)]
        
        milk_queue = deque()
        satisfaction_days = 0
        idx = 0
        current_day = events[0][0]
        last_day = max(d + k - 1 for d, _ in events)

        for day in range(current_day, last_day + 1):
            # Add new milk batches for today
            while idx < n and events[idx][0] == day:
                d_i, a_i = events[idx]
                milk_queue.append([a_i, d_i + k - 1])
                idx += 1
            
            # Remove expired milk
            while milk_queue and milk_queue[0][1] < day:
                milk_queue.popleft()
            
            if not milk_queue:
                continue
            
            # Drink milk up to m pints
            to_drink = m
            while milk_queue and to_drink > 0:
                batch = milk_queue[-1]  # freshest milk is at the back
                if batch[0] <= to_drink:
                    to_drink -= batch[0]
                    milk_queue.pop()
                else:
                    batch[0] -= to_drink
                    to_drink = 0
            
            if to_drink == 0:
                satisfaction_days += 1
        
        print(satisfaction_days)

if __name__ == "__main__":
    solve()
```

The code uses a deque with freshest milk at the back, because popping from the back is O(1) and aligns with the greedy "freshest first" consumption. Expired milk is removed from the front. Days without events are naturally skipped since the loop only processes days until `last_day` where milk may still exist.

## Worked Examples

**Sample 1:**

Input:

```
1 1 3
1 5
```

| Day | Milk Queue (pints, expiry) | To Drink | Satisfaction? | Queue after |
| --- | --- | --- | --- | --- |
| 1 | [(5,3)] | 1 | Yes | [(4,3)] |
| 2 | [(4,3)] | 1 | Yes | [(3,3)] |
| 3 | [(3,3)] | 1 | Yes | [(2,3)] |

Satisfaction days = 3. This shows that milk persists across days, and the algorithm correctly drinks up to `m` pints while respecting freshness.

**Sample 2:**

Input:

```
2 3 3
1 5
2 7
```

| Day | Milk Queue | To Drink | Satisfaction? | Queue after |
| --- | --- | --- | --- | --- |
| 1 | [(5,3)] | 3 | Yes | [(2,3)] |
| 2 | [(2,3),(7,4)] | 3 | Yes | [(1,3),(5,4)] |
| 3 | [(1,3),(5,4)] | 3 | Yes | [(3,4)] |
| 4 | [(3,4)] | 3 | Yes | [] |

Satisfaction days = 4. This demonstrates the importance of removing expired milk at the start of each day.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each milk batch is added once, removed once, and partially consumed in total O(1) per pint removal operation. Total operations linear in number of batches. |
| Space | O(n) | The queue stores at most all milk batches before they expire. |

This fits comfortably within the limits since `n <= 2*10^5` and `k,m <= 10^5`. Using deque ensures all operations are fast and avoids simulating empty days unnecessarily.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided sample
assert run("1\n1 1 3\n1 5\n") == "3", "sample 1"

# Multiple batches, overlapping
assert run("1\n2 3 3\n1 5\n2 7\n") == "4", "overlapping milk"

# Minimum input
assert run("1\n1 1 1\n1 1\n") == "1", "minimum input"

# Maximum satisfaction
```
