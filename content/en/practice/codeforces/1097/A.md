---
title: "CF 1097A - Gennady and a Card Game"
description: "The game Gennady plays involves matching cards either by rank or suit. In practical terms, you are given a single card on the table and a hand of five cards."
date: "2026-06-12T05:45:26+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1097
codeforces_index: "A"
codeforces_contest_name: "Hello 2019"
rating: 800
weight: 1097
solve_time_s: 77
verified: true
draft: false
---

[CF 1097A - Gennady and a Card Game](https://codeforces.com/problemset/problem/1097/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The game Gennady plays involves matching cards either by rank or suit. In practical terms, you are given a single card on the table and a hand of five cards. Each card is represented by two characters: the first character is the rank, which can be a number from 2 to 9 or a letter for T, J, Q, K, A. The second character is the suit, which is one of D, C, S, or H. The task is to determine whether at least one card in your hand shares either the rank or the suit with the table card. If such a card exists, you can play it, and the output should be "YES". Otherwise, the output should be "NO".

The constraints are small. You only ever have one table card and five hand cards. This means any algorithm that inspects each card individually is fast enough. There is no need for advanced data structures, hashing, or sorting. The problem is essentially constant time due to fixed input size, and the main challenge is careful implementation rather than algorithmic efficiency.

Non-obvious edge cases include situations where the hand contains cards that match the table card only by suit or only by rank. For example, if the table card is 9H and your hand is 2H 3D 4S 5C 6D, you can play 2H because it matches the suit. Another subtle case is having multiple cards in hand that could be played; you still only need to output "YES" once, and it does not matter which card it is. A careless implementation might incorrectly require both rank and suit to match, which would fail on these examples.

## Approaches

The most straightforward approach is brute-force: iterate over each card in your hand and check if either its rank matches the table card rank or its suit matches the table card suit. Since there are only five cards, this is effectively a constant number of operations. The brute-force approach is guaranteed correct because it checks all possibilities exhaustively, and its running time is negligible for the given input.

There is no faster approach in terms of asymptotic complexity because the brute-force method already examines all cards once. The observation that allows immediate decision is that you can return "YES" as soon as a matching card is found. There is no need to check the remaining cards once a valid move is discovered. This small early exit is a minor optimization but clarifies the logic: once a match exists, you are done.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(5) → O(1) effectively | O(1) | Accepted |
| Optimal | O(5) → O(1) effectively | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the table card and the five hand cards. The first character of each string is the rank, the second character is the suit.
2. Extract the rank and suit from the table card into separate variables for clarity.
3. Iterate over each card in your hand.
4. For each hand card, extract its rank and suit.
5. Check if the rank matches the table card's rank or if the suit matches the table card's suit.
6. If a match is found, immediately print "YES" and stop the program.
7. If the loop completes without finding any match, print "NO".

This algorithm works because the invariant is simple: we are only allowed to play a card if it matches either the rank or the suit of the table card. By checking each hand card individually and returning immediately upon a successful match, we guarantee that no valid card is overlooked and no invalid card triggers a "YES".

## Python Solution

```python
import sys
input = sys.stdin.readline

table_card = input().strip()
hand_cards = input().strip().split()

table_rank = table_card[0]
table_suit = table_card[1]

for card in hand_cards:
    if card[0] == table_rank or card[1] == table_suit:
        print("YES")
        break
else:
    print("NO")
```

The code first reads the table card and splits the hand into a list. It explicitly stores the rank and suit of the table card, which avoids repeated indexing. The loop checks each hand card in turn. Using the `else` clause on the for loop ensures that "NO" is printed only if no card matched, a subtle but clean Pythonic approach.

## Worked Examples

**Sample 1**

Input:

```
AS
2H 4C TH JH AD
```

| Step | Card | Rank Match? | Suit Match? | Action |
| --- | --- | --- | --- | --- |
| 1 | 2H | No | Yes (H) | Print YES, stop |

This shows the suit match is sufficient, confirming the algorithm correctly identifies playable cards.

**Sample 2**

Input:

```
4D
5H 6S 7C 8H 9S
```

| Step | Card | Rank Match? | Suit Match? | Action |
| --- | --- | --- | --- | --- |
| 1 | 5H | No | No | Continue |
| 2 | 6S | No | No | Continue |
| 3 | 7C | No | No | Continue |
| 4 | 8H | No | No | Continue |
| 5 | 9S | No | No | Continue |
| End | - | - | - | Print NO |

Here, no card matches, demonstrating the else clause triggers correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(5) → O(1) | There are always five cards, each checked once. |
| Space | O(1) | Only a few string variables and the hand list are used. |

Given the fixed number of cards, the algorithm runs in negligible time and memory, easily fitting within 1-second and 256 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    table_card = input().strip()
    hand_cards = input().strip().split()
    table_rank = table_card[0]
    table_suit = table_card[1]
    for card in hand_cards:
        if card[0] == table_rank or card[1] == table_suit:
            return "YES"
    return "NO"

# Provided samples
assert run("AS\n2H 4C TH JH AD\n") == "YES", "sample 1"
assert run("4D\n5H 6S 7C 8H 9S\n") == "NO", "sample 2"

# Custom cases
assert run("9H\n9D 2C 3S 4D 5C\n") == "YES", "rank match only"
assert run("KH\n2H 3H 4H 5H 6H\n") == "YES", "suit match multiple"
assert run("TD\n2C 3S 4H 5C 6S\n") == "NO", "no match at all"
assert run("AS\nAD 2D 3D 4D 5D\n") == "YES", "rank match with first card"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 9H\n9D 2C 3S 4D 5C | YES | Rank match only |
| KH\n2H 3H 4H 5H 6H | YES | Multiple cards match suit |
| TD\n2C 3S 4H 5C 6S | NO | No card matches either rank or suit |
| AS\nAD 2D 3D 4D 5D | YES | First card matches rank |

## Edge Cases

For a case where only suit matches, `table_card = 7C` and `hand_cards = 2C 3H 4S 5D 6H`, the first hand card has a suit match. The loop identifies it immediately, printing "YES" and exiting. For a case where only rank matches, `table_card = 5D` and `hand_cards = 5H 2S 3C 4H 6S`, the first card matches by rank, also triggering "YES". For a hand with no matches, the loop completes without finding a match, and the `else` clause correctly prints "NO". This confirms the algorithm handles all non-obvious edge cases correctly.
