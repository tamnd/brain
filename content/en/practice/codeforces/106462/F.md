---
title: "CF 106462F - \u041b\u0430\u0431\u0438\u0440\u0438\u043d\u0442"
description: "The grid describes a rectangular maze made of cells, where some cells are blocked by walls and the rest are walkable. Among the walkable cells there is exactly one starting position marked as A and exactly one target cell marked as G."
date: "2026-06-25T08:58:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106462
codeforces_index: "F"
codeforces_contest_name: "\u041f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0441\u0440\u0435\u0434\u0438 \u043d\u0430\u0447\u0438\u043d\u0430\u044e\u0449\u0438\u0445 2026"
rating: 0
weight: 106462
solve_time_s: 36
verified: true
draft: false
---

[CF 106462F - \u041b\u0430\u0431\u0438\u0440\u0438\u043d\u0442](https://codeforces.com/problemset/problem/106462/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid describes a rectangular maze made of cells, where some cells are blocked by walls and the rest are walkable. Among the walkable cells there is exactly one starting position marked as A and exactly one target cell marked as G. From the starting cell, movement is allowed one step at a time in the four cardinal directions, but only onto cells that are not walls. The task is to determine whether there exists any sequence of valid moves that starts at A and eventually reaches G.

Although the maze may look complicated, the problem is purely about connectivity in a grid graph. Each free cell acts as a node, and edges exist between orthogonally adjacent free cells.

The constraints are small: the grid is at most 100 by 100, so there are at most 10,000 nodes. This size already suggests that any solution that explores the entire grid multiple times would still be fast enough. A traversal that touches each cell a constant number of times is well within limits, while anything superlinear per cell pair, such as checking all paths explicitly, is unnecessary.

A few edge situations matter more than they appear at first glance. One is when A and G are enclosed in separate regions by walls. For example, a narrow corridor split by a single blocking cell:

```
A . #
# # #
. . G
```

Even though both A and G exist, they lie in disconnected components, so the answer must be NO. A naive approach that assumes “open space implies reachability” would fail here.

Another case is when the shortest path exists but is not obvious because it requires detouring around obstacles:

```
A . # . G
# . # . #
# . . . #
```

Here, greedy movement toward G can fail, because local choices do not guarantee progress in a maze. Any correct solution must explore alternatives rather than committing to a single direction.

Finally, it is possible for A and G to be adjacent but still blocked diagonally or by walls around them in a way that prevents movement. Only shared edges matter; diagonal proximity does not allow movement.

## Approaches

A direct approach is to treat this as a path-finding problem and try to explicitly construct a route from A to G. One could imagine recursively trying all possible movement sequences, marking visited cells to avoid cycles. This works because the grid is finite and movement is restricted, so eventually all reachable states are explored. However, in the worst case, the number of possible paths grows exponentially with the number of open cells. In a 100 by 100 grid with many empty cells, this approach would attempt an enormous number of redundant partial paths, revisiting the same regions through different orders of steps.

The key observation is that the order of visiting cells does not matter for reachability. What matters is only whether G lies in the same connected component as A in the implicit graph of grid cells. Once this is seen, the problem reduces to a standard graph traversal: starting from A, we explore all reachable cells using either breadth-first search or depth-first search. Each cell is processed at most once, and every edge is checked only when we expand a node.

This eliminates path enumeration entirely. Instead of reasoning about sequences of moves, we reason about reachability as a property of a graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force path enumeration | Exponential in open cells | O(H·W) recursion stack | Too slow |
| BFS / DFS reachability | O(H·W) | O(H·W) | Accepted |

## Algorithm Walkthrough

We model the grid as a graph where each free cell is a node and edges connect adjacent free cells.

1. Locate the coordinates of A and G while reading the grid. This gives the start and target nodes in the graph.
2. Initialize a queue for BFS (or a stack for DFS) and insert the starting position A. Also maintain a visited array of the same size as the grid to avoid revisiting cells.
3. While the structure is not empty, remove the next cell and treat it as the current position.
4. If the current position is G, we can stop immediately because we have proven that G is reachable from A.
5. Otherwise, attempt to move in the four directions: up, down, left, right. For each neighbor, check whether it is inside the grid, not a wall, and not already visited. If all conditions hold, mark it visited and add it to the queue.
6. If the traversal finishes without ever reaching G, then G is not reachable from A.

The correctness comes from the invariant that the queue always contains exactly the set of grid cells that are reachable from A through some path, but not yet processed. Every time we pop a cell, we fully explore all ways to extend a valid path from A through that cell. Since every reachable cell is eventually discovered, if G is reachable, it must eventually be enqueued and processed.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    H, W = map(int, input().split())
    grid = []
    start = goal = None

    for i in range(H):
        row = list(input().strip())
        grid.append(row)
        for j, c in enumerate(row):
            if c == 'A':
                start = (i, j)
            elif c == 'G':
                goal = (i, j)

    sx, sy = start
    gx, gy = goal

    q = deque()
    q.append((sx, sy))
    visited = [[False] * W for _ in range(H)]
    visited[sx][sy] = True

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        x, y = q.popleft()

        if (x, y) == (gx, gy):
            print("YES")
            return

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < H and 0 <= ny < W:
                if not visited[nx][ny] and grid[nx][ny] != '#':
                    visited[nx][ny] = True
                    q.append((nx, ny))

    print("NO")

if __name__ == "__main__":
    solve()
```

The solution keeps the grid unchanged and only tracks reachability. The visited array is essential because without it, the BFS would repeatedly re-enter cycles in open regions and degrade into exponential repetition.

The early exit when reaching G avoids unnecessary traversal once the answer is already determined.

## Worked Examples

### Example 1

Input:

```
5 5
#####
#...#
#.#.#
#A#G#
#####
```

| Step | Queue | Visited (partial) | Current | Action |
| --- | --- | --- | --- | --- |
| 0 | (3,1) | A | (3,1) | Start from A |
| 1 | neighbors | A + reachable | (2,1) | Expand |
| 2 | ... | ... | (3,3)=G | Found |

The traversal quickly reaches G through the only narrow corridor. This confirms that the BFS correctly follows forced paths when they exist.

### Example 2

Input:

```
5 5
#####
#.G.#
#####
#A..#
#####
```

| Step | Queue | Visited | Current | Action |
| --- | --- | --- | --- | --- |
| 0 | (3,1) | A | (3,1) | Start |
| 1 | (3,2) | A + bottom row | (3,2) | Expand |
| 2 | empty region | bottom region only | - | G unreachable |

The wall row fully separates A from G, so BFS never crosses into the upper region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(H·W) | Each cell is enqueued and processed at most once, and each of its four edges is checked once |
| Space | O(H·W) | Visited array and queue store at most all grid cells |

Given H, W ≤ 100, the total operations are at most a few thousand, well within limits.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    return out.getvalue().strip()

# sample 1
assert run("""5 5
#####
#...#
#.#.#
#A#G#
#####""") == "YES"

# sample 2
assert run("""5 5
#####
#.G.#
#####
#A..#
#####""") == "NO"

# minimum grid
assert run("""5 5
#####
#A..#
#.###
#..G#
#####""") == "YES"

# fully blocked separation
assert run("""5 5
#####
#A###
#####
###G#
#####""") == "NO"

# long corridor
assert run("""5 7
#######
#A....#
#.###.#
#....G#
#######""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | YES | basic connectivity |
| sample 2 | NO | separated components |
| minimum grid | YES | shortest non-trivial path |
| fully blocked separation | NO | no reachable region |
| long corridor | YES | detour path handling |

## Edge Cases

A case where A and G are adjacent but separated by a wall checks that adjacency alone is not enough. In an input like:

```
#####
#AG##
#####
#...#
#####
```

BFS starts from A, marks it visited, and inspects neighbors. The cell containing G is adjacent, but if it is a wall or blocked position (as per rules it would be '#' or inaccessible), it is never enqueued. The algorithm only adds cells that satisfy the walkable condition, so G is ignored unless it is truly reachable.

A case where the maze is a single long winding corridor ensures that revisiting prevention is necessary. Without the visited array, the algorithm would bounce back and forth between two cells indefinitely. With it, each corridor cell is processed once, and the traversal proceeds linearly until reaching the goal or exhausting the corridor.
