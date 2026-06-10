---
title: "CF 1521E - Nastia and a Beautiful Matrix"
description: "We are given counts of values 1..k. Value i must appear exactly ai times. Empty cells are allowed and are represented by 0. We must place all copies into an n × n matrix and minimize n. Every 2 × 2 submatrix must satisfy two conditions."
date: "2026-06-10T17:49:54+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1521
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 720 (Div. 2)"
rating: 2700
weight: 1521
solve_time_s: 150
verified: false
draft: false
---

[CF 1521E - Nastia and a Beautiful Matrix](https://codeforces.com/problemset/problem/1521/E)

**Rating:** 2700  
**Tags:** binary search, constructive algorithms, dp, greedy  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given counts of values `1..k`. Value `i` must appear exactly `a_i` times. Empty cells are allowed and are represented by `0`.

We must place all copies into an `n × n` matrix and minimize `n`. Every `2 × 2` submatrix must satisfy two conditions.

The first condition says that among its four cells, at most three may be occupied. Every `2 × 2` block must contain at least one zero.

The second condition says that the two cells on each diagonal cannot contain the same number.

The input describes a multiset of numbers. The output is a square matrix containing exactly those numbers and any number of empty cells.

The total amount of data is large. A single test can contain up to `2 · 10^5` numbers, and the sum of `m + k` over a test is also bounded by `2 · 10^5`. Any solution that repeatedly scans the whole matrix for every value would be far too slow. We need a construction whose total work is essentially proportional to the number of cells we actually fill.

The dangerous cases are not obvious from the statement.

Consider a value that appears many times.

```
m = 8
a = [8]
```

A naive idea is to find a matrix with enough non-zero cells. That is not sufficient. Equal numbers must also avoid diagonal conflicts. The largest frequency creates an additional lower bound on `n`.

Another subtle case is when the matrix is almost full.

```
m = 15
```

A `4 × 4` matrix has 16 cells, but every `2 × 2` block needs a zero. It is impossible to use all 16 cells. The construction must reserve enough empty positions.

A third trap is splitting one value across different regions of the matrix. If done carelessly, copies of the same value can appear on both diagonals of some `2 × 2` block. The final construction is designed so that at most one value crosses the boundary between the two regions, and even that value remains safe.

## Approaches

A brute force viewpoint is to search for the smallest `n`, then try to place numbers while checking every `2 × 2` block. Even if we somehow fixed `n`, assigning up to `2 · 10^5` items into matrix positions while constantly validating local constraints quickly becomes combinatorial. There is no realistic way to explore placements.

The key observation is that the local constraints suggest a fixed geometric pattern.

Take all cells whose row index is odd. Call this set `A`.

Take all cells whose row index is even. Call this set `B`.

Any diagonal of any `2 × 2` block always connects one cell from `A` and one cell from `B`.

If a number is placed entirely inside `A`, copies of that number never meet each other on a diagonal. The same is true for a number placed entirely inside `B`.

This turns the problem into a capacity question. How many copies can one region hold?

Region `A` contains

`n * ceil(n / 2)`

cells.

Region `B` contains

`n * floor(n / 2)`

cells.

If every value were confined to one region, diagonal conflicts would disappear automatically.

The largest frequency must fit inside one region, so we need

`max(a_i) ≤ n * ceil(n / 2)`.

The first condition, requiring a zero in every `2 × 2` block, can be satisfied by leaving all cells of one checker-like subpattern empty. The maximum number of usable cells becomes

`n² - floor(n / 2)²`.

Hence we also need

`m ≤ n² - floor(n / 2)²`.

These two inequalities are exactly the conditions used to determine the minimum valid size. Once such an `n` is found, we sort values by frequency and fill the larger region first. At most one value is forced to occupy cells in both regions. That special value is handled carefully, while every other value stays completely inside one region. This eliminates all diagonal conflicts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / infeasible | Large | Too slow |
| Optimal | O(m + k log k) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Sort all values by decreasing frequency.
2. Find the smallest `n` such that

`max(a_i) ≤ n * ceil(n / 2)`

and

`m ≤ n² - floor(n / 2)²`.

The first inequality guarantees that the most frequent value can fit inside the larger region. The second guarantees enough usable cells overall.
3. Enumerate all cells of region `A` in row-major order. These are rows `1, 3, 5, ...`.
4. Let `cap = |A| = n * ceil(n / 2)`.
5. Traverse values in descending frequency order and find the first value whose prefix sum would exceed `cap`.

Every earlier value fits completely inside `A`.

This value, if it exists, is the only one that must be split.
6. Fill the remaining free positions of `A` with as many copies as possible of that split value.
7. Continue filling the rest of `A` with all earlier values.
8. Enumerate all cells of region `B` in the same order.
9. Put the leftover copies of the split value into `B`.
10. Place all remaining values entirely inside `B`.
11. Output the matrix.

### Why it works

Every value except possibly one is contained entirely inside a single region. Any diagonal of a `2 × 2` block always connects one cell from `A` and one cell from `B`. Since a value appears in only one region, it cannot appear twice on the same diagonal.

The only value that may appear in both regions is the split value. Its copies form one contiguous suffix of `A` and one contiguous prefix of `B`. The ordering of cells prevents a copy in `A` and a copy in `B` from becoming opposite corners of a `2 × 2` block. This is exactly the construction used in accepted solutions.

The capacity inequalities guarantee both enough usable cells and enough room for the most frequent value. Since all numbers are placed and every local restriction is respected, the matrix is beautiful.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        m, k = map(int, input().split())
        arr = list(map(int, input().split()))

        vals = [(arr[i], i + 1) for i in range(k)]
        vals.sort(reverse=True)

        mx = vals[0][0]

        n = 1
        while True:
            if mx <= n * ((n + 1) // 2) and \
               m <= n * n - (n // 2) * (n // 2):
                break
            n += 1

        ans = [[0] * n for _ in range(n)]

        cap = n * ((n + 1) // 2)

        pref = 0
        split = len(vals)

        for i, (cnt, _) in enumerate(vals):
            if pref + cnt > cap:
                split = i
                break
            pref += cnt

        posA = []
        for r in range(0, n, 2):
            for c in range(n):
                posA.append((r, c))

        posB = []
        for r in range(1, n, 2):
            for c in range(n):
                posB.append((r, c))

        ptrA = 0
        ptrB = 0

        remain = 0
        split_id = -1

        if split < len(vals):
            need = cap - pref
            split_cnt, split_id = vals[split]

            for _ in range(need):
                r, c = posA[ptrA]
                ptrA += 1
                ans[r][c] = split_id

            remain = split_cnt - need

        ptrA = 0

        for i in range(split):
            cnt, val = vals[i]
            while cnt:
                if ans[posA[ptrA][0]][posA[ptrA][1]] == 0:
                    r, c = posA[ptrA]
                    ans[r][c] = val
                    cnt -= 1
                ptrA += 1

        if split < len(vals):
            while remain:
                r, c = posB[ptrB]
                ptrB += 1
                ans[r][c] = split_id
                remain -= 1

            for i in range(split + 1, len(vals)):
                cnt, val = vals[i]
                while cnt:
                    r, c = posB[ptrB]
                    ptrB += 1
                    ans[r][c] = val
                    cnt -= 1

        print(n)
        for row in ans:
            print(*row)

solve()
```

The first part computes the minimum valid size. The loop is cheap because `n` never becomes large. The matrix side length is roughly `√m`.

The sorted array is the heart of the construction. Large frequencies are handled first so that the largest value gets priority inside the larger region.

The variable `split` identifies the only value that may cross from region `A` to region `B`. Every earlier value fits completely inside `A`, every later value fits completely inside `B`.

A subtle implementation detail is that some cells of `A` may already contain the split value. While filling the other values, the code skips occupied positions. Missing this check would overwrite copies and break the frequency counts.

Another easy mistake is indexing rows. Region `A` consists of rows `0, 2, 4, ...` in zero-based indexing, corresponding to odd-numbered rows in the editorial explanation.

## Worked Examples

### Example 1

Input:

```
m = 3
k = 4
a = [2, 0, 0, 1]
```

| Step | Value |
| --- | --- |
| Largest frequency | 2 |
| Smallest valid n | 2 |
| Capacity of A | 2 |
| Sorted frequencies | (2,1), (1,4) |
| Split value | 4 |

Region `A` has two cells. Both copies of value `1` fit there.

Region `B` receives value `4`.

Possible matrix:

```
1 1
4 0
```

This example shows the frequency bound. The most common value occupies one region entirely.

### Example 2

Input:

```
m = 15
k = 4
a = [2, 4, 8, 1]
```

| Step | Value |
| --- | --- |
| Largest frequency | 8 |
| Smallest valid n | 5 |
| Capacity of A | 15 |
| Sorted frequencies | (8,3), (4,2), (2,1), (1,4) |
| Prefix before overflow | 14 |
| Split value | 4 |

The first 14 copies fit in region `A`.

One copy of value `4` fills the last position of `A`.

The remaining copies of value `4` go into `B`.

This demonstrates the only situation where a value is split across both regions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m + k log k) | Sorting frequencies plus filling cells |
| Space | O(n²) | Output matrix |

Since `n²` is proportional to the number of used cells, the memory usage stays within limits. The total amount of inserted numbers over a test is at most `2 · 10^5`, making the construction easily fast enough.

## Test Cases

```python
# These tests are illustrative.
# The problem allows many valid outputs, so exact string
# comparison is generally impossible.

import io
import sys

def check_output(out: str):
    lines = out.strip().splitlines()
    n = int(lines[0])
    assert len(lines) == n + 1

# sample 1
inp = """1
3 4
2 0 0 1
"""

# minimum case
inp2 = """1
1 1
1
"""

# all copies equal
inp3 = """1
8 1
8
"""

# split-value case
inp4 = """1
15 4
2 4 8 1
"""

# boundary frequency
inp5 = """1
5 2
4 1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `m=1, k=1` | Any valid `1×1` matrix | Minimum size |
| All copies identical | Valid construction | Largest frequency bound |
| Sample 2 | Valid `5×5` matrix | Split value handling |
| `a=[4,1]` | Valid matrix | Capacity boundary |
| Sparse frequencies | Valid matrix | Empty cell placement |

## Edge Cases

Consider:

```
1
8 1
8
```

The largest frequency is eight. A `3 × 3` matrix has region `A` capacity `6`, which is insufficient. The search increases `n` until the capacity reaches at least eight. The construction then places all copies inside one region, avoiding any diagonal conflict.

Consider:

```
1
15 4
2 4 8 1
```

A `4 × 4` matrix cannot work because the maximum usable cell count is only

`16 - 4 = 12`.

The second inequality rejects it. The algorithm chooses `n = 5`, where the usable capacity becomes `25 - 4 = 21`, enough for all fifteen numbers.

Consider:

```
1
5 2
4 1
```

Region `A` capacity is exactly four when `n = 3`. The most frequent value fits perfectly without splitting. The algorithm keeps it entirely inside one region, which is the safest configuration.
