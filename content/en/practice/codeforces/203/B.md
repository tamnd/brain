---
title: "CF 203B - Game on Paper"
description: "We have an n × n grid that starts completely white. Cells are painted black one by one, and every move paints a different cell. After each move, we want to know whether the board already contains a completely black 3 × 3 square."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 203
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 128 (Div. 2)"
rating: 1300
weight: 203
solve_time_s: 101
verified: true
draft: false
---

[CF 203B - Game on Paper](https://codeforces.com/problemset/problem/203/B)

**Rating:** 1300  
**Tags:** brute force, implementation  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n × n` grid that starts completely white. Cells are painted black one by one, and every move paints a different cell. After each move, we want to know whether the board already contains a completely black `3 × 3` square.

The task is to output the earliest move index where such a square first appears. If no `3 × 3` block ever becomes fully black, we print `-1`.

The grid size is at most `1000 × 1000`, which means the board contains at most one million cells. The number of painting operations is at most `10^5`. That immediately rules out any approach that repeatedly scans the entire board after every move. Rechecking all possible `3 × 3` squares every time would take roughly:

$$10^5 \times 10^6 = 10^{11}$$

operations in the worst case, which is far beyond the limit.

The small fixed square size is the key detail here. We are not searching for arbitrary rectangles or large patterns. Every valid configuration is exactly `3 × 3`, so each newly painted cell can only affect a tiny number of candidate squares nearby.

There are a few easy-to-miss edge cases.

Suppose the board is too small to even contain a `3 × 3` square.

Input:

```
2 4
1 1
1 2
2 1
2 2
```

Correct output:

```
-1
```

A careless implementation might still try to check neighboring positions and accidentally access invalid indices.

Another subtle case appears when the final painted cell is not the top-left corner of the completed square.

Input:

```
3 9
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
3 3
```

Correct output:

```
9
```

If we only check squares whose top-left corner equals the newly painted cell, we miss this completely. The last move is `(3,3)`, but the relevant `3 × 3` square starts at `(1,1)`.

There is also the situation where several `3 × 3` squares overlap.

Input:

```
4 10
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
4 1
3 3
```

Correct output:

```
10
```

The algorithm must stop at the first moment any valid square exists, not after processing all moves.

## Approaches

The most direct solution is brute force. After every move, we scan every possible `3 × 3` subgrid and check whether all nine cells are black.

There are `(n - 2)^2` candidate squares, and each check examines 9 cells. The complexity becomes:

$$O(m \cdot n^2)$$

For `n = 1000` and `m = 10^5`, this becomes far too large.

The important observation is that painting one cell only changes squares that contain that cell. Since the target square size is fixed at `3 × 3`, a single cell belongs to at most 9 different `3 × 3` squares.

For example, if we paint cell `(x, y)`, then the top-left corner of any affected `3 × 3` square must lie in:

$$(x-2 \dots x,\ y-2 \dots y)$$

There are only 9 possibilities. Every other square on the board remains unchanged and does not need to be checked again.

This transforms the problem from repeatedly scanning the entire grid into checking only a constant number of local configurations after each move.

The resulting complexity becomes linear in the number of moves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m · n²) | O(n²) | Too slow |
| Optimal | O(m) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Create an `n × n` boolean grid initialized to `False`.

Each cell stores whether it has already been painted black.
2. Process the moves one by one in input order.

The first move that creates a valid `3 × 3` square is the answer, so we must evaluate moves sequentially.
3. Mark the current cell `(x, y)` as black.
4. Enumerate all possible top-left corners of `3 × 3` squares that could contain `(x, y)`.

These corners are:

```
(x-2, y-2) ... (x, y)
```

There are at most 9 candidates.
5. For each candidate top-left corner `(r, c)`, first verify that the square stays inside the board.

We need:

```
0 ≤ r ≤ n-3
0 ≤ c ≤ n-3
```
6. Check all 9 cells inside that `3 × 3` square.

If every cell is black, immediately print the current move number and terminate.
7. If all moves finish without finding a valid square, print `-1`.

### Why it works

A `3 × 3` square can only change status when one of its cells is painted. Before painting `(x, y)`, every unaffected square has exactly the same cells as before, so its validity cannot change.

That means after a move, the only squares worth checking are the ones containing the newly painted cell. Since every such square is examined explicitly, the algorithm cannot miss the first completed `3 × 3` block.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())

    grid = [[False] * n for _ in range(n)]

    for move in range(1, m + 1):
        x, y = map(int, input().split())
        x -= 1
        y -= 1

        grid[x][y] = True

        for r in range(x - 2, x + 1):
            for c in range(y - 2, y + 1):

                if r < 0 or c < 0 or r + 2 >= n or c + 2 >= n:
                    continue

                ok = True

                for i in range(r, r + 3):
                    for j in range(c, c + 3):
                        if not grid[i][j]:
                            ok = False
                            break

                    if not ok:
                        break

                if ok:
                    print(move)
                    return

    print(-1)

if __name__ == "__main__":
    main()
```

The solution stores the board as a boolean matrix. Using booleans keeps the implementation simple and efficient because each lookup becomes a direct array access.

Coordinates are converted to zero-based indexing immediately after reading input. This avoids repeated `-1` adjustments later and makes boundary conditions easier to reason about.

The loops:

```
for r in range(x - 2, x + 1):
    for c in range(y - 2, y + 1):
```

enumerate every possible `3 × 3` square containing `(x, y)`. A common mistake is checking only `(x, y)` as the top-left corner, which misses many valid configurations.

The boundary test:

```
if r < 0 or c < 0 or r + 2 >= n or c + 2 >= n:
```

prevents invalid indexing near the edges of the board.

The nested loops over the `3 × 3` region stop early as soon as one white cell is found. This keeps the constant factor small.

The moment a valid square appears, the program prints the move index and exits immediately. Since moves are processed in chronological order, the first detected square is guaranteed to be the earliest one.

## Worked Examples

### Example 1

Input:

```
4 11
1 1
1 2
1 3
2 2
2 3
1 4
2 4
3 4
3 2
3 3
4 1
```

Trace:

| Move | Painted Cell | Completed 3×3 Exists? |
| --- | --- | --- |
| 1 | (1,1) | No |
| 2 | (1,2) | No |
| 3 | (1,3) | No |
| 4 | (2,2) | No |
| 5 | (2,3) | No |
| 6 | (1,4) | No |
| 7 | (2,4) | No |
| 8 | (3,4) | No |
| 9 | (3,2) | No |
| 10 | (3,3) | Yes |
| 11 | not processed | already terminated |

At move 10, the cells:

```
(1,2) (1,3) (1,4)
(2,2) (2,3) (2,4)
(3,2) (3,3) (3,4)
```

form a complete `3 × 3` square.

This example demonstrates why checking only around the latest painted cell is enough. The newly painted cell `(3,3)` belongs to the finished square, so the algorithm detects it immediately.

### Example 2

Input:

```
3 8
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
```

Trace:

| Move | Painted Cell | Completed 3×3 Exists? |
| --- | --- | --- |
| 1 | (1,1) | No |
| 2 | (1,2) | No |
| 3 | (1,3) | No |
| 4 | (2,1) | No |
| 5 | (2,2) | No |
| 6 | (2,3) | No |
| 7 | (3,1) | No |
| 8 | (3,2) | No |

Cell `(3,3)` is never painted, so the only possible `3 × 3` square remains incomplete.

Output:

```
-1
```

This trace confirms that the algorithm does not produce false positives when a square is almost complete.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each move checks at most 9 candidate squares, each containing 9 cells |
| Space | O(n²) | The board state is stored explicitly |

The maximum work per move is bounded by a small constant. Even for `10^5` moves, the total number of cell checks remains comfortably within the time limit. The memory usage is also safe because a `1000 × 1000` boolean grid fits easily inside 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    grid = [[False] * n for _ in range(n)]

    for move in range(1, m + 1):
        x, y = map(int, input().split())
        x -= 1
        y -= 1

        grid[x][y] = True

        for r in range(x - 2, x + 1):
            for c in range(y - 2, y + 1):

                if r < 0 or c < 0 or r + 2 >= n or c + 2 >= n:
                    continue

                ok = True

                for i in range(r, r + 3):
                    for j in range(c, c + 3):
                        if not grid[i][j]:
                            ok = False
                            break

                    if not ok:
                        break

                if ok:
                    print(move)
                    return

    print(-1)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""4 11
1 1
1 2
1 3
2 2
2 3
1 4
2 4
3 4
3 2
3 3
4 1
"""
) == "10\n", "sample 1"

# minimum board size
assert run(
"""1 1
1 1
"""
) == "-1\n", "1x1 board cannot contain 3x3"

# exact 3x3 completion
assert run(
"""3 9
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
3 3
"""
) == "9\n", "entire board becomes black"

# incomplete square
assert run(
"""3 8
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
"""
) == "-1\n", "one missing cell"

# edge-aligned square
assert run(
"""5 9
3 3
3 4
3 5
4 3
4 4
4 5
5 3
5 4
5 5
"""
) == "9\n", "square touching lower-right boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` board | `-1` | No possible `3 × 3` square |
| Full `3×3` board | `9` | Correct detection timing |
| One missing cell | `-1` | No false positives |
| Boundary-aligned square | `9` | Correct edge handling |

## Edge Cases

Consider the smallest possible board.

Input:

```
2 4
1 1
1 2
2 1
2 2
```

A `3 × 3` square cannot exist on a `2 × 2` board. During every move, candidate top-left positions fail the boundary check:

```
r + 2 >= n
```

so no square is tested. The algorithm correctly prints:

```
-1
```

Now consider the case where the final painted cell is not the top-left corner.

Input:

```
3 9
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
3 3
```

At move 9, the painted cell is `(3,3)`. The algorithm checks all candidate top-left corners from `(1,1)` to `(3,3)` in zero-based coordinates. The valid square starting at `(1,1)` is examined and found fully black.

This confirms why checking all nearby top-left corners is necessary.

Finally, consider a square touching the border.

Input:

```
5 9
3 3
3 4
3 5
4 3
4 4
4 5
5 3
5 4
5 5
```

The completed square occupies the bottom-right corner of the board. The valid top-left corner is `(3,3)` in one-based indexing. The boundary condition allows this square because:

```
r + 2 = 4
c + 2 = 4
```

which still lies inside a `5 × 5` grid using zero-based indexing. The algorithm correctly outputs:

```
9
```
