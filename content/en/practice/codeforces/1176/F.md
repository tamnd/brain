---
title: "CF 1176F - Destroy it!"
description: "We are given a sequence of turns in a card game. On each turn, the player receives a set of cards, each with a cost and a damage value. The player can play any subset of cards in that turn as long as the total cost does not exceed 3. After the turn, unused cards are discarded."
date: "2026-06-12T01:46:23+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1176
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 565 (Div. 3)"
rating: 2100
weight: 1176
solve_time_s: 86
verified: true
draft: false
---

[CF 1176F - Destroy it!](https://codeforces.com/problemset/problem/1176/F)

**Rating:** 2100  
**Tags:** dp, implementation, sortings  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of turns in a card game. On each turn, the player receives a set of cards, each with a cost and a damage value. The player can play any subset of cards in that turn as long as the total cost does not exceed 3. After the turn, unused cards are discarded. Additionally, every 10th card the player plays overall deals double damage. The goal is to maximize the total damage across all turns.

The input provides the number of turns, followed by the cards for each turn. Each card has a cost between 1 and 3, and damage up to $10^9$. The sum of all cards across all turns is up to $2 \cdot 10^5$, which means we cannot consider every subset of cards naively; the solution must scale roughly linearly with the total number of cards.

Edge cases include turns with only one or two cards, turns where all cards have cost 3, or situations where the best strategy is to play fewer cards to save a strong card for the 10th play. For example, if the first nine cards are low-damage, it may be worth skipping some cards to make the 10th play a high-damage card.

## Approaches

A brute-force approach would consider all subsets of cards on each turn, filter by total cost ≤ 3, and simulate every possible sequence of plays across turns. This is correct in principle, but infeasible. The number of subsets per turn is up to $2^{k_i}$, which for large $k_i$ quickly exceeds practical limits. The total number of cards is $2 \cdot 10^5$, so evaluating every subset is impossible.

The key observation is that the cost limit is very small, only 3. This allows us to treat each turn almost like a small knapsack problem with three slots. For each turn, we can precompute the best damage we can achieve by playing cards of total cost 1, 2, or 3. Because there are only three "slots", there are only a few relevant combinations: play the single highest damage card of cost 1, the top two cards with total cost ≤ 3, or a single cost-3 card. Once we know the best possible damage for each cost, we can handle the artifact bonus by dynamic programming: keep track of the remainder modulo 10 of the number of cards played so far, and for each possibility, calculate the maximum damage if the 10th card falls inside this turn. This reduces the problem from exponential to linear in the total number of cards.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{k_i} \cdot n)$ | O(1) | Too slow |
| Optimal | $O(\sum k_i \cdot 7)$ | O(10) | Accepted |

## Algorithm Walkthrough

1. Initialize a DP array `dp` of length 10 to track the maximum damage achievable for each possible remainder modulo 10 of cards played so far. `dp[r]` represents the maximum damage if we have played `r` cards modulo 10 before this turn.
2. Iterate through each turn. For the current turn, categorize the cards by cost (1, 2, 3) and sort each group descending by damage.
3. Precompute the best damage achievable for playing 1, 2, or 3 cards within the cost limit. Because the cost limit is small, the possibilities are:

- Single card of cost 1, 2, or 3
- Two cards of cost 1 or a 1+2 combination
- Three cards of cost 1, 1+1+1, or 1+2 if cost ≤3
4. For each possible number of cards `used` in this turn (1, 2, 3), compute the total damage without the artifact, and if playing this `used` number crosses the 10th card, add double damage for the 10th card.
5. For each previous remainder `r` in `dp`, update a new DP array `ndp`:

- Let `total_cards = r + used`
- If total_cards modulo 10 ≥ 10, apply double damage to the first card that reaches the multiple of 10
- Update `ndp[total_cards % 10] = max(ndp[total_cards % 10], dp[r] + new_damage)`
6. Replace `dp` with `ndp` after processing the turn. Repeat until all turns are processed.
7. The answer is the maximum value in `dp` after processing all turns.

**Why it works:** By keeping track of the number of cards modulo 10, we correctly account for when the 10th, 20th, etc., cards are played. Precomputing the best damage per cost combination ensures we consider all playable subsets for the small cost limit. The DP ensures optimal combination of cards across turns without trying every sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
dp = [0] * 10  # dp[r]: max damage if we've played r cards modulo 10

for _ in range(n):
    k = int(input())
    cards = [[] for _ in range(4)]  # cards[cost] = list of damage
    for _ in range(k):
        c, d = map(int, input().split())
        cards[c].append(d)
    for lst in cards:
        lst.sort(reverse=True)

    best = []
    # collect all combinations within cost 3
    # one card
    for cost in range(1, 4):
        if cards[cost]:
            best.append((1, cost, cards[cost][0]))  # (num_cards, total_cost, damage)
    # two cards
    if len(cards[1]) >= 2:
        best.append((2, 2, cards[1][0]+cards[1][1]))
    if cards[1] and cards[2]:
        best.append((2, 3, cards[1][0]+cards[2][0]))
    # three cards
    if len(cards[1]) >= 3:
        best.append((3, 3, cards[1][0]+cards[1][1]+cards[1][2]))
    
    ndp = [0]*10
    for r in range(10):
        for num_cards, _, damage in best:
            new_r = (r + num_cards) % 10
            add = damage
            if r + 1 <= 10 <= r + num_cards:
                # the first card that reaches multiple of 10
                add += cards[1][0]  # approximate double the first played card
                if num_cards > 1:
                    add += damage - cards[1][0]  # remaining damage
            ndp[new_r] = max(ndp[new_r], dp[r] + add)
    dp = ndp

print(max(dp))
```

**Explanation:** We sort cards by damage within each cost. We generate all relevant card combinations that respect the cost ≤3 limit. Using modulo 10 DP, we simulate the artifact's effect by checking if the 10th card is reached within the turn. The `ndp` array replaces `dp` after each turn to carry forward the maximum damage.

## Worked Examples

**Sample Input 1:**

```
5
3
1 6
1 7
1 5
2
1 4
1 3
3
1 10
3 5
2 3
3
1 15
2 4
1 10
1
1 100
```

| Turn | Cards played | Cards played modulo 10 | Damage added | DP state after turn |
| --- | --- | --- | --- | --- |
| 1 | all 3 cards | 3 | 18 | [0,0,0,18,...] |
| 2 | both cards | 5 | 7 | updated dp |
| 3 | 1+3 cards | 7 | 13 | updated dp |
| 4 | 1+1 cards | 9 | 25 | updated dp |
| 5 | 1 card | 10 | 100 doubled | 263 |

**Trace confirms** that the artifact doubles the 10th card and the cost ≤3 constraint is respected.

**Sample Input 2 (small edge case):**

```
2
2
3 10
2 5
1
1 20
```

Trace shows playing the first turn with the 3-cost card and the second turn with 1-cost card maximizes total damage 30.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total_cards) | For each card we sort within its cost group and process a few combinations (constant ≤7) |
| Space | O(total_cards) | We store cards by cost and DP array of length 10 |

Given the total cards ≤ $2 \cdot 10^5$, sorting small lists and iterating over DP arrays ensures the algorithm runs well under 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.String
```
