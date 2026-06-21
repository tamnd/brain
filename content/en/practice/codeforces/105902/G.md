---
title: "CF 105902G - Still No Money?"
description: "We are given a two-player deterministic game played with a pile of skewers. At the start there are x skewers and a parameter k. Players alternate turns, with OC always moving first."
date: "2026-06-21T15:24:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105902
codeforces_index: "G"
codeforces_contest_name: "2025 Fujian Normal University Programming Contest"
rating: 0
weight: 105902
solve_time_s: 45
verified: true
draft: false
---

[CF 105902G - Still No Money?](https://codeforces.com/problemset/problem/105902/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a two-player deterministic game played with a pile of skewers. At the start there are `x` skewers and a parameter `k`. Players alternate turns, with OC always moving first. On a player’s turn, they choose a number of skewers to remove, anywhere from 1 up to the current value of `k`, provided enough skewers remain. After every move, the value of `k` decreases by exactly 1. Once `k` reaches 0, no further moves are possible, so whoever is to move at that point immediately loses.

The winner depends entirely on optimal play, meaning both players always choose moves that maximize their chance of winning.

The input gives multiple independent games. Each game is defined by the initial pile size `x` and initial move limit `k`. The output is simply the identity of the winning player.

The constraints push us toward an `O(1)` or `O(log x)` per test solution. With up to `10^5` test cases and values up to `10^18`, any simulation over moves or states is impossible. Even simulating a single game is infeasible because `k` itself can be as large as `10^18`.

A subtle edge case appears when `k` is large relative to `x`. For example, if `x = 4, k = 10`, OC can take all skewers immediately because the first move allows up to 10 removals, and the game ends instantly. A naive approach that assumes the game always lasts exactly `k` moves would be incorrect.

Another corner case is when `k = 1`. The first player can remove exactly one skewer, but immediately afterward `k` becomes 0, meaning the second player has no legal move regardless of remaining skewers. This creates immediate first-player wins independent of `x` as long as `x ≥ 1`.

Finally, when `x` is extremely large and `k` is small, the skewers never matter because the game ends purely due to the decreasing move limit before the pile is exhausted.

## Approaches

A brute-force simulation would explicitly play the game: on each turn try all possible removals from 1 to `k`, recursively evaluate outcomes, and reduce `k` each step. This correctly models optimal play because it explores the full game tree.

However, the branching factor is up to `k`, and the depth is also up to `k`, since `k` decreases every move until it reaches zero. Even ignoring `x`, the number of states grows like a factorial-like explosion in practice. With `k` up to `10^18`, this is completely infeasible.

The key insight is that the pile size `x` only matters until it becomes large enough that it never constrains play. After that, the game is governed entirely by the sequence of decreasing move limits. Each move reduces `k` by exactly 1, so the game has a deterministic maximum number of turns: it stops after at most `k` moves unless the pile runs out earlier.

Thus the real question becomes: how many total moves will actually happen? Each move reduces `k` by 1, so after `k` moves the value becomes 0 and the next player cannot move. Therefore, if the pile never runs out, the game always lasts exactly `k` moves, and the winner is determined by parity: OC wins if `k` is odd, KP wins if `k` is even.

The only complication is whether the pile ends earlier than `k` moves. But OC can always remove at least 1 skewer per turn, so after `t` moves, at least `t` skewers have been removed. Therefore, if `x < k`, the game ends after exactly `x` moves, because after `x` moves the pile is empty and the next player cannot move. If `x ≥ k`, the game ends after exactly `k` moves due to `k` reaching zero.

So the number of moves is simply `min(x, k)`, and the winner is determined by whether that number is odd or even.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential in k | O(k) | Too slow |
| Optimal Parity Reduction | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the game to counting how many moves will actually occur and then determine who makes the final move.

1. Compute `m = min(x, k)`. This represents the maximum number of moves that can actually happen before the game becomes impossible to continue.
2. Decide the winner based on the parity of `m`. OC makes the first move, so OC wins if `m` is odd, otherwise KP wins.

The reasoning behind the first step is that each move guarantees at least one skewer is removed and decreases `k` by exactly one, so neither resource can allow the game to exceed `min(x, k)` moves.

The second step comes from alternating turns. If the total number of moves is odd, the first player OC performs the last valid move and leaves the second player with no move. If it is even, KP performs the last move and OC is stuck next.

### Why it works

At every stage of the game, two independent “budgets” are shrinking: skewers and move allowance. Skewers decrease by at least one per move, and the move limit decreases by exactly one per move. Because both decrease monotonically and neither can be bypassed, the game is fully determined by which resource runs out first. Once we recognize that every move can always be made in a way that removes only one skewer, the worst-case duration is forced, and no strategic choice can extend or shorten the game beyond `min(x, k)`. After that reduction, the game becomes a simple alternating turn count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x, k = map(int, input().split())
        m = x if x < k else k
        if m % 2 == 1:
            print("OC")
        else:
            print("KP")

if __name__ == "__main__":
    solve()
```

The code directly computes the number of effective moves using a simple minimum operation. The comparison `x < k` avoids overhead of function calls and ensures constant time per test case. The parity check then determines the winner, relying on OC always starting first.

A common implementation mistake is to assume the game always lasts exactly `k` moves. That fails when `x < k`, because the pile empties earlier. Another mistake is trying to simulate moves greedily with variable removal amounts, which is unnecessary since optimal play does not affect total move count.

## Worked Examples

### Example 1

Input:

`x = 4, k = 4`

We track the effective move limit:

| Move | Remaining x | Remaining k | Notes |
| --- | --- | --- | --- |
| 0 | 4 | 4 | start |
| 1 | 3 | 3 | OC moves |
| 2 | 2 | 2 | KP moves |
| 3 | 1 | 1 | OC moves |
| 4 | 0 | 0 | KP moves ends game |

Here `m = min(4, 4) = 4`. The game lasts 4 moves, an even number, so KP wins. This confirms that when both resources run out together, parity alone determines the winner.

### Example 2

Input:

`x = 2, k = 1`

| Move | Remaining x | Remaining k | Notes |
| --- | --- | --- | --- |
| 0 | 2 | 1 | start |
| 1 | 1 | 0 | OC takes 1, k becomes 0 |

Here `m = min(2, 1) = 1`. Only one move is possible because after that `k = 0`. OC makes that move and wins immediately, demonstrating the case where move limit dominates pile size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses constant-time arithmetic operations |
| Space | O(1) | Only a few variables are stored regardless of input size |

The solution comfortably handles up to `10^5` test cases because each one is processed with a single min computation and parity check, both constant-time operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        x, k = map(int, input().split())
        m = x if x < k else k
        out.append("OC" if m % 2 == 1 else "KP")
    return "\n".join(out) + "\n"

# provided samples
assert run("4\n4 4\n2 1\n100000000 10\n1 1\n") == "KP\nOC\nKP\nOC\n"

# custom cases
assert run("1\n1 1\n") == "OC\n"
assert run("1\n10 1\n") == "OC\n"
assert run("1\n1 10\n") == "OC\n"
assert run("1\n100 100\n") == "KP\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | OC | smallest symmetric case |
| `10 1` | OC | k dominates, single move |
| `1 10` | OC | x dominates, early termination |
| `100 100` | KP | parity tie at large scale |

## Edge Cases

When `k = 1`, the game collapses immediately. OC moves once, reducing `k` to 0, and KP has no legal move regardless of how many skewers remain. The algorithm computes `m = min(x, 1) = 1`, which is odd, so OC wins correctly.

When `x < k`, such as `x = 2, k = 10`, the game ends due to exhaustion of skewers rather than move limit. OC removes 1 skewer, KP removes 1 skewer, and the pile becomes empty after 2 moves. The algorithm uses `m = 2`, giving KP the win since the second move is final.

When `x = k`, both constraints align perfectly, and the game always lasts exactly `k` moves. The solution reduces cleanly to parity of `k`, matching the alternating structure of turns.
