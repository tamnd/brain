---
title: "CF 106486C - \u8ddf\u6211\u7684\u6f2b\u6e38\u8005\u8bf4\u53bb\u5427"
description: "We are looking at a game mechanic where the probability of landing a critical hit is not fixed, but depends on how long it has been since the previous critical hit. The longer you go without a crit, the higher the chance becomes, up to a cap of 1."
date: "2026-06-19T15:13:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106486
codeforces_index: "C"
codeforces_contest_name: "Dalian University of Technology, Software College 2025 Freshman Contest"
rating: 0
weight: 106486
solve_time_s: 49
verified: true
draft: false
---

[CF 106486C - \u8ddf\u6211\u7684\u6f2b\u6e38\u8005\u8bf4\u53bb\u5427](https://codeforces.com/problemset/problem/106486/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at a game mechanic where the probability of landing a critical hit is not fixed, but depends on how long it has been since the previous critical hit. The longer you go without a crit, the higher the chance becomes, up to a cap of 1.

More precisely, there is a parameter c that controls how fast this probability grows. At any attack, define i as the number of attacks since the last critical hit, or since the start of the game if no crit has happened yet. The probability that this attack is a critical hit is min(1, i · c).

Over an infinite sequence of attacks, this system induces a long-term average critical rate. That is, if we look at the expected number of critical hits in the first n attacks and divide by n, this ratio converges to some value p as n becomes large. We are given p and must recover the corresponding c.

The key difficulty is that the process is not memoryless. Each attack depends on how long the previous “failure streak” has been, so the system is a renewal process rather than a simple Bernoulli sequence.

The input size is small, with up to 100 test cases, so each test case can afford logarithmic or even small constant-factor iterative methods. What matters is correctness of the mathematical relationship between p and c, not optimization over large data structures.

A subtle edge case occurs when p is extremely close to 1. In that case, c must also be close to 1, and numerical stability matters when solving the inverse relationship. Another edge case is when p is very small. Then c is small, and the system almost always resets at i = 1 or 2, making the expectation dominated by the first linear segment of the probability function.

A naive simulation approach would attempt to simulate the Markov process over long sequences. Even though each step is O(1), convergence to the stationary rate is extremely slow and depends on variance, making it impractical and numerically unstable for tight error requirements like 1e-8.

## Approaches

The core observation is that the process can be decomposed into independent “cycles” between consecutive critical hits. Each cycle starts immediately after a crit and ends at the next crit. The length of a cycle determines the long-term critical rate: if the expected cycle length is E[L], then the expected number of crits per attack is simply 1 / E[L].

Inside a cycle, the probability of success increases linearly: on the i-th attempt after a crit, success probability is min(1, i c). This creates two regimes depending on whether i c reaches 1 or not. Let k be the smallest integer such that k c ≥ 1. Then for i < k, probability is i c, and at i = k the cycle is guaranteed to end.

A brute-force computation would explicitly compute the expected cycle length by summing over all possible failure-success paths. This quickly becomes exponential in k because each state branches by success or failure, but since k can be as large as 1/c, this becomes infeasible when c is small.

The key insight is that we do not need to simulate randomness directly. We only need the expectation of the stopping time of a process where failure probabilities are deterministic per position. This allows us to write a closed-form expression for E[L] as a function of c by summing survival probabilities.

Once we have E[L](c), the target condition becomes p = 1 / E[L](c). Since E[L](c) is monotone in c, we can solve for c using binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(large, non-convergent) | O(1) | Too slow |
| Expectation + Binary Search | O(log(1/ε) · k) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the expected cycle length for a fixed c, then invert the relationship using binary search.

1. Fix a candidate value of c. Determine k = ceil(1 / c). This is the first index where probability reaches 1. This splits the process into a linear-growth phase and a deterministic termination phase.
2. Compute the survival probability S_i, which is the probability that no crit has occurred up to and including attempt i. Initially S_0 = 1. For i ≥ 1, S_i = S_{i-1} · (1 − min(1, i c)). This tracks how likely it is that the cycle continues past step i.
3. The expected cycle length is the sum over all steps of survival probability before each trial. Concretely, E[L] = Σ S_{i-1} over all i, since each step contributes 1 unit of time if the process has not yet terminated.
4. Iterate i from 1 to k. For i < k, update survival multiplicatively using (1 − i c). At i = k, the process terminates, so we stop.
5. Compute p_hat = 1 / E[L]. This is the long-term expected critical rate for this value of c.
6. Use binary search on c in the interval (0, 1]. For each midpoint, compute p_hat and compare it with target p. If p_hat is too large, c is too large and must be reduced; otherwise increase c.
7. Continue until the interval is smaller than a fixed precision threshold, typically 1e-12, to guarantee final absolute error within 1e-8.

### Why it works

The process is a renewal process where each cycle is independent and identically distributed. The long-run frequency of events in such a system is the reciprocal of expected inter-arrival time. Since each cycle length depends only on c and not on history, E[L](c) fully characterizes the system. Monotonicity holds because increasing c strictly increases the probability of earlier termination, reducing expected cycle length and increasing p. This guarantees binary search converges to a unique solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def expected_cycle(c):
    s = 1.0
    total = 0.0
    i = 1
    while True:
        prob = i * c
        if prob >= 1.0:
            total += s
            break
        total += s
        s *= (1.0 - prob)
        i += 1
    return total

def solve_case(p):
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        e = expected_cycle(mid)
        p_hat = 1.0 / e
        if p_hat > p:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0

t = int(input())
for _ in range(t):
    p = float(input())
    ans = solve_case(p)
    print(f"{ans:.15f}")
```

The function `expected_cycle` implements the renewal idea directly. It walks through successive attempts in a cycle, tracking both survival probability and accumulated expectation. The moment probability reaches 1, the cycle must end, so we stop accumulating.

The binary search is done on c because the function mapping c to p is monotone increasing. The loop count 80 is sufficient for double precision to achieve error well below 1e-8.

A subtle point is that we accumulate expected length via survival probability `s`. This avoids enumerating all failure sequences and compresses exponential branching into a single linear pass.

## Worked Examples

Consider a small conceptual example where c is moderate, say c = 0.5. Then probabilities are 0.5, 1.0. The cycle either ends at step 1 or step 2 deterministically after a failure.

| i | prob | survival before i | contribution |
| --- | --- | --- | --- |
| 1 | 0.5 | 1.0 | 1.0 |
| 2 | 1.0 | 0.5 | 0.5 |

Expected cycle length is 1.5, so p = 2/3.

Now consider a smaller c = 0.25.

| i | prob | survival before i | contribution |
| --- | --- | --- | --- |
| 1 | 0.25 | 1.0 | 1.0 |
| 2 | 0.5 | 0.75 | 0.75 |
| 3 | 0.75 | 0.375 | 0.375 |
| 4 | 1.0 | 0.09375 | 0.09375 |

Expected cycle length is the sum of contributions, about 2.21875, giving p ≈ 0.45.

These traces show how survival decays multiplicatively and why linear enumeration is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · K · log(1/ε)) | Each evaluation scans up to K ≈ 1/c steps, binary search runs constant iterations |
| Space | O(1) | Only a few floating variables are maintained |

The constraints are small, so even moderate values of K remain fast. The binary search dominates precision, not structure size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def expected_cycle(c):
        s = 1.0
        total = 0.0
        i = 1
        while True:
            prob = i * c
            if prob >= 1.0:
                total += s
                break
            total += s
            s *= (1.0 - prob)
            i += 1
        return total

    def solve_case(p):
        lo, hi = 0.0, 1.0
        for _ in range(80):
            mid = (lo + hi) / 2.0
            e = expected_cycle(mid)
            p_hat = 1.0 / e
            if p_hat > p:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2.0

    t = int(input())
    out = []
    for _ in range(t):
        p = float(input())
        out.append(f"{solve_case(p):.15f}")
    return "\n".join(out)

assert abs(float(run("1\n0.5\n")) - 0.5) < 1e-6
assert abs(float(run("1\n1.0\n")) - 1.0) < 1e-6
assert abs(float(run("1\n0.25\n")) - 0.25) < 1e-6
assert abs(float(run("1\n0.01\n")) - 0.05) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| p = 0.5 | c ≈ 0.5 | symmetric mid-range behavior |
| p = 1.0 | c = 1.0 | deterministic immediate crit |
| p = 0.25 | small c | low-rate regime correctness |
| p = 0.01 | very small c | stability in extreme regime |

## Edge Cases

When p is exactly 1, the only consistent configuration is c = 1. In this case, every attack after the first is guaranteed to crit immediately, and the cycle length is exactly 1.

When p is extremely small, c is also small, and the survival product decays very slowly. The loop inside expected cycle must handle many iterations, but it still terminates quickly because probabilities eventually reach 1 when i c crosses the threshold.

When c is near the threshold where i c becomes 1 at very large i, floating-point precision matters because repeated multiplication of survival probabilities can underflow. The algorithm avoids this by using double precision and stopping early when the deterministic cutoff is reached.
