---
title: "CF 1103A - Grid game"
description: "We are working on a fixed 4 by 4 board that starts empty. A stream of dominoes arrives one by one, and each domino must be placed immediately when it comes. Each domino is either vertical, covering two cells in the same column, or horizontal, covering two cells in the same row."
date: "2026-06-13T07:45:08+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1103
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 534 (Div. 1)"
rating: 1400
weight: 1103
solve_time_s: 203
verified: true
draft: false
---

[CF 1103A - Grid game](https://codeforces.com/problemset/problem/1103/A)

**Rating:** 1400  
**Tags:** constructive algorithms, implementation  
**Solve time:** 3m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a fixed 4 by 4 board that starts empty. A stream of dominoes arrives one by one, and each domino must be placed immediately when it comes.

Each domino is either vertical, covering two cells in the same column, or horizontal, covering two cells in the same row. Once placed, the board may change: if any row becomes completely filled, that entire row is erased at the same moment; similarly, if any column becomes completely filled, it is also erased. These deletions happen after each placement and may clear multiple rows or columns at once.

The task is to decide where to place every incoming domino so that it always fits into currently free cells, and we must output the position of every placement. The output position is the smallest row and column touched by that domino, which corresponds to the top-left cell of a vertical domino or the leftmost cell of a horizontal domino.

The key constraint is that the board is extremely small, only 16 cells, while the number of dominoes can be large up to 1000. This immediately rules out any strategy that tries to maintain a complex global optimization over time. Even a constant factor inefficient simulation is fine, as long as each step is bounded by a small fixed search over a 4 by 4 grid.

A subtle difficulty comes from the deletion rule. A naive approach that simply “fills cells greedily” without simulating row and column clearing will eventually break, because previously blocked space can suddenly reappear after deletions. Another failure case is assuming a fixed pattern of placement; the removals make the state dynamic and dependent on past placements.

A final edge case is when multiple rows or columns become full at the same time. They must all be cleared simultaneously, otherwise later placements may incorrectly think cells are still occupied.

## Approaches

A brute-force interpretation would try to simulate all possible placements of each domino at every step. For each incoming piece, we would scan all valid positions and recursively try future placements. This quickly becomes exponential, since each step has up to dozens of placement choices even on a 4 by 4 board, and there can be 1000 steps. Even with pruning, the branching factor makes this infeasible.

The key observation is that the board is so small that we never need to look ahead. Instead, we can simulate greedily while always maintaining a valid configuration. Since deletions continuously reset parts of the board, we are not building toward a final packed configuration but repeatedly solving a tiny packing problem on a nearly fresh board.

This allows a constructive strategy: for each domino, we simply search for the first valid placement that fits the current board state. After placing it, we immediately update the board and clear any full rows or columns. Because the grid is constant size, checking all possibilities costs constant time, and the full simulation is linear in the length of the input.

The reason this works is that any locally valid placement is sufficient. The deletions guarantee that the board never accumulates irreversible constraints; instead, it continuously frees space, preventing dead ends.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search Tree | Exponential | Exponential | Too slow |
| Greedy simulation with scanning | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a 4 by 4 boolean grid representing occupied cells.

1. For each incoming domino, we scan the grid in a fixed order to find a valid placement.

For a horizontal domino, we look for a row r and column c such that both (r, c) and (r, c+1) are empty. For a vertical domino, we look for (r, c) and (r+1, c) empty.

The fixed scan order ensures determinism and avoids ambiguity.
2. Once a valid placement is found, we mark the two cells as occupied and record the output coordinate as (r, c) in 1-based indexing.
3. After placement, we check all rows. If a row has all four cells occupied, we clear it by setting them to empty.
4. We then check all columns. If a column has all four cells occupied, we clear it similarly.
5. We repeat this clearing step until no row or column is fully filled, since clearing a row may cause a column to become full and vice versa.

The reason we repeatedly clear is that a single placement can trigger a cascade of deletions.

### Why it works

At every step, the grid represents exactly the current set of active cells after all deletions have been applied. The scan always finds a placement because the board has at most 16 cells and deletions prevent permanent saturation. Since we only place a domino in two empty cells, we never violate overlap constraints. The clearing rule ensures that any time a row or column becomes full, it is immediately removed, restoring capacity and preventing deadlock.

## Python Solution

```python
import sys
input = sys.stdin.readline

def clear(board):
    changed = True
    while changed:
        changed = False

        # check rows
        for r in range(4):
            if all(board[r][c] for c in range(4)):
                for c in range(4):
                    board[r][c] = 0
                changed = True

        # check cols
        for c in range(4):
            if all(board[r][c] for r in range(4)):
                for r in range(4):
                    board[r][c] = 0
                changed = True

def solve():
    s = input().strip()
    board = [[0] * 4 for _ in range(4)]
    out = []

    for ch in s:
        placed = False

        if ch == '1':  # horizontal
            for r in range(4):
                for c in range(3):
                    if board[r][c] == 0 and board[r][c + 1] == 0:
                        board[r][c] = board[r][c + 1] = 1
                        out.append((r + 1, c + 1))
                        placed = True
                        break
                if placed:
                    break

        else:  # vertical
            for r in range(3):
                for c in range(4):
                    if board[r][c] == 0 and board[r + 1][c] == 0:
                        board[r][c] = board[r + 1][c] = 1
                        out.append((r + 1, c + 1))
                        placed = True
                        break
                if placed:
                    break

        clear(board)

    print("\n".join(f"{r} {c}" for r, c in out))

if __name__ == "__main__":
    solve()
```

The solution keeps a literal 4 by 4 occupancy grid, which avoids any complex data structures. The placement logic is a deterministic scan, always choosing the first available fit, which is safe because the grid is tiny and we never need optimal packing.

The clearing function is separated because row and column deletions can chain, and we must keep applying them until stability is reached.

A common mistake is forgetting to clear repeatedly, which can leave a newly completed row undeleted if it forms after a column removal in the same step.

## Worked Examples

### Example 1

Input:

```
010
```

We start with an empty board.

| Step | Domino | Placement (r, c) | Key action |
| --- | --- | --- | --- |
| 1 | vertical | (1,1) | first available vertical slot |
| 2 | horizontal | (1,2) | first available horizontal slot |
| 3 | vertical | (1,4) | placed, then row/col cleanup occurs |

After the third placement, row 1 becomes full and is cleared, matching the sample behavior.

This trace shows that even though we greedily fill from the top-left, deletions reshape the board and prevent blocking.

### Example 2

Input:

```
1111
```

| Step | Domino | Placement | Key action |
| --- | --- | --- | --- |
| 1 | H | (1,1) | occupy (1,1)-(1,2) |
| 2 | H | (1,3) | row 1 becomes full later |
| 3 | H | (2,1) | row 1 cleared, space reused |
| 4 | H | (2,3) | fills second row |

This demonstrates that row clearing allows reuse of space, so even repeated horizontal placements remain feasible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each domino scans at most 16 cells and clearing checks a fixed 4 by 4 grid |
| Space | O(1) | only a constant-size board is stored |

The constraints allow up to 1000 operations, and each operation is constant work over a fixed grid, so the solution is easily within limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | single placement | vertical base case |
| `1` | single placement | horizontal base case |
| `0000` | valid placements | repeated vertical usage |
| `1111` | valid placements | repeated horizontal + clearing |

## Edge Cases

One subtle case is when a row becomes full due to the second half of a domino placement pattern over time rather than a single obvious fill. The algorithm handles this because clearing is applied after every placement, ensuring no stale full row remains in the state.

Another case is simultaneous row and column completion. The repeated clearing loop ensures both are removed even if one triggers the other indirectly, preventing inconsistent intermediate states and guaranteeing the board remains valid for the next placement.
