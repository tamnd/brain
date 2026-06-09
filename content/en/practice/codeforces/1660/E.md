---
title: "CF 1660E - Matrix and Shifts"
description: "We are given a binary square matrix, and we are allowed to rearrange it using cyclic shifts of rows and columns. These shifts do not change values, they only rotate positions, so what ultimately matters is how we align the matrix before we start paying to flip bits."
date: "2026-06-10T03:03:38+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1660
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 780 (Div. 3)"
rating: 1600
weight: 1660
solve_time_s: 78
verified: true
draft: false
---

[CF 1660E - Matrix and Shifts](https://codeforces.com/problemset/problem/1660/E)

**Rating:** 1600  
**Tags:** brute force, constructive algorithms, greedy, implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary square matrix, and we are allowed to rearrange it using cyclic shifts of rows and columns. These shifts do not change values, they only rotate positions, so what ultimately matters is how we align the matrix before we start paying to flip bits.

After choosing any sequence of row and column rotations, we are allowed to flip individual cells (toggle 0 to 1 or 1 to 0), and each flip costs one unit. The goal is to transform the matrix into a unit matrix, meaning every diagonal cell must be 1 and every off-diagonal cell must be 0.

The key difficulty is that we are not forced to fix the diagonal at the original positions. By shifting rows and columns cyclically, we effectively choose a cyclic shift of row indices and a cyclic shift of column indices. This means the diagonal we are targeting is not fixed, but can be “moved” relative to the original matrix.

Each test case is independent. The matrix size can be up to 2000, and the total number of cells across tests is up to 4 million, so any solution must avoid cubic or repeated heavy recomputation per alignment.

A naive approach would try all row shifts and all column shifts, giving O(n^2) alignments. For each alignment, we would compute how many flips are needed to make diagonal ones and everything else zero. This would cost O(n^3), which is too slow.

A subtle edge case appears when the matrix already has structure close to diagonal under some shift but not under others. For example, in a permutation-like matrix, only one specific cyclic alignment produces a perfect diagonal. A careless approach that assumes only row or only column shifts matter will fail because both dimensions interact.

## Approaches

If we ignore the shift operations, the problem is simple: we must flip every mismatched cell compared to identity, which is just counting differences with the identity matrix. The complication is that we can cyclically rotate rows and columns first.

A brute-force strategy is to try every possible pair of cyclic shifts, one for rows and one for columns. After applying a shift pair, we check every cell and count how many flips are needed to make the matrix unitary. Since there are n choices for row shift and n choices for column shift, and each evaluation costs O(n^2), the total complexity becomes O(n^4) or O(n^3) depending on how carefully we reuse computations. Either way, this is far beyond the limit for n up to 2000.

The key insight is that shifts only reindex rows and columns cyclically. Instead of thinking about moving the matrix, we can think about choosing a target diagonal. A diagonal in a cyclically shifted matrix corresponds to pairs of indices (i, j) where j - i is constant modulo n. So each shift configuration corresponds to selecting a diagonal offset.

Once we fix a diagonal offset d, every cell (i, j) is classified as either on the diagonal if j - i ≡ d (mod n), or off-diagonal otherwise. For a fixed d, we can compute cost directly: diagonal cells must become 1, off-diagonal must become 0. The cost is just counting mismatches.

So instead of trying n^2 shift pairs, we only need to try n possible diagonal offsets. Each evaluation costs O(n^2), giving O(n^3). This is still too large in worst case.

We reduce further by observing that each cell contributes independently to each diagonal choice. If A[i][j] is 1, it helps exactly one diagonal offset (when j - i matches that offset). For all other offsets it is an off-diagonal cell that should be 0, so it contributes a penalty if it is 1 there. Similarly, a 0 contributes a penalty if it lies on the chosen diagonal.

We can precompute contributions per offset in O(n^2): for each cell we update two aggregated structures, one counting how many 1s fall on each diagonal, and implicitly deriving off-diagonal cost. This allows computing the best offset in O(n^2) total per test case.

This reduces the problem from searching over placements to aggregating contributions per modular diagonal class.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force shifts | O(n^4) | O(n^2) | Too slow |
| Check all diagonals directly | O(n^3) | O(n^2) | Too slow |
| Diagonal contribution aggregation | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

We reframe the problem as choosing a diagonal offset that minimizes mismatch cost.

1. Compute, for every possible diagonal offset d, how many ones fall on that diagonal. We define the diagonal class by (j - i mod n). This step is necessary because only cells on the chosen diagonal are required to be 1.
2. For each offset d, we compute the number of diagonal cells, which is exactly n. So off-diagonal cells are n^2 - n.
3. For a fixed d, cost is computed as follows: all diagonal positions that contain 0 must be flipped to 1, and all off-diagonal positions that contain 1 must be flipped to 0. This splits cost into two independent parts.
4. For each d, compute cost using the precomputed counts:

the diagonal mismatch is (n - ones_on_diagonal[d]),

the off-diagonal mismatch is (total_ones - ones_on_diagonal[d]).
5. The total cost becomes:

cost[d] = (n - ones_on_diagonal[d]) + (total_ones - ones_on_diagonal[d]).
6. Iterate over all d and take the minimum cost.

The reason this works is that cyclic shifts do not change which cells share the same value of (j - i mod n). They only rotate which diagonal is considered the main one. Thus every valid shifted configuration corresponds exactly to choosing one of these diagonal classes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t_line = input().strip()
    while t_line == "":
        t_line = input().strip()
    t = int(t_line)

    for _ in range(t):
        line = input().strip()
        while line == "":
            line = input().strip()
        n = int(line)

        grid = []
        total_ones = 0

        for _ in range(n):
            row = input().strip()
            grid.append(row)
            total_ones += row.count('1')

        diag_ones = [0] * n

        for i in range(n):
            row = grid[i]
            for j, ch in enumerate(row):
                if ch == '1':
                    diag_ones[(j - i) % n] += 1

        ans = 10**18

        for d in range(n):
            ones_on_diag = diag_ones[d]
            cost = (n - ones_on_diag) + (total_ones - ones_on_diag)
            ans = min(ans, cost)

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first aggregates all ones per diagonal class using the modular difference (j - i). This encodes the effect of all possible cyclic row and column shifts. It then evaluates each diagonal choice by computing how many corrections are needed inside and outside the diagonal.

A subtle point is that we never explicitly simulate shifts. The modulo indexing already captures all possible cyclic alignments.

## Worked Examples

### Example 1

Input:

```
n = 3
010
011
100
```

We compute total ones and diagonal contributions.

| i | j | A[i][j] | (j - i mod 3) |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 0 |
| 1 | 2 | 1 | 1 |
| 2 | 0 | 1 | 1 |

So diag_ones = [1, 3, 0], total_ones = 4.

Now evaluate cost:

For d = 1, diagonal has 3 ones, so diagonal flips = 3 - 3 = 0, off-diagonal flips = 4 - 3 = 1, total = 1.

For other d values, cost is larger.

This confirms that best alignment corresponds to shifting so that diagonal class 1 becomes main diagonal.

### Example 2

Input:

```
n = 2
10
10
```

All ones are in column 0.

| i | j | A[i][j] | (j - i mod 2) |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 1 |

So diag_ones = [1, 1], total_ones = 2.

For both d values, cost = (2 - 1) + (2 - 1) = 2.

This shows symmetry: no shift improves alignment, and both diagonals are equally valid but still require two flips.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per test | Each cell contributes to one diagonal class, then we scan n diagonals |
| Space | O(n) | Only diagonal counters are stored |

The total complexity across all test cases is bounded by 4 million cells, so this solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t_line = input().strip()
        while t_line == "":
            t_line = input().strip()
        t = int(t_line)

        out = []
        for _ in range(t):
            line = input().strip()
            while line == "":
                line = input().strip()
            n = int(line)

            grid = []
            total_ones = 0
            for _ in range(n):
                row = input().strip()
                grid.append(row)
                total_ones += row.count('1')

            diag = [0] * n
            for i in range(n):
                for j, ch in enumerate(grid[i]):
                    if ch == '1':
                        diag[(j - i) % n] += 1

            ans = 10**18
            for d in range(n):
                ones = diag[d]
                ans = min(ans, (n - ones) + (total_ones - ones))

            out.append(str(ans))

        return "\n".join(out)

    return solve()

# provided samples
assert run("""
4

3
010
011
100

5
00010
00001
10000
01000
00100

2
10
10

4
1111
1011
1111
1111
""".strip()) == """1
0
2
11"""

# custom cases
assert run("""
1
1
0
""".strip()) == "1", "single cell flip"

assert run("""
1
2
00
00
""".strip()) == "2", "all zeros must create one 1 on diagonal"

assert run("""
1
3
111
111
111
""".strip()) == "6", "dense matrix requires clearing off-diagonal ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 zero | 1 | minimal flip case |
| all zeros 2x2 | 2 | must create diagonal ones |
| all ones 3x3 | 6 | off-diagonal cleanup cost |

## Edge Cases

A minimal 1x1 matrix contains no structural freedom. The only requirement is making the single cell equal to 1, so if it starts as 0, one flip is required. The algorithm handles this because there is only one diagonal class and the computation reduces to a direct mismatch count.

A matrix filled entirely with zeros has no diagonal alignment advantage. Every diagonal choice produces the same cost, since all diagonal positions are zeros and must be flipped. The algorithm reflects this because diag_ones[d] is zero for all d, and the cost becomes constant.

A matrix filled with ones stresses the off-diagonal penalty. Even if a diagonal is chosen to maximize alignment, all off-diagonal ones must be flipped away. The formula captures this directly through total_ones - diag_ones[d], ensuring correct accumulation of off-diagonal corrections.
