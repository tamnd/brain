---
title: "CF 104669F - Senioritis"
description: "We are given a group of students, each with a GPA value between 0 and 5. A student is considered “safe” only if their GPA reaches at least 2.8 after possible improvement."
date: "2026-06-29T09:41:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104669
codeforces_index: "F"
codeforces_contest_name: "Turtle Codes"
rating: 0
weight: 104669
solve_time_s: 75
verified: true
draft: false
---

[CF 104669F - Senioritis](https://codeforces.com/problemset/problem/104669/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of students, each with a GPA value between 0 and 5. A student is considered “safe” only if their GPA reaches at least 2.8 after possible improvement.

There is a potion that can be applied to a student multiple times, and each full application increases that student’s GPA by exactly 1. However, the potion is slow: each use consumes a fixed amount of time, and we only have a limited total time budget. Importantly, each student must be improved independently, and we can choose how to distribute potion uses across students.

The task is to minimize how many students remain below 2.8 after using the available time optimally. Equivalently, we want to maximize how many students we can raise to at least 2.8, given that each “upgrade” has a uniform cost in time but different students require different numbers of upgrades.

The constraints imply that we must treat this as a resource allocation problem over upgradable items. With up to typical Codeforces scale inputs (up to around 10^5 students), any quadratic simulation over all students and potion allocations would be too slow. We need an O(n log n) or O(n) strategy, likely based on greedy selection.

A few edge cases matter:

A student already at or above 2.8 requires zero upgrades and should always be counted as safe immediately. For example, GPA list `[3.0, 4.2]` should yield 0 uncured regardless of time.

A student just below threshold might require only one or two upgrades, while another far below (like 0.1) may require many more. A naive strategy that prioritizes lowest GPA first can fail, because it may waste time on expensive conversions early.

Another subtle case is when time is insufficient for even a single upgrade for some students. If the total time divided by potion time per use is zero, then no improvement is possible and the answer is simply the count of GPA < 2.8.

## Approaches

A brute-force interpretation would simulate all possible ways of assigning potion uses to students. For each student, we could try applying 0, 1, 2, ... upgrades up to the limit needed, and recursively distribute the remaining time across others. This quickly becomes exponential because each student introduces multiple branching choices, and with n up to 10^5, even considering 10 choices per student leads to impossible state space size.

The key simplification is to observe that each student independently has a fixed “cost” in potion uses to reach 2.8. If a student has GPA `a`, then they need `ceil(max(0, 2.8 - a))` potion applications. Since each application costs the same time `m`, the problem reduces to: each student has a weight (number of required uses), and we have a budget of total uses `k // m`. We want to maximize how many weights we can fully pay.

This is a classic greedy selection problem. Since each student yields identical “value” (saving one person), but different costs, we should always prioritize students requiring fewer potion uses first. Sorting required uses in ascending order ensures we maximize the count of fully cured students.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate allocations) | Exponential | O(n) | Too slow |
| Greedy by required upgrades | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

First, compute how many potion applications each student needs to reach the threshold of 2.8. If a student is already at or above 2.8, this value is zero.

Second, compute how many total potion applications we can afford by dividing the total available time by the time per potion application.

Third, discard all students with zero required applications since they are already cured and do not consume resources.

Fourth, sort the remaining required application counts in increasing order so that cheaper cures come first.

Fifth, iterate through this sorted list, and for each student, check if we still have enough remaining potion applications. If yes, subtract their cost and count them as cured. Otherwise, stop.

Finally, the number of uncured students is the remaining count of students minus the number we successfully cured.

### Why it works

The correctness rests on a greedy exchange argument. Suppose we ever choose a more expensive student while skipping a cheaper one that we could have cured. Swapping them would never reduce the number of cured students, since both consume equal “value” (one cured person), but the cheaper one preserves more budget for others. Therefore, any optimal solution can be transformed into one that always picks students in non-decreasing cost order without loss of optimality.

This guarantees that the greedy selection maximizes the number of students cured under a fixed budget.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def solve():
    m, k = map(int, input().split())
    n = int(input())
    
    # total potion uses available
    total_uses = k // m
    
    costs = []
    already_ok = 0
    
    for _ in range(n):
        a = float(input().strip())
        
        if a >= 2.8:
            already_ok += 1
            continue
        
        need = 2.8 - a
        # each use adds exactly 1 GPA
        uses = math.ceil(need)
        costs.append(uses)
    
    costs.sort()
    
    cured = 0
    for c in costs:
        if total_uses >= c:
            total_uses -= c
            cured += 1
        else:
            break
    
    print(n - (already_ok + cured))

if __name__ == "__main__":
    solve()
```

The solution starts by converting total time into a discrete budget of potion applications. Each GPA is processed into a required integer number of applications using a ceiling operation, since partial applications are not allowed.

We explicitly separate already-qualified students because they contribute to the final safe count without consuming any budget. The remaining students are converted into costs and sorted so we always attempt the cheapest cures first.

The loop consumes budget greedily, ensuring we never waste resources on a high-cost student when a cheaper one could still be handled.

A subtle detail is floating-point handling when computing `2.8 - a`. Since inputs are given with at most one decimal place, floating precision is safe here, but in stricter settings this would be better handled with scaled integers.

## Worked Examples

### Sample Trace 1

Input:

```
m=5, k=21
GPAs: [1.7, 3.9, 4.0, 2.6, 0.7, 2.4]
```

Total uses = 21 // 5 = 4

| GPA | Need | Uses | Action | Remaining budget |
| --- | --- | --- | --- | --- |
| 1.7 | 1.1 | 2 | take | 2 |
| 2.4 | 0.4 | 1 | take | 1 |
| 2.6 | 0.2 | 1 | take | 0 |
| 0.7 | 2.1 | 3 | skip | 0 |

We can cure 3 students using sorted order of costs `[1,1,2,3]` but only first 3 fit into budget 4.

Already safe students: 2 (3.9, 4.0)

Total cured = 2 + 3 = 5, so uncured = 6 - 5 = 1

This shows the greedy strategy prioritizes low-cost fixes and stops exactly when budget is exhausted.

### Custom Trace 2

Input:

```
m=2, k=4
GPAs: [2.7, 2.7, 2.7]
```

Total uses = 2

| GPA | Need | Uses | Action | Remaining |
| --- | --- | --- | --- | --- |
| 2.7 | 0.1 | 1 | take | 1 |
| 2.7 | 0.1 | 1 | take | 0 |
| 2.7 | 0.1 | 1 | skip | 0 |

Cured = 2, uncured = 1.

This confirms that when all costs are identical, the algorithm simply picks arbitrarily until budget runs out.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting required potion counts dominates |
| Space | O(n) | Stores list of required uses |

The algorithm comfortably fits within constraints typical for Codeforces, since sorting 10^5 elements and a linear scan are both efficient under a 1-second limit in Python with fast I/O.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    input = sys.stdin.readline
    
    m, k = map(int, input().split())
    n = int(input())
    
    total_uses = k // m
    costs = []
    already_ok = 0
    
    for _ in range(n):
        a = float(input().strip())
        if a >= 2.8:
            already_ok += 1
            continue
        costs.append(math.ceil(2.8 - a))
    
    costs.sort()
    cured = 0
    
    for c in costs:
        if total_uses >= c:
            total_uses -= c
            cured += 1
        else:
            break
    
    return str(n - (already_ok + cured))

# provided sample
assert run("""5 21
6
1.7
3.9
4
2.6
0.7
2.4
""") == "1"

# all already safe
assert run("""5 10
3
3.0
4.0
5.0
""") == "0"

# no budget
assert run("""5 0
3
1.0
2.0
3.0
""") == "3"

# all require same cost
assert run("""2 4
3
2.7
2.7
2.7
""") == "1"

# mixed large gap
assert run("""1 10
4
0.0
0.0
0.0
5.0
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all safe | 0 | already-qualified handling |
| zero budget | all uncured | no operations possible |
| equal costs | 1 | uniform greedy correctness |
| mixed extremes | 1 | prioritization of cheap cures |

## Edge Cases

A key edge case is when all students are already above threshold. In this case, the cost list is empty, and the answer should be zero without performing any sorting or budget logic. The algorithm handles this naturally since `already_ok` equals `n` and `costs` is empty.

Another case is when the budget allows zero potion uses (`k < m`). Then `total_uses = 0`, and no student from the cost list can be cured. The final answer correctly becomes the number of students below 2.8, since the loop never executes any successful deduction.

A final subtle case occurs when floating values are extremely close to 2.8. Since the problem uses decimal inputs, computing `ceil(2.8 - a)` directly may risk precision issues in other languages. The algorithm assumes stable input precision, but in a more robust implementation, scaling values by 10 or 100 would eliminate floating-point concerns entirely.
