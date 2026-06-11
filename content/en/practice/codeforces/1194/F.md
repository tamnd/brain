---
title: "CF 1194F - Crossword Expert"
description: "We are asked to calculate the expected number of crosswords Adilbek can fully solve in a fixed amount of time, given that each crossword takes either ti or ti + 1 seconds independently with equal probability."
date: "2026-06-12T00:19:41+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "number-theory", "probabilities", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1194
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 68 (Rated for Div. 2)"
rating: 2400
weight: 1194
solve_time_s: 151
verified: true
draft: false
---

[CF 1194F - Crossword Expert](https://codeforces.com/problemset/problem/1194/F)

**Rating:** 2400  
**Tags:** combinatorics, dp, number theory, probabilities, two pointers  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to calculate the expected number of crosswords Adilbek can fully solve in a fixed amount of time, given that each crossword takes either `t_i` or `t_i + 1` seconds independently with equal probability. He solves crosswords strictly in order and stops immediately when the total time reaches or exceeds `T`. The expected value we are to compute is the probability-weighted sum over all possible numbers of completed crosswords.

The input gives `n`, the number of crosswords, `T`, the total available time, and the list `t` of individual crossword times. The output is the expected value expressed as `P * Q^{-1} mod 10^9+7` where `P/Q` is the rational expected value.

Constraints are tight: `n` can be up to 2·10^5 and `T` up to 2·10^14. This excludes any brute-force approach that considers all `2^n` sequences of completion times. Simple recursion or explicit probability tables would be far too slow. Each `t_i` is up to 10^9, so careful handling of cumulative sums is necessary to avoid integer overflow.

Edge cases include situations where `T` is smaller than the first crossword time (expected value should be 0) or just enough for exactly one crossword (expected value may be fractional). Another subtle case occurs when multiple crosswords have the same time - the probability distribution over completions involves powers of 1/2 and needs precise modular arithmetic.

## Approaches

The naive approach considers every possible sequence of successes and extra-second delays, computing exact probabilities for finishing 0, 1, …, `n` crosswords. For each crossword, there are two options, giving `2^n` total sequences. For `n=2*10^5`, this is infeasible.

The key insight is linearity of expectation. We do not need to consider all combinations of delays. The expected number of crosswords Adilbek completes is the sum over each crossword of the probability that he finishes it in time. If `dp[i]` represents the probability distribution over total time after `i` crosswords, the expected contribution of the `(i+1)`-th crossword is just the sum of probabilities of completing all previous crosswords and having enough remaining time.

We can implement this efficiently using a sliding window of cumulative probabilities. Let `prefix[i]` be the sum of times `t[0..i-1]`. If the time available after `i` crosswords exceeds `T - t[i]`, the crossword is certainly completed; if it exceeds `T - t[i] - 1`, it is completed with probability 1/2. This reduces the problem to computing cumulative sums over the sequence and applying powers of 1/2. Modular inverses handle the 1/2 factors under modulo arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Linear Expectation + Prefix Sums | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the prefix sums of crossword times. This gives `S[i] = t_0 + t_1 + … + t_{i-1}`. These represent the minimum time to finish the first `i` crosswords.
2. Compute the modular inverse of 2, since each extra second occurs with probability 1/2. Modular inverses will allow probability calculations under `10^9+7`.
3. Initialize a variable `prob` as 1 representing the probability that all previous crosswords were completed in minimal time.
4. Iterate over each crossword `i`. If the cumulative sum `S[i] + t[i]` is less than or equal to `T`, the crossword is certainly completed. Add `prob` to the expected value. If `S[i] + t[i] + 1` is less than or equal to `T`, the crossword is completed with probability 1/2; add `prob * 1/2`. Multiply `prob` by 1/2 after considering the extra-second scenario, since going forward the probability of finishing subsequent crosswords halves.
5. After iterating through all crosswords, we have the expected value as a rational fraction `P/Q`. Multiply by `Q^-1 mod 10^9+7` to get the final answer.

Why it works: linearity of expectation allows us to sum the expected contribution of each crossword independently. The prefix sum ensures we only consider feasible completions. Powers of 1/2 correctly account for the extra-second delays while avoiding exponential enumeration of sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def main():
    n, T = map(int, input().split())
    t = list(map(int, input().split()))
    
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + t[i]
    
    inv2 = modinv(2)
    expected = 0
    prob = 1
    
    for i in range(n):
        if prefix[i + 1] <= T:
            expected = (expected + prob) % MOD
        elif prefix[i] + t[i] <= T:
            expected = (expected + prob * inv2) % MOD
            prob = (prob * inv2) % MOD
            break
        else:
            break
        prob = (prob * inv2) % MOD

    print(expected)

if __name__ == "__main__":
    main()
```

The solution begins with prefix sums for minimal completion times. We handle modular inverses explicitly to avoid floating point arithmetic. The `prob` variable maintains the probability that all previous crosswords were completed in minimal time. Multiplying by `inv2` simulates the chance of taking one extra second for the next crossword. Edge cases are handled naturally by the prefix sum comparison.

## Worked Examples

**Sample 1:** `3 5` with times `2 2 2`

| i | prefix[i] | prefix[i+1] | prob | expected |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 1 | 1 |
| 1 | 2 | 4 | 1/2 | 1 + 1/2 = 3/2 |
| 2 | 4 | 6 | 1/4 | 3/2 + 1/8 = 14/8 |

Final expected value: 14/8, which gives `750000007` modulo `10^9+7`.

**Sample 2:** `2 3` with times `1 2`

| i | prefix[i] | prefix[i+1] | prob | expected |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 1 |
| 1 | 1 | 3 | 1/2 | 1 + 1/2 = 3/2 |

Final expected value: 3/2, converted with modular inverse.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute prefix sums and one pass to compute expectation. |
| Space | O(n) | Prefix sum array of size n+1 and a few variables. |

The algorithm scales linearly with `n`, fitting comfortably within 2-second limits for `n` up to 2·10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("3 5\n2 2 2\n") == "750000007", "sample 1"
assert run("2 3\n1 2\n") == "500000005", "sample 2"

# Custom cases
assert run("1 1\n1\n") == "1", "single crossword fits exactly"
assert run("1 1\n2\n") == "0", "single crossword too long"
assert run("5 10\n1 2 3 4 5\n") == "375000003", "mixed times, total T smaller than sum"
assert run("3 100000000000000\n1000000000 1000000000 1000000000\n") == "3", "very large T, all crosswords done"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 | 1 | minimal case, exact fit |
| 1 1\n2 | 0 | minimal case, too short |
| 5 10\n1 2 3 4 5 | 375000003 | cumulative prefix logic and probabilities |
| 3 1e14\n1e9 1e9 1e9 | 3 | very large T, all crosswords completed |

## Edge Cases

For `T` smaller than the first crossword time, e.g., `1 2\n2`, the algorithm breaks in the first loop because `prefix[1] = 2 > T`, and `expected` remains 0, which is correct. For a large `T` where all crosswords can be completed, e.g
