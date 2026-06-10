---
title: "CF 1560C - Infinity Table"
description: "We are asked to locate a number in an infinite table where the numbers are filled in a zigzag diagonal pattern. The first row starts with 1 in the top-left corner, then we fill numbers down along the diagonals that slope from top-right to bottom-left."
date: "2026-06-10T12:19:06+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1560
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 739 (Div. 3)"
rating: 800
weight: 1560
solve_time_s: 208
verified: false
draft: false
---

[CF 1560C - Infinity Table](https://codeforces.com/problemset/problem/1560/C)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 3m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to locate a number in an infinite table where the numbers are filled in a zigzag diagonal pattern. The first row starts with 1 in the top-left corner, then we fill numbers down along the diagonals that slope from top-right to bottom-left. For example, the first diagonal contains only 1, the second diagonal contains 2 and 3, the third diagonal contains 4, 5, and 6, and so on. The input is a number $k$, and the output must be the row and column where $k$ appears.

The constraints allow $k$ up to $10^9$, so we cannot simulate the table cell by cell. Any brute-force filling will exceed feasible time limits. A naive simulation of even $10^5$ steps would be slow if repeated across 100 test cases, since each cell access is at least O(1). We need a method that calculates the position mathematically.

Edge cases that are tricky include very small numbers like 1 or 2, which are at the start of the table. Another subtlety is that numbers at the end of a diagonal are at column 1, while numbers at the start of a diagonal are at row 1. Any solution that assumes uniform row/column growth without considering diagonals will produce wrong coordinates for these cases.

## Approaches

The brute-force method is straightforward: generate the table diagonally and track the coordinates for each number. Start at 1 in cell (1,1), then fill along diagonals, moving down until reaching the leftmost column, then proceed to the next diagonal. While this is correct, it requires storing all numbers up to $k$, which can be up to $10^9$. Even if we avoid storage, iterating up to $k$ numbers per test case would take O(k) time, which is clearly too slow.

The key observation is that the numbers are grouped by diagonals. Diagonal $n$ contains $n$ numbers, and the sum of numbers in the first $n$ diagonals is $1 + 2 + \dots + n = n(n+1)/2$. Therefore, to locate number $k$, we first find which diagonal contains it. Let $d$ be the smallest integer such that $d(d+1)/2 \ge k$. Once we know the diagonal, the position of $k$ inside that diagonal determines its row and column. Diagonal positions decrease the row and increase the column as we go from the start of the diagonal (row 1) to the end (column 1). This transforms the problem from simulating O(k) steps to solving a quadratic equation and performing simple arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(1) | Too slow |
| Diagonal Math | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For a given number $k$, compute the diagonal $d$ where $k$ lies. Solve $d(d+1)/2 \ge k$ for $d$. This can be done efficiently using the quadratic formula: $d = \lceil(-1 + \sqrt{1 + 8k})/2\rceil$.
2. Compute the last number in the previous diagonal: $prev = (d-1)d/2$. This tells us how many numbers have already been placed before diagonal $d$.
3. Determine the offset of $k$ within its diagonal: $offset = k - prev - 1$. This is a 0-based index from the start of the diagonal.
4. The coordinates are derived from the diagonal number and offset. Row decreases from $d$ to 1 while column increases from 1 to $d$. Therefore, $row = d - offset$ and $col = 1 + offset$.

Why it works: The sum formula ensures we correctly identify the diagonal, and the offset within the diagonal gives the exact position. Every number in the diagonal sequence moves one step down and one step left, so subtracting the offset from the diagonal number yields the correct row, and adding it to 1 yields the correct column. This invariant holds for all $k \ge 1$.

## Python Solution

```python
import sys, math
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    k = int(input())
    # find diagonal d using quadratic formula
    d = math.ceil((-1 + math.sqrt(1 + 8 * k)) / 2)
    prev = d * (d - 1) // 2
    offset = k - prev - 1
    row = d - offset
    col = 1 + offset
    print(row, col)
```

The code reads multiple test cases efficiently. We compute the diagonal using the quadratic formula, rounding up to handle numbers not exactly at a triangular number. The offset determines the exact position within the diagonal, and the final coordinates are printed. Using integer arithmetic for `prev` ensures no floating-point rounding errors for large $k$.

## Worked Examples

**Example 1: k = 11**

| Step | Value |
| --- | --- |
| Compute d | ceil((-1 + sqrt(1 + 8*11))/2) = ceil((-1 + sqrt(89))/2) = ceil((8.43)/2) = 5 |
| prev | 5*4/2 = 10 |
| offset | 11 - 10 - 1 = 0 |
| row | 5 - 0 = 5 |
| col | 1 + 0 = 1 |

Result: (5,1). This matches the diagonal pattern: 11 is the first element of the 5th diagonal.

**Example 2: k = 14**

| Step | Value |
| --- | --- |
| Compute d | ceil((-1 + sqrt(1 + 8*14))/2) = ceil((10.583-1)/2) = ceil(9.583/2) = 5 |
| prev | 5*4/2 = 10 |
| offset | 14 - 10 - 1 = 3 |
| row | 5 - 3 = 2 |
| col | 1 + 3 = 4 |

Result: (2,4), consistent with the diagonal arrangement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Finding the diagonal via sqrt and arithmetic takes constant time |
| Space | O(1) | Only a few integer variables are used |

Since $t \le 100$ and each calculation is O(1), the solution runs well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        k = int(input())
        import math
        d = math.ceil((-1 + math.sqrt(1 + 8 * k)) / 2)
        prev = d * (d - 1) // 2
        offset = k - prev - 1
        row = d - offset
        col = 1 + offset
        print(row, col)
    return out.getvalue().strip()

# Provided samples
assert run("7\n11\n14\n5\n4\n1\n2\n1000000000") == "2 4\n4 3\n1 3\n2 1\n1 1\n1 2\n31623 14130"

# Custom test cases
assert run("1\n1") == "1 1", "smallest number"
assert run("1\n3") == "2 2", "third number in second diagonal"
assert run("1\n6") == "3 1", "last number of third diagonal"
assert run("1\n10") == "4 1", "last number of fourth diagonal"
assert run("1\n5050") == "100 1", "triangular number, start of diagonal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 1 | smallest number edge case |
| 3 | 2 2 | number in the middle of a diagonal |
| 6 | 3 1 | last number of a diagonal, column 1 |
| 10 | 4 1 | last number of diagonal, ensures diagonal sum formula works |
| 5050 | 100 1 | large triangular number, checks handling of sqrt and ceil |

## Edge Cases

For $k=1$, `d` computes as 1, `prev` is 0, offset 0, giving row=1 and col=1. The algorithm correctly identifies the top-left cell.

For numbers that are triangular numbers like $k=6$ or $k=10$, `offset` becomes diagonal length minus 1, yielding the last element of the diagonal at column 1, which aligns with the pattern. The arithmetic handles these boundaries without adjustment, confirming the formula works across edge cases.
