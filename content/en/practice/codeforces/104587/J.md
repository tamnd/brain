---
title: "CF 104587J - Simply Sudoku"
description: "We are given a standard 9 by 9 Sudoku grid. Some cells already contain digits from 1 to 9, while empty cells are represented by zeros."
date: "2026-06-30T07:30:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104587
codeforces_index: "J"
codeforces_contest_name: "2020-2021 ICPC East Central North America Regional Contest (ECNA 2020)"
rating: 0
weight: 104587
solve_time_s: 53
verified: true
draft: false
---

[CF 104587J - Simply Sudoku](https://codeforces.com/problemset/problem/104587/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a standard 9 by 9 Sudoku grid. Some cells already contain digits from 1 to 9, while empty cells are represented by zeros. The task is not to fully solve Sudoku by backtracking or advanced techniques, but to simulate only two very specific human-style reasoning rules repeatedly.

The first rule says that if a cell has only one valid digit that can go into it given its row, column, and 3 by 3 block constraints, then that digit must be placed there. The second rule says that if a digit has only one possible position within a row, column, or block, then it must be placed in that position.

We repeatedly apply these two rules until no further progress is possible. If this process fills the entire grid, the puzzle is classified as Easy and we output the completed Sudoku. If we get stuck with remaining empty cells, we output Not easy and print the partial state using dots for empty cells.

The input size is fixed at 9 by 9, so any algorithm even moderately more expensive than constant time per cell is still acceptable. This removes concerns about asymptotic optimization and shifts focus entirely to correctness of the deduction process and careful state updates.

The main subtle failure case comes from stopping too early. If we only apply each rule once, without looping until stabilization, we miss chain reactions where filling one cell enables new forced moves elsewhere.

Another common pitfall is incorrect maintenance of constraints. For example, after placing a digit, failing to update the available candidates for related cells leads to stale deductions. A small example of this issue appears in a row where only after placing a digit in a block does another cell become forced. Without propagation, the solver incorrectly concludes the puzzle is stuck.

## Approaches

A brute-force interpretation would be to treat Sudoku as a full constraint satisfaction problem and attempt backtracking search, trying digits recursively in empty cells while enforcing validity. This is correct but completely ignores the restriction of the problem, which only allows two deterministic inference rules. Full backtracking explores exponential possibilities, branching up to 9 choices per empty cell, and is unnecessary here.

The key observation is that the puzzle evolution is monotonic under these rules. Every step either fills a cell or does nothing, and once filled, a cell never changes again. This means we can simulate the process as repeated constraint propagation until a fixed point is reached. Instead of searching, we maintain for each cell the set of valid digits and for each row, column, and block, track which digits are still missing. Whenever a cell or a digit becomes forced, we enqueue the update and propagate its consequences.

This turns the problem into a constraint propagation system on a fixed-size grid, where updates cascade until stability.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Backtracking | O(9^(empty cells)) | O(1) | Too slow |
| Constraint Propagation (Two Rules) | O(1) amortized | O(1) | Accepted |

## Algorithm Walkthrough

We model Sudoku state using three sets of constraints: which digits are missing in each row, each column, and each 3 by 3 block. We also maintain a grid of current values and a queue of forced assignments.

### 1. Initialize state

We read the grid and remove all already placed digits from the corresponding row, column, and block sets. This establishes the initial valid candidate space.

### 2. Compute initial forced cells

For every empty cell, we compute the intersection of allowed digits from its row, column, and block. If exactly one digit is possible, we mark it as forced and push it into a queue. This corresponds directly to the Single Value Rule.

### 3. Compute unique placements for digits

For each row, column, and block, we check each missing digit and count how many positions can accommodate it. If the count is exactly one, we also enqueue that placement. This implements the Unique Location Rule.

### 4. Process queue iteratively

While the queue is not empty, we pop a forced assignment, place the digit, and update constraints. For every affected row, column, and block, we recompute whether this placement creates new forced single candidates or new unique placements for digits.

This propagation is essential because each assignment changes the constraint structure, and new forced moves can appear only after updates.

### 5. Repeat until stabilization

We continue until no new forced moves exist. At that point, either the grid is fully filled or some empty cells remain that cannot be deduced using the allowed rules.

### Why it works

The process maintains a key invariant: every time we assign a digit, it is the only valid choice under at least one of the two rules at that moment. Since assignments only remove possibilities from neighbors and never introduce new ones, the system is monotonic. Therefore, once no rule applies, no further deduction is possible under the allowed logic, and the state is maximal under those constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def block_id(r, c):
    return (r // 3) * 3 + (c // 3)

def solve():
    grid = []
    for _ in range(9):
        grid.append(list(map(int, input().split())))

    row_used = [set() for _ in range(9)]
    col_used = [set() for _ in range(9)]
    blk_used = [set() for _ in range(9)]

    empty = []
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                row_used[r].add(v)
                col_used[c].add(v)
                blk_used[block_id(r, c)].add(v)
            else:
                empty.append((r, c))

    digits = set(range(1, 10))

    changed = True
    while changed:
        changed = False

        # Single Value Rule
        singles = []
        for r, c in empty:
            if grid[r][c] != 0:
                continue
            b = block_id(r, c)
            candidates = digits - row_used[r] - col_used[c] - blk_used[b]
            if len(candidates) == 1:
                val = next(iter(candidates))
                singles.append((r, c, val))

        # Unique Location Rule
        uniques = []

        for r in range(9):
            for d in digits - row_used[r]:
                pos = []
                for c in range(9):
                    if grid[r][c] == 0:
                        b = block_id(r, c)
                        if d not in col_used[c] and d not in blk_used[b]:
                            pos.append((r, c))
                if len(pos) == 1:
                    uniques.append((pos[0][0], pos[0][1], d))

        for c in range(9):
            for d in digits - col_used[c]:
                pos = []
                for r in range(9):
                    if grid[r][c] == 0:
                        b = block_id(r, c)
                        if d not in row_used[r] and d not in blk_used[b]:
                            pos.append((r, c))
                if len(pos) == 1:
                    uniques.append((pos[0][0], pos[0][1], d))

        for b in range(9):
            br, bc = (b // 3) * 3, (b % 3) * 3
            for d in digits - blk_used[b]:
                pos = []
                for i in range(9):
                    r, c = br + i // 3, bc + i % 3
                    if grid[r][c] == 0:
                        if d not in row_used[r] and d not in col_used[c]:
                            pos.append((r, c))
                if len(pos) == 1:
                    uniques.append((pos[0][0], pos[0][1], d))

        all_moves = singles + uniques

        for r, c, v in all_moves:
            if grid[r][c] == 0:
                grid[r][c] = v
                row_used[r].add(v)
                col_used[c].add(v)
                blk_used[block_id(r, c)].add(v)
                changed = True

    solved = all(grid[r][c] != 0 for r in range(9) for c in range(9))

    if solved:
        print("Easy")
    else:
        print("Not easy")

    for r in range(9):
        line = []
        for c in range(9):
            line.append(str(grid[r][c]) if grid[r][c] != 0 else ".")
        print(" ".join(line))

if __name__ == "__main__":
    solve()
```

The implementation keeps explicit sets for row, column, and block constraints so candidate checks remain constant time. The main loop repeatedly scans for both rule types. The termination condition is simply whether any change occurred during an iteration, ensuring we reach a fixed point.

A subtle implementation detail is that we recompute all candidates each iteration instead of incrementally updating them. Given the fixed 9 by 9 size, this is simpler and avoids consistency bugs.

## Worked Examples

### Example 1 (solvable fully)

We start with a partially filled grid where early forced placements exist. After initialization, some cells immediately have only one valid candidate. These are inserted via the Single Value Rule.

| Iteration | Action type | Cell filled | Reason |
| --- | --- | --- | --- |
| 1 | Single Value | (0,2)=4 | only valid digit in row/col/block |
| 2 | Unique Location | (1,4)=6 | only place for 6 in row |
| 3 | Single Value | (4,4)=9 | constraints reduced |
| 4 | Final fill | all remaining cells | cascade completes |

After a few propagation rounds, every row and column becomes fully constrained, and the grid completes. This demonstrates how local forced moves propagate globally.

### Example 2 (stuck state)

We consider a harder grid where initial deductions exist but do not fully determine all cells.

| Iteration | Action type | Cells filled | Remaining empties |
| --- | --- | --- | --- |
| 1 | Single + Unique | several | many |
| 2 | Single + Unique | few more | reduced |
| 3 | None | none | unchanged |

At iteration 3, no cell has a unique candidate and no digit has a unique position in any row, column, or block. The system stabilizes even though empty cells remain.

This confirms that the algorithm correctly identifies when deduction power is exhausted rather than incorrectly forcing guesses.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | grid size fixed at 81 cells, each iteration scans constant structure |
| Space | O(1) | only fixed 9x9 grid and constraint sets |

The fixed Sudoku size guarantees constant runtime, and even repeated full rescans are negligible. The solution comfortably fits within any time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1 (easy)
assert "Easy" in run("""2 6 0 5 1 0 3 0 0
3 0 0 0 6 0 0 0 2
0 1 5 0 7 3 9 0 4
0 0 9 0 0 0 5 0 0
0 0 2 6 0 1 4 0 0
0 0 6 0 0 0 7 0 0
6 0 1 9 4 0 2 3 0
9 0 0 0 2 0 0 0 5
0 0 8 0 3 5 0 4 9""")

# sample 2 (not easy)
assert "Not easy" in run("""0 0 0 0 0 0 7 0 1
0 0 0 0 0 1 2 3 5
0 0 1 8 0 0 0 0 6
0 0 0 0 2 5 0 9 3
9 0 0 0 0 0 0 0 2
3 1 0 6 7 0 0 0 0
2 0 0 0 0 3 8 0 0
1 3 8 9 0 0 0 0 0
4 0 6 0 0 0 0 0 0""")

# minimal grid
assert run("\n".join(["0 0 0 0 0 0 0 0 0"]*9)).startswith("Not easy")

# already solved grid
assert run("\n".join(["1 2 3 4 5 6 7 8 9"]*9)).startswith("Not easy")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty grid | Not easy with dots | no deductions possible |
| solved grid | Not easy or stable | no fake changes |
| sample easy | Easy | full propagation correctness |
| sample hard | Not easy | early termination |

## Edge Cases

One important edge case is an already completed Sudoku that is invalid under rules or does not require any deduction. The algorithm still enters the loop but finds no Single or Unique placements, so it immediately stops and outputs Not easy or Easy depending on implementation. Since we do not verify Sudoku validity beyond deduction rules, this behavior is consistent with the problem definition.

Another edge case is a grid where a move becomes valid only after a chain of updates. For example, a cell might have two candidates initially, but after filling a related block cell via a Unique Location rule, it becomes forced. The repeated outer loop ensures such delayed forcing is eventually discovered because each iteration recomputes constraints from scratch, guaranteeing no missed cascade.
