---
title: "CF 102261C - \u0418\u043d\u0442\u0435\u0440\u0435\u0441\u043d\u0430\u044f \u0438\u0433\u0440\u0430"
description: "Petya has a sequence of N cards, and each card contains a nonnegative integer. Before the game starts, Vasya chooses the target score K. Petya then reveals the cards from left to right."
date: "2026-08-17T20:45:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102261
codeforces_index: "C"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102261
solve_time_s: 75
verified: true
draft: false
---

[CF 102261C - \u0418\u043d\u0442\u0435\u0440\u0435\u0441\u043d\u0430\u044f \u0438\u0433\u0440\u0430](https://codeforces.com/problemset/problem/102261/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

Petya has a sequence of N cards, and each card contains a nonnegative integer. Before the game starts, Vasya chooses the target score K. Petya then reveals the cards from left to right.

A card divisible by 5 gives Vasya one point, while a card divisible by 3 gives Petya one point. A number divisible by both 3 and 5 gives nobody a point, as does a number divisible by neither. The game ends immediately when one player reaches K points. If all cards have been processed without either player reaching K, the player with the larger score wins, and equal scores produce a draw.

The input gives K, the target score, followed by N and the N card values. The required output is `Petya`, `Vasya`, or `Draw`, depending on the winner of this exact sequential game.

The important constraint is N <= 10^6. A solution has to be essentially linear in the number of cards because even O(N log N) is unnecessary here, while anything quadratic would require around 10^12 operations in the worst case. Each card value is at most 1000, so testing divisibility by the two fixed numbers 3 and 5 can be done with constant-time remainder operations.

There are several edge cases that can make an apparently reasonable implementation wrong. First, a number divisible by both 3 and 5 gives no points. For example,

```
1 1
15
```

produces `Draw`, not `Petya` or `Vasya`. Since 15 is divisible by both numbers, neither score changes.

Second, the order of the cards matters because the game stops immediately. For example,

```
2 3
3 5 3
```

produces `Petya`. Petya receives points from the first and third cards, but after the third card he reaches 2 points and wins. A solution that simply counts all cards and compares totals would happen to get this case right, but that approach cannot reproduce cases where one player reaches K before later cards are processed.

Third, zero is divisible by every positive integer. Thus,

```
1 1
0
```

produces `Draw`, because zero is divisible by both 3 and 5 and awards nobody a point. Treating zero as divisible by neither would incorrectly give the result `Petya` or `Vasya` depending on the implementation.

## Approaches

A direct brute-force implementation can simulate the game, but suppose divisibility is handled by a generic search over possible divisors for every card. For a card with value x, such a method may inspect up to x candidates before deciding how the card behaves. Since x can be 1000 and there can be 10^6 cards, the worst case reaches about 10^9 divisor checks. That is far beyond what a one-second limit can tolerate.

The brute-force simulation is conceptually correct because every card affects the score exactly according to its divisibility properties, and processing cards in order reproduces the actual game. The problem is not the simulation itself. The waste comes from treating a very simple divisibility test as a general arithmetic search.

The key observation is that the only relevant divisors are fixed in advance: 3 and 5. We do not need to discover whether a number is divisible by them. Two remainder operations, `x % 3` and `x % 5`, completely determine the card's effect.

There is another useful observation about the stopping condition. The moment either score reaches K, the answer is already known, so there is no reason to inspect later cards. In the worst case we still process all N cards, but the complexity is O(N), which is optimal because the input itself contains N values.

The resulting approach is simply one left-to-right scan. For every card, first check the case where it is divisible by both 3 and 5, because that case gives no points. Otherwise, increment Petya's score if it is divisible by 3, or Vasya's score if it is divisible by 5. After every scoring card, check whether the corresponding player has reached K.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Generic divisor search | O(N · max(A)) | O(1) | Too slow |
| Direct simulation with `% 3` and `% 5` | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read K and N, then process the cards from the first one to the last one. The order must be preserved because reaching K ends the game immediately.
2. Maintain two counters, `petya` and `vasya`, initially both zero. They represent the exact scores after all cards processed so far.
3. For each value `x`, first check whether `x` is divisible by both 3 and 5. If it is, leave both counters unchanged. This condition must be checked before the individual divisibility tests because such a card awards no point to either player.
4. If `x` is divisible by 3 but not by 5, increment `petya`. Immediately check whether `petya == K`. If so, print `Petya` and terminate because later cards cannot change the winner.
5. If `x` is divisible by 5 but not by 3, increment `vasya`. Immediately check whether `vasya == K`. If so, print `Vasya` and terminate for the same reason.
6. If all N cards have been processed without either player reaching K, compare the two final scores. The larger score determines the winner, while equal scores produce `Draw`.

The invariant is that after processing any prefix of the card sequence, `petya` and `vasya` are exactly the scores that the real game would have at that moment, provided the game has not already ended. Every card falls into exactly one relevant category: divisible by both, divisible only by 3, divisible only by 5, or divisible by neither. The algorithm applies exactly the rule for that category. Because it checks the target immediately after every score increase, it also stops at exactly the same card where the real game would stop. If no target is reached, the final counters are the actual final scores, so their comparison gives the required result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    K, N = map(int, input().split())

    petya = 0
    vasya = 0

    for _ in range(N):
        x = int(input().split()[0]) if False else None

    # The official input places all N numbers on the next line.
    # Re-read using a direct iterator for fast processing.
```

The input contains all N card values on the next line, so the clean implementation is to iterate over that line directly:

```python
import sys
input = sys.stdin.readline

def solve():
    K, N = map(int, input().split())

    petya = 0
    vasya = 0

    cards = map(int, input().split())

    for x in cards:
        divisible_by_3 = (x % 3 == 0)
        divisible_by_5 = (x % 5 == 0)

        if divisible_by_3 and divisible_by_5:
            continue

        if divisible_by_3:
            petya += 1
            if petya == K:
                print("Petya")
                return

        elif divisible_by_5:
            vasya += 1
            if vasya == K:
                print("Vasya")
                return

    if petya > vasya:
        print("Petya")
    elif vasya > petya:
        print("Vasya")
    else:
        print("Draw")

if __name__ == "__main__":
    solve()
```

The first two variables store the current scores. They never need to exceed K because the function returns immediately when a score reaches the target.

The two boolean expressions compute the divisibility properties once per card. The combined case is handled first, which is essential for values such as 0, 15, 30, and every other multiple of 15.

The `elif` structure also guarantees that a card divisible only by 3 gives exactly one point to Petya, while a card divisible only by 5 gives exactly one point to Vasya. A number divisible by neither reaches neither branch.

The equality check against K is sufficient because a counter increases only by one. A score cannot jump from K-1 to a value greater than K. The function returns as soon as the winner is determined, so the remaining cards do not affect the result.

The solution follows the input format directly and does not store the entire card array. `map` produces the converted integers lazily from the split input tokens, keeping the algorithm's additional data structure effectively constant-sized.

## Worked Examples

For Sample 1, the input is:

```
3 10
1 2 3 4 5 6 7 8 9 10
```

The target is 3. Values divisible by 3 give Petya points, and values divisible by 5 give Vasya points.

| Card | Value | Petya score | Vasya score | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | No point |
| 2 | 2 | 0 | 0 | No point |
| 3 | 3 | 1 | 0 | Petya scores |
| 4 | 4 | 1 | 0 | No point |
| 5 | 5 | 1 | 1 | Vasya scores |
| 6 | 6 | 2 | 1 | Petya scores |
| 7 | 7 | 2 | 1 | No point |
| 8 | 8 | 2 | 1 | No point |
| 9 | 9 | 3 | 1 | Petya reaches K |

Petya reaches three points on the ninth card, so the algorithm returns immediately with `Petya`. The final card is never relevant to the result.

For Sample 2, the input is:

```
4 16
1 2 3 4 5 6 7 8 9 10 15 20 25 24 21 18
```

Here K is 4. The cards divisible by both 3 and 5, such as 15, must not give points.

| Card | Value | Petya score | Vasya score | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | No point |
| 2 | 2 | 0 | 0 | No point |
| 3 | 3 | 1 | 0 | Petya scores |
| 4 | 4 | 1 | 0 | No point |
| 5 | 5 | 1 | 1 | Vasya scores |
| 6 | 6 | 2 | 1 | Petya scores |
| 7 | 7 | 2 | 1 | No point |
| 8 | 8 | 2 | 1 | No point |
| 9 | 9 | 3 | 1 | Petya scores |
| 10 | 10 | 3 | 2 | Vasya scores |
| 11 | 15 | 3 | 2 | Both divisible, no point |
| 12 | 20 | 3 | 3 | Vasya scores |
| 13 | 25 | 3 | 4 | Vasya reaches K |

Vasya reaches four points on card 13, so the game ends there and the answer is `Vasya`. The last three cards do not matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each card is inspected once and uses a constant number of arithmetic operations. |
| Space | O(1) auxiliary | Only K, N, and the two score counters are stored explicitly. |

With N up to 10^6, a linear scan performs at most one million card iterations, which is appropriate for the constraints. There is no sorting, nested iteration, or auxiliary array proportional to N. The direct remainder checks also avoid any dependence on the numerical value beyond constant-time arithmetic.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def solve():
    K, N = map(int, input().split())

    petya = 0
    vasya = 0

    for x in map(int, input().split()):
        by3 = (x % 3 == 0)
        by5 = (x % 5 == 0)

        if by3 and by5:
            continue

        if by3:
            petya += 1
            if petya == K:
                print("Petya")
                return

        elif by5:
            vasya += 1
            if vasya == K:
                print("Vasya")
                return

    if petya > vasya:
        print("Petya")
    elif vasya > petya:
        print("Vasya")
    else:
        print("Draw")

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            solve()
            return sys.stdout.getvalue().strip()
        finally:
            sys.stdout = old_stdout
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run("""3 10
1 2 3 4 5 6 7 8 9 10
""") == "Petya", "sample 1"

assert run("""4 16
1 2 3 4 5 6 7 8 9 10 15 20 25 24 21 18
""") == "Vasya", "sample 2"

assert run("""3 5
3 5 15 15 15
""") == "Draw", "sample 3"

# Minimum-size input, zero is divisible by both 3 and 5.
assert run("""1 1
0
""") == "Draw", "zero gives nobody a point"

# K is reached exactly on the final card.
assert run("""2 3
5 3 6
""") == "Petya", "Petya reaches K on the final card"

# All cards are divisible by both 3 and 5.
assert run("""1 4
0 15 30 45
""") == "Draw", "all cards give no points"

# Vasya reaches K before a later Petya-scoring card.
assert run("""2 4
5 10 3 3
""") == "Vasya", "immediate stopping"

# Large N. Petya reaches K very early, while the remaining cards are irrelevant.
large_input = "1000 1000000\n" + "3 " * 1000000
assert run(large_input) == "Petya", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `Draw` | Minimum input and the special divisibility behavior of zero |
| `2 3 / 5 3 6` | `Petya` | Reaching K exactly on the final card |
| `1 4 / 0 15 30 45` | `Draw` | Every card divisible by both 3 and 5 |
| `2 4 / 5 10 3 3` | `Vasya` | The game stops immediately when Vasya reaches K |
| `1000 1000000 / 3 ...` | `Petya` | Maximum N and early termination |

## Edge Cases

The first edge case is a card divisible by both 3 and 5. Consider:

```
1 1
15
```

For `x = 15`, both `x % 3 == 0` and `x % 5 == 0` are true. The combined condition executes `continue`, so both scores remain zero. All cards are now exhausted, the scores are equal, and the result is `Draw`. Without the combined check, the same card could incorrectly award a point to one of the players.

The second edge case is zero:

```
1 1
0
```

Zero satisfies both divisibility tests because 0 is a multiple of every positive integer. The algorithm consequently treats it exactly like 15 and awards no points. The final scores are 0 and 0, so the result is `Draw`.

The third edge case is immediate termination:

```
2 4
5 10 3 3
```

After the first card the scores are 0 and 1. After the second they are 0 and 2, so Vasya reaches K and the algorithm prints `Vasya` immediately. The two remaining cards would give Petya two points, but they must never be considered because the actual game has already ended.

The fourth edge case is reaching K exactly at the end:

```
2 3
5 3 6
```

The scores after the first two cards are 1 for Vasya and 1 for Petya. The final card, 6, is divisible by 3 but not by 5, so Petya becomes the first player to reach 2 points. The algorithm prints `Petya` at that moment rather than falling through to the final score comparison.

The fifth edge case is when nobody reaches K and the final scores determine the winner. For example,

```
5 4
3 5 6 5
```

gives Petya two points from 3 and 6, while Vasya gets two points from the two 5s. Neither reaches five, so the cards finish with equal scores and the result is `Draw`. The final comparison is only used after the entire sequence has been processed without an earlier winner.
