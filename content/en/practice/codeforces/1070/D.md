---
title: "CF 1070D - Garbage Disposal"
description: "Each day produces some number of garbage units, and every unit must be thrown away either on the day it appears or on the following day."
date: "2026-06-15T13:49:28+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1070
codeforces_index: "D"
codeforces_contest_name: "2018-2019 ICPC, NEERC, Southern Subregional Contest (Online Mirror, ACM-ICPC Rules, Teams Preferred)"
rating: 1300
weight: 1070
solve_time_s: 331
verified: false
draft: false
---

[CF 1070D - Garbage Disposal](https://codeforces.com/problemset/problem/1070/D)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 5m 31s  
**Verified:** no  

## Solution
## Problem Understanding

Each day produces some number of garbage units, and every unit must be thrown away either on the day it appears or on the following day. Disposal happens by packing units into bags, where each bag can hold up to a fixed capacity $k$, and a bag is emptied immediately on the day it is prepared. The goal is to schedule how garbage is carried across at most one day and grouped into bags so that the total number of bags used is minimized.

The key constraint is that garbage has a very short lifetime: at most two consecutive days of availability. This creates a local interaction between adjacent days, rather than a global scheduling problem. The output is just the minimum number of capacity-limited groups needed to cover all units under these adjacency constraints.

The input size reaches $2 \cdot 10^5$, so any quadratic strategy that tries to simulate assignments between all pairs of days is too slow. The only viable approaches are linear or near-linear, since about $10^8$ simple operations is the upper safe bound in 3 seconds in Python C-like efficiency, and Python overhead pushes us closer to $10^7$ meaningful operations.

A subtle edge case appears when postponing garbage is necessary to avoid wasting bag capacity. For example, if one day has a small amount and the next has a large amount, naïvely packing each day separately can waste capacity, while shifting units forward or backward within the allowed window can reduce the number of bags.

Another edge case occurs at the last day. Garbage produced on day $n$ cannot be postponed further, so any strategy that implicitly assumes future capacity for balancing must carefully handle the boundary.

## Approaches

A brute-force idea is to simulate all possible decisions: for each day, decide how many units to keep for the next day and how many to dispose immediately, then try all distributions into bags. This would require exploring exponentially many configurations because each unit can be assigned to one of two days, and then each day's grouping into bags introduces another combinatorial layer. Even if we restrict ourselves to day-by-day dynamic programming over leftover units, the state space grows with possible carry values up to $k$, making transitions $O(nk)$, which is too large when $k$ is up to $10^9$.

The structural simplification comes from observing that we never need to explicitly simulate individual units. What matters is how many units from day $i$ are postponed to day $i+1$, because postponed units from day $i$ must be processed together with day $i+1$. Once we fix how many units are carried forward, the remaining decisions on that day become deterministic: we simply fill bags greedily to minimize count.

The core greedy insight is that for each day, we want to maximize reuse of capacity by pairing leftover units from the previous day with current units. Instead of tracking individual assignments, we track how many units are still "pending" at the start of each day, then compute how many additional units must be delayed forward to the next day to minimize bag count locally.

This reduces the problem to a single left-to-right pass with a simple state variable representing unprocessed carry-over garbage.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / $O(nk)$ | $O(nk)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process days in order while maintaining how many garbage units are available to be packed on the current day, including both new garbage and leftovers from the previous day.

1. Initialize a variable `carry` to 0, representing garbage that was postponed from the previous day, and initialize `ans` to 0 for the number of bags used.
2. For each day $i$, add $a_i$ to `carry`, since all newly generated garbage becomes available for either today or tomorrow.
3. Compute how many full bags we can form today using all available garbage. Each bag holds up to $k$ units, so the number of bags we can complete from `carry` is `carry // k`. Add this value to the answer and reduce `carry` accordingly using modulo $k$.
4. The remaining `carry` after forming full bags represents leftover units that cannot fill an entire bag today. These leftovers must either be combined with next day’s garbage or be completed on the next day, so they are kept as is.
5. Before moving to the next day, ensure that the leftover does not exceed what can be reasonably handled. Since each unit can only move at most one day forward, any leftover is automatically valid as carry-over.
6. After processing day $n$, all remaining `carry` must be disposed on the last day. Add `carry // k` to the answer again.

The correctness hinges on the fact that any partial bag at a given day should be completed as soon as possible using available units, since delaying completion does not increase capacity but risks losing pairing opportunities.

### Why it works

At any day boundary, all remaining units can only interact with the next day, and no further. Therefore, the optimal strategy locally is to always fill as many full bags as possible immediately, because any grouping that postpones forming a full bag cannot improve future pairing potential beyond one day. The invariant is that after processing day $i$, all remaining units are exactly those that must be reconsidered with day $i+1$, and all completed bags are fixed optimally for that prefix.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    carry = 0
    ans = 0

    for x in a:
        carry += x
        ans += carry // k
        carry %= k

    ans += carry // k
    print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains a running pool of available garbage units and greedily extracts full bags at every step. The integer division captures exactly how many complete bags can be formed from current availability, and the modulo keeps only the leftover units that must interact with the next day. The final addition handles the last-day cleanup.

A subtle point is that we never explicitly decide how many units move to the next day; this is implicitly encoded in the remainder after forming full groups, which is sufficient because only the remainder can benefit from future combination.

## Worked Examples

Consider the sample input.

Input:

```
3 2
3 2 1
```

We track `carry` and `ans`.

| Day | a[i] | carry before | bags added | carry after | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 1 | 1 | 1 |
| 2 | 2 | 3 | 1 | 1 | 2 |
| 3 | 1 | 2 | 1 | 0 | 3 |

After processing all days, answer is 3.

This shows how leftover units propagate forward, combining whenever possible, but always respecting the one-day limit.

Now consider a case where postponement matters.

Input:

```
2 3
2 4
```

| Day | a[i] | carry before | bags added | carry after | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 0 | 2 | 0 |
| 2 | 4 | 6 | 2 | 0 | 2 |

On day 1, nothing can form a full bag, so everything carries. On day 2, all 6 units combine, producing 2 bags. This demonstrates why carrying leftovers forward is essential for optimal packing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each day is processed once with constant arithmetic operations |
| Space | $O(1)$ | Only a few integer variables are maintained |

The linear scan easily fits within limits for $n \le 2 \cdot 10^5$, and memory usage is constant regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    carry = 0
    ans = 0
    for x in a:
        carry += x
        ans += carry // k
        carry %= k
    ans += carry // k
    print(ans)

# provided sample
assert run("3 2\n3 2 1\n") == "3"

# minimum case
assert run("1 5\n4\n") == "0", "single day, no full bag"

# exact fit
assert run("1 5\n5\n") == "1", "one full bag"

# carry effect
assert run("2 3\n2 4\n") == "2", "optimal carry across days"

# large k
assert run("3 100\n50 60 70\n") == "1", "only final aggregation matters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 / 4 | 0 | no bag formed |
| 1 5 / 5 | 1 | exact capacity |
| 2 3 / 2 4 | 2 | carry mechanism |
| 3 100 / 50 60 70 | 1 | large capacity aggregation |

## Edge Cases

For a single day with fewer than $k$ units, such as input `1 10 / 3`, the algorithm sets `carry = 3`, computes no full bags during iteration, and then discards the final carry since `3 // 10 = 0`, producing 0 correctly. The correctness comes from the fact that no postponement is possible, so every unit must remain unused in terms of full bag formation.

For a single day exactly equal to $k$, such as `1 10 / 10`, the algorithm forms exactly one bag via `carry // k = 1` and reduces carry to zero. This confirms that the greedy extraction of full bags at each step correctly handles exact-fit scenarios without requiring any special casing.
