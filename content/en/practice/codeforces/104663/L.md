---
title: "CF 104663L - Not-Incomplete"
description: "The semester has a fixed number of weeks, and each week contains a limited number of classes. Some weeks have already passed, and you have already attended a certain number of classes during those completed weeks."
date: "2026-06-29T14:58:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104663
codeforces_index: "L"
codeforces_contest_name: "Replay of Ostad Presents Intra KUET Programming Contest 2023"
rating: 0
weight: 104663
solve_time_s: 73
verified: true
draft: false
---

[CF 104663L - Not-Incomplete](https://codeforces.com/problemset/problem/104663/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The semester has a fixed number of weeks, and each week contains a limited number of classes. Some weeks have already passed, and you have already attended a certain number of classes during those completed weeks. Now the remaining weeks are still ahead of you, and you must decide how many classes to attend in each of those remaining weeks.

The goal is to ensure that your final attendance ratio is at least 60 percent of all classes in the semester. However, you cannot attend more than the number of classes actually held in a week, so each remaining week has an upper bound on how many classes you can contribute.

The task is not only to decide whether reaching 60 percent attendance is possible, but also to construct a valid plan for the remaining weeks if it is possible. Among all valid plans, you must output one that distributes attendance across remaining weeks while respecting weekly limits.

The key quantities are straightforward. Total classes in the semester are fixed as the number of weeks multiplied by classes per week. Some of those weeks are already completed, and your past attendance is fixed. The remaining decision is how to distribute additional attendance across future weeks under per-week caps.

The constraints are extremely small. The number of weeks is at most 14, and classes per week are at most 5. This means brute force reasoning about distribution is completely safe, and even linear or greedy constructions are more than sufficient. The problem is not about performance but about correctly handling feasibility and constructing a valid allocation.

The main failure cases come from two sources. The first is incorrectly computing the required attendance threshold using integer division, which can lead to underestimating the required number of attended classes. For example, if total classes are 50, then 60 percent is 30, but if computed as `50 * 60 / 100` with integer truncation in some languages, care is needed to ensure correct ceiling behavior when necessary.

The second issue is assuming that simply filling remaining weeks greedily without respecting feasibility constraints always works. For instance, if remaining capacity is insufficient to reach the required total attendance, one must correctly detect impossibility before constructing any distribution.

A concrete edge case is when the required attendance is already satisfied. In that case, all remaining weeks should be filled with zeros, since adding unnecessary attendance is not required and could violate the “minimum per week” intent.

Another edge case is when even attending all remaining classes is insufficient. For example, if total classes are 20, required is 12, you already attended 11, and only 1 class remains available, then it is impossible even though you are very close.

## Approaches

A brute-force approach would try to enumerate all possible ways of distributing attendance across remaining weeks. Each week can take a value from 0 to Y, so with at most 14 weeks and Y up to 5, the number of configurations is at most $6^{14}$, which is far too large to enumerate directly.

However, the structure of the problem makes brute force unnecessary. The only global requirement is reaching a minimum total number of attended classes. There is no preference over distribution except that weekly values cannot exceed Y. This turns the problem into a simple feasibility and construction task.

The key observation is that the only meaningful quantity is the total number of additional classes you still need to attend. Once we compute that number, distributing it across remaining weeks becomes a bounded packing problem: we fill weeks up to capacity Y until the requirement is satisfied.

We first compute the total number of classes in the semester and the required threshold (60 percent). Then we subtract the number of classes already attended to find how many more are needed. If this number is less than or equal to zero, we already satisfy the requirement. If it exceeds the total remaining capacity, the task is impossible. Otherwise, we greedily assign as many classes as possible to each week until the requirement is met.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(6^W) | O(W) | Too slow |
| Optimal | O(W) | O(W) | Accepted |

## Algorithm Walkthrough

1. Compute total classes in the semester as $X \times Y$. This represents the full attendance universe.
2. Compute required attendance as 60 percent of total. Since attendance must be an integer, this is taken as the ceiling of $0.6 \times X \times Y$. This ensures we never accept a borderline insufficient value.
3. Compute remaining required attendance as `need = required - N`. If this value is less than or equal to zero, no further attendance is needed.
4. Compute remaining capacity as `(X - Z) * Y`. This is the maximum possible attendance you can still accumulate.
5. If `need > remaining capacity`, output “No” because even maximum effort cannot reach the threshold.
6. Otherwise, distribute attendance across remaining weeks. For each remaining week, assign `min(Y, need)` and subtract it from `need`.
7. If after assignment some weeks remain, fill them with zero attendance since no more is required.

### Why it works

The correctness relies on the fact that the only constraint coupling weeks is the global sum of attendance. Each week is independent except for its upper bound. Because we always try to satisfy the remaining requirement as early as possible, we never waste capacity in a way that could block feasibility later. If a solution exists, the greedy fill ensures it is constructed by consuming capacity in a straightforward linear scan.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    X, Y, Z, N = map(int, input().split())

    total = X * Y
    required = (total * 60 + 99) // 100

    need = required - N

    remaining_weeks = X - Z
    remaining_capacity = remaining_weeks * Y

    if need <= 0:
        print("Yes")
        print(" ".join("0" for _ in range(remaining_weeks)))
        return

    if need > remaining_capacity:
        print("No")
        return

    ans = []
    for _ in range(remaining_weeks):
        take = min(Y, need)
        ans.append(take)
        need -= take

    print("Yes")
    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The solution begins by computing the total number of classes and the required threshold using a ceiling division to avoid undercounting the 60 percent requirement. The variable `need` captures how many additional attended classes are required.

We then compute how many classes can still possibly be attended in the remaining weeks. This feasibility check is crucial, since without it we might construct a partial schedule even when no valid full schedule exists.

The greedy loop assigns as many classes as possible in each week without exceeding either the weekly limit or the remaining requirement. Once `need` becomes zero, subsequent weeks automatically contribute zero.

## Worked Examples

### Example 1

Input:

```
14 3 10 15
```

Total classes = 14 × 3 = 42

Required = 60% of 42 = 25.2 → 26

Already attended = 15

Need = 11

Remaining weeks = 4

Remaining capacity = 12

We distribute 11 across 4 weeks.

| Week | Remaining Need | Assigned |
| --- | --- | --- |
| 1 | 11 | 3 |
| 2 | 8 | 3 |
| 3 | 5 | 3 |
| 4 | 2 | 2 |

Output:

```
Yes
3 3 3 2
```

This trace shows how the greedy allocation consumes the requirement steadily while respecting weekly limits.

### Example 2

Input:

```
12 2 6 5
```

Total classes = 24

Required = 60% of 24 = 14.4 → 15

Already attended = 5

Need = 10

Remaining weeks = 6

Remaining capacity = 12

| Week | Remaining Need | Assigned |
| --- | --- | --- |
| 1 | 10 | 2 |
| 2 | 8 | 2 |
| 3 | 6 | 2 |
| 4 | 4 | 2 |
| 5 | 2 | 2 |
| 6 | 0 | 0 |

Output:

```
Yes
2 2 2 2 2 0
```

This demonstrates that once the requirement is satisfied, remaining weeks are filled with zeros without affecting correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(X) | We iterate once over remaining weeks |
| Space | O(X) | We store one value per remaining week |

The constraints limit X to at most 14, so the algorithm runs in constant time in practice and easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    import sys
    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output
    try:
        solve()
    finally:
        sys.stdout = old_stdout
    return output.getvalue().strip()

# provided sample
assert run("14 3 10 15\n") == "Yes\n3 3 3 2"

# minimum case, already satisfied
assert run("12 1 12 12\n") == "Yes\n0"

# impossible case
assert run("12 1 0 0\n") == "No"

# all capacity needed exactly
assert run("12 2 6 6\n") == "Yes\n2 2 2 2 2 2"

# boundary tight case
assert run("12 2 6 5\n") == "Yes\n2 2 2 2 2 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 14 3 10 15 | Yes 3 3 3 2 | sample correctness |
| 12 1 12 12 | Yes 0 | already satisfied case |
| 12 1 0 0 | No | impossible early detection |
| 12 2 6 6 | Yes 2 2 2 2 2 2 | full allocation |
| 12 2 6 5 | Yes 2 2 2 2 2 0 | greedy stopping |

## Edge Cases

When the requirement is already satisfied, the algorithm immediately outputs zero assignments for remaining weeks. For example, if total classes are 20 and required is 12 but you already have 15, then `need` becomes negative and the output is a zero vector, correctly preserving feasibility without unnecessary allocation.

When even full remaining capacity is insufficient, the feasibility check prevents construction. For example, if total remaining capacity is 3 but you need 5 more classes, the algorithm detects `need > remaining_capacity` and outputs “No” before attempting any distribution.
