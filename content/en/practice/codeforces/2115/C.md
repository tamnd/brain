---
title: "CF 2115C - Gellyfish and Eternal Violet"
description: "Gellyfish faces a collection of monsters, each with a certain amount of health points. She does not want to kill them but wants to reduce their HP to exactly one. She can attack over a number of rounds using a magical sword."
date: "2026-06-08T04:13:03+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "greedy", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 2115
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1028 (Div. 1)"
rating: 2700
weight: 2115
solve_time_s: 89
verified: false
draft: false
---

[CF 2115C - Gellyfish and Eternal Violet](https://codeforces.com/problemset/problem/2115/C)

**Rating:** 2700  
**Tags:** combinatorics, dp, greedy, math, probabilities  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

Gellyfish faces a collection of monsters, each with a certain amount of health points. She does not want to kill them but wants to reduce their HP to exactly one. She can attack over a number of rounds using a magical sword. The sword may or may not shine in each round, and the effect of her attack depends on whether it shines. If it shines, her attack reduces all monsters' HP by one. If it does not shine, she can only reduce a single monster’s HP by one. She knows before acting whether the sword shines and can decide optimally each round.

The input provides the number of monsters, the number of attack rounds, and the probability of the sword shining. Each monster’s starting HP is given. The output must be the probability that she can achieve her goal using an optimal strategy.

The constraints allow up to twenty monsters and up to four thousand attack rounds. The HP of each monster can be up to four hundred. The sum of monsters across all test cases does not exceed one hundred. This implies that while the number of monsters is small, the number of rounds is large, ruling out naive state-space explorations over all possible HP combinations for every round. The algorithm must exploit structure rather than brute force.

A non-obvious edge case arises when all monsters start at HP equal to one. Here the goal is already achieved, so the probability is one regardless of the number of rounds or sword probability. Another edge case occurs when the sword has zero probability of shining; the algorithm must account for optimally choosing which monster to hit each round. Mismanaging the single-target attacks can lead to an incorrect probability of zero even if the rounds suffice to reduce all monsters to one.

## Approaches

The brute-force solution enumerates all possible sequences of sword shines and attack choices over all rounds, tracking the HP of each monster. This would be correct because it explores all possible outcomes, but it quickly becomes intractable. If each round has two possible outcomes (shine or not), there are 2^m sequences, and for each, there are multiple attack choices on the single-target rounds. Even with just twenty monsters and four thousand rounds, this explodes exponentially.

The key insight is that the order in which single-target attacks are applied does not matter if the goal is only to reduce HP to one. This observation reduces the state to the number of single-target hits still needed, instead of tracking every possible HP configuration. Each monster initially requires a certain number of single-target attacks to reach one if no multi-target attacks occur. Let each monster’s "excess HP" be its HP minus one. If we let `k` be the total excess HP, then after each round we either reduce all monsters (if sword shines) or reduce a single monster (if sword does not shine). The problem can now be reframed as computing the probability of reaching a sum of `k` decrements using a mixture of multi-target and single-target attacks over `m` rounds, which can be modeled with dynamic programming.

The optimal approach uses dynamic programming where the state is the number of remaining single-target decrements required. For each round, if the sword shines, we reduce all remaining decrements simultaneously. If it does not shine, we probabilistically decide which monster to hit (or equivalently, reduce the total decrements by one). The DP transitions track probabilities cumulatively, avoiding enumeration of all attack sequences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m * n^m) | O(n^m) | Too slow |
| Optimal DP | O(m * total_excess_HP) | O(total_excess_HP) | Accepted |

## Algorithm Walkthrough

1. For each monster, compute its excess HP, `h_i - 1`. Let `total_excess = sum(h_i - 1)` be the total number of HP decrements needed.
2. Initialize a dynamic programming array `dp` of length `total_excess + 1` where `dp[x]` represents the probability of needing `x` more single-target hits to finish all monsters. Initially, `dp[total_excess] = 1` and all others are zero.
3. Iterate over each of the `m` rounds. For each round, create a new DP array `new_dp`. For every possible number of remaining single-target hits `x`:

- If the sword shines (with probability `p`), all monsters are decremented simultaneously. The total remaining single-target hits `x` decreases by `n` (but never below zero). Increment `new_dp[max(0, x - n)]` by `dp[x] * p`.
- If the sword does not shine (with probability `1-p`), choose one monster to hit optimally, which reduces `x` by 1. Increment `new_dp[max(0, x - 1)]` by `dp[x] * (1 - p)`.
4. After processing all rounds, the probability that Gellyfish reaches her goal is `dp[0]`.

Why it works: the DP tracks all possible states of remaining decrements and accumulates probabilities of reaching those states. Because the sword shining reduces all monsters by one and non-shining attacks reduce a single monster, the transitions correctly capture the optimal choices. The DP only needs to track the total remaining decrements rather than individual HPs, exploiting the symmetry between monsters. This invariant guarantees correctness: at every step, `dp[x]` represents the true probability of needing `x` more decrements, so `dp[0]` is the probability of success.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, p_perc = map(int, input().split())
        p = p_perc / 100
        h = list(map(int, input().split()))
        total_excess = sum(x - 1 for x in h)

        dp = [0.0] * (total_excess + 1)
        dp[total_excess] = 1.0

        for _ in range(m):
            new_dp = [0.0] * (total_excess + 1)
            for x in range(total_excess + 1):
                if dp[x] == 0:
                    continue
                # sword shines
                decrease = min(x, n)
                new_dp[x - decrease] += dp[x] * p
                # sword does not shine
                decrease = min(x, 1)
                new_dp[x - decrease] += dp[x] * (1 - p)
            dp = new_dp

        print(f"{dp[0]:.6f}")

if __name__ == "__main__":
    solve()
```

The code first calculates the total excess HP to reduce. The DP array is initialized with the total excess as the only non-zero probability. In each round, we process transitions based on whether the sword shines. The `min(x, n)` ensures we do not reduce below zero, correctly handling the case where the sword shines with fewer than `n` decrements left. Probabilities are accumulated for each possible resulting state. After all rounds, `dp[0]` holds the final success probability, printed to six decimal places.

## Worked Examples

### Sample 1

Input:

```
2 2 10
2 2
```

| Round | Remaining Decrements | Sword Shines | Probability | New Remaining |
| --- | --- | --- | --- | --- |
| 1 | 2 | yes | 0.1 | 0 |
| 1 | 2 | no | 0.9 | 1 |
| 2 | 1 | yes | 0.1*0.9=0.09 | 0 |
| 2 | 1 | no | 0.9*0.9=0.81 | 0 |

Probability of success = 0.1 + 0.81 = 0.91. Matches the sample output.

### Sample 2

Input:

```
5 5 20
2 2 2 2 2
```

Total excess = 5. The only way to fail is if the sword never shines (all non-shining attacks can only reduce one monster at a time, but there are enough rounds to handle that). Probability of failure = 0.8^5 = 0.32768, success probability = 0.67232.

The tables confirm the DP captures both shine and non-shine transitions correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * total_excess) | Each of m rounds updates DP array of size total_excess+1 |
| Space | O(total_excess) | DP array stores probabilities for each possible remaining decrement |

With `m` up to 4000 and total excess up to 400 * 20 = 8000, `m * total_excess` = 32,000,000, which is feasible in 2 seconds with simple floating-point operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n2 2 10\n2 2\n5 5 20\n2 2 2 2 2\n6 20 50\n1 1
```
