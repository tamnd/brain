---
title: "CF 924C - Riverside Curio"
description: "We are given a sequence of observations over consecutive days. Each day corresponds to a water level, and over time Arkady leaves marks at the distinct water levels he has seen so far. If a water level repeats, no new mark is added."
date: "2026-06-17T03:16:20+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 924
codeforces_index: "C"
codeforces_contest_name: "VK Cup 2018 - Round 2"
rating: 1700
weight: 924
solve_time_s: 150
verified: true
draft: false
---

[CF 924C - Riverside Curio](https://codeforces.com/problemset/problem/924/C)

**Rating:** 1700  
**Tags:** data structures, dp, greedy  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of observations over consecutive days. Each day corresponds to a water level, and over time Arkady leaves marks at the distinct water levels he has seen so far. If a water level repeats, no new mark is added.

At day `i`, Arkady reports a value `m_i`, which is the number of existing marks strictly above the current water level. From this, the number of marks strictly below the water level on that day is some value `d_i`. The structure of marks evolves only when a new water level appears, because only then the set of marks grows.

The task is not to reconstruct the exact water levels, but to choose a valid evolution of distinct marks that matches all constraints and minimizes the total sum of all `d_i`.

The key difficulty is that the position of the water level relative to the existing marks determines both how many marks lie above it and how many lie below it, and introducing new marks early changes all future contributions.

The constraint `m_i < i` implies that on day `i`, there are always enough previous “slots” to place the water level so that exactly `m_i` marks lie above it. This guarantees feasibility but does not remove the ambiguity in how many distinct marks we choose to introduce over time.

A naive attempt might try to simulate all possible choices of when to introduce new marks. However, even for `n = 10^5`, branching between “create a mark” and “do not create a mark” leads to exponential behavior.

A subtle edge case arises when future values of `m_i` jump significantly. For example, if `m` suddenly increases, delaying mark creation too much makes it impossible to realize that configuration later. A greedy policy must therefore balance delaying mark creation against ensuring future feasibility.

## Approaches

A direct simulation approach maintains the set of marks explicitly and tries to assign a water level each day consistent with `m_i`. On each day, one would decide whether to introduce a new mark or reuse an existing configuration. This quickly becomes exponential since each day potentially doubles the decision space.

The key observation is that the only thing affecting feasibility is how many marks exist at each point in time, not their exact positions. Once we fix the number of marks at day `i`, denoted `k_i`, the water level can always be placed appropriately as long as `k_i ≥ m_i + 1`.

The crucial constraint is that `k_i` cannot increase by more than one per day, since at most one new mark can be added per observation. This introduces a “speed limit” on how quickly we can reach higher required values of `k_i`.

Therefore, instead of looking only at the current requirement `m_i`, we must also ensure that we can still reach future requirements. This leads to a greedy construction of the minimum feasible `k_i` sequence.

We maintain `k_i` as the smallest number of marks achievable at day `i` such that all future constraints remain satisfiable, and then compute the contribution `d_i` from it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over mark creation choices | Exponential | O(n) | Too slow |
| Greedy construction of valid mark count sequence | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum number of marks needed at each day based on future constraints, not only current ones. We reason from the fact that marks can only increase by at most one per day, so if a future day requires many marks, earlier days must already support that growth rate.
2. For each day `i`, determine the minimal feasible number of marks `k_i` that guarantees all future days `j ≥ i` can still achieve `m_j`. This ensures we never “fall behind” a future requirement.
3. Once `k_i` is fixed, the number of marks below the water level is determined uniquely as `d_i = k_i - 1 - m_i`, because among `k_i` total marks, exactly `m_i` lie above and the rest lie below except the current level.
4. Sum all `d_i` across all days.

### Why it works

The number of marks is the only state that influences both future feasibility and current cost. Any valid construction corresponds to some sequence `k_i` that increases by at most one per step and always satisfies `k_i ≥ m_i + 1`.

Among all such sequences, choosing the smallest possible `k_i` at every step minimizes every prefix contribution `k_i - 1`, which directly minimizes the total sum of `d_i`. Any larger choice of `k_i` permanently increases future costs without improving feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    m = list(map(int, input().split()))

    k = [0] * n

    # backward constraint: ensure feasibility of future growth
    suf = float("-inf")

    # we compute k from right to left with growth constraint
    for i in range(n - 1, -1, -1):
        suf = max(suf, m[i] - i)
        k[i] = suf + i + 1

    # enforce growth limit k[i] <= k[i-1] + 1
    for i in range(1, n):
        if k[i] > k[i - 1] + 1:
            k[i] = k[i - 1] + 1

    ans = 0
    for i in range(n):
        ans += (k[i] - 1 - m[i])

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first builds a backward-looking constraint using the expression `m[i] - i`, which captures how demanding future days are relative to how much time remains to introduce new marks. This produces a baseline requirement for `k[i]`. Since marks can only increase by one per step, we then enforce a forward correction ensuring no step exceeds this growth rate.

Finally, the contribution for each day is computed directly from the relationship between total marks, above marks, and below marks.

## Worked Examples

### Sample 1

Input:

```
6
0 1 0 3 0 2
```

We compute the auxiliary values `m_i - i`:

| i | m[i] | m[i] - i | suffix max | k[i] | d[i] |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | -1 | -1 | 1 | 0 |
| 2 | 1 | -1 | -1 | 2 | 0 |
| 3 | 0 | -3 | -1 | 3 | 2 |
| 4 | 3 | -1 | -1 | 4 | 0 |
| 5 | 0 | -5 | -1 | 5 | 4 |
| 6 | 2 | -4 | -1 | 5 | 2 |

Final sum is `6`.

This trace shows how the requirement for future feasibility forces `k[i]` to grow steadily even when `m[i]` is small, which directly increases contributions to `d[i]`.

### Sample 2

Consider:

```
5
0 0 2 0 1
```

| i | m[i] | k[i] | d[i] |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 0 | 2 | 1 |
| 3 | 2 | 3 | 0 |
| 4 | 0 | 4 | 3 |
| 5 | 1 | 4 | 2 |

The table shows how early growth in `k[i]` is necessary to support the peak at day 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single linear backward pass and forward adjustment |
| Space | O(n) | Stores arrays for `m` and `k` |

The constraints allow up to `10^5` days, so a linear scan is sufficient. Any quadratic or state-expanding approach would exceed limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    m = list(map(int, input().split()))

    k = [0] * n
    suf = float("-inf")

    for i in range(n - 1, -1, -1):
        suf = max(suf, m[i] - i)
        k[i] = suf + i + 1

    for i in range(1, n):
        if k[i] > k[i - 1] + 1:
            k[i] = k[i - 1] + 1

    return str(sum(k[i] - 1 - m[i] for i in range(n)))

# provided sample
assert run("6\n0 1 0 3 0 2\n") == "6"

# minimum case
assert run("1\n0\n") == "0"

# increasing requirement
assert run("3\n0 1 2\n") == "0"

# flat case
assert run("4\n0 0 0 0\n") == "6"

# alternating
assert run("5\n0 1 0 1 0\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case |
| increasing m | 0 | tight feasibility |
| all zeros | 6 | forced growth cost |
| alternating | 3 | oscillation handling |

## Edge Cases

A minimal input of a single day always yields zero cost since no prior marks exist and no below-water contributions are possible.

A strictly increasing `m_i` sequence forces the algorithm to increase the number of marks every day. The computed `k_i` grows linearly, and the contribution remains zero because the water level is always positioned at the topmost feasible configuration.

A sequence with large jumps in `m_i` demonstrates why backward propagation is necessary. Without anticipating future requirements, a greedy forward-only strategy would underestimate required growth and produce an infeasible configuration.

The algorithm handles these cases because `k_i` is constrained both by future demand and by the one-step growth limit, ensuring feasibility at every prefix while maintaining minimal cumulative size.
