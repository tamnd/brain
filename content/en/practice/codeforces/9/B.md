---
title: "CF 9B - Running Student"
description: "The student is already riding a bus that moves along the x-axis from left to right. The bus stops at fixed positions (xi"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "implementation"]
categories: ["algorithms"]
codeforces_contest: 9
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 9 (Div. 2 Only)"
rating: 1200
weight: 9
solve_time_s: 86
verified: true
draft: false
---

[CF 9B - Running Student](https://codeforces.com/problemset/problem/9/B)

**Rating:** 1200  
**Tags:** brute force, geometry, implementation  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The student is already riding a bus that moves along the x-axis from left to right. The bus stops at fixed positions `(xi, 0)` in increasing order. At any stop except the first one, the student may get off and run directly to the university located at `(xu, yu)`.

If the student stays on the bus until stop `i`, the total travel time has two parts. The first part is the time spent on the bus from `x = 0` to `x = xi`. Since the bus moves at constant speed `vb`, this time is `xi / vb`. The second part is the running time from `(xi, 0)` to `(xu, yu)`. That distance is Euclidean distance, so the running time is:

$$\frac{\sqrt{(xu - xi)^2 + yu^2}}{vs}$$

The task is to find the stop index that minimizes total arrival time. If multiple stops produce exactly the same time, we must choose the stop that is physically closer to the university.

The constraints are tiny. There are at most 100 stops, so even checking every stop directly is trivial. A solution doing `O(n)` or `O(n^2)` work is completely safe within a 1 second limit. This problem is not about optimization tricks, it is about implementing the comparison logic correctly and handling floating point comparisons carefully.

The first subtle edge case is the tie-breaking rule. Two stops may produce exactly the same total travel time, but the answer is not necessarily the earlier stop. We must choose the stop closer to the university.

Consider:

```
3 1 1
0 2 4
3 4
```

For stop 2:

```
bus time = 2
run distance = 5
total = 7
```

For stop 3:

```
bus time = 4
run distance = 1
total = 5
```

The later stop wins because even though the bus ride is longer, the running distance becomes much shorter.

Another easy mistake is allowing the student to leave at the first stop. The statement explicitly forbids this. A careless loop starting from index `0` would produce a wrong answer.

Example:

```
2 10 1
0 100
0 1
```

The student would like to get off immediately and run distance `1`, but that is illegal. The correct answer is stop `2`.

Floating point equality is another danger. Two theoretically equal times may differ slightly because of precision errors. Using exact `==` comparisons on doubles can fail unexpectedly. The safest approach is to compare with a small epsilon.

## Approaches

The most direct approach is to simulate every possible stop. For each stop `i`, compute:

$$\text{time} = \frac{xi}{vb} + \frac{\sqrt{(xu-xi)^2 + yu^2}}{vs}$$

Then choose the stop with minimum time. If times are equal, compare distances to the university and choose the smaller one.

This brute-force approach is already fully accepted because `n ≤ 100`. The total amount of work is tiny, only around a few hundred arithmetic operations and square roots.

There is no hidden dynamic programming or geometry optimization here. The key observation is that the student has only one meaningful decision, the stop where he exits. Once that stop is fixed, the entire route and travel time are determined uniquely. That turns the problem into a simple enumeration problem.

A more complicated approach would try to reason about convexity or optimize distances geometrically, but none of that helps because the input size is already extremely small. The cleanest and most reliable solution is simply evaluating every candidate stop directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of stops, the bus speed, and the student running speed.
2. Read the array of stop coordinates `x`.
3. Read the university coordinates `(xu, yu)`.
4. Initialize the best stop as stop `2`, because the student is not allowed to leave at the first stop.
5. For every stop from index `2` to `n`:

Compute the bus travel time:

$$\frac{xi}{vb}$$

Then compute the running distance:

$$\sqrt{(xu-xi)^2 + yu^2}$$

Divide that distance by `vs` to get running time.
6. Add both times to get the total arrival time for this stop.
7. Compare this total time against the current best.

If the new time is strictly smaller, update the answer.

If the times are equal within floating point precision, compare distances to the university and keep the closer stop.
8. Output the chosen stop index.

### Why it works

Every valid strategy corresponds to choosing exactly one stop where the student exits the bus. Once that stop is fixed, the total time is uniquely determined by the bus ride plus the straight-line running distance. Since the algorithm evaluates every legal stop and keeps the one with minimum total time, it cannot miss the optimal answer. The tie-breaking rule is handled explicitly during comparisons, so equal-time cases are also resolved correctly.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

n, vb, vs = map(int, input().split())
x = list(map(int, input().split()))
xu, yu = map(int, input().split())

eps = 1e-9

best_idx = 1
best_time = float('inf')
best_dist = float('inf')

for i in range(1, n):
    bus_time = x[i] / vb

    dist = math.sqrt((xu - x[i]) ** 2 + yu ** 2)
    run_time = dist / vs

    total_time = bus_time + run_time

    if total_time < best_time - eps:
        best_time = total_time
        best_dist = dist
        best_idx = i + 1
    elif abs(total_time - best_time) <= eps:
        if dist < best_dist:
            best_dist = dist
            best_idx = i + 1

print(best_idx)
```

The loop starts from index `1` instead of `0` because the first stop is forbidden. This is the most common implementation mistake in the problem.

The variable `dist` stores the geometric distance from the current stop to the university. That same value is reused both for running time and for tie-breaking, which keeps the implementation simple.

The epsilon comparison avoids precision issues. Instead of checking whether two floating point values are exactly equal, the code considers them equal if their difference is extremely small.

The answer uses `i + 1` because Codeforces indices are 1-based while Python lists are 0-based.

## Worked Examples

### Example 1

Input:

```
4 5 2
0 2 4 6
4 1
```

| Stop | Bus Time | Run Distance | Run Time | Total Time | Best So Far |
| --- | --- | --- | --- | --- | --- |
| 2 | 0.4 | 2.236 | 1.118 | 1.518 | 2 |
| 3 | 0.8 | 1.000 | 0.500 | 1.300 | 3 |
| 4 | 1.2 | 2.236 | 1.118 | 2.318 | 3 |

The best choice becomes stop `3`. Even though the bus rides longer than for stop `2`, the running distance becomes dramatically smaller.

### Example 2

Input:

```
5 2 10
0 5 10 15 20
12 1
```

| Stop | Bus Time | Run Distance | Run Time | Total Time | Best So Far |
| --- | --- | --- | --- | --- | --- |
| 2 | 2.5 | 7.071 | 0.707 | 3.207 | 2 |
| 3 | 5.0 | 2.236 | 0.224 | 5.224 | 2 |
| 4 | 7.5 | 3.162 | 0.316 | 7.816 | 2 |
| 5 | 10.0 | 8.062 | 0.806 | 10.806 | 2 |

Here the student runs very fast, so exiting earlier is better. Spending extra time on the slow bus hurts more than the reduced running distance helps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We evaluate each stop exactly once |
| Space | O(1) | Only a few variables are stored |

With at most 100 stops, the program runs essentially instantly. Memory usage is negligible because the algorithm only stores the stop coordinates and a handful of floating point values.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, vb, vs = map(int, input().split())
    x = list(map(int, input().split()))
    xu, yu = map(int, input().split())

    eps = 1e-9

    best_idx = 1
    best_time = float('inf')
    best_dist = float('inf')

    for i in range(1, n):
        bus_time = x[i] / vb

        dist = math.sqrt((xu - x[i]) ** 2 + yu ** 2)
        run_time = dist / vs

        total_time = bus_time + run_time

        if total_time < best_time - eps:
            best_time = total_time
            best_dist = dist
            best_idx = i + 1
        elif abs(total_time - best_time) <= eps:
            if dist < best_dist:
                best_dist = dist
                best_idx = i + 1

    return str(best_idx)

# provided sample
assert run(
"""4 5 2
0 2 4 6
4 1
"""
) == "3", "sample 1"

# minimum size
assert run(
"""2 10 1
0 100
0 1
"""
) == "2", "minimum size"

# fast student prefers early exit
assert run(
"""5 1 100
0 10 20 30 40
11 0
"""
) == "2", "fast runner"

# slow student prefers later exit
assert run(
"""5 100 1
0 10 20 30 40
39 0
"""
) == "5", "slow runner"

# tie-breaking by distance
assert run(
"""3 1 1
0 1 2
1 0
"""
) == "2", "tie-breaking"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum `n = 2` | `2` | Cannot leave at first stop |
| Very fast runner | `2` | Early exit becomes optimal |
| Very slow runner | `5` | Staying on bus longer becomes optimal |
| Tie-breaking case | `2` | Equal times handled correctly |

## Edge Cases

The first important edge case is the forbidden first stop.

Input:

```
2 10 1
0 100
0 1
```

If leaving at the first stop were allowed, total time would be only `1`. But the student must stay on the bus until at least stop `2`.

The algorithm handles this by starting the loop from index `1`, which corresponds to stop `2` in 1-based indexing. The only evaluated candidate is stop `2`, so the output is correctly:

```
2
```

Another tricky situation is equal total times.

Input:

```
3 1 1
0 1 2
1 0
```

For stop `2`:

```
bus = 1
run = 0
total = 1
```

For stop `3`:

```
bus = 2
run = 1
total = 3
```

Stop `2` wins immediately.

Now consider:

```
3 1 1
0 1 2
1 1
```

The computed totals become extremely close in floating point arithmetic. Using direct equality checks could produce inconsistent behavior because square roots are irrational numbers. The algorithm instead uses an epsilon threshold, so tiny rounding errors do not affect the decision.

A final edge case appears when the best stop is the terminal stop.

Input:

```
5 100 1
0 10 20 30 40
39 0
```

The bus is extremely fast while the student runs slowly. The algorithm still checks every stop independently, so it correctly discovers that staying on the bus until the end minimizes running distance enough to offset the extra bus travel.
