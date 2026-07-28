---
title: "CF 102740C - Isabelle's Redecorating"
description: "The room is a rectangle of unit squares with dimensions N by M. Isabelle wants to cover every square using identical L-shaped tiles."
date: "2026-07-29T00:57:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102740
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 9-25-20 Div. 2"
rating: 0
weight: 102740
solve_time_s: 48
verified: true
draft: false
---

[CF 102740C - Isabelle's Redecorating](https://codeforces.com/problemset/problem/102740/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The room is a rectangle of unit squares with dimensions `N` by `M`. Isabelle wants to cover every square using identical L-shaped tiles. The tile is a tetromino made of four squares: three consecutive squares in a line and one additional square attached to one of the ends, like an L-shaped Tetris piece. The tile may be rotated and reflected.

The task is only to decide whether a complete tiling exists. The output is `YES` if every floor square can be covered exactly once, and `NO` otherwise.

The dimensions can be as large as 1000, so a solution that tries to construct a board or search through placements is unnecessary and would be the wrong direction. The input size suggests that the answer must come from a mathematical property of the rectangle rather than simulation.

A common mistake is checking only whether the area is divisible by the tile size. Every tile covers four squares, so the area must be a multiple of four, but that condition is not enough. For example, a `2 x 2` room has area `4`, yet a single L-shaped tetromino cannot fill it because the tile always has a missing corner.

Another edge case is a one-row or one-column room. For example:

```
Input:
1 8

Output:
NO
```

The area is divisible by four, but every tile needs two rows or two columns after rotation, so a straight strip cannot be covered.

A second important case is when both dimensions are greater than one but the area is not divisible by eight:

```
Input:
3 4

Output:
NO
```

The area is `12`, which is divisible by four, but an L-tetromino coloring argument shows that the number of tiles must be even, so the total area must actually be divisible by eight.

## Approaches

The brute-force approach would try every possible placement of every L-shaped tile and use backtracking to determine whether the rectangle can be completely covered. This is correct because it explores every possible tiling, but the number of placements grows rapidly. Even a small rectangle has many possible tile orientations and positions, and the search space becomes exponential. With dimensions up to 1000, this approach is impossible.

The useful observation is that the rectangle dimensions contain all the information we need. Every L-tetromino covers four squares, but it also has a color imbalance when the board is colored in alternating horizontal stripes. If we color every other row black and the remaining rows white, an L-tetromino always covers either three black squares and one white square, or three white squares and one black square. For the entire rectangle to be covered, the number of tiles with each imbalance must be equal, which means the number of tiles must be even. Since every tile covers four squares, the rectangle area must be divisible by eight.

This condition is also sufficient. Any rectangle with both sides greater than one and area divisible by eight can be split into smaller rectangles that can be tiled with L-tetrominoes. The smallest useful building blocks are rectangles such as `2 x 4` and `3 x 8`, and larger valid rectangles can be decomposed into these patterns.

The brute-force works because it directly searches for a placement arrangement, but fails because the number of arrangements is enormous. The coloring invariant reduces the entire problem to checking a few arithmetic conditions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Mathematical condition | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two dimensions of the room.
2. Check whether either dimension is `1`. A single row or column cannot contain an L-shaped tetromino, so the answer is immediately `NO`.
3. Compute the area `N * M`. If it is not divisible by `8`, the rectangle cannot be tiled because the number of tiles must be even.
4. If both conditions pass, output `YES`.

Why it works: the algorithm relies on the invariant that every valid tiling uses an even number of L-tetrominoes. Since each tile contributes four cells, every valid rectangle must have area divisible by eight. The remaining dimensions condition removes impossible thin rectangles where the tile cannot physically fit.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    if n == 1 or m == 1:
        print("NO")
    elif (n * m) % 8 != 0:
        print("NO")
    else:
        print("YES")

if __name__ == "__main__":
    solve()
```

The program first handles the geometric boundary case where one side is one. This check is separate because the area condition alone would incorrectly accept examples like `1 x 8`.

The multiplication `n * m` is safe in Python because integers have arbitrary precision. The final condition checks the divisibility requirement derived from the coloring argument.

There are no loops or stored structures because the answer depends only on the two input dimensions.

## Worked Examples

For the first example:

```
Input:
6 4
```

| Step | n | m | Condition | Result |
| --- | --- | --- | --- | --- |
| 1 | 6 | 4 | Both dimensions are greater than 1 | Continue |
| 2 | 6 | 4 | Area = 24, divisible by 8 | YES |

The rectangle has enough space for the required L-tetromino pattern, and the area satisfies the necessary invariant.

For the second example:

```
Input:
9 6
```

| Step | n | m | Condition | Result |
| --- | --- | --- | --- | --- |
| 1 | 9 | 6 | Both dimensions are greater than 1 | Continue |
| 2 | 9 | 6 | Area = 54, not divisible by 8 | NO |

Although the room is large enough physically, the coloring invariant prevents a complete tiling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic checks are performed. |
| Space | O(1) | No additional data structures are used. |

The constraints allow dimensions up to 1000, and this constant-time solution easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

def solve():
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())

    if n == 1 or m == 1:
        print("NO")
    elif (n * m) % 8 != 0:
        print("NO")
    else:
        print("YES")

assert run("6 4\n") == "YES\n", "sample 1"
assert run("9 6\n") == "NO\n", "sample 2"

assert run("1 8\n") == "NO\n", "single row cannot fit"
assert run("2 4\n") == "YES\n", "smallest valid rectangle"
assert run("3 4\n") == "NO\n", "area divisible by 4 but not 8"
assert run("1000 1000\n") == "YES\n", "large valid rectangle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 8` | `NO` | Checks the one-dimensional boundary case. |
| `2 4` | `YES` | Checks the smallest basic tiling block. |
| `3 4` | `NO` | Catches solutions that only check divisibility by four. |
| `1000 1000` | `YES` | Confirms the arithmetic solution handles maximum dimensions. |

## Edge Cases

For a `1 x 8` room, the algorithm first checks the dimensions and returns `NO`. Even though eight cells could be divided into two groups of four, the tile cannot be placed because it needs a second row after any rotation.

For a `3 x 4` room, the algorithm computes an area of `12`. The area is large enough for three tiles by count, but three tiles would violate the even-number-of-tiles invariant. The divisibility-by-eight check catches this and returns `NO`.

For a `2 x 4` room, the area is `8`, and both dimensions are greater than one. The algorithm returns `YES`, matching the fact that this rectangle can be split into two L-shaped tetromino placements.

For a `1000 x 1000` room, the dimensions are valid but the area is `1,000,000`, which is not divisible by eight. The algorithm still finishes immediately and correctly returns `NO`.
