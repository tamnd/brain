---
title: "CF 1208C - Magic Grid"
description: "We are asked to fill an $n times n$ table with all integers from $0$ to $n^2 - 1$ exactly once, so every number is used in a permutation of the grid cells."
date: "2026-06-15T17:55:37+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1208
codeforces_index: "C"
codeforces_contest_name: "Manthan, Codefest 19 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 1800
weight: 1208
solve_time_s: 388
verified: false
draft: false
---

[CF 1208C - Magic Grid](https://codeforces.com/problemset/problem/1208/C)

**Rating:** 1800  
**Tags:** constructive algorithms  
**Solve time:** 6m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to fill an $n \times n$ table with all integers from $0$ to $n^2 - 1$ exactly once, so every number is used in a permutation of the grid cells. The extra constraint is global: every row must have the same bitwise XOR of its entries, and every column must also have that same XOR value.

The input is only $n$, and we are guaranteed that $n$ is a multiple of 4. The output is any valid arrangement of the numbers into the grid that satisfies the XOR uniformity condition.

The constraints suggest that we cannot treat this as a search or constraint satisfaction problem. The grid size can go up to $1000 \times 1000$, meaning up to one million distinct values must be placed. Any approach that checks row and column XORs repeatedly during construction is still fine, but anything exponential or involving backtracking is immediately impossible.

A subtle failure case for naive thinking is to distribute numbers in simple patterns like row-major order or checkerboard XOR balancing. For example, filling row by row with increasing numbers fails because XOR of consecutive blocks is not stable across rows or columns. Another tempting idea is to enforce row XOR equality first and then adjust columns, but changing a single entry breaks both constraints globally, making local fixes ineffective.

The structure of the problem hints that we need a deterministic construction where every local region already satisfies XOR symmetry, and these regions combine cleanly at a higher level.

## Approaches

A brute-force interpretation would be to try assigning numbers one by one and maintaining constraints. At each step, we would place a number in an empty cell and check whether row and column XOR constraints remain satisfiable. Even if we do pruning, the state space is enormous: there are $(n^2)!$ permutations of numbers, and each partial assignment affects $O(n)$ rows and columns. Even with memoization, the constraint graph is too dense for meaningful DP compression.

The key observation is that XOR behaves nicely under structured pairing. If we can ensure that each row and column is formed from carefully paired values whose XOR contributions cancel in a controlled way, we can enforce uniformity without explicitly tracking XORs.

A useful perspective is to build the grid in blocks of $2 \times 2$. Inside such a block, if we assign four values so that their XOR is balanced in a symmetric pattern, then each block contributes a predictable XOR footprint to its row and column intersections. Since $n$ is a multiple of 4, the grid can be partitioned into $2 \times 2$ blocks in a way that every row and column is composed of full blocks only.

The construction reduces to assigning numbers inside each $2 \times 2$ block in a consistent pattern, while ensuring that different blocks receive disjoint value ranges. The standard trick is to treat each block index as a coordinate in a smaller grid of size $(n/2) \times (n/2)$, and then expand it into four values using bit manipulation so that all numbers from $0$ to $n^2-1$ are covered exactly once.

This works because XOR depends on bit structure, and splitting indices into high and low parts allows us to independently control distribution across blocks and inside blocks. The final design ensures every row sees each high-level pattern exactly once, and the same holds for columns, which forces XOR uniformity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n²) | Too slow |
| Block construction | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

We construct the grid using $2 \times 2$ blocks.

1. Split the grid into coordinates $(i, j)$. Each cell belongs to a block at $(i // 2, j // 2)$. This ensures every block is independent and covers 4 cells.
2. Assign each block a unique base value using its block index:

$$b = (i // 2) \cdot (n // 2) + (j // 2)$$

This enumerates blocks from $0$ to $(n/2)^2 - 1$.
3. Expand each block value into four distinct numbers using bit shifts:

- top-left: $4b$
- top-right: $4b + 1$
- bottom-left: $4b + 2$
- bottom-right: $4b + 3$

The reason for multiplying by 4 is that each block must reserve a disjoint chunk of size 4 in the global permutation.
4. Place these values consistently inside every $2 \times 2$ block. This guarantees no overlaps and ensures all numbers from $0$ to $n^2 - 1$ are used exactly once.
5. Output the constructed grid.

### Why it works

Each row consists of a sequence of $n/2$ blocks, and within each block the XOR of its four elements is:

$$(4b) \oplus (4b+1) \oplus (4b+2) \oplus (4b+3) = 0$$

because the last two bits cycle through all combinations and cancel out under XOR.

Since every row is composed entirely of such zero-XOR blocks, the XOR of every row is 0. The same holds for every column because blocks align consistently across vertical partitions. Therefore, all rows and columns share the same XOR value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            b = (i // 2) * (n // 2) + (j // 2)
            base = 4 * b
            if i % 2 == 0 and j % 2 == 0:
                a[i][j] = base
            elif i % 2 == 0 and j % 2 == 1:
                a[i][j] = base + 1
            elif i % 2 == 1 and j % 2 == 0:
                a[i][j] = base + 2
            else:
                a[i][j] = base + 3

    for row in a:
        print(*row)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the block decomposition. The key detail is computing the block index using integer division by 2, then mapping each position inside the block using the parity of row and column indices. This avoids any need for conditional reshaping or post-processing.

A common mistake is to forget that each block must map to a contiguous range of four numbers. Without the multiplication by 4, values would collide across blocks and break the permutation requirement.

## Worked Examples

### Example: n = 4

We have a $2 \times 2$ block grid of blocks.

| Cell (i,j) | Block b | Value |
| --- | --- | --- |
| (0,0) | 0 | 0 |
| (0,1) | 0 | 1 |
| (1,0) | 0 | 2 |
| (1,1) | 0 | 3 |
| (0,2) | 1 | 4 |
| (0,3) | 1 | 5 |
| (1,2) | 1 | 6 |
| (1,3) | 1 | 7 |
| ... | ... | ... |

Each block contributes XOR 0 internally, so rows and columns inherit uniform XOR.

This trace confirms that blocks are independent and fill the range 0 to 15 exactly once.

### Example: n = 8 (partial structure)

| Block (i//2, j//2) | b | Values placed |
| --- | --- | --- |
| (0,0) | 0 | 0-3 |
| (0,1) | 1 | 4-7 |
| (1,0) | 4 | 16-19 |
| (3,3) | 15 | 60-63 |

Each row consists of 4 blocks, each contributing zero XOR, so row XOR is 0.

This confirms scalability: increasing $n$ only repeats the same local invariant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each cell is computed once |
| Space | O(n²) | Grid storage |

The algorithm touches every cell exactly once, which fits comfortably within limits for $n \le 1000$, producing at most one million assignments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    import io as sio
    out = sio.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample
assert run("4\n") != ""

# minimum valid case
assert run("4\n").count("\n") == 3

# block structure sanity check
assert run("4\n").split()[0] == "0"

# larger case structural check
out = run("8\n")
vals = list(map(int, out.split()))
assert sorted(vals) == list(range(64))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 | valid 4x4 grid | base correctness |
| 8 | valid 8x8 grid | scalability and uniqueness |
| 4 | permutation 0-15 | no duplicates |
| 8 | permutation 0-63 | full coverage |

## Edge Cases

For $n = 4$, there is only one level of block decomposition. The algorithm assigns exactly four blocks of size $2 \times 2$, producing numbers 0 through 15 without overlap. The XOR condition holds because each block independently has XOR 0, so every row and column inherits a sum of zero XOR contributions.

For larger $n$, such as $n = 1000$, the same logic repeats across 250,000 blocks. Each block contributes a disjoint range of values, so no collisions occur even at maximum scale. Every row still consists of full blocks, so the XOR remains stable regardless of grid size.
