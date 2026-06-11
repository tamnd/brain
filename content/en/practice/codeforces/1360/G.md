---
title: "CF 1360G - A/B Matrix"
description: "We are asked to construct a binary matrix with given dimensions where each row contains exactly a certain number of ones, and each column also contains exactly a certain number of ones. The input gives the number of rows and columns, and the counts of ones per row and per column."
date: "2026-06-11T13:03:37+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1360
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 644 (Div. 3)"
rating: 1900
weight: 1360
solve_time_s: 779
verified: false
draft: false
---

[CF 1360G - A/B Matrix](https://codeforces.com/problemset/problem/1360/G)

**Rating:** 1900  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 12m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a binary matrix with given dimensions where each row contains exactly a certain number of ones, and each column also contains exactly a certain number of ones. The input gives the number of rows and columns, and the counts of ones per row and per column. The output is either a matrix that satisfies these constraints or an indication that it is impossible.

The constraints are small: $n$ and $m$ are up to 50, so we can afford algorithms that are quadratic in $n$ and $m$. Each test case can be handled independently, and the number of test cases is up to 1000, but even in the worst case this results in a manageable total number of operations, around a few million.

A non-obvious edge case is when the total number of ones implied by the row counts does not match the total number of ones implied by the column counts. For instance, if $n = 2$, $m = 3$, $a = 2$, and $b = 1$, then the total ones by rows is $2 \cdot 2 = 4$, but the total ones by columns is $3 \cdot 1 = 3$. In such a situation, it is impossible to construct a matrix, and a naive approach that tries to fill rows or columns greedily might produce a matrix with row sums correct but column sums wrong.

Another tricky case arises when the ones must be distributed cyclically. For example, if the ones per row and column are both greater than 1, a simple left-to-right fill may overfill some columns while leaving others empty. The construction must ensure that every column ends up with exactly the required number of ones without violating row counts.

## Approaches

The brute-force approach is to try all ways to place ones in each row until the column sums match the required values. For $n \cdot m$ up to 2500, the number of subsets per row is exponential, $O(\binom{m}{a})$, which becomes infeasible even for moderate $a$ and $m$. Checking all arrangements would exceed any reasonable time limit.

The key insight is that the problem is entirely combinatorial and regular: the only requirement is that each row has $a$ ones, each column has $b$ ones, and the totals match. If the total ones implied by rows equals that implied by columns ($n \cdot a = m \cdot b$), a solution exists. Once we know a solution exists, we can construct it systematically by shifting the ones across columns in each row. We can start the first row with ones in the first $a$ positions, then shift the pattern to the right by $a$ positions for each subsequent row, wrapping around when exceeding the number of columns. This ensures uniform distribution and guarantees each column ends up with exactly $b$ ones. The cyclic shift leverages the regularity of the counts and avoids the combinatorial explosion of the naive approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O($\binom{m}{a}^n$) | O(n*m) | Too slow |
| Optimal | O(n*m) | O(n*m) | Accepted |

## Algorithm Walkthrough

1. First, check if a solution is possible by verifying that the total number of ones implied by rows equals the total number of ones implied by columns, i.e., $n \cdot a = m \cdot b$. If not, print "NO" for that test case.
2. If a solution exists, initialize an empty matrix of size $n \times m$ filled with zeros. This sets up a workspace to place ones systematically.
3. For the first row, place ones in the first $a$ columns. This satisfies the row sum for the first row.
4. For each subsequent row, shift the positions of ones from the previous row to the right by $a$ positions modulo $m$. This ensures the cyclic distribution of ones across columns. For example, if the previous row had ones in columns 0 and 1 for $a = 2$ and $m = 6$, the next row will have ones in columns 2 and 3.
5. Continue this process for all $n$ rows. Because the total ones match the total columns and the shift is consistent, each column will receive exactly $b$ ones at the end.
6. After filling all rows, print "YES" followed by the matrix.

Why it works: the invariant is that the pattern of ones is shifted uniformly across rows. Since the total ones are balanced ($n \cdot a = m \cdot b$), the cyclic placement guarantees that no column is overfilled or underfilled. The modulo operation ensures wrapping around the columns, maintaining the correct counts throughout.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, a, b = map(int, input().split())
    if n * a != m * b:
        print("NO")
        continue
    print("YES")
    matrix = [[0]*m for _ in range(n)]
    shift = 0
    for i in range(n):
        for j in range(a):
            col = (shift + j) % m
            matrix[i][col] = 1
        shift = (shift + a) % m
    for row in matrix:
        print("".join(map(str, row)))
```

The solution first checks feasibility by comparing total ones for rows and columns. The matrix is built row by row, using a shift variable to determine which columns to place ones in. The modulo operation guarantees wrapping around without exceeding column bounds. Finally, the matrix is printed as requested, with each row joined as a string of digits.

## Worked Examples

Consider the first sample input: $n = 3$, $m = 6$, $a = 2$, $b = 1$. The total ones for rows is $3 \cdot 2 = 6$, which matches the total for columns $6 \cdot 1 = 6$. Start with the first row placing ones at columns 0 and 1. The next row shifts two positions to columns 2 and 3. The third row shifts again to columns 4 and 5. Each row has two ones, each column has one one, satisfying all constraints.

| Row | Shift | Ones Columns |
| --- | --- | --- |
| 0 | 0 | 0,1 |
| 1 | 2 | 2,3 |
| 2 | 4 | 4,5 |

Another example: $n = 4$, $m = 4$, $a = 2$, $b = 2$. Total ones match. First row has ones at 0,1. Second row shifts by 2 to 2,3. Third row shifts by 2 to 0,1. Fourth row shifts by 2 to 2,3. Each row has 2 ones, each column has 2 ones.

| Row | Shift | Ones Columns |
| --- | --- | --- |
| 0 | 0 | 0,1 |
| 1 | 2 | 2,3 |
| 2 | 0 | 0,1 |
| 3 | 2 | 2,3 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) | Each of n rows is filled in O(a) ≤ O(m) steps. |
| Space | O(n*m) | We store the entire matrix explicitly. |

Given n and m up to 50 and t up to 1000, the total operations are under 3 million, well within the 2-second time limit. Memory usage is also negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    for _ in range(t):
        n, m, a, b = map(int, input().split())
        if n * a != m * b:
            out.append("NO")
            continue
        out.append("YES")
        matrix = [[0]*m for _ in range(n)]
        shift = 0
        for i in range(n):
            for j in range(a):
                col = (shift + j) % m
                matrix[i][col] = 1
            shift = (shift + a) % m
        for row in matrix:
            out.append("".join(map(str, row)))
    return "\n".join(out)

# provided sample
assert run("5\n3 6 2 1\n2 2 2 1\n2 2 2 2\n4 4 2 2\n2 1 1 2\n") == """YES
110000
001100
000011
NO
YES
11
11
YES
1100
1100
0011
0011
YES
1
1""", "sample 1"

# custom cases
assert run("1\n2 3 1 1\n") == "YES\n100\n010", "small balanced"
assert run("1\n3 3 2 2\n") == "YES\n110\n011\n101", "full matrix"
assert run("1\n2 3 2 2\n") == "NO", "impossible case"
assert
```
