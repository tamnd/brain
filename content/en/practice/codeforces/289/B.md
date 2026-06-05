---
title: "CF 289B - Polo the Penguin and Matrix"
description: "We are given a rectangular grid of integers, and we are allowed to perform a very specific operation: pick a single cell and add or subtract a fixed value d to it. Each such operation costs one move."
date: "2026-06-05T10:32:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation", "sortings", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 289
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 177 (Div. 2)"
rating: 1400
weight: 289
solve_time_s: 65
verified: true
draft: false
---

[CF 289B - Polo the Penguin and Matrix](https://codeforces.com/problemset/problem/289/B)

**Rating:** 1400  
**Tags:** brute force, dp, implementation, sortings, ternary search  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of integers, and we are allowed to perform a very specific operation: pick a single cell and add or subtract a fixed value `d` to it. Each such operation costs one move. The goal is to transform the entire grid so that every cell contains exactly the same number, using as few moves as possible, or determine that this is impossible.

The key observation from the start is that the operation does not let us change values arbitrarily. Every cell value can only move within its arithmetic progression modulo `d`. If a value starts at `x`, then after any number of operations it can only become numbers of the form `x + k·d`. This immediately implies a structural constraint: all cells must be congruent modulo `d`, otherwise no sequence of operations can ever align them.

The constraints are small: at most 100 by 100 grid, so up to 10,000 values. This allows an `O(nm log(nm))` approach comfortably, since sorting or scanning all values multiple times is cheap. Anything quadratic or cubic per cell is also fine here, but we do not need anything close to that.

A few edge cases are easy to miss.

If all numbers are not congruent modulo `d`, the answer is immediately impossible. For example, if `d = 2` and the grid contains both `1` and `2`, then `1` can only reach odd numbers, while `2` can only reach even numbers. No common target exists.

If all values are already equal, the answer is zero. This is trivial but should not be overlooked in implementation.

Another subtle case is when values are different but aligned modulo `d`, for example `[1, 5, 9]` with `d = 4`. These are all equivalent modulo 4, so a solution exists even though the values are far apart. A naive “make everything equal to average” intuition would fail here because averaging is irrelevant under constrained moves.

## Approaches

The brute-force idea is to try every possible final value and compute the cost of converting all elements to it. Since each operation changes a value by exactly `d`, any valid final value must lie in the same modulo class as all elements. So we could pick each candidate value from the grid as a potential target and compute the total number of steps required to convert every cell to that target.

For a chosen target `t`, each element `a[i][j]` contributes `|a[i][j] - t| / d` moves, assuming divisibility holds. We sum this across all cells. This gives correctness, since every conversion is independent.

However, there are up to 10,000 candidates and up to 10,000 cells, so this becomes about 100 million operations, which is still borderline but unnecessary. More importantly, we are repeating essentially the same computation for many equivalent candidates.

The key insight is that all values are in one arithmetic progression class modulo `d`, so we can normalize them. If we divide all values by `d` after shifting by a common remainder, the problem reduces to choosing a single integer target minimizing absolute deviation. That is a classic “minimize sum of absolute differences” problem, solved optimally by the median.

So we transform each value as `b[i] = a[i] // d` (after ensuring feasibility). The optimal target is the median of `b`, because the sum of absolute deviations is minimized at the median. Once the median is chosen, the answer is simply the total distance to it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over targets | O(n²m²) | O(1) | Too slow |
| Sort + median reduction | O(nm log(nm)) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Read the matrix and flatten all values into a single list. This simplifies reasoning because we no longer need row-column structure.
2. Check feasibility by ensuring all values share the same remainder modulo `d`. If even one value differs, we immediately return `-1` because no sequence of ±d operations can bridge different residue classes.
3. Normalize each value by dividing by `d`. This converts the problem into integer steps on a line, where each operation is ±1.
4. Sort the normalized values. Sorting is necessary because the optimal meeting point depends on order statistics, not arithmetic mean.
5. Choose the median value as the target. This works because moving all points to the median minimizes total absolute deviation in a 1D array.
6. Compute the total cost by summing absolute differences from the median.

### Why it works

Each move shifts a single cell by exactly one unit in the normalized space, so every cell evolves independently along a line. The total cost is the sum of distances to a chosen point. In one dimension, the function formed by absolute deviations is convex and piecewise linear, and its minimum always lies at a median. Since we have reduced the grid to independent 1D points under a shared constraint, no interaction between cells affects optimality, and selecting the median globally minimizes total moves.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, d = map(int, input().split())
    vals = []

    for _ in range(n):
        row = list(map(int, input().split()))
        vals.extend(row)

    # feasibility check: all must share same mod d
    r = vals[0] % d
    for v in vals:
        if v % d != r:
            print(-1)
            return

    # normalize
    vals = [v // d for v in vals]
    vals.sort()

    median = vals[len(vals) // 2]

    ans = 0
    for v in vals:
        ans += abs(v - median)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by flattening the matrix so that all reasoning can be done on a single array. The modulo check ensures we never attempt impossible transformations. The division by `d` reduces the operation space so that each move corresponds to a unit step, which is essential for the median argument to apply cleanly.

Sorting is the pivot step: without ordering, we cannot identify the median efficiently. The final loop computes total distance, which directly corresponds to the number of required ±1 steps in normalized space.

## Worked Examples

### Example 1

Input:

```
2 2 2
2 4
6 8
```

Flattened values: `[2, 4, 6, 8]`, `d = 2`

Normalized: `[1, 2, 3, 4]`

| Step | Array | Median | Cost |
| --- | --- | --- | --- |
| Normalize | [1, 2, 3, 4] | - | - |
| Sort | [1, 2, 3, 4] | - | - |
| Choose median | - | 3 | - |
| Compute cost | - | 3 | 2+1+0+1 = 4 |

Output is `4`.

This confirms that even distribution around the median yields minimal movement cost.

### Example 2

Input:

```
3 3 3
3 6 9
12 15 18
21 24 27
```

Flattened: `[3,6,9,12,15,18,21,24,27]`

Normalized by `d=3`: `[1,2,3,4,5,6,7,8,9]`

| Step | Array | Median | Cost |
| --- | --- | --- | --- |
| Normalize | [1..9] | - | - |
| Median | - | 5 | - |
| Sum distance | - | 5 | 20 |

This demonstrates symmetry: values equally spaced around the center produce minimal total movement when targeting the median.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm log(nm)) | dominated by sorting the flattened grid |
| Space | O(nm) | storing all values in a single array |

The constraints allow up to 10,000 values, so sorting and linear scanning are easily within limits. The algorithm avoids any nested recomputation over candidate targets, keeping runtime stable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline  # placeholder, replaced below

def solve():
    input = sys.stdin.readline
    n, m, d = map(int, input().split())
    vals = []
    for _ in range(n):
        vals.extend(map(int, input().split()))

    r = vals[0] % d
    for v in vals:
        if v % d != r:
            return "-1\n"

    vals = [v // d for v in vals]
    vals.sort()
    med = vals[len(vals)//2]

    return str(sum(abs(v - med) for v in vals)) + "\n"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("2 2 2\n2 4\n6 8\n") == "4\n"

# all equal
assert run("2 2 3\n9 9\n9 9\n") == "0\n"

# impossible case
assert run("2 2 2\n1 2\n3 4\n") == "-1\n"

# single element
assert run("1 1 10\n5\n") == "0\n"

# larger spread
assert run("1 5 2\n2 4 6 8 10\n") == "6\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2x2 equal mod consistent grid | 4 | basic correctness |
| all equal grid | 0 | trivial identity case |
| mixed parity grid | -1 | feasibility check |
| single cell | 0 | minimal edge case |
| evenly spaced row | 6 | median behavior |

## Edge Cases

A fully uniform grid such as `[[7,7],[7,7]]` demonstrates that the algorithm correctly short-circuits after normalization: all values match, median equals value, and the cost sum is zero.

A grid with incompatible residues such as `[[1,2],[3,4]]` when `d=2` triggers immediate rejection. The modulo check catches this before any sorting, avoiding unnecessary computation.

A single-cell grid shows that the median step degenerates cleanly: the only element is already the target, and the algorithm correctly returns zero without special casing beyond standard logic.
