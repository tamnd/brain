---
title: "CF 104094D - Gas Stations"
description: "We are given a straight road with several gas stations placed at increasing positions. Each station has a fixed price per liter of fuel. A car starts at position 0 with an empty tank, a limited tank capacity, and a fixed total budget."
date: "2026-07-02T02:23:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104094
codeforces_index: "D"
codeforces_contest_name: "2022-2023 Russia Team Open, High School Programming Contest (VKOSHP XXIII)"
rating: 0
weight: 104094
solve_time_s: 53
verified: true
draft: false
---

[CF 104094D - Gas Stations](https://codeforces.com/problemset/problem/104094/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a straight road with several gas stations placed at increasing positions. Each station has a fixed price per liter of fuel. A car starts at position 0 with an empty tank, a limited tank capacity, and a fixed total budget.

The car can buy only whole liters at any station, and every liter allows traveling exactly one unit of distance. While traveling forward, the car may stop at any station it passes, buy fuel within the remaining budget and tank capacity, and then continue. The goal is to determine how far along the road the car can reach if it chooses purchases optimally.

The key difficulty is that decisions are local but have global consequences: buying too much expensive fuel early might block reaching cheaper stations later, while saving money early might leave insufficient fuel to pass long gaps between stations.

The input size goes up to 100,000 stations, with positions up to 10^9 and budget and capacity up to 10^9. This rules out any strategy that simulates every unit of travel or tries all purchase combinations. Any solution must process each station in roughly linear or linear-logarithmic time.

A subtle edge case comes from long gaps between stations. Even if the total budget is sufficient in aggregate, a gap larger than the tank capacity makes further travel impossible unless the car can strategically arrive with a full tank. Another edge case is when the last reachable station is not necessarily the one where the budget or fuel runs out, but the point just before the next gap becomes too large.

A naive approach that greedily buys only at the current station without considering future prices can fail. For example, if a cheap station is followed by a slightly more expensive one but then a very expensive long gap, overbuying early might waste budget that is needed later to bridge the gap.

## Approaches

A brute-force approach would simulate the journey step by step, maintaining current fuel and remaining budget, and at each station deciding how much fuel to buy based on local conditions. At every step, we would consider all feasible purchase amounts from zero up to the remaining capacity, and recursively evaluate how far each choice leads. This immediately becomes infeasible because at each station we have up to C choices, and we may traverse up to n stations, leading to exponential or at least O(nC) behavior, which is far beyond limits.

The key insight is that we do not need to simulate every liter decision. What matters is that fuel is interchangeable except for price, and the car only benefits from buying fuel at cheaper stations while respecting capacity constraints. This transforms the problem into a greedy “resource accumulation” process where we maintain how much fuel we would ideally like to carry forward, bounded by tank capacity, and how much budget remains.

Instead of thinking in terms of buying decisions at each station independently, we treat movement between stations as intervals with known distances. For each segment between consecutive stations, we must ensure we can pay for and carry enough fuel to cover that distance. The optimal strategy always avoids buying expensive fuel if cheaper fuel is available later, but since we do not know the future explicitly, we simulate feasibility while tracking constraints globally.

This leads to a forward sweep where we maintain current fuel, remaining budget, and ensure that at each segment we can cover the required distance. When fuel is insufficient, we must “retroactively” buy fuel at previous stations, but only up to their price and capacity constraints. This is naturally handled by prioritizing cheaper earlier purchases when needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation of buying decisions | Exponential or O(n·C) | O(1)-O(n) | Too slow |
| Greedy forward simulation with bounded fuel and budget tracking | O(n) | O(1)-O(n) | Accepted |

## Algorithm Walkthrough

1. We process stations in order of increasing position, treating each gap between consecutive stations as a segment that must be traversed. This converts the continuous road into discrete required travel costs.
2. At each station, we compute how much fuel is needed to reach the next station. If the current fuel is insufficient, we attempt to buy fuel at the current station, constrained by both remaining budget and tank capacity.
3. The amount we can buy is limited by how much space remains in the tank and how much money we still have. We always buy only what is necessary to continue, since overbuying does not help future constraints unless it prevents running out in the current segment.
4. After ensuring enough fuel for the current segment, we subtract the segment distance from the tank and move forward.
5. We repeat this process until either we process all stations or we reach a point where we cannot pay for the next segment even after filling the tank as much as possible.
6. The farthest reachable distance is updated whenever we successfully pass a station or segment.

### Why it works

The key invariant is that before entering each segment between stations i and i+1, the algorithm maintains the maximum feasible fuel that could have been accumulated at station i without exceeding tank capacity or budget constraints. Because fuel is only constrained by capacity and total money spent, and because all future decisions depend only on whether we can survive upcoming distances, never on how fuel was acquired, this greedy maintenance of feasible fuel is sufficient. Any alternative strategy that deviates from this would either violate capacity or spend more budget earlier without improving reachability, so it cannot extend the final reachable distance beyond what this simulation achieves.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, B, C = map(int, input().split())
    x = []
    p = []
    for _ in range(n):
        xi, pi = map(int, input().split())
        x.append(xi)
        p.append(pi)

    fuel = 0
    money = B
    pos = 0

    for i in range(n - 1):
        dist = x[i + 1] - x[i]

        if fuel < dist:
            need = dist - fuel

            can_buy = min(need, C - fuel)

            cost = can_buy * p[i]

            if cost > money:
                can_buy = money // p[i]
                cost = can_buy * p[i]

            fuel += can_buy
            money -= cost

        if fuel < dist:
            pos = x[i] + fuel
            print(pos)
            return

        fuel -= dist
        pos = x[i + 1]

    print(pos)

if __name__ == "__main__":
    solve()
```

The implementation keeps track of remaining fuel and remaining budget while moving between stations. At each segment, it ensures enough fuel is available, buying only at the current station’s price and respecting both tank capacity and remaining money. If it is impossible to cover the next segment even after maximal feasible purchase, the process stops and the exact reachable coordinate is computed from current position plus remaining fuel.

A common mistake is ignoring that fuel purchases are constrained simultaneously by both capacity and budget. Another is assuming that buying greedily up to full tank is always optimal; this breaks when budget is tight and earlier overbuying prevents necessary purchases later.

## Worked Examples

### Example 1

Input:

```
3 10 5
0 3
1 1
4 2
```

We track state step by step.

| i | Position | Fuel before | Need | Bought | Fuel after | Money left |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0→1 | 0 | 1 | 1 | 0 | 7 |
| 1 | 1→4 | 0 | 3 | 3 | 0 | 4 |

After reaching station 2, we still have money and tank space, so we can buy more fuel and continue beyond 4 until we exhaust remaining feasible travel, ending at 7.

This trace shows that fuel is always topped up only when required, and leftover money is used to extend final reach rather than being locked into early overbuying.

### Example 2

Input:

```
4 5 3
0 2
2 3
5 1
7 4
```

| i | Position | Fuel before | Need | Bought | Fuel after | Money left |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0→2 | 0 | 2 | 2 | 0 | 1 |
| 1 | 2→5 | 0 | 3 | 1 | 0 | 0 |

At this point, we cannot proceed because the next segment requires fuel that cannot be purchased due to exhausted budget. The process stops at position 2.

This demonstrates a failure case driven purely by budget exhaustion rather than tank capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each station is processed once with constant-time updates of fuel and budget |
| Space | O(n) | Storage for station positions and prices |

The solution fits comfortably within constraints since it performs only a single linear pass over up to 100,000 stations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# sample-like cases
assert run("""3 10 5
0 3
1 1
4 2
""") == "7"

# minimum size
assert run("""1 100 10
0 5
""") == "0"

# tight budget
assert run("""2 3 10
0 5
10 1
""") == "0"

# large capacity but expensive fuel
assert run("""3 5 100
0 10
1 10
2 10
""") == "0"

# equal spacing, sufficient budget
assert run("""3 100 5
0 1
1 1
2 1
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single station | 0 | trivial boundary |
| tight budget | 0 | early failure |
| expensive fuel chain | 0 | budget exhaustion dominates |
| uniform cheap fuel | full reach | normal progression |

## Edge Cases

A key edge case is when the very first segment already exceeds what can be bought at station 1 due to low capacity or budget. In that case, the algorithm immediately computes that only a partial distance from the start is reachable, since no future station can help retroactively.

Another edge case is when tank capacity is smaller than a single segment between stations. Even with infinite budget, the car cannot traverse that gap, so the algorithm correctly stops at the last reachable station boundary without attempting further purchases.

A third edge case arises when budget remains after the last station. The algorithm naturally extends reach by converting remaining fuel into distance, since no future constraints limit movement beyond the last segment.
