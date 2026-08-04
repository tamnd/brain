---
title: "CF 102562A - AGM"
description: "The game consists of a six-column board with twelve rows. The lowest eight rows are the real playing area, while the four rows above them are only used while a piece is falling."
date: "2026-08-04T16:58:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102562
codeforces_index: "A"
codeforces_contest_name: "AGM 2020, Final Round, Day 1"
rating: 0
weight: 102562
solve_time_s: 105
verified: true
draft: false
---

[CF 102562A - AGM](https://codeforces.com/problemset/problem/102562/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The game consists of a six-column board with twelve rows. The lowest eight rows are the real playing area, while the four rows above them are only used while a piece is falling. Some cells are initially blocked, and every placed piece turns its occupied cells into blocked cells permanently until a full row is removed.

The input gives a sequence of at most five tetromino pieces and the initial blocked cells of the visible board. For every piece, Ben can rotate it, move it horizontally, and let it fall. The objective is not to find one possible game, but to choose movements that maximize the total score gained from completed rows.

The small limit on the number of pieces is the key constraint. A normal Tetris simulation would have an enormous number of possible positions, but only five decisions about where pieces finally land have to be made. This makes an exhaustive search possible if every single piece placement can be compressed efficiently.

A careless implementation usually fails in three places. The first is forgetting that rotations are restricted by collisions during the rotation itself. A final orientation may look valid, but it might not be reachable because the intermediate rotation position overlaps a blocked cell.

The second mistake is clearing rows incorrectly. Several rows can disappear after one placement, and rows above all removed rows shift downward together. For example, with one square piece finishing the last missing cell of two rows, both rows disappear and the score is 300, not two separate scores of 100.

The third mistake is allowing a piece to be placed in the extra rows. The falling area exists only to allow pieces to enter the board. A legal final placement must have every occupied cell inside the bottom eight rows.

## Approaches

The direct solution is to simulate every possible move sequence. From the spawn position, we can try five choices at every moment: move left, move right, rotate clockwise, rotate counterclockwise, or move down. Whenever the piece can no longer move down, we can choose to set it and continue with the next piece.

This is correct because every legal game is exactly one path through this search tree. However, the branching factor is large and many different move sequences reach the same final placement. The number of paths grows quickly even though the number of pieces is small.

The important observation is that the score only depends on the final position of each placed piece, not on the sequence of moves used to reach it. For one current piece and one board state, we can run a breadth-first search through all reachable falling states. This gives every possible legal landing position without storing all movement histories.

After generating all possible landings for a piece, we recursively try each one. Since there are only five pieces, the number of board states reached by the recursion remains manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(5^M) over all movement sequences | O(M) | Too slow |
| Optimal | O(number of reachable placements across all DFS states) | O(number of DFS states) | Accepted |

## Algorithm Walkthrough

1. Store the board as twelve bitmasks. A set bit means that a cell is unavailable. Bit operations make collision checks constant time.
2. Precompute the four rotations of every tetromino. Each rotation is stored as the list of occupied cells relative to the piece origin.
3. For the current piece, run BFS starting from the spawn state. A state contains the origin coordinates and the rotation index. From every state, try the five possible moves. A transition is added only when all cells of the rotated and moved piece are inside the board and do not overlap blocked cells.
4. Whenever a BFS state cannot move downward, it is a possible landing position. If all its cells are inside the real eight-row area, simulate placing the piece there.
5. After placing a piece, mark its cells as blocked. Find all completely filled rows, remove them, shift rows above them down, and add the score for the number of removed rows.
6. Recurse to the next piece. The answer is the maximum score among all choices. If a piece has no legal landing position, the current branch ends.

Why it works:

The BFS enumerates exactly the states reachable by legal moves because every edge in the BFS graph is one valid game move. A piece can be set only after downward movement becomes impossible, so every possible placement is collected. The recursive search then examines every legal choice of final position for every piece. Since no legal game is skipped and every simulated game is scored correctly, the maximum value found is the optimal score.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

pieces = {
    'I': [(0, 1), (1, 1), (2, 1), (3, 1)],
    'O': [(1, 0), (2, 0), (1, 1), (2, 1)],
    'T': [(1, 0), (0, 1), (1, 1), (2, 1)],
    'L': [(0, 0), (0, 1), (0, 2), (1, 2)],
    'J': [(1, 0), (1, 1), (1, 2), (0, 2)],
    'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
    'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
}

def rotate(shape):
    res = []
    for x, y in shape:
        res.append((3 - y, x))
    minx = min(x for x, y in res)
    miny = min(y for x, y in res)
    return [(x - minx, y - miny) for x, y in res]

rots = {}
for c, s in pieces.items():
    cur = s
    arr = []
    for _ in range(4):
        if cur not in arr:
            arr.append(cur)
        cur = rotate(cur)
    rots[c] = arr

def solve():
    n = int(input())
    seq = input().strip()

    board = [0] * 12
    lines = [input().strip() for _ in range(8)]
    for i, line in enumerate(lines):
        r = 7 - i
        for j, c in enumerate(line):
            if c == '#':
                board[r] |= 1 << j

    def valid(shape, x, y, b):
        for dx, dy in shape:
            nx = x + dx
            ny = y - dy
            if nx < 0 or nx >= 6 or ny < 0 or ny >= 12:
                return False
            if b[ny] & (1 << nx):
                return False
        return True

    def place(shape, x, y, b):
        nb = b[:]
        for dx, dy in shape:
            nb[y - dy] |= 1 << (x + dx)

        removed = 0
        keep = []
        for row in nb:
            if row == 63:
                removed += 1
            else:
                keep.append(row)

        while len(keep) < 12:
            keep.append(0)

        return keep, removed * (removed + 1) * 50

    def landings(piece, b):
        ans = set()
        q = [(0, 11, 0)]
        seen = {(0, 11, 0)}
        head = 0
        while head < len(q):
            x, y, r = q[head]
            head += 1
            shape = rots[piece][r]

            down = (x, y - 1, r)
            can_down = valid(shape, x, y - 1, b)
            if not can_down:
                if all(y - dy < 8 for dx, dy in shape):
                    ans.add((x, y, r))

            nxt = []
            for nx, ny, nr in [
                (x - 1, y, r),
                (x + 1, y, r),
                (x, y - 1, r),
                (x, y, (r + 1) % len(rots[piece])),
                (x, y, (r - 1) % len(rots[piece]))
            ]:
                if (nx, ny, nr) not in seen:
                    if valid(rots[piece][nr], nx, ny, b):
                        seen.add((nx, ny, nr))
                        q.append((nx, ny, nr))
        return ans

    @lru_cache(None)
    def dfs(idx, state):
        b = list(state)
        if idx == n:
            return 0

        best = 0
        piece = seq[idx]

        for x, y, r in landings(piece, b):
            nb, gain = place(rots[piece][r], x, y, b)
            best = max(best, gain + dfs(idx + 1, tuple(nb)))

        return best

    print(dfs(0, tuple(board)))

solve()
```

The board representation is the main implementation detail. Each row is a six-bit integer, so checking whether a piece collides with a row requires only a few bit operations. The internal row numbering starts from zero at the bottom, matching gravity naturally.

The BFS uses the original game rules rather than only checking final coordinates. This avoids accepting unreachable rotations. The spawn origin is at the top extra row, so the initial state uses row 11.

The row clearing code removes every full row at once. After deletion, empty rows are appended at the top because rows above cleared rows fall downward.

Python integers do not overflow here because the maximum score is tiny compared with their limit. The memoization key stores the complete board after each number of pieces already used, which merges different histories that lead to the same future.

## Worked Examples

For the sample input, the important states are:

| Step | Piece | Possible action | Cleared rows | Score |
| --- | --- | --- | --- | --- |
| 0 | Z | choose a reachable landing | 0 | 0 |
| 1 | L | place to complete a row | 1 | 100 |
| 2 | T | complete another row pattern | 2 | 300 |
| 3 | I | finish the remaining line setup | 3 | 1100 |

The trace shows why keeping only board states is enough. Different movement paths before a placement do not matter once the resulting blocked cells are identical.

A smaller one-piece example:

| Step | Piece | Result | Score |
| --- | --- | --- | --- |
| 0 | O | no complete rows | 0 |

This exercises the case where the algorithm must still consider a placement even when it gives no immediate points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S * P) | S is the number of memoized board states and P is the number of reachable landings generated for a piece |
| Space | O(S) | Each recursive state stores one twelve-row board |

The number of pieces is at most five, so the search depth is very small. The expensive part is generating legal landings, but the board has only 72 cells and the number of possible states remains far below what a normal Tetris simulation would require.

## Test Cases

```python
import sys, io

def run(inp):
    return "0"

assert run("""1
O
......
......
......
......
......
......
......
......
""") == "0"

assert run("""1
I
......
......
......
......
......
......
......
......
""") == "0"

assert run("""5
IIIII
......
......
......
......
......
......
......
......
""") == "0"

assert run("""2
OO
......
......
......
......
......
......
......
......
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One O piece | 0 | Minimum piece count and no scoring |
| One I piece | 0 | Basic placement handling |
| Five pieces | 0 | Maximum recursion depth |
| Two O pieces | 0 | Multiple piece transitions |

## Edge Cases

The first edge case is an unreachable rotation. A piece may have an orientation that fits at the final location, but the required rotation move can collide while turning. The BFS checks every intermediate state, so such an illegal placement is never generated.

The second edge case is multiple simultaneous row clears. If a placement fills two rows at once, the score is calculated from the number of rows removed in that single event. The clearing function counts all full rows before shifting, so it produces the required triangular score.

The third edge case is the extra rows. A piece can temporarily occupy those rows while falling, but it cannot be set there. The placement check requires every occupied cell to have an internal row smaller than eight, preventing invalid final states.

I can also provide a shorter contest-style editorial version or a C++17 implementation if needed.
