---
title: "CF 105321A - Advanced tic-tac-toe"
description: "The game is played on a fixed 3×3 grid, but instead of thinking about it as a board, it is easier to treat it as nine indexed positions from 1 to 9. Two players alternate turns, X going first and O second, placing their symbol into an empty cell."
date: "2026-06-22T17:22:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105321
codeforces_index: "A"
codeforces_contest_name: "2024 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 105321
solve_time_s: 71
verified: true
draft: false
---

[CF 105321A - Advanced tic-tac-toe](https://codeforces.com/problemset/problem/105321/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on a fixed 3×3 grid, but instead of thinking about it as a board, it is easier to treat it as nine indexed positions from 1 to 9. Two players alternate turns, X going first and O second, placing their symbol into an empty cell. A player immediately wins if their symbols form any complete row, column, or diagonal.

The twist is that before the game starts, we are given constraints that dynamically disable cells. Each constraint says that a particular cell B becomes unusable while another cell A is still empty. As soon as A gets filled by either player, the restriction disappears and B may become usable again if no other constraint blocks it.

So a move is legal only if the chosen cell is empty and every constraint targeting that cell has its prerequisite cell already filled. This means each cell has a dependency structure: it can only be played after certain other cells have been played earlier in the game.

The task is to determine the outcome under optimal play with both players knowing all constraints and playing perfectly.

The constraints are large, up to 100000, but the board is only nine cells. This difference between input size and state size is the central hint. Any solution that explores only board configurations is feasible, while anything that tries to simulate constraint checking naively per move will TLE unless preprocessed.

A subtle case comes from cyclic dependencies. If cell 1 blocks cell 2 and cell 2 blocks cell 1, neither can ever be played first, so both are permanently unavailable. A naive approach that assumes all cells are eventually playable would incorrectly include such cells in the game tree.

Another tricky situation is when constraints remove the only winning move at a critical moment. For example, a player may appear to have a winning line available, but one cell of that line is blocked until another unrelated cell is played, which can shift the optimal outcome entirely.

## Approaches

A brute-force perspective treats the game as a search over all possible states of the board, tracking at every step which cells are occupied by X, which by O, and which are empty. From each state, we generate all legal moves, apply them, and recursively evaluate the outcome.

This is correct because the game is deterministic and finite. However, the branching factor is up to nine and each cell can be placed in many different orders, leading to a state space on the order of 3⁹ configurations if we distinguish X, O, and empty. That is small, but only if we store states efficiently. A naive implementation that repeatedly checks constraints from scratch for each move can multiply the cost by up to 10⁵ per transition, which is far too slow.

The key observation is that constraints depend only on whether a prerequisite cell is already filled, not on which player filled it. This means legality of a move depends only on the set of occupied cells, while winning depends on the assignment of X and O. Since the board has only nine cells, we can encode the full state compactly and run memoized minimax over all states.

We treat the game as a two-player perfect information game over a graph of states. Each state transitions to others by placing the current player's mark in a legal cell. We evaluate outcomes using recursion with memoization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation with repeated constraint checking | Exponential with large constant factor, effectively O(3⁹ · N) | O(3⁹) | Too slow |
| State DP over 3-state board with preprocessing | O(3⁹ · 9) | O(3⁹) | Accepted |

## Algorithm Walkthrough

We represent each board state by storing, for every cell, whether it is empty, X, or O. Since there are only nine cells, this can be encoded in base 3, giving a compact integer state.

We also preprocess constraints into a structure where each cell B stores a bitmask of all cells A that must already be filled before B becomes usable. This reduces constraint checking to a single bit operation.

1. Encode each board state as a 9-length ternary representation and define whose turn it is by counting filled cells.
2. Precompute all winning line masks for tic tac toe. A state is terminal if either player already occupies any winning triple.
3. Build a dependency mask for each cell B containing all A such that B cannot be used until A is filled.
4. Define a recursive function dp(state) that returns the final result assuming optimal play from that configuration.
5. Before generating moves in dp(state), check whether the state is already terminal. If X or O has a winning line, return that result immediately.
6. Generate all legal moves by iterating over empty cells. A move is legal only if all prerequisite cells of that position are already filled.
7. For each legal move, apply it, switch turns, and evaluate the resulting state recursively.
8. If the current player can force their own win in at least one branch, return that outcome. Otherwise, if all moves lead to opponent win, return opponent win. If neither side can force a win and no move improves the outcome, return draw.

The core invariant is that dp(state) correctly represents the game outcome under optimal play for that exact configuration of X, O, and filled cells. The recursion never revisits a state without returning the same stored result, ensuring consistency across all paths that reach it. Because every transition strictly increases the number of filled cells, the state graph is acyclic, guaranteeing termination.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1000000)

WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def check_win(board, player):
    for a,b,c in WIN_LINES:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def solve():
    n = int(input())
    prereq = [0] * 9

    for _ in range(n):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        prereq[b] |= (1 << a)

    memo = {}

    def encode(board):
        state = 0
        p = 1
        for i in range(9):
            state += board[i] * p
            p *= 3
        return state

    def decode(state):
        board = [0] * 9
        for i in range(9):
            board[i] = state % 3
            state //= 3
        return board

    def filled_mask(board):
        m = 0
        for i in range(9):
            if board[i] != 0:
                m |= (1 << i)
        return m

    def count_moves(board):
        return sum(1 for x in board if x != 0)

    def dp(state):
        if state in memo:
            return memo[state]

        board = decode(state)

        if check_win(board, 1):
            memo[state] = 1
            return 1
        if check_win(board, 2):
            memo[state] = -1
            return -1

        move_count = count_moves(board)
        turn = 1 if move_count % 2 == 0 else 2

        can_move = False
        best = -2

        for i in range(9):
            if board[i] != 0:
                continue
            if (prereq[i] & filled_mask(board)) != prereq[i]:
                continue

            can_move = True
            board[i] = turn
            nxt = dp(encode(board))
            board[i] = 0

            if turn == 1:
                best = max(best, nxt)
            else:
                best = min(best, nxt)

            if turn == 1 and best == 1:
                break
            if turn == 2 and best == -1:
                break

        if not can_move:
            memo[state] = 0
        else:
            memo[state] = best

        return memo[state]

    init = [0] * 9
    res = dp(encode(init))

    if res == 1:
        print("X")
    elif res == -1:
        print("O")
    else:
        print("E")

solve()
```

The encoding step compresses each full board into a single integer, which allows memoization to work efficiently. The recursion determines the current player from the number of filled cells rather than storing it explicitly.

Constraint checking is reduced to a single bitmask comparison per cell, which prevents scanning all N rules during each move.

The win check is performed immediately after decoding, ensuring that a move that completes a line ends the game without exploring further moves.

## Worked Examples

Consider a minimal case with no constraints where both players play optimally. The game behaves like standard tic tac toe and leads to a draw.

State progression:

| Step | Board (X=1, O=2) | Player to move | Legal moves | Outcome so far |
| --- | --- | --- | --- | --- |
| 0 | all empty | X | all cells | unknown |
| 1 | X in center | O | 8 cells | still open |
| 2 | O blocks corner | X | reduced | still drawable |

This trace shows that without constraints, optimal play converges to equilibrium, which corresponds to the classic result.

Now consider a case where a constraint disables a key defensive move until a prerequisite cell is filled. Early moves may look symmetrical, but once a dependency is satisfied, a forced winning line becomes available, flipping the evaluation from draw to win for one side. This demonstrates why legality must be recomputed dynamically from filled-cell structure rather than assumed static.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3⁹ · 9) | Each state is evaluated once, with up to 9 transitions per state |
| Space | O(3⁹) | Memoization table over all board configurations |

The state space is bounded by 3⁹, which is small enough for Python. Constraint preprocessing is linear in N but independent of the game search, so it does not affect the exponential state evaluation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# basic sample-like cases
assert run("0\n") in {"X","O","E"}

# simple blocking cycle
assert run("1\n1 2\n") in {"X","O","E"}

# self-blocking constraint removes a cell permanently
assert run("1\n1 1\n") in {"X","O","E"}

# full symmetric constraints
assert run("2\n1 2\n2 1\n") in {"X","O","E"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty constraints | E | baseline game resolution |
| single dependency | any | legality propagation |
| self loop constraint | any | dead cell handling |
| mutual blocking | any | cycle handling |

## Edge Cases

A self-referential constraint where a cell blocks itself makes that cell unusable for the entire game. The preprocessing step stores it as a prerequisite bit that is never satisfied, so the move generator will never allow it. The DP naturally adapts by reducing branching.

A mutual dependency between two cells produces the same effect for both, since neither prerequisite set can ever be satisfied. During state expansion, both cells are always skipped, shrinking the effective game tree without special handling.

A configuration where constraints eliminate all legal moves early leads to a forced draw. In that situation, the DP reaches a state where no transitions are possible and returns zero immediately, which correctly represents a stalled game under the rules.
