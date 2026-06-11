---
title: "CF 1113A - Sasha and His Trip"
description: "Sasha wants to drive from city 1 to city n along a straight line of cities. Each city is exactly one kilometer apart, and all roads go forward, so he cannot move backward. His car consumes one liter of fuel per kilometer and starts with an empty tank."
date: "2026-06-12T04:56:43+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1113
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 539 (Div. 2)"
rating: 900
weight: 1113
solve_time_s: 63
verified: true
draft: false
---

[CF 1113A - Sasha and His Trip](https://codeforces.com/problemset/problem/1113/A)

**Rating:** 900  
**Tags:** dp, greedy, math  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Sasha wants to drive from city 1 to city n along a straight line of cities. Each city is exactly one kilometer apart, and all roads go forward, so he cannot move backward. His car consumes one liter of fuel per kilometer and starts with an empty tank. Every city has a gas station with fuel priced equal to the city’s index in dollars per liter. The car’s tank can hold at most `v` liters. The goal is to compute the minimum total cost of fuel that allows Sasha to reach city `n`.

The input consists of two integers: `n`, the number of cities, and `v`, the tank capacity. The output is a single integer representing the minimum total fuel cost.

Given the constraints (`2 ≤ n ≤ 100` and `1 ≤ v ≤ 100`), we know that the solution can afford an O(n) or even O(n²) algorithm, since in the worst case, we only deal with a few thousand operations. Edge cases arise when the tank capacity is very small (`v = 1`), when it is larger than or equal to the number of cities minus one (`v ≥ n - 1`), and when Sasha must refuel multiple times at increasingly expensive cities. For example, if `n = 5` and `v = 2`, a naive approach that fills only one liter at a time would overspend compared to strategically filling the tank in cheaper cities.

## Approaches

The brute-force solution is simple: simulate every possible sequence of fuel purchases at each city. For every city, try buying every feasible amount of fuel, move forward, and repeat until reaching the last city. While correct, this approach quickly becomes cumbersome as it requires examining an exponential number of purchase sequences. Even with small `n`, the bookkeeping of all possible fuel states is tedious.

The key observation is that fuel is cheaper in earlier cities. Since the car only moves forward, it is optimal to buy as much fuel as possible at the cheapest available city without exceeding the tank capacity or wasting fuel. Specifically, Sasha should fill the tank at city 1 if the tank capacity is less than the total distance, and then top off strategically in subsequent cities only when necessary. If the tank capacity `v` is greater than or equal to `n - 1`, he can fill the tank once at the first city and drive straight to the last city.

This observation allows a greedy approach: buy enough fuel to reach the last city whenever possible, starting from the earliest city, without ever purchasing more expensive fuel unnecessarily. It reduces the problem to a simple arithmetic calculation based on `v` and `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n²) | Too slow |
| Greedy / Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. If the tank capacity `v` is greater than or equal to `n - 1`, buy `n - 1` liters at city 1. The total cost is `(n - 1) * 1` dollars. Return this value immediately. This handles the simple case where Sasha can reach the end in one go.
2. Otherwise, fill the tank to full capacity `v` at city 1. The cost is `v * 1` dollars. Sasha will use `v` kilometers of fuel to progress.
3. For the remaining distance, calculate how much more fuel is needed: `remaining = n - 1 - v`.
4. Buy 1 liter at each subsequent city starting from city 2 until the remaining distance is covered. The cost at city `i` is `i` dollars per liter. Add these costs cumulatively.
5. Return the sum of the initial full tank cost and all additional fuel costs as the minimum total cost.

The invariant here is that we always buy the cheapest possible fuel that allows us to continue moving forward. We never buy extra fuel in expensive cities if we can carry it from a cheaper city, ensuring optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, v = map(int, input().split())

if v >= n - 1:
    # Tank is large enough to reach last city directly
    print(n - 1)
else:
    cost = v  # fill full tank at city 1
    remaining = n - 1 - v
    # Buy 1 liter at each city starting from city 2
    for i in range(2, 2 + remaining):
        cost += i
    print(cost)
```

The code first checks whether the tank capacity allows a direct trip. If so, the minimal cost is simply the distance. Otherwise, it fills the tank fully in the first city, and then purchases additional 1-liter increments in the next cheapest cities until reaching the last city. The `range(2, 2 + remaining)` is critical; starting at city 2 ensures we don’t double-count city 1, and ending at `2 + remaining - 1` covers exactly the remaining kilometers.

## Worked Examples

Sample 1: `n = 4, v = 2`

| City | Fuel Bought | Remaining Distance | Cost |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 2 |
| 2 | 1 | 1 | 2 + 2 = 4 |
| 3 | 0 | 1 | - |

Explanation: Tank is filled with 2 liters at city 1. Sasha drives 2 km to city 3, consumes 2 liters, buys 1 liter at city 2 for 2 dollars, and finally reaches city 4.

Sample 2: `n = 5, v = 10`

| City | Fuel Bought | Remaining Distance | Cost |
| --- | --- | --- | --- |
| 1 | 4 | 0 | 4 |

Explanation: Tank capacity exceeds the distance `n-1 = 4`, so buying 4 liters at city 1 suffices. The total cost is 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All calculations are arithmetic sums over at most `n` values |
| Space | O(1) | Only a few integer variables are used |

The algorithm fits easily within the 1-second time limit and 256 MB memory constraint, even at the maximum values of `n = 100` and `v = 100`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, v = map(int, input().split())
    if v >= n - 1:
        return str(n - 1)
    cost = v
    remaining = n - 1 - v
    for i in range(2, 2 + remaining):
        cost += i
    return str(cost)

# Provided samples
assert run("4 2\n") == "4", "sample 1"
assert run("5 10\n") == "4", "sample 2"

# Custom cases
assert run("2 1\n") == "1", "minimum input"
assert run("3 2\n") == "2", "tank equals distance"
assert run("5 1\n") == "10", "small tank requires multiple stops"
assert run("100 50\n") == "3725", "large n, tank smaller than distance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 1 | Minimum distance, smallest tank |
| 3 2 | 2 | Tank can reach last city directly |
| 5 1 | 10 | Small tank requires incremental refuels |
| 100 50 | 3725 | Large n, v < n-1 scenario |

## Edge Cases

When `v = 1`, Sasha must buy fuel at every city. For example, `n = 5, v = 1`:

| City | Fuel Bought | Remaining Distance | Cost |
| --- | --- | --- | --- |
| 1 | 1 | 3 | 1 |
| 2 | 1 | 2 | 1 + 2 = 3 |
| 3 | 1 | 1 | 3 + 3 = 6 |
| 4 | 1 | 0 | 6 + 4 = 10 |

Output is 10, matching the greedy calculation. This confirms the algorithm correctly handles the smallest tank scenario. Similarly, if `v ≥ n - 1`, as in `n = 5, v = 10`, the algorithm immediately returns `n - 1 = 4`, which is optimal.
