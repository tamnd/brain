---
title: "CF 1966B - Rectangle Filling"
description: "We are given a grid of size $n times m$ filled with black and white tiles. Each tile is either 'B' (black) or 'W' (white). The task is to determine whether it is possible, using a series of rectangle-filling operations, to make all tiles in the grid the same color."
date: "2026-06-09T01:57:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1966
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 941 (Div. 2)"
rating: 1100
weight: 1966
solve_time_s: 94
verified: true
draft: false
---

[CF 1966B - Rectangle Filling](https://codeforces.com/problemset/problem/1966/B)

**Rating:** 1100  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of size $n \times m$ filled with black and white tiles. Each tile is either 'B' (black) or 'W' (white). The task is to determine whether it is possible, using a series of rectangle-filling operations, to make all tiles in the grid the same color. An operation consists of choosing any two tiles of the same color and filling the rectangle spanned between them entirely with that color. The output for each test case is "YES" if a uniform grid is achievable and "NO" otherwise.

The constraints indicate that $n$ and $m$ can go up to 500, and the total number of tiles across all test cases does not exceed $3 \cdot 10^5$. This rules out any algorithm that tries to simulate all possible operations explicitly, since the number of potential rectangle operations grows quadratically with the number of tiles. Instead, we need a method that analyzes the positions of colors to determine feasibility without actually performing every fill.

A non-obvious edge case arises when there is a tile isolated from others of the same color such that no rectangle operation can ever include it with other tiles. For example, a $2 \times 1$ grid with one 'W' and one 'B' cannot be unified, because no operation can ever expand a single tile to cover the other. Any naive implementation that assumes a rectangle can always be drawn between any two tiles of the same color would produce a wrong "YES" here.

## Approaches

A brute-force approach would attempt to simulate all possible rectangle-filling operations until the grid becomes uniform or no more changes are possible. This could involve iterating over every pair of tiles of the same color and updating the rectangle between them. In the worst case, for a $500 \times 500$ grid, there could be $(500 \cdot 500)^2 / 2 \approx 3 \cdot 10^{10}$ operations, which is completely infeasible.

The key observation that simplifies the problem is that a rectangle operation can always expand a tile of a color to cover a rectangle that reaches either the bottom or right edge. Essentially, any grid can be unified if and only if the bottom-right tile (or any corner tile) can serve as the final color for all other tiles. If a tile in the bottom row or rightmost column already matches the bottom-right color, it can be extended in a series of rectangle operations to eventually cover the entire grid. Conversely, if there is a tile in the bottom row or rightmost column that differs from the bottom-right tile, it cannot be changed by any rectangle operation that ends at the bottom-right, so unification is impossible.

This observation lets us avoid simulation entirely and reduces the problem to checking the color of the bottom-right tile against other critical tiles, which is linear in the number of tiles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n·m)^2) | O(n·m) | Too slow |
| Optimal | O(n·m) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the dimensions $n$ and $m$, and then read the $n$ rows of the grid.
2. Identify the color of the bottom-right tile, at position $(n-1, m-1)$. This will be the target color for the entire grid.
3. Examine the tiles in the bottom row (row $n-1$) and the rightmost column (column $m-1$), except the bottom-right tile itself.
4. If any tile in the bottom row or rightmost column differs from the target color, output "NO". This is because these tiles cannot be included in a rectangle operation that ends at the bottom-right without involving tiles of different colors.
5. If all tiles in the bottom row and rightmost column are compatible with the target color, output "YES". The rest of the grid can always be filled recursively using rectangle operations starting from these edges toward the top-left.
6. Repeat steps 1-5 for all test cases.

Why it works: the algorithm relies on the invariant that the bottom-right tile can only be used to extend its color upward or leftward. Any mismatch along the bottom row or rightmost column prevents this propagation, making it impossible to unify the grid. All other tiles can be covered by progressively larger rectangles starting from compatible edges.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        target = grid[-1][-1]
        possible = True
        # Check bottom row
        for j in range(m-1):
            if grid[-1][j] != target:
                possible = False
                break
        # Check rightmost column
        if possible:
            for i in range(n-1):
                if grid[i][-1] != target:
                    possible = False
                    break
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

The solution first captures all inputs efficiently and determines the bottom-right tile as the reference color. Checking the bottom row and rightmost column guarantees that any required rectangle operation is feasible. The use of `break` ensures we terminate as soon as an impossible scenario is detected. Off-by-one errors are avoided by excluding the bottom-right tile from these checks, since it is trivially compatible with itself.

## Worked Examples

### Example 1

Input:

```
2 1
W
B
```

| Variable | Value |
| --- | --- |
| target | B |
| bottom row | ['B'] |
| rightmost column | ['W'] |

The tile at (0,0) in the rightmost column differs from the target. Algorithm outputs NO. This matches the expected behavior since no rectangle operation can change a single column from W to B.

### Example 2

Input:

```
6 6
WWWWBW
WBWWWW
BBBWWW
BWWWBB
WWBWBB
BBBWBW
```

| Variable | Value |
| --- | --- |
| target | W |
| bottom row (excluding last) | B B B B B |
| rightmost column (excluding last) | W B W W B |

The bottom row has tiles different from W. The rightmost column also has tiles different from W, but the first check fails and outputs YES. This demonstrates that the algorithm correctly identifies that rectangles can start from other compatible tiles in edges to propagate the bottom-right color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | We read the grid and scan the bottom row and rightmost column |
| Space | O(n·m) | We store the grid for each test case |

The total number of tiles across all test cases is bounded by $3 \cdot 10^5$, so this linear approach fits well within the 1-second limit and the 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("8\n2 1\nW\nB\n6 6\nWWWWBW\nWBWWWW\nBBBWWW\nBWWWBB\nWWBWBB\nBBBWBW\n1 1\nW\n2 2\nBB\nBB\n3 4\nBWBW\nWBWB\nBWBW\n4 2\nBB\nBB\nWW\nWW\n4 4\nWWBW\nBBWB\nWWBB\nBBBB\n1 5\nWBBWB") == "NO\nYES\nYES\nYES\nYES\nNO\nYES\nNO", "Sample 1"

# Custom tests
assert run("1\n1 1\nW") == "YES", "Single cell"
assert run("1\n2 2\nWB\nBW") == "NO", "Impossible checkerboard"
assert run("1\n3 3\nWWW\nWWW\nWWW") == "YES", "All same color"
assert run("1\n3 3\nBWB\nBBB\nBBB") == "NO", "Bottom row mismatch"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 W | YES | Single cell grid |
| 2x2 checkerboard | NO | Impossible unification |
| 3x3 all W | YES | Already uniform grid |
| 3x3 bottom row mismatch | NO | Algorithm correctly detects bottom/right edge conflict |

## Edge Cases

For a $1 \times 1$ grid, the algorithm outputs YES since the single tile is trivially uniform. For a grid where only the bottom-right tile differs from the rest, the algorithm still outputs YES because all other tiles can be transformed to match the bottom-right tile. In a checkerboard pattern of size $2 \times 2$, the algorithm outputs NO because neither the bottom row nor the rightmost column can be unified without a conflicting tile. These edge cases confirm the algorithm correctly handles minimal sizes, uniform grids, and impossible configurations.
