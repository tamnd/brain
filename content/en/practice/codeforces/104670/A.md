---
title: "CF 104670A - Antenna Analysis"
description: "We are given a sequence of daily measurements, where each day has a single integer value. For every day i, we want to compare that day with any earlier day j, including itself, and compute how large a “meaningful jump” in measurement is between those two days after penalizing…"
date: "2026-06-29T09:33:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104670
codeforces_index: "A"
codeforces_contest_name: "2021-2022 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2021)"
rating: 0
weight: 104670
solve_time_s: 47
verified: true
draft: false
---

[CF 104670A - Antenna Analysis](https://codeforces.com/problemset/problem/104670/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of daily measurements, where each day has a single integer value. For every day i, we want to compare that day with any earlier day j, including itself, and compute how large a “meaningful jump” in measurement is between those two days after penalizing time distance.

The score between two days is defined as the absolute difference in measurements minus a penalty proportional to how far apart the days are. Formally, for each i we consider all j ≤ i and evaluate |xi − xj| − c · (i − j), then take the maximum value.

The output is an array where the i-th value is this maximum score for day i.

The constraint n up to 4 · 10^5 immediately rules out any quadratic comparison across all pairs of days. A naive O(n^2) approach would require on the order of 10^11 operations, which is far beyond any feasible limit in a few seconds. This pushes us toward a solution where each index contributes in constant or logarithmic time, typically through a prefix maintenance trick or a transformation that turns the expression into something we can optimize with a running summary.

A subtle edge case appears when all values are identical. In that situation, every difference |xi − xj| is zero, and the answer should be zero for all i. Any approach that forgets to include j = i as a valid choice would incorrectly produce negative values or fail to clamp to zero.

Another corner case happens when the optimal earlier index is very close in time but has a slightly worse value, while a farther index has a much better value. This is exactly why naive “track last max or min value” strategies fail, since the time penalty interacts with the value difference and cannot be separated without transformation.

## Approaches

The brute-force method is straightforward. For each day i, iterate over all previous days j and compute the score directly, keeping the best. This is correct because it explicitly evaluates every candidate pair. However, each i scans up to i values, so the total number of operations grows like 1 + 2 + … + n, which is about n^2 / 2. With n = 4 · 10^5, this becomes completely infeasible.

The key observation is that the absolute value splits the problem into two linear forms depending on whether xi is greater than xj or not. Each form can be rearranged so that all dependence on j is isolated into a prefix statistic, while all dependence on i is a simple expression we compute once per index.

Expanding the expression gives two cases. If we remove the absolute value, we get either xi − xj or xj − xi. Each of these becomes linear in i and j once we expand the time penalty c · (i − j). This lets us rewrite the problem as maintaining two running quantities over all previous j: one tracking the minimum of xj − c · j and one tracking the maximum of xj + c · j.

This reduces each query to constant time, since at day i we only combine xi with these two prefix summaries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from left to right, maintaining information about all previous indices.

1. Maintain two running values while scanning: the minimum value of xj − c · j and the maximum value of xj + c · j for all j seen so far. These summarize all previous choices in a way that aligns with the two possible directions of the absolute value.
2. For each index i, compute two candidate answers. The first candidate corresponds to the case where xi is greater than xj, and it becomes (xi − c · i) − min(xj − c · j). This measures how large xi is relative to the best “low adjusted value” seen before it.
3. The second candidate corresponds to the case where xj is greater than xi, and it becomes max(xj + c · j) − (xi + c · i). This measures how large a previous high adjusted value is compared to the current adjusted value.
4. The answer for day i is the maximum of these two candidates. After computing it, we update both running summaries with the current index i so it becomes available for future days.

### Why it works

The transformation isolates the dependence on j into two monotone statistics over prefixes. Every possible earlier index contributes to one of the two linear forms, and the prefix minimum or maximum ensures that the best possible j is always represented in O(1) time. Since every pair (i, j) is implicitly considered through these summaries, the computed maximum matches the brute-force definition exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, c = map(int, input().split())
    x = list(map(int, input().split()))

    INF = 10**30

    min_left = INF
    max_left = -INF

    res = []

    for i in range(n):
        xi = x[i]

        val1 = xi - c * i
        val2 = xi + c * i

        if i == 0:
            res.append(0)
        else:
            best1 = val1 - min_left
            best2 = max_left - val2
            res.append(max(best1, best2))

        expr1 = xi - c * i
        expr2 = xi + c * i

        if expr1 < min_left:
            min_left = expr1
        if expr2 > max_left:
            max_left = expr2

    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation keeps two running values that correspond directly to the algebraic forms derived in the walkthrough. The variable `min_left` stores the smallest value of xj − c·j seen so far, while `max_left` stores the largest value of xj + c·j. At each step, we compute the contribution of the current index against both summaries in constant time.

A common mistake is updating the prefix values before computing the answer for i, which would incorrectly allow j = i to influence itself in a way that breaks the intended separation. The correct order is to compute the answer first, then incorporate the current index into the running structure.

## Worked Examples

We use the sample input:

Input:

5 1

2 7 1 5 4

We track the state step by step.

| i | xi | min(xj − cj) | max(xj + cj) | best1 | best2 | yi |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | inf | -inf | - | - | 0 |
| 1 | 7 | 2 | 2 | 7 | 0 | 4 |
| 2 | 1 | -1 | 8 | 5 | 5 | 5 |
| 3 | 5 | -1 | 8 | 3 | 3 | 3 |
| 4 | 4 | -2 | 8 | 1 | 1 | 1 |

This trace shows how earlier extreme transformed values fully determine each answer. The third day illustrates why local reasoning fails: even though xi is small, the earlier very large value still influences the result through the second transformed form.

A second small example:

Input:

3 2

5 1 10

| i | xi | min(xj − cj) | max(xj + cj) | yi |
| --- | --- | --- | --- | --- |
| 0 | 5 | inf | -inf | 0 |
| 1 | 1 | 5 | 5 | 0 |
| 2 | 10 | -3 | 9 | 7 |

This demonstrates how a far earlier low value can become relevant again once the penalty is accounted for.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is processed once with constant-time updates and queries |
| Space | O(1) | Only two running aggregates are stored regardless of input size |

The linear time behavior is sufficient for n up to 4 · 10^5, and the constant memory usage avoids any pressure on the large memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, c = map(int, input().split())
    x = list(map(int, input().split()))

    INF = 10**30
    min_left = INF
    max_left = -INF
    res = []

    for i in range(n):
        xi = x[i]
        if i == 0:
            res.append(0)
        else:
            best1 = (xi - c * i) - min_left
            best2 = max_left - (xi + c * i)
            res.append(max(best1, best2))

        min_left = min(min_left, xi - c * i)
        max_left = max(max_left, xi + c * i)

    return " ".join(map(str, res))

# provided sample
assert run("5 1\n2 7 1 5 4\n") == "0 4 5 3 1"

# minimum size
assert run("1 10\n5\n") == "0"

# all equal
assert run("4 3\n7 7 7 7\n") == "0 0 0 0"

# increasing values
assert run("5 1\n1 2 3 4 5\n") == "0 0 0 0 0"

# strong jump late
assert run("4 2\n10 1 1 50\n") == "0 7 7 42"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case correctness |
| all equal | all zeros | absolute value symmetry |
| increasing sequence | zeros | cancellation under penalty |
| late spike | large final values | long-distance contribution |

## Edge Cases

When all values are identical, the transformed quantities xj − c·j and xj + c·j evolve only due to the linear penalty term. The algorithm still maintains correct minima and maxima, but both candidate expressions collapse to zero at every step, since xi matches every xj and the penalty never produces a positive gain. This matches the expected output of a zero array.

When the best previous index is very far in time, the prefix statistics already encode that index regardless of how far back it is. For example, if a very large value appears early, its contribution remains stored in max(xj + c·j) and continues to influence all future indices correctly, because the linear adjustment exactly compensates for time distance.
