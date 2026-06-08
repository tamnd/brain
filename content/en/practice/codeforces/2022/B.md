---
title: "CF 2022B - Kar Salesman"
description: "Each test case describes a dealership with several car models, where model i has ai identical cars that must all be sold."
date: "2026-06-08T12:36:17+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2022
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 978 (Div. 2)"
rating: 1300
weight: 2022
solve_time_s: 113
verified: true
draft: false
---

[CF 2022B - Kar Salesman](https://codeforces.com/problemset/problem/2022/B)

**Rating:** 1300  
**Tags:** binary search, greedy, math  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a dealership with several car models, where model `i` has `a_i` identical cars that must all be sold. A customer can be convinced to buy up to `x` cars, but only if all chosen cars come from distinct models, meaning a single customer cannot take two cars of the same type.

We want to schedule customers, where each customer selects up to `x` different models and removes one car from each chosen model. The goal is to reduce all `a_i` to zero while minimizing the number of customers.

The constraint `x ≤ 10` is small, but the number of models `n` can be large up to `5 · 10^5`, so any solution that tries to simulate customers one by one or repeatedly scans all models per customer will be too slow. The total sum of `n` across tests also reaches `5 · 10^5`, which enforces essentially linear or near-linear behavior per test.

A subtle edge case arises when one model dominates all others. For example, if one `a_i` is extremely large while others are small, the limiting factor is how many different models can be paired per customer, not the total number of cars. Another tricky situation is when counts are very balanced, where greedy intuition like always picking the largest `x` groups may still fail unless formalized correctly.

## Approaches

A naive approach would simulate customers explicitly. Each time, we would pick up to `x` models with remaining cars and decrement them. This works conceptually because it follows the rules exactly, but each customer requires selecting up to `x` models from up to `n`, leading to at least `O(n)` work per customer. Since the number of customers can also be on the order of the maximum `a_i`, this approach becomes infeasible.

The key observation is that the process is equivalent to distributing `sum(a_i)` units into groups of size at most `x`, where no group can take more than one unit from each index per round. The real bottleneck is not total sum but how many times a model must be served. If a model has `a_i` cars, it must appear in at least `a_i` different customers, but each customer can cover at most `x` models. This creates a packing constraint: each customer reduces at most `x` total remaining units across different indices.

A useful way to view the process is by considering how many “layers” of removals are required if we repeatedly take at most `x` distinct active models per layer. Each layer reduces at most `x` total remaining cars, so a lower bound is `ceil(sum(a_i) / x)`. However, this is not sufficient, because a single model might force more layers than its contribution to the sum suggests if it is too concentrated. The correct idea is that we always need at least `max(a_i)` layers where each layer can touch that model at most once, and also at least `ceil(sum(a_i) / x)` layers due to capacity.

The optimal answer is therefore the maximum of these two constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | O(steps · n) | O(1) | Too slow |
| Max constraint reasoning | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total number of cars across all models. This captures the overall workload that must be processed.
2. Find the maximum value among all `a_i`. This captures the most demanding single model, since it can only contribute once per customer.
3. Compute the lower bound from total capacity as `(sum(a_i) + x - 1) // x`. This reflects that each customer can remove at most `x` cars in total, regardless of distribution.
4. Take the maximum of the two bounds. This ensures both global capacity and per-model constraints are satisfied.
5. Output this value for each test case.

### Why it works

Each customer removes at most one car from any model, so a model with `a_i` cars requires at least `a_i` distinct customers. This gives the constraint that the answer cannot be smaller than `max(a_i)`. At the same time, every customer removes at most `x` cars total, so removing `S = sum(a_i)` cars requires at least `ceil(S / x)` customers.

A schedule achieving this bound exists because we can always greedily assign cars in batches: at each step pick up to `x` models with remaining cars and remove one from each. This process never gets stuck as long as at least one of the two constraints is not yet satisfied, since either total remaining cars or remaining maximum column height is still positive.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        s = sum(a)
        mx = max(a)
        
        ans = max(mx, (s + x - 1) // x)
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution processes each test case independently. It reads the array, computes the total sum and maximum in a single pass, and applies the derived formula.

The only subtle implementation detail is using integer ceiling division for `sum(a_i) / x`, implemented as `(s + x - 1) // x`. This avoids floating point errors and ensures correctness for large values.

## Worked Examples

### Example 1

Input:

```
3 2
3 1 2
```

We compute the total sum `6` and maximum `3`. The capacity bound is `ceil(6 / 2) = 3`.

| Step | sum | max | ceil(sum/x) | answer |
| --- | --- | --- | --- | --- |
| init | 6 | 3 | 3 | 3 |

The result is `3`, meaning three customers are sufficient and necessary.

This demonstrates a balanced case where both constraints coincide.

### Example 2

Input:

```
5 3
2 2 1 9 2
```

Sum is `16`, maximum is `9`, capacity bound is `ceil(16 / 3) = 6`.

| Step | sum | max | ceil(sum/x) | answer |
| --- | --- | --- | --- | --- |
| init | 16 | 9 | 6 | 9 |

Here the dominant constraint is the single large model, which forces nine separate customers.

This shows why only summation-based reasoning is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | each array is scanned once to compute sum and max |
| Space | O(1) extra | only a few accumulator variables are used |

The total `n` across tests is at most `5 · 10^5`, so a linear scan per test is easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        s = sum(a)
        mx = max(a)
        out.append(str(max(mx, (s + x - 1) // x)))
    return "\n".join(out)

# provided samples
assert run("""4
3 2
3 1 2
3 3
2 1 3
5 3
2 2 1 9 2
7 4
2 5 3 3 5 2 5
""") == """3
3
9
7"""

# custom cases
assert run("""1
1 10
5
""") == "5", "single model"

assert run("""1
3 2
100 100 100
""") == "150", "balanced large case"

assert run("""1
4 3
10 1 1 1
""") == "10", "dominant max constraint"

assert run("""1
5 5
1 1 1 1 1
""") == "1", "best packing case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single model | 5 | max(a_i) dominance |
| balanced large case | 150 | sum constraint correctness |
| dominant max constraint | 10 | single heavy pile |
| best packing case | 1 | perfect grouping when x ≥ n |
