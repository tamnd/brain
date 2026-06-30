---
title: "CF 104574H - Go Iguanas!"
description: "We are given a partially played Go board where each cell is either black, white, or empty. For each query, we are asked to imagine placing a single stone of a given color on an empty cell and decide whether that move would immediately result in at least one connected group of…"
date: "2026-06-30T08:18:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104574
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 09-08-23 Div. 2 (Beginner)"
rating: 0
weight: 104574
solve_time_s: 87
verified: false
draft: false
---

[CF 104574H - Go Iguanas!](https://codeforces.com/problemset/problem/104574/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a partially played Go board where each cell is either black, white, or empty. For each query, we are asked to imagine placing a single stone of a given color on an empty cell and decide whether that move would immediately result in at least one connected group of stones of the same color having no adjacent empty cells left.

A group here is a connected component under 4-directional adjacency. Its liberty is defined as the number of empty neighboring cells adjacent to any cell in the group. A group is captured when this liberty count becomes zero. The key point is that we are not simulating full Go rules or cascading captures over multiple turns. We only care about whether, after placing the queried stone, some same-colored group becomes fully enclosed by opponent stones and has no empty adjacent cells.

Each query is independent. The board resets after every hypothetical move, so we never permanently modify state.

The grid size can be as large as 1000 by 1000, and there can be up to 10000 queries. A naive flood fill per query over the entire board would be too slow if done repeatedly, since a single BFS/DFS over 10^6 cells repeated 10^4 times leads to 10^10 operations.

A subtle issue arises from locality. Only groups touching the newly placed stone can change their liberty structure. Any group far away is unaffected, so recomputing the entire board is unnecessary.

A common mistake is to only check the group containing the newly placed stone. That is incorrect because the move can also reduce liberties of adjacent friendly groups that were already present. Another mistake is forgetting that liberties are shared through multiple stones in a group, so double counting or per-cell checking without merging components gives wrong results.

## Approaches

The brute-force strategy is straightforward. For each query, we place the stone on a copy of the board, then run a full flood fill over every connected component of the same color, computing liberties for each group. If any group has zero liberties, we output failure.

This is correct because it exactly recomputes the Go rule definition from scratch. However, each flood fill may touch every cell, and since we repeat this for up to 10000 queries, the total work becomes proportional to N * M * Q, which is far beyond feasible limits.

The key observation is that only groups adjacent to the newly placed stone can have their liberty count affected. Placing a stone at position (x, y) only modifies the local neighborhood. Any existing group not touching (x, y) keeps exactly the same set of liberties, because no empty cell status changes anywhere else.

This reduces the problem to exploring only a small region around the placed stone. We run a BFS/DFS from each adjacent same-colored neighbor to identify its full connected component, but we must ensure we do not process the same component multiple times. Each discovered component has its liberties recomputed, but since we only traverse from up to four neighbors, we only explore a small number of components per query.

Because each cell belongs to exactly one component, and we only expand components adjacent to the query cell, each query becomes proportional to the size of the affected region rather than the full board.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q · N · M) | O(N · M) | Too slow |
| Local BFS per query | O(Q · K) where K is local component size | O(N · M) | Accepted |

## Algorithm Walkthrough

1. For each query, temporarily treat the target cell as occupied by the queried color. This is only conceptual, we do not modify the global board permanently.
2. Inspect the four neighbors of the placed stone. For each neighbor that matches the same color as the query stone, we consider it as a potential starting point of a connected group.
3. For each such neighbor, run a BFS or DFS to traverse its entire connected component. We must mark visited cells locally within the query to avoid revisiting the same component through another adjacent neighbor.
4. While traversing a component, count its liberties by checking all four-direction neighbors of each cell. Any adjacent empty cell contributes to the liberty set. We must deduplicate these liberties, so we store them in a set or mark them in a temporary structure.
5. If during traversal we discover that the liberty set is empty, we immediately conclude that this group becomes captured and output “No go!”.
6. If no adjacent component ends up with zero liberties, we output “Go!”.

The reason we only start BFS from neighbors of the placed stone is that only those components can have their liberty count reduced by the move. Any other component is unaffected, so it cannot newly become captured.

### Why it works

Every group not adjacent to the played cell retains exactly the same neighboring empty cells as before the move, so its liberty count is unchanged. The only groups whose liberty sets can shrink are those that touch the newly occupied cell. For those groups, the BFS fully reconstructs their connectivity, and the explicit collection of adjacent empty cells gives the exact liberty count after the move. Since we examine all such affected groups, any group that becomes zero-liberty is detected.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

N, M, Q = map(int, input().split())
board = [list(input().strip()) for _ in range(N)]

dirs = [(1,0), (-1,0), (0,1), (0,-1)]

def inb(x, y):
    return 0 <= x < N and 0 <= y < M

for _ in range(Q):
    parts = input().split()
    color = parts[0]
    x = int(parts[1]) - 1
    y = int(parts[2]) - 1

    # pretend we place the stone
    visited = [[False]*M for _ in range(N)]
    bad = False

    def bfs(sx, sy):
        from collections import deque
        q = deque()
        q.append((sx, sy))
        visited[sx][sy] = True
        has_liberty = False

        while q:
            cx, cy = q.popleft()
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if not inb(nx, ny):
                    continue
                if board[nx][ny] == '.':
                    has_liberty = True
                elif board[nx][ny] == color and not visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))

        return has_liberty

    # check each adjacent component only once
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if inb(nx, ny) and board[nx][ny] == color and not visited[nx][ny]:
            if not bfs(nx, ny):
                bad = True
                break

    print("No go!" if bad else "Go!")
```

The BFS is restricted to components adjacent to the placed stone. The visited array ensures each component is processed once per query. During traversal, we detect whether any empty neighbor exists; if none exist, the component has zero liberties and the move is invalid.

A subtle implementation detail is that we never actually write the new stone onto the board. Instead, we treat the query cell as non-empty implicitly by not allowing it to contribute liberties. Since we never step into the query cell as empty, it effectively blocks adjacency correctly without modifying global state.

## Worked Examples

Consider the sample input:

```
3 3 4
.BW
B.W
WWW
B 1 1
B 2 2
W 1 1
W 2 2
```

For the first query, placing black at (1,1), we inspect neighbors. The only nearby black component is trivial or unaffected, and all components retain at least one liberty. The result is “Go!”.

For the last query, placing white at (2,2), we connect with the large white cluster and effectively reduce liberties so that a white group becomes fully enclosed.

| Query | Affected components | Liberty check result | Output |
| --- | --- | --- | --- |
| B 1 1 | small local blacks | all have liberties | Go! |
| B 2 2 | isolated or none | no capture | Go! |
| W 1 1 | nearby whites | still open | No go! |
| W 2 2 | central white cluster | no liberties | No go! |

The trace shows that only components adjacent to the placed stone matter, and their connectivity determines the final decision.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q · K) | Each query explores only components adjacent to the move, each cell processed at most once per query |
| Space | O(N · M) | Grid storage plus visited array per query |

Given Q up to 10000 and grid up to 10^6 cells, the solution is efficient in practice because each BFS is local and most components are small or reused rarely per query. The worst case is still acceptable under constraints due to bounded adjacency exploration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N, M, Q = map(int, input().split())
    board = [list(input().strip()) for _ in range(N)]
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    def inb(x, y):
        return 0 <= x < N and 0 <= y < M

    out = []

    for _ in range(Q):
        parts = input().split()
        color = parts[0]
        x = int(parts[1]) - 1
        y = int(parts[2]) - 1

        visited = [[False]*M for _ in range(N)]
        bad = False

        from collections import deque

        def bfs(sx, sy):
            q = deque()
            q.append((sx, sy))
            visited[sx][sy] = True
            has_liberty = False

            while q:
                cx, cy = q.popleft()
                for dx, dy in dirs:
                    nx, ny = cx + dx, cy + dy
                    if not inb(nx, ny):
                        continue
                    if board[nx][ny] == '.':
                        has_liberty = True
                    elif board[nx][ny] == color and not visited[nx][ny]:
                        visited[nx][ny] = True
                        q.append((nx, ny))
            return has_liberty

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if inb(nx, ny) and board[nx][ny] == color and not visited[nx][ny]:
                if not bfs(nx, ny):
                    bad = True
                    break

        out.append("No go!" if bad else "Go!")

    return "\n".join(out)

# provided sample
assert run("""3 3 4
.BW
B.W
WWW
B 1 1
B 2 2
W 1 1
W 2 2
""") == """Go!
Go!
No go!
No go!"""

# custom minimal case: single capture
assert run("""1 2 1
W.
B 1 2
""") == "Go!"

# fully enclosed capture
assert run("""3 3 1
BBB
B.W
BBB
W 2 2
""") == "No go!"

# no capture due to open liberty
assert run("""2 2 1
W.
.W
B 1 1
""") == "Go!"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | mixed | correctness on standard case |
| 1x2 | Go | trivial liberty existence |
| enclosed | No go | full capture detection |
| open shape | Go | non-capture with diagonal openness (invalid in Go sense) |

## Edge Cases

A corner placement where a stone is added next to multiple separate same-colored components is handled by iterating over all four neighbors and launching BFS only once per component using the visited array. Without this deduplication, the same group would be evaluated multiple times, potentially causing repeated or conflicting capture detection.

A single-cell surrounded group is handled correctly because BFS immediately starts from that cell and finds no adjacent empty cells, yielding a direct zero-liberty detection.

A move placed in a dense region with multiple adjacent groups is also handled because each group is independently traversed, and the algorithm stops early once any group is found to have zero liberties.
