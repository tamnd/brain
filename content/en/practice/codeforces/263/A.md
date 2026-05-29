---
title: "CF 263A - Beautiful Matrix"
description: "We are given a fixed 5 by 5 grid that contains mostly zeros and exactly one cell containing a one. In one move, we are allowed to swap adjacent rows or swap adjacent columns. Each such swap moves the entire row or column by exactly one position."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 263
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 161 (Div. 2)"
rating: 800
weight: 263
solve_time_s: 91
verified: false
draft: false
---

[CF 263A - Beautiful Matrix](https://codeforces.com/problemset/problem/263/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed 5 by 5 grid that contains mostly zeros and exactly one cell containing a one. In one move, we are allowed to swap adjacent rows or swap adjacent columns. Each such swap moves the entire row or column by exactly one position.

The goal is to move the single one into the center cell of the grid, which is at position (3, 3), using as few swaps as possible. Since each move only shifts a row or column by one step, the cost is purely determined by how far the one is from the center in grid distance terms, where we only move vertically via row swaps and horizontally via column swaps.

The constraints are trivial in size, since the grid is always 25 cells. This rules out any need for optimization techniques or data structures. Any solution that scans the grid once and computes a small arithmetic expression will run instantly.

A naive mistake comes from trying to simulate swaps literally. For example, if the one is at (1, 5), a simulation might repeatedly swap rows and columns until reaching the center. That works, but it is unnecessary and can easily introduce off-by-one mistakes or inefficient logic even though constraints are small.

Another subtle mistake is misunderstanding that row and column swaps are independent. Someone might incorrectly try to move diagonally in one step or count swaps incorrectly when mixing row and column operations in a single looped simulation.

## Approaches

The brute-force interpretation is to simulate moving the one step by step toward the center, repeatedly swapping either rows or columns until it reaches (3, 3). Each swap reduces either the row distance or column distance by exactly one. This is correct, but it overcomplicates the problem and risks incorrect bookkeeping if simulated explicitly.

The key observation is that swapping adjacent rows is exactly equivalent to moving the one up or down by one cell, and swapping adjacent columns is exactly equivalent to moving it left or right by one cell. Since these two dimensions do not interact, the total number of moves is simply the Manhattan distance from the current position of the one to the center.

So instead of simulating operations, we locate the position (r, c) of the one and compute how far it is from (3, 3). Each unit of vertical distance costs one row swap, and each unit of horizontal distance costs one column swap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation of swaps | O(k) | O(1) | Accepted but unnecessary |
| Manhattan distance formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to finding the coordinates of the single nonzero element and computing its distance to the center.

1. Scan the 5 by 5 matrix to locate the cell (r, c) where the value is 1. This is the only meaningful information in the grid.
2. Compute the vertical distance as |r - 3|. This counts how many adjacent row swaps are needed to bring the element to row 3.
3. Compute the horizontal distance as |c - 3|. This counts how many adjacent column swaps are needed to bring the element to column 3.
4. Add the two distances to obtain the total number of moves.

The separation into row and column contributions works because row swaps never affect columns and column swaps never affect rows, so the two dimensions evolve independently.

### Why it works

Every move changes exactly one coordinate of the position of the one by ±1, either row or column. No move affects both coordinates simultaneously. This means any path from (r, c) to (3, 3) in this operation graph must consist of exactly |r - 3| row moves and |c - 3| column moves in some order. Any deviation would either fail to reach the target or use extra moves that undo progress, so the Manhattan distance is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    r = c = -1
    
    for i in range(5):
        row = list(map(int, input().split()))
        for j in range(5):
            if row[j] == 1:
                r, c = i, j
    
    print(abs(r - 2) + abs(c - 2))

if __name__ == "__main__":
    solve()
```

The program scans the grid once and records the position of the single one. The indices are stored in zero-based form, so the center (3, 3) becomes (2, 2). The final answer is computed as the sum of absolute differences in both dimensions.

A common implementation detail is index convention. The problem statement uses 1-based indexing, but the code uses 0-based indexing, so the center shifts from (3, 3) to (2, 2). Mixing these conventions is the main source of off-by-one errors.

## Worked Examples

### Example 1

Input:

```
0 0 0 0 0
0 0 0 0 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

The position of 1 is (2, 4) in 0-based indexing.

| Step | Row | Col | |r - 2| | |c - 2| | Total |

|------|-----|-----|--------|--------|--------|--------|

| Start | 2 | 4 | 0 | 2 | 2 |

The row is already centered, but the column is two steps away, so two column swaps are required. This confirms that horizontal movement alone determines the cost here.

### Example 2

Input:

```
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

The position of 1 is (0, 0).

| Step | Row | Col | |r - 2| | |c - 2| | Total |

|------|-----|-----|--------|--------|--------|--------|

| Start | 0 | 0 | 2 | 2 | 4 |

Here both row and column are far from the center, and both contributions add up independently. This shows the independence of the two axes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The grid size is constant (25 cells), so scanning is bounded |
| Space | O(1) | Only a few integer variables are stored |

The solution trivially satisfies the constraints since the input size never grows beyond a fixed 5 by 5 matrix.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    grid = []
    r = c = -1
    
    for i in range(5):
        row = list(map(int, input().split()))
        for j in range(5):
            if row[j] == 1:
                r, c = i, j
    
    return str(abs(r - 2) + abs(c - 2))

# provided sample
assert run("""0 0 0 0 0
0 0 0 0 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0""") == "3"

# center already
assert run("""0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 0 0 0
0 0 0 0 0""") == "0"

# top-left corner
assert run("""1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0""") == "4"

# bottom-right corner
assert run("""0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 1 0""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| center cell | 0 | no moves needed |
| top-left | 4 | maximum symmetric distance |
| bottom-right | 4 | opposite corner symmetry |

## Edge Cases

A potential edge case is when the one is already in the center. For example:

Input:

```
0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 0 0 0
0 0 0 0 0
```

The scan finds (2, 2). The computation gives |2 - 2| + |2 - 2| = 0. No moves are needed, and the algorithm naturally handles this without special cases.

Another edge case is when the one is in any corner. The algorithm treats all corners uniformly through Manhattan distance. For (0, 0), it computes 2 + 2 = 4, matching the fact that two row swaps and two column swaps are necessary, and no sequence can do better because each move only changes one coordinate by one step.
