---
title: "CF 959A - Mahmoud and Ehab and the even-odd game"
description: "The game starts with a single integer value, and two players alternately reduce it. On Mahmoud’s turn, he is only allowed to subtract an even positive number that does not exceed the current value."
date: "2026-06-17T01:53:56+07:00"
tags: ["codeforces", "competitive-programming", "games", "math"]
categories: ["algorithms"]
codeforces_contest: 959
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 473 (Div. 2)"
rating: 800
weight: 959
solve_time_s: 58
verified: true
draft: false
---

[CF 959A - Mahmoud and Ehab and the even-odd game](https://codeforces.com/problemset/problem/959/A)

**Rating:** 800  
**Tags:** games, math  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The game starts with a single integer value, and two players alternately reduce it. On Mahmoud’s turn, he is only allowed to subtract an even positive number that does not exceed the current value. On Ehab’s turn, he is only allowed to subtract an odd positive number within the same bound. If a player has no legal subtraction available on their turn, that player loses immediately.

The key aspect is that the game is fully determined by the parity structure of allowed moves, not by any strategic choice among many values. Each move reduces the number strictly, so the game must terminate after finitely many steps, and optimal play reduces to determining whether the starting position is winning or losing for the first player.

The input size constraint allows n up to 10^9. This immediately rules out any simulation that attempts to explore states of the game tree, since even a linear traversal over all states up to n would be too slow. Any valid solution must compress the game into a constant-time decision based on a property of n.

A subtle edge case occurs when n is very small. For example, when n = 1, Mahmoud cannot subtract any even number, so he loses immediately. When n = 2, Mahmoud can subtract 2, leaving 0 for Ehab, who then has no odd move available, so Mahmoud wins. These small cases reveal that parity of available moves matters more than the magnitude of n itself.

Another potential pitfall is assuming that both players can always move until n becomes 0. This is false because the allowed parity restricts available moves asymmetrically, so one player may be forced into a losing position earlier than expected.

## Approaches

A direct approach is to simulate the game. At each step, we try all valid moves for the current player, recursively evaluate resulting states, and determine if any move leads to a losing position for the opponent. This is a standard minimax game on a line of states from 0 to n.

This works conceptually because the game is finite and deterministic. However, from any state n, Mahmoud can try up to n/2 even moves and Ehab up to (n+1)/2 odd moves. Each move reduces the state but creates a new branch. In the worst case, the recursion explores a large fraction of states repeatedly, leading to exponential behavior if memoization is not used, and at least linear behavior even with memoization. Since n can be 10^9, even O(n) is impossible.

The key observation is that the structure of allowed moves collapses the game into a simple parity condition. Mahmoud can only move if there exists at least one even number ≤ n, which happens exactly when n ≥ 2. Ehab can always move whenever n ≥ 1, since 1 is always a valid odd subtraction. The interaction between these constraints shows that the only meaningful distinction is whether n is even or odd at the start. If n is even, Mahmoud can make a move that preserves structure in a way that forces Ehab into a position with no winning continuation. If n is odd, Mahmoud is immediately unable to make an even move that fully stabilizes advantage, and Ehab takes control.

This reduces the entire game to checking parity of n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) or worse | O(n) | Too slow |
| Parity Observation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer n, which represents the initial state of the game.
2. Check whether n is even or odd, since only parity determines whether Mahmoud has a winning first move.
3. If n is odd, conclude Mahmoud cannot make a move that leaves a favorable structure, so Ehab wins immediately.
4. If n is even, Mahmoud can subtract 2 initially, leaving an odd number for Ehab, after which Mahmoud can always respond to Ehab’s forced odd moves in a way that maintains control of the parity advantage, so Mahmoud wins.

### Why it works

The game reduces to tracking which player is forced to face a position where no legal move exists first. Mahmoud is constrained to even moves, which effectively means he loses control when the starting state is odd because he cannot immediately respond in a way that preserves a balanced reduction pattern. When n is even, Mahmoud can always make the first reduction to an odd state, after which Ehab is forced into a disadvantageous parity position. Since every move strictly reduces n and parity alternates under optimal play, the initial parity fully determines which player is eventually blocked.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n % 2 == 1:
    print("Ehab")
else:
    print("Mahmoud")
```

The solution reads a single integer and immediately checks its parity. No state tracking or simulation is needed because the game collapses to a binary classification. The modulo operation is constant time, and printing the result finalizes the decision.

The only subtle implementation detail is ensuring correct parity handling for n = 1 and n = 2. These are already covered by the same condition, since 1 is odd and 2 is even, matching the known outcomes.

## Worked Examples

### Example 1

Input: n = 1

| Turn | Player | n before | Move | n after |
| --- | --- | --- | --- | --- |
| 1 | Mahmoud | 1 | no valid even move | terminal |

Mahmoud has no legal move at the start, so the game ends immediately with Mahmoud losing. This confirms the rule that odd n leads to Ehab’s win.

### Example 2

Input: n = 2

| Turn | Player | n before | Move | n after |
| --- | --- | --- | --- | --- |
| 1 | Mahmoud | 2 | subtract 2 | 0 |
| 2 | Ehab | 0 | no valid odd move | terminal |

Mahmoud forces the game into a terminal state where Ehab cannot respond. This confirms that even n leads to Mahmoud’s win.

These two traces demonstrate that the entire game outcome is fixed immediately by the parity of the initial state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a parity check and output |
| Space | O(1) | No additional data structures used |

The input constraint allows up to 10^9, so any linear or recursive approach would be infeasible. The constant-time parity check fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    return "Ehab" if n % 2 == 1 else "Mahmoud"

# provided samples
assert run("1\n") == "Ehab", "sample 1"
assert run("2\n") == "Mahmoud", "sample 2"

# custom cases
assert run("3\n") == "Ehab", "small odd"
assert run("4\n") == "Mahmoud", "small even"
assert run("1000000000\n") == "Mahmoud", "large even"
assert run("999999999\n") == "Ehab", "large odd"
assert run("5\n") == "Ehab", "odd mid case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | Ehab | minimum losing case for Mahmoud |
| 2 | Mahmoud | smallest winning case |
| 1000000000 | Mahmoud | large boundary even input |
| 999999999 | Ehab | large boundary odd input |
| 5 | Ehab | typical odd case consistency |

## Edge Cases

For n = 1, the algorithm checks parity and outputs Ehab. This matches the fact that Mahmoud has no even move at all, so the game ends immediately on the first turn.

For n = 2, the algorithm outputs Mahmoud. Tracing the logic, n is even so Mahmoud is declared winner, consistent with the move sequence where he subtracts 2 and forces Ehab into n = 0 with no legal odd subtraction.

For very large n such as 10^9, the computation remains identical since only modulo 2 is evaluated, and no iteration depends on magnitude.
