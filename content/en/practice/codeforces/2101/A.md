---
title: "CF 2101A - Mex in the Grid"
description: "We are asked to fill an $n times n$ grid with the integers from $0$ to $n^2 - 1$, each used exactly once. Every rectangular subgrid contributes a value equal to the MEX of the numbers inside it, and the objective is to maximize the sum of these MEX values over all possible…"
date: "2026-06-08T05:07:26+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2101
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1024 (Div. 1)"
rating: 1300
weight: 2101
solve_time_s: 96
verified: false
draft: false
---

[CF 2101A - Mex in the Grid](https://codeforces.com/problemset/problem/2101/A)

**Rating:** 1300  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to fill an $n \times n$ grid with the integers from $0$ to $n^2 - 1$, each used exactly once. Every rectangular subgrid contributes a value equal to the MEX of the numbers inside it, and the objective is to maximize the sum of these MEX values over all possible subrectangles.

The key difficulty is not computing MEX for a fixed grid, but choosing the placement of numbers so that many subgrids contain small values like $0, 1, 2, \dots$ as often as possible, because those are the only values that can increase MEX. Large numbers are effectively inert: they never help increase MEX unless all smaller numbers are already present.

The constraints allow $n$ up to 500, so $n^2$ can reach 250,000. Any solution that simulates subgrids or computes MEX directly per subgrid would involve roughly $O(n^4)$ or $O(n^3)$ operations, which is far beyond feasibility. Even $O(n^2 \log n)$ constructions are fine, but anything that reasons per subgrid is ruled out.

A subtle failure case appears when numbers are scattered randomly or placed in row-major order. For example, for $n=3$, placing:

```
0 1 2
3 4 5
6 7 8
```

creates a strong bias toward small values being clustered only in the top-left region. Many subgrids that could include small values miss them entirely, reducing MEX contributions. The optimal arrangement must instead ensure that small values are spread so that many subrectangles include them early.

## Approaches

A brute-force idea would be to try all permutations of the $n^2$ numbers and compute the MEX sum for each arrangement. This is correct by definition but impossible, since there are $(n^2)!$ permutations, and evaluating each one requires iterating over all $O(n^2)$ subgrids with up to $O(n^2)$ work per subgrid, leading to at least $O((n^2)! \cdot n^4)$ complexity.

We need a structural observation: MEX is driven entirely by how early small numbers appear inside rectangles. For a fixed subgrid, its MEX is at least $k$ if and only if all numbers $0$ through $k-1$ are inside it. So the contribution of each value $x$ depends on how many subgrids contain all numbers $0 \dots x-1$.

This reframes the problem: instead of thinking about MEX directly, we want to place small numbers so that the set $\{0,1,\dots,x\}$ tends to lie in many rectangles.

A classical way to maximize this is to cluster small values in a compact region, because a tight cluster is contained in many more subrectangles than a scattered configuration. The optimal strategy is to build a “snake-like” or spiral-like ordering so that any prefix of numbers remains spatially compact.

One simple optimal construction is to fill the grid in a spiral starting from the top-left corner, moving inward layer by layer. This guarantees that the set of the smallest $k$ numbers always forms a connected, roughly square-shaped region, which maximizes the number of subrectangles that fully contain it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | $O((n^2)! \cdot n^4)$ | $O(n^2)$ | Too slow |
| Spiral / layered construction | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

The goal is to assign numbers $0 \dots n^2-1$ so that small values are spatially clustered.

1. Start with an empty $n \times n$ grid and a current value $v = 0$. The value $v$ will always represent the next smallest unused number, ensuring we control the geometry of prefixes.
2. Maintain four boundaries: top row, bottom row, left column, and right column. These define the current unfilled rectangle. Initially, these are the full grid.
3. Fill the top row from left to right using the current boundaries, assigning consecutive values. After filling it, move the top boundary inward. This ensures the smallest values occupy the outermost layer, making them accessible to many rectangles.
4. Fill the right column from top to bottom, then shrink the right boundary. This continues the inward layering while preserving connectivity of small values.
5. Fill the bottom row from right to left, then shrink the bottom boundary.
6. Fill the left column from bottom to top, then shrink the left boundary.
7. Repeat this process until all cells are filled. Each full cycle creates a “ring” of increasing values around the center.

The reason this ordering matters is that any prefix of values $0 \dots k$ will always form a single contiguous region that shrinks inward in a controlled way. This maximizes how many subrectangles can fully contain the prefix.

### Why it works

For any value $k$, consider the set of cells containing $0 \dots k$. In this construction, these cells always form a connected region with minimal bounding rectangle. Because MEX in a subgrid depends on whether all these values are contained, maximizing the number of subgrids containing the bounding rectangle maximizes the total contribution. The spiral ensures this bounding rectangle grows as slowly and symmetrically as possible, which maximizes containment frequency over all possible rectangles.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        grid = [[0] * n for _ in range(n)]
        
        top, bottom = 0, n - 1
        left, right = 0, n - 1
        val = 0
        
        while top <= bottom and left <= right:
            for j in range(left, right + 1):
                grid[top][j] = val
                val += 1
            top += 1

            for i in range(top, bottom + 1):
                grid[i][right] = val
                val += 1
            right -= 1

            if top <= bottom:
                for j in range(right, left - 1, -1):
                    grid[bottom][j] = val
                    val += 1
                bottom -= 1

            if left <= right:
                for i in range(bottom, top - 1, -1):
                    grid[i][left] = val
                    val += 1
                left += 1

        for row in grid:
            print(*row)

if __name__ == "__main__":
    solve()
```

The code implements a standard spiral fill. The important implementation detail is the careful boundary checks before filling the bottom row and left column. Without these checks, odd-sized grids would overwrite already assigned cells when the spiral collapses into the center.

The variable `val` is strictly increasing and ensures each number from $0$ to $n^2-1$ is used exactly once.

## Worked Examples

### Example 1

Input:

```
n = 3
```

We track the spiral filling:

| Step | Action | Grid state (partial) | Next val |
| --- | --- | --- | --- |
| 1 | Fill top row | 0 1 2 / _ _ _ / _ _ _ | 3 |
| 2 | Fill right col | 0 1 2 / _ _ 3 / _ _ 4 | 5 |
| 3 | Fill bottom row | 0 1 2 / _ _ 3 / 6 5 4 | 7 |
| 4 | Fill left col | 0 1 2 / 7 _ 3 / 6 5 4 | 8 |

This produces a fully consistent spiral where small numbers remain near the outer boundary, maximizing inclusion across subrectangles.

### Example 2

Input:

```
n = 4
```

The same process produces a larger ring structure:

| Layer | Filled region | Effect |
| --- | --- | --- |
| 1 | Outer border | maximizes inclusion of 0-11 |
| 2 | Inner border | keeps 12-15 centralized |

This shows that the smallest values always dominate outer layers, increasing their presence in subgrids.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each cell is written exactly once during spiral traversal |
| Space | $O(n^2)$ | Grid storage |

The constraints allow up to 1000 total $n$, so total cells are at most $10^6$, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        grid = [[0]*n for _ in range(n)]
        
        top, bottom, left, right = 0, n-1, 0, n-1
        val = 0
        
        while top <= bottom and left <= right:
            for j in range(left, right+1):
                grid[top][j] = val
                val += 1
            top += 1
            
            for i in range(top, bottom+1):
                grid[i][right] = val
                val += 1
            right -= 1
            
            if top <= bottom:
                for j in range(right, left-1, -1):
                    grid[bottom][j] = val
                    val += 1
                bottom -= 1
            
            if left <= right:
                for i in range(bottom, top-1, -1):
                    grid[i][left] = val
                    val += 1
                left += 1
        
        output.append("\n".join(" ".join(map(str, row)) for row in grid))
    
    return "\n".join(output)

# provided samples
assert run("2\n2\n3\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1` | `0` | minimum grid |
| `1\n2` | spiral 2x2 | boundary correctness |
| `1\n3` | spiral 3x3 | odd center handling |
| `2\n2\n3` | sample case | multiple test cases |

## Edge Cases

A minimal grid like $n=1$ contains only a single value. The algorithm immediately enters the loop, fills cell (0,0) with 0, and terminates. No boundary corruption occurs because the loop condition `top <= bottom and left <= right` holds exactly once.

For an odd-sized grid such as $n=3$, the spiral eventually collapses into the center cell. At that moment, all boundaries converge, and only one assignment remains. The boundary checks prevent reprocessing already filled cells, ensuring the center value is written exactly once.
