---
title: "CF 1520C - Not Adjacent Matrix"
description: "We are asked to fill an $n times n$ square grid with the numbers from $1$ to $n^2$ such that no two horizontally or vertically neighboring cells contain consecutive integers. In other words, the difference between numbers in adjacent cells cannot be exactly one."
date: "2026-06-10T18:04:40+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1520
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 719 (Div. 3)"
rating: 1000
weight: 1520
solve_time_s: 138
verified: true
draft: false
---

[CF 1520C - Not Adjacent Matrix](https://codeforces.com/problemset/problem/1520/C)

**Rating:** 1000  
**Tags:** constructive algorithms  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to fill an $n \times n$ square grid with the numbers from $1$ to $n^2$ such that no two horizontally or vertically neighboring cells contain consecutive integers. In other words, the difference between numbers in adjacent cells cannot be exactly one. The input consists of multiple test cases, each providing a single integer $n$, and the output is either a valid matrix for that size or $-1$ if no solution exists.

The constraints are fairly small: $n$ ranges from 1 to 100, and there can be up to 100 test cases. This means we can afford solutions with complexity roughly $O(n^2)$ per test case, since $100 \cdot 100^2 = 10^6$ operations is acceptable within a 4-second time limit.

Some edge cases are immediately apparent. For $n = 1$, the solution is trivial: a single cell with the number 1. For $n = 2$, however, no arrangement exists. Any placement of 1 through 4 will force at least one pair of consecutive numbers to share an edge. For larger $n$, the challenge is arranging the numbers to avoid adjacency of consecutive integers, and naive filling row by row will fail because consecutive numbers will inevitably be neighbors.

## Approaches

A brute-force approach would attempt to generate all permutations of $1$ to $n^2$ and check each one for adjacency violations. While this is correct in principle, it is completely infeasible: for $n = 5$, there are $25!$ permutations, which is astronomically large.

The key observation is that we can avoid consecutive numbers being adjacent by separating them into two sets: the odd numbers and the even numbers. If we fill the grid first with all odd numbers and then with all even numbers, the difference between any two consecutive numbers (which are always one apart) is never adjacent horizontally or vertically. This works for all $n \ge 3$. The arrangement within these subsets can follow a simple top-to-bottom, left-to-right pattern.

This idea drastically reduces complexity: instead of checking permutations, we systematically place numbers in order by parity. The only exceptions are $n = 2$, which cannot be solved, and $n = 1$, which is trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n^2)!) | O(n^2) | Too slow |
| Odd-Even Placement | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$. If $n = 2$, output $-1$ immediately because no solution exists. If $n = 1$, output a single cell containing 1.
2. Initialize an empty $n \times n$ grid.
3. Generate two lists: one with all odd numbers from 1 to $n^2$ and one with all even numbers from 1 to $n^2$.
4. Concatenate the odd list with the even list to form the final sequence. This ensures consecutive numbers never appear consecutively in the grid.
5. Fill the grid row by row, left to right, using the concatenated sequence. Maintain a pointer to track the next number to place.
6. Output the completed grid.

Why it works: the key invariant is that every pair of consecutive integers is separated into different sets, and we fill the grid sequentially. By placing all odd numbers first, no two numbers with a difference of 1 can end up in adjacent cells horizontally or vertically. This simple ordering solves the adjacency constraint for all $n \ge 3$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def not_adjacent_matrix(n):
    if n == 2:
        return -1
    if n == 1:
        return [[1]]
    
    grid = [[0] * n for _ in range(n)]
    odds = [i for i in range(1, n*n + 1) if i % 2 == 1]
    evens = [i for i in range(1, n*n + 1) if i % 2 == 0]
    sequence = odds + evens
    
    idx = 0
    for r in range(n):
        for c in range(n):
            grid[r][c] = sequence[idx]
            idx += 1
    return grid

t = int(input())
for _ in range(t):
    n = int(input())
    result = not_adjacent_matrix(n)
    if result == -1:
        print(-1)
    else:
        for row in result:
            print(' '.join(map(str, row)))
```

The code handles fast input using `sys.stdin.readline`. The `not_adjacent_matrix` function first checks for the unsolvable $n = 2$ and trivial $n = 1$ cases. It constructs odd and even lists and concatenates them, then fills the grid row by row. The use of a simple index `idx` ensures we sequentially place numbers without mistakes. Using list comprehensions guarantees correctness and avoids off-by-one errors.

## Worked Examples

For input `n = 3`, the odd numbers are `[1, 3, 5, 7, 9]` and the even numbers `[2, 4, 6, 8]`. Concatenated: `[1, 3, 5, 7, 9, 2, 4, 6, 8]`. Filling row by row produces:

| r/c | 0 | 1 | 2 |
| --- | --- | --- | --- |
| 0 | 1 | 3 | 5 |
| 1 | 7 | 9 | 2 |
| 2 | 4 | 6 | 8 |

No horizontal or vertical neighbor differs by 1.

For input `n = 2`, we immediately return `-1` because any placement of 1-4 will have a neighboring pair with difference 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Filling the grid and generating odd/even lists are O(n^2) |
| Space | O(n^2) | Storing the grid and the odd/even sequences |

With $n \le 100$, the algorithm performs at most 10,000 operations per test case, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
```
