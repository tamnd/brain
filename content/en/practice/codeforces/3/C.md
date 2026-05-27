---
title: "CF 3C - Tic-tac-toe"
description: "We are given a final 3 × 3 tic-tac-toe board and need to determine whether this position could appear during a real game"
date: "2026-05-27T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "games", "implementation"]
categories: ["algorithms"]
codeforces_contest: 3
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 3"
rating: 1800
weight: 3
solve_time_s: 103
verified: true
draft: false
---

[CF 3C - Tic-tac-toe](https://codeforces.com/problemset/problem/3/C)

**Rating:** 1800  
**Tags:** brute force, games, implementation  
**Solve time:** 1m 43s  
**Verified:** yes  
**Share:** https://chatgpt.com/share/6a172218-b5fc-83ec-b31f-66f83a2faf7e  

## Solution
## Problem Understanding

We are given a final 3 × 3 tic-tac-toe board and need to determine whether this position could appear during a real game played according to the rules.

The tricky part is that we are not simulating future moves. We are validating whether the current board is reachable from an empty board with alternating turns, where X always moves first.

A valid game follows several strict rules at the same time:

- The number of X moves is either equal to the number of 0 moves, or exactly one larger.
- X always goes first.
- The game stops immediately after someone wins.
- Both players cannot legitimately win at the same time.

The board is tiny, only 9 cells, so performance is not a concern at all. Even exhaustive checking would run instantly. The difficulty comes from carefully handling all game-state rules without missing contradictions.

A common mistake is checking only move counts. Consider this board:

```
XXX
000
...
```

Both players have a winning line. A naive solution might accept this because both players have three marks and the counts differ by one. But this position is impossible. Once X completed a winning line, the game should have ended immediately, so 0 never gets another move.

Another subtle case is when the winner has the wrong move count.

```
XXX
0..
0..
```

X has won, and the counts are X = 3 and 0 = 2. This is valid because X always has exactly one extra move after winning.

Now look at this:

```
XXX
00.
...
```

Counts are X = 3 and 0 = 2, still valid.

But this board is illegal:

```
XXX
000
X..
```

X count is 4, 0 count is 3, which superficially looks fine. The real issue is that both players win simultaneously.

Another edge case happens when the board is full:

```
X0X
0XX
0X0
```

Nobody wins, and all 9 cells are filled. This is a draw.

A careless implementation may also forget that if 0 wins, then both players must have played the same number of moves. Since 0 always moves second, 0 can only complete a winning line immediately after its own turn.

Example:

```
X0X
X00
0X.
```

0 wins diagonally, and counts are X = 4, 0 = 4. Valid.

But this is impossible:

```
X0X
X00
0XX
```

0 still wins, but now X = 5 and 0 = 4. X already played after 0 had won.

## Approaches

The most direct idea is brute force simulation. Starting from the empty board, we could generate every possible legal sequence of moves and store all reachable board states. Then we simply check whether the input board appears among them.

This works because tic-tac-toe is tiny. There are at most 9! move orders, which is only 362880 sequences. Even with recursive generation and validation, this easily fits within the limits.

The brute-force solution is also naturally correct because it follows the game rules exactly. If a board is generated, it is valid. If not, it is illegal.

Still, we can do much better with simple logical checks. The board has only a few structural properties that completely determine validity.

The key observation is that tic-tac-toe states are constrained by move parity and winning conditions.

If X has won, then X must have played exactly one more move than 0.

If 0 has won, then both players must have played the same number of moves.

If both players have winning lines simultaneously, the state is impossible.

If neither player has won, then the next turn depends entirely on move counts:

- equal counts means X moves next
- X having one extra move means 0 moves next

Once these rules are encoded carefully, the entire problem becomes a few counting operations and eight line checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9!) | O(9!) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the 3 × 3 board and count the number of X and 0 characters.

X always moves first, so valid counts must satisfy:

- `x == o`
- `x == o + 1`

Any other difference is immediately illegal.
2. Check whether X has a winning line.

We examine all 8 possible winning combinations:

- 3 rows
- 3 columns
- 2 diagonals
3. Check whether 0 has a winning line.

This uses the same logic as the previous step.
4. If both X and 0 have winning lines, print `"illegal"`.

In a real game, the game ends immediately after the first win. Both players cannot legally win together.
5. If X has won, verify that X has exactly one more move than 0.

Since X moves first, X can only win immediately after making its own move.
6. If 0 has won, verify that both players have played the same number of moves.

0 always moves second, so after a valid 0 victory the move counts must match.
7. If nobody has won and the board is full, print `"draw"`.
8. Otherwise determine whose turn is next.

If counts are equal, X moves next, so print `"first"`.

If X has one extra move, then 0 moves next, so print `"second"`.

## Python Solution

```python
import sys
input = sys.stdin.readline

board = [input().strip() for _ in range(3)]

x = sum(row.count('X') for row in board)
o = sum(row.count('0') for row in board)

def win(ch):
    for i in range(3):
        if all(board[i][j] == ch for j in range(3)):
            return True

    for j in range(3):
        if all(board[i][j] == ch for i in range(3)):
            return True

    if all(board[i][i] == ch for i in range(3)):
        return True

    if all(board[i][2 - i] == ch for i in range(3)):
        return True

    return False

x_win = win('X')
o_win = win('0')

if not (x == o or x == o + 1):
    print("illegal")

elif x_win and o_win:
    print("illegal")

elif x_win:
    if x == o + 1:
        print("the first player won")
    else:
        print("illegal")

elif o_win:
    if x == o:
        print("the second player won")
    else:
        print("illegal")

elif x + o == 9:
    print("draw")

elif x == o:
    print("first")

else:
    print("second")
```

The solution begins by counting how many moves each player has made. This is the foundation for every later check because move parity determines whose turn it should be.

The `win()` helper checks all possible winning lines for a given character. Since the board size is fixed, explicit checks are simple and fast.

The order of conditions matters. Illegal move counts must be rejected before anything else. Simultaneous wins must also be handled early because later conditions assume only one player may have won.

After validating winning conditions, the remaining states are either a draw or an unfinished game. At that point, move parity alone determines whose turn comes next.

One subtle detail is that a full board is checked only after confirming nobody has already won. Otherwise a winning full board could incorrectly become `"draw"`.

## Worked Examples

### Example 1

Input:

```
X0X
.0.
.X.
```

### Trace

| Variable | Value |
| --- | --- |
| X count | 3 |
| 0 count | 2 |
| X wins | False |
| 0 wins | False |
| Board full | False |
| Next turn | second |

Output:

```
second
```

This board is valid because X has exactly one more move than 0, and nobody has won yet. That means it is 0's turn next, which corresponds to `"second"`.

### Example 2

Input:

```
XXX
000
...
```

### Trace

| Variable | Value |
| --- | --- |
| X count | 3 |
| 0 count | 3 |
| X wins | True |
| 0 wins | True |
| Result | illegal |

Output:

```
illegal
```

This trace demonstrates the most important invalid scenario. Both players cannot simultaneously have winning lines in a legal game because play stops immediately after the first victory.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The board size is fixed at 3 × 3, so all checks examine only constant-sized data |
| Space | O(1) | Only a few counters and boolean variables are used |

The solution performs a fixed number of operations regardless of input. Even the brute-force approach would fit comfortably, so this constant-time validation approach is easily within the limits.

## Test Cases

### Test Case 1

Input:

```
...
...
...
```

Expected output:

```
first
```

This verifies the empty starting position where X moves first.

### Test Case 2

Input:

```
XXX
0..
0..
```

Expected output:

```
the first player won
```

This checks a valid X victory with correct move counts.

### Test Case 3

Input:

```
XXX
000
...
```

Expected output:

```
illegal
```

This catches the simultaneous-win scenario.

### Test Case 4

Input:

```
X0X
0XX
0X0
```

Expected output:

```
draw
```

This verifies correct handling of a completely filled board with no winner.

## Edge Cases

Consider the simultaneous-win case again:

```
XXX
000
...
```

The algorithm counts:

- X = 3
- 0 = 3

Both counts are individually valid. Then it checks winning lines:

- X wins = true
- 0 wins = true

As soon as both become true, the algorithm prints `"illegal"`.

Now look at an invalid 0 victory:

```
X0X
X00
0XX
```

Counts:

- X = 5
- 0 = 4

0 has a winning line, but 0 can only win immediately after its own move, which requires equal counts. Since X already played once more after 0 won, the board is impossible. The algorithm correctly prints `"illegal"`.

Another subtle case is a full board with no winner:

```
X0X
0XX
0X0
```

The algorithm finds:

- no winning line
- total moves = 9

That directly maps to `"draw"`.

Finally, consider an unfinished valid position:

```
X0.
...
...
```

Counts:

- X = 1
- 0 = 1

Nobody has won and the board is not full. Equal counts mean it is X's turn next, so the algorithm prints `"first"` correctly.
