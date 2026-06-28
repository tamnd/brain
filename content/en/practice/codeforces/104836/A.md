---
title: "CF 104836A - \u0427\u0438\u0441\u043b\u043e \u0431\u0435\u043b\u044b\u0445 \u043a\u0432\u0430\u0434\u0440\u0430\u0442\u043e\u0432"
description: "We are given a standard $n times n$ chessboard where the top-left square is colored black and colors alternate perfectly both horizontally and vertically. This creates the usual checkerboard pattern. The task is to determine how many squares of size $1 times 1$ are white."
date: "2026-06-28T11:42:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104836
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u0433\u043e\u0440\u043e\u0434\u0435 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u0440\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0435 \u041a\u0430\u0440\u0435\u043b\u0438\u044f 2023-2024 (9-11 \u043a\u043b\u0430\u0441\u0441)"
rating: 0
weight: 104836
solve_time_s: 60
verified: true
draft: false
---

[CF 104836A - \u0427\u0438\u0441\u043b\u043e \u0431\u0435\u043b\u044b\u0445 \u043a\u0432\u0430\u0434\u0440\u0430\u0442\u043e\u0432](https://codeforces.com/problemset/problem/104836/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a standard $n \times n$ chessboard where the top-left square is colored black and colors alternate perfectly both horizontally and vertically. This creates the usual checkerboard pattern. The task is to determine how many squares of size $1 \times 1$ are white.

The board size is controlled by a single integer $n$. The output is just the count of white cells in this alternating pattern.

The constraints matter because $n$ can be as large as $10^9$. Any solution that tries to build the grid or iterate over all cells is immediately impossible. A full simulation would require $n^2$ operations, which reaches $10^{18}$ in the worst case, far beyond feasible limits even for $n \le 10^3$.

A naive pitfall appears when trying to explicitly color rows and count white cells row by row. For example, for $n = 4$, one might attempt to construct the grid:

Input:

```
4
```

A brute simulation would fill 16 cells, alternate colors, and count whites. That works for small $n$, but the same logic becomes infeasible for $n = 10^9$, where no explicit construction can exist in memory or time.

Another subtle edge case is odd-sized boards. For example:

Input:

```
3
```

Output:

```
4
```

A naive assumption that half of the cells are always white would give $4.5$, which is not meaningful. The parity structure matters.

## Approaches

The brute-force approach is to iterate over every cell $(i, j)$, determine whether it is white based on parity, and increment a counter. A cell is white if the sum of its coordinates has the opposite parity of the top-left black cell. Since black starts at $(1,1)$, which has sum $2$, a cell is white when $(i + j)$ is odd.

This method is correct because it directly encodes the coloring rule. However, it requires $n^2$ checks. When $n = 10^9$, this becomes $10^{18}$ operations, which is completely infeasible.

The key observation is that the board is perfectly periodic. Every 2 by 2 block contains exactly two white and two black cells. This removes any need for iteration. Instead of counting cells individually, we only need to count how many full pairs of rows and columns exist and how the remainder behaves when $n$ is odd.

If $n$ is even, the board splits into $2 \times 2$ blocks, each contributing exactly 2 white cells. If $n$ is odd, there is an additional partial row and column that preserve the alternating structure, adding one extra white cell in total relative to the even case.

This leads directly to a closed-form expression based on integer division.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Observe that each cell’s color depends only on the parity of its coordinates. A white cell occurs when the coordinate sum is odd under the given starting configuration. This removes the need for any simulation.
2. Split the board into full $2 \times 2$ blocks. Each such block contains exactly 2 white cells. The number of complete blocks is $(n // 2)^2$. This captures all fully paired structure.
3. Handle the leftover rows and columns when $n$ is odd. If there is a last row or last column, they contribute additional cells following the alternating pattern, resulting in exactly $\lfloor n^2 / 2 \rfloor$ white cells overall.
4. Compute the final answer as integer division $n \cdot n // 2$, which naturally handles both even and odd cases without branching.

### Why it works

The coloring induces a strict parity partition of the grid: every cell belongs to exactly one of two classes based on $(i + j) \bmod 2$. Because the grid starts with a black cell at $(1,1)$, white cells correspond to one of the parity classes uniformly distributed across the grid. Over any rectangular region, parity alternates perfectly, and imbalance can only occur by at most one cell when the area is odd. This guarantees that exactly half the cells, rounded down, are white.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
print((n * n) // 2)
```

The solution relies entirely on the parity structure of the chessboard. The expression $n * n$ computes the total number of cells. Dividing by 2 using integer division automatically handles both even and odd cases by rounding down, which matches the exact count of white cells.

A subtle point is that Python integers handle large values safely, so even when $n = 10^9$, computing $n^2$ remains valid. In languages with fixed-width integers, one would need to ensure 64-bit arithmetic to avoid overflow.

## Worked Examples

### Example 1: $n = 2$

We compute $n^2 = 4$, then floor divide by 2.

| Step | Value |
| --- | --- |
| n | 2 |
| n² | 4 |
| white cells | 2 |

This matches the explicit grid:

Black, White

White, Black

So there are 2 white cells.

The trace confirms that the formula correctly handles the smallest non-trivial square.

### Example 2: $n = 3$

| Step | Value |
| --- | --- |
| n | 3 |
| n² | 9 |
| white cells | 4 |

A manual view of the board shows:

Black, White, Black

White, Black, White

Black, White, Black

Counting whites gives 4. The formula correctly resolves the imbalance created by the odd-sized grid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only arithmetic operations are performed regardless of input size |
| Space | $O(1)$ | No auxiliary data structures are used |

The solution trivially satisfies the constraints up to $n = 10^9$, since it performs a constant number of operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline().strip())
    return str((n * n) // 2)

assert run("2\n") == "2", "sample 1"
assert run("3\n") == "4", "sample 2"
assert run("1\n") == "0", "minimum size"
assert run("4\n") == "8", "even square"
assert run("1000000000\n") == str((10**9 * 10**9)//2), "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | smallest grid edge case |
| 3 | 4 | odd-sized parity behavior |
| 10^9 | 5e17 | large input stability |
| 4 | 8 | even grid correctness |

## Edge Cases

For $n = 1$, the grid has a single black cell. The formula gives $1 // 2 = 0$, which matches the fact that no white cells exist. The parity argument holds even in this degenerate case.

For odd $n$, such as $n = 5$, the grid contains $25$ cells. The formula gives $12$, while a naive “half is 12.5” would be incorrect. The missing half-cell is resolved by flooring, which corresponds to the exact distribution of parity classes in an odd-sized square.

For large $n$, such as $10^9$, no structural change occurs. The computation remains a single multiplication and division, confirming that the combinatorial structure fully replaces any geometric reasoning.
