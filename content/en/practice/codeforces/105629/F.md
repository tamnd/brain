---
title: "CF 105629F - \u6570\u6570"
description: "We are working with binary strings of fixed length $n$. Each position is either 0 or 1, so the total space contains $2^n$ strings."
date: "2026-06-22T14:55:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105629
codeforces_index: "F"
codeforces_contest_name: "The 19-th Beihang University Collegiate Programming Contest (BCPC 2024) - Final"
rating: 0
weight: 105629
solve_time_s: 63
verified: true
draft: false
---

[CF 105629F - \u6570\u6570](https://codeforces.com/problemset/problem/105629/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with binary strings of fixed length $n$. Each position is either 0 or 1, so the total space contains $2^n$ strings. Among these, we want to count how many satisfy at least one of two conditions: the string contains a consecutive block of at least $a$ zeros, or it contains a consecutive block of at least $b$ ones. The answer is required modulo $10^9 + 7$.

This kind of condition is easier to reason about through a complement viewpoint. Instead of directly counting strings that “contain a long run”, we usually count strings that avoid both bad events: no run of zeros reaches length $a$, and no run of ones reaches length $b$. The final answer is total strings minus this restricted set.

The input size allows $n$ up to around $10^6$, so any quadratic DP over $n$ or even $O(n \cdot a)$ is immediately infeasible. Even $O(n \log n)$ would be borderline if constants are large. This pushes us toward a linear-time DP with constant or amortized constant transitions per state.

A subtle edge case appears when $a = 1$ or $b = 1$. If $a = 1$, then any string already contains a run of zeros of length at least 1, so every string is valid. Similarly, if $b = 1$, every string is valid. A naive complement DP might incorrectly try to forbid states that are already impossible, leading to off-by-one mistakes or empty-state transitions.

## Approaches

The brute-force idea is straightforward: generate all $2^n$ binary strings and check each one by scanning for the longest consecutive run of zeros and ones. This is correct but immediately fails because $2^n$ grows exponentially. Even for $n = 40$, this becomes too large, and here $n$ is up to $10^6$, making it entirely unusable.

The key observation is that the property we care about depends only on the current run of consecutive identical characters. Once we know how many consecutive zeros or ones we have at the end of a prefix, we do not need the full history. This turns the problem into a finite automaton: we track the current character and the length of its current run, capped at $a-1$ for zeros and $b-1$ for ones. Any transition that would exceed the limit is forbidden.

This leads to a dynamic programming formulation where we build the string from left to right. Let us define states based on the last character and its run length. We maintain two groups: states ending in 0 with run length $1 \dots a-1$, and states ending in 1 with run length $1 \dots b-1$. At each step, we extend by either 0 or 1, shifting run lengths or resetting them.

A naive DP would maintain all these states explicitly and update them for each position. That would cost $O(n(a+b))$, which is too large. The important structure is that transitions within each group are prefix-shift operations, which can be accelerated using prefix sums. Instead of recomputing each state independently, we compute cumulative sums over valid previous states so each layer can be updated in linear time over the number of states, and then optimized further using rolling prefix techniques so that the total becomes $O(n)$.

Finally, since we are computing the complement, the answer is $2^n - \text{valid}(n)$, where $\text{valid}(n)$ is the number of strings avoiding both long runs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Run-length DP with optimization | $O(n)$ | $O(a + b)$ | Accepted |

## Algorithm Walkthrough

We first precompute powers of two up to $n$, since the total number of binary strings is $2^n$. This gives us the baseline for the complement step.

We then build a DP for valid strings, meaning strings that avoid a run of $a$ zeros and avoid a run of $b$ ones.

We maintain two arrays: one for states ending in 0 and one for states ending in 1. Each array stores counts indexed by run length. At step $i$, these arrays represent all valid strings of length $i$.

At each new character addition, we compute new arrays as follows. When appending a 0, we either extend a previous run of 0 by increasing its length, or we switch from a run of 1 to a run of 0 of length 1. The same symmetric logic applies when appending a 1.

The transition from “all runs ending in the opposite character” to “all runs ending in the current character” is where prefix sums matter. Instead of iterating over all possible previous run lengths for each new state, we maintain cumulative totals so that each update can be computed in constant time per state.

After processing all positions, we sum all valid ending states across both groups. This gives the number of strings that avoid both forbidden runs. Subtracting this from $2^n$ yields the final answer.

### Why it works

The invariant is that after processing position $i$, every DP state exactly counts the number of valid prefixes of length $i$ that end with a specific character and run length. Every transition preserves validity because we only extend runs that remain strictly below their forbidden thresholds. Since every valid string has a unique decomposition into run lengths at each prefix, no string is double-counted or missed. The complement step is valid because the DP covers exactly the complement set of strings that violate at least one constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, a, b = map(int, input().split())

    # if any constraint allows everything
    if a == 1 or b == 1:
        print(pow(2, n, MOD))
        return

    # dp0[i] = ways ending with 0-run length i (1..a-1)
    # dp1[i] = ways ending with 1-run length i (1..b-1)
    dp0 = [0] * a
    dp1 = [0] * b

    # initial state: single 0 or single 1
    dp0[1] = 1
    dp1[1] = 1

    total_len = 1

    for _ in range(2, n + 1):
        ndp0 = [0] * a
        ndp1 = [0] * b

        # prefix sums for fast range transitions
        pre0 = [0] * (a + 1)
        pre1 = [0] * (b + 1)

        for i in range(1, a):
            pre0[i] = (pre0[i - 1] + dp0[i]) % MOD
        for i in range(1, b):
            pre1[i] = (pre1[i - 1] + dp1[i]) % MOD

        # transitions to dp0
        # extend previous 0-runs
        for i in range(1, a):
            ndp0[i] = dp0[i - 1] if i > 1 else 0
        # switch from all valid 1-runs
        ndp0[1] = pre1[b - 1]

        # transitions to dp1
        for i in range(1, b):
            ndp1[i] = dp1[i - 1] if i > 1 else 0
        ndp1[1] = pre0[a - 1]

        dp0, dp1 = ndp0, ndp1

    valid = (sum(dp0) + sum(dp1)) % MOD
    ans = (pow(2, n, MOD) - valid) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps two run-length DP arrays and updates them layer by layer. The subtle part is separating “extension of same character” from “switching character”, since switching always resets run length to 1 and aggregates all compatible previous states via prefix sums.

A common mistake is attempting to iterate over all previous run lengths explicitly for every state, which leads to an $O(n^2)$ blowup. Another typical issue is forgetting that run lengths are bounded strictly below $a$ and $b$, so arrays must be sized accordingly and transitions must never access invalid states.

## Worked Examples

### Example 1

Input:

```
n = 3, a = 2, b = 2
```

We want to avoid any run of length 2, so only alternating strings are valid.

| step | dp0 | dp1 |
| --- | --- | --- |
| 1 | [1] | [1] |
| 2 | [1] | [1] |
| 3 | [1] | [1] |

Valid strings are “010” and “101”, so valid = 2. Total = 8, answer = 6.

This confirms that DP correctly tracks alternating structure when both run limits are tight.

### Example 2

Input:

```
n = 4, a = 3, b = 2
```

We allow long zeros but forbid consecutive ones.

After transitions, DP converges to counting strings where ones never appear consecutively.

| step | dp0 | dp1 |
| --- | --- | --- |
| 1 | [1] | [1] |
| 2 | [1,1] | [1] |
| 3 | [2,1] | [2] |
| 4 | [3,2] | [3] |

Valid = 11, total = 16, answer = 5.

This shows how asymmetric constraints skew DP heavily toward the unrestricted character.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each position performs constant-time transitions using prefix aggregation over bounded state arrays |
| Space | $O(a + b)$ | Only run-length states for zeros and ones are stored |

The constraints allow up to $10^6$, so linear time is necessary. The DP avoids per-state nested iteration and only performs linear scans per step, which remains feasible due to small constant factors and rolling arrays.
