---
title: "CF 106263G - \u5c0f\u6a58\u7684\u7cd6\u679c\u6e38\u620f"
description: "We are given a turn-based game played on a single pile of candies. Two players alternate moves, with the first player always moving first. On each move, the current player must remove exactly 1, 3, or 4 candies from the pile."
date: "2026-06-18T23:20:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106263
codeforces_index: "G"
codeforces_contest_name: "2025 \u534e\u5357\u5e08\u8303\u5927\u5b66\u201c\u5353\u8d8a\u6559\u80b2\u676f\u201d\u7b97\u6cd5\u4e0e\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u65b0\u751f\u8d5b\uff09"
rating: 0
weight: 106263
solve_time_s: 64
verified: true
draft: false
---

[CF 106263G - \u5c0f\u6a58\u7684\u7cd6\u679c\u6e38\u620f](https://codeforces.com/problemset/problem/106263/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a turn-based game played on a single pile of candies. Two players alternate moves, with the first player always moving first. On each move, the current player must remove exactly 1, 3, or 4 candies from the pile. If a player starts their turn and cannot make a legal move, meaning the pile is empty or no allowed move fits the remaining count, that player loses immediately.

Each test case gives an initial number of candies, and we need to determine which player wins under optimal play. The output is simply the name of the winning player: “Orange” for the first mover and “ice” for the second mover.

The constraints allow up to 100000 test cases and values of n up to 1e9. This immediately rules out any per-test dynamic programming over the full range up to n. Even a linear DP up to 1e9 is impossible, and even precomputing up to 1e9 is infeasible in both time and memory. The solution must reduce each query to constant time after a small preprocessing phase or derive a direct formula.

There are two subtle edge cases that often break naive reasoning.

First, n = 0. The first player has no move and loses immediately, so the answer must be “ice”. Any DP that assumes starting positions are winning will incorrectly mark this as a win unless explicitly handled.

Second, small values like n = 2 expose incorrect greedy thinking. From 2 candies, the only move is to take 1, leaving 1 for the opponent, and that position is winning for the next player. So 2 is losing for the current player, even though it might look symmetric or “small enough to win”.

A third structural edge case is that the allowed moves are not symmetric like {1,2}. The presence of 3 and 4 creates a periodic structure rather than a simple parity pattern. Any attempt to reduce the game to “odd wins, even loses” fails immediately, for example n = 3 is directly winning because you can take all candies.

## Approaches

The most direct way to analyze this game is standard impartial game DP. Let us define a state dp[n] that is true if the current player can force a win with n candies remaining. From a position n, the player tries all valid moves: removing 1, 3, or 4 candies, and transitions to dp[n-1], dp[n-3], and dp[n-4] when those states exist. A position is winning if at least one move leads to a losing position for the opponent.

This recurrence is correct, but computing it up to n = 1e9 is impossible. Even if we only compute up to a moderate limit like 1e7, the number of test cases and memory requirements become too large.

The key observation is that this is a subtraction game with a fixed move set. Such games often become periodic after a short prefix because the state only depends on a small number of previous values. Here dp[n] depends only on dp[n-1], dp[n-3], and dp[n-4], so the state space is bounded and the sequence eventually repeats.

By computing dp for the first few dozen values, we observe a repeating pattern. In fact, the losing positions repeat with period 7. Once this cycle is identified, every query reduces to computing n modulo 7 and checking a fixed lookup table.

This turns the problem into constant time per query after O(1) preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute DP up to n | O(n) per test or O(max n) total | O(n) | Too slow |
| Periodic DP + modulo | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We first compute the winning and losing states for small values of n until a cycle becomes apparent. We define a boolean array where false means losing and true means winning.

We initialize dp[0] as losing because a player with no candies cannot move. From there, we iteratively compute dp[i] using the allowed transitions from i − 1, i − 3, and i − 4 whenever those indices are valid.

As we extend the table, we look for repetition in the pattern of dp values. Once we see that the sequence stabilizes into a repeating cycle of length 7, we stop preprocessing and record the period.

At this point, we build a lookup table of size 7 that encodes whether n mod 7 corresponds to a winning or losing position.

For each query n, we compute r = n mod 7. If dp_pattern[r] indicates a winning state, we output “Orange”, otherwise we output “ice”.

### Why it works

This game is a finite subtraction game with a bounded move set. The state of each position depends only on a constant number of previous states, so the sequence of dp values forms a linear recurrence over a finite binary alphabet. Such sequences must eventually become periodic. Once the periodic region is reached, the value of dp[n] depends only on n modulo the cycle length, so reducing n modulo the discovered period preserves correctness for all large values.

## Python Solution

```python
import sys
input = sys.stdin.readline

# Precompute DP until we see a cycle
moves = [1, 3, 4]
N = 50  # enough to observe periodicity

dp = [False] * (N + 1)
dp[0] = False

for i in range(1, N + 1):
    win = False
    for m in moves:
        if i - m >= 0 and not dp[i - m]:
            win = True
    dp[i] = win

# Observed cycle for this problem: period 7 starting early
# We extract pattern for mod 7
pattern = [dp[i] for i in range(7)]

t = int(input())
out = []

for _ in range(t):
    n = int(input())
    if pattern[n % 7]:
        out.append("Orange")
    else:
        out.append("ice")

print("\n".join(out))
```

The code first builds a small DP table sufficient to reveal the structure of the game. The transition checks whether any valid move leads to a losing state; if so, the current state is winning.

After computing enough values, we directly read off the behavior of dp[i] modulo 7. The constant-size pattern array stores whether each residue class is winning.

Each query then reduces to a single modulo operation and a table lookup. This avoids any dependence on n.

A subtle point is handling dp[0] correctly. It must be initialized as losing, since the current player has no valid move. All further states depend on this base case.

## Worked Examples

Consider n = 5, n = 6, and n = 7. We trace the DP decisions.

### Example trace

| i | i-1 | i-3 | i-4 | dp[i] decision |
| --- | --- | --- | --- | --- |
| 0 | - | - | - | losing |
| 1 | 0 | - | - | win (take 1) |
| 2 | 1 | - | - | losing |
| 3 | 2 | 0 | - | win (take 3) |
| 4 | 3 | 1 | 0 | win |
| 5 | 4 | 2 | 1 | win |

For n = 2, every move leads to a winning state for the opponent, so it is losing. For n = 4, taking 4 immediately wins, making it winning.

Now consider larger values to show periodicity:

| n | n mod 7 | result |
| --- | --- | --- |
| 6 | 6 | losing |
| 7 | 0 | losing |
| 8 | 1 | winning |

This confirms that behavior stabilizes into a repeating pattern based on residue class.

The traces show that the game is not governed by parity alone. The availability of 3 and 4 moves creates winning jumps that disrupt simple patterns but still produce a bounded cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | each test case uses one modulo and lookup |
| Space | O(1) | only a constant-size DP pattern is stored |

The solution easily fits within constraints since T can be as large as 100000 and each query is answered in constant time with negligible overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    moves = [1, 3, 4]
    N = 50

    dp = [False] * (N + 1)
    dp[0] = False

    for i in range(1, N + 1):
        win = False
        for m in moves:
            if i - m >= 0 and not dp[i - m]:
                win = True
        dp[i] = win

    pattern = [dp[i] for i in range(7)]

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        res.append("Orange" if pattern[n % 7] else "ice")

    return "\n".join(res)

# provided sample (illustrative; exact sample not fully specified)
# assert run("3\n0\n1\n2\n") == "ice\nOrange\nice"

# custom cases
assert run("1\n0\n") == "ice"
assert run("1\n3\n") == "Orange"
assert run("1\n2\n") == "ice"
assert run("1\n7\n") == "ice"
assert run("1\n8\n") == "Orange"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 0 | ice | empty pile losing base case |
| 1, 3 | Orange | immediate winning move exists |
| 1, 2 | ice | forced loss case |
| 1, 7 | ice | periodic losing residue |
| 1, 8 | Orange | wrap-around correctness after period |

## Edge Cases

For n = 0, the algorithm directly assigns ice because dp_pattern[0] is false. This matches the fact that no move exists, so the first player immediately loses.

For n = 2, the residue class leads to a losing state. Tracing the DP confirms that both possible outcomes (taking 1) leave a winning position for the opponent, so the correct output is ice.

For n = 7, we compute r = 0. The pattern marks this as losing, so ice wins. Even though 7 allows multiple moves, each option leads to a state that can be countered optimally.

For n = 8, r = 1, which is winning. The algorithm outputs Orange, consistent with the fact that the first player can force a win by moving into a losing residue class.
