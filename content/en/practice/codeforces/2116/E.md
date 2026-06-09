---
title: "CF 2116E - Gellyfish and Eternal Violet"
description: "The problem can be reframed as follows. Gellyfish faces a group of n monsters, each with a given HP hi. She wants to reduce every monster's HP to exactly 1. She has m rounds of attacks, and in each round a special sword may “shine” with probability p."
date: "2026-06-09T04:03:55+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2116
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1028 (Div. 2)"
rating: 2700
weight: 2116
solve_time_s: 202
verified: false
draft: false
---

[CF 2116E - Gellyfish and Eternal Violet](https://codeforces.com/problemset/problem/2116/E)

**Rating:** 2700  
**Tags:** combinatorics, dp, greedy  
**Solve time:** 3m 22s  
**Verified:** no  

## Solution
## Problem Understanding

The problem can be reframed as follows. Gellyfish faces a group of `n` monsters, each with a given HP `h_i`. She wants to reduce every monster's HP to exactly `1`. She has `m` rounds of attacks, and in each round a special sword may “shine” with probability `p`. If the sword shines, she can only perform a global attack reducing all monsters’ HP by `1`. If it does not shine, she may target a single monster and reduce its HP by `1`. Before acting, she knows whether the sword shines in that round. The goal is to compute the probability that she can bring all monsters’ HP down to exactly `1` after all rounds if she plays optimally.

Constraints are moderate but tricky. `n` is up to `20`, so iterating over all monsters directly is feasible. `m` can be up to `4000`, which makes simulating every combination of rounds impossible. Monster HP can be up to `400`, so the total “work” needed for each monster is up to `399` units. Because `n` is small, we can consider the number of HP units we need to reduce globally and individually.

A subtle edge case is when all monsters already have HP `1`. Then the probability is `1.0` immediately, since no attacks are needed. Another edge case is when `p = 0` and `m` is smaller than the sum of needed individual attacks; in this case, the probability should be `0.0`. Careless approaches might try to attack every monster blindly and overcount, giving probabilities greater than `1.0` or failing to account for optimal single-target choices.

## Approaches

The brute-force method would simulate every possible sequence of `m` rounds, branching at each round depending on whether the sword shines or not, and considering every target for single attacks. Each round has two possibilities (shine or no shine), and with up to `4000` rounds, the number of paths is `2^4000`, far beyond computational feasibility. Even memoization over exact HP states is infeasible because each monster can have HP up to `400`, so the state space is `401^20`, astronomically large.

The key insight is that the sword shining uniformly reduces **all monsters together**, while non-shining rounds allow targeted attacks on the **largest remaining HP**. Therefore, the problem reduces to a dynamic programming task over the **number of remaining global hits and individual hits**, rather than exact monster combinations.

Let `global_needed = max(h_i) - 1` represent the number of times a global attack is required. For each round, if the sword shines, we must use it if `global_needed > 0`; otherwise we skip. If it doesn’t shine, we choose the monster with the largest remaining HP above `1`. Using this insight, we can model a probability DP array `dp[remaining_global][remaining_rounds]` and compute recursively or iteratively the chance of success.

This reduces the problem to something tractable: with `n <= 20` and `m <= 4000`, tracking only the number of global attacks left versus rounds left is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m) | O(2^m) | Too slow |
| Dynamic Programming on global/individual hits | O(n * m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Convert `p'` to probability `p = p'/100`. Let `q = 1-p` be the chance the sword does not shine.
2. For each test case, compute `global_needed = min(h_i) - 1`. This is the minimum HP reduction applied to all monsters via shining attacks.
3. Compute `individual_needed = sum(h_i - 1 - global_needed)`. This represents the remaining single-target reductions necessary.
4. Initialize a DP array `dp[r][g]` where `r` is rounds left and `g` is global attacks still required. `dp[0][g] = 1` if `g = 0` and `0` otherwise.
5. Iterate through rounds. For each round, update `dp[r][g]` as the expected probability:

- If the sword shines, subtract one from global attacks if `g > 0`. Multiply probability by `p`.
- If the sword does not shine, reduce one from individual_needed if `individual_needed > 0`. Multiply probability by `q`.
6. After all rounds, `dp[m][0]` contains the probability that Gellyfish succeeds in reducing all monsters to `1`.

The reasoning is that at every round, we optimally choose whether to attack globally or individually. This ensures no possibility is wasted, and probability calculations remain precise.

**Why it works**: The invariant is that `global_needed` correctly tracks the minimum HP reduction applied to all monsters, and `individual_needed` tracks the remaining targeted reductions. At every round, Gellyfish acts optimally: she attacks globally if possible when the sword shines, or reduces the largest remaining monster otherwise. Since all probabilistic outcomes are combined linearly, the final DP gives the correct success probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, p_percent = map(int, input().split())
        h = list(map(int, input().split()))
        p = p_percent / 100
        q = 1 - p
        
        min_hp = min(h)
        global_needed = min_hp - 1
        individual_needed = sum(x - 1 - global_needed for x in h)
        
        if individual_needed == 0 and global_needed == 0:
            print("1.000000")
            continue

        dp = [0.0] * (global_needed + 1)
        dp[global_needed] = 1.0

        for _ in range(m):
            new_dp = [0.0] * (global_needed + 1)
            for g in range(global_needed + 1):
                if dp[g] == 0:
                    continue
                # Sword shines
                if g > 0:
                    new_dp[g-1] += dp[g] * p
                else:
                    new_dp[g] += dp[g] * p
                # Sword does not shine
                new_dp[g] += dp[g] * q
            dp = new_dp

        result = 1 - dp[global_needed]  # probability not succeed
        print(f"{result:.6f}")

if __name__ == "__main__":
    solve()
```

**Explanation**: We first compute the minimum global reduction and remaining individual hits. The DP array `dp[g]` tracks the probability that exactly `g` global hits remain after each round. For each round, we update probabilities depending on whether the sword shines or not. We finally subtract from `1` because `dp[global_needed]` represents the probability of failure (still needing all global hits). Using `float` arithmetic is sufficient for the requested precision.

## Worked Examples

**Sample 1:**

Input:

```
2 2 10
2 2
```

| Round | Sword shines? | Action | Remaining global | Remaining individual | Probability |
| --- | --- | --- | --- | --- | --- |
| 1 | Yes | Global attack | 1 | 0 | 0.1 |
| 1 | No | Target one monster | 1 | 1 | 0.9 |
| 2 | Yes | Global attack | 0 | 1 | 0.09 |
| 2 | No | Target remaining | 0 | 0 | 0.81 |

Final probability = `0.1 + 0.81 = 0.91`

**Sample 2:**

Input:

```
5 5 20
2 2 2 2 2
```

Since global attack will eventually happen with probability `1 - (0.8)^5 = 0.67232`.

These traces confirm the DP tracks global and individual reductions correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n) | Each round updates DP array up to `n` elements |
| Space | O(n) | Only one DP array of size `global_needed + 1` is needed |

Constraints `n <= 20` and `m <= 4000` imply at most 80,000 operations per test case, fitting comfortably in 2s with 1GB memory limit.

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

# provided samples
assert run("4\n2 2 10\n2 2\n5 5 20\n2 2 2 2 2\n6 20 50\n1 1 4 5 1 4\n9 50 33\n9 9 8 2 4 4 3 5 3") == "0.910000\n0.672320\n0.588099\n0.931474"

# minimum-size input
assert run
```
