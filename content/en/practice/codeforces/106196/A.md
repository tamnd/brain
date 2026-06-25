---
title: "CF 106196A - \u041a\u0440\u0443\u0433\u043b\u0430\u044f \u043a\u0430\u0440\u0442\u0430"
description: "The task describes one decision in the card game Durak. We are given the trump suit and two different cards. The first card is played as the attacking card, and we need to decide whether it can cover the second card. A card can cover another card in exactly two situations."
date: "2026-06-25T10:34:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106196
codeforces_index: "A"
codeforces_contest_name: "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2025"
rating: 0
weight: 106196
solve_time_s: 32
verified: true
draft: false
---

[CF 106196A - \u041a\u0440\u0443\u0433\u043b\u0430\u044f \u043a\u0430\u0440\u0442\u0430](https://codeforces.com/problemset/problem/106196/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes one decision in the card game Durak. We are given the trump suit and two different cards. The first card is played as the attacking card, and we need to decide whether it can cover the second card.

A card can cover another card in exactly two situations. If both cards have the same suit, the first card wins when its rank is higher. If the first card belongs to the trump suit and the second card does not, the first card also wins regardless of ranks. All other combinations are losing.

The input contains a single character for the trump suit, followed by two card descriptions. Each card has two characters: the first is its rank and the second is its suit. The output is `YES` when the first card covers the second one, otherwise it is `NO`.

The constraints are tiny because there are only two cards and no repeated processing. A simulation, sorting, or any advanced data structure would be unnecessary. The solution only needs a few comparisons, so constant time is enough.

The main mistakes come from confusing the two rules or forgetting their order. A common wrong approach is to compare ranks before checking suits, which incorrectly allows a strong non-trump card to beat a trump card.

For example:

```
Input:
H
AS KH

Output:
NO
```

A careless implementation might see that `A` is higher than `K` and answer `YES`, but the suits are different and the first card is not a trump card. The second card cannot be covered.

Another edge case is when both cards are trump cards.

```
Input:
S
7S 6S

Output:
YES
```

The trump rule does not need to be used here. The cards simply have the same suit, and the rank comparison decides the result.

A final edge case is when the first card is trump and the second one is not, even if the trump card has a smaller rank.

```
Input:
C
6C AS

Output:
YES
```

The rank comparison alone would fail because `6` is lower than `A`, but the trump rule overrides ranks.

## Approaches

The brute-force approach would be to try to model the entire game logic, checking possible ways cards could interact and searching through all rules. This would still produce the correct result because the game has only one comparison to make, but it solves a much larger problem than necessary. Even a tiny simulation is wasted work here because the answer depends only on the two given cards and the trump suit.

The key observation is that the covering relation has a direct definition. We do not need to explore possibilities. We only need to translate the two winning conditions into boolean checks.

The brute-force idea fails in the sense that it adds unnecessary complexity. The observation that there are only two independent reasons for one card to beat another reduces the problem to a constant number of character comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of simulated game states) | O(number of simulated states) | Too complex for the task |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the trump suit and the two card descriptions. Split each card into its rank and suit so the two properties can be compared independently.
2. Check whether the first card is a trump card while the second card is not. If this is true, the first card immediately covers the second one because trump always beats a non-trump card.
3. If the trump condition did not decide the answer, check whether both cards have the same suit. When the suits match, compare their ranks using the given rank order.
4. Output `YES` if the rank of the first card is higher in the same suit case. Otherwise output `NO`.

Why it works: the algorithm follows the complete definition of the covering relation. The only winning cases are a trump card beating a non-trump card or two cards of the same suit where the first has a higher rank. Since every possible pair of cards either satisfies one of these conditions or does not, the result is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    trump = input().strip()
    a, b = input().split()

    ranks = "6789TJQKA"

    a_rank, a_suit = a[0], a[1]
    b_rank, b_suit = b[0], b[1]

    if a_suit == trump and b_suit != trump:
        print("YES")
    elif a_suit == b_suit and ranks.index(a_rank) > ranks.index(b_rank):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The string `ranks` stores the cards in increasing order. Using `index` converts a rank character into a number that can be compared directly. For example, `K` appears after `Q`, so its index is larger.

The trump check is performed first because it does not depend on rank. A low trump card can still beat a high non-trump card, so comparing ranks before checking trump would introduce an error.

The second condition handles cards of the same suit. Since the input guarantees the cards are different, equality of ranks cannot happen between the two cards, but the strict comparison also matches the rules exactly.

The implementation uses only a few variables and never creates extra collections, so there are no boundary or memory concerns.

## Worked Examples

### Sample 1

Input:

```
H
QH 9S
```

The first card is `QH`, the second is `9S`.

| Step | Trump | First card | Second card | Condition checked | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | H | QH | 9S | First card is trump and second is not | True |
| 2 | H | QH | 9S | Covering succeeds | YES |

The first card is a heart, which is trump, while the second card is not. Rank comparison is irrelevant.

### Sample 2

Input:

```
S
8D 6D
```

| Step | Trump | First card | Second card | Condition checked | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | S | 8D | 6D | First card is trump and second is not | False |
| 2 | S | 8D | 6D | Same suit and higher rank | True |
| 3 | S | 8D | 6D | Final answer | YES |

This example confirms the normal same-suit comparison. The trump suit does not matter because neither card is a trump card.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of character comparisons and rank lookups are performed |
| Space | O(1) | Only a few strings and variables are stored |

The solution easily fits within the limits because the work does not depend on any large input size. It performs the same amount of computation for every test case.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    trump = sys.stdin.readline().strip()
    a, b = sys.stdin.readline().split()

    ranks = "6789TJQKA"

    a_rank, a_suit = a[0], a[1]
    b_rank, b_suit = b[0], b[1]

    if a_suit == trump and b_suit != trump:
        ans = "YES"
    elif a_suit == b_suit and ranks.index(a_rank) > ranks.index(b_rank):
        ans = "YES"
    else:
        ans = "NO"

    sys.stdin = old_stdin
    return ans

assert solve_data("H\nQH 9S\n") == "YES", "sample 1"
assert solve_data("S\n8D 6D\n") == "YES", "sample 2"
assert solve_data("C\n7H AS\n") == "NO", "sample 3"

assert solve_data("C\n6C AS\n") == "YES", "trump beats stronger non-trump"
assert solve_data("H\n6S AH\n") == "NO", "non-trump cannot beat trump"
assert solve_data("D\nAD KD\n") == "YES", "same suit highest rank"
assert solve_data("S\n6H 7H\n") == "NO", "same suit lower rank"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `C / 6C AS` | YES | Trump rule works even with a lower rank |
| `H / 6S AH` | NO | Non-trump cards cannot beat trump cards |
| `D / AD KD` | YES | Highest same-suit rank comparison |
| `S / 6H 7H` | NO | Lower same-suit card fails |

## Edge Cases

For the trump versus non-trump case:

```
Input:
C
6C AS
```

The algorithm first checks whether the first card is a trump card. `6C` has the trump suit and `AS` does not, so it immediately returns `YES`. It never compares `6` and `A`, which avoids the common mistake of rejecting a valid trump move.

For the case where the second card is trump:

```
Input:
H
6S AH
```

The first card is not a trump card and the suits differ. The first condition fails, and the same-suit condition also fails. The algorithm returns `NO`, which matches the rule that non-trump cards cannot cover trump cards.

For same-suit cards:

```
Input:
D
AD KD
```

Both cards have diamonds. The trump suit is irrelevant because the first card already wins by having a higher rank in the same suit. The rank lookup gives `A` a larger position than `K`, so the answer is `YES`.

For the lower-rank same-suit case:

```
Input:
S
6H 7H
```

Both cards are hearts, but the first card's rank is smaller. The algorithm reaches the same-suit comparison and returns `NO`, preventing an incorrect answer caused by checking only whether suits match.
