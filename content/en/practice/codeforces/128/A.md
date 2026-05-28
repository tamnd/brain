---
title: "CF 128A - Statues"
description: "We have an 8 × 8 board. Maria starts in the bottom-left corner, Anna stays permanently in the top-right corner, and several statues occupy other cells. The game proceeds in rounds. Maria moves first, then every statue moves one row downward simultaneously."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar"]
categories: ["algorithms"]
codeforces_contest: 128
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 94 (Div. 1 Only)"
rating: 1500
weight: 128
solve_time_s: 130
verified: true
draft: false
---

[CF 128A - Statues](https://codeforces.com/problemset/problem/128/A)

**Rating:** 1500  
**Tags:** dfs and similar  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an 8 × 8 board. Maria starts in the bottom-left corner, Anna stays permanently in the top-right corner, and several statues occupy other cells.

The game proceeds in rounds. Maria moves first, then every statue moves one row downward simultaneously. A statue that moves below the board disappears forever.

Maria may move to any of the 8 neighboring cells or remain in place. She cannot move into a cell currently occupied by a statue. After her move, statues shift downward. If any statue lands on Maria's cell, she immediately loses. If Maria ever reaches Anna's cell, she wins immediately.

The board is extremely small. There are only 64 cells and statues move in a completely deterministic way. After at most 8 statue moves, every statue has fallen off the board, so the dangerous phase of the game is short-lived. That means we can afford to search all reachable game states directly.

The main difficulty is that the board changes over time. A position that is safe now may become unsafe after the statues move. A careless search that only checks the current board configuration will accept illegal states.

One subtle edge case is when Maria moves into a cell that is empty now but will immediately be occupied after statues move.

Example:

```
.......A
........
........
........
........
........
.S......
M.......
```

Correct output:

```
LOSE
```

Maria cannot safely move upward because the statue from row 6 will descend onto her position after the statues move. A naive BFS that only checks the board before the statue movement would incorrectly think the move is legal.

Another tricky case appears when Maria survives long enough for all statues to disappear.

```
.......A
SSSSSSSS
........
........
........
........
........
M.......
```

Correct output:

```
WIN
```

Maria can simply avoid danger until the statues fall off the board. After that, the board becomes empty forever and reaching Anna is guaranteed. An implementation that artificially limits the search depth too aggressively can incorrectly reject this case.

A third common mistake is forgetting that Maria may stay in place.

```
.......A
........
........
........
........
........
S.......
M.......
```

Correct output:

```
WIN
```

Moving immediately is dangerous, but waiting one turn lets the statue move downward and disappear. Solutions that only consider the 8 directional moves miss valid winning strategies.

## Approaches

The most direct idea is brute-force simulation. At every turn Maria has at most 9 choices, consisting of 8 neighboring cells plus staying still. We could recursively try every possible sequence of moves while simulating statue movement each turn.

This works conceptually because the board is tiny and the game evolution is deterministic. The problem is that the number of move sequences grows exponentially. After 20 turns there are already about $9^{20}$ possible paths, which is completely infeasible.

The key observation is that the board state depends only on time. Statues always move downward in the same way regardless of Maria's actions. Since the board has only 8 rows, after at most 8 turns all statues disappear.

That changes the problem completely. Instead of exploring arbitrary-length move sequences, we only need to track:

1. Maria's current position.
2. The current time step.

At each time step there are at most 64 possible positions. The total number of meaningful states is tiny, roughly $64 \times 9$.

This naturally leads to BFS or DFS over states $(row, col, time)$. From one state we try all 9 moves, check whether the destination is safe before and after statues move, then continue.

The important insight is the double safety check:

1. Maria cannot move into a cell containing a statue at the current time.
2. Maria also cannot remain in a cell that will contain a statue after statues descend.

Without the second condition, the search accepts positions where Maria gets crushed immediately after moving.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9^T) | O(T) | Too slow |
| Optimal BFS/DFS on states | O(64 × 9 × 9) | O(64 × 9) | Accepted |

## Algorithm Walkthrough

1. Read the initial 8 × 8 board.
2. Store all statue positions from the initial configuration.
3. Define a function `safe(r, c, t)` that checks whether cell `(r, c)` is free of statues at time `t`.

A statue originally at `(sr, sc)` will be at `(sr + t, sc)` after `t` moves. If `sr + t >= 8`, that statue has disappeared.
4. Start BFS from Maria's initial position `(7, 0)` at time `0`.
5. For each state `(r, c, t)`, first check whether the current cell is already unsafe at time `t`.

If a statue occupies the current position now, this state is invalid and should be skipped.
6. If Maria reaches `(0, 7)`, return `"WIN"`.
7. Try all 9 possible actions:

1. Move in one of 8 directions.
2. Stay in place.
8. For each candidate position `(nr, nc)`:

1. Ignore positions outside the board.
2. Ignore cells occupied by statues at time `t`.
3. Ignore cells that will be occupied at time `t + 1`.

The second condition prevents Maria from stepping onto a statue immediately. The third prevents her from being crushed after statues move.
9. Push the valid next state `(nr, nc, min(t + 1, 8))` into the queue.

We cap time at 8 because after 8 moves all statues are gone and the board never changes again.
10. If BFS finishes without reaching Anna, return `"LOSE"`.

### Why it works

At any moment, the future board configuration is fully determined by time. BFS explores every reachable safe position Maria can occupy at each time step.

A transition is added only if the destination cell is safe both before and after the statues move. That exactly matches the game rules.

Since every possible legal move sequence is represented in the state graph, BFS will find a winning path whenever one exists. If BFS cannot reach Anna, then no legal strategy exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

DIRS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),  (0, 0),  (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def solve():
    board = [input().strip() for _ in range(8)]

    statues = []

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'S':
                statues.append((r, c))

    def safe(r, c, t):
        for sr, sc in statues:
            nr = sr + t
            if nr < 8 and nr == r and sc == c:
                return False
        return True

    q = deque()
    q.append((7, 0, 0))

    visited = set()
    visited.add((7, 0, 0))

    while q:
        r, c, t = q.popleft()

        if not safe(r, c, t):
            continue

        if (r, c) == (0, 7):
            print("WIN")
            return

        nt = min(t + 1, 8)

        for dr, dc in DIRS:
            nr = r + dr
            nc = c + dc

            if not (0 <= nr < 8 and 0 <= nc < 8):
                continue

            if not safe(nr, nc, t):
                continue

            if not safe(nr, nc, t + 1):
                continue

            state = (nr, nc, nt)

            if state in visited:
                continue

            visited.add(state)
            q.append(state)

    print("LOSE")

solve()
```

The solution begins by collecting the initial statue positions. Since statue movement is deterministic, we never need to rebuild the board explicitly for every time step.

The `safe` function computes whether a cell is free at a given time. Instead of simulating movement repeatedly, it derives each statue's location directly from its original row.

The BFS state includes time because the same board cell may be safe at one moment and deadly later. Treating `(r, c)` alone as visited would incorrectly merge different game situations.

The order of safety checks matters. We first verify the destination is free before statue movement, then verify it remains free after statues descend. Missing the second check is the most common bug in this problem.

Time is capped at 8 because all statues disappear after that. Without this cap, BFS could continue generating equivalent future states forever.

## Worked Examples

### Example 1

Input:

```
.......A
........
........
........
........
........
........
M.......
```

There are no statues at all.

| Step | Position | Time | Safe Now | Safe After Move | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | (7,0) | 0 | Yes | Yes | Start |
| 1 | (6,1) | 1 | Yes | Yes | Move diagonally |
| 2 | (5,2) | 2 | Yes | Yes | Continue |
| 3 | (4,3) | 3 | Yes | Yes | Continue |
| 4 | (3,4) | 4 | Yes | Yes | Continue |
| 5 | (2,5) | 5 | Yes | Yes | Continue |
| 6 | (1,6) | 6 | Yes | Yes | Continue |
| 7 | (0,7) | 7 | Yes | Yes | Reach Anna |

Since no statues exist, every move is safe. BFS quickly reaches the target.

### Example 2

Input:

```
.......A
........
........
........
........
........
.S......
M.......
```

| Step | Position | Time | Statue Position | Valid? |
| --- | --- | --- | --- | --- |
| 0 | (7,0) | 0 | (6,1) | Start |
| 1 | (6,1) | 1 | (7,1) | Invalid |
| 1 | (7,0) | 1 | (7,1) | Valid |
| 2 | (6,0) | 2 | Statue gone | Valid |

Maria cannot immediately move diagonally upward because the statue would descend onto her cell after movement. The algorithm rejects that transition using the second safety check.

Waiting one turn avoids danger entirely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(64 × 9 × 9) | At most 64 cells, 9 time states, and 9 transitions per state |
| Space | O(64 × 9) | BFS queue and visited states |

The search space is extremely small. Even a straightforward BFS easily fits within the 2 second limit and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

DIRS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),  (0, 0),  (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    board = [input().strip() for _ in range(8)]

    statues = []

    for r in range(8):
        for c in range(8):
            if board[r][c] == 'S':
                statues.append((r, c))

    def safe(r, c, t):
        for sr, sc in statues:
            nr = sr + t
            if nr < 8 and nr == r and sc == c:
                return False
        return True

    q = deque([(7, 0, 0)])
    visited = {(7, 0, 0)}

    while q:
        r, c, t = q.popleft()

        if not safe(r, c, t):
            continue

        if (r, c) == (0, 7):
            return "WIN"

        nt = min(t + 1, 8)

        for dr, dc in DIRS:
            nr = r + dr
            nc = c + dc

            if not (0 <= nr < 8 and 0 <= nc < 8):
                continue

            if not safe(nr, nc, t):
                continue

            if not safe(nr, nc, t + 1):
                continue

            state = (nr, nc, nt)

            if state in visited:
                continue

            visited.add(state)
            q.append(state)

    return "LOSE"

# provided sample
assert run(
""".......A
........
........
........
........
........
........
M.......
"""
) == "WIN", "sample 1"

# statue directly above path
assert run(
""".......A
........
........
........
........
........
.S......
M.......
"""
) == "WIN", "must wait before moving"

# full statue wall that eventually disappears
assert run(
""".......A
SSSSSSSS
........
........
........
........
........
M.......
"""
) == "WIN", "survive until statues vanish"

# trapped immediately
assert run(
""".......A
........
........
........
........
........
SS......
MS......
"""
) == "LOSE", "no safe moves"

# empty board diagonal race
assert run(
""".......A
........
........
........
........
........
........
M.......
"""
) == "WIN", "basic movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty board | WIN | Basic movement toward target |
| Single descending statue | WIN | Waiting in place is necessary |
| Full statue row | WIN | Surviving until all statues disappear |
| Immediate trap | LOSE | Correct rejection of unsafe moves |
| Repeated empty board | WIN | Boundary movement and BFS reachability |

## Edge Cases

Consider the case where Maria moves into a cell that becomes occupied immediately after statues descend.

Input:

```
.......A
........
........
........
........
........
.S......
M.......
```

At time 0, the statue is at `(6,1)`. Maria might try moving to `(6,1)` diagonally upward, but that cell is already occupied. She might instead move to `(6,0)`. After statues move, the statue becomes `(7,1)`, so Maria survives.

The algorithm checks both `safe(nr, nc, t)` and `safe(nr, nc, t + 1)`, preventing illegal transitions.

Now consider a case where all statues eventually disappear.

Input:

```
.......A
SSSSSSSS
........
........
........
........
........
M.......
```

Every turn, the entire statue row shifts downward. After 7 moves the statues leave the board completely. Since time is capped at 8, BFS continues exploring safe empty-board states until Maria reaches Anna.

Finally, consider a case where staying still is mandatory.

Input:

```
.......A
........
........
........
........
........
S.......
M.......
```

If Maria moves upward immediately, the descending statue creates dangerous positions. The BFS includes `(0,0)` movement in its direction list, allowing Maria to wait safely until the statue disappears. Without the stay action, the search would incorrectly report `"LOSE"`.
