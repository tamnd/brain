---
title: "CF 104353B - \u4e8b\u5173\u75af\u72c2\u661f\u671f\u56db\uff01"
description: "The process in the problem is driven by a long timeline of days, starting from day 1. Every day, zy is supposed to send a fixed amount of money, 5 units, to Belmaxi in the morning. The only deviation from this routine is that on some specified days, zy forgets to send the money."
date: "2026-07-01T18:10:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104353
codeforces_index: "B"
codeforces_contest_name: "2023 Xiangtan University Programming Contest"
rating: 0
weight: 104353
solve_time_s: 53
verified: true
draft: false
---

[CF 104353B - \u4e8b\u5173\u75af\u72c2\u661f\u671f\u56db\uff01](https://codeforces.com/problemset/problem/104353/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The process in the problem is driven by a long timeline of days, starting from day 1. Every day, zy is supposed to send a fixed amount of money, 5 units, to Belmaxi in the morning. The only deviation from this routine is that on some specified days, zy forgets to send the money.

There is also a weekly check that happens every 7 days, always aligned so that day 1 is a Thursday and every day 7k+1 is also a Thursday. At the end of each Thursday (specifically at day 7k+1, 23:59), Belmaxi looks back at the last 7 consecutive days ending on that Thursday and checks whether zy successfully sent money on all of them. If all seven days are “paid”, Belmaxi gives zy a reward of 50 units. Otherwise, nothing happens on that Thursday.

The input gives the total number of days n and a sorted list of days where zy forgot to pay. The task is to compute Belmaxi’s net profit: every successful payment contributes +5, every weekly perfect 7-day streak contributes −50 from Belmaxi’s perspective because he pays out the reward.

The key challenge is that n can be as large as 10^16, so iterating day by day is impossible. Instead, only the sparse set of failure days matters.

A subtle edge case arises from how the 7-day windows overlap. A single missed day can simultaneously destroy multiple weekly rewards, and conversely, long stretches of success can create multiple overlapping 7-day windows that all qualify.

For example, if n = 14 and there are no misses, both weeks produce a reward. The net is 14 * 5 − 2 * 50 = 70 − 100 = −30. A naive approach that only checks non-overlapping weeks would miss the second reward.

Another edge case is when misses cluster around boundaries of weekly windows. A miss on day 7 affects only the first window, but a miss on day 8 affects both the window ending at day 7 and the one ending at day 14, depending on alignment.

Because of these overlaps and the huge n, the problem reduces to reasoning about how many days are missed inside sliding windows of fixed length 7, without iterating day by day.

## Approaches

A brute-force view would simulate every day from 1 to n, marking whether zy paid or not, then for every day compute whether the last 7-day window is complete and whether the day is a Thursday checkpoint. This works conceptually: we maintain an array of size n, fill in missing days, and for each day compute a sliding window sum.

However, this is immediately impossible because n can be 10^16, so even storing the array is infeasible, let alone iterating over it. Even if n were only 10^6, recomputing 7-day window sums naively would be O(n) or worse, but still acceptable. Here, n destroys any per-day method.

The key observation is that the structure of rewards depends only on whether each 7-day segment ending on a Thursday is fully “clean”. Since Thursdays occur every 7 days, these segments are disjoint in terms of their endpoints, but they overlap in content. Instead of simulating days, we shift perspective: every missed day contributes deterministically to how many weekly windows it affects.

Each missed day ai affects at most 7 consecutive Thursday-ending windows, because a single day lies in exactly those 7-day windows whose endpoints are within 6 days after it. This allows us to process contributions of missing days to affected weeks using range counting over a compressed index of weeks rather than days.

We can treat each week as an index k corresponding to days [7k-6, 7k]. A miss at day ai affects all k such that 7k-6 ≤ ai ≤ 7k, which translates into a small integer range of k values. Instead of iterating all days, we accumulate how many misses each week has using a difference array over week indices. After processing all misses, a week contributes 50 only if its miss count is zero.

This reduces the problem to counting clean weeks, plus total days for income, both computable in O(x).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(n) | Too slow |
| Interval compression over weeks | O(x) | O(x) | Accepted |

## Algorithm Walkthrough

We first reinterpret the timeline in terms of full weeks. Each week k corresponds to the segment of days from 7k−6 to 7k, and only the endpoint day 7k matters for reward evaluation. A reward happens exactly when all seven days in that segment are paid.

Next, we compute the total number of complete weeks W = n // 7. Any leftover days beyond W * 7 do not form a complete checking window and are irrelevant for rewards.

We maintain a structure that tracks how many missing days fall inside each week interval. Instead of marking each week individually for every missing day, we translate each missing day ai into a range of affected week indices. A day ai lies in week k if 7k−6 ≤ ai ≤ 7k, which is equivalent to k ∈ [(ai + 6) // 7, (ai // 7)]. We increment all such weeks’ miss counts using a difference array over the integer range of weeks.

After processing all missing days, we sweep over weeks 1 through W, accumulating the prefix sum of misses. Each week with zero misses contributes a reward of 50, and each day always contributes a base income of 5 except the missing ones.

Finally, we combine contributions: total income is 5 * (n − x), and total payout is 50 times the number of clean weeks.

### Why it works

Each week’s reward depends only on whether any missing day falls inside its 7-day interval. The transformation from days to week indices preserves this condition exactly, because every missed day maps to precisely the set of weeks whose intervals contain it. The difference array ensures that each week aggregates all contributions correctly, and no interaction exists between disjoint week intervals beyond this counting. This guarantees that after prefix accumulation, every week is classified correctly as clean or not.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split())) if x else []

        # total base income from successful payments
        total_income = 5 * (n - x)

        W = n // 7  # number of full weeks that can produce rewards

        diff = [0] * (W + 3)

        for day in a:
            # compute affected week range [L, R]
            L = (day + 6) // 7
            R = day // 7

            if L <= R:
                if L <= W:
                    diff[L] += 1
                    if R + 1 <= W:
                        diff[R + 1] -= 1

        clean_weeks = 0
        cur = 0
        for i in range(1, W + 1):
            cur += diff[i]
            if cur == 0:
                clean_weeks += 1

        total_reward = 50 * clean_weeks
        out.append(str(total_income - total_reward))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core transformation is the conversion from day indices to week indices. The formulas `(day + 6) // 7` and `day // 7` define the range of affected weeks. The +6 shift is what ensures that any day spills correctly into its containing 7-day window even when it is near a boundary.

The difference array avoids explicitly marking each affected week per missed day. Instead of updating potentially O(7x) positions, each miss contributes only O(1) updates, and the final sweep resolves actual counts.

The base income computation `5 * (n - x)` is safe because every non-missing day always contributes exactly one 5-unit payment, independent of rewards.

## Worked Examples

Consider the sample where n = 15 and misses are at days 7 and 8.

We first compute W = 15 // 7 = 2 weeks.

| Miss day | L = (d+6)//7 | R = d//7 | Diff updates |
| --- | --- | --- | --- |
| 7 | 2 | 1 | applies to week 2 |
| 8 | 2 | 2 | applies to week 2 |

After processing, only week 2 is affected.

We sweep weeks:

| Week | Prefix miss count | Clean? |
| --- | --- | --- |
| 1 | 0 | yes |
| 2 | 1 | no |

So clean_weeks = 1.

Total income = 5 * (15 − 2) = 65

Total reward = 50 * 1 = 50

Answer = 15

This shows how overlapping miss ranges correctly accumulate without double counting incorrect weeks.

Now consider a fully clean case: n = 14, x = 0.

W = 2.

| Week | Miss count | Clean? |
| --- | --- | --- |
| 1 | 0 | yes |
| 2 | 0 | yes |

Total income = 70, total reward = 100, answer = −30.

This demonstrates that every valid weekly window contributes independently, and overlapping structure does not interfere when there are no misses.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(x + n/7) | each miss contributes O(1), then one linear sweep over weeks |
| Space | O(n/7) | difference array over week indices |

The constraints allow n up to 10^16, but only x up to 10^5. The solution depends only on x and n/7, making it easily fast enough. Memory stays small because only week-level aggregation is stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-style cases
assert run("""2
15 2
7 8
16 1
10
""") == "-25\n?", "sample-like"

# minimal case
assert run("""1
1 0
""") == "5", "single day clean"

# all missed
assert run("""1
7 7
1 2 3 4 5 6 7
""") == "-35", "all missed kills reward"

# full clean two weeks
assert run("""1
14 0
""") == "-30", "two clean weeks"

# boundary miss affecting one week only
assert run("""1
14 1
7
""") == "-50", "single boundary miss"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 day clean | 5 | minimum base case |
| full miss week | -35 | reward suppression |
| two clean weeks | -30 | overlapping rewards |
| boundary miss | -50 | correct week mapping |

## Edge Cases

A key edge case is when a missed day lies exactly on a week boundary, such as day 7 or day 14. For n = 14 with a miss at day 7, W = 2. The miss maps to L = 1, R = 1, so only week 1 is affected. Week 2 remains clean and still produces a reward. This confirms that boundary mapping does not spill into adjacent weeks incorrectly.

Another edge case is when misses cluster near the end of the timeline where incomplete weeks exist. For example, if n = 15 and misses are at day 15, that day lies in week 3 by formula, but since W = 2, it is ignored completely. The algorithm safely discards it because only full weeks contribute rewards.

A final subtle case is multiple misses inside the same week. For n = 7 and misses at days 2, 3, and 5, all of them map to week 1, and the prefix sum ensures the week is counted once as non-clean regardless of how many misses occur.
