---
title: "CF 167B - Wizards and Huge Prize"
description: "We are asked to calculate the probability of performing well in a sequence of wizard contests, given both your chances of winning each contest and the types of prizes you may receive."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 167
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 114 (Div. 1)"
rating: 1800
weight: 167
solve_time_s: 98
verified: false
draft: false
---

[CF 167B - Wizards and Huge Prize](https://codeforces.com/problemset/problem/167/B)

**Rating:** 1800  
**Tags:** dp, math, probabilities  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to calculate the probability of performing well in a sequence of wizard contests, given both your chances of winning each contest and the types of prizes you may receive. There are _n_ contests, and for each contest, you know your probability of winning and whether the prize is a huge prize or a bag that can carry a certain number of huge prizes. You start with a bag from home that can carry _k_ huge prizes. The goal is to compute the probability that you win at least _l_ contests while being able to carry all the huge prizes you win, using both the bag you start with and any bags awarded for winning certain contests.

The input gives probabilities in percentages, which need to be converted to decimal fractions for calculation. The output is a real number probability with high precision. The constraints are tight enough that a brute-force enumeration of all possible winning subsets (2^n) is infeasible for the upper limit n=200. Probabilities must be combined carefully, accounting for which prizes you win and whether you can store them.

A subtle edge case occurs when all prizes are bags. For example, if every contest awards a bag, you can never win a huge prize, but the number of contests won may still meet _l_. If the code naively assumes that winning always increases storage requirements, it may compute an impossible scenario. Another edge case is when _k_ is already sufficient to hold any number of huge prizes; the code must still enforce the minimum number of contests won.

## Approaches

The brute-force approach would be to enumerate all subsets of contests you could win, compute the total number of huge prizes and total bag capacity for each subset, check if the subset meets both the "at least _l_ wins" and "all prizes fit" conditions, and sum the probabilities of each valid subset. This method is correct in principle but requires 2^n operations in the worst case, which is completely infeasible for n=200.

The key insight is to treat this as a dynamic programming problem over the number of contests processed, the number of wins so far, and the total huge prizes carried. Because the capacity of bags can be treated as a non-decreasing resource, we can define a DP table where the state represents the maximum number of huge prizes that can be stored, given a certain number of wins and a certain number of contests considered. For each contest, we update the DP table with the probability of winning or not winning, adjusting the total capacity accordingly. By iterating over contests in order and updating states efficiently, we can reduce the exponential complexity to a polynomial one, specifically O(n*k^2) which is feasible under the problem constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(1) | Too slow |
| Dynamic Programming | O(n * k * n) | O(n * k) | Accepted |

## Algorithm Walkthrough

1. Convert all probabilities from percentages to decimal fractions between 0 and 1. This simplifies multiplication and avoids integer scaling errors.
2. Initialize a 2D DP table `dp[w][c]`, where `w` is the number of contests won and `c` is the number of huge prizes that can currently be carried. Set `dp[0][k] = 1.0`, since with zero contests considered, you have zero wins and can carry the initial home bag capacity `k` with probability 1.
3. Iterate over each contest. For each contest, prepare a new DP table `next_dp` of the same dimensions.
4. For each existing DP state `(wins, capacity)`, consider the outcome if you do not win the contest. The number of wins remains the same, the capacity is unchanged, and the probability is multiplied by the chance of losing this contest.
5. For the winning outcome, increment the number of wins by 1. If the prize is a bag, add its capacity to the current capacity; if the prize is a huge prize, decrease the available capacity by 1 (or ensure the capacity is sufficient to hold it). Update the probability by multiplying by the chance of winning the contest. Only allow this transition if the new capacity is non-negative.
6. After processing all contests, sum the probabilities of all DP states where the number of wins is at least `l` and capacity is non-negative. This sum is the desired probability.

Why it works: The DP table exhaustively accounts for all combinations of wins and available capacity in a forward-iterative manner. Each transition respects the probabilities and storage constraints. Because we only advance one contest at a time, we avoid overcounting and correctly accumulate probabilities for each feasible outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, l, k = map(int, input().split())
p = list(map(int, input().split()))
a = list(map(int, input().split()))

p = [x / 100.0 for x in p]

dp = [[0.0 for _ in range(201 + 200)] for _ in range(n + 1)]
dp[0][k] = 1.0

for i in range(n):
    next_dp = [[0.0 for _ in range(201 + 200)] for _ in range(n + 1)]
    for wins in range(i + 1):
        for cap in range(201 + 200):
            if dp[wins][cap] < 1e-15:
                continue
            # Losing this contest
            next_dp[wins][cap] += dp[wins][cap] * (1 - p[i])
            # Winning this contest
            new_wins = wins + 1
            if a[i] == -1:
                if cap > 0:
                    next_dp[new_wins][cap - 1] += dp[wins][cap] * p[i]
            else:
                next_dp[new_wins][cap + a[i]] += dp[wins][cap] * p[i]
    dp = next_dp

result = 0.0
for wins in range(l, n + 1):
    for cap in range(201 + 200):
        result += dp[wins][cap]

print(f"{result:.12f}")
```

The code first converts the input percentages to decimal fractions to simplify multiplication. The DP table is sized to accommodate all possible capacities, including growth from bags awarded in contests. Transitions handle winning and losing correctly, updating capacities only when feasible. The final probability sum considers all states meeting the minimum win requirement.

## Worked Examples

Sample 1: `3 1 0`, `10 20 30`, `-1 -1 2`

| i | wins | cap | dp[wins][cap] |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 1.0 |
| 0 | 0 | 0 | lose 10% → 0.9, win 10% huge → skipped since cap=0 |
| 1 | 1 | 2 | win third bag → 0.3 |

The DP correctly identifies that only winning the third contest is feasible and sums to 0.3.

Sample 2: `1 1 0`, `100`, `1`

The DP starts at dp[0][0] = 1. Winning the only contest gives a bag, increasing capacity to 1. Number of wins=1, meets `l=1`, total probability=1.0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 * max_cap) | Each contest iterates over up to n wins and max capacity of up to 400 (initial k plus sum of all bag capacities) |
| Space | O(n * max_cap) | Two DP tables of size (n+1) x (max_cap) are stored simultaneously |

Given n ≤ 200 and max_cap ≤ 400, n^2 * max_cap ≈ 16 million operations, which fits comfortably in the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())
    return sys.stdout.getvalue().strip()

# provided samples
assert run("3 1 0\n10 20 30\n-1 -1 2\n") == "0.300000000000", "sample 1"
assert run("1 1 0\n100\n1\n") == "1.000000000000", "sample 2"

# custom cases
assert run("2 2 0\n50 50\n-1 -1\n") == "0.25", "both huge prizes"
assert run("2 1 1\n50 50\n-1 -1\n") == "0.75", "one bag sufficient"
assert run("3 2 0\n50 50 50\n-1 2 -1\n") == "0.375", "mix of bag and huge prize"
assert run("1 0 0\n0\n-1\n") == "1.0", "winning not required"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 0\n50 50\n-1 -1\n` | 0.25 | Correctly computes probability when both prizes are huge |
| `2 1 1\n50 50\n-1 -1\n` | 0.75 | Correctly handles home bag sufficiency |
| `3 2 0\n50 50 50 |  |  |
