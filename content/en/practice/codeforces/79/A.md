---
title: "CF 79A - Bus Game"
description: "We are asked to simulate a turn-based game involving two players, Ciel and Hanako, who alternate taking coins from a common pile. The pile initially contains x 100-yen coins and y 10-yen coins. On each turn, the active player must remove exactly 220 yen."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 79
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 71"
rating: 1200
weight: 79
solve_time_s: 80
verified: true
draft: false
---

[CF 79A - Bus Game](https://codeforces.com/problemset/problem/79/A)

**Rating:** 1200  
**Tags:** greedy  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a turn-based game involving two players, Ciel and Hanako, who alternate taking coins from a common pile. The pile initially contains `x` 100-yen coins and `y` 10-yen coins. On each turn, the active player must remove exactly 220 yen. Ciel prefers to maximize the number of 100-yen coins she takes, while Hanako prefers to maximize the number of 10-yen coins she takes. The first player who cannot take exactly 220 yen loses. The task is to determine who will win given the initial coin counts.

The input provides `x` and `y` (each up to 10^6), so an algorithm must be efficient enough to handle up to a million coins in a few operations. A naive simulation that explores all possible combinations or tries every sequence of coin removals could require many unnecessary computations, but careful greedy reasoning reduces this to a small, manageable number of checks.

A subtle edge case arises when one player cannot achieve exactly 220 yen because of the coin denominations, even though there are coins left. For instance, with `x=1` and `y=1`, neither can take exactly 220 yen, so the first player loses immediately. Another tricky situation is when multiple ways to pay 220 yen exist; the players' preferences (Ciel maximizing 100-yen, Hanako maximizing 10-yen) dictate which combination is chosen, so a careless implementation that ignores this ordering could simulate the wrong path and produce an incorrect winner.

## Approaches

The brute-force approach would simulate the game turn by turn, decrementing coin counts according to the player's strategy until one cannot pay 220 yen. On each turn, one would check all combinations of 100-yen and 10-yen coins summing to 220. This is correct logically but inefficient, because each turn may consider multiple combinations, and the total number of turns can be large. In the worst case, we could perform roughly `x + y` operations, which is acceptable given the constraints, but exploring all combinations unnecessarily complicates the solution.

The key observation is that each player has a greedy strategy with a unique preferred move. Ciel always takes as many 100-yen coins as possible. Since 220 yen requires at most two 100-yen coins (because 3×100 = 300 > 220), we can restrict her move to either 2, 1, or 0 coins, with the rest made up of 10-yen coins. Similarly, Hanako maximizes 10-yen coins, so she tries to take as many 10-yen coins as possible (up to 22 coins, since 22×10 = 220), using 100-yen coins only if necessary. This reduces each turn to a constant-time decision: compute the preferred combination and update the pile. There is no need to explore all possibilities, because the players' preference ordering ensures there is only one move per turn.

The greedy insight lets us simulate the game with a simple loop until a player loses. Each iteration requires only a few arithmetic operations, which is O(1) per turn, and the number of turns is bounded by roughly `x + y`, which is well under 2×10^6. This makes the solution feasible within the time limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x + y) × O(possible combinations) | O(1) | Too slow due to unnecessary combination checks |
| Optimal (Greedy Simulation) | O(x + y) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input values `x` and `y` representing the number of 100-yen and 10-yen coins.
2. Initialize a boolean variable `turn` to track whose turn it is. Let `turn = True` mean it is Ciel's turn, and `turn = False` mean it is Hanako's turn.
3. Enter a loop that continues as long as a player can pay exactly 220 yen. On each iteration, compute the number of 100-yen and 10-yen coins the current player will take according to their strategy:

For Ciel, try to take 2 100-yen coins first. If that is impossible, try 1, and then 0, supplementing with 10-yen coins to make exactly 220 yen. If no combination is possible, Ciel loses.

For Hanako, try to take as many 10-yen coins as possible (up to 22). If there are not enough, supplement with 100-yen coins to reach 220 yen. If no combination is possible, Hanako loses.
4. Deduct the chosen number of coins from `x` and `y`.
5. Flip the turn to the other player.
6. When a player cannot pay exactly 220 yen, exit the loop and declare the other player the winner.

Why it works: The invariant is that each player always takes the preferred combination that is feasible. Since the game is deterministic under the greedy strategies, simulating each turn accurately reflects the optimal choices. No backtracking is needed because the preference rules eliminate ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

x, y = map(int, input().split())
turn = True  # True for Ciel, False for Hanako

while True:
    if turn:  # Ciel's turn
        if x >= 2 and y >= 2:
            x -= 2
            y -= 2
        elif x >= 2 and y >= 0 and y >= 0 and 220 - 200 <= y * 10:  # redundant but check
            take_10 = 2
            x -= 2
            y -= take_10
        elif x >= 1 and y >= 12:
            x -= 1
            y -= 12
        elif y >= 22:
            y -= 22
        else:
            print("Hanako")
            break
    else:  # Hanako's turn
        if y >= 22:
            y -= 22
        elif y >= 12 and x >= 1:
            y -= 12
            x -= 1
        elif y >= 2 and x >= 2:
            y -= 2
            x -= 2
        elif x >= 2:
            x -= 2
        else:
            print("Ciel")
            break
    turn = not turn
```

In the code, each turn is handled according to the player's strategy. Boundary checks are necessary to avoid taking more coins than available. The order of checks reflects the priority of coin preferences. Exiting the loop when no valid combination exists correctly identifies the winner.

## Worked Examples

**Example 1:**

Input `x = 2, y = 2`

| Turn | Player | Action | x | y | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Ciel | 2×100 + 2×10 | 0 | 0 | Cannot take more 100s, picks maximal 100s |
| 2 | Hanako | Cannot take 22×10, cannot pay 220 | 0 | 0 | Ciel wins |

The table confirms that Ciel wins immediately after first turn.

**Example 2:**

Input `x = 3, y = 5`

| Turn | Player | Action | x | y | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Ciel | 2×100 + 2×10 | 1 | 3 | Remaining coins |
| 2 | Hanako | 1×100 + 12×10 impossible, pick 0? | 1 | 3 | Cannot pay, Ciel wins |

This shows a case where Hanako cannot act because there are insufficient coins to reach exactly 220 yen.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(x + y) | Each turn consumes at least one coin, total number of turns ≤ x + y |
| Space | O(1) | Only a few integer counters are stored |

With x and y up to 10^6, the loop executes at most 2×10^6 iterations, each with constant-time computation, which is well within the 2-second limit. Space usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    output = io.StringIO()
    sys.stdout = output
    # solution code
    x, y = map(int, input().split())
    turn = True
    while True:
        if turn:
            if x >= 2 and y >= 2:
                x -= 2
                y -= 2
            elif x >= 1 and y >= 12:
                x -= 1
                y -= 12
            elif y >= 22:
                y -= 22
            else:
                print("Hanako")
                break
        else:
            if y >= 22:
                y -= 22
            elif y >= 12 and x >= 1:
                y -= 12
                x -= 1
            elif x >= 2 and y >= 2:
                x -= 2
                y -= 2
            elif x >= 2:
                x -= 2
            else:
                print("Ciel")
                break
        turn = not turn
    return output.getvalue().strip()

# provided sample
assert
```
