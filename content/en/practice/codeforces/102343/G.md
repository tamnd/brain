---
title: "CF 102343G - Cooperative Escape"
description: "The city is a rectangular grid with at most 30 rows and 30 columns. Bonnie starts at one cell, Clyde starts at another, and the getaway car is at a third cell. Some cells are blocked. Each person moves one cell at a time in the four cardinal directions."
date: "2026-08-19T05:32:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "G"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 229
verified: true
draft: false
---

[CF 102343G - Cooperative Escape](https://codeforces.com/problemset/problem/102343/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is a rectangular grid with at most 30 rows and 30 columns. Bonnie starts at one cell, Clyde starts at another, and the getaway car is at a third cell. Some cells are blocked. Each person moves one cell at a time in the four cardinal directions.

The unusual restriction is that every traversable cell may be used at most once by the two people together. If Bonnie walks through a cell, Clyde can never enter it later, and vice versa. Their starting cells are also forbidden to the other person. Both people must eventually reach the car, and the objective is to minimize the sum of their numbers of moves. If no pair of valid routes exists, the answer is `-1`. The official UCF statement confirms these grid dimensions and the single-use-cell rule.

The grid contains at most (30 \times 30 = 900) cells. That is small enough to build an explicit graph with roughly a few thousand edges, but it is nowhere near small enough for a state containing the set of already visited cells. A naive search over both people's complete routes has exponentially many possibilities, so a solution based on subsets of cells or exhaustive path enumeration is not viable.

The tricky cases are caused by the interaction between the two routes. A shortest path for Bonnie and a shortest path for Clyde considered independently can share a cell, even though the pair is illegal. For example,

```
3 3
B.F
...
.C.
```

The individual shortest routes both want to use the middle area, so simply adding two ordinary BFS distances does not necessarily produce a legal pair of routes.

A second edge case is that the two starting cells cannot be entered by the other person. For example,

```
2 3
BCF
...
```

The correct answer is `3`: Bonnie can move directly from `(1,1)` to `(1,3)` in two moves, while Clyde moves from `(1,2)` to `(1,3)` in one move. A careless vertex-disjoint-path model that merely gives every cell capacity one can still allow a flow to enter a starting cell belonging to the other route unless incoming edges to the two starts are explicitly forbidden.

A third edge case is that both people are allowed to occupy the car. For example,

```
2 2
BF
C.
```

The answer is `2`. Bonnie needs one move and Clyde needs one move, and both paths end at the same cell. Giving the car capacity one would incorrectly declare this impossible.

## Approaches

The brute-force approach is to enumerate possible simple paths from Bonnie to the car and possible simple paths from Clyde to the car. For every pair, we check whether the two paths are internally disjoint and keep the minimum sum of their lengths. This is correct because every legal solution is exactly such a pair of paths.

The problem is the number of simple paths. In a grid with (V) usable cells, the number of simple paths can be exponential in (V), so enumerating them requires (2^{\Theta(V)}) or more work in dense grid regions. With (V=900), this is far beyond any practical operation budget. Even a search that represents the visited cells explicitly has up to (2^{900}) possible visited sets.

The key observation is that the restriction is not really about the order in which the two people move. It only says that the final two routes may not share a cell, except that they are both allowed to finish at the car. In graph terms, we need two vertex-disjoint paths from the two starting vertices to one common destination, minimizing their total number of edges.

That is exactly what a flow network with vertex capacities represents. Split every grid cell into an `in` vertex and an `out` vertex. The edge from `in` to `out` has capacity one, meaning that at most one route can use the cell. Movement from one cell to an adjacent cell becomes an edge from the first cell's `out` vertex to the second cell's `in` vertex. Since every movement costs one, give every movement edge cost one.

Then add a super-source connected to Bonnie and Clyde, with capacity one on each edge, and require two units of flow to reach the car. The car's capacity is two because both people are allowed to finish there. The minimum-cost flow is exactly the minimum total number of moves.

The brute-force works because every legal answer can be described by two paths, but fails because there are exponentially many such paths. The observation that cell usage is simply a capacity constraint lets us forget the actual search history and solve the whole problem as a minimum-cost flow instance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in (rc) | Exponential in (rc) in the worst case | Too slow |
| Optimal | (O(VE)) for two SPFA augmentations | (O(V+E)) | Accepted |

Here (V=O(rc)) and (E=O(rc)). The factor of two from the required flow value is constant.

## Algorithm Walkthrough

1. Read the grid and locate Bonnie, Clyde, and the car. Every non-`x` cell becomes a graph vertex.
2. Split every usable cell (v) into two graph vertices, `vin` and `vout`. Add an edge `vin -> vout` with capacity one and cost zero. This edge represents using that cell, so its capacity enforces the single-use rule.
3. For every pair of adjacent usable cells (u) and (v), add an edge `uout -> vin` with capacity one and cost one. Traversing this edge corresponds to making one grid move, so the total flow cost is exactly the total number of moves.
4. Do not add movement edges entering Bonnie's starting cell or Clyde's starting cell. Their own source edges are the only way to enter those cells. This directly models the rule that neither person may move into the other's starting position.
5. Add a super-source `S` and connect it to Bonnie's `in` vertex and Clyde's `in` vertex with capacity one and cost zero. Sending two units from `S` forces one unit to originate from each starting cell.
6. Give the car's `in -> out` edge capacity two. Both people must finish at the car, so this is the only ordinary cell that may be used by both flows.
7. Run minimum-cost flow until either two units have reached the car or no augmenting path exists. Since the required flow is only two, we perform at most two augmentations.
8. If two units of flow were sent, print their minimum total cost. Otherwise print `-1`, because at least one of the two people cannot be routed to the car without violating the cell-sharing restriction.

### Why it works

Every unit of flow corresponds to a route from one starting cell to the car. The capacity-one `in -> out` edge of every ordinary cell prevents two routes from using that cell, so the routes are vertex-disjoint. The starting-cell edges prevent either route from entering the other person's starting position. The car has capacity two, allowing both routes to end there.

Conversely, every legal pair of routes can be converted into two units of flow by following their grid edges. Because the routes do not share ordinary cells, all capacity constraints are respected. Each grid move contributes exactly one unit of cost, so the flow cost equals the sum of the two route lengths. Thus minimizing flow cost is exactly the original optimization problem.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10**9

class MinCostMaxFlow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap, cost):
        self.g[u].append([v, cap, cost, len(self.g[v])])
        self.g[v].append([u, 0, -cost, len(self.g[u]) - 1])

    def min_cost_flow(self, s, t, required):
        flow = 0
        cost = 0

        while flow < required:
            dist = [INF] * self.n
            prev_v = [-1] * self.n
            prev_e = [-1] * self.n
            in_queue = [False] * self.n

            dist[s] = 0
            q = deque([s])
            in_queue[s] = True

            while q:
                u = q.popleft()
                in_queue[u] = False

                for ei, edge in enumerate(self.g[u]):
                    v, cap, edge_cost, rev = edge
                    if cap > 0 and dist[v] > dist[u] + edge_cost:
                        dist[v] = dist[u] + edge_cost
                        prev_v[v] = u
                        prev_e[v] = ei

                        if not in_queue[v]:
                            q.append(v)
                            in_queue[v] = True

            if dist[t] == INF:
                break

            add = required - flow
            v = t

            while v != s:
                u = prev_v[v]
                ei = prev_e[v]
                add = min(add, self.g[u][ei][1])
                v = u

            v = t
            while v != s:
                u = prev_v[v]
                ei = prev_e[v]

                edge = self.g[u][ei]
                rev = edge[3]

                edge[1] -= add
                self.g[v][rev][1] += add

                v = u

            flow += add
            cost += add * dist[t]

        return flow, cost

def solve():
    r, c = map(int, input().split())
    grid = [input().strip() for _ in range(r)]

    cells = []
    pos = {}

    for i in range(r):
        for j in range(c):
            if grid[i][j] != 'x':
                idx = len(cells)
                cells.append((i, j))
                pos[(i, j)] = idx

    n_cells = len(cells)

    source = 2 * n_cells
    sink = 2 * n_cells + 1
    mcmf = MinCostMaxFlow(2 * n_cells + 2)

    start_b = start_c = finish = -1

    for idx, (i, j) in enumerate(cells):
        ch = grid[i][j]

        if ch == 'B':
            start_b = idx
        elif ch == 'C':
            start_c = idx
        elif ch == 'F':
            finish = idx

        capacity = 2 if ch == 'F' else 1
        mcmf.add_edge(2 * idx, 2 * idx + 1, capacity, 0)

    mcmf.add_edge(source, 2 * start_b, 1, 0)
    mcmf.add_edge(source, 2 * start_c, 1, 0)

    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for idx, (i, j) in enumerate(cells):
        # The two starting cells may only be entered from the super-source.
        if idx != start_b and idx != start_c:
            for di, dj in directions:
                ni, nj = i + di, j + dj
                nxt = pos.get((ni, nj))
                if nxt is not None:
                    mcmf.add_edge(2 * idx + 1, 2 * nxt, 1, 1)

    mcmf.add_edge(2 * finish + 1, sink, 2, 0)

    flow, cost = mcmf.min_cost_flow(source, sink, 2)

    if flow < 2:
        print(-1)
    else:
        print(cost)

if __name__ == "__main__":
    solve()
```

The `MinCostMaxFlow` class stores each residual edge as a four-element list containing its destination, remaining capacity, cost, and reverse-edge index. Residual edges have the negative of the original cost, which is why an ordinary BFS is not sufficient for shortest paths. The implementation uses SPFA to find the cheapest augmenting path.

The grid cells are numbered from zero to `n_cells - 1`. Cell `idx` becomes graph vertices `2 * idx` and `2 * idx + 1`. Keeping this mapping arithmetic rather than using dictionaries for graph vertices makes the network compact.

The capacity of the `in -> out` edge is one for ordinary cells and two for the car. The car is the only place where the two routes are allowed to meet.

The movement edges are deliberately added only when the current cell is not one of the two starting cells. That is slightly stronger than merely giving the starting cells capacity one. Without it, the flow could enter a starting cell from another grid cell after another unit of flow has already originated there, which does not correspond to a legal movement sequence.

Every movement edge has cost one, while all structural edges have cost zero. A path containing (k) movements consequently has cost exactly (k).

SPFA is safe here despite its unfavorable theoretical worst case because the graph has at most 900 grid cells, only two units of flow are needed, and the grid produces only (O(rc)) edges.

## Worked Examples

Since the problem statement available here does not expose sample input/output blocks, the following are two representative traces using the original input format.

### Example 1

Consider

```
3 4
B..F
.xx.
C...
```

Bonnie can take the top route in three moves. Clyde can take the bottom route in four moves. They do not share any ordinary cell, so the answer is seven.

| Augmentation | Route found | Path cost | Total flow | Total cost |
| --- | --- | --- | --- | --- |
| 1 | `B -> (1,2) -> (1,3) -> F` | 3 | 1 | 3 |
| 2 | `C -> (3,2) -> (3,3) -> (3,4) -> F` | 4 | 2 | 7 |

The first augmentation reserves the three cells on Bonnie's route. The second shortest augmenting path must respect those capacity-one edges, so it automatically chooses a route that does not reuse them. The final cost is `3 + 4 = 7`.

### Example 2

Consider

```
3 3
B.F
...
C..
```

The individually shortest routes both want to use the central region. A legal solution instead sends Bonnie across the upper row and Clyde through the lower row.

| Augmentation | Route found | Path cost | Total flow | Total cost |
| --- | --- | --- | --- | --- |
| 1 | `B -> (1,2) -> F` | 2 | 1 | 2 |
| 2 | `C -> (3,2) -> (3,3) -> F` | 3 | 2 | 5 |

The first route consumes `(1,2)`. The residual network records that capacity, so the second augmentation cannot use that cell. The resulting pair is vertex-disjoint and has total cost five.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(VE)) | At most two SPFA shortest-path computations are needed, each with the standard (O(VE)) worst-case bound |
| Space | (O(V+E)) | The split-cell graph and its residual edges contain (O(rc)) vertices and edges |

With at most 900 grid cells, the transformed network remains small. The important part is that the algorithm never stores a subset of visited cells and never enumerates pairs of routes. The two-unit flow formulation removes the exponential component entirely.

## Test Cases

The official statement provides the input format and constraints but the sample blocks are not present in the supplied problem text, so the tests below use the two worked examples and four additional cases. The helper reloads the solver for every invocation by redirecting standard input and output.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample-style case 1
assert run("""\
3 4
B..F
.xx.
C...
""") == "7\n", "two disjoint routes"

# Sample-style case 2
assert run("""\
3 3
B.F
...
C..
""") == "5\n", "shared-region routes must be separated"

# Minimum-size grid
assert run("""\
2 2
BF
C.
""") == "2\n", "both people reach the car in one move"

# No possible route for Clyde
assert run("""\
2 3
B.F
Cx.
""") == "-1\n", "one starting cell is trapped"

# All traversable cells form a narrow corridor
assert run("""\
2 4
BC.F
....
""") == "5\n", "starting cells and shared destination"

# Boundary-heavy case
assert run("""\
3 3
F.B
...
C..
""") == "5\n", "paths begin and end on grid boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 x 4` with separated upper and lower routes | `7` | Basic vertex-disjoint minimum-cost routing |
| `3 x 3` with competing shortest routes | `5` | The cell-capacity constraint changes the answer |
| `2 x 2` with `B`, `C`, and `F` adjacent | `2` | Minimum-size grid and capacity two at the car |
| `2 x 3` with Clyde trapped | `-1` | Correct detection when two units of flow are impossible |
| `2 x 4` corridor | `5` | Starting-cell restrictions and narrow geometry |
| `3 x 3` with boundary starts and destination | `5` | Boundary movement and off-by-one handling |

## Edge Cases

For the minimum-size case

```
2 2
BF
C.
```

the graph sends one unit from `B` through the single movement edge into `F`, and another unit from `C` through its movement edge into `F`. The car's split edge has capacity two, so both flows can terminate there. The two augmentations cost one each, giving `2`.

For a blocked participant,

```
2 3
B.F
Cx.
```

Clyde has no usable neighbor at all. The source can send one unit through Bonnie, but after that there is no second augmenting path to the sink. The algorithm stops with flow one instead of two and prints `-1`.

For the starting-position restriction,

```
2 3
BCF
...
```

the movement edges entering the `B` and `C` cells are absent. Each of those cells can only receive its own unit of flow from the super-source. This prevents a route from illegally entering the other person's starting cell.

For the shared destination,

```
2 2
BF
C.
```

the two paths both terminate at `F`, but no ordinary cell is shared. The capacity two on the car is exactly what distinguishes this valid meeting point from an ordinary cell, whose capacity remains one.

For boundary cells, such as

```
3 3
F.B
...
C..
```

the graph simply omits neighbors outside the grid. There is no special movement logic for the first or last row and column beyond checking whether a neighboring coordinate exists in the `pos` dictionary, which avoids boundary off-by-one errors.
