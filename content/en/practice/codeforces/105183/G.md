---
title: "CF 105183G - \u041f\u0440\u043e\u0441\u0442\u044b\u0435 \u0448\u0430\u0445\u043c\u0430\u0442\u044b"
description: "We are given a sequence of moves played on a simplified chess board of size $8 times 8$. Initially, all white pieces occupy rows 1 and 2, and all black pieces occupy rows 7 and 8. Each side has 16 pieces, and pieces are indistinguishable except for color."
date: "2026-06-27T06:14:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105183
codeforces_index: "G"
codeforces_contest_name: "XX \u041d\u0438\u0436\u0435\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u0412. \u0414. \u041b\u0435\u043b\u044e\u0445\u0430"
rating: 0
weight: 105183
solve_time_s: 75
verified: false
draft: false
---

[CF 105183G - \u041f\u0440\u043e\u0441\u0442\u044b\u0435 \u0448\u0430\u0445\u043c\u0430\u0442\u044b](https://codeforces.com/problemset/problem/105183/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of moves played on a simplified chess board of size $8 \times 8$. Initially, all white pieces occupy rows 1 and 2, and all black pieces occupy rows 7 and 8. Each side has 16 pieces, and pieces are indistinguishable except for color. A move consists of selecting a specific piece by its current coordinates and moving it to a new coordinate. The move is allowed to capture an opponent piece by landing on it, in which case that opponent piece is removed. A move is invalid if any of its assumptions about the current state of the board is wrong.

The task is not to reconstruct a valid game, but to detect the earliest point in the recorded history where the log becomes impossible. We read moves in order and must output the smallest index $i$ such that the first $i$ moves cannot all be valid under the rules and initial configuration. If every move can be simulated consistently, the answer is $-1$.

The key difficulty is that the log refers to pieces by coordinates, not by identity. Since pieces move and get captured, a coordinate in the log may no longer contain the same color, or may be empty. This forces us to maintain the full board state precisely.

The constraints are small: at most 100 moves on a fixed $8 \times 8$ board. This immediately rules out anything beyond straightforward simulation. Even an $O(n)$ or $O(n \cdot 64)$ simulation is trivial. The only real concern is correctness of state updates and early termination at the first invalid step.

A subtle failure case appears when a move refers to a piece that was already captured earlier, or when a piece is assumed to still be at its original square but has already moved away. Another failure case is attempting to move onto a square occupied by the same color.

For example, suppose a white piece at (1,1) moves to (3,3). A later move claims to move a white piece from (1,1) again. That is impossible because the piece has already moved. A naive implementation that only checks initial existence would incorrectly accept this.

## Approaches

A brute-force interpretation would try to “rebuild” which exact piece is being referred to by searching among all pieces of that color and tracking identities explicitly. That is unnecessary because the log already gives the exact source coordinate of the piece being moved. The only requirement is that at that moment, a piece of the correct color actually exists at that square.

So the problem reduces to maintaining a dynamic grid. Each cell stores either empty, white, or black. We also maintain whose turn it is. For each move, we validate three conditions: the starting cell contains the correct color, the turn matches the player, and the destination does not contain a piece of the same color. If valid, we update the board by moving the piece and clearing the source cell, and possibly removing an opponent piece.

The brute-force cost is $O(n)$ with constant work per move. There is no need for more complex structures because the board size is fixed and tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Reconstruct identities / search pieces | $O(n \cdot 64)$ or worse | $O(64)$ | Accepted but unnecessary |
| Direct simulation on grid | $O(n)$ | $O(64)$ | Accepted |

## Algorithm Walkthrough

We simulate the game step by step while maintaining the board state.

### 1. Initialize the board

We create an $8 \times 8$ grid. Cells in rows 1 and 2 are marked white, rows 7 and 8 are marked black, and everything else is empty. We also set the current player to white, since white moves first.

This establishes the exact starting configuration from which every move must be valid.

### 2. Process each move in order

For each move $i$, we read $(x_1, y_1, x_2, y_2)$ and interpret them as 1-indexed coordinates.

We immediately check whether it is the correct player’s turn. If not, the log is inconsistent at this point.

### 3. Validate the source cell

We check whether the cell $(x_1, y_1)$ contains a piece of the current player’s color. If the cell is empty or contains the opponent’s piece, the move contradicts the history and we stop.

This condition catches cases where a piece has already moved away or been captured earlier.

### 4. Validate the destination cell

We check whether the destination contains a piece of the same color. If it does, the move is illegal because pieces cannot stack or capture their own side.

### 5. Apply the move

We clear the source cell and set the destination cell to the current player’s color. If the destination contained an opponent piece, it is simply overwritten, representing capture.

### 6. Switch turns

After a valid move, we switch the active player and continue.

### Why it works

At any moment, the grid exactly represents the true occupancy of the board after processing all previous valid moves. Each move is checked against this state, so any deviation from a possible physical configuration is detected immediately. Since every update is deterministic and based only on local cell changes, no hidden history can contradict the simulation. Therefore, the first invalid operation must be detected at the earliest prefix where the recorded move conflicts with the maintained state.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    board = [[0]*8 for _ in range(8)]
    
    # 1 = white, 2 = black
    for i in range(8):
        for j in range(8):
            if i < 2:
                board[i][j] = 1
            elif i >= 6:
                board[i][j] = 2
    
    turn = 1  # white starts
    
    for i in range(1, n+1):
        x1, y1, x2, y2 = map(int, input().split())
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1
        
        # check turn consistency
        if turn == 1:
            color = 1
        else:
            color = 2
        
        if board[x1][y1] != color:
            print(i)
            return
        
        # destination cannot contain same color
        if board[x2][y2] == color:
            print(i)
            return
        
        # move piece (capture if needed)
        board[x1][y1] = 0
        board[x2][y2] = color
        
        turn ^= 3  # switch 1 <-> 2
    
    print(-1)

if __name__ == "__main__":
    solve()
```

The implementation follows the grid simulation directly. The board is a simple integer matrix where 0 represents empty, 1 represents white, and 2 represents black. Each move is validated before any state mutation, which is important because once we modify the board we cannot recover the previous configuration for error reporting.

The turn handling uses a simple toggle between 1 and 2. All coordinates are converted to 0-based indexing immediately to avoid repeated adjustment errors. The validation order ensures that the earliest violation is reported exactly at the first inconsistent move.

## Worked Examples

### Example trace

Consider a short scenario:

Input:

```
3
1 1 3 3
7 7 6 6
1 1 4 4
```

| Move | Turn | (x1,y1) valid | (x2,y2) valid | Action | Board effect |
| --- | --- | --- | --- | --- | --- |
| 1 | White | Yes (white exists) | Empty | Move | (1,1)->(3,3) |
| 2 | Black | Yes | Empty | Move | (7,7)->(6,6) |
| 3 | White | No (1,1 empty) | - | Stop | Invalid |

After move 1, the white piece originally at (1,1) no longer exists there. Move 3 incorrectly assumes it still exists, so the prefix of length 3 is invalid.

This shows how the invariant that “coordinates uniquely identify current pieces” is maintained strictly through simulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each move performs constant-time checks and updates on a fixed 8×8 board |
| Space | $O(1)$ | The board size is constant and independent of input |

The constraints allow up to 100 moves, so even a direct Python simulation runs instantly. The fixed board size ensures memory usage and computation are both bounded.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# sample-like case: immediate valid moves
assert run("""2
1 1 3 3
7 7 5 5
""") == "-1"

# invalid due to moving empty square
assert run("""2
1 1 3 3
1 1 2 2
""") == "2"

# capture scenario
assert run("""2
1 1 7 7
7 7 8 8
""") == "-1"

# turn violation
assert run("""1
7 7 6 6
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| two valid moves | -1 | normal simulation |
| reuse empty source | 2 | stale coordinate detection |
| capture chain | -1 | overwriting opponent piece |
| wrong turn behavior | 1 | turn enforcement |

## Edge Cases

A common failure mode is assuming that a coordinate always refers to a valid piece if it was valid earlier. The simulation prevents this because each move updates the board immediately. For instance, once a piece moves from (1,1), any later reference to (1,1) will correctly fail.

Another subtle case is capture overwriting. When a piece moves to a square occupied by the opponent, the opponent is removed implicitly by assignment. This ensures no stale opponent pieces remain on the board, preventing phantom collisions in later moves.
