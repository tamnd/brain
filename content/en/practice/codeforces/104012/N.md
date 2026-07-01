---
title: "CF 104012N - New Time"
description: "We are given two moments in a day written on a 24-hour digital clock. The first is the current displayed time, and the second is the target correct time."
date: "2026-07-02T05:10:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104012
codeforces_index: "N"
codeforces_contest_name: "2022-2023 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104012
solve_time_s: 42
verified: true
draft: false
---

[CF 104012N - New Time](https://codeforces.com/problemset/problem/104012/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two moments in a day written on a 24-hour digital clock. The first is the current displayed time, and the second is the target correct time. The clock can only be changed forward using two operations: one button increases the time by exactly one minute, and the other increases the time by exactly one hour. Both operations wrap around the 24-hour day, so moving forward past 23:59 returns to 00:00.

The task is to determine the minimum number of button presses required to transform the displayed time into the target time.

A useful way to think about the state space is that the clock has 24 × 60 = 1440 distinct states, and both operations move forward along this circular structure. Each minute press advances by 1 state, each hour press advances by 60 states modulo 1440.

The constraints are small enough that any approach that runs in constant time per test case is sufficient. Even a brute-force shortest path search over all 1440 states would be trivial, but the structure allows an even simpler closed-form solution.

A subtle edge case arises from wrap-around behavior. For example, converting 23:59 to 00:00 is a single minute press, not a large backward adjustment. Another corner case is when the target time is earlier in the day than the current time in normal ordering, since forward movement must cross midnight.

## Approaches

A naive approach is to model this as a shortest path problem on a circular graph of 1440 nodes, where each node corresponds to a time of day. From each node, there are two outgoing edges: one to the next minute and one to the next hour. We could run a BFS from the starting time until we reach the target time. This is correct because every operation has equal cost, and BFS guarantees the shortest path in an unweighted graph.

However, BFS is unnecessary here because the graph structure is extremely regular. Any sequence of operations corresponds to choosing a total number of hour steps and minute steps whose combined effect is a forward displacement modulo 1440. If we denote the difference in minutes between the two times as D, then the problem reduces to expressing D as a combination of 60-minute and 1-minute forward moves with minimum number of operations.

The key observation is that hour moves are always more efficient than 60 minute moves, since one hour press replaces 60 minute presses with a single operation. Therefore, for a fixed forward distance D, the optimal strategy is to use as many hour moves as possible, followed by minute moves for the remainder.

So the problem reduces to computing the forward distance in minutes modulo 1440, then minimizing:

floor(D / 60) + (D mod 60).

This eliminates any need for search or dynamic programming.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| BFS over 1440 states | O(1440) | O(1440) | Accepted but unnecessary |
| Arithmetic decomposition | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert both input times into total minutes from 00:00. This gives a single integer representation for each time, removing the need to handle hours and minutes separately. The transformation is `hh * 60 + mm`.
2. Compute the forward difference `D` from current time to target time on a circular 1440-minute clock. If the target time is behind the current time, we wrap around by adding 1440 before subtracting. This ensures we always measure forward movement only.
3. Once D is known, compute how many full hour jumps fit into it using integer division `D // 60`. Each such jump corresponds to one press of button B.
4. Compute the remaining minutes after using hour jumps using `D % 60`. Each remaining minute requires one press of button A.
5. Add these two counts to get the total number of button presses.
6. Output the result.

The reason this works is that both operations only move forward, so any valid sequence of operations corresponds exactly to a decomposition of D into 60-minute chunks and 1-minute chunks. There is no interaction effect between operations, so greedy maximization of hour steps cannot worsen the solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse(t):
    h = int(t[:2])
    m = int(t[3:])
    return h * 60 + m

cur = parse(input().strip())
tar = parse(input().strip())

diff = (tar - cur) % (24 * 60)

ans = diff // 60 + diff % 60

print(ans)
```

The solution begins by parsing the HH:MM format into minutes. This avoids floating logic and keeps everything integer-based. The modulo operation ensures wrap-around behavior on the 24-hour cycle, handling cases where the target is earlier than the current time.

The decomposition step is straightforward: integer division extracts how many full hour presses are useful, and the remainder accounts for leftover minutes. No ordering issues arise because both operations are strictly additive in forward time.

## Worked Examples

### Example 1: 11:57 → 12:00

We convert times into minutes:

| Step | Current | Target | Difference |
| --- | --- | --- | --- |
| Convert | 717 | 720 | - |
| Raw diff | - | - | 3 |
| Mod 1440 | - | - | 3 |

Now we decompose 3 minutes:

| Hours used | Minutes remaining | Total presses |
| --- | --- | --- |
| 0 | 3 | 3 |

This matches pressing the minute button three times.

The trace shows that when the distance is less than 60, no hour moves are used.

### Example 2: 19:44 → 08:50

Convert to minutes:

19:44 = 1184

08:50 = 530

We compute forward difference:

| Step | Value |
| --- | --- |
| Cur | 1184 |
| Tar | 530 |
| Diff (wrapped) | 530 - 1184 + 1440 = 786 |

Now decompose 786:

| Hours used | Minutes remaining | Total presses |
| --- | --- | --- |
| 13 | 6 | 19 |

So the answer is 13 + 6 = 19.

This demonstrates the wrap-around case where the correct path crosses midnight, and the modulo step ensures correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations per test case |
| Space | O(1) | Only integer variables are used |

The problem constraints allow up to very large inputs in principle, but the solution is constant time per case, so it comfortably fits within limits even for many test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def parse(t):
        h = int(t[:2])
        m = int(t[3:])
        return h * 60 + m

    cur = parse(sys.stdin.readline().strip())
    tar = parse(sys.stdin.readline().strip())

    diff = (tar - cur) % (24 * 60)
    return str(diff // 60 + diff % 60)

# provided samples
assert run("11:57\n12:00\n") == "3"
assert run("09:09\n21:21\n") == str(( (21*60+21) - (9*60+9) ) % 1440 // 60 + ( (21*60+21) - (9*60+9) ) % 1440 % 60)

# custom cases
assert run("00:00\n00:00\n") == "0"
assert run("23:59\n00:00\n") == "1"
assert run("01:00\n02:00\n") == "1"
assert run("10:10\n09:09\n") == str(( (9*60+9)-(10*60+10) ) % 1440 // 60 + ( (9*60+9)-(10*60+10) ) % 1440 % 60)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 00:00 → 00:00 | 0 | zero movement case |
| 23:59 → 00:00 | 1 | midnight wrap minute |
| 01:00 → 02:00 | 1 | pure hour move optimality |
| 10:10 → 09:09 | computed | reverse wrap correctness |

## Edge Cases

A key edge case is when the times are identical. In this case, the difference is zero, and both hour and minute contributions are zero, so the output is correctly 0. The modulo computation naturally preserves this without special casing.

Another case is crossing midnight. For example, 23:59 to 00:00 becomes a difference of 1 minute after applying modulo 1440. The algorithm handles this because the subtraction would be negative, and the modulo correction shifts it into the correct forward distance.

A final case is when the target is exactly one hour ahead but not aligned on the hour boundary, such as 10:10 to 11:09. The difference is 59 minutes, so no hour press is used, and the solution correctly prefers 59 minute presses over an hour press that would overshoot.
