---
title: "CF 1A - Theatre Square"
description: "We are given a rectangular plaza with dimensions n×m meters, to be paved with a×a square flagstones. Find the minimum number of flagstones needed."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 1"
rating: 1000
weight: 1
solve_time_s: 241
verified: true
draft: false
---
## Problem Understanding

We are given a rectangular plaza, the Theatre Square, with dimensions _n_ meters in length and _m_ meters in width. The city wants to pave the entire area with square flagstones of side _a_. The question asks for the minimum number of flagstones required to cover the square completely. Each flagstone must be placed aligned with the sides of the square; we cannot cut them, but it is acceptable for flagstones to extend beyond the edges of the square.

The input numbers can be very large, up to 10^9. This tells us that any approach that iterates over each meter of the square or each possible tile placement is infeasible. We need a constant-time, arithmetic-based solution.

Non-obvious edge cases include situations where the square's dimensions are not divisible by the tile size. For example, if the square is 6×6 meters and the flagstone is 4×4 meters, a naive integer division might suggest 1 flagstone per dimension (6 // 4 = 1), giving a total of 1. This is clearly wrong because a single 4×4 flagstone cannot cover 6 meters. The correct approach must round up the division to account for any remainder.

Another subtle case is when _n_ or _m_ is exactly divisible by _a_, which should not add an extra flagstone. For instance, a 12×8 square with 4×4 tiles should use exactly 6 tiles (3 along the length, 2 along the width), not more.

## Approaches

A brute-force approach would attempt to simulate placing each tile, counting how many fit along the length and width, and adding extra tiles for leftover space. Conceptually, we could imagine a nested loop iterating over each tile's top-left corner. While correct, the number of operations in the worst case could reach 10^18 for maximum inputs (n = m = 10^9, a = 1), which is entirely unworkable.

The key insight is that we do not need to simulate anything. Each dimension can be handled independently. Along one dimension, the number of tiles required is the ceiling of the division of the square's length by the tile size. Mathematically, this is `ceil(n / a)`. Doing this for both dimensions and multiplying the results gives the total number of tiles. The rounding up ensures that even if a small remainder exists, we allocate an extra tile to cover it.

The ceiling operation can be computed without floating-point arithmetic using integer division: `(n + a - 1) // a`. This works because if `n` is not divisible by `a`, adding `a-1` ensures the quotient rounds up. If `n` is divisible by `a`, the addition does not change the quotient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m / a^2) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input values `n`, `m`, and `a`. These represent the length, width, and tile size.
2. Compute the number of tiles along the length using integer arithmetic: `tiles_along_length = (n + a - 1) // a`. Adding `a - 1` ensures rounding up if `n` is not divisible by `a`.
3. Compute the number of tiles along the width in the same manner: `tiles_along_width = (m + a - 1) // a`.
4. Multiply the two results to get the total number of tiles: `total_tiles = tiles_along_length * tiles_along_width`.
5. Print the result.

Why it works: Each dimension is independently covered using the minimal number of tiles to cover the full length. Multiplying ensures the two-dimensional coverage of the rectangular area. The rounding-up step guarantees no uncovered space even when `n` or `m` is not a multiple of `a`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, a = map(int, input().split())

tiles_along_length = (n + a - 1) // a
tiles_along_width = (m + a - 1) // a

total_tiles = tiles_along_length * tiles_along_width
print(total_tiles)
```

The code directly follows the algorithm. Reading input with `sys.stdin.readline` avoids I/O overhead for large inputs. The `(n + a - 1) // a` trick avoids floating-point division, preventing precision issues and overflow. Multiplying the two counts gives the correct total number of flagstones.

## Worked Examples

Sample Input 1:

```
6 6 4
```

| n | m | a | tiles_along_length | tiles_along_width | total_tiles |
| --- | --- | --- | --- | --- | --- |
| 6 | 6 | 4 | 2 | 2 | 4 |

This shows that even though 6 / 4 is 1.5, rounding up to 2 ensures full coverage.

Sample Input 2 (constructed):

```
12 8 4
```

| n | m | a | tiles_along_length | tiles_along_width | total_tiles |
| --- | --- | --- | --- | --- | --- |
| 12 | 8 | 4 | 3 | 2 | 6 |

This demonstrates a case where both dimensions are exactly divisible by `a`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations are performed; no loops. |
| Space | O(1) | Only a few integer variables are stored. |

Given the constraints up to 10^9, the solution easily runs within 1 second and 256 MB of memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, a = map(int, sys.stdin.readline().split())
    return str(((n + a - 1) // a) * ((m + a - 1) // a))

# Provided sample
assert run("6 6 4\n") == "4", "sample 1"

# Custom cases
assert run("12 8 4\n") == "6", "exact division"
assert run("1 1 1\n") == "1", "minimum-size input"
assert run("1000000000 1000000000 1\n") == "1000000000000000000", "maximum-size input"
assert run("5 5 3\n") == "4", "odd dimensions with remainder"
assert run("10 10 10\n") == "1", "tile exactly fits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 12 8 4 | 6 | Exact division, no rounding needed |
| 1 1 1 | 1 | Minimum-size input |
| 1000000000 1000000000 1 | 1000000000000000000 | Maximum input values, integer overflow safety |
| 5 5 3 | 4 | Remainder causes rounding up |
| 10 10 10 | 1 | Tile exactly covers dimension |

## Edge Cases

For the case `n = 5, m = 5, a = 3`, the calculation is `(5 + 3 - 1) // 3 = 7 // 3 = 2` tiles per dimension. Multiplying gives 4 tiles. Each dimension is fully covered despite the remainder of 2 meters. A naive integer division without rounding up would have returned 1×1 = 1 tile, which is clearly insufficient. This confirms the rounding logic correctly handles non-divisible dimensions.

For maximum values `n = m = 10^9, a = 1`, the calculation `(10^9 + 1 - 1) // 1 = 10^9` per dimension, giving `10^9 × 10^9 = 10^18` tiles. Python handles this large integer without overflow, validating the approach for extreme inputs.
