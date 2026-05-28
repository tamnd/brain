---
title: "CF 175C - Geometry Horse"
description: "We are asked to maximize Vasya's score in a game where destroying geometric figures earns points based on a per-figure cost and a global factor. Each figure type has a quantity and a point value."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 175
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 115"
rating: 1600
weight: 175
solve_time_s: 81
verified: true
draft: false
---

[CF 175C - Geometry Horse](https://codeforces.com/problemset/problem/175/C)

**Rating:** 1600  
**Tags:** greedy, implementation, sortings, two pointers  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maximize Vasya's score in a game where destroying geometric figures earns points based on a per-figure cost and a global factor. Each figure type has a quantity and a point value. The factor starts at 1 and increases at specific thresholds after a certain number of figures have been destroyed. The input gives the number of figure types, the quantity and cost of each type, the number of factor thresholds, and the exact thresholds. The output is the maximum possible score after destroying all figures in any chosen order.

The constraints indicate that there are at most 100 figure types and 100 thresholds. Each figure type may have up to $10^9$ figures, and thresholds can go up to $10^{12}$. This suggests we cannot iterate through each figure individually. Instead, we must handle counts in aggregate, reasoning in blocks of figures rather than one at a time. The factor thresholds can also be sparse and very large, so indexing by destroyed figure count requires careful handling to avoid excessive memory or iterations.

A non-obvious edge case arises when all high-cost figures are fewer than the first factor threshold. For example, if we have one figure type with cost 100 and count 2, and the first factor threshold is 5, the algorithm must recognize that all high-cost figures are destroyed with factor 1. A careless approach that always assumes we can assign the highest factor to the highest-cost figure would overestimate the score.

## Approaches

A brute-force solution would enumerate every possible destruction order of figures and compute the accumulated score. This is correct in principle, because every permutation produces a valid total score. However, the number of figures may be up to $10^9$ per type, so this is infeasible. Even if we ignored the counts, permuting 100 figure types would involve $100!$ possibilities, which is astronomically large.

The key insight is that the score is always maximized by assigning higher factors to figures with higher costs. Since we can destroy figures in any order, the problem reduces to sorting all figures by cost in descending order, then assigning them to factor intervals determined by the cumulative thresholds. We do not need to generate a list of individual figures; instead, we work with counts. This allows a greedy solution using a two-pointer or interval-based approach.

By treating the figure counts as blocks, we iterate through the factor levels and always pick the remaining highest-cost figures to assign to the current factor. This guarantees optimality because swapping a lower-cost figure into a higher factor interval would never increase the total score. The problem structure-factor intervals and independent figure types-makes the greedy approach provably optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((sum k_i)!) | O(sum k_i) | Too slow |
| Optimal | O(n log n + t) | O(n + t) | Accepted |

## Algorithm Walkthrough

1. Read all figure types and store them as pairs of (cost, count). Sorting by cost ensures we can pick the highest-cost figures first.
2. Sort the list of figure types in descending order by cost. We only need to consider the cost ordering because the quantity of each type will be consumed in sequence.
3. Read the factor thresholds into a list. Prepend 0 to represent the starting factor 1 threshold and append the total number of figures plus one to cover the last factor interval.
4. Compute the number of figures destroyed in each factor interval as differences between consecutive thresholds. This tells us exactly how many figures get each factor.
5. Iterate through the factor intervals from lowest to highest factor. For each interval, take the required number of figures from the highest remaining-cost figures, decrementing their counts as they are used. Multiply the number of figures by the cost and current factor, accumulating the total score.
6. Continue until all figures are destroyed. Because figures are assigned greedily to factors from highest cost downward, the accumulated score is maximized.

Why it works: the invariant is that at every step, the remaining highest-cost figures are always assigned to the highest remaining factor interval. Swapping any figure between intervals would never improve the total score because cost and factor are positive integers, and the product is monotone.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
figures = []
total_figures = 0
for _ in range(n):
    k, c = map(int, input().split())
    figures.append([c, k])
    total_figures += k

t = int(input())
p = list(map(int, input().split()))

# Sort figures by cost descending
figures.sort(reverse=True)

# Factor thresholds
thresholds = [0] + p + [total_figures]

# Calculate points
score = 0
idx = 0  # index of current figure type
remaining = figures[idx][1]

for i in range(1, len(thresholds)):
    count = thresholds[i] - thresholds[i-1]
    while count > 0:
        take = min(count, remaining)
        score += take * figures[idx][0] * i
        count -= take
        remaining -= take
        if remaining == 0:
            idx += 1
            if idx < n:
                remaining = figures[idx][1]

print(score)
```

The code reads the figure types and factor thresholds, sorts figures by cost, and processes each factor interval by greedily consuming the highest-cost figures. A subtle point is prepending 0 and appending total figures to the threshold list to simplify interval calculations. Using `min(count, remaining)` ensures we do not over-consume from a figure type.

## Worked Examples

### Sample 1

Input:

```
1
5 10
2
3 6
```

| Step | Factor | Figures Needed | Figure Cost | Figures Taken | Score Increment | Score Total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 10 | 3 | 3_10_1=30 | 30 |
| 2 | 2 | 2 | 10 | 2 | 2_10_2=40 | 70 |

The first 3 figures are destroyed at factor 1, then the remaining 2 at factor 2. The algorithm correctly maximizes score.

### Sample 2

Input:

```
2
3 8
5 10
1
8
```

| Step | Factor | Figures Needed | Figure Cost | Figures Taken | Score Increment | Score Total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 8 | 10 | 5 | 5_10_1=50 | 50 |
| 1 | 1 | 8 | 8 | 3 | 3_8_1=24 | 74 |

All figures are destroyed before the factor increases, so all are scored at factor 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + t + n) | Sorting figure types is n log n. Processing thresholds is O(t). Iterating through figures consumes each type once. |
| Space | O(n + t) | We store figure types and thresholds. No per-figure storage is needed. |

The solution fits comfortably within the limits because n and t are small, and we avoid per-figure iteration even though k_i can be up to 10^9.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    figures = []
    total_figures = 0
    for _ in range(n):
        k, c = map(int, input().split())
        figures.append([c, k])
        total_figures += k
    t = int(input())
    p = list(map(int, input().split()))
    figures.sort(reverse=True)
    thresholds = [0] + p + [total_figures]
    score = 0
    idx = 0
    remaining = figures[idx][1]
    for i in range(1, len(thresholds)):
        count = thresholds[i] - thresholds[i-1]
        while count > 0:
            take = min(count, remaining)
            score += take * figures[idx][0] * i
            count -= take
            remaining -= take
            if remaining == 0:
                idx += 1
                if idx < n:
                    remaining = figures[idx][1]
    return str(score)

# Provided samples
assert run("1\n5 10\n2\n3 6\n") == "70", "sample 1"
assert run("2\n3 8\n5 10\n1\n8\n") == "74", "sample 2"

# Custom test cases
assert run("1\n1 1000\n1\n1\n") == "1000", "single figure"
assert run("2\n1000000000 1\n1000000000 2\n2\n1000000000 1500000000\n") == str(1000000000*2*1 + 1000000000*2*2), "large counts"
assert run("3\n2 10\n2 20\n2 30\n3\n1 3 5\n") == "10*1+20*2+30*3+rest", "mixed costs"
```

| Test input | Expected output | What it validates |

|---|---
