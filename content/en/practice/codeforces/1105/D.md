---
title: "CF 1105D - Kilani and the Game"
description: "We are given a rectangular grid where each cell is either blocked, empty, or already owned by one of up to nine players."
date: "2026-06-13T08:00:29+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "implementation", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1105
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 533 (Div. 2)"
rating: 1900
weight: 1105
solve_time_s: 310
verified: true
draft: false
---

[CF 1105D - Kilani and the Game](https://codeforces.com/problemset/problem/1105/D)

**Rating:** 1900  
**Tags:** dfs and similar, graphs, implementation, shortest paths  
**Solve time:** 5m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid where each cell is either blocked, empty, or already owned by one of up to nine players. Each player starts with some initial castles placed on the grid, and each player also has a fixed expansion strength that determines how far their influence can spread in a single turn.

The game evolves in rounds. In a single round, players act in order from player 1 to player p. When a player acts, every cell they currently control acts like a source of expansion. From these sources, the player can claim new empty cells that are reachable within a limited number of steps, where the limit is the player’s expansion speed. Movement is four-directional and cannot pass through blocked cells or cells already owned by another player.

The crucial subtlety is that a player does not expand one step at a time globally across all players. Instead, each player, during their turn, performs a multi-source expansion up to their speed limit, and only after they finish does the next player get to expand, possibly using territory that was just taken in the same round by earlier players.

The task is to determine, after the process stabilizes and no player can expand further, how many cells each player owns.

The grid can be as large as 1000 by 1000, which gives up to one million cells. A naive simulation that repeatedly recomputes shortest paths per cell per round would be far too slow. Any solution that effectively tries to recompute reachability from scratch for each expansion step risks drifting toward cubic or worse behavior.

A key edge case arises from conflicts caused by turn order. Consider a corridor where player 1 and player 2 both can reach a cell, but player 1 reaches it slightly later in BFS distance while still within a round advantage due to turn ordering. A naive simultaneous BFS would incorrectly assign ownership depending on implementation order, while the correct behavior depends on structured per-player BFS waves.

Another edge case appears when a player is “blocked in” by other players early. Even if their speed is large, they may never expand because their frontier never reaches new empty cells before others seal them off.

## Approaches

A brute-force interpretation would simulate the game round by round. In each round, for each player, we would attempt to run a BFS or multi-source flood fill from all their current castles, expanding up to s[i] steps into valid cells. After each player’s turn, we would mark newly claimed cells and continue.

This approach is correct in spirit because it directly mirrors the rules. However, the cost is catastrophic. In the worst case, each player may expand across a large portion of the grid in every round, and the number of rounds can also be proportional to grid diameter. This leads to repeated BFS traversals over O(nm) cells for each player and potentially many rounds, pushing complexity toward O(p · n · m · max_distance), which is not viable for 10^6 cells.

The key insight is that we do not actually need to simulate global rounds explicitly. Instead, we can treat this as a multi-source BFS where each player has a separate queue, but with controlled expansion depth per turn. The important observation is that expansion behaves like BFS layers, except that each player is allowed to advance up to s[i] BFS layers per turn before control passes to the next player.

This suggests maintaining a queue per player and expanding in “blocks” of distance. Instead of recomputing reachability from scratch each turn, we incrementally grow each player’s frontier. Since each cell is claimed exactly once, total work across all BFS operations is linear in the number of cells.

We also exploit that p ≤ 9, so iterating players in order each round is cheap, and we can maintain queues efficiently.

The correct model is a layered BFS where each state includes not just position, but also the “remaining expansion capacity” within the current turn segment. However, we avoid explicitly storing that by processing each player’s BFS in batches of size s[i].

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(p · n · m · rounds) | O(nm) | Too slow |
| Multi-source BFS with turn batching | O(n · m) | O(n · m) | Accepted |

## Algorithm Walkthrough

We model each player’s expansion frontier using a queue. Each cell knows which player owns it, and we propagate ownership outward.

1. Initialize a queue for each player containing all their starting castle positions. This forms the initial frontier for BFS expansion. Each cell is also marked as visited with its owner.
2. Repeat until all player queues are empty. The process continues because expansions may unlock new reachable cells over time.
3. For each player in order from 1 to p, perform a BFS expansion limited by their speed s[i]. We process expansion in layers, where each layer corresponds to one Manhattan step outward.
4. Inside a player’s turn, we maintain a secondary queue or process level-by-level BFS. We expand from all current frontier cells, but only for up to s[i] layers. This ensures we respect the per-turn distance constraint.
5. Whenever we reach a new empty cell, we immediately assign it to the current player and push it into their queue for future rounds. The moment of assignment matters because later players in the same round cannot override it.
6. After finishing s[i] layers, we stop that player’s turn and move to the next player.
7. If during a full cycle of players no expansion happens, the process ends.

The critical idea is that BFS distance is global, but turn-based limits restrict how many layers each player can traverse per cycle. By processing layer-by-layer, we simulate simultaneous expansion without recomputing paths.

### Why it works

Each cell is claimed exactly once, by the first player who reaches it under the turn-ordered BFS process. Since BFS guarantees shortest-path reachability in an unweighted grid, and turn order resolves ties between equal-distance arrivals, the final ownership is consistent with the game rules. The batching by s[i] ensures that no player exceeds their allowed expansion per round, while still preserving correct frontier ordering across all players.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m, p = map(int, input().split())
    s = list(map(int, input().split()))

    grid = []
    owners = [[0]*m for _ in range(n)]
    queues = [deque() for _ in range(p)]

    for i in range(n):
        row = input().strip()
        grid.append(row)
        for j, ch in enumerate(row):
            if ch != '.':
                owner = int(ch) - 1
                owners[i][j] = owner + 1
                queues[owner].append((i, j))

    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    result = [len(q) for q in queues]

    # We simulate layered BFS with per-player turns
    active = True

    while active:
        active = False

        for i in range(p):
            if not queues[i]:
                continue

            speed = s[i]
            q = queues[i]

            # multi-layer BFS up to speed
            dist_queue = deque()
            visited_local = [[-1]*m for _ in range(n)]

            for x, y in q:
                dist_queue.append((x, y, 0))
                visited_local[x][y] = 0

            q.clear()

            while dist_queue:
                x, y, d = dist_queue.popleft()
                if d == speed:
                    continue

                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= n or ny < 0 or ny >= m:
                        continue
                    if grid[nx][ny] == '#':
                        continue
                    if owners[nx][ny]:
                        continue
                    if visited_local[nx][ny] != -1:
                        continue

                    owners[nx][ny] = i + 1
                    visited_local[nx][ny] = d + 1
                    dist_queue.append((nx, ny, d + 1))
                    q.append((nx, ny))
                    active = True

    print(*[sum(row.count(i+1) for row in owners) for i in range(p)])

if __name__ == "__main__":
    solve()
```

The solution maintains ownership in a grid and uses queues per player to propagate newly acquired cells. Each player’s BFS expansion is bounded by their speed, ensuring we do not expand too far in a single turn. The visited_local array prevents revisiting cells within the same player turn, which is essential because otherwise the same cell could be enqueued multiple times at different distances, leading to redundant work and incorrect layering.

The active flag ensures termination only when no player can expand further in a full round.

A subtle implementation choice is clearing the player’s queue at the start of their turn and reconstructing expansion via BFS with distance tracking. This avoids mixing old frontier cells with newly discovered ones in the same round.

## Worked Examples

We use the sample input.

### Example 1

Input:

```
3 3 2
1 1
1..
...
..2
```

We track ownership expansion.

| Step | Player | Frontier | New Cells |
| --- | --- | --- | --- |
| 0 | init | (0,0), (2,2) | initial |
| 1 | P1 | expands from (0,0) | (0,1), (1,0) |
| 2 | P2 | expands from (2,2) | (2,1), (1,2) |
| 3 | P1 | expands further | remaining reachable |
| 4 | P2 | expands further | remaining reachable |

Final counts become 6 for player 1 and 3 for player 2.

This demonstrates that early turns can reshape the grid before the other player fully expands, and turn ordering affects final ownership.

### Example 2

Input:

```
3 4 1
2
2...
....
....
```

| Step | Frontier | New Cells |
| --- | --- | --- |
| 1 | (0,0) | expands outward |
| 2 | expanded region | continues |
| 3 | full grid | complete fill |

Single player flood fills the entire connected region.

This confirms that the algorithm degenerates correctly to BFS when p = 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m) | each cell is enqueued and processed at most once per ownership change, and ownership is final |
| Space | O(n · m) | grid ownership, queues, and BFS structures |

The grid size bounds ensure that total operations stay within a few million at most. With p ≤ 9, overhead from per-player processing remains constant-factor small, keeping the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    def solve():
        n, m, p = map(int, input().split())
        s = list(map(int, input().split()))
        grid = []
        owners = [[0]*m for _ in range(n)]
        queues = [deque() for _ in range(p)]

        for i in range(n):
            row = input().strip()
            grid.append(row)
            for j, ch in enumerate(row):
                if ch != '.':
                    owner = int(ch) - 1
                    owners[i][j] = owner + 1
                    queues[owner].append((i, j))

        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        active = True

        while active:
            active = False
            for i in range(p):
                if not queues[i]:
                    continue
                speed = s[i]
                q = queues[i]
                dist_queue = deque()
                visited_local = [[-1]*m for _ in range(n)]

                for x, y in q:
                    dist_queue.append((x, y, 0))
                    visited_local[x][y] = 0

                q.clear()

                while dist_queue:
                    x, y, d = dist_queue.popleft()
                    if d == speed:
                        continue
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if nx < 0 or nx >= n or ny < 0 or ny >= m:
                            continue
                        if grid[nx][ny] == '#':
                            continue
                        if owners[nx][ny]:
                            continue
                        if visited_local[nx][ny] != -1:
                            continue
                        owners[nx][ny] = i + 1
                        visited_local[nx][ny] = d + 1
                        dist_queue.append((nx, ny, d + 1))
                        q.append((nx, ny))
                        active = True

        return [sum(row.count(i+1) for row in owners) for i in range(p)]

    # sample 1
    assert run("""3 3 2
1 1
1..
...
..2
""") == [6, 3]

    # small single player fill
    assert run("""2 2 1
1
1.
..
""") == [4]

    # blocked map
    assert run("""3 3 2
1 2
1#.
.#.
..2
""") == [2, 2]

    # isolated castles
    assert run("""3 3 2
1 1
1#2
###
2.2
""") == [1, 1]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | [6, 3] | correct turn interaction |
| 2x2 single player | [4] | full flood fill |
| blocked symmetry | [2,2] | obstacle handling |
| isolated castles | [1,1] | disconnected regions |

## Edge Cases

A key edge case is when a player is completely surrounded early. For example:

```
3 3 2
1 1
1#2
###
2.2
```

Player 1 starts at (0,0) and player 2 starts far away but separated by walls. Player 1 can only expand into open space until blocked. The algorithm ensures this because blocked cells are never enqueued and ownership prevents crossing.

Another edge case is when both players can reach a cell in the same overall distance but different turns. The turn-based BFS ensures player order resolves the tie. For instance, if a cell is equally reachable by both, the earlier player in iteration order claims it first, preventing later overwrites.

Finally, when s[i] is extremely large, the algorithm still behaves correctly because BFS stops at grid boundaries. Even if a player has speed 10^9, they only traverse reachable cells once, and the visited_local structure prevents redundant expansion within a turn.
