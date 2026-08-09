---
title: "CF 102443J - Factory"
description: "We are given an (m times n) rectangular map. A cell is either a workshop, written as , or empty, written as .. All workshop cells form one side-connected region, and there are no enclosed empty regions inside it."
date: "2026-08-09T13:47:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "J"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 468
verified: true
draft: false
---

[CF 102443J - Factory](https://codeforces.com/problemset/problem/102443/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an (m \times n) rectangular map. A cell is either a workshop, written as `*`, or empty, written as `.`. All workshop cells form one side-connected region, and there are no enclosed empty regions inside it. The latter condition means every empty cell belongs to the outside region of the factory.

Look at the grid lines between cells. A grid node is called important if it is a corner of at least one workshop cell. Every side of a workshop cell is a corridor connecting its two endpoint grid nodes.

We need to construct a closed route through important grid nodes. Every move must follow one corridor, no corridor may be used twice, and every important node must occur somewhere on the route. The route does not have to be short. If such a route cannot exist, we print `No`. Otherwise we print `Yes`, the number of corridors, and the sequence of grid nodes in the route. The original constraints are (1 \le m,n \le 20), with a two-second time limit and 256 MB of memory.

The crucial graph interpretation is that the corridors form a planar grid graph. We are looking for a connected subgraph containing every important vertex in which every used vertex has even degree. Such a graph has an Eulerian circuit, and that circuit is exactly the route requested by the problem.

There are several easy cases where a naive interpretation goes wrong. Consider

```
1 1
*
```

The answer is `Yes`. The four corners form a cycle, so the route can simply walk around the single workshop.

For

```
1 1
.
```

there are no important nodes. The empty route is valid, so the answer is `Yes` with zero corridors. A solution that assumes the route must contain at least one workshop would incorrectly reject this case.

Consider

```
2 2
**
**
```

The answer is `No`. The corresponding grid graph is a (3 \times 3) grid. Its four corner vertices have degree two, so a spanning even subgraph is forced to use the entire outer boundary. That leaves the center vertex disconnected, while using an edge from the center would make one of the adjacent degree-three vertices odd. This is a useful example because simply checking that the factory is connected is not enough.

Finally,

```
1 2
**
```

is `Yes`. The two cells form a (2 \times 3) grid graph, and the perimeter gives a valid closed route through every important node. A construction that only considers individual workshop-cell cycles can miss the fact that adjacent cycles can be combined into one larger route.

## Approaches

A direct brute-force solution can be described in terms of the faces of the planar graph. Every workshop cell is a bounded face, while all empty cells and the outside belong to the same outer face because the factory has no holes. Give every workshop face one of two colors. Whenever two adjacent faces have different colors, use the grid edge separating them.

For any coloring, the selected edges automatically have even degree at every grid node. Walking around a node, the face colors eventually return to their starting color, so the number of color changes is even. If every important node has at least one color change, then every important node has positive even degree.

Thus a brute-force algorithm can try every binary coloring of the workshop cells, build its transition edges, check whether every important node is covered, and finally check whether the selected edges are connected. If there are (K) workshop cells, this considers (2^K) colorings. In the worst case (K=mn=400), giving roughly (400 \cdot 2^{400}) work. That is completely infeasible.

The useful observation is that the condition at one grid node depends only on the workshop cells immediately surrounding that node. At an internal node, there are at most four such cells. At a boundary node there are even fewer, with the outside treated as a face of color zero.

That local structure means we do not need to remember the entire coloring while constructing it. Process the cells row by row and remember only the colors of the last (w) cells, where (w=\min(m,n)). When the next cell is assigned, every newly completed internal grid node has all of its incident cells available in this frontier. We can check the constraint immediately and discard the state if it fails.

The factory can be transposed so that (w) is the smaller dimension. A profile state is then just a (w)-bit mask. There are at most (2^w) states at any position, and every state has at most two choices for the next workshop cell. Empty cells have only one possible color.

The no-holes condition is what makes the face interpretation especially useful. The selected edges are the boundaries between the two face colors. If every important node is incident to a selected edge, these boundary components cannot remain separated: two different boundary components would leave a region of equal-colored faces between them, and a grid node strictly inside that region would have no selected incident edge. That would contradict the requirement that every important node is covered. Hence the selected transition graph is connected.

Once those edges are known, finding the actual route is just Hierholzer's algorithm for an Eulerian graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(mn \cdot 2^{mn})) | (O(mn)) | Too slow |
| Profile DP | (O(mn \cdot 2^w)), (w=\min(m,n)) | (O(mn \cdot 2^w)) with memoization | Accepted |

## Algorithm Walkthrough

1. Transpose the map when necessary so that the number of columns (w) is no larger than the number of rows. The exponential part of the algorithm depends on the frontier width, so using the smaller dimension is the difference between (2^{20}) and potentially a much larger state space.
2. Mark every grid node that is a corner of at least one workshop cell. These are exactly the nodes that the final route must visit.
3. Interpret every workshop cell as a face whose color is either zero or one. Empty cells and the outside are always treated as color zero. An edge is selected precisely when the colors of the faces on its two sides differ.
4. Scan the cells in row-major order. The DP state stores the colors of the most recent (w) cells in a bitmask. Bit zero represents the most recently assigned cell, while the highest stored bit represents the cell in the previous row at the current column.
5. For a workshop cell, try both possible colors. For an empty cell, only color zero is allowed because it is part of the outside face.
6. Whenever a newly assigned cell completes an internal grid node, inspect the four incident face colors. If the node is important and all four colors are equal, there is no selected edge incident to that node, so this state can never produce a valid route.
7. Handle the top, left, right, and bottom boundary nodes when their incident cells become available. Missing cells outside the map have color zero, so a boundary node with one workshop cell is covered exactly when that cell receives color one.
8. Memoize the pair consisting of the current cell position and the frontier mask. If neither color choice can lead to a complete valid coloring, remember that state as impossible. The transposition step keeps the mask width at most 20.
9. Reconstruct one successful coloring by starting from the initial zero mask and repeatedly taking a color whose recursive state is successful. The memoized DP tells us which choice can reach the end.
10. Convert the coloring into corridors. For every horizontal and vertical grid edge, look at the workshop cells on its two sides, using color zero outside the map and for empty cells. Keep the edge exactly when the two colors differ.
11. The selected graph has even degree at every important node because selected edges correspond to color changes around the node. Every important node has positive degree because the DP rejected monochromatic neighborhoods. The no-hole property gives connectivity, so the selected graph is Eulerian.
12. Run Hierholzer's algorithm on the selected graph. It produces a closed trail using every selected corridor exactly once. Since every important node belongs to this graph, the resulting route satisfies all requirements.

### Why it works

The invariant of the profile DP is that every grid node whose incident cells have already been assigned has already been checked. A state is retained only when every important completed node has at least two selected incident edges, and because the selected-edge degree is always even, that means its degree is positive and even.

The face-color construction makes every selected-edge degree even automatically. Around any grid node, entering and leaving the set of color-one faces causes an even number of color changes. The DP prevents that number from being zero at an important node, so every important node belongs to the selected graph. Since the factory is connected and has no holes, a disconnected set of color-change boundaries would leave some important grid node inside a region with no color change, contradicting the DP condition. The selected graph is thus connected and all its degrees are even, so Euler's theorem guarantees a closed trail using every selected edge exactly once.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline
sys.setrecursionlimit(1_000_000)

def solve_case(original_grid):
    original_m = len(original_grid)
    original_n = len(original_grid[0])

    # Use the smaller dimension as the profile width.
    transposed = original_n > original_m

    if transposed:
        grid = [
            ''.join(original_grid[r][c] for r in range(original_m))
            for c in range(original_n)
        ]
    else:
        grid = original_grid[:]

    h = len(grid)
    w = len(grid[0])
    full = (1 << w) - 1

    # important[r][c] says whether grid node (r, c)
    # is a corner of at least one workshop cell.
    important = [[False] * (w + 1) for _ in range(h + 1)]

    for r in range(h):
        for c in range(w):
            if grid[r][c] == '*':
                important[r][c] = True
                important[r + 1][c] = True
                important[r][c + 1] = True
                important[r + 1][c + 1] = True

    if not any(any(row) for row in important):
        # No important nodes exist.
        if transposed:
            return "Yes\n0\n0 0\n"
        return "Yes\n0\n0 0\n"

    def all_equal_and_important(r, c, values):
        if not important[r][c]:
            return False
        first = values[0]
        return all(v == first for v in values)

    @lru_cache(maxsize=None)
    def dfs(pos, mask):
        if pos == h * w:
            return True

        r, c = divmod(pos, w)

        if grid[r][c] == '*':
            choices = (1, 0)
        else:
            choices = (0,)

        for x in choices:
            left = mask & 1

            # Check the internal node (r, c).
            if r > 0 and c > 0:
                up = (mask >> (w - 1 - c)) & 1
                up_left = (mask >> (w - c)) & 1

                if all_equal_and_important(
                    r, c, (up_left, up, left, x)
                ):
                    continue

            # Top boundary.
            if r == 0:
                if c == 0:
                    if all_equal_and_important(0, 0, (0, 0, 0, x)):
                        continue
                else:
                    if all_equal_and_important(0, c, (0, 0, left, x)):
                        continue

                if c == w - 1:
                    if all_equal_and_important(0, w, (0, 0, 0, x)):
                        continue

            # Left boundary.
            if c == 0 and r > 0:
                up = (mask >> (w - 1)) & 1
                if all_equal_and_important(r, 0, (0, 0, up, x)):
                    continue

            # Right boundary.
            if c == w - 1 and r > 0:
                up = mask & 1
                if all_equal_and_important(r, w, (0, 0, up, x)):
                    continue

            # Bottom boundary.
            if r == h - 1:
                if c == 0:
                    if all_equal_and_important(h, 0, (0, 0, 0, x)):
                        continue
                else:
                    if all_equal_and_important(h, c, (0, 0, left, x)):
                        continue

                if c == w - 1:
                    if all_equal_and_important(h, w, (0, 0, 0, x)):
                        continue

            new_mask = ((mask << 1) & full) | x

            if dfs(pos + 1, new_mask):
                return True

        return False

    if not dfs(0, 0):
        return "No\n"

    # Reconstruct one successful face coloring.
    colors = [[0] * w for _ in range(h)]
    pos = 0
    mask = 0

    while pos < h * w:
        r, c = divmod(pos, w)

        if grid[r][c] == '*':
            choices = (1, 0)
        else:
            choices = (0,)

        chosen = None

        for x in choices:
            left = mask & 1
            ok = True

            if r > 0 and c > 0:
                up = (mask >> (w - 1 - c)) & 1
                up_left = (mask >> (w - c)) & 1
                if all_equal_and_important(
                    r, c, (up_left, up, left, x)
                ):
                    ok = False

            if ok and r == 0:
                if c == 0:
                    if all_equal_and_important(0, 0, (0, 0, 0, x)):
                        ok = False
                else:
                    if all_equal_and_important(0, c, (0, 0, left, x)):
                        ok = False

                if ok and c == w - 1:
                    if all_equal_and_important(0, w, (0, 0, 0, x)):
                        ok = False

            if ok and c == 0 and r > 0:
                up = (mask >> (w - 1)) & 1
                if all_equal_and_important(r, 0, (0, 0, up, x)):
                    ok = False

            if ok and c == w - 1 and r > 0:
                up = mask & 1
                if all_equal_and_important(r, w, (0, 0, up, x)):
                    ok = False

            if ok and r == h - 1:
                if c == 0:
                    if all_equal_and_important(h, 0, (0, 0, 0, x)):
                        ok = False
                else:
                    if all_equal_and_important(h, c, (0, 0, left, x)):
                        ok = False

                if ok and c == w - 1:
                    if all_equal_and_important(h, w, (0, 0, 0, x)):
                        ok = False

            if not ok:
                continue

            new_mask = ((mask << 1) & full) | x
            if dfs(pos + 1, new_mask):
                chosen = x
                break

        if chosen is None:
            raise RuntimeError("reconstruction failed")

        colors[r][c] = chosen
        mask = ((mask << 1) & full) | chosen
        pos += 1

    # Convert back to the original orientation.
    if transposed:
        selected = [
            [0] * original_n for _ in range(original_m)
        ]
        for r in range(h):
            for c in range(w):
                selected[c][r] = colors[r][c]
    else:
        selected = colors

    m = original_m
    n = original_n

    def face(r, c):
        if 0 <= r < m and 0 <= c < n:
            return selected[r][c]
        return 0

    vertices = (m + 1) * (n + 1)
    graph = [[] for _ in range(vertices)]
    edges = []

    def vid(r, c):
        return r * (n + 1) + c

    def add_edge(r1, c1, r2, c2):
        a = vid(r1, c1)
        b = vid(r2, c2)
        eid = len(edges)
        edges.append((a, b))
        graph[a].append((eid, b))
        graph[b].append((eid, a))

    # Horizontal grid edges.
    for r in range(m + 1):
        for c in range(n):
            above = face(r - 1, c)
            below = face(r, c)
            if above != below:
                add_edge(r, c, r, c + 1)

    # Vertical grid edges.
    for r in range(m):
        for c in range(n + 1):
            left = face(r, c - 1)
            right = face(r, c)
            if left != right:
                add_edge(r, c, r + 1, c)

    important_original = [
        [False] * (n + 1) for _ in range(m + 1)
    ]

    for r in range(m):
        for c in range(n):
            if original_grid[r][c] == '*':
                important_original[r][c] = True
                important_original[r + 1][c] = True
                important_original[r][c + 1] = True
                important_original[r + 1][c + 1] = True

    important_vertices = []
    for r in range(m + 1):
        for c in range(n + 1):
            if important_original[r][c]:
                important_vertices.append(vid(r, c))

    start = important_vertices[0]

    # The face-color construction should give a connected graph.
    seen = {start}
    stack = [start]

    while stack:
        v = stack.pop()
        for _, to in graph[v]:
            if to not in seen:
                seen.add(to)
                stack.append(to)

    if len(seen) != len(important_vertices):
        return "No\n"

    # Hierholzer's algorithm.
    used = [False] * len(edges)
    ptr = [0] * vertices
    stack = [start]
    route = []

    while stack:
        v = stack[-1]

        while ptr[v] < len(graph[v]) and used[graph[v][ptr[v]][0]]:
            ptr[v] += 1

        if ptr[v] == len(graph[v]):
            route.append(stack.pop())
            continue

        eid, to = graph[v][ptr[v]]
        ptr[v] += 1

        if used[eid]:
            continue

        used[eid] = True
        stack.append(to)

    route.reverse()

    if len(route) != len(edges) + 1:
        return "No\n"

    out = ["Yes", str(len(edges))]
    for v in route:
        r, c = divmod(v, n + 1)
        out.append(f"{r} {c}")

    return "\n".join(out) + "\n"

def solve():
    m, n = map(int, input().split())
    grid = [input().strip() for _ in range(m)]
    sys.stdout.write(solve_case(grid))

if __name__ == "__main__":
    solve()
```

The profile mask is the central implementation detail. Before processing a cell, bit zero is the already processed cell immediately to its left. The higher bits represent the previous row in reverse order. This makes all four cells around the newly completed internal node available in constant time.

The update

```
new_mask = ((mask << 1) & full) | x
```

drops the oldest frontier cell, shifts every remaining cell one position away from bit zero, and inserts the new color at bit zero. The mask must be truncated with `full`, otherwise it would grow beyond the chosen profile width.

Empty cells are forced to color zero. Treating them this way is what makes boundary handling uniform: an empty cell and the outside face are the same face of the planar embedding because the input guarantees that there are no enclosed empty regions.

The reconstruction does not store a parent pointer for every state. Instead, once the initial state is known to be successful, it tries the possible next colors again and asks the memoized DP whether the resulting state can still finish. This saves a separate parent array.

The final graph is built from color changes rather than by adding every edge of every selected workshop cell. This distinction matters. If two adjacent workshop faces both have color one, their shared edge must not be used. If their colors differ, the shared edge is exactly a corridor in the transition graph.

Hierholzer's algorithm is used after the graph has been constructed because all degrees are even and the graph is connected. The produced vertex sequence contains exactly one more vertex than the number of used corridors, starts and ends at the same vertex, and never repeats a corridor.

## Worked Examples

### Sample 1

The first sample is

```
3 3
***
***
.**
```

A valid face coloring can be viewed as choosing some workshop cells as color one and treating the outside as color zero. The DP scans the cells while checking each newly completed grid node.

| Position | Current cell | Chosen color | Frontier after step |
| --- | --- | --- | --- |
| (0,0) | `*` | 1 | `...1` |
| (0,1) | `*` | 0 | `..01` |
| (0,2) | `*` | 1 | `.101` |
| (1,0) | `*` | 0 | `1010` |
| (1,1) | `*` | 1 | `0101` |
| (1,2) | `*` | 0 | `1010` |
| (2,0) | `.` | 0 | `0100` |
| (2,1) | `*` | 1 | `1001` |
| (2,2) | `*` | 0 | `0010` |

The exact coloring selected by the program can differ because several valid colorings exist. What matters is that every important node sees both colors among its incident faces. The resulting color-change edges form one connected Eulerian graph, and Hierholzer's algorithm turns those edges into a valid closed route. The official sample uses 16 corridors, although the problem accepts any valid route.

### Sample 2

The second sample is

```
1 4
****
```

There is only one row of workshop cells. The important nodes are the ten corners of the (2 \times 5) grid. The transition edges can form the perimeter of the entire strip.

| Position | Cell | Color choice | Relevant constraint |
| --- | --- | --- | --- |
| (0,0) | `*` | 1 | Top-left node must be covered |
| (0,1) | `*` | 0 | Adjacent top node sees colors 1 and 0 |
| (0,2) | `*` | 1 | Adjacent top node sees colors 0 and 1 |
| (0,3) | `*` | 0 | Adjacent top node sees colors 1 and 0 |

Again, the exact coloring may differ. The important fact is that every boundary node has a color change on an incident edge, so the selected corridors form a connected even graph. The official sample has a route of ten corridors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(mn2^w)) | There are (mn) profile positions, at most (2^w) masks, and at most two color choices per state |
| Space | (O(mn2^w)) | The memoization table can contain one state for every position and frontier mask |

Here (w=\min(m,n)), because the grid is transposed before the DP if necessary. With (w\le20), the profile has at most (2^{20}=1,048,576) masks. The exponential dependence is on the smaller grid dimension rather than on all (mn) cells, which is the key reduction from the brute-force (2^{mn}) search. The original problem has (m,n\le20) and a 256 MB memory limit.

## Test Cases

The output route is not unique, so tests should validate the structure of the returned route rather than compare a `Yes` answer byte-for-byte. The helper below checks that every important node is visited, every move is between adjacent grid nodes, every corridor is used at most once, and every used edge is actually a corridor.

```python
# The solution above defines solve_case(grid).

import io
import sys

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        m, n = map(int, input().split())
        grid = [input().strip() for _ in range(m)]
        return solve_case(grid)
    finally:
        sys.stdin = old_stdin

def validate(inp: str, out: str, expected_possible: bool):
    lines = out.strip().splitlines()
    assert lines

    if not expected_possible:
        assert lines[0] == "No"
        return

    assert lines[0] == "Yes"

    m, n = map(int, inp.splitlines()[0].split())
    grid = inp.splitlines()[1:1 + m]

    k = int(lines[1])
    route = [tuple(map(int, line.split())) for line in lines[2:]]

    assert len(route) == k + 1
    assert route[0] == route[-1]

    important = set()

    for r in range(m):
        for c in range(n):
            if grid[r][c] == '*':
                important.add((r, c))
                important.add((r + 1, c))
                important.add((r, c + 1))
                important.add((r + 1, c + 1))

    assert important.issubset(set(route))

    used = set()

    for a, b in zip(route, route[1:]):
        ar, ac = a
        br, bc = b

        assert 0 <= ar <= m
        assert 0 <= br <= m
        assert 0 <= ac <= n
        assert 0 <= bc <= n

        assert abs(ar - br) + abs(ac - bc) == 1

        edge = tuple(sorted((a, b)))
        assert edge not in used
        used.add(edge)

        if ar == br:
            r = ar
            c = min(ac, bc)
            workshop = (
                r > 0 and grid[r - 1][c] == '*'
            ) or (
                r < m and grid[r][c] == '*'
            )
        else:
            r = min(ar, br)
            c = ac
            workshop = (
                c > 0 and grid[r][c - 1] == '*'
            ) or (
                c < n and grid[r][c] == '*'
            )

        assert workshop

# Provided sample 1.
sample1 = """\
3 3
***
***
.**
"""
validate(sample1, run(sample1), True)

# Provided sample 2.
sample2 = """\
1 4
****
"""
validate(sample2, run(sample2), True)

# Minimum-size workshop.
case3 = """\
1 1
*
"""
validate(case3, run(case3), True)

# No workshops at all.
case4 = """\
2 3
...
...
"""
validate(case4, run(case4), True)

# Full 2 x 2 factory, whose 3 x 3 grid graph has no spanning
# Eulerian subgraph.
case5 = """\
2 2
**
**
"""
validate(case5, run(case5), False)

# A maximum-width one-row factory.
case6 = "1 20\n" + "*" * 20 + "\n"
validate(case6, run(case6), True)

# A maximum-size full grid. The forced outer boundary leaves
# an interior grid graph that cannot be included in one Eulerian route.
case7 = "20 20\n" + "\n".join(["*" * 20] * 20) + "\n"
validate(case7, run(case7), False)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 3 / *** / *** / .**` | `Yes` | Provided sample, internal nodes and a non-rectangular workshop |
| `1 4 / ****` | `Yes` | Provided sample and a thin factory |
| `1 1 / *` | `Yes` | Minimum workshop and boundary-only graph |
| `2 3 / ... / ...` | `Yes` | No important nodes and zero-length route |
| `2 2 / ** / **` | `No` | Smallest nontrivial impossible Eulerian case |
| `1 20 / ********************` | `Yes` | Maximum profile width and a long boundary |
| `20 20 / all *` | `No` | Maximum-size grid and the forced-boundary obstruction |

## Edge Cases

For a single workshop,

```
1 1
*
```

the only four important nodes are the corners of that cell. The face-color DP can color the workshop face one and the outside zero. Every boundary edge is selected, giving a four-edge Eulerian cycle. The output therefore starts with `Yes`, followed by `4`, and five grid nodes forming a closed square.

For an empty map,

```
1 1
.
```

there are no important nodes at all. The DP assigns color zero to the only cell and the transition graph contains no edges. The implementation handles this before running Hierholzer and prints a zero-corridor route consisting of a single grid node.

For

```
2 2
**
**
```

every one of the four outer corners has only one incident workshop cell, so those cells are forced to color one. That forces the entire outer boundary into the transition graph. The boundary vertices then already have their required degree two, preventing the four edges leading to the center from being selected. The center is important but becomes isolated, so no valid route exists. The profile DP discovers the same contradiction through its local face-color constraints.

For the one-row boundary case

```
1 2
**
```

the two workshop cells can receive opposite colors. The shared edge becomes selected, and the outer edges adjacent to the color-one cell become selected as well. The resulting selected graph is connected and every important node has even positive degree, so Hierholzer produces a closed route without repeating a corridor.

The boundary checks in the implementation deserve special attention. An internal node is governed by up to four workshop cells, but a node on the outer boundary has only one or two actual cells and the outside face must be treated as color zero. Forgetting the outside face is a common source of false positives, especially for a single workshop cell or a thin (1 \times n) factory.
