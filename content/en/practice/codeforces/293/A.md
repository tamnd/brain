---
title: "CF 293A - Weird Game"
description: "We are asked to analyze a turn-based game played by two players, Yaroslav and Andrey, each starting with a binary string of length 2·n. On their turn, a player chooses an index in the string that hasn’t been picked yet and writes down the corresponding character on their paper."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 293
codeforces_index: "A"
codeforces_contest_name: "Croc Champ 2013 - Round 2"
rating: 1500
weight: 293
solve_time_s: 53
verified: true
draft: false
---

[CF 293A - Weird Game](https://codeforces.com/problemset/problem/293/A)

**Rating:** 1500  
**Tags:** games, greedy  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to analyze a turn-based game played by two players, Yaroslav and Andrey, each starting with a binary string of length 2·n. On their turn, a player chooses an index in the string that hasn’t been picked yet and writes down the corresponding character on their paper. Yaroslav always moves first. After all 2·n moves, both players rearrange their collected characters to form the largest possible integer. The goal is to determine the winner if both play optimally: either Yaroslav ("First"), Andrey ("Second"), or a draw ("Draw").

Each string contains only 0s and 1s, so the largest number each player can make is determined entirely by maximizing the number of 1s on their paper. Since Yaroslav starts first, he can sometimes secure a crucial advantage if he correctly prioritizes positions.

The constraints allow n up to 10^6, giving 2·n up to 2·10^6 characters. A naive simulation of all possible sequences of moves would require exploring O((2·n)!) possibilities, which is impossible. Any solution must therefore operate in linear time, or at worst linearithmic time, over the input size. The key observation is that the problem reduces to counting 1s and 0s and choosing moves greedily, rather than simulating every sequence.

A subtle edge case arises when both strings are identical or nearly identical. For instance, if s = "1111" and t = "1111" with n = 2, each player can always pick a 1, leading to a draw. A naive implementation might incorrectly assign priority without considering that a player can react to the opponent’s choice.

Another tricky scenario is when one string has a surplus of 1s while the other has an equal number of 1s spread differently. Optimal moves require prioritizing matching or countering 1s rather than blindly picking the largest available digit.

## Approaches

The simplest brute-force approach would try to simulate every turn for both players, keeping track of which indices remain and generating all sequences of choices. On each turn, one would attempt to pick the best available number to maximize the final integer. While correct in principle, this approach is factorial in complexity, O((2·n)!), because the order of moves matters. Clearly, for n = 10^6, this is entirely infeasible.

The key observation to simplify the problem is that both players only care about maximizing the count of 1s in their final number, as 1s dominate 0s. The optimal strategy becomes a greedy selection: each player should try to take positions where their character is 1 while simultaneously denying the opponent a 1 if possible. This reduces the problem to counting the number of positions in four categories: (1) both strings have 1, (2) Yaroslav has 1 and Andrey has 0, (3) Yaroslav has 0 and Andrey has 1, (4) both have 0. Each turn, the current player can pick a position in a category that maximizes their own 1s or reduces the opponent’s 1s.

This observation transforms a combinatorial explosion into a deterministic greedy procedure that processes the counts rather than simulating each index individually. We can implement this with counters for the four categories and simulate alternating moves in O(n) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2·n)!) | O(2·n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of positions where both players have 1s, Yaroslav has 1 and Andrey has 0, Yaroslav has 0 and Andrey has 1, and both have 0s. Let these counts be `c11`, `c10`, `c01`, and `c00`.
2. Initialize two variables `score_first` and `score_second` to zero. These represent the number of 1s each player will collect.
3. Simulate the game for 2·n moves. On odd-numbered moves (Yaroslav’s turn), pick the best available position to maximize his score:

- If `c11` > 0, pick from `c11`, increment `score_first`, decrement `c11`.
- Else if `c10` > 0, pick from `c10`, increment `score_first`, decrement `c10`.
- Else if `c01` > 0, pick from `c01`, decrement `c01` without increasing `score_first`.
- Else, pick from `c00`, decrement `c00`.
4. On even-numbered moves (Andrey’s turn), pick the best available position similarly:

- If `c11` > 0, pick from `c11`, increment `score_second`, decrement `c11`.
- Else if `c01` > 0, pick from `c01`, increment `score_second`, decrement `c01`.
- Else if `c10` > 0, pick from `c10`, decrement `c10` without increasing `score_second`.
- Else, pick from `c00`, decrement `c00`.
5. After all moves, compare `score_first` and `score_second`. If `score_first` > `score_second`, Yaroslav wins; if less, Andrey wins; if equal, the game is a draw.

Why it works: At each turn, a player either maximizes their own 1s if possible, or minimizes the opponent’s future 1s by removing positions where the opponent would gain a 1. Since moves alternate and the counts are updated correctly, no better outcome is achievable by deviating from this strategy.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()
t = input().strip()

c11 = c10 = c01 = c00 = 0
for i in range(2 * n):
    if s[i] == '1' and t[i] == '1':
        c11 += 1
    elif s[i] == '1' and t[i] == '0':
        c10 += 1
    elif s[i] == '0' and t[i] == '1':
        c01 += 1
    else:
        c00 += 1

score_first = 0
score_second = 0
for move in range(2 * n):
    if move % 2 == 0:
        # Yaroslav's turn
        if c11 > 0:
            c11 -= 1
            score_first += 1
        elif c10 > 0:
            c10 -= 1
            score_first += 1
        elif c01 > 0:
            c01 -= 1
        else:
            c00 -= 1
    else:
        # Andrey's turn
        if c11 > 0:
            c11 -= 1
            score_second += 1
        elif c01 > 0:
            c01 -= 1
            score_second += 1
        elif c10 > 0:
            c10 -= 1
        else:
            c00 -= 1

if score_first > score_second:
    print("First")
elif score_first < score_second:
    print("Second")
else:
    print("Draw")
```

We first categorize positions into four types to decide which ones should be picked. The turn simulation strictly alternates, and each choice is greedy based on maximizing collected 1s or minimizing the opponent’s future 1s. Off-by-one errors are avoided by counting `move % 2 == 0` for the first player. The algorithm uses O(1) extra memory beyond input strings and runs in O(n).

## Worked Examples

### Sample 1

Input:

```
2
0111
0001
```

| move | c11 | c10 | c01 | c00 | score_first | score_second | action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 (Y) | 1 | 2 | 0 | 1 | 1 | 0 | pick c11 |
| 1 (A) | 0 | 2 | 0 | 1 | 1 | 0 | pick c10 (no gain) |
| 2 (Y) | 0 | 1 | 0 | 1 | 2 | 0 | pick c10 |
| 3 (A) | 0 | 0 | 0 | 1 | 2 | 0 | pick c00 (no gain) |

Yaroslav ends with 2 ones, Andrey with 0 ones, so Yaroslav wins.

### Sample 2

Input:

```
1
10
01
```

| move | c11 | c10 | c01 | c00 | score_first | score_second | action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 (Y) | 0 | 1 | 1 | 0 | 1 | 0 | pick c10 |
| 1 (A) | 0 | 0 | 1 | 0 | 1 | 1 | pick c01 |

Scores are equal, so output is Draw.

These traces confirm the algorithm correctly prioritizes
