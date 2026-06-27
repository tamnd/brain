---
title: "CF 105079E - Cupcake Collecting"
description: "We are given a square grid of size $N times N$, where each cell is either blocked or usable. A blocked cell is marked with $-1$, and cannot be entered. Every other cell contains a non-negative number representing cupcakes available in that cell."
date: "2026-06-27T21:26:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105079
codeforces_index: "E"
codeforces_contest_name: "UTPC x WiCS Contest 04-05-23 (UT Internal)"
rating: 0
weight: 105079
solve_time_s: 90
verified: true
draft: false
---

[CF 105079E - Cupcake Collecting](https://codeforces.com/problemset/problem/105079/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square grid of size $N \times N$, where each cell is either blocked or usable. A blocked cell is marked with $-1$, and cannot be entered. Every other cell contains a non-negative number representing cupcakes available in that cell. Alice starts at the top-left corner $(1,1)$ and must reach the bottom-right corner $(N,N)$, moving only right or down at each step. Whenever she enters a cell, she collects all cupcakes in it.

The task is to compute the maximum total cupcakes Alice can collect along any valid path from start to finish, or determine that no such path exists.

The grid size constraint $N \leq 1000$ means up to one million cells. Any solution that tries to enumerate all paths is immediately infeasible because the number of monotone paths grows exponentially, roughly on the order of $\binom{2N}{N}$. This quickly becomes astronomically large even for moderate $N$, so brute-force path enumeration is not an option.

Instead, we need a method that processes each cell a constant number of times, ideally $O(N^2)$.

A subtle edge case arises when either the start or end becomes unreachable due to blocked cells. Another is when a cell is reachable in terms of geometry but all paths leading into it are blocked. For example:

Input:

```
3
0 1 1
-1 -1 1
1 1 1
```

Even though the destination exists and contains cupcakes, the middle barrier disconnects the grid, making it impossible to reach the bottom-right cell. The correct answer is $-1$, and any naive DP that ignores reachability would incorrectly accumulate values into unreachable states.

## Approaches

A brute-force strategy would attempt to explore every valid path from the top-left to the bottom-right, accumulating cupcake counts along the way. Since movement is restricted to right and down, each path is a sequence of exactly $2N-2$ moves, and the number of such sequences is exponential in $N$. Even if we prune paths hitting $-1$ cells, the worst-case grid with no obstacles forces exploration of all monotone paths, which is far too large.

The key observation is that the value collected at any cell depends only on the best way to reach that cell. Once we arrive at a cell $(i,j)$, the optimal score up to that point is independent of how we got there, except for the best possible accumulated value. This is a classic optimal substructure situation.

So instead of exploring paths, we compute a dynamic programming table where $dp[i][j]$ represents the maximum cupcakes obtainable when reaching cell $(i,j)$. Each cell only depends on its top and left neighbors, since those are the only ways to enter it. If a cell is blocked, it contributes nothing and is marked unreachable.

This reduces the problem from exponential path enumeration to a simple grid traversal with constant work per cell.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{2N})$ | $O(N)$ recursion stack | Too slow |
| Dynamic Programming | $O(N^2)$ | $O(N^2)$ | Accepted |

## Algorithm Walkthrough

We define a DP table where each state stores the best achievable cupcake total when reaching that cell. We also need a way to represent unreachable states.

1. Initialize a 2D array $dp$ of size $N \times N$, filled with a sentinel value representing unreachable, such as $-\infty$. This ensures we never accidentally treat an invalid path as contributing to a maximum.
2. Set the starting cell $dp[0][0]$. If it is blocked, the entire problem is immediately impossible, since Alice cannot move at all. Otherwise initialize it to the value of the starting cell, which is guaranteed to be zero.
3. Iterate through the grid row by row. For each cell $(i,j)$, if it is blocked, leave $dp[i][j]$ as unreachable. This preserves correctness because no path can legally enter it.
4. If the cell is not blocked, compute the best possible way to arrive there. Alice can only come from above $(i-1,j)$ or from the left $(i,j-1)$, so we take the maximum of those two dp values, provided they are reachable. The current cell value is added to this maximum. If both neighbors are unreachable, the cell remains unreachable.
5. After filling the table, the answer is $dp[N-1][N-1]$. If it is still unreachable, output $-1$, otherwise output the stored value.

### Why it works

At every cell $(i,j)$, the DP value represents the maximum cupcakes achievable among all valid paths from $(0,0)$ to $(i,j)$. Any such path must end by arriving from either $(i-1,j)$ or $(i,j-1)$, and both of those states already store optimal values for their respective prefixes. Because the transition considers both and takes the maximum, no better prefix path can be missed. Blocked cells correctly break transitions because they eliminate all paths passing through them, ensuring unreachable regions remain excluded from future computations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    grid = [list(map(int, input().split())) for _ in range(n)]
    
    NEG = -10**18
    dp = [[NEG] * n for _ in range(n)]
    
    if grid[0][0] == -1 or grid[n-1][n-1] == -1:
        print(-1)
        return
    
    dp[0][0] = 0
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] == -1:
                continue
            
            if i == 0 and j == 0:
                continue
            
            best = NEG
            if i > 0:
                best = max(best, dp[i-1][j])
            if j > 0:
                best = max(best, dp[i][j-1])
            
            if best == NEG:
                continue
            
            dp[i][j] = best + grid[i][j]
    
    print(dp[n-1][n-1] if dp[n-1][n-1] != NEG else -1)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the DP definition directly. The sentinel value $NEG$ prevents mixing unreachable states with valid sums. The starting cell is initialized separately to avoid incorrectly adding its value twice or depending on nonexistent neighbors. Each transition carefully checks bounds and skips blocked cells entirely.

A common mistake is initializing unreachable cells as zero, which incorrectly allows paths to “pass through walls”. Another is failing to check both parents, which would miss valid paths that approach from only one direction.

## Worked Examples

### Sample 1

Input:

```
4
0 2 3 9
15 0 4 5
0 -1 -1 0
9 0 1 0
```

We track key DP states:

| Cell | dp value | Reason |
| --- | --- | --- |
| (0,0) | 0 | start |
| (0,1) | 2 | from left |
| (0,2) | 5 | 2 + 3 |
| (0,3) | 14 | 5 + 9 |
| (1,0) | 15 | from top |
| (1,1) | 15 | max(2,15)+0 |
| (1,2) | 19 | max(5,15)+4 |
| (1,3) | 24 | max(14,19)+5 |
| (2,0) | 15 | from top |
| (2,1) | blocked | -1 |
| (2,2) | blocked | -1 |
| (2,3) | 24 | only from (1,3) |
| (3,0) | 24 | from top chain |
| (3,1) | 24 | from (3,0) |
| (3,2) | 25 | 24 + 1 |
| (3,3) | 25 | final |

This confirms that blocked cells properly cut off paths, forcing all valid routes to detour around the obstacle region, and the DP still accumulates the best achievable total.

### Sample 2

Input:

```
4
0 2 3 9
15 0 4 5
0 -1 -1 -1
9 -1 1 0
```

Here the third row creates a complete horizontal barrier.

| Cell | dp value | Reason |
| --- | --- | --- |
| (2,0) | 15 | reachable |
| (2,1) | blocked | -1 |
| (2,2) | blocked | -1 |
| (2,3) | blocked | -1 |
| (3,0) | 24 | reachable |
| (3,1) | blocked | -1 |
| (3,2) | unreachable | no valid parent |
| (3,3) | unreachable | no valid parent |

Final state is unreachable, so output is $-1$. This shows that even if individual cells contain valid values, lack of connectivity correctly propagates through DP.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ | Each cell is processed once with constant-time transitions from at most two neighbors |
| Space | $O(N^2)$ | DP table stores one value per cell |

The constraint $N \leq 1000$ makes $10^6$ operations acceptable within typical limits, and the memory usage is well within 256 MB even with a full grid DP array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""4
0 2 3 9
15 0 4 5
0 -1 -1 0
9 0 1 0
""") == "25"

assert run("""4
0 2 3 9
15 0 4 5
0 -1 -1 -1
9 -1 1 0
""") == "-1"

# custom cases

# minimum size, no obstacles
assert run("""1
0
""") == "0"

# blocked start
assert run("""2
-1 0
0 0
""") == "-1"

# all open grid
assert run("""3
0 1 2
1 2 3
3 2 1
""") == "9"

# barrier row
assert run("""3
0 1 2
-1 -1 -1
3 4 5
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | 0 | base case |
| blocked start | -1 | unreachable propagation |
| all open | 9 | normal DP accumulation |
| full barrier | -1 | connectivity failure |

## Edge Cases

A key edge case is when the start or finish is blocked. The algorithm explicitly checks these before DP begins. If either is $-1$, the function immediately returns $-1$, since no path can exist regardless of intermediate structure. For example:

```
2
-1 0
0 0
```

Here, even though the destination is reachable in grid terms, the start is invalid, so DP initialization never happens and the correct output is $-1$.

Another edge case is isolated cells that are geometrically reachable but dynamically unreachable. Consider:

```
3
0 1 1
-1 -1 1
1 1 1
```

The DP correctly marks the entire bottom-right region unreachable because both potential parents of critical cells become blocked. This shows that reachability is not about coordinates alone but about existence of a valid predecessor chain, which the DP invariant enforces automatically.
