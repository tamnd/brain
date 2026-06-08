---
title: "CF 1972B - Coin Games"
description: "We are given a circular arrangement of coins. Each coin is either facing up or facing down. Two players alternate turns, and on each turn a player must pick one coin that is currently facing up, remove it, and then flip its two neighbors."
date: "2026-06-09T02:05:57+07:00"
tags: ["codeforces", "competitive-programming", "games"]
categories: ["algorithms"]
codeforces_contest: 1972
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 942 (Div. 2)"
rating: 900
weight: 1972
solve_time_s: 236
verified: false
draft: false
---

[CF 1972B - Coin Games](https://codeforces.com/problemset/problem/1972/B)

**Rating:** 900  
**Tags:** games  
**Solve time:** 3m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular arrangement of coins. Each coin is either facing up or facing down. Two players alternate turns, and on each turn a player must pick one coin that is currently facing up, remove it, and then flip its two neighbors. The circle shrinks as coins are removed, and the adjacency structure changes dynamically.

A player loses immediately if they are to move and there are no upward-facing coins available. The game always ends because each move reduces the number of coins.

The task is to decide, for each initial configuration, whether the first player can force a win assuming perfect play from both sides.

The constraints are small, with at most 100 coins per test case. This allows us to consider strategies that reason about structural properties of the game rather than needing heavy computation or search over large states. A full game-tree simulation is theoretically possible but quickly becomes infeasible because each move branches over all currently valid “up” positions, and the state space grows exponentially.

A subtle edge case arises when there are very few coins, especially $n \le 3$. In such cases, the flipping rule degenerates because removing a coin can flip the same coin twice or eliminate all adjacency effects. A naive simulation that assumes stable three-neighbor structure would produce incorrect transitions for these small cases.

## Approaches

A brute-force solution would simulate the entire game as a recursive minimax process over all reachable configurations. Each state is defined by the current circular binary string and the player to move. From each state, we try every possible up coin removal and recursively compute the result of the resulting configuration. This approach is correct because it directly encodes the game definition, but it is far too slow because the number of states grows exponentially with $n$, and even for $n = 100$, the number of reachable configurations is astronomically large.

The key observation is that the game is not sensitive to exact positions of up coins beyond a simple structural parity effect. Each move removes one up coin and flips two neighbors, which effectively toggles local parity and transfers “activity” around the circle. This type of operation is characteristic of impartial games where only the parity of the number of active elements matters, not their exact arrangement.

The decisive simplification is that the winner depends only on whether the number of up coins is odd or even, with a small correction for the case where no moves are possible initially. If there are no up coins at the start, the first player immediately loses. Otherwise, the first player can always force a win if and only if the count of up coins is odd.

This works because every move removes exactly one up coin and preserves the parity structure of the remaining active set after flips. The flips do not change the parity of the total number of up coins in a way that can be controlled by the opponent, so the game reduces to a parity game.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases and process each configuration independently. Each configuration is independent because there is no interaction between test cases.
2. Count how many coins are currently facing up. This is the only state variable that matters for determining the outcome.
3. If there are zero up coins, the first player cannot make a move and immediately loses. This is a forced losing position.
4. Otherwise, check the parity of the number of up coins. If it is odd, the first player wins; if it is even, the second player wins.
5. Output the result for each test case.

The reason this works is that every move removes exactly one up coin, and the flipping operation does not allow a player to change the parity of the “effective active set” in a way that breaks this invariant. The game reduces to alternating removal of effective active units, and the first player wins precisely when they start in a position where this alternating process ends in their favor.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input().strip())
    s = input().strip()

    ups = s.count('U')

    if ups == 0:
        print("NO")
    elif ups % 2 == 1:
        print("YES")
    else:
        print("NO")
```

The implementation directly follows the derived invariant. We only compute the number of up coins and apply a parity check. The string is read once per test case, and counting is linear in its length.

A common implementation pitfall is forgetting to strip newline characters when reading the string or accidentally reading multiple lines incorrectly. Another subtle issue is assuming the circle structure needs explicit modeling, but none of that is necessary once the invariant is identified.

## Worked Examples

We trace two configurations to illustrate how the parity rule applies.

### Example 1

Input:

```
5
UUDUD
```

We compute the number of up coins.

| Step | State | Ups count | Decision |
| --- | --- | --- | --- |
| 1 | UUDUD | 3 | start |
| 2 | count ups | 3 | compute |
| 3 | parity | odd | Alice wins |

Since the number of up coins is odd, the first player wins.

This shows that structural flipping does not matter for outcome classification.

### Example 2

Input:

```
5
UDDUD
```

| Step | State | Ups count | Decision |
| --- | --- | --- | --- |
| 1 | UDDUD | 2 | start |
| 2 | count ups | 2 | compute |
| 3 | parity | even | Bob wins |

Even though moves exist, the parity forces a losing position for the first player.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting characters per test case |
| Space | O(1) | Only storing the input string and a counter |

The constraints allow up to 100 test cases with strings of length up to 100. A linear scan per test case is easily fast enough within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        ups = s.count('U')
        if ups == 0:
            out.append("NO")
        elif ups % 2 == 1:
            out.append("YES")
        else:
            out.append("NO")

    return "\n".join(out)

# provided samples
assert run("""3
5
UUDUD
5
UDDUD
2
UU""") == """YES
NO
NO"""

# custom cases
assert run("""4
1
D
1
U
3
UUU
4
UUDD""") == """NO
YES
YES
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 D | NO | no moves possible |
| 1 U | YES | single winning move |
| UUU | YES | odd parity multi-case |
| UUDD | NO | even parity mixed case |

## Edge Cases

For a single coin, the behavior depends entirely on whether it is up or down. If it is down, the first player has no move and loses immediately. If it is up, they remove it and the game ends instantly in their favor. The parity rule matches both cases correctly.

For all coins up, every move removes one active coin while flipping neighbors, but the parity remains the deciding factor. If the count is odd, the first player always retains the final move advantage.

For alternating configurations like UUDD, there are valid moves, but the structure of flips does not change the parity outcome, so the second player wins under optimal play.
