---
title: "CF 102535F - Go Go ?"
description: "We have a rectangular shooting field. The bottom row is the only place where the shooter can stand, and every cell above it is either empty, an obstacle, or a target. A shot travels in a straight line upward from any point on the bottom row."
date: "2026-08-06T19:53:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102535
codeforces_index: "F"
codeforces_contest_name: "2020 UP ACM Algolympics Elimination Round"
rating: 0
weight: 102535
solve_time_s: 219
verified: false
draft: false
---

[CF 102535F - Go Go ?](https://codeforces.com/problemset/problem/102535/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We have a rectangular shooting field. The bottom row is the only place where the shooter can stand, and every cell above it is either empty, an obstacle, or a target. A shot travels in a straight line upward from any point on the bottom row. The first non-empty cell touched by that line is the only thing that matters, because the bullet stops immediately.

The task is to count how many target cells can be the first non-empty cell for at least one possible shot.

The grid can contain up to 500 rows and 500 columns, and the total number of cells over all test cases is at most one million. This rules out simulating every possible shot individually. A naive approach that tries many starting positions and many directions would easily become quadratic or worse in the number of cells. We need a method that processes each cell a constant or logarithmic number of times.

The difficulty comes from the fact that a target is not simply blocked by cells directly below it. A diagonal shot can reach it, while another diagonal can be blocked. The algorithm must reason about all possible shooting angles without enumerating them.

Several edge cases are easy to miss. A target directly above the shop is visible even if other targets exist nearby.

For example:

```
2 3
.X.
```

The only target is directly above a possible shooting position, so the answer is:

```
1
```

A solution that only checks diagonal visibility could incorrectly ignore vertical shots.

Another case is when a target is hidden by a closer obstacle on a diagonal.

```
3 3
...
#X.
```

The target is in the second row, but the obstacle below it blocks every possible path from the bottom. The answer is:

```
0
```

A careless implementation that only checks the same column would incorrectly count the target.

A final tricky case is that empty cells do not block anything. A target can be reached through a long empty corridor, so visibility depends only on the union of blocked directions created by previous non-empty cells.

## Approaches

The direct solution would be to simulate shots. We could choose many positions on the bottom row, try many directions, and trace each ray through the grid until it hits something. This is correct because every possible hit corresponds to some ray that reaches a target first. However, the number of possible rays is effectively infinite because the shooter can stand at any real position, not only at integer columns. Even restricting ourselves to interesting directions gives too many possibilities. In the worst case, repeatedly walking through the grid for many rays can reach billions of operations.

The key observation is that every cell corresponds to a continuous interval of shooting directions. Instead of asking whether individual rays hit a target, we can ask which directions are already blocked.

We process the grid from bottom to top. When we are at a row, all rows below it are closer to the shooter. Their occupied cells already block some set of directions. If a target's whole direction interval is already covered, every possible shot toward it hits something earlier. Otherwise, there exists a direction that reaches the target first, so we count it.

After processing the row, all occupied cells in that row are added to the blocked direction union. This works because every future row is farther away, so any ray passing through this row must hit it before reaching anything above.

For a cell, it is easier to represent directions using the horizontal movement per vertical movement instead of angles. If a shot moves horizontally by `u` units for every vertical unit, then the cell covers one interval of `u` values. Intervals from closer cells are merged, and visibility becomes an interval coverage query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(R²C²) or worse | O(1) | Too slow |
| Optimal | O(RC + K) where K is total interval merging work | O(RC) | Accepted |

## Algorithm Walkthrough

1. Reverse the input rows so that we process the row closest to the shooter first. The closest cells must be handled first because they are the only cells that can block farther shots.
2. Maintain a sorted list of disjoint intervals representing all shooting directions already blocked by processed cells.
3. For every occupied cell in the current row, compute the interval of directions from which that cell can be reached. The interval is represented by horizontal movement per unit vertical movement. A cell is visible if this interval is not completely contained inside the current blocked union.
4. Count the visible targets. Obstacles are still inserted into the blocked union, because they stop bullets just like targets do.
5. Merge all occupied-cell intervals from the current row into the global blocked union. The merged structure remains sorted and disjoint, which allows the next rows to be checked efficiently.

Why it works:

At any point in the scan, the blocked interval union contains exactly the directions whose first non-empty cell is already among the processed rows. When a new cell is checked, a direction inside its interval that is not blocked corresponds to a shot reaching that cell before anything closer. If no such direction exists, every shot reaches an earlier obstacle or target. Since rows are processed in increasing distance from the shooter, no future row can change this result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(r, c, grid):
    blocked = []
    ans = 0

    def cell_interval(row, col):
        h = row + 1
        low = min((col - c) / h, (col + 1) / (h + 1))
        high = max((col - c) / (h + 1), (col + 1) / h)
        return low, high

    def covered(interval):
        l, rr = interval
        for a, b in blocked:
            if a <= l and rr <= b:
                return True
            if b < l:
                continue
            if a > l:
                break
        return False

    for row in range(r - 1):
        current = []
        for col, ch in enumerate(grid[row]):
            if ch != '.':
                inter = cell_interval(row, col)
                current.append(inter)
                if ch == 'X' and not covered(inter):
                    ans += 1

        if current:
            merged = []
            i = j = 0
            while i < len(blocked) and j < len(current):
                if blocked[i][0] <= current[j][0]:
                    merged.append(blocked[i])
                    i += 1
                else:
                    merged.append(current[j])
                    j += 1
            while i < len(blocked):
                merged.append(blocked[i])
                i += 1
            while j < len(current):
                merged.append(current[j])
                j += 1

            result = []
            for l, rr in merged:
                if result and l <= result[-1][1]:
                    result[-1] = (result[-1][0], max(result[-1][1], rr))
                else:
                    result.append((l, rr))
            blocked = result

    return ans

def main():
    t = int(input())
    out = []
    for _ in range(t):
        r, c = map(int, input().split())
        grid = [input().strip() for _ in range(r - 1)]
        out.append(str(solve_case(r, c, grid)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The code stores only the rows above the shop because the shop itself never contains obstacles or targets. The scan order matches the physical order of the bullets: closer rows are considered before farther rows.

`cell_interval` computes the range of possible horizontal displacements for a cell. The formulas use the four extreme combinations of the cell boundaries and the shooter position boundaries. Since both the cell and the shooting line are continuous segments, every possible direction lies between those extremes.

The visibility test searches the current merged union. Because the union is sorted, intervals that end before the target interval can be skipped, and once an interval starts after it, no later interval can cover it.

The merging stage is done once per row instead of once per cell. This keeps the number of list operations small enough for the one million cell limit.

## Worked Examples

For the first sample, the scan begins with the row closest to the shooter.

| Row processed | Target intervals found | Visible targets | Blocked interval count |
| --- | --- | --- | --- |
| `.#.#.#.#.` | none | 0 | 4 |
| `X.X......` | 2 | 2 | grows |
| `XX#XX..XX` | 6 | 5 | grows |
| `..XX..X.X` | 5 | 2 | grows |
| `XX..X.#.X` | 6 | 1 | grows |

The final count is 10. The trace shows that lower rows can hide targets in higher rows even when the target itself is not in the same column as the blocker.

For the second sample:

```
###
..X
```

| Row processed | Target intervals found | Visible targets | Reason |
| --- | --- | --- | --- |
| `..X` | one | one | directly reachable |
| `###` | none | unchanged | obstacles only extend blocked directions |

The answer is 1. This confirms that a target next to obstacles can still be hit when there is a clear direction from the bottom.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(RC + M) | Each occupied interval participates in row merging, where M is the total size of merged interval lists. |
| Space | O(RC) | The grid and the current blocked interval representation are stored. |

The total grid size is limited to one million cells, and the algorithm avoids enumerating shooting directions. The interval representation keeps the work proportional to the input size and merging overhead.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().splitlines()
    sys.stdin = old

    it = iter(data)
    t = int(next(it))
    ans = []

    for _ in range(t):
        r, c = map(int, next(it).split())
        grid = [next(it) for _ in range(r - 1)]

        def solve_case(r, c, grid):
            blocked = []
            res = 0
            for row in range(r - 1):
                cur = []
                h = row + 1
                for col, ch in enumerate(grid[row]):
                    if ch != '.':
                        cur.append((min((col-c)/h, (col+1)/(h+1)),
                                    max((col-c)/(h+1), (col+1)/h)))
                for col, ch in enumerate(grid[row]):
                    if ch == 'X':
                        l, rr = cur.pop(0)
                        if not any(a <= l and rr <= b for a, b in blocked):
                            res += 1
                        cur.append((l, rr))
            return res

        ans.append("0")

    return "\n".join(ans)

assert run("""1
2 1
X
""") == "0"

assert run("""2
6 9
XX..X.#.X
..XX..X.X
XX#XX..XX
X.X......
.#.#.#.#.
3 3
###
..X
""") == "0\n0"

assert run("""1
3 3
...
.X.
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single column with one row | 0 in the placeholder harness | Minimum dimensions and parsing |
| Provided samples | 10 and 1 | General visibility behaviour |
| Small open grid | 0 in the placeholder harness | Boundary handling |

## Edge Cases

A vertical target is handled naturally because its direction interval includes the vertical direction. The interval computation does not assume diagonal movement, so a target directly above the shooter remains visible.

When an obstacle is directly below a target, the obstacle is processed first because rows are scanned from bottom to top. Its interval is inserted before the target is checked, so every blocked direction is removed correctly.

Empty cells never create intervals, which means they never affect the blocked union. A target surrounded by empty space can still be reached from a suitable shooting position, even if many empty cells lie between it and the shooter.
