---
title: "CF 1676D - X-Sum"
description: "We are given a two-dimensional grid representing a chessboard where each cell contains a non-negative integer. A bishop can be placed on any cell, and it attacks all cells along the four diagonals that intersect at its position. The cell the bishop occupies counts as attacked."
date: "2026-06-10T00:59:24+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1676
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 790 (Div. 4)"
rating: 1000
weight: 1676
solve_time_s: 107
verified: true
draft: false
---

[CF 1676D - X-Sum](https://codeforces.com/problemset/problem/1676/D)

**Rating:** 1000  
**Tags:** brute force, greedy, implementation  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a two-dimensional grid representing a chessboard where each cell contains a non-negative integer. A bishop can be placed on any cell, and it attacks all cells along the four diagonals that intersect at its position. The cell the bishop occupies counts as attacked. Our task is to find the maximum sum of values from the cells that a bishop can attack, considering all possible placements on the board.

The input specifies multiple test cases, each with its own board dimensions and values. The constraints tell us that the board can be as large as 200 by 200, and the sum of all cells across all test cases is capped at 40,000. This implies that while a simple solution that examines each cell individually might work for a single test case, a naive nested iteration over diagonals for every cell will be too slow for larger boards and multiple test cases.

Edge cases include boards with only one row or column, where the bishop can attack very few cells, and boards where all values are zero except a single large value. A careless approach that miscounts diagonals or double-counts the central cell could fail in these situations. For example, a 2x2 board with values `[[1, 2], [3, 4]]` has the bishop placed at (1,1) achieving a sum of 1+4=5 if counting only the two diagonal cells correctly, but a naive summation might double-count or miss some cells.

## Approaches

A brute-force approach would involve iterating over every cell on the board, then iterating along all four diagonals to sum the attacked values. This works because each bishop’s attack region is predictable, but it becomes too slow for the largest boards. For a single 200x200 board, each cell could take O(n+m) to sum diagonals, leading to O(n_m_(n+m)) = O(200_200_400) = 16,000,000 operations per test case, which is near the upper edge of feasibility and slow for multiple test cases.

The key observation is that cells lying on the same diagonal share a property: either the difference `(row - col)` or the sum `(row + col)` is constant. The top-left to bottom-right diagonals are identified by `row - col`, and the top-right to bottom-left diagonals are identified by `row + col`. If we precompute the sum of each diagonal, the sum of all cells attacked by a bishop at position `(i,j)` is simply the sum of its `row-col` diagonal plus the sum of its `row+col` diagonal, minus the value at `(i,j)` (to avoid double-counting the cell itself). Precomputing these diagonals reduces the per-cell calculation to O(1), giving a total complexity of O(n*m) per board, which is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n_m_(n+m)) | O(1) | Too slow for large boards |
| Optimal | O(n*m) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Initialize two dictionaries to hold the sum of values along diagonals. One dictionary maps `row - col` to the sum of values along that diagonal, and the other maps `row + col` to the sum of values along that diagonal.
2. Iterate over every cell `(i,j)` in the board. Add its value to the corresponding `row - col` diagonal sum and the `row + col` diagonal sum. This step aggregates the contributions from all cells to their diagonals in a single pass.
3. After computing the diagonal sums, iterate again over every cell `(i,j)` and calculate the sum of cells attacked by placing the bishop at `(i,j)` as the sum of its `row - col` diagonal plus the sum of its `row + col` diagonal, minus the cell’s own value to avoid double-counting.
4. Track the maximum sum encountered during this iteration. After examining all cells, the maximum sum is the answer for that test case.

Why it works: The algorithm guarantees correctness because each diagonal sum contains exactly all values on that diagonal. By combining the two diagonals passing through a cell and subtracting the central cell once, we precisely account for every cell the bishop attacks, without missing or double-counting any value.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]
    
    diag1 = {}
    diag2 = {}
    
    for i in range(n):
        for j in range(m):
            d1 = i - j
            d2 = i + j
            diag1[d1] = diag1.get(d1, 0) + a[i][j]
            diag2[d2] = diag2.get(d2, 0) + a[i][j]
    
    max_sum = 0
    for i in range(n):
        for j in range(m):
            total = diag1[i - j] + diag2[i + j] - a[i][j]
            if total > max_sum:
                max_sum = total
    
    print(max_sum)
```

The first loop builds the diagonal sums. Using dictionaries ensures we handle negative indices from `row-col` diagonals without errors. The second loop computes the bishop attack sum efficiently for every cell using these precomputed sums. Subtracting `a[i][j]` avoids double-counting the cell itself, a subtle point that is easy to overlook.

## Worked Examples

### Sample 1

Board:

```
1 2 2 1
2 4 2 4
2 2 3 1
2 4 2 4
```

Key diagonal sums:

| Diagonal (i-j) | Sum |
| --- | --- |
| -3 | 1 |
| -2 | 2+2=4 |
| -1 | 2+2+4=8 |
| 0 | 1+4+3+4=12 |
| 1 | 2+2+2=6 |
| 2 | 2+4=6 |
| 3 | 1+4=5 |

| Diagonal (i+j) | Sum |
| --- | --- |
| 0 | 1 |
| 1 | 2+2=4 |
| 2 | 2+4+2=8 |
| 3 | 1+2+3+1=7 |
| 4 | 4+2+2=8 |
| 5 | 4+4=8 |
| 6 | 4 |

Bishop at `(1,1)` has `diag1[0]=12` and `diag2[2]=8`, minus `4` for double-counted cell, giving total 16. The maximum occurs at `(1,2)` or `(3,1)` with sum 20.

### Sample 2

Board:

```
1
0
```

Only one cell, the bishop sum is 1. The algorithm correctly computes `diag1[0]=1`, `diag2[0]=1`, minus `1`, total 1.

These traces show that diagonal sums aggregate correctly, and subtracting the cell value avoids double-counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) | Two full iterations over the board: first to compute diagonal sums, second to compute maximum attack sum |
| Space | O(n+m) | Storing sums for up to n+m diagonals in two dictionaries |

The solution handles the sum of all cells up to 40,000 easily. Even with 1,000 test cases, each small board completes quickly due to the linear per-cell processing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution starts here
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]
        
        diag1 = {}
        diag2 = {}
        for i in range(n):
            for j in range(m):
                diag1[i - j] = diag1.get(i - j, 0) + a[i][j]
                diag2[i + j] = diag2.get(i + j, 0) + a[i][j]
        
        max_sum = 0
        for i in range(n):
            for j in range(m):
                total = diag1[i - j] + diag2[i + j] - a[i][j]
                if total > max_sum:
                    max_sum = total
        print(max_sum)
    return output.getvalue().strip()

# Provided samples
assert run("4\n4 4\n1 2 2 1\n2 4 2 4\n2 2 3 1\n2 4 2 4\n2 1\n1\n0\n3 3\n1 1 1\n1 1 1\n1 1 1\n3 3\n0 1 1\n1 0 1\n1 1 0\n") == "20\n1\n5\n3", "sample 1"

# Custom cases
assert run("1\n1 1\n100\n") == "100", "single cell"
assert run("1\n2 2\n
```
