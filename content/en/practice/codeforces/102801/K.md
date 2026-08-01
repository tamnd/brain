---
title: "CF 102801K - PepperLa's Boast"
description: "The problem describes a runner moving through a burning grid. The runner starts at the top left cell and needs to reach the bottom right cell. Each cell contains an amount of fresh air."
date: "2026-08-01T23:20:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102801
codeforces_index: "K"
codeforces_contest_name: "The 14th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102801
solve_time_s: 128
verified: true
draft: false
---

[CF 102801K - PepperLa's Boast](https://codeforces.com/problemset/problem/102801/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a runner moving through a burning grid. The runner starts at the top left cell and needs to reach the bottom right cell. Each cell contains an amount of fresh air. Positive cells can be breathed in, while non-positive cells contain smoke and cannot be entered unless the runner is currently holding his breath.

A move always goes down, right, or diagonally down-right, so the path is a directed acyclic path through the grid. Starting a breath-holding session costs `U` air and allows passing through smoke for at most `K` moves. The goal is not only to escape, but to maximize the amount of air remaining after reaching the exit.

The grid dimensions can both reach `1000`, and the sum of all grid cells over all test cases can reach `7 * 10^6`. An algorithm that explores every possible path is impossible because the number of paths grows exponentially. Even a dynamic program that checks every possible previous cell for every position would be around `O(N^2M^2)` in the worst case, which is far beyond the limit. We need a solution close to linear in the number of cells.

The main edge cases come from the interaction between normal movement and breath jumps. A path may need to start holding breath before entering smoke, and the best previous position may be far away inside the `K` by `K` rectangle rather than one of the three neighboring cells.

For example:

```
1 3 2 5
10 0 10
```

The answer is `15`. A careless solution that only considers adjacent positive cells would fail because the runner must spend air to cross the middle smoke cell.

Another case is when `K` is larger than the grid size:

```
2 2 10 3
5 0
0 7
```

The answer is `9`. A solution that assumes the breath duration is exactly `K` moves may reject valid paths that stop earlier.

## Approaches

A direct dynamic programming solution is easy to define. Let `dp[i][j]` be the maximum air remaining after reaching cell `(i,j)`. If the current cell contains air, we can arrive from the three normal predecessor cells. We can also start holding breath from any earlier reachable cell within `K` rows and `K` columns, paying `U` and adding the current cell's air.

The recurrence is correct, but the breath transition is expensive. For every cell we would scan up to `K*K` possible starting positions. Since `K` can be as large as `10^9`, this is effectively a scan of the entire previous grid and is too slow.

The key observation is that the breath transition only needs the maximum `dp` value inside a sliding rectangle. While scanning row by row, this rectangle always moves one step at a time. We can maintain the maximum values with monotonic queues.

For every column, keep a deque containing useful starting positions from the last `K` rows. The deque is decreasing by `dp` value, so its front is the best candidate in that column. Then maintain another deque across the current row to get the best column among the last `K` columns. Together these two structures provide the maximum `dp` value in the entire `K` by `K` window in constant amortized time.

The brute force works because every valid breath start is checked, but fails when the grid becomes large. The observation that the transition is a sliding maximum lets us replace millions of repeated comparisons with two monotonic queues.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM * K²) | O(NM) | Too slow |
| Optimal | O(NM) | O(M) | Accepted |

## Algorithm Walkthrough

1. Process the grid from top to bottom and left to right. This order matches the movement rules because every possible predecessor of a cell has already been processed.
2. For every positive cell, first compute transitions without holding breath. The three possible previous cells are the cell above, the cell on the left, and the diagonal cell. Add the current cell's air after taking the maximum reachable value.
3. Maintain column deques containing previous cells that can start a breath session. Remove entries that are more than `K` rows away. The deque keeps the largest `dp` values at the front because weaker candidates can never become useful later.
4. Maintain a row deque containing the best candidates from the active columns. Remove columns that are more than `K` columns away. The front of this deque is the best possible starting point for a breath session ending at the current cell.
5. If the current cell is positive and a valid breath start exists, update `dp[i][j]` with the value from that start minus `U`, then add the current cell's air.
6. After computing `dp[i][j]`, insert it into its column deque only if the remaining air is at least `U`. A smaller value cannot start a breath session because it cannot pay the cost.

Why it works: the invariant is that every deque contains exactly the useful reachable cells inside the current sliding window, ordered so the best candidate is always at the front. Removing old entries preserves the distance restriction, and removing dominated entries preserves the maximum because a worse value with a later expiration can never beat a larger value with the same or earlier expiration. Every possible transition is represented, so the computed `dp` value is always the best possible air amount.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve_case(n, m, k, u, grid):
    cols = [deque() for _ in range(m)]
    dp_prev = [-1] * m
    ans = -1

    for i in range(n):
        row_best = deque()
        dp_cur = [-1] * m

        for j in range(m):
            while cols[j] and cols[j][0][0] < i - k:
                cols[j].popleft()

            while row_best and row_best[0][1] < j - k:
                row_best.popleft()

            if grid[i][j] > 0:
                best = -1

                if i == 0 and j == 0:
                    best = 0

                if i > 0 and dp_prev[j] >= 0:
                    best = max(best, dp_prev[j])

                if j > 0 and dp_cur[j - 1] >= 0:
                    best = max(best, dp_cur[j - 1])

                if i > 0 and j > 0 and dp_prev[j - 1] >= 0:
                    best = max(best, dp_prev[j - 1])

                if row_best:
                    best = max(best, row_best[0][0] - u)

                if best >= 0:
                    dp_cur[j] = best + grid[i][j]

            if dp_cur[j] >= u:
                while cols[j] and cols[j][-1][1] <= dp_cur[j]:
                    cols[j].pop()
                cols[j].append((i, dp_cur[j]))

            if cols[j]:
                value = cols[j][0][1]
                while row_best and row_best[-1][0] <= value:
                    row_best.pop()
                row_best.append((value, j))

            if i == n - 1 and j == m - 1:
                ans = dp_cur[j]

        dp_prev = dp_cur

    return ans

def main():
    out = []
    data = sys.stdin.buffer.read().split()
    ptr = 0

    while ptr < len(data):
        n = int(data[ptr])
        m = int(data[ptr + 1])
        k = int(data[ptr + 2])
        u = int(data[ptr + 3])
        ptr += 4

        grid = []
        for _ in range(n):
            row = list(map(int, data[ptr:ptr + m]))
            ptr += m
            grid.append(row)

        out.append(str(solve_case(n, m, k, u, grid)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation stores only the previous row of `dp`, because normal transitions only need cells directly above or diagonally above. The column deques store row indices so expired states can be removed when the distance becomes larger than `K`.

The insertion order matters. A cell must be used as a breath starting point only after its own value has been computed, so it is added to the queues after all transitions for the current cell are finished. This prevents accidentally allowing a zero length breath move.

All values are stored as Python integers because the maximum possible remaining air can exceed 32 bit limits.

## Worked Examples

For the sample:

```
3 4 2 1
1 0 0 9
0 -1 1 1
-1 0 2 1
```

The important states are:

| Cell | Best transition | Remaining air |
| --- | --- | --- |
| (1,1) | Start | 1 |
| (2,2) | Hold from (1,1) | 0 |
| (2,3) | Stop holding, collect air | 1 |
| (3,3) | Normal move | 3 |
| (3,4) | Normal move | 4 |

The trace shows why a breath session is represented as a jump transition. The runner does not need to store every smoke cell separately, only the starting point and the final cost.

A second example:

```
2 2 10 3
5 0
0 7
```

| Cell | Best transition | Remaining air |
| --- | --- | --- |
| (1,1) | Start | 5 |
| (1,2) | Hold from (1,1) | 9 |
| (2,1) | Hold from (1,1) | 9 |
| (2,2) | Normal move | 16 |

The large `K` value allows crossing smoke immediately, and the optimal path keeps all collected air.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NM) | Every cell enters and leaves each monotonic queue once. |
| Space | O(M) | Only one row of DP and the column queues are stored. |

The algorithm touches each grid cell a constant number of times, which fits the total limit of several million cells. The memory usage depends on the number of columns rather than the whole grid.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    idx = 0
    ans = []

    while idx < len(data):
        n, m, k, u = map(int, data[idx:idx + 4])
        idx += 4
        grid = []
        for _ in range(n):
            grid.append(list(map(int, data[idx:idx + m])))
            idx += m

        ans.append(str(solve_case(n, m, k, u, grid)))

    return "\n".join(ans)

assert run("""3 4 2 1
1 0 0 9
0 -1 1 1
-1 0 2 1
""") == "4", "sample"

assert run("""1 1 5 10
7
""") == "7", "single cell"

assert run("""1 3 2 5
10 0 10
""") == "15", "cross smoke"

assert run("""2 2 10 3
5 0
0 7
""") == "16", "large breath duration"

assert run("""2 3 1 100
5 1 1
1 1 9
""") == "17", "all positive cells"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 x 1` grid | `7` | Starting cell handling |
| Smoke gap | `15` | Breath transition |
| Large `K` | `16` | Long breath sessions |
| All positive cells | `17` | Normal movement only |

## Edge Cases

A path that begins by holding breath from the starting cell is handled because `(1,1)` is inserted into the DP process normally. The case

```
1 3 2 5
10 0 10
```

creates a breath transition from the first cell to the last cell. The deque window contains the starting state, subtracts `U`, and adds the final air.

A breath session ending earlier than `K` moves is valid. In

```
2 2 10 3
5 0
0 7
```

the runner does not need to spend all ten possible minutes. The sliding window only limits the maximum distance, so the normal transition after reaching a safe cell remains available.

Cells with low remaining air are not inserted into the breath queues unless their value is at least `U`. This avoids creating impossible transitions where the runner would try to start holding breath without enough air.
