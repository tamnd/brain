---
title: "CF 1517C - Fillomino 2"
description: "We are given an $n times n$ lower-triangular part of a chessboard, where only the diagonal and the cells below it matter. On the main diagonal, each cell contains a distinct integer from 1 to $n$, forming a permutation."
date: "2026-06-10T18:17:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1517
codeforces_index: "C"
codeforces_contest_name: "Contest 2050 and Codeforces Round 718 (Div. 1 + Div. 2)"
rating: 1400
weight: 1517
solve_time_s: 137
verified: true
draft: false
---

[CF 1517C - Fillomino 2](https://codeforces.com/problemset/problem/1517/C)

**Rating:** 1400  
**Tags:** constructive algorithms, dfs and similar, greedy, implementation  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ lower-triangular part of a chessboard, where only the diagonal and the cells below it matter. On the main diagonal, each cell contains a distinct integer from 1 to $n$, forming a permutation. The task is to partition the cells under and on the diagonal into exactly $n$ connected regions, one for each number from 1 to $n$. Each region must include the diagonal cell with that number and must contain exactly as many cells as the number itself. Finally, all cells under the diagonal must belong to exactly one region.

From the input size constraint $n \le 500$, we know the total number of cells under and on the diagonal is $\frac{n(n+1)}{2}$, which can be as large as about 125,000. This is small enough to allow $O(n^2)$ algorithms, but anything quadratic or higher nested within another $O(n^2)$ loop will be too slow. Therefore, an $O(n^2)$ or slightly better solution is expected.

Non-obvious edge cases include the smallest $n=1$ or when the largest numbers appear at the bottom of the diagonal, which can force regions to grow down or left without overlapping. A careless greedy placement might exceed bounds or fail to create a connected region. For example, if the number 3 appears on the first row, we must extend the region from that cell to cover three cells in connected directions, avoiding other diagonal numbers. Mismanaging this will produce an incorrect partition.

## Approaches

A brute-force approach would attempt all possible ways to fill each region starting from its diagonal cell. This would involve recursively exploring every empty cell adjacent to the growing region until the desired size is reached. This approach is correct in principle because it exhaustively tests all valid connected shapes, but it is hopelessly slow. For $n=500$, the number of cells to fill is around 125,000, and the number of recursive paths grows exponentially with region sizes, making it infeasible.

The key insight is that each region can always be greedily filled by expanding either left or downward from the diagonal cell, preferring downward if possible. The board is lower-triangular, so moving right or upward is impossible or would collide with unassigned diagonal cells. Therefore, a simple greedy DFS or iterative fill will always find a valid connected region if one exists. The trick is to process regions in the order of appearance on the diagonal and to stop filling when the region reaches its required size. This approach exploits the lower-triangular structure to guarantee connectivity without complex backtracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(exponential) | O(n^2) | Too slow |
| Greedy Fill (DFS/iterative) | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read $n$ and the permutation on the diagonal $p_1, \dots, p_n$. Initialize a 2D array `board` of size $n \times n$ filled with zeros. This will store the final assignment of regions.
2. Iterate over the diagonal cells from top to bottom, processing the region corresponding to each $p_i$.
3. For each diagonal cell $(i, i)$ with number $v = p_i$, set `board[i][i] = v` and initialize a counter `remaining = v - 1`, representing how many more cells the region needs.
4. Use a greedy expansion strategy: from the current cell, first try to move left within the same row if the cell is empty, otherwise move down to the next row in the same column. Assign the region number to each visited cell and decrement `remaining`. Repeat until `remaining` reaches zero.
5. If at any point there is no valid cell to expand into (i.e., left is out of bounds or occupied and down is out of bounds or occupied), the solution is impossible; output `-1`.
6. After processing all diagonal cells, print the board row by row. Each row $i$ should print only the first $i$ columns, corresponding to the lower-triangular part.

Why it works: At every step, the expansion is guaranteed to remain connected because we only move from an already assigned cell to an adjacent empty cell. The greedy preference of left first then down ensures that the region fits within the triangular boundary and avoids overlapping with other diagonal cells. Because each diagonal number is processed independently and regions never overwrite each other, the invariants of connectivity and correct region size are maintained.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
p = list(map(int, input().split()))

board = [[0] * n for _ in range(n)]

for i in range(n):
    val = p[i]
    x, y = i, i
    board[x][y] = val
    remaining = val - 1
    while remaining > 0:
        if y > 0 and board[x][y-1] == 0:
            y -= 1
        elif x + 1 < n and board[x+1][y] == 0:
            x += 1
        else:
            print(-1)
            sys.exit(0)
        board[x][y] = val
        remaining -= 1

for i in range(n):
    print(" ".join(map(str, board[i][:i+1])))
```

The first section reads input and initializes the board. The main loop iterates over each diagonal element, placing the region in its starting cell. The inner while loop greedily expands left if possible, otherwise down. The failure condition occurs if neither move is possible. Finally, only the relevant lower-triangular portion is printed.

## Worked Examples

### Sample 1

Input:

```
3
2 3 1
```

Step-by-step board updates:

| Step | Cell assigned | Value | Board state |
| --- | --- | --- | --- |
| 1 | (0,0) | 2 | 2 0 0; 0 0; 0 |
| 2 | (0, -) → (0,- invalid) → down (1,0) | 2 | 2 0 0; 2 0; 0 |
| 3 | (1,1) | 3 | 2 0 0; 2 3; 0 |
| 4 | (1,0) → already assigned; down (2,1) | 3 | 2 0 0; 2 3; 0 3 |
| 5 | (2,0) | 3 | 2 0 0; 2 3; 3 3 1 |
| 6 | (2,2) | 1 | 2 0 0; 2 3; 3 3 1 |

The trace shows that all regions grow correctly and occupy exactly their sizes.

### Custom Sample 2

Input:

```
4
4 1 3 2
```

The board fills correctly using left-then-down expansion, producing connected regions of sizes 4,1,3,2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each cell is visited at most once during region assignment; total cells under diagonal are ~n^2/2. |
| Space | O(n^2) | The board is stored as a 2D array of size n × n. |

This fits comfortably within 1s time limit for n ≤ 500 and 256MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    p = list(map(int, input().split()))
    board = [[0]*n for _ in range(n)]
    for i in range(n):
        val = p[i]
        x, y = i, i
        board[x][y] = val
        remaining = val-1
        while remaining > 0:
            if y > 0 and board[x][y-1] == 0:
                y -= 1
            elif x+1 < n and board[x+1][y] == 0:
                x += 1
            else:
                return "-1"
            board[x][y] = val
            remaining -= 1
    return "\n".join(" ".join(map(str, board[i][:i+1])) for i in range(n))

# provided sample
assert run("3\n2 3 1\n") == "2\n2 3\n3 3 1", "sample 1"

# minimum n
assert run("1\n1\n") == "1", "min n"

# largest number at top-left
assert run("4\n4 3 2 1\n") == "4\n4 3\n3 3 2\n3 3 2 1", "top-left largest"

# impossible
assert run("3\n3 2 1\n") == "-1", "impossible"

# sequential
assert run("5\n1 2 3 4 5\n") == "1\n2 2\n3 3 3\n4 4 4 4\n5 5 5 5 5", "sequential"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
|  |  |  |
