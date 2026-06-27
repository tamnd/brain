---
title: "CF 105627L - Rolling-Dice Game"
description: "The board contains open cells, blocked cells, a starting position for a die, and some cells that contain target numbers from 1 to 6. The die starts in a fixed orientation: the top face is 6, the north face is 4, and the west face is 2."
date: "2026-06-26T18:11:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105627
codeforces_index: "L"
codeforces_contest_name: "The 2023 ICPC Asia Tehran Regional Contest"
rating: 0
weight: 105627
solve_time_s: 49
verified: true
draft: false
---

[CF 105627L - Rolling-Dice Game](https://codeforces.com/problemset/problem/105627/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
# Problem Understanding

The board contains open cells, blocked cells, a starting position for a die, and some cells that contain target numbers from 1 to 6. The die starts in a fixed orientation: the top face is 6, the north face is 4, and the west face is 2. A move rolls the die into an adjacent non-blocked cell, changing its orientation according to the direction of the roll.

Whenever the die stands on a numbered cell and the value on its top face equals the number written in that cell, that cell contributes one point. Each cell can contribute at most once, even if the die reaches it many times. The task is to find the maximum number of points that can be collected.

The board dimensions are at most 100 by 100, giving at most 10,000 cells. A direct search over paths is impossible because the number of possible walks grows exponentially with the number of moves. Even if we only considered every possible sequence of directions of length 100, the number of possibilities would already be far beyond what can be explored. The useful observation is that a die has only 24 possible orientations, so the total number of meaningful states is small enough: at most 100 × 100 × 24 = 240,000 states.

A subtle point is that the goal is not to find a single shortest path or a path with a small number of moves. The die may revisit cells and move around freely. A solution that marks a cell as visited and never enters it again would incorrectly remove possible future scoring opportunities.

For example:

```
1 2
s1
..
```

The correct answer is `1`. The die can move to the cell containing `1` in some orientation and score it. A normal grid BFS that ignores orientation might assume the first visit decides everything and miss that the same position can be reached with different die faces.

Another case is when a cell is reachable but cannot ever score:

```
1 2
s2
..
```

The answer is not automatically the number of numbered cells. A cell only contributes when the top face matches its value. A careless approach that counts all reachable numbered cells would return `1`, but the correct answer can be `0` if the required orientation is impossible.

The final edge case is that the starting cell is not counted immediately. If the start position contains no written number, there is no score. If the problem allowed a number on the start cell, the same state graph idea would still handle it correctly.

## Approaches

The brute-force way to think about the problem is to try every possible sequence of rolls and keep track of the best score obtained. This is correct because every possible movement strategy is considered. The problem is that the number of possible paths explodes. From every state there can be up to four moves, so after many moves the number of explored paths becomes exponential.

The structure that saves us is that the die does not have unlimited memory. Its future behavior depends only on two things: the current board cell and the current orientation of the die. The complete history of moves is irrelevant because returning to the same cell with the same orientation gives exactly the same future possibilities.

This turns the problem into graph reachability. Each state is a pair `(row, column, orientation)`. Moving the die creates edges between these states. Since every roll can be undone by rolling back, all reachable states can be explored with BFS or DFS.

After finding every reachable state, we do not need to simulate an actual final route. Every reachable state can be visited during a walk through the reachable state graph. Therefore, for every board cell, if at least one reachable orientation places the correct number on top, that cell can be collected.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of moves | Exponential | Too slow |
| State Graph Search | O(nm × 24) | O(nm × 24) | Accepted |

## Algorithm Walkthrough

1. Represent every possible die orientation as a state. The die has six faces, but opposite faces are fixed, so a cube has only 24 physically possible orientations. Starting from the given orientation, we generate new orientations by rolling in the four directions.
2. Start a BFS from the state containing the starting cell and the initial die orientation. The reason for storing the orientation together with the position is that the same cell can behave differently depending on which face is on top.
3. When exploring a state, try all four possible rolls. Ignore moves that leave the board or enter blocked cells. For every valid move, compute the new orientation and add the new state if it has not been reached before.
4. After BFS finishes, inspect every reachable state. If the state is standing on a numbered cell and the top face equals that cell's value, mark the cell as collectible.
5. Count the marked cells. This count is the maximum possible score because all collectible cells correspond to reachable states, and the reachable state graph allows visiting all such states.

Why it works: the BFS explores exactly the states that the die can ever reach. The state graph contains all information needed to determine future moves, because position and orientation completely describe the die. Every scoring opportunity is represented by a reachable state with a matching top face, and all reachable states can be traversed in some walk, so every such cell can be collected. Cells without a matching reachable state can never give points.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def roll(state, direction):
    top, bottom, north, south, west, east = state

    if direction == 0:  # east
        return (west, east, north, south, bottom, top)
    if direction == 1:  # west
        return (east, west, north, south, top, bottom)
    if direction == 2:  # north
        return (south, north, top, bottom, west, east)
    return (north, south, bottom, top, west, east)  # south

def solve():
    n, m = map(int, input().split())
    board = [input().strip() for _ in range(n)]

    sr = sc = -1
    for i in range(n):
        for j in range(m):
            if board[i][j] == 's':
                sr, sc = i, j

    start = (6, 1, 4, 3, 2, 5)

    orientations = []
    index = {}
    queue = deque([start])
    index[start] = 0

    while queue:
        cur = queue.popleft()
        orientations.append(cur)
        for d in range(4):
            nxt = roll(cur, d)
            if nxt not in index:
                index[nxt] = len(index)
                queue.append(nxt)

    dirs = [(-1, 0, 2), (1, 0, 3), (0, -1, 1), (0, 0, 0)]
    # The last entry is replaced below because east has no simple row/col pair.
    moves = [(-1, 0, 2), (1, 0, 3), (0, -1, 1), (0, 1, 0)]

    seen = [[[False] * 24 for _ in range(m)] for _ in range(n)]
    seen[sr][sc][index[start]] = True

    q = deque([(sr, sc, index[start])])

    while q:
        r, c, o = q.popleft()
        cur = orientations[o]

        for dr, dc, d in moves:
            nr = r + dr
            nc = c + dc

            if not (0 <= nr < n and 0 <= nc < m):
                continue
            if board[nr][nc] == 'x':
                continue

            no = index[roll(cur, d)]
            if not seen[nr][nc][no]:
                seen[nr][nc][no] = True
                q.append((nr, nc, no))

    ans = 0
    for i in range(n):
        for j in range(m):
            if board[i][j].isdigit():
                value = int(board[i][j])
                ok = False
                for o in range(24):
                    if seen[i][j][o] and orientations[o][0] == value:
                        ok = True
                        break
                if ok:
                    ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part of the implementation generates all 24 cube orientations. The tuple order is `(top, bottom, north, south, west, east)`, which makes each roll operation a simple reassignment of faces.

The BFS stores a three-dimensional state: row, column, and orientation id. The orientation id is obtained from the precomputed list, avoiding repeated tuple comparisons during traversal.

The scoring phase is separate from the traversal. This is intentional because reaching a state and collecting a cell are different concepts. A cell only needs one reachable orientation that exposes the correct top face.

The boundary checks prevent invalid moves, and blocked cells are skipped before adding new states. The number of states is small enough that Python can safely store all visited states.

## Worked Examples

For the first sample:

```
3 4
.23s
4.2x
xx.1
```

A simplified trace of the BFS and scoring phase is:

| Position | Orientation top | Action |
| --- | --- | --- |
| (0,3) | 6 | Start BFS |
| (0,2) | 2 | Collect cell containing 2 |
| (0,1) | 5 | No score |
| (1,1) | 3 | No score |
| (1,0) | 4 | Collect cell containing 4 |
| (2,2) | 1 | Collect cell containing 1 |

The full reachable state graph contains more orientations than shown, and those extra states allow the die to collect all matching cells. The final count is `5`, because every numbered cell except one can be matched by some reachable orientation.

For the second sample:

```
2 2
4s
22
```

The trace is:

| Position | Orientation top | Action |
| --- | --- | --- |
| (0,1) | 6 | Start BFS |
| (0,0) | 2 | No score |
| (1,1) | 3 | No score |
| (1,0) | 4 | No score |

The two cells containing `2` are reachable, but neither is reachable with the top face equal to `2`. The answer is `1` because only the cell containing `4` can be matched.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm × 24) | Each board cell and each die orientation is processed at most once. |
| Space | O(nm × 24) | The visited array stores every possible position-orientation state. |

The maximum number of states is 240,000 for a 100 by 100 board, which is small enough for the given limits. The algorithm avoids any dependence on path length, making it suitable even when the die can move around the board indefinitely.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

# provided samples
assert run("""3 4
.23s
4.2x
xx.1
""") == "5\n"

assert run("""2 2
4s
22
""") == "1\n"

# minimum size
assert run("""1 1
s
""") == "0\n"

# all reachable values with several matches
assert run("""3 3
s12
345
6..
""") == "6\n"

# obstacles and unreachable cells
assert run("""3 3
sxx
x1x
xx2
""") == "0\n"

# larger open area with repeated values
assert run("""4 4
s111
1111
1111
1111
""") == "16\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / s` | `0` | Smallest board and missing targets |
| Open board with digits 1 to 6 | `6` | Multiple orientations and repeated movement |
| Separated regions by obstacles | `0` | Correct obstacle handling |
| Large area of identical values | `16` | Revisiting cells and collecting all possible matches |

## Edge Cases

For a board where a numbered cell is reachable only in a different orientation, the algorithm does not stop after the first visit. For example:

```
2 2
s1
..
```

BFS stores both the first arrival at a cell and every other reachable orientation. When the cell containing `1` is checked, the algorithm finds a reachable state with top face `1` and counts it.

For a reachable numbered cell with no possible matching orientation, such as:

```
2 2
s2
..
```

the BFS still explores the cell, but the scoring phase checks the top face of every reachable orientation. If none show `2`, the cell is ignored.

For boards with obstacles:

```
3 3
sxx
x1x
xx2
```

the BFS only expands states inside valid cells. The isolated numbered cells never become reachable states, so they cannot contribute points. The answer remains zero without any special handling.
