---
title: "CF 106494B - Rest Point"
description: "We are given several independent intervals, and from each interval we must pick a single value. After choosing one value per interval, we treat those values as magnitudes of vectors."
date: "2026-06-19T17:33:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106494
codeforces_index: "B"
codeforces_contest_name: "MEPhI Spring Cup 2026"
rating: 0
weight: 106494
solve_time_s: 51
verified: true
draft: false
---

[CF 106494B - Rest Point](https://codeforces.com/problemset/problem/106494/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent intervals, and from each interval we must pick a single value. After choosing one value per interval, we treat those values as magnitudes of vectors. The key question is whether we can assign directions to these vectors so that their vector sum becomes exactly zero.

The geometry behind the problem reduces everything to a single condition on numbers. If one chosen value is too large compared to the sum of all the others, then no matter how we orient directions, that largest vector cannot be fully canceled by the rest. If no such imbalance exists, then a valid orientation always exists in one dimension, because we can always continuously adjust directions to balance the system at some point.

Each interval contributes flexibility, but only within its bounds. The real decision is how to choose one value from each interval so that the multiset of chosen values can satisfy a balance condition.

The constraints imply we need an O(n) or O(n log n) solution per test case at worst. Any approach that tries to explore combinations of picks from intervals, even in a reduced form, immediately becomes exponential and unusable once n grows beyond a few dozen.

A subtle failure case appears when the largest interval is not fixed at its maximum endpoint. For example, consider intervals [5, 10], [1, 2], [1, 2]. A naive approach might assume choosing all maximums is always optimal, but that can inflate the largest value unnecessarily and incorrectly reject a feasible configuration. The correct reasoning must consider adjusting the largest interval downward while respecting feasibility.

Another edge case arises when multiple intervals tie for maximum lower bound or when reducing the largest element changes which interval becomes dominant. A careless implementation that fixes the maximum by r-value instead of l-value will fail here.

## Approaches

A brute-force interpretation would try all choices of one value per interval, and for each selection, check whether we can assign signs to make the sum zero. Checking a fixed selection reduces to verifying whether any element exceeds half of the total sum, which is linear. However, the number of selections is the product of interval lengths, which is exponential in n, making this impossible beyond very small inputs.

The key observation is that we do not actually need to enumerate choices. We only care about whether there exists a selection that avoids a “dominant element” exceeding the sum of all others. This turns the problem into constructing a valid multiset of chosen values.

We identify the interval with the largest lower bound, since this interval is the hardest to reduce. We tentatively fix a candidate value from it, and then try to ensure all other chosen values can support it without violating the balance condition.

If we pick a value x from the critical interval, then all other intervals contribute values at most their chosen bounds, and we want the total sum of the others to be at least x. This transforms the problem into checking whether x can be supported by the remaining intervals under their constraints. The greedy strategy is to maximize contributions from other intervals without exceeding x, since anything above x does not help further balance the condition.

This leads to a direct construction: pick the interval with maximum lower bound l_i as the anchor, set its value to l_i, and for every other interval choose min(r_j, l_i). This maximizes the contribution toward supporting the anchor while keeping consistency with interval bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We focus on constructing a feasible selection rather than searching.

### 1. Identify the critical interval

We find the interval with the largest left endpoint. This interval is the most restrictive because it forces any valid solution to potentially support at least that magnitude.

### 2. Tentatively fix its chosen value

We set the chosen value for this interval to its lower bound. We do not try larger values because increasing it only makes balancing harder.

### 3. Assign values to all other intervals greedily

For every other interval, we choose the maximum value that does not exceed the critical value. Concretely, we pick min(r_j, l_max). This ensures every interval contributes as much as possible toward supporting the critical value without breaking feasibility.

### 4. Check feasibility via sum comparison

We compute the total sum of all chosen values. If this sum is at least twice the chosen critical value, then the remaining values can counterbalance it, meaning a zero vector configuration is possible.

If the sum is smaller, no valid construction exists.

### Why it works

The correctness relies on transforming the vector cancellation condition into a single dominance constraint. A configuration is feasible if and only if no element exceeds the sum of all others after choosing values. By anchoring the largest lower bound interval and maximizing all other contributions up to that anchor, we construct the best possible supporting environment for that interval. If even this maximal support fails, any other choice would only reduce the support further, making feasibility impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    seg = [tuple(map(int, input().split())) for _ in range(n)]

    # find interval with maximum left endpoint
    i_max = 0
    for i in range(1, n):
        if seg[i][0] > seg[i_max][0]:
            i_max = i

    x = seg[i_max][0]

    total = 0
    for i, (l, r) in enumerate(seg):
        if i == i_max:
            total += x
        else:
            if r < x:
                total += r
            else:
                total += x

    # feasibility condition
    print("YES" if total >= 2 * x else "NO")

if __name__ == "__main__":
    solve()
```

The code first identifies the interval with the largest lower bound, since that determines the hardest constraint to satisfy. It then fixes its chosen value to that lower bound. For every other interval, it contributes as much as possible toward supporting this anchor, but never exceeding it.

The final check compares total contribution against twice the anchor, which encodes whether the remaining vectors can fully counterbalance it.

A subtle point is that we never explicitly compute “sum of others” separately; instead we include the anchor in the total and compare against 2x. This avoids off-by-one mistakes and keeps the implementation linear.

## Worked Examples

### Example 1

Consider intervals:

[3, 5], [1, 2], [2, 4]

The maximum left endpoint is 3, so x = 3.

| Interval | Chosen value | Contribution |
| --- | --- | --- |
| [3,5] | 3 | 3 |
| [1,2] | 2 | 2 |
| [2,4] | 3 | 3 |

Total = 8, and 2x = 6, so condition holds.

This shows that even though some intervals cannot reach 3, their maximum contribution still suffices to balance the anchor.

### Example 2

Consider intervals:

[10, 10], [1, 2], [1, 2]

Here x = 10.

| Interval | Chosen value | Contribution |
| --- | --- | --- |
| [10,10] | 10 | 10 |
| [1,2] | 2 | 2 |
| [1,2] | 2 | 2 |

Total = 14, and 2x = 20, so condition fails.

This demonstrates the failure mode where one interval is too large relative to all others, even under maximal support.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass to find max left endpoint and single pass to compute sum |
| Space | O(1) | only constant extra variables besides input storage |

The solution fits easily within limits since each test case requires only linear scanning over intervals.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio

    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n = int(input())
    seg = [tuple(map(int, input().split())) for _ in range(n)]

    i_max = 0
    for i in range(1, n):
        if seg[i][0] > seg[i_max][0]:
            i_max = i

    x = seg[i_max][0]

    total = 0
    for i, (l, r) in enumerate(seg):
        total += x if (i == i_max and l <= x <= r) else min(r, x)

    print("YES" if total >= 2 * x else "NO")

# sample-like cases
assert run("3\n3 5\n1 2\n2 4\n") == "YES"
assert run("3\n10 10\n1 2\n1 2\n") == "NO"

# minimum case
assert run("1\n0 5\n") == "YES"

# tight boundary case
assert run("2\n5 5\n5 5\n") == "YES"

# impossible spread
assert run("2\n10 10\n1 1\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 intervals mixed | YES | standard feasibility case |
| dominant large interval | NO | impossibility detection |
| single interval | YES | trivial balance case |
| equal tight intervals | YES | boundary equality handling |
| extreme imbalance | NO | worst-case rejection |

## Edge Cases

A single interval case is the simplest. For input [0, 5], the algorithm selects x = 0 and immediately satisfies the condition since there are no other constraints. The computed total equals zero and 2x is also zero, so the answer is YES.

A tightly constrained equal-interval case such as [5,5], [5,5] sets x = 5. Both intervals contribute 5, giving total 10 which equals 2x, producing YES. This confirms equality handling is correct and no strict inequality is required.

A strongly imbalanced case like [10,10], [1,1] sets x = 10. The second interval contributes only 1, making total 11 which is far below 20, so the algorithm correctly rejects it. This shows that even if smaller intervals are maximized, they cannot compensate for an overly large anchor interval.
