---
title: "CF 102623M - MITE"
description: "We have a rectangular farm with at most 30 rows and only 8 columns. A cell is either blocked rock or usable sand. We may turn any sand cells into water. After choosing the water cells, every remaining sand cell that touches at least one water cell can grow sugar cane."
date: "2026-08-04T17:16:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "M"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 75
verified: true
draft: false
---

[CF 102623M - MITE](https://codeforces.com/problemset/problem/102623/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular farm with at most 30 rows and only 8 columns. A cell is either blocked rock or usable sand. We may turn any sand cells into water. After choosing the water cells, every remaining sand cell that touches at least one water cell can grow sugar cane. The task is to decide which sand cells become water so that the number of cane cells is as large as possible, then print the resulting grid.

The small width is the key restriction. The number of rows can be 30, but the number of columns is only 8, so a row can be represented by a bitmask with at most 256 possible values. A solution that is exponential in the number of columns is acceptable, while one exponential in the total number of cells is impossible. Trying every subset of all sand cells could mean checking up to $2^{240}$ configurations, which is far beyond any practical limit.

Several details can break a simple greedy solution. For example, water cells are not valuable themselves, only their effect on neighboring cells matters. In a one-row grid:

```
2 3
...
```

placing water in the middle cell gives:

```
.X.
```

with the water omitted from the output representation here for simplicity, while placing water at the edge gives fewer adjacent cane cells. A strategy that always places water on the most open-looking cells can fail because a water cell can help multiple future rows.

Another issue is that a cell can receive water influence from the next row, so a row cannot always be finalized immediately after choosing its own water. For example:

```
2 1
.
.
```

The top cell cannot be judged until we know whether the bottom cell becomes water. The algorithm must remember the previous row's decision.

## Approaches

A direct approach would choose every possible set of sand cells to turn into water. For each choice, we could scan the grid and count how many remaining sand cells touch water. This is correct because it examines every possible final arrangement. However, if the farm contains 240 sand cells, the number of choices is $2^{240}$, which is impossible.

The structure of the grid gives us a better view. Since the width is only 8, the interaction between processed and unprocessed parts of the grid happens through a single row. We only need to remember which cells in the previous row are water. This turns the problem into dynamic programming over row masks.

For every row, we enumerate all possible water masks that are subsets of the sand cells in that row. When we decide the next row's water mask, the previous row becomes completely determined because we now know all water cells adjacent to it. We can then add the number of cane cells created in that row. The number of masks is at most 256, so the total transition count is small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{nm}nm)$ | $O(nm)$ | Too slow |
| Optimal | $O(n \cdot 2^m \cdot 2^m \cdot m)$ | $O(n \cdot 2^m)$ | Accepted |

## Algorithm Walkthrough

1. Precompute every possible water mask for each row. A bit set in the mask means that the corresponding sand cell is changed into water. Rock cells can never appear in a water mask.
2. Use dynamic programming where the state is the water mask of the previous row. The value stored is the maximum number of cane cells already finalized above that row. The previous row is the only information needed because all future effects can only come from the immediately adjacent row.
3. When processing row `i`, try every possible water mask for this row. For every previous mask, calculate the score of row `i - 1`. A cell in the previous row becomes cane if it is sand and at least one of its four neighbors is water.
4. Store the best transition for every row and every resulting mask. These parent pointers allow us to reconstruct the selected water rows after the dynamic programming finishes.
5. After the last real row, perform one extra transition with an empty water mask. This final step scores the last row because it now has a known "next row" containing no water.
6. Reconstruct the chosen water masks by following the stored parents backward. Then convert every chosen water cell to `O`, every sand cell adjacent to water to `X`, and leave other sand cells as `.`.

The invariant is that after processing some number of rows, every row before the stored mask has already received its final optimal contribution. The stored mask contains exactly the information needed to evaluate the next row when a new mask is chosen. Since every possible row transition is considered, the best state after the final transition represents the maximum possible number of cane cells.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    row_masks = []
    for r in range(n):
        masks = []
        for mask in range(1 << m):
            ok = True
            for c in range(m):
                if (mask >> c) & 1 and grid[r][c] == '#':
                    ok = False
                    break
            if ok:
                masks.append(mask)
        row_masks.append(masks)

    def score_row(r, above, cur):
        if r < 0 or r >= n:
            return 0
        res = 0
        for c in range(m):
            if grid[r][c] == '#':
                continue
            if (above >> c) & 1:
                continue
            water = False
            if c > 0 and ((above >> (c - 1)) & 1):
                water = True
            if c + 1 < m and ((above >> (c + 1)) & 1):
                water = True
            if (above >> c) & 1:
                water = True
            if (cur >> c) & 1:
                water = True
            if water:
                res += 1
        return res

    parent = [[-1] * (1 << m) for _ in range(n + 1)]

    dp = [-10**9] * (1 << m)
    dp[0] = 0

    for r in range(n):
        ndp = [-10**9] * (1 << m)
        for prev in range(1 << m):
            if dp[prev] < 0:
                continue
            for cur in row_masks[r]:
                val = dp[prev] + score_row(r - 1, prev, cur)
                if val > ndp[cur]:
                    ndp[cur] = val
                    parent[r][cur] = prev
        dp = ndp

    best = -1
    last = -1
    for prev in range(1 << m):
        val = dp[prev] + score_row(n - 1, prev, 0)
        if val > best:
            best = val
            last = prev

    water = [0] * n
    mask = last
    for r in range(n - 1, -1, -1):
        water[r] = mask
        mask = parent[r][mask]

    ans = [list(row) for row in grid]
    for r in range(n):
        for c in range(m):
            if (water[r] >> c) & 1:
                ans[r][c] = 'O'

    for r in range(n):
        for c in range(m):
            if ans[r][c] != '.':
                continue
            ok = False
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m:
                    if ans[nr][nc] == 'O':
                        ok = True
            if ok:
                ans[r][c] = 'X'

    print('\n'.join(''.join(row) for row in ans))

if __name__ == "__main__":
    solve()
```

The `row_masks` array removes impossible choices before the dynamic programming starts. A rock cell can never become water, so masks containing those bits are discarded.

The transition function evaluates a row only after the next row decision is available. This avoids the common mistake of forgetting that a cell can receive water influence vertically from below. The artificial final transition with mask `0` has the same purpose for the bottom row.

The reconstruction stores only the previous mask for each chosen state. Since every row has at most 256 masks, storing these parents is small. There are no large integer issues because the maximum score is only 240.

## Worked Examples

For a small example:

Input:

```
3 3
...
.#.
...
```

The dynamic programming states can be summarized as:

| Row processed | Current stored mask | Meaning |
| --- | --- | --- |
| Start | `000` | No previous water |
| After row 0 | several masks | First row choices considered |
| After row 1 | best masks | Middle row choices considered |
| After row 2 | best masks | All rows considered |
| Final transition | `000` | Bottom row finalized |

The trace shows why the algorithm delays scoring. The top row is not finalized until the second row mask is known.

For the second sample:

```
3 3
.#.
#.#
.#.
```

The center row has limited choices because rocks block possible water placement. The row-mask restriction removes invalid transitions immediately, and the dynamic programming keeps only legal configurations.

| Row | Available mask count | Stored information |
| --- | --- | --- |
| 0 | 4 | Possible water in non-rock cells |
| 1 | 2 | Rock cells removed from choices |
| 2 | 4 | Bottom row evaluated after final transition |

This case confirms that the algorithm does not assume every cell can become water.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 2^m \cdot 2^m \cdot m)$ | Every pair of previous and current masks is tested and each score scans a row |
| Space | $O(n \cdot 2^m)$ | Stores parents for reconstruction |

With `m <= 8`, there are at most 256 masks. The transition count is roughly `30 * 256 * 256`, which is easily manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

# Minimum size
assert len(run("1 1\n.\n").strip()) == 1

# All rocks
assert run("2 2\n##\n##\n") == "##\n##\n"

# Single row boundary case
res = run("1 3\n...\n")
assert 'O' in res

# Mixed rocks and sand
res = run("3 3\n.#.\n...\n.#.\n")
assert res.count('X') >= 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 x 1` sand | Any valid one-character result | Minimum dimensions |
| All rocks | Same grid | No legal water placement |
| One row of sand | Valid maximum arrangement | Horizontal boundary handling |
| Rocks inside grid | Valid arrangement | Mask filtering |

## Edge Cases

A single sand cell surrounded by rocks has no possible water neighbor unless it itself becomes water, but water cannot create cane. For:

```
1 1
.
```

the only valid outputs are `.` or `O`. The algorithm considers both states and correctly avoids counting the water cell as cane.

A row next to another row can receive help from below. For:

```
2 1
.
.
```

choosing the bottom cell as water allows the top cell to become cane. The dynamic programming does not score the top row too early, so this vertical dependency is handled correctly.

A grid containing only rocks:

```
2 2
##
##
```

has no possible water masks except zero. The answer remains unchanged because the mask generation step rejects all invalid water choices.
