---
title: "CF 102386G - \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0438\u0435 \u0431\u043b\u0438\u043d\u0447\u0438\u043a\u0438"
description: "Think of every non-burnt cell as a vertex of a graph. Two vertices are connected when their cells share a side. The statement guarantees that this graph is connected."
date: "2026-08-12T21:44:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "G"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 530
verified: true
draft: false
---

[CF 102386G - \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0438\u0435 \u0431\u043b\u0438\u043d\u0447\u0438\u043a\u0438](https://codeforces.com/problemset/problem/102386/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of every non-burnt cell as a vertex of a graph. Two vertices are connected when their cells share a side. The statement guarantees that this graph is connected. Every pancake initially occupies its own vertex, and every move takes the top pancake from one vertex to an adjacent vertex. A move flips that pancake, so after an odd number of moves it is correctly oriented, while after an even number it has returned to its original orientation.

Stacks make the problem deceptive. A pancake may temporarily share a cell with other pancakes, but only the top pancake can move again. At the end, every pancake must be alone and every pancake must have moved an odd number of times.

The grid graph is bipartite. Color a cell black when the sum of its row and column indices is even, and white otherwise. Every move goes between opposite colors. Consequently, a pancake that starts on black and eventually becomes correctly oriented must finish on white, and a pancake starting on white must finish on black. The final positions are distinct, so the number of pancakes initially on black cannot exceed the number of white cells, and symmetrically the number initially on white cannot exceed the number of black cells.

With at most 100 rows and 100 columns, there are at most 10,000 usable cells. A linear or near-linear graph algorithm is easily fast enough for the one-second limit. An algorithm depending exponentially on the number of pancakes is completely infeasible, because the maximum number of pancakes is also 10,000.

There is one structural edge case that the color-count condition alone misses. Consider

```
1 2
PP
```

There is one black cell and one white cell, so the counts look perfectly balanced. Nevertheless the answer is `NO`. With only two adjacent cells, whichever pancake is moved onto the other one becomes the top pancake. It must move back before the pancake underneath can be accessed, so the two pancakes cannot be exchanged. More generally, when every usable cell is occupied, we need a cycle in the usable-cell graph to provide a genuine buffer.

Another easy case to mishandle is the sample

```
1 3
P.P
```

The two pancakes are both on cells of the same color, while there is only one cell of the opposite color. Both pancakes would have to finish on distinct opposite-colored cells, which is impossible. The answer is `NO`.

A final edge case is a single pancake. For example,

```
1 2
P.
```

has one black pancake and one white target cell, so the answer is `YES`. The pancake simply moves once. Any solution that requires at least two pancakes would incorrectly reject this case.

## Approaches

A direct brute-force solution would treat the entire arrangement as a state. A state has to record the position of every pancake, its orientation, and the order of pancakes inside every stack. From each state we can try moving the top pancake of every nonempty cell to each adjacent usable cell. A breadth-first search would be correct because every legal operation is represented by one transition, and reaching a state with all pancakes correctly oriented and separated proves that a valid sequence exists.

The problem is the size of that state space. If there are (V) usable cells and (k) pancakes, merely choosing a cell for each labeled pancake gives (V^k) possibilities. Orientations multiply this by (2^k), and possible orders inside stacks add another factorial-sized component. Even the much smaller upper bound (2^kV^k) is already hopeless for (k,V) around 10,000. The brute force is useful for understanding the rules, but not for solving the actual constraints.

The key observation is that the exact sequence of moves is unnecessary. Every move changes both the pancake's position color and its orientation. Thus a pancake starting on black can be correct only when it finishes on white, and a pancake starting on white can be correct only when it finishes on black. This gives the necessary color-capacity inequalities immediately.

The surprising part is that these inequalities are also sufficient whenever there is at least one empty usable cell. Because the usable graph is connected, that empty cell can be transported through the graph and used as a buffer. Stacks allow pancakes to pass through occupied vertices while the buffer is moved around. Consequently, we can realize the required redistribution of pancakes between the two color classes.

If every usable cell already contains a pancake, there is no empty buffer. In that case a cycle is necessary and sufficient. On a cycle, pancakes can be shifted around it, so every pancake on the cycle can move an odd number of times without leaving a stack behind. The cycle then acts as the missing workspace for rearranging the remaining part of the connected graph. A connected graph without a cycle is a tree, and with every vertex occupied there is no way to create a permanent workspace and change the required arrangement.

Thus the entire problem reduces to two checks: the bipartite color capacities, and, only when every usable cell is occupied, whether the usable-cell graph contains a cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^kV^k k!)) states in the worst case | (O(2^kV^k k!)) | Too slow |
| Optimal | (O(nm)) | (O(nm)) | Accepted |

## Algorithm Walkthrough

1. Treat every cell different from `#` as a vertex of the usable graph. Color it black or white according to ((i+j)\bmod 2). This is a valid bipartition because every legal move changes exactly one row or one column by one.
2. Count the total number of usable black and white cells, and separately count how many pancakes initially occupy black and white cells. If the number of black pancakes is greater than the number of white usable cells, print `NO`. If the number of white pancakes is greater than the number of black usable cells, print `NO`. Each pancake must finish on the opposite color, and final cells cannot contain two pancakes.
3. Count the usable cells and the pancakes. If the number of pancakes is smaller than the number of usable cells, at least one cell is empty. The connected graph can then use that empty cell as a moving buffer, so the color inequalities are sufficient. Print `YES`.
4. If every usable cell contains a pancake, the color inequalities imply that the two color classes have equal size. We now need to determine whether the usable graph contains a cycle. Count every pair of adjacent usable cells as an undirected edge. Because the graph is connected, it contains a cycle exactly when the number of edges is at least the number of vertices.
5. If the full usable graph contains a cycle, print `YES`; otherwise print `NO`. A connected acyclic graph is a tree, and when every vertex is occupied there is no empty cell or cycle available to rearrange the pancakes.

Why it works: every legal move crosses the bipartition and flips the pancake, so a correctly oriented pancake must end in the color opposite to its starting cell. This proves the two capacity inequalities are necessary. When an empty cell exists, connectivity lets us use it as a buffer while moving pancakes through the graph, and the stack rule permits temporary collisions. When there is no empty cell, a cycle is exactly the structure that supplies a closed buffer route. A tree has no such route, while a cycle lets the occupied configuration be rotated and the remaining connected parts be processed through it. Hence the checks above characterize precisely when a valid sequence exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    cells = 0
    pancakes = 0

    black_cells = 0
    white_cells = 0
    black_pancakes = 0
    white_pancakes = 0

    edges = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                continue

            cells += 1

            if (i + j) % 2 == 0:
                black_cells += 1
            else:
                white_cells += 1

            if grid[i][j] == 'P':
                pancakes += 1
                if (i + j) % 2 == 0:
                    black_pancakes += 1
                else:
                    white_pancakes += 1

            if i + 1 < n and grid[i + 1][j] != '#':
                edges += 1
            if j + 1 < m and grid[i][j + 1] != '#':
                edges += 1

    if black_pancakes > white_cells:
        print("NO")
        return

    if white_pancakes > black_cells:
        print("NO")
        return

    if pancakes < cells:
        print("YES")
        return

    # Every usable cell is occupied.
    # The usable graph is connected, so it has a cycle iff E >= V.
    if edges >= cells:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The first loop classifies every usable cell by the parity of its coordinates. Using zero-based indices does not change the bipartition, because adding one to both coordinates changes their sum by two.

The two pancake counters record the colors of the initial positions. They are compared against the number of available cells of the opposite color, since every pancake that finishes correctly must have crossed the bipartition an odd number of times.

The edge counter only looks down and right. Every horizontal or vertical edge is consequently counted exactly once, avoiding both double counting and a separate graph data structure.

The `pancakes < cells` check is the critical distinction between the two structural cases. If there is at least one empty usable cell, the buffer argument applies. If all usable cells are occupied, we need to inspect the graph for a cycle.

Because the usable region is guaranteed to be connected, the standard characterization of a tree applies: a connected graph with (V) vertices is acyclic exactly when it has (V-1) edges. Thus `edges >= cells` detects a cycle without DFS or a disjoint-set structure.

No arithmetic can exceed a few tens of thousands, so integer overflow is not an issue in Python or in a typical C++ implementation.

## Worked Examples

### Sample 1

The input is

```
1 3
P.P
```

Using zero-based coordinates, cells 0 and 2 have the same color.

| Variable | After scanning |
| --- | --- |
| `cells` | 3 |
| `pancakes` | 2 |
| `black_cells` | 2 |
| `white_cells` | 1 |
| `black_pancakes` | 2 |
| `white_pancakes` | 0 |

The condition `black_pancakes > white_cells` is (2 > 1), so the algorithm immediately prints `NO`.

This demonstrates why simply checking that there are free cells is insufficient. There is one free cell, but both pancakes need distinct cells of the opposite color after being flipped.

### Sample 2

The input is

```
2 2
PP
PP
```

The four cells form a 4-cycle, with two cells of each color.

| Variable | After scanning |
| --- | --- |
| `cells` | 4 |
| `pancakes` | 4 |
| `black_cells` | 2 |
| `white_cells` | 2 |
| `black_pancakes` | 2 |
| `white_pancakes` | 2 |
| `edges` | 4 |

Both color-capacity inequalities hold. Since `pancakes == cells`, the algorithm checks for a cycle. Here `edges >= cells`, because (4 \ge 4), so the answer is `YES`.

The cycle provides exactly the workspace that is missing in the two-cell case. The four pancakes can be shifted around the square, moving each one to the opposite color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm)) | Every grid cell is inspected once and only constant work is performed for each cell. |
| Space | (O(nm)) | The grid itself uses (O(nm)) memory; all additional counters use (O(1)). |

At the maximum size, the grid contains only 10,000 cells, so the algorithm performs a few constant-time checks per cell. It is comfortably within the one-second and 256 MB limits of the contest problem.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    cells = 0
    pancakes = 0
    black_cells = 0
    white_cells = 0
    black_pancakes = 0
    white_pancakes = 0
    edges = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                continue

            cells += 1

            if (i + j) % 2 == 0:
                black_cells += 1
            else:
                white_cells += 1

            if grid[i][j] == 'P':
                pancakes += 1
                if (i + j) % 2 == 0:
                    black_pancakes += 1
                else:
                    white_pancakes += 1

            if i + 1 < n and grid[i + 1][j] != '#':
                edges += 1
            if j + 1 < m and grid[i][j + 1] != '#':
                edges += 1

    if black_pancakes > white_cells:
        print("NO")
    elif white_pancakes > black_cells:
        print("NO")
    elif pancakes < cells:
        print("YES")
    elif edges >= cells:
        print("YES")
    else:
        print("NO")

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

# provided samples
assert run("1 3\nP.P\n") == "NO", "sample 1"
assert run("2 2\nPP\nPP\n") == "YES", "sample 2"
assert run("2 2\nPP\nP#\n") == "NO", "sample 3"

# minimum-size board, one pancake and one available neighbor
assert run("1 2\nP.\n") == "YES", "single pancake"

# two cells, both occupied, balanced colors but no cycle
assert run("1 2\nPP\n") == "NO", "occupied tree with two vertices"

# full 1 x 4 path, balanced colors but still no cycle
assert run("1 4\nPPPP\n") == "NO", "full occupied tree"

# maximum-size grid, all cells occupied, many cycles and balanced colors
grid = "\n".join(["P" * 100 for _ in range(100)])
assert run("100 100\n" + grid + "\n") == "YES", "maximum grid"

# a connected region with an empty cell and valid color capacities
assert run("2 3\nPP.\n...\n") == "YES", "empty buffer"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 / P.` | `YES` | Minimum nontrivial board and a single pancake. |
| `1 2 / PP` | `NO` | Balanced color counts are not sufficient when every vertex of a two-vertex tree is occupied. |
| `1 4 / PPPP` | `NO` | Full occupancy of a larger acyclic graph, catching solutions that only check color counts. |
| `100 100 / all P` | `YES` | Maximum grid size and the cycle condition on a large connected region. |
| `2 3 / PP. / ...` | `YES` | Presence of an empty buffer cell, where the color inequalities are sufficient. |

## Edge Cases

The first edge case is a board with two usable cells and two pancakes:

```
1 2
PP
```

There is one cell of each color, and one pancake of each color, so both capacity inequalities pass. However, all cells are occupied and the graph has one edge and two vertices, so `edges >= cells` is false. The algorithm prints `NO`. The missing cycle cannot be replaced by stacking because the top pancake would have to leave the second cell before the bottom pancake could move.

The second edge case is the original `1 x 3` example:

```
1 3
P.P
```

The usable cells have colors black, white, black. There are two black pancakes but only one white cell. The first capacity check fails immediately, giving `NO`. No amount of temporary stacking can solve a shortage of possible final cells.

The third edge case is a single pancake:

```
1 2
P.
```

There is one black pancake and one white cell. The first capacity inequality is (1 \le 1), the second is trivial, and there is an empty cell because two usable cells contain only one pancake. The algorithm prints `YES`, corresponding to moving the pancake once to its neighboring cell.

The fourth edge case is a fully occupied path with four cells:

```
1 4
PPPP
```

The two colors each contain two cells and two pancakes, so the parity counts are balanced. However, the graph has four vertices and only three edges, making it a tree. Since there is no empty cell and no cycle, the algorithm prints `NO`. This is the larger version of the two-cell obstruction.

The fifth edge case is the fully occupied (2 \times 2) board:

```
2 2
PP
PP
```

There are two cells and pancakes of each color, and the four usable cells contain four edges around a cycle. The algorithm reaches the full-occupancy branch and finds `edges >= cells`, so it prints `YES`. The cycle allows the occupied configuration to rotate and gives the required odd move count.
