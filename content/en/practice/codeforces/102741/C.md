---
title: "CF 102741C - Isabelle's Redecorating"
description: "The room is an N × M grid of square floor cells. Isabelle wants to replace the whole grid with identical L-shaped tiles. Each tile covers four cells: three cells in a straight line and one extra cell attached to one end, and the tile can be rotated."
date: "2026-07-29T00:43:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102741
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 9-25-20 Div. 1"
rating: 0
weight: 102741
solve_time_s: 63
verified: true
draft: false
---

[CF 102741C - Isabelle's Redecorating](https://codeforces.com/problemset/problem/102741/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The room is an `N × M` grid of square floor cells. Isabelle wants to replace the whole grid with identical L-shaped tiles. Each tile covers four cells: three cells in a straight line and one extra cell attached to one end, and the tile can be rotated. The task is to decide whether some arrangement of these tiles can cover the entire rectangle without gaps or overlaps.

A tile always covers exactly four cells, so the first restriction comes from area. The rectangle area must be divisible by four. However, this condition alone is not enough. L-tetrominoes have a stronger parity restriction: every valid rectangle also needs its area divisible by eight, and rectangles with a side of length one cannot be covered because every tile occupies at least two rows and two columns.

The input values are at most 1000, which means a solution should be based on a mathematical observation rather than simulating placements. A grid with up to one million cells is already too large for searching possible tile arrangements. A backtracking solution would branch on many possible tile positions and quickly become infeasible.

The tricky cases are the ones where area divisibility looks sufficient but the geometry rejects the rectangle.

For example, a room with dimensions `1 8` has area eight, but the answer is `NO`. A careless solution checking only `N*M % 8 == 0` would accept it, even though a single row cannot contain an L-shaped tile.

Another example is `2 2`. The area is four, but the answer is `NO`. The rectangle is too small to contain even one L-tetromino.

A case that passes the conditions is `2 4`. The area is eight and both dimensions are greater than one, so the answer is `YES`. Two L-shaped tiles can be arranged to fill the rectangle.

## Approaches

The direct approach is to try placing tiles on the floor one by one. A brute-force search can choose an uncovered cell, try every possible rotation of an L-shaped tile covering that cell, and continue recursively. This is correct because it explores every possible tiling. The problem is that the number of possible arrangements grows exponentially. Even for a moderately sized rectangle, the search tree becomes enormous because many different tile orders represent the same final arrangement.

The useful observation is that the exact placement does not need to be constructed. We only need to recognize when a rectangle has a valid tiling. An L-tetromino covers four cells, but a column coloring argument gives a stronger condition: a valid tiling always uses an even number of tiles, which means the total area must be divisible by eight. This removes many rectangles immediately.

The remaining question is whether this condition is also sufficient. If both dimensions are greater than one and the area is divisible by eight, the rectangle can always be split into smaller rectangles that can be tiled. When one side is even, the rectangle can be divided into `2 × 4` blocks, and each such block can be filled by two L-tetrominoes. When one side is odd, the area condition forces the other side to be a multiple of eight, allowing the rectangle to be partitioned into `3 × 8` blocks and `2 × 4` blocks. Both block types have valid L-tetromino tilings.

The entire problem reduces to checking two conditions: the room must have no dimension equal to one, and its area must be divisible by eight.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(NM) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two room dimensions `N` and `M`.
2. Check whether either dimension is equal to one. If it is, output `NO` because an L-tetromino cannot fit inside a single row or column.
3. Compute `N * M` and check whether it is divisible by eight. The divisibility condition captures the tile-count restriction created by the shape of the L-tetromino.
4. Output `YES` if both conditions are satisfied. Otherwise, output `NO`.

Why it works: Every valid tiling must satisfy the area restriction and the dimension restriction, so rejecting rectangles that fail either condition is safe. For every rectangle that satisfies both conditions, the rectangle can be decomposed into smaller regions that are individually tileable by L-tetrominoes. The conditions are both necessary and sufficient, so the algorithm always returns the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

if n == 1 or m == 1:
    print("NO")
elif (n * m) % 8 == 0:
    print("YES")
else:
    print("NO")
```

The code reads the two dimensions and immediately applies the two mathematical checks from the algorithm. The first condition handles thin rooms, where no placement is possible. The second condition uses the area restriction.

The multiplication `n * m` is safe in Python because integers have arbitrary precision, although even a fixed-width 32-bit integer would be enough for the given limits because the maximum area is only one million.

There are no loops, so there are no boundary traversal issues or off-by-one errors. The only possible mistake is forgetting the dimension-one case and accepting rectangles whose area happens to be divisible by eight.

## Worked Examples

### Sample 1

Input:

```
6 4
```

The algorithm checks the two conditions:

| Step | N | M | Area | Decision |
| --- | --- | --- | --- | --- |
| Initial | 6 | 4 | 24 | Both dimensions are greater than one |
| Area check | 6 | 4 | 24 | 24 is divisible by 8 |
| Final | 6 | 4 | 24 | YES |

The rectangle has enough area and dimensions to be split into valid tileable sections.

### Sample 2

Input:

```
9 6
```

| Step | N | M | Area | Decision |
| --- | --- | --- | --- | --- |
| Initial | 9 | 6 | 54 | Both dimensions are greater than one |
| Area check | 9 | 6 | 54 | 54 is not divisible by 8 |
| Final | 9 | 6 | 54 | NO |

The rectangle has the correct shape, but the number of cells cannot be divided into complete groups of L-tetromino coverage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs only a few arithmetic checks. |
| Space | O(1) | No additional data structures are created. |

The solution easily fits the constraints because it does not depend on the size of the grid. Even the largest possible room, `1000 × 1000`, is handled with constant work.

## Test Cases

```python
import sys
import io

def solve(data: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)
    n, m = map(int, sys.stdin.readline().split())

    if n == 1 or m == 1:
        ans = "NO"
    elif (n * m) % 8 == 0:
        ans = "YES"
    else:
        ans = "NO"

    sys.stdin = old_stdin
    return ans

# provided samples
assert solve("6 4\n") == "YES", "sample 1"
assert solve("9 6\n") == "NO", "sample 2"

# custom cases
assert solve("1 8\n") == "NO", "single row cannot fit L tiles"
assert solve("2 4\n") == "YES", "small valid rectangle"
assert solve("2 2\n") == "NO", "area is not enough"
assert solve("1000 1000\n") == "YES", "maximum size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 8` | `NO` | Rejects one-dimensional rooms |
| `2 4` | `YES` | Confirms the smallest common valid construction |
| `2 2` | `NO` | Catches solutions checking only area divisibility |
| `1000 1000` | `YES` | Confirms large inputs are handled in constant time |

## Edge Cases

For `1 8`, the algorithm first sees that one dimension is one and immediately returns `NO`. Although the area is divisible by eight, every L-tetromino needs space in two directions, so the rectangle cannot be covered.

For `2 2`, the area is only four. The algorithm rejects it because four is not divisible by eight. A solution based only on the fact that each tile covers four cells would incorrectly accept this case.

For `2 4`, the algorithm checks that both dimensions are greater than one and that the area is eight. It returns `YES`. This is a valid base construction where two L-tetrominoes exactly cover the rectangle.

For `9 6`, the algorithm reaches the area check after passing the dimension check. The area is `54`, and `54 % 8` is not zero, so it returns `NO`. The rectangle is large enough geometrically, but the number of cells cannot be partitioned into valid L-tile groups.
