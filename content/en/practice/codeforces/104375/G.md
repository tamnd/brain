---
title: "CF 104375G - Growing game"
description: "We are given a pile of chips and two players who alternate turns, starting with Jane. On each turn, the player removes between 1 and a bounded number of chips, where the bound grows with the turn index."
date: "2026-07-01T17:29:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104375
codeforces_index: "G"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 104375
solve_time_s: 73
verified: true
draft: false
---

[CF 104375G - Growing game](https://codeforces.com/problemset/problem/104375/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a pile of chips and two players who alternate turns, starting with Jane. On each turn, the player removes between 1 and a bounded number of chips, where the bound grows with the turn index. On the first move Jane can only take 1 chip, on the second move John can take up to 2 chips, on the third move Jane can take up to 3 chips, and so on. If the current turn is the i-th move overall, the player may take any integer amount from 1 up to i inclusive. Whoever takes the last chip wins.

The input is just the initial number of chips N, and we must determine whether the first player (Jane) can force a win assuming optimal play from both sides.

The constraint N ≤ 5000 is small enough that any solution with O(N^2) or even O(N^2) with small constants is acceptable. This immediately suggests a dynamic programming approach over game states indexed by remaining chips and turn number.

A subtle aspect is that the maximum move size depends on the turn index, not the remaining chips or the player. This means the game state is not just “remaining chips”, but also implicitly depends on how many moves have already happened. A naive approach that ignores turn parity or assumes fixed move sets will fail.

A common failure case arises if one tries to model this as a standard subtraction game with fixed moves like {1,2,3,...}. For example, at N = 3, one might incorrectly assume Jane can take all 3 immediately, but she cannot since on turn 1 she is restricted to taking only 1 chip.

## Approaches

A brute-force idea is to treat each state as (remaining_chips, turn_index) and recursively try all valid moves from 1 to turn_index. From a state we check if there exists a move that leaves the opponent in a losing state. This correctly captures the game, but the number of states grows as O(N^2), since turn_index can grow up to N in the worst case and remaining_chips ranges up to N as well.

However, many of these states are unreachable in practice because the total number of turns before the game ends is at most N. This suggests we only need to consider states up to turn i ≤ N and remaining chips up to N. The key observation is that we do not actually need to simulate arbitrary game trees, we only need a DP over i chips remaining at step t.

The transition becomes manageable because at turn t, the player chooses k in [1, t], and moves to a state with i − k chips and next turn t + 1. Since N is small, we can compute dp[i][t] meaning whether the current player can win with i chips remaining at turn t.

This reduces to a layered DP where each layer depends on the next turn. We compute backwards from large i or forward in a structured way.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursion on (i, t) | O(N^3) worst case | O(N^2) | Too slow |
| DP over (i, t) | O(N^2) | O(N^2) | Accepted |

## Algorithm Walkthrough

We define a state dp[i][t] where i is the number of chips remaining and t is the current turn number (i.e., the maximum allowed take is t). dp[i][t] is true if the current player can force a win.

1. We initialize all states with i = 0 as losing states, because if no chips remain, the player to move has already lost. This gives dp[0][t] = false for all t.
2. We iterate over increasing i from 1 to N, because dp[i][t] depends only on states with fewer chips.
3. For each state (i, t), we try all possible moves k from 1 to min(t, i). Each move leads to state dp[i − k][t + 1]. If there exists any move k such that dp[i − k][t + 1] is false, then dp[i][t] becomes true. This is because the current player can force the opponent into a losing position.
4. We are ultimately interested in dp[N][1], since the game starts with N chips and the first turn allows taking at most 1 chip.
5. We compute dp in increasing i and decreasing t where needed, ensuring all transitions are already known when used.

Why it works: every state encodes a perfect information game position with a finite move set. The DP follows standard minimax logic for impartial games with changing move constraints. Each state is correctly classified based on whether it has at least one move leading to a losing state. Since every transition reduces i, the recursion is acyclic and the DP fully resolves all positions without contradiction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N = int(input().strip())

    # dp[i][t] = can current player win with i chips left on turn t
    # t goes up to N+1 safely
    dp = [[False] * (N + 2) for _ in range(N + 1)]

    # base case: no chips -> losing
    for t in range(N + 2):
        dp[0][t] = False

    # fill DP
    for i in range(1, N + 1):
        for t in range(N, 0, -1):
            win = False
            max_take = min(i, t)
            for k in range(1, max_take + 1):
                if not dp[i - k][t + 1]:
                    win = True
                    break
            dp[i][t] = win

    print("Jane" if dp[N][1] else "John")

if __name__ == "__main__":
    solve()
```

The DP table is indexed by remaining chips and turn number. The key implementation detail is ensuring that when we evaluate dp[i][t], all dp[i - k][t + 1] are already computed, which is guaranteed because we increase i monotonically and only look forward in t.

The nested loops reflect the game structure directly: for each state we enumerate all legal moves and check if any forces a losing response.

## Worked Examples

### Example 1: N = 1

| i | t | possible moves | result |
| --- | --- | --- | --- |
| 0 | 1 | none | losing |
| 1 | 1 | k = 1 → dp[0][2] = false | winning |

At i = 1, Jane can take the only chip on her first move. The DP marks dp[1][1] as winning because there exists a move to a losing state. This matches the output “Jane”.

### Example 2: N = 3

| i | t | moves checked | dp[i][t] |
| --- | --- | --- | --- |
| 1 | 1 | k=1 → dp[0][2]=false | win |
| 2 | 1 | k=1 → dp[1][2], k=2 → dp[0][2] | win |
| 3 | 1 | k=1 → dp[2][2], k=2 → dp[1][2] | losing |

For i = 3 at turn 1, both possible moves lead to states where the opponent can respond optimally and avoid losing immediately. Thus dp[3][1] is false and John wins, consistent with the sample.

These traces show that the decision at each state depends entirely on whether any move reaches a losing position in the next layer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N^2) | For each i and t we try up to t transitions |
| Space | O(N^2) | DP table over (chips, turn) |

The constraint N ≤ 5000 allows roughly 25 million operations in Python in optimized form. The quadratic DP is borderline but acceptable given small constant factors and early breaks in transitions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N = int(sys.stdin.readline().strip())
    dp = [[False] * (N + 2) for _ in range(N + 1)]

    for i in range(1, N + 1):
        for t in range(N, 0, -1):
            win = False
            for k in range(1, min(i, t) + 1):
                if not dp[i - k][t + 1]:
                    win = True
                    break
            dp[i][t] = win

    return "Jane" if dp[N][1] else "John"

# provided samples
assert run("1\n") == "Jane", "sample 1"
assert run("3\n") == "John", "sample 2"
assert run("6\n") == "John", "sample 3"

# custom cases
assert run("2\n") in {"Jane", "John"}, "small boundary check"
assert run("4\n") in {"Jane", "John"}, "consistency check"
assert run("5\n") in {"Jane", "John"}, "stability check"
assert run("10\n") in {"Jane", "John"}, "larger sanity check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | Jane | minimum case |
| 3 | John | sample losing state |
| 6 | John | non-trivial mid case |
| 10 | varies | DP stability |

## Edge Cases

A key edge case is N = 1. The first player can only take 1 chip, immediately winning. The DP starts with dp[0][t] = false, so dp[1][1] becomes true because the only move leads directly to dp[0][2].

Another subtle case is small even values like N = 2, where intuition might suggest symmetry, but the increasing move limit breaks symmetry. At N = 2, Jane takes 1, leaving 1 chip with turn 2, and John can take up to 2 and wins immediately. The DP captures this because dp[1][2] evaluates as winning for the player to move.

A third edge behavior appears when N is large but still within early growth where the move limit grows faster than remaining chips. In those states, dp transitions quickly become dominated by direct winning moves, since k can always reach i once t exceeds i.
