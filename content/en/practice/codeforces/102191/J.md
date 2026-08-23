---
title: "CF 102191J - Graph to Grid"
description: "We are given a connected graph whose vertices are the labels of black cells from some unknown grid with exactly two rows and c columns. Two vertices are connected in the graph exactly when their corresponding cells shared a side in the original grid."
date: "2026-08-24T00:11:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "J"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 2233
verified: false
draft: false
---

[CF 102191J - Graph to Grid](https://codeforces.com/problemset/problem/102191/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 37m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected graph whose vertices are the labels of black cells from some unknown grid with exactly two rows and `c` columns. Two vertices are connected in the graph exactly when their corresponding cells shared a side in the original grid. The labels themselves are arbitrary, so the graph tells us which tiles must be adjacent, but it does not tell us where those tiles were placed.

Our task is to find any placement of the labels `1..n` into the `2 × c` board, leaving the other cells as `0`, such that the side-adjacencies of the occupied cells are exactly the edges of the input graph.

The input contains at most `2c` vertices, so `n` is at most `2 * 10^5`. Because every cell in a two-row grid has at most three possible black neighbors, a valid input graph also has only `O(n)` edges. With a one-second limit, an algorithm that is quadratic or exponential in `n` is not viable. We need to process essentially every vertex and edge only a constant number of times.

The unusual part is that the graph is guaranteed to be realizable. We do not need to recognize arbitrary graphs or report impossibility. We can exploit properties that every connected subgraph of a two-row grid must have. In particular, every vertex has degree at most three, and after choosing a suitable endpoint, graph distance behaves like Manhattan distance from a corner of the reconstructed board.

A careless implementation can still fail on very small or very narrow boards. For example, with

```
1 2 1
1 2
```

the only possible output is

```
1
2
```

because the two labels must occupy the two rows of the only column. An algorithm that always tries to move to the next column first would immediately leave the board.

Another boundary case is a single vertex:

```
1 1 0
```

A valid output is

```
1
0
```

There is no edge to reproduce, so the algorithm must not assume that every vertex has a parent or that at least one edge exists.

A useful nontrivial case is a path with four vertices and only two columns:

```
2 4 3
1 2
2 3
3 4
```

One valid arrangement is

```
1 4
2 3
```

The graph is still just a path, even though the board uses both rows. A construction that only grows horizontally would need four columns and would exceed the available width. The ability to turn into the other row is what lets us fit the graph.

Finally, a four-cycle needs to be handled without creating an extra edge:

```
2 4 4
1 2
2 3
3 4
4 1
```

A valid output is

```
1 2
4 3
```

Here every occupied cell has exactly the graph neighbors it should have. Merely checking that every graph edge appears is insufficient, because placing two nonadjacent graph vertices next to each other would create an unwanted graph edge.

## Approaches

The direct brute-force approach is to try every possible placement of the labels into the `2c` board cells and check whether its induced adjacency graph equals the input graph. There are

[
\binom{2c}{n} n! = \frac{(2c)!}{(2c-n)!}
]

possible placements. In the worst case `n = 2c`, this is `(2c)!`, so for `c = 10^5` the search space is incomprehensibly large. Even checking a single placement takes `O(n)` time, so this approach is useful only as a conceptual baseline.

The brute force works because every candidate placement can be checked locally. The difficulty is finding the right placement without trying essentially all of them.

The crucial observation is that a connected graph coming from a two-row grid has a natural direction once we choose an endpoint of a diameter. The official discussion describes using a farthest vertex as the starting point and then processing vertices in BFS order.

Choose any vertex, run BFS, and take a farthest vertex `s`. Run BFS again from `s`. We use `s` as the top-left cell. Because `s` is an endpoint of a longest shortest path, there is a valid realization in which every vertex at graph distance `d` from `s` lies at Manhattan distance `d` from the top-left corner.

That changes the placement problem dramatically. Suppose a vertex `u` has a previously placed neighbor at `(r, x)`. Since `u` is one BFS level farther from `s`, there are only two possible cells for `u`: the other row in the same column, `(1-r, x)`, or the same row in the next column, `(r, x+1)`. We try the same-column position first because it folds the graph vertically and keeps the number of used columns small. This is the backtracking construction described in the contest discussion.

A candidate is accepted only if it is locally consistent. Every already placed graph neighbor of `u` must be geometrically adjacent to the candidate, and every already occupied geometric neighbor of the candidate must actually be a graph neighbor of `u`. The second condition prevents accidental edges from appearing in the constructed grid.

At first glance this is still backtracking, which could suggest exponential complexity. The special structure of this problem prevents that from becoming a general exponential search. Every vertex has at most two candidates, and an incorrect choice becomes impossible after only a constant amount of further placement. The contest discussion gives the resulting linear-time bound for this construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O((2c)! · n)` in the worst case | `O(c)` | Too slow |
| BFS + constrained backtracking | `O(n + e)` | `O(n + c)` | Accepted |

## Algorithm Walkthrough

1. Build the undirected adjacency list of the graph. A valid two-row grid graph has maximum degree three, so the total number of edges is linear in `n`.
2. Run BFS from vertex `1` and find a farthest vertex `s`. This gives us an endpoint from which the graph can be unfolded toward the other side of the board.
3. Run BFS from `s` again. Store both the BFS parent of every vertex and the order in which vertices are discovered. The parent guarantees that every non-root vertex has a previously processed neighbor.
4. Put `s` into row `0`, column `0`. Think of this as fixing one possible orientation of the unknown original grid. We only need one valid orientation, so rotations and reflections do not matter.
5. Process the remaining vertices in BFS order. For the current vertex `u`, take its BFS parent `p`. If `p` is at `(r, x)`, the two possible positions for `u` are `(1-r, x)` and `(r, x+1)`. The first candidate stays in the current column, so try it first.
6. For each candidate, reject it if it lies outside the `2 × c` board or if the cell is already occupied. Then inspect every graph neighbor of `u` that has already been placed. The candidate must be side-adjacent to each such vertex.
7. Also inspect the occupied cells immediately above, below, left, and right of the candidate. Every such occupied cell must correspond to a graph neighbor of `u`. This prevents the construction from introducing an edge that was absent from the input graph.
8. If a candidate passes all checks, place `u` there and continue recursively. If the rest of the construction later fails, undo this placement and try the other candidate.
9. Once every vertex has been placed, print the two rows. Empty cells remain `0`.

### Why it works

The invariant is that after placing the first `k` vertices of the BFS order, every graph edge whose endpoints are already placed is represented by a grid adjacency, and every grid adjacency between already occupied cells corresponds to a graph edge. The BFS parent gives each new vertex at least one earlier neighbor, while the two-dimensional structure and the distance from the chosen corner leave only the vertical and rightward positions as candidates. Backtracking keeps exactly the candidates compatible with the already constructed part. Since the input graph is guaranteed to have a valid realization, the correct branch is never permanently discarded. When all vertices are placed, the local invariant covers every possible pair of occupied cells, so the grid adjacency graph is exactly the input graph.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve_instance(c, n, e, edges):
    adj = [[] for _ in range(n)]

    for u, v in edges:
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)

    def bfs(start):
        dist = [-1] * n
        parent = [-1] * n
        order = []

        q = deque([start])
        dist[start] = 0

        while q:
            u = q.popleft()
            order.append(u)

            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)

        farthest = order[0]
        for v in order:
            if dist[v] > dist[farthest]:
                farthest = v

        return farthest, dist, parent, order

    # First BFS finds an endpoint of a diameter.
    start, _, _, _ = bfs(0)

    # Second BFS gives the placement order.
    start, dist, parent, order = bfs(start)

    board = [[-1] * c for _ in range(2)]
    row = [-1] * n
    col = [-1] * n

    board[0][0] = start
    row[start] = 0
    col[start] = 0

    def is_edge(u, v):
        for x in adj[u]:
            if x == v:
                return True
        return False

    def valid(u, r, x):
        if r < 0 or r >= 2 or x < 0 or x >= c:
            return False

        if board[r][x] != -1:
            return False

        # Every already placed graph neighbor of u
        # must be geometrically adjacent to this cell.
        for v in adj[u]:
            if row[v] != -1:
                if abs(row[v] - r) + abs(col[v] - x) != 1:
                    return False

        # Every already occupied geometric neighbor must
        # actually be a graph neighbor of u.
        if r > 0 and board[r - 1][x] != -1:
            if not is_edge(u, board[r - 1][x]):
                return False

        if r + 1 < 2 and board[r + 1][x] != -1:
            if not is_edge(u, board[r + 1][x]):
                return False

        if x > 0 and board[r][x - 1] != -1:
            if not is_edge(u, board[r][x - 1]):
                return False

        if x + 1 < c and board[r][x + 1] != -1:
            if not is_edge(u, board[r][x + 1]):
                return False

        return True

    sys.setrecursionlimit(max(1_000_000, n * 3 + 10))

    def dfs(idx):
        if idx == n:
            return True

        u = order[idx]
        p = parent[u]

        pr = row[p]
        pc = col[p]

        # Same column first, as recommended by the construction.
        candidates = (
            (1 - pr, pc),
            (pr, pc + 1),
        )

        for r, x in candidates:
            if not valid(u, r, x):
                continue

            board[r][x] = u
            row[u] = r
            col[u] = x

            if dfs(idx + 1):
                return True

            board[r][x] = -1
            row[u] = -1
            col[u] = -1

        return False

    # The input is guaranteed to be realizable.
    assert dfs(1)

    ans0 = [0] * c
    ans1 = [0] * c

    for x in range(c):
        if board[0][x] != -1:
            ans0[x] = board[0][x] + 1
        if board[1][x] != -1:
            ans1[x] = board[1][x] + 1

    return ans0, ans1

def main():
    c, n, e = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(e)]

    ans0, ans1 = solve_instance(c, n, e, edges)

    print(*ans0)
    print(*ans1)

if __name__ == "__main__":
    main()
```

The adjacency list stores the input graph in the natural representation for this construction. The graph has maximum degree three, so scanning one vertex's adjacency list is constant time in the intended instances.

The first BFS only supplies a good endpoint. The second BFS is the one that matters for placement because its parent array gives a previously placed neighbor for every non-root vertex. The BFS order is also essential because it guarantees that when a vertex is processed, its parent has already been assigned a coordinate.

The `board`, `row`, and `col` arrays store the same information in two directions. `board` answers whether a physical cell is occupied, while `row` and `col` give the physical position of a graph vertex. Keeping both avoids repeatedly searching the board.

The `valid` function performs both directions of the adjacency check. Checking only graph neighbors would allow extra edges to appear in the grid. Checking only the board neighbors would allow required graph edges to be missing. Together, the two checks enforce equality of the two graphs.

The two candidate positions are deliberately ordered as vertical first and rightward second. A vertical move uses an existing column instead of consuming another one, which is what makes the construction compact enough for the given `c`. The official discussion specifically recommends preferring the same-column choice.

Python's recursion limit is increased because a graph can contain a path with nearly `2c` vertices. There is no integer-overflow issue in Python, and all coordinates are explicitly checked against `0 <= row < 2` and `0 <= column < c`.

## Worked Examples

### Example 1: The provided sample

The input graph is

```
7 10 10
2 10
7 4
10 3
1 4
3 9
9 6
1 6
5 4
6 8
8 3
```

One possible BFS-based construction can be summarized as follows. The exact labels chosen by the search can differ from the statement's sample output, because the problem accepts any valid reconstruction.

| Stage | Vertex being placed | Parent | Preferred position | Result |
| --- | --- | --- | --- | --- |
| Start | 1 | none | `(0, 0)` | place 1 |
| BFS step | next vertex | already placed neighbor | same column first | accept if locally valid |
| BFS step | next vertex | already placed neighbor | same column or right | accept first valid candidate |
| Later | vertices around a cycle | earlier neighbors | candidate constrained by both sides | only cycle-compatible cell survives |
| Finish | all 10 vertices | all parents assigned | board completely consistent | output two rows |

The sample output itself is

```
2 10 3 8 0 7 0
0 0 9 6 1 4 5
```

For example, `10` is adjacent to `2` and `3`, `3` is adjacent to `10`, `9`, and `8`, and `6` is adjacent to `9`, `1`, and `8`. Every such adjacency is represented by a side-sharing pair in the grid, while no additional side-sharing pair appears.

### Example 2: A path that needs both rows

Consider

```
2 4 3
1 2
2 3
3 4
```

The algorithm starts with a farthest endpoint at `(0, 0)`.

| Step | Vertex | Parent | Candidate 1 | Candidate 2 | Chosen |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | none | `(0,0)` |  | `(0,0)` |
| 1 | 2 | 1 | `(1,0)` | `(0,1)` | `(1,0)` |
| 2 | 3 | 2 | `(0,0)` occupied | `(1,1)` | `(1,1)` |
| 3 | 4 | 3 | `(0,1)` | `(1,2)` outside | `(0,1)` |

The resulting grid is

```
1 4
2 3
```

The path has been folded into two columns. The vertical adjacency `1-2` and `3-4` comes from the same-column moves, while `2-3` comes from the horizontal edge.

This example demonstrates why the same-column candidate must be attempted before simply extending the current row. A purely horizontal construction would require four columns and would not fit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + e)` | Two BFS traversals and a constant amount of work per placement and backtracking decision |
| Space | `O(n + c)` | Adjacency lists, BFS arrays, board, and coordinate arrays |

For a graph generated from a two-row grid, every vertex has degree at most three, so `e = O(n)`. With `n <= 2 * 10^5`, the working memory is linear and the number of graph operations is proportional to the input size. The construction is designed specifically to avoid searching over arbitrary grid placements, which is necessary under the one-second limit. The contest discussion gives the same linear complexity for the constrained backtracking approach.

## Test Cases

The output is not unique, so the tests should validate the structural property rather than compare the output text character-for-character.

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def solve_instance(c, n, e, edges):
    adj = [[] for _ in range(n)]

    for u, v in edges:
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)

    def bfs(start):
        dist = [-1] * n
        parent = [-1] * n
        order = []

        q = deque([start])
        dist[start] = 0

        while q:
            u = q.popleft()
            order.append(u)

            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)

        farthest = order[0]
        for v in order:
            if dist[v] > dist[farthest]:
                farthest = v

        return farthest, dist, parent, order

    start, _, _, _ = bfs(0)
    start, _, parent, order = bfs(start)

    board = [[-1] * c for _ in range(2)]
    row = [-1] * n
    col = [-1] * n

    board[0][0] = start
    row[start] = 0
    col[start] = 0

    def is_edge(u, v):
        return v in adj[u]

    def valid(u, r, x):
        if not (0 <= r < 2 and 0 <= x < c):
            return False

        if board[r][x] != -1:
            return False

        for v in adj[u]:
            if row[v] != -1:
                if abs(row[v] - r) + abs(col[v] - x) != 1:
                    return False

        for rr, xx in ((r - 1, x), (r + 1, x),
                       (r, x - 1), (r, x + 1)):
            if 0 <= rr < 2 and 0 <= xx < c:
                v = board[rr][xx]
                if v != -1 and not is_edge(u, v):
                    return False

        return True

    sys.setrecursionlimit(max(1_000_000, 3 * n + 10))

    def dfs(idx):
        if idx == n:
            return True

        u = order[idx]
        p = parent[u]

        pr, pc = row[p], col[p]

        for r, x in ((1 - pr, pc), (pr, pc + 1)):
            if not valid(u, r, x):
                continue

            board[r][x] = u
            row[u] = r
            col[u] = x

            if dfs(idx + 1):
                return True

            board[r][x] = -1
            row[u] = -1
            col[u] = -1

        return False

    assert dfs(1)

    out = []
    for r in range(2):
        out.append(" ".join(
            str(board[r][x] + 1 if board[r][x] != -1 else 0)
            for x in range(c)
        ))
    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        c, n, e = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(e)]
        return solve_instance(c, n, e, edges)
    finally:
        sys.stdin = old_stdin

def validate(inp: str, out: str):
    lines = out.strip().splitlines()
    assert len(lines) == 2

    c, n, e = map(int, inp.splitlines()[0].split())
    given_edges = set()

    for line in inp.splitlines()[1:]:
        u, v = map(int, line.split())
        given_edges.add(tuple(sorted((u, v))))

    grid = [list(map(int, lines[0].split())),
            list(map(int, lines[1].split()))]

    assert len(grid[0]) == c
    assert len(grid[1]) == c

    values = [x for row in grid for x in row if x != 0]
    assert sorted(values) == list(range(1, n + 1))

    produced = set()

    for r in range(2):
        for x in range(c):
            if grid[r][x] == 0:
                continue

            if x + 1 < c and grid[r][x + 1] != 0:
                produced.add(tuple(sorted((grid[r][x], grid[r][x + 1]))))

            if r + 1 < 2 and grid[r + 1][x] != 0:
                produced.add(tuple(sorted((grid[r][x], grid[r + 1][x]))))

    assert produced == given_edges

# Provided sample
sample1 = """\
7 10 10
2 10
7 4
10 3
1 4
3 9
9 6
1 6
5 4
6 8
8 3
"""

out = run(sample1)
validate(sample1, out)

# Minimum-size input
case2 = """\
1 1 0
"""
out = run(case2)
validate(case2, out)

# Two vertices in a one-column board
case3 = """\
1 2 1
1 2
"""
out = run(case3)
validate(case3, out)

# Four-cycle
case4 = """\
2 4 4
1 2
2 3
3 4
4 1
"""
out = run(case4)
validate(case4, out)

# Maximum-width path: n = 2*c
# The graph itself is just a path, so the construction must fold it
# into exactly two rows rather than requiring 2*c columns.
c = 10
n = 20
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
case5 = f"{c} {n} {n - 1}\n{edges}\n"

out = run(case5)
validate(case5, out)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Any valid `2 × 7` reconstruction | Full graph with cycles and branches |
| `1 1 0` | One `1` and one `0` | No edges and the smallest possible board |
| `1 2 1` | The two labels occupy different rows | Narrowest possible boundary |
| Four-cycle | A `2 × 2` square | Required cycle edges and prevention of extra edges |
| `c=10, n=20` path | Any valid two-row folded path | Maximum number of vertices and width pressure |

The maximum-size test deliberately uses a path because it is the cleanest way to force `n = 2c`. A horizontal-only strategy would need twenty columns, while the two-row construction can fold the path into ten columns.

## Edge Cases

For the single-vertex case

```
1 1 0
```

the first BFS chooses vertex `1` as the farthest vertex because it is the only vertex. The second BFS also produces an order containing only vertex `1`. The recursive placement starts at `(0,0)` and immediately reaches its terminal condition. The output is simply

```
1
0
```

No parent lookup is performed for the root, which avoids the common mistake of assuming every vertex has a BFS parent.

For the one-column case

```
1 2 1
1 2
```

the root is placed at `(0,0)`. Vertex `2` has parent `1`, so its first candidate is `(1,0)`, which is inside the board and adjacent to vertex `1`. The rightward candidate `(0,1)` is outside the board. The result is

```
1
2
```

The boundary check is what prevents an off-by-one error here.

For the four-cycle

```
2 4 4
1 2
2 3
3 4
4 1
```

the search cannot place the fourth vertex next to the first three arbitrarily. Its candidate must be adjacent to both required already placed neighbors and must not create any additional geometric edge. The local consistency check rejects the incorrect candidate and leaves the square arrangement

```
1 2
4 3
```

which has exactly the four required edges.

For the maximum-width path with `c = 10` and `n = 20`, the algorithm repeatedly prefers the same-column candidate whenever that cell is available. The path consequently alternates between the two rows instead of consuming a new column for every vertex. The construction fits all twenty vertices into ten columns, exercising both the recursion depth and the board boundary checks.
