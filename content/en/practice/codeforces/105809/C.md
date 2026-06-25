---
title: "CF 105809C - Chess in 3D"
description: "We have a three dimensional chessboard with dimensions $A times B times C$. Some cells are blocked and cannot contain a knight. Every remaining cell is a potential position for a 3D knight."
date: "2026-06-25T15:28:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105809
codeforces_index: "C"
codeforces_contest_name: "Code Rush 2025"
rating: 0
weight: 105809
solve_time_s: 54
verified: true
draft: false
---

[CF 105809C - Chess in 3D](https://codeforces.com/problemset/problem/105809/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a three dimensional chessboard with dimensions $A \times B \times C$. Some cells are blocked and cannot contain a knight. Every remaining cell is a potential position for a 3D knight.

A knight moves exactly as described by the usual chess pattern extended into three dimensions. It chooses two axes, moves by 2 along one of them and by 1 along the other, while the third coordinate stays unchanged. Any move that leaves the board is invalid. The goal is to place as many knights as possible so that no two knights attack each other in a single move.

The board dimensions are at most 10 in each direction, so the entire board contains at most $10^3 = 1000$ cells. Even before removing blocked cells, the number of usable positions is small enough that we can think in terms of graph vertices. The challenge is not the number of cells, but the combinatorial nature of choosing a largest non-attacking subset.

A naive search over all subsets would require examining up to $2^{1000}$ configurations, which is completely impossible. We need to exploit structure in the knight-move graph.

One subtle case appears when the board is so small that no knight move exists.

Example:

```
1 1 1
1
1 1 1
```

There are no usable cells, so the answer is 0. A solution that assumes at least one knight can be placed would fail.

Another interesting case is a board with available cells but no attacking pairs.

```
1 1 2
1
1 1 1
```

Only one usable cell remains. The answer is 1. Any graph-based solution must correctly handle isolated vertices.

A more dangerous mistake is forgetting to remove blocked cells from the graph. Consider:

```
3 3 3
1
2 2 2
```

The center cell is unavailable. If we still create edges through that vertex or count it as a candidate position, the final answer becomes too large or too small depending on the implementation. The correct answer is 14.

## Approaches

The most direct interpretation is to build a graph where every usable cell is a vertex and an edge connects two cells if knights placed there attack each other. The task then becomes finding the largest set of vertices with no edge between any pair. In graph theory, that is a maximum independent set.

The brute-force approach would try every subset of usable cells and check whether any attacking pair exists. If there are $N$ usable cells, this requires $2^N$ subsets. Even for $N = 50$, this is already hopeless, while the actual limit is up to 1000 cells.

The key observation comes from the parity of coordinates.

A knight move changes coordinates by $(\pm2,\pm1,0)$ in some order. The total change in $x+y+z$ is always odd because $2+1=3$. That means every knight move flips the parity of $x+y+z$.

If we color every cell according to the parity of $x+y+z$, every edge connects opposite colors. The attack graph is bipartite.

Now the problem becomes much easier because of a classical theorem. In any graph:

$$\text{Maximum Independent Set}
=
|V|
-
\text{Minimum Vertex Cover}$$

For bipartite graphs, König's theorem states:

$$\text{Minimum Vertex Cover}
=
\text{Maximum Matching}$$

Combining both facts:

$$\text{Answer}
=
|V|
-
\text{Maximum Matching}$$

So instead of searching for a largest independent set directly, we build the bipartite graph of knight attacks, compute a maximum matching, and subtract its size from the number of usable cells.

The board has at most 1000 usable cells. Each cell has only a constant number of knight moves, so the graph remains sparse. Hopcroft-Karp easily handles this size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N)$ | $O(N)$ | Too slow |
| Optimal | $O(E\sqrt{V})$ | $O(V+E)$ | Accepted |

## Algorithm Walkthrough

1. Read the board dimensions and mark all blocked cells.
2. Assign an integer id to every usable cell. These ids become graph vertices.
3. Split vertices into two partitions according to the parity of $x+y+z$.
4. For every usable cell in the even partition, generate all possible knight moves.
5. If a destination cell is inside the board and not blocked, add an edge between the two corresponding vertices.
6. Run Hopcroft-Karp on the resulting bipartite graph to compute the maximum matching.
7. Let $N$ be the number of usable cells and $M$ be the maximum matching size.
8. Output $N-M$.

The reason step 8 is correct is the chain of equalities:

$$\text{Maximum Independent Set}
=
N-\text{Minimum Vertex Cover}
=
N-\text{Maximum Matching}$$

### Why it works

Every knight move changes parity, so the attack graph is bipartite. Any valid knight placement corresponds exactly to an independent set in this graph because no two selected vertices may share an attack edge.

For bipartite graphs, König's theorem converts the minimum vertex cover problem into a maximum matching problem. Since the complement of a minimum vertex cover is a maximum independent set, subtracting the matching size from the total number of vertices gives the largest possible set of mutually non-attacking knights. No valid placement can contain more vertices than this value, and the theorem guarantees that such a placement exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    A, B, C = map(int, input().split())
    K = int(input())

    blocked = set()
    for _ in range(K):
        x, y, z = map(int, input().split())
        blocked.add((x - 1, y - 1, z - 1))

    cell_id = {}
    cells = []

    for x in range(A):
        for y in range(B):
            for z in range(C):
                if (x, y, z) not in blocked:
                    cell_id[(x, y, z)] = len(cells)
                    cells.append((x, y, z))

    n = len(cells)

    moves = []
    for axis2 in [2, -2]:
        for axis1 in [1, -1]:
            moves.extend([
                (axis2, axis1, 0),
                (axis2, 0, axis1),
                (axis1, axis2, 0),
                (0, axis2, axis1),
                (axis1, 0, axis2),
                (0, axis1, axis2),
            ])

    left_vertices = []
    for idx, (x, y, z) in enumerate(cells):
        if (x + y + z) % 2 == 0:
            left_vertices.append(idx)

    adj = [[] for _ in range(n)]

    for idx in left_vertices:
        x, y, z = cells[idx]

        for dx, dy, dz in moves:
            nx, ny, nz = x + dx, y + dy, z + dz

            if not (0 <= nx < A and 0 <= ny < B and 0 <= nz < C):
                continue

            if (nx, ny, nz) not in cell_id:
                continue

            adj[idx].append(cell_id[(nx, ny, nz)])

    INF = 10 ** 18

    pair_u = [-1] * n
    pair_v = [-1] * n
    dist = [0] * n

    def bfs():
        q = deque()

        for u in left_vertices:
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF

        found = False

        while q:
            u = q.popleft()

            for v in adj[u]:
                pu = pair_v[v]

                if pu == -1:
                    found = True
                elif dist[pu] == INF:
                    dist[pu] = dist[u] + 1
                    q.append(pu)

        return found

    def dfs(u):
        for v in adj[u]:
            pu = pair_v[v]

            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pair_u[u] = v
                pair_v[v] = u
                return True

        dist[u] = INF
        return False

    matching = 0

    while bfs():
        for u in left_vertices:
            if pair_u[u] == -1 and dfs(u):
                matching += 1

    print(n - matching)

solve()
```

The first part constructs the set of usable cells and assigns each one a compact vertex id. Working with integer ids makes the matching implementation much simpler.

The move generation explicitly creates all 24 knight moves in three dimensions. Several implementations accidentally miss some coordinate permutations, which produces a graph with missing edges and an answer that is too large.

Only even-parity vertices create outgoing edges. This avoids storing every edge twice and naturally forms the left side of the bipartite graph.

The Hopcroft-Karp implementation uses the standard BFS layering phase followed by DFS augmentation. The graph is sparse, so this runs comfortably within the limits.

A common source of bugs is forgetting that blocked cells do not exist as vertices. Every destination must be checked against `cell_id` before adding an edge.

## Worked Examples

### Example 1

```
1 1 2
1
1 1 1
```

Usable cells:

| Cell | Parity |
| --- | --- |
| (1,1,2) | odd |

There are no knight moves.

| Quantity | Value |
| --- | --- |
| Usable vertices | 1 |
| Matching size | 0 |
| Answer | 1 |

This demonstrates that isolated vertices automatically belong to the maximum independent set.

### Example 2

```
3 3 3
1
2 2 2
```

There are 26 cells total and one blocked cell.

| Quantity | Value |
| --- | --- |
| Total cells | 27 |
| Blocked cells | 1 |
| Usable vertices | 26 |

Running Hopcroft-Karp finds:

| Quantity | Value |
| --- | --- |
| Maximum matching | 12 |
| Answer | 14 |

The result matches the sample output.

This example demonstrates the full reduction from knight placement to bipartite matching.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(E\sqrt{V})$ | Hopcroft-Karp maximum matching |
| Space | $O(V+E)$ | Graph storage and matching arrays |

The board contains at most 1000 usable cells. Each cell has at most 24 knight moves, so $E$ is only a few tens of thousands. Hopcroft-Karp on a graph of this size is easily fast enough for a one second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    from collections import deque

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    A, B, C = map(int, input().split())
    K = int(input())

    blocked = set()
    for _ in range(K):
        x, y, z = map(int, input().split())
        blocked.add((x - 1, y - 1, z - 1))

    cell_id = {}
    cells = []

    for x in range(A):
        for y in range(B):
            for z in range(C):
                if (x, y, z) not in blocked:
                    cell_id[(x, y, z)] = len(cells)
                    cells.append((x, y, z))

    n = len(cells)

    moves = []
    for a in [2, -2]:
        for b in [1, -1]:
            moves.extend([
                (a, b, 0),
                (a, 0, b),
                (b, a, 0),
                (0, a, b),
                (b, 0, a),
                (0, b, a),
            ])

    left = [i for i, (x, y, z) in enumerate(cells)
            if (x + y + z) % 2 == 0]

    adj = [[] for _ in range(n)]

    for u in left:
        x, y, z = cells[u]
        for dx, dy, dz in moves:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) in cell_id:
                adj[u].append(cell_id[(nx, ny, nz)])

    INF = 10**18
    pair_u = [-1] * n
    pair_v = [-1] * n
    dist = [0] * n

    def bfs():
        q = deque()
        found = False

        for u in left:
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF

        while q:
            u = q.popleft()
            for v in adj[u]:
                pu = pair_v[v]
                if pu == -1:
                    found = True
                elif dist[pu] == INF:
                    dist[pu] = dist[u] + 1
                    q.append(pu)
        return found

    def dfs(u):
        for v in adj[u]:
            pu = pair_v[v]
            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in left:
            if pair_u[u] == -1 and dfs(u):
                matching += 1

    return str(n - matching) + "\n"

# sample
assert run("3 3 3\n1\n2 2 2\n") == "14\n"

# minimum usable board
assert run("1 1 1\n1\n1 1 1\n") == "0\n"

# single available cell
assert run("1 1 2\n1\n1 1 1\n") == "1\n"

# no knight moves anywhere
assert run("2 2 2\n1\n1 1 1\n") == "7\n"

# one-dimensional line
assert run("1 1 3\n1\n1 1 1\n") == "2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1×1 fully blocked | 0 | Empty graph |
| 1×1×2 with one blocked cell | 1 | Single isolated vertex |
| 2×2×2 | 7 | No valid knight moves exist |
| 1×1×3 | 2 | Degenerate dimension handling |
| Sample case | 14 | Full matching logic |

## Edge Cases

Consider the completely blocked board:

```
1 1 1
1
1 1 1
```

No vertices are created. The matching size is 0 and the algorithm outputs $0 - 0 = 0$. The empty placement is the only valid placement.

Consider a board with one available cell:

```
1 1 2
1
1 1 1
```

The graph contains one vertex and no edges. Hopcroft-Karp finds no matching. The answer becomes $1 - 0 = 1$, which is optimal because the lone cell can always contain a knight.

Consider the sample:

```
3 3 3
1
2 2 2
```

The blocked center cell is never inserted into the graph. Every attack edge is generated only between usable cells. The matching size is 12, so the maximum independent set size is $26 - 12 = 14$. This confirms that blocked cells are handled correctly and do not participate in either the graph or the final count.
