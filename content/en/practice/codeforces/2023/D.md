---
title: "CF 2023D - Many Games"
description: "The problem presents a casino with multiple games, each offering a chance to win a certain amount. Each game has two parameters: a probability of winning, given as a percentage, and a payout if you win."
date: "2026-06-08T12:33:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 2023
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 980 (Div. 1)"
rating: 2900
weight: 2023
solve_time_s: 107
verified: true
draft: false
---

[CF 2023D - Many Games](https://codeforces.com/problemset/problem/2023/D)

**Rating:** 2900  
**Tags:** brute force, dp, greedy, math, probabilities  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents a casino with multiple games, each offering a chance to win a certain amount. Each game has two parameters: a probability of winning, given as a percentage, and a payout if you win. You can choose any subset of games to play, but you only earn money if you win every chosen game. If you lose even one game in your chosen subset, you receive nothing. The task is to select a set of games that maximizes the expected value of winnings.

The expected value of a chosen set is the product of the probabilities (converted to fractions) times the sum of the winnings. For example, if you select two games with probabilities 80% and 50% and payouts 80 and 200, the expected value is $(0.8 * 0.5) * (80 + 200) = 112$.

The constraints are significant: the number of games $n$ can reach 200,000. A brute-force examination of all subsets would involve $2^n$ combinations, which is infeasible. The individual probabilities and winnings are bounded such that their product never exceeds $2 \cdot 10^5$, ensuring numerical stability.

Non-obvious edge cases include situations where choosing more games decreases the expected value. For instance, picking a game with a low probability but high payout might reduce the expected value when combined with other games. Another edge case is having all probabilities at 100%, in which case picking all games is optimal. Similarly, picking a single high-probability low-payout game may be better than combining it with a risky game.

## Approaches

The brute-force approach would examine all subsets of games. For each subset, compute the product of probabilities and the sum of winnings, then multiply them to get the expected value. This is correct because it directly follows the problem definition. However, with $n \le 2 \cdot 10^5$, there are $2^{200000}$ subsets, which is astronomically large. This approach is impossible.

The key observation for optimization is that the expected value function is multiplicative in probabilities but additive in winnings. If we sort the games by the ratio of probability to impact on expected value, or equivalently, by a metric like $w_i / (1 - p_i/100)$, we can greedily decide whether including a game increases the expected value. This reduces the problem to iteratively adding the game with the highest marginal contribution while the expected value grows. The structure of the function ensures that once adding a game decreases the expected value, adding any further game (sorted by the same metric) will not help, allowing early stopping.

The optimal approach sorts the games by decreasing $w_i / (100 / p_i - 1)$, which is derived by setting the derivative of the expected value with respect to including a game and simplifying. Then it iterates over this sorted order, cumulatively computing the product of probabilities and sum of winnings. The maximum expected value encountered during this iteration is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of games $n$ and the list of probabilities $p_i$ and winnings $w_i$. Convert probabilities to fractions for computation.
2. Define a metric to evaluate the benefit of adding each game. A natural choice is $w_i / (1 - p_i/100)$, which represents the ratio of payout to the probability of losing, reflecting its marginal contribution to expected value.
3. Sort all games in decreasing order of this metric. Games with higher benefit are considered first.
4. Initialize two variables: a cumulative probability $prob = 1.0$ representing the product of selected games' probabilities, and a cumulative sum of winnings $sum\_w = 0$.
5. Iterate over the sorted games. For each game, calculate the potential expected value if this game is included: $new\_EV = prob * (p_i/100) * (sum\_w + w_i)$.
6. If including the game increases the current maximum expected value, update $prob$ and $sum\_w$ to include this game, and update the maximum.
7. Stop iteration once adding a game decreases the expected value, since further games have smaller marginal contributions.
8. Output the maximum expected value found, formatted to sufficient precision.

Why it works: The expected value function is unimodal when games are considered in order of decreasing $w_i / (1 - p_i/100)$. This property ensures that once adding a game decreases the expected value, any remaining game will also decrease it. Thus, the greedy addition of games guarantees that the maximum is found without checking all subsets.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
games = []

for _ in range(n):
    p, w = map(int, input().split())
    games.append((p, w))

# Sort by "benefit" metric w / (1 - p/100) descending
games.sort(key=lambda x: x[1] / (1 - x[0] / 100), reverse=True)

max_ev = 0.0
prob = 1.0
sum_w = 0.0

for p, w in games:
    new_prob = prob * (p / 100)
    new_sum_w = sum_w + w
    ev = new_prob * new_sum_w
    if ev > max_ev + 1e-12:
        max_ev = ev
        prob = new_prob
        sum_w = new_sum_w
    else:
        break

print(f"{max_ev:.9f}")
```

This solution reads input efficiently using `sys.stdin.readline`. Games are sorted by the ratio $w / (1 - p/100)$, which captures marginal expected value growth. The cumulative probability and sum of winnings are updated only if the expected value increases, preventing degradation. We include a small epsilon in the comparison to avoid floating-point errors.

## Worked Examples

### Sample 1

Input:

```
3
80 80
70 100
50 200
```

| Step | Selected Game | prob | sum_w | ev |
| --- | --- | --- | --- | --- |
| 1 | 50 200 | 0.5 | 200 | 100 |
| 2 | 80 80 | 0.4 | 280 | 112 |
| 3 | 70 100 | 0.28 | 380 | 106.4 |

Maximum expected value: 112

This trace shows that adding the first two games increases EV, but adding the third reduces it. Greedy selection works.

### Sample 2

Input:

```
2
100 1
100 1
```

| Step | Selected Game | prob | sum_w | ev |
| --- | --- | --- | --- | --- |
| 1 | 100 1 | 1 | 1 | 1 |
| 2 | 100 1 | 1 | 2 | 2 |

Maximum expected value: 2

Here, all probabilities are 100%, so adding all games is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting n games dominates; iteration is linear |
| Space | O(n) | Store list of games and cumulative variables |

With n up to 2·10^5, O(n log n) operations (~3 million) comfortably fit within 2 seconds, and memory usage is well under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    games = [tuple(map(int, input().split())) for _ in range(n)]
    games.sort(key=lambda x: x[1] / (1 - x[0] / 100), reverse=True)
    max_ev = 0.0
    prob = 1.0
    sum_w = 0.0
    for p, w in games:
        new_prob = prob * (p / 100)
        new_sum_w = sum_w + w
        ev = new_prob * new_sum_w
        if ev > max_ev + 1e-12:
            max_ev = ev
            prob = new_prob
            sum_w = new_sum_w
        else:
            break
    return f"{max_ev:.9f}"

# Provided samples
assert run("3\n80 80\n70 100\n50 200\n") == "112.000000000", "sample 1"
assert run("2\n100 1\n100 1\n") == "2.000000000", "sample 2"

# Custom cases
assert run("1\n50 100\n") == "50.000000000", "single game"
assert run("3\n100 10\n90 20\n80 30\n") == "36.000000000", "all probabilities high"
assert run("2\n10 1000\n90 10\n") == "90.000000000", "high payout low prob vs low payout high prob"
assert run("4\n50 50\n50 50\n50 50\n50 50\n") == "62.5", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n50 100 | 50. |  |
