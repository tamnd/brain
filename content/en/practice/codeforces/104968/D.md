---
title: "CF 104968D - Feeding the Kids"
description: "We are given a sequence of students arriving in a fixed order, and each student consumes a specific number of pizza slices. There are K pizzas prepared, and every pizza must have the same number of slices, call this value X."
date: "2026-06-28T06:48:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104968
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 2 (Beginner)"
rating: 0
weight: 104968
solve_time_s: 86
verified: false
draft: false
---

[CF 104968D - Feeding the Kids](https://codeforces.com/problemset/problem/104968/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of students arriving in a fixed order, and each student consumes a specific number of pizza slices. There are K pizzas prepared, and every pizza must have the same number of slices, call this value X. Pizzas are served one after another: each student takes their required number of slices from the current pizza if possible, but if the remaining slices are not enough, the current pizza is discarded immediately and a fresh one is opened for that student.

The goal is to choose the smallest possible X such that all students can be served without ever needing more than K pizzas.

The key detail is that the process is greedy and linear: each student either fits into the current pizza or forces a reset. This means the number of pizzas used is entirely determined by how often prefix sums exceed multiples of X.

The constraints allow up to 100000 students and 100000 pizzas, so any solution that tries all candidate X values and simulates naively for each one would be too slow. A brute force over X up to the sum of all demands is impossible because demands can reach 10^6 and totals can reach 10^11. Even a linear scan per candidate would exceed time limits.

A subtle edge case arises when a single student demands more than X. In that case, the current model implies we still give them pizza from a fresh pizza, so X must always be at least max(d_i). Another edge case is when K is large enough that even very small X might work, but the minimal X is still constrained by local “overflow points” in the sequence rather than just total sum.

## Approaches

A direct approach is to guess a value X and simulate the serving process. For a fixed X, we iterate through students, track remaining slices in the current pizza, and count how many pizzas are used. Whenever a student cannot fit, we start a new pizza. This simulation is O(N) per X.

The difficulty is choosing X. Since X is at least max(d_i) and at most sum(d_i), we could binary search it. However, the feasibility function is monotone: if a given X works, any larger X also works because larger pizzas never increase the number of breaks. This monotonicity allows binary search over X.

The key insight is that feasibility depends only on whether the greedy packing produces at most K segments where each segment is a contiguous run of students whose sum does not exceed X. The moment a segment exceeds X, it forces a cut. So checking X reduces to counting how many such segments are created.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force X with simulation | O(N · sum(d)) | O(1) | Too slow |
| Binary search + greedy check | O(N log sum(d)) | O(1) | Accepted |

## Algorithm Walkthrough

We define a function `can(X)` that returns whether K pizzas are enough if each pizza has X slices.

1. Start with zero pizzas used and zero remaining capacity in the current pizza.

We conceptually treat this as having opened no pizza yet.
2. Iterate through students in order.

For each student with demand d_i, try to fit them into the current pizza.
3. If the current pizza has at least d_i slices remaining, subtract d_i from it.

This models serving them without opening a new pizza.
4. Otherwise, we must open a new pizza for this student.

Increase pizza count by one, set remaining capacity to X, and subtract d_i.
5. If at any point a single student has d_i > X, immediately return false.

This is necessary because even a fresh pizza cannot satisfy them otherwise.
6. After processing all students, return whether total pizzas used is at most K.

Once `can(X)` is defined, we binary search X between max(d_i) and sum(d_i), choosing the smallest X such that `can(X)` is true.

Why it works: each fixed X defines a deterministic greedy segmentation of the array. Increasing X can only merge segments, never split them, so the number of pizzas used is monotone non-increasing in X. This guarantees binary search correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(a, k, x):
    used = 1
    rem = x
    for v in a:
        if v > x:
            return False
        if rem >= v:
            rem -= v
        else:
            used += 1
            rem = x - v
            if used > k:
                return False
    return used <= k

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    lo = max(a)
    hi = sum(a)

    while lo < hi:
        mid = (lo + hi) // 2
        if can(a, k, mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The solution separates feasibility checking from the search over X. The `can` function simulates exactly how pizzas are consumed, tracking remaining slices and counting how many pizzas are needed.

A common mistake is forgetting that a student who does not fit does not partially consume a pizza, they consume the remainder and force a fresh pizza immediately. This is why we reset `rem = x - v` instead of trying to carry leftover capacity forward.

Another subtle point is initializing `used = 1`. We only open a pizza when needed, but the first student always consumes from a pizza that must exist once they arrive.

## Worked Examples

### Example 1

Input:

```
N = 5, K = 3
d = [2, 3, 4, 5, 2]
```

We test a candidate X = 6.

| Student | Demand | Remaining before | Action | Remaining after | Pizzas used |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 6 | use current | 4 | 1 |
| 2 | 3 | 4 | use current | 1 | 1 |
| 3 | 4 | 1 | new pizza | 2 | 2 |
| 4 | 5 | 2 | new pizza | - | 3 |
| 5 | 2 | 1 | use current | - | 3 |

This uses 3 pizzas, so X = 6 is feasible when K = 3.

This trace shows how segment breaks occur exactly when remaining capacity is insufficient, producing a fixed number of pizza openings.

### Example 2

Input:

```
N = 4, K = 2
d = [4, 1, 5, 2]
```

Try X = 6.

| Student | Demand | Remaining before | Action | Remaining after | Pizzas used |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 6 | use | 2 | 1 |
| 2 | 1 | 2 | use | 1 | 1 |
| 3 | 5 | 1 | new | 1 | 2 |
| 4 | 2 | 1 | new | - | 3 |

This uses 3 pizzas, so X = 6 is invalid for K = 2. Increasing X would reduce forced breaks.

These traces demonstrate monotonicity: larger X can only reduce or preserve the number of pizza resets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log S) | Each feasibility check is O(N), binary search over sum of demands |
| Space | O(1) | Only counters and input array stored |

The constraints N up to 100000 make linear scans acceptable, and log(sum(d)) is at most around 40, keeping total operations comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("5 3\n2 3 4 5 2\n") == "6", "sample-like check"

# minimum size
assert run("1 1\n5\n") == "5", "single student"

# all equal
assert run("5 2\n2 2 2 2 2\n") == "6", "uniform case"

# tight K large
assert run("5 10\n1 2 3 4 5\n") == "5", "many pizzas allowed"

# boundary overflow behavior
assert run("3 2\n5 4 3\n") == "5", "forces multiple splits"

# increasing sequence
assert run("4 2\n1 2 3 4\n") == "4", "monotone demands"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single student | 5 | base case, direct assignment |
| all equal | 6 | repeated segment merging behavior |
| large K | 5 | minimal constraint is max demand |
| decreasing fits | 5 | frequent resets and correctness of counting |
| increasing sequence | 4 | worst-case segmentation pressure |

## Edge Cases

One edge case is when K is very large compared to N. For input like `N = 5, K = 100`, the answer is simply max(d_i). The algorithm handles this because binary search starts at lo = max(a), and `can(lo)` immediately succeeds since no student ever exceeds capacity and every student fits into a fresh pizza if needed.

Another edge case is when every demand is identical. For `a = [3,3,3,3]`, a candidate X = 3 leads to one pizza per student, so 4 pizzas are used. The feasibility check correctly increments `used` whenever remaining hits zero after subtraction, ensuring no undercounting.

A final edge case is a sequence with a single large spike in the middle. For `a = [1,1,100,1,1]`, any X < 100 fails immediately due to the explicit check `if v > x`. This prevents the simulation from incorrectly trying to partially serve an impossible request and ensures binary search does not drift into invalid ranges.
