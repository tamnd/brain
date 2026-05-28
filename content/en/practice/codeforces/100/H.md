---
title: "CF 100H - Battleship"
description: "We are given several 10 × 10 Battleship boards. Each cell is either empty or occupied by part of a ship. The task is to verify whether every occupied cell belongs to a valid fleet configuration."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dfs-and-similar", "implementation"]
categories: ["algorithms"]
codeforces_contest: 100
codeforces_index: "H"
codeforces_contest_name: "Unknown Language Round 3"
rating: 2100
weight: 100
solve_time_s: 184
verified: true
draft: false
---

[CF 100H - Battleship](https://codeforces.com/problemset/problem/100/H)

**Rating:** 2100  
**Tags:** *special, dfs and similar, implementation  
**Solve time:** 3m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several 10 × 10 Battleship boards. Each cell is either empty or occupied by part of a ship. The task is to verify whether every occupied cell belongs to a valid fleet configuration.

A valid Battleship fleet contains exactly one ship of length 4, two ships of length 3, three ships of length 2, and four ships of length 1. Every ship must be a straight horizontal or vertical segment. Ships cannot overlap, cannot bend, and cannot touch each other, even diagonally.

The board is tiny, only 100 cells. Even with up to 10 boards, we only process at most 1000 cells total. This immediately rules out performance as the main challenge. The difficulty is purely in validating all geometric conditions correctly.

The most dangerous mistakes come from accepting invalid ship shapes or forgetting diagonal adjacency checks.

Consider this board fragment:

```
**00000000
*000000000
0000000000
```

The three occupied cells form an L-shape. A careless DFS that only counts connected components would see a component of size 3 and might incorrectly classify it as a valid ship of length 3. The correct answer is NO because ships must be straight.

Another common pitfall is diagonal touching:

```
*000000000
0*00000000
0000000000
```

These are two single-cell ships touching diagonally. Battleship rules forbid this, so the board is invalid. Solutions that only check 4-direction adjacency will miss this.

A third subtle case is merged ships:

```
***0000000
00*0000000
0000000000
```

The vertical cell touches the horizontal ship orthogonally, creating a bent component. The board must be rejected immediately.

The final class of bugs comes from ship counting. Even if every connected component is a straight line, the fleet composition must exactly match the required counts. For example, having two ships of length 4 and no ships of length 3 is invalid.

## Approaches

The brute-force idea is straightforward. We can try to identify every possible ship placement independently and remove matched ships from the board. Since the board is only 10 × 10, even fairly clumsy enumeration would still run quickly.

One naive strategy is to repeatedly scan the board for horizontal or vertical segments, mark them as ships, and hope the remaining cells also form valid ships. The problem is ambiguity. A malformed shape can accidentally be decomposed into multiple legal ships. For example, an L-shape could be interpreted as a length-2 ship plus a single-cell ship, even though the component itself is invalid.

The correct way to think about the board is as a graph problem. Every occupied cell belongs to exactly one connected component under 4-direction adjacency. Since ships cannot touch orthogonally, each connected component must correspond to exactly one ship.

This observation simplifies everything:

1. Run DFS or BFS on every unvisited occupied cell.
2. Extract the entire connected component.
3. Verify that all cells lie on one row or one column.
4. Verify that the cells form a continuous segment.
5. Verify that no cell touches another ship diagonally.
6. Count the ship length.

Because the board has only 100 cells, DFS over the entire board is effectively constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100³) | O(100) | Accepted but awkward |
| Optimal | O(100) | O(100) | Accepted |

## Algorithm Walkthrough

1. Read the 10 × 10 board into a grid.
2. Maintain a visited array so each occupied cell is processed exactly once.
3. Iterate through every cell of the board.
4. When an unvisited `'*'` cell is found, start a DFS or BFS from it to collect its entire connected component using only 4-direction movement.

Using 4 directions is correct because ships connect only horizontally or vertically. Diagonal cells must never belong to the same ship.
5. For every cell inside the component, check all four diagonal neighbors.

If any diagonal neighbor contains `'*'`, the board is immediately invalid because ships are not allowed to touch diagonally.
6. After collecting the component, validate its shape.

If the component has size 1, it is automatically a valid single-cell ship.

Otherwise, either:

- all cells must share the same row, or
- all cells must share the same column.

If neither condition holds, the ship bends and the board is invalid.
7. Check continuity.

For a horizontal ship, sort the column indices and verify they form consecutive integers.

For a vertical ship, sort the row indices and verify they form consecutive integers.

This prevents disconnected shapes like:

```
*0*
```
8. Record the ship length.
9. After processing all components, verify the exact fleet composition:

- one ship of size 4,
- two ships of size 3,
- three ships of size 2,
- four ships of size 1.
10. Print YES if all checks succeed, otherwise print NO.

### Why it works

Every occupied cell belongs to exactly one connected component under 4-direction adjacency. Because ships cannot overlap or touch orthogonally, each component must represent a single ship.

The algorithm validates every necessary property of a legal ship:

- diagonal checks prevent touching ships,
- row/column alignment prevents bends,
- continuity checks prevent gaps,
- fleet counting enforces the exact required ship inventory.

Since every component is checked independently and every occupied cell is processed exactly once, no invalid configuration can escape detection.

## Python Solution

```python
import sys
input = sys.stdin.readline

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAG = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def solve_board(grid):
    visited = [[False] * 10 for _ in range(10)]
    counts = [0] * 5

    def inside(r, c):
        return 0 <= r < 10 and 0 <= c < 10

    def dfs(sr, sc):
        stack = [(sr, sc)]
        visited[sr][sc] = True
        cells = []

        while stack:
            r, c = stack.pop()
            cells.append((r, c))

            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc

                if inside(nr, nc) and not visited[nr][nc] and grid[nr][nc] == '*':
                    visited[nr][nc] = True
                    stack.append((nr, nc))

        return cells

    for r in range(10):
        for c in range(10):
            if grid[r][c] == '*' and not visited[r][c]:
                cells = dfs(r, c)

                # diagonal touching check
                for x, y in cells:
                    for dx, dy in DIAG:
                        nx, ny = x + dx, y + dy

                        if inside(nx, ny) and grid[nx][ny] == '*':
                            return False

                size = len(cells)

                if size > 4:
                    return False

                rows = set(x for x, _ in cells)
                cols = set(y for _, y in cells)

                if len(rows) != 1 and len(cols) != 1:
                    return False

                if len(rows) == 1:
                    vals = sorted(y for _, y in cells)
                else:
                    vals = sorted(x for x, _ in cells)

                for i in range(1, len(vals)):
                    if vals[i] != vals[i - 1] + 1:
                        return False

                counts[size] += 1

    return counts[1] == 4 and counts[2] == 3 and counts[3] == 2 and counts[4] == 1

def main():
    t = int(input())
    ans = []

    for _ in range(t):
        grid = []

        while len(grid) < 10:
            line = input().strip()

            if line:
                grid.append(line)

        ans.append("YES" if solve_board(grid) else "NO")

    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The solution separates validation into independent checks, which makes debugging much easier.

The DFS collects exactly one connected component at a time. Because we only move in four directions, diagonally touching ships remain separate components, which is exactly what we want.

The diagonal validation is intentionally performed after component extraction. At that point we already know which cells belong to the current ship, so any diagonal `'*'` must belong to another ship and immediately violates the rules.

The row and column set checks are the core shape validation. If both sets have size larger than one, the component bends. This catches all L-shapes and T-shapes.

The continuity check is subtle but necessary. A component like:

```
*0*
```

cannot appear under valid 4-direction connectivity, but checking continuity still makes the logic robust and self-contained.

The final fleet count verification guarantees the exact Battleship inventory. Even perfectly shaped ships are rejected if the counts do not match the official rules.

## Worked Examples

### Sample 1

Input board:

```
****000000
0000000000
***00***00
0000000000
00000000**
000**00000
00000000**
000*000000
00000*00*0
0*00000000
```

Trace of detected ships:

| Component Cells | Shape | Length | Valid |
| --- | --- | --- | --- |
| (0,0)-(0,3) | Horizontal | 4 | Yes |
| (2,0)-(2,2) | Horizontal | 3 | Yes |
| (2,5)-(2,7) | Horizontal | 3 | Yes |
| (4,8)-(4,9) | Horizontal | 2 | Yes |
| (5,3)-(5,4) | Horizontal | 2 | Yes |
| (6,8)-(6,9) | Horizontal | 2 | Yes |
| (7,3) | Single | 1 | Yes |
| (8,5) | Single | 1 | Yes |
| (8,8) | Single | 1 | Yes |
| (9,1) | Single | 1 | Yes |

Final counts:

| Ship Size | Required | Found |
| --- | --- | --- |
| 1 | 4 | 4 |
| 2 | 3 | 3 |
| 3 | 2 | 2 |
| 4 | 1 | 1 |

The board satisfies all geometric constraints and all fleet counts, so the answer is YES.

### Invalid Example

```
**00000000
*000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

Trace:

| Component Cells | Shape | Result |
| --- | --- | --- |
| (0,0), (0,1), (1,0) | L-shape | Invalid |

The component spans multiple rows and multiple columns, so it is not a straight ship. The algorithm immediately rejects the board.

This example demonstrates why counting connected component sizes alone is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(100) | Each cell is visited at most once |
| Space | O(100) | Visited array and DFS stack |

The board size is fixed at 10 × 10, so the running time is effectively constant. Even with 10 test cases, the total work is tiny compared to the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    DIAG = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def solve_board(grid):
        visited = [[False] * 10 for _ in range(10)]
        counts = [0] * 5

        def inside(r, c):
            return 0 <= r < 10 and 0 <= c < 10

        def dfs(sr, sc):
            stack = [(sr, sc)]
            visited[sr][sc] = True
            cells = []

            while stack:
                r, c = stack.pop()
                cells.append((r, c))

                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc

                    if inside(nr, nc) and not visited[nr][nc] and grid[nr][nc] == '*':
                        visited[nr][nc] = True
                        stack.append((nr, nc))

            return cells

        for r in range(10):
            for c in range(10):
                if grid[r][c] == '*' and not visited[r][c]:
                    cells = dfs(r, c)

                    for x, y in cells:
                        for dx, dy in DIAG:
                            nx, ny = x + dx, y + dy

                            if inside(nx, ny) and grid[nx][ny] == '*':
                                return False

                    size = len(cells)

                    if size > 4:
                        return False

                    rows = set(x for x, _ in cells)
                    cols = set(y for _, y in cells)

                    if len(rows) != 1 and len(cols) != 1:
                        return False

                    if len(rows) == 1:
                        vals = sorted(y for _, y in cells)
                    else:
                        vals = sorted(x for x, _ in cells)

                    for i in range(1, len(vals)):
                        if vals[i] != vals[i - 1] + 1:
                            return False

                    counts[size] += 1

        return counts[1] == 4 and counts[2] == 3 and counts[3] == 2 and counts[4] == 1

    t = int(input())
    out = []

    for _ in range(t):
        grid = []

        while len(grid) < 10:
            line = input().strip()

            if line:
                grid.append(line)

        out.append("YES" if solve_board(grid) else "NO")

    return "\n".join(out)

# provided samples
assert solve(
"""2
****000000
0000000000
***00***00
0000000000
00000000**
000**00000
00000000**
000*000000
00000*00*0
0*00000000

****000000
0000000000
***00***00
0000000000
00000000**
000**00000
00000000**
0000*00000
00000*00*0
0*00000000
"""
) == "YES\nNO"

# diagonal touching
assert solve(
"""1
*000000000
0*00000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
"""
) == "NO"

# bent ship
assert solve(
"""1
**00000000
*000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
"""
) == "NO"

# too many large ships
assert solve(
"""1
****0****0
0000000000
***00***00
0000000000
00000000**
000**00000
00000000**
000*000000
00000*00*0
0*00000000
"""
) == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | YES / NO | Basic correctness |
| Diagonal touching | NO | Detects forbidden diagonal adjacency |
| Bent ship | NO | Rejects non-linear components |
| Extra size-4 ship | NO | Verifies exact fleet counts |

## Edge Cases

### Diagonal Touching

Input:

```
1
*000000000
0*00000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

The DFS finds two separate single-cell components. During diagonal validation, the cell `(0,0)` detects another `'*'` at `(1,1)`. The algorithm immediately returns NO.

This case confirms that diagonal neighbors are checked independently from component construction.

### Bent Ship

Input:

```
1
**00000000
*000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

The DFS collects the component:

```
(0,0), (0,1), (1,0)
```

The set of rows is `{0,1}` and the set of columns is `{0,1}`. Since both dimensions vary, the component is not a straight line. The algorithm rejects the board.

This prevents accidental acceptance of L-shaped ships.

### Incorrect Fleet Composition

Input:

```
1
****0****0
0000000000
***00***00
0000000000
00000000**
000**00000
00000000**
000*000000
00000*00*0
0*00000000
```

Every component is individually valid, but the final counts become:

| Ship Size | Found |
| --- | --- |
| 1 | 4 |
| 2 | 3 |
| 3 | 2 |
| 4 | 2 |

The required number of length-4 ships is exactly one, so the board is invalid.

This confirms that geometry alone is insufficient, the fleet inventory must also match exactly.
