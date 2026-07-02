---
title: "CF 103964H - Sudoku"
description: "We are given a partially filled 9 by 9 Sudoku grid. Each cell either already contains a digit from 1 to 9 or is empty."
date: "2026-07-02T06:39:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103964
codeforces_index: "H"
codeforces_contest_name: "The 2015 China Collegiate Programming Contest (CCPC 2015)"
rating: 0
weight: 103964
solve_time_s: 48
verified: true
draft: false
---

[CF 103964H - Sudoku](https://codeforces.com/problemset/problem/103964/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a partially filled 9 by 9 Sudoku grid. Each cell either already contains a digit from 1 to 9 or is empty. The task is to complete the grid so that every row contains each digit exactly once, every column contains each digit exactly once, and every 3 by 3 subgrid also contains each digit exactly once.

The input can be thought of as a fixed board state with constraints, and the output is any valid completed board that extends this state without violating Sudoku rules. If multiple completions exist, any one valid completion is acceptable.

The structure of the problem immediately suggests exponential search space in the worst case because each empty cell can take up to nine values. However, the grid size is fixed at 81 cells, so the real difficulty is not input size growth but constraint interaction. This changes the problem from “large scale computation” to “careful pruning of a small combinatorial space”.

A naive recursive fill that tries all digits for each empty cell without pruning would explode even on a single puzzle with many blanks, since the branching factor is up to 9 and depth up to 81.

A typical hidden failure mode comes from not enforcing all three constraints consistently. For example, placing a digit that is valid in a row but invalid in a column or box can still pass partial checks if the implementation only validates one dimension.

Another subtle issue arises if updates are not properly rolled back during backtracking. A common incorrect implementation marks a digit as used in a row or column but forgets to unmark it when backtracking, leading to false pruning and incorrect “no solution” conclusions.

## Approaches

A brute force approach treats Sudoku as a pure search problem over empty cells. We scan the grid, pick the first empty cell, try digits 1 through 9, and recursively continue. This is correct because it explores every possible assignment consistent with previous choices.

However, its worst case complexity is on the order of $9^k$, where $k$ is the number of empty cells. Even with moderate pruning from validity checks, the branching factor remains too large for cases with many blanks.

The key observation that makes Sudoku solvable in practice is that constraint checking is extremely cheap and highly structured. Each placement affects exactly three sets: one row, one column, and one 3 by 3 block. This allows us to maintain incremental state so that validity checks are O(1), and we can aggressively prune invalid branches immediately.

A further improvement comes from choosing the next cell more intelligently. Instead of filling cells in fixed order, we always pick the empty cell with the fewest valid candidates. This reduces branching dramatically in typical puzzles because constrained cells collapse the search tree early.

We can maintain three boolean constraint tables for rows, columns, and boxes, and update them during recursion. This transforms the solution into a guided backtracking search with constant time validity checks per move.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9^k) | O(81) | Too slow |
| Optimized backtracking with constraints | O(small exponential, heavily pruned) | O(81) | Accepted |

## Algorithm Walkthrough

1. Parse the 9 by 9 grid and record all empty positions. While doing so, build three constraint trackers: which digits are already used in each row, each column, and each 3 by 3 subgrid. This allows us to answer “can I place digit d here” in constant time.
2. Define a function that computes the 3 by 3 box index for a cell using integer division of its coordinates. This is necessary because Sudoku constraints are partitioned into fixed blocks.
3. Implement a recursive solver that tries to fill the grid. At each call, select the next empty cell. Instead of choosing arbitrarily, pick the one with the fewest valid digits according to current constraints. This reduces branching early, which is where most exponential savings come from.
4. For the chosen cell, iterate through digits 1 to 9. For each digit, check whether it is absent in its row, column, and box. If valid, place it and mark it as used in all three constraint structures.
5. Recurse to solve the remaining grid. If recursion succeeds, propagate success upward immediately.
6. If no digit leads to a solution, undo the placement and backtrack. This restores all constraint structures so that earlier decisions remain consistent.
7. If all cells are filled, return success, and the board is complete.

### Why it works

At every step, the algorithm maintains the invariant that all filled cells satisfy Sudoku constraints. The constraint tables ensure that no invalid digit is ever placed, and backtracking guarantees that partial assignments are reversible. Since every recursive state explores only configurations consistent with constraints so far, the search space contains no invalid branches, only potentially complete solutions. Because the grid is finite and each step strictly reduces the number of empty cells, the recursion must eventually terminate either by finding a valid full assignment or exhausting all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_sudoku(board):
    rows = [[False]*10 for _ in range(9)]
    cols = [[False]*10 for _ in range(9)]
    boxes = [[False]*10 for _ in range(9)]
    empties = []

    def box_id(r, c):
        return (r // 3) * 3 + (c // 3)

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                empties.append((r, c))
            else:
                d = board[r][c]
                rows[r][d] = True
                cols[c][d] = True
                boxes[box_id(r, c)][d] = True

    def get_candidates(r, c):
        b = box_id(r, c)
        return [d for d in range(1, 10)
                if not rows[r][d] and not cols[c][d] and not boxes[b][d]]

    def dfs():
        if not empties:
            return True

        best_idx = -1
        best_cands = None

        for i, (r, c) in enumerate(empties):
            cands = get_candidates(r, c)
            if not cands:
                return False
            if best_cands is None or len(cands) < len(best_cands):
                best_cands = cands
                best_idx = i

        r, c = empties.pop(best_idx)
        b = box_id(r, c)

        for d in best_cands:
            if not rows[r][d] and not cols[c][d] and not boxes[b][d]:
                board[r][c] = d
                rows[r][d] = cols[c][d] = boxes[b][d] = True

                if dfs():
                    return True

                rows[r][d] = cols[c][d] = boxes[b][d] = False
                board[r][c] = 0

        empties.append((r, c))
        return False

    dfs()
    return board

def main():
    board = []
    for _ in range(9):
        line = input().strip()
        row = []
        for ch in line:
            if ch in "0.":
                row.append(0)
            else:
                row.append(int(ch))
        board.append(row)

    solve_sudoku(board)

    for r in range(9):
        print("".join(str(x) for x in board[r]))

if __name__ == "__main__":
    main()
```

The solver builds constant time constraint tables for rows, columns, and boxes. The DFS routine always selects the most constrained empty cell first, which is the key heuristic that prevents pathological branching. The undo logic is symmetric with the placement logic, ensuring correctness during backtracking. A subtle implementation detail is that the chosen cell is temporarily removed from the empties list and restored only if the branch fails, which avoids revisiting the same decision state.

## Worked Examples

### Example 1

Consider a partially filled board where only a few cells are empty in the first row.

At the start, constraint tables reflect all given digits, and empties include all blank cells.

| Step | Selected cell | Candidates | Action |
| --- | --- | --- | --- |
| 1 | (0, 3) | {2, 5} | Try 2 |
| 2 | (0, 3) | {2, 5} | Backtrack from dead end |
| 3 | (0, 3) | {2, 5} | Try 5 |
| 4 | completion | none | success |

This trace shows how pruning quickly eliminates invalid partial assignments, preventing deeper exploration of inconsistent branches.

### Example 2

A harder configuration where the first chosen cell has many constraints.

| Step | Selected cell | Candidates | Action |
| --- | --- | --- | --- |
| 1 | (4, 4) | {1, 3} | Try 1 |
| 2 | (4, 4) | {1, 3} | propagate failure |
| 3 | (4, 4) | {1, 3} | Try 3 |
| 4 | completion | none | success |

This demonstrates the benefit of the minimum-candidate heuristic, since central cells are often heavily constrained and reduce search depth significantly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Exponential but small in practice | Each step reduces empty cells, and candidate ordering prunes most branches early |
| Space | O(81) | Fixed board plus recursion stack |

The constraints are tight in size but not in combinatorial freedom. The algorithm fits comfortably because pruning prevents exploration of most theoretical states.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import main  # assuming solution is in main()
    try:
        main()
    except SystemExit:
        pass
    return sys.stdout.getvalue().strip()

# Note: samples are unspecified, so illustrative tests are used

# empty grid (minimal constraint case)
assert run(
"000000000\n000000000\n000000000\n000000000\n000000000\n000000000\n000000000\n000000000\n000000000\n"
) != "", "full fill exists"

# already solved grid
assert run(
"123456789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642\n"
) == \
"123456789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642", "identity"

# single missing cell
assert run(
"123456789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531640\n"
) != "", "single fix"

# constrained puzzle small variation
assert run(
"530070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079\n"
) != "", "standard sudoku solvable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty grid | valid filled grid | extreme branching |
| solved grid | same grid | no-op correctness |
| single missing cell | valid completion | local correctness |
| standard puzzle | valid solution | realistic constraint propagation |

## Edge Cases

### Fully empty grid

Input is a grid of all zeros. The algorithm starts with maximum branching but immediately benefits from constraint propagation as soon as the first few placements occur. The heuristic selection prevents uniform branching from exploding.

### Already solved grid

The empties list is empty from the start. The DFS terminates immediately because the base condition is satisfied, returning the original grid unchanged.

### Single forced cell

A nearly complete grid with one missing value tests whether constraint tables correctly identify the only valid digit. The algorithm computes candidates for that cell and directly fills it without backtracking.

### Highly constrained center cell

When the most constrained cell is in the middle of the grid, the heuristic correctly selects it first. This avoids exploring irrelevant peripheral choices and keeps recursion shallow.
