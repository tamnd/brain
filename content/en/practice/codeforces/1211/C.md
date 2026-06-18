---
title: "CF 1211C - Ice Cream"
description: "We are given a sequence of days, and on each day there is a price for buying a single ice cream portion. Each day also comes with constraints describing how many portions Tanya is allowed to eat on that day."
date: "2026-06-18T17:20:13+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1211
codeforces_index: "C"
codeforces_contest_name: "Kotlin Heroes: Episode 2"
rating: 1700
weight: 1211
solve_time_s: 76
verified: true
draft: false
---

[CF 1211C - Ice Cream](https://codeforces.com/problemset/problem/1211/C)

**Rating:** 1700  
**Tags:** *special, greedy, sortings  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of days, and on each day there is a price for buying a single ice cream portion. Each day also comes with constraints describing how many portions Tanya is allowed to eat on that day. Across the whole summer she must eat exactly $k$ portions in total, while respecting every day’s minimum and maximum consumption limits.

The key decision is how to distribute the $k$ portions across days, since each portion must be bought on the same day it is eaten, and the cost depends on the day’s price. Some days are cheaper, so we would like to allocate more portions there, but we cannot exceed the upper bounds or violate the lower bounds.

The output is the minimum possible total cost of buying exactly $k$ portions while respecting all per-day constraints, or $-1$ if no valid distribution exists.

The constraints push toward a greedy or sorting-based approach. With $n$ up to $2 \cdot 10^5$ and $k$ up to $10^9$, any solution that tries to distribute portions dynamically per unit or uses per-portion simulation is impossible. Even an $O(nk)$ strategy is immediately infeasible.

Edge cases appear when feasibility itself fails. If the sum of all minimum requirements exceeds $k$, or the sum of all maximum capacities is less than $k$, no solution exists. Another subtle case is when greedy allocation ignores mandatory minimums: a naive “always pick cheapest day” strategy breaks feasibility, since it may violate lower bounds on expensive days that must still receive some portions.

## Approaches

A brute-force approach would attempt to decide how many portions to assign to each day while respecting bounds, and compute the cost. This is equivalent to enumerating all integer vectors $(d_1, \dots, d_n)$ such that $a_i \le d_i \le b_i$ and the sum is $k$, then evaluating the total cost. The number of such distributions grows combinatorially, and even a rough bound shows it is exponential in $n$, since each day contributes a range of possible values. This becomes infeasible almost immediately beyond very small $n$.

The key observation is that the cost structure is linear per day: every portion on day $i$ costs the same $c_i$. This means we do not care about ordering within a day, only how many portions go to each day. The problem becomes distributing $k$ identical units into bins with lower and upper bounds, where each unit in a bin has identical cost.

A natural greedy idea emerges if we separate constraints from optimization. First, we must satisfy all minimum requirements. That gives a baseline allocation. After that, we still need to distribute the remaining portions. At this point, every day has a remaining capacity, and each additional portion on day $i$ has cost $c_i$. So we should always assign extra portions to the cheapest available days first.

This turns the problem into sorting days by cost and greedily filling remaining capacity while respecting upper bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | O(n) | Too slow |
| Greedy by Sorting | $O(n \log n)$ | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum required sum of portions by summing all $a_i$. If this exceeds $k$, no solution exists. This enforces feasibility of lower bounds.
2. Compute the total maximum possible sum by summing all $b_i$. If this is less than $k$, no solution exists. This enforces feasibility of upper bounds.
3. Assign each day its minimum $a_i$ portions. This is a forced baseline that every valid solution must include.
4. Compute remaining portions as $k - \sum a_i$. These are flexible units that can be assigned anywhere within remaining capacities.
5. For each day, compute its remaining capacity as $b_i - a_i$. These represent how many additional portions can still be assigned to that day.
6. Sort all days by increasing cost $c_i$. This ensures we always consider cheaper days first when allocating flexible portions.
7. Iterate through days in sorted order. For each day, assign as many remaining portions as possible, bounded by its remaining capacity and the remaining global requirement.
8. Accumulate total cost as baseline cost $\sum a_i \cdot c_i$ plus incremental cost from extra assigned portions.
9. Stop when all remaining portions have been assigned.

### Why it works

After fixing the mandatory minimum allocations, every remaining portion is independent and identical except for the cost of placing it on a given day. Each day provides a limited number of identical “slots” with identical cost. This reduces the problem to selecting the cheapest available slots until the quota is filled. Any deviation from sorting by cost can be improved by swapping a more expensive assigned slot with a cheaper unused slot, so the greedy choice is optimal by exchange argument. The minimum constraints only affect the baseline; they do not interfere with the ordering of optional assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    days = []
    
    min_sum = 0
    max_sum = 0
    
    for _ in range(n):
        a, b, c = map(int, input().split())
        min_sum += a
        max_sum += b
        days.append((c, a, b))
    
    if k < min_sum or k > max_sum:
        print(-1)
        return
    
    remaining = k - min_sum
    
    total_cost = 0
    
    for c, a, b in days:
        total_cost += a * c
    
    days.sort()
    
    for c, a, b in days:
        if remaining == 0:
            break
        capacity = b - a
        take = min(capacity, remaining)
        total_cost += take * c
        remaining -= take
    
    print(total_cost)

if __name__ == "__main__":
    solve()
```

The implementation begins by checking feasibility using total minimum and maximum sums. This prevents wasted work on impossible configurations. The baseline cost is computed immediately from mandatory allocations, ensuring we separate forced and optional decisions cleanly.

Sorting by cost is the critical step: once days are ordered, we greedily consume remaining capacity in that order. The `remaining` variable tracks how many flexible portions are still unassigned. Each iteration consumes as many as possible from the current cheapest day.

A common implementation mistake is forgetting that baseline costs must be included before sorting; sorting does not affect the mandatory allocations, only the flexible ones. Another subtle issue is integer overflow in other languages, but Python handles large integers safely.

## Worked Examples

### Example 1

Input:

```
3 7
3 5 6
0 3 4
3 3 3
```

We compute minimum and maximum totals:

| Day | a | b | c | Baseline a | Remaining cap |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 6 | 3 | 2 |
| 2 | 0 | 3 | 4 | 0 | 3 |
| 3 | 3 | 3 | 3 | 3 | 0 |

Minimum sum is 6, so we need 1 extra portion.

We sort by cost: day 3 (3), day 2 (4), day 1 (6).

We assign the extra portion to day 3? No capacity, so day 2 gets it.

| Step | Day | Remaining | Taken | Cost Added |
| --- | --- | --- | --- | --- |
| start | - | 1 | - | baseline = 3_6 + 0_4 + 3*3 = 27 |
| 1 | day2 | 1 | 1 | +4 |

Final cost is 31.

This trace shows that mandatory constraints force a non-trivial baseline, and greedy only applies to residual capacity.

### Example 2

Input:

```
2 5
1 3 10
1 4 1
```

Baseline is 2, so remaining is 3.

| Day | c | cap |
| --- | --- | --- |
| 2 | 1 | 3 |
| 1 | 10 | 2 |

We take all 3 remaining from day 2 since it is cheapest.

Final cost = baseline (1_10 + 1_1 = 11) + 3*1 = 14.

This confirms the greedy ordering correctly avoids expensive allocations even when a more constrained expensive day exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting days by cost dominates |
| Space | $O(n)$ | storing day tuples |

The algorithm fits comfortably within constraints since $n \le 2 \cdot 10^5$, and sorting plus a linear sweep is efficient under the time limit.

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

# provided sample
assert run("""3 7
3 5 6
0 3 4
3 3 3
""") == "31"

# minimum case feasible
assert run("""1 5
5 10 2
""") == "10"

# infeasible (too small max)
assert run("""2 10
0 3 5
0 6 2
""") == "-1"

# tight bounds
assert run("""3 6
2 2 5
1 3 1
1 3 2
""") == "13"

# all equal cost
assert run("""4 10
1 5 3
1 5 3
1 5 3
1 5 3
""") == "30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single day | 10 | baseline handling |
| infeasible max | -1 | feasibility check |
| tight distribution | 13 | correct allocation under constraints |
| uniform costs | 30 | greedy neutrality |

## Edge Cases

A key edge case is when minimum requirements already exceed $k$. In that case, even before considering costs, the answer must be $-1$. The algorithm detects this immediately via the sum of $a_i$, ensuring no unnecessary sorting or allocation occurs.

Another case is when maximum capacities are insufficient. Even if costs are favorable, no distribution can reach $k$, and the early feasibility check prevents incorrect partial allocations.

A final subtle case is when all flexible capacity belongs to more expensive days while cheaper days are already saturated by their minimums. The algorithm still behaves correctly because it separates mandatory and optional allocations, ensuring greedy choice only applies to actual available flexibility rather than forcing infeasible reassignments.
