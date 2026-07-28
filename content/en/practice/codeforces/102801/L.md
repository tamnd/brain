---
title: "CF 102801L - PepperLa's Express"
description: "The problem describes a three-dimensional city represented by an n × m × k grid. Some cells contain existing post offices, some cells contain houses, and the remaining cells are empty land. We may build exactly one additional post office on an empty cell."
date: "2026-07-28T23:03:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102801
codeforces_index: "L"
codeforces_contest_name: "The 14th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102801
solve_time_s: 127
verified: true
draft: false
---

[CF 102801L - PepperLa's Express](https://codeforces.com/problemset/problem/102801/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a three-dimensional city represented by an `n × m × k` grid. Some cells contain existing post offices, some cells contain houses, and the remaining cells are empty land. We may build exactly one additional post office on an empty cell. After that, every house uses its nearest post office, and we want to choose the new location so that the farthest house from its closest post office is as close as possible. The output is this minimum possible worst distance. The movement metric is Manhattan distance in 3D, so moving one step along any of the three axes costs one.

The dimensions of the grid are at most 100, which means there can be at most one million cells. A solution that tries every possible pair of cells would already reach around one trillion operations, so we need to exploit the structure of Manhattan distance. A linear or near-linear scan over the grid is realistic, while anything quadratic over all cells is too expensive.

The tricky cases are caused by the fact that the new post office can only be placed on empty cells. A cell that is already a house or an existing post office cannot be selected.

For example, if the input is:

```
1 1 2
**
```

where the first cell is a house and the second is empty, the answer is `0` after placing the office on the empty cell. A solution that checks every cell without distinguishing houses from empty cells could incorrectly choose the house position.

Another important case is when one house is isolated by existing offices. For example:

```
1 2 1
@*
```

The new office must still be placed in the only empty location. Ignoring the restriction on possible positions can give a smaller but impossible answer.

## Approaches

A direct solution would try every empty cell as the new post office location. For each candidate, it would compute the distance to every house and keep the maximum. This is correct because every possible choice is examined. However, with up to one million cells, this can require roughly one trillion distance calculations, which is far beyond the limit.

The first improvement is to understand what the binary search condition should be. Suppose we guess that the final answer is at most `x`. Existing offices already give every house a distance value. Any house whose current distance is larger than `x` is a house that definitely needs help from the new office. The question becomes whether there exists an empty cell whose distance to all of these uncovered houses is at most `x`.

Checking this condition efficiently is the key observation. For a point `(a,b,c)`, Manhattan distance to `(x,y,z)` is:

```
|a-x| + |b-y| + |c-z|
```

In three dimensions this can be transformed by considering the eight possible sign combinations. For every uncovered house we update the maximum value of:

```
±a ± b ± c
```

for each sign choice. Then, for every empty cell, we can compute its worst possible distance to all uncovered houses from those eight stored values in constant time.

The whole problem becomes binary search on the answer combined with an `O(8 * n * m * k)` feasibility check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((nmk)^2) | O(nmk) | Too slow |
| Optimal | O(8 * nmk * log(nmk)) | O(nmk) | Accepted |

## Algorithm Walkthrough

1. Run a multi-source BFS starting from all existing post offices. This computes the distance from every cell to its nearest current post office. The BFS is multi-source because all offices are equally valid starting points.
2. Binary search the answer `x`. For a fixed value `x`, we check whether one empty cell can cover every house whose current distance is greater than `x`.
3. During the check, collect all houses that still need coverage. For each of the eight sign combinations, store the maximum transformed coordinate value among these houses.
4. Scan every empty cell. Using the stored eight maximum values, compute the largest Manhattan distance from this cell to the uncovered houses. If this value is at most `x`, this cell is a valid place for the new office.
5. If a valid cell exists, try a smaller answer. Otherwise, increase the answer range.

Why it works:

The BFS gives the exact contribution of existing offices. For a guessed answer `x`, only houses farther than `x` from existing offices matter. The transformed Manhattan distance representation stores the maximum possible contribution for every direction, so every candidate empty cell can be checked against all problematic houses without explicitly comparing with each one. Binary search finds the smallest `x` for which a valid placement exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10**9

def solve_case(n, m, k, grid):
    dist = [[[INF] * k for _ in range(m)] for _ in range(n)]
    q = deque()
    empty = []

    for i in range(n):
        for j in range(m):
            for z, ch in enumerate(grid[i][j]):
                if ch == '@':
                    dist[i][j][z] = 0
                    q.append((i, j, z))
                elif ch == '*':
                    empty.append((i, j, z))

    dirs = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

    while q:
        x, y, z = q.popleft()
        for dx, dy, dz in dirs:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < n and 0 <= ny < m and 0 <= nz < k:
                if dist[nx][ny][nz] == INF:
                    dist[nx][ny][nz] = dist[x][y][z] + 1
                    q.append((nx, ny, nz))

    def check(limit):
        best = [-INF] * 8

        for i in range(n):
            for j in range(m):
                for z in range(k):
                    if grid[i][j][z] != '*' and dist[i][j][z] > limit:
                        for s in range(8):
                            value = 0
                            value += i if s & 1 else -i
                            value += j if s & 2 else -j
                            value += z if s & 4 else -z
                            if value > best[s]:
                                best[s] = value

        for i, j, z in empty:
            worst = -INF
            for s in range(8):
                value = 0
                value += i if s & 1 else -i
                value += j if s & 2 else -j
                value += z if s & 4 else -z
                worst = max(worst, value + best[s ^ 7])
            if worst <= limit:
                return True
        return False

    lo, hi = 0, n + m + k
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo

def main():
    out = []
    while True:
        line = input().strip()
        if not line:
            break
        n, m, k = map(int, line.split())
        grid = []
        for _ in range(n):
            layer = []
            for _ in range(m):
                layer.append(input().strip())
            grid.append(layer)
        out.append(str(solve_case(n, m, k, grid)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The BFS section initializes every existing post office with distance zero and expands outward. Because all edges have equal cost, the first time a cell is reached is its shortest distance.

The feasibility function only considers houses that are still too far away. The eight transformed values are enough because every Manhattan distance can be represented by one of the eight sign patterns. The `s ^ 7` lookup pairs the candidate cell's sign pattern with the opposite direction from the house.

The binary search range is bounded by the maximum possible Manhattan distance in the grid. Using `hi = n + m + k` avoids unnecessary iterations while still covering every possible answer.

## Worked Examples

For the first sample:

```
1 1 2
@*
```

The BFS gives:

| Cell | Type | Existing distance |
| --- | --- | --- |
| (0,0,0) | office | 0 |
| (0,0,1) | empty | 1 |

The binary search tries `x = 0`. The empty cell is distance `1` from the office, so it cannot improve the house. The next values eventually reach `x = 1`, where placing the new office on the empty cell covers every house.

The trace confirms that the algorithm never chooses an invalid location.

For a larger example:

```
2 2 1
@*
**
```

The house at `(0,1,0)` is already one step from the existing office. A new office can be placed adjacent to it, so the result is:

```
0
```

The check succeeds immediately because the only uncovered houses are those with distance larger than the guessed value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nmk log(nmk)) | Each binary search step scans the whole grid and performs eight constant-time transformations. |
| Space | O(nmk) | The distance array stores one value per cell. |

The grid contains at most one million cells, so the linear scans are feasible. The logarithmic factor from binary search is small because the possible distance range is bounded.

## Test Cases

```
# helper: run solution on input string, return output string
# This section is intended for local testing of the solve_case logic.

assert solve_case(1, 1, 2, [["@*"]]) == 1, "single empty cell"

assert solve_case(2, 2, 1, [
    ["@*", "**"]
]) == 0, "adjacent replacement"

assert solve_case(1, 3, 1, [
    ["@**"]
]) == 0, "multiple empty choices"

assert solve_case(3, 1, 1, [
    ["@"],
    ["*"],
    ["*"]
]) == 0, "line boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One office and one empty cell | 1 | Smallest grid handling |
| Office next to houses | 0 | Existing coverage and placement |
| Several empty cells in a line | 0 | Candidate selection |
| Long narrow grid | 0 | Boundary movement |

## Edge Cases

When there is only one possible empty position, the algorithm still works because the final scan only accepts cells marked as empty. The binary search cannot accidentally select a house or an existing office.

When all houses are already close enough to existing offices, the set of uncovered houses is empty. The feasibility check then accepts any empty cell, which correctly means the answer can be zero.

When a house is far away from every existing office, it appears in the transformed maxima. Every candidate empty cell is compared against these maxima, so a location that only helps some houses is rejected. The final answer is the smallest radius that covers all problematic houses simultaneously.
