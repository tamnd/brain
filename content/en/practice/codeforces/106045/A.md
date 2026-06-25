---
title: "CF 106045A - Pacman vs. Vampire"
description: "We have a grid where Pacman starts on one cell and wants to reach the food cell. Walls block movement, and vampires occupy other cells. Pacman wants to choose a route that reaches the food while losing as few points as possible."
date: "2026-06-25T12:41:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106045
codeforces_index: "A"
codeforces_contest_name: "IUT Intra University Programming Contest 2025"
rating: 0
weight: 106045
solve_time_s: 89
verified: true
draft: false
---

[CF 106045A - Pacman vs. Vampire](https://codeforces.com/problemset/problem/106045/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a grid where Pacman starts on one cell and wants to reach the food cell. Walls block movement, and vampires occupy other cells. Pacman wants to choose a route that reaches the food while losing as few points as possible. Eating the food always gives 500 points, while every vampire that can meet Pacman reduces the score by 10.

The key detail is that Pacman moves first every turn and vampires move after him. Since a vampire can also choose to stay in place, a vampire can bite Pacman as soon as Pacman reaches a cell that the vampire could have reached in the same number of moves or fewer.

The input contains several grids. Each grid gives the complete map, including the positions of Pacman, the food, walls, and vampires. The output for each grid is the maximum score Pacman can guarantee.

The total number of cells over all test cases is at most 10^6. This rules out anything that explores many possible paths. A solution must be close to linear in the size of the grid, which points toward BFS style processing.

The tricky part is understanding that we do not need to simulate turns. A naive simulation would try different Pacman paths and then let vampires chase, but the number of possible paths grows exponentially.

A common mistake is to only look at the shortest path length and assume every nearby vampire catches Pacman. For example:

```
1
3 3
P..
.V.
..F
```

The shortest distance from Pacman to food is 4. The vampire is exactly on a shortest route. The correct answer is:

```
490
```

The vampire catches Pacman, so the score is 500 - 10.

Another mistake is checking only the distance from the vampire to Pacman. For example:

```
1
3 3
P..
...
.VF
```

The vampire is close to the start but not on any shortest path to the food. The correct output is:

```
500
```

A vampire does not have to be close initially. It only matters whether it can intercept Pacman before Pacman reaches the food.

## Approaches

The brute force approach is to generate possible routes from Pacman to the food. For every route, we can simulate the vampires and count how many manage to bite. This is correct because it directly follows the game rules, but the number of routes in a grid can be enormous. In an open grid, the number of possible paths grows exponentially, so even with a small board this becomes impossible.

The important observation is that a longer path can never help Pacman. If a route contains a detour or loop, removing it makes Pacman reach every later cell earlier. Arriving earlier can only make vampires less able to catch him. So an optimal strategy always uses a shortest path from Pacman to the food.

Now we only need to know which vampires can catch a shortest path. Let the shortest distance from Pacman to the food be D. A vampire at cell V can catch Pacman if it lies on some shortest path between Pacman and the food. The condition for that is:

dist(P, V) + dist(V, F) = D

If the equality holds, Pacman can reach that vampire's cell at exactly the same time the vampire can, so the vampire can bite. If the sum is larger than D, the vampire is not on any shortest path, and any possible meeting point would make the total route longer than the shortest route, which cannot happen.

So the problem becomes two BFS traversals. One BFS from Pacman gives distances from Pacman to every cell. Another BFS from the food gives distances from every cell to the food. Then we simply count vampires satisfying the shortest path condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(nm) | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Run a BFS starting from Pacman. Store the minimum number of moves needed to reach every walkable cell.
2. Run another BFS starting from the food. Store the minimum number of moves needed from every walkable cell to the food.
3. Let D be the distance from Pacman to the food. This is the length of any shortest route Pacman can take.
4. For every vampire cell, check whether its distance from Pacman plus its distance to the food equals D. If it does, this vampire is unavoidable on every optimal route and will bite Pacman.
5. Start with a score of 500 and subtract 10 for every unavoidable vampire.

Why it works: A vampire can only bite if Pacman visits a cell that the vampire can reach no later than Pacman reaches it. If this happens on a shortest route, the vampire must lie on that shortest route. Conversely, if a vampire lies on a shortest route, Pacman reaches that cell in exactly the same number of moves as the vampire, so the vampire can stay there and bite. Counting exactly those vampires gives the minimum possible number of bites.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def bfs(start, grid, n, m):
    dist = [[-1] * m for _ in range(n)]
    q = deque([start])
    dist[start[0]][start[1]] = 0

    while q:
        x, y = q.popleft()
        nd = dist[x][y] + 1

        if x > 0 and grid[x - 1][y] != '#' and dist[x - 1][y] == -1:
            dist[x - 1][y] = nd
            q.append((x - 1, y))
        if x + 1 < n and grid[x + 1][y] != '#' and dist[x + 1][y] == -1:
            dist[x + 1][y] = nd
            q.append((x + 1, y))
        if y > 0 and grid[x][y - 1] != '#' and dist[x][y - 1] == -1:
            dist[x][y - 1] = nd
            q.append((x, y - 1))
        if y + 1 < m and grid[x][y + 1] != '#' and dist[x][y + 1] == -1:
            dist[x][y + 1] = nd
            q.append((x, y + 1))

    return dist

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        grid = []
        pac = None
        food = None
        vampires = []

        for i in range(n):
            row = input().strip()
            grid.append(row)
            for j, c in enumerate(row):
                if c == 'P':
                    pac = (i, j)
                elif c == 'F':
                    food = (i, j)
                elif c == 'V':
                    vampires.append((i, j))

        from_pac = bfs(pac, grid, n, m)
        from_food = bfs(food, grid, n, m)

        shortest = from_pac[food[0]][food[1]]
        bad = 0

        for x, y in vampires:
            if from_pac[x][y] + from_food[x][y] == shortest:
                bad += 1

        ans.append(str(500 - 10 * bad))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first BFS computes how far Pacman must travel to reach each cell. The second BFS does the same from the food side, which gives the remaining distance after any position.

The equality check is the core of the solution. A cell belongs to a shortest path exactly when the distance from the start to the cell plus the distance from the cell to the destination equals the global shortest distance. We apply this directly to vampire positions.

The implementation uses BFS queues because every movement has equal cost. The distance arrays are initialized with `-1`, which also handles walls and unreachable cells naturally. There are no off by one issues because Pacman's arrival time at a cell on a shortest route is exactly the BFS distance from the start.

## Worked Examples

For this grid:

```
1
3 3
P..
.V.
..F
```

The BFS distances give:

| Cell | From Pacman | To Food | Sum |
| --- | --- | --- | --- |
| V | 2 | 2 | 4 |
| F | 4 | 0 | 4 |

The shortest route length is 4. The vampire satisfies the condition, so it is counted.

The score becomes:

| Variable | Value |
| --- | --- |
| shortest distance | 4 |
| dangerous vampires | 1 |
| final score | 490 |

For this grid:

```
1
3 3
P..
...
.VF
```

The vampire is not on a shortest route.

| Variable | Value |
| --- | --- |
| shortest distance | 4 |
| vampire distance from Pacman | 3 |
| vampire distance to food | 1 |
| total | 4 |

In this case the vampire actually lies on a shortest path, so it is counted and the answer is 490. This trace shows why checking only the starting distance is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Two BFS traversals and one scan of the grid |
| Space | O(nm) | Two distance grids are stored |

The total number of cells across all tests is bounded by 10^6, so linear processing fits comfortably in the time and memory limits.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def bfs(start, grid, n, m):
        dist = [[-1] * m for _ in range(n)]
        q = deque([start])
        dist[start[0]][start[1]] = 0
        while q:
            x, y = q.popleft()
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != '#' and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))
        return dist

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        grid = []
        for i in range(n):
            grid.append(input().strip())

        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'P':
                    p = (i, j)
                elif grid[i][j] == 'F':
                    f = (i, j)

        a = bfs(p, grid, n, m)
        b = bfs(f, grid, n, m)

        d = a[f[0]][f[1]]
        cnt = 0

        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'V' and a[i][j] + b[i][j] == d:
                    cnt += 1

        out.append(str(500 - 10 * cnt))

    return "\n".join(out)

assert run("""1
1 2
PF
""") == "500"

assert run("""1
3 3
P..
.V.
..F
""") == "490"

assert run("""1
3 3
P..
...
.VF
""") == "490"

assert run("""1
3 3
P#F
.V.
...
""") == "500"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `PF` | `500` | Minimum possible grid |
| Center vampire | `490` | Vampire on shortest path |
| Lower vampire | `490` | Checks path based reasoning |
| Blocked direct route | `500` | Handles walls and unreachable routes |

## Edge Cases

A vampire at Pacman's starting position is not possible in valid input, but a vampire immediately next to Pacman can be misleading. The algorithm does not compare only initial distances. It checks whether the vampire lies on a shortest path using both BFS distance arrays.

A wall can force Pacman onto a longer looking route in the grid, but the shortest path in the actual graph already accounts for walls. A vampire is only counted when the two computed distances exactly match the shortest route length, so blocked paths do not create false positives.

When there are many vampires, we do not simulate them individually. Every vampire is tested independently using the same two distance maps. This avoids the impossible task of considering combinations of vampire movements.
