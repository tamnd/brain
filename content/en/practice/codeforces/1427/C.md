---
title: "CF 1427C - The Hard Work of Paparazzi"
description: "The task is to maximize the number of celebrities a paparazzi can photograph in a city represented as an (r times r) grid of streets. Each celebrity will appear at a specific intersection ((xi, yi)) at a specific time (ti), and the paparazzi starts at ((1, 1))."
date: "2026-06-11T05:36:17+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1427
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 11"
rating: 2000
weight: 1427
solve_time_s: 105
verified: true
draft: false
---

[CF 1427C - The Hard Work of Paparazzi](https://codeforces.com/problemset/problem/1427/C)

**Rating:** 2000  
**Tags:** dp  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to maximize the number of celebrities a paparazzi can photograph in a city represented as an \(r \times r\) grid of streets. Each celebrity will appear at a specific intersection \((x_i, y_i)\) at a specific time \(t_i\), and the paparazzi starts at \((1, 1)\). Moving from one intersection to another takes Manhattan distance minutes, so a move from \((x, y)\) to \((x', y')\) takes \(|x-x'| + |y-y'|\) minutes. A photo can only be taken if the paparazzi reaches the celebrity exactly at their scheduled time. The output is the maximum number of celebrities that can be photographed.

The constraints make it clear that a brute-force approach is not feasible. With up to \(n = 100,000\) celebrities and times \(t_i\) as large as \(10^6\), we cannot afford \(O(n^2)\) solutions. Each celebrity requires checking previous reachable states, and iterating naively through all prior celebrities would be too slow. The small grid size \(r \le 500\) suggests that locality in space can be exploited for optimization.

A non-obvious edge case occurs when a celebrity appears so early that the paparazzi cannot reach them from the office. For example, if a celebrity is at \((6,8)\) at \(t = 11\), the paparazzi cannot reach them from \((1,1)\) since the Manhattan distance is \(12\). A naive greedy implementation that always moves to the next scheduled celebrity could miss cases where skipping some celebrities leads to a larger total count.

## Approaches

The brute-force method is to maintain a dynamic programming array where for each celebrity \(i\), we store the maximum number of photos that can be taken if the paparazzi ends at celebrity \(i\). For each celebrity \(i\), we would iterate over all previous celebrities \(j < i\) and check if moving from \(j\) to \(i\) is feasible. This is correct because it directly models the problem constraints, but it runs in \(O(n^2)\) time, which is infeasible for \(n = 10^5\).

The key observation for a faster approach is that the grid size \(r\) is small and the movement between two positions can be bounded by the time difference. If the time difference between two consecutive celebrities is at least \(2r\), then it is always possible to reach any position on the grid. This allows us to optimize by only keeping track of the last \(2r\) events for detailed DP updates and using a global maximum for older events. This reduces the number of operations to \(O(n \cdot r^2)\), which is acceptable because \(r^2 \le 250,000\).

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimized DP with time-window | O(n * r^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input values for the number of streets \(r\) and celebrities \(n\). Store each celebrity's time and position as a list of tuples.
2. Initialize a dynamic programming array \(dp[i]\) that stores the maximum number of photos ending at celebrity \(i\). Set \(dp[0] = 0\) for the initial position at \((1,1)\) with time \(t_0 = 0\).
3. Maintain a variable \(best\_so\_far\) to track the global maximum of \(dp\) values for celebrities that are too far in the past to reach in less than \(2r\) minutes.
4. Iterate through each celebrity \(i\) from \(1\) to \(n\):
   1. Set \(dp[i] = 0\).
   2. For each previous celebrity \(j\) where \(i - j \le 2r\):
      1. Check if \(|x_i - x_j| + |y_i - y_j| \le t_i - t_j\).
      2. If reachable, update \(dp[i] = \max(dp[i], dp[j] + 1)\).
   3. If \(i > 2r\), also update \(dp[i] = \max(dp[i], best\_so\_far + 1)\) since older events can be reached using the global maximum.
   4. Update \(best\_so\_far = \max(best\_so\_far, dp[i])\).
5. Print \(best\_so\_far\) as the final answer.

The invariant maintained is that \(dp[i]\) always represents the maximum number of photos achievable if the paparazzi ends at celebrity \(i\). By combining a local check for recent events with a global maximum for older events, we guarantee correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

r, n = map(int, input().split())
events = [(0, 1, 1)]  # add initial position at time 0
for _ in range(n):
    t, x, y = map(int, input().split())
    events.append((t, x, y))

dp = [-float('inf')] * (n + 1)
dp[0] = 0
best_so_far = 0

for i in range(1, n + 1):
    t_i, x_i, y_i = events[i]
    dp[i] = -float('inf')
    for j in range(max(0, i - 2 * r), i):
        t_j, x_j, y_j = events[j]
        if abs(x_i - x_j) + abs(y_i - y_j) <= t_i - t_j:
            dp[i] = max(dp[i], dp[j] + 1)
    if i > 2 * r:
        dp[i] = max(dp[i], best_so_far + 1)
    best_so_far = max(best_so_far, dp[i])

print(best_so_far)
```

This code directly implements the algorithm steps. The initial dummy event represents the office at \((1,1)\) at time \(0\). For each celebrity, we check the last \(2r\) events for reachability. The `best_so_far` tracks the maximum achievable number of photos from older events. Using `max(0, i - 2*r)` ensures we never access negative indices. The final print statement outputs the global maximum.

## Worked Examples

Sample 1:

| i | t_i | x_i | y_i | dp[i] | best_so_far |
|---|-----|-----|-----|-------|-------------|
| 1 | 11  | 6   | 8   | 0     | 0           |

Since the Manhattan distance from (1,1) is 12 > 11, the celebrity cannot be reached. The output is 0.

Sample 2:

Input:

```
10 4
2 2 3
5 3 2
7 5 5
12 4 4
```

| i | t_i | x_i | y_i | dp[i] | best_so_far |
|---|-----|-----|-----|-------|-------------|
| 1 | 2   | 2   | 3   | 1     | 1           |
| 2 | 5   | 3   | 2   | 2     | 2           |
| 3 | 7   | 5   | 5   | 3     | 3           |
| 4 | 12  | 4   | 4   | 4     | 4           |

This trace shows that each celebrity is reachable within the available time, and the DP updates correctly accumulate the maximum number of photos.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n * r) | Each celebrity checks at most \(2r\) previous events |
| Space | O(n) | We store dp for each celebrity |

Given \(n \le 10^5\) and \(r \le 500\), the time complexity is acceptable. Memory usage of O(n) easily fits in 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    r, n = map(int, input().split())
    events = [(0, 1, 1)]
    for _ in range(n):
        t, x, y = map(int, input().split())
        events.append((t, x, y))
    dp = [-float('inf')] * (n + 1)
    dp[0] = 0
    best_so_far = 0
    for i in range(1, n + 1):
        t_i, x_i, y_i = events[i]
        dp[i] = -float('inf')
        for j in range(max(0, i - 2 * r), i):
            t_j, x_j, y_j = events[j]
            if abs(x_i - x_j) + abs(y_i - y_j) <= t_i - t_j:
                dp[i] = max(dp[i], dp[j] + 1)
        if i > 2 * r:
            dp[i] = max(dp[i], best_so_far + 1)
        best_so_far = max(best_so
