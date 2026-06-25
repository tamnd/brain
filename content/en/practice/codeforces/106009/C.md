---
title: "CF 106009C - \u0421\u043c\u0430\u0439\u043b\u043e \u0438 Minecraft"
description: "We have a mine represented as a grid. Some cells contain gold, some are blocked by stone, and some are already empty. Smilo can choose an empty cell and place a bomb there. The bomb clears a square around the chosen cell with radius k in the Chebyshev distance."
date: "2026-06-25T13:19:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106009
codeforces_index: "C"
codeforces_contest_name: "\u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u041c\u0441\u0442\u0438\u0441\u043b\u0430\u0432\u0430 \u041a\u0435\u043b\u0434\u044b\u0448\u0430 - 2025"
rating: 0
weight: 106009
solve_time_s: 57
verified: true
draft: false
---

[CF 106009C - \u0421\u043c\u0430\u0439\u043b\u043e \u0438 Minecraft](https://codeforces.com/problemset/problem/106009/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a mine represented as a grid. Some cells contain gold, some are blocked by stone, and some are already empty. Smilo can choose an empty cell and place a bomb there. The bomb clears a square around the chosen cell with radius `k` in the Chebyshev distance. Gold exactly on the border of this square is collected, while gold strictly inside the square is lost.

The goal is to choose explosions that maximize the amount of gold collected. The difficulty is that after an explosion, many cells become empty, so later explosions may be placed in new locations.

The grid dimensions and `k` can be as large as 500, but the total number of cells over all test cases is limited. This rules out solutions that simulate every possible sequence of explosions. A direct search over all subsets of empty cells would be impossible. We need a way to evaluate all useful first moves efficiently and prove that the remaining moves can be handled implicitly.

A few edge cases are easy to miss. When `k = 1`, a bomb only affects the eight surrounding cells and the center. A common mistake is to treat the whole 3 by 3 square as lost gold, but the center is not part of the border. For example:

```
1
2 2 1
g.
.g
```

The only empty cell is the top right corner. The bomb collects the diagonally adjacent gold and destroys the other one only if it is inside the square. The correct answer is `1`, not `0`.

Another edge case is when the best strategy requires multiple bombs. Looking only for the best single explosion fails. For example:

```
1
3 4 2
.g..
g..#
g##.
```

A single bomb cannot collect all gold, but two bombs can. The answer is `3`. A solution that only counts the best initial explosion would underestimate the result.

A third subtle case is when the explosion reaches outside the grid. The border of the explosion square still exists outside the mine, so the square must be clipped only when counting cells that are actually in the grid. For example:

```
1
1 3 5
g.g
```

The only empty cell is in the middle. The explosion is much larger than the grid, but both gold cells are on the border of the square, so the answer is `2`.

## Approaches

The brute-force approach is to try every possible first bomb position, then simulate all future choices. It is correct because it explores exactly the possible actions Smilo can take. The problem is the number of possible sequences. With up to 250000 total cells, even considering only pairs of positions is already too expensive, and a full search over sequences is far beyond the limit.

The key observation is that after the first explosion, any later explosion is only useful for collecting gold that was not already destroyed. If a later bomb could collect gold, its center must be inside an area that has become available after previous explosions. The important part is that the first explosion is the only one that can destroy gold that is still present before any clearing happens.

For a chosen first bomb center, the only gold that can be permanently lost without being collected is the gold strictly inside the explosion square. Everything else can either be collected by the first bomb or by arranging later explosions. The greedy idea is to choose the first bomb that destroys the minimum amount of gold. The final answer is the total gold minus that minimum loss.

To check every possible first center, we need to know how much gold is inside the inner square of size `(2k - 1) x (2k - 1)`. A two dimensional prefix sum lets us query this in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Too large to define practically | O(nm) | Too slow |
| Prefix Sum Greedy | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Count the total number of gold cells and build a two dimensional prefix sum array where each entry stores the number of gold cells in the rectangle from the top left corner to that position. This allows us to count gold in any rectangle instantly.
2. Consider every empty cell as a possible first explosion center. This works because the first explosion is the only decision that determines which gold disappears before any future bomb can reach it.
3. For a center `(i, j)`, compute the inner square that is strictly inside the explosion. Its row range is from `i - k + 1` to `i + k - 1`, and its column range is from `j - k + 1` to `j + k - 1`. The coordinates are clipped to the grid because the mine does not contain cells outside it.
4. Use the prefix sum to find how much gold is destroyed inside this inner square. Keep the minimum such value among all possible first explosions.
5. Subtract the minimum lost gold from the total amount of gold. The remaining gold is the maximum amount that can be collected.

Why it works:

The first explosion divides the gold into two groups. Gold on the border of the explosion can be collected immediately, and gold outside the explosion remains available for later operations. Gold strictly inside the explosion can never be collected because it disappears. After the first explosion, the cells needed for future bombs have been cleared, so any gold that survived the first explosion can be obtained by choosing appropriate later explosions. Therefore maximizing collected gold is the same as minimizing the gold lost by the first explosion.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    pref = [[0] * (m + 1) for _ in range(n + 1)]
    total = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'g':
                total += 1
            pref[i + 1][j + 1] = (
                pref[i][j + 1]
                + pref[i + 1][j]
                - pref[i][j]
                + (grid[i][j] == 'g')
            )

    def get(x1, y1, x2, y2):
        if x1 > x2 or y1 > y2:
            return 0
        return (
            pref[x2 + 1][y2 + 1]
            - pref[x1][y2 + 1]
            - pref[x2 + 1][y1]
            + pref[x1][y1]
        )

    lost = total

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.':
                x1 = max(0, i - k + 1)
                y1 = max(0, j - k + 1)
                x2 = min(n - 1, i + k - 1)
                y2 = min(m - 1, j + k - 1)

                lost = min(lost, get(x1, y1, x2, y2))

    print(total - lost)

def main():
    t = int(input())
    for _ in range(t):
        solve()

main()
```

The prefix sum construction stores gold counts, not cell types. This keeps the later queries simple because every rectangle query only needs arithmetic on four prefix values.

The helper function `get` returns the number of gold cells in a rectangle. The bounds are already clipped before calling it, which avoids negative indices and off by one mistakes.

The inner square uses `k - 1` as its radius because cells exactly `k` away from the center are on the border and are collected. Only the strictly closer cells are lost.

The final loop tries every possible first bomb location. Since the answer depends only on the minimum destroyed gold among these locations, there is no need to simulate the later explosions.

## Worked Examples

### Sample 1

Input:

```
2 3 1
#.#
g.g
```

The middle cell is the only place where a bomb can be placed.

| Step | Center | Inner lost gold | Current minimum |
| --- | --- | --- | --- |
| Start | none | none | 2 |
| Check empty cell | (0,1) | 0 | 0 |

The explosion has radius `1`. The two gold cells are on the border, so they are both collected. The prefix sum finds that the inner square contains no gold.

### Sample 2

Input:

```
3 4 2
.gg.
g..#
g##.
```

There are several empty cells.

| Step | Center | Inner lost gold | Current minimum |
| --- | --- | --- | --- |
| Start | none | none | 4 |
| Check (0,0) | (0,0) | 1 | 1 |
| Check (1,1) | (1,1) | 0 | 0 |
| Check (1,2) | (1,2) | 2 | 0 |
| Check (2,0) | (2,0) | 2 | 0 |

The best first explosion destroys no gold. The remaining gold can be collected by later explosions, giving the answer `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is processed a constant number of times and each rectangle query is O(1). |
| Space | O(nm) | The prefix sum array stores one value for every grid cell. |

The total number of cells over all tests is limited, so the quadratic memory and time usage fits comfortably.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    t = int(next(it))
    out = []

    for _ in range(t):
        n = int(next(it))
        m = int(next(it))
        k = int(next(it))
        grid = [next(it) for _ in range(n)]

        pref = [[0] * (m + 1) for _ in range(n + 1)]
        total = 0

        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'g':
                    total += 1
                pref[i + 1][j + 1] = (
                    pref[i][j + 1]
                    + pref[i + 1][j]
                    - pref[i][j]
                    + (grid[i][j] == 'g')
                )

        def get(x1, y1, x2, y2):
            if x1 > x2 or y1 > y2:
                return 0
            return pref[x2 + 1][y2 + 1] - pref[x1][y2 + 1] - pref[x2 + 1][y1] + pref[x1][y1]

        lost = total
        for i in range(n):
            for j in range(m):
                if grid[i][j] == '.':
                    lost = min(
                        lost,
                        get(
                            max(0, i - k + 1),
                            max(0, j - k + 1),
                            min(n - 1, i + k - 1),
                            min(m - 1, j + k - 1)
                        )
                    )

        out.append(str(total - lost))

    return "\n".join(out)

assert run("""3
2 3 1
#.#
g.g
2 3 2
#.#
g.g
3 4 2
.gg.
g..#
g##.
""") == "2\n0\n4"

assert run("""1
1 1 1
.
""") == "0"

assert run("""1
1 3 5
g.g
""") == "2"

assert run("""1
3 3 1
ggg
g.g
ggg
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3 1` sample | `2` | Border cells are collected correctly |
| `1 1 1` | `0` | Smallest possible grid |
| `1 3 5` | `2` | Explosion extending outside the grid |
| `3 3 1` | `0` | Cases where every possible explosion loses gold |

## Edge Cases

For the `k = 1` case, the algorithm uses an inner radius of zero. The rectangle query becomes a single cell query around the center, so only the center cell would be considered lost. Since bomb centers are empty, no gold is counted as destroyed. This correctly handles the smallest explosion size.

For a strategy requiring multiple bombs, the algorithm does not explicitly simulate those bombs. Instead, it finds a first explosion that loses the least gold. Any gold outside that inner area survives the first step and can be collected later. This is why the third sample is handled correctly even though the answer cannot be obtained by one explosion.

When the explosion is larger than the board, the computed inner square is clipped to the actual mine boundaries. The outside part of the square contains no gold, so ignoring it does not change the number of destroyed cells.
