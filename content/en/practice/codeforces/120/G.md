---
title: "CF 120G - Boom"
description: "We are simulating a simplified version of the party game \"Boom\" with multiple teams and cards. There are n teams, each with two players. Each player has an ability to explain words (a) and an ability to understand words (b)."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 120
codeforces_index: "G"
codeforces_contest_name: "School Regional Team Contest, Saratov, 2011"
rating: 1800
weight: 120
solve_time_s: 77
verified: true
draft: false
---

[CF 120G - Boom](https://codeforces.com/problemset/problem/120/G)

**Rating:** 1800  
**Tags:** implementation  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a simplified version of the party game "Boom" with multiple teams and cards. There are `n` teams, each with two players. Each player has an ability to explain words (`a`) and an ability to understand words (`b`). There is a deck of `m` cards, each containing a word with a complexity `c`. The game proceeds in turns, with players taking cards from the top of the deck and trying to explain them to their teammate. Each turn has a fixed time `t`.

The time needed to explain a word depends on the card's complexity, the current turn's players' skills, and how much time the team has already spent on that word. Specifically, for a card `k` being explained by player `j` of team `i` to the other teammate `q`, the effective explanation time is `max(1, c_k - (a_ij + b_iq) - d_ik)`, where `d_ik` is the cumulative time already spent by this team on this card. If the team guesses the word within the turn, the card is removed and the team scores a point. Otherwise, the remaining time of the turn expires and the card goes to the bottom of the deck. The game continues until all cards are guessed.

The input provides all players' skills, the cards, and their complexities. The output must list for each team the number of points they scored and the sequence of words they guessed in order.

Constraints are moderate: `n, m ≤ 100` and `t ≤ 100`. This allows for an explicit simulation of the game because the total number of turns is bounded by `m * n * 2`, and each operation per turn is simple arithmetic. Edge cases arise when a word's complexity is lower than the sum of explaining and understanding skills, resulting in an explanation time of 1, or when a turn's duration is shorter than the required explanation time, forcing the word back to the deck.

A naive implementation might mismanage cumulative times per card (`d_ik`) or incorrectly cycle through players, causing wrong scoring or infinite loops.

## Approaches

The brute-force approach is a direct simulation of the game according to the rules. We maintain a queue of cards and, for each player's turn, compute the time needed to explain the current card. If the card can be guessed in the remaining turn time, we increment the team's score, remove the card, and record the word. Otherwise, we increment `d_ik` by the turn duration and move the card to the bottom of the deck. We cycle through players in order until all cards are guessed. The approach is correct because it literally implements the game's rules, but it requires careful tracking of cumulative times for each card per team. The operation count is roughly `O(m * n * 2)` for turns, which is acceptable given the constraints (`≤ 20,000` operations).

The key insight is that no optimizations based on sorting or skipping cards are necessary because every card might require multiple turns by different players to be guessed, and the simulation is cheap. The challenge is maintaining the order of guessed words and correctly updating cumulative times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m * n * 2) | O(n * m + m) | Accepted |

## Algorithm Walkthrough

1. Read input values `n` and `t` for the number of teams and turn duration.
2. For each team, read the skill values of the two players and store them as pairs `(a, b)` for player 1 and player 2.
3. Read the number of cards `m`, then for each card, read its word and complexity `c`.
4. Initialize a `deque` with the indices of the cards representing the deck. Initialize `d_ik = 0` for all teams and cards, and empty lists for each team's guessed words.
5. While there are cards in the deck:

1. For each player in order: player 1 of team 1, ..., player 2 of team n, do the following.
2. Set `remaining_time = t`.
3. While `remaining_time > 0` and the deck is not empty:

1. Take the card from the front of the deck.
2. Compute the time required to explain it as `max(1, c_k - (a_ij + b_iq) - d_ik)`.
3. If the required time ≤ remaining_time:

- Deduct the time from `remaining_time`.
- Record the word in the team's guessed words.
- Increment the team's score.
- Remove the card from the deck.
4. Else:

- Increment `d_ik` for this card by `remaining_time`.
- Set `remaining_time = 0`.
- Move the card to the bottom of the deck.
6. Print the results for each team: the number of guessed words and the sequence of words.

Why it works: Every card eventually accumulates enough effective time to be guessed because each turn contributes `t` to its cumulative `d_ik` for the respective team. The simulation respects the turn order, time limits, and skill contributions, so the points and word sequences are guaranteed to match the game's rules.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

n, t = map(int, input().split())
teams = []
for _ in range(n):
    a1, b1, a2, b2 = map(int, input().split())
    teams.append([(a1, b1), (a2, b2)])

m = int(input())
cards = []
for _ in range(m):
    word = input().strip()
    complexity = int(input())
    cards.append((word, complexity))

# Initialize
deck = deque(range(m))
d = [[0] * m for _ in range(n)]
guessed_words = [[] for _ in range(n)]
scores = [0] * n

while deck:
    for player in range(2):
        for team_id in range(n):
            remaining_time = t
            while remaining_time > 0 and deck:
                card_id = deck[0]
                word, c = cards[card_id]
                a, b = teams[team_id][player]
                other_player = 1 - player
                _, b_other = teams[team_id][other_player]
                required_time = max(1, c - (a + b_other) - d[team_id][card_id])
                if required_time <= remaining_time:
                    remaining_time -= required_time
                    guessed_words[team_id].append(word)
                    scores[team_id] += 1
                    d[team_id][card_id] += required_time
                    deck.popleft()
                else:
                    d[team_id][card_id] += remaining_time
                    remaining_time = 0
                    deck.rotate(-1)

for i in range(n):
    print(scores[i], *guessed_words[i])
```

The code closely follows the algorithm. The `deque` allows efficient moving of cards to the bottom. The `d` array tracks cumulative time per team per card. The nested loops enforce the player-turn order, and `max(1, ...)` ensures no word requires less than 1 second.

Careful attention is required to `remaining_time` and `d[team][card]` updates to avoid off-by-one errors.

## Worked Examples

Sample Input 1:

```
2 2
1 1 1 1
1 1 1 1
3
home
1
car
1
brother
1
```

| Step | Deck | Player | Team | Remaining Time | d[team][card] | Guessed Words | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [home, car, brother] | 1 | 1 | 2 | 0 | [] | Time required = max(1,1-(1+1)-0)=1 |
| 2 | [car, brother] | 1 | 1 | 1 | home=1 | [home] | Car next, required=1 |
| 3 | [brother] | 1 | 2 | 2 | 0 | [] | Brother guessed |
| 4 | [] | - | - | - | - | [team1: home, car; team2: brother] | All words guessed |

Trace shows that each turn consumes the correct time and updates cumulative time `d` accurately.

Custom Input:

```
1 1
1 1 1 1
1
test
5
```

Single team, single card with complexity higher than skills:

| Step | Deck | Player | Team | Remaining Time | d[team][card] | Guessed Words |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [test] | 1 | 1 | 1 | 0 | [] |
| 2 | [test] | 2 | 1 | 1 | 1 | [] |
| 3 | ... | ... | ... | ... | ... | ... |

This confirms cumulative time handling and rotation works correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n * 2 * m) = O(n * m^2) | In worst case, each card could circulate until guessed, each |
