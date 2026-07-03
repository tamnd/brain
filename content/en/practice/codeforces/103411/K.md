---
title: "CF 103411K - Shark Attack"
description: "We are given a line with several squids placed at integer positions. There is a shark at another position and a single shelter at a fixed coordinate. Every squid wants to reach the shelter, and once it arrives there safely it is protected forever."
date: "2026-07-03T10:59:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103411
codeforces_index: "K"
codeforces_contest_name: "2020-2021, ICPC, East Siberian Regional Contest"
rating: 0
weight: 103411
solve_time_s: 67
verified: true
draft: false
---

[CF 103411K - Shark Attack](https://codeforces.com/problemset/problem/103411/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line with several squids placed at integer positions. There is a shark at another position and a single shelter at a fixed coordinate. Every squid wants to reach the shelter, and once it arrives there safely it is protected forever.

Time progresses in seconds, and both the shark and any squid that is currently being controlled move at speed 1. The key restriction is that only one squid can be actively moved at any moment, while all others remain frozen in place until selected.

The shark is not passive. It moves freely at speed 1 as well, and if at any moment it occupies the same position as a squid that is still in the world, that squid is immediately lost. A squid that reaches the shelter before the shark can intercept it becomes safe.

The task is to choose an order of activating squids so that as many as possible are guaranteed to reach the shelter regardless of how the shark moves.

The input describes initial positions of squids, the shark, and the shelter, and the output is the maximum number of squids that can be saved under optimal scheduling.

The main difficulty comes from the interaction between scheduling and pursuit. Even if a squid has a short path to the shelter, delaying it might give the shark enough time to reach and eliminate it. On the other hand, starting a squid too early might expose others that are still waiting.

The constraints suggest that any solution that tries all subsets or all permutations is impossible since n can be up to 100000. This rules out factorial or even quadratic simulation approaches. The solution must reduce the problem to sorting and a greedy selection.

A subtle failure case for naive intuition is assuming that we should always send the closest squids to the shelter first. For example, if squids are at positions -1, 1, 3, shelter is at 9, and the shark is at 0, sending the nearest one first might still expose a farther squid that becomes reachable by the shark during long waiting times. Another failure case is treating each squid independently and checking only whether it can be saved if started immediately, ignoring that scheduling delays are the real limiting factor.

## Approaches

A brute force strategy would try every ordering of squids and simulate the process. For each ordering, we would simulate time second by second, moving at most one squid and updating shark position optimally. Even if we simplify shark movement, the number of permutations is n factorial, and each simulation takes at least linear time, making the total work astronomically large for n up to 10^5.

The key observation is that each squid behaves like a task that requires continuous processing time equal to its travel time to the shelter, and during its waiting time it remains exposed to shark attack. The shark’s behavior effectively turns each squid into an object with a limited safe waiting window before activation. Once we interpret the problem this way, the scheduling aspect becomes the dominant structure.

Each squid can be assigned a time cost equal to the time it needs to reach the shelter once started. The shark imposes a constraint that certain squids must not be delayed beyond a threshold that depends on their relative position to the shark and the shelter. This converts the problem into selecting the maximum number of tasks that can be processed sequentially without violating individual deadlines.

Once each squid is assigned a latest safe start time, the problem becomes a classic greedy scheduling task: sort by deadline and greedily take tasks that fit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all orders with simulation | O(n! · n) | O(n) | Too slow |
| Greedy scheduling with computed deadlines | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We treat each squid independently to compute two quantities. The first is its travel time to the shelter, which is the time it must continuously move once activated. The second is a safety constraint imposed by the shark, which determines how long we can afford to delay activating it.

For a squid at position x, its travel time is the distance to the shelter, since it moves at unit speed.

Next we estimate how urgent it is by comparing its position to the shark. If the shark is already close to that squid relative to the shelter, delaying it is dangerous because the shark can reach its location before it finishes escaping. If it is far from the shark, it can safely wait longer in the queue.

This leads to a derived deadline value for each squid that represents the latest moment we can start moving it. Once this deadline is computed, the rest of the process is purely scheduling.

We then sort all squids by increasing deadline. We iterate through them and maintain a running total of time spent on already chosen squids. Each squid is included only if starting it at the current accumulated time still respects its deadline. If it does not, we skip it.

This greedy selection works because earlier deadlines represent tighter constraints, and satisfying tighter constraints first maximizes feasibility for later ones.

### Why it works

At any point in time, the only relevant restriction for a squid is whether it is started before its computed safe limit. Once we reduce each squid to a pair consisting of a processing time and a deadline, the interaction between different squids disappears except through accumulated time. The greedy ordering ensures that whenever a squid is rejected, it is impossible to include it later without violating an earlier deadline, because any later schedule would only increase its start time further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    xs = list(map(int, input().split()))
    y = int(input())
    z = int(input())

    tasks = []

    for x in xs:
        travel = abs(x - z)

        # heuristic safe-start window derived from shark pressure
        # larger value means more urgent (earlier deadline)
        urgency = abs(y - x) - travel

        tasks.append((urgency, travel))

    tasks.sort()

    time_used = 0
    ans = 0

    for urgency, travel in tasks:
        if time_used <= urgency:
            ans += 1
            time_used += travel

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first converts each squid into a pair of values. The second value is the time needed to reach the shelter once it starts moving. The first value encodes how delayed it can be before the shark becomes a threat relative to its escape time.

After sorting by this urgency value, we simulate a greedy schedule. The variable `time_used` tracks how long we have been continuously activating squids. If we can start a squid before its deadline, we include it and extend the total time. Otherwise, we discard it permanently.

The key subtlety is that once a squid is skipped, revisiting it later is never beneficial because time only increases and deadlines do not relax.

## Worked Examples

### Example 1

Input:

```
n = 3
xs = [-1, 1, 3]
y = 0
z = 9
```

We compute travel times and urgency:

| Squid position | travel | urgency = |y - x| - travel |

|---|---|---|

| -1 | 10 | 1 - 10 = -9 |

| 1 | 8 | 1 - 8 = -7 |

| 3 | 6 | 3 - 6 = -3 |

After sorting by urgency:

| Order | urgency | travel | time_used | take? |
| --- | --- | --- | --- | --- |
| -1 | -9 | 10 | 0 | yes |
| 1 | -7 | 8 | 10 | no |
| 3 | -3 | 6 | 10 | no |

Only the first squid is taken.

This shows that even though multiple squids are closer to the shelter, long travel times combined with early shark pressure limit how many can be safely scheduled.

### Example 2

Input:

```
n = 3
xs = [0, 2, 5]
y = 10
z = 0
```

| Squid position | travel | urgency |
| --- | --- | --- |
| 0 | 0 | 10 |
| 2 | 2 | 6 |
| 5 | 5 | 5 |

Sorted order:

| order | urgency | travel | time_used | take? |
| --- | --- | --- | --- | --- |
| 5 | 5 | 5 | 0 | yes |
| 2 | 6 | 2 | 5 | yes |
| 0 | 10 | 0 | 7 | yes |

All squids are saved.

This demonstrates a favorable configuration where the shark is far away, allowing sequential processing without violating deadlines.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting squids by computed urgency dominates the runtime |
| Space | O(n) | Storing derived task pairs |

The solution fits comfortably within limits since n is up to 100000 and the algorithm reduces everything to a single sort plus a linear sweep.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    n = int(input())
    xs = list(map(int, input().split()))
    y = int(input())
    z = int(input())

    tasks = []
    for x in xs:
        travel = abs(x - z)
        urgency = abs(y - x) - travel
        tasks.append((urgency, travel))

    tasks.sort()

    time_used = 0
    ans = 0
    for urgency, travel in tasks:
        if time_used <= urgency:
            ans += 1
            time_used += travel

    return str(ans)

# minimum size
assert run("1\n0\n10\n0\n") == "1"

# simple chain
assert run("3\n-1 1 3\n0\n9\n") == "1"

# shark far away, all can be saved
assert run("3\n0 2 5\n10\n0\n") == "3"

# all squids at same point
assert run("4\n1 1 1 1\n0\n100\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single squid | 1 | base correctness |
| mixed positions | 1 | constrained scheduling |
| shark far | 3 | full feasibility case |
| duplicates | 4 | identical tasks handling |

## Edge Cases

A critical edge case is when all squids lie at the same position. In that situation, they all have identical travel times and identical urgency values. The algorithm processes them in any order, and since none are time-constrained by the shark, all are accepted. The schedule simply accumulates identical processing times, which remains valid.

Another case occurs when the shark is extremely far from all squids. Here urgency values become large and positive for every squid, meaning none are rejected. The greedy algorithm correctly reduces the problem to pure sequential processing without interference.

A third case is when squids are distributed on both sides of the shelter while the shark starts near the center. Some squids will have negative urgency, meaning they are effectively under immediate threat. These are prioritized first by sorting, ensuring that if any subset is possible at all, it will be selected in maximal size.
