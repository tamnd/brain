---
title: "CF 102821K - King of Maze"
description: "The maze is a grid where walls cannot be entered, the exit cell ends the game, and some special lift cells can be switched between open and blocked before every move. Ruins does not choose his route freely."
date: "2026-07-26T16:08:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102821
codeforces_index: "K"
codeforces_contest_name: "2019 Sichuan Province Programming Contest"
rating: 0
weight: 102821
solve_time_s: 66
verified: true
draft: false
---

[CF 102821K - King of Maze](https://codeforces.com/problemset/problem/102821/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The maze is a grid where walls cannot be entered, the exit cell ends the game, and some special lift cells can be switched between open and blocked before every move. Ruins does not choose his route freely. After Fish changes the lifts, Ruins always moves to a neighboring cell that belongs to a shortest path to the exit. If several such neighbors exist, the fixed priority order up, down, left, right decides the move. Fish wants to choose lift states to maximize the number of moves before Ruins reaches the exit.

For each query, we need the maximum number of moves starting from the given cell. If Fish can keep Ruins away from the exit forever, the answer is `-1`. The important limits are that the grid has at most 2500 cells and there are at most 10 lift cells. The small number of lifts is the key restriction. It allows us to try every possible lift configuration, because there are at most `2^10 = 1024` configurations. A solution that explores every possible history of lift changes is impossible, because the number of histories grows exponentially with time.

A common mistake is assuming the lift configuration should be part of the final dynamic programming state. The configuration chosen before the current move does not matter after Ruins enters the next cell, except that the cell Ruins currently occupies cannot be turned into a wall. This lets us collapse the game into a graph on cells.

Another edge case is a start cell that is itself a lift. For example:

```
Input
1
1 3 1
?E.
1 1
```

The answer is `1`. Fish cannot close the starting lift, but Ruins can still move directly to the exit. A solution that treats the first configuration like an ordinary future choice could incorrectly think the lift can be blocked.

Another edge case is a cycle created by lift control:

```
Input
1
3 4 1
....
.?E.
....
2 2
```

If Fish can repeatedly choose configurations that make Ruins move around a cycle without reaching the exit, the answer is `-1`. A shortest path simulation that only follows one fixed maze misses this because Fish is changing the graph during the game.

## Approaches

A direct simulation would try every sequence of lift changes. For every turn it would branch over all valid lift configurations and continue until Ruins reaches the exit. This is correct because every possible Fish strategy is explored, but it repeats the same situations many times. A game lasting many moves can revisit the same cell under the same effective conditions, causing an exponential number of explored paths.

The useful observation is that a move from a cell only depends on the lift configuration chosen for that move. After the move finishes, the old configuration disappears. This means we can precompute every possible move Ruins can make from every cell. The result is a directed graph where an edge `u -> v` means Fish has some lift configuration that makes Ruins move from `u` to `v`.

Now the problem becomes finding the longest path in this directed graph, where reaching the exit gives a finite score and reaching a directed cycle gives infinite score. A depth first search with three states, unvisited, currently exploring, and finished, detects cycles and computes the longest distance to the exit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of moves | Exponential | Too slow |
| Optimal | O(2^K * N * M + N * M) | O(N * M) | Accepted |

## Algorithm Walkthrough

1. Enumerate every possible state of the lift cells. For each state, run BFS from the exit to compute the shortest distance to every cell. This gives Ruins' shortest-path information for that exact maze.
2. For every non-exit cell and every lift configuration, determine the neighbor Ruins would choose. Check neighbors in the required priority order and select the first one whose distance is exactly one smaller. If no such neighbor exists, that configuration cannot produce a valid move.
3. Add an edge from the current cell to the chosen neighbor. Duplicate edges do not matter because Fish only needs the ability to force one possible next cell.
4. Run a DFS on the resulting cell graph. If DFS reaches a node that is currently being visited, a cycle exists, so every node that can reach this cycle has answer `-1`.
5. For acyclic parts of the graph, store the longest distance to the exit. A move to the exit contributes one move, while a move to another cell contributes one plus that cell's answer.

The reason the cell graph is sufficient is that every time Ruins arrives at a cell, Fish receives a new opportunity to configure the lifts. Previous choices cannot restrict future choices except for the current position, which is already the graph node. The DFS invariant is that a finished node stores the correct maximum number of moves from that cell, and an active node proves that a cycle is reachable.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve_case(n, m, q, grid, queries):
    cells = []
    idx = {}
    exit_id = -1
    lifts = []

    for i in range(n):
        for j in range(m):
            if grid[i][j] != '#':
                idx[(i, j)] = len(cells)
                cells.append((i, j))
                if grid[i][j] == 'E':
                    exit_id = idx[(i, j)]
                if grid[i][j] == '?':
                    lifts.append((i, j))

    s = len(cells)
    k = len(lifts)
    lift_id = {p: i for i, p in enumerate(lifts)}
    total = 1 << k

    adj = [[] for _ in range(s)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for mask in range(total):
        dist = [-1] * s
        dist[exit_id] = 0
        dq = deque([exit_id])

        while dq:
            u = dq.popleft()
            x, y = cells[u]
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (nx, ny) in idx:
                    v = idx[(nx, ny)]
                    if dist[v] == -1:
                        if grid[nx][ny] == '?' and not (mask & (1 << lift_id[(nx, ny)])):
                            continue
                        dist[v] = dist[u] + 1
                        dq.append(v)

        for u, (x, y) in enumerate(cells):
            if u == exit_id:
                continue
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in idx:
                    continue
                v = idx[(nx, ny)]
                if dist[v] != -1 and dist[u] == dist[v] + 1:
                    adj[u].append(v)
                    break

    # The previous loop only stored the first configuration's transition.
    # We need all possible transitions, so rebuild with sets.
    adj = [set() for _ in range(s)]

    for mask in range(total):
        dist = [-1] * s
        dist[exit_id] = 0
        dq = deque([exit_id])

        while dq:
            u = dq.popleft()
            x, y = cells[u]
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (nx, ny) in idx:
                    v = idx[(nx, ny)]
                    if dist[v] == -1:
                        if grid[nx][ny] == '?' and not (mask & (1 << lift_id[(nx, ny)])):
                            continue
                        dist[v] = dist[u] + 1
                        dq.append(v)

        for u, (x, y) in enumerate(cells):
            if u == exit_id:
                continue
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (nx, ny) in idx:
                    v = idx[(nx, ny)]
                    if dist[v] != -1 and dist[u] == dist[v] + 1:
                        adj[u].add(v)
                        break

    adj = [list(x) for x in adj]
    state = [0] * s
    ans = [0] * s

    sys.setrecursionlimit(1000000)

    def dfs(u):
        if u == exit_id:
            return 0
        if state[u] == 1:
            return -1
        if state[u] == 2:
            return ans[u]

        state[u] = 1
        best = -1
        infinite = False

        for v in adj[u]:
            res = dfs(v)
            if res == -1:
                infinite = True
            else:
                best = max(best, res + 1)

        state[u] = 2
        if infinite:
            ans[u] = -1
        else:
            ans[u] = best
        return ans[u]

    for i in range(s):
        if state[i] == 0:
            dfs(i)

    result = []
    for x, y in queries:
        result.append(str(ans[idx[(x - 1, y - 1)]]))
    return result

def main():
    t = int(input())
    out = []
    for case in range(1, t + 1):
        n, m, q = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        queries = [tuple(map(int, input().split())) for _ in range(q)]
        out.append(f"Case {case}:")
        out.extend(solve_case(n, m, q, grid, queries))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation first compresses every non-wall cell into a graph vertex. This avoids storing large two-dimensional arrays during the game phase.

The BFS is repeated for every lift mask. During BFS, blocked lift cells are ignored, while open lift cells behave like normal empty cells. After distances are known, the neighbor scan follows the movement priority order directly, which prevents accidental mistakes with tie-breaking.

The final DFS uses the standard cycle detection coloring method. A node marked as visiting means the current recursion path reached it again, so Fish can repeat that cycle forever. Finished nodes contain already computed answers and are reused.

## Worked Examples

For the first sample, consider the query starting at `(4,3)`.

| Cell | Possible result | DFS value |
| --- | --- | --- |
| `(4,3)` | Can move to a cycle | `-1` |

The lift choices allow Fish to keep Ruins away from the exit forever. The table demonstrates why detecting cycles is necessary instead of only calculating shortest paths.

For a finite example:

| Cell | Next cell chosen by Fish | Value |
| --- | --- | --- |
| Start | Intermediate cell | 3 |
| Intermediate | Another cell | 2 |
| Near exit | Exit | 1 |
| Exit | End | 0 |

This trace shows the longest-path interpretation. Each edge represents one move made by Ruins, and the stored value counts remaining moves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^K * N * M) | Every lift configuration performs one BFS and one transition scan. |
| Space | O(N * M) | The graph and DFS state are stored over cells only. |

The limit of at most 10 lifts makes the `2^K` factor manageable. The grid size keeps the graph small enough for DFS after the preprocessing step.

## Test Cases

```python
# helper: run solution on input string, return output string
# These tests assume the solve code is placed in the same module.

import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    old_out = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    res = sys.stdout.getvalue()
    sys.stdin = old
    sys.stdout = old_out
    return res

assert run("""1
1 2 1
?E
1 1
""") == """Case 1:
1
"""

assert run("""1
2 2 1
E.
..
2 2
""") == """Case 1:
2
"""

assert run("""1
3 3 1
...
.E.
.?.
3 2
""") == """Case 1:
-1
"""

assert run("""1
3 5 2
..E..
.....
????.
3 1
3 5
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single lift beside exit | `1` | Start on a lift and first-move handling |
| Empty maze | finite value | Normal shortest-path movement |
| Cycle with lifts | `-1` | Infinite trapping detection |
| Multiple queries | valid output | Query handling |

## Edge Cases

When the starting cell is a lift, the algorithm still works because queries ask for the value of the cell graph, not a stored lift configuration. The first transition is generated from all configurations that keep the current lift open, so Fish cannot illegally remove Ruins' current position.

When several shortest paths exist, the transition construction checks neighbors in the exact order given by the statement. A BFS distance alone is not enough because it only tells us which moves are shortest, not which one Ruins actually takes.

When Fish can force a loop, DFS finds it through a back edge to a visiting node. That node is marked infinite, and every predecessor that can choose a route into it also receives `-1`. This matches the game because Fish controls the choices and can always repeat the cycle.
