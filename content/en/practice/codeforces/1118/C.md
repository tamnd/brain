---
title: "CF 1118C - Palindromic Matrix"
description: "We are asked to arrange n^2 integers into an n x n square matrix so that the matrix is palindromic along both axes. A palindromic matrix does not change when we reverse the order of rows or reverse the order of columns."
date: "2026-06-12T04:32:44+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1118
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 540 (Div. 3)"
rating: 1700
weight: 1118
solve_time_s: 86
verified: false
draft: false
---

[CF 1118C - Palindromic Matrix](https://codeforces.com/problemset/problem/1118/C)

**Rating:** 1700  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to arrange `n^2` integers into an `n x n` square matrix so that the matrix is palindromic along both axes. A palindromic matrix does not change when we reverse the order of rows or reverse the order of columns. Another way to see it is that each cell `(i, j)` must mirror its symmetric counterparts `(n-i-1, j)`, `(i, n-j-1)`, and `(n-i-1, n-j-1)`. For example, the four corners of the matrix all have to contain the same number. The same principle applies recursively for the inner layers.

The input gives us the size `n` and a list of `n^2` numbers to place. We need to either construct such a matrix using each number exactly once or report impossibility. Since `n` is at most 20, the total number of cells is at most 400. This is small enough for an approach that checks combinations of numbers into positions by frequency, as brute-force enumeration of all permutations (which would be `400!`) is clearly infeasible.

The non-obvious edge cases arise when `n` is odd. In an odd-sized matrix, there is a single center cell and `2n-2` cells along the middle row and middle column that only need to be mirrored once, not four times. If these positions cannot be filled with numbers that appear in the required multiples, a naive implementation that only checks for quadruples will fail. For instance, for `n = 3`, the center cell can take any number that appears at least once, while the four corners need numbers appearing at least four times.

## Approaches

A brute-force approach would try every permutation of the `n^2` numbers and test if the resulting matrix is palindromic. This works for very small `n`, but the number of permutations grows factorially and becomes infeasible even for `n = 5`, which would be `25!` permutations.

The key insight is to exploit symmetry. Every position in the matrix belongs to a group of either four, two, or one cells that must all contain the same number. Specifically, for even `n`, all positions form groups of four cells, so each number must appear in multiples of four. For odd `n`, the center cell is a singleton, positions on the central row or column excluding the center form pairs, and the remaining positions form quadruples. This observation reduces the problem to counting frequencies of numbers and fitting them into groups of size 4, 2, or 1, which is computationally trivial for `n ≤ 20`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n^2)!) | O(n^2) | Too slow |
| Frequency Grouping | O(n^2) | O(1000) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of each number in the input array. This lets us know how many quadruples, pairs, and singletons we can form from each number.
2. Initialize an `n x n` matrix filled with zeros. We will fill it layer by layer from outermost to innermost.
3. If `n` is even, all cells belong to quadruple groups. Iterate over the top-left quadrant and assign numbers that appear at least four times to each 2x2 square of the quadrant. After placing a number, decrement its frequency by four. If no number has at least four left when needed, output "NO".
4. If `n` is odd, first handle the outer layers exactly as in the even case. Then handle the central row and central column (excluding the center cell) using numbers with at least two remaining copies. Assign one number to the mirrored pair and decrement its count by two.
5. Finally, handle the single center cell, which can be filled by any number with at least one remaining count.
6. Output "YES" and the completed matrix.

**Why it works:** At every stage, the algorithm ensures that the frequency of numbers can satisfy the symmetry requirements of their positions. Quadruple groups guarantee corner symmetries, pair groups guarantee middle row/column symmetries, and the singleton guarantees the center. If at any stage the required group cannot be formed, it is impossible to construct a palindromic matrix.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

n = int(input())
a = list(map(int, input().split()))
freq = Counter(a)
matrix = [[0]*n for _ in range(n)]

def place_quad(i, j):
    for num in list(freq):
        if freq[num] >= 4:
            matrix[i][j] = matrix[i][n-j-1] = matrix[n-i-1][j] = matrix[n-i-1][n-j-1] = num
            freq[num] -= 4
            if freq[num] == 0:
                del freq[num]
            return True
    return False

def place_pair(i, j, mirrored_i, mirrored_j):
    for num in list(freq):
        if freq[num] >= 2:
            matrix[i][j] = matrix[mirrored_i][mirrored_j] = num
            freq[num] -= 2
            if freq[num] == 0:
                del freq[num]
            return True
    return False

# Fill quadruples
for i in range(n//2):
    for j in range(n//2):
        if not place_quad(i, j):
            print("NO")
            sys.exit()

# Fill middle row/column if n is odd
if n % 2 == 1:
    mid = n//2
    for i in range(n//2):
        if not place_pair(mid, i, mid, n-i-1):
            print("NO")
            sys.exit()
    for i in range(n//2):
        if not place_pair(i, mid, n-i-1, mid):
            print("NO")
            sys.exit()
    # Fill center
    for num in list(freq):
        if freq[num] >= 1:
            matrix[mid][mid] = num
            freq[num] -= 1
            if freq[num] == 0:
                del freq[num]
            break
    else:
        print("NO")
        sys.exit()

print("YES")
for row in matrix:
    print(' '.join(map(str,row)))
```

The solution first counts number frequencies, which makes it easy to know which numbers can fill quadruples or pairs. The `place_quad` and `place_pair` functions directly handle symmetry by filling the mirrored positions. For odd `n`, careful handling of the middle row, middle column, and center ensures that all symmetry conditions are satisfied.

## Worked Examples

**Sample 1**

Input: `4 1 8 8 1 2 2 2 2 2 2 2 2 1 8 8 1`

| Step | Action | Matrix |
| --- | --- | --- |
| 1 | Fill top-left 2x2 quadrants with numbers with freq ≥ 4 | [[1,2,2,1],[8,2,2,8],[8,2,2,8],[1,2,2,1]] |

Matrix is filled; output "YES". This confirms quadruples are enough for even `n`.

**Odd n example**

Input: `3 1 1 1 1 2 2 2 2 3`

| Step | Action | Matrix |
| --- | --- | --- |
| 1 | Fill corners (quadruples) | [[1,2,1],[2,0,2],[1,2,1]] |
| 2 | Fill center | [[1,2,1],[2,3,2],[1,2,1]] |

Confirms algorithm handles odd `n` with a single center correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each matrix cell is filled once, and frequency check is O(1) per number |
| Space | O(n^2 + U) | O(n^2) for the matrix, O(U) for Counter of unique numbers (U ≤ 1000) |

Since n ≤ 20, n^2 ≤ 400, the algorithm easily runs within 2 seconds and 256 MB memory.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("4\n1 8 8 1 2 2 2 2 2 2 2 2 1 8 8 1\n") == "YES\n1 2 2 1\n8 2 2 8\n8 2 2 8\n1 2 2 1", "sample 1"

# Minimum size n=1
assert run("1\n5\n") == "YES\n5", "min size"

# Maximum size n=20, all equal numbers
all_equal = " ".join(["1"]*400)
assert run(f"20\n{all_equal}\n").startswith("YES"), "max size equal numbers"

# Odd n, impossible
assert run("3\n1 1 2 2 3 3 4 4 5\n") == "NO", "odd impossible"

# Odd n, exact frequencies
assert run("3\n1 1 1 1
```
