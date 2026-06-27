---
title: "CF 105093F - Meta Sudoku"
description: "We are working with a fixed 4 by 4 Sudoku variant. Each cell contains a digit from 1 to 4, and validity means three simultaneous constraints: every row contains no repeated digit, every column contains no repeated digit, and each of the four 2 by 2 blocks also contains no…"
date: "2026-06-27T20:50:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105093
codeforces_index: "F"
codeforces_contest_name: "2024 UP ACM Algolympics Final Round"
rating: 0
weight: 105093
solve_time_s: 47
verified: true
draft: false
---

[CF 105093F - Meta Sudoku](https://codeforces.com/problemset/problem/105093/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a fixed 4 by 4 Sudoku variant. Each cell contains a digit from 1 to 4, and validity means three simultaneous constraints: every row contains no repeated digit, every column contains no repeated digit, and each of the four 2 by 2 blocks also contains no repeated digit.

Alongside this we are given a partially filled 4 by 4 grid, where some cells are fixed clues and others are empty. We are also given a target fully filled valid Sudoku grid. The operation allowed is to erase clues from the puzzle. A cell that is erased becomes empty and imposes no constraint.

The question is: for how many valid complete Sudoku grids can we transform the given puzzle into a state where that grid is a valid completion, if we are allowed to erase at most k clues.

Equivalently, for each valid full Sudoku grid S, we look at how many cells in the puzzle currently disagree with S in a problematic way: if a cell contains a clue different from S, we must erase it. We want to know whether the number of such forced deletions is at most k. We count how many S satisfy this condition.

The input size is extremely small in structure: the grid is always 4 by 4. However, the number of test cases is up to 5000, so we cannot afford any per test brute force that depends on enumerating all valid Sudoku completions from scratch with expensive search.

The key observation is that the 4 by 4 Sudoku universe is tiny. The total number of valid completed grids is fixed and can be enumerated once. The real task is then checking compatibility of each candidate solution with the given puzzle under a deletion budget.

A subtle edge case arises when the puzzle already contains conflicting clues. For example, a row like `112.` is invalid as a partial Sudoku state. This does not matter, because we are not required to use the puzzle as a valid partial solution. We only erase clues; we never modify values. So inconsistent puzzles are allowed and simply force more deletions.

Another edge case is when k is large, up to 16. This means we could erase everything, so every valid Sudoku solution must be counted. That corresponds to the total number of 4 by 4 Sudokus consistent with the rules.

## Approaches

The brute force idea is straightforward: generate all possible 4 by 4 grids filled with digits 1 to 4, filter those that satisfy Sudoku constraints, and then for each test case compare against the puzzle by counting mismatched filled cells.

A naive generation tries 4^(16) grids, which is about 4.3 billion possibilities. Even with pruning, this is still too large if repeated per test case. However, the crucial point is that valid 4 by 4 Sudokus are far fewer. We can precompute all valid completions once using backtracking with constraint checking. The state space collapses quickly because each row and column must be permutations of 1 to 4 and blocks must also be consistent.

After enumeration, each test case reduces to a comparison problem: for a candidate solution S, we compute how many cells in the puzzle have a conflicting clue. If this count is at most k, we count S.

The optimization is to precompute the full list of valid Sudoku grids once. The number of such grids is small enough that brute force backtracking over 16 cells with pruning is instantaneous. Then each query is only 16 comparisons per solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full brute force per test | O(T · 4^16) | O(1) | Too slow |
| Precompute all Sudokus + check | O(S · T · 16) | O(S) | Accepted |

Here S is the number of valid 4 by 4 Sudoku solutions, a small constant.

## Algorithm Walkthrough

1. Precompute all valid 4 by 4 Sudoku grids using backtracking. We fill the grid cell by cell, maintaining row masks, column masks, and 2 by 2 block masks. This ensures we only explore valid partial states.
2. Store every completed valid grid in a list. Each grid can be stored as a 16 element array or 4 strings.
3. For each test case, read the puzzle grid and record the positions and values of all clues.
4. Initialize a counter to zero for this test case.
5. For each precomputed Sudoku solution S, compute the number of mandatory deletions required to make the puzzle compatible with S. This is simply the number of clue cells where the puzzle value differs from S.
6. If this number is at most k, increment the answer.
7. Output the final count.

Why it works: every valid Sudoku solution in the 4 by 4 space is explicitly enumerated exactly once. For a fixed solution S, the puzzle can be turned into S if and only if every conflicting clue is removed. Since erasing is the only allowed operation, and each erased cell removes one constraint, the minimal number of deletions needed is exactly the number of mismatching clues. Therefore S is feasible if and only if this mismatch count does not exceed k. The algorithm checks this condition for all S, so it counts exactly the valid ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

# Precompute all valid 4x4 Sudoku solutions
solutions = []

grid = [[0] * 4 for _ in range(4)]

row_mask = [0] * 4
col_mask = [0] * 4
block_mask = [[0] * 2 for _ in range(2)]

def block_id(r, c):
    return r // 2, c // 2

def dfs(cell):
    if cell == 16:
        solutions.append([row[:] for row in grid])
        return

    r = cell // 4
    c = cell % 4
    br, bc = block_id(r, c)

    used = row_mask[r] | col_mask[c] | block_mask[br][bc]
    for v in range(1, 5):
        bit = 1 << v
        if used & bit:
            continue

        grid[r][c] = v
        row_mask[r] |= bit
        col_mask[c] |= bit
        block_mask[br][bc] |= bit

        dfs(cell + 1)

        row_mask[r] ^= bit
        col_mask[c] ^= bit
        block_mask[br][bc] ^= bit

        grid[r][c] = 0

dfs(0)

T = int(input())
for _ in range(T):
    k = int(input())
    puzzle = [input().strip() for _ in range(4)]

    clues = []
    for i in range(4):
        for j in range(4):
            if puzzle[i][j] != '.':
                clues.append((i, j, int(puzzle[i][j])))

    ans = 0
    for sol in solutions:
        need = 0
        for i, j, v in clues:
            if sol[i][j] != v:
                need += 1
                if need > k:
                    break
        if need <= k:
            ans += 1

    print(ans)
```

The precomputation step builds every valid Sudoku grid once using depth-first search with bitmask pruning. The masks encode whether a digit is already used in a row, column, or block, so each placement check is constant time.

During each test case, we extract only the fixed clues, ignoring empty cells. This is important because only existing clues impose deletion cost. For each candidate solution, we compare only against these clues. The early exit when `need > k` prevents unnecessary full scanning.

## Worked Examples

Consider a simple case where k is large enough that deletions are not restrictive. Then every valid Sudoku solution is counted.

For a more illustrative case, suppose the puzzle has two conflicting clues in the same cell positions across different candidate solutions.

| Solution | (0,0) | (0,1) | Clue mismatch count | Valid (k = 1) |
| --- | --- | --- | --- | --- |
| S1 | 1 | 2 | 0 | Yes |
| S2 | 1 | 3 | 1 | Yes |
| S3 | 4 | 2 | 1 | Yes |
| S4 | 3 | 3 | 2 | No |

This shows that the algorithm is effectively filtering solutions by Hamming distance over the clue set.

The trace confirms that only mismatches on fixed clues matter, and empty cells never influence feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S · T · C) | S is number of valid 4x4 Sudokus, C is number of clues (≤16) |
| Space | O(S) | storage of all valid Sudoku grids |

The number of valid 4 by 4 Sudoku grids is a small constant, so S is bounded and precomputation is negligible. Each test case only scans at most 16 clues per solution, so the total runtime easily fits within limits even for T = 5000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    solutions = []
    grid = [[0]*4 for _ in range(4)]
    row = [0]*4
    col = [0]*4
    blk = [[0]*2 for _ in range(2)]

    def dfs(cell):
        if cell == 16:
            solutions.append([r[:] for r in grid])
            return
        r = cell // 4
        c = cell % 4
        br, bc = r//2, c//2
        used = row[r] | col[c] | blk[br][bc]
        for v in range(1,5):
            bit = 1<<v
            if used & bit: continue
            grid[r][c] = v
            row[r] |= bit
            col[c] |= bit
            blk[br][bc] |= bit
            dfs(cell+1)
            row[r] ^= bit
            col[c] ^= bit
            blk[br][bc] ^= bit

    dfs(0)

    T = int(input())
    out = []
    for _ in range(T):
        k = int(input())
        g = [input().strip() for _ in range(4)]
        clues = [(i,j,int(g[i][j])) for i in range(4) for j in range(4) if g[i][j] != '.']

        ans = 0
        for s in solutions:
            need = 0
            for i,j,v in clues:
                if s[i][j] != v:
                    need += 1
                    if need > k:
                        break
            if need <= k:
                ans += 1
        out.append(str(ans))
    return "\n".join(out)

# small sanity checks
assert run("""1
0
....
....
....
....""") == "288"  # all valid 4x4 sudokus (known constant)

assert run("""1
16
1111
....
....
....""") == run("""1
16
....
....
....
....""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty grid, k=0 | total number of Sudokus | base enumeration correctness |
| Fully constrained single row clue | reduced compatibility | deletion logic |
| Max k = 16 | full solution count | boundary behavior |

## Edge Cases

A key edge case is when the puzzle has no clues at all. In this case, every valid Sudoku is achievable with zero deletions, so the answer equals the total number of valid 4 by 4 Sudoku grids. The algorithm handles this naturally because the clue list is empty, so every solution has mismatch count zero.

Another case is when k equals 16, the maximum possible number of clues. Even if every clue conflicts with a candidate solution, we can erase them all. The algorithm correctly counts all valid Sudoku grids because every mismatch count is ≤ 16.

A final subtle case is inconsistent clue placement. For example, a row may contain repeated digits. This does not break correctness because the algorithm never validates the puzzle itself; it only compares candidate solutions against existing clues. Each conflicting clue simply increments the deletion cost independently, which matches the problem definition exactly.
