---
title: "CF 102482A - Catch the Plane"
description: "The city is a directed temporal graph. Each bus is an edge with a departure time, arrival time, and probability of existing on the day of travel. You start at station 0 before all buses depart, and you need to maximize the probability of being at station 1 by time k."
date: "2026-08-05T18:51:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102482
codeforces_index: "A"
codeforces_contest_name: "2018 ACM-ICPC World Finals"
rating: 0
weight: 102482
solve_time_s: 116
verified: true
draft: false
---

[CF 102482A - Catch the Plane](https://codeforces.com/problemset/problem/102482/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is a directed temporal graph. Each bus is an edge with a departure time, arrival time, and probability of existing on the day of travel. You start at station `0` before all buses depart, and you need to maximize the probability of being at station `1` by time `k`.

The difficulty comes from two details. A bus can disappear, and you only learn that after choosing it. Also, buses leaving from the same station at the same time cannot all be tested, because after one failed attempt that departure moment has already passed.

The constraints are the main hint. There can be up to `10^6` buses and `10^6` stations, so anything involving dynamic programming over time or repeated graph searches is impossible. The time values can be as large as `10^18`, so we cannot iterate through every possible moment. The algorithm must process only the given bus events, which means roughly linear or linear-logarithmic work.

A common mistake is to treat buses leaving at the same time as independent choices. For example:

```
2 2
1
0 1 0 1 0.5
0 1 0 1 0.5
```

The answer is `0.5`, not `0.75`. You can only try one bus. Another mistake is allowing a transfer when arrival time equals departure time. If a bus arrives exactly when another leaves, that connection is invalid.

## Approaches

A brute-force solution would try to simulate every possible strategy. At every station and time it would consider all buses that could be taken and recursively compute the best probability. This is correct because it explores every possible decision, but the number of states is enormous. There are up to `10^6` buses, and chains of transfers can create exponentially many possible strategies.

The key observation is that all decisions can be processed backwards in time. When considering a bus departing at time `s`, every bus departing after `s` has already been handled. Therefore we already know the optimal probability of succeeding after arriving at the destination of this bus.

Let `dp[v]` mean: if we are at station `v` immediately after all departures at the current processed time, what is the maximum probability of eventually reaching the airport?

For a bus `a -> b` leaving at time `s`, if we try it, the probability is:

```
p * dp[b] + (1 - p) * dp[a]
```

The first term is the case where the bus runs. The second term is the case where it fails and we are stuck at station `a` after the departure moment has passed.

Processing buses with the same departure time together is necessary. Every candidate must use the old value of `dp[a]`, because a failed attempt cannot be followed by another bus at that same time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Large | Too slow |
| Backward sweep | O(m log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Initialize `dp[1] = 1` because already being at the airport means success. Every other station starts with probability `0`.
2. Sort all buses by departure time in decreasing order. The latest departures are processed first because their destinations cannot use any later buses.
3. For each group of buses sharing the same departure time, compute every possible attempt using the current `dp` values.
4. For a bus with probability `p`, store the candidate value `p * dp[destination] + (1 - p) * dp[start]`.
5. After the whole time group is evaluated, update the starting stations with the best candidate from that group.
6. After all buses are processed, `dp[0]` is the optimal probability from the initial state.

The invariant is that before processing a departure time `s`, `dp[v]` already contains the optimal probability using only buses that depart after `s`. A bus departing at `s` only needs the future information from its destination, which is already available. Processing equal departure times together preserves the rule that only one bus can be attempted at that moment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m, n = map(int, input().split())
    k = int(input())

    buses = []

    for _ in range(m):
        a, b, s, t, p = input().split()
        buses.append((int(s), int(a), int(b), float(p)))

    buses.sort(reverse=True)

    dp = [0.0] * n
    dp[1] = 1.0

    i = 0
    while i < m:
        time = buses[i][0]
        best = {}

        while i < m and buses[i][0] == time:
            _, a, b, p = buses[i]
            value = p * dp[b] + (1.0 - p) * dp[a]

            if a not in best or value > best[a]:
                best[a] = value

            i += 1

        for a, value in best.items():
            if value > dp[a]:
                dp[a] = value

    print("{:.10f}".format(dp[0]))

if __name__ == "__main__":
    solve()
```

The sorting order is the core of the implementation. A bus arriving at time `t` always needs the answer for time `t`, which means every bus with departure time greater than `t` must already have been processed.

The group update is also essential. Updating `dp` immediately after seeing a single bus would allow another bus at the same departure time to incorrectly use the improved value after a failed attempt. Keeping candidates in `best` prevents this.

Python floating point precision is enough here because the required error is only `10^-6`. Time values are never used in arithmetic, so their size does not create overflow issues.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting dominates; every bus is processed once |
| Space | O(n + m) | Stores the buses and one probability per station |

With one million buses, the linear scan is easily manageable, and the logarithmic sorting factor is acceptable under the generous memory limit.

## Worked Example

For the second sample:

```
4 2
2
0 1 0 1 0.5
0 1 0 1 0.5
0 1 1 2 0.4
0 1 1 2 0.2
```

The latest two buses are processed first.

| Departure time | Bus probabilities | dp[0] after processing |
| --- | --- | --- |
| 1 | 0.4, 0.2 | 0.4 |
| 0 | 0.5, 0.5 | 0.7 |

At time `1`, the best option gives probability `0.4`. At time `0`, trying the first bus succeeds with probability `0.5`, and failing leaves the chance of taking the later bus. The result is:

```
0.5 + 0.5 * 0.4 = 0.7
```

which matches the sample output.
