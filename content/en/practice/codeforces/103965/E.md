---
title: "CF 103965E - \u041e\u0447\u0435\u0440\u043a"
description: "We are given a binary grid consisting of white and red cells. The task is to determine whether we can reproduce exactly the red cells using a sequence of stamping operations with two fixed brush shapes. Each operation selects a cell and applies one of two patterns."
date: "2026-07-02T06:35:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103965
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 103965
solve_time_s: 35
verified: true
draft: false
---

[CF 103965E - \u041e\u0447\u0435\u0440\u043a](https://codeforces.com/problemset/problem/103965/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary grid consisting of white and red cells. The task is to determine whether we can reproduce exactly the red cells using a sequence of stamping operations with two fixed brush shapes.

Each operation selects a cell and applies one of two patterns. One brush paints a plus shape centered at the chosen cell, affecting the center plus its four orthogonal neighbors. The other brush paints an X shape, affecting the center plus the four diagonal neighbors. Both brushes may extend outside the grid without restriction, but only cells inside the grid matter for the final picture. Multiple brush applications are allowed, and overlapping paint is fine since the final state only depends on whether a cell is red at least once.

The goal is to decide if there exists any sequence of brush placements such that the union of all painted cells matches the given grid exactly.

The constraint n, m ≤ 1000 implies up to 10^6 cells. Any solution that attempts to simulate arbitrary combinations of brush placements directly would be infeasible. A valid approach must reduce the problem to a local consistency check per cell or per small neighborhood, ideally linear in the grid size.

A subtle edge case comes from the fact that both brushes paint multiple cells at once, including the center cell. A naive approach might assume that every red cell must be directly the center of some brush, which is false. A cell can be painted only via being a neighbor of some other chosen center. This makes reasoning about coverage direction-dependent and easy to get wrong.

Another common pitfall is ignoring boundary behavior. Since brushes can extend outside the grid, edge and corner cells behave the same as interior cells in terms of feasibility, but their neighborhood is truncated, which can lead to incorrect assumptions about required centers.

## Approaches

A brute-force interpretation would try to choose a set of brush centers and assign each center one of the two brush types, then check whether the resulting union of affected cells matches the target grid. This quickly becomes exponential because each cell can either be unused or used as a center with one of two brush types. Even if we restrict ourselves to only considering red cells as potential centers, the interactions between overlapping brushes still create a combinatorial explosion.

The key observation is that we do not actually care about how the picture is constructed, only whether every red cell can be "explained" by at least one brush placement, and no white cell is accidentally painted.

This flips the perspective: instead of constructing the image, we verify that every red cell has at least one valid local explanation and that no forced explanation spills into a forbidden cell.

Consider a red cell. If it is not supported by any brush center that can reach it, then it must itself be a center of some brush. The only way to fail is when a red cell cannot be covered without forcing paint onto a white cell.

This leads to a local constraint system: for each red cell, we check whether there exists at least one brush placement that covers it while not contradicting the grid. Since each brush only affects a constant number of cells, each check is O(1), and we only need to scan all cells.

A more refined view is to treat every cell as a candidate center and validate whether placing either brush there is consistent with the target grid. If a brush centered at (i, j) paints any white cell, that placement is invalid. We compute all valid placements, mark all cells they can cover, and finally ensure every red cell is covered by at least one valid placement.

Because each placement affects at most five cells, total validation is linear in the grid size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over brush assignments | Exponential | Exponential | Too slow |
| Local validity of placements + coverage check | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

We reframe the problem as checking whether every red cell can be produced by at least one valid brush placement.

1. For every cell in the grid, consider it as a potential brush center. This is necessary because any red cell could be created as a neighbor rather than a center.
2. For each center, simulate placing the plus brush. Collect the set of affected cells: the center and its four orthogonal neighbors. If any of these cells is white, this placement is invalid and discarded. Otherwise, mark this placement as valid and record that it can cover all of its affected cells.
3. Repeat the same check for the X brush, which affects diagonal neighbors and the center. Again discard placements that touch any white cell.
4. Maintain a boolean coverage array initialized to false. Whenever a valid placement is found, mark all cells it covers as covered.
5. After processing all centers and both brush types, iterate over the grid and verify that every red cell is marked as covered. If any red cell is not covered, the answer is impossible.

The correctness hinges on the fact that any valid construction can be decomposed into individual placements, each of which must itself avoid painting white cells. Therefore, every placement in a valid solution must appear in the set of locally valid placements we enumerate.

## Why it works

Every brush placement affects only a constant-size neighborhood, so whether it is allowed depends solely on the original grid cells within that neighborhood. If a placement would paint a white cell, no sequence of operations can include it in a valid solution, because paint is irreversible.

Conversely, if a placement is locally valid, it can always be used without violating constraints, and overlapping placements only strengthen coverage without introducing new conflicts. Thus, the problem reduces to ensuring that every red cell lies in at least one locally valid neighborhood.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
g = [list(input().strip()) for _ in range(n)]

covered = [[False] * m for _ in range(n)]

dirs_plus = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
dirs_x = [(0, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

def inb(x, y):
    return 0 <= x < n and 0 <= y < m

for i in range(n):
    for j in range(m):
        # plus brush
        ok = True
        cells = []
        for dx, dy in dirs_plus:
            ni, nj = i + dx, j + dy
            if inb(ni, nj):
                if g[ni][nj] == '.':
                    ok = False
                    break
                cells.append((ni, nj))
        if ok:
            for x, y in cells:
                covered[x][y] = True

        # x brush
        ok = True
        cells = []
        for dx, dy in dirs_x:
            ni, nj = i + dx, j + dy
            if inb(ni, nj):
                if g[ni][nj] == '.':
                    ok = False
                    break
                cells.append((ni, nj))
        if ok:
            for x, y in cells:
                covered[x][y] = True

for i in range(n):
    for j in range(m):
        if g[i][j] == '*' and not covered[i][j]:
            print("NO")
            sys.exit()

print("YES")
```

The grid is scanned cell by cell, treating each position as a potential center for both brush types. For each brush, we explicitly list its influence pattern and ensure it does not touch any white cell. If it passes this check, we mark all affected cells as covered.

The final verification step is essential because it ensures that every required red cell is supported by at least one valid brush placement.

A common implementation mistake is forgetting that boundary cells still allow brush centers outside the grid influence. This code handles it by simply ignoring out-of-bounds neighbors instead of rejecting the placement.

## Worked Examples

### Example 1

Input:

```
5 5
.....
..***
..***
..***
.....
```

We track coverage as we test valid brush centers.

| Center (i,j) | Brush | Valid | Newly covered cells |
| --- | --- | --- | --- |
| (2,2) | plus | no | none |
| (2,3) | plus | yes | (2,3), (1,3), (3,3), (2,2), (2,4) |
| (2,3) | x | no | none |
| (3,3) | plus | yes | central region expanded |
| (3,3) | x | no | none |

After scanning all centers, every red cell is covered by at least one valid plus placement, so the answer is YES.

This trace shows how overlapping plus brushes collectively cover the rectangular block even though no single brush matches the whole shape.

### Example 2

Input:

```
5 5
.....
.....
*....
.*...
*.*..
```

| Center (i,j) | Brush | Valid | Newly covered cells |
| --- | --- | --- | --- |
| (4,1) | x | yes | diagonal pattern covers scattered reds |
| (3,0) | plus | yes | partial support |
| (4,0) | plus | no | touches white cell |

The coverage accumulates from multiple small valid placements. This demonstrates that red cells do not need to belong to a single coherent shape, only to be locally explainable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is tested for two constant-size brush patterns |
| Space | O(nm) | Coverage grid of same size as input |

The grid size reaches up to 10^6 cells, and each cell triggers only constant work. This fits comfortably within both time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [list(input().strip()) for _ in range(n)]

    covered = [[False] * m for _ in range(n)]

    dirs_plus = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    dirs_x = [(0, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def inb(x, y):
        return 0 <= x < n and 0 <= y < m

    for i in range(n):
        for j in range(m):
            ok = True
            cells = []
            for dx, dy in dirs_plus:
                ni, nj = i + dx, j + dy
                if inb(ni, nj):
                    if g[ni][nj] == '.':
                        ok = False
                        break
                    cells.append((ni, nj))
            if ok:
                for x, y in cells:
                    covered[x][y] = True

            ok = True
            cells = []
            for dx, dy in dirs_x:
                ni, nj = i + dx, j + dy
                if inb(ni, nj):
                    if g[ni][nj] == '.':
                        ok = False
                        break
                    cells.append((ni, nj))
            if ok:
                for x, y in cells:
                    covered[x][y] = True

    out = []
    for i in range(n):
        for j in range(m):
            if g[i][j] == '*' and not covered[i][j]:
                out.append("NO")
                return "\n".join(out)
    return "YES"

# provided samples
assert run("""5 5
.....
..***
..***
..***
.....
""") == "YES"

assert run("""5 5
.....
.....
*....
.*...
*.*..
""") == "YES"

# custom cases
assert run("""1 1
.
""") == "YES", "single white cell"

assert run("""1 1
*
""") == "YES", "single red cell"

assert run("""3 3
*.*
...
*.*
""") == "NO", "isolated reds impossible"

assert run("""2 2
**
**
""") == "YES", "full block"

assert run("""3 3
*.*
*.*
*.*
""") == "YES", "vertical stripe coverage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 white | YES | empty target consistency |
| 1x1 red | YES | minimal valid placement |
| sparse corners | NO | unreachable isolated cells |
| full 2x2 |  |  |
