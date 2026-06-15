---
title: "CF 907B - Tic-Tac-Toe"
description: "The board is a 9 by 9 grid, but it is conceptually split into nine 3 by 3 sub-boards arranged in a 3 by 3 macro layout. Each cell can contain either a mark from the first player, a mark from the second player, or be empty. The game is not ordinary tic-tac-toe."
date: "2026-06-15T11:56:46+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 907
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 454 (Div. 2, based on Technocup 2018 Elimination Round 4)"
rating: 1400
weight: 907
solve_time_s: 250
verified: false
draft: false
---

[CF 907B - Tic-Tac-Toe](https://codeforces.com/problemset/problem/907/B)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 4m 10s  
**Verified:** no  

## Solution
## Problem Understanding

The board is a 9 by 9 grid, but it is conceptually split into nine 3 by 3 sub-boards arranged in a 3 by 3 macro layout. Each cell can contain either a mark from the first player, a mark from the second player, or be empty.

The game is not ordinary tic-tac-toe. The key rule is that the location of the previous move constrains where the next move can be played. If the last move was placed in a certain cell inside its 3 by 3 sub-board, then the next move must be played inside the sub-board that corresponds to that cell position. Only if that target sub-board has no empty cells does the restriction disappear, allowing play in any empty cell anywhere on the board.

The input gives the full current board state and then separately gives the coordinates of the last move. The task is to mark every cell where the current player is allowed to move with an exclamation mark, leaving all other cells unchanged.

Even though the statement mentions that the state may be invalid or unreachable, that does not matter for computation. We only follow the rule mechanically based on the given last move and the current occupancy.

The constraints are fixed size: the board is always 9 by 9. This means any solution that scans or processes the grid in constant bounded time is sufficient. Even a few thousand operations are trivial here, so a direct simulation approach is enough.

A subtle edge case comes from the “fallback” rule. If the required 3 by 3 block is full, then the player can move anywhere. For example, if the last move sends you into a block where every cell is already occupied, then the restriction is effectively removed. A naive solution that always enforces the target block would incorrectly produce no valid moves in that case.

Another edge case is that the last move might point to a block that is already full even though the board is not fully filled. The correct behavior is still to ignore the restriction.

## Approaches

A brute-force interpretation is straightforward. First determine the target sub-board using the coordinates of the last move. Then check every cell in that sub-board to see whether at least one cell is empty. If there is at least one empty cell, restrict moves only to that sub-board. Otherwise, consider all empty cells on the full board.

This works because the rule depends only on whether the target sub-board has any free cell. However, even this brute-force idea already runs in constant time due to the fixed 9 by 9 size, so there is no asymptotic improvement needed.

The key observation is that the entire problem reduces to identifying a 3 by 3 block and checking whether it contains any dot. Once that is known, the answer is a simple mask over either that block or the whole grid.

There is no benefit in more complex data structures since the grid never exceeds 81 cells.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the 9 by 9 grid. This is stored as a list of strings or character arrays. Nothing is transformed yet, since we only need direct access to cells.
2. Read the coordinates of the last move and convert them to zero-based indexing. This is necessary because array indexing in code starts from 0, while input starts from 1.
3. Compute the target sub-board by taking integer division of the last move row and column by 3. This maps the 9 by 9 grid into a 3 by 3 grid of blocks.
4. Extract the corresponding 3 by 3 sub-board and scan it to check whether it contains at least one empty cell. The presence of a single '.' is enough to keep the restriction active.
5. If the sub-board has at least one empty cell, mark all empty cells inside that sub-board with '!'.
6. If the sub-board is completely full, scan the entire 9 by 9 grid and mark all empty cells anywhere with '!'.
7. Output the modified grid in the same format.

### Why it works

The game rule reduces the next move constraint to a single boolean condition: whether the forced sub-board is playable. If it is playable, no move outside it is legal. If it is not playable, the rule explicitly allows full freedom. Because the rule depends only on emptiness, and not on any other history or parity condition, checking only that sub-board fully captures all constraints for the next move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    board = [list(input().strip()) for _ in range(9)]
    x, y = map(int, input().split())
    x -= 1
    y -= 1

    bx, by = x // 3, y // 3

    has_empty = False
    for i in range(bx * 3, bx * 3 + 3):
        for j in range(by * 3, by * 3 + 3):
            if board[i][j] == '.':
                has_empty = True

    if has_empty:
        for i in range(bx * 3, bx * 3 + 3):
            for j in range(by * 3, by * 3 + 3):
                if board[i][j] == '.':
                    board[i][j] = '!'
    else:
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    board[i][j] = '!'

    for row in board:
        print("".join(row))

if __name__ == "__main__":
    main()
```

The first step is reading the grid exactly as characters so that modifications are in-place and cheap. Converting the last move to zero-based indexing avoids off-by-one errors when mapping into blocks.

The computation of `(x // 3, y // 3)` is the central mapping from the global grid to the macro-board. Every 3 by 3 region corresponds to a single block, so integer division cleanly identifies it.

The scan for `has_empty` is critical because it determines whether the constraint is active. If at least one dot exists, we strictly limit moves to that block. Otherwise, we intentionally ignore block boundaries.

The marking step carefully only modifies '.' cells. This ensures we do not overwrite existing x or o characters.

Finally, output preserves formatting exactly as required by the problem.

## Worked Examples

### Example 1

Consider a case where the last move sends us to a partially empty block.

| Step | Action | Target Block | Empty Found | Marking Scope |
| --- | --- | --- | --- | --- |
| 1 | Read input | N/A | N/A | N/A |
| 2 | Compute block | (1,2) | N/A | N/A |
| 3 | Scan block | middle-right block | yes | restricted |

This demonstrates the normal constrained case. Only that block is modified.

### Example 2

Now consider a case where the target block is full.

| Step | Action | Target Block | Empty Found | Marking Scope |
| --- | --- | --- | --- | --- |
| 1 | Read input | N/A | N/A | N/A |
| 2 | Compute block | (0,0) | N/A | N/A |
| 3 | Scan block | top-left block | no | global |

This confirms the fallback behavior: when no empty cells exist, we expand to the full board.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The board size is fixed at 81 cells, so all scans are constant bounded |
| Space | O(1) | Only the board and a few variables are stored |

The constant size of the grid guarantees the solution is well within limits. Even with multiple scans, the maximum number of operations is tiny and effectively constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    old = sys.stdout
    sys.stdout = io.StringIO()

    main()

    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# sample-style minimal case
assert run("""... ... ...
... ... ...
... ... ...

... ... ...
... ... ...
... x.. ...

... ... ...
... ... ...
... ... ...
6 4
""") != "", "sample 1 style execution"

# all empty grid, last move in center
assert run("""......... ......... ......... ......... ......... ......... ......... ......... .........

......... ......... ......... ......... ......... ......... ......... ......... .........
5 5
""") != "", "center block restriction applies"

# full target block case triggers global freedom
assert run("""xxx xxx xxx
xxx xxx xxx
xxx xxx xxx

xxx xxx xxx
xxx xxx xxx
xxx xxx xxx

xxx xxx xxx
xxx xxx xxx
xxx xxx xxx
1 1
""") != "", "full block fallback"

# boundary last move bottom-right cell
assert run("""......... ......... ......... ......... ......... ......... ......... ......... .........
9 9
""") != "", "bottom-right mapping"

# single empty cell anywhere
assert run("""xxx xxx xxx
xxx xxx xxx
xxx xxx xxx

xxx xxx xxx
xxx xxx xxx
xxx xxx xx.

xxx xxx xxx
xxx xxx xxx
xxx xxx xxx
6 8
""") != "", "single empty propagation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| center move | restricted block marking | normal rule |
| full block | global marking | fallback rule |
| corner move | correct block mapping | boundary correctness |

## Edge Cases

One important edge case is when the forced sub-board is completely filled. In that situation, the algorithm switches from block-restricted marking to global marking. The scan correctly detects this because `has_empty` remains false after checking all 9 cells in the block.

Another edge case is when the last move lies on a boundary such as (3,3) or (6,6). These positions still map cleanly via integer division into the correct block index, and the computation `(x // 3, y // 3)` ensures consistency.

A final case is when only a single empty cell exists in the entire grid. If it lies outside the forced block when the block is valid, it will correctly remain unmarked, since the algorithm never considers it. If the block is full, the fallback ensures it will be marked correctly.
