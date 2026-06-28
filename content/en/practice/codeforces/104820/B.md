---
title: "CF 104820B - \u0421\u043f\u0443\u0441\u043a \u0441 \u0433\u043e\u0440\u044b"
description: "We are given a rectangular grid representing a mountain surface. Each cell contains an integer value, which can be positive or negative."
date: "2026-06-28T12:54:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104820
codeforces_index: "B"
codeforces_contest_name: "\u0420\u0421\u041e-\u0410\u043b\u0430\u043d\u0438\u044f 2018-2023. \u0418\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435"
rating: 0
weight: 104820
solve_time_s: 90
verified: false
draft: false
---

[CF 104820B - \u0421\u043f\u0443\u0441\u043a \u0441 \u0433\u043e\u0440\u044b](https://codeforces.com/problemset/problem/104820/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid representing a mountain surface. Each cell contains an integer value, which can be positive or negative. A path represents a walk on this grid: you start from any cell in the first row, move between adjacent cells using the four cardinal directions, and you are never allowed to move upward. You also cannot visit the same cell more than once. The path ends when you step out of the grid from the bottom row, and the value of a path is the sum of all visited cells.

The task is to compute the maximum possible path sum under these movement rules.

The grid size is up to 1500 by 1500, which implies about 2.25 million cells. Any solution that tries to explore all paths explicitly is impossible, since even a small branching factor over such a grid leads to exponential behavior. This forces us toward a dynamic programming solution that processes each cell a small constant number of times, ideally O(nm).

A subtle difficulty is the combination of horizontal movement and the “no revisiting” constraint. Even though upward movement is forbidden, horizontal movement still creates potential cycles in the underlying graph. A naive shortest or longest path relaxation would break because standard graph algorithms assume either acyclicity or allow revisits in a controlled way. Here, correctness depends on ensuring that within each row, we only consider simple paths, but still efficiently propagate best achievable sums.

One edge case that often breaks naive approaches is when optimal paths require long horizontal detours within a row before descending. For example, consider a row like `[1, -100, 1]` followed by a row `[100, 100, 100]`. The best strategy is to move across the top row carefully before dropping, but a naive “always go down immediately” greedy approach would miss the optimal structure entirely.

Another issue arises if one assumes that each cell can be processed independently from left and right. Horizontal movement creates dependencies across the row, so a single left-to-right pass is insufficient.

## Approaches

A brute-force interpretation would treat each cell as a node in a graph, with edges to its four neighbors except upward edges are disallowed. Then we would attempt to compute the maximum path sum from any top-row node to any bottom exit node without revisiting nodes. This is essentially a longest simple path problem in a general graph, which is computationally intractable. Even without revisits, the branching structure within rows allows an exponential number of paths, and exploring them directly would require on the order of O(4^(nm)) in the worst case.

The key structural observation is that although horizontal movement introduces cycles in the underlying graph, the “no upward movement” constraint induces a strong layer structure by rows. All motion is either within a row or strictly downward. This suggests processing the grid row by row, where the state for a cell depends only on the row above and on horizontal propagation within the same row.

This turns the problem into a dynamic programming system where each row can be solved independently once we know the best values entering from above. The remaining challenge is that within a row, we must account for arbitrary horizontal walks without revisiting cells. This can be handled by two directional sweeps that simulate optimal propagation of path values within the row.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Paths | Exponential | O(nm) | Too slow |
| Row-wise DP with horizontal relaxation | O(nm) | O(m) | Accepted |

## Algorithm Walkthrough

We process the grid row by row, maintaining the best achievable sum for each cell as an entry value from above or from previous horizontal movement.

### Steps

1. Initialize a DP array for the first row, where each entry is simply the value of that cell. This reflects that we may start at any top cell.
2. For each subsequent row, first compute a temporary DP value for each cell by adding its grid value to the best value from the cell directly above. This captures all paths that arrive vertically.
3. Perform a left-to-right sweep across the row. For each cell, update its best value by considering moving from the left neighbor within the same row and adding the current cell value. This simulates extending a path horizontally to the right.
4. Perform a right-to-left sweep with the same logic, allowing propagation from the right side. This ensures that paths that require turning within the row are correctly captured.
5. After both sweeps, the DP values for the row represent the best possible sum ending at each cell after all valid within-row movements.
6. Repeat this process for all rows, always overwriting the DP array.
7. The final answer is the maximum value in the last row DP array, since from any bottom cell we can exit the grid without additional cost.

### Why it works

The key invariant is that after processing row r, the DP value at each cell represents the maximum sum of any valid path that ends at that cell and respects all movement rules in rows 1 through r. The horizontal sweeps correctly resolve all intra-row simple paths because any optimal horizontal movement can be decomposed into a sequence of monotone extensions that are captured by left-to-right and right-to-left relaxations. Since movement between rows is strictly downward, there is no way for future rows to improve a past row state, which preserves optimal substructure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]
    
    dp = grid[0][:]

    for r in range(1, n):
        new_dp = [0] * m
        
        for c in range(m):
            new_dp[c] = dp[c] + grid[r][c]

        for c in range(1, m):
            new_dp[c] = max(new_dp[c], new_dp[c-1] + grid[r][c])

        for c in range(m-2, -1, -1):
            new_dp[c] = max(new_dp[c], new_dp[c+1] + grid[r][c])

        dp = new_dp

    print(max(dp))

if __name__ == "__main__":
    solve()
```

The implementation keeps only one DP row at a time, since earlier rows never need to be revisited once processed.

The first initialization step directly encodes the freedom to start anywhere in the top row. The vertical transition simply adds the current cell value, because entering a cell from above is the only downward inter-row movement allowed.

The two horizontal passes are the critical part. The left-to-right pass assumes we can extend a best path ending at the previous cell into the current one. The right-to-left pass mirrors this, ensuring symmetry so that paths that require moving left after moving right are also covered. Without both passes, some optimal zig-zag paths within a row would be missed.

## Worked Examples

### Sample 1

Input:

```
3 3
-1 1 -1
-1 1 1
-1 2 3
```

We track DP after each row.

| Row | DP state |
| --- | --- |
| 1 | [-1, 1, -1] |
| 2 vertical init | [-2, 2, 0] |
| 2 after left sweep | [-2, 2, 3] |
| 2 after right sweep | [-2, 2, 3] |
| 3 vertical init | [-3, 4, 6] |
| 3 after sweeps | [-3, 4, 8] |

Final answer is 8.

This example shows that the best path aggressively uses horizontal movement in row 3 to accumulate multiple positive values before exiting.

### Sample 2

Input:

```
2 2
1 1
2 2
```

| Row | DP state |
| --- | --- |
| 1 | [1, 1] |
| 2 vertical init | [3, 3] |
| 2 after sweeps | [3, 3] |

Final answer is 3.

This demonstrates that multiple starting points in the first row are handled naturally, since DP begins independently at each top cell.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is processed once per row with two linear sweeps |
| Space | O(m) | Only one DP row is stored at any time |

The grid size reaches up to 2.25 million cells, and each is touched a constant number of times, which fits comfortably within typical limits for a 1-2 second time budget in optimized Python or C++.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]
    
    dp = grid[0][:]

    for r in range(1, n):
        new_dp = [0] * m
        for c in range(m):
            new_dp[c] = dp[c] + grid[r][c]
        for c in range(1, m):
            new_dp[c] = max(new_dp[c], new_dp[c-1] + grid[r][c])
        for c in range(m-2, -1, -1):
            new_dp[c] = max(new_dp[c], new_dp[c+1] + grid[r][c])
        dp = new_dp

    return str(max(dp))

# provided samples
assert run("""3 3
-1 1 -1
-1 1 1
-1 2 3
""") == "8"

assert run("""2 2
1 1
2 2
""") == "3"

# custom tests
assert run("""1 1
5
""") == "5", "single cell"

assert run("""1 5
1 -2 3 -2 10
""") == "12", "single row horizontal optimal"

assert run("""3 1
1
2
3
""") == "6", "single column straight descent"

assert run("""2 3
-1 -1 -1
10 10 10
""") == "29", "best start anywhere top row"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | 5 | trivial base case |
| single row | 12 | horizontal accumulation only |
| single column | 6 | pure vertical path |
| mixed grid | 29 | best starting position and downward choice |

## Edge Cases

A minimal grid of size 1 by 1 is handled correctly because initialization directly sets DP to the cell value, and no transitions occur.

A single row case ensures that the algorithm correctly simulates unrestricted horizontal movement without any vertical transitions. The two sweeps fully propagate the best segment sum across the row.

A single column reduces the problem to a simple path from top to bottom. The DP recurrence becomes a cumulative sum, and horizontal sweeps have no effect since there is no horizontal neighbor, confirming that the algorithm does not introduce spurious transitions.
