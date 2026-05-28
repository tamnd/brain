---
title: "CF 104A - Blackjack"
description: "We are given a simplified blackjack scenario where the first card is fixed: the queen of spades, which contributes 10 points. The player wants the sum of this card and a second card to equal a given number n, which ranges from 1 to 25."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 104
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 80 (Div. 2 Only)"
rating: 800
weight: 104
solve_time_s: 74
verified: true
draft: false
---

[CF 104A - Blackjack](https://codeforces.com/problemset/problem/104/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a simplified blackjack scenario where the first card is fixed: the queen of spades, which contributes 10 points. The player wants the sum of this card and a second card to equal a given number `n`, which ranges from 1 to 25. The task is to determine how many different second cards will produce exactly that total.

Cards have the following point values: 2 through 10 are worth their face value, jacks, queens, and kings are worth 10, and aces can be 1 or 11. Each value has four cards, one per suit, except that the queen of spades is already taken and cannot be reused.

The problem’s constraints are small: `n` goes up to 25, and the deck size is fixed at 52 cards. This means any solution that iterates through card values and suits a few times will run comfortably under the 2-second limit. The key non-obvious detail is handling aces correctly: they can be counted as 1 or 11, and the queen’s 10 points combine with that choice to reach `n`. Another subtlety is that if `n` is less than or equal to 10, an ace counted as 11 would overshoot, so it must be considered carefully. For instance, if `n = 11`, the second card could be an ace counted as 1, but the ace as 11 would exceed `n`. Ignoring this will produce incorrect counts.

## Approaches

A naive approach would iterate through all 51 remaining cards, sum their values with the queen’s 10 points, and count the ones matching `n`. This would be correct but somewhat inelegant. Given the small input size, even such an exhaustive check works, but reasoning carefully allows a direct computation based on card values and suits.

The key insight is to think in terms of the required value for the second card rather than enumerating every card. Since the first card contributes 10 points, the second card must provide exactly `n - 10` points. Then we map this target to the set of possible card values: 2 through 10, jacks, queens, kings (all 10 points), and ace (1 or 11). Each numeric value from 2 to 10 has four suits, 10-point face cards have four suits each (minus the queen of spades), and aces have four suits. Checking these combinations directly produces the count without iterating through every card individually. This avoids unnecessary looping while staying intuitive.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(51) | O(1) | Acceptable due to small deck size |
| Optimal | O(1) | O(1) | Accepted and clean |

## Algorithm Walkthrough

1. Read `n`, the target sum including the first card.
2. The first card is a queen of spades, so its value is 10. Compute the remaining value required from the second card: `needed = n - 10`.
3. If `needed` is less than 1 or greater than 11, no card can satisfy the requirement, so the result is 0. This handles the edge cases where the target sum is impossible given blackjack rules.
4. If `needed` is exactly 10, the second card can be any 10-point card. Normally, there are 16 ten-point cards (four tens, four jacks, four queens, four kings). Since the queen of spades is already used, subtract 1 to get 15.
5. If `needed` is exactly 11, only an ace counted as 11 works, and there are 4 aces.
6. For all other values between 1 and 9 inclusive, there are exactly 4 cards corresponding to that numeric value, one per suit.
7. Print the computed number.

The correctness comes from exhaustively mapping the required points to the set of possible card values, considering the special values (10 points for face cards and aces’ dual value) and the already used queen. Each step handles all possible numeric outcomes.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
needed = n - 10

if needed < 1 or needed > 11:
    print(0)
elif needed == 10:
    # tens, jacks, queens, kings: 16 total, minus the queen of spades
    print(15)
elif needed == 11:
    # only aces counted as 11
    print(4)
else:
    # 2-9 and ace as 1
    print(4)
```

The code begins by computing the difference between the target sum and the queen’s value. Conditional branches handle impossible values, 10-point cards (subtracting the queen of spades), aces as 11, and numeric cards. There are no loops because the mapping is direct, avoiding off-by-one mistakes in counting suits.

## Worked Examples

### Sample Input 1

```
12
```

| Variable | Value |
| --- | --- |
| n | 12 |
| needed | 2 |
| Output | 4 |

Explanation: To reach 12, the second card must be worth 2 points. There are four twos (hearts, diamonds, clubs, spades). Each is valid.

### Sample Input 2

```
20
```

| Variable | Value |
| --- | --- |
| n | 20 |
| needed | 10 |
| Output | 15 |

Explanation: The second card must be 10 points. Tens, jacks, queens, and kings count. There are 16 cards in total, but the queen of spades is already in play, leaving 15.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic and conditional checks; no loops over cards |
| Space | O(1) | Constant space for a few integer variables |

Given the fixed deck size and small `n` values, this solution is effectively instantaneous and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    needed = n - 10
    if needed < 1 or needed > 11:
        return "0"
    elif needed == 10:
        return "15"
    elif needed == 11:
        return "4"
    else:
        return "4"

# Provided samples
assert run("12\n") == "4", "sample 1"
assert run("20\n") == "15", "sample 2"
assert run("10\n") == "0", "sample 3"

# Custom cases
assert run("1\n") == "0", "minimum impossible"
assert run("11\n") == "4", "ace counted as 1"
assert run("21\n") == "4", "ace counted as 11"
assert run("15\n") == "4", "numeric card in range 2-9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | n too low to reach 10 points |
| 11 | 4 | ace counted as 1 |
| 21 | 4 | ace counted as 11 |
| 15 | 4 | numeric card in 2-9 range |

## Edge Cases

For `n = 1`, `needed = -9`. Since no card can subtract points, the output is correctly 0. For `n = 21`, `needed = 11`. Only aces counted as 11 suffice; all four suits are valid, confirming correct handling of aces. For `n = 20`, `needed = 10`. Subtracting the queen of spades ensures we do not overcount 10-point cards. Each of these demonstrates the algorithm handles boundary conditions and special card values correctly.
