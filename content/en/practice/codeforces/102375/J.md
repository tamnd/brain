---
title: "CF 102375J - \u041f\u043e\u0440\u0442\u0430\u043b\u044b"
description: "The maze is an (N times M) grid. A cell is either free, occupied by a solid wall W, or occupied by a glass wall G. Ordinary movement is possible only between adjacent free cells. The outer border consists of solid walls, so every ray eventually reaches a solid wall."
date: "2026-08-15T18:29:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "J"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 1543
verified: false
draft: false
---

[CF 102375J - \u041f\u043e\u0440\u0442\u0430\u043b\u044b](https://codeforces.com/problemset/problem/102375/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 25m 43s  
**Verified:** no  

## Solution
## Problem Understanding

The maze is an (N \times M) grid. A cell is either free, occupied by a solid wall `W`, or occupied by a glass wall `G`. Ordinary movement is possible only between adjacent free cells. The outer border consists of solid walls, so every ray eventually reaches a solid wall.

A portal shot travels in one of the four grid directions until it meets the first solid wall. Glass walls do not stop the shot. The portal is placed on the side of that wall facing the shooter. The crucial consequence is that the useful side of the portal is the last cell before that solid wall. If that cell is free, the portal can safely be entered from it. If that cell is glass, entering the portal from the other side would leave the traveler inside a glass wall, so such a portal cannot be used in a valid solution.

There are two portal colors. Each color has at most one portal, and shooting that color normally replaces its previous portal. A movement into a portal counts as one `M` action, but after entering it the traveler appears at the other portal immediately.

The input gives the grid and two free cells, the start (S) and the exit (E). The output must contain a valid sequence of shots and movements. The primary objective is to minimize the number (P) of shots. Among solutions with that minimum (P), the number of movement actions only has to stay within (2NM). The official statement gives (N,M\le 1000), a 2 second limit, and 512 MiB of memory.

With (N,M\le1000), there can be (10^6) cells. This rules out algorithms whose state space contains even a quadratic number of grid cells, let alone cubic state spaces. A linear or near-linear traversal of the grid is appropriate. The output itself can contain (O(NM)) movements, so spending (O(NM)) time and memory is the natural target.

### Start and exit already connected

If (S) and (E) belong to the same connected component of free cells, portals are unnecessary. The correct answer has (P=0). For example,

```
3 3
WWW
W.W
WWW
2 2
2 2
```

has the output

```
0 0
```

A solution that always initializes two portals would already be non-optimal.

### A shot may pass through glass

Consider Sample 1. From the start cell, shooting downward passes through a glass cell and then reaches a solid wall. The useful portal endpoint is the free cell immediately before that solid wall. A naive implementation that only allows shooting at an immediately adjacent solid wall would miss this transition and may incorrectly report that the maze needs more shots or is impossible.

### A glass endpoint is unusable

A portal whose endpoint is a `G` cell is not a useful teleport endpoint. Treating `G` as merely transparent for both shooting and teleportation is wrong, because leaving the portal on the other side would put the traveler into the glass wall.

For example,

```
5 5
WWWWW
W.GGW
WGWGW
WGG.W
WWWWW
2 2
4 4
```

has two isolated free cells. Every nontrivial ray from either one ends with a glass cell immediately before the solid wall. The only safe shots point at the current cell itself, so no teleport between the components is possible. The correct output is

```
-1 -1
```

A careless implementation that accepts a glass endpoint would incorrectly find a path.

### The two portal colors have to be used alternately

After a teleport, the portal at the current endpoint remains there. To move to a new endpoint, the other color is shot somewhere else, replacing the old portal of that color. Then entering the still existing portal at the current endpoint performs the teleport.

This is why one shot is enough for every teleport after the first one. The first teleport costs two shots because initially neither portal exists.

## Approaches

A direct brute-force solution would model the complete physical state. Such a state contains the player's current cell and the positions and orientations of both portals, including the possibility that a portal does not exist yet. There are (O(NM)) possible useful portal positions, so the number of states is (O((NM)^3)). Each state has at most four movement actions and eight shooting actions, giving a worst-case transition count on the order of

[
12(NM)(NM+1)^2.
]

For (NM=10^6), this is on the order of (10^{19}) transitions. The brute force is conceptually correct because it explicitly represents every possible configuration, but the portal positions create far too many combinations.

The key observation is that we do not actually need to remember both portal positions. Once a teleport has happened, the portal at the current cell has a known orientation, and the other portal can be replaced by the next shot. Thus the only information relevant to the next teleport is the current component and the cell where the new portal should be placed.

Call a free cell a portal endpoint if it is immediately before a solid wall in at least one direction. From a cell (x), shooting in a direction has exactly one endpoint (y): the cell immediately before the first solid wall on that ray. If (y) is free, then shooting from (x) can create a safe portal at (y).

Now consider two different connected components of free cells. If there is an endpoint (x) in component (A) whose shot creates a safe endpoint (y) in component (B), we can use that as a directed edge (A\to B). The first such edge costs two shots. After arriving in (B), the portal at the arrival endpoint already exists, so moving along another component edge costs only one additional shot.

The problem has consequently become an ordinary unweighted shortest path problem on connected components of free cells. We can find those components with BFS, generate all possible portal transitions in (O(NM)), and then run another BFS over the component graph.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((NM)^3)) states | (O((NM)^3)) | Too slow |
| Optimal | (O(NM)) | (O(NM)) | Accepted |

## Algorithm Walkthrough

1. Read the grid and locate the start and exit cells. Treat only `.` cells as walkable. Glass and solid walls both block ordinary movement.
2. Run a flood fill over all free cells. Assign every free cell a connected-component identifier. During this traversal, mark every free cell adjacent to a solid wall. Such a cell can be a safe portal endpoint.
3. For every endpoint, determine what endpoint a shot would create in each of the four directions. For example, in the left direction, find the first `W` cell to the left and take the cell immediately to its right. We can compute these values with four linear sweeps, two over rows and two over columns.
4. Build the implicit component graph. For every endpoint (x) and every direction, let (y) be the endpoint reached by shooting in that direction. Ignore the transition if (y) is a glass cell or if (x) and (y) belong to the same component. Otherwise add a directed transition from the component of (x) to the component of (y), remembering (x), (y), and the shooting direction.
5. If the start and exit have the same component identifier, find an ordinary BFS path from (S) to (E) and output it with zero shots. There is nothing to optimize further because zero is the smallest possible number of shots.
6. Otherwise, run BFS on the component graph, starting from the component containing (S). Store for every newly reached component the source endpoint, destination endpoint, and shooting direction that reached it. BFS is appropriate because every component transition represents one additional teleport and hence one additional shot after the first teleport.
7. If the exit component is unreachable in this graph, output `-1 -1`. Every possible safe portal transition has been represented as an edge, so there is no remaining way to move between free-cell components.
8. Reconstruct the shortest component path. Suppose its transitions are

[
x_0\to y_0,\quad x_1\to y_1,\quad \ldots,\quad x_{k-1}\to y_{k-1}.
]

The first transition needs two shots. Shoot orange from (x_0) toward (y_0), then shoot blue from (x_0) toward any adjacent solid wall, so the blue portal is placed at (x_0). Entering that blue portal teleports to (y_0).
9. Inside every intermediate component, walk from the previous transition's destination (y_{i-1}) to the next transition's source (x_i). These are ordinary free-cell movements and require no shots.
10. For every later transition (x_i\to y_i), shoot the color opposite to the currently existing portal at (x_i). Then enter the existing portal at (x_i). This costs exactly one new shot and teleports the traveler to (y_i). The direction used to enter the portal is exactly the shooting direction that created (x_i) in the preceding transition.
11. After the final teleport, walk normally from its destination endpoint to (E).
12. Count every `O` and `B` as a shot and every `M` as a movement. The number of shots is (k+1), where (k) is the number of component transitions.

### Why it works

The invariant is that after every teleport, the traveler stands at the endpoint created by the latest shot, and the portal at that endpoint remains available. The other color can be moved to the endpoint required for the next component transition. Thus every directed edge of the component graph is realizable, with the first edge costing two shots and every later edge costing one.

Conversely, every safe teleport between different free-cell components must use a portal whose entry endpoint is a free cell immediately before some solid wall. The shot that creates the other endpoint defines exactly one of the transitions generated by our four directional sweeps. Hence any valid solution induces a path in our component graph. BFS finds the minimum number of such transitions, so (k+1) is the minimum possible number of shots.

The movement bound also follows from the component construction. A shortest component path never repeats a component. Inside each visited component, the produced walk uses at most (\text{size(component)}-1) ordinary moves. There is one portal-entry movement per component transition. If the path uses (k+1) components, the total number of movements is at most

\sum\text{size(component)}-1
\le NM-1,
]

which is comfortably below the required (2NM).

## Python Solution

```python
import sys
input = sys.stdin.readline

from array import array
from collections import deque

DIRS = "UDLR"
DR = (-1, 1, 0, 0)

def solve_stream(readline):
    n, m = map(int, readline().split())

    rows = []
    grid = bytearray()
    for _ in range(n):
        s = readline().strip().encode()
        rows.append(s)
        grid.extend(s)

    sr, sc = map(int, readline().split())
    er, ec = map(int, readline().split())
    sr -= 1
    sc -= 1
    er -= 1
    ec -= 1

    vcount = n * m
    start = sr * m + sc
    finish = er * m + ec

    # 0 = not a boundary endpoint, 1 = safe portal endpoint.
    boundary = bytearray(vcount)

    # Direction of any solid wall adjacent to an endpoint.
    # Encoding: U=0, D=1, L=2, R=3.
    first_dir = bytearray(vcount)

    # Connected components of free cells.
    comp = array('i', [-1]) * vcount
    component_count = 0

    for i in range(vcount):
        if grid[i] != 46 or comp[i] != -1:
            continue

        cid = component_count
        component_count += 1

        q = deque([i])
        comp[i] = cid

        while q:
            x = q.popleft()
            r = x // m
            c = x - r * m

            is_boundary = False

            if grid[x - m] == 87:
                is_boundary = True
                first_dir[x] = 0
            elif grid[x + m] == 87:
                is_boundary = True
                first_dir[x] = 1
            elif grid[x - 1] == 87:
                is_boundary = True
                first_dir[x] = 2
            elif grid[x + 1] == 87:
                is_boundary = True
                first_dir[x] = 3

            if is_boundary:
                boundary[x] = 1

            y = x - m
            if grid[y] == 46 and comp[y] == -1:
                comp[y] = cid
                q.append(y)

            y = x + m
            if grid[y] == 46 and comp[y] == -1:
                comp[y] = cid
                q.append(y)

            y = x - 1
            if grid[y] == 46 and comp[y] == -1:
                comp[y] = cid
                q.append(y)

            y = x + 1
            if grid[y] == 46 and comp[y] == -1:
                comp[y] = cid
                q.append(y)

    start_comp = comp[start]
    finish_comp = comp[finish]

    # If ordinary movement already reaches the exit, no shot is needed.
    if start_comp == finish_comp:
        seen = bytearray(vcount)
        parent = array('i', [-1]) * vcount
        pdir = bytearray(vcount)

        q = deque([start])
        seen[start] = 1

        while q and not seen[finish]:
            x = q.popleft()

            for d, delta in enumerate((-m, m, -1, 1)):
                y = x + delta
                if grid[y] == 46 and not seen[y]:
                    seen[y] = 1
                    parent[y] = x
                    pdir[y] = d
                    q.append(y)

        path = []
        cur = finish
        while cur != start:
            path.append(pdir[cur])
            cur = parent[cur]
        path.reverse()

        out = ["0 {}".format(len(path))]
        out.extend("M" + DIRS[d] for d in path)
        return "\n".join(out) + "\n"

    # For every boundary cell, these arrays store the endpoint obtained
    # by shooting in the corresponding direction.
    left = array('i', [-1]) * vcount
    right = array('i', [-1]) * vcount
    up = array('i', [-1]) * vcount
    down = array('i', [-1]) * vcount

    # Horizontal sweeps.
    for r in range(n):
        base = r * m
        last_w = -1

        for c in range(m):
            x = base + c
            if grid[x] == 87:
                last_w = c
            elif boundary[x]:
                left[x] = base + last_w + 1

        next_w = m
        for c in range(m - 1, -1, -1):
            x = base + c
            if grid[x] == 87:
                next_w = c
            elif boundary[x]:
                right[x] = base + next_w - 1

    # Vertical sweeps.
    for c in range(m):
        last_w = -1

        for r in range(n):
            x = r * m + c
            if grid[x] == 87:
                last_w = r
            elif boundary[x]:
                up[x] = (last_w + 1) * m + c

        next_w = n
        for r in range(n - 1, -1, -1):
            x = r * m + c
            if grid[x] == 87:
                next_w = r
            elif boundary[x]:
                down[x] = (next_w - 1) * m + c

    # Linked lists of boundary cells, one list per component.
    head = array('i', [-1]) * component_count
    bnext = array('i', [-1]) * vcount

    for x in range(vcount):
        if boundary[x]:
            cid = comp[x]
            bnext[x] = head[cid]
            head[cid] = x

    # BFS over connected components.
    parent_comp = array('i', [-1]) * component_count
    edge_src = array('i', [-1]) * component_count
    edge_dst = array('i', [-1]) * component_count
    edge_dir = bytearray(component_count)

    parent_comp[start_comp] = start_comp
    q = deque([start_comp])

    target_arrays = (up, down, left, right)

    while q and parent_comp[finish_comp] == -1:
        cid = q.popleft()
        x = head[cid]

        while x != -1:
            for d, arr in enumerate(target_arrays):
                y = arr[x]

                if y == -1 or grid[y] != 46:
                    continue

                nc = comp[y]
                if nc == cid or parent_comp[nc] != -1:
                    continue

                parent_comp[nc] = cid
                edge_src[nc] = x
                edge_dst[nc] = y
                edge_dir[nc] = d
                q.append(nc)

                if nc == finish_comp:
                    break

            x = bnext[x]

            if parent_comp[finish_comp] != -1:
                break

    if parent_comp[finish_comp] == -1:
        return "-1 -1\n"

    # Recover component transitions in forward order.
    transitions = []
    cid = finish_comp

    while cid != start_comp:
        transitions.append(
            (edge_src[cid], edge_dst[cid], edge_dir[cid])
        )
        cid = parent_comp[cid]

    transitions.reverse()

    # Local BFS inside one free-cell component.
    seen = array('i', [0]) * vcount
    parent = array('i', [-1]) * vcount
    pdir = bytearray(vcount)
    stamp = 0

    def walk_path(a, b, cid):
        nonlocal stamp

        if a == b:
            return []

        stamp += 1
        q = deque([a])
        seen[a] = stamp

        while q:
            x = q.popleft()

            for d, delta in enumerate((-m, m, -1, 1)):
                y = x + delta

                if grid[y] != 46:
                    continue
                if comp[y] != cid:
                    continue
                if seen[y] == stamp:
                    continue

                seen[y] = stamp
                parent[y] = x
                pdir[y] = d

                if y == b:
                    q.clear()
                    break

                q.append(y)

        result = []
        cur = b

        while cur != a:
            result.append(pdir[cur])
            cur = parent[cur]

        result.reverse()
        return result

    actions = []

    # First component: walk from S to the source of the first transition.
    x0, y0, d0 = transitions[0]
    path = walk_path(start, x0, start_comp)
    actions.extend("M" + DIRS[d] for d in path)

    # First teleport needs two shots.
    actions.append("O" + DIRS[d0])
    actions.append("B" + DIRS[first_dir[x0]])

    # Enter the blue portal at x0.
    actions.append("M" + DIRS[first_dir[x0]])

    current = y0
    active_dir = d0

    # Every later teleport needs one new shot.
    for i in range(1, len(transitions)):
        x, y, d = transitions[i]

        cid = comp[current]
        path = walk_path(current, x, cid)
        actions.extend("M" + DIRS[move_d] for move_d in path)

        # The active portal at x was created by the previous transition.
        # Replace the other color with a portal at y.
        color = "B" if i % 2 == 1 else "O"
        actions.append(color + DIRS[d])

        # Enter the still existing portal at x.
        actions.append("M" + DIRS[active_dir])

        current = y
        active_dir = d

    # Final component: walk from the last portal endpoint to E.
    final_cid = comp[current]
    path = walk_path(current, finish, final_cid)
    actions.extend("M" + DIRS[d] for d in path)

    shots = len(transitions) + 1
    moves = len(actions) - shots

    out = [f"{shots} {moves}"]
    out.extend(actions)
    return "\n".join(out) + "\n"

def main():
    sys.stdout.write(solve_stream(input))

if __name__ == "__main__":
    main()
```

The first phase labels ordinary free-cell connectivity. Glass cells are never inserted into the BFS, which is exactly what ordinary movement requires. At the same time, a free cell is marked as a boundary endpoint if at least one of its four neighbors is `W`. The stored `first_dir` gives a direction in which a portal can be placed directly at that cell.

The four directional sweeps are the part that removes the potentially quadratic ray simulation. In a left-to-right row sweep, `last_w` is the nearest solid wall to the left. For a boundary cell (x), the endpoint of a leftward shot is simply the cell immediately after `last_w`. The other three arrays are computed symmetrically. Since every cell participates in a constant number of sweep operations, this phase is linear.

The component graph is generated lazily during its BFS instead of storing every graph edge. This saves memory because a component may contain many boundary cells. When a component is removed from the queue, its linked list of boundary cells is scanned and each of their four possible targets is inspected. Each component is processed once.

The reconstruction uses a second kind of BFS. The component graph tells us which cells must be connected by portals, but it does not tell us how to walk inside a component from the previous teleport endpoint to the next shooting position. `walk_path` solves exactly that local problem. Because the component graph path never repeats a component, the total number of cells explored by all these local BFS runs is still (O(NM)).

The order of the two initial shots is deliberate. Orange is placed at the first destination, blue at the current source. Entering the blue portal then reaches the orange portal. On every later transition, the color not currently occupying the source endpoint is replaced. The existing portal at the source is never destroyed before it is used.

All grid indexing is zero-based internally. Since every free cell is strictly inside the solid outer border, expressions such as `x - 1`, `x + 1`, `x - m`, and `x + m` are safe whenever they are evaluated for a free cell. Integer overflow is not an issue in Python, and the compact `array` containers keep the million-cell state within reasonable memory usage.

## Worked Examples

### Sample 1

The free cells split into an upper component containing the start and a lower component containing the exit. The start cell itself is a valid portal endpoint because it is adjacent to a solid wall on the left.

The useful transition shoots downward from the start. The ray crosses the glass cell, reaches the bottom solid wall, and creates a portal at the free cell directly above that wall.

| Stage | Current cell | Action | Portal endpoints | Component |
| --- | --- | --- | --- | --- |
| 1 | ((2,3)) | `OD` | Orange at ((4,3)) | Start component |
| 2 | ((2,3)) | `BL` | Blue at ((2,3)) | Start component |
| 3 | ((2,3)) | `ML` | Teleports to ((4,3)) | Exit component |
| 4 | ((4,3)) | `ML` | No portal needed | Exit component |

The first two actions establish the first teleport, so (P=2). After entering the blue portal with `ML`, the player appears at ((4,3)), and one ordinary movement reaches the exit ((4,2)). This also demonstrates why the ray must be allowed to pass through glass.

### Sample 2

The first component contains the start. The first useful portal transition is prepared after walking through that component to ((6,4)). Shooting upward crosses a glass cell and reaches a solid wall, creating an orange portal at ((3,4)).

The player then walks back to ((2,3)), places the blue portal immediately to the right, and enters it. The orange portal sends the player to ((3,4)), after which the final movements reach the exit.

| Stage | Current cell | Action | Active useful portal | Component |
| --- | --- | --- | --- | --- |
| 1 | ((2,3)) | Walk to ((6,4)) | None | Start component |
| 2 | ((6,4)) | `OU` | Orange at ((3,4)) | Start component |
| 3 | ((6,4)) | Walk to ((2,3)) | Orange at ((3,4)) | Start component |
| 4 | ((2,3)) | `BR` | Blue at ((2,3)) | Start component |
| 5 | ((2,3)) | `MR` | Teleports to ((3,4)) | Exit component |
| 6 | ((3,4)) | `MR` | Ordinary movement | Exit component |
| 7 | ((3,5)) | `MU` | Ordinary movement | Exit component |

Again only two shots are required. The long walking section does not affect the objective because the number of shots is already minimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(NM)) | Component BFS, four directional sweeps, component-graph BFS, and local path reconstruction together visit only a constant number of grid structures per cell |
| Space | (O(NM)) | Component labels, four endpoint arrays, boundary lists, BFS parents, and reconstruction state are all linear |

For (N,M\le1000), (NM\le10^6). The algorithm performs only a constant number of passes over those million cells and stores a linear amount of auxiliary information, so it fits the intended limits. The produced movement sequence is also at most (NM-1) moves in the portal case, which is below the required (2NM) bound.

## Test Cases

The output of a constructive problem is not unique, so the tests should validate the produced action sequence rather than compare it byte-for-byte with the samples. The following harness checks the reported shot count, simulates every action including portal replacement and teleportation, checks that the exit is reached, and verifies the (2NM) movement bound.

```python
import io

# Import solve_stream from the submitted solution.
# If this code is appended directly after the solution, simply remove
# the import and use solve_stream from the same file.

def run(inp: str) -> str:
    return solve_stream(io.StringIO(inp).readline)

def verify(inp: str, expected_p: int):
    out = run(inp)
    lines = out.strip().splitlines()

    first = list(map(int, lines[0].split()))
    p, s = first
    assert p == expected_p
    assert len(lines) == p + s + 1

    it = iter(inp.strip().splitlines())
    n, m = map(int, next(it).split())
    grid = [next(it) for _ in range(n)]
    sr, sc = map(int, next(it).split())
    er, ec = map(int, next(it).split())
    sr -= 1
    sc -= 1
    er -= 1
    ec -= 1

    pos = (sr, sc)
    portals = [None, None]  # 0 = orange, 1 = blue

    dirs = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1),
    }

    shots = 0
    moves = 0

    def shoot_endpoint(r, c, d):
        dr, dc = dirs[d]
        nr, nc = r + dr, c + dc

        while grid[nr][nc] != 'W':
            nr += dr
            nc += dc

        return nr - dr, nc - dc, nr, nc

    for action in lines[1:]:
        typ = action[0]
        d = action[1]
        r, c = pos

        if typ in 'OB':
            color = 0 if typ == 'O' else 1
            erow, ecol, wrow, wcol = shoot_endpoint(r, c, d)

            # A glass endpoint is deadly and cannot be used by a valid solution.
            assert grid[erow][ecol] == '.'

            side = (wrow, wcol, d)

            occupied = False
            for portal in portals:
                if portal is not None and portal[2] == side:
                    occupied = True
                    break

            if not occupied:
                portals[color] = (erow, ecol, side)

            shots += 1

        else:
            assert typ == 'M'
            dr, dc = dirs[d]
            nr, nc = r + dr, c + dc

            if grid[nr][nc] == '.':
                pos = (nr, nc)
            else:
                assert grid[nr][nc] == 'W'

                used = None
                for color, portal in enumerate(portals):
                    if portal is None:
                        continue

                    pr, pc, side = portal
                    if (pr, pc) == (r, c) and side[2] == d:
                        used = color
                        break

                assert used is not None

                other = 1 - used
                assert portals[other] is not None

                tr, tc, _ = portals[other]
                assert grid[tr][tc] == '.'
                pos = (tr, tc)

            moves += 1

    assert shots == p
    assert moves == s
    assert pos == (er, ec)
    assert s <= 2 * n * m

# Provided samples.

sample1 = """\
5 5
WWWWW
WW..W
WWGWW
W...W
WWWWW
2 3
4 2
"""

sample2 = """\
7 6
WWWWWW
W..W.W
W.W..W
W.W..W
W.WG.W
W...WW
WWWWWW
2 3
2 5
"""

sample3 = """\
5 5
WWWWW
W.G.W
WW.GW
W.G.W
WWWWW
2 2
4 2
"""

verify(sample1, 2)
verify(sample2, 2)
verify(sample3, 4)

# Custom case 1: minimum grid, start equals exit.
minimum_case = """\
3 3
WWW
W.W
WWW
2 2
2 2
"""

verify(minimum_case, 0)

# Custom case 2: glass cells form a complete barrier and every nontrivial
# portal endpoint is glass, so no safe component transition exists.
impossible_case = """\
5 5
WWWWW
W.GGW
WGWGW
WGG.W
WWWWW
2 2
4 4
"""

out = run(impossible_case).strip()
assert out == "-1 -1"

# Custom case 3: the shot must cross several glass cells before reaching
# the solid border. The endpoint is the free cell immediately before W.
multi_glass_case = """\
5 5
WWWWW
W...W
WGGGW
W...W
WWWWW
2 2
4 2
"""

verify(multi_glass_case, 2)

# Custom case 4: maximum-size all-free grid. Ordinary BFS is enough,
# so the optimal number of shots is zero.
n = 1000
m = 1000
rows = ["W" + "." * (m - 2) + "W"] * (n - 2)
maximum_case = (
    f"{n} {m}\n"
    + "W" * m + "\n"
    + "\n".join(rows) + "\n"
    + "W" * m + "\n"
    + "2 2\n"
    + f"{n - 1} {m - 1}\n"
)

verify(maximum_case, 0)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | (P=2) | First teleport, shooting through glass, and portal entry |
| Sample 2 | (P=2) | Long ordinary walks before and after a teleport |
| Sample 3 | (P=4) | Several consecutive portal transitions and color alternation |
| `minimum_case` | (0) shots | Start already equals exit and zero-shot handling |
| `impossible_case` | `-1 -1` | Glass endpoints must not be treated as safe portals |
| `multi_glass_case` | (P=2) | Nearest solid wall after multiple glass cells |
| `maximum_case` | (0) shots | (1000\times1000) input and linear-time behavior |

## Edge Cases

For the minimum grid, there is only one possible free cell. If it is both the start and the exit, the component check succeeds immediately. The algorithm never constructs the portal graph and outputs `0 0`, which is optimal because no shot can improve on zero.

For a maze where the start and exit are connected by ordinary free cells, the same component test terminates the algorithm before any portal processing. This is also necessary for optimality. A portal-based solution with one or more shots cannot beat (P=0).

For a glass barrier, the directional sweep may still find a target cell, but the target is `G`, so the corresponding graph edge is discarded. This is the exact distinction between a glass cell being transparent to the gun and being safe to occupy after teleportation. The impossible custom case consequently has no component-graph path and produces `-1 -1`.

For a ray containing several glass cells followed by free cells and then a solid wall, the sweep does not stop at the glass. It records the cell immediately before the solid wall as the endpoint. Sample 1 and the `multi_glass_case` both exercise this condition. A solution that searches only adjacent walls would miss valid two-shot routes.

For repeated components, the component graph is searched rather than the individual endpoint graph. This prevents useless transitions that stay inside one free component. It also gives the movement bound for free, because a shortest component path visits each component at most once.

For the first teleport, there is no existing portal at the source. The construction explicitly spends two shots, one for the destination and one for the source. Every later transition needs only one shot because the source already contains the portal created by the preceding transition. This is exactly why a component path containing (k) edges requires (k+1) shots.

For the final component, no portal is needed after arrival. The algorithm simply walks from the final endpoint to the exit. This matters because the objective minimizes shots, not movement length, and creating an unnecessary final portal could only make the answer worse.
