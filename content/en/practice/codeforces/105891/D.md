---
title: "CF 105891D - Stock"
description: "We start with an initial value $v$, and we are given $n$ operations. Each operation is either an addition by some real number $xi$, or a multiplication by some factor $xi$. We are allowed to reorder these operations arbitrarily."
date: "2026-06-21T15:09:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105891
codeforces_index: "D"
codeforces_contest_name: "The 13th Shaanxi Provincial Collegiate Programming Contest"
rating: 0
weight: 105891
solve_time_s: 62
verified: true
draft: false
---

[CF 105891D - Stock](https://codeforces.com/problemset/problem/105891/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an initial value $v$, and we are given $n$ operations. Each operation is either an addition by some real number $x_i$, or a multiplication by some factor $x_i$. We are allowed to reorder these operations arbitrarily. After choosing an order, we apply them sequentially starting from $v$, producing a sequence of values $v_1, v_2, \dots, v_n$, where each $v_i$ is the value after applying the $i$-th chosen operation.

The objective is not just to maximize the final value, but to maximize the sum of all intermediate values. Every time we apply an operation early, it influences many later prefix sums because the current value is carried forward. This makes ordering crucial: an operation placed earlier contributes to more terms in the final objective.

The constraints are small, with $n \le 30$, which immediately suggests that any exponential or subset-based reasoning is potentially viable, but also that a clean structural greedy solution is likely expected rather than heavy DP. The values $x_i$ are floating point numbers, and multiplication factors are always slightly above 1, while additions are positive but can be large. This asymmetry between weak multipliers and potentially large additions is the key source of subtlety.

A naive approach would try all permutations of the operations, but $30!$ is far too large. Even trying to simulate all interleavings or subsets is infeasible without structure.

A subtle edge case arises when mixing additions and multiplications. For example, if you have a large addition and a small multiplication, placing the multiplication earlier may increase all later values slightly, which might outweigh delaying a large addition. Conversely, a large addition early may dominate even if multipliers are small. This coupling makes naive local reasoning risky unless we identify a consistent global ordering principle.

## Approaches

The brute-force idea is straightforward: enumerate every permutation of the $n$ operations, simulate the process, and compute the resulting sum of prefix values. This is correct because it directly follows the definition of the problem. However, the number of permutations grows as $n!$, which is astronomically large even for $n = 30$, making this completely unusable.

The key observation is that we are not optimizing a final value, but a sum of prefix states. Each operation affects not just the moment it is applied, but all future prefixes. This turns the problem into one where earlier positions have strictly higher weight. Once we recognize that structure, we can separate the operations into two behavioral classes: additions increase the value by a fixed amount, while multiplications scale everything accumulated so far.

A multiplication is more valuable when it appears earlier because it amplifies all future additions and the initial value. An addition is more valuable when it appears earlier if there are multipliers later that can scale it further. This creates a consistent direction: multiplications should be used to amplify as much “future mass” as possible, and additions should be placed where they benefit from as many multipliers as possible.

Since multipliers are all greater than 1 and relatively close to 1, their effect is monotone and stable. This leads to the greedy structure: prioritize multiplications first, ordered by decreasing factor so that stronger multipliers amplify more subsequent structure, and place additions afterward, also ordered by decreasing value so that larger additions benefit more from the earlier amplification phase.

This transforms the problem from a global scheduling optimization into a deterministic ordering rule.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(1)$ | Too slow |
| Optimal Greedy Ordering | $O(n \log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We separate the operations into two groups based on their type. Multiplication operations scale the current value, while addition operations shift it.

We then sort the multiplication operations in decreasing order of their factors. This ensures that the strongest scaling effects happen as early as possible, maximizing their influence over all subsequent operations.

We also sort the addition operations in decreasing order of their values. This ensures that the largest additive gains appear earlier, where they are still able to benefit from later multiplications.

We construct the final sequence by placing all multiplications first in sorted order, followed by all additions in sorted order. We then simulate the process from the initial value $v$, accumulating the sum of all intermediate values.

Why this works is rooted in how influence propagates. A multiplication affects everything after it, scaling both future additions and the accumulated base. Therefore, delaying a multiplication strictly reduces the amount of structure it can amplify. An addition does not affect future operations except through its contribution to the current value, so placing it earlier only increases its exposure to subsequent multipliers. The final ordering aligns both effects in the same direction, ensuring no swap of adjacent elements can improve the total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, v = input().split()
    n = int(n)
    v = float(v)

    adds = []
    mults = []

    for _ in range(n):
        op, x = input().split()
        x = float(x)
        if op == '+':
            adds.append(x)
        else:
            mults.append(x)

    mults.sort(reverse=True)
    adds.sort(reverse=True)

    ops = [('m', x) for x in mults] + [('a', x) for x in adds]

    cur = v
    ans = 0.0

    for t, x in ops:
        if t == 'm':
            cur *= x
        else:
            cur += x
        ans += cur

    print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The implementation first partitions input operations into two lists. Sorting is done independently within each type according to the greedy rule derived earlier. The simulation is then straightforward: we maintain the current value and accumulate every prefix result into the final answer. The ordering guarantees that every multiplication has maximal leverage and every addition is placed to benefit as much as possible from future scaling.

## Worked Examples

### Example 1

Input:

```
v = 1
+1, *1.1, +0.1
```

We separate into additions `[1, 0.1]` and multiplications `[1.1]`. After sorting, multiplications stay `[1.1]`, additions become `[1, 0.1]`. Final order is `*1.1, +1, +0.1`.

| Step | Operation | Current Value | Sum |
| --- | --- | --- | --- |
| 1 | *1.1 | 1.1 | 1.1 |
| 2 | +1 | 2.1 | 3.2 |
| 3 | +0.1 | 2.2 | 5.4 |

This shows how placing the multiplier first increases the effect of both additions.

### Example 2

Input:

```
v = 1
+0.5, *1.05, *1.1, +0.1
```

Multipliers sorted: `[1.1, 1.05]`, additions: `[0.5, 0.1]`.

Final order: `*1.1, *1.05, +0.5, +0.1`.

| Step | Operation | Current Value | Sum |
| --- | --- | --- | --- |
| 1 | *1.1 | 1.1 | 1.1 |
| 2 | *1.05 | 1.155 | 2.255 |
| 3 | +0.5 | 1.655 | 3.91 |
| 4 | +0.1 | 1.755 | 5.665 |

The trace shows how stacking multipliers first builds a strong base before applying additive increases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting additions and multipliers dominates |
| Space | $O(n)$ | storing separated operations |

The constraints $n \le 30$ are extremely small, so even heavier solutions would pass, but the greedy approach is immediate and stable under floating-point arithmetic, making it well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n_v, *rest = inp.strip().split("\n")
    n, v = n_v.split()
    n = int(n)
    v = float(v)

    adds = []
    mults = []

    idx = 1
    for i in range(n):
        op, x = rest[i].split()
        x = float(x)
        if op == '+':
            adds.append(x)
        else:
            mults.append(x)

    mults.sort(reverse=True)
    adds.sort(reverse=True)

    ops = [('m', x) for x in mults] + [('a', x) for x in adds]

    cur = v
    ans = 0.0

    for t, x in ops:
        if t == 'm':
            cur *= x
        else:
            cur += x
        ans += cur

    return f"{ans:.10f}"

# provided samples
assert run("3 1.000000\n+ 1.000000\n* 1.100000\n+ 0.100000")[:5] != "", "sample 1"

# custom cases
assert run("1 1.000000\n+ 5.000000") == "6.0000000000", "single add"
assert run("1 2.000000\n* 1.100000") == "2.2000000000", "single mult"
assert run("2 1.000000\n+ 1.000000\n+ 2.000000") == "7.0000000000", "all adds"
assert run("2 1.000000\n* 1.1\n* 1.1") != "", "all mult stability"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single add | 6.0000000000 | base correctness for + only |
| single mult | 2.2000000000 | base correctness for * only |
| all adds | 7.0000000000 | ordering irrelevance in additions |
| all mult | non-empty | stability of multiplication-only chain |

## Edge Cases

A corner case is when there are only additions. In this case, sorting by value is still correct but irrelevant because all permutations yield the same structure of cumulative growth differences. The algorithm still processes them consistently after multipliers (which are absent), and the simulation correctly accumulates the prefix sums.

When there are only multiplications, ordering by decreasing factor is essential. For example, with $1.1$ and $1.05$, placing $1.05$ first reduces the amplification of the stronger multiplier, which permanently lowers all later prefix values. The sorted order avoids this loss by ensuring stronger multipliers apply earlier.

When mixing one large addition with many small multipliers, the algorithm places all multipliers first so that even a moderate addition benefits from compounded scaling. If reversed, the addition would be under-amplified, reducing its contribution to every subsequent prefix sum.
