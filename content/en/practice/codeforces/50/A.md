---
title: "CF 50A - Domino piling"
description: "We are asked to place as many standard dominoes as possible on a rectangular board of size _M_ by _N_. Each domino covers exactly two adjacent squares, and dominoes cannot overlap or extend outside the board."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 50
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 47"
rating: 800
weight: 50
solve_time_s: 65
verified: true
draft: false
---
[CF 50A - Domino piling](https://codeforces.com/problemset/problem/50/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to place as many standard dominoes as possible on a rectangular board of size _M_ by _N_. Each domino covers exactly two adjacent squares, and dominoes cannot overlap or extend outside the board. The input gives us two integers, _M_ and _N_, representing the height and width of the board in squares. The output is a single integer: the maximum number of dominoes that can be placed under these rules. Dominoes can be rotated, so we can place them vertically or horizontally, whichever fits.

The constraints are very small: _M_ and _N_ are at most 16. This immediately rules out any concerns about large-scale computational complexity. Even the total number of squares on the board is at most 16 × 16 = 256, so any algorithm that processes each square a few times is fast enough. We do not need anything fancy like dynamic programming or backtracking for efficiency, although thinking about it geometrically is helpful.

A few edge cases are subtle. If the board has only one row or one column, the maximum number of dominoes is simply the number of squares divided by two, rounding down. For example, a 1×5 board can only hold 2 dominoes because 5 divided by 2 is 2 with a remainder. Another edge case occurs when the total number of squares is odd. The last square will never be covered by a domino, so the maximal number is always the total area divided by 2, ignoring any remainder.

## Approaches

A brute-force approach would consider every possible way to place dominoes on the board. We could try every position and orientation recursively, marking squares as used, and counting the maximum configuration. This is correct in principle, but the number of configurations grows exponentially with the board area. Even with 256 squares, the number of subsets of squares is 2^256, which is astronomically huge. So while the brute-force works because it explores all valid placements, it fails due to combinatorial explosion.

The key observation that simplifies the problem is that each domino always covers exactly two squares. The total number of squares is _M_ × _N_. Each domino uses two squares, so the maximal number of dominoes we can ever place is simply the total number of squares divided by two. If the total is even, the board can be completely covered. If it is odd, one square will remain uncovered. This insight reduces the problem to a simple arithmetic calculation: floor division of the area by 2. This approach leverages the structure of dominoes and the uniformity of the board, rather than exploring individual placements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(M×N)) | O(M×N) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers _M_ and _N_ representing the board dimensions.
2. Compute the total number of squares on the board as _M_ × _N_. This represents the total space available for dominoes.
3. Divide the total number of squares by 2 using integer division. This accounts for the fact that each domino covers exactly two squares. If the total area is odd, the integer division automatically drops the remainder, leaving one square uncovered, which is correct.
4. Print the result.

Why it works: the invariant is that each domino always occupies exactly two squares and cannot overlap. The maximal packing of dominoes can never exceed half of the total squares, since each domino must use two. Any arrangement that covers more than floor(M×N/2) squares would violate the coverage constraint. The simplicity of the board (rectangular, no holes) guarantees that this division yields the maximum number of dominoes without having to consider specific placements.

## Python Solution

```python
import sys
input = sys.stdin.readline

m, n = map(int, input().split())
print((m * n) // 2)
```

This solution first reads the board dimensions, multiplies them to get the total number of squares, and then divides by two using integer division. We use integer division to automatically handle odd board sizes, ensuring the result is an integer. This is robust for all values within the input constraints, including the smallest (1×1) and largest (16×16) boards.

## Worked Examples

For a 2×4 board:

| m | n | m*n | (m*n)//2 |
| --- | --- | --- | --- |
| 2 | 4 | 8 | 4 |

The calculation confirms we can place 4 dominoes. This matches the sample output.

For a 3×3 board:

| m | n | m*n | (m*n)//2 |
| --- | --- | --- | --- |
| 3 | 3 | 9 | 4 |

The calculation shows that we can place 4 dominoes, leaving one square uncovered. This demonstrates correct handling of odd areas.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single multiplication and division are performed |
| Space | O(1) | Only a few integers are stored |

Given the constraints, this solution runs in constant time and uses minimal memory, far below the allowed limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    m, n = map(int, input().split())
    return str((m * n) // 2)

# Provided sample
assert run("2 4\n") == "4", "sample 1"

# Custom cases
assert run("1 1\n") == "0", "single square board"
assert run("1 5\n") == "2", "single row with odd length"
assert run("16 16\n") == "128", "largest even board"
assert run("3 3\n") == "4", "odd area 3x3 board"
assert run("2 3\n") == "3", "small rectangle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0 | Minimum-size board, cannot place any domino |
| 1 5 | 2 | Single row with odd number of squares |
| 16 16 | 128 | Maximum-size board, even area |
| 3 3 | 4 | Odd total squares, leaves one uncovered |
| 2 3 | 3 | General small rectangle, handles mixed dimensions |

## Edge Cases

For a 1×1 board, the algorithm computes 1_1=1, then 1//2=0. The output is correct since a single square cannot hold a domino. For a 1×5 board, 1_5=5, then 5//2=2. The output correctly leaves one square uncovered. For a 3×3 board, the algorithm computes 9//2=4, leaving one square free. In all cases, integer division ensures the correct maximal domino count without over-counting or missing edge conditions.
