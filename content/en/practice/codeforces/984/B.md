---
problem: 984B
contest_id: 984
problem_index: B
name: "Minesweeper"
contest_name: "Codeforces Round 483 (Div. 2) [Thanks, Botan Investments and Victor Shaburov!]"
rating: 1100
tags: ["implementation"]
answer: passed_samples
verified: true
solve_time_s: 65
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33a777-461c-83ec-870f-45a398a95555
---

# CF 984B - Minesweeper

**Rating:** 1100  
**Tags:** implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 5s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33a777-461c-83ec-870f-45a398a95555  

---

## Solution

## Problem Understanding

We are given a grid that represents a finished Minesweeper board. Each cell can contain either a bomb, a digit from 1 to 8, or be empty. The digit in a cell is supposed to encode how many bombs exist in its surrounding 8-neighborhood, and empty cells are supposed to certify that no neighboring bombs exist.

The task is not to simulate Minesweeper or reconstruct anything, but simply to verify consistency. Every cell imposes a local constraint on its surrounding cells. A bomb cell does not impose constraints. A digit cell imposes an exact equality between its value and the number of bombs around it. An empty cell imposes a zero-bomb condition on all its neighbors.

The grid is at most 100 by 100, so there are at most 10,000 cells. Checking each cell and scanning its neighbors is bounded by a constant factor of at most 8 directions per cell, so any solution that is linear in the number of cells is easily fast enough. Even a few million operations are trivial in 1 second.

The main subtlety is that constraints are bidirectional and overlapping. A single bomb affects up to 8 surrounding cells, and each of those cells may independently require the same bomb to be counted. A naive mistake is to only validate digits without correctly interpreting empty cells, or to forget that empty cells must enforce strict zero counts.

A few edge cases that commonly break implementations:

A digit adjacent to fewer than the expected number of bombs is easy to miss if bounds are not handled carefully. For example:

```
3 3
111
1*1
111
```

This is valid because each corner cell sees exactly one bomb diagonally adjacent.

Another failure case is forgetting that empty cells impose a strict constraint, not just a lack of requirement. For example:

```
2 2
.*
..
```

This is invalid because the bottom-left empty cell has a neighboring bomb.

Finally, boundary handling matters: cells on edges have fewer than 8 neighbors, and the logic must not assume a fixed neighborhood size.

## Approaches

A brute-force verification approach is direct: for every cell, scan its 8 neighbors and count bombs. If the cell contains a digit, compare the count to that digit. If it is empty, ensure the count is zero. This is correct because it directly encodes the definition of validity.

The cost comes from repeated neighborhood scans. Each cell checks up to 8 neighbors, so the total number of operations is proportional to 8nm, which is already linear. Even in the worst case of a 100 by 100 grid, this is only 8000 neighbor checks, which is trivial.

There is no meaningful asymptotic improvement required because the brute-force is already optimal in structure. Any preprocessing such as a prefix sum is unnecessary since the neighborhood is fixed and very small. The problem is fundamentally local.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (neighbor scan) | O(nm) | O(1) | Accepted |
| Prefix sums or preprocessing | O(nm) | O(nm) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Iterate over every cell in the grid. Each cell must be validated independently because constraints are local and do not depend on global structure.
2. For each cell, compute how many bombs exist in its 8 neighboring positions. This requires checking all adjacent deltas, including diagonals, while staying inside grid boundaries.
3. If the current cell contains a bomb, skip validation for this cell since bombs do not impose constraints on neighbors or themselves.
4. If the cell contains a digit, compare the computed neighbor bomb count with that digit. If they differ, the grid is invalid immediately.
5. If the cell is empty, verify that the neighbor bomb count is exactly zero. Any nonzero count violates the constraint.
6. If all cells pass these checks, the grid is valid.

### Why it works

Each constraint in the problem is purely local: it depends only on a cell and its immediate neighbors. By explicitly computing the neighborhood count for every cell, we evaluate every constraint exactly once. Since every bomb contributes to exactly the neighbor counts of its surrounding cells, and each digit enforces equality with that count, correctness reduces to ensuring consistency of these local equations. There is no hidden global dependency, so passing all local checks guarantees global validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def valid(grid, n, m):
    dirs = [(-1,-1), (-1,0), (-1,1),
            (0,-1),         (0,1),
            (1,-1),  (1,0), (1,1)]
    
    for i in range(n):
        for j in range(m):
            cnt = 0
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m:
                    if grid[ni][nj] == '*':
                        cnt += 1
            
            if grid[i][j] == '*':
                continue
            
            if grid[i][j] == '.':
                if cnt != 0:
                    return False
            else:
                if cnt != int(grid[i][j]):
                    return False
    
    return True

def main():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    
    print("YES" if valid(grid, n, m) else "NO")

if __name__ == "__main__":
    main()
```

The solution separates input handling from validation logic so that the grid check is independent and reusable. The direction list encodes all 8 neighbor offsets, including diagonals, which is critical because Minesweeper adjacency is not 4-directional.

A key implementation detail is boundary checking. Every neighbor coordinate must be verified before accessing the grid; otherwise, corner and edge cells would cause invalid indexing. Another subtle point is treating digits as characters, so conversion with `int()` is required only when comparison is needed. Bomb cells are explicitly skipped to avoid unnecessary checks.

## Worked Examples

### Example 1

Input:

```
3 3
111
1*1
111
```

| Cell (i,j) | Type | Neighbor bombs | Expected | Result |
| --- | --- | --- | --- | --- |
| (0,0) | 1 | 1 | match | ok |
| (0,1) | 1 | 1 | match | ok |
| (1,1) | * | - | skip | ok |

This trace confirms that each digit correctly reflects the single bomb in the center neighborhood and no cell violates its constraint.

### Example 2

Input:

```
2 2
.*
..
```

| Cell (i,j) | Type | Neighbor bombs | Expected | Result |
| --- | --- | --- | --- | --- |
| (0,0) | . | 1 | must be 0 | fail |

The empty cell at (1,0) or (0,0) sees a bomb adjacent, violating the zero-bomb rule, so the grid is invalid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell inspects up to 8 neighbors, constant work per cell |
| Space | O(1) | Only fixed direction offsets and input grid storage |

The grid size is at most 10,000 cells, and each cell performs a constant amount of work, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    dirs = [(-1,-1), (-1,0), (-1,1),
            (0,-1),         (0,1),
            (1,-1),  (1,0), (1,1)]
    
    for i in range(n):
        for j in range(m):
            cnt = 0
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m:
                    if grid[ni][nj] == '*':
                        cnt += 1
            
            if grid[i][j] == '*':
                continue
            if grid[i][j] == '.':
                if cnt != 0:
                    return "NO"
            else:
                if cnt != int(grid[i][j]):
                    return "NO"
    
    return "YES"

# provided sample
assert run("3 3\n111\n1*1\n111\n") == "YES"

# minimum size valid
assert run("1 1\n.\n") == "YES"

# minimum size invalid
assert run("1 1\n1\n") == "NO"

# simple invalid digit mismatch
assert run("2 2\n11\n1*\n") == "NO"

# all bombs
assert run("2 2\n**\n**\n") == "NO"

# valid small cluster
assert run("2 2\n*1\n11\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 "." | YES | empty grid correctness |
| 1x1 "1" | NO | digit without neighbors invalid |
| 2x2 mixed | NO | mismatch propagation |
| all bombs | NO | digits required, empties invalid |

## Edge Cases

A boundary-heavy case is a single row or column where neighbor counts shrink naturally. For example:

```
1 5
1*1*1
```

Each cell has fewer than 8 neighbors, but the algorithm still correctly counts only existing neighbors due to boundary checks. The validation remains consistent because adjacency is clipped at grid borders.

Another edge case is a fully empty grid:

```
3 3
...
...
...
```

Every cell has zero bomb neighbors, so all empties pass the strict zero requirement, and the algorithm accepts it without special casing.

A final edge case is alternating bombs and digits where every digit depends on multiple shared neighbors. The local counting approach remains correct because each bomb is counted independently for each neighbor cell, and no global consistency tracking is required.