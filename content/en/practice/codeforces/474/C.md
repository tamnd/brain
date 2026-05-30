---
title: "CF 474C - Captain Marmot"
description: "We are asked to help Captain Marmot organize his regiments of moles so that each group of four forms a perfect square on a plane. Each mole starts at a position (xi, yi) and has a “home” at (ai, bi)."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry"]
categories: ["algorithms"]
codeforces_contest: 474
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 271 (Div. 2)"
rating: 2000
weight: 474
solve_time_s: 72
verified: true
draft: false
---

[CF 474C - Captain Marmot](https://codeforces.com/problemset/problem/474/C)

**Rating:** 2000  
**Tags:** brute force, geometry  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to help Captain Marmot organize his regiments of moles so that each group of four forms a perfect square on a plane. Each mole starts at a position `(xi, yi)` and has a “home” at `(ai, bi)`. The only allowed operation is to rotate a mole 90 degrees counter-clockwise around its home. Each rotation counts as one move, and the goal is to minimize the total moves needed to form a square for each regiment.

The input consists of `n` regiments, each with 4 moles, so in total we have `4*n` moles. The coordinates range from `-10^4` to `10^4`. Given `n` can be up to 100, we have at most 400 moles. The output is the minimal number of moves per regiment, or -1 if forming a square is impossible.

Edge cases include situations where all moles are at the same position, which cannot form a non-degenerate square, or where multiple rotations are required on the same mole. A naive approach that only checks one fixed rotation per mole could fail, because we need to explore all 0-3 rotations for each mole and find the combination that forms a square with minimal moves.

## Approaches

The brute-force method is straightforward: for each regiment, try all possible rotations (0, 90, 180, 270 degrees) for all four moles. Since each mole has 4 options, there are 4^4 = 256 combinations per regiment. For each combination, we check if the four resulting points form a square. This is feasible given the constraint n ≤ 100, as 256 * 100 = 25,600 checks in total.

The key insight for optimization is realizing that 256 combinations per regiment is small enough that no further pruning is strictly necessary. The main work is in efficiently checking if four points form a square. A square has equal side lengths and equal diagonals. Instead of computing angles or using floating point, we can use squared distances to avoid precision errors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 4^4) | O(1) | Accepted |
| Optimal | O(n * 4^4) | O(1) | Accepted |

The optimal approach is essentially the brute-force approach implemented carefully with integer arithmetic to check for squares.

## Algorithm Walkthrough

1. Read the number of regiments `n`.
2. For each regiment, read the positions and home coordinates for the four moles.
3. For each mole, precompute its four possible positions after 0, 1, 2, or 3 rotations around its home. The rotation formula is `(x, y)` rotated around `(a, b)` 90 degrees counter-clockwise: `(a - (y-b), b + (x-a))`.
4. Generate all 4^4 = 256 combinations of rotations, one per mole. Track the total moves for each combination (sum of the rotations used).
5. For each combination, check if the resulting four points form a non-degenerate square:

- Compute all pairwise squared distances. There should be exactly two unique distances: the smaller is a side, the larger is a diagonal.
- Ensure the diagonal distance occurs exactly twice, the side distance occurs exactly four times, and side distance > 0.
6. Track the minimal total moves over all valid square combinations. If no valid combination exists, output -1 for that regiment.
7. Print the results for all regiments.

Why it works: By generating all possible rotations and checking each combination, we guarantee that if a square configuration is possible, we will find it. Using squared distances ensures correctness without floating-point errors.

## Python Solution

```python
import sys
input = sys.stdin.readline
from itertools import product
from collections import Counter

def rotate_90(x, y, a, b):
    # rotate (x, y) 90 degrees CCW around (a, b)
    return a - (y - b), b + (x - a)

def is_square(points):
    dists = []
    for i in range(4):
        for j in range(i+1, 4):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dists.append(dx*dx + dy*dy)
    count = Counter(dists)
    if len(count) != 2:
        return False
    side, diag = sorted(count.keys())
    return count[side] == 4 and count[diag] == 2 and side > 0

n = int(input())
results = []
for _ in range(n):
    moles = [tuple(map(int, input().split())) for _ in range(4)]
    rotations = []
    for x, y, a, b in moles:
        r = [(x, y)]
        for _ in range(3):
            x, y = rotate_90(x, y, a, b)
            r.append((x, y))
        rotations.append(r)
    min_moves = float('inf')
    for choice in product(range(4), repeat=4):
        points = [rotations[i][choice[i]] for i in range(4)]
        moves = sum(choice)
        if is_square(points):
            min_moves = min(min_moves, moves)
    results.append(-1 if min_moves == float('inf') else min_moves)

for res in results:
    print(res)
```

This code first computes all possible positions for each mole, then iterates over all rotation combinations using `itertools.product`. The `is_square` function ensures we correctly identify squares without precision errors by working with squared distances. Minimal moves are tracked for each regiment, and -1 is returned if no configuration works.

## Worked Examples

For the first sample input, the rotations for the first regiment produce possible positions:

| Mole | 0° | 90° | 180° | 270° |
| --- | --- | --- | --- | --- |
| 1 | (1,1) | (-1,1) | (-1,-1) | (1,-1) |
| 2 | (-1,1) | (-1,-1) | (1,-1) | (1,1) |
| 3 | (-1,1) | (-1,-1) | (1,-1) | (1,1) |
| 4 | (1,-1) | (1,1) | (-1,1) | (-1,-1) |

Trying the combination `(0,1,0,0)` yields points `(1,1)`, `(-1,-1)`, `(-1,1)`, `(1,-1)`, which forms a square. The sum of moves is 1. No combination yields fewer moves.

For the second regiment, no combination of rotations produces four points forming a square. All attempts yield collinear points or zero-area configurations, so the output is -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 4^4) | For each regiment, 4 moles with 4 rotation choices → 256 combinations; n ≤ 100, so 256*100 = 25,600 checks. Checking distances takes O(6) per combination. |
| Space | O(4*4) per regiment | Store 4 positions per mole for 4 rotations; constant extra memory. |

Given the low total number of operations (~25k) and small data structures, this fits comfortably in the 1-second time limit.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    from itertools import product
    from collections import Counter

    def rotate_90(x, y, a, b):
        return a - (y - b), b + (x - a)

    def is_square(points):
        dists = []
        for i in range(4):
            for j in range(i+1, 4):
                dx = points[i][0] - points[j][0]
                dy = points[i][1] - points[j][1]
                dists.append(dx*dx + dy*dy)
        count = Counter(dists)
        if len(count) != 2:
            return False
        side, diag = sorted(count.keys())
        return count[side] == 4 and count[diag] == 2 and side > 0

    n = int(input())
    results = []
    for _ in range(n):
        moles = [tuple(map(int, input().split())) for _ in range(4)]
        rotations = []
        for x, y, a, b in moles:
            r = [(x, y)]
            for _ in range(3):
                x, y = rotate_90(x, y, a, b)
                r.append((x, y))
            rotations.append(r)
        min_moves = float('inf')
        for choice in product(range(4), repeat=4):
            points = [rotations[i][choice[i]] for i in range(4)]
            moves = sum(choice)
            if is_square(points):
                min_moves = min(min_moves, moves)
        results.append(-1 if min_moves == float('inf') else min_moves)

    return "\n".join(map(str, results))

# Provided sample
assert run("""4
1 1 0 0
-1 1 0 0
-1 1 0
```
