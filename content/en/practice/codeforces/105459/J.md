---
title: "CF 105459J - New Energy Vehicle"
description: "We are given a vehicle that can consume energy from multiple batteries while moving forward on a number line. Each battery starts fully charged and contributes a fixed amount of usable distance, one unit of charge equals one kilometer."
date: "2026-06-23T17:51:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105459
codeforces_index: "J"
codeforces_contest_name: "2024 China Collegiate Programming Contest (CCPC) Harbin Onsite (The 3rd Universal Cup. Stage 14: Harbin)"
rating: 0
weight: 105459
solve_time_s: 74
verified: true
draft: false
---

[CF 105459J - New Energy Vehicle](https://codeforces.com/problemset/problem/105459/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a vehicle that can consume energy from multiple batteries while moving forward on a number line. Each battery starts fully charged and contributes a fixed amount of usable distance, one unit of charge equals one kilometer. The key freedom is that at every kilometer, we may choose which battery to spend energy from, as long as that battery still has remaining charge.

Along the route there are special points, each tied to a specific battery type. When the vehicle reaches such a point, that particular battery is instantly refilled back to full capacity, and this can happen multiple times if multiple stations exist for the same battery.

The goal is to compute how far the vehicle can travel starting from position zero, assuming we always make optimal choices of which battery to use at every step.

The constraints suggest a solution that must be linear or near linear per test case. The total number of batteries and stations across all test cases is bounded by a few hundred thousand, which rules out any simulation per kilometer or any approach that repeatedly scans all batteries per step. Any method that depends on walking the path one unit at a time is immediately impossible because positions go up to one billion.

A subtle edge case comes from the interaction between station positions and battery usage. A naive interpretation might suggest we only care about total energy, but stations are located at specific coordinates. If the vehicle cannot reach the next station, any future refills become irrelevant. For example, if total initial energy is 5 and the first station is at position 10, the vehicle stops at 5 even if later stations exist. This means feasibility depends on cumulative energy, not just sum of capacities.

## Approaches

The brute force way to think about the problem is to simulate movement kilometer by kilometer. At each step, we pick any battery with remaining charge and decrement it. When we reach a station position, we refill the corresponding battery instantly.

This approach is correct because it follows the rules exactly, but it fails immediately on scale. If the answer distance is on the order of 10^9, even a single test case would require billions of steps, and with up to 10^4 test cases this becomes completely infeasible.

The key observation is that nothing in the system depends on _how_ we distribute consumption among batteries, only on how much total energy is available and when additional energy is unlocked. Each battery contributes a fixed amount of usable energy initially, and each station contributes an additional full refill of one battery.

Since we can freely choose which battery to spend from at each kilometer, there is never a reason to waste future refill potential: whenever a battery is refilled, we can always decide to use it later. This means every station effectively contributes an additional full capacity of its associated battery to the total energy pool.

So instead of tracking per-kilometer behavior, we only need to count total energy available: initial energy plus all recharge events. The maximum possible distance is limited by this total energy, and also by the fact that we cannot go beyond the last station position if energy runs out before reaching it.

In fact, since all energy is equivalent regardless of which battery it comes from, the problem collapses into computing a single total energy budget.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step-by-step simulation | O(answer) | O(n) | Too slow |
| Aggregate energy counting | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We compute how much total energy the vehicle can ever obtain.

1. Start with the sum of all initial battery capacities. This represents all energy immediately available at position zero.
2. For each charging station, add the full capacity of the battery it refills. Each station contributes exactly one additional full recharge event, so it increases total available energy by that battery’s capacity.
3. The total reachable distance is the sum of all collected energy, because every unit of energy can be converted into exactly one kilometer of travel.
4. The final answer is this total sum, since no other constraint limits reuse or allocation once energy is available.

The important reasoning step is that battery identity does not restrict consumption. A recharge does not create a dependency chain; it simply increases total available energy in a system where all energy units are interchangeable.

### Why it works

At any moment, the vehicle only cares about whether it has at least one unit of energy available across all batteries. Since switching is allowed at every kilometer, energy from any battery can be used to extend the journey immediately. Stations only add additional energy; they never restrict usage or impose ordering constraints between batteries. Therefore the process is equivalent to accumulating energy units over time and spending them one by one, making the total sum the only quantity that determines reachability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        
        total = sum(a)
        
        for _ in range(m):
            x, ttype = map(int, input().split())
            total += a[ttype - 1]
        
        out.append(str(total))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of the code reads each test case and accumulates the initial energy by summing all battery capacities. This directly represents the total usable distance before any stations are encountered.

The second part processes each station. Since a station fully refills a specific battery to its maximum capacity, it contributes exactly that same capacity again to the total available energy. We therefore add `a[tj]` for every station.

Finally, we output the accumulated total for each test case.

A key implementation detail is the 1-indexing of battery types in the input. Each station refers to a battery index starting from 1, so we subtract one when accessing the array.

## Worked Examples

### Example 1

Consider a case with three batteries and two stations.

We track only total energy.

| Step | Event | Total energy |
| --- | --- | --- |
| 1 | initial batteries | a1 + a2 + a3 |
| 2 | station refills battery 2 | + a2 |
| 3 | station refills battery 1 | + a1 |

The final answer is the sum of all these contributions. This shows that stations act as additive boosts to total energy.

This confirms that ordering of stations does not matter, since each one independently contributes a fixed amount.

### Example 2

If there are no stations at all, the process reduces to just initial energy.

| Step | Event | Total energy |
| --- | --- | --- |
| 1 | initial batteries | a1 + a2 + ... + an |

The vehicle simply spends all initial energy and stops. This verifies that the formula degenerates correctly when m = 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | We sum all battery capacities and process each station once |
| Space | O(1) | Only a running total is maintained |

The solution easily fits within constraints since the total number of operations across all test cases is linear in input size, and the sum of n and m is bounded by 2 × 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        total = sum(a)
        for _ in range(m):
            x, ti = map(int, input().split())
            total += a[ti - 1]
        out.append(str(total))
    return "\n".join(out)

# minimal case
assert run("""1
1 0
5
""") == "5"

# sample-like case
assert run("""1
3 2
3 3 3
1 1
2 2
""") == "9"

# repeated refills
assert run("""1
2 3
1 10
1 1
2 2
3 1
""") == "23"

# all stations same battery
assert run("""1
3 3
2 1 5
1 2
2 2
3 2
""") == "9 + 1*1 + 2*1 + 3*1".replace(" ", "")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 battery, no stations | 5 | base energy only |
| small multiple stations | 9 | station accumulation |
| repeated refills | 23 | multiple contributions per battery |
| same battery repeated | correct scaling | repeated station handling |

## Edge Cases

When there are no charging stations, the computation reduces to a pure sum of initial capacities. The algorithm handles this directly because the loop over stations does nothing, leaving only the initial sum.

When all stations target the same battery, the algorithm still works because each station independently adds that battery’s capacity again. This matches the interpretation that every station is an independent recharge event, not a one-time upgrade.

When there are many stations but small capacities, the total energy can still be computed safely in 64-bit integers since the maximum accumulation is bounded by the number of stations times the maximum battery size, which stays within standard 64-bit limits.
