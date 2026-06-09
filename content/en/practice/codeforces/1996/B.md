---
title: "CF 1996B - Scale"
description: "We are given a square grid of size $n times n$ where each cell contains either a zero or a one. The task is to reduce this grid by a factor $k$, which is guaranteed to divide $n$ evenly."
date: "2026-06-08T14:41:24+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1996
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 962 (Div. 3)"
rating: 800
weight: 1996
solve_time_s: 151
verified: true
draft: false
---

[CF 1996B - Scale](https://codeforces.com/problemset/problem/1996/B)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square grid of size $n \times n$ where each cell contains either a zero or a one. The task is to reduce this grid by a factor $k$, which is guaranteed to divide $n$ evenly. Reduction works by partitioning the grid into $k \times k$ non-overlapping blocks, where each block contains the same value, and replacing each block with a single cell representing that value. The output is the smaller grid of size $(n/k) \times (n/k)$ that results from this block compression.

Given the constraints, $n$ can be as large as 1000, but the sum of $n$ across all test cases is at most 1000. This implies that a straightforward iteration over all cells is acceptable, since we will not exceed about $10^6$ operations in total. The non-obvious edge cases arise when $k = 1$ or $k = n$. If $k = 1$, the reduced grid is the same as the original, so we must avoid inadvertently skipping any rows or columns. If $k = n$, the entire grid collapses into a single cell. A careless implementation might attempt to read indices beyond the grid bounds or mix up the block starting points in these cases.

## Approaches

The brute-force approach is simple: iterate over all blocks of size $k \times k$, pick any representative cell (for instance, the top-left cell), and place its value into the reduced grid. This works correctly because the problem guarantees all cells in a block are identical. The naive implementation would check each cell in each block, but that is unnecessary and redundant because of the guarantee.

The optimal approach leverages this guarantee by only reading one cell per block. This reduces work to $(n/k)^2$ operations per grid, which is trivial given the constraints. The observation that every $k \times k$ block is homogeneous allows us to skip iterating over all $k^2$ cells in the block, making the solution both simpler and faster.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Check all cells in each block | O(n^2) | O(n^2) | Accepted due to small total n |
| Check only top-left cell per block | O((n/k)^2) | O((n/k)^2) | Accepted, simpler and faster |

## Algorithm Walkthrough

1. Read the number of test cases $t$. Each test case consists of a grid size $n$, reduction factor $k$, and $n$ lines of $n$ characters each.
2. For each test case, determine the size of the reduced grid, which is $m = n/k$.
3. Initialize an empty list to store the reduced grid.
4. Iterate over each block row index $i$ from 0 to $m-1$. The corresponding original grid row is $i \cdot k$.
5. Within each block row, iterate over each block column index $j$ from 0 to $m-1$. The corresponding original grid column is $j \cdot k$.
6. Take the top-left cell of the $k \times k$ block at $(i \cdot k, j \cdot k)$ and append it to the current row of the reduced grid.
7. After processing all columns for the current block row, append the row to the reduced grid.
8. Print the reduced grid row by row.

Why it works: the guarantee that all cells in a $k \times k$ block are identical allows us to safely pick only the top-left cell. Iterating over block indices instead of individual cells ensures we cover all blocks exactly once without missing or duplicating any.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        m = n // k
        reduced = []
        for i in range(m):
            row = []
            for j in range(m):
                row.append(grid[i * k][j * k])
            reduced.append("".join(row))
        print("\n".join(reduced))

if __name__ == "__main__":
    solve()
```

The solution first reads the number of test cases and then processes each test case separately. The original grid is read fully into memory. The reduced grid is constructed by accessing the top-left cell of each $k \times k$ block. Each row of the reduced grid is joined into a string and printed sequentially. Using integer division ensures correct block indexing. This handles the edge cases $k=1$ and $k=n$ naturally because the loops adapt to the reduced size $m = n/k$.

## Worked Examples

Consider the input:

```
6 3
000111
000111
000111
111000
111000
111000
```

We have $n = 6, k = 3$, so $m = 2$. The reduced grid is constructed by taking the top-left of each $3 \times 3$ block:

| Block indices | Top-left cell | Reduced grid |
| --- | --- | --- |
| (0,0) | 0 | 0 |
| (0,1) | 1 | 01 |
| (1,0) | 1 | 10 |
| (1,1) | 0 | 10 |

The reduced grid is:

```
01
10
```

This demonstrates correct mapping from the original grid to the reduced one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 / k^2) per test case | We only iterate over block indices, reading one cell per block. |
| Space | O(n^2) | We store the original grid. Reduced grid is negligible by comparison. |

Given the constraint that the sum of $n$ across all test cases does not exceed 1000, the total number of operations is small and easily fits within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided sample
assert run("4\n4 4\n0000\n0000\n0000\n0000\n6 3\n000111\n000111\n000111\n111000\n111000\n111000\n6 2\n001100\n001100\n111111\n111111\n110000\n110000\n8 1\n11111111\n11111111\n11111111\n11111111\n11111111\n11111111\n11111111\n11111111\n") == "0\n01\n10\n010\n111\n100\n11111111\n11111111\n11111111\n11111111\n11111111\n11111111\n11111111\n11111111"

# Custom cases
assert run("1\n1 1\n1\n") == "1", "minimum size"
assert run("1\n4 2\n1111\n1111\n1111\n1111\n") == "11\n11", "all equal"
assert run("1\n4 4\n1010\n1010\n1010\n1010\n") == "1", "full collapse"
assert run("1\n4 1\n1010\n0101\n1010\n0101\n") == "1010\n0101\n1010\n0101", "k=1 identity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | Minimum size grid |
| 4 2 | 11\n11 | Homogeneous blocks |
| 4 4 | 1 | Full grid collapse to single cell |
| 4 1 | 1010\n0101\n1010\n0101 | k=1 identity mapping |

## Edge Cases

When $k = 1$, the algorithm iterates over each cell individually, effectively copying the original grid. For $k = n$, the reduced grid is a single cell. Both cases work without any special handling because the loop limits are computed as $m = n/k$, which becomes 1 in the collapse case and $n$ in the identity case. The choice to always read the top-left cell of each block safely leverages the guarantee of homogeneity, avoiding any off-by-one or index errors.
