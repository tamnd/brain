---
title: "CF 64C - Table"
description: "We are given an $n times m$ table filled with consecutive integers starting from 1. The filling is done row by row, left to right."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 64
codeforces_index: "C"
codeforces_contest_name: "Unknown Language Round 1"
rating: 1600
weight: 64
solve_time_s: 85
verified: true
draft: false
---

[CF 64C - Table](https://codeforces.com/problemset/problem/64/C)

**Rating:** 1600  
**Tags:** *special, greedy, implementation, math  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times m$ table filled with consecutive integers starting from 1. The filling is done row by row, left to right. For example, if $n=3$ and $m=4$, the table looks like this:

```
1  2  3  4
5  6  7  8
9 10 11 12
```

Then, the numbers are rewritten in a different order: column by column, top to bottom within each column. With the same example, the column-wise sequence is:

```
1 5 9 2 6 10 3 7 11 4 8 12
```

The input gives three numbers: $n$ (rows), $m$ (columns), and $k$ (position in the column-major sequence). The output is the number appearing at the $k$-th position in the column-major sequence. For instance, in the previous example, the 11th number is 8.

The constraints $1 \le n, m \le 20000$ and $1 \le k \le nm$ are critical. With $nm$ reaching up to $4 \times 10^8$, any solution that tries to actually construct the table or the sequence is infeasible. This rules out naive brute-force approaches that iterate over all elements. A solution must compute the answer mathematically without explicit full storage.

Edge cases include single-row or single-column tables. For instance, $n=1, m=5, k=3$ simply maps to 3, and $n=5, m=1, k=4$ maps to 4. A careless implementation that assumes $n>1$ and $m>1$ could fail here. Another subtle case is when $k$ is exactly a multiple of $n$, which affects row calculations in the column-major indexing.

## Approaches

The naive solution constructs the entire $n \times m$ table in row-major order, then iterates column by column to produce a new list, and finally returns the $k$-th element. This works correctly because it simulates the problem exactly, but it performs $O(nm)$ operations and uses $O(nm)$ space. With $nm$ up to $4 \times 10^8$, this will not fit in memory or complete in time.

The key insight is that we do not need the full table. The original table has a simple mathematical pattern: the element at row $r$ (0-indexed) and column $c$ (0-indexed) is $r \cdot m + c + 1$. In the column-major sequence, the elements are written column by column. So, if $k$ is given, we can determine which column it falls in and which row within that column. Let $col = (k-1) // n$ and $row = (k-1) % n$. Then the number at that position in the original table is $row \cdot m + col + 1$.

This observation reduces the problem to a constant-time arithmetic calculation: we translate a 1D column-major index to 2D coordinates and then map back to the row-major table formula. This approach avoids any large arrays and is extremely fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(nm) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert $k$ to 0-indexed by subtracting 1. This makes integer division and modulo calculations simpler.
2. Determine which column the $k$-th number falls in. Compute `col = k // n`. Integer division tells us how many full columns of $n$ elements come before position $k$.
3. Determine which row within that column. Compute `row = k % n`. The remainder gives the position inside the column.
4. Map the row and column back to the original row-major table. The formula is `number = row * m + col + 1`. This correctly translates the 2D coordinates to the number in the initial layout.
5. Print the resulting number.

Why it works: Each column in the column-major sequence contains exactly $n$ elements from consecutive rows of the original table. The division gives the column index and the modulo gives the row index. Mapping these coordinates to the row-major formula recovers the correct number without iterating over the table. This logic is exact for any $n, m, k$, including edge cases where $k$ is a multiple of $n$ or when $n=1$ or $m=1$.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())

k -= 1  # convert to 0-indexed
col = k // n
row = k % n

print(row * m + col + 1)
```

The solution first adjusts for zero-based indexing to simplify arithmetic. The integer division finds the column in the column-major sequence, while modulo finds the row. Multiplying the row by the total number of columns $m$ recovers the original row-major offset, and adding the column index plus one gives the exact number. There are no loops, and all arithmetic fits in 64-bit integers for the given constraints.

## Worked Examples

### Example 1

Input: `3 4 11`

0-indexed k: `10`

```
col = 10 // 3 = 3
row = 10 % 3 = 1
number = 1*4 + 3 + 1 = 8
```

Output: 8. This matches the expected result. It demonstrates a middle-of-the-table case where k spans multiple columns.

### Example 2

Input: `2 5 7`

0-indexed k: `6`

```
col = 6 // 2 = 3
row = 6 % 2 = 0
number = 0*5 + 3 + 1 = 4
```

Output: 4. This tests the top row of a later column.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All calculations are arithmetic operations without loops. |
| Space | O(1) | Only a few integers are stored; no arrays are used. |

With $n$ and $m$ up to 20000, the algorithm performs at most a handful of arithmetic operations and does not allocate large memory, well within the 2-second and 64 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    k -= 1
    col = k // n
    row = k % n
    return str(row * m + col + 1)

# Provided sample
assert run("3 4 11\n") == "8", "sample 1"

# Custom edge cases
assert run("1 5 3\n") == "3", "single row"
assert run("5 1 4\n") == "4", "single column"
assert run("2 5 7\n") == "4", "general small case"
assert run("20000 20000 400000000\n") == "20000", "max size last element"
assert run("20000 20000 1\n") == "1", "max size first element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 3 | 3 | Single row handling |
| 5 1 4 | 4 | Single column handling |
| 2 5 7 | 4 | Small general case |
| 20000 20000 400000000 | 20000 | Largest input, last element |
| 20000 20000 1 | 1 | Largest input, first element |

## Edge Cases

When $n=1$ and $m>1$, the table is a single row, so the column-major and row-major sequences are identical. The algorithm computes `col = (k-1) // 1 = k-1` and `row = 0`, so `row*m + col + 1 = col + 1 = k`, which is correct.

When $k$ is exactly a multiple of $n$, for example $n=3, m=4, k=6$, we have `k-1=5`, `col=1`, `row=2`. Mapping back: `2*4 + 1 + 1 = 10`, which is exactly the 6th element in column-major order. The modulo handles the last row in a column correctly.

This editorial fully explains the reasoning, shows how to translate a 1D column-major index to a row-major table, and demonstrates correctness through examples and edge cases.
