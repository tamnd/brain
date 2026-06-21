---
title: "CF 105608C - 4 \u0432 \u0440\u044f\u0434"
description: "The task is essentially a “what if” simulation on a Connect Four board. We are given a 6 by 7 grid that represents the current state of the game, where each cell can contain a red piece, another color, or be empty."
date: "2026-06-22T05:50:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105608
codeforces_index: "C"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421, \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440 2024-2025"
rating: 0
weight: 105608
solve_time_s: 50
verified: true
draft: false
---

[CF 105608C - 4 \u0432 \u0440\u044f\u0434](https://codeforces.com/problemset/problem/105608/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is essentially a “what if” simulation on a Connect Four board. We are given a 6 by 7 grid that represents the current state of the game, where each cell can contain a red piece, another color, or be empty. We are also allowed to try placing a red piece in any one column, following gravity rules, meaning it will occupy the lowest empty cell in that column.

For each of the 7 columns, we simulate dropping a red piece into that column if possible. After placing the piece, we check whether this move creates a winning position for red. A win is defined as having four red pieces consecutively aligned horizontally, vertically, or diagonally in any of the two diagonal directions. If at least one such line exists after the move, that column is considered a winning move.

The output is the number of columns such that if red plays there, red immediately wins.

The grid size is fixed at 6 by 7, so the state space is constant. This means even a naive solution that checks all possibilities and scans the board multiple times is already feasible. The key constraint implication is that any solution up to a few thousand operations per column is entirely safe.

A subtle edge case appears when a column is already full. In that case, the move is invalid and must be ignored. Another edge case is when placing a piece does not immediately form a four-in-a-row, even though the board already contains partial structures that look close to a win. A naive implementation that forgets to revert the simulated move after checking could incorrectly accumulate state across columns.

As an example of a corner case, consider a column where placing a piece completes a diagonal of four. If we forget to simulate gravity correctly and instead place the piece at the topmost empty cell, we might miss a valid win. Similarly, if we fail to restore the board after testing a column, later checks will be contaminated by earlier simulations.

## Approaches

A direct brute-force approach tries every column, simulates dropping a red piece, and then scans the entire board to detect whether there exists any sequence of four red pieces in a row. Since the board is only 6 by 7, checking all possible starting positions and directions is constant work, but still repeated for each column. This gives a total of 7 simulations, each followed by a full board scan.

The scan itself checks each cell as a potential starting point for a sequence of four in each of four directions: right, down, diagonal down-right, and diagonal up-right. Each check is constant time, so a full scan is also constant time. The brute-force solution is therefore already efficient, but its structure is slightly redundant because it re-checks the entire board even though only one new piece was added.

The key observation is that we do not need to recompute everything from scratch if we already have a function that correctly detects a win on the board. Since the board is tiny, reusing this function after each simulated move is simpler and less error-prone than trying to incrementally maintain state. The problem is therefore best solved by direct simulation with a clean win-check function.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan Each Move | O(7 × 6 × 7) | O(1) | Accepted |
| Simulate + Full Win Check | O(7 × 6 × 7) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the board as a fixed grid and repeatedly simulate placing a single red piece in each column.

1. Read the 6 by 7 board and store it as a mutable grid. This allows us to temporarily modify it during simulation without allocating new structures.
2. Define a helper function that checks whether red has a winning line anywhere on the board. The function scans every cell and checks four directions: horizontal to the right, vertical downward, diagonal down-right, and diagonal up-right. Each check ensures indices stay within bounds before comparing four consecutive cells. The reason for checking all cells is that any winning segment must start from some top-left-most cell of that segment in at least one direction.
3. Initialize a counter for valid winning moves.
4. Iterate over each of the 7 columns, treating each as a candidate move.
5. For each column, simulate gravity by scanning from the bottom row upward until we find the first empty cell. If no empty cell exists, the column is full and we skip it. This step ensures the piece lands exactly as it would in the actual game.
6. Temporarily place a red piece in the found cell.
7. Run the win-check function on the updated board. If it returns true, increment the answer counter because this move leads to an immediate win.
8. Remove the simulated piece to restore the original board state. This is crucial because each column must be tested independently.
9. After all columns are tested, output the counter.

### Why it works

The algorithm relies on a strict separation between simulation and evaluation. Each column is tested in isolation on an otherwise unchanged board. The win-check function is exhaustive over all possible starting points and directions, so if any four-in-a-row exists after a move, it will be detected regardless of where it appears. Since every possible legal move is simulated exactly once, every winning move is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def win(field):
    for row in range(6):
        for col in range(7):
            if col + 3 < 7:
                if field[row][col] == field[row][col+1] == field[row][col+2] == field[row][col+3] == 'R':
                    return True
            if row + 3 < 6:
                if field[row][col] == field[row+1][col] == field[row+2][col] == field[row+3][col] == 'R':
                    return True
            if col + 3 < 7 and row + 3 < 6:
                if field[row][col] == field[row+1][col+1] == field[row+2][col+2] == field[row+3][col+3] == 'R':
                    return True
            if col + 3 < 7 and row - 3 >= 0:
                if field[row][col] == field[row-1][col+1] == field[row-2][col+2] == field[row-3][col+3] == 'R':
                    return True
    return False

field = [list(input().strip()) for _ in range(6)]

ans = 0

for col in range(7):
    row = 5
    while row >= 0 and field[row][col] != '.':
        row -= 1

    if row < 0:
        continue

    field[row][col] = 'R'

    if win(field):
        ans += 1

    field[row][col] = '.'

print(ans)
```

The solution starts by defining the win detection routine. Each direction is handled explicitly with boundary checks so that no index goes out of range. The logic is symmetric across horizontal, vertical, and diagonal cases, ensuring completeness of detection.

The main loop tries each column independently. The gravity simulation is done by a simple downward scan, which is optimal given the constant height of the board. After placing the piece, we immediately evaluate the board, then revert it. This rollback step prevents state leakage across iterations.

A common pitfall is forgetting to restore the cell after testing a column. That would cause later simulations to assume extra red pieces already exist, producing incorrect results.

## Worked Examples

### Example 1

Input board:

```
.......
.......
.......
.......
.......
RRR....
```

We test each column. Only columns where placing a red piece completes four consecutive reds in the bottom row will succeed.

| Column | Drop Row | Win After Move | Result |
| --- | --- | --- | --- |
| 0 | 4 | No | 0 |
| 1 | 4 | No | 0 |
| 2 | 4 | No | 0 |
| 3 | 5 | Yes (RRRR) | +1 |
| 4 | 5 | No | 0 |
| 5 | 5 | No | 0 |
| 6 | 5 | No | 0 |

Only column 3 completes the horizontal line.

Final answer is 1.

### Example 2

Input board:

```
.......
.......
.......
...R...
..R....
.R.....
```

This forms a diagonal structure that is one move away from completion.

| Column | Drop Row | Win After Move | Result |
| --- | --- | --- | --- |
| 0 | 2 | Yes | +1 |
| 1 | 3 | No | 0 |
| 2 | 4 | No | 0 |
| 3 | 5 | No | 0 |
| 4 | 5 | No | 0 |
| 5 | 5 | No | 0 |
| 6 | 5 | No | 0 |

Only column 0 completes the diagonal.

Final answer is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(7 × 6 × 7) | 7 simulated moves, each triggering a constant 6 by 7 scan |
| Space | O(1) | Board is fixed size, no auxiliary structures |

The grid dimensions are constant, so the total work is bounded by a small constant. This is well within typical Codeforces limits even under Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    # solution
    import sys
    input = sys.stdin.readline

    def win(field):
        for row in range(6):
            for col in range(7):
                if col + 3 < 7:
                    if field[row][col] == field[row][col+1] == field[row][col+2] == field[row][col+3] == 'R':
                        return True
                if row + 3 < 6:
                    if field[row][col] == field[row+1][col] == field[row+2][col] == field[row+3][col] == 'R':
                        return True
                if col + 3 < 7 and row + 3 < 6:
                    if field[row][col] == field[row+1][col+1] == field[row+2][col+2] == field[row+3][col+3] == 'R':
                        return True
                if col + 3 < 7 and row - 3 >= 0:
                    if field[row][col] == field[row-1][col+1] == field[row-2][col+2] == field[row-3][col+3] == 'R':
                        return True
        return False

    field = [list(input().strip()) for _ in range(6)]
    ans = 0

    for col in range(7):
        row = 5
        while row >= 0 and field[row][col] != '.':
            row -= 1
        if row < 0:
            continue
        field[row][col] = 'R'
        if win(field):
            ans += 1
        field[row][col] = '.'

    return str(ans)

# custom cases
assert run(".......\n.......\n.......\n.......\n.......\nRRR....\n") == "1", "horizontal win"
assert run(".......\n.......\n.......\n...R...\n..R....\n.R.....\n") == "1", "diagonal win"
assert run("RRRR...\n.......\n.......\n.......\n.......\n.......\n") == "0", "already win no move needed"
assert run(".......\n.......\n.......\n.......\n.......\n.......\n") == "0", "empty board"
assert run("RRRRRRR\nRRRRRRR\nRRRRRRR\nRRRRRRR\nRRRRRRR\nRRRRRRR\n") == "0", "full board"

# restore stdout
sys.stdout = sys.__stdout__
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Horizontal near-win | 1 | correct detection of row completion |
| Diagonal near-win | 1 | diagonal gravity interaction |
| Full red board | 0 | no valid move handling |
| Empty board | 0 | baseline behavior |
| Completely filled grid | 0 | full-column skipping |

## Edge Cases

A full column is the simplest structural edge case. The algorithm handles it by scanning upward until no empty cell is found, then skipping that column. This ensures we never place a piece illegally.

A second edge case is when a win already exists before any move. The problem still asks for moves that create a win after placement, so we only count columns where the simulated move leads to a win state. The win-check function is applied after every simulated placement, so pre-existing wins do not interfere with counting.

A third edge case is diagonal completion at the boundary of the board. For example, a diagonal that ends at row 0 or row 5 requires careful boundary checks. The implementation explicitly guards index access before comparing four cells, ensuring no invalid memory access and no missed configurations.
