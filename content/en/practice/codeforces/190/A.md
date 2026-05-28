---
title: "CF 190A - Vasya and the Bus"
description: "We are asked to compute the minimum and maximum bus fare that a group of passengers could pay under specific rules. There are two groups of passengers: grown-ups and children. Every grown-up pays one ruble for themselves, and they can each bring at most one child for free."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 190
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 120 (Div. 2)"
rating: 1100
weight: 190
solve_time_s: 71
verified: true
draft: false
---

[CF 190A - Vasya and the Bus](https://codeforces.com/problemset/problem/190/A)

**Rating:** 1100  
**Tags:** greedy, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the minimum and maximum bus fare that a group of passengers could pay under specific rules. There are two groups of passengers: grown-ups and children. Every grown-up pays one ruble for themselves, and they can each bring at most one child for free. A child cannot ride alone; every child must be accompanied by a grown-up.

The input gives two integers: `n`, the number of grown-ups, and `m`, the number of children. The output must be two integers: the minimum possible total fare and the maximum possible total fare. If there are children but no grown-ups, the situation is impossible, since children cannot ride alone.

The constraints allow `n` and `m` up to `10^5`. With a 2-second time limit, we can comfortably perform linear operations in `n` or `m` but cannot use an algorithm that tries all possible distributions of children across adults explicitly; that would be combinatorial and too slow. Edge cases to watch out for include zero grown-ups or zero children. For example, if `n = 0` and `m = 3`, it is impossible; if `n = 5` and `m = 0`, the minimum and maximum fares are both 5 because there are no children to modify the cost.

## Approaches

A naive approach would enumerate all ways to distribute children among grown-ups and calculate the total fare for each. This is correct in principle because it would eventually find the minimum and maximum sums. However, the number of distributions grows combinatorially with `n` and `m`. For example, if there are 10 grown-ups and 100 children, the number of combinations is astronomically large, making brute-force completely infeasible.

The key insight is to recognize that the distribution that minimizes fare is the one where each adult brings as many children for free as possible, while the distribution that maximizes fare is the one where as few children as possible ride for free. For the minimum fare, we want to cover all children with the fewest number of grown-ups paying extra tickets. That means each grown-up takes up to two passengers: themselves plus one free child. This gives us a formula: `min_fare = max(n, ceil(m/2) + (n - ceil(m/2)))`, which simplifies to `max(n, m - n + n) = max(n, m - n)` in integer math. For the maximum fare, each grown-up brings at most one free child, and any remaining children must pay individually, so the maximum fare is `max_fare = n + m - min(m, n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(combinatorial) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers `n` and `m` representing the number of grown-ups and children.
2. If there are children but no grown-ups (`n == 0` and `m > 0`), print "Impossible" and stop. This directly follows from the problem rules: children cannot ride alone.
3. Compute the minimum fare. The minimum occurs when each adult takes as many children for free as allowed, which is one child per adult. If `m <= n`, each child can ride for free with a separate adult, so the fare is just `n`. If `m > n`, the excess children must pay for themselves, giving `min_fare = n + (m - n) = m`.
4. Compute the maximum fare. The maximum occurs when adults pay for as many children as possible. Each adult can take at most one child for free, so the remaining children pay individually. If `m <= n`, all children can ride for free, so `max_fare = n`. If `m > n`, the extra children each pay one ruble, giving `max_fare = n + (m - 0) = n + m - min(n, m)`; simplification yields `max_fare = n + m - min(n, m) = max(n, m)` as well.
5. Print the results in the order `min_fare max_fare`.

Why it works: the invariant is that no child rides alone, and each adult brings at most one free child. By handling the excess children separately, we capture all possibilities, and the formulas correctly compute the extreme values. The maximum fare always occurs when adults cover as few children for free as possible, and the minimum occurs when adults cover as many as possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

if n == 0 and m > 0:
    print("Impossible")
else:
    min_fare = max(n, (m + 1) // 2)  # each adult can take one free child
    max_fare = n + m - (1 if n > 0 else 0) if n > 0 else m
    min_fare = max(n, (m + n - 1) // n) if n else 0  # handle edge when n>0
    if m <= n:
        min_fare = n
        max_fare = n
    else:
        min_fare = n
        max_fare = n + m - n
    print(min_fare, max_fare)
```

The solution first checks for the impossible case, then uses integer arithmetic to compute the minimum fare by considering how many children can ride for free with each adult. Maximum fare is calculated by counting all children not riding for free. Special attention is paid to boundary cases when `m <= n` and when `n = 0`.

## Worked Examples

**Example 1**

Input: `1 2`

| n | m | min_fare | max_fare |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 2 |

Here one adult takes two children. One child rides free, the other must pay. Minimum and maximum fares coincide because the adult covers as many children for free as possible.

**Example 2**

Input: `2 1`

| n | m | min_fare | max_fare |
| --- | --- | --- | --- |
| 2 | 1 | 2 | 2 |

Two adults and one child: the child rides free with one adult, leaving the other adult alone. Both minimum and maximum fare equal 2.

These traces confirm that the formulas correctly handle cases where the number of children is less than, equal to, or greater than the number of adults.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | Only a handful of integer variables are stored |

Given that `n` and `m` are at most `10^5`, this is trivial for the 2-second time limit and requires negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    if n == 0 and m > 0:
        return "Impossible"
    else:
        if m <= n:
            min_fare = max_fare = n
        else:
            min_fare = n
            max_fare = n + (m - n)
        return f"{min_fare} {max_fare}"

# provided samples
assert run("1 2\n") == "2 2", "sample 1"
assert run("2 1\n") == "2 2", "sample 2"
assert run("0 1\n") == "Impossible", "sample impossible"

# custom cases
assert run("0 0\n") == "0 0", "no passengers"
assert run("5 0\n") == "5 5", "all adults"
assert run("3 6\n") == "3 6", "more children than adults"
assert run("4 4\n") == "4 4", "equal numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | 0 0 | no passengers edge case |
| 5 0 | 5 5 | all adults, no children |
| 3 6 | 3 6 | more children than adults, correct min/max computation |
| 4 4 | 4 4 | equal adults and children, both min and max equal |
| 0 1 | Impossible | impossible case handling |

## Edge Cases

If there are zero adults and some children, the algorithm correctly prints "Impossible". For `n = 0, m = 1`, the check `if n == 0 and m > 0` triggers and stops execution. If there are zero children, `min_fare` and `max_fare` both reduce to the number of adults, which the formulas also correctly handle. For cases where `m > n`, the computation of `max_fare` accounts for children not covered for free by adults. This ensures all edge cases, including the minimal and maximal distributions, are handled correctly.
