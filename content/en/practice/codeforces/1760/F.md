---
title: "CF 1760F - Quests"
description: "We have n quests. Quest i gives a[i] coins whenever it is completed. During d days we may perform at most one quest per day. After doing a quest, we must wait k days before doing that same quest again."
date: "2026-06-09T14:24:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1760
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 835 (Div. 4)"
rating: 1500
weight: 1760
solve_time_s: 189
verified: true
draft: false
---

[CF 1760F - Quests](https://codeforces.com/problemset/problem/1760/F)

**Rating:** 1500  
**Tags:** binary search, greedy, sortings  
**Solve time:** 3m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` quests. Quest `i` gives `a[i]` coins whenever it is completed.

During `d` days we may perform at most one quest per day. After doing a quest, we must wait `k` days before doing that same quest again.

We need the largest `k` for which it is possible to earn at least `c` coins within `d` days.

If even `k = 0` cannot reach `c`, the answer is `Impossible`.

If arbitrarily large `k` values work, the answer is `Infinity`.

The sum of all `n` and all `d` is at most `2·10^5`, so an `O(n log n + d log d)` style solution per test case is acceptable. Exhaustively simulating many candidate values of `k` is not.

## Key Observation

Sort rewards in descending order.

For a fixed cooldown `k`, the optimal strategy is greedy:

During any block of `k+1` consecutive days, a quest cannot appear twice. Therefore the best possible block consists of the largest `k+1` quest values.

Let

```
cycle = k + 1
```

Suppose we have

```
full = d // cycle
rem  = d % cycle
```

Every complete cycle contributes the sum of the largest `cycle` rewards.

The remaining `rem` days contribute the sum of the largest `rem` rewards.

If `cycle > n`, we simply use all available quests once inside a cycle, because there are no more distinct quests.

This gives an efficient way to compute the maximum obtainable coins for a fixed `k`.

## Why Binary Search Works

As `k` increases, the restriction becomes stricter.

The maximum achievable coins is monotone non-increasing with respect to `k`.

Therefore:

```
can(k) = achievable_coins(k) >= c
```

is a monotone predicate.

We can binary search the largest valid `k`.

## Detecting Infinity

If `k` is arbitrarily large, every quest can effectively be used at most once during the whole period.

The best possible income then is

```
sum of largest min(n, d) rewards
```

If this value is already at least `c`, then every sufficiently large `k` works.

Answer:

```
Infinity
```

## Detecting Impossible

When `k = 0`, we may repeat the best quest every day.

Maximum possible income becomes

```
d * max(a)
```

If this is still below `c`, reaching the target is impossible.

Answer:

```
Impossible
```

## Algorithm

1. Sort rewards descending.
2. Build prefix sums.
3. Check Infinity.
4. Check Impossible.
5. Binary search the largest valid `k`.
6. Output that value.

## Correctness Sketch

For a fixed `k`, any quest can appear at most once in every block of length `k+1`.

Thus the optimal schedule repeatedly takes the largest available rewards within each such block. Since rewards are independent and never decrease, choosing the largest rewards maximizes every cycle independently.

The resulting value computed by `can(k)` equals the true optimum for that cooldown.

Since increasing `k` only removes feasible schedules, `can(k)` is monotone. Binary search therefore finds the maximum feasible `k`.

The Infinity check evaluates the limit where quests are never repeated. The Impossible check evaluates the opposite extreme where repetition is unrestricted. These cover the two special outputs.

Hence the algorithm always returns the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, c, d = map(int, input().split())
        a = list(map(int, input().split()))

        a.sort(reverse=True)

        pref = [0]
        for x in a:
            pref.append(pref[-1] + x)

        # Infinity
        if pref[min(n, d)] >= c:
            print("Infinity")
            continue

        # Impossible
        if a[0] * d < c:
            print("Impossible")
            continue

        def can(k):
            cycle = k + 1

            take = min(cycle, n)
            cycle_sum = pref[take]

            full = d // cycle
            rem = d % cycle

            total = full * cycle_sum
            total += pref[min(rem, n)]

            return total >= c

        lo, hi = 0, d
        ans = 0

        while lo <= hi:
            mid = (lo + hi) // 2

            if can(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        print(ans)

solve()
```

## Complexity Analysis

| Measure | Complexity |
| --- | --- |
| Sorting | `O(n log n)` |
| Each feasibility check | `O(1)` |
| Binary search | `O(log d)` |
| Total per test case | `O(n log n + log d)` |
| Space | `O(n)` |

Since the sums of `n` and `d` over all test cases are both at most `2·10^5`, this easily fits within the limits.
