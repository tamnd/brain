---
title: "CF 486B - OR in Matrix"
description: "We are given a matrix B of size m × n, where each element is either 0 or 1. This matrix was supposedly generated from some original matrix A of the same size using a specific rule: each element B[i][j] equals the logical OR of all elements in the i-th row of A combined with all…"
date: "2026-06-07T17:26:52+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "hashing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 486
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 277 (Div. 2)"
rating: 1300
weight: 486
solve_time_s: 92
verified: true
draft: false
---

[CF 486B - OR in Matrix](https://codeforces.com/problemset/problem/486/B)

**Rating:** 1300  
**Tags:** greedy, hashing, implementation  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a matrix `B` of size `m × n`, where each element is either 0 or 1. This matrix was supposedly generated from some original matrix `A` of the same size using a specific rule: each element `B[i][j]` equals the logical OR of all elements in the `i`-th row of `A` combined with all elements in the `j`-th column of `A`. Formally, `B[i][j] = (OR of row i in A) OR (OR of column j in A)`.

The task is to reconstruct any matrix `A` that could have produced `B`, or determine that no such matrix exists because `B` is inconsistent with the OR rule. The input size limits are modest (`m, n ≤ 100`), allowing solutions that run in roughly `O(m*n)` time.

A subtle edge case occurs when a zero appears in `B`. If `B[i][j]` is zero, it forces all elements in row `i` and column `j` of `A` to be zero. Any failure to enforce this produces a contradiction. A naive approach that tries to greedily fill ones wherever `B[i][j]` is one can fail if a zero somewhere else conflicts.

For example, consider:

```
2 2
1 0
0 0
```

Here `B[1][2] = 0` forces `A[1][2] = A[2][2] = 0`. Similarly, `B[2][1] = 0` forces `A[2][1] = A[2][2] = 0`. But `B[1][1] = 1` requires at least one 1 in row 1 or column 1. Any assignment of zeros that satisfies the zeros prevents placing a 1 for `B[1][1]`, so no solution exists. Detecting these contradictions is key.

## Approaches

The brute-force approach is to try all `2^(m*n)` possible assignments for `A` and check whether the resulting `B` matches the given one. This is theoretically correct but completely infeasible for `m = n = 100`, as it would involve up to `2^10000` combinations.

The key insight is that zeros in `B` strictly constrain elements in `A`: if `B[i][j] = 0`, all of row `i` and column `j` must be zero. Ones in `B` are more flexible, requiring at least one 1 in the union of row `i` and column `j`. Therefore, we can start by initializing `A` with ones everywhere, then explicitly zero out rows and columns corresponding to zeros in `B`. Finally, we verify whether all ones in `B` are still satisfied. This reduces the problem to a straightforward two-pass approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(m*n)) | O(m*n) | Too slow |
| Zero-propagation + verification | O(m*n) | O(m*n) | Accepted |

## Algorithm Walkthrough

1. Initialize a matrix `A` of size `m × n` filled with ones. This is an optimistic assumption that ones can satisfy all `B[i][j] = 1` constraints.
2. For each element `B[i][j]` equal to zero, set every element in row `i` and column `j` of `A` to zero. This enforces the strict requirement that a zero in `B` cannot arise if any element in the corresponding row or column of `A` is one.
3. Construct a new matrix `C` by computing `(OR of row i in A) OR (OR of column j in A)` for each element. This simulates the generation of `B` from the candidate `A`.
4. Compare `C` to the original `B`. If they match exactly, print "YES" and the matrix `A`. Otherwise, print "NO".

Why it works: step 2 guarantees that all zero entries in `B` are respected in `A`. Step 3 checks that all ones in `B` are achievable with the chosen zero placements. If a conflict arises, it will be detected during verification, ensuring correctness. The zero-propagation captures all hard constraints; any remaining ones can be arbitrarily placed to satisfy `B`.

## Python Solution

```python
import sys
input = sys.stdin.readline

m, n = map(int, input().split())
B = [list(map(int, input().split())) for _ in range(m)]

# Step 1: Initialize A with ones
A = [[1]*n for _ in range(m)]

# Step 2: Zero out rows and columns based on zeros in B
for i in range(m):
    for j in range(n):
        if B[i][j] == 0:
            for k in range(n):
                A[i][k] = 0
            for k in range(m):
                A[k][j] = 0

# Step 3: Verify by reconstructing B
C = [[0]*n for _ in range(m)]
row_or = [0]*m
col_or = [0]*n

for i in range(m):
    row_or[i] = 0
    for j in range(n):
        row_or[i] |= A[i][j]

for j in range(n):
    col_or[j] = 0
    for i in range(m):
        col_or[j] |= A[i][j]

valid = True
for i in range(m):
    for j in range(n):
        C[i][j] = row_or[i] | col_or[j]
        if C[i][j] != B[i][j]:
            valid = False
            break
    if not valid:
        break

if valid:
    print("YES")
    for row in A:
        print(' '.join(map(str, row)))
else:
    print("NO")
```

The code first constructs a candidate `A` by zeroing out rows and columns indicated by zeros in `B`. It then precomputes the OR of each row and column to rebuild `B`. If the rebuilt matrix matches, the candidate is valid; otherwise, it is rejected. Using precomputed row and column ORs avoids repeated computation for every element.

## Worked Examples

### Sample 1

Input:

```
2 2
1 0
0 0
```

| i | j | B[i][j] | Action on A |
| --- | --- | --- | --- |
| 0 | 0 | 1 | none initially |
| 0 | 1 | 0 | zero row 0 and col 1 |
| 1 | 0 | 0 | zero row 1 and col 0 |
| 1 | 1 | 0 | already zero |

Reconstructed matrix `C`:

```
0 0
0 0
```

Does not match `B`, so output is `NO`. This demonstrates detection of conflicting constraints.

### Sample 2

Input:

```
3 3
1 1 1
1 0 1
1 1 1
```

Step 2 zeroing:

- `B[1][1] = 0` → zero row 1 and column 1.

Candidate `A`:

```
1 0 1
0 0 0
1 0 1
```

Reconstruct `C`:

```
1 1 1
1 0 1
1 1 1
```

Matches `B`, so output is `YES` with candidate `A`. Confirms that ones can coexist with enforced zeros.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m*n) | Each zero triggers O(m+n) updates; reconstructing B requires O(m*n) operations. |
| Space | O(m*n) | Storing matrices A, B, C, plus row_or and col_or arrays. |

With `m, n ≤ 100`, `m*n ≤ 10000`, this fits comfortably in the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    m, n = map(int, input().split())
    B = [list(map(int, input().split())) for _ in range(m)]
    A = [[1]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if B[i][j] == 0:
                for k in range(n):
                    A[i][k] = 0
                for k in range(m):
                    A[k][j] = 0
    row_or = [0]*m
    col_or = [0]*n
    for i in range(m):
        for j in range(n):
            row_or[i] |= A[i][j]
    for j in range(n):
        for i in range(m):
            col_or[j] |= A[i][j]
    valid = True
    for i in range(m):
        for j in range(n):
            if (row_or[i]|col_or[j]) != B[i][j]:
                valid = False
                break
        if not valid:
            break
    if valid:
        print("YES")
        for row in A:
            print(' '.join(map(str, row)))
    else:
        print
```
