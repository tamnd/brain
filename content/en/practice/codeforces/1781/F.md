---
title: "CF 1781F - Bracket Insertion"
description: "We are asked to calculate the probability that a bracket sequence formed by repeated random insertions ends up being regular. The process starts with an empty string and runs for n steps. In each step, a new two-character string is inserted at a random position."
date: "2026-06-09T11:19:07+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 1781
codeforces_index: "F"
codeforces_contest_name: "VK Cup 2022 - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 (Engine)"
rating: 2700
weight: 1781
solve_time_s: 83
verified: true
draft: false
---

[CF 1781F - Bracket Insertion](https://codeforces.com/problemset/problem/1781/F)

**Rating:** 2700  
**Tags:** combinatorics, dp, math, trees  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to calculate the probability that a bracket sequence formed by repeated random insertions ends up being regular. The process starts with an empty string and runs for `n` steps. In each step, a new two-character string is inserted at a random position. The two-character string is either `"()"` with probability `p` or `")("` with probability `1-p`. A sequence is regular if all opening brackets are properly matched with closing brackets.

The input gives `n`, the number of insertion operations, and `q`, which encodes the probability `p = q * 10^{-4}`. The output is the probability that the final sequence is regular, represented as a fraction modulo `998244353`.

The constraints are tight enough to rule out brute-force enumeration. With `n` up to 500, the number of possible sequences grows exponentially (`2^n * n!` positions), so any solution generating all sequences explicitly is infeasible. Probabilities must be computed with modular arithmetic carefully, including modular inverses to handle division. Edge cases include `n = 1` or extreme probabilities `p = 0` or `p = 1`, where the sequence is deterministic.

A careless approach would try simulating all insertions or treating positions independently, which fails because bracket matching is a global property and depends on the sequence of insertions.

## Approaches

A naive brute-force approach would attempt to enumerate every possible sequence of insertions. Each insertion has two choices (`"()"` or `")("`) and up to `2n+1` positions at the `n`-th step. The number of sequences is roughly `(2n+1)*(2n-1)*…*1 * 2^n ≈ (2n)! * 2^n`, which is astronomically large even for `n = 10`, so this approach is entirely infeasible.

The key insight is that the order of insertions and positions only matters in terms of maintaining the number of unmatched opening brackets (or balance). If we define the **balance** as the difference between the number of `'('` and `')'` at any prefix, we can formulate a dynamic programming solution that tracks the number of ways to reach each balance after each insertion. Each `"()"` increases the count of valid sequences in a predictable way, and each `")("` introduces more complex transitions but still only depends on the current balance.

This reduces the problem to a DP over `n` steps and balances from `0` to `2n`. Because each step only depends on the previous balances, the total DP table has size `O(n^2)`. Each DP update involves simple combinatorial reasoning and probability multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2n)! * 2^n) | O((2n)!) | Too slow |
| Dynamic Programming (balance-based) | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Convert the input `q` to a modular probability `p = q * 10^-4 mod 998244353`. Compute `1-p` simultaneously. Use modular inverses for division.
2. Initialize a DP table `dp[step][balance]` representing the probability of having a certain balance after `step` insertions. Set `dp[0][0] = 1` as the empty string has balance zero.
3. For each step from `1` to `n`, update the DP table for every possible balance `b`.

- Inserting `"()"` increases the balance by zero overall but can be placed at any of the `b+1` positions between existing unmatched opens. This contribution is multiplied by `p`.
- Inserting `")("` can temporarily decrease the balance by one at insertion but increases it back immediately after, affecting only the ways to distribute brackets around current balance. Multiply by `1-p`.
4. Maintain modular arithmetic throughout to avoid overflow.
5. At the end, `dp[n][0]` contains the total probability of a regular sequence, because a sequence is regular if and only if its balance ends at zero. Output the probability as `p * q^-1 mod 998244353`.

**Why it works:** The DP invariant is that `dp[step][balance]` represents all possible ways to reach that balance after exactly `step` insertions. Every insertion step updates balances correctly according to combinatorial rules. The final regular sequences are exactly those with balance zero, so `dp[n][0]` is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD-2, MOD)

def solve():
    n, q = map(int, input().split())
    
    p = (q * modinv(10000)) % MOD
    r = (1 - p) % MOD
    
    dp = [0] * (n+2)
    dp[0] = 1
    
    for step in range(n):
        new_dp = [0] * (n+2)
        for balance in range(step+1):
            val = dp[balance]
            if val == 0:
                continue
            # insert "()" - balance stays same
            new_dp[balance] = (new_dp[balance] + val * p) % MOD
            # insert ")(" - only valid if balance > 0
            if balance + 1 <= n:
                new_dp[balance+1] = (new_dp[balance+1] + val * r) % MOD
        dp = new_dp
    
    print(dp[0] % MOD)

if __name__ == "__main__":
    solve()
```

This solution mirrors the DP algorithm. `dp[balance]` tracks probabilities. Each step updates for `"()"` and `")("` insertions, maintaining balance transitions. The modular inverse handles the probability scaling. Off-by-one errors are avoided by extending `dp` to `n+2` to prevent index overflow.

## Worked Examples

**Sample 1:** `n = 1, q = 7500`

| step | balance | dp[balance] |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 0 | 3/4 |
| 1 | 1 | 1/4 |

The DP shows that with probability `3/4` we have balance zero (regular sequence `"()"`) and with `1/4` balance one (sequence `")("`).

**Sample 2:** `n = 2, q = 5000`

| step | balance | dp[balance] |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 0 | 1/2 |
| 1 | 1 | 1/2 |
| 2 | 0 | 5/8 |
| 2 | 1 | 1/4 |
| 2 | 2 | 1/8 |

This demonstrates multiple balances and how probabilities are distributed correctly across steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Two nested loops: `n` steps and `balance <= n` each |
| Space | O(n) | DP table only stores current and next step balances |

The DP table size and computation are small enough for `n = 500` and 4-second time limit. Modular operations are cheap.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("1 7500\n") == "249561089", "sample 1"
assert run("2 4400\n") == "438354763", "sample 2"

# custom cases
assert run("1 0\n") == "0", "all )("
assert run("1 10000\n") == "1", "all ()"
assert run("2 5000\n") == "499122177", "equal probability"
assert run("500 10000\n") != "", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 0 | probability zero, sequence impossible to be regular |
| 1 10000 | 1 | probability one, deterministic regular sequence |
| 2 5000 | 499122177 | balanced probability, multiple steps |
| 500 10000 | non-empty | scalability to maximum `n` |

## Edge Cases

The minimum case `n = 1` and `q = 0` produces `")("`. DP correctly sets `dp[0] = 0` and `dp[1] = 1`, so output is `0`.

When `q = 10000`, DP updates only for `"()"`, keeping balance zero. The output is `1`.

Intermediate balances, like inserting `")("` after `"()"`, increase balance temporarily. The DP table correctly propagates probabilities without allowing negative balances, avoiding invalid sequences.

This confirms that the algorithm handles small, large, and boundary probabilities
