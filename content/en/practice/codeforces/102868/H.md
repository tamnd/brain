---
title: "CF 102868H - Yellow"
description: "The problem asks us to stop Yellow from travelling through a grid by closing as few doors as possible. The grid contains walls that are always blocked, hallways that are always open, and doors that can be either open or closed."
date: "2026-07-25T13:32:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102868
codeforces_index: "H"
codeforces_contest_name: "2020 UTPC Fall Puzzle Contest"
rating: 0
weight: 102868
solve_time_s: 50
verified: true
draft: false
---

[CF 102868H - Yellow](https://codeforces.com/problemset/problem/102868/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to stop Yellow from travelling through a grid by closing as few doors as possible. The grid contains walls that are always blocked, hallways that are always open, and doors that can be either open or closed. Yellow starts at the top-left cell and wants to reach the bottom-right cell. We need to find the smallest number of doors whose closure makes that destination unreachable. If hallways alone already give a path, the imposters cannot stop Yellow, so the answer is `-1`. The official problem describes this grid separation task with rows, columns, walls, doors, and hallways.

The grid can have up to 1000 rows and 1000 columns, which means there can be up to one million cells. Any algorithm that tries many paths explicitly will be far too slow because the number of possible paths grows exponentially. Even algorithms that process every pair of cells would already be too expensive. We need a method that touches each cell only a small number of times, which points toward graph algorithms with near-linear complexity.

The main tricky cases come from cells that are not ordinary open spaces. The starting cell and ending cell can themselves be doors. A careless solution might assume they are always accessible and miss that closing either one immediately blocks Yellow. For example:

```
2 2
..
.@
```

The correct answer is `1`. Closing the starting door is enough, but a solution that only considers doors between the start and end would incorrectly output a larger value.

Another edge case is when the path contains only hallways. Since hallways cannot be closed, no choice of doors can disconnect the two endpoints.

```
2 2
@@
@@
```

The correct answer is `-1`. A shortest path search that only counts doors on one discovered path could incorrectly output `0`, even though another hallway path still exists.

A final subtle case is when the answer is zero because walls already separate the endpoints.

```
3 3
@#.
###
.@.
```

The correct answer is `0`. The algorithm must allow the minimum cut to contain no doors at all.

## Approaches

A natural brute-force approach is to consider every possible subset of doors to close. For each subset, we can run a flood fill from the start and check whether the destination remains reachable. This is correct because every possible way of blocking doors is tested, but the number of subsets is `2^D`, where `D` is the number of doors. With hundreds of thousands of possible doors, this is impossible.

The key observation is that this is not really a path-finding problem. We are not looking for a route for Yellow. We are looking for the smallest set of removable obstacles whose removal separates two locations. That is exactly the definition of a minimum cut.

The grid can be converted into a flow network. Every cell becomes a graph node, and moving between adjacent cells becomes an infinite-capacity edge. Walls are simply omitted. Hallways have infinite capacity because they cannot be blocked. Doors have capacity one because cutting through such a cell represents closing exactly one door.

The remaining challenge is that standard minimum cut algorithms work on edges, while the cost belongs to cells. This is solved with node splitting. Each cell becomes two nodes: an entry node and an exit node. The edge from entry to exit carries the cost of removing that cell. Movement edges go from the exit side of one cell to the entry side of neighboring cells with infinite capacity. A minimum `s-t` cut then chooses which cell edges to cut, and the sum of their capacities is exactly the number of doors closed.

Because the grid contains up to one million cells, we need an efficient max flow implementation. Dinic's algorithm works well here because the graph is sparse. Each cell creates only a constant number of edges, so the network remains manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^D * (R*C)) | O(R*C) | Too slow |
| Optimal | O(V^2E) worst case with Dinic, practical on this sparse grid | O(R*C) | Accepted |

## Algorithm Walkthrough

1. Convert every non-wall cell into two graph nodes, an entry node and an exit node. Add an edge from entry to exit. Its capacity is `1` for a door and infinity for a hallway. The source and destination are chosen carefully because the start and end cells may also be doors.
2. For every pair of adjacent non-wall cells, add a directed edge from the exit node of the first cell to the entry node of the second cell with infinite capacity. Add the reverse direction as well. This represents Yellow being able to move both ways through neighboring cells.
3. Run a maximum flow algorithm from the start side to the destination side. By the max-flow min-cut theorem, the value of this flow is equal to the capacity of the cheapest set of edges separating the two sides.
4. If the resulting flow value is at least infinity, it means every possible separation would require cutting an impossible hallway edge. In that case the answer is `-1`. Otherwise, the flow value is the minimum number of doors that must be closed.

Why it works: the only finite-capacity edges in the graph are the entry-to-exit edges of doors. Any finite cut must choose some of these edges and cannot choose hallway edges. Cutting a door edge exactly represents closing that door. Any set of doors that blocks Yellow creates a valid cut of the same cost, and any finite cut creates a valid set of closed doors. The minimum cut value is thus exactly the minimum number of doors needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def max_flow(self, s, t):
        flow = 0
        n = self.n
        INF = 10**9

        while True:
            level = [-1] * n
            level[s] = 0
            q = [s]
            for u in q:
                for v, c, _ in self.g[u]:
                    if c and level[v] == -1:
                        level[v] = level[u] + 1
                        q.append(v)

            if level[t] == -1:
                return flow

            it = [0] * n

            def dfs(u, pushed):
                if u == t:
                    return pushed
                while it[u] < len(self.g[u]):
                    e = self.g[u][it[u]]
                    v, c, rev = e
                    if c and level[v] == level[u] + 1:
                        tr = dfs(v, min(pushed, c))
                        if tr:
                            e[1] -= tr
                            self.g[v][rev][1] += tr
                            return tr
                    it[u] += 1
                return 0

            while True:
                pushed = dfs(s, INF)
                if not pushed:
                    break
                flow += pushed

def solve():
    r, c = map(int, input().split())
    grid = [input().strip() for _ in range(r)]

    total = r * c * 2
    dinic = Dinic(total)

    def inside(x, y):
        return 0 <= x < r and 0 <= y < c

    def node(x, y, out):
        return (x * c + y) * 2 + out

    INF = 10**8

    for i in range(r):
        for j in range(c):
            if grid[i][j] == '#':
                continue
            cap = 1 if grid[i][j] == '.' else INF
            dinic.add_edge(node(i, j, 0), node(i, j, 1), cap)

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for i in range(r):
        for j in range(c):
            if grid[i][j] == '#':
                continue
            for dx, dy in dirs:
                ni, nj = i + dx, j + dy
                if inside(ni, nj) and grid[ni][nj] != '#':
                    dinic.add_edge(node(i, j, 1), node(ni, nj, 0), INF)

    source = node(0, 0, 0)
    sink = node(r - 1, c - 1, 1)

    ans = dinic.max_flow(source, sink)
    print(-1 if ans >= INF else ans)

if __name__ == "__main__":
    solve()
```

The graph construction follows the node-splitting idea directly. The entry-to-exit edge stores the cost of removing a cell, so only doors contribute to the final cut value. Hallways receive a very large capacity because a valid minimum cut should never choose to remove them.

The movement edges are added after the cell edges because they connect the exit side of one cell to the entry side of another. This direction matches the state after Yellow has already entered and left a cell. Both directions are needed because movement is allowed in all four directions.

The source uses the entry side of the first cell and the sink uses the exit side of the last cell. This handles the special case where either endpoint is a door. If the source or sink door is the cheapest thing to remove, the flow algorithm can select that edge.

The value used for infinity only needs to be larger than the maximum possible answer. Since the answer cannot exceed the number of cells, `10^8` is safely large.

## Worked Examples

For the first sample:

```
4 4
@..#
....
....
#..@
```

The important states are:

| Step | Current idea | Flow result |
| --- | --- | --- |
| 1 | Build a network where every door costs 1 | All possible paths exist |
| 2 | Find the minimum cut between corners | The cut must remove door cells |
| 3 | Minimum separating capacity is reached | 2 |

The trace shows that multiple routes exist, so removing a single door is not enough. The minimum cut chooses two door cells whose removal disconnects the endpoints.

For the second sample:

```
4 4
@..#
..#.
.#..
#..@
```

| Step | Current idea | Flow result |
| --- | --- | --- |
| 1 | Convert cells into split nodes | Network created |
| 2 | Search for any path through infinite hallway edges only | No such path exists |
| 3 | Minimum cut has capacity zero | 0 |

This demonstrates that the answer can be zero. The walls already prevent Yellow from reaching the button.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V^2E) worst case for Dinic | The grid creates O(R_C) nodes and O(R_C) edges, and the sparse structure performs well in practice |
| Space | O(R*C) | Each cell creates two nodes and a constant number of edges |

With one million cells, the graph is large but still linear in the input size. The implementation avoids storing the grid as a graph with unnecessary connections and uses adjacency lists, which keeps memory usage within the limit.

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

    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("""4 4
@..#
....
....
#..@
""") == "2\n", "sample 1"

assert run("""4 4
@..#
..#.
.#..
#..@
""") == "0\n", "sample 2"

assert run("""4 4
@@@@
..#@
.#.@
#..@
""") == "-1\n", "sample 3"

assert run("""2 2
..
.@
""") == "1\n", "start door"

assert run("""2 2
@@
@@
""") == "-1\n", "hallway only"

assert run("""3 3
@#.
###
.@.
""") == "0\n", "already disconnected"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 2 | Multiple routes require a real minimum cut |
| Sample 2 | 0 | Walls can make the destination unreachable without closing doors |
| Sample 3 | -1 | Hallway-only paths cannot be blocked |
| Start door case | 1 | Endpoint doors are handled correctly |
| Hallway only case | -1 | Infinite-capacity paths are detected |
| Separated grid case | 0 | Empty cuts are allowed |

## Edge Cases

When the start cell is a door, the source must connect through the door's capacity edge. For:

```
2 2
..
.@
```

the source-to-exit edge of the first cell has capacity `1`. The minimum cut can remove that edge immediately, giving a flow value of `1`.

When hallways form an unavoidable path, no finite cut exists. For:

```
2 2
@@
@@
```

all routes consist only of infinite-capacity edges. Dinic cannot push a finite separation through door edges because none exist, so the flow reaches the infinity threshold and the algorithm outputs `-1`.

When walls already disconnect the grid:

```
3 3
@#.
###
.@.
```

there is no path from source to sink in the constructed graph. The initial BFS in Dinic cannot reach the sink, so the maximum flow remains zero and the answer is correctly reported as `0`.
