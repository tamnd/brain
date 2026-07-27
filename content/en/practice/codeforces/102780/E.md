---
title: "CF 102780E - Printed circuit board"
description: "The board is a drawing of wires placed on a rectangular grid. Each non-empty tile describes which sides of that tile contain wire segments."
date: "2026-07-27T20:09:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102780
codeforces_index: "E"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19)"
rating: 0
weight: 102780
solve_time_s: 93
verified: true
draft: false
---

[CF 102780E - Printed circuit board](https://codeforces.com/problemset/problem/102780/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The board is a drawing of wires placed on a rectangular grid. Each non-empty tile describes which sides of that tile contain wire segments. A command for the plotter starts at one grid position and gives a sequence of moves, so one command corresponds to walking along one continuous trail of the wire graph.

The task is not to recreate the picture in any particular order. We only need to split the existing wire into the smallest possible number of continuous trails and print those trails as commands. A trail may revisit a junction, but it may never draw a segment that was already drawn.

The natural model is a graph. Every occupied grid cell becomes a vertex. Every connection between two neighboring cells becomes an undirected edge. A command is exactly a walk over edges of this graph. The problem becomes finding the minimum number of trails that cover every edge once.

The grid dimensions are at most 100 by 100, so there are at most 10000 cells and roughly 20000 possible connections. This rules out approaches that repeatedly search over all possible decompositions or try permutations of edges. A graph traversal solution with linear complexity is easily fast enough.

Several details make this problem easier to get wrong. The coordinates in the output are column first and row second, while the input is read as rows. A careless implementation can swap them and produce invalid commands.

For example, consider:

```
1 3
r-*
```

The correct output can be:

```
1
1 1 RRU
```

The wire starts at the first cell, goes right through the middle cell, reaches the star, and the command must use coordinates as x y. A solution that treats input coordinates as x y would start at `(1, 3)`, which is outside the board.

Another edge case is a closed cycle:

```
3 3
*-*
|.|
L-J
```

The answer is one command, because all vertices have even degree and the whole component has an Euler circuit. A solution that only starts trails from odd degree vertices would output nothing and miss the cycle.

A third case is a crossing point:

```
5 5
..*..
..|..
*-*-*
..|..
..*..
```

The center star has degree four. It is not an endpoint. The correct answer is two commands, each being an Euler trail through part of the graph. Treating every star as a line endpoint gives too many commands.

## Approaches

A direct brute-force idea is to repeatedly pick an unused edge and search for the best way to continue drawing. This works because every valid command is a trail, and eventually every edge must be included. However, the number of possible choices grows explosively. With around 20000 edges, even considering only different starting points and local continuations already becomes impossible. The problem is not finding one valid drawing, but minimizing the number of trails.

The key observation is that the minimum number of trails in an undirected graph is determined only by vertex parity. Every trail changes parity at its two endpoints. A vertex with odd degree must be an endpoint of some trail. Since one trail contributes two endpoints, a connected component with `odd` odd-degree vertices needs at least `odd / 2` trails. If there are no odd-degree vertices, one Euler circuit is enough.

The remaining question is how to actually construct these trails. The graph is small enough for Hierholzer's algorithm, which builds Euler paths by following unused edges until returning to the start, then merging cycles. If a component has odd vertices, we start from them in pairs. If it has only even vertices, we start once from any vertex in that component.

The brute-force works because it tries to reason about the order of edges. The parity observation removes that search completely and reduces the problem to finding Euler trails in each connected component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of edges | O(V + E) | Too slow |
| Optimal | O(V + E) | O(V + E) | Accepted |

## Algorithm Walkthrough

1. Parse every tile and create the graph. Each occupied tile is a vertex. Whenever two neighboring tiles both claim a connection between them, add one undirected edge.

The graph representation is useful because the plotter's movement is exactly movement along graph edges. The original drawing symbols only describe local connections, so after conversion the geometry is no longer needed.

1. Find every connected component containing at least one edge. During traversal of a component, collect all vertices with odd degree.

Only vertices with odd degree affect the number of commands. Even degree vertices can be entered and left without forcing a new trail.

1. For each component, choose starting points for Euler trails. If the component has odd vertices, use them as starts. If it has no odd vertices, choose any vertex in the component.

This gives the minimum number of trails. Odd vertices must appear as endpoints, while an all-even component has one closed Euler trail.

1. Run Hierholzer's algorithm from every chosen start. Each traversal consumes unused edges and records the sequence of visited vertices.

Every edge is removed exactly once, so no command can draw over an existing line.

1. Convert each vertex sequence into a command. The first vertex becomes the output coordinate. Consecutive vertices determine the movement letters.

The graph uses row and column internally, but the output requires column then row, so the conversion happens only when printing.

Why it works:

For any connected component, every trail has exactly two endpoints unless it is a closed trail. Odd-degree vertices cannot be internal points of all trails because entering and leaving already uses two incident edges. Thus at least half of the odd vertices are required as trail endpoints. The algorithm creates exactly that many trails by starting from odd vertices, or exactly one trail when there are no odd vertices.

Hierholzer's algorithm is valid because it always follows unused edges and produces an Euler trail whenever the required parity conditions hold. Since every component is processed separately, every edge in the drawing is included exactly once and the number of commands is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    board = [input().rstrip("\n") for _ in range(n)]

    dirs = {
        '-': [(0, -1), (0, 1)],
        '|': [(-1, 0), (1, 0)],
        'L': [(-1, 0), (0, 1)],
        'J': [(-1, 0), (0, -1)],
        'r': [(1, 0), (0, 1)],
        '7': [(1, 0), (0, -1)],
        '*': [(-1, 0), (1, 0), (0, -1), (0, 1)]
    }

    rev = {
        (-1, 0): (1, 0),
        (1, 0): (-1, 0),
        (0, -1): (0, 1),
        (0, 1): (0, -1)
    }

    adj = [[] for _ in range(n * m)]

    def node(r, c):
        return r * m + c

    for r in range(n):
        for c in range(m):
            if board[r][c] == '.':
                continue
            for dr, dc in dirs[board[r][c]]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and board[nr][nc] != '.':
                    if rev[(dr, dc)] in dirs[board[nr][nc]]:
                        if node(r, c) < node(nr, nc):
                            a, b = node(r, c), node(nr, nc)
                            adj[a].append(b)
                            adj[b].append(a)

    used = [False] * n * m
    edge_used = [False] * sum(len(x) for x in adj) 
    edge_id = {}
    eid = 0
    for u in range(n * m):
        for v in adj[u]:
            if u < v:
                edge_id[(u, v)] = eid
                edge_id[(v, u)] = eid
                eid += 1

    for u in range(n * m):
        for i, v in enumerate(adj[u]):
            adj[u][i] = (v, edge_id[(u, v)])

    def hierholzer(start):
        stack = [(start, -1)]
        path = []
        while stack:
            u, incoming = stack[-1]
            while adj[u] and edge_used[adj[u][-1][1]]:
                adj[u].pop()
            if adj[u]:
                v, e = adj[u].pop()
                if edge_used[e]:
                    continue
                edge_used[e] = True
                stack.append((v, e))
            else:
                path.append(u)
                stack.pop()
        path.reverse()
        return path

    result = []
    visited = [False] * (n * m)

    for s in range(n * m):
        if board[s // m][s % m] != '.' and not visited[s]:
            stack = [s]
            comp = []
            visited[s] = True
            while stack:
                u = stack.pop()
                comp.append(u)
                for v, _ in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        stack.append(v)

            starts = [u for u in comp if len(adj[u]) % 2 == 1]
            if not starts:
                starts = [comp[0]]

            for start in starts:
                path = hierholzer(start)
                if len(path) > 1:
                    result.append(path)

    def direction(a, b):
        ar, ac = divmod(a, m)
        br, bc = divmod(b, m)
        if br == ar - 1:
            return 'U'
        if br == ar + 1:
            return 'D'
        if bc == ac - 1:
            return 'L'
        return 'R'

    out = [str(len(result))]
    for path in result:
        r, c = divmod(path[0], m)
        moves = ''.join(direction(path[i], path[i + 1])
                        for i in range(len(path) - 1))
        out.append(f"{c + 1} {r + 1} {moves}")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part converts the picture into an adjacency list. The special handling of `*` is deliberate: a star does not tell us which directions are used, but it can only be connected to actual neighboring wire tiles, so allowing all four directions and validating the neighbor gives the correct edges.

The edge IDs allow Hierholzer's algorithm to mark an edge once even though every edge appears twice in the adjacency lists. Removing entries while traversing also avoids scanning already exhausted edges repeatedly.

The component search is performed before creating trails because Euler conditions apply separately to each connected part of the drawing. The output conversion adds one to both coordinates because the input and internal arrays are zero-indexed while the problem uses one-indexed coordinates.

## Worked Examples

For the first sample:

```
3 4
r--*
*...
L--*
```

The graph has one connected component. Its odd vertices are the three stars? Actually the bottom and top stars plus the isolated-looking middle left star connect into the same component, giving four odd vertices. The algorithm creates two trails.

| Step | Component vertices | Odd starts | Generated path |
| --- | --- | --- | --- |
| Build graph | All non-empty cells connected | Four endpoints | Not yet |
| Choose starts | Star cells with odd degree | Two starts per pair | Pairing is arbitrary |
| Euler traversal | Consume every edge once | None remaining | Two command paths |

This demonstrates that the algorithm does not need to preserve the original drawing order. Any minimum set of commands is valid.

For the second sample:

```
4 3
r--*
L--7
*--J
```

The component forms a closed loop. Every vertex has even degree, so the algorithm chooses one arbitrary start and creates one Euler circuit.

| Step | Component vertices | Odd starts | Generated path |
| --- | --- | --- | --- |
| Build graph | One cycle | Empty | Need one circuit |
| Choose starts | First occupied cell | One start | Euler traversal begins |
| Euler traversal | All edges consumed | None | One closed command |

This confirms the special handling of all-even components.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every tile and every edge is processed a constant number of times |
| Space | O(nm) | The graph, visited arrays, and traversal state are linear in the number of cells |

The largest board contains only 10000 cells, so a linear graph traversal easily fits the one second time limit and the 64 MB memory limit.

## Test Cases

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
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("""3 4
r--*
*...
L--*
""").splitlines()[0] == "2"

assert run("""4 3
r--*
L--7
*--J
""").splitlines()[0] == "1"

assert run("""1 3
r-*
""").splitlines()[0] == "1"

assert run("""1 1
*
""") == "0"

assert run("""5 5
..*..
..|..
*-*-*
..|..
..*..
""").splitlines()[0] == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First sample | Two commands | Multiple odd-degree endpoints |
| Second sample | One command | Euler circuit handling |
| Single horizontal segment | One command | Coordinate and direction conversion |
| Single star | Zero commands | Empty graph handling |
| Cross shaped drawing | Two commands | Degree four intersections |

## Edge Cases

The isolated star case:

```
1 1
*
```

contains a marked point but no wire segment. The graph has no edges, so no command is needed. The algorithm never starts Hierholzer's traversal because there is no component with edges.

The closed loop case:

```
3 3
*-*
|.|
L-J
```

has no odd-degree vertices. The component traversal finds an empty odd list and selects one arbitrary cell as the Euler start. Hierholzer consumes the entire loop and returns one command.

The crossing case:

```
5 5
..*..
..|..
*-*-*
..|..
..*..
```

contains a center vertex of degree four. Its degree is even, so it does not increase the number of commands. The component has four odd endpoints, which forces two trails. The algorithm starts from those endpoints and covers every branch exactly once.

The coordinate boundary case:

```
1 3
r-*
```

uses cells on the edge of the board. Direction generation only compares neighboring indices, so it never moves outside the array. The final output swaps the internal row and column order correctly before printing.
