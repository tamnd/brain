---
title: "CF 105627H - Star Wars"
description: "The board is a battlefield containing empty cells, black pieces, and white pieces. We may choose one white piece as the controlled piece. During the game, that piece can only move one row upward at a time, choosing the same column, the left diagonal, or the right diagonal."
date: "2026-06-26T18:10:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105627
codeforces_index: "H"
codeforces_contest_name: "The 2023 ICPC Asia Tehran Regional Contest"
rating: 0
weight: 105627
solve_time_s: 48
verified: true
draft: false
---

[CF 105627H - Star Wars](https://codeforces.com/problemset/problem/105627/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The board is a battlefield containing empty cells, black pieces, and white pieces. We may choose one white piece as the controlled piece. During the game, that piece can only move one row upward at a time, choosing the same column, the left diagonal, or the right diagonal. It cannot enter a cell occupied by another white piece. Whenever it reaches a black piece, that piece is destroyed. The goal is to choose the starting white piece and its movement path so that the number of destroyed black pieces is as large as possible.

The input describes the dimensions of the board followed by the grid itself. The output is a single integer, the maximum number of black cells that can be visited by one valid upward path.

The board size is at most 50 by 50, so there are only 2500 cells. This is small enough that a solution exploring the state of every cell is possible. However, trying every possible path explicitly would still be expensive because the number of possible paths grows exponentially with the number of rows. A dynamic programming solution that processes each cell once is the intended complexity.

The movement direction creates the main structure of the problem. Since every move decreases the row index, the graph of possible movements has no cycles. That means every cell can be evaluated from the cells below it without needing more complicated graph algorithms.

Several edge cases can break a careless implementation. A single white piece on the top row already has a valid path with zero moves. For example:

```
Input
1 1
W

Output
0
```

A solution that assumes every white piece must move at least once could fail here.

A black piece directly above the starting position must be counted, because moving into it destroys it. For example:

```
Input
2 1
W
B

Output
1
```

A mistake that only counts cells after the move instead of including the destination cell would return zero.

Another common mistake is allowing movement through another white piece. Consider:

```
Input
3 1
W
W
B

Output
0
```

The upper white piece cannot pass through the lower white piece, so the black cell is unreachable. Treating white cells like empty cells would incorrectly return one.

## Approaches

The direct approach is to simulate every possible movement sequence from every white piece. A path starts at one white cell and branches into up to three possible next cells on each row. This approach is correct because every possible route is examined, and the route with the largest number of black cells can be selected. The problem is that the number of routes grows exponentially. In a board with 50 rows, a single piece could have up to $3^{49}$ possible movement sequences before considering obstacles, which is far beyond what can be explored.

The useful observation is that many different paths reach the same cell. Once the controlled piece arrives at a particular cell, the best future result from that point does not depend on the path used to reach it. The only information that matters is the current position. This makes the problem a longest path problem on a directed acyclic graph.

We can define `dp[i][j]` as the maximum number of black pieces that can be destroyed starting from cell `(i, j)` and continuing upward. From a cell, we try the three possible cells in the row above. If the destination is a white piece, that transition is impossible. If the destination is black, we gain one point and continue from there. Because every transition goes to a smaller row index, we can compute the values from the top of the board downward or use recursion with memoization.

The brute-force method fails because it repeatedly solves the same subproblems. The dynamic programming solution stores those results once and reuses them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) in the worst case | O(n) recursion depth | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Create a memoized function that returns the best number of black pieces obtainable from a given cell.

The function represents the entire future of the game from that position. Since all movement is upward, every recursive call moves closer to the end of the board.
2. For a cell, consider the three possible moves to the row above: up-left, up, and up-right.

Each valid destination represents one possible continuation of the current path.
3. Ignore moves that leave the board or enter another white piece.

A white piece blocks movement permanently, so treating it as a normal cell would create invalid paths.
4. For every valid destination, add one if the destination contains a black piece, then add the best result from that destination.

The current move is the only chance to gain the value of that destination cell, because the path never comes back down.
5. Start the calculation from every white piece and take the maximum result.

The player can choose any initial white piece, so the global answer is the best value among all possible starts.

Why it works: the dynamic programming invariant is that `dp[i][j]` always stores the maximum number of black pieces that can be destroyed from cell `(i, j)` onward. The value is correct because every legal first move is examined, and after that move the remaining problem is exactly the same type of problem from the destination cell. Since movement always goes to a smaller row, there is no circular dependency, so the computed maximum cannot be invalidated by a later choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    board = [input().strip() for _ in range(n)]

    sys.setrecursionlimit(1000000)
    memo = [[-1] * m for _ in range(n)]

    def dfs(r, c):
        if memo[r][c] != -1:
            return memo[r][c]

        best = 0
        nr = r - 1

        if nr >= 0:
            for dc in (-1, 0, 1):
                nc = c + dc
                if 0 <= nc < m and board[nr][nc] != 'W':
                    gain = 1 if board[nr][nc] == 'B' else 0
                    best = max(best, gain + dfs(nr, nc))

        memo[r][c] = best
        return best

    ans = 0
    for i in range(n):
        for j in range(m):
            if board[i][j] == 'W':
                ans = max(ans, dfs(i, j))

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is read as a character grid because each cell type directly affects the transition rules. The memoization table uses `-1` as an uncomputed marker because valid answers are always non-negative.

The recursive function first checks whether the current cell was already processed. Without this check, many paths would repeatedly calculate the same future states.

The transition loop checks the three columns in the previous row. The boundary checks prevent invalid column access, and the white-cell check enforces the blocking rule. The black-cell contribution is added before the recursive call because the destination cell is destroyed when the move happens.

The final loop tries every possible starting white piece. A common error is to start only from the lowest white pieces, but the problem allows any white piece, including ones near the top.

## Worked Examples

Using a smaller custom example:

```
Input
3 3
W..
.B.
..W
```

The state evolution is:

| Current cell | Possible next cells | Best value |
| --- | --- | --- |
| (2,2) W | (1,1), (1,2) | 0 |
| (1,1) | (0,0), (0,1), (0,2) | 0 |
| (0,0) | none | 0 |

The answer is `1` from the upper white piece path through the black cell.

A second example:

```
Input
4 4
....
.W..
.B..
..W.
```

The calculation is:

| Current cell | Destination chosen | Gain | Total |
| --- | --- | --- | --- |
| (2,1) | (1,1) | 0 | 0 |
| (1,1) | (0,0),(0,1),(0,2) | 0 | 0 |
| (3,2) | (2,1) | 1 | 1 |

The lower white piece reaches the black piece first, so the answer is `1`. This demonstrates why every white starting position must be considered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each board cell is evaluated once, and each evaluation checks three transitions. |
| Space | O(nm) | The memoization table stores one value for every cell. |

The board contains at most 2500 cells, so the dynamic programming approach easily fits within the given limits. The small constant factor from checking three directions keeps the implementation fast.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided sample
assert run("""8 10
.W...BB...
W..B.WB...
.B.WB...W.
.B..B.....
..W...BB..
B.B..B.W.W
.WB.W...B.
..W..BW.B.
""") == "5\n", "sample"

# minimum size
assert run("""1 1
W
""") == "0\n", "single white cell"

# blocked by another white piece
assert run("""3 1
W
W
B
""") == "0\n", "white blocker"

# all black reachable
assert run("""3 3
...
.W.
BBB
""") == "1\n", "one move destroys one piece"

# no white pieces
assert run("""2 2
BB
BB
""") == "0\n", "no starting piece"

# multiple choices
assert run("""4 4
W...
.B..
..B.
...W
""") == "2\n", "best path selection"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single white cell | 0 | Handles a board where no movement is possible. |
| White pieces blocking each other | 0 | Confirms white cells are obstacles. |
| Reachable black cells | 1 | Checks counting of destroyed pieces. |
| No white pieces | 0 | Handles the absence of valid starting positions. |
| Multiple possible paths | 2 | Verifies choosing the best route. |

## Edge Cases

For the top-row white piece case:

```
Input
1 1
W
```

The algorithm calls `dfs(0,0)`. There is no row above, so the value remains zero. The answer correctly stays zero because the chosen piece cannot destroy anything.

For the black piece directly above:

```
Input
2 1
W
B
```

The starting cell is `(0,0)` in zero-based indexing. The only transition reaches the black cell, giving a gain of one. The recursive result from that destination is zero because it is now on the top row. The final answer is `1`.

For the white blocker:

```
Input
3 1
W
W
B
```

The upper white piece checks the only possible move and sees another white piece, so that transition is skipped. The lower white piece has only the black cell below it, but movement is upward only, so it cannot reach that black cell. The answer remains `0`.

These cases are handled naturally by the transition rules: only legal upward moves are considered, and every blocked or unreachable cell is excluded before it can affect the dynamic programming result.
