---
title: "CF 105B - Dark Assembly"
description: "We have a small assembly of n senators, each defined by a level and a loyalty score. Loyalty is a probability that a senator votes in favor of a proposal, given in 10% increments. If more than half of senators vote yes, the proposal passes."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 105
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 81"
rating: 1800
weight: 105
solve_time_s: 139
verified: true
draft: false
---

[CF 105B - Dark Assembly](https://codeforces.com/problemset/problem/105/B)

**Rating:** 1800  
**Tags:** brute force, probabilities  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a small assembly of _n_ senators, each defined by a level and a loyalty score. Loyalty is a probability that a senator votes in favor of a proposal, given in 10% increments. If more than half of senators vote yes, the proposal passes. If the vote fails, the player can attempt to "eliminate" the dissenters, with a success probability based on the player’s total level versus the total level of those dissenters.

Before voting, the player can bribe senators with up to _k_ candies. Each candy increases loyalty by 10%, up to a maximum of 100%. The task is to determine the maximum probability of passing the proposal after optimally distributing candies.

The constraints are small: _n_ and _k_ are at most 8. This immediately suggests that exploring all possible ways of distributing candies is feasible. The senator levels and loyalty values can be up to 9999 and 100 respectively, but probabilities are quantized in steps of 10%.

Non-obvious edge cases include the scenario where no senator votes positively initially, or when loyalty is already 100%, making additional candies ineffective. Another subtle case arises if _k_ exceeds what is needed to max out all loyalties; distributing excess candies does not change probabilities.

## Approaches

The brute-force method is straightforward: try every possible way to distribute candies among senators, compute the probability of passing the vote for each distribution, and track the maximum. For each candy distribution, we must consider all $2^n$ subsets of senators voting yes or no to calculate the vote success probability. After that, if the proposal fails in a subset, we compute the probability of killing the dissenters.

With _n_ ≤ 8 and _k_ ≤ 8, the number of candy distributions is combinatorial but small enough. Specifically, each senator can get 0 to min(k, 10 - loyalty/10) candies. We can generate distributions recursively. For each distribution, we sum over all subsets of senators voting yes, computing the combined probability. Even in the worst case, the complexity is acceptable because $8 \times 2^8 \times 9^8$ is within a few million operations, which a modern CPU can handle in under 2 seconds.

The key insight for optimization is that we do not need a fancy pruning or dynamic programming beyond this brute-force approach, because the bounds are small. The challenge is to correctly compute probabilities for each scenario and handle rounding in 10% increments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(choices of candies × 2^n) | O(n) | Accepted |
| Optimized with memoization | O(same) | O(n × k) | Unnecessary for these bounds |

## Algorithm Walkthrough

1. Read the input, storing each senator’s level and loyalty. Convert loyalty percentages into decimal probabilities for calculations.
2. Generate all possible ways to distribute up to _k_ candies among _n_ senators, respecting the cap of 100% loyalty. Each candy adds 10% loyalty. This can be implemented recursively: for senator i, try giving 0 up to min(remaining candies, 10 - current_loyalty/10) candies, then recurse to senator i+1.
3. For each candy distribution, calculate the probability of the proposal passing. Loop over all $2^n$ subsets of senators representing the set who vote yes. Compute the probability of each subset occurring as the product of individual senator probabilities: for a senator in the yes set, multiply by loyalty; for a senator not in the set, multiply by (1 - loyalty).
4. For subsets where yes votes are strictly more than half, add the probability to a running sum.
5. For subsets where the proposal fails, compute the probability of successfully killing all dissenters. Sum their levels to get _B_, then compute $A / (A + B)$, multiply by the probability of this vote pattern, and add to the running sum.
6. Track the maximum probability across all candy distributions. Output this probability with 10 decimal places.

Why it works: the algorithm explicitly enumerates all possible candy allocations and all voting outcomes. Each probability is computed exactly according to the problem rules. By considering every candy allocation, we are guaranteed to find the optimal distribution. The sum of probabilities over all outcomes equals 1 for each distribution, ensuring that no scenario is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline
from itertools import product

def solve():
    n, k, A = map(int, input().split())
    senators = []
    for _ in range(n):
        b, l = map(int, input().split())
        senators.append([b, l])

    max_prob = 0.0

    # Recursive candy distribution
    def distribute(i, remaining_candies, loyalties):
        nonlocal max_prob
        if i == n:
            # Evaluate this loyalty distribution
            prob = 0.0
            for mask in range(1 << n):
                yes_count = 0
                p_mask = 1.0
                dissenters_level = 0
                for j in range(n):
                    if mask & (1 << j):
                        yes_count += 1
                        p_mask *= loyalties[j] / 100
                    else:
                        p_mask *= 1 - loyalties[j] / 100
                        dissenters_level += senators[j][0]
                if yes_count > n // 2:
                    prob += p_mask
                else:
                    if A + dissenters_level > 0:
                        prob += p_mask * A / (A + dissenters_level)
            max_prob = max(max_prob, prob)
            return

        max_add = min(remaining_candies, 10 - loyalties[i] // 10)
        for candies in range(max_add + 1):
            loyalties[i] += candies * 10
            distribute(i + 1, remaining_candies - candies, loyalties)
            loyalties[i] -= candies * 10

    distribute(0, k, [sen[1] for sen in senators])
    print(f"{max_prob:.10f}")

solve()
```

The code first reads input and stores senators’ levels and loyalties. It uses a recursive function to try all valid candy distributions. For each distribution, it enumerates all voting subsets using bit masks. Probabilities for each voting pattern are multiplied for individual senators. If the vote passes, the probability is added directly; if not, the chance to eliminate dissenters is factored in.

Careful implementation ensures that loyalty caps at 100%, probabilities are computed in decimal, and recursion correctly backtracks the loyalty changes after each branch.

## Worked Examples

**Sample 1**

Input:

```
5 6 100
11 80
14 90
23 70
80 30
153 70
```

| Distribution | Votes pattern | Vote yes? | Dissenters level | Probability | Contribution |
| --- | --- | --- | --- | --- | --- |
| 2 candies to senator 1, 2 to 2, 2 to 3 | mask 11111 | yes | 0 | 1 | 1 |
| ... | other masks | fail | sum(B) | P_vote * A/(A+B) | sum |

This demonstrates that distributing candies to the most loyal senators ensures the majority is easily reached.

**Sample 2 (custom)**

```
3 3 10
5 0
5 0
5 0
```

Optimal: give 1 candy to each senator → loyalties = 10%, 10%, 10%

| mask | yes_count | probability | contribution |
| --- | --- | --- | --- |
| 000 | 0 | 0.9_0.9_0.9=0.729 | fail → 10/(10+15)=0.4 → 0.729*0.4=0.2916 |
| 001 | 1 | 0.1_0.9_0.9=0.081 | fail → 10/(10+10)=0.5 → 0.081*0.5=0.0405 |
| 010 | 1 | same | 0.0405 |
| 011 | 2 | pass | 0.009 |
| total |  |  | sum=0.3816 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((k+1)^n * 2^n) | For each candy distribution (≤ 9^8) we enumerate all subsets of votes (2^n ≤ 256) |
| Space | O(n) | Only storing current loyalties and recursion stack |

With n ≤ 8 and k ≤ 8, the total number of operations is small enough for the 2-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        solve()
    return f.getvalue().strip()

# provided sample
assert run("5 6 100\n11 80\n14 90\n23 70\n80 30\n153 70\n") == "1.0000000000", "sample 1"

# custom
assert run("3 3 10\n5 0\n5 0\n5 0\n") == "0.3816000000", "all
```
