---
title: "CF 152E - Garden"
description: "We have a rectangular grid where every cell has a cost, the number of flowers destroyed if we pave that cell with concrete. Among all cells, there are up to seven special cells containing important buildings."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 152
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 108 (Div. 2)"
rating: 2500
weight: 152
solve_time_s: 144
verified: true
draft: false
---

[CF 152E - Garden](https://codeforces.com/problemset/problem/152/E)

**Rating:** 2500  
**Tags:** bitmasks, dp, graphs, trees  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular grid where every cell has a cost, the number of flowers destroyed if we pave that cell with concrete. Among all cells, there are up to seven special cells containing important buildings. We must choose a connected set of paved cells such that every important cell belongs to the paved region, and every important cell can reach every other one using 4-directional moves through paved cells.

The objective is to minimize the total sum of costs of all paved cells.

A useful way to think about the grid is as a weighted graph. Every cell is a vertex, adjacent cells are connected by edges, and entering a cell costs its flower count. We are looking for a minimum-cost connected subgraph containing all terminals. This is exactly a Steiner Tree problem on a grid graph.

The grid can contain at most 200 cells, which is small enough for graph algorithms over all vertices. The number of terminals is at most 7, which is the real clue. A general Steiner Tree problem is NP-hard, but when the number of terminals is tiny, subset dynamic programming becomes feasible.

A naive subset enumeration over all grid subsets would require checking up to $2^{200}$ states, completely impossible. Even enumerating all trees or all paths between terminals explodes combinatorially.

The small terminal count suggests DP over terminal masks. Since $2^7 = 128$, we can maintain a DP state for every subset of terminals and every cell.

There are several easy-to-miss corner cases.

One subtle case is when the optimal solution revisits cells shared by multiple terminal connections.

Example:

```
2 3 3
1 100 1
1 1 1
1 1
1 3
2 2
```

The cheapest structure is not three separate shortest paths. The middle bottom row acts as a shared corridor. A greedy strategy connecting terminals pairwise independently would overcount costs and produce a non-optimal union.

Another tricky case is when two terminals are adjacent.

```
1 2 2
5 7
1 1
1 2
```

The answer must pave both cells with total cost 12. A careless implementation that treats path cost as edge cost instead of vertex cost may forget to include one endpoint.

A more subtle issue appears during reconstruction. Different subsets may merge at the same cell.

```
3 3 3
1 1 1
1 100 1
1 1 1
1 1
1 3
3 2
```

The optimal tree merges around cheap outer cells and avoids the center. If parent tracking only stores shortest-path relaxations and not subset merges, reconstruction fails even if the DP values are correct.

## Approaches

The brute-force approach is to enumerate every subset of grid cells, check whether it forms a connected component containing all terminals, and compute its total cost. The grid has at most 200 cells, so this requires examining $2^{200}$ subsets, which is astronomically large.

A slightly smarter brute-force idea is to try all possible trees connecting terminals. Since the graph itself has up to 200 vertices and many possible Steiner points, the number of candidate trees is still far beyond feasible.

The key observation is that the number of important cells is extremely small. When only a few terminals exist, we can describe connectivity requirements using a bitmask.

Suppose we define:

$$dp[mask][v]$$

as the minimum cost of a connected paved region that contains exactly the terminals in `mask` and ends at cell `v`, meaning `v` belongs to the connected structure.

Now the problem starts looking manageable. There are only $2^k \le 128$ masks and at most 200 cells, so the total number of states is around 25,000.

The next observation is how these states combine.

If two connected structures both end at the same cell `v`, one covering subset `A` and the other covering subset `B`, then merging them at `v` creates a valid connected structure for `A ∪ B`.

That gives the transition:

$$dp[A \cup B][v] = dp[A][v] + dp[B][v] - cost(v)$$

We subtract the cell cost once because both structures already counted it.

After performing subset merges, we still need to move across the grid. From every cell we can relax neighbors exactly like shortest paths on a graph. Since all edge additions correspond to paying the neighbor's cell cost, multi-source shortest path propagation updates all reachable endpoints optimally.

This combination of subset DP and shortest paths is the classic Dreyfus-Wagner style Steiner Tree DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{nm})$ | $O(2^{nm})$ | Too slow |
| Optimal | $O(3^k \cdot nm + 2^k \cdot (nm)^2)$ | $O(2^k \cdot nm)$ | Accepted |

## Algorithm Walkthrough

1. Convert every grid cell into a graph vertex.

Give each cell an integer id. Adjacent cells in the four cardinal directions are connected.
2. Define the DP state.

Let:

$$dp[mask][v]$$

be the minimum total paving cost for a connected structure containing all terminals in `mask` and ending at vertex `v`.
3. Initialize singleton masks.

If terminal `i` is located at vertex `v`, then:

$$dp[1 << i][v] = cost(v)$$

because the smallest connected structure containing only that terminal is the single cell itself.
4. Merge smaller subsets into larger subsets.

For every mask and every non-empty proper submask:

$$sub \subset mask$$

update:

$$dp[mask][v] = \min( dp[mask][v], dp[sub][v] + dp[mask \oplus sub][v] - cost(v) )$$

Both connected structures meet at the same cell `v`, producing a larger connected structure.
5. Run shortest path relaxation for every mask.

After subset merges, the best structure ending at one cell may be extended through neighboring cells.

Since all costs are positive, Dijkstra works naturally.

For each mask, run Dijkstra starting from all vertices with initial distances `dp[mask][v]`.

Relaxing from `u` to `to` adds `cost(to)`.
6. Track parent information.

Reconstruction needs two kinds of parents:

First, shortest-path parents from Dijkstra.

Second, subset split parents showing which two submasks were merged.
7. Find the best endpoint.

The answer is:

$$\min_v dp[(1<<k)-1][v]$$

Any endpoint works because the structure itself is connected.
8. Reconstruct the used cells.

Recursively follow parent pointers.

Whenever a state comes from a subset merge, recurse into both parts.

Whenever a state comes from shortest-path relaxation, recurse into the predecessor cell.

Mark every visited cell as paved.

### Why it works

The DP invariant is:

$$dp[mask][v]$$

always equals the minimum cost among all connected paved subgraphs containing every terminal in `mask` and containing vertex `v`.

The subset transition is correct because any connected Steiner tree can be decomposed at a branching vertex into smaller connected trees covering disjoint terminal subsets.

The shortest-path relaxation is correct because extending a connected structure by one neighboring cell preserves connectivity and adds exactly that cell's paving cost.

Since every connected Steiner tree can be built by repeatedly merging smaller terminal groups and extending through adjacent cells, the DP explores all valid possibilities. Every transition preserves optimality, so the final state for the full mask is globally optimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**18

def solve():
    n, m, k = map(int, input().split())

    grid = [list(map(int, input().split())) for _ in range(n)]

    terminals = []
    for _ in range(k):
        x, y = map(int, input().split())
        terminals.append((x - 1, y - 1))

    V = n * m

    def vid(x, y):
        return x * m + y

    cost = [0] * V

    for i in range(n):
        for j in range(m):
            cost[vid(i, j)] = grid[i][j]

    adj = [[] for _ in range(V)]

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    for x in range(n):
        for y in range(m):
            v = vid(x, y)

            for d in range(4):
                nx = x + dx[d]
                ny = y + dy[d]

                if 0 <= nx < n and 0 <= ny < m:
                    adj[v].append(vid(nx, ny))

    FULL = 1 << k

    dp = [[INF] * V for _ in range(FULL)]

    parent = [[None] * V for _ in range(FULL)]

    for i, (x, y) in enumerate(terminals):
        v = vid(x, y)
        dp[1 << i][v] = cost[v]

    for mask in range(FULL):

        sub = (mask - 1) & mask

        while sub:
            other = mask ^ sub

            for v in range(V):
                val = dp[sub][v] + dp[other][v] - cost[v]

                if val < dp[mask][v]:
                    dp[mask][v] = val
                    parent[mask][v] = ("merge", sub, other)

            sub = (sub - 1) & mask

        pq = []

        for v in range(V):
            if dp[mask][v] < INF:
                heapq.heappush(pq, (dp[mask][v], v))

        while pq:
            dist, v = heapq.heappop(pq)

            if dist != dp[mask][v]:
                continue

            for to in adj[v]:
                nd = dist + cost[to]

                if nd < dp[mask][to]:
                    dp[mask][to] = nd
                    parent[mask][to] = ("move", v)

                    heapq.heappush(pq, (nd, to))

    full = FULL - 1

    best_v = min(range(V), key=lambda v: dp[full][v])

    ans = dp[full][best_v]

    used = [[False] * m for _ in range(n)]

    sys.setrecursionlimit(10**6)

    def build(mask, v):
        x = v // m
        y = v % m

        used[x][y] = True

        p = parent[mask][v]

        if p is None:
            return

        if p[0] == "move":
            build(mask, p[1])

        else:
            _, a, b = p
            build(a, v)
            build(b, v)

    build(full, best_v)

    print(ans)

    for i in range(n):
        row = []

        for j in range(m):
            row.append('X' if used[i][j] else '.')

        print("".join(row))

solve()
```

The solution has two intertwined components, subset DP and shortest paths.

The DP table stores the best connected structure for every terminal subset and endpoint. Since all terminal counts are tiny, iterating over all masks is feasible.

The subset merging loop uses the standard submask iteration pattern:

```
sub = (mask - 1) & mask
```

This enumerates all proper non-empty submasks efficiently.

A common bug here is double counting the meeting cell. Both partial structures already include vertex `v`, so we subtract its cost once during merging.

After merging, Dijkstra propagates the connected structure through the grid. The distance update adds the destination cell cost because entering a new paved cell destroys its flowers.

Parent tracking stores two kinds of transitions.

```
("move", prev_vertex)
```

means Dijkstra relaxation.

```
("merge", left_mask, right_mask)
```

means two subsets were merged at the same vertex.

The reconstruction DFS follows these transitions recursively and marks all visited cells.

One subtle detail is that multiple recursive calls may revisit the same state. That is harmless because we only need the final set of used cells.

## Worked Examples

### Example 1

Input:

```
3 3 2
1 2 3
1 2 3
1 2 3
1 2
3 3
```

The terminals are at `(1,2)` and `(3,3)`.

| Step | Mask | Endpoint | Cost |
| --- | --- | --- | --- |
| Initialize | 01 | (1,2) | 2 |
| Initialize | 10 | (3,3) | 3 |
| Dijkstra | 01 | reachable cells | shortest costs |
| Dijkstra | 10 | reachable cells | shortest costs |
| Merge | 11 | common endpoint | combined |
| Final | 11 | (3,2) | 9 |

The reconstructed structure becomes:

```
.X.
.X.
.XX
```

This trace demonstrates the key invariant: every DP state represents a connected structure. The merge happens only after both subsets independently become connected.

### Example 2

Input:

```
2 3 3
1 100 1
1 1 1
1 1
1 3
2 2
```

| Step | Mask | Endpoint | Best Cost |
| --- | --- | --- | --- |
| Initialize | 001 | (1,1) | 1 |
| Initialize | 010 | (1,3) | 1 |
| Initialize | 100 | (2,2) | 1 |
| Merge | 101 | (2,1) | 3 |
| Merge | 111 | (2,2) | 5 |

Optimal paving:

```
X.X
XXX
```

The expensive top-middle cell with cost 100 is avoided entirely. This example shows why the algorithm must consider Steiner points instead of independently connecting terminal pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(3^k \cdot nm + 2^k \cdot nm \log(nm))$ | subset merges plus Dijkstra for each mask |
| Space | $O(2^k \cdot nm)$ | DP table and parent tracking |

With at most 128 masks and 200 vertices, the DP contains roughly 25,000 states. Dijkstra over such a small graph is extremely fast, so the solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    import heapq

    input = sys.stdin.readline
    INF = 10**18

    out = io.StringIO()
    sys.stdout = out

    n, m, k = map(int, input().split())

    grid = [list(map(int, input().split())) for _ in range(n)]

    terminals = []
    for _ in range(k):
        x, y = map(int, input().split())
        terminals.append((x - 1, y - 1))

    V = n * m

    def vid(x, y):
        return x * m + y

    cost = [0] * V

    for i in range(n):
        for j in range(m):
            cost[vid(i, j)] = grid[i][j]

    adj = [[] for _ in range(V)]

    for x in range(n):
        for y in range(m):
            v = vid(x, y)

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx = x + dx
                ny = y + dy

                if 0 <= nx < n and 0 <= ny < m:
                    adj[v].append(vid(nx, ny))

    FULL = 1 << k

    dp = [[INF] * V for _ in range(FULL)]

    for i, (x, y) in enumerate(terminals):
        dp[1 << i][vid(x, y)] = cost[vid(x, y)]

    for mask in range(FULL):

        sub = (mask - 1) & mask

        while sub:
            other = mask ^ sub

            for v in range(V):
                dp[mask][v] = min(
                    dp[mask][v],
                    dp[sub][v] + dp[other][v] - cost[v]
                )

            sub = (sub - 1) & mask

        pq = []

        for v in range(V):
            if dp[mask][v] < INF:
                heapq.heappush(pq, (dp[mask][v], v))

        while pq:
            dist, v = heapq.heappop(pq)

            if dist != dp[mask][v]:
                continue

            for to in adj[v]:
                nd = dist + cost[to]

                if nd < dp[mask][to]:
                    dp[mask][to] = nd
                    heapq.heappush(pq, (nd, to))

    ans = min(dp[FULL - 1])

    print(ans)

    sys.stdout = sys.__stdout__

    return out.getvalue().strip()

# provided sample
assert run(
"""3 3 2
1 2 3
1 2 3
1 2 3
1 2
3 3
"""
) == "9"

# minimum size
assert run(
"""1 1 1
5
1 1
"""
) == "5"

# adjacent terminals
assert run(
"""1 2 2
5 7
1 1
1 2
"""
) == "12"

# avoid expensive center
assert run(
"""2 3 3
1 100 1
1 1 1
1 1
1 3
2 2
"""
) == "5"

# all equal values
assert run(
"""2 2 2
1 1
1 1
1 1
2 2
"""
) == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1` grid | `5` | smallest possible state space |
| Adjacent terminals | `12` | endpoint costs counted correctly |
| Expensive center | `5` | Steiner routing avoids costly cells |
| All equal costs | `3` | multiple optimal paths handled correctly |

## Edge Cases

Consider the adjacent-terminal case:

```
1 2 2
5 7
1 1
1 2
```

Initialization creates:

```
dp[01][left] = 5
dp[10][right] = 7
```

Dijkstra propagation allows each state to reach the neighboring cell. When the two masks merge at either endpoint, the total becomes:

```
5 + 7 = 12
```

The subtraction during merging prevents double counting.

Now consider the expensive-center example:

```
2 3 3
1 100 1
1 1 1
1 1
1 3
2 2
```

A naive shortest-path union would use the top row and pay 102. The DP instead discovers that all subsets can merge cheaply along the second row:

```
X.X
XXX
```

with total cost 5.

Finally, consider a merge-heavy structure:

```
3 3 3
1 1 1
1 100 1
1 1 1
1 1
1 3
3 2
```

The optimal tree bends around the expensive center and merges at outer cells. During reconstruction, recursive calls follow both subset merges and movement transitions, correctly recovering the full connected structure without including the center cell.
