---
title: "CF 276A - Lunch Rush"
description: "We are given a list of restaurants, where each restaurant has two values: a baseline enjoyment score and the time required to eat there. The coach only allows a fixed lunch duration."
date: "2026-06-05T02:15:33+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 276
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 169 (Div. 2)"
rating: 900
weight: 276
solve_time_s: 79
verified: true
draft: false
---

[CF 276A - Lunch Rush](https://codeforces.com/problemset/problem/276/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of restaurants, where each restaurant has two values: a baseline enjoyment score and the time required to eat there. The coach only allows a fixed lunch duration. If a restaurant can be finished within the allowed time, the team receives the full enjoyment value. If the restaurant takes longer than the allowed time, the enjoyment is reduced by exactly the amount of extra time spent beyond the limit.

The task is to choose exactly one restaurant in a way that maximizes the resulting enjoyment after applying this rule.

The input size reaches up to ten thousand restaurants, which means a solution that recomputes complex logic for every restaurant independently is still acceptable, but anything quadratic with nested processing over large data structures would be unnecessary overhead. A single pass over the data is easily fast enough under these constraints, since we are only evaluating a simple formula per restaurant.

There is one subtle case that often causes mistakes. When a restaurant takes less or equal time than allowed, the answer is simply the base enjoyment. When it exceeds the time limit, we must subtract only the excess portion, not the full time. For example, if the limit is 5, a restaurant with enjoyment 10 and time 8 yields 10 − (8 − 5) = 7. A common mistake is to subtract the full time instead of just the overflow, which would incorrectly give 2.

Another edge case appears when all restaurants exceed the time limit and have small base values. The corrected formula can produce negative results, and the correct answer may be negative. This means we cannot default to zero or assume a non-negative result.

## Approaches

A direct approach is to compute the enjoyment for each restaurant independently using the given rule and track the maximum. For each restaurant, we check whether its time is within the allowed limit. If so, we take the base value; otherwise we subtract the excess time. This gives a constant amount of work per restaurant.

This works because the problem does not introduce dependencies between restaurants. Each option is evaluated in isolation, so there is no need for sorting, dynamic programming, or prefix processing. The only requirement is to scan all candidates and compute their adjusted value.

The naive interpretation might suggest handling different cases separately in more complex ways, but there is no structure that allows reuse of intermediate results. Every restaurant must be evaluated at least once, so the optimal solution is already linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable to store the best enjoyment seen so far, starting from a very small number. This ensures even negative results are handled correctly.
2. Iterate over each restaurant one by one.
3. For each restaurant, compute its effective enjoyment. If its time is less than or equal to the allowed limit, use its base enjoyment directly. Otherwise subtract the overflow `(t_i - k)` from its base value. This directly matches the problem’s rule.
4. Compare this computed value with the current best value and update the best value if the new one is larger.
5. After processing all restaurants, output the best value found.

### Why it works

Each restaurant contributes exactly one candidate value that depends only on its own parameters and the global constant `k`. Since there are no interactions between choices, the optimal solution must be the maximum over all individually computed adjusted values. The algorithm maintains the invariant that after processing the i-th restaurant, the stored best value equals the maximum adjusted enjoyment among the first i restaurants. This invariant guarantees correctness because it is preserved by comparing the current candidate against the stored maximum at every step.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    best = -10**18

    for _ in range(n):
        f, t = map(int, input().split())
        if t <= k:
            val = f
        else:
            val = f - (t - k)
        if val > best:
            best = val

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. The key detail is using a very small initial value for `best`, since valid answers can be negative and we must not clamp the result. Each iteration computes the adjusted enjoyment exactly as defined, with a conditional split based on whether the time exceeds the limit.

The subtraction is carefully structured as `f - (t - k)` rather than `f - t + k` only for clarity, although both are equivalent. This reduces the chance of sign mistakes during implementation.

## Worked Examples

We use the provided sample and an additional constructed case.

### Sample 1

Input:

```
2 5
3 3
4 5
```

| Restaurant | f | t | Calculation | Value | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | within limit | 3 | 3 |
| 2 | 4 | 5 | within limit | 4 | 4 |

The second restaurant gives higher enjoyment, so the answer is 4.

This trace shows the invariant clearly: after each step, we maintain the best value among processed restaurants.

### Sample 2 (constructed)

Input:

```
3 4
10 6
7 3
5 10
```

| Restaurant | f | t | Calculation | Value | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 6 | 10 - (6 - 4) = 8 | 8 | 8 |
| 2 | 7 | 3 | within limit | 7 | 8 |
| 3 | 5 | 10 | 5 - (10 - 4) = -1 | -1 | 8 |

The first restaurant sets a high adjusted value, and later entries do not exceed it. This confirms that even negative results are correctly handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each restaurant is processed once with constant-time arithmetic |
| Space | O(1) | Only a single variable is used for tracking the maximum |

The constraints allow up to ten thousand restaurants, and a single linear pass with simple arithmetic comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve() if solve() is not None else "").strip()

# provided sample
assert run("2 5\n3 3\n4 5\n") == "4", "sample 1"

# all within limit
assert run("3 10\n5 1\n6 2\n7 3\n") == "7", "all within limit"

# all exceed limit
assert run("2 5\n10 10\n8 9\n") == "5", "penalized values"

# mixed positive and negative results
assert run("3 4\n1 10\n2 3\n3 20\n") == "2", "mixed case"

# single element
assert run("1 5\n100 10\n") == "95", "single restaurant"

# large k trivial case
assert run("2 100\n1 50\n2 60\n") == "2", "large k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all within limit | 7 | basic max selection |
| all exceed limit | 5 | penalty handling |
| mixed values | 2 | negative and positive mix |
| single restaurant | 95 | base correctness |
| large k | 2 | no penalties when k is large |

## Edge Cases

When all restaurants exceed the time limit, the algorithm still works because it computes a reduced value for each option and compares them directly. For example, with `k = 5` and a restaurant `(f=10, t=10)`, the value becomes `10 - 5 = 5`. The maximum over such transformed values is still correctly selected.

When some adjusted values become negative, the initialization of `best` as a very small number ensures these are still considered. For instance, with input:

```
2 3
1 10
2 10
```

the computed values are `1 - 7 = -6` and `2 - 7 = -5`. The algorithm correctly returns `-5`, since it tracks the maximum even among negatives.
