---
title: "CF 105093H - Rainbow Energy"
description: "We are given several independent test cases. In each one, there is a collection of crystals, each crystal having a color and a radiation value."
date: "2026-06-27T20:50:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105093
codeforces_index: "H"
codeforces_contest_name: "2024 UP ACM Algolympics Final Round"
rating: 0
weight: 105093
solve_time_s: 36
verified: true
draft: false
---

[CF 105093H - Rainbow Energy](https://codeforces.com/problemset/problem/105093/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each one, there is a collection of crystals, each crystal having a color and a radiation value. We must choose at most $m$ crystals, but before using them, we are allowed to merge any number of crystals of the same color by repeatedly replacing two of them with one whose radiation is the sum of the two originals. Merging does not change color, only aggregates radiation.

After all merges, each remaining color contributes at most one crystal, because if two crystals of the same color remain, that is invalid for the final device. The final score is the product of radiation values of all selected distinct-color crystals. The task is to pick up to $m$ original crystals, merge them optimally within colors, and maximize this product.

The key structure constraint is that $n \le 15$, so even exponential subsets are feasible. However, radiation values are small and multiplicative behavior suggests that greedy choices are not obviously safe without enumerating configurations. This small $n$ immediately rules out any solution that tries to optimize over large state spaces or do continuous DP over sums, but strongly invites subset enumeration or bitmask dynamic programming.

A subtle pitfall is misunderstanding the “knapsack of size $m$” constraint. You do not pick colors; you pick original crystals. But merging means that selecting multiple crystals of a color effectively transforms them into a single stronger item. For example, selecting three crystals of color 2 yields a single crystal with summed radiation, and contributes exactly one factor in the final product.

Another subtle case is that taking more crystals of a color is not always beneficial unless it increases the product after merging. For instance, two crystals with radiation 1 and 1 become 2, which may or may not improve the product depending on other chosen values.

## Approaches

The brute-force approach is to try every subset of crystals of size at most $m$. For each subset, we simulate merging by grouping by color and summing radiation per group. Then we compute the product of the resulting per-color sums. This is correct because it directly models the process. The number of subsets is $2^n$, and with $n \le 15$, this is at most 32768 subsets, which is small enough. However, we also need to enforce subset size constraint and compute grouping per subset, giving an additional $O(n)$ factor, which is still fine in isolation.

The subtle issue is that we are actually double-counting structure if we are not careful: merging order does not matter, only total per color matters. So each subset uniquely maps to a multiset of colors with aggregated weights.

The key observation is that since $n$ is tiny, we do not need to be clever with DP compression or greedy strategies. We directly enumerate subsets, compute per-color aggregated sums, and evaluate product. The “knapsack of size $m$” constraint is handled simply by skipping subsets larger than $m$.

This reduces the problem to subset enumeration with linear evaluation per subset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | $O(2^n \cdot n)$ | $O(n)$ | Accepted |
| Bitmask evaluation (optimal) | $O(2^n \cdot n)$ | $O(n)$ | Accepted |

In practice, both are identical; the “optimization” is recognizing that no more advanced structure is needed.

## Algorithm Walkthrough

1. For each test case, read all crystals and store them as pairs of color and radiation.
2. Iterate over all bitmasks from $0$ to $2^n - 1$, where each bitmask represents a subset of crystals. This encodes the decision of which crystals we take before any merging.
3. For each subset, count how many crystals are selected. If this exceeds $m$, discard the subset immediately because it violates the knapsack constraint.
4. Build an array or dictionary indexed by color, and accumulate radiation values of all selected crystals of that color. This simulates all allowed merges, since merging within a color is equivalent to summing.
5. Compute the product of all nonzero color sums.
6. Track the maximum product across all valid subsets.

The correctness hinges on the fact that once a subset is fixed, merging is deterministic: all crystals of a given color collapse into a single value equal to their sum. There is no alternative configuration that changes the outcome.

### Why it works

Any valid final configuration corresponds to choosing some subset of original crystals, then merging within each color arbitrarily. Merging does not change the total radiation per color, only the number of items per color. Therefore, each subset uniquely determines a final product, and every feasible solution corresponds to exactly one subset. Exhausting all subsets guarantees we examine every possible outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        c = []
        r = []
        for _ in range(n):
            ci, ri = map(int, input().split())
            c.append(ci)
            r.append(ri)

        ans = 0

        for mask in range(1 << n):
            if mask.bit_count() > m:
                continue

            color_sum = {}
            for i in range(n):
                if mask & (1 << i):
                    color_sum[c[i]] = color_sum.get(c[i], 0) + r[i]

            prod = 1
            for val in color_sum.values():
                prod *= val

            if prod > ans:
                ans = prod

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the subset enumeration strategy. The `bit_count()` check enforces the size constraint early, pruning invalid subsets. The dictionary `color_sum` aggregates radiation per color, which models all allowed merges implicitly.

The product computation multiplies all aggregated values, skipping empty colors since they do not appear in the dictionary. The answer is updated greedily across all subsets.

A subtle point is that radiation values are small individually, but products can grow quickly. Python’s arbitrary precision integers prevent overflow issues, so no extra handling is required.

## Worked Examples

Consider a simple case with three crystals: $(1, 3), (2, 2), (2, 2)$, and $m = 3$.

We enumerate subsets:

| mask | selected crystals | color sums | product | valid |
| --- | --- | --- | --- | --- |
| 000 | none | {} | 1 | yes |
| 001 | (1,3) | {1:3} | 3 | yes |
| 010 | (2,2) | {2:2} | 2 | yes |
| 011 | (2,2),(1,3) | {1:3,2:2} | 6 | yes |
| 110 | (2,2),(2,2) | {2:4} | 4 | yes |
| 111 | all | {1:3,2:4} | 12 | yes |

The maximum is 12, achieved by taking all crystals and merging the two color-2 crystals.

This trace shows that merging is never a decision point: once a subset is fixed, the aggregation is deterministic.

Now consider $m = 2$ on the same input.

| mask | selected | size | valid | product |
| --- | --- | --- | --- | --- |
| 011 | (1,3),(2,2) | 2 | yes | 6 |
| 110 | (2,2),(2,2) | 2 | yes | 4 |

The best is 6. This demonstrates that limiting subset size directly prunes configurations that would otherwise benefit from merging.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \cdot 2^n \cdot n)$ | Each subset is enumerated, and for each we scan all elements to accumulate per-color sums |
| Space | $O(n)$ | Storage for input arrays and temporary color aggregation |

With $n \le 15$, the maximum number of
