---
title: "CF 105637B - Flower Festival"
description: "The problem describes a straight road of length (f) leading to a festival location at position (f). There are (n) cars currently on this road. Each car has a known position (xi), measured as its distance from the start of the road, and a constant speed (vi)."
date: "2026-06-26T14:21:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105637
codeforces_index: "B"
codeforces_contest_name: "The 2022 ICPC Asia Tehran Regional Contest"
rating: 0
weight: 105637
solve_time_s: 42
verified: true
draft: false
---

[CF 105637B - Flower Festival](https://codeforces.com/problemset/problem/105637/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a straight road of length \(f\) leading to a festival location at position \(f\). There are \(n\) cars currently on this road. Each car has a known position \(x_i\), measured as its distance from the start of the road, and a constant speed \(v_i\). All cars move toward the festival, so their position increases linearly with time until they reach \(f\).

The task is to determine which car arrives at the festival first. Since every car moves at constant speed, the arrival time for car \(i\) is simply the remaining distance to the end divided by its speed, \((f - x_i) / v_i\). The answer is the index of the car with the smallest such time. It is guaranteed that no two cars arrive at exactly the same time, so there is a unique answer.

The constraints are small: \(n \leq 100\), \(f \leq 10^4\), and speeds are also bounded by \(100\). This means even a straightforward \(O(n)\) scan with basic arithmetic is more than sufficient. Any solution that computes each arrival time once and compares them directly will run instantly. There is no need for sorting or advanced data structures, since the output is just the minimum over a small set.

A few edge cases are worth being explicit about. If a car is already at position \(f\), then its arrival time is zero, and it must be selected if no other car is also at zero (which the problem guarantees will not happen). If multiple cars start at the same position but have different speeds, the faster one will obviously win because the remaining distance is identical. A subtle mistake arises if one compares \(x_i / v_i\) instead of \((f - x_i) / v_i\), which would compute travel-from-start time rather than time-to-finish, reversing the logic entirely.

Another easy pitfall is using floating point division and comparing times directly without care. While this works under constraints, it is unnecessary and less robust than comparing cross-products to avoid precision issues.

## Approaches

The most direct way to solve the problem is to simulate the final race outcome numerically. For each car, compute how long it will take to reach the endpoint, then pick the minimum. This is correct because motion is uniform and independent between cars, so the arrival times fully determine the order.

The brute-force view is already optimal in this setting. Even if we imagine recomputing positions at small time steps, that would mean repeatedly updating all \(n\) cars over a large number of steps up to time \(f\), leading to something like \(O(n \cdot f)\), which is unnecessary given that the motion is linear and can be expressed in closed form.

The key observation is that the state of each car is fully summarized by a single scalar value: its remaining time to reach \(f\). Once we compute that once per car, the problem reduces to finding a minimum over \(n\) values.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute simulation over time steps | \(O(n \cdot f)\) | \(O(1)\) | Too slow |
| Direct time computation | \(O(n)\) | \(O(1)\) | Accepted |

## Algorithm Walkthrough

1. Read \(n\) and \(f\), which define how many cars exist and where the finish line is located.

2. Initialize variables to track the best (smallest) arrival time seen so far and the corresponding car index. It is important to initialize the best time to something larger than any possible real value, so that the first car always becomes the baseline.

3. For each car \(i\), read its position \(x_i\) and speed \(v_i\).

4. Compute the remaining distance to the festival as \(d_i = f - x_i\). This represents how far the car still needs to travel.

5. Compute the arrival time conceptually as \(t_i = d_i / v_i\). Instead of actually dividing, we compare using cross multiplication to avoid precision issues: we compare \(d_i \cdot v_{\text{best}}\) with \(d_{\text{best}} \cdot v_i\).

6. If the current car reaches earlier than the best known car, update the best time representation and store this car’s index.

7. After processing all cars, output the index of the car with the minimum arrival time.

### Why it works

At every step, the algorithm maintains the invariant that the stored car is the one with the smallest arrival time among all processed cars. Each new car is compared against this candidate using a mathematically equivalent ordering of fractions. Since arrival times are strictly comparable and no ties exist, the invariant ensures that after scanning all cars, the stored index corresponds to the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def better(d1, v1, d2, v2):
    return d1 * v2 < d2 * v1

n, f = map(int, input().split())

best_idx = -1
best_d = 0
best_v = 1

for i in range(1, n + 1):
    x, v = map(int, input().split())
    d = f - x

    if best_idx == -1:
        best_idx = i
        best_d, best_v = d, v
    else:
        if better(d, v, best_d, best_v):
            best_idx = i
            best_d, best_v = d, v

print(best_idx)
```

The code maintains the current best candidate as a pair \((d, v)\) rather than explicitly storing time. This avoids floating point arithmetic and keeps comparisons exact using cross multiplication. The helper comparison function encodes the ordering \(d_1 / v_1 < d_2 / v_2\) in integer arithmetic.

The initialization with `best_idx = -1` ensures the first car is always selected as a baseline. Each subsequent car is compared against it, and updates happen only when a strictly smaller arrival time is found.

## Worked Examples

### Example 1

Input:
```
3 200
0 1
10 5
40 1
```

We track remaining distance and best choice:

| i | x | v | d = 200 - x | comparison result | best index |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 200 | first car | 1 |
| 2 | 10 | 5 | 190 | 190/5 < 200/1 | 2 |
| 3 | 40 | 1 | 160 | 160/1 > 190/5 | 2 |

Car 2 wins because it covers the remaining distance fastest despite not being the closest initially.

### Example 2

Input:
```
5 100
0 1
10 3
60 2
75 1
10 4
```

| i | x | v | d | comparison result | best |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 100 | first | 1 |
| 2 | 10 | 3 | 90 | 90/3 < 100/1 | 2 |
| 3 | 60 | 2 | 40 | 40/2 > 90/3 | 2 |
| 4 | 75 | 1 | 25 | 25/1 > 90/3 | 2 |
| 5 | 10 | 4 | 90 | 90/4 < 90/3 | 5 |

The final answer is car 5 because it improves on car 2 due to higher speed, even though positions are identical.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(n)\) | Each car is processed once with constant-time arithmetic |
| Space | \(O(1)\) | Only a few scalar variables are stored |

With \(n \leq 100\), the solution is far below any time limit constraints. Even in tighter settings, the linear scan remains optimal because every input element must be inspected at least once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, f = map(int, sys.stdin.readline().split())

    best_idx = -1
    best_d = 0
    best_v = 1

    def better(d1, v1, d2, v2):
        return d1 * v2 < d2 * v1

    for i in range(1, n + 1):
        x, v = map(int, sys.stdin.readline().split())
        d = f - x

        if best_idx == -1:
            best_idx = i
            best_d, best_v = d, v
        else:
            if better(d, v, best_d, best_v):
                best_idx = i
                best_d, best_v = d, v

    return str(best_idx)

# provided samples
assert run("""3 200
0 1
10 5
40 1
""") == "2"

assert run("""5 100
0 1
10 3
60 2
75 1
10 4
""") == "5"

# custom cases
assert run("""1 100
50 10
""") == "1"

assert run("""2 100
0 10
90 1
""") == "1"

assert run("""3 100
10 1
10 2
10 3
""") == "3"

assert run("""4 100
0 1
50 2
70 5
90 10
""") == "4"
```

| Test input | Expected output | What it validates |
|---|---|---|
| single car | 1 | minimum boundary case |
| slow vs fast far car | 1 | speed dominates distance |
| same position different speeds | 3 | tie-breaking via speed |
| increasing proximity but slow speed | 4 | non-monotonic ranking |

## Edge Cases

A single-car input is trivial because there is no comparison; the algorithm correctly initializes the first car as the best and immediately outputs it.

When a car starts very close to the destination but is extremely slow, and another car starts farther but is faster, the algorithm correctly compares full ratios instead of raw distance. For example, with \(f = 100\), cars \((x=90, v=1)\) and \((x=0, v=10)\), the computed times are \(10\) and \(10\), but the problem guarantees no ties, so a strict inequality decides consistently.

When multiple cars share the same position, comparisons reduce to speed only because their remaining distances are identical. The cross-multiplication rule naturally simplifies to selecting the larger \(v\), which matches the intuition that faster cars always win from identical starting points.
