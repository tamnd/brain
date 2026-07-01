---
title: "CF 104262D - Celestial Sky"
description: "We are working on a 2D grid where both stars and black holes are placed at integer coordinates in a small bounded space. Stars represent points we want to count, while black holes invalidate nearby stars."
date: "2026-07-01T21:35:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104262
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 03-24-23 Div. 1 (Advanced)"
rating: 0
weight: 104262
solve_time_s: 75
verified: true
draft: false
---

[CF 104262D - Celestial Sky](https://codeforces.com/problemset/problem/104262/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a 2D grid where both stars and black holes are placed at integer coordinates in a small bounded space. Stars represent points we want to count, while black holes invalidate nearby stars.

Each black hole removes all stars inside a 3×3 square centered at its position, meaning every cell within one unit in both x and y directions from the black hole becomes unsafe. After this removal process, we are asked to answer multiple rectangle queries, each asking how many remaining stars lie inside that rectangle.

The key difficulty is that stars can overlap, black hole effects can overlap, and we must answer up to 100000 queries efficiently after applying all removals.

The coordinate range is small, from 0 to 999 in both dimensions. This immediately suggests that while the number of objects is large, the geometry is dense but bounded, which often points toward grid preprocessing or prefix sums rather than dynamic structures.

A naive approach would check every star for every query and also test whether it is destroyed by any black hole. That would be too slow because with 100000 stars and 100000 queries, we could reach 10^10 operations.

A subtle edge case is overlapping black holes. For example, if one black hole is at (5,5) and another at (6,6), their 3×3 destruction zones overlap heavily. A naive implementation might incorrectly subtract multiple times or fail to mark all affected stars if it only checks direct proximity without aggregating coverage first.

Another edge case is overlapping stars. If multiple stars share the same coordinate, all of them are counted individually unless destroyed. Any grid-based solution must accumulate counts rather than treat coordinates as sets.

Finally, black hole destruction must be applied before answering queries. If one mistakenly processes queries first or lazily evaluates destruction per query, results will be inconsistent.

## Approaches

The brute-force idea is straightforward. For each star, we scan through all black holes to determine whether it lies inside at least one 3×3 destruction region. If it is not destroyed, we keep it. Then for each query, we scan all remaining stars and count those inside the query rectangle.

This is correct because it directly follows the definition of destruction and counting. However, the complexity becomes prohibitive. Checking destruction alone costs O(NM), which at 10^5 each is 10^10 operations. Even if optimized slightly, this is far beyond limits. Adding query evaluation multiplies the cost further.

The key observation comes from the coordinate constraint. Since all coordinates lie in a 1000×1000 grid, we can precompute everything on a fixed-size array. Instead of tracking stars individually, we aggregate them into a frequency grid. Instead of simulating destruction per star, we mark a second grid of “blocked” cells and propagate black hole influence locally. Once both are encoded on the grid, we can compute a final valid-star grid and build a 2D prefix sum to answer queries in O(1).

This transforms the problem from event processing into static grid preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM + QN) | O(N) | Too slow |
| Grid + Prefix Sums | O(N + M + 1000² + Q) | O(1000²) | Accepted |

## Algorithm Walkthrough

We compress all information into a fixed 1000×1000 grid so that operations become constant-time per cell.

1. Build a 2D array `stars[x][y]` counting how many stars exist at each coordinate. This is necessary because multiple stars can occupy the same position, and we must preserve multiplicity.
2. Build a second 2D array `bad[x][y]` initialized to zero. This will mark all cells affected by at least one black hole.
3. For each black hole at (x, y), mark all cells in the square from (x−1, y−1) to (x+1, y+1) as bad, taking care to clamp boundaries to the grid limits. This expands the black hole effect explicitly so we avoid per-star checking later. The reason we expand immediately is to convert a geometric condition into a precomputed boolean grid.
4. Build a final grid `valid[x][y]` such that it equals `stars[x][y]` if the cell is not bad, otherwise zero. This step collapses destruction into a simple filter.
5. Construct a 2D prefix sum over `valid`. Each prefix cell stores cumulative sum of valid stars in the rectangle from (0,0) to (x,y). This enables constant-time rectangle queries.
6. For each query rectangle (x1, y1, x2, y2), normalize coordinates so x1 ≤ x2 and y1 ≤ y2, then compute the sum using inclusion-exclusion on the prefix grid.

### Why it works

The correctness comes from separating concerns. Black hole effects depend only on local neighborhoods, so they can be fully resolved before any query is considered. Once we convert destruction into a static mask over the grid, the remaining problem is purely a 2D range sum query over a fixed matrix. The prefix sum invariant guarantees that every cell contribution is counted exactly once in any queried rectangle, and no destroyed cell contributes because it is explicitly zeroed before prefix construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX = 1000

def main():
    N, M, Q = map(int, input().split())

    stars = [[0] * MAX for _ in range(MAX)]
    bad = [[0] * MAX for _ in range(MAX)]

    for _ in range(N):
        x, y = map(int, input().split())
        stars[x][y] += 1

    for _ in range(M):
        x, y = map(int, input().split())
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < MAX and 0 <= ny < MAX:
                    bad[nx][ny] = 1

    valid = [[0] * MAX for _ in range(MAX)]
    for i in range(MAX):
        for j in range(MAX):
            if not bad[i][j]:
                valid[i][j] = stars[i][j]

    pref = [[0] * (MAX + 1) for _ in range(MAX + 1)]

    for i in range(1, MAX + 1):
        for j in range(1, MAX + 1):
            pref[i][j] = (
                valid[i - 1][j - 1]
                + pref[i - 1][j]
                + pref[i][j - 1]
                - pref[i - 1][j - 1]
            )

    def query(x1, y1, x2, y2):
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        x1 += 1
        y1 += 1
        x2 += 1
        y2 += 1
        return (
            pref[x2][y2]
            - pref[x1 - 1][y2]
            - pref[x2][y1 - 1]
            + pref[x1 - 1][y1 - 1]
        )

    out = []
    for _ in range(Q):
        x1, y1, x2, y2 = map(int, input().split())
        out.append(str(query(x1, y1, x2, y2)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation begins by compressing stars into a frequency grid so that duplicates are naturally handled. The black hole step explicitly paints a 3×3 neighborhood, which avoids repeated geometric checks later. The prefix sum array is built with one-indexing to simplify boundary handling, which is why all query coordinates are shifted by one. The inclusion-exclusion formula is the standard 2D range sum identity and is the only reason queries become O(1).

A common mistake here is forgetting that coordinates are inclusive and small. Another is failing to clamp black hole influence, which would lead to index errors. One more subtle issue is forgetting to accumulate stars instead of overwriting them.

## Worked Examples

Using the sample input:

We first build the star grid and mark all affected cells.

| Step | Action | Key State (conceptual) |
| --- | --- | --- |
| 1 | Insert stars | multiple coordinates populated |
| 2 | Apply black holes | 3×3 regions around (2,4) and (6,8) marked bad |
| 3 | Filter stars | only stars outside affected zones remain |
| 4 | Prefix build | cumulative sums prepared |
| 5 | Queries | rectangles evaluated via prefix |

For the first query `2 6 3 8`, only one surviving star lies inside the rectangle, so result is 1.

For the second query `4 2 9 5`, four valid stars remain in that region after filtering.

For the full grid query `2 2 9 9`, all surviving stars are counted, giving 8.

These traces show that destruction is applied globally before querying, not per query.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1000² + N + M + Q) | grid construction, marking, prefix sums, and O(1) queries |
| Space | O(1000²) | fixed-size grids for stars, bad cells, and prefix sums |

The 1000×1000 bound ensures that the quadratic preprocessing is small enough to run comfortably within limits, even in Python. All heavy computation is independent of N, M, and Q after preprocessing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    MAX = 1000

    N, M, Q = map(int, sys.stdin.readline().split())

    stars = [[0] * MAX for _ in range(MAX)]
    bad = [[0] * MAX for _ in range(MAX)]

    for _ in range(N):
        x, y = map(int, sys.stdin.readline().split())
        stars[x][y] += 1

    for _ in range(M):
        x, y = map(int, sys.stdin.readline().split())
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < MAX and 0 <= ny < MAX:
                    bad[nx][ny] = 1

    valid = [[0] * MAX for _ in range(MAX)]
    for i in range(MAX):
        for j in range(MAX):
            if not bad[i][j]:
                valid[i][j] = stars[i][j]

    pref = [[0] * (MAX + 1) for _ in range(MAX + 1)]
    for i in range(1, MAX + 1):
        for j in range(1, MAX + 1):
            pref[i][j] = valid[i-1][j-1] + pref[i-1][j] + pref[i][j-1] - pref[i-1][j-1]

    def query(x1,y1,x2,y2):
        x1,x2=min(x1,x2),max(x1,x2)
        y1,y2=min(y1,y2),max(y1,y2)
        x1+=1;y1+=1;x2+=1;y2+=1
        return pref[x2][y2]-pref[x1-1][y2]-pref[x2][y1-1]+pref[x1-1][y1-1]

    out=[]
    for _ in range(Q):
        x1,y1,x2,y2=map(int, sys.stdin.readline().split())
        out.append(str(query(x1,y1,x2,y2)))

    return "\n".join(out)

# provided sample
assert run("""12 2 3
1 4
2 5
2 6
4 8
5 3
5 6
5 9
6 2
6 7
7 3
8 3
8 9
2 4
6 8
2 6 3 8
4 2 9 5
2 2 9 9
""") == "1\n4\n8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single star, no black holes | 1 | basic counting |
| Star inside black hole zone | 0 | destruction masking |
| Multiple overlapping black holes | correct filtering | overlap handling |
| Full grid query | total survivors | prefix correctness |

## Edge Cases

A critical edge case is overlapping black holes. If one is at (5,5) and another at (6,6), the algorithm marks all cells in both 3×3 neighborhoods. The second marking does not undo or double count anything because `bad[x][y]` is boolean. This ensures the final mask is stable regardless of overlap order.

Another edge case is stars located exactly on the boundary of a black hole’s 3×3 region. For a black hole at (2,2), a star at (1,3) is still removed because it lies within one unit in both axes. The explicit loop over dx and dy guarantees inclusion of all boundary cells.

Finally, queries that cover the full grid test whether prefix sums correctly accumulate all valid stars. The inclusion-exclusion structure ensures no overcounting even when many stars share coordinates.
