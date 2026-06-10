---
title: "CF 1451F - Nullify The Matrix"
description: "The problem describes a two-player game played on an $n times m$ matrix of non-negative integers. Players alternate moves, starting with Ashish."
date: "2026-06-11T03:35:31+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "games"]
categories: ["algorithms"]
codeforces_contest: 1451
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 685 (Div. 2)"
rating: 2700
weight: 1451
solve_time_s: 266
verified: true
draft: false
---

[CF 1451F - Nullify The Matrix](https://codeforces.com/problemset/problem/1451/F)

**Rating:** 2700  
**Tags:** constructive algorithms, games  
**Solve time:** 4m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a two-player game played on an $n \times m$ matrix of non-negative integers. Players alternate moves, starting with Ashish. On each move, a player selects a starting cell with a non-zero value, chooses an ending cell that is not above or to the left of the starting cell, decreases the starting cell by some positive integer, and may adjust values along a shortest path from the start to the end. The game ends when all cells are zero, and the player who cannot make a move loses.

Given the initial matrix, the task is to predict the winner assuming both play optimally. The input consists of multiple test cases, each with the matrix dimensions and the initial matrix values.

Constraints are modest: $n, m \le 100$ and $a_{i,j} \le 10^6$, with up to 10 test cases. This allows algorithms with quadratic time in the matrix size, roughly up to $10^6$ operations, to run comfortably within the time limit.

The non-obvious aspect is that, although the moves allow complex path manipulations, the game can be reduced to a simpler strategy. Naively simulating every possible move would be infeasible because the branching factor is enormous. Edge cases include matrices with all zeros, single-row or single-column matrices, and matrices where only one cell is non-zero. These edge cases require careful reasoning about whether the first player can move.

## Approaches

A brute-force approach would attempt to simulate all possible moves, adjusting paths and values at each turn. This is correct in principle, but the number of move sequences grows combinatorially with the matrix size and cell values, making it intractable.

The key insight is that the game is equivalent to a classic impartial game on a bipartite graph, specifically a variant of a two-dimensional nim game. Each move effectively "removes" one row and one column (since a non-zero cell is chosen, and the minimal path affects a rectangle). The winner can be determined by counting the number of rows and columns that contain at least one non-zero element. If the minimum of these counts is odd, the first player can force a win by always targeting a cell in that minimal set; if it is even, the second player can mirror moves to win.

This reduction drastically simplifies the problem from simulating moves to counting non-zero rows and columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^(n*m)) | O(n*m) | Too slow |
| Optimal Counting | O(n*m) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the dimensions $n$ and $m$ and the matrix.
2. Count the number of rows that contain at least one non-zero element. This can be done by iterating over each row and checking for any non-zero cell.
3. Count the number of columns that contain at least one non-zero element. This can be done by iterating over each column and checking for any non-zero cell.
4. Compute the minimum of the non-zero row count and the non-zero column count. This value represents the maximum number of moves possible where each move can target a unique row and column intersection.
5. If this minimum value is odd, Ashish, as the first player, can force a win. Otherwise, Jeel, the second player, can win by mirroring Ashish's moves.
6. Output "Ashish" if Ashish wins, or "Jeel" otherwise.

Why it works: Each move in the game effectively removes one active row and one active column. The player who can make the last such move wins. By counting active rows and columns, we reduce the game to a nim-like scenario with a single pile of size equal to the minimal count. This guarantees correctness without simulating all possible paths.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        matrix = [list(map(int, input().split())) for _ in range(n)]
        
        # count non-zero rows
        rows = sum(1 for row in matrix if any(cell != 0 for cell in row))
        # count non-zero columns
        cols = sum(1 for c in range(m) if any(matrix[r][c] != 0 for r in range(n)))
        
        min_count = min(rows, cols)
        print("Ashish" if min_count % 2 == 1 else "Jeel")

if __name__ == "__main__":
    solve()
```

Each part of the code corresponds directly to the algorithm steps. Counting non-zero rows and columns is straightforward but requires careful iteration to avoid off-by-one errors. Taking the minimum ensures we capture the limiting factor for available moves. The parity check directly translates to determining the winner.

## Worked Examples

For the second sample input:

```
1 3
0 0 5
```

| Variable | Value |
| --- | --- |
| rows with non-zero | 1 |
| columns with non-zero | 1 |
| min(rows, cols) | 1 |
| winner | Ashish |

This shows that the first player can make the only available move and win.

For the third sample input:

```
2 2
0 1
1 0
```

| Variable | Value |
| --- | --- |
| rows with non-zero | 2 |
| columns with non-zero | 2 |
| min(rows, cols) | 2 |
| winner | Jeel |

This demonstrates that the first player cannot win if the minimal count is even, and the second player can mirror the moves to win.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) | Each cell is visited twice: once for row check, once for column check |
| Space | O(n*m) | Storing the input matrix |

The solution is well within the limits, as n and m are at most 100, and t ≤ 10, giving at most 100_100_10 = 100,000 operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("4\n1 1\n0\n1 3\n0 0 5\n2 2\n0 1\n1 0\n3 3\n1 2 3\n4 5 6\n7 8 9\n") == "Jeel\nAshish\nJeel\nAshish"

# custom cases
assert run("1\n1 1\n1\n") == "Ashish", "single non-zero cell"
assert run("1\n2 2\n0 0\n0 0\n") == "Jeel", "all zeros"
assert run("1\n3 3\n1 0 0\n0 1 0\n0 0 1\n") == "Ashish", "diagonal ones"
assert run("1\n2 3\n1 0 0\n0 0 1\n") == "Jeel", "minimum count even"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 with 1 | Ashish | first player can move and win |
| 2x2 all zeros | Jeel | no moves available |
| 3x3 diagonal | Ashish | odd minimal count gives first player win |
| 2x3 | Jeel | minimal count even gives second player win |

## Edge Cases

For a matrix where only one row or one column has non-zero values, the algorithm correctly identifies the minimal count as 1. For example, a 1x5 matrix `[0,0,0,0,7]` has one non-zero row and one non-zero column. The minimum is 1, so Ashish wins by removing the last non-zero cell. This illustrates that the algorithm properly handles sparse matrices. Similarly, for a fully zero matrix, both counts are zero, the minimum is zero, and the second player wins because the first cannot make any moves.
