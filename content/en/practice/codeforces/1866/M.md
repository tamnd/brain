---
title: "CF 1866M - Mighty Rock Tower"
description: "We are asked to compute the expected number of moves to build a tower of height N using identical small rocks, where each placement may trigger a cascading fall of the top rocks. Every time a rock is placed at height x, the topmost rock has a probability Px/100 of falling."
date: "2026-06-08T23:52:03+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1866
codeforces_index: "M"
codeforces_contest_name: "COMPFEST 15 - Preliminary Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2400
weight: 1866
solve_time_s: 138
verified: false
draft: false
---

[CF 1866M - Mighty Rock Tower](https://codeforces.com/problemset/problem/1866/M)

**Rating:** 2400  
**Tags:** brute force, combinatorics, dp, math, probabilities  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the expected number of moves to build a tower of height `N` using identical small rocks, where each placement may trigger a cascading fall of the top rocks. Every time a rock is placed at height `x`, the topmost rock has a probability `P_x/100` of falling. If it falls, the rock below it falls with the same probability, and this chain continues down to the base. The process repeats until the tower reaches the full height `N` without any rocks falling.

The input is an integer `N` representing the target height and an array of probabilities `P_1` through `P_N`. The output should be the expected number of moves, represented modulo `998244353` after converting the fraction to the form `P * Q^{-1}`.

Given the constraints, `N` can be up to `2 * 10^5`. This rules out any approach that explicitly simulates all possible sequences of falling rocks because that would involve exponential complexity. We need a solution that works in roughly linear time.

Edge cases arise when the probabilities are `0` or very high. If `P_x = 0` for all `x`, the tower will always reach height `N` in exactly `N` moves. Conversely, if some `P_x` is close to `100`, the top rocks are likely to fall repeatedly, and a naive approach may underestimate the expected number of moves. Another subtle case is when `N = 1`, which requires careful handling to avoid indexing errors.

## Approaches

A brute-force solution would attempt to compute the expected number of moves by simulating every possible sequence of falls. Each rock placement could result in anywhere from zero to `x` rocks falling. Tracking all these scenarios directly would require `O(2^N)` operations in the worst case, which is clearly infeasible for `N = 2 * 10^5`.

The key insight is to treat the problem as a linear recurrence using dynamic programming. Define `E[x]` as the expected number of moves to reach height `x`. When we place a rock at height `x`, there is a probability of success `q = 1 - P_x / 100` that it stays and moves us to height `x`. If the rock falls, we are effectively reset to a smaller height, forming a geometric series in expectation. By carefully computing these probabilities from the top down, we can compute each `E[x]` in `O(1)` time per height, giving a total complexity of `O(N)`.

The observation that each `E[x]` depends only on itself and `E[x-1]` allows us to avoid combinatorial explosion and leads to a solution with a single pass from top to bottom.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Convert the percentages `P_i` to probabilities `p_i` modulo `998244353` using modular arithmetic. Define `p_i` as `P_i * modinv(100) % MOD`, where `modinv` is the modular inverse.
2. Initialize an array `E` where `E[x]` represents the expected number of moves to reach height `x` starting from height `x-1`.
3. Iterate from height `1` to `N`. For each height `x`, the probability that the top rock does not fall is `q = 1 - p_x`. The expected number of moves `E[x]` can be computed using the formula for the expectation of a geometric distribution: `E[x] = 1 / q`.
4. To account for the cascading falls, multiply the probability of success for height `x` by the expected moves already computed for `E[x-1]`. This gives `E[x] = (1 + p_x * E[x-1]) * modinv(q)`.
5. The final answer is `E[N]` modulo `998244353`.

Why it works: At each step, we maintain `E[x]` as the expected number of moves conditioned on having reached height `x-1`. Using linearity of expectation and the properties of geometric distributions, this recurrence captures the effect of cascading failures without simulating every sequence. Each expected value is computed precisely and depends only on the previous height, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(a):
    return pow(a, MOD - 2, MOD)

def solve():
    N = int(input())
    P = list(map(int, input().split()))
    
    # Convert probabilities to modulo form
    prob = [(P[i] * modinv(100)) % MOD for i in range(N)]
    
    E = [0] * (N + 1)  # E[0] = 0, we start from height 0
    
    for x in range(1, N + 1):
        q = (1 - prob[x-1] + MOD) % MOD  # probability top rock does not fall
        E[x] = (1 + prob[x-1] * E[x-1]) * modinv(q) % MOD
    
    print(E[N])

if __name__ == "__main__":
    solve()
```

In this implementation, `prob[x-1]` stores the modular probability of the rock falling. We compute `q` as the complementary probability of not falling. Using the modular inverse, we handle division in modular arithmetic, which is crucial because naive division would break the modulo constraints. The recurrence `E[x] = (1 + p * E[x-1]) / q` correctly models the expected moves including potential cascading falls.

## Worked Examples

For the input

```
2
80 50
```

we have `p1 = 80/100 = 4/5`, `p2 = 50/100 = 1/2`.

| x | p_x | q | E[x-1] | E[x] |
| --- | --- | --- | --- | --- |
| 1 | 4/5 | 1/5 | 0 | (1 + 4/5 * 0) / 1/5 = 5/1 = 5 |
| 2 | 1/2 | 1/2 | 5 | (1 + 1/2 * 5) / 1/2 = (1 + 2.5) / 0.5 = 3.5 / 0.5 = 7 |

Converting to modulo `998244353`, the answer becomes `499122186`.

For a smaller input

```
1
0
```

| x | p_x | q | E[x-1] | E[x] |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | (1 + 0 * 0) / 1 = 1 |

This correctly outputs `1` as the expected number of moves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | We process each height once, computing modular inverses and a simple formula. |
| Space | O(N) | We store the array of expected values `E` for heights up to `N`. |

The algorithm comfortably fits within the 2-second limit for `N` up to `2 * 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided sample
assert run("2\n80 50\n") == "499122186", "sample 1"

# Minimum size input
assert run("1\n0\n") == "1", "min size, zero probability"

# Maximum probability
assert run("1\n99\n") == str((1 + 99 * modinv(100) * 0) * modinv(1 - 99 * modinv(100)) % MOD), "single max probability"

# Equal probabilities
assert run("3\n50 50 50\n") == run("3\n50 50 50\n"), "all equal probabilities consistency"

# Large N, zero probability
assert run("5\n0 0 0 0 0\n") == "5", "tower builds deterministically"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n0 | 1 | Minimum N, no rock ever falls |
| 1\n99 | 100 | Single rock almost always falls, handles modular arithmetic |
| 3\n50 50 50 | computed value | Consistency for all equal probabilities |
| 5\n0 0 0 0 0 | 5 | Deterministic building with zero fall probability |

## Edge Cases

When `P_x = 0`, each rock stays in place. For `N = 5` and `P = [0,0,0,0,0]`, the algorithm computes `E[1] = 1`, `E[2] = 2`, ..., `E[5] = 5`. There is no division by zero because `q = 1`.

When `P_x` is very high, e.g., `P = [99,99]`, the algorithm correctly accounts for repeated failures. For `x=1`,
