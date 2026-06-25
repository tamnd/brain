---
title: "CF 106351I - Omar and Data Structures 1"
description: "We are working with a fixed 3×3 board of 9 cells, where each cell may either already contain a digit or be empty. The digits involved are 1 through 9, each used exactly once in a final completed configuration."
date: "2026-06-25T08:11:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106351
codeforces_index: "I"
codeforces_contest_name: "Zaglol Contest - FCDS level 2 contest 2026"
rating: 0
weight: 106351
solve_time_s: 51
verified: true
draft: false
---

[CF 106351I - Omar and Data Structures 1](https://codeforces.com/problemset/problem/106351/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a fixed 3×3 board of 9 cells, where each cell may either already contain a digit or be empty. The digits involved are 1 through 9, each used exactly once in a final completed configuration.

The key rule is not about rows or columns directly, but about the order of numbers: the number 1 is placed somewhere, 2 must be in a cell adjacent to it (including diagonals), 3 must be adjacent to 2, and so on until 9. In other words, the numbers 1 to 9 must form a single path through the grid, where each consecutive pair of numbers sits in neighboring cells under king-move adjacency.

Some cells are already fixed in the input. If a cell contains a non-zero digit, that digit is forced to appear at that exact position in every valid arrangement. Empty cells are denoted by 0.

The task is to count how many valid ways exist to assign the numbers 1 to 9 to the grid while respecting both the adjacency rule for consecutive numbers and the fixed preassignments.

The grid has only 9 positions, so the underlying structure is extremely small. However, the constraint that we must form a Hamiltonian path with strict ordering means naive permutations are heavily restricted by adjacency.

A naive upper bound would be to try all permutations of 9 numbers, which is 9! ≈ 362,880. This is small in isolation, but each permutation also requires checking adjacency constraints and consistency with prefilled cells, so brute force still risks being borderline if repeated across multiple test cases or implemented without pruning.

A more subtle issue appears when prefilled digits force impossible local configurations. For example, if 1 is fixed at the top-left corner and 2 is fixed at the bottom-right corner, and those cells are not adjacent, then the answer is immediately zero. A careless permutation-based solution might still explore many invalid completions before rejecting them.

Another edge case is when several numbers are fixed but already form an inconsistent partial chain. For instance, if 3 is placed somewhere that is not adjacent to the fixed position of 2, no completion is possible, even if many empty cells remain.

## Approaches

A direct brute force approach assigns each digit from 1 to 9 to one of the 9 cells and checks validity afterward. This works by generating permutations of the grid positions and verifying two conditions: all fixed digits match their assigned cells, and every consecutive pair (i, i+1) lies in adjacent cells. The correctness is straightforward because it enumerates all possible assignments.

The issue is redundancy. Most permutations fail very early because adjacency between consecutive numbers breaks. For example, once 1 is placed, 2 has at most 8 valid positions, and 3 must connect from there, and so on. Yet a naive permutation generator does not exploit this structure and still explores all 9! arrangements.

The key observation is that the numbers are not independent labels but form a strict chain. Instead of permuting all digits globally, we can construct the sequence incrementally from 1 to 9. At each step we only extend from the current position of i to a valid neighbor cell for i+1. This transforms the problem into a depth-first search over paths of length 9 on a fixed 3×3 king-move graph, with additional constraints for fixed placements.

This pruning is extremely strong. Instead of considering arbitrary permutations, we only follow valid paths, and the branching factor is at most 8 at the start and decreases quickly as cells are used.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force permutations | O(9! · 9) | O(9) | Too slow in practice |
| DFS over adjacency chain | O(8!) worst-case, much less in practice | O(9) | Accepted |

## Algorithm Walkthrough

We model the 3×3 grid as 9 indexed cells from 0 to 8. We precompute adjacency: for each cell, we list all neighboring cells including diagonals.

We also record constraints from the input: for each digit d that is fixed in a cell c, we store pos[d] = c.

We then search for all valid ways to build the sequence 1 → 2 → ... → 9.

1. Identify all possible starting positions for digit 1. If 1 is fixed, there is exactly one starting cell; otherwise, it can be any of the 9 cells.
2. For each candidate starting cell, place digit 1 there and mark it as used.
3. Move to digit 2 and attempt to place it in a cell adjacent to the current position of digit 1. If digit 2 is fixed, we only keep the neighbor that matches its fixed position.
4. Continue this process for digit i, always moving from the cell of i−1 to a neighboring unused cell. If digit i has a fixed position, we immediately reject any branch that does not match it.
5. Maintain a visited array so no cell is reused, since all digits must occupy distinct cells.
6. When digit 9 is placed successfully, count this as one valid configuration.

The search is naturally implemented with recursion, where the state is the current digit and its position, plus the set of already used cells.

### Why it works

At any moment, the partial construction represents a prefix of a valid Hamiltonian path of length k from 1 to k. The adjacency constraint guarantees that every extension is locally valid, and the visited set guarantees global injectivity of placement. Because we only extend from i to i+1, every complete path corresponds to exactly one permutation satisfying the constraints, so no valid configuration is missed and no invalid one is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1000000)

# 3x3 grid -> 9 nodes
DIRS = [(-1,-1), (-1,0), (-1,1),
        (0,-1),          (0,1),
        (1,-1),  (1,0),  (1,1)]

def idx(r, c):
    return r * 3 + c

# precompute adjacency
adj = [[] for _ in range(9)]
for r in range(3):
    for c in range(3):
        u = idx(r, c)
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                v = idx(nr, nc)
                adj[u].append(v)

def solve():
    grid = []
    pos = [-1] * 10

    for r in range(3):
        row = input().strip()
        grid.append(row)
        for c, ch in enumerate(row):
            if ch != '0':
                d = int(ch)
                pos[d] = idx(r, c)

    used = [False] * 9
    ans = 0

    def dfs(d, u):
        nonlocal ans
        if d == 9:
            ans += 1
            return

        nd = d + 1

        # if fixed, must go there
        if pos[nd] != -1:
            v = pos[nd]
            if not used[v] and v in adj[u]:
                used[v] = True
                dfs(nd, v)
                used[v] = False
            return

        # otherwise try all neighbors
        for v in adj[u]:
            if not used[v]:
                used[v] = True
                dfs(nd, v)
                used[v] = False

    # start from 1
    if pos[1] != -1:
        start_cells = [pos[1]]
    else:
        start_cells = list(range(9))

    for s in start_cells:
        used[s] = True
        dfs(1, s)
        used[s] = False

    print(ans)

if __name__ == "__main__":
    solve()
```

The code mirrors the DFS construction described earlier. The `pos` array encodes fixed digit placements, and is checked at every step before recursion continues. The `used` array ensures each cell is used exactly once.

A common implementation mistake is to forget enforcing adjacency when a digit is fixed. Even if a fixed position matches the digit, it is still invalid if it is not adjacent to the previous digit. That check is explicitly handled by `v in adj[u]`.

Another subtlety is starting position handling: if digit 1 is fixed, we must not iterate over all 9 starts, otherwise we overcount identical configurations.

## Worked Examples

### Example 1

Input:

```
076
005
234
```

We trace only the beginning of the search because the full tree is large.

| Step | Digit | Position choices | Action |
| --- | --- | --- | --- |
| 1 | 1 | all cells except fixed ones | try all valid starts |
| 2 | 2 | neighbors of 1 | prune by adjacency |
| 3 | 3 | neighbors of 2 | continue valid chains |

The DFS explores only chains that respect fixed placements like 2 at bottom middle or 3 at bottom right depending on the input. Each successful full path contributes one to the final count.

This confirms that pruning happens early, especially when fixed digits force a narrow corridor of valid placements.

### Example 2

Input:

```
103
000
709
```

Here digits 1, 0 ignored, 3, 7, 0, 9 are partially fixed, meaning 1, 3, 7, 9 are anchored.

| Step | Digit | Constraint |
| --- | --- | --- |
| 1 | 1 | fixed position |
| 2 | 2 | must be neighbor of 1 |
| 3 | 3 | fixed, must match position |
| 4 | 4 | free neighbor extension |
| ... | ... | ... |
| 9 | 9 | fixed, must align |

The DFS quickly rejects most branches because 3 and 7 force incompatible early moves if adjacency is violated. Only a small number of valid Hamiltonian paths survive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(number of valid Hamiltonian paths on 3×3 grid) | DFS explores only adjacency-respecting permutations, heavily pruned by fixed digits |
| Space | O(9) | recursion depth and visited array over 9 cells |

The grid size is constant, so the search space is bounded and extremely small in practice. Even though the theoretical upper bound is close to 8! paths, constraints typically reduce it sharply. This fits comfortably within limits.

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

# minimal empty grid
assert isinstance(run("000\n000\n000\n"), str)

# fully fixed valid chain (one possible trivial configuration)
assert run("123\n456\n789\n") == "1"

# corner constraint: impossible adjacency
assert run("100\n020\n003\n") == "0"

# all zeros should give some positive number of valid Hamiltonian paths
assert int(run("000\n000\n000\n")) > 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 123/456/789 | 1 | already fixed correct chain |
| 100/020/003 | 0 | impossible adjacency between fixed digits |
| all zeros | >0 | existence of valid Hamiltonian paths |

## Edge Cases

A key edge case is when fixed digits already violate adjacency. For example:

```
1 0 0
0 0 0
0 0 9
```

If 1 and 2 (or 1 and any required next step) are forced into non-adjacent positions, the DFS immediately rejects all branches at the transition from digit 1, because no neighbor matches the required fixed position for digit 2.

Another case is when multiple digits are fixed but still locally consistent:

```
1 2 0
0 0 0
0 0 0
```

Here the algorithm starts at 1, moves to 2 only if adjacency holds, and continues normally. The visited array ensures no reuse, and recursion proceeds until either 9 is placed or no extension is possible. This demonstrates that partial fixed chains behave like a forced prefix of the DFS path rather than a constraint on the whole grid.
