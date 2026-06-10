---
title: "CF 1475F - Unusual Matrix"
description: "We are given two square binary matrices of the same size, called a and b. Each element is either 0 or 1. The allowed operations are flipping an entire row or flipping an entire column, where flipping means XORing each element with 1."
date: "2026-06-11T00:10:34+07:00"
tags: ["codeforces", "competitive-programming", "2-sat", "brute-force", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1475
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 697 (Div. 3)"
rating: 1900
weight: 1475
solve_time_s: 123
verified: true
draft: false
---

[CF 1475F - Unusual Matrix](https://codeforces.com/problemset/problem/1475/F)

**Rating:** 1900  
**Tags:** 2-sat, brute force, constructive algorithms  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two square binary matrices of the same size, called `a` and `b`. Each element is either 0 or 1. The allowed operations are flipping an entire row or flipping an entire column, where flipping means XORing each element with 1. Our task is to determine whether it is possible to transform `a` into `b` using any sequence of these row and column flips.

The input specifies multiple test cases, each giving the size of the matrix and the two matrices themselves. The output should be "YES" if a sequence of flips exists to make the matrices equal, or "NO" otherwise.

The main constraint that drives the algorithm design is that `n` can be up to 1000, and the total sum of `n` across all test cases does not exceed 1000. This implies that an O(n^3) brute-force solution would be too slow, since 1000^3 = 10^9 operations. An O(n^2) approach is feasible because we are allowed to process matrices of total size up to roughly 10^6 elements in a few seconds.

A subtle edge case is when matrices are of size 1x1 or 2x2. For example, a single-element matrix can only be flipped once in its row and once in its column, so we must ensure that our solution accounts for parity correctly. Another tricky case is when rows and columns need alternating flips; a naive approach that flips everything greedily could produce an impossible intermediate state and incorrectly conclude "NO".

## Approaches

The most straightforward method would be to try all possible sequences of row and column flips, but there are 2^n possible flips for rows and 2^n for columns. Trying all combinations results in O(2^(2n) * n^2) operations, which is exponentially slow for n ≥ 20. This brute-force works in theory because each flip either changes a cell or does not, so every configuration is reachable, but it fails in practice for large matrices.

The key insight is to notice that the effect of row and column flips can be captured by considering the difference between `a` and `b`. For a particular cell (i, j), after some flips, its final value will be `a[i][j] XOR row_flip[i] XOR col_flip[j]`. This equation must equal `b[i][j]`. Equivalently, for each cell, we have:

```
row_flip[i] XOR col_flip[j] = a[i][j] XOR b[i][j]
```

If we choose the first row’s flips arbitrarily, the flips for the columns are uniquely determined. Then the flips for the remaining rows must satisfy the same XOR equations; if they do, the transformation is possible. This reduces the problem to checking consistency of a system of XOR equations, which can be done in O(n^2).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(2n) * n^2) | O(n^2) | Too slow |
| XOR Parity / Constructive | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute a new matrix `d` where `d[i][j] = a[i][j] XOR b[i][j]`. Each entry represents whether `a[i][j]` needs to be flipped an odd number of times to match `b[i][j]`. This converts the problem from matrix operations to a system of XOR constraints.
2. Decide arbitrarily on the flip of the first row, for instance, assume `row_flip[0] = 0`. Then, for each column `j`, the required column flip can be computed as `col_flip[j] = d[0][j] XOR row_flip[0]`.
3. For each remaining row `i > 0`, compute the required row flip by comparing the first column: `row_flip[i] = d[i][0] XOR col_flip[0]`. This ensures that the first column in each row matches the target.
4. Verify that all other entries satisfy the XOR condition: `row_flip[i] XOR col_flip[j] == d[i][j]`. If any cell violates this equation, the system is inconsistent and the answer is "NO".
5. If all cells satisfy the equations, the sequence of flips exists, and the answer is "YES".

Why it works: Once the flips for the first row and first column are chosen, the rest of the flips are determined. The XOR system guarantees that every cell is either consistent or not. This approach checks all consistency constraints without needing to try all sequences of flips explicitly. The arbitrary choice of `row_flip[0]` works because flipping the first row can always be combined with column flips; if a solution exists, it will be discovered under either choice of `row_flip[0]`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = [list(map(int, list(input().strip()))) for _ in range(n)]
        input()  # skip empty line
        b = [list(map(int, list(input().strip()))) for _ in range(n)]
        
        # compute difference matrix
        d = [[a[i][j] ^ b[i][j] for j in range(n)] for i in range(n)]
        
        # assume first row flip = 0
        row_flip = [0] * n
        col_flip = [d[0][j] for j in range(n)]
        
        possible = True
        for i in range(1, n):
            row_flip[i] = d[i][0] ^ col_flip[0]
            for j in range(1, n):
                if row_flip[i] ^ col_flip[j] != d[i][j]:
                    possible = False
                    break
            if not possible:
                break
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

The code first reads the matrices, computes their XOR difference, and initializes row and column flip arrays. It sets the first row to zero and derives column flips directly. Remaining rows are then checked against the XOR constraints. If any inconsistency is found, the answer is "NO"; otherwise, it is "YES". Skipping the empty line between matrices avoids misalignment in input reading. Using list comprehension ensures that the matrix differences are computed efficiently.

## Worked Examples

**Example 1**

Input:

```
3
3
110
001
110

000
000
000
```

| Step | d[i][j] | row_flip | col_flip | Check |
| --- | --- | --- | --- | --- |
| Initial | 110 ^ 000 = 110 | row_flip[0]=0 | col_flip=[1,1,0] | - |
| Row 1 | d[1][0]=0, col_flip[0]=1 => row_flip[1]=1 | row_flip=[0,1,?] | col_flip=[1,1,0] | check d[1][1]=0? row_flip^col_flip=1^1=0 , d[1][2]=1? row_flip^col_flip=1^0=1  |
| Row 2 | d[2][0]=1, col_flip[0]=1 => row_flip[2]=0 | row_flip=[0,1,0] | col_flip=[1,1,0] | check d[2][1]=1? 0^1=1 , d[2][2]=0? 0^0=0  |

All cells satisfy XOR condition, output "YES".

**Example 2**

Input:

```
2
01
11

10
10
```

| Step | d[i][j] | row_flip | col_flip | Check |
| --- | --- | --- | --- | --- |
| Initial | 01^10=11, 11^10=01 | row_flip[0]=0 | col_flip=[1,1] | Row 1 check: row_flip[1]=0^1=1, check d[1][1]=1^1=0? d[1][1]=1  |

Inconsistency detected, output "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each test case requires computing a difference matrix and verifying each cell once. |
| Space | O(n^2) | Storing `a`, `b`, and `d` matrices. Row and column flips use O(n) additional space. |

Given the sum of n across all test cases does not exceed 1000, the total number of operations is below 10^6, well within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("""3
3
110
001
110

000
000
000
3
101
010
101

010
101
010
2
01
11

10
10""") == "YES\nYES\nNO"

# Custom tests
# Minimum-size input
assert run("""1
1
0

1""") == "YES", "1x1, flip required"
assert run("""1
1
1

1""") == "YES", "1x1, no flip required"

#
```
