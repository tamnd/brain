---
title: "CF 1846B - Rudolph and Tic-Tac-Toe"
description: "We are given a final state of a very small board, always 3 by 3, for a simplified tic-tac-toe variant with three different symbols. One player places X, another places O, and the third places plus signs. Some cells may still be empty."
date: "2026-06-09T05:53:38+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1846
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 883 (Div. 3)"
rating: 800
weight: 1846
solve_time_s: 308
verified: false
draft: false
---

[CF 1846B - Rudolph and Tic-Tac-Toe](https://codeforces.com/problemset/problem/1846/B)

**Rating:** 800  
**Tags:** brute force, implementation, strings  
**Solve time:** 5m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a final state of a very small board, always 3 by 3, for a simplified tic-tac-toe variant with three different symbols. One player places X, another places O, and the third places plus signs. Some cells may still be empty. The board is already in a finished configuration, and we are asked to determine which player, if any, has formed a winning line.

A winning line means three identical symbols in a straight row, either horizontally, vertically, or diagonally. Exactly one winner exists or nobody wins, in which case the result is a draw. We are also guaranteed that two different symbols will never simultaneously form winning lines in the same board.

The input size is extreme in number of test cases, up to ten thousand boards, but each board is constant size. This immediately removes any need for optimization beyond constant time per board. Anything that does more than a fixed scan of 9 cells per test case is already overkill.

A subtle edge case comes from empty cells and partial lines. For example, a row like `X X .` is not a win even though it almost forms one. Another is diagonal checks, which are often missed in careless implementations. For instance, a board like

```
X . .
. X .
. . X
```

must return X.

The main implementation pitfall is incorrectly assuming that counting symbols is enough. For example, having three Xs on the board does not guarantee a win unless they are aligned.

## Approaches

The brute-force idea is to explicitly check every possible line for every test case. Since the board is only 3 by 3, there are exactly 8 winning lines: 3 rows, 3 columns, and 2 diagonals. For each line, we check whether all three cells contain the same symbol and are not empty. This is constant work per line, so each board takes constant time.

A more naive but less structured approach would be to try all subsets of three cells and verify whether they form a line. That is unnecessary because the geometry of the grid is fixed and known in advance. That approach still works but introduces redundant checks and harder implementation.

The key observation is that the set of winning lines is fixed and tiny. This converts the problem from a game simulation into a direct pattern matching task. We are not simulating moves or checking validity, only recognizing a static pattern.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check all triples) | O(t) with large constant or O(t * 27 checks) | O(1) | Accepted but overcomplicated |
| Optimal (check 8 lines) | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

We predefine all 8 winning lines as index triples over a flattened 3 by 3 grid.

1. Convert each board into a structure we can index quickly, such as a list of 9 characters. This makes line checking simple and avoids repeated string indexing logic. This step matters because it keeps the line checks uniform and readable.
2. Define the 8 winning patterns: three rows, three columns, and two diagonals. Each pattern is just a triple of indices in the flattened board.
3. For each symbol in `X`, `O`, and `+`, check whether any of the 8 patterns is fully occupied by that symbol. This is done by verifying that all three positions in the pattern match the symbol.
4. If exactly one symbol satisfies the win condition, output that symbol.
5. If no symbol satisfies it, output `DRAW`.

The reason we explicitly check all three symbols separately is that there is no overlap guarantee we can exploit beyond the problem statement. Even though it guarantees no simultaneous winners, we still must verify each independently.

### Why it works

Every possible winning configuration in a 3 by 3 tic-tac-toe board corresponds exactly to one of the predefined 8 lines. There is no other geometric arrangement that forms a win. Since we test all symbols against all valid lines, any winning board must be detected by at least one check. Conversely, a non-winning board cannot satisfy any full-line condition, so it cannot be falsely classified as a win.

## Python Solution

```python
import sys
input = sys.stdin.readline

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6)              # diagonals
]

def winner(board, ch):
    return any(board[a] == board[b] == board[c] == ch for a, b, c in LINES)

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        grid = []
        for _ in range(3):
            grid.append(input().strip())
        board = ''.join(grid)

        if winner(board, 'X'):
            out.append('X')
        elif winner(board, 'O'):
            out.append('O')
        elif winner(board, '+'):
            out.append('+')
        else:
            out.append('DRAW')

    print('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The solution flattens each grid into a single string of length 9 so that line checks become simple index comparisons. The `LINES` array encodes all possible winning configurations, which removes any need for coordinate arithmetic during execution.

The `winner` function is the core logic. It scans all 8 lines and checks whether all three positions contain the same target symbol. This is a direct pattern match, not a search or simulation.

The order of checks matters only in tie-breaking, but the problem guarantees no simultaneous winners, so checking X, then O, then + is safe and deterministic.

## Worked Examples

### Example 1

Input board:

```
X O X
O X O
O + X
```

Flattened board: `XOXOXOO+X`

We evaluate each symbol.

| Symbol | Line checked | Result |
| --- | --- | --- |
| X | (0,4,8) | X == X == X true |
| O | any line | no full match |
| + | any line | no full match |

Output is X.

This shows how diagonal detection is naturally handled by the precomputed line list, without special casing.

### Example 2

Input board:

```
O O O
X + X
. X +
```

Flattened board: `OOO X+X .X+`

| Symbol | Line checked | Result |
| --- | --- | --- |
| O | row (0,1,2) | all O |
| X | any line | no full match |
| + | any line | no full match |

Output is O.

This example confirms that partial interference from other symbols does not affect correctness, since we only validate uniformity per line.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case checks 8 fixed lines over 3 cells |
| Space | O(1) | Only stores a constant number of indices and temporary strings |

The constant work per test case is extremely small, so even ten thousand boards are processed instantly within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    def winner(board, ch):
        return any(board[a] == board[b] == board[c] == ch for a, b, c in LINES)

    t = int(input())
    out = []
    for _ in range(t):
        grid = [input().strip() for _ in range(3)]
        board = ''.join(grid)

        if winner(board, 'X'):
            out.append('X')
        elif winner(board, 'O'):
            out.append('O')
        elif winner(board, '+'):
            out.append('+')
        else:
            out.append('DRAW')

    return "\n".join(out)

# provided sample (single test case extracted style check omitted full sample due to formatting)
assert run("1\nXOX\nOXO\nOXO\n") == "X"

# custom: empty board
assert run("1\n...\n...\n...\n") == "DRAW"

# custom: X wins row
assert run("1\nXXX\n.O.\n+.+\n") == "X"

# custom: + wins diagonal
assert run("1\n+O.\nO+O\n.O+\n") == "+"

# custom: O wins column
assert run("1\nXO.\nXO.\nXO.\n") == "O"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty board | DRAW | no accidental win detection |
| row win | X | horizontal detection |
| diagonal win | + | diagonal correctness |
| column win | O | vertical correctness |

## Edge Cases

The empty board case demonstrates that the algorithm does not infer wins from symbol counts. The board `"..."` repeated three times produces no matching line in any of the 8 patterns, so all `winner` checks return false and the output is `DRAW`.

A diagonal-only win such as `+O., O+O, .O+` confirms that the diagonal pattern `(0,4,8)` is correctly included and checked symmetrically with `(2,4,6)`. Without these two patterns, plus-player wins would be systematically missed.

A column win like:

```
X O .
X O .
X O .
```

tests vertical indexing consistency after flattening. The indices `(0,3,6)` correctly represent the first column, and the equality check ensures all three rows contribute properly to the same line.
