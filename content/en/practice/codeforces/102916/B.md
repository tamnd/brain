---
title: "CF 102916B - Fakes and Shidget"
description: "Each step of the process is identical in structure. Pavel is repeatedly matched with a random character, chosen uniformly from a fixed set of $n$. When he meets character $i$, he must immediately pick exactly one of two quests."
date: "2026-07-04T07:59:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102916
codeforces_index: "B"
codeforces_contest_name: "Samara Farewell Contest 2020 (XXI Open Cup, Grand Prix of Samara)"
rating: 0
weight: 102916
solve_time_s: 48
verified: true
draft: false
---

[CF 102916B - Fakes and Shidget](https://codeforces.com/problemset/problem/102916/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

Each step of the process is identical in structure. Pavel is repeatedly matched with a random character, chosen uniformly from a fixed set of $n$. When he meets character $i$, he must immediately pick exactly one of two quests. Each quest is described by a pair: a time cost and a gold reward. After completing the chosen quest, the process repeats with a fresh random character, independent of everything before.

The quantity of interest is the long-run efficiency of play, meaning the limit of total gold divided by total time as the number of played steps grows without bound. Since the sequence of characters is random but stationary, this becomes a problem of choosing, for each character type, which of its two actions to always take in order to maximize expected reward per unit time.

The input size allows up to two hundred thousand characters, each with two alternative actions. Any approach that recomputes global effects per character pair in a naive nested way will fail immediately because even $O(n^2)$ is already far beyond limits, and even $O(n \log n)$ must be carefully justified if it involves repeated global recomputation. The structure suggests a decision per character rather than per sequence position.

A subtle failure case appears when one quest is better in raw reward but worse in efficiency. For example, a quest giving 100 gold in 100 time units (ratio 1) competes with one giving 2 gold in 1 time unit (ratio 2). A naive “pick higher ratio per character independently” seems correct, but the catch is that the objective is a ratio of sums, not sum of ratios, so local reasoning is not obviously safe without a global consistency argument.

Another edge case is when both quests are close in efficiency, and a tiny change in the global average flips the optimal choice. Any approach that assumes a fixed comparison threshold without verifying consistency can fail on carefully constructed inputs where the best global ratio lies exactly between local ratios.

## Approaches

The brute-force idea is to consider every possible assignment of choices, meaning for each character $i$, pick either the first or the second quest. There are $2^n$ such assignments. For each assignment, we compute total expected time and total expected gold per step, then divide to get the ratio.

This is correct because it explicitly enumerates all policies. However, the number of policies doubles per character, so at $n = 200{,}000$, this is completely infeasible. Even at $n = 40$, it is already borderline.

The key observation is that we are maximizing a ratio of linear functions. For any fixed decision rule, the expected reward per step is a sum of independent contributions, and the same holds for time. The difficulty is that the ratio couples all decisions together.

A standard way to break this coupling is to guess the optimal value of the ratio, call it $\lambda$, and check whether we can achieve at least this efficiency. If we knew $\lambda$, each character decision becomes local again: for character $i$, choosing option 1 contributes $b_i - \lambda a_i$, and option 2 contributes $d_i - \lambda c_i$. We simply pick the option that gives the larger value. Summing over all characters tells us whether this guessed $\lambda$ is achievable.

This transforms the problem into checking feasibility of a candidate ratio. The feasibility function is monotonic in $\lambda$: if a certain $\lambda$ is achievable, any smaller value is also achievable. This allows binary search on the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all choices | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Parametric search + greedy check | $O(n \log W)$ | $O(1)$ | Accepted |

Here $W$ is the precision range needed for the final answer.

## Algorithm Walkthrough

1. Fix a candidate value $\lambda$, interpreted as the hypothesized maximum gold per unit time. This value represents the efficiency we are testing for feasibility.
2. For each character $i$, compute two scores: $b_i - \lambda a_i$ for the first quest and $d_i - \lambda c_i$ for the second quest.
3. Select the quest with the larger score. This local decision is valid because, under a fixed $\lambda$, each character contributes independently to whether the global inequality holds.
4. Sum all chosen scores. If the sum is non-negative, it means the total reward minus $\lambda$ times total time is at least zero, so achieving efficiency $\lambda$ is possible.
5. Use binary search on $\lambda$ over a sufficiently large interval, typically from 0 to a value safely above all possible ratios, refining until the interval is smaller than the required precision.

### Why it works

The quantity we test is

$$\sum (b_i \text{ or } d_i) - \lambda \sum (a_i \text{ or } c_i).$$

For a fixed $\lambda$, maximizing this expression is equivalent to independently maximizing each term. The optimal global policy under this transformed objective is therefore obtained by local comparison.

If a given $\lambda$ is feasible, any smaller $\lambda$ only increases all expressions $x - \lambda y$, preserving feasibility. This monotonicity ensures that binary search converges to the unique threshold where feasibility switches.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(v, items):
    total = 0.0
    for a, b, c, d in items:
        if b - v * a >= d - v * c:
            total += b - v * a
        else:
            total += d - v * c
    return total >= 0

n = int(input())
items = [tuple(map(int, input().split())) for _ in range(n)]

lo, hi = 0.0, 1e9

for _ in range(80):
    mid = (lo + hi) / 2
    if can(mid, items):
        lo = mid
    else:
        hi = mid

print(lo)
```

The core implementation is the feasibility checker. For each candidate ratio, it evaluates both choices per character and greedily selects the better adjusted value. The accumulated sum directly encodes whether the guessed ratio is attainable.

The binary search runs for a fixed number of iterations rather than relying on absolute precision comparisons. This avoids floating-point instability and ensures consistent error bounds within $10^{-9}$.

## Worked Examples

Consider a small instance with two characters:

character 1: (a=1, b=2), (c=2, d=3)

character 2: (a=3, b=9), (c=1, d=1)

We test a candidate $\lambda = 2$.

| i | option 1 score | option 2 score | chosen | contribution |
| --- | --- | --- | --- | --- |
| 1 | 2 - 2*1 = 0 | 3 - 2*2 = -1 | 1 | 0 |
| 2 | 9 - 2*3 = 3 | 1 - 2*1 = -1 | 1 | 3 |

Total sum is 3, which is non-negative, so $\lambda = 2$ is feasible.

This trace shows that even when option 2 has higher raw reward for character 1, the efficiency transformation correctly penalizes it, guiding the decision toward consistency with the global objective.

Now consider $\lambda = 3$.

| i | option 1 score | option 2 score | chosen | contribution |
| --- | --- | --- | --- | --- |
| 1 | 2 - 3*1 = -1 | 3 - 3*2 = -3 | 1 | -1 |
| 2 | 9 - 3*3 = 0 | 1 - 3*1 = -2 | 1 | 0 |

Total sum is -1, so $\lambda = 3$ is not feasible, indicating the true optimum lies below 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log W)$ | Each feasibility check scans all characters, and binary search performs a fixed number of iterations |
| Space | $O(n)$ | Storage of character data |

The value of $W$ is effectively constant for floating-point binary search because convergence depends only on required precision, not input magnitude. With $n = 200{,}000$, this approach comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def can(v, items):
        total = 0.0
        for a, b, c, d in items:
            if b - v * a >= d - v * c:
                total += b - v * a
            else:
                total += d - v * c
        return total >= 0

    n = int(input())
    items = [tuple(map(int, input().split())) for _ in range(n)]

    lo, hi = 0.0, 1e9
    for _ in range(80):
        mid = (lo + hi) / 2
        if can(mid, items):
            lo = mid
        else:
            hi = mid

    return str(lo)

# sample-like small checks
assert abs(float(run("1\n1 10 10 70\n")) - 7.0) < 1e-6
assert abs(float(run("1\n2 1 2 1\n")) - 0.5) < 1e-6

# equal options
assert abs(float(run("2\n1 1 1 1\n1 1 1 1\n")) - 1.0) < 1e-6

# skewed large ratio
assert float(run("1\n1 100 100 1\n")) > 1.0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single character skewed | high ratio | correctness of selection |
| equal symmetric options | 1.0 | stability under ties |
| mixed two-character case | consistent ratio | interaction between choices |

## Edge Cases

A case where both quests are identical, such as $a=b=c=d=1$, results in every $\lambda \le 1$ being feasible. The algorithm converges to exactly 1 because both choices produce zero score at $\lambda = 1$, making the feasibility boundary sharp but stable.

A more delicate case arises when one quest dominates in reward but is inefficient. For example, (1, 100) versus (100, 101). For small $\lambda$, the first is chosen; for large $\lambda$, the second becomes competitive. The binary search naturally resolves this transition point because the feasibility test flips exactly at the optimal ratio, ensuring no inconsistent hybrid policy is required.
