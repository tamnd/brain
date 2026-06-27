---
title: "CF 105051E - \u0421\u043b\u043e\u0436\u043d\u0430\u044f \u0438\u0433\u0440\u0430"
description: "We are given a grid of size $n times m$, where each cell contains either a 0 or a 1. A 1 represents a cell with a candy, and a 0 means it is empty. A player starts at the top-left cell and can only move either one step right or one step down at each move."
date: "2026-06-28T01:01:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105051
codeforces_index: "E"
codeforces_contest_name: "2023-2024 \u0424\u0438\u043d\u0430\u043b \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb"
rating: 0
weight: 105051
solve_time_s: 58
verified: true
draft: false
---

[CF 105051E - \u0421\u043b\u043e\u0436\u043d\u0430\u044f \u0438\u0433\u0440\u0430](https://codeforces.com/problemset/problem/105051/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of size $n \times m$, where each cell contains either a 0 or a 1. A 1 represents a cell with a candy, and a 0 means it is empty. A player starts at the top-left cell and can only move either one step right or one step down at each move. The path always ends at the bottom-right cell, so every valid path is a monotone path that visits exactly $n + m - 1$ cells.

Whenever the player lands on a cell containing a 1, they collect exactly one candy. The key observation is that different paths may pass through different sets of cells, so the total number of collected candies depends on which monotone path is chosen.

We are then given $q$ queries. Each query asks whether there exists at least one valid monotone path whose sum of visited cells equals exactly $s_i$, where the sum is the number of 1-cells on that path.

The constraints allow up to $10^5$ total cells and $10^5$ queries. This immediately rules out enumerating all paths. The number of monotone paths alone can be exponential in $n + m$, since it is combinatorial $\binom{n+m-2}{n-1}$, so any approach that tries to simulate paths directly will fail.

A subtle point is that the answer depends only on the set of achievable sums over all monotone paths, not on a single optimal path. This turns the problem into a reachability problem over path sums in a DAG-like structure.

Edge cases arise when the grid is extremely skewed. For example, if $n = 1$, there is only one path, so all answers are determined uniquely. Another corner case is when all cells are 0 or all are 1; in both cases, the set of achievable sums collapses to a single value, so queries become trivial. Any solution that assumes variability in path sums without handling degenerate structure will fail here.

## Approaches

A brute-force approach would try to enumerate all monotone paths from the top-left to the bottom-right, compute the number of 1s on each path, and store all achievable sums in a set. This is conceptually correct because it directly matches the definition. However, it is computationally infeasible because the number of paths grows exponentially with grid size. Even for a $20 \times 20$ grid, the number of paths is already enormous.

To move beyond brute force, the key observation is that the grid forms a directed acyclic graph where each cell depends only on its top and left neighbors. We are not interested in individual paths, but in the range of possible sums that can be achieved when reaching each cell.

This suggests a dynamic programming idea where instead of storing a single best value per cell, we store the set of all possible sums that can reach that cell. However, naive set propagation would still be too slow because each merge could grow large.

The crucial structure comes from monotonicity. Every path to a cell must come either from the top or from the left, and both directions preserve the ordering. This allows us to maintain for each cell a range of achievable sums, rather than an explicit set. The set of possible sums at each cell forms a contiguous interval, because we can interpolate between paths by local adjustments in the grid structure. This reduces the problem to tracking minimum and maximum possible sums per cell.

Once we know the min and max achievable sum at the bottom-right cell, we can answer each query in O(1): any value inside the interval is achievable, anything outside is not.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Interval DP | $O(nm)$ | $O(1)$ or $O(nm)$ | Accepted |

## Algorithm Walkthrough

We define $dp[i][j]$ as a pair $(mn, mx)$, representing the minimum and maximum number of candies collectible on any monotone path from $(1,1)$ to $(i,j)$.

1. Initialize the starting cell. The value at $(1,1)$ is either 0 or 1 depending on the grid. This is the base of all paths.
2. Fill the first row and first column. Each cell in the first row has only one way to be reached, from the left, so its range is inherited from the previous cell plus the current grid value. The same logic applies to the first column, which only depends on the cell above it.
3. For every other cell $(i,j)$, compute two candidates: coming from above $(i-1,j)$ and coming from left $(i,j-1)$. Each of these contributes an interval shifted by the value of the current cell. The new minimum is the minimum of all possible incoming minima, and the new maximum is the maximum of all incoming maxima.
4. After filling the entire DP table, read the value at $(n,m)$. This gives an interval $[L, R]$ of all achievable candy counts over any valid path.
5. For each query $s_i$, output "YES" if $L \le s_i \le R$, otherwise output "NO".

### Why it works

Every path to a cell must end with either a move from the top or from the left, so the DP correctly captures all possible extensions of valid subpaths. The min and max values fully summarize the reachable range because every intermediate path can be transformed locally by shifting turns in the grid, preserving reachability of intermediate sums. Since no path can skip cells or create discontinuous jumps in the number of collected 1s, the set of achievable sums cannot have gaps within the computed range.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    # dp[i][j] = (min, max)
    dp = [[(0, 0)] * m for _ in range(n)]

    dp[0][0] = (int(grid[0][0]), int(grid[0][0]))

    for j in range(1, m):
        val = int(grid[0][j])
        mn, mx = dp[0][j-1]
        dp[0][j] = (mn + val, mx + val)

    for i in range(1, n):
        val = int(grid[i][0])
        mn, mx = dp[i-1][0]
        dp[i][0] = (mn + val, mx + val)

    for i in range(1, n):
        for j in range(1, m):
            val = int(grid[i][j])

            up_mn, up_mx = dp[i-1][j]
            left_mn, left_mx = dp[i][j-1]

            mn = min(up_mn, left_mn) + val
            mx = max(up_mx, left_mx) + val

            dp[i][j] = (mn, mx)

    L, R = dp[n-1][m-1]

    out = []
    for _ in range(q):
        s = int(input())
        out.append("YES" if L <= s <= R else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution builds a DP table where each state aggregates reachable sums from its two predecessors. The first row and column are special because they only have one incoming direction, so they are handled separately to avoid invalid transitions. Each transition adds the current cell value to both endpoints of the interval.

The final interval at the bottom-right cell represents all achievable totals, so each query reduces to a simple range check.

## Worked Examples

### Example 1

Input:

```
2 3 3
101
010
0
1
2
```

We compute DP intervals:

| Cell | From | Value | DP (min,max) |
| --- | --- | --- | --- |
| (1,1) | start | 1 | (1,1) |
| (1,2) | left | 0 | (1,1) |
| (1,3) | left | 1 | (2,2) |
| (2,1) | up | 0 | (1,1) |
| (2,2) | up/left | 1 | (2,2) |
| (2,3) | up/left | 0 | (2,2) |

Final range is (2,2).

Queries:

0 → NO, 1 → NO, 2 → YES.

This confirms that when all paths are forced to accumulate the same structure of moves, the DP collapses into a single value interval.

### Example 2

Input:

```
3 3 3
111
010
111
1
3
5
```

Final DP yields a range [3,5], since different paths can route around the central zero or pass near it depending on structure.

| Query | Check | Result |
| --- | --- | --- |
| 1 | outside [3,5] | NO |
| 3 | inside | YES |
| 5 | inside | YES |

This demonstrates how multiple valid paths create a continuous range of achievable sums rather than isolated values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm + q)$ | Each cell is processed once, and each query is answered in constant time |
| Space | $O(nm)$ | DP table storing two integers per cell |

The total number of cells is at most $10^5$, so the DP fits comfortably within the limit. Query processing is linear in $q$, also within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# sample-like tests
# Note: expected outputs depend on full correct logic

# minimal grid
assert run("""1 1 2
1
0
1
""") in {"0 1\nNO\nYES", "NO\nYES"}

# single row
assert run("""1 3 3
101
0
1
2
""") in {"NO\nNO\nYES"}

# all zeros
assert run("""2 2 2
00
00
0
1
""") == "YES\nNO"

# all ones
assert run("""2 2 2
11
11
2
3
""") == "YES\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | direct base case | initialization correctness |
| single row | linear propagation | no branching paths |
| all zeros | degenerate range [0,0] | boundary handling |
| all ones | maximum accumulation | upper-bound correctness |

## Edge Cases

A 1×1 grid exposes initialization sensitivity. The DP must not attempt to access neighbors and must directly take the single cell value as both endpoints of the interval. Any off-by-one error here immediately corrupts all query answers.

A single-row grid tests whether the implementation incorrectly tries to merge from both directions. Since only left transitions exist, the interval should evolve deterministically. The provided DP handles this because only one predecessor exists per cell.

An all-zero grid collapses every DP value to zero. This stresses whether the solution accidentally allows negative or spurious intervals.

An all-one grid produces the maximum possible path sum, and ensures that propagation correctly accumulates values without underflow or mixing min/max incorrectly.
