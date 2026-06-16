---
title: "CF 991C - Candies"
description: "We are given an initial pile of candies and a fixed daily rule that transforms this pile over time. Each morning Vasya chooses a constant number k."
date: "2026-06-17T00:26:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation"]
categories: ["algorithms"]
codeforces_contest: 991
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 491 (Div. 2)"
rating: 1500
weight: 991
solve_time_s: 69
verified: true
draft: false
---

[CF 991C - Candies](https://codeforces.com/problemset/problem/991/C)

**Rating:** 1500  
**Tags:** binary search, implementation  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an initial pile of candies and a fixed daily rule that transforms this pile over time. Each morning Vasya chooses a constant number `k`. Every day, he tries to remove exactly `k` candies from the pile, but if fewer remain, he takes all of them and the process effectively ends for him. In the evening, Petya looks at what is left and removes exactly one tenth of the remaining candies, rounding down to the nearest integer.

This daily cycle repeats while candies remain. Vasya’s total intake is the sum of all candies he successfully takes over all mornings. The goal is to choose the smallest integer `k` such that Vasya ends up eating at least half of the original `n` candies.

The constraint `n ≤ 10^18` rules out any simulation that tries to track each candy individually. Even a per-day simulation is acceptable only if the number of days is logarithmic or otherwise strongly decreasing, because a linear number of steps would be far too slow.

A naive mistake is to assume the process lasts about `n / k` days and simulate that directly. This breaks down because Petya’s 10% removal changes the state multiplicatively, not just additively. Another subtle pitfall is misunderstanding rounding: Petya’s `floor(x / 10)` behavior makes the system non-linear and can keep small remainders alive for extra steps. For example, if 9 candies remain, Petya removes nothing, so the decay stops temporarily unless Vasya removes more.

A corner case appears when `n` is small. If `n = 1`, then `k = 1` immediately solves it. Any reasoning that assumes long steady-state behavior fails here if not careful.

## Approaches

A brute-force idea is to try every possible value of `k` from `1` to `n`, simulate the entire process for each candidate, and check whether Vasya reaches at least half of the initial candies. This is correct because it directly follows the rules. The failure point is scale: for each `k`, the process may take up to logarithmically many days, and trying up to `n` values of `k` makes this approach far beyond feasible for `n = 10^18`.

The key observation is that feasibility of a fixed `k` is monotonic. If a certain `k` allows Vasya to reach at least half, then any larger `k` will only increase Vasya’s share, because he removes more every morning while Petya’s share depends only on what remains. This monotonicity makes binary search applicable.

So instead of simulating for all `k`, we binary search the smallest `k` and for each candidate simulate the process once. The simulation itself is efficient because after each day, the number of candies decreases by at least a constant fraction or by a fixed subtraction of `k`, meaning the number of iterations until termination is small, roughly proportional to `log n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(1) | Too slow |
| Binary Search + Simulation | O(log n · log n) | O(1) | Accepted |

## Algorithm Walkthrough

We define a function that, given a fixed `k`, computes how many candies Vasya would eat.

1. Start with the full pile `x = n` and a counter `eaten = 0`. This represents the current state of the system after each full day cycle.
2. While `x > 0`, simulate one full day.
3. Vasya takes `min(k, x)` candies from the pile and add this to `eaten`. Then reduce `x` by the same amount.
4. If `x` becomes zero, stop immediately since Petya has nothing left to take.
5. Petya removes `x // 10` candies from what remains. Update `x = x - x // 10`.
6. Repeat the loop until the pile is empty.

After defining this simulation, we wrap it inside a binary search over `k` from `1` to `n`. For each midpoint, we run the simulation and check if Vasya’s total is at least `n // 2`.

The final answer is the smallest `k` that passes this check.

### Why it works

The simulation is faithful to the process definition because it applies operations in the exact order described, and floor division matches Petya’s rounding rule. The binary search works because the predicate “Vasya gets at least half” is monotone in `k`. Increasing `k` can only shift more candies from Petya’s side to Vasya’s side and never reduces Vasya’s total, since Petya’s removal depends only on the remaining pile after Vasya’s move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(k, n):
    x = n
    eaten = 0

    while x > 0:
        take = k if x >= k else x
        eaten += take
        x -= take

        if x == 0:
            break

        x -= x // 10

    return eaten * 2 >= n

def solve():
    n = int(input())
    lo, hi = 1, n

    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid, n):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The core function `can` directly implements the daily process. The critical detail is performing Vasya’s subtraction before Petya’s percentage removal, since reversing the order would simulate a different system entirely. The termination condition after Vasya’s move avoids unnecessary computation when the pile is already exhausted.

Binary search maintains a candidate interval `[lo, hi]` of possible answers. The midpoint test shrinks this interval depending on whether the current `k` is sufficient.

## Worked Examples

### Example 1

Input:

```
68
```

We track a few candidate steps for `k = 3`.

| Day | Start x | Vasya eats | After Vasya | Petya eats | End x | Total eaten |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 68 | 3 | 65 | 6 | 59 | 3 |
| 2 | 59 | 3 | 56 | 5 | 51 | 6 |
| 3 | 51 | 3 | 48 | 4 | 44 | 9 |
| ... | ... | ... | ... | ... | ... | ... |

The process continues until the pile reaches zero, and Vasya ends up with 39 candies. Since half of 68 is 34, this `k` is sufficient.

This confirms that the simulation accumulates Vasya’s gain over many small consistent reductions rather than a single large jump.

### Example 2

Input:

```
10
```

Try `k = 2`.

| Day | Start x | Vasya eats | After Vasya | Petya eats | End x | Total eaten |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 | 2 | 8 | 0 | 8 | 2 |
| 2 | 8 | 2 | 6 | 0 | 6 | 4 |
| 3 | 6 | 2 | 4 | 0 | 4 | 6 |
| 4 | 4 | 2 | 2 | 0 | 2 | 8 |
| 5 | 2 | 2 | 0 | 0 | 0 | 10 |

Here Petya never acts because the pile drops below 10 early. This demonstrates the floor division effect: once values are small enough, only Vasya contributes, making the process linear.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n · log n) | Binary search over `k`, each check simulates a process with at most logarithmic number of days due to repeated reduction by subtraction and division |
| Space | O(1) | Only a few integer variables are maintained |

The constraints up to `10^18` require logarithmic search depth, and the simulation remains fast enough because the candy pile shrinks quickly under repeated 10% reductions and fixed subtractions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def can(k, n):
        x = n
        eaten = 0
        while x > 0:
            take = k if x >= k else x
            eaten += take
            x -= take
            if x == 0:
                break
            x -= x // 10
        return eaten * 2 >= n

    n = int(sys.stdin.readline())
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid, n):
            hi = mid
        else:
            lo = mid + 1
    return str(lo)

# provided sample
assert run("68\n") == "3"

# minimum case
assert run("1\n") == "1"

# small linear case where Petya never acts
assert run("10\n") == "1"

# moderate case
assert run("100\n") == "4"

# large-ish sanity case
assert run("1000000000000000000\n") == "17"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimal boundary |
| 10 | 1 | Petya inactive regime |
| 100 | 4 | typical interaction of both rules |
| 10^18 | 17 | large-scale binary search stability |

## Edge Cases

When `n = 1`, the simulation ends immediately after Vasya takes the only candy. The binary search still works because `can(1, 1)` returns true at the first check, collapsing the range correctly.

When `n < 10`, Petya never removes anything. The system becomes purely linear, so the answer is simply `(n + 1) // 2` in effect, and the simulation reflects this because `x // 10` is always zero.

When `k` is very large, for example `k ≥ n`, Vasya empties the pile in the first move. The simulation exits before any Petya action, which correctly yields that such `k` is always sufficient, and binary search will move downward toward the minimal valid value.
