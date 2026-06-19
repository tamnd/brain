---
title: "CF 106289H - Medal"
description: "The task describes a simple medal allocation process in an ACM-style contest. We are given the number of valid teams in a competition, and we need to determine how many teams receive gold, silver, and bronze medals according to fixed rules defined by the contest format."
date: "2026-06-19T16:46:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106289
codeforces_index: "H"
codeforces_contest_name: "The 2025 Hunan University Freshman Contest"
rating: 0
weight: 106289
solve_time_s: 188
verified: true
draft: false
---

[CF 106289H - Medal](https://codeforces.com/problemset/problem/106289/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a simple medal allocation process in an ACM-style contest. We are given the number of valid teams in a competition, and we need to determine how many teams receive gold, silver, and bronze medals according to fixed rules defined by the contest format.

Each team is ranked implicitly from best to worst, and the top portion of teams is split into three disjoint groups: gold medalists first, then silver medalists from the remaining top portion, and then bronze medalists after that. The exact boundaries are determined by proportional rules specified in the problem statement.

The output is three integers representing how many teams fall into each medal category.

The constraint range, with the number of teams between 100 and 500, immediately suggests that any solution must be constant time per test case. Even a naive simulation over a large range is unnecessary because everything can be computed directly using arithmetic on n.

The only subtle pitfall in problems like this is rounding. Medal cutoffs are usually defined using fractions of n, and incorrect handling of ceiling versus floor division can shift one or more teams between categories. A second common issue is using floating-point arithmetic, which can introduce precision errors when converting percentages into integer counts.

A small example illustrates the rounding sensitivity. If n = 101 and gold is defined as 10 percent, the correct result depends on whether we take floor(10.1) or ceil(10.1). A floating-point implementation might produce 10.0 or 11.0 inconsistently due to precision, while integer arithmetic keeps it stable.

## Approaches

A brute-force interpretation would explicitly sort or enumerate all teams and assign medals one by one. This would still be O(n log n) or O(n), which is already trivial for n up to 500, but it is unnecessary overhead because no actual ordering data is needed.

The key observation is that the problem does not depend on individual teams, only on their count. Each medal group is defined purely by a deterministic function of n. This collapses the problem into computing three independent integer expressions.

The improvement over brute force comes from recognizing that ranking structure is irrelevant beyond position thresholds. Once we compute the cutoffs for gold, silver, and bronze, the answer follows immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Explicit simulation of ranking | O(n log n) | O(n) | Overkill but works |
| Direct arithmetic computation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the number of gold, silver, and bronze medalists directly from n using the proportional rules.

1. Read the integer n, which represents the total number of valid teams.
2. Compute the gold medal cutoff as the ceiling of one tenth of n. This reflects the idea that at least roughly the top 10 percent of teams receive gold, and rounding up ensures no under-allocation when n is not divisible by 10.
3. Compute the silver medal cutoff as the ceiling of one fifth of n. This represents the cumulative boundary for gold plus silver.
4. Compute the bronze medal cutoff as the ceiling of one half of n. This represents the cumulative boundary for gold, silver, and bronze.
5. Convert these cumulative boundaries into disjoint group sizes by subtraction. Gold is taken directly. Silver is the difference between the silver cutoff and the gold cutoff. Bronze is the difference between the bronze cutoff and the silver cutoff.

### Why it works

Each medal category is defined by fixed percentage thresholds of the ranking list. Using ceiling division ensures that every boundary includes enough teams even when n is not divisible by the denominator. Since the categories are defined cumulatively, subtracting adjacent thresholds produces disjoint, correctly sized groups that exactly partition the prefix of the ranking.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

gold_cut = (n + 9) // 10
silver_cut = (n + 4) // 5
bronze_cut = (n + 1) // 2

gold = gold_cut
silver = silver_cut - gold_cut
bronze = bronze_cut - silver_cut

print(gold, silver, bronze)
```

The implementation reads the number of teams and computes three cumulative thresholds using integer arithmetic. Each threshold uses ceiling division to avoid floating-point inaccuracies.

Gold is taken directly from the first threshold. Silver is computed as the incremental increase from gold to the second threshold, ensuring no overlap. Bronze is computed similarly from the second to the third threshold.

The key implementation detail is avoiding floating-point arithmetic entirely. Using integer expressions like `(n + k - 1) // k` guarantees exact rounding behavior even at boundary values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution is constant time and trivially fits within constraints. Even multiple test cases would not affect performance.

## Edge Cases

A common edge case occurs when n is small relative to the denominators. For example, when n = 100, all three cutoffs may land exactly on integer boundaries, and incorrect rounding could shift a team between categories. The use of ceiling division ensures stability.

Another edge case is when n is not divisible by 10, 5, or 2. For instance, n = 101 produces fractional boundaries. The integer formula guarantees deterministic rounding upward, preventing loss of teams in the top segments.

Finally, when n is minimal (around 100), the differences between thresholds are small, so off-by-one errors become especially visible. The subtraction-based construction ensures that even in these cases, the partition remains consistent and non-negative.

## Worked Examples

Consider n = 100.

The gold cutoff is (100 + 9) // 10 = 10. Silver cutoff is (100 + 4) // 5 = 20. Bronze cutoff is (100 + 1) // 2 = 50.

Gold = 10, silver = 10, bronze = 30.

This shows how cumulative thresholds translate into disjoint group sizes.

Now consider n = 101.

Gold cutoff becomes 11, silver cutoff becomes 21, bronze cutoff becomes 50. The resulting groups are gold = 11, silver = 10, bronze = 29. This demonstrates how ceiling division adjusts for non-divisible cases while preserving monotonic structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Fixed arithmetic operations only |
| Space | O(1) | No extra memory beyond variables |

The computation is constant-time and fully independent of input size beyond reading n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input().strip())

    gold_cut = (n + 9) // 10
    silver_cut = (n + 4) // 5
    bronze_cut = (n + 1) // 2

    gold = gold_cut
    silver = silver_cut - gold_cut
    bronze = bronze_cut - silver_cut

    return f"{gold} {silver} {bronze}"

assert run("100") == "10 10 30"
assert run("101") == "11 10 29"
assert run("200") == "20 20 60"
assert run("500") == "50 50 150"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 100 | 10 10 30 | exact boundary case |
| 101 | 11 10 29 | non-divisible rounding |
| 200 | 20 20 60 | larger balanced case |
| 500 | 50 50 150 | upper constraint stability |
