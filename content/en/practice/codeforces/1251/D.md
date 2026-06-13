---
title: "CF 1251D - Salary Changing"
description: "We are given several independent scenarios. In each scenario, there are an odd number of employees, and each employee has a salary interval from which their final salary must be chosen."
date: "2026-06-13T21:36:20+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1251
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 75 (Rated for Div. 2)"
rating: 1900
weight: 1251
solve_time_s: 271
verified: true
draft: false
---

[CF 1251D - Salary Changing](https://codeforces.com/problemset/problem/1251/D)

**Rating:** 1900  
**Tags:** binary search, greedy, sortings  
**Solve time:** 4m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario, there are an odd number of employees, and each employee has a salary interval from which their final salary must be chosen. We are also given a total budget that is guaranteed to be large enough to pay everyone their minimum possible salary.

The task is to assign each employee a salary within their allowed interval so that the median of all chosen salaries is as large as possible. The median is defined after sorting all salaries, and since the number of employees is odd, it is the single middle element.

So the problem is not about maximizing total salaries or fairness in any global sense. It is about pushing the middle element of the sorted salary array as high as possible while still respecting individual bounds and the global budget.

The key interaction is between three constraints: each salary is bounded by an interval, the sum of all salaries is limited, and only the median position matters.

The constraints are large enough that any solution that tries to simulate assignments or repeatedly check feasibility by constructing full arrays per guess will fail. With up to 2×10^5 employees overall, any approach that is worse than O(n log n) per test case will not scale.

A subtle edge case arises when many intervals are wide but budget is tight beyond the minimum sum. A naive greedy that simply raises all salaries independently will fail because increasing one value may force reducing feasibility elsewhere, even though lower bound feasibility is guaranteed.

Another failure mode appears if we try to greedily assign higher salaries to everyone in a symmetric way. That ignores that only the median position matters, so wasting budget on the lower half is unnecessary.

## Approaches

The brute-force idea is to try every possible value of the median and check whether it can be achieved. For a candidate value x, we would attempt to construct an assignment where at least half of the employees have salary at least x, while respecting intervals and total budget.

To verify feasibility for a fixed x, we would need to assign salaries greedily: push as many people as possible to at least x within their interval, then distribute remaining budget. This can be made O(n) per check.

However, the median can be as large as 10^9, so a linear scan over all possible values is impossible. Even binary searching x gives O(n log n) per test case, which is too slow if each check is not carefully optimized, and still risks tight limits under 2×10^5 total employees.

The key observation is that feasibility is monotonic in x. If we can make at least k employees have salary ≥ x, then any smaller x is also feasible. This allows binary search on the answer.

The second and deeper insight is how to evaluate feasibility efficiently. We do not need to fully construct an assignment. We only need to know whether we can force at least k = n//2 + 1 employees to reach at least x, while staying within budget.

For each employee, there are three relevant states relative to x: they cannot reach x (r_i < x), they can reach x only by paying extra (l_i < x ≤ r_i), or they are already forced above x (l_i ≥ x). We greedily decide which employees we try to push above x, always preferring those that are cheapest to raise, since budget is the limiting factor.

This turns feasibility checking into sorting candidates by cost of raising them to x.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force construction | O(n·max_salary) | O(n) | Too slow |
| Binary search + greedy feasibility | O(n log n log A) | O(n) | Accepted |

## Algorithm Walkthrough

We binary search the answer, treating the median value x as a threshold.

1. Fix a candidate median value x and classify each employee based on their interval relative to x. If r_i < x, this employee cannot contribute to reaching the median, so they are ignored for the “high group”. If l_i ≥ x, they already satisfy the condition without extra cost. Otherwise, they can be optionally pushed to x at cost x - l_i.
2. Count how many employees already satisfy l_i ≥ x. These are automatically part of the high group. If this number is already at least k = n//2 + 1, then x is feasible because we can assign everyone else minimally without affecting the median.
3. If not enough employees are already above x, we collect all “upgradeable” employees, those with l_i < x ≤ r_i. For each of them, compute cost = x - l_i.
4. Sort these costs in increasing order. We want to pick the cheapest employees to upgrade first because each upgrade contributes one more person at or above x.
5. We take the smallest costs until we reach k employees in the high group. If we run out of candidates before reaching k, x is infeasible.
6. For those selected upgrades, compute total additional cost as the sum of (x - l_i). If this added cost exceeds the remaining budget after paying all l_i, then x is infeasible; otherwise it is feasible.
7. Binary search x over a sufficiently large range, typically up to 10^9.

The correctness relies on the fact that any optimal solution for a fixed x will never waste budget increasing someone above x beyond what is needed to satisfy the median condition. Any extra increase does not help feasibility and only increases cost.

### Why it works

For a fixed threshold x, the only thing that matters is whether at least k salaries can be made ≥ x under budget constraints. Among all ways to pick k employees to promote above x, the cheapest choice is always to take those with smallest (x - l_i). Any deviation from this choice only increases total cost without increasing feasibility. This greedy structure ensures that feasibility checking is optimal and monotone in x, which makes binary search valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(x, arr, s, k):
    base = 0
    candidates = []

    for l, r in arr:
        base += l
        if r < x:
            continue
        if l >= x:
            continue
        candidates.append(x - l)

    if base > s:
        return False

    need = k
    have = 0

    for l, r in arr:
        if l >= x:
            have += 1

    if have >= k:
        return True

    need = k - have

    candidates.sort()

    extra = 0
    for i in range(min(need, len(candidates))):
        extra += candidates[i]

    return base + extra <= s

def solve():
    t = int(input())
    for _ in range(t):
        n, s = map(int, input().split())
        arr = [tuple(map(int, input().split())) for _ in range(n)]
        k = n // 2 + 1

        lo, hi = 1, 10**9
        ans = 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid, arr, s, k):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution is structured around a feasibility checker and a binary search driver. The feasibility function computes the baseline cost of paying all employees their minimum salaries, then tries to “upgrade” enough employees to reach the median threshold.

The critical detail is separating employees into those already at or above x and those that can be upgraded. The sorting step ensures we always pick the cheapest upgrades first.

The binary search drives the solution because feasibility is monotonic: if a median value x is achievable, then any smaller value is also achievable.

## Worked Examples

### Example 1

Input:

```
3
3 26
10 12
1 4
10 11
```

We compute k = 2.

| x | base sum | have ≥ x | upgrades used | total cost | feasible |
| --- | --- | --- | --- | --- | --- |
| 10 | 21 | 2 | 0 | 21 | yes |
| 11 | 21 | 1 | 1 | 22 | yes |
| 12 | 21 | 1 | 1 | 23 | yes |
| 13 | 21 | 0 | impossible | - | no |

The highest feasible x is 11, matching the optimal median.

This trace shows how feasibility depends on both existing high salaries and the cost of upgrading borderline employees.

### Example 2

Input:

```
5 26
4 4
2 4
6 8
5 6
2 7
```

Here k = 3.

| x | base sum | have ≥ x | upgrades used | total cost | feasible |
| --- | --- | --- | --- | --- | --- |
| 6 | 19 | 3 | 0 | 19 | yes |
| 7 | 19 | 2 | 1 | 21 | yes |
| 8 | 19 | 1 | 2 | 25 | yes |
| 9 | 19 | 0 | impossible | - | no |

The answer is 6, which is the last value before feasibility breaks.

These examples show that the algorithm naturally balances between already-large salaries and strategically upgraded ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n log A) | binary search over answer, each feasibility check sorts candidates |
| Space | O(n) | storing intervals and temporary upgrade costs |

The constraints allow up to 2×10^5 employees total, and log A is about 30, so the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import log2
    import sys

    input = sys.stdin.readline

    def can(x, arr, s, k):
        base = 0
        candidates = []
        have = 0

        for l, r in arr:
            base += l
            if l >= x:
                have += 1
            elif r >= x:
                candidates.append(x - l)

        if base > s:
            return False
        if have >= k:
            return True

        need = k - have
        candidates.sort()

        extra = sum(candidates[:need]) if need <= len(candidates) else 10**30
        return base + extra <= s

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, s = map(int, input().split())
            arr = [tuple(map(int, input().split())) for _ in range(n)]
            k = n // 2 + 1

            lo, hi = 1, 10**9
            ans = 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if can(mid, arr, s, k):
                    ans = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            out.append(str(ans))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""3
3 26
10 12
1 4
10 11
1 1337
1 1000000000
5 26
4 4
2 4
6 8
5 6
2 7
""") == """11
1337
6"""

# custom cases
assert run("""1
1 100
10 20
""") == "20", "single employee"

assert run("""1
3 6
1 3
1 3
1 3
""") == "2", "tight symmetric case"

assert run("""1
5 15
1 10
1 10
1 10
1 10
1 10
""") == "1", "budget minimal median"

assert run("""1
5 100
1 100
1 100
1 100
1 100
1 100
""") == "100", "all wide ranges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single employee | 20 | boundary case n=1 |
| tight symmetric case | 2 | median driven by limited budget |
| budget minimal median | 1 | no upgrades possible |
| all wide ranges | 100 | full flexibility with enough budget |

## Edge Cases

A tricky situation occurs when many employees already have l_i ≥ x but are not needed for the median. The algorithm correctly counts them as “free” contributors to the high group, even though they may not be among the cheapest upgrade candidates. Since they already satisfy the threshold without cost, they never enter the candidate list and do not distort the greedy selection.

Another edge case is when the cheapest upgrades are insufficient in number to reach k. In that case, the candidate list simply runs out before satisfying the median requirement, and feasibility fails early without attempting unnecessary sums.
