---
title: "CF 104344H - Shrek II"
description: "We are given two piles of coins, one with $A$ coins and another with $B$ coins. Two players alternate turns, and in each turn a player must remove exactly one coin either from the first pile, or from the second pile, or from both piles simultaneously."
date: "2026-07-01T18:30:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104344
codeforces_index: "H"
codeforces_contest_name: "Maratona dos Bixes 2023 - UNICAMP"
rating: 0
weight: 104344
solve_time_s: 95
verified: true
draft: false
---

[CF 104344H - Shrek II](https://codeforces.com/problemset/problem/104344/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two piles of coins, one with $A$ coins and another with $B$ coins. Two players alternate turns, and in each turn a player must remove exactly one coin either from the first pile, or from the second pile, or from both piles simultaneously. A move that removes coins is mandatory, so no passing is allowed. The player who removes the last remaining coin from the system wins the game.

We are asked to analyze this game from the perspective of the first player, the Burro. For a given starting configuration $(A, B)$, we must decide whether the first player can force a win assuming both players play optimally. If a winning strategy exists, we must also output a valid first move that guarantees that outcome.

The constraints allow $A, B \le 10^9$, which immediately tells us that any state-space exploration over all positions is impossible. Even a linear scan over all states is out of the question, and any solution must reduce the game to a closed-form condition computable in constant time per test case.

A subtle edge case is the situation where both piles are already empty. In that case, the game is already over and the first player has no move, which should be treated consistently with the losing condition.

Another delicate case is when one pile is empty. The move set still allows taking from the non-empty pile or taking from both, but the behavior becomes asymmetric and can mislead naive parity reasoning if not carefully derived from full game structure rather than intuition about single heaps.

## Approaches

A brute-force approach would treat every position $(a, b)$ as a game state and recursively try all possible moves: removing from the first pile, removing from the second pile, or removing from both. A position is winning if at least one move leads to a losing position, and losing if all moves lead to winning positions.

This recursion correctly models the game, but the state space is $(A+1)(B+1)$, which in the worst case is on the order of $10^{18}$. Even with memoization, the number of reachable states remains too large for any direct dynamic programming.

The key observation is that the move set always reduces the total number of coins by exactly one or two, and the game behaves like a very structured subtraction game on a grid. Computing small values reveals a stable pattern in losing positions: whenever both piles are even, the position becomes losing, and all other configurations are winning.

This collapses the entire game into a parity condition rather than a graph traversal problem. Once the losing states are identified, the winning move can be constructed by forcing the opponent into a state where both piles are even.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (game tree DP) | $O(AB)$ | $O(AB)$ | Too slow |
| Parity characterization | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Step 1: Identify losing positions

A position is losing if both $A$ and $B$ are even. If the game starts in such a position, any move necessarily breaks this property and gives the opponent a winning configuration.

### Step 2: If current state is losing

If both $A$ and $B$ are even, output that no winning strategy exists for the first player.

### Step 3: Construct a winning move otherwise

We try to move into a losing position, i.e., into a state where both piles become even.

### Step 4: Choose move based on parity

If $A$ is even and $B$ is odd, reduce $B$ by 1.

If $A$ is odd and $B$ is even, reduce $A$ by 1.

If both are odd, remove one coin from each pile simultaneously.

Each of these moves flips parity exactly in the way needed to reach an even-even state.

### Why it works

The key invariant is that even-even positions are exactly the P-positions of the game. From any even-even state, every valid move changes at least one pile parity, producing a non-even-even state. From any non-even-even state, there is always a move that flips odd counts down to reach even-even in one step, because we can independently adjust parity using the three allowed move types. This guarantees that the game reduces to alternating forced transitions between winning and losing regions.

## Python Solution

```python
import sys
input = sys.stdin.readline

A, B = map(int, input().split())

# losing position for first player
if A % 2 == 0 and B % 2 == 0:
    print("N")
else:
    print("S")
    if A % 2 == 0 and B % 2 == 1:
        print("B")
    elif A % 2 == 1 and B % 2 == 0:
        print("A")
    else:
        print("A B")
```

The code directly encodes the parity characterization. The first condition checks whether the starting state is losing, in which case no move is printed. Otherwise, it selects a move that forces both piles into an even configuration.

The decision structure is exhaustive over parity cases, and each branch corresponds exactly to a move that reduces the state into the losing class for the opponent.

## Worked Examples

### Example 1: Input `1 1`

| Step | A | B | Action | Resulting state |
| --- | --- | --- | --- | --- |
| Start | 1 | 1 | Check parity | both odd |
| Move choice | 1 | 1 | remove both | (0, 0) |

This confirms that when both piles are odd, the optimal move is to remove from both piles, immediately forcing a terminal losing position for the opponent.

The trace shows how the game transitions directly into the base losing state.

### Example 2: Input `2 1`

| Step | A | B | Action | Resulting state |
| --- | --- | --- | --- | --- |
| Start | 2 | 1 | Check parity | mixed |
| Move choice | 2 | 1 | remove from B | (2, 0) |

After the move, both piles are even, meaning the opponent receives a losing position. This confirms that mixed parity states always allow a direct transition into the losing region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only parity checks and one decision |
| Space | $O(1)$ | No additional data structures used |

The solution fits easily within limits since each test case is resolved with a constant number of arithmetic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    A, B = map(int, input().split())
    if A % 2 == 0 and B % 2 == 0:
        return "N"
    if A % 2 == 0 and B % 2 == 1:
        return "S\nB"
    if A % 2 == 1 and B % 2 == 0:
        return "S\nA"
    return "S\nA B"

# provided samples
assert run("1 0") == "S\nA", "sample 1"
assert run("1 1") == "S\nA B", "sample 2"
assert run("2 1") == "S\nB", "sample 3"

# custom cases
assert run("0 0") == "N", "empty game"
assert run("2 2") == "N", "even-even losing state"
assert run("3 3") == "S\nA B", "odd symmetric win"
assert run("4 2") == "N", "even-even larger losing state"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | N | terminal losing state |
| 2 2 | N | even-even rule |
| 3 3 | S A B | odd symmetric winning move |
| 4 2 | N | non-obvious even-even losing case |

## Edge Cases

### Case: both piles empty `(0, 0)`

The algorithm classifies this as even-even, so it outputs `N`. This matches the fact that the player to move has no legal move and therefore loses immediately.

### Case: large even-even state `(10^9, 10^9)`

Both values are even, so the output is `N` in constant time. No exploration of state transitions is needed because parity alone determines the outcome.

### Case: mixed parity `(even, odd)`

The algorithm always reduces the odd pile by one, producing an even-even state. For example, `(6, 5)` becomes `(6, 4)`, forcing the opponent into a losing configuration.

### Case: both odd `(odd, odd)`

The move `(A-1, B-1)` is always valid and transforms the position into even-even. For example, `(7, 3)` becomes `(6, 2)`, again handing a losing state to the opponent.
