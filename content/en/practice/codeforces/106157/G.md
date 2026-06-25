---
title: "CF 106157G - Get Good"
description: "Charlie has n days before a contest. When he is fresh, he gains a skill points per day, but only for the first x consecutive working days after a reset. If he keeps working beyond those x days, he becomes tired and gains only b skill points per day, where a ≥ b."
date: "2026-06-25T11:19:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106157
codeforces_index: "G"
codeforces_contest_name: "2025 United Kingdom and Ireland Programming Contest (UKIEPC 2025)"
rating: 0
weight: 106157
solve_time_s: 51
verified: true
draft: false
---

[CF 106157G - Get Good](https://codeforces.com/problemset/problem/106157/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

Charlie has `n` days before a contest.

When he is fresh, he gains `a` skill points per day, but only for the first `x` consecutive working days after a reset. If he keeps working beyond those `x` days, he becomes tired and gains only `b` skill points per day, where `a ≥ b`.

At any moment he may start a break. A break lasts exactly `y` consecutive days and gives no skill points. After the break finishes, Charlie becomes fresh again and can once more enjoy `x` days of gain `a`. The goal is to maximize the total skill points collected over the available `n` days.

The constraints are the key part of the problem. Both `n` and the other parameters can be as large as `10^9`, and there may be up to `10^4` test cases. Any simulation day by day is impossible. The solution must be based on a closed-form optimization that runs in constant time per test case.

A subtle point is that breaks are not always useful. If taking a break costs more skill than the fresh period gains back, then the optimal strategy may be to never rest at all.

Another easy mistake is assuming that every fresh period should always be fully used. Near the end of the schedule, there may not be enough remaining days to consume all `x` fresh days, so the final segment has to be handled carefully.

Consider:

```
n = 5, a = 4, b = 1, x = 3, y = 1
```

Working all five days gives:

```
4 + 4 + 4 + 1 + 1 = 14
```

Taking a break after day 3 gives:

```
4 + 4 + 4 + 0 + 4 = 16
```

The break is worthwhile because it trades one tired day for another fresh day.

Now consider:

```
n = 10, a = 6, b = 5, x = 1, y = 5
```

A break consumes five days just to recover a single high-value day. Continuing to work is much better.

## Approaches

A brute-force view is to try every possible placement of breaks. Each schedule consists of working segments separated by breaks. The gain of a segment of length `L` is

```
a * min(L, x) + b * max(0, L - x)
```

This formulation is correct, but the number of possible break placements grows exponentially and becomes hopeless even for moderate values of `n`.

The important observation is that only the number of breaks matters.

Suppose we take exactly `m` breaks.

Those breaks consume `m * y` days, leaving

```
W = n - m * y
```

working days.

The total bonus above the tired rate comes from fresh days. Every working day is worth at least `b`. A fresh day contributes an additional

```
a - b
```

bonus.

With `m` breaks, there are `m + 1` working segments. Each segment can contribute at most `x` fresh days, so the total number of fresh days cannot exceed

```
(m + 1) * x
```

and also cannot exceed the number of working days `W`.

Hence:

```
fresh_days = min(W, (m + 1) * x)
```

The total gain becomes

```
b * W + (a - b) * fresh_days
```

or

```
G(m) = b * (n - m y)
     + (a - b) * min(n - m y, (m + 1) x)
```

Now the problem has become a one-dimensional optimization.

There are two regions.

When

```
n - m y > (m + 1) x
```

all fresh slots are fully used. Then

```
G(m)
= b n + (a - b) x + m((a - b)x - by)
```

which is linear in `m`.

When

```
n - m y ≤ (m + 1) x
```

every working day is fresh, so

```
G(m) = a(n - m y)
```

which decreases as `m` increases.

A linear function followed by a decreasing function means the optimum can only occur at one of the boundary points. We can compute those directly in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over schedules | Exponential | Exponential | Too slow |
| Closed-form optimization | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. If `n ≤ x`, every available day can be spent in the initial fresh period. The answer is simply:

```
a * n
```
2. Compute

```
m0 = ceil((n - x) / (x + y))
```

This is the smallest number of breaks for which every remaining working day can be fresh.
3. Evaluate the first candidate:

```
G2 = a * (n - m0 * y)
```

This corresponds to the second region where all working days are fresh.
4. Compute

```
c = (a - b) * x - b * y
```

This is the profit obtained by adding one more complete cycle consisting of `x` fresh days and `y` break days.
5. If `c ≤ 0`, the linear region is decreasing, so its best point is `m = 0`.
6. If `c > 0`, the linear region is increasing, so its best point is the largest valid `m` before crossing into the second region:

```
m1 = m0 - 1
```
7. Evaluate

```
G1 = G(m1)
```

or `G(0)` when `c ≤ 0`.
8. The answer is

```
max(G1, G2)
```

### Why it works

For a fixed number of breaks, the optimal arrangement is determined entirely by how many working segments exist. Each segment contributes at most `x` fresh days, so the total number of fresh days is exactly `min(W, (m + 1)x)`.

This reduces the whole problem to a function of a single integer `m`. That function is linear while fresh capacity is fully saturated, then becomes a decreasing line once every working day is already fresh. Since the function has only one transition point, the maximum must occur either at the best point of the first line or at the first point of the second line. Evaluating those candidates is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, a, b, x, y = map(int, input().split())

        if n <= x:
            print(a * n)
            continue

        m0 = (n - x + (x + y) - 1) // (x + y)

        ans = a * (n - m0 * y)

        c = (a - b) * x - b * y

        if c <= 0:
            m = 0
        else:
            m = m0 - 1

        w = n - m * y
        g = b * w + (a - b) * min(w, (m + 1) * x)

        ans = max(ans, g)

        print(ans)

solve()
```

The first branch handles the easy situation where the initial fresh period already covers all available days.

`m0` is the first break count for which the total fresh capacity becomes large enough to cover every working day. Computing it with ceiling division is the most delicate part of the implementation.

The variable `c` measures whether adding another full fresh cycle is profitable. If it is not profitable, the best point in the linear region is immediately at `m = 0`. Otherwise the linear region increases up to its boundary, so we evaluate the last valid point before the transition.

All arithmetic fits comfortably in 64-bit integers, but Python's arbitrary-precision integers remove even that concern.

## Worked Examples

### Example 1

Input:

```
5 4 1 3 1
```

| Variable | Value |
| --- | --- |
| n | 5 |
| a | 4 |
| b | 1 |
| x | 3 |
| y | 1 |

Compute:

| Step | Value |
| --- | --- |
| m0 | 1 |
| G2 | 4 × (5 - 1) = 16 |
| c | (4 - 1) × 3 - 1 × 1 = 8 |
| m1 | 0 |
| G1 | 14 |

Answer:

```
16
```

This demonstrates a case where taking a break is beneficial.

### Example 2

Input:

```
10 6 5 1 5
```

| Step | Value |
| --- | --- |
| m0 | 2 |
| G2 | 0 |
| c | (6 - 5) × 1 - 5 × 5 = -24 |
| m | 0 |
| G1 | 51 |

Answer:

```
51
```

This shows a situation where breaks are too expensive and the optimal strategy is continuous work.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations |
| Space | O(1) | No auxiliary structures |

Even with `10^4` test cases and parameters up to `10^9`, this runs comfortably within the limits because every test case is solved using constant-time arithmetic.

## Test Cases

```python
# helper reference implementation

def solve_case(n, a, b, x, y):
    if n <= x:
        return a * n

    m0 = (n - x + (x + y) - 1) // (x + y)

    ans = a * (n - m0 * y)

    c = (a - b) * x - b * y

    if c <= 0:
        m = 0
    else:
        m = m0 - 1

    w = n - m * y
    g = b * w + (a - b) * min(w, (m + 1) * x)

    return max(ans, g)

assert solve_case(2, 2, 2, 2, 2) == 4
assert solve_case(4, 4, 2, 3, 3) == 14
assert solve_case(5, 3, 2, 3, 1) == 13
assert solve_case(5, 4, 1, 3, 1) == 16

assert solve_case(1, 10, 5, 7, 3) == 10
assert solve_case(10, 5, 5, 3, 2) == 50
assert solve_case(10, 6, 5, 1, 5) == 51
assert solve_case(1000000000, 1000000000, 1, 1000000000, 1) == 1000000000000000000
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 10 5 7 3` | `10` | Minimum-length schedule |
| `10 5 5 3 2` | `50` | Equal rates, breaks never help |
| `10 6 5 1 5` | `51` | Negative cycle profit |
| Large values | `10^18` | 64-bit scale arithmetic |

## Edge Cases

Consider:

```
1
1 10 5 7 3
```

Since `n ≤ x`, Charlie never becomes tired. The algorithm immediately returns:

```
10 × 1 = 10
```

No break-related logic is needed.

Consider:

```
1
10 5 5 3 2
```

Fresh and tired days have identical value. The cycle profit is negative because breaks only waste time. The algorithm selects `m = 0`, producing:

```
10 × 5 = 50
```

which is optimal.

Consider:

```
1
5 4 1 3 1
```

The transition point occurs exactly at one break. The algorithm evaluates both sides of the boundary:

```
G(0) = 14
G(1) = 16
```

and chooses `16`, correctly handling the point where the optimal strategy changes from continuous work to using a reset.
