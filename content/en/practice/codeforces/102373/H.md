---
title: "CF 102373H - Escape from the Abundoned House"
description: "The grid is a graph whose vertices are all non-wall cells, with edges between cells sharing a side. The friends start at s and need to reach f. Every horizontal move changes the temperature by -1, regardless of whether the move goes left or right."
date: "2026-08-12T23:09:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102373
codeforces_index: "H"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102373
solve_time_s: 456
verified: true
draft: false
---

[CF 102373H - Escape from the Abundoned House](https://codeforces.com/problemset/problem/102373/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid is a graph whose vertices are all non-wall cells, with edges between cells sharing a side. The friends start at `s` and need to reach `f`.

Every horizontal move changes the temperature by `-1`, regardless of whether the move goes left or right. Every vertical move changes it by `+1`, regardless of whether the move goes up or down. Thus, for a walk containing `H` horizontal moves and `V` vertical moves, the final temperature differs from the initial temperature by

[
V-H.
]

The friends may revisit cells and edges arbitrarily many times. We need the smallest possible value of

[
|V-H|.
]

If `f` is unreachable from `s`, the answer is `-1`.

The grid can contain up to (10^6) cells. That immediately rules out anything that stores a large state for every possible path length or temperature value. We need to inspect each cell and each local adjacency only a constant number of times, giving an (O(nm)) target. A traversal with linear memory also fits naturally because there are only (O(nm)) reachable cells.

There are several cases where a seemingly reasonable shortcut gives the wrong result.

Consider a single horizontal corridor.

```
1 3
s.f
```

The only useful path has two horizontal moves, so the temperature changes by `-2` and the answer is `2`. A solution that assumes the answer is always determined only by the parity of the path length would incorrectly return `0`, because this component has no vertical edge with which to compensate for horizontal moves.

The vertical analogue has the same issue.

```
3 1
s
.
f
```

Every move is vertical, so the shortest path changes the temperature by `+2`. The correct answer is `2`.

A disconnected exit must also be handled separately.

```
1 3
s#f
```

There is no walk from `s` to `f`, so the answer is `-1`. Running a calculation on the coordinates of `s` and `f` without checking connectivity would silently produce a finite value.

Finally, having both horizontal and vertical edges does not mean the answer is always zero. Consider

```
2 2
sf
..
```

There is a direct horizontal path with temperature change `-1`. Because the component contains both kinds of edges, we can change any walk's temperature change by multiples of `2`, but we can never change its parity. Since every `s` to `f` walk has odd length here, its temperature change is always odd. The correct answer is `1`.

## Approaches

A direct brute-force approach would enumerate walks from `s` and keep track of their accumulated temperature change. This is conceptually correct because every possible walk corresponds to one possible final temperature. The problem is that walks may revisit cells, so there are infinitely many walks. Even if we artificially restrict the search to walks of length at most (L), a grid vertex can have up to four choices at each step, giving (O(4^L)) candidate walks in the worst case. Increasing (L) does not solve the problem cleanly because a valid optimal walk may deliberately contain repetitions.

Trying to enumerate only simple paths is not a valid replacement. The statement explicitly allows revisiting cells, and those repetitions are exactly what let us compensate temperature changes.

The key observation comes from looking at one edge traversed twice. If the edge is horizontal, going across it and immediately coming back costs `-2`. If the edge is vertical, going across it and immediately coming back costs `+2`. Since the friends can insert such a round trip anywhere along a valid walk, the presence of a horizontal edge lets us decrease the total by `2` whenever we want, while the presence of a vertical edge lets us increase the total by `2` whenever we want.

Suppose the connected component containing `s` and `f` has both a horizontal edge and a vertical edge. Start with any `s` to `f` path whose temperature change is (W). By repeatedly inserting a horizontal round trip we can replace (W) by (W-2k), and by repeatedly inserting a vertical round trip we can replace it by (W+2k). Thus every integer having the same parity as (W) is achievable.

The parity of (W) is particularly simple. Every move changes the path length by one, and

[
V-H=(V+H)-2H.
]

Therefore (V-H) has the same parity as the total number of moves. Every path from `s` to `f` has the same length parity, because changing the parity of a grid coordinate requires one move. Consequently, when both edge types exist, the answer is `0` for an even path length and `1` for an odd path length.

There is one special case. If the component contains only horizontal edges, every possible walk has only horizontal moves, so its temperature change is exactly the negative of its length. The smallest absolute value is then obtained by the shortest path from `s` to `f`. The same reasoning applies if the component contains only vertical edges, except the temperature change is the positive path length.

A single BFS gives us everything we need. It finds the shortest distance to `f`, determines whether `f` is reachable, and while traversing the component it tells us whether at least one horizontal and at least one vertical edge are present.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded, (O(4^L)) for walks of length (L) | Unbounded with search depth | Too slow |
| Optimal | (O(nm)) | (O(nm)) | Accepted |

## Algorithm Walkthrough

1. Read the grid and locate the start cell `s` and exit cell `f`. Treat every character except `#` as traversable.
2. Run BFS from `s`. Store the shortest distance from `s` to every visited cell. BFS is appropriate because every grid move has unit length, so the first time a cell is reached gives its shortest path length.
3. While examining a cell and each of its reachable neighbors, classify the corresponding edge. If the row changes, the component contains a vertical edge. If the column changes, it contains a horizontal edge. We only need two boolean flags.
4. If `f` was never visited, output `-1`. The friends cannot reach the exit at all.
5. If the component contains both a horizontal and a vertical edge, output `dist[f] % 2`. The shortest path length determines the parity of every possible temperature change, and both signs of a change by `2` are available through edge round trips. Hence an even parity allows exact cancellation, while an odd parity leaves minimum absolute difference `1`.
6. If the component has only horizontal edges, output `dist[f]`. Every possible walk has temperature change equal to the negative of its length, so the shortest path is optimal.
7. If the component has only vertical edges, output `dist[f]` as well. Every possible walk has temperature change equal to its length, so again the shortest path is optimal.

### Why it works

The central invariant is that inserting a horizontal edge round trip changes the temperature by exactly `-2`, while inserting a vertical edge round trip changes it by exactly `+2`. If both edge types occur in the connected component, any walk's temperature change can be shifted by any even integer. The parity cannot change, because the temperature change (V-H) has the same parity as the number of moves, and every `s` to `f` walk has the same endpoint parity. Thus the closest achievable value to zero is exactly `0` for even parity and `1` for odd parity.

If only one edge type exists, every walk has a fixed sign of temperature change and its magnitude equals its length. The shortest path consequently minimizes the absolute temperature difference. BFS computes that shortest length exactly.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    start = None
    finish = None

    for r in range(n):
        for c in range(m):
            if grid[r][c] == 's':
                start = (r, c)
            elif grid[r][c] == 'f':
                finish = (r, c)

    sr, sc = start
    fr, fc = finish

    dist = [[-1] * m for _ in range(n)]
    dist[sr][sc] = 0

    q = deque([(sr, sc)])

    has_horizontal = False
    has_vertical = False

    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while q:
        r, c = q.popleft()

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if nr < 0 or nr >= n or nc < 0 or nc >= m:
                continue
            if grid[nr][nc] == '#':
                continue

            if dr == 0:
                has_horizontal = True
            else:
                has_vertical = True

            if dist[nr][nc] != -1:
                continue

            dist[nr][nc] = dist[r][c] + 1
            q.append((nr, nc))

    d = dist[fr][fc]

    if d == -1:
        print(-1)
        return

    if has_horizontal and has_vertical:
        print(d & 1)
    else:
        print(d)

if __name__ == "__main__":
    solve()
```

The grid is stored as a list of strings, so checking whether a cell is a wall is a constant-time operation. The two special cells are located in the initial scan.

The BFS distance array uses `-1` for unvisited cells and `0` for the start. Since every legal move costs one step, `dist[f]` is the shortest path length whenever the exit is reachable.

The edge-type flags are updated only for valid, non-wall neighbors. A horizontal adjacency is detected by `dr == 0`, while a vertical adjacency has `dr != 0`. The same edge may be encountered from both endpoints, but setting a boolean twice has no effect.

The boundary checks must happen before indexing the grid. This avoids accidentally treating negative Python indices as valid cells, which is an especially easy bug to introduce in grid BFS.

There is no integer overflow issue in Python. Even in a C++ implementation, the maximum shortest distance is only (O(nm)), so a standard integer type is sufficient.

The final decision deliberately uses the BFS distance rather than the actual temperature change of that path. Once both edge types exist, only its parity matters. When one type is missing, the distance itself is the minimum possible absolute change.

## Worked Examples

### Sample 1

The grid is

```
4 3
..f
..#
s##
...
```

Starting at `(2,0)`, BFS can reach `(1,0)`, then `(0,0)`, then the exit `(0,2)`. The component contains both vertical and horizontal edges.

| Current cell | Distance | New cell | Edge type | New distance |
| --- | --- | --- | --- | --- |
| `(2,0)` | 0 | `(1,0)` | Vertical | 1 |
| `(1,0)` | 1 | `(0,0)` | Vertical | 2 |
| `(0,0)` | 2 | `(0,1)` | Horizontal | 3 |
| `(0,1)` | 3 | `(0,2)` | Horizontal | 4 |

The shortest distance to `f` is `4`, which is even. Because the component has both edge types, the answer is `4 % 2 = 0`.

The direct path itself already has two vertical and two horizontal moves, giving temperature change `2 - 2 = 0`. The BFS parity argument confirms that exact cancellation is possible.

### Custom Example 2

Consider a one-row corridor.

```
1 3
s.f
```

There are no vertical edges.

| Current cell | Distance | New cell | Edge type | New distance |
| --- | --- | --- | --- | --- |
| `(0,0)` | 0 | `(0,1)` | Horizontal | 1 |
| `(0,1)` | 1 | `(0,2)` | Horizontal | 2 |

The exit has distance `2`, and the component contains only horizontal edges. Every possible walk has temperature change equal to the negative of its length. The shortest possible length is `2`, so the answer is `2`.

This example demonstrates why the presence of both edge types must be checked rather than simply returning the parity of the shortest path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm)) | Every cell is inserted into BFS at most once, and each visited cell checks at most four neighbors. |
| Space | (O(nm)) | The grid, distance array, and BFS queue use linear space in the number of cells. |

With (n,m \le 1000), there are at most (10^6) cells. The algorithm performs only a constant amount of work per cell and adjacency, so it scales linearly with the entire grid rather than with the number of possible walks. The memory consumption is also linear and remains practical for a million-cell grid.

## Test Cases

```python
import sys
import io
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    start = None
    finish = None

    for r in range(n):
        for c in range(m):
            if grid[r][c] == 's':
                start = (r, c)
            elif grid[r][c] == 'f':
                finish = (r, c)

    sr, sc = start
    fr, fc = finish

    dist = [[-1] * m for _ in range(n)]
    dist[sr][sc] = 0

    q = deque([(sr, sc)])

    has_horizontal = False
    has_vertical = False

    for_dr_dc = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while q:
        r, c = q.popleft()

        for dr, dc in for_dr_dc:
            nr = r + dr
            nc = c + dc

            if nr < 0 or nr >= n or nc < 0 or nc >= m:
                continue
            if grid[nr][nc] == '#':
                continue

            if dr == 0:
                has_horizontal = True
            else:
                has_vertical = True

            if dist[nr][nc] != -1:
                continue

            dist[nr][nc] = dist[r][c] + 1
            q.append((nr, nc))

    d = dist[fr][fc]

    if d == -1:
        print(-1)
    elif has_horizontal and has_vertical:
        print(d & 1)
    else:
        print(d)

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

assert run(
    """4 3
..f
..#
s##
...
"""
) == "0", "sample 1"

assert run(
    """1 2
sf
"""
) == "1", "minimum horizontal case"

assert run(
    """1 3
s.f
"""
) == "2", "horizontal-only component"

assert run(
    """3 1
s
.
f
"""
) == "2", "vertical-only component"

assert run(
    """1 3
s#f
"""
) == "-1", "unreachable exit"

assert run(
    """2 2
sf
..
"""
) == "1", "both edge types with odd distance"

n = 1000
m = 1000
rows = [['.'] * m for _ in range(n)]
rows[0][0] = 's'
rows[n - 1][m - 1] = 'f'
large_input = f"{n} {m}\n" + "\n".join("".join(row) for row in rows) + "\n"

assert run(large_input) == "0", "maximum-size open grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 x 3` sample grid | `0` | Provided sample and a component containing both edge types |
| `1 x 2`, `sf` | `1` | Minimum possible grid and a single horizontal edge |
| `1 x 3`, `s.f` | `2` | Horizontal-only component where parity alone is insufficient |
| `3 x 1`, `s`, `.`, `f` | `2` | Vertical-only component |
| `1 x 3`, `s#f` | `-1` | Connectivity and unreachable exit |
| `2 x 2`, `sf`, `..` | `1` | Both edge types exist, but every `s` to `f` walk has odd parity |
| `1000 x 1000` open grid | `0` | Maximum dimensions, BFS scalability, and even endpoint parity |

## Edge Cases

For the horizontal-only case

```
1 3
s.f
```

BFS reaches the exit at distance `2`. During the traversal it sets `has_horizontal` to `True`, but `has_vertical` remains `False`. The algorithm consequently takes the single-direction branch and outputs `2`. Repeatedly traversing an available horizontal edge can only add another `-2` to the temperature change, so no detour can improve on the shortest path.

For the vertical-only case

```
3 1
s
.
f
```

BFS again obtains distance `2`, but this time only `has_vertical` becomes true. Every walk has temperature change equal to its length, so its absolute change is at least `2`. The algorithm outputs `2`.

For a component containing both edge types,

```
2 2
sf
..
```

the first horizontal move reaches `f` with distance `1`. BFS also encounters vertical edges elsewhere in the component, so both flags become true. The algorithm outputs `1 & 1 = 1`. A vertical round trip can add `+2`, and a horizontal round trip can add `-2`, but neither operation changes the odd parity, so zero is impossible.

For the disconnected case,

```
1 3
s#f
```

BFS visits only the start cell because the middle cell is a wall. `dist[f]` remains `-1`, and the algorithm immediately outputs `-1`. No temperature calculation is attempted for a nonexistent path.

For the maximum-size case, a completely open (1000 \times 1000) grid has both horizontal and vertical edges. If `s` is at `(0,0)` and `f` is at `(999,999)`, the shortest distance is `1998`, which is even. The algorithm therefore returns `0`. Even though the shortest path itself is long, BFS processes each of the at most one million cells only once, preserving the (O(nm)) bound.
