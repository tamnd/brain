---
title: "CF 3C - Tic-tac-toe"
description: "We are given a snapshot of a tic-tac-toe board, represented as a 3×3 grid. Each cell is either empty (.), contains a cross (X), or contains a nought (0). The first player always places crosses, and the second player places noughts."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "games", "implementation"]
categories: ["algorithms"]
codeforces_contest: 3
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 3"
rating: 1800
weight: 3
solve_time_s: 277
verified: true
draft: false
---
[CF 3C - Tic-tac-toe](https://codeforces.com/problemset/problem/3/C)

**Rating:** 1800  
**Tags:** brute force, games, implementation  
**Solve time:** 4m 37s  
**Verified:** yes  

## Problem Understanding

We are given a snapshot of a tic-tac-toe board, represented as a 3×3 grid. Each cell is either empty (`.`), contains a cross (`X`), or contains a nought (`0`). The first player always places crosses, and the second player places noughts. The board might be partially filled, completely filled, or even in an impossible state.

The task is to determine what state the game is in. We can output one of six possible results: the first player won, the second player won, it is the first player's turn next, it is the second player's turn next, the game is a draw, or the board is illegal. Illegal boards occur when the placement of Xs and 0s is inconsistent with the rules, for example if the second player has played more times than the first player, or both players have winning lines simultaneously.

The constraints are small: a fixed 3×3 board. This tells us that any solution that iterates over cells a constant number of times will run well under the 1-second time limit. There is no need for optimization based on n, because n is always 9 or fewer. Edge cases are tricky because a naive check of “who has more Xs” may fail to detect illegal states where both players seem to have winning lines, or when the counts do not match the turn order. For example:

```
XXX
000
...
```

Here both players appear to have winning lines. The correct output is `illegal`. A careless implementation that checks wins independently without validating turn counts would incorrectly return `first player won` or `second player won`. Another subtle case is:

```
X0X
0X0
X..
```

Here the first player has a winning line along the first column, but the counts of Xs and 0s must still be consistent with the first player moving first. The correct result is `the first player won`, not `illegal`.

## Approaches

A brute-force approach would consider generating every possible sequence of moves that could lead to the given board and check if it is legal. Each turn has at most 9 options initially, 8 in the next turn, etc. This is factorial complexity (9!) and unnecessary given the small fixed size of the board. It would be correct but overly cumbersome.

The insight for an optimal approach is that legality and game state can be determined entirely by two factors: the counts of Xs and 0s, and the existence of winning lines. A board is legal if the number of Xs is equal to the number of 0s or one more than the number of 0s. If there is a winning line, the winner must have played last, and counts must align: X wins only if Xs are one more than 0s; 0 wins only if Xs equal 0s. Boards where both X and 0 have winning lines are always illegal. Once legality is established, determining whose turn is next is trivial by comparing counts. A draw occurs if the board is full and no player has won.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9!) | O(1) | Too slow / unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of Xs and 0s on the board. Let these be `count_X` and `count_0`. The counts determine whose turn it is. If `count_0 > count_X` or `count_X - count_0 > 1`, the board is illegal. This ensures turn order is respected.
2. Check for winning lines. Define a winning line as three identical symbols in a row, column, or diagonal. Iterate over all rows, columns, and both diagonals, marking whether X has won and whether 0 has won.
3. If both X and 0 have winning lines simultaneously, the board is illegal. Tic-tac-toe cannot reach a state where both players have completed a winning line on the same board because the game ends immediately when a player wins.
4. If X has a winning line, check that `count_X == count_0 + 1`. If this is false, the board is illegal. If true, output `the first player won`.
5. If 0 has a winning line, check that `count_X == count_0`. If this is false, the board is illegal. If true, output `the second player won`.
6. If no one has won, check whether the board is full. If full, output `draw`. If not full, determine whose turn it is: if `count_X == count_0`, it is the first player’s turn; if `count_X == count_0 + 1`, it is the second player’s turn.

Why it works: This algorithm maintains the invariant that any decision is consistent with the rules of tic-tac-toe: turns alternate starting with X, the game ends immediately when someone wins, and the counts of symbols on the board are consistent with the winner. By checking counts and winning lines in this order, all illegal configurations are caught.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check_winner(board, symbol):
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)):
            return True
        if all(board[j][i] == symbol for j in range(3)):
            return True
    if all(board[i][i] == symbol for i in range(3)):
        return True
    if all(board[i][2-i] == symbol for i in range(3)):
        return True
    return False

board = [input().strip() for _ in range(3)]
count_X = sum(row.count('X') for row in board)
count_0 = sum(row.count('0') for row in board)

x_wins = check_winner(board, 'X')
o_wins = check_winner(board, '0')

if count_0 > count_X or count_X - count_0 > 1:
    print("illegal")
elif x_wins and o_wins:
    print("illegal")
elif x_wins:
    print("the first player won" if count_X == count_0 + 1 else "illegal")
elif o_wins:
    print("the second player won" if count_X == count_0 else "illegal")
elif count_X + count_0 == 9:
    print("draw")
else:
    print("first" if count_X == count_0 else "second")
```

The solution first counts Xs and 0s to validate turn order. The `check_winner` function evaluates all rows, columns, and diagonals to determine winners. Each decision after that directly implements the rules described in the algorithm walkthrough.

## Worked Examples

**Sample 1**

Input:

```
X0X
.0.
.X.
```

| Variable | Value |
| --- | --- |
| count_X | 3 |
| count_0 | 2 |
| x_wins | False |
| o_wins | False |
| Board full? | False |

No winner yet, counts are `count_X = count_0 + 1`, so it is the second player’s turn. Output is `second`.

**Sample 2**

Input:

```
XXX
0.0
..0
```

| Variable | Value |
| --- | --- |
| count_X | 3 |
| count_0 | 3 |
| x_wins | True |
| o_wins | False |

X has a winning line but `count_X` is not `count_0 + 1`. Output is `illegal`.

These traces show how counting and line checks enforce legality and determine turn or winner.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Fixed 3×3 grid, constant number of checks (3 rows + 3 cols + 2 diagonals). |
| Space | O(1) | Only counters and board storage, no extra structures. |

The solution comfortably fits within 1-second time and 64 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        # solution
        board = [input().strip() for _ in range(3)]
        count_X = sum(row.count('X') for row in board)
        count_0 = sum(row.count('0') for row in board)

        def check_winner(board, symbol):
            for i in range(3):
                if all(board[i][j] == symbol for j in range(3)):
                    return True
                if all(board[j][i] == symbol for j in range(3)):
                    return True
            if all(board[i][i] == symbol for i in range(3)):
                return True
            if all(board[i][2-i] == symbol for i in range(3)):
                return True
            return False

        x_wins = check_winner(board, 'X')
        o_wins = check_winner(board, '0')

        if count_0 > count_X or count_X - count_0 > 1:
            print("illegal")
        elif x_wins and o_wins:
            print("illegal")
        elif x_wins:
            print("the first player
```
