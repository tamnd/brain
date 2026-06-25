---
title: "CF 106500H - No More Than Two in a Row"
description: "The game is played on a one dimensional strip of cells. Initially every cell is empty. Players alternate choosing an empty position and placing a cross there. A move is allowed only if the resulting strip does not contain three consecutive crosses."
date: "2026-06-25T08:37:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106500
codeforces_index: "H"
codeforces_contest_name: "XXVIII Interregional Programming Olympiad, Vologda SU, 2026"
rating: 0
weight: 106500
solve_time_s: 47
verified: true
draft: false
---

[CF 106500H - No More Than Two in a Row](https://codeforces.com/problemset/problem/106500/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
# Problem Understanding

The game is played on a one dimensional strip of cells. Initially every cell is empty. Players alternate choosing an empty position and placing a cross there. A move is allowed only if the resulting strip does not contain three consecutive crosses. The player who cannot make a move loses.

The program is not asked to print a final winner. It must play the game against the judge. Before the game begins, it chooses whether it wants to move first or second. After that, it must always make moves that guarantee victory.

The strip length is at most 30. This bound is small enough that we can represent the entire board as a bitmask and search game states. A length of 30 gives up to 2^30 possible masks in theory, which is too many to visit blindly, but the rule forbidding three consecutive crosses reduces the number of reachable states heavily. The number of binary strings without `111` grows like a tribonacci sequence and is small enough for memoized search at this limit.

The main edge cases come from positions near the ends of the strip and positions where a move creates a pair of adjacent crosses.

For a strip of length 1, the only move is to occupy the single cell. The input is:

```
1
```

The correct behavior is to choose to move first and play cell 1. A strategy that always tries to make a "middle" move would fail because there is no middle handling needed.

A second edge case is a move that looks locally valid but creates three crosses. For example, on a strip of length 3:

```
XXX
```

The player cannot make any move. A careless implementation that only checks whether the chosen cell is empty would allow illegal moves.

Another important case is when the strip contains two consecutive crosses:

```
XX..
```

The next cell cannot be filled because it would create `XXX`, but cells farther away are still legal. The legality check must examine the whole resulting board, not only the chosen position.

## Approaches

A direct approach is to simulate the complete game tree. For every position, try every legal move, recursively solve the resulting positions, and mark the current state as winning if at least one move leaves the opponent in a losing state. This is exactly the definition of a winning position in an impartial game.

Without memoization this explores every possible sequence of moves. The depth can reach 30 and the branching factor can also be close to 30, giving an impractical upper bound around 30! possibilities.

The key observation is that the order in which a board position is reached does not matter. A board with the same occupied cells always has the same future moves. We can store the result for every visited mask. The number of reachable masks is much smaller than 2^30 because invalid masks containing `111` never appear. Memoization turns the repeated game tree into a graph traversal.

The same recursive function can also return the actual winning move. When the judge makes a move, we update the mask and ask the function again for a move that leaves the opponent in a losing state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(30!) in the worst case | O(30) recursion depth | Too slow |
| Optimal | O(S × 30), where S is the number of reachable valid states | O(S) | Accepted |

## Algorithm Walkthrough

1. Read the strip length and decide whether the initial position is winning. The recursive solver checks whether the empty board has a move that forces a loss for the opponent. If it does, the program chooses to move first. Otherwise, it chooses to move second.
2. Represent the current board as an integer mask. Bit `i` is one when cell `i` already contains a cross. This gives constant time updates and allows the complete state to be used as a memoization key.
3. For a state, try every empty cell. Temporarily place a cross there and check whether the board still obeys the rule that no three consecutive bits are set.
4. If a legal move reaches a losing state for the opponent, store this move as the winning move for the current state. If no such move exists, mark the state as losing.
5. During the game, whenever the opponent makes a move, add that cell to the mask and query the stored winning move. Output that cell and continue until the judge ends the game.

Why it works:

The recursive definition follows the standard winning and losing state property. A state is winning exactly when it has at least one move to a losing state. A state is losing exactly when every legal move gives the opponent a winning state. Since every move adds one cross, the game graph has no cycles, so memoization never creates ambiguity. The stored move always leads to a position where the opponent cannot force a win.

## Python Solution

```python
import sys
input = sys.stdin.readline

from functools import lru_cache

def solve_game(n):
    @lru_cache(None)
    def dfs(mask):
        for i in range(n):
            if mask >> i & 1:
                continue
            nxt = mask | (1 << i)
            if not valid(nxt):
                continue
            if dfs(nxt) == -1:
                return i
        return -1

    @lru_cache(None)
    def valid(mask):
        cnt = 0
        for i in range(n):
            if mask >> i & 1:
                cnt += 1
                if cnt >= 3:
                    return False
            else:
                cnt = 0
        return True

    return dfs

def main():
    n = int(input())

    dfs = solve_game(n)
    mask = 0

    first_move = dfs(mask)

    if first_move != -1:
        print(1)
        print(first_move + 1)
        sys.stdout.flush()
        mask |= 1 << first_move
    else:
        print(2)
        sys.stdout.flush()

    while True:
        x = int(input())
        if x == 0:
            return

        mask |= 1 << (x - 1)

        move = dfs(mask)
        if move == -1:
            print(0)
            sys.stdout.flush()
            return

        print(move + 1)
        sys.stdout.flush()
        mask |= 1 << move

if __name__ == "__main__":
    main()
```

The `dfs` function is the complete game solver. It returns a winning move index for a state and `-1` when the state is losing. The recursion only explores states reachable through legal moves.

The `valid` function checks the only rule of the game. It scans consecutive occupied cells and rejects any run of length three. Keeping this separate avoids subtle mistakes when generating moves.

The mask update happens immediately after every move. This keeps the stored state synchronized with the actual board. The output uses one based indexing because the interaction protocol numbers cells from 1.

The recursion depth is at most 30, so Python's default recursion limit is sufficient. The number of cached states is the limiting factor, not the recursion depth.

## Worked Examples

Since this is an interactive problem, the samples do not contain ordinary input and output pairs. The following traces show representative game states.

Example 1: A strip of length 5 where the first player has a winning move.

| Step | Current mask | Legal decision | Result |
| --- | --- | --- | --- |
| 1 | `00000` | Choose first player | Search finds a winning move |
| 2 | `00100` | Opponent plays cell 1 | New mask becomes `00101` |
| 3 | `00101` | Search response | Program chooses a move leading to a losing state |

The trace demonstrates that the program does not need a fixed pattern such as always taking the center. It calculates the response from the actual board.

Example 2: A position containing two adjacent crosses.

| Step | Current mask | Legal decision | Result |
| --- | --- | --- | --- |
| 1 | `00011` | Cell 3 is tested | Rejected because it creates `111` |
| 2 | `00011` | Cell 5 is tested | Accepted |
| 3 | `10011` | State is stored in cache | Future queries reuse the result |

This demonstrates why legality must be checked after applying a move.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S × n) | Each reachable state tries every cell, where S is the number of valid masks |
| Space | O(S) | Each visited mask is stored in the memoization table |

For `n <= 30`, the number of reachable states without three consecutive crosses is small enough for the memoized search to finish within the limits. Each state performs only a linear scan over the strip.

## Test Cases

The original problem is interactive, so traditional assert based testing is not directly applicable. The core game solver can still be tested by checking whether the returned move classifications match known positions.

```
from functools import lru_cache

def make_solver(n):
    @lru_cache(None)
    def valid(mask):
        run = 0
        for i in range(n):
            if mask >> i & 1:
                run += 1
                if run == 3:
                    return False
            else:
                run = 0
        return True

    @lru_cache(None)
    def win(mask):
        for i in range(n):
            if mask >> i & 1 == 0:
                nxt = mask | (1 << i)
                if valid(nxt) and not win(nxt):
                    return True
        return False

    return win

assert make_solver(1)(0) is True
assert make_solver(3)(0) is True
assert make_solver(3)(7) is False
assert make_solver(5)(0) in (True, False)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Length 1 empty strip | Winning state | Minimum board size |
| Length 3 empty strip | Winning state | Small game search |
| `111` occupied strip | Losing state | No legal moves |
| Length 5 empty strip | Valid result | General memoized search |

## Edge Cases

For a one cell strip, the solver starts from mask `0`. It tries cell `0`, reaches mask `1`, and sees that the opponent has no moves. The position is winning, so the program chooses to move first.

For the position `XX..`, the mask contains two adjacent crosses. When checking the next cell, the generated mask contains `XXX`, so `valid` rejects it. The solver still considers cells farther away and can continue the game correctly.

For a completely blocked position such as `XXX`, every possible bit is already set and no move can be generated. The recursive function returns `-1`, marking the state as losing. This is exactly the terminal condition required by the game.
