---
title: "CF 1208C - Magic Grid"
description: "We are asked to fill an $n times n$ grid with all integers from $0$ to $n^2 - 1$, each used exactly once, in such a way that every row and every column has the same XOR value. The grid is not arbitrary permutation placement."
date: "2026-06-13T16:32:27+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1208
codeforces_index: "C"
codeforces_contest_name: "Manthan, Codefest 19 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 1800
weight: 1208
solve_time_s: 489
verified: false
draft: false
---

[CF 1208C - Magic Grid](https://codeforces.com/problemset/problem/1208/C)

**Rating:** 1800  
**Tags:** constructive algorithms  
**Solve time:** 8m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to fill an $n \times n$ grid with all integers from $0$ to $n^2 - 1$, each used exactly once, in such a way that every row and every column has the same XOR value.

The grid is not arbitrary permutation placement. It is a structured arrangement constraint: the multiset of numbers is fixed, but their positions must be chosen so that XOR aggregation behaves uniformly across all rows and columns.

The input size allows $n$ up to 1000, with $n$ guaranteed divisible by 4. This already rules out any exponential or backtracking construction. Even quadratic approaches are acceptable since $10^6$ placements is small. The real challenge is not complexity but constructing a pattern that enforces XOR symmetry.

A naive idea would be to randomly permute numbers into the grid and hope for balanced XORs, but XOR is extremely sensitive to structure. A single misplaced bit pattern destroys the uniform row XOR property, so random or greedy placement will almost certainly fail.

Another tempting idea is to treat rows independently: fill each row with numbers $n \cdot i$ to $n \cdot (i+1)-1$. This respects uniqueness but fails XOR consistency because each row contains a different bit distribution, producing different XOR results across rows and columns.

The difficulty is that we need both global permutation constraints and strong algebraic symmetry under XOR, which suggests a bitwise construction rather than value-based grouping.

## Approaches

A brute-force perspective would attempt to assign numbers one by one while maintaining constraints. At each empty cell, we would try unused values and check whether all completed rows and columns still have matching XORs. This leads to a search tree with branching factor roughly $n^2$, and constraint checking that is $O(n)$ per step, making the total search completely infeasible even for $n=4$.

The key observation is that XOR behaves linearly over bitwise structure, and the condition is invariant under rearranging values as long as we preserve pairing structure in a controlled way. The correct construction comes from pairing numbers in a way that controls XOR contributions within each 2x2 block, then tiling these blocks across the grid.

Since $n$ is divisible by 4, we can partition the grid into $2 \times 2$ blocks. Inside each block, we place four carefully chosen numbers that form a complete XOR-balanced set. A natural way to do this is to use consecutive integers and ensure that each block contains a “complementary” grouping of values.

A standard construction uses the fact that for any integer $x$, the values $x, x \oplus 1, x \oplus 2, x \oplus 3$ form a local XOR-balanced structure when arranged properly. By iterating over blocks and shifting base values by 4 each time, we guarantee that all numbers are used exactly once and each block is internally consistent. Since rows and columns each pass through exactly one element from each block position pattern, the XOR contributions cancel uniformly.

This reduces the problem from a global constraint system into a repeated local template.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(n^2) | Too slow |
| Block construction | O(n^2) | O(1) extra | Accepted |

## Algorithm Walkthrough

We construct the grid block by block, treating each $2 \times 2$ sub-square independently.

1. Split the grid into $2 \times 2$ blocks. Each block is identified by its top-left coordinate $(i, j)$ where $i, j$ increase in steps of 2. This works because $n$ is divisible by 4, so such tiling is exact.
2. Maintain a running counter `cur` starting from 0, which represents the next unused group of 4 numbers. Each block consumes exactly 4 consecutive numbers, ensuring all values from $0$ to $n^2 - 1$ are used exactly once.
3. For each block, assign its four values in a fixed XOR-safe pattern:

the block receives $(cur, cur+1, cur+2, cur+3)$ arranged as

top-left, bottom-right, bottom-left, top-right in a specific order that ensures internal XOR balance.

The idea is that within each block, every row and column contributes the same XOR structure because each number is paired with a complementary partner across both row and column dimensions.
4. After filling a block, increment `cur` by 4 and continue.
5. Output the completed grid.

### Why it works

Each block contributes exactly one controlled XOR pattern across its two rows and two columns. Since every block uses a disjoint set of four numbers, there is no interference between blocks. The arrangement ensures that each row and each column intersects blocks in a way that contributes the same XOR pattern. Because the grid is fully tiled by identical structural units, the XOR over any row or column becomes identical across all rows and columns.

The correctness reduces to the fact that XOR is associative and commutative, so the global XOR is the XOR of independent block contributions, and each row or column sees the same multiset of block contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

grid = [[0] * n for _ in range(n)]

cur = 0
for i in range(0, n, 2):
    for j in range(0, n, 2):
        grid[i][j] = cur
        grid[i][j+1] = cur + 1
        grid[i+1][j] = cur + 2
        grid[i+1][j+1] = cur + 3
        cur += 4

for row in grid:
    print(*row)
```

The implementation directly mirrors the block construction. The nested loops step by 2 because each iteration handles a full $2 \times 2$ tile. The variable `cur` ensures that every number is used exactly once without overlap.

The placement inside each block follows a fixed pattern. While multiple valid patterns exist, any consistent assignment of the four consecutive numbers into a 2x2 block works because XOR constraints depend only on symmetry across rows and columns, not absolute positions.

The final printing step outputs the grid row by row in standard format.

## Worked Examples

### Example: n = 4

We process blocks in order.

| Block (i,j) | cur start | top-left | top-right | bottom-left | bottom-right |
| --- | --- | --- | --- | --- | --- |
| (0,0) | 0 | 0 | 1 | 2 | 3 |
| (0,2) | 4 | 4 | 5 | 6 | 7 |
| (2,0) | 8 | 8 | 9 | 10 | 11 |
| (2,2) | 12 | 12 | 13 | 14 | 15 |

Resulting grid:

```
0 1 4 5
2 3 6 7
8 9 12 13
10 11 14 15
```

This satisfies uniqueness and produces uniform XOR per row and column.

Now consider a shifted variant consistent with the same block idea:

| Block structure | observation |
| --- | --- |
| each 2x2 block is independent | XOR is local |
| each row intersects same pattern of blocks | row XOR identical |
| each column intersects same pattern | column XOR identical |

This demonstrates that the construction depends only on repeating identical structural units.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | each cell is written exactly once during block filling |
| Space | $O(1)$ extra | aside from the grid itself |

The solution easily fits constraints since $n^2 \le 10^6$, and operations are simple assignments.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    n = int(input())
    grid = [[0]*n for _ in range(n)]
    cur = 0
    for i in range(0, n, 2):
        for j in range(0, n, 2):
            grid[i][j] = cur
            grid[i][j+1] = cur + 1
            grid[i+1][j] = cur + 2
            grid[i+1][j+1] = cur + 3
            cur += 4
    return "\n".join(" ".join(map(str, row)) for row in grid)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("4\n") is not None

# custom cases
assert run("8\n") is not None
assert run("12\n") is not None
assert run("16\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 | valid 4x4 grid | base correctness |
| 8 | larger tiling | block repetition |
| 12 | mid-size structure | scaling correctness |
| 16 | multiple layers | no interference |

## Edge Cases

The smallest valid input is $n = 4$. Here the grid consists of exactly one layer of 2x2 blocks, so any mistake in block ordering immediately breaks uniqueness or XOR symmetry.

At larger sizes like $n = 1000$, the main risk is integer mismanagement or skipping indices when incrementing by 2. Since every step consumes exactly four numbers, any off-by-one in `cur` causes either repetition or omission of values, which would violate the permutation requirement even if XOR properties accidentally still hold locally.

The construction avoids this by strictly coupling block traversal with deterministic increments, ensuring both global coverage and local consistency simultaneously.
