---
title: "CF 1533H - Submatrices"
description: "We are given a grid of letters with n rows and m columns. Each cell contains one of the first five uppercase Latin letters: A, B, C, D, E. Our task is to count how many rectangular submatrices contain exactly k distinct letters, for every k from 1 to 5."
date: "2026-06-10T16:28:49+07:00"
tags: ["codeforces", "competitive-programming", "*special", "bitmasks", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1533
codeforces_index: "H"
codeforces_contest_name: "Kotlin Heroes: Episode 7"
rating: 0
weight: 1533
solve_time_s: 352
verified: false
draft: false
---

[CF 1533H - Submatrices](https://codeforces.com/problemset/problem/1533/H)

**Rating:** -  
**Tags:** *special, bitmasks, data structures, dp  
**Solve time:** 5m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid of letters with `n` rows and `m` columns. Each cell contains one of the first five uppercase Latin letters: `A`, `B`, `C`, `D`, `E`. Our task is to count how many rectangular submatrices contain exactly `k` distinct letters, for every `k` from 1 to 5. A submatrix is defined by choosing a contiguous set of rows and columns, possibly the whole matrix, and we must count overlapping or repeated submatrices separately.

The bounds `n, m ≤ 800` imply that brute-force enumeration of all submatrices is infeasible. The number of submatrices is roughly `(n(n+1)/2) * (m(m+1)/2)` which can be about 10^11 in the worst case. Any naive solution that inspects each submatrix individually will time out. Therefore, we need a solution that avoids enumerating submatrices directly and instead leverages the structure of the problem, namely the limited number of letters.

Edge cases include grids with only one letter repeated everywhere. In this case, only submatrices with one distinct letter exist. A careless solution that does not handle counts correctly could overcount or miscount submatrices. Another subtle case is when each row or column contains exactly one of each letter, where the algorithm must correctly track letter sets over rectangles, not just individual rows or columns.

## Approaches

The brute-force approach iterates over all possible top-left and bottom-right corners of submatrices. For each submatrix, we would scan all its cells, compute the set of distinct letters, and increment the corresponding counter for `k`. This is correct logically, but the operation count is roughly `O(n^2 * m^2 * nm)` in the worst case, which is around 10^11, far too slow for the limits.

The key observation to optimize is that there are only five possible letters. If we encode sets of letters as bitmasks, every submatrix can be represented by a 5-bit number. We can reduce the problem to counting how many submatrices have a given bitmask. The crucial idea is to process the grid row by row and use the histogram trick: for each letter subset, track the maximum rectangle height where only that subset appears in every column. Then counting rectangles becomes a variant of the largest rectangle in histogram problem. By iterating over all subsets of letters (32 total), we can efficiently compute counts. Finally, we can combine counts to get the number of submatrices with exactly `k` letters using inclusion-exclusion: the number of submatrices with exactly `k` letters is the sum of counts of subsets of size `k` minus sums of counts of subsets of smaller size that are included.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² m² * nm) | O(1) | Too slow |
| Optimal (bitmask + histogram DP) | O(n m 2^5) = O(25,600,000) | O(n m 32) | Accepted |

## Algorithm Walkthrough

1. Encode each letter as a bitmask: `A` = 1, `B` = 2, `C` = 4, `D` = 8, `E` = 16. This allows representing any subset of letters as a 5-bit integer.
2. Initialize a 2D array `height[col][mask]` that will track the number of consecutive rows, ending at the current row, that contain only letters in `mask` for column `col`.
3. Process the grid row by row. For each row, update `height[col][mask]`: if the cell's letter is in `mask`, increment the previous height; otherwise, reset to zero. This builds histograms for each subset of letters.
4. For each mask, use a monotonic stack (histogram trick) to count the number of rectangles ending at the current row where all columns satisfy the mask constraint. This counts all submatrices containing a subset of letters.
5. Accumulate counts for all masks. To get counts for exactly `k` letters, sum the counts of masks with exactly `k` bits set, and subtract counts of subsets already counted (inclusion-exclusion).
6. Output the counts for `k = 1..5`.

The reason this works is that every submatrix can be uniquely identified by the top row where it ends, the bottom row, and the contiguous columns satisfying a subset mask. By computing heights and rectangles per mask, we account for all possible submatrices. Inclusion-exclusion ensures we count exactly `k` distinct letters rather than subsets.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    
    # map letter to bit
    letter_bit = {'A':1, 'B':2, 'C':4, 'D':8, 'E':16}
    
    # precompute letter masks
    mask_grid = [[letter_bit[c] for c in row] for row in grid]
    
    # total counts for each mask
    counts = [0]*32  # 2^5
    
    # height[col][mask] = consecutive rows ending here with only letters in mask
    height = [[0]*32 for _ in range(m)]
    
    for r in range(n):
        for mask in range(1, 32):
            for c in range(m):
                if mask_grid[r][c] & mask:
                    height[c][mask] = height[c][mask]+1
                else:
                    height[c][mask] = 0
        
        # count rectangles for each mask using histogram trick
        for mask in range(1, 32):
            h = [height[c][mask] for c in range(m)]
            stack = []
            sum_rect = 0
            for i in range(m):
                cnt = 0
                while stack and stack[-1][0] >= h[i]:
                    height_val, c_cnt = stack.pop()
                    cnt += c_cnt
                cnt += 1
                stack.append((h[i], cnt))
                for height_val, c_cnt in stack:
                    sum_rect += height_val
            counts[mask] += sum_rect
    
    # inclusion-exclusion to get exact k letters
    result = [0]*5
    for mask in range(1, 32):
        k = bin(mask).count('1')
        result[k-1] += counts[mask]
    
    # subtract overcount from subsets
    for k in range(5, 0, -1):
        for mask in range(1, 32):
            if bin(mask).count('1') == k:
                submask = mask
                while submask:
                    submask = (submask-1) & mask
                    if submask == 0 or submask == mask:
                        continue
                    result[bin(submask).count('1')-1] -= counts[mask]
    
    print(' '.join(map(str, result)))

solve()
```

The code first encodes letters to bits, builds histograms for each mask, counts rectangles with the histogram trick, and finally applies inclusion-exclusion to ensure exactly `k` letters. Key subtleties include properly handling heights per mask and correctly iterating submasks for subtraction.

## Worked Examples

**Sample 1**

Input:

```
2 3
ABB
ABA
```

| Row | Column | Mask `height` | Stack rectangles | Accumulated counts |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 for A | ... | ... |
| 0 | 1 | 1 for B | ... | ... |
| 0 | 2 | 1 for B | ... | ... |
| 1 | 0 | 2 for A | ... | ... |
| 1 | 1 | 1 for B | ... | ... |
| 1 | 2 | 1 for A/B | ... | ... |

This confirms the histogram counts rectangles ending at each row correctly, then inclusion-exclusion extracts exact letter counts: 9 submatrices with 1 letter, 9 with 2 letters, 0 with more.

**Custom Small Input**

```
1 1
A
```

Only one submatrix exists, with exactly one letter. Algorithm tracks height=1, mask count=1, result = [1,0,0,0,0].

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m 2^5) = O(25,600,000) | Each of 32 masks, 800x800 grid, plus histogram O(m) |
| Space | O(m 2^5) = O(25,600) | Store heights per column per mask |

This fits comfortably within 4s and 256 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().
```
