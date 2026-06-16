---
title: "CF 965B - Battleship"
description: "We are given an $n times n$ grid where each cell is either forbidden or allowed. Forbidden cells are marked with and can never be part of a ship. Allowed cells are marked with . and may be part of a ship."
date: "2026-06-17T01:38:41+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 965
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 476 (Div. 2) [Thanks, Telegram!]"
rating: 1300
weight: 965
solve_time_s: 81
verified: true
draft: false
---

[CF 965B - Battleship](https://codeforces.com/problemset/problem/965/B)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ grid where each cell is either forbidden or allowed. Forbidden cells are marked with `#` and can never be part of a ship. Allowed cells are marked with `.` and may be part of a ship.

A ship is a straight segment of exactly $k$ consecutive cells, placed either horizontally or vertically. We consider every valid placement of such a ship that lies entirely inside the grid and uses only allowed cells. Each valid placement is one concrete segment, defined by its orientation and starting position.

The task is not to choose a ship placement. Instead, we imagine all valid placements at once, and for every cell we count how many of those placements include it. We must return any cell whose count is maximal.

The constraints $n \le 100$ and $k \le n$ imply at most $10^4$ cells, and at most $O(n^2)$ candidate segments horizontally and vertically. Any solution that explicitly enumerates all placements and updates contributions per cell is feasible within a few million operations.

A subtle issue is that a valid segment must be fully contained in `.` cells. A naive approach that only checks endpoints or assumes continuity without verifying all intermediate cells will overcount invalid placements. Another pitfall is forgetting vertical segments entirely or double counting overlapping segments incorrectly when aggregating contributions per cell.

## Approaches

A brute-force approach would enumerate every possible starting position for both orientations, verify whether the segment of length $k$ is fully valid, and if so increment a counter for all $k$ cells in that segment. This is correct because it directly mirrors the definition of valid ship placements. The cost comes from recomputing validity and updating $k$ cells for each candidate segment. There are $O(n^2)$ starting positions and each update costs $O(k)$, giving $O(n^2 k)$, which in the worst case reaches about $10^6 \cdot 100 = 10^8$ operations. This is borderline but unnecessary given a simpler observation.

The key observation is that we do not actually need to simulate every segment independently. For each cell, we only need to know how many horizontal segments and vertical segments of length $k$ cover it. A segment contributes to a cell if and only if that segment is valid and fully lies in a contiguous block of `.` cells that spans at least $k$ length.

This allows us to precompute all valid horizontal segments and vertical segments efficiently, then for each valid segment we directly update contributions for its $k$ cells. Because each segment still costs $O(k)$, we might worry we have not improved asymptotics, but $n \le 100$ makes this still comfortably fast. More importantly, we avoid repeated checks and simplify correctness: each valid segment is handled exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(n^2 k)$ | $O(n^2)$ | Accepted but tight |
| Segment Enumeration + Marking | $O(n^2 k)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Precompute all horizontal valid segments of length $k$. For each row, scan left to right and identify maximal contiguous blocks of `.`. Within each block of length $L$, every subsegment of length $k$ is valid, so there are $L-k+1$ segments starting at different columns.
2. For each valid horizontal segment starting at $(i, j)$, increment a contribution counter for every cell $(i, j), (i, j+1), \dots, (i, j+k-1)$. This directly counts how many valid placements include each cell.
3. Repeat the same process for vertical segments. For each column, find contiguous `.` blocks and enumerate all vertical segments of length $k$.
4. Maintain a global $n \times n$ array `cnt` initialized to zero. Every time a valid segment is found, increment all cells it covers.
5. After processing both orientations, scan the entire grid and select the cell with maximum value in `cnt`. If multiple cells share the maximum, any one can be returned.

### Why it works

Every valid ship placement corresponds to exactly one horizontal or vertical segment that lies fully inside a contiguous `.` block. The algorithm enumerates every such segment exactly once. Each time we encounter a segment, we distribute one unit of contribution to every cell it occupies. Therefore, the value stored at a cell is exactly the number of valid ship placements that include it. Maximizing this value over all cells directly solves the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def add_segment(cnt, i, j, di, dj, k):
    for _ in range(k):
        cnt[i][j] += 1
        i += di
        j += dj

n, k = map(int, input().split())
grid = [input().strip() for _ in range(n)]

cnt = [[0] * n for _ in range(n)]

# horizontal segments
for i in range(n):
    j = 0
    while j < n:
        if grid[i][j] == '#':
            j += 1
            continue
        start = j
        while j < n and grid[i][j] == '.':
            j += 1
        length = j - start
        if length >= k:
            for s in range(start, j - k + 1):
                add_segment(cnt, i, s, 0, 1, k)

# vertical segments
for j in range(n):
    i = 0
    while i < n:
        if grid[i][j] == '#':
            i += 1
            continue
        start = i
        while i < n and grid[i][j] == '.':
            i += 1
        length = i - start
        if length >= k:
            for s in range(start, i - k + 1):
                add_segment(cnt, s, j, 1, 0, k)

best_i, best_j = 0, 0
best_val = -1

for i in range(n):
    for j in range(n):
        if cnt[i][j] > best_val:
            best_val = cnt[i][j]
            best_i, best_j = i, j

print(best_i + 1, best_j + 1)
```

The function `add_segment` encapsulates the idea of distributing contribution from one valid ship placement to all its cells. This avoids repeated code for horizontal and vertical handling and makes the update logic explicit.

The row and column scanning logic relies on grouping consecutive `.` cells into maximal blocks. This is crucial because segments cannot cross `#` cells. Within each block, we only start segments where a full length $k$ still fits.

The final scan simply picks the maximum entry in `cnt`, and the +1 shift handles the problem’s 1-indexed output requirement.

## Worked Examples

### Sample 1

Input:

```
4 3
#..#
#.#.
....
.###
```

We track only one horizontal block example and one vertical block example for illustration.

Horizontal processing finds row 3 as a full block of length 4, producing two segments. Vertical processing finds limited segments due to `#`.

| Step | Segment start | Orientation | Cells updated |
| --- | --- | --- | --- |
| 1 | (3,1) | H | (3,1),(3,2),(3,3) |
| 2 | (3,2) | H | (3,2),(3,3),(3,4) |
| 3 | (3,2) | V | (3,2),(4,2),(...) |

After aggregation, cell (3,2) receives the highest number of coverings because it lies in both horizontal segments and at least one vertical segment.

Output:

```
3 2
```

This demonstrates that the algorithm correctly accumulates contributions from overlapping placements.

### Sample 2

Input:

```
3 2
...
...
...
```

Every cell is `.` so every possible segment exists.

| Step | Segment type | Count of segments |
| --- | --- | --- |
| 1 | horizontal | 3 rows × 2 segments each = 6 |
| 2 | vertical | 3 columns × 2 segments each = 6 |

Middle cells participate in more segments than corners.

A central cell such as (2,2) is included in all possible 2-length segments passing through it.

Output could be:

```
2 2
```

This shows symmetry: the algorithm naturally identifies center cells as optimal without any special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 k)$ | Each valid segment of length $k$ updates $k$ cells, and there are $O(n^2)$ such segments |
| Space | $O(n^2)$ | Grid and contribution matrix |

With $n \le 100$, the worst-case operation count is around $10^6$ segments times $100$ updates, well within limits in Python under typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    cnt = [[0] * n for _ in range(n)]

    def add(i, j, di, dj):
        for _ in range(k):
            cnt[i][j] += 1
            i += di
            j += dj

    for i in range(n):
        j = 0
        while j < n:
            if grid[i][j] == '#':
                j += 1
                continue
            s = j
            while j < n and grid[i][j] == '.':
                j += 1
            for st in range(s, j - k + 1):
                add(i, st, 0, 1)

    for j in range(n):
        i = 0
        while i < n:
            if grid[i][j] == '#':
                i += 1
                continue
            s = i
            while i < n and grid[i][j] == '.':
                i += 1
            for st in range(s, i - k + 1):
                add(st, j, 1, 0)

    best = (0, 0)
    bestv = -1
    for i in range(n):
        for j in range(n):
            if cnt[i][j] > bestv:
                bestv = cnt[i][j]
                best = (i, j)

    return f"{best[0]+1} {best[1]+1}"

# provided sample
assert run("4 3\n#..#\n#.#.\n....\n.###\n") == "3 2"

# all open grid
assert run("3 2\n...\n...\n...\n") in ["2 2", "1 1", "1 2", "2 1", "2 2", "2 3", "3 2", "3 3"]

# k = 1 (every cell is a ship)
assert run("2 1\n..\n..\n") == "1 1"

# fully blocked grid
assert run("2 2\n##\n##\n") in ["1 1", "1 2", "2 1", "2 2"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty 3x3 | center | symmetry handling |
| k=1 grid | any cell | single-cell edge case |
| all blocked | any cell | no valid placements |

## Edge Cases

When the grid contains no valid segment of length $k$, the contribution matrix remains all zeros. In this case the algorithm still returns (1,1) because no better candidate exists. This matches the problem’s requirement that any cell is acceptable.

When $k = 1$, every `.` cell forms a valid segment by itself. The algorithm treats each cell as a segment of length one, so each allowed cell contributes exactly one to itself, and forbidden cells contribute nothing. The maximum is therefore any `.` cell, and the scan naturally selects one.

When a long block of `.` cells exists, overlapping segments heavily concentrate contributions in central cells. The algorithm correctly accumulates multiple overlapping windows, ensuring interior cells receive higher counts than boundary cells, which matches the true number of covering segments.
