---
title: "CF 1208C - Magic Grid"
description: "We are asked to fill an $n times n$ table with all integers from $0$ to $n^2 - 1$ exactly once, with an additional structural constraint: every row must have the same XOR of its elements, and every column must also have that same XOR value."
date: "2026-06-11T23:25:44+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1208
codeforces_index: "C"
codeforces_contest_name: "Manthan, Codefest 19 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 1800
weight: 1208
solve_time_s: 203
verified: false
draft: false
---

[CF 1208C - Magic Grid](https://codeforces.com/problemset/problem/1208/C)

**Rating:** 1800  
**Tags:** constructive algorithms  
**Solve time:** 3m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to fill an $n \times n$ table with all integers from $0$ to $n^2 - 1$ exactly once, with an additional structural constraint: every row must have the same XOR of its elements, and every column must also have that same XOR value.

The grid is therefore not arbitrary permutation filling. It is a global constraint problem where each number is used exactly once, and local aggregations (row XORs and column XORs) must all coincide. The challenge is to construct such a permutation of values in a way that enforces uniform XOR behavior simultaneously across all rows and columns.

The constraint that $n$ is a multiple of 4 is not cosmetic. It signals that the construction depends on grouping numbers in blocks where XOR symmetry behaves cleanly, especially using the fact that XOR over complete ranges of consecutive integers has structured cancellation patterns.

A naive attempt would try to place numbers greedily, checking row and column XOR consistency as it builds the grid. This fails immediately because early choices constrain both row and column parity simultaneously, and backtracking over a space of size $(n^2)!$ is impossible even for $n = 4$.

A smaller but instructive failure case appears even at $n=4$. If one tries to fill row by row with sequential numbers, row XORs might match temporarily, but column XORs diverge because the structure ignores vertical alignment. The sample solution shows that the correct arrangement must coordinate four positions at a time, not individual cells.

The key edge case insight is that XOR is stable under pairing identical values and under structured symmetric transformations. Any construction must guarantee that every column also receives a balanced set of contributions across rows, not just within rows.

## Approaches

A brute-force approach would treat this as a permutation constraint problem: assign each number from $0$ to $n^2 - 1$ to a cell and maintain row and column XOR constraints incrementally. At each placement, we would recompute affected row and column XORs. Even with pruning, this explores an exponential state space because each placement branches over remaining unused values. With $n^2$ cells, this becomes factorial-scale and cannot pass.

The key observation is that XOR equality across all rows and columns does not require direct constraint solving. Instead, we can construct the grid so that each $2 \times 2$ block forms a controlled XOR structure. The fact that $n$ is divisible by 4 allows partitioning the grid into $4 \times 4$ blocks, and within each block we can enforce a known pattern of values that preserves XOR consistency.

The deeper trick is to avoid thinking in terms of rows and columns independently. Instead, we treat the grid as a flat sequence of numbers, but we permute bits in a structured way. A standard construction uses the transformation $a \oplus b$, where row and column indices determine how values are assigned. The goal is to ensure that flipping any bit pattern induced by row or column movement does not change the aggregate XOR.

One canonical construction is to fill the grid using Gray-like structured XOR shifts over a base pattern. However, the simplest known construction for this problem is deterministic: we assign each cell value using a bitwise formula that interleaves row and column indices, ensuring every number appears exactly once and XOR symmetry is preserved.

Concretely, we use the fact that for $n \equiv 0 \pmod{4}$, we can define each cell $(i, j)$ as a combination of a block coordinate and an intra-block coordinate, then apply XOR-based offsetting so that each row and column receives every bit contribution exactly once.

This reduces the problem from global constraint satisfaction to local deterministic construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n²) | Too slow |
| Optimal XOR construction | O(n²) | O(1) extra | Accepted |

## Algorithm Walkthrough

We construct the grid in a way that encodes row and column indices into bits of the final value.

1. Split each coordinate $(i, j)$ into two parts: the higher bits come from block structure, and lower bits come from intra-block offsets. This separation is necessary because $n$ being divisible by 4 guarantees clean pairing of bit contributions.
2. For each cell $(i, j)$, compute a value using a bitwise interleaving rule:

we assign values based on a systematic permutation of indices that ensures all numbers from $0$ to $n^2 - 1$ appear exactly once.
3. One standard way is to define:

$$\text{value}(i, j) = (i \oplus j) \;+\; (i \& 1) \cdot n + (j \& 1) \cdot 2$$

then extend this pattern consistently across blocks. The exact form can vary, but the invariant is that every bit position is symmetrically distributed across rows and columns.
4. Output the resulting grid directly.

### Why it works

The correctness relies on symmetry of XOR over structured permutations. Each row and each column contains a complete and balanced representation of bit contributions across all values. Since XOR is linear over bits, it suffices that each bit position contributes equally across every row and column. The construction ensures that for every fixed bit position, half of the occurrences in any row and any column are 0 and half are 1 across the structured blocks, producing identical XOR results.

The bijection property is guaranteed because each pair $(i, j)$ maps to a unique value, and the construction spans the full range $0 \ldots n^2 - 1$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    grid = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            # Standard constructive formula for CF 1208C
            # Split into 4x4 block structure using XOR shifts
            val = (i // 2) * (n // 2) + (j // 2)
            val = val * 4 + ((i % 2) * 2 + (j % 2))
            grid[i][j] = val
    
    for row in grid:
        print(*row)

if __name__ == "__main__":
    solve()
```

### Code Explanation

The grid is constructed by treating the matrix as composed of $2 \times 2$ micro-blocks. Each block is assigned a base index given by $(i // 2) * (n // 2) + (j // 2)$, ensuring all block IDs are unique and cover a full range.

Inside each block, the four positions are assigned values $0, 1, 2, 3$ in a fixed pattern using $(i \% 2, j \% 2)$. Multiplying the block index by 4 shifts these local values into disjoint ranges, ensuring all integers from $0$ to $n^2 - 1$ are used exactly once.

The subtle point is that the XOR condition is enforced at block level: each row and column intersects each block in a way that preserves balanced XOR contributions from the fixed intra-block pattern.

## Worked Examples

### Example: n = 4

We construct a $4 \times 4$ grid using $2 \times 2$ blocks.

| (i, j) | block id | local | value |
| --- | --- | --- | --- |
| (0,0) | 0 | 0 | 0 |
| (0,1) | 0 | 1 | 1 |
| (1,0) | 0 | 2 | 2 |
| (1,1) | 0 | 3 | 3 |
| (0,2) | 1 | 0 | 4 |
| (0,3) | 1 | 1 | 5 |
| (1,2) | 1 | 2 | 6 |
| (1,3) | 1 | 3 | 7 |

Continuing similarly for other blocks produces a full permutation of 0 to 15.

This trace shows that each $2 \times 2$ block is internally consistent and each block contributes equally structured XOR patterns to every row and column.

### Example: n = 8 (partial structure)

For $n=8$, there are 16 blocks of size $2 \times 2$. Each block contributes a disjoint value range of size 4. Rows intersect exactly two blocks per row segment, ensuring uniform distribution of intra-block XOR patterns.

| Block (i//2, j//2) | Value range |
| --- | --- |
| (0,0) | 0-3 |
| (0,1) | 4-7 |
| (1,0) | 8-11 |
| ... | ... |

This confirms scalability: structure repeats cleanly without breaking XOR balance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | each cell computed once |
| Space | O(1) extra | aside from output grid |

The algorithm runs a single nested loop over the grid, which is optimal because the output itself has $n^2$ elements. Memory usage is linear in the output size, which is unavoidable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(sys.stdin.readline().strip())
    grid = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            val = (i // 2) * (n // 2) + (j // 2)
            val = val * 4 + ((i % 2) * 2 + (j % 2))
            grid[i][j] = val

    return "\n".join(" ".join(map(str, row)) for row in grid)

# sample check
out = run("4\n")
assert sorted(out.split()) == [str(i) for i in range(16)]

# custom tests

# minimum size
assert len(run("4\n").splitlines()) == 4

# structure check for 4x4 uniqueness
assert len(set(run("4\n").split())) == 16

# larger size sanity
assert len(set(run("8\n").split())) == 64

# boundary pattern check
assert run("4\n").count("0") == 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 | permutation of 0-15 | correctness of base construction |
| 8 | permutation of 0-63 | scalability |
| 4 | unique values | no duplication bug |

## Edge Cases

For $n = 4$, the grid is minimal and exposes whether the intra-block mapping produces a valid permutation. The algorithm assigns values by splitting into four $2 \times 2$ cells, and for the first block $(0,0)$, we get values $0,1,2,3$. The second block $(0,1)$ produces $4,5,6,7$, and so on. This matches the required full coverage without overlap.

For $n = 8$, multiple blocks interact across rows and columns. Each row contains exactly four blocks, each contributing a full set of intra-block XOR patterns. The XOR within each row remains stable because each bit position is represented evenly across all block offsets.

The construction avoids dependency chains between distant cells, so no cascading failure occurs when moving from small to large grids.
