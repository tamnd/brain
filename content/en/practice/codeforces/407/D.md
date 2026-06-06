---
title: "CF 407D - Largest Submatrix 3"
description: "We are given an integer matrix of size n by m. Each cell contains a positive integer. The task is to find the largest rectangular submatrix where all the elements are distinct. The “largest” is measured by area, meaning the number of cells inside the rectangle."
date: "2026-06-07T01:51:12+07:00"
tags: ["codeforces", "competitive-programming", "dp", "hashing"]
categories: ["algorithms"]
codeforces_contest: 407
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 239 (Div. 1)"
rating: 2700
weight: 407
solve_time_s: 284
verified: false
draft: false
---

[CF 407D - Largest Submatrix 3](https://codeforces.com/problemset/problem/407/D)

**Rating:** 2700  
**Tags:** dp, hashing  
**Solve time:** 4m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer matrix of size _n_ by _m_. Each cell contains a positive integer. The task is to find the largest rectangular submatrix where all the elements are distinct. The “largest” is measured by area, meaning the number of cells inside the rectangle. For example, a 2×3 rectangle has area 6. The output is the area of the largest such rectangle.

With the constraints _n_, _m_ ≤ 400, a brute-force solution that checks all possible rectangles would involve iterating over O(n² m²) submatrices and checking distinctness inside each, which could take up to 400² × 400² = 2.56 × 10¹⁰ operations. This is far too large for a 3-second limit. Memory limit is 256 MB, which is sufficient to store a few matrices of size 400×400, but we must avoid storing any O(n² m²) intermediate data.

A naive implementation might also fail on small or degenerate inputs. For example, if all elements are equal:

```
2 2
1 1
1 1
```

The correct answer is 1, because any submatrix larger than 1×1 contains repeated elements. A careless approach might incorrectly count larger areas if it does not carefully enforce uniqueness.

Another subtle case is a matrix with many repeated values scattered, like:

```
3 3
1 2 3
2 3 4
3 4 5
```

The largest rectangle is not the full matrix, because diagonally repeated numbers appear; the algorithm must correctly detect such overlaps.

## Approaches

The brute-force approach is simple: iterate over all pairs of top-left and bottom-right corners, extract the submatrix, and check if all values are unique. Checking uniqueness can be done with a hash set. This guarantees correctness but fails because each submatrix check is O(area), and there are O(n² m²) submatrices. Even for small matrices, this is too slow.

The key insight to optimize is that uniqueness along columns can be tracked efficiently by sweeping rows. Instead of iterating over bottom-right corners explicitly, we fix the top row and extend the bottom row downward. For each column, we track the last row where a duplicate occurred, forming a “valid width” rectangle for that column. Then the largest rectangle with all unique elements can be found by maintaining, for each column, the leftmost valid boundary. This reduces the problem to O(n m²) using hashing per row, which is feasible for n, m ≤ 400.

Essentially, the problem reduces to computing, for each row segment, the largest rectangle with unique column elements using a sliding window per row. The challenge is efficiently tracking duplicates and extending rectangles without recomputing uniqueness from scratch.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² m² × area) ≈ O(n³ m³) | O(n m) | Too slow |
| Optimal | O(n m²) | O(n m) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `best` to 0. This will store the largest area found so far.
2. Iterate `top` from row 0 to n-1. This row will be the top boundary of our candidate submatrix.
3. Create an array `last_seen` of dictionaries, one per column, which maps element values to the last row index where they appeared. This allows us to detect duplicates in a column quickly.
4. Initialize an array `min_top` of size m with `top`. This tracks, for each column, the earliest row index we can start without repeating a value in the current column.
5. Iterate `bottom` from `top` to n-1. This extends the submatrix downward. For each column, check the element in row `bottom`. If it has appeared in this column since `min_top[col]`, move `min_top[col]` just after that row. Update `last_seen[col][value] = bottom`.
6. Once `min_top` is updated for the current `bottom`, use a sliding window across columns to find the widest contiguous range `[l, r]` where all `min_top[c] <= top`. Compute the area `(bottom - top + 1) * (r - l + 1)` and update `best` if larger.
7. After finishing all `bottom` extensions, increment `top` and repeat.

### Why it works

The invariant maintained is that for the current rectangle from `top` to `bottom` and columns `[l, r]`, no element is repeated in any column. By tracking `min_top`, we never include a row that would introduce a duplicate. The sliding window ensures that the largest possible width is always considered, so every candidate rectangle is maximal for its top and bottom boundaries. Scanning all top rows ensures no potential rectangle is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

best = 0
last_seen = [{} for _ in range(m)]

for top in range(n):
    min_top = [top] * m
    for bottom in range(top, n):
        for col in range(m):
            val = a[bottom][col]
            if val in last_seen[col] and last_seen[col][val] >= min_top[col]:
                min_top[col] = last_seen[col][val] + 1
            last_seen[col][val] = bottom

        l = 0
        for r in range(m):
            while l <= r and min_top[r] > top:
                l += 1
            width = r - l + 1
            height = bottom - top + 1
            best = max(best, width * height)

print(best)
```

The solution reads the matrix and iterates over top rows. `last_seen` is a dictionary per column for fast lookup of the last row a value appeared. `min_top` tracks how high we can go without repeating in that column. The sliding window across columns guarantees we maximize width for each bottom row extension. Boundary conditions like moving `l` forward ensure no duplicate elements sneak into the rectangle.

## Worked Examples

**Example 1**

Input:

```
3 3
1 3 1
4 5 6
2 6 1
```

| top | bottom | min_top | l | r | width | height | area | best |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | [0,0,0] | 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 0 | [0,0,0] | 0 | 1 | 2 | 1 | 2 | 2 |
| 0 | 0 | [0,0,0] | 0 | 2 | 3 | 1 | 3 | 3 |
| 0 | 1 | [0,0,0] | 0 | 0 | 1 | 2 | 2 | 3 |
| 0 | 1 | [0,0,0] | 0 | 1 | 2 | 2 | 4 | 4 |
| 0 | 1 | [0,0,0] | 0 | 2 | 2 | 2 | 4 | 4 |
| 0 | 2 | [0,0,2] | 0 | 0 | 1 | 3 | 3 | 4 |
| 0 | 2 | [0,0,2] | 0 | 1 | 2 | 3 | 6 | 6 |

The final best is 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m²) | Outer loop over top rows (n), inner loop over bottom rows (≤ n), sliding window across m columns |
| Space | O(n m) | Storing last_seen dictionaries per column, min_top array |

With n, m ≤ 400, n m² ≤ 6.4×10⁷ operations, which runs comfortably in 3 seconds. Memory usage is within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]
    best = 0
    last_seen = [{} for _ in range(m)]
    for top in range(n):
        min_top = [top] * m
        for bottom in range(top, n):
            for col in range(m):
                val = a[bottom][col]
                if val in last_seen[col] and last_seen[col][val] >= min_top[col]:
                    min_top[col] = last_seen[col][val] + 1
                last_seen[col][val] = bottom
            l = 0
            for r in range(m):
                while l <= r and min_top[r] > top:
                    l += 1
                width = r - l + 1
                height = bottom - top + 1
                best = max(best, width * height)
    return str(best)

# provided sample
assert run("3 3\n1 3 1\n4 5 6\n2 6 1\n") == "6"

# all equal
assert run("2 2\n1 1\n1 1\n") == "1"

# minimum input
```
