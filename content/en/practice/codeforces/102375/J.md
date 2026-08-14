---
title: "CF 102375J - \u041f\u043e\u0440\u0442\u0430\u043b\u044b"
description: "The maze is an (N times M) grid. A cell is either ordinary free space, a glass wall, or a solid wall. Ordinary movement is possible only between adjacent free cells. Glass blocks movement, but a portal shot can pass through it. The outer border consists entirely of solid walls."
date: "2026-08-14T13:19:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "J"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 866
verified: false
draft: false
---

[CF 102375J - \u041f\u043e\u0440\u0442\u0430\u043b\u044b](https://codeforces.com/problemset/problem/102375/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 26s  
**Verified:** no  

## Solution
## Problem Understanding

The maze is an (N \times M) grid. A cell is either ordinary free space, a glass wall, or a solid wall. Ordinary movement is possible only between adjacent free cells. Glass blocks movement, but a portal shot can pass through it. The outer border consists entirely of solid walls.

A portal is attached to one side of a solid-wall cell. There are two colors, orange and blue, and only one portal of each color can exist at a time. Shooting replaces the old portal of that color. When a shot is made in some direction, the ray continues until it reaches the nearest solid wall. Glass cells do not stop the ray. The portal is placed on the side of that wall facing the shooter.

A portal is useful only when its side is adjacent to a free cell. If the corresponding side is glass, entering or leaving the portal would be impossible or fatal, so such a portal cannot participate in a valid route.

The interesting part is that the two portal positions are persistent. After using one portal, the other portal remains where it was. This allows us to replace one color with a new destination portal using a single additional shot, then enter the other color and teleport to the new destination.

The output does not ask for the shortest route in ordinary movement. The primary objective is to minimize the number of shots. Among all solutions with that minimum number of shots, any route with at most (2NM) movement steps is accepted. The problem allows (N,M\le1000), so there can be up to (10^6) cells. An algorithm with quadratic or cubic dependence on the number of cells is already too large, while an (O(NM)) solution is the natural target. The original contest limits are 2 seconds and 512 MiB.

The first edge case is when start and exit are in the same ordinary connected component. For example,

```
3 3
WWW
W.W
WWW
2 2
2 2
```

The correct output is

```
0 0
```

There are no actions at all. A solution that always constructs two portals before considering ordinary movement would unnecessarily use the gun.

The second edge case is a glass cell immediately before a solid wall. Consider

```
5 5
WWWWW
W.GWW
WWWWW
W...W
WWWWW
2 2
4 2
```

The start and exit are in different components. Shooting right from the start reaches the solid wall after the glass cell, but the portal is placed next to the glass cell, so it cannot be safely used. Shooting in the other directions only reaches solid walls directly around the start component. The correct output is `-1 -1`. A careless implementation that treats every wall visible through glass as a usable destination would incorrectly claim that the two components can be connected.

The third edge case is a portal that targets the same ordinary component. In a completely open interior, a shot toward a boundary wall may create a portal, but both sides relevant to the route are already connected by ordinary movement. Such a portal must not be counted as progress. Treating every possible shot as a graph edge would create many useless self-loops.

The fourth edge case is that a component may contain free cells but have no free cell directly adjacent to a solid wall. Such a component can sometimes shoot through glass and create a portal somewhere else, but it cannot place a usable source portal for itself. Consequently, it cannot be used as the current side of a teleport. This distinction matters when deciding which graph edges are actually traversable.

## Approaches

A direct brute-force model starts from the full physical state. The state has to contain the current free cell and the positions of both colored portals. There are (O(NM)) possible relevant wall faces for one portal, so a pair of portals already gives (O((NM)^2)) configurations. Multiplying by the current position gives (O((NM)^3)) possible states. With (NM=10^6), this is on the order of (10^{18}) states in the worst case. Even storing one byte per state would be impossible, so a full state-space search is not a viable approach.

The key observation is that ordinary movement completely removes the need to distinguish individual cells when counting shots. Inside one connected component of free cells, we can move to any other cell without firing the gun. The only meaningful transition is a teleport from one free-space component to another.

Consider a horizontal or vertical sequence of cells containing no solid wall. Suppose its right endpoint is followed by a solid wall, and the cell immediately before that wall is free. Every free cell in the sequence can shoot toward the wall. The resulting portal is placed on the wall side adjacent to that final free cell. Glass cells between the shooter and the wall do not matter. Consequently, every free component represented in that sequence can create a portal whose usable endpoint belongs to the component containing the final free cell.

This gives a directed graph whose vertices are connected components of free cells. There is an edge (A\to B) when a cell in component (A) can shoot toward a solid wall and the side of that wall facing the shooter is adjacent to a free cell in component (B). Component (B) is then a possible destination for a newly created portal.

The direction is significant. If (A) can see a usable portal side belonging to (B), then from (A) we can create that destination portal. The reverse transition may not be possible with one new shot.

The portal colors explain why this graph is enough. The first teleport needs two shots because both colors initially have no portal. Put one color at any usable wall face in the current component and the other color at the destination described by the graph edge. After the teleport, one portal is in the current component and the other is in the new component. To reach another component, only one shot is necessary. Replace the portal that is still behind you with a new portal at the next destination, then enter the portal that remains in your current component.

Thus a route using (K) graph edges requires exactly (K+1) shots when (K>0). A route using zero edges requires zero shots. Minimizing the number of shots is consequently the same as finding a shortest directed path in the component graph.

We do not need to explicitly search all possible rays. A horizontal segment between two solid walls can be processed with two sweeps, one for each shooting direction. A vertical segment is handled in the same way. Each free cell participates in a constant number of operations, so the complete graph can be constructed in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full state-space search | (O((NM)^3)) states | (O((NM)^3)) | Too slow |
| Optimal component graph | (O(NM)) | (O(NM)) | Accepted |

## Algorithm Walkthrough

1. Label every connected component of `.` cells using BFS. Two free cells belong to the same component exactly when they can be connected using ordinary movement without crossing `G` or `W`.

While discovering a component, remember one free cell directly adjacent to a solid wall and the direction of that wall. Such a cell gives us a valid location for the source portal whenever the component needs to perform a teleport.
2. Build the directed component graph by scanning every row.

For a fixed row, look at a maximal interval containing no `W`. If the cell immediately before the solid wall on the right is free, then every free cell in the interval can shoot right and create a usable portal belonging to the component of that final free cell. Add an edge from the component of each shooter to that target component.

Repeat the same scan from left to right to obtain left-directed edges.
3. Perform the analogous two sweeps for every column.

The downward sweep handles portals whose wall is below the shooter. The upward sweep handles portals whose wall is above the shooter.

A glass cell never stops a sweep. It only matters whether the cell immediately adjacent to the solid wall is free. If that cell is `G`, the portal would have a glass wall on its usable side and must not be added as an edge.
4. Ignore graph edges whose source and destination components are equal.

Ordinary movement already connects every pair of cells in such a component, so a portal cannot improve the number of shots.
5. Run BFS on the directed component graph from the start component.

Every graph edge represents one teleport to a new component. All edges have equal cost, so ordinary BFS gives the minimum number of teleports. Store the predecessor component and the exact shooting cell and direction for every discovered edge. Those witnesses are needed later to reconstruct the actual actions.
6. If the exit component is unreachable, print `-1 -1`.

The component graph describes every possible way to introduce a new usable portal destination. If the exit component cannot be reached in this graph, no sequence of portal shots can make it reachable.
7. If start and exit are in the same component, reconstruct an ordinary path between their cells and output it with zero shots.
8. Otherwise, reconstruct the sequence of components found by BFS.

Suppose the first graph edge uses shooter cell (u), direction (d), and arrives at cell (v). Choose the remembered wall-adjacent cell (q) of the start component as the first portal location. Walk from the start to (q), place the blue portal there, walk to (u), place the orange portal using direction (d), return to (q), and move into the blue portal. The teleport brings us to (v).

Two shots were used, which is exactly the required cost for the first teleport.
9. For every later graph edge, there is already one portal in the current component. Walk from the current arrival cell to the shooting witness (u), shoot the other color toward the next destination, return to the old portal, and enter it.

The new portal is now in the next component. This costs exactly one shot.
10. After reaching the exit component, walk normally from the arrival cell to the exit.

For every component we use a simple BFS path inside that component. Each component occurs at most once on the shortest component path, so the total amount of ordinary walking stays within the required (2NM) bound.

### Why it works

The invariant is that immediately before every graph transition, one portal is placed on a usable wall side in the current component. The other portal is either irrelevant or is being replaced by the next shot. The stored graph edge tells us exactly where to shoot so that the new portal is placed on a usable wall side in the next component. We then return to the existing portal and cross it, reaching the new component.

Every first teleport needs two shots because both colors are initially absent. Every later teleport to a newly reached component needs at least one new shot, because without changing a portal position the pair of destinations cannot acquire a new component. Conversely, the construction uses exactly one new shot for every subsequent graph edge. Thus a shortest graph path with (K) edges gives the minimum possible (K+1) shots.

The graph contains exactly the useful teleport transitions. A transition can be created precisely when the destination wall side is visible through free or glass cells and its immediate cell is free. The four sweeps enumerate exactly those situations. Hence BFS on this graph finds the minimum possible number of new portal destinations, which is the required optimum.

## Python Solution

```python
import sys
from collections import deque
from array import array

input = sys.stdin.readline

# Direction codes:
# 0 = U, 1 = D, 2 = L, 3 = R
DR = (-1, 1, 0, 0)
DC = (0, 0, -1, 1)
DIR_CHARS = b"UDLR"
OPPOSITE = (1, 0, 3, 2)

def solve():
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    sr, sc = map(int, input().split())
    er, ec = map(int, input().split())
    sr -= 1
    sc -= 1
    er -= 1
    ec -= 1

    total = n * m
    start = sr * m + sc
    finish = er * m + ec

    # Component id of every cell, -1 for walls and glass.
    comp = array('i', [-1]) * total

    # One usable portal position for each component.
    portal_cell = array('i')
    portal_dir = bytearray()

    component_count = 0
    q = deque()

    for r in range(1, n - 1):
        row = g[r]
        for c in range(1, m - 1):
            pos = r * m + c
            if row[c] != '.' or comp[pos] != -1:
                continue

            cid = component_count
            component_count += 1
            portal_cell.append(-1)
            portal_dir.append(0)

            comp[pos] = cid
            q.clear()
            q.append(pos)

            while q:
                p = q.popleft()
                pr = p // m
                pc = p - pr * m

                # Find one free cell with a solid wall next to it.
                if portal_cell[cid] == -1:
                    if g[pr - 1][pc] == 'W':
                        portal_cell[cid] = p
                        portal_dir[cid] = 0
                    elif g[pr + 1][pc] == 'W':
                        portal_cell[cid] = p
                        portal_dir[cid] = 1
                    elif g[pr][pc - 1] == 'W':
                        portal_cell[cid] = p
                        portal_dir[cid] = 2
                    elif g[pr][pc + 1] == 'W':
                        portal_cell[cid] = p
                        portal_dir[cid] = 3

                np = p - m
                if g[pr - 1][pc] == '.' and comp[np] == -1:
                    comp[np] = cid
                    q.append(np)

                np = p + m
                if g[pr + 1][pc] == '.' and comp[np] == -1:
                    comp[np] = cid
                    q.append(np)

                np = p - 1
                if g[pr][pc - 1] == '.' and comp[np] == -1:
                    comp[np] = cid
                    q.append(np)

                np = p + 1
                if g[pr][pc + 1] == '.' and comp[np] == -1:
                    comp[np] = cid
                    q.append(np)

    start_comp = comp[start]
    finish_comp = comp[finish]

    # If ordinary movement is already enough, construct that path later.
    # Otherwise build the component graph.
    head = array('i', [-1]) * component_count
    to = array('i')
    nxt = array('i')
    witness = array('i')
    target_cell = array('i')
    edge_dir = bytearray()

    def add_edge(a, b, u, v, d):
        if a == b:
            return
        idx = len(to)
        to.append(b)
        witness.append(u)
        target_cell.append(v)
        edge_dir.append(d)
        nxt.append(head[a])
        head[a] = idx

    # Horizontal edges: shooting right.
    for r in range(1, n - 1):
        target = -1
        base = r * m
        for c in range(m - 1, 0, -1):
            ch = g[r][c]
            if ch == 'W':
                if g[r][c - 1] == '.':
                    target = base + c - 1
                else:
                    target = -1
            elif ch == '.' and target != -1:
                u = base + c
                add_edge(comp[u], comp[target], u, target, 3)

    # Horizontal edges: shooting left.
    for r in range(1, n - 1):
        target = -1
        base = r * m
        for c in range(0, m - 1):
            ch = g[r][c]
            if ch == 'W':
                if g[r][c + 1] == '.':
                    target = base + c + 1
                else:
                    target = -1
            elif ch == '.' and target != -1:
                u = base + c
                add_edge(comp[u], comp[target], u, target, 2)

    # Vertical edges: shooting down.
    for c in range(1, m - 1):
        target = -1
        for r in range(n - 1, 0, -1):
            ch = g[r][c]
            if ch == 'W':
                if g[r - 1][c] == '.':
                    target = (r - 1) * m + c
                else:
                    target = -1
            elif ch == '.':
                if target != -1:
                    u = r * m + c
                    add_edge(comp[u], comp[target], u, target, 1)

    # Vertical edges: shooting up.
    for c in range(1, m - 1):
        target = -1
        for r in range(0, n - 1):
            ch = g[r][c]
            if ch == 'W':
                if g[r + 1][c] == '.':
                    target = (r + 1) * m + c
                else:
                    target = -1
            elif ch == '.' and target != -1:
                u = r * m + c
                add_edge(comp[u], comp[target], u, target, 0)

    # BFS on the component graph.
    parent_comp = array('i', [-1]) * component_count
    parent_edge = array('i', [-1]) * component_count

    parent_comp[start_comp] = start_comp
    cq = deque([start_comp])

    while cq:
        a = cq.popleft()

        if a == finish_comp:
            break

        # A component without a free cell directly adjacent to W
        # cannot serve as the source of a usable portal.
        if portal_cell[a] == -1:
            continue

        e = head[a]
        while e != -1:
            b = to[e]
            if parent_comp[b] == -1:
                parent_comp[b] = a
                parent_edge[b] = e
                cq.append(b)
            e = nxt[e]

    if parent_comp[finish_comp] == -1:
        print("-1 -1")
        return

    # Temporary arrays for paths inside ordinary components.
    cell_parent = array('i', [-1]) * total

    def get_path(a, b, cid):
        """Return direction codes of a shortest ordinary path a -> b."""
        if a == b:
            return []

        bfsq = [a]
        visited = [a]
        cell_parent[a] = a
        qi = 0

        while qi < len(bfsq):
            p = bfsq[qi]
            qi += 1

            if p == b:
                break

            r = p // m
            c = p - r * m

            np = p - m
            if comp[np] == cid and cell_parent[np] == -1:
                cell_parent[np] = p
                bfsq.append(np)
                visited.append(np)

            np = p + m
            if comp[np] == cid and cell_parent[np] == -1:
                cell_parent[np] = p
                bfsq.append(np)
                visited.append(np)

            np = p - 1
            if comp[np] == cid and cell_parent[np] == -1:
                cell_parent[np] = p
                bfsq.append(np)
                visited.append(np)

            np = p + 1
            if comp[np] == cid and cell_parent[np] == -1:
                cell_parent[np] = p
                bfsq.append(np)
                visited.append(np)

        path = []
        cur = b
        while cur != a:
            p = cell_parent[cur]
            delta = cur - p
            if delta == -m:
                path.append(0)
            elif delta == m:
                path.append(1)
            elif delta == -1:
                path.append(2)
            else:
                path.append(3)
            cur = p

        path.reverse()

        for v in visited:
            cell_parent[v] = -1

        return path

    # Reconstruct component path and corresponding graph edges.
    components = []
    edges = []

    cur = finish_comp
    while cur != start_comp:
        components.append(cur)
        e = parent_edge[cur]
        edges.append(e)
        cur = parent_comp[cur]

    components.append(start_comp)
    components.reverse()
    edges.reverse()

    actions = bytearray()
    shots = 0
    steps = 0

    def add_move(d):
        nonlocal steps
        actions.extend((77, DIR_CHARS[d], 10))
        steps += 1

    def add_shot(color, d):
        nonlocal shots
        actions.extend((color, DIR_CHARS[d], 10))
        shots += 1

    if not edges:
        path = get_path(start, finish, start_comp)
        for d in path:
            add_move(d)

        out = bytearray()
        out.extend(f"{shots} {steps}\n".encode())
        out.extend(actions)
        sys.stdout.buffer.write(out)
        return

    # First teleport.
    first_edge = edges[0]
    first_comp = start_comp

    q_cell = portal_cell[first_comp]
    q_dir = portal_dir[first_comp]

    u = witness[first_edge]
    v = target_cell[first_edge]
    d = edge_dir[first_edge]

    # Move to the source portal position.
    path = get_path(start, q_cell, first_comp)
    for x in path:
        add_move(x)

    # Blue is the initial source portal.
    add_shot(ord('B'), q_dir)

    # Move to the shooting position for the destination portal.
    path = get_path(q_cell, u, first_comp)
    for x in path:
        add_move(x)

    # Orange becomes the destination portal.
    add_shot(ord('O'), d)

    # Return to the blue portal.
    for x in reversed(path):
        add_move(OPPOSITE[x])

    # Enter the blue portal and arrive at v.
    add_move(q_dir)

    current_cell = v
    current_portal_dir = d
    current_portal_color = ord('O')

    # Remaining teleports.
    for i in range(1, len(edges)):
        e = edges[i]
        cid = components[i]

        u = witness[e]
        v = target_cell[e]
        d = edge_dir[e]

        # Move from the arrival point to the shooting position.
        path = get_path(current_cell, u, cid)
        for x in path:
            add_move(x)

        # Replace the portal of the opposite color.
        new_color = ord('B') if current_portal_color == ord('O') else ord('O')
        add_shot(new_color, d)

        # Return to the existing portal.
        for x in reversed(path):
            add_move(OPPOSITE[x])

        # Enter the existing portal.
        add_move(current_portal_dir)

        current_cell = v
        current_portal_dir = d
        current_portal_color = new_color

    # Finish by ordinary movement.
    final_cid = finish_comp
    path = get_path(current_cell, finish, final_cid)
    for x in path:
        add_move(x)

    out = bytearray()
    out.extend(f"{shots} {steps}\n".encode())
    out.extend(actions)
    sys.stdout.buffer.write(out)

if __name__ == "__main__":
    solve()
```

The first phase labels only `.` cells. The `comp` array is a compact integer array rather than a Python list, which matters because there can be one million cells. During the same BFS, the code remembers a free cell adjacent to a solid wall. That is the location from which the first portal of a teleport sequence can be placed.

The graph construction deliberately avoids storing four nearest-wall values for every cell. Instead, each row and column is swept twice. During the right-to-left sweep, when a solid wall is encountered, the code remembers the free cell immediately to its left. Every later free cell before another solid wall can shoot toward that wall. The left, up, and down sweeps are symmetric.

The condition checking the cell immediately adjacent to the solid wall is the subtle part. A glass cell can be anywhere between the shooter and the wall, but the cell touching the portal must be free. If it is `G`, the portal cannot be safely used, so the target is discarded.

The component BFS stores the exact graph edge used to reach every component. That edge contains the shooting cell, direction, and destination cell. Consequently, the graph search does not merely tell us that a transition exists, it also gives enough geometric information to print the corresponding `O` or `B` action.

The `get_path` function performs an ordinary BFS restricted to one component. It is called only for components appearing on the final component path. A simple path inside a component has fewer than its number of cells, so the total work remains linear. The predecessor array is reset only for cells touched by that BFS instead of rebuilding a million-element structure every time.

The output is accumulated in a `bytearray`. A valid solution can contain up to millions of actions, so storing every action as a separate Python string would create unnecessary object overhead. The byte representation is compact and can be written directly at the end.

The portal colors alternate after the first teleport. The first blue portal is the source, while orange is the first destination. After reaching that destination, orange is the portal currently available in the current component. The next shot creates a blue destination, after which the orange portal is used. This alternating pattern is exactly what makes every later teleport cost one shot.

The ordinary movement bound follows from the construction. Inside each non-final component, the route goes from its entry cell to a shooting cell and back, costing at most twice the number of cells in that component. The final component is traversed only once. Entering each portal adds one movement action, and the resulting total is at most (2NM).

## Worked Examples

### Sample 1

The free cells split into two ordinary components. The start component contains `(2,3)` and `(2,4)`, while the exit component contains the free cells on row 4.

The vertical corridor through column 3 contains a glass cell between the start component and the lower component. The solid boundary wall below it has a free cell immediately above it, so shooting down from the start can create a usable portal for the lower component.

| Action | Current cell | Existing useful portal | Operation | Result |
| --- | --- | --- | --- | --- |
| `OD` | `(2,3)` | none | Place orange below through glass | Orange belongs to lower component |
| `BL` | `(2,3)` | orange below | Place blue on the left wall | Blue is the source portal |
| `ML` | `(2,3)` | blue left | Enter blue portal | Teleport to lower component |
| `ML` | lower component | orange below | Ordinary move | Reach exit |

The solution needs two shots, because this is the first teleport. The important geometric point is that the glass cell does not prevent the shot from reaching the solid boundary, and the free cell immediately before the boundary makes the resulting portal usable.

### Sample 2

The start and exit lie in different ordinary components. The component graph contains a path using one teleport, so the minimum number of shots is two.

| Phase | Component | Operation | Purpose |
| --- | --- | --- | --- |
| 1 | Start | Ordinary moves | Reach a useful shooting position |
| 2 | Start | `OU` | Create destination portal |
| 3 | Start | Ordinary moves | Reach the source portal |
| 4 | Start | `BR` | Create source portal |
| 5 | Start | `M` into blue portal | Teleport |
| 6 | Exit component | Ordinary moves | Reach the exit |

The exact ordinary path can differ from the sample output. The checker does not require the shortest number of movement steps, only at most (2NM). The graph BFS is concerned exclusively with the number of teleports, which is the quantity that determines the minimum shot count.

The sample also demonstrates why portal replacement matters. After the first teleport, one portal remains in the old component and the other is in the new component. A later shot can replace the old portal with a destination portal, allowing another teleport for only one additional shot.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(NM)) | Component BFS, four grid sweeps, component BFS, and path reconstruction each process only a constant number of grid cells or graph edges |
| Space | (O(NM)) | Component ids, graph edges, BFS predecessors, and the output action buffer are all linear in the grid size |

There are at most (10^6) cells. The graph construction creates only a constant number of candidate edges per free cell, and all graph searches are linear in the number of cells and edges. The compact `array` structures keep the memory usage proportional to the input size rather than to the much larger Python object overhead of a full state-space representation.

## Test Cases

The output is not unique, so comparing the entire output string is not a useful test for this problem. The tests below compare the mandatory properties instead: whether the solution is unreachable, the minimum number of shots, and the movement bound. They also verify that the number of printed actions matches the header.

```python
# Save the submitted solution as solution.py.
# The helper imports its solve() function.

import io
import sys

from solution import solve

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

def header(out: str):
    first = out.splitlines()[0].split()
    return tuple(map(int, first))

def check_valid_header(inp: str, out: str, expected_p: int):
    lines = out.splitlines()
    p, s = map(int, lines[0].split())

    assert p == expected_p
    assert s >= 0

    n, m = map(int, inp.splitlines()[0].split())
    assert s <= 2 * n * m
    assert len(lines) - 1 == p + s

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

assert header(run(sample1))[0] == 2, "sample 1 must use two shots"
check_valid_header(sample1, run(sample1), 2)

assert header(run(sample2))[0] == 2, "sample 2 must use two shots"
check_valid_header(sample2, run(sample2), 2)

assert header(run(sample3))[0] == 4, "sample 3 must use four shots"
check_valid_header(sample3, run(sample3), 4)

# Minimum-size grid, start equals exit.
minimum_case = """\
3 3
WWW
W.W
WWW
2 2
2 2
"""

assert run(minimum_case) == "0 0\n", "same start and exit need no actions"

# Different components with no usable portal transition.
unreachable_case = """\
5 5
WWWWW
W.GWW
WWWWW
W...W
WWWWW
2 2
4 2
"""

assert run(unreachable_case) == "-1 -1\n", "glass directly before a solid wall must not create an edge"

# Boundary-adjacent free cells, but ordinary movement is already sufficient.
boundary_case = """\
5 5
WWWWW
W...W
W.W.W
W...W
WWWWW
2 2
4 4
"""

out = run(boundary_case)
assert header(out)[0] == 0
check_valid_header(boundary_case, out, 0)

# Maximum-size all-open interior. Everything is one ordinary component.
# The minimum number of shots is zero and a shortest Manhattan path has
# 1994 movement steps.
n = 1000
m = 1000
rows = []
rows.append("W" * m)
for _ in range(n - 2):
    rows.append("W" + "." * (m - 2) + "W")
rows.append("W" * m)

maximum_case = (
    f"{n} {m}\n"
    + "\n".join(rows)
    + "\n2 2\n999 999\n"
)

out = run(maximum_case)
p, s = header(out)
assert p == 0
assert s == 1994
check_valid_header(maximum_case, out, 0)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | (P=2), valid (S\le2NM) | First portal transition through glass |
| Sample 2 | (P=2), valid (S\le2NM) | Nontrivial ordinary movement around the portal transition |
| Sample 3 | (P=4), valid (S\le2NM) | Several consecutive one-shot portal replacements |
| `3 x 3`, start equals exit | `0 0` | Minimum grid and zero-shot case |
| Isolated components with `G` before `W` | `-1 -1` | Prevents treating a dangerous portal as usable |
| Boundary-adjacent ordinary maze | (P=0) | Boundary handling and ordinary connectivity |
| `1000 x 1000` open interior | `P=0`, `S=1994` | Maximum grid size, memory usage, and linear-time behavior |

## Edge Cases

For the minimum grid

```
3 3
WWW
W.W
WWW
2 2
2 2
```

the component labeling creates exactly one free component containing the start and exit. The component BFS is never needed because the two cells are identical. The path reconstruction returns an empty path, so the program prints `0 0`.

For the glass-before-solid-wall case

```
5 5
WWWWW
W.GWW
WWWWW
W...W
WWWWW
2 2
4 2
```

the start component has a free cell next to the solid wall above and below, but neither gives access to the other component. In the rightward sweep, the solid wall at column 4 has a glass cell at column 3 immediately before it. The target is consequently discarded. The other directions reach solid walls whose portal sides remain in the start component. The exit component is never discovered by the component BFS, so the answer is `-1 -1`.

For a grid with several free cells in the same component, such as

```
5 5
WWWWW
W...W
W.W.W
W...W
WWWWW
2 2
4 4
```

component labeling puts all free cells into one component. Any graph edges produced by visible boundary walls are self-edges and are ignored. The ordinary path is sufficient, so the result has zero shots. This prevents the graph construction from confusing a possible portal placement with a necessary portal transition.

For a component surrounded by glass, the component may still appear as a shooter in a visibility sweep, because a shot can pass through glass. However, if the component has no free cell directly adjacent to a solid wall, `portal_cell[cid]` stays `-1`. The BFS then refuses to use that component as a source of a teleport. This matches the physical rule: the component can fire, but it has no safe portal through which the player can leave.

For the maximum-size case with a (1000\times1000) grid and an open interior, the entire interior is one component. The ordinary shortest path from `(2,2)` to `(999,999)` has (997+997=1994) steps, so the program returns zero shots and 1994 movement steps. The graph construction still scans only a constant number of times over the million cells, demonstrating why the linear formulation fits the constraints.
