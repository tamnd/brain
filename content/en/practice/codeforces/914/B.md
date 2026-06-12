---
title: "CF 914B - Conan and Agasa play a Card Game"
description: "We have a game where Conan and Agasa take turns removing cards from a pile. Each card has a positive integer written on it. When a player chooses a card, not only does that card get removed, but all cards with strictly smaller numbers are removed as well."
date: "2026-06-12T10:02:13+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 914
codeforces_index: "B"
codeforces_contest_name: "Codecraft-18 and Codeforces Round 458 (Div. 1 + Div. 2, combined)"
rating: 1200
weight: 914
solve_time_s: 155
verified: true
draft: false
---

[CF 914B - Conan and Agasa play a Card Game](https://codeforces.com/problemset/problem/914/B)

**Rating:** 1200  
**Tags:** games, greedy, implementation  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a game where Conan and Agasa take turns removing cards from a pile. Each card has a positive integer written on it. When a player chooses a card, not only does that card get removed, but all cards with strictly smaller numbers are removed as well. The game ends when a player cannot make a move because there are no cards left, and that player loses. Conan always moves first. The task is to determine who will win if both play optimally.

The input gives the number of cards `n` and the list of integers on those cards. The output is either "Conan" if the first player can force a win, or "Agasa" if the second player can. The constraints allow `n` up to 100,000 and card values up to 100,000. This means any solution that iterates in quadratic time over the cards or simulates all possible moves is likely too slow. We need a linear or linearithmic solution.

Edge cases arise when many cards have the same number. For example, if all cards are identical and there are an even number, Conan cannot remove all cards in a single turn. Choosing any card only removes cards of that value. Then Agasa can mirror moves until all cards are gone. A small input like `2\n5 5` should output "Agasa", but a careless approach that assumes the largest card always wins would incorrectly return "Conan". Similarly, if one card is unique and larger than all others, Conan can take it and win immediately, as in `3\n4 5 7` where choosing 7 removes all cards.

## Approaches

The brute-force approach would simulate every possible sequence of moves. On Conan's turn, try each card, remove the chosen card and all smaller cards, then recursively compute the opponent's optimal moves. This would be correct but exponential in `n`, since each card choice can lead to multiple recursive branches. Even with memoization, the state space is huge because each subset of remaining cards is a separate state, which makes it infeasible for `n = 10^5`.

The key observation is that the only factor that matters is the **parity of the frequency of each card number**. Each move removes all smaller numbers, so the game effectively reduces to counting how many cards exist for each unique value. If there exists any number with an **odd count**, Conan can always start by taking one of them, leaving an even count or forcing Agasa into a losing position. Conversely, if all counts are even, Agasa can mirror Conan's moves, eventually leaving Conan with no cards on his turn. This reduces the problem to a simple frequency check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input number of cards `n` and the list of card values.
2. Count the frequency of each card value using a dictionary or a `Counter`.
3. Iterate through the frequency values.
4. If any frequency is odd, print "Conan" and stop. The reasoning is that an odd count allows Conan to force the first advantage; whatever move Agasa makes, Conan can respond to maintain parity.
5. If all frequencies are even, print "Agasa". In this case, every move Conan makes can be mirrored by Agasa until the last card is taken on Agasa's turn.
6. End.

Why it works: The invariant is that on any turn, if the frequency of the smallest remaining number is even, the current player cannot gain a decisive advantage. The parity determines who can force a win. By checking odd counts, we immediately determine which player can control the flow.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

n = int(input())
cards = list(map(int, input().split()))
freq = Counter(cards)

for count in freq.values():
    if count % 2 == 1:
        print("Conan")
        break
else:
    print("Agasa")
```

The code reads the number of cards and the card values efficiently. The `Counter` counts how many times each unique card appears. The loop checks for any odd count, which guarantees a winning move for Conan. The `else` on the loop triggers only if no break occurs, meaning all counts are even.

## Worked Examples

**Sample 1**

Input:

```
3
4 5 7
```

| Step | freq | Odd found? | Output decision |
| --- | --- | --- | --- |
| Initialize | {4:1, 5:1, 7:1} | 1st: 1 is odd | Print "Conan" |

Here, all counts are odd, but the first odd detected is enough to declare Conan's win. Choosing the card 7 removes all cards.

**Sample 2**

Input:

```
4
2 2 3 3
```

| Step | freq | Odd found? | Output decision |
| --- | --- | --- | --- |
| Initialize | {2:2, 3:2} | 2 and 2 are even | Loop completes |

All counts are even. Any card Conan takes can be mirrored by Agasa. Eventually, Conan has no moves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Reading input and counting frequencies scales linearly with the number of cards |
| Space | O(n) | The counter stores frequencies for each unique card value, at most `n` keys |

The solution easily fits within the limits for `n = 10^5` and memory of 256 MB.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    cards = list(map(int, input().split()))
    freq = Counter(cards)
    for count in freq.values():
        if count % 2 == 1:
            return "Conan"
    return "Agasa"

# Provided samples
assert run("3\n4 5 7\n") == "Conan", "sample 1"
assert run("4\n2 2 3 3\n") == "Agasa", "sample 2"

# Custom cases
assert run("1\n5\n") == "Conan", "single card"
assert run("2\n5 5\n") == "Agasa", "two identical cards"
assert run("5\n1 1 2 2 2\n") == "Conan", "mixed parity counts"
assert run("6\n1 1 2 2 3 3\n") == "Agasa", "all even counts"
assert run("7\n7 7 7 8 8 8 9\n") == "Conan", "complex parity mix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n5 | Conan | Single card, first player wins |
| 2\n5 5 | Agasa | Even count of identical cards |
| 5\n1 1 2 2 2 | Conan | Mixed parity counts |
| 6\n1 1 2 2 3 3 | Agasa | All even counts |
| 7\n7 7 7 8 8 8 9 | Conan | Odd counts among multiple numbers |

## Edge Cases

For a single card `1\n5`, the frequency is `{5:1}`, which is odd. The algorithm prints "Conan" as expected. For two identical cards `2\n5 5`, the frequency is `{5:2}`, even. The loop finds no odd count, so "Agasa" is printed. For a mixed count like `5\n1 1 2 2 2`, frequencies are `{1:2, 2:3}`. The first odd (2:3) triggers "Conan", showing the algorithm correctly detects the winning strategy. The implementation consistently handles large inputs and parity logic correctly.
