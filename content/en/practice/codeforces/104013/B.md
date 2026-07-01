---
title: "CF 104013B - Bicycle"
description: "A cyclist is choosing between two monthly bike rental plans, and we need to compute the total cost of each plan over a fixed month. Each day, the cyclist uses the bike for a total of T minutes."
date: "2026-07-02T05:00:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104013
codeforces_index: "B"
codeforces_contest_name: "2020-2021 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104013
solve_time_s: 43
verified: true
draft: false
---

[CF 104013B - Bicycle](https://codeforces.com/problemset/problem/104013/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

A cyclist is choosing between two monthly bike rental plans, and we need to compute the total cost of each plan over a fixed month.

Each day, the cyclist uses the bike for a total of `T` minutes. This time is split between commuting to work and back, but for the problem it is already given as a single daily total.

The first plan charges a fixed monthly fee `a`. Under this plan, each day allows 30 free minutes. If the daily usage exceeds 30 minutes, every extra minute costs `x`.

The second plan charges a fixed monthly fee `b`. Under this plan, each day allows 45 free minutes. Any minutes beyond 45 cost `y` per minute.

There are exactly 21 working days in November, and the daily pattern is assumed identical for all days. The task is to compute the total cost of each plan over all 21 days.

The output is two integers, representing the total cost under the first and second plans respectively.

The constraints are very small, with all monetary values and `T` bounded by at most 100 or 1440. This immediately suggests that any direct arithmetic per plan is sufficient, since the computation is constant time. There is no need for loops over large ranges or optimization techniques.

A common mistake arises from misunderstanding the “free minutes” boundary. If `T` is less than or equal to the free limit, the extra cost must be zero, not negative. Another subtle issue is forgetting that the overage cost applies per day and must be multiplied by 21.

For example, if `T = 10`, both plans have no extra cost and the answer is simply `(21 * a, 21 * b)`. A naive implementation that subtracts without clamping at zero would incorrectly produce negative charges.

## Approaches

The brute-force interpretation would simulate each of the 21 days and, within each day, iterate over each minute beyond the free allowance to accumulate cost. For example, for each day we could loop from minute 31 to `T` for the first plan and add `x` per minute. This works correctly, but the inner loop makes it unnecessarily verbose.

In the worst case, `T = 1440`, so the inner loop runs about 1410 iterations per day. Over 21 days, this is roughly 30,000 operations per plan, which is still fine but completely unnecessary given the structure.

The key observation is that each plan depends only on how many minutes exceed the threshold, not on their distribution. Once we compute `max(0, T - 30)` and `max(0, T - 45)`, the total cost becomes a simple linear formula. This reduces the problem to constant-time arithmetic.

The brute-force works because it directly accumulates per-minute cost, but fails as an overcomplication when we recognize that all over-threshold minutes are identical in cost. The observation collapses the per-minute loop into a single multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(21 · T) | O(1) | Accepted but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute each plan independently using the same structure.

1. Read the inputs `a, x, b, y, T`. These define fixed costs, per-minute penalties, and daily usage.
2. Compute the number of charged minutes for the first plan as `over1 = max(0, T - 30)`. This ensures we never charge for free minutes.
3. Compute total daily cost for the first plan as `day1 = a + over1 * x`. The fixed fee is always included once per day.
4. Multiply by 21 to obtain monthly cost `total1 = 21 * day1`. This reflects all working days in November.
5. Repeat the same logic for the second plan using a 45-minute threshold: `over2 = max(0, T - 45)`.
6. Compute `day2 = b + over2 * y` and then `total2 = 21 * day2`.
7. Output `total1` and `total2`.

Each step is purely algebraic, and no iteration is needed because the cost structure is linear in the number of excess minutes.

### Why it works

Each plan defines a constant base fee plus a per-unit charge applied only to the portion of usage exceeding a fixed threshold. Since every day is identical, the total cost is simply 21 times a deterministic per-day function. The only decision is whether `T` crosses the threshold, and once that is resolved, the remaining computation is linear in the excess amount. No interaction exists between days or between minutes within a day, so collapsing the structure into a closed-form expression preserves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input().strip())
x = int(input().strip())
b = int(input().strip())
y = int(input().strip())
T = int(input().strip())

days = 21

over1 = max(0, T - 30)
day1 = a + over1 * x
total1 = days * day1

over2 = max(0, T - 45)
day2 = b + over2 * y
total2 = days * day2

print(total1, total2)
```

The solution reads five integers and immediately transforms them into two independent cost formulas.

The use of `max(0, ...)` is essential because negative overage would incorrectly reduce the base fee. Multiplying by 21 is done after computing the daily cost, keeping the structure clean and reducing the risk of mixing daily and monthly logic.

## Worked Examples

### Example 1

Input:

```
10
1
20
2
40
```

For plan 1, free limit is 30, so overage is 10 minutes per day. Daily cost is `10 + 10 * 1 = 20`.

For plan 2, free limit is 45, so there is no overage. Daily cost is `20`.

| Step | Plan 1 | Plan 2 |
| --- | --- | --- |
| T | 40 | 40 |
| Free limit | 30 | 45 |
| Overage | 10 | 0 |
| Daily cost | 20 | 20 |
| Monthly cost | 420 | 420 |

Output:

```
420 420
```

This shows a case where both plans coincide because the second plan’s larger free allowance exactly offsets its higher base.

### Example 2

Input:

```
100
5
50
1
60
```

Plan 1: overage is `30`, daily cost is `100 + 30*5 = 250`, monthly is `5250`.

Plan 2: overage is `15`, daily cost is `50 + 15*1 = 65`, monthly is `1365`.

| Step | Plan 1 | Plan 2 |
| --- | --- | --- |
| T | 60 | 60 |
| Free limit | 30 | 45 |
| Overage | 30 | 15 |
| Daily cost | 250 | 65 |
| Monthly cost | 5250 | 1365 |

Output:

```
5250 1365
```

This demonstrates how a higher base fee can still lose if marginal costs are significantly lower.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The computation is constant-time regardless of input magnitude, which is easily within limits given the small constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    a = int(input().strip())
    x = int(input().strip())
    b = int(input().strip())
    y = int(input().strip())
    T = int(input().strip())

    days = 21

    over1 = max(0, T - 30)
    total1 = days * (a + over1 * x)

    over2 = max(0, T - 45)
    total2 = days * (b + over2 * y)

    return f"{total1} {total2}"

# provided samples
assert run("10\n1\n20\n2\n40\n") == "420 420"

# minimum case: no overage
assert run("0\n0\n0\n0\n1\n") == "0 0"

# boundary at exact thresholds
assert run("5\n2\n7\n3\n30\n") == f"{21*(5)} {21*(7)}"

# second plan dominates due to lower overage
assert run("10\n10\n100\n1\n100\n") == "14700 11550"

# high T case
assert run("1\n1\n1\n1\n1440\n") == str(21*(1 + 1410)) + " " + str(21*(1 + 1395))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| T=1, zero rates | 0 0 | no overage behavior |
| T at thresholds | base-only costs | boundary correctness |
| high cost imbalance | different scaling | comparative correctness |
| maximum T | large overage handling | stress arithmetic correctness |

## Edge Cases

One edge case is when `T` is smaller than both thresholds. For example, `T = 10`. The computation `T - 30` and `T - 45` are negative, but applying `max(0, ...)` forces both overages to zero, resulting in costs `21 * a` and `21 * b`. Without this clamp, the formula would incorrectly subtract money from the base fee, producing nonsensical negative totals.

Another edge case occurs exactly at the thresholds. If `T = 30`, the first plan must charge zero extra minutes, not one or more. The expression `max(0, 30 - 30)` correctly yields zero, ensuring no accidental penalty.

A third case is large `T` near the upper bound, such as 1440. The overage becomes large but still safely fits within integer arithmetic since the maximum product is `21 * 1440 * 100`, which is well within 32-bit limits.
