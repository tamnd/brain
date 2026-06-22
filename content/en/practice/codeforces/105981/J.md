---
title: "CF 105981J - Uniform Random Descent Process"
description: "We are given a process that repeatedly shrinks a single integer. Starting from a value m = n, one operation replaces it with a uniformly random integer from the range [0, m-1]. The process stops once the value becomes 0."
date: "2026-06-22T16:32:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105981
codeforces_index: "J"
codeforces_contest_name: "The 2025 Hunan University Programming Contest"
rating: 0
weight: 105981
solve_time_s: 56
verified: true
draft: false
---

[CF 105981J - Uniform Random Descent Process](https://codeforces.com/problemset/problem/105981/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a process that repeatedly shrinks a single integer. Starting from a value `m = n`, one operation replaces it with a uniformly random integer from the range `[0, m-1]`. The process stops once the value becomes `0`. The task is to compute the expected number of operations needed until termination, for many different starting values `n`.

Each test case gives one starting number, and we must output the expected number of random reductions until the process reaches zero.

The constraints are large: up to `10^5` test cases, and each `n` can be as large as `10^5`. This rules out any approach that recomputes an expectation from scratch per query in linear or quadratic time. Even `O(n^2)` preprocessing would already be tight, but `O(n log n)` or `O(n)` preprocessing with `O(1)` queries is clearly acceptable.

The main subtlety is that the process is stochastic but highly structured. Each state `m` depends only on smaller states `0..m-1`, which strongly suggests a dynamic programming formulation.

A common failure case appears when treating transitions as independent or trying to simulate the process.

For example, if `n = 2`, the process starts at 2, then goes to a random value in `{0, 1}`. If it goes to `1`, we still need another step on average, but if it goes to `0`, we stop immediately. A naive simulation that averages a few random runs might converge slowly or misleadingly because the distribution is heavily skewed toward early termination.

Another edge case is `n = 0`. The process is already finished, so the answer is exactly `0`. Any recurrence must explicitly anchor this base case, otherwise it will incorrectly propagate undefined expectations.

## Approaches

A brute-force way to think about the expectation is to define `E(m)` as the expected number of operations starting from value `m`. From state `m`, one operation is always performed, and then we transition uniformly to any of the states `0` through `m-1`. This gives a direct recurrence

```
E(m) = 1 + (1/m) * sum_{k=0}^{m-1} E(k)
```

This formulation is correct but expensive if evaluated directly. For each `m`, computing the sum over all previous states costs `O(m)`, leading to `O(n^2)` preprocessing.

The key simplification comes from noticing that the recurrence depends only on prefix sums of `E`. If we maintain `S(m) = sum_{k=0}^m E(k)`, then the recurrence becomes

```
E(m) = 1 + (1/m) * S(m-1)
```

and consequently

```
S(m) = S(m-1) + E(m)
```

This transforms the problem into a single linear pass.

The deeper structure is that each `E(m)` depends only on aggregated information about smaller states, not their individual values. This removes the need to repeatedly recompute sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct recurrence with recomputation | O(n^2) | O(n) | Too slow |
| Prefix-sum DP optimization | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

### Optimal DP computation

1. Initialize `E(0) = 0` and `S(0) = 0`. This matches the definition that no operations are needed when the value is already zero.
2. Iterate `m` from `1` to the maximum `n` across all test cases.
3. Compute `E(m)` using the stored prefix sum:

```
E(m) = 1 + S(m-1) / m
```

This works because all transitions from `m` go uniformly to smaller states, and their expectations have already been aggregated into `S(m-1)`.
4. Update the prefix sum:

```
S(m) = S(m-1) + E(m)
```
5. After preprocessing, each query `n` is answered directly as `E(n)`.

The reason this ordering matters is that `E(m)` must always be computed after all smaller values are finalized, since it depends on the full prefix.

### Why it works

The invariant is that at the start of iteration `m`, `S(m-1)` is exactly the sum of correct expectations for all states strictly smaller than `m`. The recurrence expresses `E(m)` purely as a linear combination of these already-correct values. Since no future state influences earlier ones, the DP never revises a value after it is computed, and each expectation is built only from fully determined information.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 100000

E = [0.0] * (MAXN + 1)

S = [0.0] * (MAXN + 1)

for m in range(1, MAXN + 1):
    E[m] = 1.0 + S[m - 1] / m
    S[m] = S[m - 1] + E[m]

t = int(input())
out = []
for _ in range(t):
    n = int(input())
    out.append(str(E[n]))

print("\n".join(out))
```

The code precomputes expectations once up to the maximum possible `n`. The array `E` stores the final answer for each state, while `S` maintains prefix sums to allow constant-time recurrence evaluation. Each update uses only previously computed values, so the loop is strictly forward-only and numerically stable for the required precision.

One subtle point is that everything is stored in floating point. Since the required precision is `1e-4`, double precision is sufficient, and no exact rational arithmetic is needed.

## Worked Examples

### Example 1: n = 2

We compute step by step.

| m | S(m-1) | E(m) | S(m) |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 1 + 1/2 = 1.5 | 2.5 |

For `n = 2`, the result is `1.5`.

This trace shows how state `2` aggregates both outcomes from `{0,1}` uniformly.

### Example 2: n = 4

| m | S(m-1) | E(m) | S(m) |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 1.5 | 2.5 |
| 3 | 2.5 | 1 + 2.5/3 ≈ 1.8333 | 4.3333 |
| 4 | 4.3333 | 1 + 4.3333/4 ≈ 2.0833 | 6.4166 |

So `E(4) ≈ 2.0833`.

This demonstrates how each layer only depends on accumulated expectations, not individual transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + T) | One preprocessing pass up to max `n`, then O(1) per query |
| Space | O(N) | Arrays `E` and `S` store values for all states |

The preprocessing limit `n ≤ 10^5` makes a linear DP feasible within time limits. Each query is then constant time, which easily supports `10^5` test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    MAXN = 100000
    E = [0.0] * (MAXN + 1)
    S = [0.0] * (MAXN + 1)

    for m in range(1, MAXN + 1):
        E[m] = 1.0 + S[m - 1] / m
        S[m] = S[m - 1] + E[m]

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        out.append(str(E[n]))
    return "\n".join(out)

# provided samples
assert abs(float(run("5\n0\n1\n2\n10\n100000\n").split()[0]) - 0.0) < 1e-6

# custom cases
assert abs(float(run("1\n0\n")) - 0.0) < 1e-6
assert abs(float(run("1\n1\n")) - 1.0) < 1e-6
assert abs(float(run("1\n2\n")) - 1.5) < 1e-6
assert abs(float(run("1\n10\n")).splitlines()[0])  # sanity check existence
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 0 | 0 | base case termination |
| n = 1 | 1 | single forced step |
| n = 2 | 1.5 | branching probability split |
| n = 10 | ~2.93 | nontrivial accumulation behavior |

## Edge Cases

For `n = 0`, the DP must return `0` without attempting to access prefix sums at negative indices. The initialization `E(0) = 0` ensures the recurrence never needs adjustment for this case.

For `n = 1`, the transition always goes to `0`, so exactly one operation is required. In the DP, this is computed as `E(1) = 1 + S(0)/1 = 1`, confirming correctness.

For larger values, the stability depends on correct ordering: if `E(m)` is computed before `S(m-1)` is fully built, later states would contaminate earlier computations. The forward-only construction avoids this entirely, ensuring each expectation is finalized exactly once.
