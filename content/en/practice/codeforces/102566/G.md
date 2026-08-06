---
title: "CF 102566G - PokerStars"
description: "We are given a poker table state after every player has received five private cards. The only unknown cards are the two shared table cards. The task is to compute, for every player, the probability that they become the winner after those two cards are revealed."
date: "2026-08-06T21:00:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102566
codeforces_index: "G"
codeforces_contest_name: "AGM 2020, Qualification Round"
rating: 0
weight: 102566
solve_time_s: 96
verified: true
draft: false
---

[CF 102566G - PokerStars](https://codeforces.com/problemset/problem/102566/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a poker table state after every player has received five private cards. The only unknown cards are the two shared table cards. The task is to compute, for every player, the probability that they become the winner after those two cards are revealed.

A test case gives the number of players and then the five cards belonging to each player. The remaining cards form the deck from which the two community cards are chosen. For every possible pair of remaining cards, we determine the strongest five card poker hand each player can make from their seven available cards, decide the winner using the poker ordering rules, and count how often each player wins. The answer is each player's win count divided by the number of possible table card pairs, printed modulo the given prime.

The important constraint is hidden in the game design. There are always only two unknown cards. Even if every player is considered, the total number of possible boards is at most choosing two cards from a 52 card deck, which is only 1326 possibilities. This means the expensive part is not enumerating outcomes, but evaluating poker hands correctly. A solution that tries to simulate all future deals of the deck would be unnecessary and far too large, while a direct enumeration of all possible boards is easily manageable.

The tricky parts are mostly in poker comparison. A low ace straight such as A,2,3,4,5 must be treated as having high card 5, not ace. A flush comparison ignores the suit and compares the sorted card ranks. A player can have several possible five card hands inside their seven cards, so only evaluating the first five cards or greedily selecting cards gives wrong answers.

For example, if a player has A hearts, K hearts, Q hearts, J hearts, 10 clubs and the board contains 9 hearts and 2 clubs, the correct hand is only a flush, not a royal flush. A careless implementation that only checks ranks and forgets that all five cards must have the same suit would overestimate the player.

Another common mistake is ignoring the final tie rule. If two players have exactly the same poker hand, the lower indexed player wins. For a test case where two players receive identical hand strength after every possible board, the first player must receive probability 1 and the second probability 0.

## Approaches

The straightforward approach is to try every possible pair of community cards. For each pair, add the two cards to every player's hand, inspect all possible five card selections from the resulting seven cards, and keep the strongest one. This is correct because the unknown part of the game consists only of those two cards.

The number of possible boards is at most 1326. Each player requires checking 21 possible five card subsets, because seven cards contain exactly C(7,5) choices. Since 21 is a small constant, exhaustive evaluation is fast enough.

The main insight is that the probability space is tiny. Poker itself looks complicated because of the hand hierarchy, but the number of future states is very small. We do not need advanced probability formulas, simulation, or dynamic programming. We only need a reliable poker evaluator.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(52,2) * N * 21) | O(N) | Accepted after optimizing hand evaluation |
| Optimal | O(C(52,2) * N * 21) | O(N) | Accepted |

The brute force and optimal approaches are the same enumeration idea. The optimization is recognizing that this is already small enough and focusing effort on constant factors and correctness.

## Algorithm Walkthrough

1. Convert every card into numeric values for rank and suit. Store each player's five private cards and mark all used cards.
2. Generate the list of remaining cards. Every possible pair from this list represents one equally likely future table state.
3. For each possible table pair, evaluate every player. Combine their five private cards with the two table cards and enumerate all 21 possible five card hands. Keep the best hand according to poker ranking.
4. Compare all players' best hands for this table state. The player with the highest hand wins. If several players have equal hand values, choose the smallest index.
5. Add one win to the chosen player's counter. After all table pairs are processed, multiply each counter by the modular inverse of the number of possible pairs.

Why it works: every possible final game state is represented exactly once because every possible pair of remaining cards is enumerated. The hand evaluator returns the same ordering as the poker rules because each hand is converted into a category and tie breaking values. Since the winner of every possible state is counted, the final ratios are exactly the required probabilities.

## Python Solution

```python
import sys
from itertools import combinations

input = sys.stdin.readline

MOD = 100055128505716009

rank_map = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 11, "Q": 12, "K": 13, "A": 14
}

suits = {
    "clubs": 0,
    "diamonds": 1,
    "hearts": 2,
    "spades": 3
}

def evaluate_five(cards):
    ranks = sorted([x[0] for x in cards], reverse=True)
    cnt = {}
    for r in ranks:
        cnt[r] = cnt.get(r, 0) + 1

    groups = sorted(((c, r) for r, c in cnt.items()), reverse=True)

    flush = len({x[1] for x in cards}) == 1

    unique = sorted(set(ranks))
    straight = False
    high = 0
    if len(unique) == 5:
        if unique == [2, 3, 4, 5, 14]:
            straight = True
            high = 5
        elif unique[-1] - unique[0] == 4:
            straight = True
            high = unique[-1]

    if straight and flush:
        return (8, high)

    if groups[0][0] == 4:
        return (7, groups[0][1], groups[1][1])

    if groups[0][0] == 3 and groups[1][0] == 2:
        return (6, groups[0][1], groups[1][1])

    if flush:
        return (5, *ranks)

    if straight:
        return (4, high)

    if groups[0][0] == 3:
        kickers = sorted([r for r in ranks if r != groups[0][1]], reverse=True)
        return (3, groups[0][1], *kickers)

    if groups[0][0] == 2 and groups[1][0] == 2:
        pairs = sorted([groups[0][1], groups[1][1]], reverse=True)
        return (2, pairs[0], pairs[1], groups[2][1])

    if groups[0][0] == 2:
        kickers = sorted([r for r in ranks if r != groups[0][1]], reverse=True)
        return (1, groups[0][1], *kickers)

    return (0, *ranks)

def evaluate_seven(cards):
    best = None
    for comb in combinations(cards, 5):
        cur = evaluate_five(comb)
        if best is None or cur > best:
            best = cur
    return best

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        players = []
        used = set()

        for _ in range(n):
            hand = []
            for _ in range(5):
                r, s = input().split()
                card = (rank_map[r], suits[s])
                hand.append(card)
                used.add(card)
            players.append(hand)

        deck = []
        for r in range(2, 15):
            for s in range(4):
                if (r, s) not in used:
                    deck.append((r, s))

        wins = [0] * n
        total = 0

        for a, b in combinations(deck, 2):
            total += 1
            board = [a, b]
            best = None
            winner = -1

            for i in range(n):
                cur = evaluate_seven(players[i] + board)
                if best is None or cur > best:
                    best = cur
                    winner = i

            wins[winner] += 1

        inv = pow(total, MOD - 2, MOD)
        ans.append(" ".join(str(x * inv % MOD) for x in wins))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The card encoding turns ranks and suits into integers, which makes comparisons simple and avoids string handling during the expensive part of the algorithm.

The function `evaluate_five` follows the poker hierarchy directly. The returned tuple starts with the hand category, so a stronger category automatically compares larger. The remaining tuple entries are ordered tie breakers, matching the rules for that category.

The seven card evaluator checks every possible five card selection. There are only 21 of them, so this direct method is clearer and safer than trying to build complicated case based logic for seven cards.

The modular inverse is computed with Fermat's theorem because the modulus is prime. Python integers do not overflow, so the multiplication by the inverse is safe.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(C(R,2) * N * 21 * 5) | R is the number of remaining cards, at most 52 |
| Space | O(N) | Stores players and temporary card lists |

The largest possible number of boards is 1326, so even with many players the algorithm stays within the intended limits. The memory usage is dominated by storing the input hands.

## Worked Examples

For a simple single player case:

Input:

```
1
1
A hearts
K hearts
Q hearts
J hearts
10 hearts
```

The trace is:

| Boards checked | Player hand | Best category | Wins |
| --- | --- | --- | --- |
| first board | already has royal flush | straight flush | 1 |
| all boards | unchanged winner | straight flush | all |

The player always wins because there is only one participant. The probability is 1.

For two players:

| Boards checked | Player 1 | Player 2 | Winner |
| --- | --- | --- | --- |
| board 1 | pair of aces | high card | Player 1 |
| board 2 | pair of aces | pair of kings | Player 1 |
| all boards | compared normally | compared normally | counted |

This demonstrates that the algorithm never assumes the private cards alone decide the winner. Every possible table card pair can change the result.

## Test Cases

```
# These tests illustrate the expected behavior of the algorithm.
# They are intended for use with the solve() function.

sample = """1
4
2 clubs
4 diamonds
7 hearts
J spades
Q clubs
2 diamonds
4 hearts
7 spades
J clubs
Q diamonds
2 hearts
4 spades
7 clubs
J diamonds
Q hearts
2 spades
4 clubs
7 diamonds
J hearts
Q spades
"""

# Expected output:
# 1 0 0 0

single = """1
1
A hearts
K hearts
Q hearts
J hearts
10 hearts
"""

# Expected output:
# 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single player with royal flush | 1 | Handles the minimum number of players |
| Four player sample | 1 0 0 0 | Handles multiple players and tie breaking |

## Edge Cases

A low ace straight is handled by explicitly checking the sequence A,2,3,4,5. Without this special case, a hand such as A hearts, 2 clubs, 3 diamonds, 4 spades, 5 hearts would incorrectly receive high card ace instead of straight high card five.

A tie between players is handled after comparing the complete hand tuples. If two players have identical category and tie breakers, the comparison keeps the earlier index as the winner. This matches the rule that the smallest player index wins unresolved ties.

A player with seven cards may have multiple strong combinations. For example, holding A spades, A hearts, A diamonds, K clubs, K hearts with a board containing another ace creates both a full house and three of a kind possibilities. Enumerating all five card subsets guarantees that the full house is selected.
